# SIKK 候选币状态机汇总

- 更新时间：2026-04-30T11:47:46Z
- 候选数量：1
- 执行边界：只管理状态与纸面准备，不执行真实 swap。

## 状态统计

- DISCOVERED：0
- WATCHING：0
- ACCUMULATING：0
- READY_TO_BUY：0
- PAPER_READY：1
- BLOCKED：0
- FAILED：0
- EXITED：0

## 候选状态

- 代币：PIPE / Pipe111111111111111111111111111111111111111
  - 当前状态：PAPER_READY
  - 状态原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - 信号等级：S4_强确认信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
