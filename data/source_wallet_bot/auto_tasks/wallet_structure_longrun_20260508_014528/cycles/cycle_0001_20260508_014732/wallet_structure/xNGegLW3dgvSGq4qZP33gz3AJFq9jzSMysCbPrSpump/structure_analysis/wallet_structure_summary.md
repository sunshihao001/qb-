# SIKK-SOL v1.0 钱包结构门禁

- 代币符号：MV
- 代币地址：xNGegLW3dgvSGq4qZP33gz3AJFq9jzSMysCbPrSpump
- 钱包结构结论：WALLET_BLOCK
- 筹码控制权状态：CONTROL_MIGRATING_TO_COUNTERPARTY
- 钱包结构评分：0
- 钱包风险评分：100
- 对手盘压力评分：100
- 数据质量评分：100
- 钱包结构系数：0.0
- 建议状态调整：调整为 BLOCKED
- 状态调整原因：对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_MIGRATING_TO_COUNTERPARTY；筹码控制状态机：COUNTERPARTY_PRESSURE_HIGH
- 边界：只做钱包结构门禁，不执行真实 swap；WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。
