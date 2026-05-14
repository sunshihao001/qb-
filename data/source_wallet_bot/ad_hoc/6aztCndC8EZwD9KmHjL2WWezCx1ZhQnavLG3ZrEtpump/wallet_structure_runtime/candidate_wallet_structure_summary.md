# SIKK 候选币钱包结构门禁汇总

- 更新时间：2026-05-13T00:58:14Z
- 处理数量：1
- 边界：只做钱包结构门禁，不执行真实 swap。

## 统计
- WALLET_BLOCK：1

## 处理结果
- 代币： / 6aztCndC8EZwD9KmHjL2WWezCx1ZhQnavLG3ZrEtpump
  - 钱包结构结论：WALLET_BLOCK
  - 建议状态调整：调整为 BLOCKED
  - 原因：发现分发侧钱包 4 个；对手盘压力高，接盘/套牢筹码占比偏高；缺失字段：game_side；筹码控制状态机：CONTROL_BREAK_OR_DISTRIBUTION；筹码控制状态机：WALLET_BLOCK；筹码控制状态机：DISTRIBUTION_ACTIVE
