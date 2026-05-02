"""SIKK 自动交易准备框架：仓位建议。"""

from __future__ import annotations

from sikk_auto_trade_types import PositionPlan, RiskGateResult, SignalLevel, SignalResult, TradePermission


def calculate_position_plan(
    *,
    account_equity_sol: float,
    risk_per_trade_pct: float,
    entry_price: float,
    stop_price: float | None,
    signal: SignalResult,
    risk_gate: RiskGateResult,
    max_position_sol: float = 0.2,
    liquidity_factor: float = 1.0,
) -> PositionPlan:
    """根据止损距离和信号等级计算建议纸面仓位。

    参数中的 `risk_per_trade_pct` 使用百分数，例如 0.25 表示 0.25%。
    """

    risk_per_trade_sol = account_equity_sol * (risk_per_trade_pct / 100.0)

    if risk_gate.permission in {TradePermission.BLOCK_BUY, TradePermission.PAUSE_NEED_CONFIRM}:
        return PositionPlan(0.0, max_position_sol, risk_per_trade_sol, stop_price, "无", "风险门禁未通过，仓位为 0")
    if signal.signal_level not in {SignalLevel.S3, SignalLevel.S4}:
        return PositionPlan(0.0, max_position_sol, risk_per_trade_sol, stop_price, "无", "信号等级不足，仓位为 0")
    if not entry_price or not stop_price or stop_price >= entry_price:
        return PositionPlan(0.0, max_position_sol, risk_per_trade_sol, stop_price, "无", "止损价无效，仓位为 0")

    stop_distance_pct = (entry_price - stop_price) / entry_price
    if stop_distance_pct <= 0:
        return PositionPlan(0.0, max_position_sol, risk_per_trade_sol, stop_price, "无", "止损距离无效，仓位为 0")

    signal_factor = 0.5 if signal.signal_level == SignalLevel.S3 else 1.0
    theoretical_position = risk_per_trade_sol / stop_distance_pct
    position = theoretical_position * signal_factor * max(0.0, min(liquidity_factor, 1.0))
    position = round(min(position, max_position_sol), 6)

    return PositionPlan(
        suggested_position_sol=position,
        max_position_sol=max_position_sol,
        risk_per_trade_sol=round(risk_per_trade_sol, 6),
        stop_price=stop_price,
        stop_type="结构止损",
        position_reason=f"按 {risk_per_trade_pct}% 单笔风险、{signal.signal_level.value} 信号、止损距离 {stop_distance_pct:.2%} 计算",
    )
