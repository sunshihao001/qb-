# P04 Chip Structure Controller Context

P04 是筹码结构会计与迁移状态控制器。它读取 P03 handoff 中的钱包实体、同源/同步/接收/对手盘候选、持仓事实和行为事实，将其转化为可追踪、可量化、可交接的筹码结构状态。

## 底层原则
- 筹码守恒：买入 - 卖出 - 转出 + 转入 = 当前可解释持仓。
- 没有 supply denominator 不得严肃计算持仓比例。
- 必须分 early / structural / same-source / sync / receiver / profit collection / counterparty / unknown cohort。
- P04 只输出候选结构状态，不确认庄家、主控、市场意图或操盘意图。
- P04 不生成 evidence object；P05 才负责证据与反证对象。
- P04 不输出 scenario、strategy、PAPER_READY，不进入 paper/live runtime。
