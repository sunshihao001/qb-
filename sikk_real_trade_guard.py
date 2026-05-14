"""SIKK v0.2 真实交易确认保护层。

真实执行必须满足：
1. mode=real；
2. 用户显式输入 CONFIRM_REAL_TRADE；
3. 信号等级为 S3/S4；
4. 滑点不超过计划上限；
5. 本模块只授权，不执行 swap。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TradePlan:
    """真实交易计划摘要。"""

    mode: str
    chain: str
    wallet_address: str
    input_token: str
    output_token: str
    human_amount: str
    strategy_type: str
    signal_level: str
    max_slippage_pct: float


@dataclass
class TradeAuthorization:
    """真实交易授权结果。"""

    allowed: bool
    reason: str
    requires_confirmation: bool


class RealTradeGuard:
    """真实交易前的最后一道人工确认门。"""

    required_confirmation_text = "CONFIRM_REAL_TRADE"

    def authorize(self, plan: TradePlan, user_confirmation_text: str) -> TradeAuthorization:
        """判断是否允许把交易计划交给真实执行器。

        注意：即使 allowed=True，本方法也不会执行任何交易。
        """

        if plan.mode != "real":
            if plan.mode == "paper":
                return TradeAuthorization(False, "paper 模式禁止真实执行", True)
            return TradeAuthorization(False, f"未知执行模式：{plan.mode}", True)

        if user_confirmation_text.strip() != self.required_confirmation_text:
            return TradeAuthorization(False, "缺少明确人工确认 CONFIRM_REAL_TRADE", True)

        if plan.signal_level not in {"S3_策略观察信号", "S4_强确认信号", "S3", "S4"}:
            return TradeAuthorization(False, "信号等级不足，禁止真实执行", True)

        if plan.max_slippage_pct > 20:
            return TradeAuthorization(False, "滑点上限超过 20%，禁止真实执行", True)

        if not plan.wallet_address or not plan.input_token or not plan.output_token:
            return TradeAuthorization(False, "交易计划缺少钱包或代币地址", True)

        return TradeAuthorization(True, "已通过真实交易人工确认门；仍需执行层二次报价与安全扫描", False)
