#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 主导侧心理与生命周期解释引擎。

本模块只把已有 K线/钱包/生命周期/筹码控制证据翻译成可读认知，
不重新裁决、不输出确定“庄家”、不执行真实交易。
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

BOUNDARY_NOTE = "主导侧心理解释只用于 paper 观察、复盘与风险审计；不执行真实 swap，不读取私钥，不签名，不广播。"

LABELS = {
    "ACCUMULATE_QUIETLY": "静默吸筹 / 早期控筹",
    "DEFEND_STRUCTURE_LEVEL": "防守结构位 / 箱体控筹",
    "TEST_BUY_DEPTH": "测试买盘深度 / 突破试盘",
    "CREATE_FOMO_LIQUIDITY": "制造追涨流动性 / 推升扩张",
    "DISTRIBUTE_INTO_DEMAND": "借需求派发 / 高位兑现",
    "TRAP_COUNTERPARTY": "诱导对手盘承接 / 套牢风险",
    "ABANDON_STRUCTURE": "放弃结构维护 / 控制失效",
    "REACCUMULATE_AFTER_WASH": "洗盘后再控筹 / 结构修复",
    "DATA_INSUFFICIENT": "证据不足 / 待复查",
}


def _pick(mapping: Mapping[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return value
    return default


def _nested(status: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    obj = status.get(name)
    return obj if isinstance(obj, Mapping) else {}


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except Exception:
        return default


def _upper(value: Any) -> str:
    return str(value or "").upper()


def _field(status: Mapping[str, Any], nested_name: str, *keys: str, default: Any = "") -> Any:
    nested = _nested(status, nested_name)
    return _pick(nested, *keys, default="") or _pick(status, *keys, default=default)


def evaluate_operator_psychology(status: Mapping[str, Any]) -> Dict[str, Any]:
    lifecycle = _upper(_field(status, "lifecycle", "dominant_side_lifecycle", "operator_lifecycle_stage", default="UNKNOWN"))
    intent = _upper(_field(status, "lifecycle", "dominant_side_intent", default="UNKNOWN"))
    counterparty = _upper(_field(status, "lifecycle", "counterparty_state", default="UNKNOWN"))
    liquidity_intent = _upper(_field(status, "lifecycle", "liquidity_intent", default="UNKNOWN"))
    trap = _upper(_field(status, "lifecycle", "trap_risk_type", default="UNKNOWN"))
    defense = _upper(_field(status, "lifecycle", "structure_defense_status", default="UNKNOWN"))
    chip_state = _upper(_field(status, "chip_control", "chip_control_state", default="CONTROL_UNCLEAR"))
    current_state = _upper(_pick(status, "current_state", default="UNKNOWN"))
    paper = _nested(status, "paper")
    paper_status = _upper(_pick(paper, "paper_status", "status", default=_pick(status, "status", default="")))
    market_ctx = _nested(status, "market_cap_context")
    cap_change = _num(_pick(market_ctx, "market_cap_change_from_discovery_pct", default=_pick(status, "entry_market_cap_change_from_discovery_pct", default=0)))

    psychology = "DATA_INSUFFICIENT"
    stage = lifecycle if lifecycle and lifecycle != "UNKNOWN" else "UNKNOWN"
    evidence_level = "E1"
    alignment = "DATA_INSUFFICIENT"
    risk_focus = "证据不足，先复查生命周期、钱包结构、市值上下文与多轮快照。"
    invalidation = ["生命周期证据缺失", "钱包结构或 K线 delta 未形成"]
    reason_parts = []

    if lifecycle in {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION", "PARTIAL_DISTRIBUTION"} or intent == "ACTIVE_DISTRIBUTION":
        psychology = "DISTRIBUTE_INTO_DEMAND"
        evidence_level = "E4" if lifecycle == "ACTIVE_DISTRIBUTION" and counterparty in {"EXIT_LIQUIDITY_FORMING", "TRAPPED_COUNTERPARTY"} else "E3"
        alignment = "LATE_IN_DISTRIBUTION" if paper_status in {"OPEN", "PAPER_OPEN"} or current_state in {"PAPER_READY", "PAPER_OPEN"} else "DISTRIBUTION_RISK_OBSERVED"
        risk_focus = "重点观察早期/高结果钱包剩余仓位、同步卖出、对手盘承接和价格是否跌破结构位。"
        invalidation = ["同源卖出停止", "对手盘压力下降", "结构侧重新防守并多轮确认"]
        reason_parts.append("生命周期进入派发/兑现侧，主导侧更可能在利用需求与流动性完成减仓。")
    elif lifecycle in {"STRUCTURE_COLLAPSE", "DEAD_SIDEWAYS"} or intent == "ABANDONMENT":
        psychology = "ABANDON_STRUCTURE"
        evidence_level = "E3"
        alignment = "AGAINST_LIFECYCLE"
        risk_focus = "重点观察是否只是短期换手噪音，还是结构侧已经不再维护价格与流动性。"
        invalidation = ["重新站回结构位", "成交量恢复且钱包风险下降", "筹码控制权重新回到结构侧"]
        reason_parts.append("结构维护失败或长时间低量横盘，疑似主导侧降低维护意愿。")
    elif lifecycle in {"SECOND_STAGE_EXPANSION", "REACTIVATION", "FAST_ACCUMULATION_LAUNCH"} or intent in {"MARKUP", "REACTIVATION"}:
        psychology = "CREATE_FOMO_LIQUIDITY"
        evidence_level = "E3"
        alignment = "ALIGNED_WITH_BREAKOUT" if cap_change < 300 else "CHASE_RISK_AFTER_MARKUP"
        risk_focus = "重点观察放量后是否回踩不破、早期钱包是否同步卖出、是否从推升转为派发。"
        invalidation = ["放量失败", "回踩跌破结构位", "早期钱包同步卖出增强"]
        reason_parts.append("二段/再激活/快速放量阶段更像制造突破流动性与追涨需求。")
    elif lifecycle in {"SECOND_STAGE_PREPARATION"} or intent in {"BREAKOUT_TEST"}:
        psychology = "TEST_BUY_DEPTH"
        evidence_level = "E2"
        alignment = "WATCH_BREAKOUT_CONFIRMATION"
        risk_focus = "观察突破是否放量、回踩是否守住、钱包结构是否继续支持。"
        invalidation = ["突破无量", "回踩跌破箱体上沿", "钱包结构转 WALLET_BLOCK"]
        reason_parts.append("接近突破但尚未完成确认，更像测试买盘深度。")
    elif lifecycle in {"CONTROL_BOX_ACCUMULATION", "REACCUMULATION"} or intent in {"CONTROL", "REACCUMULATION"} or defense == "DEFENDING_CONTROL_BOX":
        psychology = "DEFEND_STRUCTURE_LEVEL" if defense == "DEFENDING_CONTROL_BOX" or lifecycle == "CONTROL_BOX_ACCUMULATION" else "REACCUMULATE_AFTER_WASH"
        evidence_level = "E2"
        alignment = "ALIGNED_WITH_ACCUMULATION_OR_CONTROL"
        risk_focus = "观察箱体上下沿、成交量压缩后放大、结构钱包是否保留筹码。"
        invalidation = ["跌破箱体下沿", "结构钱包持续派发", "对手盘压力升高"]
        reason_parts.append("箱体/再控筹阶段更像结构侧维护价格区间并等待下一次流动性测试。")
    elif lifecycle in {"EARLY_ACCUMULATION"} or intent == "ACCUMULATE":
        psychology = "ACCUMULATE_QUIETLY"
        evidence_level = "E2"
        alignment = "ALIGNED_WITH_ACCUMULATION_OR_CONTROL"
        risk_focus = "观察早期钱包进入密度、GMGN 标签、是否转入 P1/P2 拉升。"
        invalidation = ["早期钱包快速清仓", "无后续成交量", "风险标签增强"]
        reason_parts.append("早期吸筹阶段更像低位建立初始筹码，但证据通常仍偏早。")
    elif counterparty in {"TRAPPED_COUNTERPARTY", "EXIT_LIQUIDITY_FORMING", "WHALE_ABSORBING"} or trap == "PUMP_TO_DISTRIBUTE":
        psychology = "TRAP_COUNTERPARTY"
        evidence_level = "E2"
        alignment = "COUNTERPARTY_TRAP_RISK"
        risk_focus = "观察晚买大额钱包、浮亏承接、派发侧卖压是否同步出现。"
        invalidation = ["对手盘浮亏修复", "派发侧停止卖出", "结构侧重新控筹"]
        reason_parts.append("对手盘承接/套牢证据出现，需要把上涨解释为可能的流动性制造，而非单纯利好。")
    else:
        reason_parts.append("主导侧心理证据不足，不能把盘型直接解释为明确控筹或派发。")

    if chip_state in {"CONTROL_LOST_TO_DISTRIBUTION_SIDE", "CONTROL_LOST", "DISTRIBUTION_CONTROL"} and psychology not in {"DISTRIBUTE_INTO_DEMAND", "ABANDON_STRUCTURE"}:
        reason_parts.append(f"筹码控制权状态={chip_state}，需提高派发/失控风险权重。")
    if cap_change >= 300 and psychology in {"CREATE_FOMO_LIQUIDITY", "DISTRIBUTE_INTO_DEMAND"}:
        reason_parts.append(f"相对发现时市值涨幅约 {cap_change:.1f}%，纸面入场需警惕追高与流动性承接。")

    reason = "".join(reason_parts)
    return {
        "token_address": _pick(status, "token_address", "代币地址", default=""),
        "token_symbol": _pick(status, "token_symbol", "代币符号", default=""),
        "operator_lifecycle_stage": stage,
        "operator_psychology": psychology,
        "operator_psychology_label": LABELS.get(psychology, psychology),
        "dominant_side_intent": intent,
        "counterparty_psychology": counterparty,
        "liquidity_intent": liquidity_intent,
        "trap_risk_type": trap,
        "structure_defense_status": defense,
        "chip_control_state": chip_state,
        "paper_trade_alignment": alignment,
        "psychology_evidence_level": evidence_level,
        "psychology_reason": f"主导侧心理解释：{reason}",
        "next_observation_focus": risk_focus,
        "invalidation_conditions": invalidation,
        "scope_note": BOUNDARY_NOTE,
    }


def enrich_status_with_operator_psychology(status: Mapping[str, Any]) -> Dict[str, Any]:
    enriched = dict(status)
    psychology = evaluate_operator_psychology(enriched)
    enriched["operator_psychology"] = psychology
    enriched["operator_lifecycle_stage"] = psychology["operator_lifecycle_stage"]
    enriched["operator_psychology_label"] = psychology["operator_psychology_label"]
    enriched["paper_trade_alignment"] = psychology["paper_trade_alignment"]
    return enriched


__all__ = ["evaluate_operator_psychology", "enrich_status_with_operator_psychology"]
