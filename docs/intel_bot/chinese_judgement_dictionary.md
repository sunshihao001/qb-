# SIKK Intel Bot 中文化判断标准层

> 目标：将钱包结构研究、GMGN 备注、报告解释、门禁输出、失败归因统一为中文表达。
>
> 约束：
> - 文件名、函数名、Python 变量名、JSON key、数据库字段名、外部原始字段可保留英文。
> - 所有面向用户的判断结果 value 必须提供中文版本。
> - 英文枚举如需保留，只能作为内部兼容字段，并且必须同时输出中文解释字段。

## 1. 地址角色中文字典

- `NEW_SNIPER`：`疑似新钱包狙击`
- `TEMP_EXEC`：`疑似临时执行钱包`
- `SAME_SRC_MEMBER`：`疑似同源执行组成员`
- `TOKEN_RECEIVER`：`疑似 Token 接收钱包`
- `DISTRIBUTION_SELLER`：`疑似分发派发钱包`
- `PROFIT_BACKFLOW`：`疑似利润回收钱包`
- `CORE_FUND_SRC`：`疑似核心资金源候选`
- `RESULT_WALLET`：`疑似结果钱包`
- `BAGHOLDER_WHALE`：`疑似接盘鲸鱼`
- `TRAPPED_WALLET`：`疑似套牢钱包`
- `NORMAL_PARTICIPANT`：`普通参与者`
- `NOISE_WALLET`：`噪音钱包`
- `INFRA_WALLET`：`基础设施地址`
- `UNKNOWN_ROLE`：`角色未知`

## 2. Token 来源中文字典

- `ACTIVE_BUY`：`主动买入`
- `TOKEN_IN`：`Token 转入`
- `DISTRIBUTION_RECEIVE`：`分发接收`
- `AIRDROP_RECEIVE`：`空投接收`
- `UNKNOWN_SOURCE`：`来源未知`

## 3. 资金来源中文字典

- `EXCHANGE_SOURCE`：`交易所来源`
- `SINGLE_ADDRESS_SOURCE`：`单一地址来源`
- `MULTI_ADDRESS_SOURCE`：`多地址来源`
- `SAME_SOURCE_CLUSTER`：`同源资金组`
- `BACKFLOW_SOURCE`：`回流资金源`
- `POTENTIAL_CORE_SOURCE`：`疑似核心资金源`
- `UNKNOWN_FUND_SOURCE`：`资金来源未知`

## 4. 筹码迁移状态中文字典

- `CHIP_RETAINED`：`筹码仍在结构侧`
- `CHIP_ROTATING`：`结构侧部分轮换`
- `CHIP_TOWARD_COUNTERPARTY`：`筹码转向对手盘`
- `ACTIVE_DISTRIBUTION`：`疑似主动派发`
- `STRUCTURE_COLLAPSED`：`结构侧崩塌`
- `CHIP_UNKNOWN`：`筹码状态未知`

## 5. 钱包结构状态中文字典

- `WALLET_SUPPORT`：`钱包结构支持`
- `WALLET_NEUTRAL`：`钱包结构中性`
- `WALLET_PAUSE`：`钱包结构暂停`
- `WALLET_BLOCK`：`钱包结构阻断`
- `WALLET_UNKNOWN`：`钱包结构未知`

## 6. 主导侧生命周期中文字典

- `EARLY_ACCUMULATION`：`早期吸筹`
- `CONTROL_RANGE`：`控盘箱体`
- `FIRST_RALLY`：`一段拉升`
- `PARTIAL_DISTRIBUTION`：`部分派发`
- `RE_ACCUMULATION`：`再吸筹`
- `SECOND_STAGE_READY`：`二段准备`
- `SECOND_STAGE_VOLUME`：`二段放量`
- `ACTIVE_DISTRIBUTION`：`主动派发`
- `STRUCTURE_COLLAPSE`：`结构崩塌`
- `DEAD_SIDEWAYS`：`死亡横盘`
- `RE_ACTIVATION`：`再激活`
- `LIFECYCLE_UNKNOWN`：`生命周期未知`

## 7. 主导侧行为动机中文字典

专业标准枚举：
- `ACCUMULATE`：`疑似吸筹`
- `CONTROL`：`疑似控盘`
- `WASHOUT`：`疑似洗盘`
- `BREAKOUT_TEST`：`疑似测试突破`
- `MARKUP`：`疑似推进拉升`
- `PARTIAL_DISTRIBUTION`：`疑似部分派发`
- `ACTIVE_DISTRIBUTION`：`疑似主动派发`
- `REACCUMULATION`：`疑似再吸筹`
- `REACTIVATION`：`疑似再激活`
- `ABANDONMENT`：`疑似放弃维护`
- `MOTIVE_UNKNOWN`：`行为动机未知`

兼容旧枚举：
- `POSSIBLE_ACCUMULATION`：`疑似吸筹`
- `POSSIBLE_CONTROL`：`疑似控盘`
- `POSSIBLE_WASHING`：`疑似洗盘`
- `POSSIBLE_LIQUIDITY_TEST`：`疑似流动性测试`
- `POSSIBLE_BREAKOUT_TEST`：`疑似突破测试`
- `POSSIBLE_PUSH_UP`：`疑似推进拉升`
- `POSSIBLE_PARTIAL_DISTRIBUTION`：`疑似部分派发`
- `POSSIBLE_ACTIVE_DISTRIBUTION`：`疑似主动派发`
- `POSSIBLE_RE_ACCUMULATION`：`疑似再吸筹`
- `POSSIBLE_RE_ACTIVATION`：`疑似再激活`
- `POSSIBLE_ABANDON_CONTROL`：`疑似放弃维护`

## 8. 策略门禁中文字典

- `ALLOW_PAPER_READY`：`允许进入纸面交易`
- `CONTINUE_WATCHING`：`继续观察`
- `PAUSE_FOR_CONFIRMATION`：`暂停等待确认`
- `BLOCK`：`阻断`
- `EXPIRED`：`已过期`
- `GATE_UNKNOWN`：`门禁状态未知`

## 9. 时间状态中文字典

- `TIME_SYNC`：`时间同步`
- `TIME_PARTIAL_SYNC`：`时间部分同步`
- `TIME_DESYNC`：`时间不同步`
- `TIME_UNKNOWN`：`时间未知`
- `DATA_EXPIRED`：`数据过期`
- `NEED_REFRESH`：`需要刷新`

## 10. 风险等级中文字典

- `LOW_RISK`：`低风险`
- `LIGHT_OBSERVATION`：`轻度观察`
- `MEDIUM_RISK`：`中度风险`
- `HIGH_RISK`：`高风险`
- `EXTREME_RISK`：`极高风险`

## 11. 证据等级中文字典

- `E0`：`无有效证据`
- `E1`：`单点弱证据`
- `E2`：`多字段弱关联`
- `E3`：`当前代币内强证据`
- `E4`：`当前代币内强证据加同源关系`
- `E5`：`跨代币复现加同源回流盈利稳定`

## 12. 追踪等级中文字典

- `A0`：`不追踪`
- `A1`：`弱观察`
- `A2`：`普通观察`
- `A3`：`重点跟踪`
- `A4`：`核心监控`

## 13. 动作建议中文字典

- `IGNORE`：`忽略`
- `WATCH`：`观察`
- `TRACK`：`跟踪`
- `TRACK_KEY`：`重点跟踪`
- `HIGH_RISK_MONITOR`：`高风险监控`
- `WRITE_HISTORY`：`写入历史库`
- `GENERATE_GMGN_NOTE`：`生成 GMGN 备注`
- `ENTER_NEXT_GATE`：`进入后续门禁`
- `PAUSE_FOR_REFRESH`：`暂停等待刷新`
- `BLOCK_TRADE_FLOW`：`阻断进入交易流程`

## 14. 失败归因中文字典

- `WALLET_STRUCTURE_FAILURE`：`钱包结构失效`
- `EARLY_WALLET_EXIT`：`早期钱包退出`
- `SAME_SOURCE_SYNC_EXIT`：`同源组同步退出`
- `CHIP_TO_COUNTERPARTY`：`筹码转向对手盘`
- `COUNTERPARTY_PRESSURE_HIGH`：`对手盘压力过高`
- `TIME_EVIDENCE_EXPIRED`：`时间证据过期`
- `WALLET_SNAPSHOT_EXPIRED`：`钱包快照过期`
- `QUOTE_EXPIRED`：`quote 过期`
- `PATTERN_INVALID`：`盘型失效`
- `LIQUIDITY_INSUFFICIENT`：`流动性不足`
- `SECURITY_SCAN_FAILED`：`安全扫描未通过`
- `STOP_LOSS_TRIGGERED`：`止损触发`
- `TIME_STOP_LOSS`：`时间止损`
- `STRATEGY_MISMATCH`：`策略不匹配`

## 15. GMGN 备注中文模板

统一格式：

`代币-角色-结果/状态-来源/组别-风险/证据`

### 示例模板

- `ABC-新狙-3.2x-捆绑-G1`
- `ABC-临执-1.8x-单源-短持`
- `ABC-G1成员-4.5x-同源-E4`
- `ABC-分发卖出-已清仓-R3`
- `ABC-回流节点-多地址回流-A4`
- `ABC-结果钱包-8.2x-老钱包-可追踪`
- `ABC-接盘鲸鱼-高位-浮亏R2`
- `ABC-套牢-高位买入-R3`

### 备注字段建议

- `代币`：中文或原 symbol
- `角色`：中文角色短称
- `结果/状态`：收益倍数、已清仓、持有中、高位、浮亏等中文化状态
- `来源/组别`：单源、多地址、同源、捆绑、G1/G2 等
- `风险/证据`：R2/R3/E3/E4 或中文风险短语

## 16. 输出规范

### 用户可见输出
必须显示中文 value：
- 角色
- 钱包类型
- Token 来源
- 资金来源
- 同源组状态
- 筹码迁移状态
- 主导侧生命周期
- 主导侧行为动机
- 钱包结构状态
- 策略门禁状态
- 风险等级
- 证据等级
- 追踪等级
- 动作建议
- 失败归因
- GMGN 备注
- 报告解释

### 兼容输出
如果需要保留英文内部字段，推荐双字段：

- `wallet_structure_status`: `WALLET_SUPPORT`
- `wallet_structure_status_zh`: `钱包结构支持`
- `chip_transfer_status`: `CHIP_RETAINED`
- `chip_transfer_status_zh`: `筹码仍在结构侧`
- `decision_action`: `ALLOW_NEXT_GATE`
- `decision_action_zh`: `允许进入后续门禁`

### 报告要求
- 报告正文必须中文。
- 表述必须避免只输出英文枚举。
- 解释文本必须是中文完整句。
- 英文仅可作为内部兼容字段或原始字段。

### Telegram 要求
- Telegram 展示字段必须使用中文 value。
- 若同时显示兼容字段，中文字段应优先显示。

### GMGN 要求
- GMGN 备注必须中文化。
- 备注应优先采用短、稳定、可读的中文模板。
