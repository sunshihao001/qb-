# Next Round Fix Task Package (Issue Registry Only)

- ISSUE-001: 补齐 wallet row-level canonical export；保持旧路径 fallback；不改实时策略阈值
- ISSUE-002: 下一轮只评估 observe->enforce 的 Phase Controller 门禁参数，不直接改 live 策略
- ISSUE-003: 绑定现有 signal/kline/wallet outputs 到 P06 wrapper；仅生成被 replay 消费的输出
- ISSUE-004: 补 quote/security 缺字段状态化与来源标记
- ISSUE-005: 让 paper runner 对每个 closed position 写 token-level failure/review row
- ISSUE-006: 以 Phase Controller wrapper 收口 trace/handoff，不允许 runner 直连 paper

Constraints: do not add abstract standards; fix only replay-exposed issues; keep paper runner behind P07/P08.
