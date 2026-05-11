# SIKK 候选币钱包结构门禁汇总

- 更新时间：2026-05-08T01:47:36Z
- 处理数量：3
- 边界：只做钱包结构门禁，不执行真实 swap。

## 统计
- WALLET_BLOCK：3

## 处理结果
- 代币：GABI / KJtdeGP5Tha1RbCYaTvedHdv6oaXcV1kD8FCZtBpump
  - 钱包结构结论：WALLET_BLOCK
  - 建议状态调整：调整为 BLOCKED
  - 原因：发现分发侧钱包 1 个；对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_BREAK_OR_DISTRIBUTION；筹码控制状态机：WALLET_BLOCK；筹码控制状态机：DISTRIBUTION_ACTIVE
- 代币：MV / xNGegLW3dgvSGq4qZP33gz3AJFq9jzSMysCbPrSpump
  - 钱包结构结论：WALLET_BLOCK
  - 建议状态调整：调整为 BLOCKED
  - 原因：对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_MIGRATING_TO_COUNTERPARTY；筹码控制状态机：COUNTERPARTY_PRESSURE_HIGH
- 代币：MASK / GRzVr7w2QAgn2yxphqHLEPVweuuV5T741EEH3s13pump
  - 钱包结构结论：WALLET_BLOCK
  - 建议状态调整：调整为 BLOCKED
  - 原因：对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_MIGRATING_TO_COUNTERPARTY；筹码控制状态机：COUNTERPARTY_PRESSURE_HIGH
