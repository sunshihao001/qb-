#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v1.2 主导侧生命周期 + 行为动机旁路分类器。

边界：本模块只做候选生命周期/行为动机判断、paper/readiness 旁路输出和复盘字段生成；
不签名、不广播、不执行真实 swap。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from sikk_chip_control_state_machine import evaluate_chip_control_state


LIFECYCLE_BLOCK = {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION", "STRUCTURE_COLLAPSE"}
LIFECYCLE_TRADE_CANDIDATE = {"FAST_ACCUMULATION_LAUNCH", "SECOND_STAGE_EXPANSION", "REACTIVATION"}
LIFECYCLE_WATCH = {
    "EARLY_ACCUMULATION",
    "CONTROL_BOX_ACCUMULATION",
    "PARTIAL_DISTRIBUTION",
    "REACCUMULATION",
    "SECOND_STAGE_PREPARATION",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _num(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "是", "y"}
    return bool(value)


def _first(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return default


def _load_json(path: Path | str | None, default: Any) -> Any:
    if not path:
        return default
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("候选状态", "生命周期列表", "处理结果", "候选列表", "results", "items", "tokens"):
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return []


def _index_by_token(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        token = _first(row, "代币地址", "token_address", "token", "address")
        if token:
            out[str(token)] = row
    return out


def _load_wallet_decision(wallet_structure_dir: Path, token: str) -> dict[str, Any]:
    direct = wallet_structure_dir / token / "wallet_structure_decision.json"
    data = _load_json(direct, {})
    if isinstance(data, dict) and data:
        return data
    summary = _load_json(wallet_structure_dir / "candidate_wallet_structure_summary.json", {})
    for row in _rows_from_payload(summary):
        if _first(row, "代币地址", "token_address") == token:
            return row
    return {}


def _score_accumulation(wallet: dict[str, Any], market: dict[str, Any]) -> float:
    score = 0.0
    if _num(wallet.get("early_wallet_count")) >= 20:
        score += 20
    score += min(_num(wallet.get("same_source_sync_buy_score")), 100) * 0.20
    score += min(_num(wallet.get("early_wallet_remaining_pct")), 100) * 0.20
    score += min(_num(market.get("box_compression_score")), 100) * 0.15
    volume_trend = str(market.get("volume_trend", "")).upper()
    if volume_trend in {"CONTRACTING", "STABLE"}:
        score += 10
    score += max(0.0, 10 - abs(_num(market.get("top10_holder_pct_delta"), 0)))
    score += min(_num(wallet.get("data_quality_score"), 50), 100) * 0.05
    return round(max(0.0, min(score, 100.0)), 2)


def _score_distribution(wallet: dict[str, Any], market: dict[str, Any]) -> float:
    score = 0.0
    score += min(_num(wallet.get("early_wallet_sold_pct")), 100) * 0.25
    high_remain = _num(wallet.get("high_result_remaining_pct"), 50)
    score += max(0.0, 100 - high_remain) * 0.20
    score += min(_num(wallet.get("same_source_sync_sell_score")), 100) * 0.20
    score += max(0.0, -_num(_first(wallet, "top10_holder_pct_delta", default=market.get("top10_holder_pct_delta")))) * 2
    score += min(_num(wallet.get("late_large_buyer_count")), 10) * 1.0
    holder_delta = _num(_first(wallet, "holder_count_delta_pct", default=market.get("holder_count_delta_pct")))
    if holder_delta > 0 and _num(market.get("price_change_pct"), 0) <= 10:
        score += min(holder_delta, 10)
    if _bool(market.get("price_below_structure_level")) or _bool(market.get("price_below_control_box_low")):
        score += 5
    return round(max(0.0, min(score, 100.0)), 2)


def _score_control_retention(wallet: dict[str, Any], market: dict[str, Any]) -> float:
    score = 0.0
    score += min(_num(wallet.get("early_wallet_remaining_pct")), 100) * 0.25
    score += min(_num(wallet.get("high_result_remaining_pct")), 100) * 0.20
    score += min(_num(wallet.get("same_source_group_remaining_pct"), 50), 100) * 0.20
    score += max(0.0, 100 - min(_num(wallet.get("same_source_sync_sell_score")), 100)) * 0.15
    score += max(0.0, 100 - min(_num(wallet.get("counterparty_pressure_score")), 100)) * 0.10
    if not _bool(market.get("price_below_control_box_low")) and not _bool(market.get("price_below_structure_level")):
        score += 10
    return round(max(0.0, min(score, 100.0)), 2)


def classify_lifecycle(
    state_row: dict[str, Any],
    wallet_decision: dict[str, Any] | None = None,
    market_row: dict[str, Any] | None = None,
    signal_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    wallet = wallet_decision or {}
    market = market_row or {}
    signal = signal_row or {}

    token = str(_first(state_row, "代币地址", "token_address", default=_first(wallet, "代币地址", "token_address", default="")))
    symbol = str(_first(state_row, "代币符号", "token_symbol", default=_first(wallet, "代币符号", "token_symbol", default="")))
    wallet_status = str(_first(wallet, "wallet_structure_status", "钱包结构结论", default="WALLET_UNKNOWN"))
    wallet_score = _num(_first(wallet, "wallet_structure_score", "钱包结构评分", default=0))
    wallet_risk = _num(_first(wallet, "wallet_risk_score", "钱包风险评分", default=0))
    counterparty = _num(_first(wallet, "counterparty_pressure_score", "对手盘压力评分", default=0))
    data_quality = _num(_first(wallet, "data_quality_score", "数据质量评分", default=50))
    sync_sell = _num(wallet.get("same_source_sync_sell_score"))
    distribution_count = _num(wallet.get("distribution_wallet_count"))
    sold_delta = _num(wallet.get("early_wallet_sold_pct_delta"))
    top10_delta = _num(_first(wallet, "top10_holder_pct_delta", default=market.get("top10_holder_pct_delta")))
    holder_delta = _num(_first(wallet, "holder_count_delta_pct", default=market.get("holder_count_delta_pct")))
    token_age = _num(_first(market, "token_age_min", "代币年龄分钟", default=0))
    volume_expansion = _num(market.get("volume_expansion_score"))
    box_duration = _num(market.get("box_duration_min"))
    price_range = _num(market.get("price_range_pct"), 100)
    pattern = str(market.get("market_pattern_type", "UNKNOWN"))
    signal_level = str(_first(state_row, "信号等级", "signal_level", default=signal.get("信号等级", "UNKNOWN")))

    accumulation_score = _score_accumulation(wallet, market)
    distribution_score = _score_distribution(wallet, market)
    control_score = _score_control_retention(wallet, market)

    lifecycle = "UNKNOWN"
    intent = "UNKNOWN"
    allowed_action = "WATCHING"
    phase_signal = "NO_CLEAR_TRANSITION"
    risk_level = "MEDIUM"
    counterparty_state = "UNKNOWN"
    liquidity_intent = "UNKNOWN"
    defense = "UNKNOWN"
    trap = "UNKNOWN"
    evidence = "E1"
    reason_parts: list[str] = []

    structure_break = _bool(market.get("price_below_control_box_low")) or _bool(market.get("price_below_structure_level"))
    if structure_break and wallet_risk >= 70 and (sync_sell >= 60 or counterparty >= 60):
        lifecycle = "STRUCTURE_COLLAPSE"
        intent = "ABANDONMENT"
        allowed_action = "BLOCKED"
        phase_signal = "STRUCTURE_BREAKDOWN"
        risk_level = "HIGH"
        defense = "FAILED_DEFENSE"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E3"
        reason_parts.append("结构位跌破且钱包风险/同步卖出或对手盘压力同步升高")
    elif wallet_status == "WALLET_BLOCK" and (wallet_risk >= 90 or counterparty >= 70 or sync_sell >= 70 or distribution_count >= 2):
        lifecycle = "ACTIVE_DISTRIBUTION"
        intent = "ACTIVE_DISTRIBUTION"
        allowed_action = "BLOCKED"
        phase_signal = "DISTRIBUTION_ACTIVE"
        risk_level = "HIGH"
        counterparty_state = "EXIT_LIQUIDITY_FORMING" if counterparty >= 70 else "TRAPPED_COUNTERPARTY"
        liquidity_intent = "DISTRIBUTE_INTO_DEMAND"
        trap = "PUMP_TO_DISTRIBUTE" if volume_expansion >= 60 else "NO_TRAP_OBSERVED"
        evidence = "E4" if sold_delta >= 15 and top10_delta <= -5 and holder_delta >= 5 else "E3"
        reason_parts.append("钱包结构阻断，且风险/对手盘压力/分发侧证据达到主动派发条件")
    elif _num(wallet.get("early_wallet_sold_pct")) >= 85 and _num(wallet.get("high_result_remaining_pct"), 100) <= 10 and sync_sell >= 70:
        lifecycle = "FINAL_DISTRIBUTION"
        intent = "ACTIVE_DISTRIBUTION"
        allowed_action = "BLOCKED"
        phase_signal = "FINAL_EXIT"
        risk_level = "HIGH"
        counterparty_state = "TRAPPED_COUNTERPARTY"
        liquidity_intent = "DISTRIBUTE_INTO_DEMAND"
        trap = "PUMP_TO_DISTRIBUTE"
        evidence = "E3"
        reason_parts.append("早期/高结果钱包接近退出且同源卖出较强")
    elif _bool(market.get("second_stage_valid")) and volume_expansion >= 70 and counterparty < 60 and wallet_status != "WALLET_BLOCK":
        lifecycle = "REACTIVATION" if token_age > 120 else "SECOND_STAGE_EXPANSION"
        intent = "REACTIVATION" if lifecycle == "REACTIVATION" else "MARKUP"
        allowed_action = "REACTIVATED_BY_SECOND_STAGE" if lifecycle == "REACTIVATION" else "PAPER_READY_CANDIDATE"
        phase_signal = "SECOND_STAGE_VALID"
        risk_level = "LOW" if wallet_risk < 50 else "MEDIUM"
        counterparty_state = "NO_COUNTERPARTY_PRESSURE"
        liquidity_intent = "CREATE_BREAKOUT_LIQUIDITY"
        defense = "DEFENDING_CONTROL_BOX"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E3"
        reason_parts.append("出现有效二段/再激活放量，且钱包结构未冲突")
    elif (pattern == "CONTROL_BOX_ACCUMULATION" or box_duration >= 30) and price_range <= 35 and volume_expansion < 70 and counterparty < 60 and sync_sell < 60:
        if box_duration >= 120 and volume_expansion < 30 and wallet_score < 40:
            lifecycle = "DEAD_SIDEWAYS"
            intent = "ABANDONMENT"
            allowed_action = "COOLING"
            phase_signal = "NO_SECOND_STAGE"
            risk_level = "MEDIUM"
            defense = "NO_DEFENSE_OBSERVED"
            trap = "DEAD_CAT_REACTIVATION"
            reason_parts.append("长时间低量横盘且钱包结构支撑不足")
        elif volume_expansion >= 40 or _bool(market.get("price_near_control_box_high")):
            lifecycle = "SECOND_STAGE_PREPARATION"
            intent = "BREAKOUT_TEST"
            allowed_action = "HIGH_PRIORITY_WATCHING"
            phase_signal = "PRE_SECOND_STAGE"
            risk_level = "MEDIUM"
            defense = "DEFENDING_CONTROL_BOX"
            liquidity_intent = "TEST_BUY_DEPTH"
            trap = "NO_TRAP_OBSERVED"
            evidence = "E2"
            reason_parts.append("箱体横盘/压缩后接近突破测试，但尚未达到二段确认")
        else:
            lifecycle = "CONTROL_BOX_ACCUMULATION"
            intent = "CONTROL"
            allowed_action = "WATCHING"
            phase_signal = "CONTROL_BOX_ACTIVE"
            defense = "DEFENDING_CONTROL_BOX"
            liquidity_intent = "DEFEND_STRUCTURE_LEVEL"
            trap = "NO_TRAP_OBSERVED"
            evidence = "E2"
            reason_parts.append("价格区间收窄且成交量未扩张，疑似箱体控筹观察")
    elif token_age <= 45 and volume_expansion >= 70 and counterparty < 60 and wallet_status != "WALLET_BLOCK":
        lifecycle = "FAST_ACCUMULATION_LAUNCH"
        intent = "MARKUP"
        allowed_action = "PAPER_READY_CANDIDATE"
        phase_signal = "FAST_LAUNCH"
        risk_level = "MEDIUM"
        liquidity_intent = "CREATE_BREAKOUT_LIQUIDITY"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E2"
        reason_parts.append("早期快速放量且未见钱包结构冲突")
    elif token_age <= 15 and accumulation_score >= 50:
        lifecycle = "EARLY_ACCUMULATION"
        intent = "ACCUMULATE"
        allowed_action = "WATCHING"
        phase_signal = "EARLY_POSITION_BUILDING"
        risk_level = "MEDIUM"
        liquidity_intent = "BUILD_POSITION_LIQUIDITY"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E2"
        reason_parts.append("早期吸筹特征出现但仍需 K线/成交量确认")
    elif distribution_score >= 40 and control_score >= 50 and wallet_status != "WALLET_BLOCK":
        lifecycle = "PARTIAL_DISTRIBUTION"
        intent = "PARTIAL_DISTRIBUTION"
        allowed_action = "WATCHING"
        phase_signal = "PARTIAL_EXIT_REVIEW"
        risk_level = "MEDIUM"
        counterparty_state = "WHALE_ABSORBING" if counterparty >= 50 else "UNKNOWN"
        liquidity_intent = "DISTRIBUTE_INTO_DEMAND"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E2"
        reason_parts.append("存在部分派发证据，但控制权保留分仍未完全丧失")
    elif control_score >= 50 and distribution_score < 60:
        lifecycle = "REACCUMULATION"
        intent = "REACCUMULATION"
        allowed_action = "HIGH_PRIORITY_WATCHING"
        phase_signal = "REACCUMULATION_POSSIBLE"
        risk_level = "MEDIUM"
        defense = "DEFENDING_CONTROL_BOX"
        liquidity_intent = "DEFEND_STRUCTURE_LEVEL"
        trap = "NO_TRAP_OBSERVED"
        evidence = "E2"
        reason_parts.append("控制权仍部分保留且派发未进入后期，疑似再控筹观察")
    else:
        lifecycle = "UNKNOWN"
        intent = "UNKNOWN"
        allowed_action = "WATCHING"
        risk_level = "MEDIUM" if data_quality >= 50 else "HIGH"
        trap = "UNKNOWN"
        evidence = "E0" if data_quality < 50 else "E1"
        reason_parts.append("现有盘型/钱包/时间序列证据不足，保持观察")

    if counterparty_state == "UNKNOWN":
        if counterparty >= 70:
            counterparty_state = "TRAPPED_COUNTERPARTY"
        elif counterparty < 40:
            counterparty_state = "NO_COUNTERPARTY_PRESSURE"
    if defense == "UNKNOWN":
        defense = "FAILED_DEFENSE" if structure_break else "UNKNOWN"
    if trap == "UNKNOWN":
        trap = "NO_TRAP_OBSERVED" if lifecycle not in {"UNKNOWN"} else "UNKNOWN"

    would_block = lifecycle in LIFECYCLE_BLOCK
    would_pause = lifecycle in LIFECYCLE_WATCH or lifecycle == "DEAD_SIDEWAYS" or lifecycle == "UNKNOWN"
    confidence = 0.35
    if evidence == "E4":
        confidence = 0.86
    elif evidence == "E3":
        confidence = 0.74
    elif evidence == "E2":
        confidence = 0.62
    elif evidence == "E1":
        confidence = 0.45

    invalid_conditions = [
        "price_below_control_box_low",
        "same_source_sync_sell_score >= 70",
        "counterparty_pressure_score >= 70",
        "wallet_structure_status 转 WALLET_BLOCK",
    ]
    if lifecycle in LIFECYCLE_BLOCK:
        invalid_conditions = ["wallet_risk_score 降至 < 50 且多轮快照确认", "counterparty_pressure_score 降至 < 60", "同源同步卖出停止并出现结构修复"]

    alternative = "也可能只是数据缺失或单轮快照噪音，需等待多轮 wallet/kline delta 复核。"
    if lifecycle in {"SECOND_STAGE_PREPARATION", "CONTROL_BOX_ACCUMULATION"}:
        alternative = "也可能只是低量横盘后的普通反弹，需等待放量突破和回踩确认。"
    elif lifecycle in LIFECYCLE_BLOCK:
        alternative = "也可能是短期换手导致的风险升高，但需看到对手盘压力回落和结构侧重新持有才可降级。"

    reason = "；".join(reason_parts)
    chip_control = evaluate_chip_control_state(
        wallet_decision=wallet,
        lifecycle_row={
            "token_address": token,
            "token_symbol": symbol,
            "dominant_side_lifecycle": lifecycle,
            "dominant_side_intent": intent,
            "allowed_action": allowed_action,
            "counterparty_state": counterparty_state,
        },
        market_context=market,
    ).to_dict()
    return {
        "token_address": token,
        "token_symbol": symbol,
        "market_pattern_type": pattern,
        "dominant_side_lifecycle": lifecycle,
        "lifecycle_confidence": confidence,
        "accumulation_progress_score": accumulation_score,
        "distribution_progress_score": distribution_score,
        "control_retention_score": control_score,
        "phase_transition_signal": phase_signal,
        "lifecycle_risk_level": risk_level,
        "dominant_side_intent": intent,
        "intent_confidence": confidence,
        "counterparty_state": counterparty_state,
        "liquidity_intent": liquidity_intent,
        "structure_defense_status": defense,
        "trap_risk_type": trap,
        "evidence_level": evidence,
        "alternative_hypothesis": alternative,
        "invalid_conditions": invalid_conditions,
        "allowed_action": allowed_action,
        "would_block_by_lifecycle": would_block,
        "would_pause_by_lifecycle": would_pause,
        "lifecycle_reason": reason,
        "wallet_structure_status": wallet_status,
        "wallet_structure_score": wallet_score,
        "wallet_risk_score": wallet_risk,
        "counterparty_pressure_score": counterparty,
        "data_quality_score": data_quality,
        "chip_control_state": chip_control["chip_control_state"],
        "chip_control_confidence": chip_control["chip_control_confidence"],
        "chip_control_action": chip_control["chip_control_action"],
        "chip_control_reason_codes": chip_control["chip_control_reason_codes"],
        "chip_control_invalidators": chip_control["chip_control_invalidators"],
        "chip_control_evidence_refs": chip_control["chip_control_evidence_refs"],
        "current_state": _first(state_row, "当前状态", "current_state", default="UNKNOWN"),
        "signal_level": signal_level,
    }


def _cn_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "代币地址": row["token_address"],
        "代币符号": row["token_symbol"],
        "当前状态": row["current_state"],
        "信号等级": row["signal_level"],
        "盘型类型": row["market_pattern_type"],
        "主导侧生命周期": row["dominant_side_lifecycle"],
        "生命周期置信度": row["lifecycle_confidence"],
        "吸筹进度分": row["accumulation_progress_score"],
        "派发进度分": row["distribution_progress_score"],
        "控制权保留分": row["control_retention_score"],
        "阶段转换信号": row["phase_transition_signal"],
        "生命周期风险等级": row["lifecycle_risk_level"],
        "主导侧行为动机": row["dominant_side_intent"],
        "行为动机置信度": row["intent_confidence"],
        "对手盘状态": row["counterparty_state"],
        "流动性意图": row["liquidity_intent"],
        "结构防守状态": row["structure_defense_status"],
        "陷阱风险类型": row["trap_risk_type"],
        "证据等级": row["evidence_level"],
        "替代假设": row["alternative_hypothesis"],
        "失效条件": "；".join(row["invalid_conditions"]),
        "允许动作": row["allowed_action"],
        "would_block_by_lifecycle": row["would_block_by_lifecycle"],
        "would_pause_by_lifecycle": row["would_pause_by_lifecycle"],
        "生命周期原因": row["lifecycle_reason"],
        "钱包结构结论": row["wallet_structure_status"],
        "钱包结构评分": row["wallet_structure_score"],
        "钱包风险评分": row["wallet_risk_score"],
        "对手盘压力评分": row["counterparty_pressure_score"],
        "数据质量评分": row["data_quality_score"],
        "筹码控制权状态": row.get("chip_control_state"),
        "筹码控制置信度": row.get("chip_control_confidence"),
        "筹码控制动作": row.get("chip_control_action"),
        "筹码控制原因码": "；".join(row.get("chip_control_reason_codes") or []),
        "筹码控制失效条件": "；".join(row.get("chip_control_invalidators") or []),
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_md(path: Path, rows: list[dict[str, Any]], stats: dict[str, Any]) -> None:
    lines = [
        "# SIKK-SOL v1.2 主导侧生命周期旁路报告",
        "",
        "- 边界：本模块只生成生命周期旁路判断、行为动机推断和 paper/readiness 复盘字段，不执行真实 swap。",
        f"- 处理数量：{stats.get('处理数量', 0)}",
        "",
        "## 1. 生命周期统计",
    ]
    for k, v in stats.get("生命周期分布", {}).items():
        lines.append(f"- {k}：{v}")
    lines.extend(["", "## 2. 重点结果"])
    for row in rows[:30]:
        lines.extend(
            [
                f"- {row['代币符号']} / {row['代币地址']}",
                f"  - 当前状态：{row['当前状态']}",
                f"  - 主导侧生命周期：{row['主导侧生命周期']} / 置信度={row['生命周期置信度']}",
                f"  - 主导侧行为动机：{row['主导侧行为动机']}",
                f"  - 允许动作：{row['允许动作']}",
                f"  - 钱包结构：{row['钱包结构结论']} / 风险={row['钱包风险评分']} / 对手盘={row['对手盘压力评分']}",
                f"  - 原因：{row['生命周期原因']}",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_dominant_lifecycle_classifier(
    *,
    candidate_states_path: Path | str,
    wallet_structure_dir: Path | str,
    kline_summary_path: Path | str | None,
    signal_summary_path: Path | str | None,
    output_dir: Path | str,
) -> dict[str, Any]:
    candidate_states_path = Path(candidate_states_path)
    wallet_structure_dir = Path(wallet_structure_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    state_rows = _rows_from_payload(_load_json(candidate_states_path, {}))
    kline_index = _index_by_token(_rows_from_payload(_load_json(kline_summary_path, {})))
    signal_index = _index_by_token(_rows_from_payload(_load_json(signal_summary_path, {})))

    decisions: list[dict[str, Any]] = []
    cn_rows: list[dict[str, Any]] = []
    for state in state_rows:
        token = str(_first(state, "代币地址", "token_address", default=""))
        if not token:
            continue
        wallet = _load_wallet_decision(wallet_structure_dir, token)
        market = kline_index.get(token, {})
        signal = signal_index.get(token, {})
        decision = classify_lifecycle(state, wallet, market, signal)
        decisions.append(decision)
        cn = _cn_row(decision)
        cn_rows.append(cn)
        token_dir = output_dir / token
        token_dir.mkdir(parents=True, exist_ok=True)
        (token_dir / "dominant_lifecycle_decision.json").write_text(json.dumps(cn | decision, ensure_ascii=False, indent=2), encoding="utf-8")

    lifecycle_counts: dict[str, int] = {}
    action_counts: dict[str, int] = {}
    for row in decisions:
        lifecycle_counts[row["dominant_side_lifecycle"]] = lifecycle_counts.get(row["dominant_side_lifecycle"], 0) + 1
        action_counts[row["allowed_action"]] = action_counts.get(row["allowed_action"], 0) + 1

    stats = {
        "处理数量": len(decisions),
        "生命周期分布": lifecycle_counts,
        "允许动作分布": action_counts,
        "would_block数量": sum(1 for r in decisions if r["would_block_by_lifecycle"]),
        "would_pause数量": sum(1 for r in decisions if r["would_pause_by_lifecycle"]),
    }
    payload = {
        "模块": "SIKK-SOL v1.2 主导侧生命周期旁路分类器",
        "生成时间": _now_iso(),
        "统计": stats,
        "生命周期列表": cn_rows,
        "technical_results": decisions,
        "说明": "本模块只生成生命周期旁路判断和行为动机推断，不执行真实 swap；默认不改变状态机，仅供 observe/paper 复盘。",
    }
    (output_dir / "dominant_lifecycle_summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_csv(output_dir / "dominant_lifecycle_summary.csv", cn_rows)
    _write_md(output_dir / "dominant_lifecycle_summary.md", cn_rows, stats)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="SIKK-SOL v1.2 主导侧生命周期旁路分类器")
    parser.add_argument("--candidate-states", required=True)
    parser.add_argument("--wallet-structure-dir", required=True)
    parser.add_argument("--kline-summary", default="")
    parser.add_argument("--signal-summary", default="")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run_dominant_lifecycle_classifier(
        candidate_states_path=args.candidate_states,
        wallet_structure_dir=args.wallet_structure_dir,
        kline_summary_path=args.kline_summary or None,
        signal_summary_path=args.signal_summary or None,
        output_dir=args.output_dir,
    )
    print(json.dumps({"输出目录": args.output_dir, "统计": result["统计"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
