#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 钱包结构多轮快照与 delta。

本模块只记录钱包结构证据随时间的变化，用于 paper 持仓监控、失败归因与阈值校准；
不执行真实 swap、不签名、不广播交易。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_name(text: str) -> str:
    return str(text).replace(":", "").replace("-", "").replace("+", "").replace(".", "").replace("/", "_")


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _pct_change(new: float, old: float) -> float:
    if old == 0:
        return 0.0
    return round((new - old) / abs(old) * 100.0, 4)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _decision_value(decision: Any, attr: str, default: Any = None) -> Any:
    if isinstance(decision, Mapping):
        return decision.get(attr, default)
    return getattr(decision, attr, default)


def _dominant_side_from_decision(decision: Any) -> str:
    side_counts = _decision_value(decision, "game_side_counts", {}) or {}
    if not isinstance(side_counts, Mapping) or not side_counts:
        return "UNKNOWN_SIDE"
    return max(side_counts.items(), key=lambda item: item[1])[0]


def build_snapshot(
    *,
    token_address: str,
    token_symbol: str,
    decision: Any,
    market_context: Optional[Mapping[str, Any]] = None,
    snapshot_time: Optional[str] = None,
) -> Dict[str, Any]:
    """构造单轮钱包结构快照。"""

    market_context = market_context or {}
    role_counts = _decision_value(decision, "role_counts", {}) or {}
    wallet_structure_status = _decision_value(decision, "wallet_structure_status", "WALLET_NEUTRAL")
    wallet_structure_score = int(_num(_decision_value(decision, "wallet_structure_score", 0)))
    wallet_risk_score = int(_num(_decision_value(decision, "wallet_risk_score", 0)))
    counterparty_pressure_score = int(_num(_decision_value(decision, "counterparty_pressure_score", 0)))
    data_quality_score = int(_num(_decision_value(decision, "data_quality_score", 0)))
    max_sync_buy_score = int(_num(_decision_value(decision, "max_sync_buy_score", 0)))
    max_sync_sell_score = int(_num(_decision_value(decision, "max_sync_sell_score", 0)))

    early_wallet_count = int(_num(_decision_value(decision, "early_wallet_count", 0)))
    clearout_count = int(_num(role_counts.get("EARLY_EXIT", 0))) if isinstance(role_counts, Mapping) else 0
    distribution_count = int(_num(role_counts.get("DISTRIBUTION_SELLER", 0))) if isinstance(role_counts, Mapping) else 0
    bagholder_count = int(_num(role_counts.get("BAGHOLDER_WHALE", 0))) if isinstance(role_counts, Mapping) else 0
    high_result_count = int(_num(role_counts.get("HIGH_RESULT_WALLET", 0))) if isinstance(role_counts, Mapping) else 0

    same_source_group_remaining_pct = _num(_decision_value(decision, "same_source_group_remaining_pct", 0))
    same_source_group_sold_pct = _num(_decision_value(decision, "same_source_group_sold_pct", 0))

    if same_source_group_sold_pct <= 0 and max_sync_sell_score >= 70:
        same_source_group_sold_pct = 65.0
        same_source_group_remaining_pct = 35.0 if same_source_group_remaining_pct <= 0 else same_source_group_remaining_pct
    elif same_source_group_sold_pct <= 0 and max_sync_buy_score >= 70:
        same_source_group_sold_pct = 10.0
        same_source_group_remaining_pct = 90.0 if same_source_group_remaining_pct <= 0 else same_source_group_remaining_pct

    if wallet_structure_status == "WALLET_SUPPORT":
        early_remaining = 80.0
        early_sold = 20.0
        high_result_remaining = 80.0 if high_result_count else 0.0
    elif wallet_structure_status == "WALLET_BLOCK":
        early_remaining = 20.0
        early_sold = 80.0
        high_result_remaining = 20.0 if high_result_count else 0.0
    else:
        early_remaining = 50.0
        early_sold = 50.0
        high_result_remaining = 50.0 if high_result_count else 0.0

    return {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "snapshot_time": snapshot_time or _iso_now(),
        "price": _num(market_context.get("price")),
        "market_cap": _num(market_context.get("market_cap")),
        "liquidity": _num(market_context.get("liquidity")),
        "holder_count": _num(market_context.get("holder_count")),
        "top10_holder_pct": _num(market_context.get("top10_holder_pct")),
        "top20_holder_pct": _num(market_context.get("top20_holder_pct")),
        "early_wallet_count": early_wallet_count,
        "early_wallet_remaining_pct": early_remaining,
        "early_wallet_sold_pct": early_sold,
        "high_result_wallet_count": high_result_count,
        "high_result_remaining_pct": high_result_remaining,
        "same_source_group_count": 1 if max(max_sync_buy_score, max_sync_sell_score) > 0 else 0,
        "same_source_group_remaining_pct": round(same_source_group_remaining_pct, 4),
        "same_source_group_sold_pct": round(same_source_group_sold_pct, 4),
        "same_source_sync_buy_score": max_sync_buy_score,
        "same_source_sync_sell_score": max_sync_sell_score,
        "distribution_wallet_count": distribution_count,
        "bagholder_whale_count": bagholder_count,
        "late_buyer_count": bagholder_count,
        "late_large_buyer_count": bagholder_count,
        "late_buyer_buy_amount_usd": 0.0,
        "wallet_structure_status": wallet_structure_status,
        "wallet_structure_score": wallet_structure_score,
        "wallet_risk_score": wallet_risk_score,
        "counterparty_pressure_score": counterparty_pressure_score,
        "data_quality_score": data_quality_score,
        "dominant_side_status": _dominant_side_from_decision(decision),
        "chip_transfer_status": _decision_value(decision, "chip_control_state", "CONTROL_UNCLEAR"),
        "scope_note": "钱包结构快照只用于纸面交易监控和复盘，不执行真实 swap。",
    }


def interpret_delta(delta: Mapping[str, Any]) -> str:
    if _num(delta.get("same_source_group_sold_pct_delta")) >= 20:
        return "疑似同源组卖出比例明显上升，结构侧撤退风险增加"
    if _num(delta.get("counterparty_pressure_score_delta")) >= 25:
        return "对手盘压力快速上升，疑似筹码向晚期承接方转移"
    if _num(delta.get("early_wallet_sold_pct_delta")) >= 20:
        return "早期钱包卖出比例明显上升，钱包结构正在弱化"
    if _num(delta.get("price_change_pct")) > 0 and _num(delta.get("early_wallet_sold_pct_delta")) <= 5:
        return "价格推进过程中结构钱包未明显撤退，结构暂时维持"
    return "未发现明确结构迁移信号"


def classify_delta_status(delta: Mapping[str, Any]) -> str:
    if _num(delta.get("same_source_group_sold_pct_delta")) >= 20:
        return "SAME_SOURCE_EXIT"
    if _num(delta.get("counterparty_pressure_score_delta")) >= 25:
        return "COUNTERPARTY_ABSORBING"
    if _num(delta.get("wallet_risk_score_delta")) >= 20 or _num(delta.get("early_wallet_sold_pct_delta")) >= 20:
        return "STRUCTURE_WEAKENING"
    if _num(delta.get("data_quality_score_delta")) <= -25:
        return "DATA_QUALITY_FAIL"
    return "STRUCTURE_STABLE"


def build_delta(previous: Mapping[str, Any], current: Mapping[str, Any]) -> Dict[str, Any]:
    delta = {
        "token_address": current.get("token_address"),
        "token_symbol": current.get("token_symbol"),
        "from_snapshot": previous.get("snapshot_time"),
        "to_snapshot": current.get("snapshot_time"),
        "price_change_pct": _pct_change(_num(current.get("price")), _num(previous.get("price"))),
        "market_cap_change_pct": _pct_change(_num(current.get("market_cap")), _num(previous.get("market_cap"))),
        "liquidity_change_pct": _pct_change(_num(current.get("liquidity")), _num(previous.get("liquidity"))),
        "holder_count_delta": _num(current.get("holder_count")) - _num(previous.get("holder_count")),
        "holder_count_delta_pct": _pct_change(_num(current.get("holder_count")), _num(previous.get("holder_count"))),
        "top10_holder_pct_delta": _num(current.get("top10_holder_pct")) - _num(previous.get("top10_holder_pct")),
        "top20_holder_pct_delta": _num(current.get("top20_holder_pct")) - _num(previous.get("top20_holder_pct")),
        "early_wallet_remaining_pct_delta": _num(current.get("early_wallet_remaining_pct")) - _num(previous.get("early_wallet_remaining_pct")),
        "early_wallet_sold_pct_delta": _num(current.get("early_wallet_sold_pct")) - _num(previous.get("early_wallet_sold_pct")),
        "high_result_remaining_pct_delta": _num(current.get("high_result_remaining_pct")) - _num(previous.get("high_result_remaining_pct")),
        "same_source_group_remaining_pct_delta": _num(current.get("same_source_group_remaining_pct")) - _num(previous.get("same_source_group_remaining_pct")),
        "same_source_group_sold_pct_delta": _num(current.get("same_source_group_sold_pct")) - _num(previous.get("same_source_group_sold_pct")),
        "distribution_wallet_count_delta": _num(current.get("distribution_wallet_count")) - _num(previous.get("distribution_wallet_count")),
        "bagholder_whale_count_delta": _num(current.get("bagholder_whale_count")) - _num(previous.get("bagholder_whale_count")),
        "late_buyer_count_delta": _num(current.get("late_buyer_count")) - _num(previous.get("late_buyer_count")),
        "late_large_buyer_count_delta": _num(current.get("late_large_buyer_count")) - _num(previous.get("late_large_buyer_count")),
        "late_buyer_buy_amount_usd_delta": _num(current.get("late_buyer_buy_amount_usd")) - _num(previous.get("late_buyer_buy_amount_usd")),
        "wallet_structure_score_delta": _num(current.get("wallet_structure_score")) - _num(previous.get("wallet_structure_score")),
        "wallet_risk_score_delta": _num(current.get("wallet_risk_score")) - _num(previous.get("wallet_risk_score")),
        "counterparty_pressure_score_delta": _num(current.get("counterparty_pressure_score")) - _num(previous.get("counterparty_pressure_score")),
        "data_quality_score_delta": _num(current.get("data_quality_score")) - _num(previous.get("data_quality_score")),
        "dominant_side_status_from": previous.get("dominant_side_status"),
        "dominant_side_status_to": current.get("dominant_side_status"),
        "chip_transfer_status_from": previous.get("chip_transfer_status"),
        "chip_transfer_status_to": current.get("chip_transfer_status"),
    }
    delta["wallet_structure_delta_status"] = classify_delta_status(delta)
    delta["delta_interpretation"] = interpret_delta(delta)
    delta["scope_note"] = "钱包结构 delta 只用于纸面交易监控和复盘，不执行真实 swap。"
    return delta


def write_snapshot_and_delta(
    *,
    token_address: str,
    token_symbol: str,
    decision: Any,
    market_context: Optional[Mapping[str, Any]],
    base_dir: str | Path,
    snapshot_time: Optional[str] = None,
) -> Dict[str, Any]:
    base = Path(base_dir)
    snapshots_dir = base / token_address / "structure_analysis" / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    current = build_snapshot(
        token_address=token_address,
        token_symbol=token_symbol,
        decision=decision,
        market_context=market_context,
        snapshot_time=snapshot_time,
    )
    safe_ts = _safe_name(str(current["snapshot_time"]))
    snapshot_path = snapshots_dir / f"snapshot_{safe_ts}.json"
    latest_snapshot_path = snapshots_dir / "latest_snapshot.json"

    previous = _read_json(latest_snapshot_path) if latest_snapshot_path.exists() else None
    _write_json(snapshot_path, current)
    _write_json(latest_snapshot_path, current)

    result: Dict[str, Any] = {
        "snapshot_path": str(snapshot_path),
        "latest_snapshot_path": str(latest_snapshot_path),
        "delta_path": None,
        "latest_delta_path": None,
        "snapshot": current,
        "delta": None,
    }

    if previous:
        delta = build_delta(previous, current)
        delta_path = snapshots_dir / f"delta_{_safe_name(str(previous.get('snapshot_time', 'prev')))}__{safe_ts}.json"
        latest_delta_path = snapshots_dir / "latest_delta.json"
        _write_json(delta_path, delta)
        _write_json(latest_delta_path, delta)
        result.update({
            "delta_path": str(delta_path),
            "latest_delta_path": str(latest_delta_path),
            "delta": delta,
        })

    return result
