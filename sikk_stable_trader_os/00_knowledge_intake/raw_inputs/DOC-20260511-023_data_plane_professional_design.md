# Data Plane：数据平面专业化设计

## 0. 核心定位

**Data Plane 不是“抓数据脚本层”。**

它是 SIKK Stable Trader OS 的**数据事实生产层**，负责把 Domain Plane 定义出来的领域对象，转化为系统可以稳定读取、校验、评分、追踪、回放、交接的结构化数据。

一句话定义：

> **Domain Plane 定义系统要判断什么。**  
> **Data Plane 负责证明：这些判断所需的数据是否存在、是否可信、是否新鲜、是否可追溯、是否足够进入证据层。**

---

# 1. Data Plane 的阶段目标

## 1.1 总目标

建立一个轻量机构级别的数据平面，使系统后续所有判断都不再依赖“AI 临时理解”，而是依赖：

```text
字段来源清楚
字段含义清楚
字段质量清楚
字段新鲜度清楚
字段缺失状态清楚
字段能否支持判断清楚
字段到领域对象的映射清楚
字段到证据对象的交接清楚
```

Data Plane 的专业化目标不是“数据越多越好”，而是：

```text
让每一个后续判断，都能追溯到具体字段、具体来源、具体时间、具体质量等级。
```

---

# 2. Data Plane 在总体系中的位置

```text
P00 Bootstrap Control Plane
    ↓
P01 Governance Plane
    ↓
P02 Domain Plane
    ↓
P03 Data Plane
    ↓
P04 Evidence Plane
    ↓
P05 Scenario Recognition Plane
    ↓
P06 Strategy Gate Plane
    ↓
P07 Execution Risk Plane
    ↓
P08 Review / Replay Plane
    ↓
P09 Self-Upgrade Plane
```

Data Plane 是 P03。

它承接 Domain Plane 的字段需求，然后输出给 Evidence Plane。

---

# 3. Data Plane 的边界

## 3.1 它能做什么

|权限|内容|
|---|---|
|定义数据源|GMGN、OKX、链上交易、钱包快照、K线、流动性、安全扫描、历史地址库|
|定义字段字典|每个字段的含义、类型、单位、来源、刷新频率|
|定义原始数据模型|raw 数据如何保存|
|定义标准化模型|normalized 数据如何统一|
|定义快照模型|每轮采集的时间切片|
|定义事件模型|买入、卖出、转账、增持、减持、清仓、资金归集|
|定义质量模型|完整性、准确性、一致性、新鲜度、可追溯性|
|定义缺失处理|缺失字段如何标记、降权、阻断|
|定义数据交接包|输出给 Evidence Plane 的标准数据包|
|定义回放能力|后续复盘可以重建当时的数据状态|

---

## 3.2 它不能做什么

|禁止事项|原因|
|---|---|
|不能直接判断可以买|买入属于 Strategy Gate / Execution|
|不能直接判断庄家一定存在|这是主导侧推断，不是数据事实|
|不能用缺失字段补脑|数据缺失必须标记|
|不能把多个来源冲突的数据强行合并|必须保留冲突状态|
|不能覆盖 raw 原始数据|原始数据必须可追溯|
|不能只输出最终表格|必须保留 lineage、quality、snapshot|
|不能让 AI 解释字段含义|字段含义必须写入字段字典|
|不能没有新鲜度状态|过期数据不能支持强判断|

---

# 4. Data Plane 的底层逻辑

## 4.1 数据平面不是数据库，而是事实生产链

专业系统的数据平面应按这个链路建立：

```text
数据源
  ↓
原始采集
  ↓
原始落盘
  ↓
字段解析
  ↓
标准化
  ↓
实体归并
  ↓
快照生成
  ↓
质量评分
  ↓
缺失登记
  ↓
冲突登记
  ↓
领域字段映射
  ↓
交接给 Evidence Plane
```

如果跳过中间任何步骤，后续判断都会变成“看起来很智能，但不可审计”。

---

# 5. Data Plane 必须包含的数据体系

## 5.1 一级数据对象

|数据对象|作用|
|---|---|
|数据源对象|记录数据来自哪里|
|原始数据对象|保存未经修改的原始输入|
|标准化数据对象|统一字段、单位、时间格式后的数据|
|实体对象|钱包、代币、池子、交易对、群组|
|事件对象|买入、卖出、转账、清仓、归集、增持、减持|
|快照对象|某一时间点的完整状态|
|字段对象|每个字段的定义、类型、单位、质量|
|数据质量对象|完整性、准确性、新鲜度、一致性|
|数据缺失对象|哪些字段缺失，影响什么判断|
|数据冲突对象|多源数据不一致时的记录|
|数据血缘对象|字段从哪里来，经过什么处理|
|下游交接对象|给 Evidence Plane 的标准数据包|

---

# 6. Data Plane 的核心文件体系

建议目录：

```text
/root/sikk-gmgn/system/data_plane/
```

建议创建：

```text
data_plane.yaml
data_context.md
data_source_registry.yaml
data_requirement_from_domain.yaml
data_field_dictionary.yaml
data_raw_model.yaml
data_normalized_model.yaml
data_entity_model.yaml
data_event_model.yaml
data_snapshot_model.yaml
data_quality_model.yaml
data_freshness_model.yaml
data_missing_policy.yaml
data_conflict_policy.yaml
data_lineage_model.yaml
data_storage_constitution.md
data_handoff_contract.yaml
data_acceptance_criteria.md
data_gap_register.md
data_review_checklist.md
```

---

# 7. 每个文件的作用

|文件|作用|
|---|---|
|`data_plane.yaml`|阶段身份证，定义权限、上下游、状态码|
|`data_context.md`|HER 运行前必须读取的数据平面上下文|
|`data_source_registry.yaml`|数据源注册表|
|`data_requirement_from_domain.yaml`|承接 Domain Plane 的字段需求|
|`data_field_dictionary.yaml`|全系统字段字典|
|`data_raw_model.yaml`|原始数据模型|
|`data_normalized_model.yaml`|标准化数据模型|
|`data_entity_model.yaml`|钱包、代币、池子、群组实体模型|
|`data_event_model.yaml`|买卖转账等事件模型|
|`data_snapshot_model.yaml`|多轮时间快照模型|
|`data_quality_model.yaml`|数据质量评分模型|
|`data_freshness_model.yaml`|数据新鲜度规则|
|`data_missing_policy.yaml`|缺失字段处理规则|
|`data_conflict_policy.yaml`|多源冲突处理规则|
|`data_lineage_model.yaml`|数据血缘与可追溯模型|
|`data_storage_constitution.md`|数据目录宪法|
|`data_handoff_contract.yaml`|输出给 Evidence Plane 的交接合约|
|`data_acceptance_criteria.md`|DATA_READY / WITH_GAPS / REJECTED|
|`data_gap_register.md`|当前数据缺口登记|
|`data_review_checklist.md`|审计清单|

---

# 8. Data Plane 阶段身份证

文件：

```text
/root/sikk-gmgn/system/data_plane/data_plane.yaml
```

建议内容：

```yaml
plane_id: P03_DATA_PLANE
plane_name: 数据平面
plane_level: light_institutional
version: v1.0
status: DRAFT_READY_FOR_AUDIT

mission:
  primary: 把 Domain Plane 的领域字段需求转化为可采集、可校验、可追溯、可交接的数据事实体系
  secondary:
    - 建立数据源注册表
    - 建立字段字典
    - 建立原始数据与标准化数据模型
    - 建立实体、事件、快照模型
    - 建立数据质量、新鲜度、缺失、冲突、血缘模型
    - 输出给 Evidence Plane 的数据交接包

authority:
  can_define:
    - 数据源
    - 字段字典
    - 原始数据模型
    - 标准化模型
    - 实体模型
    - 事件模型
    - 快照模型
    - 数据质量规则
    - 数据新鲜度规则
    - 数据缺失规则
    - 数据冲突规则
    - 数据血缘
    - 数据交接合约

  cannot_do:
    - 直接生成买入信号
    - 直接判断主导侧意图
    - 直接输出策略结论
    - 用缺失字段强行推理
    - 覆盖原始数据
    - 忽略多源冲突
    - 忽略数据过期

upstream_planes:
  - P02_DOMAIN_PLANE

downstream_planes:
  - P04_EVIDENCE_PLANE
  - P05_SCENARIO_RECOGNITION_PLANE
  - P08_REVIEW_REPLAY_PLANE

status_codes:
  - DATA_UNINITIALIZED
  - DATA_SOURCE_REGISTERED
  - DATA_REQUIREMENT_MAPPED
  - RAW_DATA_READY
  - NORMALIZED_DATA_READY
  - DATA_QUALITY_CHECKED
  - DATA_WITH_MISSING_FIELDS
  - DATA_CONFLICT_DETECTED
  - DATA_STALE
  - DATA_READY_FOR_EVIDENCE
  - DATA_READY_WITH_GAPS
  - DATA_REJECTED
```

---

# 9. 数据源注册表

文件：

```text
data_source_registry.yaml
```

## 9.1 必须注册的数据源

|数据源|作用|关键风险|
|---|---|---|
|GMGN Token 数据|代币基础信息、持有人、交易、钱包、热门榜、新币|字段变化、接口限制、时间延迟|
|GMGN 钱包数据|钱包交易、持仓、盈利、角色线索|钱包归因误差|
|链上原始交易|转账、买卖、资金流|解析成本高|
|OKX Quote|报价、流动性、价格交叉验证|与 GMGN 报价偏差|
|OKX Security|安全扫描、合约风险|覆盖不完整|
|K 线数据|OHLCV、成交量、结构判断|数据粒度、缺口|
|流动性池数据|池子深度、滑点、LP 变化|快速变化|
|持有人快照|Top Holder、集中度、分布|快照过期|
|历史地址库|地址复现、历史表现|样本不足|
|纸面交易数据|后续回放、结果校准|不属于实时判断源|
|人工标注数据|复盘标签、样本校准|主观污染|

---

## 9.2 数据源注册格式

```yaml
data_sources:
  - source_id: GMGN_TOKEN
    source_name: GMGN 代币数据
    source_type: API_OR_AGENT_SKILL
    primary_use:
      - 代币基础信息
      - 热门候选发现
      - 持有人结构
      - 交易行为
    freshness_requirement_seconds: 60
    reliability_level: B
    raw_storage_required: true
    normalized_storage_required: true
    known_risks:
      - 字段可能变化
      - 部分数据可能延迟
      - 钱包归因需要交叉验证
    fallback_sources:
      - CHAIN_RAW
      - OKX_QUOTE

  - source_id: OKX_QUOTE
    source_name: OKX 报价数据
    source_type: API_OR_AGENT_SKILL
    primary_use:
      - 当前价格验证
      - 报价偏差检查
      - 流动性辅助判断
    freshness_requirement_seconds: 30
    reliability_level: B
    raw_storage_required: true
    normalized_storage_required: true
    known_risks:
      - 不一定覆盖所有长尾代币
      - 与 DEX 即时报价可能存在偏差
```

---

# 10. 字段字典模型

文件：

```text
data_field_dictionary.yaml
```

字段字典是 Data Plane 的核心。

如果没有字段字典，HER 后续会不知道每个字段到底代表什么。

## 10.1 字段字典标准格式

```yaml
field_dictionary:
  - field_key: token_address
    field_name_cn: 代币地址
    domain_object: 代币对象
    data_type: string
    required: true
    unit: null
    source_priority:
      - GMGN_TOKEN
      - CHAIN_RAW
    freshness_requirement_seconds: 300
    quality_dimensions:
      completeness_required: true
      accuracy_required: true
      consistency_required: true
      traceability_required: true
    downstream_use:
      - Evidence Plane
      - Scenario Plane
      - Review Plane
    missing_policy: HARD_BLOCK
    notes: 代币对象的唯一主键

  - field_key: discovery_market_cap_usd
    field_name_cn: 发现时市值
    domain_object: 市值对象
    data_type: number
    required: true
    unit: USD
    source_priority:
      - GMGN_TOKEN
      - INTERNAL_CANDIDATE_DISCOVERY
    freshness_requirement_seconds: null
    quality_dimensions:
      completeness_required: true
      accuracy_required: medium
      consistency_required: true
      traceability_required: true
    downstream_use:
      - 市值上下文
      - 追高风险判断
      - 退出流动性判断
    missing_policy: STRONG_DOWNGRADE
    notes: 必须保留首次发现时快照，不允许用当前市值覆盖
```

---

# 11. 必须定义的核心字段组

## 11.1 代币基础字段

```yaml
token_basic_fields:
  - token_address
  - token_symbol
  - token_name
  - chain
  - pair_address
  - pool_address
  - launch_time
  - discovery_time
  - token_age_seconds
  - creator_address
  - deployer_address
  - mint_authority_status
  - freeze_authority_status
  - supply_total
  - supply_circulating
```

---

## 11.2 市值字段

```yaml
market_cap_fields:
  - discovery_market_cap_usd
  - current_market_cap_usd
  - market_cap_at_wallet_decision_usd
  - market_cap_at_signal_usd
  - market_cap_at_paper_entry_usd
  - market_cap_change_from_discovery_pct
  - market_cap_stage_label
  - market_cap_context_status
```

---

## 11.3 钱包字段

```yaml
wallet_fields:
  - wallet_address
  - entity_id
  - first_seen_time
  - first_buy_time
  - first_buy_price
  - first_buy_market_cap_usd
  - first_buy_amount_token
  - first_buy_amount_usd
  - total_buy_amount_token
  - total_buy_amount_usd
  - total_sell_amount_token
  - total_sell_amount_usd
  - current_holding_amount_token
  - current_holding_pct
  - holding_duration_seconds
  - realized_profit_usd
  - unrealized_profit_usd
  - realized_profit_pct
  - funding_source_address
  - funding_source_type
  - token_source_type
  - wallet_age_seconds
  - wallet_transaction_count
  - historical_token_count
  - historical_win_rate
  - historical_recurrence_score
```

---

## 11.4 钱包群组字段

```yaml
wallet_group_fields:
  - same_source_group_id
  - sync_buy_group_id
  - sync_sell_group_id
  - distribution_path_id
  - group_wallet_count
  - group_total_holding_pct
  - group_total_buy_usd
  - group_total_sell_usd
  - group_remaining_holding_pct
  - group_sync_buy_score
  - group_sync_sell_score
  - group_funding_similarity_score
  - group_behavior_similarity_score
  - group_distribution_risk_score
```

---

## 11.5 筹码结构字段

```yaml
chip_structure_fields:
  - top_holder_pct
  - top_10_holder_pct
  - top_20_holder_pct
  - early_wallet_remaining_pct
  - early_wallet_cleared_count
  - early_wallet_partial_sell_count
  - structural_wallet_holding_pct
  - counterparty_wallet_holding_pct
  - chip_concentration_score
  - chip_distribution_score
  - chip_transfer_status
  - dominant_side_chip_retention_status
```

---

## 11.6 K 线与结构字段

```yaml
market_structure_fields:
  - candle_interval
  - open_time
  - candle_time
  - open
  - high
  - low
  - close
  - volume
  - turnover_usd
  - buy_volume
  - sell_volume
  - volume_delta
  - price_change_pct
  - box_high
  - box_low
  - box_mid
  - control_box_status
  - breakout_status
  - pullback_status
  - failure_test_status
  - avwap_status
  - poc_status
  - obv_status
  - cmf_status
  - ao_status
  - adx_noise_rejection_status
```

---

## 11.7 流动性与报价字段

```yaml
liquidity_quote_fields:
  - liquidity_usd
  - liquidity_change_pct
  - pool_age_seconds
  - estimated_slippage_pct
  - quote_price_gmgn
  - quote_price_okx
  - quote_price_chain
  - quote_deviation_pct
  - quote_consistency_status
  - buy_sell_ratio
  - trade_count_5m
  - trade_count_15m
  - trade_count_1h
```

---

## 11.8 安全字段

```yaml
security_fields:
  - contract_risk_status
  - mint_authority_risk
  - freeze_authority_risk
  - blacklist_risk
  - tax_risk
  - honeypot_risk
  - liquidity_lock_status
  - owner_permission_status
  - token_transfer_restriction_status
  - security_scan_source
  - security_scan_time
```

---

## 11.9 数据质量字段

```yaml
data_quality_fields:
  - source_id
  - source_record_id
  - raw_file_path
  - normalized_file_path
  - collected_at
  - normalized_at
  - freshness_status
  - completeness_score
  - accuracy_score
  - consistency_score
  - traceability_score
  - data_quality_score
  - missing_fields
  - conflict_fields
  - stale_fields
  - data_ready_for_evidence
```

---

# 12. 原始数据模型

文件：

```text
data_raw_model.yaml
```

## 12.1 原始数据原则

```text
原始数据只保存，不解释。
原始数据不覆盖。
原始数据必须保留采集时间。
原始数据必须保留来源。
原始数据必须能回放。
```

## 12.2 原始数据结构

```yaml
raw_data_record:
  raw_record_id: string
  source_id: string
  token_address: string
  collected_at: datetime
  collection_run_id: string
  raw_payload_type:
    - JSON
    - CSV
    - HTML
    - API_RESPONSE
    - AGENT_SKILL_OUTPUT
  raw_payload_path: string
  source_query:
    query_type: string
    query_params: object
  source_response_status: string
  source_latency_ms: number
  checksum: string
  parser_version: string
  immutable: true
```

---

# 13. 标准化数据模型

文件：

```text
data_normalized_model.yaml
```

## 13.1 标准化原则

标准化不是总结。

标准化只做：

```text
字段统一
单位统一
时间统一
地址格式统一
空值统一
来源绑定
质量标记
```

## 13.2 标准化记录

```yaml
normalized_record:
  normalized_record_id: string
  raw_record_id: string
  token_address: string
  entity_type:
    - TOKEN
    - WALLET
    - WALLET_GROUP
    - TRANSACTION
    - CANDLE
    - LIQUIDITY
    - SECURITY
    - HOLDER
  normalized_at: datetime
  normalizer_version: string
  fields:
    field_key: any
  source_lineage:
    source_id: string
    raw_payload_path: string
    raw_field_path: string
  quality:
    completeness_score: number
    consistency_score: number
    freshness_status: string
    traceability_score: number
```

---

# 14. 实体模型

文件：

```text
data_entity_model.yaml
```

## 14.1 实体类型

|实体|主键|说明|
|---|---|---|
|代币实体|token_address|当前分析标的|
|钱包实体|wallet_address|单地址|
|钱包归并实体|entity_id|多地址归并后的实体|
|钱包群组实体|group_id|同源、同步、分发路径等群组|
|池子实体|pool_address|流动性池|
|交易实体|transaction_hash|链上交易|
|快照实体|snapshot_id|某一时间点状态|
|运行实体|run_id|一次系统运行|

---

## 14.2 钱包实体

```yaml
wallet_entity:
  wallet_address: string
  entity_id: string | null
  chain: string
  first_seen_time: datetime
  entity_resolution_status:
    - SINGLE_ADDRESS
    - SAME_SOURCE_CANDIDATE
    - CONFIRMED_GROUP_MEMBER
    - UNKNOWN
  funding_source_address: string | null
  funding_source_type: string | null
  known_group_ids: list
  historical_profile_id: string | null
```

---

## 14.3 钱包群组实体

```yaml
wallet_group_entity:
  group_id: string
  group_type:
    - SAME_SOURCE_GROUP
    - SYNC_BUY_GROUP
    - SYNC_SELL_GROUP
    - DISTRIBUTION_RECEIVER_GROUP
    - PROFIT_COLLECTION_GROUP
    - COUNTERPARTY_WHALE_GROUP
  token_address: string
  wallet_addresses: list
  group_created_at: datetime
  group_confidence: number
  group_evidence_fields: list
  group_counter_evidence_fields: list
```

---

# 15. 事件模型

文件：

```text
data_event_model.yaml
```

Data Plane 必须把连续行为转成事件，否则后面 Evidence Plane 无法做证据链。

## 15.1 核心事件类型

|事件|含义|
|---|---|
|TOKEN_DISCOVERED|代币被发现|
|WALLET_FIRST_BUY|钱包首次买入|
|WALLET_ACCUMULATION|钱包持续吸筹|
|WALLET_PARTIAL_SELL|钱包部分卖出|
|WALLET_FULL_EXIT|钱包清仓|
|WALLET_TRANSFER_OUT|钱包转出筹码|
|FUNDING_SOURCE_LINKED|资金来源关联|
|SAME_SOURCE_GROUP_DETECTED|疑似同源组识别|
|SYNC_BUY_DETECTED|同步买入|
|SYNC_SELL_DETECTED|同步卖出|
|CHIP_CONCENTRATION_CHANGED|筹码集中度变化|
|CHIP_DISTRIBUTION_CHANGED|筹码派发变化|
|MARKET_CAP_STAGE_CHANGED|市值阶段变化|
|BREAKOUT_DETECTED|突破检测|
|PULLBACK_DETECTED|回踩检测|
|FAILURE_TEST_DETECTED|失败测试检测|
|QUOTE_DEVIATION_DETECTED|报价偏差|
|SECURITY_RISK_DETECTED|安全风险|

---

## 15.2 事件标准结构

```yaml
data_event:
  event_id: string
  event_type: string
  token_address: string
  related_entity_id: string
  related_wallet_address: string | null
  related_group_id: string | null
  event_time: datetime
  observed_at: datetime
  source_id: string
  source_record_id: string
  event_fields: object
  event_quality_score: number
  event_freshness_status: string
  downstream_relevance:
    - EVIDENCE_PLANE
    - SCENARIO_PLANE
    - REVIEW_PLANE
```

---

# 16. 快照模型

文件：

```text
data_snapshot_model.yaml
```

## 16.1 为什么必须有快照

SIKK 系统判断的是“状态变化”，不是单点数据。

必须知道：

```text
发现时是什么样
钱包判断时是什么样
信号出现时是什么样
纸面入场时是什么样
退出时是什么样
复盘时是什么样
```

---

## 16.2 快照类型

```yaml
snapshot_types:
  - DISCOVERY_SNAPSHOT
  - WALLET_DECISION_SNAPSHOT
  - MARKET_STRUCTURE_SNAPSHOT
  - SIGNAL_SNAPSHOT
  - PAPER_ENTRY_SNAPSHOT
  - PAPER_EXIT_SNAPSHOT
  - REVIEW_SNAPSHOT
```

---

## 16.3 快照结构

```yaml
data_snapshot:
  snapshot_id: string
  token_address: string
  snapshot_type: string
  snapshot_time: datetime
  run_id: string

  token_state:
    market_cap_usd: number
    liquidity_usd: number
    holder_count: number
    token_age_seconds: number

  wallet_state:
    early_wallet_count: number
    structural_wallet_holding_pct: number
    early_wallet_remaining_pct: number
    same_source_group_count: number
    sync_sell_group_count: number

  chip_state:
    chip_concentration_score: number
    chip_distribution_score: number
    chip_transfer_status: string

  market_state:
    price: number
    volume: number
    box_status: string
    avwap_status: string
    poc_status: string
    breakout_status: string
    pullback_status: string

  data_quality:
    required_fields_total: number
    required_fields_present: number
    missing_critical_fields: list
    data_quality_score: number
    freshness_status: string
```

---

# 17. 数据质量模型

文件：

```text
data_quality_model.yaml
```

## 17.1 数据质量维度

|维度|中文含义|关键问题|
|---|---|---|
|完整性|字段是否齐全|缺不缺关键字段|
|准确性|字段是否可信|来源是否可靠|
|一致性|多源是否一致|GMGN / OKX / 链上是否冲突|
|新鲜度|数据是否过期|是否还能用于实时判断|
|可追溯性|能否找到来源|是否有 raw 路径和 source_id|
|可复盘性|未来能否重建当时状态|是否有 snapshot|
|稳定性|字段定义是否稳定|是否接口变化|
|粒度适配|时间粒度是否够用|1m / 5m / 15m 是否满足判断|

---

## 17.2 数据质量评分

```yaml
data_quality_score_model:
  completeness_weight: 0.25
  accuracy_weight: 0.20
  consistency_weight: 0.20
  freshness_weight: 0.15
  traceability_weight: 0.10
  replayability_weight: 0.10

quality_status:
  - DATA_HIGH_CONFIDENCE
  - DATA_USABLE
  - DATA_USABLE_WITH_GAPS
  - DATA_LOW_CONFIDENCE
  - DATA_UNUSABLE
```

---

## 17.3 质量状态解释

|状态|含义|下游权限|
|---|---|---|
|DATA_HIGH_CONFIDENCE|关键字段完整，多源一致，新鲜|可进入 Evidence Plane|
|DATA_USABLE|主要字段完整，有轻微缺口|可进入 Evidence Plane，但标记|
|DATA_USABLE_WITH_GAPS|有缺失但不影响基础判断|只能弱证据|
|DATA_LOW_CONFIDENCE|关键字段不稳定|不能强判断|
|DATA_UNUSABLE|数据缺失或冲突严重|阻断|

---

# 18. 数据新鲜度模型

文件：

```text
data_freshness_model.yaml
```

## 18.1 新鲜度不是统一标准

不同数据的过期速度不同。

|数据类型|建议新鲜度|
|---|---|
|报价|15-30 秒|
|流动性|30-60 秒|
|K 线|当前周期内|
|钱包交易|60-180 秒|
|持有人快照|3-10 分钟|
|安全扫描|10-60 分钟|
|历史地址库|可长期有效，但需要版本|
|纸面交易结果|非实时判断数据|

---

## 18.2 新鲜度状态

```yaml
freshness_status:
  FRESH:
    meaning: 数据仍可用于实时判断
  ACCEPTABLE:
    meaning: 可用于辅助判断，但不能作为强证据
  STALE:
    meaning: 数据过期，只能做背景参考
  EXPIRED:
    meaning: 禁止用于实时判断
  UNKNOWN:
    meaning: 没有采集时间，必须降权
```

---

# 19. 缺失字段处理模型

文件：

```text
data_missing_policy.yaml
```

## 19.1 缺失字段分级

|缺失等级|含义|处理|
|---|---|---|
|CRITICAL_MISSING|关键字段缺失|阻断|
|HIGH_IMPACT_MISSING|高影响字段缺失|强降权|
|MEDIUM_IMPACT_MISSING|中等影响字段缺失|标记后允许弱判断|
|LOW_IMPACT_MISSING|低影响字段缺失|记录|
|UNKNOWN_MISSING|不知道影响|保守降权|

---

## 19.2 关键字段缺失示例

```yaml
critical_missing_rules:
  - rule_id: DMISS_001
    missing_field: token_address
    result: DATA_REJECTED
    reason: 无法确定代币主键

  - rule_id: DMISS_002
    missing_field: current_market_cap_usd
    result: DATA_READY_WITH_GAPS
    reason: 市值上下文不完整，不能判断追高或退出流动性风险

  - rule_id: DMISS_003
    missing_field: early_wallet_remaining_pct
    result: DATA_READY_WITH_GAPS
    reason: 不能强判断结构侧筹码留存

  - rule_id: DMISS_004
    missing_field: same_source_group_id
    result: DATA_READY_WITH_GAPS
    reason: 同源执行组风险无法确认

  - rule_id: DMISS_005
    missing_field: security_scan_status
    result: DATA_REJECTED
    reason: 安全门未完成，不能进入下游强判断
```

---

# 20. 数据冲突处理模型

文件：

```text
data_conflict_policy.yaml
```

## 20.1 多源冲突必须显式保留

例如：

```text
GMGN 当前市值 = 800K
链上估算市值 = 1.1M
OKX quote 不覆盖
```

不能直接平均，也不能随便选择。

必须输出：

```text
market_cap_conflict_detected = true
conflict_fields = [current_market_cap_usd]
preferred_source = GMGN_TOKEN
confidence = medium
```

---

## 20.2 冲突规则

```yaml
data_conflict_rules:
  - rule_id: DCONF_001
    field: current_price
    conflict_condition: source_deviation_pct > 5
    result: QUOTE_CONFLICT_DETECTED
    downstream_permission: WEAK_EVIDENCE_ONLY

  - rule_id: DCONF_002
    field: current_market_cap_usd
    conflict_condition: source_deviation_pct > 10
    result: MARKET_CAP_CONFLICT_DETECTED
    downstream_permission: NO_STRONG_MARKET_CAP_CLAIM

  - rule_id: DCONF_003
    field: wallet_current_holding_pct
    conflict_condition: snapshot_time_gap_seconds > freshness_requirement
    result: WALLET_SNAPSHOT_CONFLICT
    downstream_permission: REQUIRE_REFRESH

  - rule_id: DCONF_004
    field: liquidity_usd
    conflict_condition: liquidity_source_deviation_pct > 15
    result: LIQUIDITY_CONFLICT
    downstream_permission: EXECUTION_BLOCK_UNTIL_REFRESH
```

---

# 21. 数据血缘模型

文件：

```text
data_lineage_model.yaml
```

## 21.1 每个字段都要能追溯

字段不能只出现结果。

必须能回答：

```text
这个字段来自哪个数据源？
什么时候采集？
原始文件在哪里？
经过哪个标准化器？
是否被修正？
是否有冲突？
是否可以回放？
```

## 21.2 血缘结构

```yaml
data_lineage:
  field_key: string
  token_address: string
  entity_id: string | null
  source_id: string
  source_record_id: string
  raw_payload_path: string
  raw_field_path: string
  normalized_record_id: string
  normalizer_version: string
  collected_at: datetime
  normalized_at: datetime
  transformation_steps:
    - step_name: string
      step_version: string
      description: string
  quality_status: string
  replay_available: boolean
```

---

# 22. 数据目录宪法

文件：

```text
data_storage_constitution.md
```

## 22.1 推荐目录

```text
/root/sikk-gmgn/data/
  source_wallet_bot/
    live/
    replay/
    raw/
    normalized/
    snapshots/
    manifests/

  intel_bot/
    behavior_inference/
    counter_evidence/
    quant_scores/
    structure_conclusion/
    reports/
    manifest/

  data_plane/
    raw/
    normalized/
    entities/
    events/
    snapshots/
    quality/
    lineage/
    handoff/
    reports/
```

---

## 22.2 原则

```text
1. raw 只存原始数据，不允许覆盖。
2. normalized 存标准化数据，不允许混入推理结论。
3. entities 存钱包、代币、群组等实体。
4. events 存买卖、转账、清仓、归集等事件。
5. snapshots 存不同运行阶段的状态快照。
6. quality 存质量评分、缺失、冲突、新鲜度。
7. lineage 存字段血缘。
8. handoff 存交接给 Evidence Plane 的数据包。
9. reports 存人类可读报告。
10. legacy runtime 数据保留，不直接移动，不作为新写入主路径。
```

---

# 23. Data Plane 输出合约

文件：

```text
data_handoff_contract.yaml
```

## 23.1 输出给 Evidence Plane

```yaml
data_handoff_packet:
  packet_id: string
  token_address: string
  generated_at: datetime
  data_plane_version: string
  run_id: string

  source_summary:
    sources_used: list
    sources_missing: list
    source_conflicts: list
    source_freshness_summary: object

  normalized_entities:
    token_entity_path: string
    wallet_entities_path: string
    wallet_group_entities_path: string
    pool_entity_path: string

  normalized_events:
    transaction_events_path: string
    wallet_behavior_events_path: string
    chip_structure_events_path: string
    market_structure_events_path: string

  snapshots:
    discovery_snapshot_path: string
    wallet_decision_snapshot_path: string
    market_structure_snapshot_path: string
    latest_snapshot_path: string

  data_quality:
    overall_data_quality_score: number
    completeness_score: number
    consistency_score: number
    freshness_score: number
    traceability_score: number
    replayability_score: number
    quality_status: string

  missing_fields:
    critical_missing_fields: list
    high_impact_missing_fields: list
    medium_impact_missing_fields: list

  conflict_fields:
    fields: list
    conflict_report_path: string

  lineage:
    lineage_index_path: string
    replay_manifest_path: string

  downstream_permission:
    evidence_plane_permission:
      - ALLOW_EVIDENCE_GENERATION
      - ALLOW_WEAK_EVIDENCE_ONLY
      - REQUIRE_DATA_REFRESH
      - BLOCK_EVIDENCE_GENERATION
    forbidden_claims:
      - NO_STRONG_WALLET_STRUCTURE_CLAIM
      - NO_STRONG_MARKET_CAP_CLAIM
      - NO_STRONG_BREAKOUT_CLAIM
      - NO_EXECUTION_CLAIM
```

---

# 24. Data Plane 验收标准

文件：

```text
data_acceptance_criteria.md
```

## 24.1 DATA_READY

必须满足：

```text
1. 数据源注册表已完成
2. 字段字典已完成
3. Domain Plane 字段需求已映射
4. 原始数据模型已定义
5. 标准化数据模型已定义
6. 实体模型已定义
7. 事件模型已定义
8. 快照模型已定义
9. 数据质量模型已定义
10. 新鲜度模型已定义
11. 缺失字段处理规则已定义
12. 数据冲突处理规则已定义
13. 数据血缘模型已定义
14. 数据目录宪法已定义
15. 数据交接合约已定义
16. 不存在直接交易信号逻辑
17. 不存在用缺失数据强判断
18. 可交接给 Evidence Plane
```

---

## 24.2 DATA_READY_WITH_GAPS

允许进入下一阶段，但必须标记：

```text
1. 部分数据源尚未真实接入
2. 部分钱包历史字段缺失
3. 同源组归因字段暂时不稳定
4. 市值字段多源冲突
5. 部分 K 线指标尚未稳定计算
6. 安全扫描覆盖不完整
7. replay 样本不足
```

---

## 24.3 DATA_REJECTED

以下情况必须驳回：

```text
1. 只写了数据说明，没有字段字典
2. 只有结果表，没有 raw 数据模型
3. 没有 normalized 数据模型
4. 没有质量评分
5. 没有新鲜度判断
6. 没有缺失字段处理
7. 没有冲突处理
8. 没有数据血缘
9. 没有快照
10. 没有交接合约
11. 数据层直接输出买入信号
12. 数据层直接推断主导侧意图
```

---

# 25. 当前 Data Plane 是否达到专业化轻量机构水准？

如果按上面结构落地，可以达到：

```text
轻量机构级 v1.0 合格
```

但还不是完整机构级 v2.0。

## 25.1 已达到的部分

|能力|状态|
|---|---|
|数据源注册|已设计|
|字段字典|已设计|
|原始数据模型|已设计|
|标准化数据模型|已设计|
|实体模型|已设计|
|事件模型|已设计|
|快照模型|已设计|
|数据质量模型|已设计|
|新鲜度模型|已设计|
|缺失处理|已设计|
|冲突处理|已设计|
|数据血缘|已设计|
|下游交接合约|已设计|

---

## 25.2 还没达到完整机构级的部分

|缺口|原因|后续阶段|
|---|---|---|
|真实 API 稳定性未验证|需要实际运行|工程落地|
|字段覆盖率未知|需要跑真实 token|Data Audit|
|钱包归并准确度未知|需要历史样本|Evidence / Replay|
|多源报价偏差阈值未校准|需要统计|Replay|
|K 线指标缺口未验证|需要数据测试|Scenario|
|安全扫描覆盖不完整|需要源对比|Execution Risk|
|质量评分权重未回测|需要样本反馈|Self-Upgrade|

结论：

```text
Data Plane 当前应先建立完整数据体系，不急于写策略判断。
只要字段、质量、新鲜度、血缘、快照和 handoff 合约落地，后续 Evidence Plane 才能专业化。
```

---

# 26. 给 HER 的可执行任务书

下面可以直接复制给 HER。

```text
任务名称：建立 P03 Data Plane｜数据平面专业化阶段数据包

任务目标：
在 /root/sikk-gmgn/system/data_plane/ 下建立 SIKK Stable Trader OS 的 P03 Data Plane 数据平面。该阶段不是普通数据说明，也不是简单采集脚本，而是一个可调度的数据事实生产层，负责把 Domain Plane 的领域字段需求转化为可采集、可校验、可标准化、可追溯、可评分、可快照、可回放、可交接的数据体系。

核心原则：
1. Data Plane 不直接生成交易信号。
2. Data Plane 不直接推断主导侧意图。
3. Data Plane 不允许用缺失字段强行判断。
4. Data Plane 必须保留 raw 原始数据。
5. Data Plane 必须建立 normalized 标准化数据。
6. Data Plane 必须建立字段字典。
7. Data Plane 必须记录数据来源、采集时间、字段血缘、新鲜度、质量评分。
8. Data Plane 必须处理缺失字段和多源冲突。
9. Data Plane 必须生成可交接给 Evidence Plane 的 handoff packet。
10. 所有核心语义必须使用中文说明，字段键名可以保留工程可读英文。

需要创建目录：
/root/sikk-gmgn/system/data_plane/

需要创建文件：
1. data_plane.yaml
2. data_context.md
3. data_source_registry.yaml
4. data_requirement_from_domain.yaml
5. data_field_dictionary.yaml
6. data_raw_model.yaml
7. data_normalized_model.yaml
8. data_entity_model.yaml
9. data_event_model.yaml
10. data_snapshot_model.yaml
11. data_quality_model.yaml
12. data_freshness_model.yaml
13. data_missing_policy.yaml
14. data_conflict_policy.yaml
15. data_lineage_model.yaml
16. data_storage_constitution.md
17. data_handoff_contract.yaml
18. data_acceptance_criteria.md
19. data_gap_register.md
20. data_review_checklist.md

每个文件要求：

data_plane.yaml：
定义阶段 ID、阶段名称、版本、权限边界、上下游平面、可定义内容、禁止内容、状态码和验收状态。

data_context.md：
写成 HER 运行前必须读取的数据平面上下文压缩包，说明 Data Plane 的作用、边界、目标、核心原则、禁止事项和下游交接方式。

data_source_registry.yaml：
建立数据源注册表。至少包括 GMGN Token 数据、GMGN 钱包数据、链上原始交易、OKX Quote、OKX Security、K线数据、流动性池数据、持有人快照、历史地址库、纸面交易数据、人工标注数据。每个数据源必须包含 source_id、source_name、source_type、primary_use、freshness_requirement_seconds、reliability_level、raw_storage_required、normalized_storage_required、known_risks、fallback_sources。

data_requirement_from_domain.yaml：
承接 Domain Plane 的字段需求。必须把领域对象映射到数据字段，包括代币对象、钱包对象、钱包群组对象、筹码对象、市值对象、价格结构对象、成交结构对象、流动性对象、安全对象、证据对象。

data_field_dictionary.yaml：
建立全系统字段字典。每个字段必须包含 field_key、field_name_cn、domain_object、data_type、required、unit、source_priority、freshness_requirement_seconds、quality_dimensions、downstream_use、missing_policy、notes。

data_raw_model.yaml：
定义 raw_data_record。必须包含 raw_record_id、source_id、token_address、collected_at、collection_run_id、raw_payload_type、raw_payload_path、source_query、source_response_status、source_latency_ms、checksum、parser_version、immutable。

data_normalized_model.yaml：
定义 normalized_record。必须包含 normalized_record_id、raw_record_id、token_address、entity_type、normalized_at、normalizer_version、fields、source_lineage、quality。

data_entity_model.yaml：
定义代币实体、钱包实体、钱包归并实体、钱包群组实体、池子实体、交易实体、快照实体、运行实体。必须定义各自的主键、字段和归并状态。

data_event_model.yaml：
定义事件模型。事件类型必须包括 TOKEN_DISCOVERED、WALLET_FIRST_BUY、WALLET_ACCUMULATION、WALLET_PARTIAL_SELL、WALLET_FULL_EXIT、WALLET_TRANSFER_OUT、FUNDING_SOURCE_LINKED、SAME_SOURCE_GROUP_DETECTED、SYNC_BUY_DETECTED、SYNC_SELL_DETECTED、CHIP_CONCENTRATION_CHANGED、CHIP_DISTRIBUTION_CHANGED、MARKET_CAP_STAGE_CHANGED、BREAKOUT_DETECTED、PULLBACK_DETECTED、FAILURE_TEST_DETECTED、QUOTE_DEVIATION_DETECTED、SECURITY_RISK_DETECTED。

data_snapshot_model.yaml：
定义 DISCOVERY_SNAPSHOT、WALLET_DECISION_SNAPSHOT、MARKET_STRUCTURE_SNAPSHOT、SIGNAL_SNAPSHOT、PAPER_ENTRY_SNAPSHOT、PAPER_EXIT_SNAPSHOT、REVIEW_SNAPSHOT。每个快照必须包含 token_state、wallet_state、chip_state、market_state、data_quality。

data_quality_model.yaml：
定义数据质量评分模型，包括完整性、准确性、一致性、新鲜度、可追溯性、可复盘性、稳定性、粒度适配。必须输出 DATA_HIGH_CONFIDENCE、DATA_USABLE、DATA_USABLE_WITH_GAPS、DATA_LOW_CONFIDENCE、DATA_UNUSABLE。

data_freshness_model.yaml：
定义不同数据类型的新鲜度要求。报价 15-30 秒，流动性 30-60 秒，K线当前周期内，钱包交易 60-180 秒，持有人快照 3-10 分钟，安全扫描 10-60 分钟，历史地址库长期有效但需要版本。必须定义 FRESH、ACCEPTABLE、STALE、EXPIRED、UNKNOWN。

data_missing_policy.yaml：
定义缺失字段分级，包括 CRITICAL_MISSING、HIGH_IMPACT_MISSING、MEDIUM_IMPACT_MISSING、LOW_IMPACT_MISSING、UNKNOWN_MISSING。必须说明每类缺失对下游权限的影响。

data_conflict_policy.yaml：
定义多源冲突处理规则。包括报价冲突、市值冲突、钱包持仓快照冲突、流动性冲突。禁止直接平均或静默覆盖冲突字段。

data_lineage_model.yaml：
定义字段血缘模型。每个字段必须能追溯 source_id、source_record_id、raw_payload_path、raw_field_path、normalized_record_id、normalizer_version、collected_at、normalized_at、transformation_steps、quality_status、replay_available。

data_storage_constitution.md：
建立数据目录宪法。明确 raw、normalized、entities、events、snapshots、quality、lineage、handoff、reports 的作用。明确 legacy runtime 数据保留，不移动，不作为新写入主路径。

data_handoff_contract.yaml：
定义 data_handoff_packet。必须包含 packet_id、token_address、generated_at、data_plane_version、run_id、source_summary、normalized_entities、normalized_events、snapshots、data_quality、missing_fields、conflict_fields、lineage、downstream_permission。

data_acceptance_criteria.md：
定义 DATA_READY、DATA_READY_WITH_GAPS、DATA_REJECTED 三类验收结果。每一类必须有明确条件。

data_gap_register.md：
登记当前无法完全解决的问题，包括数据源未真实接入、字段覆盖率未知、钱包归并准确度未知、多源报价阈值未校准、K线指标缺口、安全扫描覆盖不足、质量评分权重未回测。

data_review_checklist.md：
建立审计清单，用于检查 Data Plane 是否只是数据说明，是否缺少字段字典，是否缺少 raw 模型，是否缺少 normalized 模型，是否缺少质量评分，是否缺少新鲜度，是否缺少缺失处理，是否缺少冲突处理，是否缺少血缘，是否越权输出交易信号。

验收输出：
完成后输出：
1. 文件创建清单
2. 每个文件的核心内容摘要
3. DATA_READY / DATA_READY_WITH_GAPS / DATA_REJECTED 判断
4. 数据缺口清单
5. 字段字典摘要
6. 数据源注册摘要
7. 数据质量规则摘要
8. 下游 Evidence Plane handoff packet 摘要
9. 是否存在越权逻辑
10. 是否可以交接到 P04 Evidence Plane

最终验收标准：
只有当数据源、字段字典、raw 模型、normalized 模型、实体模型、事件模型、快照模型、质量模型、新鲜度模型、缺失处理、冲突处理、血缘模型、目录宪法、handoff 合约、验收标准、缺口登记全部存在时，才允许标记为 DATA_READY。
```

---

# 27. 下一步应该做什么

Data Plane 完成后，下一阶段是：

```text
P04 Evidence Plane：证据平面
```

顺序是：

```text
P03 Data Plane 完成
    ↓
P03 数据平面审计
    ↓
DATA_READY / DATA_READY_WITH_GAPS
    ↓
P04 Evidence Plane 建立证据对象
    ↓
字段 → 证据
事件 → 证据链
快照 → 状态证据
质量分 → 证据等级
缺失字段 → 不确定性标签
冲突字段 → 反证或弱证据
```

Evidence Plane 的核心任务是：

```text
不是继续抓数据，
而是把 Data Plane 输出的数据事实，
转化为支持 / 反驳 / 未知 / 冲突 的证据对象。
```

---

# 本次认知升级点

1. **Data Plane 不是数据采集脚本，而是事实生产系统。**
    
2. **字段字典是数据平面的核心资产。**  
    没有字段字典，HER 后续所有判断都会重新变成上下文猜测。
    
3. **raw 和 normalized 必须分离。**  
    raw 保证可追溯，normalized 保证可调用。
    
4. **快照比单点数据更重要。**  
    SIKK 判断的是状态变化，不是某一刻的孤立数值。
    
5. **数据质量决定证据权限。**  
    低质量数据不能生成强证据。
    
6. **缺失字段不是小问题，而是下游权限控制问题。**
    
7. **多源冲突不能静默合并。**  
    冲突字段必须保留，并限制下游判断强度。
    
8. **Data Plane 完成后，才有资格进入 Evidence Plane。**
    

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|GMGN / OKX 真实字段覆盖率未知|已定义字段需求，未验证真实可得性|Data Audit|
|钱包归并准确率未知|已定义 entity 模型|Evidence / Replay 校准|
|同源组识别阈值未确定|已定义字段和事件|后续样本统计|
|市值多源冲突阈值未校准|已定义冲突规则|Replay 统计|
|K 线指标计算口径未完全固定|已定义字段需求|Scenario Plane 固化|
|安全扫描覆盖范围未确认|已定义字段|Execution Risk Plane 补充|
|数据质量权重未回测|已定义初始权重|P08 / P09 迭代|
|历史地址库还不成熟|已定义接入位置|Review / Replay 长期积累|
|legacy runtime 数据如何吸收|已要求保留不移动|后续建立 legacy mapping|
|数据目录是否已经实际落地|目前是设计状态|HER 执行后验收|