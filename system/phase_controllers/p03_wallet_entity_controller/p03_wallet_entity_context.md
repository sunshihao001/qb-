# P03 Wallet Entity Controller Context

P03 是钱包实体主数据治理控制器。它读取 P02 handoff 中授权的钱包事实种子、持有人快照、交易事实种子、质量/缺口/冲突记录，把地址转为 wallet entity、funding links、behavior features、same-source candidates、sync behavior candidates、role candidates。

## 边界
- 地址 ≠ 实体。
- 所有同源、同步、资金、角色判断均为 candidate。
- P03 不确认庄家/主导侧。
- P03 不判断筹码控制、派发、场景、策略准入。
- P03 不生成 evidence；证据归后续阶段。
- P03 只能交接给 P04。
- runtime/paper/live 全部阻断。
