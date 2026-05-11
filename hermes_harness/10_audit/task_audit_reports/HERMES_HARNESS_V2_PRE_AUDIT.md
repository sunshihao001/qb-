# HERMES HARNESS V2.0 PRE-AUDIT

结论：V1.7 已有 APUR、runtime hook、judgment governance、reliability calibration，但 V2.0 目标不是继续加模板，而是把运行时纪律、显式制度层、判断治理层合并为混合式 Harness。

## 缺口检查
- 显式控制面注册表：V2.0 前缺少结构化 rule_id/source/type/scope/precedence/status。
- thread_id / rollout / state bridge：V2.0 前有 runtime run，但缺稳定任务线程档案。
- tool schema / exec policy：V2.0 前有 ledger 思路，但缺策略检查器。
- context budget：已有原则，缺可检查状态文件。
- compact rebuild：已有认知，缺 post-compact 契约。
- 独立验证者 / meta-verification：V1.6 有治理产物，V2.0 需要制度化责任隔离。
- recovery circuit breaker：已有恢复规则，V2.0 需要阈值化。
- memory lifecycle：已有 revalidation 方向，V2.0 需要 candidate→verified→active→stale→superseded。
- judgment benchmark：V1.7 有 calibration，V2.0 需要样本库。
- anti-self-deception audit：V1.6 有审计，V2.0 需要固定审计面。

边界：本次只修改 /root/sikk-gmgn/hermes_harness/，不修改 SIKK 业务代码，不触发真实交易，不读取密钥。
