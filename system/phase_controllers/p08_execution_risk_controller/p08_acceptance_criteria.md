# Auto-landed by HER P08 package landing
# generated_at: 2026-05-12T05:47:29Z
# authority: user uploaded P08 Execution Risk Controller 专业版 v3.0
# P08 Acceptance Criteria

## P08_READY
- 45 个系统文件存在并可解析。
- 27 个运行数据目录存在。
- P07 handoff / P08 data request / paper runtime handoff contract 已定义。
- quote、liquidity、slippage、cost、security、sellability、freshness、invalidation、risk limits、position uniqueness、circuit breaker、permission 对象齐全。
- 明确禁止 live execution、wallet signing、real order。

## P08_READY_WITH_GAPS
包设计完成，但 runner/tool binding、真实 quote/security API、paper runtime 尚未落地。

## P08_REJECTED
缺少 P07 PAPER_CANDIDATE、输出合同或关键执行风险合同。

## P08_BLOCKED
缺 P07 handoff、trace/acceptance、quote、安全、live execution/wallet signing 请求或绕过 handoff。
