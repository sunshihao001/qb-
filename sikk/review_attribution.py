# -*- coding: utf-8 -*-
"""Review attribution and issue registry for single-token replay."""
from __future__ import annotations

from typing import Any, Dict, List


def build_issue_registry(context: Dict[str, Any], wallet_eval: Dict[str, Any], scenario_eval: Dict[str, Any], decision: Dict[str, Any]) -> str:
    missing = decision.get("missing_fields") or []
    issues: List[str] = []
    for field in missing:
        issues.append(f"- [ ] 缺失字段 `{field}`：补充本地事实缓存或只读采集结果。")
    for ce in decision.get("counter_evidence") or []:
        issues.append(f"- [ ] 反证/限制：{ce}")
    if not issues:
        issues.append("- [x] 本轮未发现阻断级缺口。")
    lines = [
        "# Issue Registry",
        "",
        f"- token: `{context.get('token')}`",
        f"- final_status: `{decision.get('final_status')}`",
        f"- decision: `{decision.get('decision')}`",
        "",
        "## 缺口 / 失败原因 / 后续补强",
        *issues,
        "",
        "## 规则升级候选（P10，仅建议，不自动改实时规则）",
    ]
    if decision.get("decision") in {"EXCLUDE", "RISK_MONITOR"}:
        lines.append(f"- 建议复核 `{scenario_eval.get('scenario')}` 场景下的钱包撤退/接盘压力阈值。")
    if "wallet_rows" in missing:
        lines.append("- 建议优先补 GMGN holders/traders 或 source_wallet_packet 钱包事实。")
    if "kline_rows" in missing:
        lines.append("- 建议补 K线/成交量以识别突破、横盘、诱多反抽。")
    if "quote_security" in missing:
        lines.append("- 建议补 quote/security 以验证流动性与安全风险。")
    if not any(line.startswith("- 建议") for line in lines):
        lines.append("- 暂无自动规则升级建议。")
    return "\n".join(lines) + "\n"


def build_review_attribution(context: Dict[str, Any], paper: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    history = context.get("paper_history") or []
    if not history:
        return {
            "has_existing_paper_result": False,
            "attribution": "暂无历史 paper 结果；本轮只记录候选决策与证据。",
            "success_factors": [],
            "failure_factors": decision.get("counter_evidence") or [],
        }
    return {
        "has_existing_paper_result": True,
        "paper_history_count": len(history),
        "attribution": "已发现历史 paper 记录，需结合实际收益字段复核。",
        "success_factors": ["历史记录存在，可用于后续人工复盘"],
        "failure_factors": decision.get("counter_evidence") or [],
    }
