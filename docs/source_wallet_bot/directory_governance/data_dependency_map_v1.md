# Source Wallet Bot 数据依赖地图 v1.0

> 目标：先定义“判断目标 → 所需字段 → 上游接口 → 原始数据 → 标准化字段 → 结构分析用途”，再做任何钱包结构结论。
>
> 原则：**先证据，后判断；先字段，后角色；先降级，后强判。**

## 1. 适用范围

本文件用于 `source_wallet_bot` 的所有钱包结构分析前置准备，包括：

- 单 token 新钱包分析
- 早期窗口钱包分类
- 同源/同步执行候选组
- Token 接收 / 分发 / 派发判断
- 结果钱包 / 高结果鲸鱼 / 套牢鲸鱼判断
- 基础设施地址识别
- 资金回流 / 利润回收路径判断

不覆盖内容：

- 真实交易执行
- 自动签名 / 广播
- 实盘策略下单
- 直接输出“庄家确认”类强结论

## 2. 统一分层

所有判断都必须按以下层次写入或读取：

1. **判断目标**：要回答什么问题
2. **必需字段**：没有这些字段就不能强判
3. **可选增强字段**：有则提高置信度，没有也可降级判断
4. **上游接口 / 数据源**：从哪里来
5. **原始数据形态**：JSON / CSV / 行级事件 / tx trace / wallet profile
6. **标准化字段**：统一成 SIKK 字段名
7. **结构分析用途**：这组字段最终支持什么判断
8. **缺失降级规则**：字段缺失时最多能退到什么结论

## 3. 分析问题清单（接口接入需求源）

在接任何钱包结构分析接口前，必须先定义问题清单。问题清单不是结论，是需求源、字段源、接口源、验收源。

### 3.1 必须覆盖的 12 类分析问题

| 分析问题 | 需要回答什么 | 必需字段摘要 | 主要上游数据源 | 缺失降级 |
|---|---|---|---|---|
| 早期钱包识别 | 谁最早买入？买了多少？还剩多少？ | 首次买入时间、买入延迟、买入金额、当前持仓、已卖出数量 | GMGN traders / holders / kline / wallet profile | 缺首次买入时间不能排序；缺当前持仓只能写早期买入候选 |
| 钱包角色分类 | 是新钱包、执行钱包、资金源、接盘钱包、派发钱包，还是利润回收钱包？ | 钱包创建时间、首次买入时间、Token 来源、资金来源、持仓、卖出/回流字段 | wallet profile / traders / holders / activity / tx trace / 历史库 | 缺资金/Token 来源时只输出交易行为角色候选 |
| 同源关系识别 | 多个钱包是否来自同一资金源或相同行为模板？ | 资金来源地址、首次入金时间、入金金额、买入时间、交易路径 | tx trace / traders / wallet profile / address edge history | 缺资金来源或链上路径，不得强判同源 |
| 同步行为识别 | 是否同步买入、同步卖出、同步转账、同步清仓？ | 事件时间、事件类型、金额、time bucket、tx hash | traders / activity / holders / tx trace | 只有时间接近时只能写同步候选组 |
| 筹码控制判断 | 结构侧是否仍持有足够筹码？是否已经派发？ | 早期钱包列表、初始买入、当前持仓、已卖出、持仓变化 | holders / traders / activity / kline / 历史库 | 缺当前持仓不能判断控筹留存 |
| 资金路径追踪 | 钱从哪里来？利润去了哪里？是否回流？ | funding source、funding amount/time、sell tx、return flow address/amount/time | tx trace / activity / 内部边库 / 历史库 | 单次回流只能写回流候选；缺卖后转账不得判断利润回流 |
| Top Holder 判断 | 早期结构钱包是否仍在大户列表中？ | Top Holder rank、当前持仓、早期钱包标记、快照时间 | GMGN holders / traders / holder delta | 缺 holder 快照只能写大户状态待查 |
| 分发路径判断 | 是否把筹码转给接盘地址、二级钱包或分发组？ | token source/out address、转出数量/时间、接收钱包、接收方卖出 | activity / holders / transfer trace / 边库 | 只看到接收无卖出时只能写分发接收候选 |
| 对手盘压力判断 | 是否出现接盘鲸鱼、散户接盘、结构侧出货给对手盘？ | 买方入场时间/市值/金额、当前持仓、未实现收益、早期钱包卖出时间 | traders / holders / kline / wallet profile | 缺买方收益或持仓时只能写对手盘压力待查 |
| 主导侧生命周期 | 当前是吸筹、控盘、洗盘、拉升、派发、再吸筹还是撤退？ | K线阶段、早期买卖趋势、持仓变化、成交量、市值变化 | kline / holders / traders / activity / 历史库 | 缺 K线或 holder delta 时不输出生命周期结论 |
| 市值上下文判断 | 当前市值相对发现时、买入时、结构判断时变化多少？ | 发现市值、买入市值、当前市值、分析市值、时间戳 | token info / pool / kline / OKX行情 | 缺关键市值时间点时标记上下文不完整 |
| 策略门禁输出 | WALLET_SUPPORT、WALLET_PAUSE、WALLET_BLOCK 的证据是什么？ | 结构分、风险分、证据等级、缺失关键字段、早期状态、控筹/对手盘压力 | 字段合同 / 结构分析 / security / market data / 门禁模块 | 证据不足默认 PAUSE 或 DATA_BACKFILL；硬风险 BLOCK |

### 3.2 分析问题 → 字段合同执行规则

- 这张问题清单就是接口接入的需求源。
- 没有问题定义，就不能定义字段、接口、降级规则或输出表。
- 每个问题必须能映射到一组必需字段、可选字段、缺失降级规则和验证路径。
- 问题优先于实现；先补问题清单，再补字段映射，再补接口接入。
- Telegram / Hermes 入口中，`分析问题 <问题名>` 应读取 `data_dependency_contract_v1.json.analysis_questions`，而不是临时文案。

### 3.3 交付要求

- 所有新接口必须说明它回答哪一个或哪几个分析问题。
- 所有字段合约必须回指到问题清单。
- 所有“看起来有用但无法回答问题”的字段，不进入首版合同。

### 3.4 接口能力清单（采集脚本前置 Gate）

在写任何采集脚本、API wrapper、自动化字段映射前，必须先完成接口能力审计：

- 主文件：`interface_capability_inventory_v1.md`
- 审计对象：GMGN / OKX / Solana RPC / 第三方交易平台 / 内部历史库等上游数据源
- 审计目标：确认平台到底能提供哪些接口、返回哪些字段、支持哪些查询维度、有哪些限制和缺失

接口能力至少分 8 类：

| 接口类别 | 用途 |
|---|---|
| Token 基础信息接口 | 获取 token 地址、名称、创建时间、市值、流动性 |
| 交易明细接口 | 获取买卖记录、成交金额、时间、价格 |
| 钱包持仓接口 | 获取当前持仓、Top Holder、余额变化 |
| 钱包画像接口 | 获取钱包历史行为、胜率、PnL、交易偏好 |
| 转账 / 资金流接口 | 获取资金来源、转移路径、利润回收 |
| K线 / 价格接口 | 获取价格结构、市值变化、成交量 |
| 安全 / 风险接口 | 检查黑名单、貔貅、权限、税费、合约风险 |
| 集群 / 关联接口 | 获取前 300 集群、持仓关联、地址行为关系 |

接口能力清单完成后，才允许判断：

- 哪些判断可以自动化；
- 哪些判断只能部分自动化；
- 哪些判断需要其他数据源补充；
- 哪些判断暂时不能做。

禁止在接口能力清单完成前直接写采集脚本或按接口可得字段反推结论。

## 4. 核心判断依赖地图

### 4.1 疑似同源钱包

| 项目 | 内容 |
|---|---|
| 判断目标 | 多个钱包是否来自同一资金部署或同一执行组 |
| 必需字段 | 资金来源地址、首次入金时间、入金金额、买入时间、买入 token、买入金额、交易路径 |
| 可选增强字段 | Gas 模式、交易频率、钱包创建时间、是否同步买入、是否同步卖出、是否共同接收资金、是否共享中转节点 |
| 上游接口 / 数据源 | GMGN holders / traders / wallet profile + 链上 tx / trace + 内部 address edge history |
| 原始数据形态 | 入金 tx、转账事件、买入事件、钱包创建事件、边关系记录 |
| 标准化字段 | `funding_source_address`、`first_funding_time`、`first_funding_amount`、`first_buy_time`、`first_buy_token`、`first_buy_amount`、`tx_path`、`gas_pattern`、`wallet_create_time`、`synchronous_buy_flag`、`synchronous_sell_flag`、`shared_funding_flag`、`shared_intermediate_node_flag` |
| 结构分析用途 | 生成“同源执行组 / 同源候选组 / 资金待查组” |
| 缺失降级规则 | 若缺少资金来源或链上路径，只能写“同步买入候选组”或“资金待查组”，不得强判同源 |

### 4.2 同步执行候选组

| 项目 | 内容 |
|---|---|
| 判断目标 | 是否存在同一时间窗口内的批量执行行为 |
| 必需字段 | 买入时间、买入 token、买入金额、钱包创建时间、是否新钱包 |
| 可选增强字段 | 资金来源、Gas 模式、转入金额、转入时间、GMGN bundler/sniper/fresh 标签 |
| 上游接口 / 数据源 | GMGN traders / holders / tags + 链上 tx |
| 原始数据形态 | 同窗口交易行、地址标签、资金边 |
| 标准化字段 | `first_buy_time`、`buy_time_bucket`、`wallet_create_time`、`is_new_wallet`、`same_window_group_id`、`buy_amount_bucket`、`gmgn_tags` |
| 结构分析用途 | 识别批量执行、狙击批次、临时执行钱包 |
| 缺失降级规则 | 只能降级为“时间接近候选组”，不能写同源组 |

### 4.3 疑似临时执行钱包

| 项目 | 内容 |
|---|---|
| 判断目标 | 钱包是否为临时创建、短期使用、完成买卖后退出 |
| 必需字段 | 钱包创建时间、首次买入时间、持有时长、资金转入时间、资金转出时间 |
| 可选增强字段 | 单 token 参与度、历史复现、是否仅服务单次事件、卖出后余额变化 |
| 上游接口 / 数据源 | GMGN wallet profile / activity + 链上 tx |
| 原始数据形态 | 钱包创建记录、买卖记录、转账记录 |
| 标准化字段 | `wallet_create_time`、`first_buy_time`、`holding_duration_type`、`funding_before_buy_minutes`、`total_transfer_out`、`single_token_only_flag` |
| 结构分析用途 | 区分执行钱包与普通散户 |
| 缺失降级规则 | 若缺少创建时间或转账路径，只能写“临时执行候选” |

### 4.4 疑似新钱包狙击

| 项目 | 内容 |
|---|---|
| 判断目标 | 新钱包是否在早期窗口快速买入 |
| 必需字段 | 钱包创建时间、首次买入时间、买入延迟、买入金额、买入市值阶段 |
| 可选增强字段 | bundler/sniper/fresh 标签、是否同批入场、是否高频短持 |
| 上游接口 / 数据源 | GMGN traders / wallet profile / market kline |
| 原始数据形态 | 钱包画像、交易时间戳、K线阶段 |
| 标准化字段 | `wallet_create_time`、`first_buy_time`、`first_buy_delay_minutes`、`entry_stage`、`is_new_wallet`、`is_sniper`、`gmgn_tags` |
| 结构分析用途 | 锁定 W1/W2 早期狙击钱包 |
| 缺失降级规则 | 若没有创建时间，只能写“早期买入候选”，不能直接写新狙击 |

### 4.5 Token 接收钱包 / 被动接收钱包

| 项目 | 内容 |
|---|---|
| 判断目标 | 地址持有 token 是主动买入还是被动收到 |
| 必需字段 | Token 来源、转入时间、转入金额、是否有主动 swap 买入 |
| 可选增强字段 | 空投标记、分发标记、LP/池交互、Token 去向 |
| 上游接口 / 数据源 | GMGN activity / holders + 链上 transfer trace |
| 原始数据形态 | token transfer、holder 变动、交易事件 |
| 标准化字段 | `token_source_type`、`token_source_address`、`token_source_time`、`token_source_amount`、`is_transferred_token`、`is_airdrop_token`、`is_distributed_token`、`is_market_buy_token` |
| 结构分析用途 | 区分主动买盘与被动接收噪音 |
| 缺失降级规则 | 若无法确认主动买入，只能写“Token 接收钱包”或“待查” |

### 4.6 疑似分发接收 / 分发派发钱包

| 项目 | 内容 |
|---|---|
| 判断目标 | 钱包是否处于 token 分发链条的接收端或派发端 |
| 必需字段 | Token 来源、转入来源、后续卖出 / 转出、卖出时间、卖出数量 |
| 可选增强字段 | 是否同一上游分发源、是否多地址接收、是否后续集中卖出、是否回流 |
| 上游接口 / 数据源 | GMGN activity / holders + 链上 trace |
| 原始数据形态 | distribution tx、sell tx、转出边 |
| 标准化字段 | `token_source_type`、`token_source_address`、`token_out_type`、`token_out_address`、`first_sell_time`、`is_partial_exit`、`is_full_exit` |
| 结构分析用途 | 识别早期分发、派发出货、接盘风险 |
| 缺失降级规则 | 若只看到接收而无后续卖出，只能写“分发接收候选” |

### 4.7 早期结构资金是否还没出完

| 项目 | 内容 |
|---|---|
| 判断目标 | 早期买入资金是否仍留在持仓中，还是已开始派发 |
| 必需字段 | 早期买入钱包列表、初始买入数量、当前剩余持仓、已卖出数量 |
| 可选增强字段 | 卖出时间、卖出价格、是否仍在 Top Holder、是否转移到新钱包、是否分发给接盘钱包 |
| 上游接口 / 数据源 | GMGN holders / traders / wallet profile + 历史边库 |
| 原始数据形态 | 持仓快照、卖出事件、地址关系边、Top Holder 变动 |
| 标准化字段 | `early_wallet_list`、`initial_buy_amount`、`current_position_remaining`、`sold_amount`、`last_sell_time`、`last_sell_price`、`is_top_holder_now`、`transferred_to_new_wallet_flag`、`distributed_to_bagholder_flag`、`holding_change_trend` |
| 结构分析用途 | 判断派发是否结束、是否仍有结构筹码未出完 |
| 缺失降级规则 | 缺少剩余持仓或卖出事件时，只能写“早期结构资金待查” |

### 4.8 结果钱包 / 高结果鲸鱼

| 项目 | 内容 |
|---|---|
| 判断目标 | 钱包是否具备稳定盈利结果，或属于高结果鲸鱼 |
| 必需字段 | 已实现利润、未实现利润、总利润、胜率、样本数、历史复现 |
| 可选增强字段 | 进入时间、退出质量、是否稳定复现、是否单次暴富 |
| 上游接口 / 数据源 | GMGN wallet profile / traders + 内部历史库 |
| 原始数据形态 | 盈亏页、历史收益记录、持仓记录 |
| 标准化字段 | `realized_profit`、`unrealized_profit`、`total_profit`、`winrate`、`sample_count`、`entry_time`、`exit_quality`、`historical_recurrence_flag` |
| 结构分析用途 | 区分结果钱包、高结果鲸鱼、单次暴富钱包 |
| 缺失降级规则 | 样本数不足时只能写“结果钱包候选”或“单次暴富候选” |

### 4.9 接盘鲸鱼 / 套牢鲸鱼

| 项目 | 内容 |
|---|---|
| 判断目标 | 是否高位接盘、浮亏、套牢、买在派发后段 |
| 必需字段 | 买入市值、买入时间、持有时长、未实现利润、当前持仓占比 |
| 可选增强字段 | 后续卖出情况、历史胜率、是否在早期钱包卖出后入场 |
| 上游接口 / 数据源 | GMGN traders / holders / market kline |
| 原始数据形态 | 买入行、持仓快照、K线阶段 |
| 标准化字段 | `entry_stage`、`avg_buy_market_cap`、`holding_duration_type`、`unrealized_profit`、`current_holding_pct`、`exit_status` |
| 结构分析用途 | 识别高位接盘、套牢、风险观察 |
| 缺失降级规则 | 没有持仓收益数据时，只能写“接盘风险候选” |

### 4.10 基础设施地址

| 项目 | 内容 |
|---|---|
| 判断目标 | 地址是否属于 CEX、LP、池子、路由、程序、可疑中转、回收节点、分发源 |
| 必需字段 | 地址类型、出现代币数、对手方数、边关系数、路由 / 池交互数 |
| 可选增强字段 | 回流次数、资金源次数、是否多 token 重复出现、是否连接执行组 |
| 上游接口 / 数据源 | 链上 trace + GMGN activity + 内部边库 |
| 原始数据形态 | 地址标签、交易路径、边关系、转账节点 |
| 标准化字段 | `entity_type`、`entity_name`、`infrastructure_level`、`exclusion_reason`、`appeared_token_count`、`counterparty_count`、`funding_source_count`、`return_flow_count`、`router_interaction_count`、`lp_interaction_count`、`keep_edges` |
| 结构分析用途 | 排除普通钱包评分，只保留关系边和结构节点证据 |
| 缺失降级规则 | 若类型未明确，只能写“可疑中转候选”或“待复查节点” |

### 4.11 利润回收 / 核心资金源

| 项目 | 内容 |
|---|---|
| 判断目标 | 多个钱包卖出后是否回到同一地址，是否形成核心资金源 |
| 必需字段 | 卖后回流边、回流地址、回流金额、回流时间、关联钱包数 |
| 可选增强字段 | 多 token 复现、同源执行组、CEX 入口、重复回流模式 |
| 上游接口 / 数据源 | 链上 trace + 内部边库 + 历史库 |
| 原始数据形态 | 卖后转账、回流边、资金树 |
| 标准化字段 | `return_flow_address`、`return_flow_amount`、`return_flow_count`、`is_return_flow`、`core_funding_source_flag` |
| 结构分析用途 | 识别利润归集、核心资金源、回收地址 |
| 缺失降级规则 | 若只有单次回流，写“利润回流候选”；不得直接写核心资金源 |

## 5. 字段缺失时的统一降级规则

| 缺失情况 | 最多可写结论 | 不允许写 |
|---|---|---|
| 没有资金来源 | 资金待查 / 同步候选 | 同源钱包、核心资金源 |
| 没有链上路径 | 时间接近候选 | 同源组、回流组 |
| 没有钱包创建时间 | 早期买入候选 | 新钱包狙击 |
| 没有持仓收益数据 | 结果候选 | 高结果鲸鱼、稳定结果 |
| 没有卖出事件 | 持有中 / 待查 | 清仓 / 分发结束 |
| 没有 Token 来源 | 事实待查 | 主动买入、Token 接收确认 |
| 没有边关系 | 单钱包记录 | 同源组、回收节点、结构网络节点 |

## 6. 标准化字段命名建议

建议所有数据层最终统一到以下字段族：

- 身份层：`wallet_address`、`wallet_alias`、`wallet_create_time`、`wallet_age_days`
- 行为层：`first_buy_time`、`first_sell_time`、`holding_duration_type`、`token_source_type`
- 资金层：`funding_source_type`、`funding_source_address`、`first_funding_time`、`first_funding_amount`
- 结果层：`realized_profit`、`unrealized_profit`、`total_profit`、`winrate`
- 控制层：`current_holding_pct`、`holding_change_trend`
- 风险层：`risk_label`、`fast_trade_flag`、`blacklist_flag`
- 结构层：`same_source_group_id`、`shared_funding_flag`、`shared_intermediate_node_flag`
- 基础设施层：`entity_type`、`infrastructure_level`、`exclusion_reason`
- 边关系层：`from_address`、`to_address`、`edge_type`、`amount`、`time`、`tx_hash`

## 7. 结构分析读入顺序

后续任何结构分析都必须按顺序读取：

1. `wallet_data/raw/`
2. `wallet_data/normalized/`
3. `structure_analysis/wallet_fact/`
4. `structure_analysis/intelligence/`
5. `history/` 或历史地址库
6. 最后才是写备注、写结论、写 tracking list

## 8. 建议落盘位置

这份数据依赖地图建议作为 Source Wallet Bot 的治理文档主文件之一，后续可继续拆分为：

- `docs/source_wallet_bot/directory_governance/data_dependency_map_v1.md`
- `research_loop/methodology/field_maps/source_wallet_bot_data_dependency_map_v1.md`
- `contracts/source_wallet_bot/data_dependency_contract_v1.json`

当前优先使用 Markdown 版作为人类治理版，后续再补机器可读版。
