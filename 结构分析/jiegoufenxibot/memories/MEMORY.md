SIKK-GMGN Intel Bot 的结构研究文档与量化输出通常放在 `sikk-gmgn/docs/intel_bot/` 和 `sikk-gmgn/data/gmgn_candidates_live_run/intel_bot/`，并且该项目明确要求只做纸面结构分析，不改状态机、不碰纸面交易/实盘逻辑。
§
Intel Bot 的结构架构升级为 11 层：1 钱包事实层，2 钱包基础分类层，3 当前 token 行为层，4 同源组与资金路径层，5 主导侧成本区计算层，6 筹码库存与派发进度层，7 继续推进 / 二段扩张动机层，8 对手盘压力层，9 钱包 × 盘型匹配层，10 主导侧生命周期层，11 wallet_structure_decision 输出层；其中第 5-7 层是核心重点。