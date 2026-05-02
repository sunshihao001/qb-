"""SIKK v0.2 预交易安全检查聚合器。

负责把 GMGN/OKX 等多源安全扫描结果合并成交易前门禁。
本模块不调用 CLI，只处理已经取得的扫描结果。
"""

from __future__ import annotations

from typing import Iterable, List

from sikk_execution_adapter_base import PreTradeSecurityDecision, SecurityScanResult, TokenSide


_RISK_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def _norm(level: str) -> str:
    value = (level or "UNKNOWN").strip().upper()
    return value if value in _RISK_RANK else "HIGH"


def evaluate_pre_trade_security(results: Iterable[SecurityScanResult]) -> PreTradeSecurityDecision:
    """聚合多源安全扫描结果。

    规则：
    - 买入侧 CRITICAL：BLOCK_BUY
    - 买入侧 HIGH：PAUSE_NEED_CONFIRM
    - 卖出侧 CRITICAL/HIGH：WARN_ALLOW_SELL，用于允许退出风险仓位
    - MEDIUM：WARN_CONTINUE
    - LOW：ALLOW
    """

    rows: List[SecurityScanResult] = list(results)
    if not rows:
        return PreTradeSecurityDecision(
            permission="PAUSE_NEED_CONFIRM",
            risk_level="UNKNOWN",
            requires_user_confirmation=True,
            reasons=["安全扫描结果缺失，需要人工确认"],
            source_count=0,
        )

    reasons: List[str] = []
    highest = "LOW"
    permission = "ALLOW"
    requires_confirmation = False

    for row in rows:
        level = _norm(row.risk_level)
        if _RISK_RANK[level] > _RISK_RANK.get(highest, 0):
            highest = level
        labels = ",".join(row.triggered_labels) if row.triggered_labels else "无标签明细"

        if row.token_side == TokenSide.BUY and level == "CRITICAL":
            permission = "BLOCK_BUY"
            reasons.append(f"买入侧 CRITICAL 风险：{row.source} {row.token_address} {labels}")
        elif row.token_side == TokenSide.BUY and level == "HIGH" and permission != "BLOCK_BUY":
            permission = "PAUSE_NEED_CONFIRM"
            requires_confirmation = True
            reasons.append(f"买入侧 HIGH 风险：{row.source} {row.token_address} {labels}")
        elif row.token_side == TokenSide.SELL and level in {"HIGH", "CRITICAL"} and permission == "ALLOW":
            permission = "WARN_ALLOW_SELL"
            reasons.append(f"卖出侧 {level} 风险：允许退出但需提示 {row.source} {labels}")
        elif level == "MEDIUM" and permission == "ALLOW":
            permission = "WARN_CONTINUE"
            reasons.append(f"{row.source} 中等风险：{labels}")

    if permission == "ALLOW":
        reasons.append("多源安全扫描未发现 HIGH/CRITICAL 买入风险")

    return PreTradeSecurityDecision(
        permission=permission,
        risk_level=highest,
        requires_user_confirmation=requires_confirmation,
        reasons=reasons,
        source_count=len(rows),
    )
