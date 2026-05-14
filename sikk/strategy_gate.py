# -*- coding: utf-8 -*-
"""Personal paper-only strategy gate.

Allowed decisions only: EXCLUDE, WATCH, RISK_MONITOR, PAPER_READY,
READY_FOR_CONFIRMATION.
"""
from __future__ import annotations

from typing import Any, Dict, List

ALLOWED_DECISIONS = ["EXCLUDE", "WATCH", "RISK_MONITOR", "PAPER_READY", "READY_FOR_CONFIRMATION"]


def decide_strategy(context: Dict[str, Any], wallet_eval: Dict[str, Any], scenario_eval: Dict[str, Any]) -> Dict[str, Any]:
    missing = list(dict.fromkeys((context.get("missing_fields") or []) + (wallet_eval.get("missing_fields") or [])))
    risk = float(wallet_eval.get("risk_score") or 0)
    support = float(wallet_eval.get("support_score") or 0)
    scenario = scenario_eval.get("scenario") or "证据不足观察"
    evidence: List[str] = list(wallet_eval.get("evidence") or []) + list(scenario_eval.get("reasons") or [])
    counter: List[str] = list(wallet_eval.get("counter_evidence") or []) + list(scenario_eval.get("counter_evidence") or [])

    if "local_token_data_files" in missing or "wallet_rows" in missing:
        decision = "EXCLUDE" if "local_token_data_files" in missing else "WATCH"
        reason = "关键本地数据不足，不能进入纸面验证"
    elif scenario in {"退出流动性陷阱", "接盘鲸鱼陷阱", "高位派发", "下跌再派发", "末端拉盘派发"}:
        decision = "RISK_MONITOR" if support >= 35 else "EXCLUDE"
        reason = f"当前场景偏风险：{scenario}"
    elif support >= 55 and risk < 55 and not missing:
        decision = "READY_FOR_CONFIRMATION"
        reason = "结构支持较强且关键字段完整，进入确认层；仍不允许实盘"
    elif support >= 45 and risk < 65:
        decision = "PAPER_READY"
        reason = "结构支持达到纸面验证阈值，只允许paper-only模拟"
    elif support >= 25:
        decision = "WATCH"
        reason = "存在观察价值但证据不足或风险偏高"
    else:
        decision = "EXCLUDE"
        reason = "结构证据不足或反证占优"

    if decision not in ALLOWED_DECISIONS:
        decision = "WATCH"
        reason = "非法决策被降级为WATCH"

    final_status = "SIKK_PERSONAL_REPLAY_READY"
    if missing and decision != "EXCLUDE":
        final_status = "SIKK_PERSONAL_REPLAY_READY_WITH_GAPS"
    if "local_token_data_files" in missing:
        final_status = "SIKK_PERSONAL_REPLAY_BLOCKED"

    return {
        "decision": decision,
        "allowed_decisions": ALLOWED_DECISIONS,
        "paper_only": True,
        "real_trade_allowed": False,
        "reason": reason,
        "support_score": support,
        "risk_score": risk,
        "scenario": scenario,
        "evidence": evidence,
        "counter_evidence": counter,
        "missing_fields": missing,
        "final_status": final_status,
    }
