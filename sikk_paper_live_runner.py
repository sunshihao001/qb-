#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Paper Live Runner v0.9.

用 OKX/GMGN 只读报价与 SIKK 候选状态做纸面自动交易实盘演练：
- 自动读取 PAPER_READY / READY_FOR_CONFIRMATION 候选；
- 只做纸面入场、纸面持仓更新、纸面退出；
- 不执行真实 swap，不签名，不广播，不托管私钥。
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

PriceProvider = Callable[[str], Dict[str, Any]]
Runner = Callable[[List[str]], str]


_FORBIDDEN_COMMAND_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "order strategy create",
    "onchainos swap execute",
]


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: str | Path | None, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if default is None:
        default = {}
    if not path:
        return default
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]], default_fieldnames: Optional[List[str]] = None) -> None:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for name in default_fieldnames or []:
        if name not in fieldnames:
            fieldnames.append(name)
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        p.write_text("", encoding="utf-8")
        return
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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

PAPER_TRADE_CSV_FIELDS = [
    "trade_id", "position_id", "token_address", "token_symbol", "side", "event_type", "trade_time",
    "price", "market_cap_usd", "liquidity_usd", "size_sol", "size_usd", "token_amount",
    "slippage_pct", "fee_sol", "quote_source", "reason",
    "事件时间", "事件类型", "代币地址", "代币符号", "价格", "仓位SOL", "原因",
]


def _append_jsonl(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        if not p.exists():
            p.write_text("", encoding="utf-8")
        return
    with p.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default




def _parse_iso_time(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        text = str(value)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _seconds_between(start: Any, end: Any) -> Optional[int]:
    a = _parse_iso_time(start)
    b = _parse_iso_time(end)
    if not a or not b:
        return None
    return int((b - a).total_seconds())


def _pct_change(new: Any, old: Any) -> Optional[float]:
    old_f = _to_float(old, 0.0)
    new_f = _to_float(new, 0.0)
    if old_f <= 0 or new_f <= 0:
        return None
    return round((new_f - old_f) / old_f * 100.0, 4)


def _market_cap_context_status(change_pct: Any) -> str:
    if change_pct is None:
        return "UNKNOWN_ENTRY"
    value = _to_float(change_pct, 0.0)
    if value < 50:
        return "EARLY_ENTRY"
    if value <= 150:
        return "NORMAL_ENTRY"
    if value <= 300:
        return "LATE_ENTRY"
    return "CHASE_ENTRY"


def _first_non_empty(*values: Any, default: Any = None) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return default


def _state_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("候选状态")
    return rows if isinstance(rows, list) else []


def _signal_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("信号结果")
    return rows if isinstance(rows, list) else []


def _quote_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("处理结果") or payload.get("results")
    return rows if isinstance(rows, list) else []


def _index_by_token(rows: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        token = str(row.get("代币地址") or row.get("token") or row.get("address") or "")
        if token:
            index[token] = row
    return index


def _readiness_path(row: Dict[str, Any]) -> str:
    outputs = row.get("自动准备输出") or row.get("outputs") or {}
    if isinstance(outputs, dict):
        return str(outputs.get("json") or outputs.get("readiness_json") or "")
    return ""


def _load_open_positions(output_dir: Path) -> List[Dict[str, Any]]:
    payload = _read_json(output_dir / "paper_positions_open.json", {"open_positions": []})
    rows = payload.get("open_positions", [])
    return rows if isinstance(rows, list) else []


def _load_closed_positions(output_dir: Path) -> List[Dict[str, Any]]:
    payload = _read_json(output_dir / "paper_positions_closed.json", {"closed_positions": []})
    rows = payload.get("closed_positions", [])
    return rows if isinstance(rows, list) else []


def _load_wallet_structure_runtime_inputs(token: str, wallet_structure_dir: str | Path | None) -> tuple[Dict[str, Any], Dict[str, Any]]:
    if not wallet_structure_dir:
        return {}, {}
    base = Path(wallet_structure_dir) / token
    decision = _read_json(base / "wallet_structure_decision.json")
    delta = _read_json(base / "snapshots" / "latest_delta.json")
    return decision, delta


def _close_position_for_wallet_action(position: Dict[str, Any], current_price: float, snapshot_time: str, action: Dict[str, Any]) -> Dict[str, Any]:
    entry_price = _to_float(position.get("entry_price"), 0.0)
    closed = dict(position)
    pnl = round((current_price - entry_price) / entry_price * 100.0, 4) if entry_price > 0 else 0.0
    closed.update({
        "status": "CLOSED",
        "exit_time": snapshot_time,
        "exit_price": current_price,
        "exit_reason": "钱包结构触发纸面强制退出",
        "最终收益率_pct": pnl,
        "wallet_position_action": action.get("action"),
        "failure_type": action.get("failure_type"),
        "failure_reason": action.get("reason"),
        "wallet_exit_trigger_time": snapshot_time,
        "wallet_exit_trigger_type": action.get("failure_type"),
        "wallet_exit_trigger_score": action.get("trigger_score") or action.get("wallet_risk_score"),
        "wallet_exit_action": action.get("action"),
        "force_exit_price": current_price,
        "shadow_hold_tracking": True,
        "shadow_hold_price_15m": None,
        "shadow_hold_price_30m": None,
        "shadow_hold_price_60m": None,
        "shadow_hold_max_profit_after_exit": None,
        "shadow_hold_max_drawdown_after_exit": None,
        "false_exit_flag": None,
        "avoided_drawdown_pct": None,
        "missed_profit_pct": None,
        "scope_note": "钱包结构触发纸面退出；不执行真实 swap。",
    })
    return closed


def _failure_attribution_row(position: Dict[str, Any], action: Dict[str, Any], snapshot_time: str) -> Dict[str, Any]:
    return {
        "事件时间": snapshot_time,
        "事件类型": action.get("action"),
        "代币地址": position.get("代币地址"),
        "代币符号": position.get("代币符号", ""),
        "failure_type": action.get("failure_type"),
        "failure_reason": action.get("reason"),
        "wallet_structure_status": position.get("wallet_structure_status"),
        "wallet_structure_score": position.get("wallet_structure_score"),
        "wallet_risk_score": position.get("wallet_risk_score"),
        "counterparty_pressure_score": position.get("counterparty_pressure_score"),
        "scope_note": "failure attribution 用于纸面复盘，不执行真实 swap。",
    }


def _extract_exit_plan(signal_row: Dict[str, Any]) -> Dict[str, Any]:
    readiness = _read_json(_readiness_path(signal_row))
    exit_plan = readiness.get("exit_plan") if isinstance(readiness, dict) else None
    if not isinstance(exit_plan, dict):
        exit_plan = {}
    position_plan = readiness.get("position_plan") if isinstance(readiness, dict) else None
    if isinstance(position_plan, dict) and not exit_plan.get("hard_stop_price"):
        exit_plan["hard_stop_price"] = position_plan.get("stop_price")
    return exit_plan


def _entry_allowed(state: Dict[str, Any], quote: Dict[str, Any]) -> tuple[bool, str]:
    current_state = str(state.get("当前状态") or "")
    trade_state = str(quote.get("交易前状态") or "")
    final_permission = str(quote.get("最终权限") or quote.get("final_permission") or quote.get("quote_security_permission") or "")
    if current_state != "PAPER_READY":
        return False, "不是 PAPER_READY"
    if quote:
        if trade_state == "BLOCK" or final_permission == "BLOCK_BUY":
            return False, "报价/安全扫描阻断 BLOCK_BUY"
        if trade_state == "PAUSE" or final_permission == "PAUSE_NEED_CONFIRM":
            return False, "报价/安全扫描暂停，需人工确认"
        if trade_state not in {"READY_FOR_CONFIRMATION", ""} or final_permission not in {"ALLOW_CONFIRMATION_LAYER", ""}:
            return False, "报价/安全扫描未允许进入确认层"
    return True, "满足纸面入场条件"


def _default_cost_model() -> Dict[str, float]:
    return {
        "buy_slippage_pct": 3.0,
        "sell_slippage_pct": 3.0,
        "dex_fee_pct": 0.25,
        "quote_deviation_buffer_pct": 1.0,
        "priority_fee_sol": 0.0005,
        "failed_tx_cost_sol": 0.0002,
    }


def _cost_buffer_pct(cost_model: Dict[str, float]) -> float:
    return round(
        _to_float(cost_model.get("buy_slippage_pct"))
        + _to_float(cost_model.get("sell_slippage_pct"))
        + _to_float(cost_model.get("dex_fee_pct"))
        + _to_float(cost_model.get("quote_deviation_buffer_pct")),
        4,
    )


def _new_position(
    *,
    token: str,
    state: Dict[str, Any],
    signal: Dict[str, Any],
    quote: Dict[str, Any],
    price_info: Dict[str, Any],
    snapshot_time: str,
) -> Dict[str, Any]:
    # 最新认知：纸面入场默认使用 live 价格；信号价作为基准证据，必须记录价差，避免历史信号价高估收益。
    signal_entry_price = _to_float(signal.get("信号价格"), 0.0) or _to_float(state.get("信号价格"), 0.0)
    live_entry_price = _to_float(price_info.get("price"), 0.0)
    if live_entry_price > 0:
        entry_price_mode = "live"
        entry_price = live_entry_price
    else:
        entry_price_mode = "signal_fallback"
        entry_price = signal_entry_price
    if entry_price <= 0:
        entry_price = signal_entry_price or live_entry_price
    entry_price_diff_pct = round((live_entry_price - signal_entry_price) / signal_entry_price * 100.0, 4) if signal_entry_price > 0 and live_entry_price > 0 else 0.0
    cost_model = _default_cost_model()
    position_sol = _to_float(signal.get("建议纸面仓位SOL"), 0.0) or _to_float(state.get("建议纸面仓位SOL"), 0.0)
    wallet_factor = _to_float(state.get("钱包结构系数"), 1.0)
    if wallet_factor <= 0:
        wallet_factor = 1.0
    position_sol = round(position_sol * wallet_factor, 10)
    exit_plan = _extract_exit_plan(signal)
    stop_price = _to_float(exit_plan.get("hard_stop_price"), 0.0) or _to_float(signal.get("止损价格"), 0.0) or entry_price * 0.8
    symbol = str(state.get("代币符号") or signal.get("代币符号") or "")
    signal_time = str(signal.get("信号时间") or state.get("信号时间") or snapshot_time)
    discovery_time = _first_non_empty(state.get("candidate_discovered_at"), state.get("discovered_at"), state.get("发现时间"), default="")
    discovery_market_cap = _first_non_empty(state.get("discovery_market_cap_usd"), state.get("发现市值USD"), default=None)
    signal_market_cap = _first_non_empty(signal.get("signal_market_cap_usd"), state.get("signal_market_cap_usd"), signal.get("信号市值USD"), default=None)
    entry_market_cap = _first_non_empty(price_info.get("market_cap_usd"), price_info.get("marketCapUsd"), state.get("paper_entry_market_cap_usd"), signal_market_cap, default=None)
    entry_liquidity = _first_non_empty(price_info.get("liquidity_usd"), price_info.get("liquidityUsd"), state.get("liquidity_usd"), state.get("discovery_liquidity_usd"), default=None)
    entry_holder_count = _first_non_empty(price_info.get("holder_count"), state.get("holder_count"), state.get("discovery_holder_count"), default=None)
    sol_usd = _to_float(price_info.get("sol_usd") or price_info.get("sol_price_usd"), 0.0)
    paper_size_usd = round(position_sol * sol_usd, 6) if sol_usd > 0 else 0.0
    estimated_token_amount = round((position_sol / entry_price), 8) if entry_price > 0 else 0.0
    delay_from_discovery = _seconds_between(discovery_time, snapshot_time)
    delay_from_signal = _seconds_between(signal_time, snapshot_time)
    cap_change_from_discovery = _pct_change(entry_market_cap, discovery_market_cap)
    cap_change_from_signal = _pct_change(entry_market_cap, signal_market_cap)
    market_cap_status = _market_cap_context_status(cap_change_from_discovery)
    wallet_status = str(state.get("钱包结构结论") or state.get("wallet_structure_status") or "未接入")
    wallet_score = _to_float(state.get("钱包结构评分") or state.get("wallet_structure_score"), 0.0)
    wallet_risk = _to_float(state.get("钱包风险评分") or state.get("wallet_risk_score"), 0.0)
    counterparty = _to_float(state.get("对手盘压力评分") or state.get("counterparty_pressure_score"), 0.0)
    data_quality = _to_float(state.get("data_quality_score") or state.get("数据质量评分"), 0.0)
    position_id = f"paper-{token}-{snapshot_time}"
    position = {
        "position_id": position_id,
        "代币地址": token,
        "代币符号": symbol,
        "token_address": token,
        "token_symbol": symbol,
        "entry_time": signal_time,
        "paper_entry_time": snapshot_time,
        "entry_price": entry_price,
        "paper_entry_price": entry_price,
        "entry_price_mode": entry_price_mode,
        "entry_quote_source": str(price_info.get("source") or "unknown"),
        "signal_entry_price": signal_entry_price,
        "live_entry_price": live_entry_price,
        "entry_raw_quote_price": live_entry_price,
        "entry_simulated_price": entry_price,
        "signal_pnl_pct": 0.0,
        "live_pnl_pct": 0.0,
        "entry_price_diff_pct": entry_price_diff_pct,
        "entry_slippage_pct": cost_model["buy_slippage_pct"],
        "entry_fee_sol": cost_model["priority_fee_sol"],
        "cost_model": cost_model,
        "cost_buffer_pct": _cost_buffer_pct(cost_model),
        "position_sol": position_sol,
        "paper_size_sol": position_sol,
        "paper_size_usd": paper_size_usd,
        "estimated_token_amount": estimated_token_amount,
        "remaining_pct": 100.0,
        "stop_price": stop_price,
        "take_profit_rules": list(exit_plan.get("take_profit_rules") or []),
        "triggered_tps": [],
        "max_price": entry_price,
        "min_price": entry_price,
        "last_price": entry_price,
        "last_update_time": snapshot_time,
        "candidate_discovered_at": discovery_time,
        "discovery_market_cap_usd": discovery_market_cap,
        "discovery_liquidity_usd": _first_non_empty(state.get("discovery_liquidity_usd"), default=None),
        "discovery_holder_count": _first_non_empty(state.get("discovery_holder_count"), default=None),
        "discovery_source": _first_non_empty(state.get("discovery_source"), default="gmgn_new_token_filter"),
        "signal_time": signal_time,
        "signal_level": str(signal.get("信号等级") or state.get("信号等级") or ""),
        "signal_type": str(signal.get("策略类型") or state.get("策略类型") or ""),
        "strategy_type": str(signal.get("策略类型") or state.get("策略类型") or ""),
        "signal_price": signal_entry_price,
        "signal_market_cap_usd": signal_market_cap,
        "wallet_decision_time": _first_non_empty(state.get("wallet_decision_time"), snapshot_time),
        "wallet_structure_status": wallet_status,
        "wallet_structure_factor": wallet_factor,
        "wallet_structure_score": wallet_score,
        "wallet_risk_score": wallet_risk,
        "counterparty_pressure_score": counterparty,
        "data_quality_score": data_quality,
        "wallet_decision_market_cap_usd": _first_non_empty(state.get("wallet_decision_market_cap_usd"), default=None),
        "wallet_structure_reason": str(state.get("钱包结构原因") or state.get("wallet_reason") or ""),
        "wallet_evidence_level": str(state.get("钱包证据等级") or ""),
        "quote_security_state": str(quote.get("交易前状态") or ""),
        "entry_market_cap_usd": entry_market_cap,
        "paper_entry_market_cap_usd": entry_market_cap,
        "entry_liquidity_usd": entry_liquidity,
        "entry_holder_count": entry_holder_count,
        "entry_delay_from_discovery_sec": delay_from_discovery,
        "entry_delay_from_signal_sec": delay_from_signal,
        "entry_market_cap_change_from_discovery_pct": cap_change_from_discovery,
        "entry_market_cap_change_from_signal_pct": cap_change_from_signal,
        "market_cap_context_status": market_cap_status,
        "status": "OPEN",
        "scope_note": "纸面持仓，不执行真实 swap。",
    }
    position["paper_entry_snapshot"] = {
        "candidate": {
            "candidate_discovered_at": discovery_time,
            "discovery_price": state.get("discovery_price"),
            "discovery_market_cap_usd": discovery_market_cap,
            "discovery_liquidity_usd": position.get("discovery_liquidity_usd"),
            "discovery_holder_count": position.get("discovery_holder_count"),
            "discovery_source": position.get("discovery_source"),
        },
        "signal": {
            "signal_time": signal_time,
            "signal_level": position["signal_level"],
            "signal_type": position["signal_type"],
            "signal_price": signal_entry_price,
            "signal_market_cap_usd": signal_market_cap,
        },
        "wallet": {
            "wallet_decision_time": position["wallet_decision_time"],
            "wallet_structure_status": wallet_status,
            "wallet_structure_score": wallet_score,
            "wallet_risk_score": wallet_risk,
            "counterparty_pressure_score": counterparty,
            "data_quality_score": data_quality,
            "wallet_decision_market_cap_usd": position.get("wallet_decision_market_cap_usd"),
            "wallet_reason": position["wallet_structure_reason"],
        },
        "entry": {
            "paper_entry_time": snapshot_time,
            "entry_price_mode": entry_price_mode,
            "entry_quote_source": position["entry_quote_source"],
            "entry_raw_quote_price": live_entry_price,
            "entry_simulated_price": entry_price,
            "entry_slippage_pct": cost_model["buy_slippage_pct"],
            "entry_fee_sol": cost_model["priority_fee_sol"],
            "entry_market_cap_usd": entry_market_cap,
            "entry_liquidity_usd": entry_liquidity,
            "entry_holder_count": entry_holder_count,
            "paper_size_sol": position_sol,
            "paper_size_usd": paper_size_usd,
            "estimated_token_amount": estimated_token_amount,
        },
    }
    return position


def _decision_get(decision: Any, key: str, default: Any = None) -> Any:
    if isinstance(decision, dict):
        return decision.get(key, default)
    return getattr(decision, key, default)


def _decision_metrics(decision: Any) -> Dict[str, Any]:
    metrics = _decision_get(decision, "metrics", None)
    if isinstance(metrics, dict):
        return metrics
    if isinstance(decision, dict):
        return decision
    return {}


def decide_wallet_position_action(
    position: Dict[str, Any],
    current_decision: Any,
    latest_delta: Optional[Dict[str, Any]] = None,
    mode: str = "paper",
) -> Dict[str, Any]:
    """钱包退出策略层：钱包结构先进入风险监控，强证据才允许 FORCE_PAPER_EXIT。

    该函数落实链接文档里的 wallet_exit_policy：
    - 钱包结构不是直接卖出按钮；
    - 默认动作是 EXIT_MONITOR；
    - FORCE_PAPER_EXIT 需要数据质量、多轮 delta、盘型冲突、市场确认同时支持；
    - live 模式仍然只生成确认要求，不自动卖出。
    """

    latest_delta = latest_delta or {}
    metrics = _decision_metrics(current_decision)
    current_status = str(_decision_get(current_decision, "wallet_structure_status", metrics.get("wallet_structure_status", "")))
    sync_sell_score = _to_float(metrics.get("same_source_sync_sell_score") or metrics.get("最高同步卖出分"), 0.0)
    counterparty_score = _to_float(_decision_get(current_decision, "counterparty_pressure_score", metrics.get("counterparty_pressure_score", 0)), 0.0)
    data_quality_score = _to_float(_decision_get(current_decision, "data_quality_score", metrics.get("data_quality_score", 0)), 0.0)

    counterparty_delta = _to_float(latest_delta.get("counterparty_pressure_score_delta"), 0.0)
    early_sold_delta = _to_float(latest_delta.get("early_wallet_sold_pct_delta"), 0.0)
    same_source_sold_delta = _to_float(latest_delta.get("same_source_group_sold_pct_delta"), 0.0)
    high_result_delta = _to_float(latest_delta.get("high_result_remaining_pct_delta"), 0.0)
    risk_delta = _to_float(latest_delta.get("wallet_risk_score_delta"), 0.0)
    delta_snapshot_count = int(_to_float(latest_delta.get("delta_snapshot_count") or latest_delta.get("snapshot_count") or latest_delta.get("confirmed_delta_rounds"), 1.0))
    pattern_type = str(position.get("pattern_type") or latest_delta.get("pattern_type") or latest_delta.get("lifecycle_phase") or "UNKNOWN")
    price_structure_status = str(latest_delta.get("price_structure_status") or latest_delta.get("control_box_status") or "")
    pattern_conflict = bool(latest_delta.get("pattern_conflict")) or pattern_type in {"PRICE_BREAKDOWN", "DISTRIBUTION_TOP", "CONTROL_LOST_TO_DISTRIBUTION"} or price_structure_status in {"BREAKDOWN", "BELOW_CONTROL_BOX", "BELOW_AVWAP"}
    market_confirmation = bool(latest_delta.get("market_confirmation")) or pattern_conflict or counterparty_delta >= 25
    position_pnl_pct = _to_float(position.get("当前收益率_pct") or position.get("unrealized_pnl_pct"), 0.0)

    def monitor(reason: str, failure_type: str | None = None, *, eligible: bool = False) -> Dict[str, Any]:
        return {
            "action": "EXIT_MONITOR",
            "failure_type": failure_type,
            "reason": reason,
            "policy_layer": "wallet_exit_policy",
            "force_exit_eligible": eligible,
            "scope_note": "纸面阶段进入退出监控；不执行真实 swap。",
        }

    def hard_exit(reason: str, failure_type: str) -> Dict[str, Any]:
        payload = {
            "failure_type": failure_type,
            "reason": reason,
            "policy_layer": "wallet_exit_policy",
            "force_exit_eligible": True,
        }
        if mode == "paper":
            payload.update({
                "action": "FORCE_PAPER_EXIT",
                "scope_note": "纸面阶段模拟强制退出，用于验证钱包结构风控；不执行真实 swap。",
            })
            return payload
        payload.update({
            "action": "REAL_TRADE_CONFIRMATION_REQUIRED",
            "scope_note": "实盘/未来 live 模式不自动卖出，只生成确认层动作，不自动广播、不自动执行。",
        })
        return payload

    if data_quality_score and data_quality_score < 65:
        return monitor("数据质量低于 wallet_exit_policy 阈值，不能强制退出，先进入 EXIT_MONITOR", "DATA_QUALITY_FAIL")

    strong_same_source = sync_sell_score >= 80 and same_source_sold_delta >= 20
    strong_counterparty = counterparty_score >= 75 and counterparty_delta >= 25
    strong_structure = current_status == "WALLET_BLOCK" and risk_delta >= 20
    strong_high_result = high_result_delta <= -30 and risk_delta >= 20
    strong_early_distribution = early_sold_delta >= 25 and (strong_counterparty or position_pnl_pct > 0)
    strong_evidence = strong_same_source or strong_counterparty or strong_structure or strong_high_result or strong_early_distribution
    force_allowed = strong_evidence and delta_snapshot_count >= 2 and pattern_conflict and market_confirmation

    if force_allowed:
        if strong_same_source:
            return hard_exit("同源组同步卖出 + 多轮 delta + 盘型/市场确认，允许 FORCE_PAPER_EXIT", "SAME_SOURCE_EXIT")
        if strong_counterparty:
            return hard_exit("对手盘压力高且快速上升，并得到市场确认，允许 FORCE_PAPER_EXIT", "COUNTERPARTY_ABSORBING")
        if strong_high_result:
            return hard_exit("高结果钱包集体退出且风险分上升，允许 FORCE_PAPER_EXIT", "HIGH_RESULT_EXIT")
        return hard_exit("钱包结构强恶化并与盘型/市场确认冲突，允许 FORCE_PAPER_EXIT", "STRUCTURE_WEAKENING")

    if current_status in {"WALLET_BLOCK", "WALLET_PAUSE"} or strong_evidence:
        missing = []
        if delta_snapshot_count < 2:
            missing.append("多轮 delta 未确认")
        if not pattern_conflict:
            missing.append("盘型冲突未确认")
        if not market_confirmation:
            missing.append("市场确认不足")
        suffix = "；".join(missing) if missing else "强证据不足"
        failure = "STRUCTURE_WEAKENING" if current_status == "WALLET_BLOCK" else "WALLET_EXIT"
        return monitor(f"钱包结构出现风险，但 {suffix}，默认 EXIT_MONITOR", failure)

    if early_sold_delta >= 20:
        return monitor("早期钱包卖出增加，先进入退出观察，等待下一轮快照", "WALLET_EXIT")
    if high_result_delta <= -20:
        return monitor("高结果钱包剩余筹码下降，进入退出观察", "HIGH_RESULT_EXIT")

    return {
        "action": "HOLD",
        "failure_type": None,
        "reason": "钱包结构未触发持仓退出条件",
        "policy_layer": "wallet_exit_policy",
        "force_exit_eligible": False,
        "scope_note": "继续纸面持仓观察；不执行真实 swap。",
    }


def _update_position(position: Dict[str, Any], price_info: Dict[str, Any], snapshot_time: str) -> tuple[Dict[str, Any] | None, Dict[str, Any] | None]:
    current_price = _to_float(price_info.get("price"), _to_float(position.get("last_price"), 0.0))
    entry_price = _to_float(position.get("entry_price"), 0.0)
    if current_price <= 0 or entry_price <= 0:
        position["last_update_time"] = snapshot_time
        return position, None

    position["last_price"] = current_price
    position["last_update_time"] = snapshot_time
    position["max_price"] = max(_to_float(position.get("max_price"), entry_price), current_price)
    position["min_price"] = min(_to_float(position.get("min_price"), entry_price), current_price)
    position["最大浮盈_pct"] = round((position["max_price"] - entry_price) / entry_price * 100.0, 4)
    position["最大浮亏_pct"] = round((position["min_price"] - entry_price) / entry_price * 100.0, 4)
    position["live_pnl_pct"] = round((current_price - entry_price) / entry_price * 100.0, 4)
    signal_entry_price = _to_float(position.get("signal_entry_price"), 0.0)
    position["signal_pnl_pct"] = round((current_price - signal_entry_price) / signal_entry_price * 100.0, 4) if signal_entry_price > 0 else position["live_pnl_pct"]

    stop_price = _to_float(position.get("stop_price"), 0.0)
    if stop_price and current_price <= stop_price:
        closed = dict(position)
        closed.update({
            "status": "CLOSED",
            "exit_time": snapshot_time,
            "exit_price": current_price,
            "exit_reason": "命中纸面止损",
            "最终收益率_pct": round((current_price - entry_price) / entry_price * 100.0, 4),
        })
        return None, closed

    triggered = list(position.get("triggered_tps") or [])
    remaining_pct = _to_float(position.get("remaining_pct"), 100.0)
    for rule in list(position.get("take_profit_rules") or []):
        trigger = _to_float(rule.get("触发收益率"), 0.0)
        if trigger <= 0 or any(_to_float(done.get("触发收益率"), 0.0) == trigger for done in triggered):
            continue
        target = entry_price * (1 + trigger / 100.0)
        if current_price >= target:
            sell_ratio = min(_to_float(rule.get("卖出比例"), 0.0), remaining_pct)
            remaining_pct = max(0.0, remaining_pct - sell_ratio)
            triggered.append({**rule, "触发时间": snapshot_time, "触发价格": current_price})

    position["triggered_tps"] = triggered
    position["remaining_pct"] = remaining_pct
    position["已触发止盈次数"] = len(triggered)
    position["当前收益率_pct"] = round((current_price - entry_price) / entry_price * 100.0, 4)
    if remaining_pct <= 0:
        closed = dict(position)
        closed.update({
            "status": "CLOSED",
            "exit_time": snapshot_time,
            "exit_price": current_price,
            "exit_reason": "纸面分批止盈全部完成",
            "最终收益率_pct": position["当前收益率_pct"],
        })
        return None, closed
    return position, None


def _assert_readonly_price_command(command: List[str]) -> None:
    joined = " ".join(command)
    for snippet in _FORBIDDEN_COMMAND_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"禁止构造/执行真实交易命令：{snippet}")
    allowed_prefix = ["onchainos", "market", "price"]
    if command[: len(allowed_prefix)] != allowed_prefix:
        raise ValueError(f"纸面 live runner 只允许 OKX 只读 market price 命令：{command}")


def run_readonly_price_cli(command: List[str], timeout: int = 30) -> str:
    """运行 OKX 只读价格命令；禁止任何 swap/execute/broadcast 命令。"""

    _assert_readonly_price_command(command)
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    return completed.stdout


def _first_payload_object(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = payload.get("data", payload)
    if isinstance(data, list):
        return data[0] if data and isinstance(data[0], dict) else {}
    if isinstance(data, dict):
        return data
    return payload


def _pick(row: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return None


def build_okx_market_price_provider(*, runner: Runner = run_readonly_price_cli) -> PriceProvider:
    """构造 OKX onchainos 只读市场价格 provider。

    只调用 `onchainos market price --address <token> --chain solana`，不执行 swap。
    """

    def provider(token: str) -> Dict[str, Any]:
        command = ["onchainos", "market", "price", "--address", token, "--chain", "solana"]
        raw = runner(command)
        try:
            payload = json.loads((raw or "").strip() or "{}")
        except json.JSONDecodeError:
            payload = {"raw_text": raw}
        row = _first_payload_object(payload)
        price = _to_float(_pick(row, "price", "priceUsd", "price_usd", "lastPrice", "currentPrice"), 0.0)
        if price <= 0:
            raise ValueError(f"OKX market price 未返回有效价格：{token}")
        return {
            "price": price,
            "source": "okx_market_price",
            "snapshot_time": str(_pick(row, "time", "timestamp", "snapshot_time") or _utc_now_text()),
            "raw": row,
        }

    return provider


def _default_price_provider(token: str) -> Dict[str, Any]:
    return build_okx_market_price_provider()(token)



def _journal_row(position: Dict[str, Any], *, snapshot_time: str, paper_action: str = "HOLD", monitor_reason: str = "") -> Dict[str, Any]:
    return {
        "time": snapshot_time,
        "position_id": position.get("position_id"),
        "token_address": position.get("token_address") or position.get("代币地址"),
        "token_symbol": position.get("token_symbol") or position.get("代币符号", ""),
        "current_price": position.get("last_price") or position.get("current_price"),
        "current_market_cap_usd": position.get("current_market_cap_usd"),
        "unrealized_pnl_pct": position.get("当前收益率_pct") or position.get("live_pnl_pct"),
        "max_floating_profit_pct": position.get("最大浮盈_pct"),
        "max_floating_loss_pct": position.get("最大浮亏_pct"),
        "wallet_structure_status": position.get("wallet_structure_status"),
        "wallet_structure_score": position.get("wallet_structure_score"),
        "wallet_risk_score": position.get("wallet_risk_score"),
        "counterparty_pressure_score": position.get("counterparty_pressure_score"),
        "paper_action": paper_action,
        "monitor_reason": monitor_reason,
        "boundary": "纸面持仓过程日志；不执行真实 swap。",
    }


def _append_position_journal(output_dir: Path, position: Dict[str, Any], *, snapshot_time: str, paper_action: str = "HOLD", monitor_reason: str = "") -> None:
    position_id = str(position.get("position_id") or position.get("代币地址") or position.get("token_address") or "unknown")
    _append_jsonl(output_dir / "position_journal" / f"{position_id}.jsonl", [_journal_row(position, snapshot_time=snapshot_time, paper_action=paper_action, monitor_reason=monitor_reason)])


def _trade_row(position: Dict[str, Any], *, event_type: str, side: str, trade_time: str, price: Any, reason: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    extra = extra or {}
    trade_id = f"TRD-{event_type}-{position.get('position_id')}-{trade_time}"
    return {
        "trade_id": trade_id,
        "position_id": position.get("position_id"),
        "token_address": position.get("token_address") or position.get("代币地址"),
        "token_symbol": position.get("token_symbol") or position.get("代币符号", ""),
        "side": side,
        "event_type": event_type,
        "trade_time": trade_time,
        "price": price,
        "market_cap_usd": extra.get("market_cap_usd") or position.get("entry_market_cap_usd") or position.get("paper_entry_market_cap_usd") or position.get("exit_market_cap_usd"),
        "liquidity_usd": extra.get("liquidity_usd") or position.get("entry_liquidity_usd"),
        "size_sol": position.get("paper_size_sol") or position.get("position_sol"),
        "size_usd": position.get("paper_size_usd"),
        "token_amount": position.get("estimated_token_amount"),
        "slippage_pct": extra.get("slippage_pct") or position.get("entry_slippage_pct"),
        "fee_sol": extra.get("fee_sol") or position.get("entry_fee_sol"),
        "quote_source": position.get("entry_quote_source") or extra.get("quote_source"),
        "reason": reason,
        "事件时间": trade_time,
        "事件类型": event_type,
        "代币地址": position.get("token_address") or position.get("代币地址"),
        "代币符号": position.get("token_symbol") or position.get("代币符号", ""),
        "价格": price,
        "仓位SOL": position.get("paper_size_sol") or position.get("position_sol"),
        "原因": reason,
        **{k: v for k, v in extra.items() if k not in {"market_cap_usd", "liquidity_usd", "slippage_pct", "fee_sol", "quote_source"}},
    }

def run_paper_live_cycle(
    *,
    candidate_states_path: str | Path,
    signal_summary_path: str | Path,
    quote_security_summary_path: str | Path | None = None,
    output_dir: str | Path = "data/paper_live",
    wallet_structure_dir: str | Path | None = None,
    price_provider: PriceProvider = _default_price_provider,
    snapshot_time: Optional[str] = None,
) -> Dict[str, str]:
    """运行一轮纸面自动交易循环并写出状态、交易、指标与日报。"""

    now = snapshot_time or _utc_now_text()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    states = _state_rows(_read_json(candidate_states_path))
    signals = _index_by_token(_signal_rows(_read_json(signal_summary_path)))
    quotes = _index_by_token(_quote_rows(_read_json(quote_security_summary_path)))

    open_positions = _load_open_positions(out)
    closed_positions = _load_closed_positions(out)
    open_tokens = {str(row.get("代币地址")) for row in open_positions}

    trades: List[Dict[str, Any]] = []
    risk_events: List[Dict[str, Any]] = []
    failure_attributions: List[Dict[str, Any]] = []
    updated_open: List[Dict[str, Any]] = []
    new_entries = 0
    exits = 0
    blocked = 0
    skipped_existing = 0

    # 先更新已有纸面持仓。
    for pos in open_positions:
        token = str(pos.get("代币地址") or "")
        try:
            price_info = price_provider(token)
            current_price = _to_float(price_info.get("price"), _to_float(pos.get("last_price"), 0.0))
            wallet_decision, latest_delta = _load_wallet_structure_runtime_inputs(token, wallet_structure_dir)
            wallet_action = decide_wallet_position_action(pos, wallet_decision, latest_delta, mode="paper") if wallet_decision or latest_delta else {"action": "HOLD"}
            if wallet_action.get("action") == "FORCE_PAPER_EXIT":
                closed = _close_position_for_wallet_action(pos, current_price, now, wallet_action)
                exits += 1
                closed_positions.append(closed)
                attribution = _failure_attribution_row(closed, wallet_action, now)
                failure_attributions.append(attribution)
                risk_events.append({**attribution, "事件类型": "PAPER_FORCE_EXIT"})
                trades.append(_trade_row(closed, event_type="PAPER_FORCE_EXIT", side="SELL", trade_time=now, price=closed.get("exit_price"), reason=closed.get("failure_reason", ""), extra={"收益率_pct": closed.get("最终收益率_pct"), "failure_type": closed.get("failure_type")}))
                continue
            if wallet_action.get("action") == "EXIT_MONITOR":
                pos["wallet_position_action"] = "EXIT_MONITOR"
                pos["wallet_exit_monitor_reason"] = wallet_action.get("reason")
                failure_attributions.append(_failure_attribution_row(pos, wallet_action, now))
            updated, closed = _update_position(pos, price_info, now)
            if closed:
                exits += 1
                closed_positions.append(closed)
                trades.append(_trade_row(closed, event_type="PAPER_EXIT", side="SELL", trade_time=now, price=closed.get("exit_price"), reason=closed.get("exit_reason", ""), extra={"收益率_pct": closed.get("最终收益率_pct")}))
            elif updated:
                _append_position_journal(out, updated, snapshot_time=now, paper_action=updated.get("wallet_position_action") or "HOLD", monitor_reason=updated.get("wallet_exit_monitor_reason", ""))
                updated_open.append(updated)
        except Exception as exc:  # pragma: no cover - defensive logging path
            updated_open.append(pos)
            risk_events.append({"事件时间": now, "事件类型": "PRICE_UPDATE_FAILED", "代币地址": token, "原因": str(exc)})

    open_positions = updated_open
    open_tokens = {str(row.get("代币地址")) for row in open_positions}

    # 再对新 PAPER_READY 候选做纸面入场。
    for state in states:
        token = str(state.get("代币地址") or "")
        if not token:
            continue
        quote = quotes.get(token, {})
        allowed, reason = _entry_allowed(state, quote)
        if not allowed:
            if "BLOCK" in reason:
                blocked += 1
                risk_events.append({
                    "事件时间": now,
                    "事件类型": "PAPER_ENTRY_BLOCKED",
                    "代币地址": token,
                    "代币符号": state.get("代币符号", ""),
                    "权限": quote.get("最终权限") or quote.get("final_permission") or "BLOCK_BUY",
                    "原因": reason,
                    "scope_note": "纸面交易阻断；不执行真实 swap。",
                })
            continue
        if token in open_tokens:
            skipped_existing += 1
            continue
        signal = signals.get(token, {})
        try:
            price_info = price_provider(token)
        except Exception as exc:
            risk_events.append({
                "事件时间": now,
                "事件类型": "PAPER_ENTRY_PRICE_FAILED",
                "代币地址": token,
                "代币符号": state.get("代币符号", ""),
                "原因": str(exc),
                "scope_note": "纸面入场价格获取失败；跳过该候选，不执行真实 swap。",
            })
            continue
        position = _new_position(token=token, state=state, signal=signal, quote=quote, price_info=price_info, snapshot_time=now)
        if position["entry_price"] <= 0 or position["position_sol"] <= 0:
            risk_events.append({"事件时间": now, "事件类型": "PAPER_ENTRY_SKIPPED", "代币地址": token, "原因": "缺少有效入场价格或纸面仓位"})
            continue
        updated, closed = _update_position(position, price_info, now)
        if closed:
            exits += 1
            closed_positions.append(closed)
        elif updated:
            _append_position_journal(out, updated, snapshot_time=now, paper_action="PAPER_ENTRY", monitor_reason="新纸面仓位入场后记录首条持仓日志")
            open_positions.append(updated)
            open_tokens.add(token)
        new_entries += 1
        trades.append(_trade_row(position, event_type="PAPER_ENTRY", side="BUY", trade_time=now, price=position.get("entry_price"), reason=reason, extra={
            "信号等级": position.get("signal_level"),
            "wallet_structure_status": position.get("wallet_structure_status"),
            "wallet_structure_factor": position.get("wallet_structure_factor"),
            "wallet_structure_score": position.get("wallet_structure_score"),
            "wallet_risk_score": position.get("wallet_risk_score"),
        }))

    closed_returns = [_to_float(row.get("最终收益率_pct"), 0.0) for row in closed_positions]
    win_count = sum(1 for value in closed_returns if value > 0)
    metrics = {
        "snapshot_time": now,
        "scope_note": "OKX/GMGN 只读报价驱动的纸面自动交易统计；不执行真实 swap。",
        "统计": {
            "读取候选数": len(states),
            "新增纸面入场数": new_entries,
            "纸面退出数": exits,
            "阻断候选数": blocked,
            "重复持仓跳过数": skipped_existing,
            "当前开放仓位数": len(open_positions),
            "累计关闭仓位数": len(closed_positions),
            "已关闭胜率_pct": round(win_count / len(closed_returns) * 100.0, 4) if closed_returns else 0.0,
            "已关闭平均收益率_pct": round(sum(closed_returns) / len(closed_returns), 4) if closed_returns else 0.0,
        },
    }

    report = [
        "# OKX/GMGN 纸面自动交易日报",
        "",
        f"- 快照时间：{now}",
        "- 边界：只做纸面入场、更新、退出和统计；不执行真实 swap，不签名，不广播。",
        f"- 新增纸面入场数：{new_entries}",
        f"- 纸面退出数：{exits}",
        f"- 当前开放仓位数：{len(open_positions)}",
        f"- 累计关闭仓位数：{len(closed_positions)}",
        f"- 已关闭胜率：{metrics['统计']['已关闭胜率_pct']}%",
        f"- 已关闭平均收益率：{metrics['统计']['已关闭平均收益率_pct']}%",
        "",
        "## 当前开放纸面仓位",
    ]
    for row in open_positions:
        report.append(f"- {row.get('代币符号') or ''} `{row.get('代币地址')}` 当前收益 {row.get('当前收益率_pct', 0)}%，已触发止盈 {row.get('已触发止盈次数', 0)} 次")

    _write_json(out / "paper_positions_open.json", {"snapshot_time": now, "open_positions": open_positions})
    _write_json(out / "paper_positions_closed.json", {"snapshot_time": now, "closed_positions": closed_positions})
    _write_csv(out / "paper_trades.csv", trades, PAPER_TRADE_CSV_FIELDS)
    _write_csv(
        out / "paper_equity_curve.csv",
        [{"snapshot_time": now, "closed_trade_count": len(closed_positions), "average_return_pct": metrics["统计"]["已关闭平均收益率_pct"]}],
    )
    _write_json(out / "strategy_metrics.json", metrics)
    _append_jsonl(out / "risk_events.jsonl", risk_events)
    _append_jsonl(out / "failure_attribution.jsonl", failure_attributions)
    daily_dir = out / "daily_reports"
    daily_report = daily_dir / f"paper_daily_report_{now[:10].replace('-', '')}.md"
    daily_report.parent.mkdir(parents=True, exist_ok=True)
    daily_report.write_text("\n".join(report) + "\n", encoding="utf-8")

    return {
        "open_positions_json": str(out / "paper_positions_open.json"),
        "closed_positions_json": str(out / "paper_positions_closed.json"),
        "paper_trades_csv": str(out / "paper_trades.csv"),
        "paper_equity_curve_csv": str(out / "paper_equity_curve.csv"),
        "strategy_metrics_json": str(out / "strategy_metrics.json"),
        "risk_events_jsonl": str(out / "risk_events.jsonl"),
        "failure_attribution_jsonl": str(out / "failure_attribution.jsonl"),
        "daily_report_md": str(daily_report),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK OKX/GMGN 纸面自动交易 live runner（不执行真实 swap）")
    parser.add_argument("--candidate-states", required=True)
    parser.add_argument("--signal-summary", required=True)
    parser.add_argument("--quote-security-summary", default=None)
    parser.add_argument("--output-dir", default="data/paper_live")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # CLI 使用 OKX onchainos 只读 market price 作为默认价格源；仍然不执行真实 swap。
    paths = run_paper_live_cycle(
        candidate_states_path=args.candidate_states,
        signal_summary_path=args.signal_summary,
        quote_security_summary_path=args.quote_security_summary,
        output_dir=args.output_dir,
    )
    print(json.dumps(paths, ensure_ascii=False, indent=2))
