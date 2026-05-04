# SIKK 候选币钱包结构门禁汇总

- 更新时间：2026-05-04T12:40:27Z
- 处理数量：1
- 边界：只做钱包结构门禁，不执行真实 swap。

## 统计
- WALLET_BLOCK：1

## 处理结果
- 代币：TROLLIEN / ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump
  - 钱包结构结论：WALLET_BLOCK
  - 建议状态调整：调整为 BLOCKED
  - 原因：对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：wallet_address, role, game_side, evidence_level；筹码控制状态机：CONTROL_MIGRATING_TO_COUNTERPARTY；筹码控制状态机：COUNTERPARTY_PRESSURE_HIGH
