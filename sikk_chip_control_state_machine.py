#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v0.3 筹码控制权状态机。

定位：把钱包结构、主导侧生命周期、市值上下文与 paper 状态压缩成可复盘的
筹码控制权状态。只输出 paper/观察层可消费的状态、证据、失效条件；不签名、
不广播、不执行真实 swap。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

CHIP_CONTROL_STATES = {
    "CONTROL_RETAINED_BY_STRUCTURE_SIDE",
    "CONTROL_MIGRATING_TO_COUNTERPARTY",
    "CONTROL_LOST_TO_DISTRIBUTION",
    "CONTROL_UNCLEAR",
    "DATA_QUALITY_FAIL",
}

STATE_TO_ACTION = {
    "CONTROL_RETAINED_BY_STRUCTURE_SIDE": "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS",
    "CONTROL_MIGRATING_TO_COUNTERPARTY": "PAUSE_OR_EXIT_MONITOR",
    "CONTROL_LOST_TO_DISTRIBUTION": "BLOCK_OR_FORCE_PAPER_EXIT",
    "CONTROL_UNCLEAR": "OBSERVE_ONLY",
    "DATA_QUALITY_FAIL": "OBSERVE_DATA_REPAIR",
}

BLOCKING_LIFECYCLES = {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION", "STRUCTURE_COLLAPSE"}
MIGRATING_LIFECYCLES = {"PARTIAL_DISTRIBUTION", "REACCUMULATION"}
SUPPORTIVE_LIFECYCLES = {"EARLY_ACCUMULATION", "CONTROL_BOX_ACCUMULATION", "SECOND_STAGE_PREPARATION", "SECOND_STAGE_EXPANSION", "REACTIVATION", "FAST_ACCUMULATION_LAUNCH"}


@dataclass
class ChipControlDecision:
    token_address: str = ""
    token_symbol: str = ""
    chip_control_state: str = "CONTROL_UNCLEAR"
    chip_control_confidence: int = 0
    chip_control_action: str = "OBSERVE_ONLY"
    risk_level: str = "INFO"
    reason_codes: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    invalidators: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    evaluated_at: str = ""
    scope_note: str = "筹码控制权状态只用于 paper/观察/复盘，不代表真实交易授权。"

    def to_dict(self) -> dict[str, Any]:
        return {
            "token_address": self.token_address,
            "token_symbol": self.token_symbol,
            "chip_control_state": self.chip_control_state,
            "筹码控制权状态": self.chip_control_state,
            "chip_control_confidence": self.chip_control_confidence,
            "筹码控制置信度": self.chip_control_confidence,
            "chip_control_action": self.chip_control_action,
            "筹码控制动作": self.chip_control_action,
            "risk_level": self.risk_level,
            "reason_codes": self.reason_codes,
            "chip_control_reason_codes": self.reason_codes,
            "evidence_refs": self.evidence_refs,
            "chip_control_evidence_refs": self.evidence_refs,
            "invalidators": self.invalidators,
            "chip_control_invalidators": self.invalidators,
            "missing_fields": self.missing_fields,
            "evaluated_at": self.evaluated_at,
            "scope_note": self.scope_note,
            "说明": self.scope_note,
        }


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _first(mapping: Mapping[str, Any] | None, *keys: str, default: Any = None) -> Any:
    if not isinstance(mapping, Mapping):
        return default
    for key in keys:
        if key in mapping and mapping[key] not in (None, "", [], {}):
            return mapping[key]
    return default


def _num(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(str(value).strip().rstrip("%"))
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "是"}
    return bool(value)


def _pct_change(start: Any, end: Any) -> float | None:
    s = _num(start, 0.0)
    e = _num(end, 0.0)
    if s <= 0 or e <= 0:
        return None
    return round((e - s) / s * 100, 4)


def evaluate_chip_control_state(
    *,
    wallet_decision: Mapping[str, Any] | None = None,
    lifecycle_row: Mapping[str, Any] | None = None,
    market_context: Mapping[str, Any] | None = None,
    paper_row: Mapping[str, Any] | None = None,
) -> ChipControlDecision:
    """Evaluate chip-control state from existing evidence.

    The function deliberately does not create trading authorization. Supportive output
    maps only to `ALLOW_PAPER_READY_IF_OTHER_GATES_PASS`.
    """

    wallet = wallet_decision or {}
    lifecycle = lifecycle_row or {}
    market = market_context or {}
    paper = paper_row or {}

    token = str(_first(wallet, "token_address", "代币地址", "token", default=_first(lifecycle, "token_address", "代币地址", default=_first(market, "token_address", "代币地址", default=""))))
    symbol = str(_first(wallet, "symbol", "token_symbol", "代币符号", default=_first(lifecycle, "symbol", "token_symbol", "代币符号", default="")))

    wallet_status = str(_first(wallet, "wallet_structure_status", "钱包结构结论", default="WALLET_UNKNOWN"))
    wallet_score = _num(_first(wallet, "wallet_structure_score", "钱包结构评分", default=0))
    wallet_risk = _num(_first(wallet, "wallet_risk_score", "钱包风险评分", default=0))
    counterparty = _num(_first(wallet, "counterparty_pressure_score", "对手盘压力评分", default=0))
    data_quality = _num(_first(wallet, "data_quality_score", "数据质量评分", default=0))
    data_quality_status = str(_first(wallet, "data_quality_status", "数据质量状态", default="UNKNOWN"))
    sync_sell = _num(_first(wallet, "max_sync_sell_score", "same_source_sync_sell_score", "最高同步卖出分", default=0))
    sync_buy = _num(_first(wallet, "max_sync_buy_score", "same_source_sync_buy_score", "最高同步买入分", default=0))
    has_clearout = _bool(_first(wallet, "has_concentrated_clearout", "是否存在集中清仓", default=False))
    has_distribution = _bool(_first(wallet, "has_distribution", "是否存在分发派发", default=False))
    has_sync_sell = _bool(_first(wallet, "has_same_source_sync_sell", "是否存在同源组同步卖出", default=False))

    lifecycle_state = str(_first(lifecycle, "dominant_side_lifecycle", "lifecycle", "主导侧生命周期", default="UNKNOWN"))
    lifecycle_intent = str(_first(lifecycle, "dominant_side_intent", "intent", "主导侧意图", default="UNKNOWN"))
    lifecycle_action = str(_first(lifecycle, "allowed_action", "允许动作", default="UNKNOWN"))

    discovery_mc = _first(market, "discovery_market_cap_usd", "发现市值", default=None)
    current_mc = _first(market, "current_market_cap_usd", "当前市值", default=None)
    paper_status = str(_first(paper, "paper_status", "纸面状态", default="NONE")).upper()

    missing: list[str] = []
    if not wallet:
        missing.append("wallet_decision")
    if data_quality_status in {"MISSING", "DEGRADED"} or data_quality <= 0:
        missing.append("wallet_data_quality")

    reasons: list[str] = []
    refs: list[str] = []
    invalidators: list[str] = []
    confidence = 20
    state = "CONTROL_UNCLEAR"
    risk_level = "INFO"

    if missing and not wallet:
        state = "DATA_QUALITY_FAIL"
        risk_level = "MEDIUM"
        reasons.append("DATA_QUALITY_FAIL")
        invalidators.append("缺少 wallet_structure_decision，不能判断筹码控制权")
    elif data_quality_status == "MISSING" or data_quality < 35:
        state = "DATA_QUALITY_FAIL"
        confidence = 35
        risk_level = "MEDIUM"
        reasons.append("WALLET_DATA_QUALITY_FAIL")
        invalidators.append("钱包结构数据质量不足，必须补采或降级观察")
    elif lifecycle_state in BLOCKING_LIFECYCLES or has_distribution:
        state = "CONTROL_LOST_TO_DISTRIBUTION"
        confidence = 85 if lifecycle_state in BLOCKING_LIFECYCLES else 78
        risk_level = "HIGH"
        reasons.append("CONTROL_BREAK_OR_DISTRIBUTION")
        if lifecycle_state in BLOCKING_LIFECYCLES:
            reasons.append(f"LIFECYCLE_{lifecycle_state}")
        if wallet_status == "WALLET_BLOCK":
            reasons.append("WALLET_BLOCK")
        if has_distribution:
            reasons.append("DISTRIBUTION_ACTIVE")
        invalidators.extend(["主动分发/生命周期阻断已出现", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
    elif has_sync_sell or sync_sell >= 60 or counterparty >= 50 or lifecycle_state in MIGRATING_LIFECYCLES:
        state = "CONTROL_MIGRATING_TO_COUNTERPARTY"
        confidence = 70 if (has_sync_sell or sync_sell >= 70 or counterparty >= 70) else 58
        risk_level = "HIGH" if counterparty >= 70 else "MEDIUM"
        reasons.append("CONTROL_MIGRATING_TO_COUNTERPARTY")
        if has_sync_sell or sync_sell >= 60:
            reasons.append("SAME_SOURCE_SYNC_SELL")
        if counterparty >= 50:
            reasons.append("COUNTERPARTY_PRESSURE_HIGH")
        if lifecycle_state in MIGRATING_LIFECYCLES:
            reasons.append(f"LIFECYCLE_{lifecycle_state}")
        invalidators.extend(["对手盘压力继续升高", "同源/同步组继续卖出", "高结果钱包持仓继续下降"])
    elif has_clearout or (wallet_status == "WALLET_BLOCK" and not has_sync_sell and sync_sell < 60):
        state = "CONTROL_LOST_TO_DISTRIBUTION" if (has_clearout or has_distribution or lifecycle_state in {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION"}) else "CONTROL_MIGRATING_TO_COUNTERPARTY"
        confidence = 85 if lifecycle_state in BLOCKING_LIFECYCLES else 75
        risk_level = "HIGH"
        reasons.append("CONTROL_BREAK_OR_DISTRIBUTION")
        if lifecycle_state in BLOCKING_LIFECYCLES:
            reasons.append(f"LIFECYCLE_{lifecycle_state}")
        if wallet_status == "WALLET_BLOCK":
            reasons.append("WALLET_BLOCK")
        if has_clearout:
            reasons.append("CONCENTRATED_CLEAROUT")
        if has_distribution:
            reasons.append("DISTRIBUTION_ACTIVE")
        invalidators.extend(["早期/结构侧钱包继续清仓", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
    elif wallet_status == "WALLET_SUPPORT" and wallet_score >= 60 and wallet_risk < 35 and counterparty < 40:
        state = "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
        confidence = 72
        risk_level = "LOW"
        reasons.append("STRUCTURE_SIDE_RETAINED")
        if sync_buy >= 70 and sync_sell < 40:
            confidence += 8
            reasons.append("SYNC_BUY_WITHOUT_SYNC_SELL")
        if lifecycle_state in SUPPORTIVE_LIFECYCLES:
            confidence += 8
            reasons.append(f"LIFECYCLE_{lifecycle_state}")
        invalidators.extend(["同源/同步组卖出分升至 60+", "对手盘压力升至 50+", "wallet_structure_status 变为 WALLET_PAUSE/WALLET_BLOCK", "quote/security 未通过时不得进入 PAPER_READY"])
    elif wallet_score >= 20 and wallet_risk < 35 and counterparty < 40 and data_quality >= 35:
        state = "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
        confidence = 48
        risk_level = "MEDIUM"
        reasons.append("MINIMAL_STRUCTURE_SIDE_RETAINED")
        invalidators.extend(["单点结构证据偏弱，只能作为记录/观察", "quote/security 未通过时不得进入 PAPER_READY"])
    else:
        state = "CONTROL_UNCLEAR"
        confidence = 45 if data_quality >= 50 else 30
        risk_level = "MEDIUM" if wallet_risk >= 35 or counterparty >= 35 else "INFO"
        reasons.append("CONTROL_UNCLEAR")
        invalidators.append("缺少足够结构侧保留或迁移证据")

    mc_change = _pct_change(discovery_mc, current_mc)
    if mc_change is not None:
        refs.append(f"market_cap_change_from_discovery_pct={mc_change}")
        if mc_change >= 500 and state == "CONTROL_RETAINED_BY_STRUCTURE_SIDE":
            risk_level = "MEDIUM"
            reasons.append("MARKET_CAP_EXTENDED_AFTER_DISCOVERY")
            invalidators.append("发现后市值已大幅拉升，需警惕高位派发/追高风险")
    elif market:
        missing.append("market_cap_context")

    if paper_status == "OPEN" and state in {"CONTROL_MIGRATING_TO_COUNTERPARTY", "CONTROL_LOST_TO_DISTRIBUTION"}:
        reasons.append("PAPER_OPEN_REQUIRES_EXIT_MONITOR")
        invalidators.append("paper 仓位应进入 EXIT_MONITOR / FORCE_PAPER_EXIT 复盘路径")

    refs.extend([
        "wallet_structure_decision.json" if wallet else "wallet_structure_decision_missing",
        "dominant_lifecycle" if lifecycle else "dominant_lifecycle_missing",
        "market_cap_context" if market else "market_cap_context_missing",
    ])
    confidence = int(max(0, min(round(confidence), 100)))
    reasons = list(dict.fromkeys(reasons))
    refs = list(dict.fromkeys(refs))
    invalidators = list(dict.fromkeys(invalidators))
    missing = list(dict.fromkeys(missing))

    return ChipControlDecision(
        token_address=token,
        token_symbol=symbol,
        chip_control_state=state,
        chip_control_confidence=confidence,
        chip_control_action=STATE_TO_ACTION[state],
        risk_level=risk_level,
        reason_codes=reasons,
        evidence_refs=refs,
        invalidators=invalidators,
        missing_fields=missing,
        evaluated_at=_now_iso(),
    )


__all__ = ["CHIP_CONTROL_STATES", "STATE_TO_ACTION", "ChipControlDecision", "evaluate_chip_control_state"]
