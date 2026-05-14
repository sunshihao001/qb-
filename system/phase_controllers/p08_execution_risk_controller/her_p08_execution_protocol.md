# Auto-landed by HER P08 package landing
# generated_at: 2026-05-12T05:47:29Z
# authority: user uploaded P08 Execution Risk Controller 专业版 v3.0
# HER P08 Execution Protocol

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P08 controller context
4. 读取 P07 → P08 handoff packet
5. 读取 p08_execution_risk_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 execution_risk_input_manifest
8. 校验 P07 candidate validity
9. 拉取或读取当前 quote snapshot
10. 执行 quote consistency check
11. 执行 liquidity depth check
12. 执行 slippage estimation
13. 建立 execution cost model
14. 执行 security recheck
15. 执行 sellability risk check
16. 执行 freshness recheck
17. 执行 invalidation precheck
18. 判断 wallet delta refresh requirement
19. 检查 runtime risk limits
20. 检查 position uniqueness
21. 检查 circuit breaker
22. 建立 paper entry simulation plan
23. 生成 paper_runtime_permission_record
24. 生成 execution_risk_block_reason_record
25. 生成 execution_risk_refresh_request_record
26. 生成 P08 gap report
27. 生成 paper_runtime_data_request_packet
28. 写入 P08 trace
29. 生成 p08_execution_risk_report
30. 生成 p08_to_paper_runtime_handoff_packet
31. 执行 P08 acceptance
32. 只允许 handoff 给 Paper-only Runtime

禁止：无 P07 handoff 启动、无 PAPER_CANDIDATE 执行、无 quote 进入纸面运行、忽略报价冲突/滑点/成本/安全/invalidation/risk limits/重复 token、绕过 Paper Runtime Handoff、生成 live execution permission、钱包签名、真实下单。
