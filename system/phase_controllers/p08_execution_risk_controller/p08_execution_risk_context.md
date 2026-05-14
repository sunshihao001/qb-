# Auto-landed by HER P08 package landing
# generated_at: 2026-05-12T05:47:29Z
# authority: user uploaded P08 Execution Risk Controller 专业版 v3.0
# P08 Execution Risk Controller Context

P08 是执行前风控、报价安全、滑点费用、纸面运行许可与 Paper-only Runtime 交接控制器。它不重新判断策略优劣，也不是下单器。P08 只能读取 P07 授权的 PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED 候选，并重新检查当前 quote、quote consistency、liquidity depth、slippage、cost、安全、sellability、freshness、P07 invalidation、wallet delta refresh、runtime risk limits、position uniqueness、circuit breaker。

最高权限：生成 `PAPER_RUNTIME_ALLOWED` 或 `PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS` 并交接给 Paper-only Runtime。

永久禁止：`LIVE_EXECUTION_ALLOWED`、钱包签名、真实下单、自动 swap、绕过 P07、绕过 Paper-only Runtime。
