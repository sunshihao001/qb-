# SIKK 候选币状态机汇总

- 更新时间：2026-05-04T12:40:32Z
- 候选数量：5
- 执行边界：只管理状态与纸面准备，不执行真实 swap。

## 状态统计

- DISCOVERED：0
- WATCHING：2
- ACCUMULATING：0
- READY_TO_BUY：0
- PAPER_READY：1
- BLOCKED：2
- FAILED：0
- EXITED：0

## 候选状态

- 代币：trollina / Y4vtfnvGSTe2exSm94SXUq3684MGWwWEhXzASkupump
  - 当前状态：BLOCKED
  - 状态原因：吸筹窗口 invalid，进入风险阻断观察
  - 信号等级：
  - 风险门禁：
  - 钱包结构结论：未接入
- 代币：CARDS / ziffq43QSCC95DUjVc7cULKYttEHyA1pops25gDpump
  - 当前状态：BLOCKED
  - 状态原因：吸筹窗口 invalid，进入风险阻断观察
  - 信号等级：
  - 风险门禁：
  - 钱包结构结论：未接入
- 代币：TROLLIEN / ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump
  - 当前状态：PAPER_READY
  - 状态原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - 信号等级：S4_强确认信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
  - 钱包结构结论：WALLET_BLOCK
- 代币：trolls / 7CR3CBpivSMzBEet3cvUckjeSLdbCKaxRB1yNNm6pump
  - 当前状态：WATCHING
  - 状态原因：SIKK 信号仍为观察/预备层
  - 信号等级：S1_观察信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
  - 钱包结构结论：未接入
- 代币：jestin  / D5GpuB8FAWAc6Qex1p3B1vT9DJKvjPNuBzQgX5y3bonk
  - 当前状态：WATCHING
  - 状态原因：候选筛选等级为观察层，等待更多 K线/结构证据
  - 信号等级：
  - 风险门禁：
  - 钱包结构结论：未接入
