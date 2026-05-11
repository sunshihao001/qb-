# SIKK-SOL v1.0 钱包结构门禁

- 代币符号：GABI
- 代币地址：KJtdeGP5Tha1RbCYaTvedHdv6oaXcV1kD8FCZtBpump
- 钱包结构结论：WALLET_BLOCK
- 筹码控制权状态：CONTROL_LOST_TO_DISTRIBUTION
- 钱包结构评分：0
- 钱包风险评分：100
- 对手盘压力评分：100
- 数据质量评分：100
- 钱包结构系数：0.0
- 建议状态调整：调整为 BLOCKED
- 状态调整原因：发现分发侧钱包 1 个；对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_BREAK_OR_DISTRIBUTION；筹码控制状态机：WALLET_BLOCK；筹码控制状态机：DISTRIBUTION_ACTIVE
- 边界：只做钱包结构门禁，不执行真实 swap；WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。
