# Phase07 Execution Risk Controller

## 阶段目标
读取 Phase06 策略资格，执行 Quote、安全、流动性、滑点、重复仓位、风险限制检查，输出纸面交易决策、人工确认票据、风险事件与 Phase08 handoff。

## 边界
- 不重新判断策略。
- 不生成买点。
- 不执行实盘。
- 硬否决高于纸面执行。

## Atomic Skills
quote_consistency_skill、liquidity_checker_skill、slippage_estimator_skill、security_gate_skill、duplicate_position_checker_skill、risk_limit_checker_skill、paper_trade_decision_skill。
