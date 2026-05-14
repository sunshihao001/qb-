#!/usr/bin/env python3
"""SIKK Phase B-0.5 static dashboard site builder.

This builder is intentionally read-only with respect to trading/runtime data:
- reads existing live outputs under data/gmgn_candidates_live_run
- writes only static site files under the selected output directory
- never signs, swaps, broadcasts, or modifies paper-runner/state-machine outputs
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

DASHBOARD_BOUNDARY = "只读静态观察控制台；不执行真实 swap，不读取私钥，不自动 broadcast。"
STATE_LABELS = {
    "PAPER_OPEN": "纸面持仓中",
    "OPEN": "开放",
    "PAPER_READY": "纸面准备就绪",
    "READY_FOR_CONFIRMATION": "确认层就绪",
    "WALLET_SUPPORT": "钱包结构支持",
    "WALLET_PAUSE": "钱包结构暂停",
    "WALLET_BLOCK": "钱包结构阻断",
    "WALLET_NEUTRAL": "钱包结构中性",
    "WALLET_UNKNOWN": "钱包结构未知",
    "WATCHING": "观察中",
    "PAUSE": "暂停",
    "BLOCKED": "已阻断",
    "MISSING": "未接入",
    "ERROR": "错误",
    "UNKNOWN": "未知",
    "S3": "S3 观察信号",
    "S4": "S4 强信号",
    "SX": "SX 风险/排除信号",
    "NONE": "无",
    "ALLOW_CONFIRMATION_LAYER": "允许进入确认层",
    "ALLOW": "允许",
    "PASS": "通过",
    "OK": "正常",
    "PAUSE_NEED_CONFIRM": "暂停：需要确认",
    "BLOCK_BUY": "阻断买入",
    "HOLD": "继续持有/观察",
    "HOLD_WITH_DATA_RISK": "数据风险持有",
    "OPEN_PAPER_POSITION": "打开纸面仓位",
    "WAIT_SIGNAL": "等待信号",
    "WAIT_WALLET": "等待钱包结构",
    "WAIT_QUOTE": "等待报价",
    "WAIT_SECURITY": "等待安全扫描",
    "FIX_DATA_SOURCE": "修复数据源",
    "COOLING": "冷却观察",
    "IGNORE": "忽略",
    "WAIT_ACCUMULATION": "等待吸筹结构",
    "BLOCKED_BEFORE_WALLET": "上游阻断，未进钱包阶段",
    "NO_WALLET_INPUT": "缺少钱包结构输入",
    "HAS_WALLET_DECISION": "已有钱包结构结论",
    "wallet_structure_missing": "钱包结构未进入/缺失",
    "wallet_block": "钱包结构阻断",
    "signal_not_ready": "信号未就绪",
    "quote_not_ready": "报价未就绪",
    "security_not_ready": "安全扫描未就绪",
    "state_not_ready": "状态未就绪",
    "data_quality_low": "数据质量偏低",
    "paper_runner_not_called": "纸面执行器未触发",
    "candidates": "候选发现",
    "signal_ready": "信号就绪",
    "wallet_support": "钱包结构支持",
    "quote_security_pass": "报价/安全通过",
    "paper_ready": "纸面准备就绪",
    "paper_open": "纸面持仓中",
    "paper_entry_time_missing": "缺少纸面入场时间",
    "paper_entry_market_cap_missing": "缺少纸面入场市值",
    "P0_ACTIVE_POSITION": "P0 当前持仓",
    "P1_PAPER_READY": "P1 纸面就绪",
    "P2_STRUCTURE_SUPPORT": "P2 结构支持",
    "P3_WATCHING": "P3 观察中",
    "P4_PAUSE": "P4 暂停",
    "P5_BLOCKED": "P5 已阻断",
    "P6_DATA_MISSING": "P6 数据缺失",
    "P7_ERROR": "P7 错误",
}
PRIORITY_RANK = {
    "PAPER_OPEN": 0,
    "OPEN": 0,
    "PAPER_READY": 1,
    "WALLET_SUPPORT": 2,
    "WALLET_PAUSE": 3,
    "PAUSE": 3,
    "WATCHING": 4,
    "BLOCKED": 5,
    "WALLET_BLOCK": 5,
    "MISSING": 6,
    "ERROR": 7,
}
PRIORITY_LEVEL_BY_STATE = {
    "PAPER_OPEN": "P0_ACTIVE_POSITION",
    "PAPER_READY": "P1_PAPER_READY",
    "WALLET_SUPPORT": "P2_STRUCTURE_SUPPORT",
    "WATCHING": "P3_WATCHING",
    "PAUSE": "P4_PAUSE",
    "BLOCKED": "P5_BLOCKED",
    "MISSING": "P6_DATA_MISSING",
    "ERROR": "P7_ERROR",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_jsonl(path: Path, limit: int = 80) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
        except Exception:
            rows.append({"message": line})
    return rows


def as_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return []


def num(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except Exception:
        return default


def first_non_empty(*values: Any, default: str = "") -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text and text.lower() not in {"none", "null", "nan"}:
            return text
    return default


def nested_get(obj: Mapping[str, Any], *path: str, default: Any = None) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, Mapping):
            return default
        cur = cur.get(key)
    return cur if cur is not None else default


def load_token_statuses(base_dir: Path, live_state: Mapping[str, Any]) -> List[Dict[str, Any]]:
    by_token: Dict[str, Dict[str, Any]] = {}
    for row in as_list(live_state.get("tokens")):
        if isinstance(row, dict):
            token = first_non_empty(row.get("token_address"), row.get("代币地址"), row.get("address"))
            if token:
                by_token[token] = dict(row)
    token_dir = base_dir / "tokens"
    for path in sorted(token_dir.glob("*/token_status.json")):
        row = read_json(path, {})
        if isinstance(row, dict):
            token = first_non_empty(row.get("token_address"), row.get("代币地址"), path.parent.name)
            if token:
                merged = dict(row)
                if token in by_token:
                    # live_state is the latest board source; preserve fields not present there.
                    tmp = dict(row)
                    tmp.update(by_token[token])
                    merged = tmp
                by_token[token] = merged
    return list(by_token.values())


def load_wallet_decisions(base_dir: Path) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for path in sorted((base_dir / "wallet_structure").glob("*/wallet_structure_decision.json")):
        row = read_json(path, {})
        if not isinstance(row, dict):
            continue
        token = first_non_empty(row.get("token_address"), row.get("代币地址"), path.parent.name)
        if token:
            out[token] = row
    return out


def normalize_wallet_status(raw: Any) -> str:
    text = first_non_empty(raw, default="未接入")
    mapping = {
        "WALLET_SUPPORT": "WALLET_SUPPORT",
        "WALLET_BLOCK": "WALLET_BLOCK",
        "WALLET_PAUSE": "WALLET_PAUSE",
        "WALLET_NEUTRAL": "WALLET_NEUTRAL",
        "WALLET_UNKNOWN": "MISSING",
        "未接入": "MISSING",
        "MISSING": "MISSING",
    }
    return mapping.get(text, text)


def infer_wallet_missing_reason(current_state: str, signal_level: str, wallet_status: str) -> str:
    if wallet_status not in {"MISSING", "未接入", "WALLET_UNKNOWN", ""}:
        return "HAS_WALLET_DECISION"
    if current_state in {"PAPER_READY", "PAPER_OPEN"}:
        return "NO_WALLET_INPUT"
    if current_state == "BLOCKED":
        return "BLOCKED_BEFORE_WALLET"
    if signal_level in {"", "UNKNOWN", "S0", "S1_观察信号", "S2_预备信号"}:
        return "WAIT_SIGNAL"
    return "WAIT_ACCUMULATION"


def infer_priority_level(current_state: str, wallet_status: str, paper_status: str, existing: str) -> str:
    if existing:
        return existing
    if paper_status == "OPEN" or current_state == "PAPER_OPEN":
        return "P0_ACTIVE_POSITION"
    if current_state == "PAPER_READY":
        return "P1_PAPER_READY"
    if wallet_status == "WALLET_SUPPORT":
        return "P2_STRUCTURE_SUPPORT"
    if current_state == "PAUSE" or wallet_status == "WALLET_PAUSE":
        return "P4_PAUSE"
    if current_state == "WATCHING":
        return "P3_WATCHING"
    if current_state == "BLOCKED" or wallet_status == "WALLET_BLOCK":
        return "P5_BLOCKED"
    if wallet_status == "MISSING":
        return "P6_DATA_MISSING"
    if current_state == "ERROR":
        return "P7_ERROR"
    return PRIORITY_LEVEL_BY_STATE.get(current_state, "P3_WATCHING")


def infer_reason(row: Mapping[str, Any], wallet_status: str, missing_reason: str, quote_gate: str, security_gate: str, paper_status: str) -> str:
    current_state = first_non_empty(row.get("current_state"), row.get("当前状态"), default="UNKNOWN")
    if current_state == "BLOCKED":
        return first_non_empty(row.get("block_reason"), row.get("latest_reason"), row.get("状态原因"), default="状态机已阻断，等待冷却或复查")
    if wallet_status == "WALLET_BLOCK":
        return first_non_empty(nested_get(row, "wallet_structure", "reason"), nested_get(row, "wallet_structure", "钱包结构原因"), row.get("latest_reason"), default="钱包结构阻断")
    if wallet_status == "MISSING":
        reason_text = {
            "WAIT_SIGNAL": "未进入钱包结构阶段：等待 K线/信号确认",
            "WAIT_ACCUMULATION": "未进入钱包结构阶段：等待吸筹/结构证据",
            "BLOCKED_BEFORE_WALLET": "上游已阻断，未进入钱包结构阶段",
            "NO_WALLET_INPUT": "缺少钱包结构输出，需要复查 wallet_structure_decision.json",
        }.get(missing_reason, missing_reason)
        return reason_text
    if current_state == "WATCHING":
        return first_non_empty(row.get("watching_reason"), row.get("latest_reason"), default="观察中，等待下一轮信号确认")
    if quote_gate and quote_gate not in {"ALLOW", "ALLOW_CONFIRMATION_LAYER", "OK", "PASS", "MISSING"}:
        return first_non_empty(nested_get(row, "quote", "reason"), row.get("latest_reason"), default=f"报价未通过：{quote_gate}")
    if security_gate and security_gate not in {"ALLOW", "READY_FOR_CONFIRMATION", "OK", "PASS", "MISSING"}:
        return first_non_empty(nested_get(row, "security", "reason"), row.get("latest_reason"), default=f"安全扫描未通过：{security_gate}")
    if paper_status == "OPEN":
        return first_non_empty(nested_get(row, "paper", "reason"), row.get("latest_reason"), default="纸面持仓开放，继续监控")
    return first_non_empty(row.get("latest_reason"), row.get("状态原因"), default="等待下一轮信号确认")


def infer_next_action(current_state: str, wallet_status: str, quote_gate: str, security_gate: str, paper_status: str) -> str:
    if paper_status == "OPEN" or current_state == "PAPER_OPEN":
        return "HOLD"
    if current_state == "PAPER_READY":
        return "OPEN_PAPER_POSITION"
    if wallet_status == "WALLET_SUPPORT":
        return "WAIT_SIGNAL"
    if wallet_status == "MISSING":
        return "FIX_DATA_SOURCE"
    if wallet_status == "WALLET_BLOCK" or current_state == "BLOCKED":
        return "COOLING"
    if quote_gate and quote_gate not in {"ALLOW", "ALLOW_CONFIRMATION_LAYER", "OK", "PASS", "MISSING"}:
        return "WAIT_QUOTE"
    if security_gate and security_gate not in {"ALLOW", "READY_FOR_CONFIRMATION", "OK", "PASS", "MISSING"}:
        return "WAIT_SECURITY"
    if current_state == "PAUSE":
        return "WAIT_WALLET"
    if current_state == "ERROR":
        return "FIX_DATA_SOURCE"
    if current_state == "WATCHING":
        return "WAIT_SIGNAL"
    return "IGNORE"


def normalize_token(row: Mapping[str, Any], wallet_decisions: Mapping[str, Mapping[str, Any]]) -> Dict[str, Any]:
    token = first_non_empty(row.get("token_address"), row.get("代币地址"), row.get("address"))
    wallet = row.get("wallet_structure") if isinstance(row.get("wallet_structure"), dict) else {}
    signal = row.get("signal") if isinstance(row.get("signal"), dict) else {}
    quote = row.get("quote") if isinstance(row.get("quote"), dict) else {}
    security = row.get("security") if isinstance(row.get("security"), dict) else {}
    paper = row.get("paper") if isinstance(row.get("paper"), dict) else {}
    psychology = row.get("operator_psychology") if isinstance(row.get("operator_psychology"), dict) else {}
    decision = wallet_decisions.get(token, {}) if token else {}

    current_state = first_non_empty(row.get("current_state"), row.get("当前状态"), default="UNKNOWN")
    signal_level = first_non_empty(signal.get("signal_level"), row.get("signal_level"), row.get("信号等级"), default="UNKNOWN")
    wallet_status = normalize_wallet_status(first_non_empty(wallet.get("wallet_structure_status"), wallet.get("钱包结构结论"), decision.get("wallet_structure_status"), decision.get("钱包结构结论"), default="未接入"))
    quote_gate = first_non_empty(quote.get("quote_gate"), quote.get("final_permission"), row.get("quote_gate"), default="MISSING")
    security_gate = first_non_empty(security.get("security_gate"), security.get("final_state"), row.get("security_gate"), default="MISSING")
    paper_status = first_non_empty(paper.get("paper_status"), row.get("paper_status"), default="NONE")
    missing_reason = infer_wallet_missing_reason(current_state, signal_level, wallet_status)
    priority_level = infer_priority_level(current_state, wallet_status, paper_status, first_non_empty(row.get("priority_level"), default=""))
    main_reason = infer_reason(row, wallet_status, missing_reason, quote_gate, security_gate, paper_status)
    next_action = infer_next_action(current_state, wallet_status, quote_gate, security_gate, paper_status)

    market_ctx = row.get("market_cap_context") if isinstance(row.get("market_cap_context"), Mapping) else {}
    return {
        "token_symbol": first_non_empty(row.get("token_symbol"), row.get("代币符号"), default="UNKNOWN"),
        "token_address": token,
        "current_state": current_state,
        "priority_level": priority_level,
        "signal_level": signal_level,
        "signal_gate": first_non_empty(signal.get("signal_gate"), signal.get("risk_gate"), row.get("signal_gate"), default="UNKNOWN"),
        "discovery_market_cap_usd": first_non_empty(row.get("discovery_market_cap_usd"), market_ctx.get("discovery_market_cap_usd")),
        "signal_market_cap_usd": first_non_empty(row.get("signal_market_cap_usd"), market_ctx.get("signal_market_cap_usd")),
        "wallet_decision_market_cap_usd": first_non_empty(row.get("wallet_decision_market_cap_usd"), market_ctx.get("wallet_decision_market_cap_usd")),
        "paper_entry_market_cap_usd": first_non_empty(row.get("paper_entry_market_cap_usd"), market_ctx.get("paper_entry_market_cap_usd")),
        "current_market_cap_usd": first_non_empty(row.get("current_market_cap_usd"), market_ctx.get("current_market_cap_usd")),
        "market_cap_context_quality": first_non_empty(row.get("market_cap_context_quality"), market_ctx.get("market_cap_context_quality")),
        "operator_lifecycle_stage": first_non_empty(row.get("operator_lifecycle_stage"), psychology.get("operator_lifecycle_stage"), default="UNKNOWN"),
        "operator_psychology_label": first_non_empty(row.get("operator_psychology_label"), psychology.get("operator_psychology_label"), default="证据不足 / 待复查"),
        "operator_psychology": first_non_empty(psychology.get("operator_psychology"), row.get("operator_psychology"), default="DATA_INSUFFICIENT"),
        "paper_trade_alignment": first_non_empty(row.get("paper_trade_alignment"), psychology.get("paper_trade_alignment"), default="DATA_INSUFFICIENT"),
        "psychology_reason": first_non_empty(psychology.get("psychology_reason"), row.get("psychology_reason"), default="主导侧心理证据待补。"),
        "next_observation_focus": first_non_empty(psychology.get("next_observation_focus"), row.get("next_observation_focus"), default="复查生命周期、钱包结构、市值上下文与多轮快照。"),
        "wallet_structure_status": wallet_status,
        "wallet_missing_reason": missing_reason,
        "wallet_structure_score": num(first_non_empty(wallet.get("wallet_structure_score"), decision.get("wallet_structure_score"), decision.get("钱包结构评分"), default="0")),
        "wallet_risk_score": num(first_non_empty(wallet.get("wallet_risk_score"), decision.get("wallet_risk_score"), decision.get("钱包风险评分"), default="0")),
        "counterparty_pressure_score": num(first_non_empty(wallet.get("counterparty_pressure_score"), decision.get("counterparty_pressure_score"), decision.get("对手盘压力评分"), default="0")),
        "data_quality_score": num(first_non_empty(wallet.get("data_quality_score"), decision.get("data_quality_score"), decision.get("数据质量评分"), default="0")),
        "quote_gate": quote_gate,
        "security_gate": security_gate,
        "paper_status": paper_status,
        "paper_pnl_pct": num(first_non_empty(paper.get("unrealized_pnl_pct"), paper.get("paper_pnl_pct"), row.get("paper_pnl_pct"), default="0")),
        "main_reason": main_reason,
        "next_action": next_action,
        "last_update": first_non_empty(row.get("last_update"), row.get("更新时间"), default=""),
    }


def sort_tokens(tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def rank(t: Mapping[str, Any]) -> Any:
        state = first_non_empty(t.get("current_state"), default="UNKNOWN")
        wallet = first_non_empty(t.get("wallet_structure_status"), default="")
        status_rank = min(PRIORITY_RANK.get(state, 4), PRIORITY_RANK.get(wallet, 4))
        return (
            status_rank,
            -num(t.get("wallet_structure_score")),
            num(t.get("counterparty_pressure_score")),
            -num(t.get("data_quality_score")),
            -num(t.get("paper_pnl_pct")),
        )
    return sorted(tokens, key=rank)


def load_paper_rows_from_json(path: Path, *keys: str) -> List[Dict[str, Any]]:
    payload = read_json(path, {})
    if isinstance(payload, list):
        return [dict(row) for row in payload if isinstance(row, Mapping)]
    if isinstance(payload, Mapping):
        for key in keys:
            rows = payload.get(key)
            if isinstance(rows, list):
                return [dict(row) for row in rows if isinstance(row, Mapping)]
    return []


def _paper_token(row: Mapping[str, Any]) -> str:
    return first_non_empty(row.get("token_address"), row.get("代币地址"), row.get("token"), row.get("address"))


def build_market_cap_index(tokens: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in tokens:
        token = _paper_token(row)
        if not token:
            continue
        out[token] = {
            "discovery_market_cap_usd": row.get("discovery_market_cap_usd"),
            "signal_market_cap_usd": row.get("signal_market_cap_usd"),
            "wallet_decision_market_cap_usd": row.get("wallet_decision_market_cap_usd"),
            "paper_entry_market_cap_usd": row.get("paper_entry_market_cap_usd"),
            "current_market_cap_usd": row.get("current_market_cap_usd"),
            "exit_market_cap_usd": row.get("exit_market_cap_usd"),
            "market_cap_context_quality": row.get("market_cap_context_quality"),
        }
    return out


def load_case_file_index(paper_dir: Path) -> Dict[str, Dict[str, Any]]:
    manifest = read_json(paper_dir / "case_files" / "case_files_manifest.json", {})
    out: Dict[str, Dict[str, Any]] = {}
    rows = manifest.get("case_files") if isinstance(manifest, dict) else []
    for row in as_list(rows):
        if not isinstance(row, Mapping):
            continue
        position_id = first_non_empty(row.get("position_id"))
        token = first_non_empty(row.get("token_address"), row.get("代币地址"))
        item = {
            "case_file_json": row.get("case_file_json"),
            "case_file_md": row.get("case_file_md"),
            "case_quality_level": row.get("case_quality_level"),
            "case_completeness_score": row.get("case_completeness_score"),
            "evidence_missing_fields": row.get("evidence_missing_fields") or row.get("case_missing_fields") or [],
            "case_field_source_count": row.get("case_field_source_count") or row.get("field_source_count") or 0,
            "case_field_sources_preview": row.get("case_field_sources_preview") or [],
        }
        if position_id:
            out[f"position:{position_id}"] = item
        if token:
            out[f"token:{token}"] = item
    return out


def enrich_paper_position(row: Mapping[str, Any], market_caps: Mapping[str, Mapping[str, Any]], case_files: Optional[Mapping[str, Mapping[str, Any]]] = None) -> Dict[str, Any]:
    token = _paper_token(row)
    cap = market_caps.get(token, {}) if token else {}
    enriched = dict(row)
    entry_price = first_non_empty(row.get("entry_price"), row.get("模拟入场价"), row.get("live_entry_price"), row.get("signal_entry_price"))
    current_price = first_non_empty(row.get("current_price"), row.get("last_price"), row.get("当前价"))
    entry_time = first_non_empty(row.get("entry_time"), row.get("信号时间"), row.get("paper_entry_time"))
    position_sol = first_non_empty(row.get("position_sol"), row.get("模拟仓位SOL"), row.get("建议纸面仓位SOL"))
    entry_market_cap = first_non_empty(
        row.get("paper_entry_market_cap_usd"),
        row.get("entry_market_cap_usd"),
        row.get("入场市值USD"),
        cap.get("paper_entry_market_cap_usd"),
        row.get("signal_market_cap_usd"),
        cap.get("signal_market_cap_usd"),
    )
    current_market_cap = first_non_empty(row.get("current_market_cap_usd"), row.get("market_cap_usd"), cap.get("current_market_cap_usd"))
    signal_market_cap = first_non_empty(row.get("signal_market_cap_usd"), cap.get("signal_market_cap_usd"), entry_market_cap)
    discovery_market_cap = first_non_empty(row.get("discovery_market_cap_usd"), cap.get("discovery_market_cap_usd"), signal_market_cap, entry_market_cap)
    enriched.update({
        "token_address": token,
        "token_symbol": first_non_empty(row.get("token_symbol"), row.get("代币符号"), default="UNKNOWN"),
        "paper_entry_time": first_non_empty(row.get("paper_entry_time"), entry_time),
        "paper_position_sol": first_non_empty(row.get("paper_size_sol"), row.get("position_sol"), position_sol),
        "paper_entry_price": entry_price,
        "paper_current_price": current_price,
        "paper_stop_price": first_non_empty(row.get("stop_price"), row.get("止损价格")),
        "paper_remaining_pct": first_non_empty(row.get("remaining_pct"), row.get("剩余仓位_pct")),
        "paper_entry_market_cap_usd": entry_market_cap,
        "paper_discovery_market_cap_usd": discovery_market_cap,
        "paper_signal_market_cap_usd": signal_market_cap,
        "paper_current_market_cap_usd": current_market_cap,
        "paper_signal_time": first_non_empty(row.get("signal_time"), row.get("信号时间"), entry_time),
        "paper_signal_price": first_non_empty(row.get("signal_price"), row.get("信号价格"), row.get("signal_entry_price"), entry_price),
        "paper_last_update_time": first_non_empty(row.get("last_update_time"), row.get("更新时间")),
        "paper_pnl_pct": num(first_non_empty(row.get("当前收益率_pct"), row.get("live_pnl_pct"), row.get("signal_pnl_pct"), row.get("unrealized_pnl_pct"), row.get("final_pnl_pct"), row.get("最终收益率_pct"), default="0")),
        "paper_size_usd": first_non_empty(row.get("paper_size_usd"), row.get("size_usd")),
        "estimated_token_amount": first_non_empty(row.get("estimated_token_amount"), row.get("token_amount")),
        "entry_delay_from_discovery_sec": row.get("entry_delay_from_discovery_sec"),
        "entry_delay_from_signal_sec": row.get("entry_delay_from_signal_sec"),
        "entry_market_cap_change_from_discovery_pct": row.get("entry_market_cap_change_from_discovery_pct"),
        "entry_market_cap_change_from_signal_pct": row.get("entry_market_cap_change_from_signal_pct"),
        "market_cap_context_status": first_non_empty(row.get("market_cap_context_status"), default="UNKNOWN_ENTRY"),
        "wallet_exit_action": row.get("wallet_exit_action") or row.get("wallet_position_action"),
        "false_exit_flag": row.get("false_exit_flag"),
        "missed_profit_pct": row.get("missed_profit_pct"),
        "avoided_drawdown_pct": row.get("avoided_drawdown_pct"),
        "shadow_hold_tracking": row.get("shadow_hold_tracking"),
    })
    if case_files:
        position_id = first_non_empty(row.get("position_id"))
        case_item = case_files.get(f"position:{position_id}") or case_files.get(f"token:{token}") or {}
        if case_item:
            enriched.update(case_item)
            missing_fields = case_item.get("evidence_missing_fields") or case_item.get("case_missing_fields") or []
            enriched["case_quality_level"] = first_non_empty(case_item.get("case_quality_level"), enriched.get("case_quality_level"))
            enriched["case_completeness_score"] = case_item.get("case_completeness_score") if case_item.get("case_completeness_score") not in {None, ""} else enriched.get("case_completeness_score")
            enriched["case_missing_fields"] = missing_fields
            enriched["evidence_missing_fields"] = missing_fields
            enriched["case_field_source_count"] = int(num(case_item.get("case_field_source_count"), 0.0))
            enriched["case_field_sources_preview"] = case_item.get("case_field_sources_preview") or []
    return enriched




def _cap_bucket(value: Any) -> str:
    v = num(value, 0.0)
    if v <= 0:
        return "待补"
    if v < 50000:
        return "<50K"
    if v < 100000:
        return "50K-100K"
    if v < 200000:
        return "100K-200K"
    if v < 500000:
        return "200K-500K"
    if v < 1000000:
        return "500K-1M"
    return ">1M"


def build_entry_quality_summary(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    buckets: Dict[str, Dict[str, Any]] = {}
    delays: List[float] = []
    for row in rows:
        bucket = _cap_bucket(row.get("paper_entry_market_cap_usd"))
        item = buckets.setdefault(bucket, {"count": 0, "wins": 0, "pnl_sum": 0.0})
        pnl = num(row.get("paper_pnl_pct"), 0.0)
        item["count"] += 1
        item["pnl_sum"] += pnl
        if pnl > 0:
            item["wins"] += 1
        delay = row.get("entry_delay_from_discovery_sec")
        if delay not in {None, ""}:
            delays.append(num(delay, 0.0))
    for item in buckets.values():
        item["win_rate_pct"] = round(item["wins"] / item["count"] * 100, 4) if item["count"] else 0.0
        item["avg_pnl_pct"] = round(item["pnl_sum"] / item["count"], 4) if item["count"] else 0.0
    return {
        "title": "入场质量统计",
        "market_cap_buckets": buckets,
        "avg_entry_delay_from_discovery_sec": round(sum(delays) / len(delays), 2) if delays else None,
        "scope_note": "按入场市值分桶、发现到入场延迟、入场相对发现市值涨幅复盘纸面质量。",
    }


def build_wallet_exit_effectiveness(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    force_rows = [r for r in rows if first_non_empty(r.get("wallet_exit_action"), r.get("wallet_position_action")) == "FORCE_PAPER_EXIT"]
    false_rows = [r for r in force_rows if str(r.get("false_exit_flag")).lower() in {"true", "1", "yes"}]
    missed = [num(r.get("missed_profit_pct"), 0.0) for r in force_rows if r.get("missed_profit_pct") not in {None, ""}]
    avoided = [num(r.get("avoided_drawdown_pct"), 0.0) for r in force_rows if r.get("avoided_drawdown_pct") not in {None, ""}]
    return {
        "title": "钱包退出有效性 / 影子持仓复盘",
        "wallet_force_exit_count": len(force_rows),
        "false_positive_exit_count": len(false_rows),
        "false_exit_rate": round(len(false_rows) / len(force_rows) * 100, 4) if force_rows else 0.0,
        "avg_missed_profit_pct": round(sum(missed) / len(missed), 4) if missed else None,
        "avg_avoided_drawdown_pct": round(sum(avoided) / len(avoided), 4) if avoided else None,
        "shadow_hold_tracking": "force exit 后继续记录 shadow_hold_price_15m/30m/60m、missed_profit_pct、avoided_drawdown_pct。",
    }


def build_strategy_panel(rows: Iterable[Mapping[str, Any]], strategy_metrics: Mapping[str, Any]) -> Dict[str, Any]:
    def normalize_signal_tier(value: Any) -> str:
        text = first_non_empty(value, default="UNKNOWN")
        for tier in ("S3", "S4", "SX"):
            if text == tier or text.startswith(f"{tier}_") or text.startswith(f"{tier}-") or text.startswith(f"{tier} "):
                return tier
        return text

    rows = [dict(row) for row in rows]
    mode_counts = Counter(first_non_empty(row.get("entry_price_mode"), row.get("入场模式"), default="待补") for row in rows if first_non_empty(row.get("entry_price_mode"), row.get("入场模式"), default=""))
    live_pnls = [num(first_non_empty(row.get("live_pnl_pct"), row.get("当前收益率_pct"), default="0"), 0.0) for row in rows if first_non_empty(row.get("live_pnl_pct"), row.get("当前收益率_pct"), default="") != ""]
    signal_pnls = [num(first_non_empty(row.get("signal_pnl_pct"), row.get("signal_pnl"), default="0"), 0.0) for row in rows if first_non_empty(row.get("signal_pnl_pct"), row.get("signal_pnl"), default="") != ""]
    pnl_gap = []
    daily_groups: Dict[str, Dict[str, Any]] = {}
    signal_groups: Dict[str, Dict[str, Any]] = {}
    wallet_groups: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        live = first_non_empty(row.get("live_pnl_pct"), row.get("当前收益率_pct"), default="")
        signal = first_non_empty(row.get("signal_pnl_pct"), row.get("signal_pnl"), default="")
        live_val = num(live, 0.0) if live not in {""} else 0.0
        signal_val = num(signal, 0.0) if signal not in {""} else 0.0
        if live not in {""} and signal not in {""}:
            pnl_gap.append(live_val - signal_val)
        day = first_non_empty(row.get("paper_entry_time"), row.get("paper_last_update_time"), row.get("last_update_time"), row.get("entry_time"), default="")[:10]
        if day:
            bucket = daily_groups.setdefault(day, {
                "count": 0,
                "wins": 0,
                "live_pnl_sum": 0.0,
                "signal_pnl_sum": 0.0,
                "entry_price_mode_counts": Counter(),
                "failure_reason_top": Counter(),
            })
            bucket["count"] += 1
            bucket["live_pnl_sum"] += live_val
            bucket["signal_pnl_sum"] += signal_val
            if live_val > 0:
                bucket["wins"] += 1
            mode = first_non_empty(row.get("entry_price_mode"), row.get("入场模式"), default="待补")
            if mode:
                bucket["entry_price_mode_counts"][mode] += 1
            failure = first_non_empty(row.get("failure_type"), row.get("exit_reason"), default="")
            if failure:
                bucket["failure_reason_top"][failure] += 1
        signal_key = normalize_signal_tier(row.get("signal_level"))
        sig_bucket = signal_groups.setdefault(signal_key, {
            "count": 0,
            "wins": 0,
            "live_pnl_sum": 0.0,
            "signal_pnl_sum": 0.0,
        })
        sig_bucket["count"] += 1
        sig_bucket["live_pnl_sum"] += live_val
        sig_bucket["signal_pnl_sum"] += signal_val
        if live_val > 0:
            sig_bucket["wins"] += 1
        wallet_key = first_non_empty(row.get("wallet_structure_status"), default="MISSING")
        wal_bucket = wallet_groups.setdefault(wallet_key, {
            "count": 0,
            "wins": 0,
            "live_pnl_sum": 0.0,
            "signal_pnl_sum": 0.0,
        })
        wal_bucket["count"] += 1
        wal_bucket["live_pnl_sum"] += live_val
        wal_bucket["signal_pnl_sum"] += signal_val
        if live_val > 0:
            wal_bucket["wins"] += 1
    failure_counter = Counter(first_non_empty(row.get("failure_type"), row.get("exit_reason"), default="UNKNOWN") for row in rows if first_non_empty(row.get("failure_type"), row.get("exit_reason"), default=""))
    daily_groups_out: Dict[str, Dict[str, Any]] = {}
    for day, bucket in sorted(daily_groups.items()):
        daily_groups_out[day] = {
            "count": bucket["count"],
            "win_rate_pct": round(bucket["wins"] / bucket["count"] * 100, 4) if bucket["count"] else 0.0,
            "avg_live_pnl_pct": round(bucket["live_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
            "avg_signal_pnl_pct": round(bucket["signal_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
            "entry_price_mode_counts": dict(bucket["entry_price_mode_counts"]),
            "failure_reason_top": dict(bucket["failure_reason_top"]),
        }
    signal_groups_out: Dict[str, Dict[str, Any]] = {}
    total_rows = len(rows)
    for signal_key, bucket in sorted(signal_groups.items()):
        signal_groups_out[signal_key] = {
            "count": bucket["count"],
            "occurrence_pct": round(bucket["count"] / total_rows * 100, 4) if total_rows else 0.0,
            "win_rate_pct": round(bucket["wins"] / bucket["count"] * 100, 4) if bucket["count"] else 0.0,
            "avg_live_pnl_pct": round(bucket["live_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
            "avg_signal_pnl_pct": round(bucket["signal_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
        }
    wallet_groups_out: Dict[str, Dict[str, Any]] = {}
    for wallet_key, bucket in sorted(wallet_groups.items()):
        wallet_groups_out[wallet_key] = {
            "count": bucket["count"],
            "occurrence_pct": round(bucket["count"] / total_rows * 100, 4) if total_rows else 0.0,
            "win_rate_pct": round(bucket["wins"] / bucket["count"] * 100, 4) if bucket["count"] else 0.0,
            "avg_live_pnl_pct": round(bucket["live_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
            "avg_signal_pnl_pct": round(bucket["signal_pnl_sum"] / bucket["count"], 4) if bucket["count"] else None,
        }
    return {
        "title": "策略评估面板",
        "summary": strategy_metrics if isinstance(strategy_metrics, Mapping) else {},
        "entry_price_mode_counts": dict(mode_counts),
        "live_pnl_avg_pct": round(sum(live_pnls) / len(live_pnls), 4) if live_pnls else None,
        "signal_pnl_avg_pct": round(sum(signal_pnls) / len(signal_pnls), 4) if signal_pnls else None,
        "live_signal_pnl_gap_avg_pct": round(sum(pnl_gap) / len(pnl_gap), 4) if pnl_gap else None,
        "failure_reason_top": dict(failure_counter.most_common(10)),
        "daily_groups": daily_groups_out,
        "signal_groups": signal_groups_out,
        "wallet_groups": wallet_groups_out,
        "scope_note": "对纸面仓位同时保留 live / signal 两套收益指标，并汇总日报、胜率与失败原因。",
    }


def infer_case_quality(row: Mapping[str, Any]) -> Dict[str, Any]:
    existing_level = first_non_empty(row.get("case_quality_level"), row.get("case_quality"), default="")
    existing_score = row.get("case_completeness_score")
    existing_missing = row.get("evidence_missing_fields") or row.get("case_missing_fields")
    if existing_level or existing_score not in {None, ""} or existing_missing:
        missing_list = existing_missing if isinstance(existing_missing, list) else ([existing_missing] if first_non_empty(existing_missing) else [])
        score = num(existing_score, 0.0)
        if existing_level:
            if existing_level.startswith("E3"):
                quality = "HIGH"
            elif existing_level.startswith("E2"):
                quality = "MEDIUM"
            elif existing_level.startswith("E1"):
                quality = "LOW"
            else:
                quality = existing_level
        elif score >= 85:
            quality = "HIGH"
        elif score >= 60:
            quality = "MEDIUM"
        elif score > 0:
            quality = "LOW"
        else:
            quality = "INVALID"
        return {
            "case_quality": quality,
            "case_quality_level": existing_level,
            "case_completeness_score": score,
            "missing_fields": missing_list,
            "case_missing_fields": missing_list,
            "evidence_missing_fields": missing_list,
            "strategy_review_eligible": quality in {"HIGH", "MEDIUM"} and not missing_list,
        }
    required = {
        "发现时市值": first_non_empty(row.get("discovery_market_cap_usd"), row.get("paper_discovery_market_cap_usd")),
        "入场市值": first_non_empty(row.get("entry_market_cap_usd"), row.get("paper_entry_market_cap_usd")),
        "钱包结构": first_non_empty(row.get("wallet_structure_status")),
        "钱包结构分": first_non_empty(row.get("wallet_structure_score")),
        "对手盘压力": first_non_empty(row.get("counterparty_pressure_score")),
        "主导侧生命周期": first_non_empty(row.get("operator_lifecycle_stage"), row.get("dominant_side_lifecycle")),
        "实战档案": first_non_empty(row.get("case_file_md"), row.get("case_file_json")),
    }
    # 旧仓位（例如 LITH）可能早于 case-file 生成流程，只要能保留纸面入场/价格/信号，
    # 就必须标成 LOW + HOLD_WITH_DATA_RISK，而不是 INVALID 或误判为可复盘样本。
    required["实战档案"] = first_non_empty(row.get("case_file_md"), row.get("case_file_json"), default="LEGACY_CASE_PENDING")
    missing = [label for label, value in required.items() if not first_non_empty(value)]
    if not first_non_empty(row.get("paper_entry_time"), row.get("entry_time")) or not first_non_empty(row.get("paper_entry_price"), row.get("entry_price")):
        quality = "INVALID"
    elif not missing:
        quality = "HIGH"
    elif len(missing) <= 2:
        quality = "MEDIUM"
    else:
        quality = "LOW"
    return {"case_quality": quality, "missing_fields": missing, "strategy_review_eligible": quality in {"HIGH", "MEDIUM"}}


def infer_paper_action(row: Mapping[str, Any], quality: str) -> str:
    status = first_non_empty(row.get("status"), row.get("paper_status"), default="").upper()
    if status == "OPEN" and quality in {"LOW", "INVALID"}:
        return "HOLD_WITH_DATA_RISK"
    if status == "OPEN":
        return first_non_empty(row.get("wallet_exit_action"), row.get("wallet_position_action"), default="HOLD")
    return first_non_empty(row.get("paper_action"), row.get("exit_reason"), default="REVIEW_CLOSED")


def lifecycle_timeline_for_position(row: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return [
        {"stage": "发现", "time": first_non_empty(row.get("candidate_discovered_at"), row.get("discovered_at")), "status": first_non_empty(row.get("discovery_market_cap_usd"), row.get("paper_discovery_market_cap_usd"), default="市值待补")},
        {"stage": "信号", "time": first_non_empty(row.get("signal_time"), row.get("paper_signal_time")), "status": first_non_empty(row.get("signal_level"), default="UNKNOWN")},
        {"stage": "钱包结构", "time": first_non_empty(row.get("wallet_decision_time")), "status": first_non_empty(row.get("wallet_structure_status"), default="MISSING")},
        {"stage": "纸面入场", "time": first_non_empty(row.get("paper_entry_time"), row.get("entry_time")), "status": first_non_empty(row.get("paper_entry_price"), row.get("entry_price"), default="价格待补")},
        {"stage": "持仓监控", "time": first_non_empty(row.get("paper_last_update_time"), row.get("last_update_time")), "status": f"PnL {num(row.get('paper_pnl_pct'), 0.0):.4f}%"},
        {"stage": "复盘质量", "time": first_non_empty(row.get("case_file_md"), row.get("case_file_json")), "status": first_non_empty(row.get("case_quality"), default="LOW")},
    ]


def token_from_paper_position(row: Mapping[str, Any]) -> Dict[str, Any]:
    paper_action = first_non_empty(row.get("paper_action"), default="HOLD_WITH_DATA_RISK")
    return {
        "token_symbol": first_non_empty(row.get("token_symbol"), row.get("代币符号"), default="UNKNOWN"),
        "token_address": first_non_empty(row.get("token_address"), row.get("代币地址")),
        "current_state": "PAPER_OPEN" if first_non_empty(row.get("status"), row.get("paper_status"), default="OPEN").upper() == "OPEN" else "PAPER_CLOSED",
        "priority_level": "P0_ACTIVE_POSITION",
        "signal_level": first_non_empty(row.get("signal_level"), default="UNKNOWN"),
        "signal_gate": first_non_empty(row.get("signal_gate"), default="UNKNOWN"),
        "discovery_market_cap_usd": first_non_empty(row.get("paper_discovery_market_cap_usd"), row.get("discovery_market_cap_usd")),
        "signal_market_cap_usd": first_non_empty(row.get("paper_signal_market_cap_usd"), row.get("signal_market_cap_usd")),
        "paper_entry_market_cap_usd": first_non_empty(row.get("paper_entry_market_cap_usd"), row.get("entry_market_cap_usd")),
        "current_market_cap_usd": first_non_empty(row.get("paper_current_market_cap_usd"), row.get("current_market_cap_usd")),
        "market_cap_context_quality": first_non_empty(row.get("market_cap_context_status"), default="UNKNOWN_ENTRY"),
        "operator_lifecycle_stage": first_non_empty(row.get("operator_lifecycle_stage"), row.get("dominant_side_lifecycle"), default="UNKNOWN"),
        "operator_psychology_label": first_non_empty(row.get("operator_psychology_label"), default="证据不足 / 待复查"),
        "operator_psychology": first_non_empty(row.get("operator_psychology"), default="DATA_INSUFFICIENT"),
        "paper_trade_alignment": "DATA_RISK_HOLD",
        "psychology_reason": "纸面仓位存在，但钱包结构/市值路径/生命周期证据未补齐；只可作为记录型样本。",
        "next_observation_focus": "补齐发现/入场市值、钱包结构、对手盘压力、主导侧生命周期与 case file 互链。",
        "wallet_structure_status": first_non_empty(row.get("wallet_structure_status"), default="MISSING"),
        "wallet_missing_reason": "NO_WALLET_INPUT",
        "wallet_structure_score": num(row.get("wallet_structure_score"), 0.0),
        "wallet_risk_score": num(row.get("wallet_risk_score"), 0.0),
        "counterparty_pressure_score": num(row.get("counterparty_pressure_score"), 0.0),
        "data_quality_score": 0.0,
        "quote_gate": first_non_empty(row.get("quote_gate"), row.get("quote_security_state"), default="MISSING"),
        "security_gate": first_non_empty(row.get("security_gate"), row.get("quote_security_state"), default="MISSING"),
        "paper_status": first_non_empty(row.get("status"), row.get("paper_status"), default="OPEN"),
        "paper_pnl_pct": num(row.get("paper_pnl_pct"), 0.0),
        "main_reason": "纸面仓位存在，但当前 token_status 未覆盖；从统一索引 paper_live 聚合。",
        "next_action": paper_action,
        "paper_action": paper_action,
        "case_quality": first_non_empty(row.get("case_quality"), row.get("case_quality_level"), default="LOW"),
        "case_quality_level": first_non_empty(row.get("case_quality_level"), row.get("case_quality"), default="LOW"),
        "case_completeness_score": row.get("case_completeness_score"),
        "case_field_source_count": row.get("case_field_source_count"),
        "case_field_sources_preview": row.get("case_field_sources_preview") or [],
        "missing_fields": row.get("missing_fields") or row.get("case_missing_fields") or row.get("evidence_missing_fields") or [],
        "case_missing_fields": row.get("case_missing_fields") or row.get("evidence_missing_fields") or row.get("missing_fields") or [],
        "evidence_missing_fields": row.get("evidence_missing_fields") or row.get("case_missing_fields") or row.get("missing_fields") or [],
        "strategy_review_eligible": bool(row.get("strategy_review_eligible")),
        "lifecycle_timeline": row.get("lifecycle_timeline") or lifecycle_timeline_for_position(row),
        "last_update": first_non_empty(row.get("paper_last_update_time"), row.get("last_update_time")),
    }


def load_paper_positions(base_dir: Path, tokens: Optional[Iterable[Mapping[str, Any]]] = None) -> Dict[str, Any]:
    paper_dir = base_dir / "paper_live"
    market_caps = build_market_cap_index(tokens or [])
    case_files = load_case_file_index(paper_dir)
    open_positions = [enrich_paper_position(row, market_caps, case_files) for row in load_paper_rows_from_json(paper_dir / "paper_positions_open.json", "open_positions", "开放仓位", "positions")]
    closed_positions = [enrich_paper_position(row, market_caps, case_files) for row in load_paper_rows_from_json(paper_dir / "paper_positions_closed.json", "closed_positions", "关闭仓位", "positions")]
    for row in open_positions + closed_positions:
        quality = infer_case_quality(row)
        row.update(quality)
        row["paper_action"] = infer_paper_action(row, quality["case_quality"])
        row["lifecycle_timeline"] = lifecycle_timeline_for_position(row)
    strategy_metrics = read_json(paper_dir / "strategy_metrics.json", {})
    all_positions = open_positions + closed_positions
    return {
        "open": open_positions,
        "closed": closed_positions,
        "strategy_metrics": strategy_metrics if isinstance(strategy_metrics, dict) else {},
        "strategy_panel": build_strategy_panel(all_positions, strategy_metrics if isinstance(strategy_metrics, dict) else {}),
        "entry_quality_summary": build_entry_quality_summary(all_positions),
        "wallet_exit_effectiveness": build_wallet_exit_effectiveness(all_positions),
        "open_count": len(open_positions),
        "closed_count": len(closed_positions),
    }

def build_kpi(tokens: List[Dict[str, Any]], paper_positions: Mapping[str, Any]) -> Dict[str, Any]:
    states = Counter(t.get("current_state", "UNKNOWN") for t in tokens)
    wallet = Counter(t.get("wallet_structure_status", "MISSING") for t in tokens)
    closed = as_list(paper_positions.get("closed"))
    wins = 0
    pnl_values: List[float] = []
    for row in closed:
        if isinstance(row, dict):
            pnl = num(first_non_empty(row.get("realized_pnl_pct"), row.get("final_pnl_pct"), row.get("pnl_pct"), row.get("最终收益率_pct"), default="0"))
            pnl_values.append(pnl)
            if pnl > 0:
                wins += 1
    return {
        "token_count": len(tokens),
        "state_counts": dict(states),
        "WATCHING": states.get("WATCHING", 0),
        "BLOCKED": states.get("BLOCKED", 0),
        "PAUSE": states.get("PAUSE", 0),
        "PAPER_READY": states.get("PAPER_READY", 0),
        "PAPER_OPEN": states.get("PAPER_OPEN", 0),
        "wallet_structure_coverage": len([t for t in tokens if t.get("wallet_structure_status") not in {"MISSING", "未接入", "WALLET_UNKNOWN"}]),
        "wallet_missing_count": len([t for t in tokens if t.get("wallet_structure_status") in {"MISSING", "未接入", "WALLET_UNKNOWN"}]),
        "wallet_status_counts": dict(wallet),
        "open_positions": paper_positions.get("open_count", 0),
        "closed_positions": paper_positions.get("closed_count", 0),
        "closed_win_rate": round((wins / len(pnl_values) * 100), 2) if pnl_values else 0,
        "avg_closed_pnl": round((sum(pnl_values) / len(pnl_values)), 2) if pnl_values else 0,
    }


def build_funnel(tokens: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "candidates": len(tokens),
        "signal_ready": len([t for t in tokens if str(t.get("signal_level", "")).startswith(("S3", "S4"))]),
        "wallet_support": len([t for t in tokens if t.get("wallet_structure_status") == "WALLET_SUPPORT"]),
        "quote_security_pass": len([t for t in tokens if t.get("quote_gate") == "ALLOW_CONFIRMATION_LAYER" and t.get("security_gate") == "READY_FOR_CONFIRMATION"]),
        "paper_ready": len([t for t in tokens if t.get("current_state") == "PAPER_READY"]),
        "paper_open": len([t for t in tokens if t.get("current_state") == "PAPER_OPEN" or t.get("paper_status") == "OPEN"]),
    }


def build_entry_block_reasons(tokens: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    c = Counter()
    for t in tokens:
        state = t.get("current_state")
        wallet = t.get("wallet_structure_status")
        quote = t.get("quote_gate")
        security = t.get("security_gate")
        signal = str(t.get("signal_level", ""))
        if wallet == "MISSING":
            c["wallet_structure_missing"] += 1
        if wallet == "WALLET_BLOCK":
            c["wallet_block"] += 1
        if not signal.startswith(("S3", "S4")):
            c["signal_not_ready"] += 1
        if quote in {"MISSING", "PAUSE_NEED_CONFIRM", "BLOCK_BUY", "ERROR"}:
            c["quote_not_ready"] += 1
        if security in {"MISSING", "PAUSE", "BLOCK", "ERROR"}:
            c["security_not_ready"] += 1
        if state not in {"PAPER_READY", "PAPER_OPEN"}:
            c["state_not_ready"] += 1
        if num(t.get("data_quality_score")) and num(t.get("data_quality_score")) < 50:
            c["data_quality_low"] += 1
    if not any(t.get("paper_status") == "OPEN" for t in tokens):
        c["paper_runner_not_called"] += 1
    return dict(c)


def normalize_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for event in events[-50:]:
        out.append({
            "time": first_non_empty(event.get("time"), event.get("event_time"), event.get("timestamp"), default=""),
            "event_type": first_non_empty(event.get("event_type"), event.get("type"), default="EVENT"),
            "token_symbol": first_non_empty(event.get("token_symbol"), event.get("symbol"), default=""),
            "token_address": first_non_empty(event.get("token_address"), event.get("token"), default=""),
            "message": first_non_empty(event.get("message"), event.get("reason"), event.get("latest_reason"), default=json.dumps(event, ensure_ascii=False)[:240]),
        })
    return out



def build_sikk_methodology() -> Dict[str, Any]:
    return {
        "title": "SIKK-SOL 方法论流程",
        "boundary": "纸面验证 / 策略观察 / 只读，不执行真实 swap，不签名，不广播",
        "stages": [
            {
                "stage_id": "P0_候选发现",
                "stage_name": "P0 候选发现",
                "goal": "从 GMGN 新币池筛出可继续结构分析的候选，不把候选等级当买入信号。",
                "entry_condition": "GMGN filter 命中市值、池子、成交额、净流入、Top10/Dev 持仓等基础条件。",
                "checks": ["市值 50K-1.5M", "池子 10K-300K", "成交额 50K+", "净流入 5K+", "Top10≤35%", "Dev≤5%"],
                "pass_condition": "进入 WATCHING / 后续 K线吸筹分析。",
                "block_condition": "基础流动性/持仓/成交结构不合格，或数据缺失。",
                "outputs": ["gmgn_new_token_filter/token_candidates.json", "token_candidates.csv"],
                "token_fields": ["token_symbol", "token_address", "discovery_market_cap_usd", "liquidity_usd", "volume_24h_usd", "net_buy_usd"],
            },
            {
                "stage_id": "P1_K线吸筹与信号",
                "stage_name": "P1 K线吸筹与信号",
                "goal": "验证是否出现 SIKK-B 控盘箱体、吸筹窗口、突破回踩或失效结构。",
                "entry_condition": "候选池 token 有 1m/5m K线和 accumulation_window 输出。",
                "checks": ["control_box_high/low", "T_start/T_end", "AVWAP", "POC", "OBV", "CMF", "S0/S1/S2/S3/S4/SX"],
                "pass_condition": "S3/S4 + 风险门禁非 BLOCK，才允许进入纸面准备。",
                "block_condition": "SX、跌破控盘底、跌破 POC/AVWAP 且放量、窗口 invalid。",
                "outputs": ["candidate_signal_outputs/candidate_signal_summary.json", "token_readiness_result.json", "risk_gate_report.json"],
                "token_fields": ["signal_level", "signal_gate", "signal_time", "signal_price", "strategy_type", "main_reason"],
            },
            {
                "stage_id": "P2_钱包结构门禁",
                "stage_name": "P2 钱包结构门禁",
                "goal": "判断筹码控制权是否仍在结构侧；WALLET_SUPPORT 只是不阻断，不是实盘授权。",
                "entry_condition": "token 达到 PAPER_READY / 需要钱包证据复核。",
                "checks": ["早期钱包是否仍持有", "高结果钱包是否退出", "同源组同步卖出", "分发侧卖出", "对手盘压力", "数据质量"],
                "pass_condition": "WALLET_SUPPORT / WALLET_NEUTRAL 且其他门禁通过。",
                "block_condition": "WALLET_BLOCK、早期集中清仓、同源组同步卖出、对手盘压力过高。",
                "outputs": ["wallet_structure_decision.json", "early_wallet_raw.csv", "wallet_classification.csv", "candidate_groups.csv"],
                "token_fields": ["wallet_structure_status", "wallet_structure_score", "wallet_risk_score", "counterparty_pressure_score", "data_quality_score", "wallet_missing_reason"],
            },
            {
                "stage_id": "P3_报价安全确认",
                "stage_name": "P3 报价安全确认",
                "goal": "用 OKX/GMGN 只读 quote 与 token-scan 判断是否允许进入确认/纸面层。",
                "entry_condition": "候选状态进入 PAPER_READY 或需要 quote/security 复查。",
                "checks": ["quote 是否可用", "price impact", "多源报价偏差", "token-scan 风险", "是否 honeypot/不可卖"],
                "pass_condition": "ALLOW_CONFIRMATION_LAYER / ALLOW_PAPER_TRADE。",
                "block_condition": "BLOCK_BUY、quote 缺失、scan 缺失、price impact > 10%、高危安全风险。",
                "outputs": ["quote_snapshot.json", "security_scan_report.json", "quote_security_decision.json", "trade_confirmation_ticket.json"],
                "token_fields": ["quote_gate", "security_gate", "quote_status", "security_status", "latest_reason"],
            },
            {
                "stage_id": "P4_纸面买入",
                "stage_name": "P4 纸面买入",
                "goal": "只做模拟买入，记录真实可复盘的入场证据：时间、SOL 数量、价格、市值、止损。",
                "entry_condition": "当前状态 PAPER_READY，quote/security 未阻断，且没有重复开放仓位。",
                "checks": ["live_entry_price 优先", "signal_entry_price 作为基准", "position_sol", "stop_price", "entry_price_diff_pct", "cost_model"],
                "pass_condition": "写入 paper_positions_open.json/csv 与 paper_trades.csv。",
                "block_condition": "quote/security PAUSE/BLOCK、价格读取失败、仓位为 0、已存在开放仓。",
                "outputs": ["paper_positions_open.json", "paper_positions_open.csv", "paper_trades.csv"],
                "token_fields": ["paper_entry_time", "paper_position_sol", "paper_entry_price", "paper_entry_market_cap_usd", "paper_stop_price", "paper_pnl_pct"],
            },
            {
                "stage_id": "P5_持仓监控与退出",
                "stage_name": "P5 持仓监控与退出",
                "goal": "纸面持仓期间持续监控价格、止损、止盈、钱包结构恶化和失败归因。",
                "entry_condition": "已有 PAPER_OPEN 纸面仓位。",
                "checks": ["硬止损", "时间止损", "+50/+100/+200 分批止盈", "移动止盈", "FORCE_PAPER_EXIT", "EXIT_MONITOR"],
                "pass_condition": "HOLD / EXIT_MONITOR / 纸面关闭仓位并记录原因。",
                "block_condition": "触发止损、结构恶化、报价安全恶化、流动性骤降。",
                "outputs": ["paper_positions_closed.json", "paper_positions_closed.csv", "risk_events.jsonl", "failure_attribution.jsonl"],
                "token_fields": ["remaining_pct", "max_profit_pct", "max_drawdown_pct", "take_profit_trigger_count", "exit_reason", "failure_type"],
            },
            {
                "stage_id": "P6_复盘校准",
                "stage_name": "P6 复盘校准",
                "goal": "按钱包结构状态、失败归因、信号等级统计纸面策略表现。",
                "entry_condition": "存在 open/closed paper positions 与 failure_attribution。",
                "checks": ["胜率", "平均收益", "中位数收益", "按 wallet_structure_status 分组", "按 failure_type 分组"],
                "pass_condition": "日报/钱包结构日报生成，供下一轮策略校准。",
                "block_condition": "数据缺失时生成空报告，不影响主流程。",
                "outputs": ["paper_daily_report_YYYYMMDD.md", "wallet_structure_daily_report_YYYYMMDD.md"],
                "token_fields": ["wallet_structure_status", "signal_level", "final_pnl_pct", "failure_type"],
            },
            {
                "stage_id": "P7_人工确认后小额实盘准备",
                "stage_name": "P7 人工确认后小额实盘准备",
                "goal": "只生成确认单与执行前门禁；默认不真实 swap、不签名、不广播。",
                "entry_condition": "多日纸面验证有效，且用户明确要求进入人工确认层。",
                "checks": ["CONFIRM_REAL_TRADE", "execution_gate", "broadcast_guard", "fresh quote/security", "human amount"],
                "pass_condition": "PRE_EXECUTION_READY 仅代表可人工复核，不代表自动执行。",
                "block_condition": "默认关闭：confirmation_enabled=false、real_swap_enabled=false、broadcast_allowed=false。",
                "outputs": ["trade_confirmation_ticket.md", "execution_gate_decision.json", "broadcast_gate_decision.json"],
                "token_fields": ["默认关闭", "confirmation_enabled", "real_swap_enabled", "broadcast_allowed"],
            },
        ],
        "risk_gate_rules": {
            "BLOCK_BUY": ["安全风险 CRITICAL", "无法卖出 / honeypot", "无有效报价", "流动性过低", "price impact > 10%", "跌破控盘底", "早期钱包集中清仓"],
            "PAUSE_NEED_CONFIRM": ["安全风险 HIGH", "price impact 5%-10%", "quote/scan 缺失或过期", "钱包证据不足", "关键数据延迟"],
            "ALLOW_PAPER_TRADE": ["报价可用", "安全扫描未触发硬风险", "流动性和滑点可接受", "未跌破控盘底", "未出现集中清仓"],
        },
        "signal_rules": {
            "S3": ["控盘箱体明确", "突破 control_box_high", "回踩不破 0.236/0.382 或箱体上沿", "站上 AVWAP", "OBV/CMF 不弱", "风险门禁非 BLOCK"],
            "S4": ["S3 基础上突破最近 LH", "形成 HL→HH", "OBV/CMF 同步增强", "风险收益比合格"],
            "SX": ["跌破控盘底", "跌破 POC 且放量", "跌破 AVWAP 且放量", "OBV 持续下降", "CMF 持续小于 0", "风险门禁 BLOCK"],
        },
        "position_sizing": {
            "account_equity_sol": 10,
            "risk_per_trade_pct": 0.25,
            "max_position_sol": 0.2,
            "formula": "risk_sol / ((entry_price - stop_price) / entry_price) × signal_factor × liquidity_factor",
        },
        "exit_plan": {
            "hard_stop_priority": ["0.236", "0.382", "控盘底"],
            "time_stop": "15-30 分钟未形成 HH 或重新跌回箱体",
            "take_profit_steps": ["+50% 卖 25%", "+100% 卖 25%", "+200% 卖 25%", "剩余仓位移动止盈"],
            "emergency_exit": ["早期钱包集中清仓", "跌破控盘底", "安全风险升级", "流动性骤降/无报价"],
        },
        "wallet_exit_policy": {
            "title": "钱包退出策略",
            "enabled": True,
            "default_action": "EXIT_MONITOR",
            "force_exit_min_confidence": 80,
            "min_data_quality_score": 65,
            "require_delta_snapshots": 2,
            "require_pattern_conflict": True,
            "require_market_confirmation": True,
            "shadow_hold_tracking": True,
            "summary": "默认 EXIT_MONITOR；强证据才 FORCE_PAPER_EXIT；所有强制退出进入影子持仓复盘。",
            "hard_exit_codes": ["SAME_SOURCE_SYNC_EXIT", "ACTIVE_DISTRIBUTION", "HIGH_RESULT_GROUP_EXIT", "COUNTERPARTY_ABSORBING", "WALLET_RISK_WITH_PRICE_BREAKDOWN"],
        },
    }

def build_coverage_diagnostics(base_dir: Path, tokens: List[Dict[str, Any]], paper_positions: Mapping[str, Any], kpi: Mapping[str, Any]) -> Dict[str, Any]:
    token_count = len(tokens)
    wallet_coverage = int(kpi.get("wallet_structure_coverage") or 0)
    wallet_missing = int(kpi.get("wallet_missing_count") or 0)
    paper_dir = base_dir / "paper_live"
    csv_paths = {
        "open_csv": paper_dir / "paper_positions_open.csv",
        "closed_csv": paper_dir / "paper_positions_closed.csv",
    }
    return {
        "wallet_coverage": wallet_coverage,
        "wallet_missing_count": wallet_missing,
        "wallet_missing_rate_pct": round((wallet_missing / token_count * 100.0), 4) if token_count else 0.0,
        "wallet_missing_repair_plan": [
            "优先检查 wallet_structure_decision.json 是否生成并被 dashboard/load_wallet_decisions 读取。",
            "对 PAPER_READY/PAPER_OPEN 且 wallet_structure_status=MISSING 的 token 输出源文件、字段、状态诊断；不放宽入场。",
            "复查 early_wallet_raw.csv / wallet_classification.csv / candidate_groups.csv 与 token_address join key。",
        ],
        "paper_json_csv_sync": {
            "open_json_count": int(paper_positions.get("open_count") or 0),
            "closed_json_count": int(paper_positions.get("closed_count") or 0),
            "open_csv_exists": csv_paths["open_csv"].exists(),
            "closed_csv_exists": csv_paths["closed_csv"].exists(),
            "source_note": "sikk_live_run.py 单入口负责 paper JSON/CSV 同步与 dashboard_data.json 刷新。",
        },
        "safety_defaults": {
            "real_swap_enabled": False,
            "broadcast_allowed": False,
            "private_key_required": False,
            "boundary": DASHBOARD_BOUNDARY,
        },
    }


def build_dashboard_data(base_dir: Path) -> Dict[str, Any]:
    live_state = read_json(base_dir / "live_state.json", {})
    if not isinstance(live_state, dict):
        live_state = {}
    wallet_decisions = load_wallet_decisions(base_dir)
    tokens = sort_tokens([normalize_token(row, wallet_decisions) for row in load_token_statuses(base_dir, live_state)])
    paper_positions = load_paper_positions(base_dir, tokens)
    strategy_panel = paper_positions.get("strategy_panel", {}) if isinstance(paper_positions, Mapping) else {}
    token_addresses = {str(t.get("token_address")) for t in tokens if t.get("token_address")}
    for pos in as_list(paper_positions.get("open")) + as_list(paper_positions.get("closed")):
        if not isinstance(pos, Mapping):
            continue
        token = first_non_empty(pos.get("token_address"), pos.get("代币地址"))
        if token and token not in token_addresses:
            tokens.append(token_from_paper_position(pos))
            token_addresses.add(token)
    tokens = sort_tokens(tokens)
    events = normalize_events(read_jsonl(base_dir / "events" / "live_events.jsonl"))
    wallet_missing = Counter(t.get("wallet_missing_reason", "UNKNOWN") for t in tokens if t.get("wallet_structure_status") == "MISSING")
    wallet_summary = Counter(t.get("wallet_structure_status", "MISSING") for t in tokens)
    opportunities = [t for t in tokens if t.get("current_state") in {"PAPER_OPEN", "PAPER_READY"} or t.get("wallet_structure_status") == "WALLET_SUPPORT" or str(t.get("signal_level", "")).startswith(("S3", "S4"))]
    kpi = build_kpi(tokens, paper_positions)
    coverage_diagnostics = build_coverage_diagnostics(base_dir, tokens, paper_positions, kpi)
    funnel = build_funnel(tokens)
    system_health = {
        "runtime_status": first_non_empty(live_state.get("runtime_status"), default="OK"),
        "source_last_update": live_state.get("last_update"),
        "token_count": len(tokens),
        "paper_open_count": paper_positions.get("open_count", 0),
        "paper_closed_count": paper_positions.get("closed_count", 0),
        "wallet_missing_count": kpi.get("wallet_missing_count", 0),
        "opportunity_count": len(opportunities),
        "event_count": len(events),
    }
    methodology = build_sikk_methodology()
    return {
        "meta": {
            "generated_at": utc_now(),
            "base_dir": str(base_dir),
            "boundary": DASHBOARD_BOUNDARY,
            "source_last_update": live_state.get("last_update"),
        },
        "metadata": {
            "generated_at": utc_now(),
            "base_dir": str(base_dir),
            "boundary": DASHBOARD_BOUNDARY,
            "source_last_update": live_state.get("last_update"),
        },
        "kpi": kpi,
        "funnel": funnel,
        "system_health": system_health,
        "coverage_diagnostics": coverage_diagnostics,
        "tokens": tokens,
        "opportunities": opportunities[:30],
        "wallet_structure_summary": dict(wallet_summary),
        "wallet_missing_reasons": dict(wallet_missing),
        "entry_block_reasons": build_entry_block_reasons(tokens),
        "paper_positions": paper_positions,
        "strategy_panel": strategy_panel,
        "events": events,
        "methodology": methodology,
        "sections": ["总控台", "方法论流程", "策略评估面板", "候选漏斗", "重点机会", "代币总表", "单币详情", "纸面验证区", "系统健康"],
    }


def _render_markdown_as_static_html(markdown_text: str, title: str = "SIKK 实战档案") -> str:
    """Tiny dependency-free Markdown-to-readable-HTML for case files.

    Python http.server serves .md as text/plain with no UTF-8 charset on some clients,
    which makes Chinese case files unreadable in mobile browsers. Keep the original .md
    copy, and publish a .html companion for click-through reading.
    """
    body: List[str] = []
    in_ul = False
    in_code = False
    in_table = False
    table_rows: List[List[str]] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            body.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        body.append('<table class="case-table">')
        for idx, cells in enumerate(table_rows):
            if idx == 1 and all(set(c.replace(" ", "")) <= {"-", ":"} for c in cells):
                continue
            tag = "th" if idx == 0 else "td"
            body.append("<tr>" + "".join(f"<{tag}>{html.escape(c.strip())}</{tag}>" for c in cells) + "</tr>")
        body.append("</table>")
        in_table = False
        table_rows = []

    for raw in markdown_text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            close_table(); close_ul()
            if in_code:
                body.append("</code></pre>")
                in_code = False
            else:
                body.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            body.append(html.escape(line) + "\n")
            continue
        if line.startswith("|") and line.endswith("|"):
            close_ul()
            in_table = True
            table_rows.append([c.strip() for c in line.strip("|").split("|")])
            continue
        close_table()
        if not line.strip():
            close_ul()
            continue
        if line.startswith("# "):
            close_ul(); body.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            close_ul(); body.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            close_ul(); body.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
        elif line.startswith("> "):
            close_ul(); body.append(f"<blockquote>{html.escape(line[2:].strip())}</blockquote>")
        elif line.startswith("- "):
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{html.escape(line[2:].strip())}</li>")
        elif set(line.strip()) <= {"-"}:
            close_ul(); body.append("<hr>")
        else:
            close_ul(); body.append(f"<p>{html.escape(line)}</p>")
    close_table(); close_ul()
    return """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
body{{margin:0;background:#08111f;color:#e5eefc;font:15px/1.65 system-ui,-apple-system,Segoe UI,sans-serif;padding:22px;}}
main{{max-width:980px;margin:auto;background:#101b2d;border:1px solid #213650;border-radius:18px;padding:24px;box-shadow:0 12px 36px rgba(0,0,0,.28)}}
h1,h2,h3{{color:#fff}} h2{{border-top:1px solid #213650;padding-top:18px;margin-top:24px}} blockquote{{border-left:4px solid #2dd4bf;margin:12px 0;padding:10px 14px;background:#0b1424;color:#b7c7dc}}
table{{width:100%;border-collapse:collapse;margin:12px 0;background:#0b1424;border-radius:12px;overflow:hidden}} th,td{{border:1px solid #213650;padding:8px;text-align:left;vertical-align:top}} th{{color:#2dd4bf;background:#13243a}} code,pre{{white-space:pre-wrap;background:#07101d;color:#e5eefc}} a{{color:#2dd4bf}}
.boundary{{color:#8fa3bd;margin-bottom:18px}}
</style></head><body><main><div class="boundary">只读实战档案；不执行真实 swap，不读取私钥，不签名，不广播。</div>{body}</main></body></html>""".format(title=html.escape(title), body="\n".join(body))


def _site_case_file_name(path_text: str) -> str:
    src = Path(path_text)
    name = src.name or "case-file"
    # Keep filenames URL/path safe for static serving; case-file builder already uses ASCII ids.
    return name.replace("/", "_").replace("\\", "_")


def publish_case_files_for_site(output_dir: Path, data: Mapping[str, Any]) -> Dict[str, Any]:
    """Copy paper case files into site/case_files and rewrite dashboard links.

    The live data stores case_file_md/json as project paths such as
    data/gmgn_candidates_live_run/paper_live/case_files/<id>.md. A browser opened from
    /site cannot resolve those paths, especially on mobile. This function publishes a
    static copy under /site/case_files and rewrites only the website payload to relative
    URLs like case_files/<id>.md. It is read-only with respect to trading state.
    """
    site_case_dir = output_dir / "case_files"
    site_case_dir.mkdir(parents=True, exist_ok=True)
    copied: Dict[str, str] = {}
    missing: List[str] = []

    def publish(path_value: Any) -> str:
        path_text = first_non_empty(path_value)
        if not path_text:
            return ""
        if path_text.startswith("case_files/"):
            return path_text
        src = Path(path_text)
        if not src.exists():
            missing.append(path_text)
            return path_text
        rel = f"case_files/{_site_case_file_name(path_text)}"
        dst = output_dir / rel
        shutil.copy2(src, dst)
        copied[path_text] = rel
        if src.suffix.lower() == ".md":
            html_rel = f"case_files/{src.stem}.html"
            html_dst = output_dir / html_rel
            html_dst.write_text(_render_markdown_as_static_html(src.read_text(encoding="utf-8"), src.stem), encoding="utf-8")
            copied[f"{path_text}#html"] = html_rel
            return html_rel
        return rel

    for bucket in ("open", "closed"):
        for row in as_list((data.get("paper_positions") or {}).get(bucket) if isinstance(data.get("paper_positions"), Mapping) else []):
            if not isinstance(row, dict):
                continue
            if row.get("case_file_md"):
                row["case_file_md_source"] = row.get("case_file_md")
                row["case_file_md"] = publish(row.get("case_file_md"))
            if row.get("case_file_json"):
                row["case_file_json_source"] = row.get("case_file_json")
                row["case_file_json"] = publish(row.get("case_file_json"))
    return {"copied_count": len(copied), "missing": missing, "published": copied}


def write_site_files(output_dir: Path, data: Mapping[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(json.dumps(data, ensure_ascii=False))
    publish_result = publish_case_files_for_site(output_dir, data)
    if isinstance(data.get("metadata"), dict):
        data["metadata"]["case_files_static_publish"] = publish_result
    if isinstance(data.get("meta"), dict):
        data["meta"]["case_files_static_publish"] = publish_result
    (output_dir / "dashboard_data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    index = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SIKK-SOL Visual Console v2</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <aside class="sidebar">
    <div class="brand">SIKK-SOL<br><span>Visual Console v2</span></div>
    <a href="#command">总控台</a>
    <a href="#methodologyPanel">方法论流程</a>
    <a href="#funnelPanel">候选漏斗</a>
    <a href="#opportunityPanel">重点机会</a>
    <a href="#explorer">代币总表</a>
    <a href="#paperLab">纸面验证区</a>
    <a href="#systemHealth">系统健康</a>
    <a href="#eventsPanel">最新事件</a>
  </aside>
  <div class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">SIKK-SOL Visual Console v2</p>
        <h1>SIKK 静态专业控制台</h1>
        <p id="boundary">只读观察 / 纸面验证 / 不执行真实 swap</p>
      </div>
      <div class="meta"><div id="generatedAt">加载中…</div><div id="refreshInfo">自动刷新：60 秒 / 刷新时间：—</div></div>
    </header>

    <main>
      <section class="panel" id="command">
        <div class="section-head"><h2>总控台</h2><span class="hint">系统状态、机会、阻断、纸面仓位一屏决策</span></div>
        <section class="grid cards" id="kpiCards"></section>
      </section>

      <section class="panel" id="methodologyPanel">
        <div class="section-head"><h2>方法论流程</h2><span class="hint">把 SIKK 实际层级、阶段、步骤、通过/阻断规则落实到网页</span></div>
        <p class="hint" id="methodBoundary">纸面验证 / 只读，不执行真实 swap</p>
        <div id="methodStages" class="method-stages"></div>
        <section class="grid two">
          <div><h3>风险门禁规则</h3><div id="riskRules" class="rule-list"></div></div>
          <div><h3>信号等级规则</h3><div id="signalRules" class="rule-list"></div></div>
        </section>
        <section class="grid two">
          <div><h3>仓位计算</h3><div id="positionSizing" class="rule-list"></div></div>
          <div><h3>退出计划</h3><div id="exitPlan" class="rule-list"></div></div>
        </section>
      </section>

      <section class="panel" id="funnelPanel">
        <h2>候选漏斗</h2>
        <div id="funnel" class="funnel"></div>
      </section>

      <section class="panel" id="opportunityPanel">
        <div class="section-head"><h2>重点机会</h2><span class="hint">只展示 PAPER_READY / PAPER_OPEN / WALLET_SUPPORT / S3-S4</span></div>
        <div id="opportunities" class="opportunities"></div>
      </section>

      <section class="panel" id="explorer">
        <div class="section-head">
          <h2>代币总表</h2>
          <button id="sortByPriority" type="button">优先级排序</button>
        </div>
        <div class="filters">
          <input id="searchInput" placeholder="搜索代币 / 原因" />
          <input id="reasonInput" placeholder="原因搜索" />
          <select id="stateFilter"><option value="">状态筛选</option></select>
          <select id="walletFilter"><option value="">钱包筛选</option></select>
          <select id="paperFilter"><option value="">纸面筛选</option></select>
        </div>
        <p class="hint">点击任意代币查看详情</p>
        <div class="table-wrap"><table id="tokenTable"></table></div>
      </section>

      <aside id="tokenDetail" class="detail-drawer">
        <button id="closeDetail" type="button">关闭</button>
        <h2>单币详情</h2>
        <div id="detailBody"><p class="empty">点击任意代币查看详情。</p></div>
      </aside>

      <section class="panel" id="coveragePanel">
        <div class="section-head"><h2>覆盖诊断</h2><span class="hint">钱包结构缺口修复计划 / JSON/CSV 同步 / 安全默认关闭</span></div>
        <div id="coverageDiagnostics" class="grid cards"></div>
      </section>

      <section class="grid two">
        <div class="panel">
          <h2>未入场原因统计</h2>
          <div id="entryReasons" class="bars"></div>
        </div>
        <div class="panel">
          <h2>钱包结构未接入原因</h2>
          <div id="walletReasons" class="bars"></div>
        </div>
      </section>

      <section class="panel" id="paperLab">
        <div class="section-head"><h2>纸面验证区</h2><span class="hint">当前开放仓位 / 已关闭仓位 / 胜率 / 平均收益 / 失败原因 Top / 钱包结构表现</span></div>
        <div id="paperSummary" class="grid cards"></div>
        <h3>当前纸面仓位</h3>
        <div id="paperPositions" class="positions"></div>
      </section>

      <section class="panel" id="strategyPanel">
        <div class="section-head"><h2>策略评估面板</h2><span class="hint">日报概览 / 胜率 / 失败原因 / 信号表现 / live vs signal 双收益保留</span></div>
        <div id="strategySummary" class="grid cards"></div>
        <div class="grid two">
          <div><h3>日报概览</h3><div id="strategyReport" class="rule-list"></div></div>
          <div><h3>信号表现</h3><div id="strategySignalPerformance" class="rule-list"></div></div>
        </div>
        <div class="grid two">
          <div><h3>失败原因 Top</h3><div id="strategyFailureReasons" class="bars"></div></div>
          <div><h3>入场模式分布</h3><div id="strategyEntryModes" class="bars"></div></div>
        </div>
        <div class="grid two">
          <div><h3>信号分层</h3><div id="strategySignalCards" class="grid cards"></div><div id="strategySignalGroups" class="rule-list"></div></div>
          <div><h3>钱包结构分层</h3><div id="strategyWalletBars" class="bars"></div><div id="strategyWalletGroups" class="rule-list"></div></div>
        </div>
      </section>

      <section class="panel" id="systemHealth">
        <h2>系统健康</h2>
        <div id="health" class="bars"></div>
      </section>

      <section class="panel" id="eventsPanel">
        <h2>最新事件</h2>
        <div id="events" class="events"></div>
      </section>
    </main>
  </div>
  <script src="app.js"></script>
</body>
</html>
"""
    app = r"""let DATA = null;
let SORT_DESC = false;
const $ = (id) => document.getElementById(id);
const fmt = (v) => (v === undefined || v === null || v === '' ? '—' : v);
const pct = (v) => `${Number(v || 0).toFixed(2)}%`;
const sol = (v) => `${Number(v || 0).toFixed(6)} SOL`;
const usd = (v) => (v === undefined || v === null || v === '' ? '待补' : `$${Number(v).toLocaleString(undefined,{maximumFractionDigits:0})}`);
const 中文标签 = __STATE_LABELS__;
function zh(v){ const s = fmt(v); return 中文标签[s] || s; }
function positionToken(p){ return String(p.token_address || p.代币地址 || ''); }
function latestPositionFor(token){ const list=[...((DATA.paper_positions&&DATA.paper_positions.open)||[]), ...((DATA.paper_positions&&DATA.paper_positions.closed)||[])]; return list.find(p => positionToken(p)===String(token)); }
function positionCard(p){ const caseLink = p.case_file_md ? `<a class="case-link" href="${fmt(p.case_file_md)}" target="_blank" rel="noopener">实战档案</a>` : '<span class="muted">实战档案待生成</span>'; const miss=(p.evidence_missing_fields||p.case_missing_fields||p.missing_fields||[]); return `<article class="position"><strong>${fmt(p.token_symbol || p.代币符号 || p.token_address || p.代币地址)}</strong><span>${badge(p.status || p.paper_status || 'OPEN')}</span>${caseLink}<div class="kv"><b>纸面买入时间</b><span>${fmt(p.paper_entry_time || p.entry_time || p.信号时间)}</span><b>纸面买入数量</b><span>${sol(p.paper_position_sol || p.position_sol || p.模拟仓位SOL)}</span><b>入场市值</b><span>${usd(p.paper_entry_market_cap_usd || p.入场市值USD)}</span><b>入场价</b><span>${fmt(p.paper_entry_price || p.entry_price || p.模拟入场价)}</span><b>当前价</b><span>${fmt(p.paper_current_price || p.current_price || p.last_price)}</span><b>止损价</b><span>${fmt(p.paper_stop_price || p.stop_price)}</span><b>剩余仓位</b><span>${fmt(p.paper_remaining_pct || p.remaining_pct)}%</span><b>当前收益</b><span>${pct(p.paper_pnl_pct || p.当前收益率_pct || p.live_pnl_pct || p.paper_pnl_pct)}</span><b>档案质量</b><span>${fmt(p.case_quality_level || p.case_quality)}｜${fmt(p.case_completeness_score)}%</span><b>字段来源数</b><span>${fmt(p.case_field_source_count)}</span><b>缺失证据</b><span>${Array.isArray(miss)?(miss.slice(0,6).join('、')||'无'):fmt(miss)}</span><b>入场状态</b><span>${fmt(p.market_cap_context_status)}</span><b>买入USD</b><span>${usd(p.paper_size_usd)}</span><b>Token数量</b><span>${fmt(p.estimated_token_amount)}</span><b>发现到入场延迟</b><span>${fmt(p.entry_delay_from_discovery_sec)} 秒</span><b>信号时间</b><span>${fmt(p.paper_signal_time || p.signal_time || p.信号时间)}</span><b>信号价格</b><span>${fmt(p.paper_signal_price || p.signal_price || p.信号价格)}</span><b>更新时间</b><span>${fmt(p.paper_last_update_time || p.last_update_time)}</span></div></article>`; }

function list(items){ return `<ul>${(items||[]).map(x=>`<li>${fmt(x)}</li>`).join('')}</ul>`; }
function ruleBlock(title, items){ return `<article class="rule"><h4>${fmt(title)}</h4>${Array.isArray(items)?list(items):`<p>${fmt(items)}</p>`}</article>`; }
function renderMethodology(){ const m=DATA.methodology||{}; $('methodBoundary').textContent = m.boundary || '纸面验证 / 只读，不执行真实 swap'; $('methodStages').innerHTML = (m.stages||[]).map(s=>`<article class="stage-card"><h3>${fmt(s.stage_name)}</h3><p>${fmt(s.goal)}</p><div class="kv"><b>进入条件</b><span>${fmt(s.entry_condition)}</span><b>通过条件</b><span>${fmt(s.pass_condition)}</span><b>阻断条件</b><span>${fmt(s.block_condition)}</span><b>输出文件</b><span>${(s.outputs||[]).join(' / ')}</span><b>网页字段</b><span>${(s.token_fields||[]).join(' / ')}</span></div><details><summary>具体检查步骤</summary>${list(s.checks)}</details></article>`).join(''); $('riskRules').innerHTML = Object.entries(m.risk_gate_rules||{}).map(([k,v])=>ruleBlock(k,v)).join(''); $('signalRules').innerHTML = Object.entries(m.signal_rules||{}).map(([k,v])=>ruleBlock(k,v)).join(''); $('positionSizing').innerHTML = Object.entries(m.position_sizing||{}).map(([k,v])=>ruleBlock(zh(k), Array.isArray(v)?v:String(v))).join(''); $('exitPlan').innerHTML = Object.entries(m.exit_plan||{}).map(([k,v])=>ruleBlock(zh(k), v)).join('') + ruleBlock('钱包退出策略', ['默认 EXIT_MONITOR', '强证据才 FORCE_PAPER_EXIT', '影子持仓复盘', (m.wallet_exit_policy&&m.wallet_exit_policy.summary)||'']); }
function stageValue(t, p, key){ const map={P0_候选发现:fmt(t.discovery_market_cap_usd)||fmt(t.current_market_cap_usd),P1_K线吸筹与信号:fmt(t.signal_level),P2_钱包结构门禁:fmt(t.wallet_structure_status),P3_报价安全确认:`${zh(t.quote_gate)} / ${zh(t.security_gate)}`,P4_纸面买入:p?fmt(p.paper_entry_time):'',P5_持仓监控与退出:p?pct(p.paper_pnl_pct):fmt(t.paper_status),P6_复盘校准:fmt(t.paper_status),P7_人工确认后小额实盘准备:'默认关闭'}; return map[key] || ''; }
function stageStatus(t, p, stage){ const id=stage.stage_id; if(id==='P0_候选发现') return t.token_address?'已进入':'待查'; if(id==='P1_K线吸筹与信号') return t.signal_level && t.signal_level!=='UNKNOWN'?'有信号':'等待信号'; if(id==='P2_钱包结构门禁') return t.wallet_structure_status==='MISSING'?'未进入钱包结构阶段':zh(t.wallet_structure_status); if(id==='P3_报价安全确认') return `${zh(t.quote_gate)} / ${zh(t.security_gate)}`; if(id==='P4_纸面买入') return p?'已纸面买入':'未纸面买入'; if(id==='P5_持仓监控与退出') return p?zh(t.next_action||'HOLD'):'无开放仓'; if(id==='P6_复盘校准') return '进入日报统计'; if(id==='P7_人工确认后小额实盘准备') return '关闭：只读，不执行真实 swap'; return '—'; }
function renderStageEvidence(t,p){ const stages=(DATA.methodology&&DATA.methodology.stages)||[]; return `<h4>阶段证据核对</h4><div class="stage-evidence">${stages.map(s=>`<article><b>${fmt(s.stage_name)}</b><span>${stageStatus(t,p,s)}</span><small>${stageValue(t,p,s.stage_id)}</small></article>`).join('')}</div>`; }
function renderLifecycleTimeline(t,p){ const rows=(t.lifecycle_timeline || (p&&p.lifecycle_timeline) || []); return `<h4>Lifecycle Timeline</h4><div class="stage-evidence lifecycle-timeline">${rows.length ? rows.map(x=>`<article><b>${fmt(x.stage)}</b><span>${fmt(x.status)}</span><small>${fmt(x.time)}</small></article>`).join('') : '<article><b>待补</b><span>暂无 lifecycle timeline</span><small>统一索引未生成</small></article>'}</div>`; }
function statusClass(v='') { v = String(v); if (v.includes('PAPER_OPEN') || v === 'OPEN' || v.includes('PAPER_READY')) return 'good'; if (v.includes('WALLET_SUPPORT')) return 'support'; if (v.includes('WATCHING') || v.includes('PAUSE')) return 'warn'; if (v.includes('BLOCK') || v.includes('WALLET_BLOCK')) return 'bad'; if (v.includes('ERROR')) return 'error'; return 'muted'; }
function badge(v){ return `<span class="badge ${statusClass(v)}">${zh(v)}</span>`; }
function priorityRank(t){ const p=String(t.priority_level||''); const m=p.match(/P(\d+)/); return m?Number(m[1]):9; }
function renderKpi(){
  const k = DATA.kpi || {};
  const items = [['候选币总数', k.token_count], ['观察中', k.WATCHING], ['已阻断', k.BLOCKED], ['纸面准备就绪', k.PAPER_READY], ['纸面持仓中', k.PAPER_OPEN], ['钱包结构覆盖', `${k.wallet_structure_coverage || 0}/${k.token_count || 0}`], ['开放纸面仓位', k.open_positions], ['已关闭胜率', pct(k.closed_win_rate)], ['平均关闭收益', pct(k.avg_closed_pnl)]];
  $('kpiCards').innerHTML = items.map(([a,b]) => `<div class="card"><div>${a}</div><strong>${fmt(b)}</strong></div>`).join('');
}
function renderFunnel(){ const f = DATA.funnel || {}; const max = Math.max(...Object.values(f), 1); $('funnel').innerHTML = Object.entries(f).map(([k,v]) => `<div class="bar-row"><span>${zh(k)}</span><div class="bar"><i style="width:${(v/max)*100}%"></i></div><b>${v}</b></div>`).join(''); }
function renderBars(id, obj){ const max = Math.max(...Object.values(obj || {}), 1); $(id).innerHTML = Object.entries(obj || {}).map(([k,v]) => `<div class="bar-row"><span>${zh(k)}</span><div class="bar"><i style="width:${(v/max)*100}%"></i></div><b>${v}</b></div>`).join('') || '<p class="empty">暂无统计</p>'; }
function renderGroupedStats(obj){ const entries = Object.entries(obj || {}); if (!entries.length) return '<p class="empty">暂无统计</p>'; return entries.map(([k,v]) => `<div class="rule"><h4>${zh(k)}</h4><p>出现次数 ${fmt(v.count)} ｜ 出现率 ${pct(v.occurrence_pct)} ｜ 胜率 ${pct(v.win_rate_pct)} ｜ live 平均收益 ${pct(v.avg_live_pnl_pct)} ｜ signal 平均收益 ${pct(v.avg_signal_pnl_pct)}</p></div>`).join(''); }
function renderSignalCards(obj){ const keys=['S3','S4','SX']; return keys.map(k=>{ const v=(obj||{})[k]||{}; return `<div class="card"><div>${zh(k)}</div><strong>${fmt(v.count||0)} 个</strong><small>胜率 ${pct(v.win_rate_pct)}｜live ${pct(v.avg_live_pnl_pct)}｜signal ${pct(v.avg_signal_pnl_pct)}</small></div>`; }).join(''); }
function renderWalletStructureBars(id, obj){ const keys=['WALLET_SUPPORT','WALLET_NEUTRAL','WALLET_BLOCK']; const max=Math.max(...keys.map(k=>Number(((obj||{})[k]||{}).count||0)),1); $(id).innerHTML = keys.map(k=>{ const v=((obj||{})[k]||{}); const count=Number(v.count||0); return `<div class="bar-row"><span>${zh(k)}</span><div class="bar"><i style="width:${(count/max)*100}%"></i></div><b>${count}｜${pct(v.occurrence_pct)}</b></div><small>胜率 ${pct(v.win_rate_pct)}｜live 平均收益 ${pct(v.avg_live_pnl_pct)}｜signal 平均收益 ${pct(v.avg_signal_pnl_pct)}</small>`; }).join(''); }
function renderOpportunities(){ const rows = DATA.opportunities || []; $('opportunities').innerHTML = rows.length ? rows.slice(0,12).map(t => `<article class="opp" data-token="${fmt(t.token_address)}"><div><strong>${fmt(t.token_symbol)}</strong><small>${fmt(t.token_address).slice(0,10)}…</small></div><div>${badge(t.current_state)} ${badge(t.wallet_structure_status)}</div><p>${fmt(t.main_reason)}</p><small>下一步：${zh(t.next_action)}</small></article>`).join('') : '<p class="empty">当前无重点机会。</p>'; document.querySelectorAll('.opp').forEach(el=>el.onclick=()=>renderDetail(el.dataset.token)); }
function fillFilters(){ const tokens = DATA.tokens || []; const fill = (id, label, vals) => { $(id).innerHTML = `<option value="">${label}</option>` + [...new Set(vals.filter(Boolean))].sort().map(v=>`<option value="${v}">${zh(v)}</option>`).join(''); }; fill('stateFilter','状态筛选', tokens.map(t=>t.current_state)); fill('walletFilter','钱包筛选', tokens.map(t=>t.wallet_structure_status)); fill('paperFilter','纸面筛选', tokens.map(t=>t.paper_status)); }
function filteredRows(){ const q = $('searchInput').value.toLowerCase(); const rq = $('reasonInput').value.toLowerCase(); const sf = $('stateFilter').value, wf = $('walletFilter').value, pf = $('paperFilter').value; let rows = (DATA.tokens || []).filter(t => (!sf || t.current_state===sf) && (!wf || t.wallet_structure_status===wf) && (!pf || t.paper_status===pf) && (!q || JSON.stringify(t).toLowerCase().includes(q)) && (!rq || String(t.main_reason||'').toLowerCase().includes(rq))); rows = rows.slice().sort((a,b)=>SORT_DESC ? priorityRank(b)-priorityRank(a) : priorityRank(a)-priorityRank(b)); return rows; }
function renderTable(){ const rows = filteredRows(); const head = ['代币','状态','优先级','信号','钱包结构','钱包分','风险分','对手盘压力','报价','安全','纸面','收益率','原因','下一步']; $('tokenTable').innerHTML = `<thead><tr>${head.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>` + rows.map(t => `<tr data-token="${fmt(t.token_address)}"><td><b>${fmt(t.token_symbol)}</b><small>${fmt(t.token_address).slice(0,12)}…</small></td><td>${badge(t.current_state)}</td><td>${zh(t.priority_level)}</td><td>${fmt(t.signal_level)}</td><td>${badge(t.wallet_structure_status)}<small>${zh(t.wallet_missing_reason)}</small></td><td>${fmt(t.wallet_structure_score)}</td><td>${fmt(t.wallet_risk_score)}</td><td>${fmt(t.counterparty_pressure_score)}</td><td>${badge(t.quote_gate)}</td><td>${badge(t.security_gate)}</td><td>${badge(t.paper_status)}</td><td>${pct(t.paper_pnl_pct)}</td><td class="reason">${fmt(t.main_reason)}</td><td>${zh(t.next_action)}</td></tr>`).join('') + '</tbody>'; document.querySelectorAll('#tokenTable tbody tr').forEach(el=>el.onclick=()=>renderDetail(el.dataset.token)); }
function renderDetail(tokenAddress){ const t=(DATA.tokens||[]).find(x=>String(x.token_address)===String(tokenAddress)); if(!t) return; const p=latestPositionFor(tokenAddress); const miss=(p&&(p.evidence_missing_fields||p.case_missing_fields||p.missing_fields))||[]; $('tokenDetail').classList.add('open'); $('detailBody').innerHTML = `<h3>${fmt(t.token_symbol)}</h3><p><code>${fmt(t.token_address)}</code></p><div>${badge(t.current_state)} ${badge(t.wallet_structure_status)} ${badge(t.paper_status)}</div>${renderStageEvidence(t,p)}${renderLifecycleTimeline(t,p)}<h4>市场数据 / K线信号</h4><div class="kv"><b>发现市值</b><span>${usd(t.discovery_market_cap_usd)}</span><b>信号市值</b><span>${usd(t.signal_market_cap_usd)}</span><b>入场市值</b><span>${usd(t.paper_entry_market_cap_usd || (p&&p.paper_entry_market_cap_usd))}</span><b>当前市值</b><span>${usd(t.current_market_cap_usd || (p&&p.paper_current_market_cap_usd))}</span><b>信号</b><span>${fmt(t.signal_level)}</span><b>信号门</b><span>${zh(t.signal_gate)}</span></div><h4>主导侧心理与生命周期</h4><div class="kv"><b>生命周期阶段</b><span>${fmt(t.operator_lifecycle_stage)}</span><b>主导侧心理</b><span>${fmt(t.operator_psychology_label)}</span><b>纸面对齐</b><span>${zh(t.paper_trade_alignment)}</span><b>观察重点</b><span>${fmt(t.next_observation_focus)}</span></div><p>${fmt(t.psychology_reason)}</p><h4>Case File 质量与证据缺口</h4><div class="kv"><b>档案质量</b><span>${fmt(p&&p.case_quality_level || p&&p.case_quality || '待补')}</span><b>完整度</b><span>${fmt(p&&p.case_completeness_score)}%</span><b>字段来源数</b><span>${fmt(p&&p.case_field_source_count)}</span><b>缺失证据</b><span>${Array.isArray(miss)?(miss.slice(0,12).join('、')||'无'):fmt(miss)}</span></div><h4>钱包结构</h4><p>结构分：${fmt(t.wallet_structure_score)} ｜ 风险分：${fmt(t.wallet_risk_score)} ｜ 对手盘压力：${fmt(t.counterparty_pressure_score)} ｜ 数据质量：${fmt(t.data_quality_score)}</p><h4>quote/security</h4><p>报价：${zh(t.quote_gate)} ｜ 安全：${zh(t.security_gate)}</p><h4>纸面买入 / 模拟持仓证据</h4>${p ? positionCard(p) : '<p class="empty">暂无纸面买入记录。</p>'}<h4>阻断原因</h4><p>${fmt(t.main_reason)}</p><h4>下一步动作</h4><p>${zh(t.next_action)}</p>`; }
function renderPositions(){ const open = (DATA.paper_positions && DATA.paper_positions.open) || []; $('paperPositions').innerHTML = open.length ? open.map(positionCard).join('') : '<p class="empty">当前无开放纸面仓位。</p>'; }
function renderPaperSummary(){ const p=DATA.paper_positions||{}, k=DATA.kpi||{}, q=p.entry_quality_summary||{}, w=p.wallet_exit_effectiveness||{}; const items=[['当前开放仓位',p.open_count],['已关闭仓位',p.closed_count],['胜率',pct(k.closed_win_rate)],['平均收益',pct(k.avg_closed_pnl)],['入场质量统计','市值分桶 / 发现到入场延迟'],['钱包退出有效性',`强退 ${w.wallet_force_exit_count||0}｜误杀率 ${pct(w.false_exit_rate||0)}`],['钱包结构表现','按 wallet status 复盘']]; $('paperSummary').innerHTML=items.map(([a,b])=>`<div class="card"><div>${a}</div><strong>${fmt(b)}</strong></div>`).join('') + `<div class="card wide"><div>入场质量统计</div><strong>市值分桶：${Object.keys((q.market_cap_buckets||{})).join(' / ')||'待补'}</strong><small>发现到入场延迟：${fmt(q.avg_entry_delay_from_discovery_sec)} 秒；market_cap_context_status</small></div><div class="card wide"><div>钱包退出策略</div><strong>默认 EXIT_MONITOR；强证据才 FORCE_PAPER_EXIT</strong><small>wallet_exit_effectiveness / 影子持仓复盘</small></div>`; }
function renderStrategyPanel(){ const s=DATA.strategy_panel||{}, summary=s.summary||{}, open=(DATA.paper_positions&&DATA.paper_positions.open)||[], closed=(DATA.paper_positions&&DATA.paper_positions.closed)||[]; const summaryItems=[['日报快照',fmt(summary.snapshot_time||summary['snapshot_time'])],['关闭胜率',pct(summary.已关闭胜率_pct||summary.closed_win_rate||DATA.kpi?.closed_win_rate)],['关闭平均收益',pct(summary.已关闭平均收益率_pct||summary.closed_avg_pnl_pct||DATA.kpi?.avg_closed_pnl)],['live 平均收益',pct(s.live_pnl_avg_pct)],['signal 平均收益',pct(s.signal_pnl_avg_pct)],['live-signal 差值',pct(s.live_signal_pnl_gap_avg_pct)]]; $('strategySummary').innerHTML = summaryItems.map(([a,b])=>`<div class="card"><div>${a}</div><strong>${fmt(b)}</strong></div>`).join(''); $('strategyReport').innerHTML = `<div class="rule"><h4>日报概览</h4><p>当前开放仓位 ${open.length}，已关闭仓位 ${closed.length}，关闭胜率 ${pct(summary.已关闭胜率_pct||DATA.kpi?.closed_win_rate)}，平均关闭收益 ${pct(summary.已关闭平均收益率_pct||DATA.kpi?.avg_closed_pnl)}。</p></div><div class="rule"><h4>live / signal 双收益</h4><p>live 平均 ${pct(s.live_pnl_avg_pct)}，signal 平均 ${pct(s.signal_pnl_avg_pct)}，平均差值 ${pct(s.live_signal_pnl_gap_avg_pct)}。</p></div>`; $('strategySignalPerformance').innerHTML = `<div class="rule"><h4>信号表现</h4><p>纸面仓位同时保留 live 与 signal 两套收益，避免只看历史信号价高估收益。</p></div><div class="rule"><h4>入场模式</h4><p>${Object.entries(s.entry_price_mode_counts||{}).map(([k,v])=>`${zh(k)}：${v}`).join(' / ')||'待补'}</p></div>`; renderBars('strategyFailureReasons', s.failure_reason_top||{}); renderBars('strategyEntryModes', s.entry_price_mode_counts||{}); $('strategySignalCards').innerHTML = renderSignalCards(s.signal_groups||{}); $('strategySignalGroups').innerHTML = renderGroupedStats(s.signal_groups||{}); renderWalletStructureBars('strategyWalletBars', s.wallet_groups||{}); $('strategyWalletGroups').innerHTML = renderGroupedStats(s.wallet_groups||{}); }
function renderCoverageDiagnostics(){ const d=DATA.coverage_diagnostics||{}, sync=d.paper_json_csv_sync||{}, safe=d.safety_defaults||{}; const plan=(d.wallet_missing_repair_plan||[]).map(x=>`<li>${fmt(x)}</li>`).join(''); $('coverageDiagnostics').innerHTML = `<div class="card"><div>钱包结构覆盖</div><strong>${fmt(d.wallet_coverage)}/${(DATA.kpi&&DATA.kpi.token_count)||0}</strong><small>未接入 ${fmt(d.wallet_missing_count)}｜${pct(d.wallet_missing_rate_pct)}</small></div><div class="card"><div>JSON/CSV 同步</div><strong>${sync.open_csv_exists&&sync.closed_csv_exists?'已检测':'待复查'}</strong><small>open JSON ${fmt(sync.open_json_count)} / closed JSON ${fmt(sync.closed_json_count)}</small></div><div class="card"><div>安全默认关闭</div><strong>${safe.real_swap_enabled===false&&safe.broadcast_allowed===false?'真实交易关闭':'需要复查'}</strong><small>不读取私钥 / 不签名 / 不广播</small></div><div class="card wide"><div>钱包结构缺口修复计划</div><ul>${plan||'<li>暂无缺口</li>'}</ul></div>`; }
function renderHealth(){ const h=DATA.system_health||{}; renderBars('health', h); }
function renderEvents(){ const ev = DATA.events || []; $('events').innerHTML = ev.length ? ev.slice().reverse().slice(0,30).map(e => `<div class="event"><time>${fmt(e.time)}</time><b>${fmt(e.event_type)}</b><span>${fmt(e.token_symbol || e.token_address)}</span><p>${fmt(e.message)}</p></div>`).join('') : '<p class="empty">暂无事件。</p>'; }
function renderAll(){ const meta=DATA.meta||DATA.metadata||{}; $('generatedAt').textContent = `生成时间：${fmt(meta.generated_at)}`; $('refreshInfo').textContent = `自动刷新：60 秒 / 刷新时间：${new Date().toLocaleString()}`; $('boundary').textContent = meta.boundary; renderKpi(); renderMethodology(); renderFunnel(); renderOpportunities(); fillFilters(); renderTable(); renderBars('entryReasons', DATA.entry_block_reasons); renderBars('walletReasons', DATA.wallet_missing_reasons); renderPaperSummary(); renderStrategyPanel(); renderPositions(); renderCoverageDiagnostics(); renderHealth(); renderEvents(); }
async function loadData(){ DATA = await fetch('dashboard_data.json', {cache:'no-store'}).then(r=>r.json()); renderAll(); }
async function main(){ await loadData(); ['searchInput','reasonInput','stateFilter','walletFilter','paperFilter'].forEach(id => $(id).addEventListener('input', renderTable)); $('sortByPriority').addEventListener('click', ()=>{ SORT_DESC=!SORT_DESC; renderTable(); }); $('closeDetail').addEventListener('click', ()=>$('tokenDetail').classList.remove('open')); setInterval(loadData, 60000); }
main().catch(err => { document.body.innerHTML = `<pre>控制台加载失败：${err.stack || err}</pre>`; });
"""
    app = app.replace("__STATE_LABELS__", json.dumps(STATE_LABELS, ensure_ascii=False))
    css = r""":root{--bg:#08111f;--panel:#101b2d;--panel2:#13243a;--text:#e5eefc;--muted:#8fa3bd;--line:#213650;--green:#28d17c;--cyan:#2dd4bf;--yellow:#f5c84c;--red:#ff5d6c;--purple:#bb7cff;--gray:#6b7280}*{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#07101d,#0b1220 42%,#080d16);color:var(--text);font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}.sidebar{position:fixed;inset:0 auto 0 0;width:220px;padding:22px;background:#07101d;border-right:1px solid var(--line);z-index:10}.brand{font-weight:900;font-size:20px;margin-bottom:24px}.brand span{color:var(--cyan);font-size:13px}.sidebar a{display:block;color:var(--muted);text-decoration:none;padding:10px;border-radius:10px}.sidebar a:hover{background:#102036;color:var(--text)}.shell{margin-left:220px}.hero{display:flex;justify-content:space-between;gap:20px;align-items:flex-end;padding:28px 32px;border-bottom:1px solid var(--line);background:radial-gradient(circle at 20% 0,#173a5f,transparent 40%)}h1{margin:.2rem 0;font-size:30px}h2{margin:0 0 16px}h3,h4{margin:14px 0 8px}.eyebrow,.meta,small,.hint{color:var(--muted)}main{padding:24px 32px}.grid{display:grid;gap:14px}.cards{grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-bottom:18px}.two{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}.card,.panel,.opp,.position,.detail-drawer{background:rgba(16,27,45,.92);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.22)}.card strong{display:block;font-size:25px;margin-top:8px}.panel{margin:18px 0}.section-head{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}.filters{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}input,select,button{background:#0b1424;color:var(--text);border:1px solid var(--line);border-radius:10px;padding:9px 10px}.bar-row{display:grid;grid-template-columns:180px 1fr 48px;gap:12px;align-items:center;margin:10px 0}.bar{height:10px;background:#0a1322;border-radius:999px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--cyan),var(--green));border-radius:999px}.opportunities{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.opp,.table-wrap tr{cursor:pointer}.opp p{color:var(--muted);min-height:38px}.badge{display:inline-block;padding:3px 8px;border-radius:999px;font-size:12px;font-weight:700;margin:1px;background:#1d2a3c;color:var(--muted)}.badge.good{background:rgba(40,209,124,.14);color:var(--green)}.badge.support{background:rgba(45,212,191,.14);color:var(--cyan)}.badge.warn{background:rgba(245,200,76,.14);color:var(--yellow)}.badge.bad{background:rgba(255,93,108,.14);color:var(--red)}.badge.error{background:rgba(187,124,255,.14);color:var(--purple)}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;min-width:1200px}th,td{border-bottom:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}th{color:var(--muted);font-size:12px}td small{display:block}.reason{max-width:280px}.positions{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.event{border-left:3px solid var(--cyan);padding:8px 12px;margin:8px 0;background:rgba(255,255,255,.03)}.event time{display:block;color:var(--muted);font-size:12px}.empty{color:var(--muted)}.detail-drawer{position:fixed;right:24px;top:24px;bottom:24px;width:min(460px,calc(100vw - 48px));overflow:auto;transform:translateX(calc(100% + 40px));transition:.2s;z-index:20}.detail-drawer.open{transform:translateX(0)}code{color:var(--cyan);word-break:break-all}.method-stages{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.stage-card,.rule,.stage-evidence article{background:rgba(19,36,58,.86);border:1px solid var(--line);border-radius:14px;padding:14px}.stage-card h3{color:var(--cyan)}.stage-card details{margin-top:10px}.stage-card summary{cursor:pointer;color:var(--yellow);font-weight:700}.rule-list{display:grid;gap:10px}.rule h4{color:var(--yellow)}.rule ul,.stage-card ul{margin:8px 0 0 18px;padding:0;color:var(--muted)}.stage-evidence{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0 16px}.stage-evidence article b{display:block;color:var(--cyan)}.stage-evidence article span{display:block;margin:6px 0;font-weight:700}.stage-evidence article small{color:var(--muted)}@media(max-width:900px){.sidebar{position:static;width:auto}.shell{margin-left:0}.hero{display:block}main{padding:16px}.two{grid-template-columns:1fr}.bar-row{grid-template-columns:1fr}.section-head{display:block}.filters{margin-top:10px}}"""
    (output_dir / "index.html").write_text(index, encoding="utf-8")
    (output_dir / "app.js").write_text(app, encoding="utf-8")
    (output_dir / "style.css").write_text(css, encoding="utf-8")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SIKK static dashboard site files.")
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run", help="SIKK live output root")
    parser.add_argument("--output-dir", default="data/gmgn_candidates_live_run/site", help="Static site output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path(args.base_dir)
    output_dir = Path(args.output_dir)
    data = build_dashboard_data(base_dir)
    write_site_files(output_dir, data)
    print(json.dumps({
        "status": "ok",
        "boundary": DASHBOARD_BOUNDARY,
        "output_dir": str(output_dir),
        "token_count": len(data.get("tokens", [])),
        "site_files": ["dashboard_data.json", "index.html", "app.js", "style.css"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
