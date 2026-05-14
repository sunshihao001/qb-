#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Live Run 主入口。

把已实现的候选发现、K线信号、钱包结构、quote/security、状态机、paper runner、
日报与 Runtime 可观测输出收敛到一条稳定主流程。默认纸面/只读/观测，不执行真实 swap。
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional

from run_sikk_gmgn_pipeline import _default_wallet_address, run_full_pipeline
from sikk_dashboard_builder import write_dashboard
from sikk_dashboard_site_builder import build_dashboard_data as build_site_dashboard_data, write_site_files as write_static_site_files
from sikk_live_orchestrator import write_live_board as write_professional_live_board
from sikk_market_cap_context import build_market_cap_context, merge_market_cap_context
from sikk_paper_live_runner import run_paper_live_cycle
from sikk_paper_explanation_builder import build_case_files
from sikk_operator_psychology_engine import enrich_status_with_operator_psychology
from sikk_wallet_structure_daily_report import build_wallet_structure_daily_report
from sikk_unified_view_builder import build_unified_indexes

DEFAULT_OUTPUT_ROOT = Path("data/gmgn_candidates_live_run")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _send_message_tool(*, target: str, message: str) -> None:
    """Placeholder for in-process Hermes sender.

    Plain project scripts cannot access the live Hermes tool bus directly. Production
    loop broadcasts are therefore sent by the assistant/session tool when starting or
    polling the process. Tests inject `message_sender` to verify formatting.
    """

    raise RuntimeError("Hermes in-process send_message is unavailable in plain Python; use external send_message tool or configure a bot notifier.")


def report_date_from_now(now: str) -> str:
    return now[:10].replace("-", "") if now else datetime.now(timezone.utc).strftime("%Y%m%d")


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def _append_jsonl(path: str | Path, row: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(row), ensure_ascii=False) + "\n")
    return str(p)


def build_runtime_candidates_from_state_file(candidate_states_path: str | Path) -> List[Dict[str, Any]]:
    """从状态机输出构建 runtime 展示候选；优先使用 `候选状态`。"""

    payload = _read_json(candidate_states_path)
    rows = payload.get("候选状态") or payload.get("candidates") or payload.get("tokens") or []
    return [dict(row) for row in rows] if isinstance(rows, list) else []


def _token_address(row: Mapping[str, Any]) -> str:
    return str(row.get("代币地址") or row.get("token_address") or row.get("token") or "")


def _token_symbol(row: Mapping[str, Any]) -> str:
    return str(row.get("代币符号") or row.get("token_symbol") or row.get("symbol") or "")


def _status_from_state_row(row: Mapping[str, Any], now: str) -> Dict[str, Any]:
    current_state = str(row.get("当前状态") or row.get("current_state") or "UNKNOWN")
    wallet_status = row.get("钱包结构结论") or row.get("wallet_structure_status") or "UNKNOWN"
    return {
        "token_address": _token_address(row),
        "token_symbol": _token_symbol(row),
        "current_state": current_state,
        "priority_level": row.get("优先级") or row.get("priority_level"),
        "last_update": now,
        "latest_action": row.get("下一步动作") or row.get("next_action") or "LIVE_RUN_SYNC",
        "latest_reason": str(row.get("状态原因") or row.get("latest_reason") or row.get("钱包结构原因") or "主入口同步状态机、纸面交易与日报输出"),
        "wallet_structure": {
            "wallet_structure_status": wallet_status,
            "wallet_structure_score": row.get("钱包结构评分") or row.get("wallet_structure_score"),
            "wallet_risk_score": row.get("钱包风险评分") or row.get("wallet_risk_score"),
            "counterparty_pressure_score": row.get("对手盘压力评分") or row.get("counterparty_pressure_score"),
            "data_quality_score": row.get("数据质量评分") or row.get("data_quality_score"),
            "missing_reason": row.get("钱包结构缺失原因") or row.get("wallet_missing_reason"),
        },
        "trade_gate": {
            "final_status": row.get("交易门控状态") or row.get("trade_gate_status") or row.get("final_status") or "未接入",
            "decision": row.get("交易门控决策") or row.get("trade_gate_decision") or row.get("decision"),
            "permission": row.get("交易权限") or row.get("permission"),
            "contract_permission": row.get("合约门控权限") or row.get("contract_permission"),
            "real_trade_enabled": bool(row.get("真实交易允许") is True or row.get("real_trade_enabled") is True),
            "execution_action": row.get("交易执行动作") or row.get("execution_action"),
            "funding_status": row.get("资金状态") or row.get("funding_status"),
            "risk_level": row.get("交易门控风险等级") or row.get("risk_level"),
            "reason_codes": row.get("交易门控原因码") or row.get("reason_codes") or [],
        },
        "lifecycle": {
            "dominant_side_lifecycle": row.get("主导侧生命周期") or row.get("dominant_side_lifecycle"),
            "dominant_side_intent": row.get("主导侧动机") or row.get("dominant_side_intent"),
            "counterparty_state": row.get("对手盘状态") or row.get("counterparty_state"),
            "liquidity_intent": row.get("流动性意图") or row.get("liquidity_intent"),
            "trap_risk_type": row.get("套牢风险类型") or row.get("trap_risk_type"),
            "structure_defense_status": row.get("结构防守状态") or row.get("structure_defense_status"),
        },
        "chip_control": {
            "chip_control_state": row.get("筹码控制权状态") or row.get("chip_control_state"),
            "chip_control_action": row.get("筹码控制权动作") or row.get("chip_control_action"),
        },
        "signal": {"signal_level": row.get("信号等级") or row.get("signal_level") or "UNKNOWN", "signal_gate": row.get("信号门禁") or row.get("signal_gate") or "UNKNOWN"},
        "quote": {"quote_gate": row.get("报价门禁") or row.get("quote_gate") or "MISSING"},
        "security": {"security_gate": row.get("安全门禁") or row.get("security_gate") or "MISSING"},
        "paper": {"paper_status": row.get("纸面状态") or row.get("paper_status") or "NONE", "unrealized_pnl_pct": row.get("纸面浮盈_pct") or row.get("paper_pnl_pct")},
        "scope_note": "token_status 只用于主流程观测与纸面验证，不执行真实 swap。",
    }


def _extract_rows(payload: Mapping[str, Any], keys: Iterable[str]) -> List[Dict[str, Any]]:
    for key in keys:
        rows = payload.get(key)
        if isinstance(rows, list):
            return [dict(row) for row in rows if isinstance(row, Mapping)]
    return []


def _index_rows_by_token(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    indexed: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        token = _token_address(row)
        if token:
            indexed[token] = dict(row)
    return indexed


def _okx_cluster_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    summary = _read_json(root / "okx_cluster" / "okx_cluster_summary.json")
    rows.extend(_extract_rows(summary, ("处理结果", "results", "decisions")))
    delta_summary = _read_json(root / "okx_cluster" / "okx_cluster_delta_summary.json")
    delta_by_token = _index_rows_by_token(_extract_rows(delta_summary, ("处理结果", "results", "deltas")))
    for path in sorted((root / "okx_cluster").glob("*/okx_cluster_decision.json")):
        payload = _read_json(path)
        if payload:
            rows.append(payload)
    indexed = _index_rows_by_token(rows)
    for token, delta in delta_by_token.items():
        row = indexed.get(token, {})
        row.update({
            "okx_cluster_delta": delta,
            "okx_cluster_failure_type": delta.get("okx_cluster_failure_type"),
            "recommended_paper_action": delta.get("recommended_paper_action"),
            "okx_cluster_delta_flags": delta.get("okx_cluster_delta_flags"),
            "largest_cluster_holding_pct_delta_round": delta.get("largest_cluster_holding_pct_delta_round"),
            "cluster_sync_sell_score_delta_round": delta.get("cluster_sync_sell_score_delta_round"),
            "okx_cluster_distribution_score_delta_round": delta.get("okx_cluster_distribution_score_delta_round"),
        })
        indexed[token] = row
    return indexed


def _quote_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    payload = _read_json(root / "quote_security" / "candidate_quote_security_summary.json")
    return _index_rows_by_token(_extract_rows(payload, ("处理结果", "quote_security_results", "results", "候选列表")))


def _open_paper_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    payload = _read_json(root / "paper_live" / "paper_positions_open.json")
    return _index_rows_by_token(_extract_rows(payload, ("open_positions", "开放仓位", "positions")))


def _closed_paper_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    payload = _read_json(root / "paper_live" / "paper_positions_closed.json")
    return _index_rows_by_token(_extract_rows(payload, ("closed_positions", "关闭仓位", "positions")))


def _failure_attribution_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in [
        root / "paper_live" / "failure_attribution.jsonl",
        *sorted((root / "okx_cluster").glob("*/okx_cluster_failure_attribution.jsonl")),
    ]:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except Exception:
                continue
            if isinstance(row, dict):
                rows.append(row)
    return _index_rows_by_token(rows)


def _trade_gate_rows(root: Path) -> Dict[str, Dict[str, Any]]:
    payload = _read_json(root / "trade_gate_runtime" / "trade_gate_runtime_summary.json")
    rows = _extract_rows(payload, ("处理结果", "trade_gate_results", "results", "tokens"))
    return _index_rows_by_token(rows)


def _merge_trade_gate_fields(status: Dict[str, Any], row: Mapping[str, Any]) -> None:
    trade_gate = status.get("trade_gate") if isinstance(status.get("trade_gate"), dict) else {}
    reason_codes = row.get("reason_codes") or row.get("交易门控原因码") or trade_gate.get("reason_codes") or []
    if isinstance(reason_codes, str):
        reason_codes = [reason_codes]
    trade_gate.update({
        "final_status": row.get("final_status") or row.get("交易门控状态") or trade_gate.get("final_status"),
        "decision": row.get("decision") or row.get("交易门控决策") or trade_gate.get("decision"),
        "permission": row.get("permission") or row.get("交易权限") or trade_gate.get("permission"),
        "contract_permission": row.get("contract_permission") or row.get("合约门控权限") or trade_gate.get("contract_permission"),
        "real_trade_enabled": bool(row.get("real_trade_enabled") is True or row.get("真实交易允许") is True or trade_gate.get("real_trade_enabled") is True),
        "execution_action": row.get("execution_action") or row.get("交易执行动作") or trade_gate.get("execution_action"),
        "funding_status": row.get("funding_status") or row.get("资金状态") or trade_gate.get("funding_status"),
        "risk_level": row.get("risk_level") or row.get("交易门控风险等级") or trade_gate.get("risk_level"),
        "reason_codes": reason_codes,
    })
    status["trade_gate"] = trade_gate


def _write_trade_gate_journal(root: Path, statuses: Iterable[Mapping[str, Any]], now: str) -> str:
    journal_path = root / "trade_gate_journal" / "trade_gate_review.jsonl"
    for status in statuses:
        trade_gate = status.get("trade_gate") if isinstance(status.get("trade_gate"), Mapping) else {}
        if not trade_gate or trade_gate.get("final_status") in {None, "", "未接入"}:
            continue
        _append_jsonl(journal_path, {
            "event_time": now,
            "token_address": status.get("token_address"),
            "token_symbol": status.get("token_symbol"),
            "current_state": status.get("current_state"),
            "latest_action": status.get("latest_action"),
            "decision": trade_gate.get("decision"),
            "final_status": trade_gate.get("final_status"),
            "permission": trade_gate.get("permission"),
            "contract_permission": trade_gate.get("contract_permission"),
            "real_trade_enabled": bool(trade_gate.get("real_trade_enabled") is True),
            "funding_status": trade_gate.get("funding_status"),
            "risk_level": trade_gate.get("risk_level"),
            "reason_codes": trade_gate.get("reason_codes") or [],
            "scope_note": "trade_gate_journal 只记录结构门控/纸面观察，不执行真实 swap。",
        })
    return str(journal_path)


def _quote_gate_from_row(row: Mapping[str, Any]) -> str:
    return str(row.get("最终权限") or row.get("final_permission") or row.get("quote_security_permission") or "MISSING")


def _security_gate_from_row(row: Mapping[str, Any]) -> str:
    return str(row.get("交易前状态") or row.get("pre_trade_state") or row.get("security_permission") or row.get("安全状态") or "MISSING")


def _paper_pnl(row: Mapping[str, Any]) -> Any:
    return row.get("unrealized_pnl_pct") if row.get("unrealized_pnl_pct") is not None else row.get("纸面浮盈_pct") or row.get("net_pnl_pct") or row.get("当前收益率_pct")


def _merge_paper_event_fields(status: Dict[str, Any], row: Mapping[str, Any], *, closed: bool = False) -> None:
    paper = status.get("paper") if isinstance(status.get("paper"), dict) else {}
    paper.update({
        "paper_entry_at": row.get("entry_time") or row.get("入场时间") or paper.get("paper_entry_at"),
        "paper_entry_price": row.get("entry_price") or row.get("入场价格") or paper.get("paper_entry_price"),
        "paper_entry_amount_sol": row.get("position_sol") or row.get("仓位SOL") or paper.get("paper_entry_amount_sol"),
        "paper_entry_amount_usd": row.get("position_usd") or row.get("仓位USD") or paper.get("paper_entry_amount_usd"),
        "paper_token_amount": row.get("token_amount") or row.get("代币数量") or paper.get("paper_token_amount"),
        "current_price": row.get("last_price") or row.get("exit_price") or row.get("当前价格") or paper.get("current_price"),
        "unrealized_pnl_sol": row.get("unrealized_pnl_sol") or row.get("net_pnl_sol") or paper.get("unrealized_pnl_sol"),
        "unrealized_pnl_pct": _paper_pnl(row),
        "exit_monitor_at": row.get("last_update_time") if row.get("wallet_position_action") == "EXIT_MONITOR" else paper.get("exit_monitor_at"),
        "failure_attribution_type": row.get("failure_type") or paper.get("failure_attribution_type"),
    })
    if closed:
        paper.update({
            "paper_status": "CLOSED",
            "paper_exit_at": row.get("exit_time") or row.get("退出时间") or paper.get("paper_exit_at"),
            "exit_reason": row.get("exit_reason") or row.get("退出原因") or paper.get("exit_reason"),
            "failure_attribution_type": row.get("failure_type") or paper.get("failure_attribution_type"),
        })
        status["current_state"] = "PAPER_EXITED"
    status["paper"] = paper


def _apply_latest_runtime_decision(status: Dict[str, Any]) -> None:
    paper_status = str((status.get("paper") or {}).get("paper_status") or "NONE").upper()
    quote_gate = str((status.get("quote") or {}).get("quote_gate") or "MISSING").upper()
    security_gate = str((status.get("security") or {}).get("security_gate") or "MISSING").upper()
    wallet_status = str((status.get("wallet_structure") or {}).get("wallet_structure_status") or "UNKNOWN").upper()
    trade_gate = status.get("trade_gate") if isinstance(status.get("trade_gate"), Mapping) else {}
    trade_final = str(trade_gate.get("final_status") or "").upper()
    trade_decision = str(trade_gate.get("decision") or "").upper()
    trade_permission = str(trade_gate.get("permission") or "").upper()
    trade_contract = str(trade_gate.get("contract_permission") or "").upper()
    current_state = str(status.get("current_state") or "UNKNOWN").upper()

    if trade_gate and trade_final not in {"", "未接入"}:
        if trade_final == "BLOCK" or "BLOCK_REAL_TRADE_AND_OBSERVE" in trade_permission or "BLOCK_REAL_TRADE_AND_OBSERVE" in trade_contract:
            status["priority_level"] = status.get("priority_level") or "P3_TRADE_GATE_BLOCKED"
            status["latest_action"] = "STRUCTURE_BLOCK"
            status["latest_reason"] = f"{status.get('latest_reason')}；交易门控：{trade_decision or trade_final} / {trade_contract or trade_permission}"
            return
        if trade_final in {"OBSERVE", "PAUSE", "PAUSED"} or trade_decision in {"OBSERVE_ONLY", "PAPER_ONLY"} or "PAUSE" in trade_contract:
            status["priority_level"] = status.get("priority_level") or "P2_STRUCTURE_OBSERVE"
            status["latest_action"] = "STRUCTURE_OBSERVE"
            status["latest_reason"] = f"{status.get('latest_reason')}；交易门控：{trade_decision or trade_final} / {trade_contract or trade_permission}"
            return

    if paper_status == "OPEN":
        status["priority_level"] = "P0_ACTIVE_POSITION"
        okx_cluster = status.get("okx_cluster") if isinstance(status.get("okx_cluster"), Mapping) else {}
        okx_action = str(okx_cluster.get("recommended_paper_action") or "").upper()
        okx_failure = str(okx_cluster.get("okx_cluster_failure_type") or "").upper()
        if okx_action == "FORCE_PAPER_EXIT":
            status["latest_action"] = "FORCE_PAPER_EXIT"
            status["latest_reason"] = f"{status.get('latest_reason')}；OKX集群归因：{okx_failure or 'CLUSTER_RISK'}（仅纸面退出/复盘）"
            return
        status["latest_action"] = "EXIT_MONITOR" if quote_gate in {"PAUSE_NEED_CONFIRM", "PAUSE", "MISSING", "ERROR", "BLOCK_BUY"} or security_gate in {"PAUSE", "PAUSE_NEED_CONFIRM", "BLOCK", "BLOCK_BUY", "MISSING", "ERROR"} or wallet_status == "WALLET_PAUSE" or okx_action == "EXIT_MONITOR" else "HOLD"
        return
    if current_state in {"PAPER_READY", "READY_FOR_CONFIRMATION"}:
        status["priority_level"] = status.get("priority_level") or "P1_PAPER_READY"
        status["latest_action"] = "OPEN_PAPER_POSITION" if quote_gate not in {"PAUSE_NEED_CONFIRM", "BLOCK_BUY", "MISSING", "ERROR"} else "WAIT_QUOTE"
    elif wallet_status == "WALLET_SUPPORT":
        status["priority_level"] = status.get("priority_level") or "P2_STRUCTURE_SUPPORT"
        status["latest_action"] = "WAIT_SIGNAL"


def build_enriched_runtime_statuses(root: str | Path, now: str) -> List[Dict[str, Any]]:
    """合并状态机、quote/security、paper-live 的证据，生成专业面板可直接消费的 token_status。"""
    base = Path(root)
    quote_by_token = _quote_rows(base)
    okx_cluster_by_token = _okx_cluster_rows(base)
    open_by_token = _open_paper_rows(base)
    closed_by_token = _closed_paper_rows(base)
    failure_by_token = _failure_attribution_rows(base)
    trade_gate_by_token = _trade_gate_rows(base)
    statuses: List[Dict[str, Any]] = []
    for row in build_runtime_candidates_from_state_file(base / "state_machine" / "candidate_states.json"):
        status = _status_from_state_row(row, now)
        token = status.get("token_address")
        quote_row = quote_by_token.get(str(token), {})
        okx_cluster_row = okx_cluster_by_token.get(str(token), {})
        trade_gate_row = trade_gate_by_token.get(str(token), {})
        if trade_gate_row:
            _merge_trade_gate_fields(status, trade_gate_row)
        if okx_cluster_row:
            status["okx_cluster"] = okx_cluster_row
        if quote_row:
            status["quote"] = {
                "quote_gate": _quote_gate_from_row(quote_row),
                "quote_security_reason": quote_row.get("说明") or quote_row.get("reason") or quote_row.get("状态原因"),
                "current_market_cap_usd": quote_row.get("current_market_cap_usd") or quote_row.get("当前市值USD") or quote_row.get("market_cap_usd"),
            }
            status["security"] = {"security_gate": _security_gate_from_row(quote_row)}
            reason = quote_row.get("说明") or quote_row.get("reason") or quote_row.get("状态原因")
            if reason:
                status["latest_reason"] = f"{status.get('latest_reason')}；quote/security：{reason}"
        paper_row = open_by_token.get(str(token), {})
        if paper_row:
            status["current_state"] = "PAPER_OPEN"
            status["paper"] = {
                "paper_status": "OPEN",
                "unrealized_pnl_pct": _paper_pnl(paper_row),
                "paper_entry_price_mode": paper_row.get("entry_price_mode") or paper_row.get("入场价格模式") or "live_or_signal_with_cost_model",
            }
            _merge_paper_event_fields(status, paper_row)
        closed_row = closed_by_token.get(str(token), {})
        if closed_row and not paper_row:
            _merge_paper_event_fields(status, closed_row, closed=True)
        failure_row = failure_by_token.get(str(token), {})
        if failure_row:
            paper = status.get("paper") if isinstance(status.get("paper"), dict) else {}
            paper["failure_attribution_type"] = failure_row.get("failure_type") or paper.get("failure_attribution_type")
            paper["okx_cluster_failure_type"] = failure_row.get("okx_cluster_failure_type") or paper.get("okx_cluster_failure_type")
            paper["recommended_paper_action"] = failure_row.get("recommended_paper_action") or paper.get("recommended_paper_action")
            paper["exit_reason"] = failure_row.get("failure_reason") or failure_row.get("原因") or paper.get("exit_reason")
            if failure_row.get("事件类型") == "EXIT_MONITOR":
                paper["exit_monitor_at"] = failure_row.get("事件时间") or paper.get("exit_monitor_at")
            status["paper"] = paper
        market_context = build_market_cap_context(
            discovery_row=row,
            signal_row={**row, **(status.get("signal") if isinstance(status.get("signal"), dict) else {})},
            wallet_row={**row, **(status.get("wallet_structure") if isinstance(status.get("wallet_structure"), dict) else {})},
            paper_row=status.get("paper") if isinstance(status.get("paper"), dict) else {},
            current_row={**row, **(status.get("quote") if isinstance(status.get("quote"), dict) else {}), **(status.get("paper") if isinstance(status.get("paper"), dict) else {})},
            exit_row=closed_row or failure_row,
        )
        merge_market_cap_context(status, market_context)
        _apply_latest_runtime_decision(status)
        status = enrich_status_with_operator_psychology(status)
        statuses.append(status)
    return statuses


def _write_token_status_files(root: Path, status: Mapping[str, Any]) -> Dict[str, str]:
    token = str(status.get("token_address") or "UNKNOWN")
    token_dir = root / "tokens" / token
    json_path = token_dir / "token_status.json"
    md_path = token_dir / "token_status.md"
    _write_json(json_path, status)
    wallet = status.get("wallet_structure", {}) if isinstance(status.get("wallet_structure"), Mapping) else {}
    signal = status.get("signal", {}) if isinstance(status.get("signal"), Mapping) else {}
    lines = [
        f"# Token 状态：{status.get('token_symbol') or '-'} / {status.get('token_address')}",
        "",
        f"- 当前状态：{status.get('current_state')}",
        f"- 更新时间：{status.get('last_update')}",
        f"- 最新动作：{status.get('latest_action')}",
        f"- 最新原因：{status.get('latest_reason')}",
        f"- 钱包结构：{wallet.get('wallet_structure_status')}",
        f"- 信号等级：{signal.get('signal_level')}",
        "- 边界：只做状态观测、纸面验证和复盘，不执行真实 swap。",
    ]
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"token_status_json": str(json_path), "token_status_md": str(md_path)}


def _write_live_state(root: Path, statuses: List[Mapping[str, Any]], now: str) -> str:
    return _write_json(root / "live_state.json", {"last_update": now, "token_count": len(statuses), "tokens": list(statuses), "scope_note": "Live state 不代表真实交易授权；以分阶段门禁和纸面验证为准。"})


def _write_live_board(root: Path, statuses: List[Mapping[str, Any]], now: str, paper_paths: Mapping[str, str], report_paths: Mapping[str, str]) -> str:
    return write_professional_live_board(statuses, base_dir=root, now=now)


def _write_static_dashboard_site(root: Path) -> Dict[str, str]:
    """刷新本地静态 dashboard site；仅写 site 目录，不改变运行/交易状态。"""

    site_dir = root / "site"
    data = build_site_dashboard_data(root)
    write_static_site_files(site_dir, data)
    return {
        "site_dashboard_data_json": str(site_dir / "dashboard_data.json"),
        "site_index_html": str(site_dir / "index.html"),
        "site_app_js": str(site_dir / "app.js"),
        "site_style_css": str(site_dir / "style.css"),
    }


def _write_latest_events(root: Path) -> str:
    events_path = root / "events" / "live_events.jsonl"
    md_path = root / "events" / "latest_events.md"
    rows: List[Mapping[str, Any]] = []
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines()[-20:]:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    lines = ["# SIKK 最新运行事件", "", "- 边界：事件只用于运行监控和纸面流程，不代表真实交易授权。", ""]
    for row in rows:
        lines.append(f"- {row.get('time')}｜{row.get('event_type')}｜{row.get('token_symbol') or '-'}｜{row.get('message')}")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(md_path)


def _format_broadcast_message(
    *,
    run_time: str,
    statuses: List[Mapping[str, Any]],
    paper_paths: Mapping[str, str],
    report_paths: Mapping[str, str],
    root: Path,
) -> str:
    from collections import Counter

    state_counts = Counter(str(row.get("current_state") or "UNKNOWN") for row in statuses)
    wallet_counts = Counter(str((row.get("wallet_structure") or {}).get("wallet_structure_status") or "UNKNOWN") for row in statuses)
    lines = [
        "## SIKK Live Run 广播",
        f"- 时间：{run_time}",
        f"- 输出目录：{root}",
        "- 边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实 swap。",
        "",
        "## 状态概览",
        f"- Token 数：{len(statuses)}",
    ]
    for state, count in sorted(state_counts.items()):
        lines.append(f"- {state}：{count}")
    lines.append("")
    lines.append("## 钱包结构")
    for status, count in sorted(wallet_counts.items()):
        lines.append(f"- {status}：{count}")
    lines.extend([
        "",
        "## 日报",
        f"- 纸面日报：{paper_paths.get('daily_report_md', '未生成')}",
        f"- 钱包结构日报：{report_paths.get('summary_md', '未生成')}",
        f"- Live Board：{root / 'live_board.md'}",
    ])
    return "\n".join(lines)


def _send_telegram_broadcast(
    *,
    enabled: bool,
    message: str,
    target: str,
    message_sender: Callable[..., Any],
    event_path: Path,
    run_time: str,
) -> None:
    if not enabled:
        return
    try:
        message_sender(target=target, message=message)
        _append_jsonl(event_path, {"time": run_time, "event_type": "TG_BROADCAST_SENT", "level": "INFO", "message": f"Telegram 广播已发送到 {target}"})
    except Exception as exc:  # pragma: no cover - defensive runtime path
        _append_jsonl(event_path, {"time": run_time, "event_type": "TG_BROADCAST_ERROR", "level": "ERROR", "message": str(exc)})


def _paper_position_rows_from_json(root: Path, filename: str, keys: Iterable[str]) -> List[Dict[str, Any]]:
    payload = _read_json(root / "paper_live" / filename)
    if not payload:
        return []
    rows = _extract_rows(payload, keys)
    if rows:
        return rows
    if isinstance(payload, list):
        return [dict(row) for row in payload if isinstance(row, Mapping)]
    return []

PAPER_POSITION_CSV_FIELDS = [
    "position_id", "token_address", "token_symbol", "代币地址", "代币符号", "status",
    "paper_entry_time", "entry_time", "paper_entry_price", "entry_price", "entry_quote_source",
    "paper_size_sol", "position_sol", "paper_size_usd", "estimated_token_amount",
    "candidate_discovered_at", "discovery_market_cap_usd", "signal_time", "signal_level", "signal_type",
    "signal_market_cap_usd", "wallet_decision_time", "wallet_structure_status", "wallet_structure_score",
    "wallet_risk_score", "counterparty_pressure_score", "data_quality_score",
    "entry_market_cap_usd", "entry_liquidity_usd", "entry_holder_count",
    "entry_delay_from_discovery_sec", "entry_delay_from_signal_sec",
    "entry_market_cap_change_from_discovery_pct", "entry_market_cap_change_from_signal_pct",
    "market_cap_context_status", "wallet_exit_action", "wallet_exit_trigger_time", "wallet_exit_trigger_type",
    "shadow_hold_tracking", "shadow_hold_price_15m", "shadow_hold_price_30m", "shadow_hold_price_60m",
    "missed_profit_pct", "avoided_drawdown_pct", "false_exit_flag", "最终收益率_pct", "exit_reason",
]


def _write_rows_csv(path: Path, rows: List[Mapping[str, Any]], default_fieldnames: Optional[List[str]] = None) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for key in default_fieldnames or []:
        key_str = str(key)
        if key_str not in fieldnames:
            fieldnames.append(key_str)
    for row in rows:
        for key in row:
            key_str = str(key)
            if key_str not in fieldnames:
                fieldnames.append(key_str)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        if not fieldnames:
            f.write("")
            return str(path)
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({str(key): value for key, value in row.items()})
    return str(path)


def sync_paper_position_csvs(root: str | Path) -> Dict[str, str]:
    """从 paper_positions_open/closed.json 重建 CSV，避免日报/面板读取旧表。

    JSON 是 paper live runner 的权威仓位源；每轮主流程结束后强制重建 CSV。
    本函数只做文件格式同步，不改变 paper 仓位、不执行真实 swap。
    """

    base = Path(root)
    open_rows = _paper_position_rows_from_json(base, "paper_positions_open.json", ("open_positions", "开放仓位", "positions"))
    closed_rows = _paper_position_rows_from_json(base, "paper_positions_closed.json", ("closed_positions", "关闭仓位", "positions"))
    paper_dir = base / "paper_live"
    return {
        "open_positions_csv": _write_rows_csv(paper_dir / "paper_positions_open.csv", open_rows, PAPER_POSITION_CSV_FIELDS),
        "closed_positions_csv": _write_rows_csv(paper_dir / "paper_positions_closed.csv", closed_rows, PAPER_POSITION_CSV_FIELDS),
    }


def _paper_closed_csv_path(root: Path) -> Path:
    return Path(sync_paper_position_csvs(root)["closed_positions_csv"])


def run_live_once(
    *,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    config_path: str | Path = "config/token_filter_config.json",
    limit: Optional[int] = None,
    include_s2: bool = False,
    quote_sources: tuple[str, ...] = ("okx",),
    default_quote_amount_sol: float = 0.01,
    wallet_address: str = "",
    use_position_amount: bool = False,
    force: bool = False,
    telegram_broadcast: bool = False,
    telegram_target: str = "telegram",
    message_sender: Callable[..., Any] = _send_message_tool,
    now: Optional[str] = None,
    pipeline_runner: Callable[..., Dict[str, str]] = run_full_pipeline,
    paper_runner: Callable[..., Dict[str, str]] = run_paper_live_cycle,
) -> Dict[str, str]:
    """运行一轮稳定主流程并写出统一观测文件。"""

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    run_time = now or iso_now()

    config = {
        "notification_enabled": telegram_broadcast,
        "telegram_broadcast_enabled": telegram_broadcast,
        "telegram_target": telegram_target if telegram_broadcast else "",
        "confirmation_enabled": False,
        "real_swap_enabled": False,
        "broadcast_allowed": False,
        "dashboard_enabled": True,
        "trace_enabled": True,
    }

    event_path = root / "events" / "live_events.jsonl"
    _append_jsonl(event_path, {"time": run_time, "event_type": "LIVE_RUN_STARTED", "level": "INFO", "message": "SIKK 主入口开始运行", "scope_note": "不执行真实 swap。"})

    pipeline_paths = pipeline_runner(
        output_root=root,
        config_path=config_path,
        limit=limit,
        include_s2=include_s2,
        run_quote_security=True,
        quote_sources=quote_sources,
        default_quote_amount_sol=default_quote_amount_sol,
        wallet_address=wallet_address,
        use_position_amount=use_position_amount,
    )

    state_path = root / "state_machine" / "candidate_states.json"
    signal_path = root / "candidate_signal_outputs" / "candidate_signal_summary.json"
    quote_path = root / "quote_security" / "candidate_quote_security_summary.json"
    wallet_structure_dir = root / "wallet_structure"

    paper_paths = paper_runner(
        candidate_states_path=state_path,
        signal_summary_path=signal_path,
        quote_security_summary_path=quote_path,
        output_dir=root / "paper_live",
        wallet_structure_dir=wallet_structure_dir,
    )
    paper_paths = {**paper_paths, **sync_paper_position_csvs(root)}
    paper_case_paths = build_case_files(paper_dir=root / "paper_live", base_dir=root, output_dir=root / "paper_live" / "case_files")
    paper_paths = {**paper_paths, **paper_case_paths}

    report_paths = build_wallet_structure_daily_report(
        closed_positions_path=Path(paper_paths["closed_positions_csv"]),
        failure_attribution_path=root / "paper_live" / "failure_attribution.jsonl",
        output_dir=root / "reports",
        report_date=report_date_from_now(run_time),
    )

    statuses = build_enriched_runtime_statuses(root, run_time)
    token_status_md = ""
    for status in statuses:
        paths = _write_token_status_files(root, status)
        token_status_md = token_status_md or paths["token_status_md"]
        _append_jsonl(root / "tokens" / str(status.get("token_address")) / "process_trace.jsonl", {
            "time": run_time,
            "previous_state": None,
            "current_state": status.get("current_state"),
            "latest_action": status.get("latest_action"),
            "latest_reason": status.get("latest_reason"),
            "scope_note": "process_trace 只记录主流程状态变化，不执行真实 swap。",
        })

    live_state = _write_live_state(root, statuses, run_time)
    trade_gate_journal = _write_trade_gate_journal(root, statuses, run_time)
    live_board = _write_live_board(root, statuses, run_time, paper_paths, report_paths)
    dashboard = write_dashboard(base_dir=root)
    site_paths: Dict[str, str] = {}
    try:
        site_paths = _write_static_dashboard_site(root)
    except Exception as exc:  # pragma: no cover - defensive runtime path
        _append_jsonl(event_path, {"time": run_time, "event_type": "STATIC_DASHBOARD_SITE_ERROR", "level": "ERROR", "message": str(exc), "scope_note": "site 生成失败不影响主流程；不执行真实 swap。"})
    latest_events = _write_latest_events(root)
    unified_paths: Dict[str, str] = {}
    try:
        unified_result = build_unified_indexes(root)
        unified_paths = {
            "unified_index_dir": unified_result.get("index_dir", ""),
            "telegram_callback_index_json": str(root / "index" / "telegram_callback_index.json"),
            "system_index_json": str(root / "index" / "system_index.json"),
        }
    except Exception as exc:  # pragma: no cover - defensive runtime path
        _append_jsonl(event_path, {"time": run_time, "event_type": "UNIFIED_INDEX_REFRESH_ERROR", "level": "ERROR", "message": str(exc), "scope_note": "统一索引刷新失败不影响主流程；不执行真实 swap。"})

    _append_jsonl(event_path, {"time": run_time, "event_type": "LIVE_RUN_FINISHED", "level": "INFO", "message": "SIKK 主入口完成一轮运行", "scope_note": "不执行真实 swap。"})

    broadcast_message = _format_broadcast_message(run_time=run_time, statuses=statuses, paper_paths=paper_paths, report_paths=report_paths, root=root)
    _send_telegram_broadcast(
        enabled=telegram_broadcast,
        message=broadcast_message,
        target=telegram_target,
        message_sender=message_sender,
        event_path=event_path,
        run_time=run_time,
    )

    manifest = {
        "模块": "SIKK Live Run 主入口",
        "模式": "paper_runtime_once",
        "运行时间": run_time,
        "输出根目录": str(root),
        "配置": config,
        "分阶段流程": [
            {"阶段": "P0_候选发现", "目标": "GMGN 新币候选池，只筛选不下单", "输出": "gmgn_new_token_filter/token_candidates.*", "完成标准": "候选等级 S1/S2/S3 与排除原因完整"},
            {"阶段": "P1_K线吸筹与信号", "目标": "K线、吸筹窗口、SIKK S0-S4/SX 信号", "输出": "candidate_signal_outputs/", "完成标准": "PAPER_READY 必须来自 S3/S4 + 风险门禁通过"},
            {"阶段": "P2_钱包结构门禁", "目标": "observe 默认记录钱包结构，不直接实盘授权", "输出": "wallet_structure/", "完成标准": "WALLET_SUPPORT 只表示不阻断；WALLET_BLOCK/PAUSE 可进入观察或阻断"},
            {"阶段": "P3_报价安全确认", "目标": "只读 quote + token-scan + confirmation ticket", "输出": "quote_security/", "完成标准": "缺 quote/scan 一律 PAUSE，不当作安全"},
            {"阶段": "P4_live纸面交易", "目标": "live 入场价/成本模型/纸面仓位更新", "输出": "paper_live/", "完成标准": "记录 signal/live 价差、滑点、费用和 paper PnL"},
            {"阶段": "P5_复盘校准", "目标": "日报、失败归因、钱包结构状态胜率统计", "输出": "reports/", "完成标准": "按 wallet_structure_status/failure_type 复盘"},
            {"阶段": "P6_人工确认后小额实盘准备", "目标": "仅生成确认层与执行前门禁，不自动广播", "输出": "confirmation/execution_gate", "完成标准": "必须人工确认，real_swap/broadcast 默认关闭"},
        ],
        "当前不足修正": {
            "默认入场价": "live优先，缺失时降级signal并标记偏差",
            "钱包结构": "observe默认接入，soft/hard需显式启用",
            "quote安全": "缺失/过期/偏差过大一律 PAUSE 或 BLOCK",
            "纸面验证": "先连续多轮统计，再考虑人工确认小额实盘",
            "真实交易": "默认关闭，只生成确认层，不广播",
        },
        "阶段输出": {
            "pipeline": pipeline_paths,
            "paper_live": paper_paths,
            "wallet_structure_daily_report": report_paths,
            "runtime": {
                "live_state_json": live_state,
                "live_board_md": live_board,
                "live_dashboard_html": dashboard,
                "trade_gate_journal_jsonl": trade_gate_journal,
                **site_paths,
                "events_jsonl": str(event_path),
                "latest_events_md": latest_events,
                "token_status_md": token_status_md,
                **unified_paths,
            },
        },
        "说明": "统一主入口只做候选发现、K线/钱包结构/quote-security、纸面交易、状态观测和日报复盘，不执行真实 swap。notification/confirmation/real swap 默认关闭。",
    }
    manifest_path = _write_json(root / "live_run_manifest.json", manifest)

    return {
        "output_root": str(root),
        "live_run_manifest_json": manifest_path,
        "live_state_json": live_state,
        "live_board_md": live_board,
        "live_dashboard_html": dashboard,
        "trade_gate_journal_jsonl": trade_gate_journal,
        **site_paths,
        "events_jsonl": str(event_path),
        "latest_events_md": latest_events,
        "paper_daily_report_md": paper_paths.get("daily_report_md", ""),
        "wallet_daily_report_md": report_paths.get("summary_md", ""),
        "token_status_md": token_status_md,
        **unified_paths,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK Live Run 主入口（纸面/只读/不执行真实 swap）")
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--config", default="config/token_filter_config.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-s2", action="store_true")
    parser.add_argument("--quote-sources", default="okx")
    parser.add_argument("--default-quote-amount-sol", type=float, default=0.01)
    parser.add_argument("--wallet-address", default=_default_wallet_address())
    parser.add_argument("--use-position-amount", action="store_true")
    parser.add_argument("--interval-sec", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--telegram-broadcast", action="store_true", help="每轮完成后向 Telegram home channel 广播运行摘要")
    parser.add_argument("--telegram-target", default="telegram", help="Hermes send_message 目标，默认 telegram home channel")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    quote_sources = tuple(source.strip() for source in args.quote_sources.split(",") if source.strip()) or ("okx",)
    while True:
        paths = run_live_once(
            output_root=args.output_root,
            config_path=args.config,
            limit=args.limit,
            include_s2=args.include_s2,
            quote_sources=quote_sources,
            default_quote_amount_sol=args.default_quote_amount_sol,
            wallet_address=args.wallet_address,
            use_position_amount=args.use_position_amount,
            force=args.force,
            telegram_broadcast=args.telegram_broadcast,
            telegram_target=args.telegram_target,
        )
        print(json.dumps(paths, ensure_ascii=False, indent=2))
        if args.mode == "once":
            break
        time.sleep(args.interval_sec)


if __name__ == "__main__":
    main()
