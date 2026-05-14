# -*- coding: utf-8 -*-
"""Tiny paper-only runner for single-token replay."""
from __future__ import annotations

from typing import Any, Dict, List
from .data_loader import utc_now


def run_paper_decision(context: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    action = "NO_PAPER_ENTRY"
    paper_state = "NOT_OPENED"
    reasons: List[str] = [decision.get("reason", "")]
    if decision.get("decision") == "PAPER_READY":
        action = "SIMULATE_PAPER_ENTRY"
        paper_state = "PAPER_ENTRY_CANDIDATE"
        reasons.append("仅记录纸面入场候选，不下单、不签名、不广播")
    elif decision.get("decision") == "READY_FOR_CONFIRMATION":
        action = "WAIT_CONFIRMATION_THEN_PAPER_ONLY"
        paper_state = "CONFIRMATION_REQUIRED"
        reasons.append("需要确认层；即使确认通过也只允许paper-only")
    elif decision.get("decision") == "RISK_MONITOR":
        action = "MONITOR_RISK_ONLY"
        paper_state = "RISK_MONITORING"
    elif decision.get("decision") == "WATCH":
        action = "WATCH_ONLY"
        paper_state = "WATCHING"
    else:
        action = "EXCLUDE_NO_ACTION"
        paper_state = "EXCLUDED"
    return {
        "paper_only": True,
        "real_trade_allowed": False,
        "action": action,
        "paper_state": paper_state,
        "token": context.get("token"),
        "created_at": utc_now(),
        "reasons": [r for r in reasons if r],
        "safety_boundary": ["不执行真实swap", "不读取/写入私钥", "不签名", "不广播", "不输出实盘买卖指令"],
    }


def render_paper_report(paper: Dict[str, Any]) -> str:
    lines = [
        "# Paper-only 决策报告",
        "",
        f"- token: `{paper.get('token')}`",
        f"- paper_state: `{paper.get('paper_state')}`",
        f"- action: `{paper.get('action')}`",
        f"- real_trade_allowed: `{paper.get('real_trade_allowed')}`",
        "",
        "## 原因",
    ]
    lines.extend([f"- {x}" for x in paper.get("reasons", [])] or ["- 无"])
    lines += ["", "## 安全边界"]
    lines.extend([f"- {x}" for x in paper.get("safety_boundary", [])])
    return "\n".join(lines) + "\n"
