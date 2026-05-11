# SIKK 候选币状态机汇总

- 更新时间：2026-05-08T01:48:00Z
- 候选数量：3
- 执行边界：只管理状态与纸面准备，不执行真实 swap。

## 状态统计

- DISCOVERED：0
- WATCHING：0
- ACCUMULATING：0
- READY_TO_BUY：0
- PAPER_READY：3
- BLOCKED：0
- FAILED：0
- EXITED：0

## 候选状态

- 代币：GABI / KJtdeGP5Tha1RbCYaTvedHdv6oaXcV1kD8FCZtBpump
  - 当前状态：PAPER_READY
  - 状态原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - 信号等级：S4_强确认信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
  - 钱包结构结论：WALLET_BLOCK
- 代币：MV / xNGegLW3dgvSGq4qZP33gz3AJFq9jzSMysCbPrSpump
  - 当前状态：PAPER_READY
  - 状态原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - 信号等级：S4_强确认信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
  - 钱包结构结论：WALLET_BLOCK
- 代币：MASK / GRzVr7w2QAgn2yxphqHLEPVweuuV5T741EEH3s13pump
  - 当前状态：PAPER_READY
  - 状态原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - 信号等级：S4_强确认信号
  - 风险门禁：ALLOW_PAPER_TRADE_允许纸面交易
  - 钱包结构结论：WALLET_BLOCK
