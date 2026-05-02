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


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        p.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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
    closed.update({
        "status": "CLOSED",
        "exit_time": snapshot_time,
        "exit_price": current_price,
        "exit_reason": "钱包结构触发纸面强制退出",
        "最终收益率_pct": round((current_price - entry_price) / entry_price * 100.0, 4) if entry_price > 0 else 0.0,
        "wallet_position_action": action.get("action"),
        "failure_type": action.get("failure_type"),
        "failure_reason": action.get("reason"),
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
    return {
        "position_id": f"paper-{token}-{snapshot_time}",
        "代币地址": token,
        "代币符号": symbol,
        "entry_time": str(signal.get("信号时间") or state.get("信号时间") or snapshot_time),
        "entry_price": entry_price,
        "entry_price_mode": entry_price_mode,
        "signal_entry_price": signal_entry_price,
        "live_entry_price": live_entry_price,
        "signal_pnl_pct": 0.0,
        "live_pnl_pct": 0.0,
        "entry_price_diff_pct": entry_price_diff_pct,
        "cost_model": cost_model,
        "cost_buffer_pct": _cost_buffer_pct(cost_model),
        "position_sol": position_sol,
        "remaining_pct": 100.0,
        "stop_price": stop_price,
        "take_profit_rules": list(exit_plan.get("take_profit_rules") or []),
        "triggered_tps": [],
        "max_price": entry_price,
        "min_price": entry_price,
        "last_price": entry_price,
        "last_update_time": snapshot_time,
        "signal_level": str(signal.get("信号等级") or state.get("信号等级") or ""),
        "strategy_type": str(signal.get("策略类型") or state.get("策略类型") or ""),
        "quote_security_state": str(quote.get("交易前状态") or ""),
        "wallet_structure_status": str(state.get("钱包结构结论") or "未接入"),
        "wallet_structure_factor": wallet_factor,
        "wallet_structure_score": _to_float(state.get("钱包结构评分"), 0.0),
        "wallet_risk_score": _to_float(state.get("钱包风险评分"), 0.0),
        "counterparty_pressure_score": _to_float(state.get("对手盘压力评分"), 0.0),
        "wallet_structure_reason": str(state.get("钱包结构原因") or ""),
        "wallet_evidence_level": str(state.get("钱包证据等级") or ""),
        "status": "OPEN",
        "scope_note": "纸面持仓，不执行真实 swap。",
    }


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
    """根据当前钱包结构与 latest_delta 决定纸面持仓动作。

    paper 模式可模拟 FORCE_PAPER_EXIT；live 模式只返回确认要求，不自动卖出。
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
    position_pnl_pct = _to_float(position.get("当前收益率_pct") or position.get("unrealized_pnl_pct"), 0.0)

    def hard_exit(reason: str, failure_type: str) -> Dict[str, Any]:
        if mode == "paper":
            return {
                "action": "FORCE_PAPER_EXIT",
                "failure_type": failure_type,
                "reason": reason,
                "scope_note": "纸面阶段模拟退出，用于验证钱包结构风控；不执行真实 swap。",
            }
        return {
            "action": "REAL_TRADE_CONFIRMATION_REQUIRED",
            "failure_type": failure_type,
            "reason": reason,
            "scope_note": "实盘/未来 live 模式不自动卖出，只生成确认层动作，不自动广播、不自动执行。",
        }

    if current_status == "WALLET_BLOCK":
        return hard_exit("钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出", "STRUCTURE_WEAKENING")
    if sync_sell_score >= 70 or same_source_sold_delta >= 20:
        return hard_exit("疑似同源组同步卖出达到高风险阈值", "SAME_SOURCE_EXIT")
    if counterparty_score >= 70 and counterparty_delta >= 25:
        return hard_exit("对手盘压力高且快速上升，疑似筹码向晚期承接方转移", "COUNTERPARTY_ABSORBING")
    if early_sold_delta >= 20:
        if position_pnl_pct <= 0:
            return hard_exit("早期钱包卖出增加且当前仓位未盈利", "WALLET_EXIT")
        return {
            "action": "EXIT_MONITOR",
            "failure_type": "WALLET_EXIT",
            "reason": "早期钱包卖出增加，但当前仓位仍盈利，先进入退出观察",
            "scope_note": "纸面阶段进入退出监控；不执行真实 swap。",
        }
    if high_result_delta <= -20:
        if risk_delta >= 20:
            return hard_exit("高结果钱包退出且钱包风险分明显上升", "HIGH_RESULT_EXIT")
        return {
            "action": "EXIT_MONITOR",
            "failure_type": "HIGH_RESULT_EXIT",
            "reason": "高结果钱包剩余筹码下降，进入退出观察",
            "scope_note": "纸面阶段进入退出监控；不执行真实 swap。",
        }
    if data_quality_score and data_quality_score < 50:
        return {
            "action": "EXIT_MONITOR",
            "failure_type": "DATA_QUALITY_FAIL",
            "reason": "当前钱包结构数据质量不足，暂停激进动作",
            "scope_note": "纸面阶段进入退出监控；不执行真实 swap。",
        }
    return {
        "action": "HOLD",
        "failure_type": None,
        "reason": "钱包结构未触发持仓退出条件",
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
                trades.append({
                    "事件时间": now,
                    "事件类型": "PAPER_FORCE_EXIT",
                    "代币地址": token,
                    "代币符号": closed.get("代币符号", ""),
                    "价格": closed.get("exit_price"),
                    "仓位SOL": closed.get("position_sol"),
                    "收益率_pct": closed.get("最终收益率_pct"),
                    "failure_type": closed.get("failure_type"),
                    "原因": closed.get("failure_reason"),
                })
                continue
            if wallet_action.get("action") == "EXIT_MONITOR":
                pos["wallet_position_action"] = "EXIT_MONITOR"
                pos["wallet_exit_monitor_reason"] = wallet_action.get("reason")
                failure_attributions.append(_failure_attribution_row(pos, wallet_action, now))
            updated, closed = _update_position(pos, price_info, now)
            if closed:
                exits += 1
                closed_positions.append(closed)
                trades.append({
                    "事件时间": now,
                    "事件类型": "PAPER_EXIT",
                    "代币地址": token,
                    "代币符号": closed.get("代币符号", ""),
                    "价格": closed.get("exit_price"),
                    "仓位SOL": closed.get("position_sol"),
                    "收益率_pct": closed.get("最终收益率_pct"),
                    "原因": closed.get("exit_reason"),
                })
            elif updated:
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
            open_positions.append(updated)
            open_tokens.add(token)
        new_entries += 1
        trades.append({
            "事件时间": now,
            "事件类型": "PAPER_ENTRY",
            "代币地址": token,
            "代币符号": position.get("代币符号", ""),
            "价格": position.get("entry_price"),
            "仓位SOL": position.get("position_sol"),
            "信号等级": position.get("signal_level"),
            "wallet_structure_status": position.get("wallet_structure_status"),
            "wallet_structure_factor": position.get("wallet_structure_factor"),
            "wallet_structure_score": position.get("wallet_structure_score"),
            "wallet_risk_score": position.get("wallet_risk_score"),
            "原因": reason,
        })

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
    _write_csv(out / "paper_trades.csv", trades)
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
