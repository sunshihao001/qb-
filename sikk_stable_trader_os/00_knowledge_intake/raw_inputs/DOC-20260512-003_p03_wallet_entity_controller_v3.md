# P03 Wallet Entity Controller 专业版 v3.0

## 钱包实体归并、地址关系建模、角色候选初判与 P04 筹码结构交接控制器

---

## 0. 先修正定位

P03 不能被设计成普通的：

```text
钱包分类脚本
同源钱包识别脚本
聪明钱标签器
疑似庄钱包判断器
```

P03 的专业定位应该是：

```text
把 P02 交接过来的钱包事实种子、持有人快照、交易事实、资金来源线索，转化为可追踪、可归并、可分组、可评分、可交接的钱包实体主数据系统。
```

一句话定义：

> **P02 负责提供钱包事实种子。**  
> **P03 负责把地址变成“钱包实体、关系候选、行为特征、角色候选”。**  
> **P04 才负责基于这些实体和行为，判断筹码结构、迁移、留存、派发、对手盘压力。**

P03 不能直接说：

```text
庄家还在
筹码未出完
可以二段扩张
可以买
PAPER_READY
```

P03 只能输出：

```text
这个地址像什么角色候选
这些地址是否疑似同源候选
这些钱包行为是否存在同步候选
这些钱包是否适合进入 P04 筹码结构分析
哪些字段缺失
哪些判断只能弱使用
```

---

# 1. P03 阶段核心目标

P03 必须一次性解决 13 个问题：

|编号|核心问题|P03 必须输出|
|---|---|---|
|1|钱包地址是谁？|`wallet_address_record`|
|2|地址是否可归并为实体？|`wallet_entity_master_record`|
|3|钱包资金从哪里来？|`funding_source_link_record`|
|4|钱包在当前 token 中做了什么？|`wallet_token_behavior_record`|
|5|钱包是否属于同源候选？|`same_source_group_candidate_record`|
|6|钱包是否存在同步买入 / 卖出候选？|`sync_behavior_group_candidate_record`|
|7|钱包是否像早期执行、接盘、分发、利润回收等角色？|`wallet_role_candidate_record`|
|8|钱包当前持仓、卖出、清仓事实如何？|`wallet_position_fact_record`|
|9|钱包历史表现是否可作为辅助？|`wallet_history_seed_record`|
|10|这些归并和角色判断质量如何？|`wallet_entity_quality_record`|
|11|哪些字段缺失、冲突、只能弱使用？|`p03_gap_report` / `field_usage_limitations`|
|12|P04 筹码结构阶段要读取什么？|`p04_chip_structure_data_request_packet`|
|13|是否可以交接给 P04？|`p03_to_p04_handoff_packet`|

---

# 2. P03 的专业角色模型

P03 应该按 8 个专业角色设计，而不是只写一个钱包分类器。

|角色|负责问题|输出|
|---|---|---|
|钱包主数据治理官|地址如何建档、去重、归并|`wallet_entity_master_record`|
|资金路径分析官|钱包资金来源、归集、转出路径|`funding_source_link_record`|
|行为特征工程师|买入、卖出、持仓、清仓、转账行为特征|`wallet_token_behavior_record`|
|同源候选分析官|资金来源相似、时间同步、行为相似|`same_source_group_candidate_record`|
|同步行为分析官|sync buy / sync sell / coordinated action|`sync_behavior_group_candidate_record`|
|角色候选映射官|地址行为映射到角色候选|`wallet_role_candidate_record`|
|质量与不确定性官|置信度、缺口、冲突、限制|`wallet_entity_quality_record`|
|下游交接官|P04 应该如何使用这些实体和角色候选|`p04_data_request_packet` / `p03_handoff_packet`|

---

# 3. P03 底层方法论

## 3.1 地址 ≠ 实体原则

一个地址不是一个完整实体。

P03 必须区分：

```text
wallet_address：单个链上地址
wallet_entity：可能由多个地址归并出的实体候选
wallet_group_candidate：多个实体或地址形成的关系候选组
```

不能看到多个地址行为相似就直接说：

```text
同一个人
庄家钱包
主控钱包
```

只能输出：

```text
same_source_candidate
sync_behavior_candidate
funding_relation_candidate
role_candidate
confidence_level
counter_evidence
```

---

## 3.2 候选归因原则

P03 的所有结论都应使用候选语言：

```text
疑似
候选
初判
弱支持
中等支持
强候选
需要 P04 / P05 继续验证
```

P03 禁止使用确定性语言：

```text
确认庄家
确认主控
确认同源
确认派发
确认控盘
```

除非后续有治理定义的强确认规则，而且也应在 P05 Evidence / P06 Scenario 后生成，不在 P03 生成。

---

## 3.3 多因子归并原则

钱包归并不能只靠一个因素。

应至少考虑：

```text
资金来源相似
首次买入时间相近
买入金额结构相似
交易节奏相似
持仓变化相似
转账路径相似
利润归集地址相似
历史 token 行为复现
当前 token 行为协同
```

单一因素只能形成弱候选，不能形成强候选。

---

## 3.4 角色候选不等于筹码结论

P03 可以判断：

```text
早期执行钱包候选
同源执行组候选
分发接收钱包候选
利润归集钱包候选
接盘鲸鱼候选
短线机器人候选
历史复现钱包候选
```

但不能判断：

```text
筹码控制仍在
结构侧未出货
对手盘压力过高
派发已完成
二段扩张成立
```

这些属于 P04-P07。

---

# 4. P03 必须建立的核心对象

## 4.1 对象总表

|对象|作用|
|---|---|
|`P03 Input Manifest`|从 P02 接收了哪些钱包事实种子|
|`Wallet Address Record`|单地址基础事实|
|`Wallet Entity Master Record`|钱包实体主档|
|`Wallet Entity Resolution Record`|地址归并与实体解析|
|`Funding Source Link Record`|资金来源链路|
|`Funding Flow Edge Record`|资金流边|
|`Wallet Token Behavior Record`|当前 token 行为特征|
|`Wallet Position Fact Record`|当前持仓、买卖、清仓事实|
|`Wallet Temporal Behavior Record`|时间行为特征|
|`Wallet Amount Pattern Record`|金额模式特征|
|`Same Source Group Candidate Record`|疑似同源组候选|
|`Sync Behavior Group Candidate Record`|同步行为组候选|
|`Distribution Receiver Candidate Record`|分发接收候选|
|`Profit Collection Candidate Record`|利润归集候选|
|`Counterparty Wallet Candidate Record`|对手盘 / 接盘钱包候选|
|`Wallet Role Candidate Record`|钱包角色候选|
|`Wallet History Seed Record`|历史表现辅助种子|
|`Wallet Entity Quality Record`|实体归并质量|
|`P03 Gap Record`|缺口、冲突、不确定性|
|`P04 Chip Structure Data Request Packet`|给 P04 的数据请求|
|`P03 to P04 Handoff Packet`|P03 → P04 交接包|

---

# 5. P03 输入：必须读取什么

P03 必须从 P02 handoff 进入，不允许自由读取旧文件。

```yaml
p03_required_inputs:
  from_p02:
    - p02_to_p03_handoff_packet
    - p03_wallet_entity_data_request_packet
    - wallet_fact_seed_records
    - holder_snapshot_fact
    - transaction_fact_seed
    - market_fact_record
    - pair_pool_fact_record
    - data_quality_report
    - data_gap_report
    - data_conflict_report
    - field_usage_permission_packet

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - limitation_transfer_packet
    - forbidden_use_policy
    - governance_handoff_packet
    - domain_wallet_role_taxonomy_handoff

  required_contracts:
    - p03_input_contract
    - p03_output_contract
    - wallet_entity_schema_contract
    - wallet_role_taxonomy_contract
    - same_source_candidate_contract
    - p04_chip_structure_input_contract
```

P03 启动前必须确认：

```text
P02 已验收
P02 handoff 已生成
P02 没有 BLOCKED 状态
P03 只读取 Handoff 授权字段
字段使用权限没有被升级
所有输入仍保持 FACTS_ONLY / NO_STRATEGY_GATE / LIVE_EXECUTION_FORBIDDEN
```

---

# 6. Wallet Address Record

P03 的第一层不是分类，而是地址建档。

```yaml
wallet_address_record:
  wallet_address: string
  chain: string
  candidate_id: string
  token_address: string

  address_identity:
    address_valid: boolean
    address_type:
      - EOA
      - CONTRACT
      - LP_ADDRESS
      - CEX_LIKE
      - UNKNOWN
    first_seen_in_candidate_at: datetime | null
    first_seen_in_system_at: datetime | null

  current_token_position:
    current_holding_amount_token: number | null
    current_holding_pct: number | null
    current_holding_value_usd: number | null
    is_top_holder: boolean | null
    holder_rank: integer | null

  transaction_summary:
    first_buy_time: datetime | null
    last_buy_time: datetime | null
    first_sell_time: datetime | null
    last_sell_time: datetime | null
    total_buy_amount_token: number | null
    total_buy_amount_usd: number | null
    total_sell_amount_token: number | null
    total_sell_amount_usd: number | null
    buy_count: integer | null
    sell_count: integer | null
    transfer_in_count: integer | null
    transfer_out_count: integer | null

  profit_summary:
    realized_profit_usd: number | null
    unrealized_profit_usd: number | null
    realized_profit_pct: number | null
    unrealized_profit_pct: number | null

  source:
    source_record_ids: list
    wallet_fact_seed_ids: list
    transaction_fact_seed_ids: list

  trace:
    wallet_address_trace_id: string
    field_trace_ids: list
```

---

# 7. Wallet Entity Master Record

这是 P03 的核心资产。

```yaml
wallet_entity_master_record:
  wallet_entity_id: string
  candidate_id: string
  token_address: string
  chain: string

  entity_membership:
    primary_wallet_address: string
    member_wallet_addresses: list
    member_count: integer
    entity_resolution_status:
      - SINGLE_ADDRESS_ENTITY
      - SAME_SOURCE_ENTITY_CANDIDATE
      - SYNC_BEHAVIOR_ENTITY_CANDIDATE
      - MULTI_ADDRESS_ENTITY_CANDIDATE
      - ENTITY_UNRESOLVED
      - ENTITY_CONFLICTED

  entity_features:
    first_seen_time: datetime | null
    earliest_buy_time: datetime | null
    latest_activity_time: datetime | null
    total_current_holding_pct: number | null
    total_buy_usd: number | null
    total_sell_usd: number | null
    net_position_token: number | null
    net_position_usd: number | null
    realized_profit_usd: number | null
    unrealized_profit_usd: number | null

  relation_features:
    funding_source_count: integer
    shared_funding_source_count: integer
    shared_profit_collection_address_count: integer
    related_group_ids: list
    related_edge_ids: list

  behavior_features:
    early_entry_score: number | null
    accumulation_behavior_score: number | null
    partial_sell_score: number | null
    full_exit_score: number | null
    sync_behavior_score: number | null
    distribution_receiver_score: number | null

  role_candidates:
    role_candidate_ids: list
    strongest_role_candidate: string | null
    strongest_role_confidence: number | null

  quality:
    entity_resolution_confidence: number
    entity_quality_status:
      - ENTITY_HIGH_CONFIDENCE
      - ENTITY_USABLE
      - ENTITY_USABLE_WITH_GAPS
      - ENTITY_LOW_CONFIDENCE
      - ENTITY_REJECTED
    uncertainty_tags: list
    counter_evidence_ids: list

  trace:
    wallet_entity_trace_id: string
    member_wallet_trace_ids: list
    funding_link_trace_ids: list
    role_candidate_trace_ids: list

  downstream:
    p04_usage_permission:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - DO_NOT_USE
```

---

# 8. Wallet Entity Resolution Record

地址归并必须可解释，不能黑箱。

```yaml
wallet_entity_resolution_record:
  resolution_id: string
  wallet_entity_id: string
  candidate_id: string

  input_addresses:
    wallet_addresses: list

  resolution_signals:
    shared_funding_source:
      detected: boolean
      source_addresses: list
      score: number

    shared_profit_collection:
      detected: boolean
      collection_addresses: list
      score: number

    synchronized_buying:
      detected: boolean
      time_window_seconds: integer | null
      score: number

    synchronized_selling:
      detected: boolean
      time_window_seconds: integer | null
      score: number

    amount_pattern_similarity:
      detected: boolean
      score: number

    transaction_sequence_similarity:
      detected: boolean
      score: number

    historical_co_occurrence:
      detected: boolean
      score: number

  counter_signals:
    different_funding_sources: boolean
    contradictory_timing: boolean
    unrelated_history: boolean
    behavior_divergence: boolean

  result:
    resolution_decision:
      - KEEP_SINGLE_ADDRESS
      - CREATE_ENTITY_CANDIDATE
      - MERGE_INTO_EXISTING_ENTITY
      - FLAG_ENTITY_CONFLICT
      - REJECT_MERGE
    resolution_confidence: number
    evidence_level:
      - STRONG_CANDIDATE
      - MEDIUM_CANDIDATE
      - WEAK_CANDIDATE
      - INSUFFICIENT

  trace:
    resolution_trace_id: string
    supporting_trace_ids: list
    counter_trace_ids: list
```

---

# 9. Funding Source Link Record

资金来源是 P03 的关键，但不能过度推断。

```yaml
funding_source_link_record:
  funding_link_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  funding_source:
    funding_source_address: string | null
    funding_source_type:
      - FRESH_WALLET
      - CEX_LIKE
      - KNOWN_FUNDER
      - SAME_SOURCE_CANDIDATE
      - PROFIT_COLLECTION
      - UNKNOWN
    funding_time: datetime | null
    funding_amount_native: number | null
    funding_amount_usd: number | null
    funding_tx_hash: string | null

  relation:
    relation_type:
      - DIRECT_FUNDING
      - SHARED_FUNDER
      - MULTI_HOP_FUNDING
      - PROFIT_RETURN
      - UNKNOWN
    hop_count: integer | null
    relation_confidence: number

  quality:
    funding_link_quality:
      - FUNDING_LINK_HIGH
      - FUNDING_LINK_USABLE
      - FUNDING_LINK_WITH_GAPS
      - FUNDING_LINK_LOW
      - FUNDING_LINK_UNKNOWN
    missing_fields: list

  trace:
    funding_link_trace_id: string
    transaction_trace_ids: list
```

---

# 10. Funding Flow Edge Record

P03 要为 P04/P05 后续结构图准备边数据。

```yaml
funding_flow_edge_record:
  edge_id: string
  candidate_id: string
  from_address: string
  to_address: string

  edge_type:
    - FUNDING
    - TOKEN_TRANSFER
    - PROFIT_COLLECTION
    - LP_INTERACTION
    - UNKNOWN

  edge_time: datetime | null
  token_or_native:
    - NATIVE
    - TOKEN
    - STABLE
    - UNKNOWN
  amount: number | null
  amount_usd: number | null
  tx_hash: string | null

  relation_context:
    before_first_buy: boolean | null
    after_partial_sell: boolean | null
    after_full_exit: boolean | null
    related_wallet_entity_ids: list

  quality:
    edge_quality_status: string
    missing_fields: list

  trace:
    edge_trace_id: string
```

---

# 11. Wallet Token Behavior Record

当前 token 行为特征是 P03 的核心输出。

```yaml
wallet_token_behavior_record:
  behavior_id: string
  candidate_id: string
  token_address: string
  wallet_address: string
  wallet_entity_id: string | null

  entry_behavior:
    first_buy_time: datetime | null
    first_buy_market_cap_usd: number | null
    first_buy_price_usd: number | null
    first_buy_amount_token: number | null
    first_buy_amount_usd: number | null
    entry_rank_by_time: integer | null
    early_entry_bucket:
      - ULTRA_EARLY
      - EARLY
      - MID
      - LATE
      - UNKNOWN

  accumulation_behavior:
    buy_count: integer | null
    cumulative_buy_usd: number | null
    buy_time_span_seconds: integer | null
    repeated_buy_detected: boolean | null
    accumulation_pattern:
      - ONE_SHOT_BUY
      - LADDER_BUY
      - BURST_BUY
      - SPREAD_BUY
      - UNKNOWN

  sell_behavior:
    sell_count: integer | null
    cumulative_sell_usd: number | null
    first_sell_time: datetime | null
    last_sell_time: datetime | null
    partial_sell_detected: boolean | null
    full_exit_detected: boolean | null
    sell_ratio_pct: number | null
    remaining_holding_pct_of_bought: number | null

  transfer_behavior:
    transfer_in_count: integer | null
    transfer_out_count: integer | null
    token_transfer_out_detected: boolean | null
    transfer_to_related_wallet_detected: boolean | null

  current_status:
    current_holding_amount_token: number | null
    current_holding_pct: number | null
    current_position_status:
      - HOLDING
      - PARTIAL_EXIT
      - FULL_EXIT
      - TRANSFERRED_OUT
      - UNKNOWN

  quality:
    behavior_fact_quality: string
    missing_behavior_fields: list
    stale_behavior_fields: list

  trace:
    behavior_trace_id: string
    transaction_trace_ids: list
    field_trace_ids: list
```

---

# 12. Wallet Position Fact Record

```yaml
wallet_position_fact_record:
  position_fact_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  position:
    total_bought_token: number | null
    total_sold_token: number | null
    net_holding_token: number | null
    net_holding_pct_supply: number | null
    net_holding_value_usd: number | null
    sold_ratio_pct: number | null
    remaining_ratio_pct: number | null

  pnl:
    realized_profit_usd: number | null
    unrealized_profit_usd: number | null
    realized_profit_pct: number | null
    unrealized_profit_pct: number | null

  status:
    position_status:
      - ACCUMULATING
      - HOLDING
      - PARTIAL_SELLING
      - FULLY_EXITED
      - TRANSFERRED_OUT
      - UNKNOWN
    status_confidence: number

  downstream_note:
    p04_can_use_for_chip_retention: boolean
    p04_usage_limitations: list
```

---

# 13. Wallet Temporal Behavior Record

时间行为决定同步候选与早期执行候选。

```yaml
wallet_temporal_behavior_record:
  temporal_behavior_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  timing:
    first_buy_time: datetime | null
    first_sell_time: datetime | null
    last_activity_time: datetime | null
    holding_duration_seconds: integer | null
    launch_to_first_buy_seconds: integer | null
    discovery_to_first_buy_seconds: integer | null

  timing_buckets:
    entry_phase:
      - PRE_DISCOVERY
      - AT_DISCOVERY
      - POST_DISCOVERY_EARLY
      - LATE_ENTRY
      - UNKNOWN
    holding_duration_bucket:
      - INSTANT_FLIP
      - SHORT_HOLD
      - MEDIUM_HOLD
      - LONG_HOLD
      - STILL_HOLDING
      - UNKNOWN

  sync_features:
    nearest_group_buy_time_delta_seconds: integer | null
    nearest_group_sell_time_delta_seconds: integer | null
    sync_buy_candidate: boolean
    sync_sell_candidate: boolean

  quality:
    temporal_quality_status: string
    missing_time_fields: list
```

---

# 14. Wallet Amount Pattern Record

金额模式用于识别机器人 / 同源执行 / 分批行为候选。

```yaml
wallet_amount_pattern_record:
  amount_pattern_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  buy_amount_pattern:
    buy_amounts_usd: list
    average_buy_amount_usd: number | null
    median_buy_amount_usd: number | null
    repeated_amount_detected: boolean
    rounded_amount_detected: boolean
    amount_similarity_group_id: string | null

  sell_amount_pattern:
    sell_amounts_usd: list
    average_sell_amount_usd: number | null
    repeated_sell_amount_detected: boolean

  pattern_class:
    - HUMAN_LIKE_IRREGULAR
    - BOT_LIKE_REPEATED
    - SPLIT_EXECUTION
    - LARGE_WHALE_SINGLE
    - SMALL_WALLET_CLUSTER
    - UNKNOWN

  score:
    amount_similarity_score: number
    bot_like_amount_score: number

  quality:
    amount_pattern_quality: string
```

---

# 15. Same Source Group Candidate Record

同源候选不能只看 funding source，要多因子。

```yaml
same_source_group_candidate_record:
  group_id: string
  candidate_id: string
  group_type: SAME_SOURCE_GROUP_CANDIDATE

  members:
    wallet_addresses: list
    wallet_entity_ids: list
    member_count: integer

  supporting_signals:
    shared_funding_source:
      detected: boolean
      shared_funding_addresses: list
      score: number

    funding_time_similarity:
      detected: boolean
      max_time_delta_seconds: integer | null
      score: number

    buy_time_similarity:
      detected: boolean
      max_time_delta_seconds: integer | null
      score: number

    amount_similarity:
      detected: boolean
      score: number

    transaction_sequence_similarity:
      detected: boolean
      score: number

    profit_collection_similarity:
      detected: boolean
      collection_addresses: list
      score: number

  counter_signals:
    distinct_funding_sources: boolean
    opposite_trading_behavior: boolean
    unrelated_history: boolean
    timing_dispersion_high: boolean

  group_score:
    same_source_score: number
    confidence_level:
      - STRONG_CANDIDATE
      - MEDIUM_CANDIDATE
      - WEAK_CANDIDATE
      - INSUFFICIENT

  downstream:
    p04_can_use_for_group_holding: boolean
    p04_usage_permission:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - DO_NOT_USE

  trace:
    group_trace_id: string
    member_trace_ids: list
    supporting_trace_ids: list
    counter_trace_ids: list
```

---

# 16. Sync Behavior Group Candidate Record

同步买卖候选要与同源候选分开。

```yaml
sync_behavior_group_candidate_record:
  sync_group_id: string
  candidate_id: string

  sync_type:
    - SYNC_BUY_CANDIDATE
    - SYNC_SELL_CANDIDATE
    - SYNC_BUY_AND_SELL_CANDIDATE
    - BURST_ACTIVITY_CANDIDATE

  members:
    wallet_addresses: list
    wallet_entity_ids: list
    member_count: integer

  sync_window:
    event_type: BUY|SELL|TRANSFER|MIXED
    window_start: datetime | null
    window_end: datetime | null
    window_seconds: integer | null

  sync_features:
    time_clustering_score: number
    amount_similarity_score: number
    sequence_similarity_score: number
    source_overlap_score: number
    sync_behavior_score: number

  interpretation_limit:
    not_same_as_same_source: true
    requires_p04_chip_context: true
    requires_p05_evidence_confirmation: true

  quality:
    sync_group_quality:
      - SYNC_GROUP_STRONG_CANDIDATE
      - SYNC_GROUP_MEDIUM_CANDIDATE
      - SYNC_GROUP_WEAK_CANDIDATE
      - SYNC_GROUP_LOW_CONFIDENCE
```

---

# 17. Distribution Receiver Candidate Record

P03 可以识别“分发接收候选”，但不能判断派发完成。

```yaml
distribution_receiver_candidate_record:
  receiver_candidate_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  receiver_signals:
    received_tokens_from_related_wallet: boolean
    received_after_price_expansion: boolean | null
    received_from_early_wallet: boolean | null
    received_without_market_buy: boolean | null
    quick_sell_after_receive: boolean | null

  relation:
    sender_wallet_address: string | null
    sender_wallet_entity_id: string | null
    transfer_tx_hash: string | null
    transfer_time: datetime | null
    transfer_amount_token: number | null

  role_candidate:
    role_type: DISTRIBUTION_RECEIVER_CANDIDATE
    role_confidence: number
    confidence_level:
      - STRONG_CANDIDATE
      - MEDIUM_CANDIDATE
      - WEAK_CANDIDATE
      - INSUFFICIENT

  downstream_limit:
    p04_must_check_chip_transfer: true
    p05_must_confirm_with_evidence: true
```

---

# 18. Profit Collection Candidate Record

```yaml
profit_collection_candidate_record:
  collection_candidate_id: string
  candidate_id: string
  collection_address: string

  collection_signals:
    receives_native_after_sells: boolean
    receives_from_multiple_wallets: boolean
    repeated_collection_pattern: boolean
    related_wallet_count: integer
    total_received_usd: number | null

  linked_wallets:
    wallet_addresses: list
    wallet_entity_ids: list

  confidence:
    profit_collection_score: number
    confidence_level:
      - STRONG_CANDIDATE
      - MEDIUM_CANDIDATE
      - WEAK_CANDIDATE
      - INSUFFICIENT

  trace:
    collection_trace_id: string
    funding_edge_trace_ids: list
```

---

# 19. Counterparty Wallet Candidate Record

P03 只识别候选，不判断“对手盘压力”。

```yaml
counterparty_wallet_candidate_record:
  counterparty_candidate_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  signals:
    bought_after_price_expansion: boolean | null
    bought_from_selling_cluster_window: boolean | null
    large_buy_near_distribution_window: boolean | null
    holding_after_early_wallet_sell: boolean | null
    high_unrealized_loss_risk: boolean | null

  role_candidate:
    role_type:
      - COUNTERPARTY_WHALE_CANDIDATE
      - LATE_BUYER_CANDIDATE
      - EXIT_LIQUIDITY_CANDIDATE
      - UNKNOWN
    role_confidence: number

  downstream_limit:
    p04_can_use_as_counterparty_seed: true
    p04_must_calculate_counterparty_pressure: true
```

---

# 20. Wallet Role Candidate Record

P03 的角色结果必须是候选标签。

```yaml
wallet_role_candidate_record:
  role_candidate_id: string
  candidate_id: string
  wallet_address: string
  wallet_entity_id: string | null

  role_taxonomy:
    candidate_roles:
      - EARLY_EXECUTION_WALLET_CANDIDATE
      - SAME_SOURCE_EXECUTION_GROUP_MEMBER_CANDIDATE
      - ACCUMULATION_WALLET_CANDIDATE
      - PARTIAL_SELLER_CANDIDATE
      - FULL_EXIT_WALLET_CANDIDATE
      - DISTRIBUTION_RECEIVER_CANDIDATE
      - PROFIT_COLLECTION_WALLET_CANDIDATE
      - COUNTERPARTY_WHALE_CANDIDATE
      - LATE_BUYER_CANDIDATE
      - BOT_LIKE_TRADER_CANDIDATE
      - HISTORICAL_RECURRENCE_WALLET_CANDIDATE
      - UNKNOWN

  role_scores:
    early_execution_score: number
    same_source_member_score: number
    accumulation_score: number
    partial_seller_score: number
    full_exit_score: number
    receiver_score: number
    profit_collection_score: number
    counterparty_score: number
    bot_like_score: number
    historical_recurrence_score: number

  strongest_role:
    role: string
    score: number
    confidence_level:
      - STRONG_CANDIDATE
      - MEDIUM_CANDIDATE
      - WEAK_CANDIDATE
      - UNKNOWN

  supporting_facts:
    field_trace_ids: list
    behavior_ids: list
    funding_link_ids: list
    group_candidate_ids: list

  counter_facts:
    counter_signal_ids: list
    uncertainty_tags: list

  forbidden_claims:
    - CONFIRMED_MARKET_MAKER
    - CONFIRMED_DOMINANT_SIDE
    - CONFIRMED_CHIP_CONTROL
    - BUY_SIGNAL
    - PAPER_READY
```

---

# 21. Wallet History Seed Record

历史地址库是辅助，不是决定性判断。

```yaml
wallet_history_seed_record:
  history_seed_id: string
  wallet_address: string
  wallet_entity_id: string | null

  historical_profile:
    historical_token_count: integer | null
    historical_win_rate: number | null
    historical_avg_profit_pct: number | null
    historical_max_profit_pct: number | null
    historical_loss_rate: number | null
    known_recurrence_count: integer | null

  historical_behavior_tags:
    - EARLY_BUYER_HISTORY
    - FAST_FLIPPER_HISTORY
    - SAME_SOURCE_RECURRING_HISTORY
    - DISTRIBUTION_RECEIVER_HISTORY
    - BOT_LIKE_HISTORY
    - UNKNOWN

  quality:
    historical_data_available: boolean
    historical_data_quality:
      - HIGH
      - USABLE
      - WEAK
      - MISSING

  usage_limit:
    can_support_role_candidate: true
    cannot_confirm_current_role_alone: true
```

---

# 22. Wallet Entity Quality Record

```yaml
wallet_entity_quality_record:
  candidate_id: string
  generated_at: datetime

  quality_dimensions:
    wallet_fact_coverage_score: number
    transaction_coverage_score: number
    funding_source_coverage_score: number
    entity_resolution_confidence_score: number
    sync_detection_quality_score: number
    role_candidate_quality_score: number
    traceability_score: number
    freshness_score: number

  weighted_quality_score: number

  quality_status:
    - WALLET_ENTITY_HIGH_CONFIDENCE
    - WALLET_ENTITY_USABLE
    - WALLET_ENTITY_USABLE_WITH_GAPS
    - WALLET_ENTITY_LOW_CONFIDENCE
    - WALLET_ENTITY_UNUSABLE

  limitations:
    missing_funding_sources: list
    stale_wallet_rows: list
    partial_transaction_history: list
    weak_group_candidates: list
    unresolved_entity_conflicts: list

  downstream_permission:
    p04_chip_structure_allowed: boolean
    p04_usage_mode:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - BLOCKED
    p05_evidence_allowed: false
    p07_strategy_gate_allowed: false
    paper_runtime_allowed: false
```

---

# 23. P03 Gap Policy

```yaml
p03_gap_policy:
  BLOCKING_GAP:
    result: P03_BLOCKED
    examples:
      - p02_handoff_missing
      - wallet_fact_seed_missing_for_all_candidates
      - no_trace
      - live_execution_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P03_REJECTED
    examples:
      - wallet_address_missing
      - wallet_fact_seed_untraceable
      - all_wallet_rows_invalid
      - output_contract_missing

  HIGH_GAP:
    result: P03_READY_WITH_GAPS
    downstream_permission: P04_LIMITED
    examples:
      - funding_source_missing
      - transaction_history_partial
      - holder_snapshot_stale
      - same_source_candidate_low_confidence
      - entity_resolution_conflicted

  MEDIUM_GAP:
    result: P03_READY_WITH_GAPS
    downstream_permission: P04_ALLOWED_WITH_LIMITATIONS
    examples:
      - historical_wallet_profile_missing
      - profit_data_missing
      - pool_interaction_missing
      - transfer_edges_partial

  LOW_GAP:
    result: P03_READY_WITH_GAPS
    downstream_permission: P04_ALLOWED_WITH_NOTE
    examples:
      - wallet_label_missing
      - token_symbol_missing
      - optional historical tags missing
```

---

# 24. P03 Hard Negative Rules

```yaml
p03_hard_negative_rules:
  - rule_id: P03_BLOCK_001
    name: 未读取 P02 handoff
    condition: p02_to_p03_handoff_packet_missing == true
    result: P03_BLOCKED
    reason: P03 不能绕过 P02 / Handoff 启动

  - rule_id: P03_BLOCK_002
    name: 钱包事实种子全部缺失
    condition: wallet_fact_seed_missing_for_all_candidates == true
    result: P03_REJECTED
    reason: 无钱包输入，无法建立钱包实体

  - rule_id: P03_BLOCK_003
    name: 钱包地址不可追踪
    condition: wallet_address_trace_missing == true
    result: P03_BLOCKED
    reason: 无 trace 的地址不能进入实体归并

  - rule_id: P03_BLOCK_004
    name: 静默合并钱包实体
    condition: entity_merge_performed == true and entity_resolution_record_missing == true
    result: P03_BLOCKED
    reason: 钱包归并必须有解析记录

  - rule_id: P03_BLOCK_005
    name: 把角色候选当作确认角色
    condition: output_contains_confirmed_market_maker_or_dominant_side == true
    result: P03_BLOCKED
    reason: P03 只能输出角色候选

  - rule_id: P03_BLOCK_006
    name: 输出筹码控制结论
    condition: output_contains in [chip_control_retained, active_distribution, counterparty_pressure_score]
    result: P03_BLOCKED
    reason: 筹码结构属于 P04

  - rule_id: P03_BLOCK_007
    name: 输出证据或场景
    condition: output_contains in [evidence_strength, scenario_claim, strategy_signal, paper_ready]
    result: P03_BLOCKED
    reason: P03 越权

  - rule_id: P03_BLOCK_008
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P03_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 25. P03 状态机专业版

```yaml
p03_wallet_entity_state_machine:
  states:
    - P03_UNINITIALIZED
    - P03_CONTEXT_LOADED
    - P03_HANDOFF_READ
    - P03_INPUT_MANIFEST_BUILT
    - P03_WALLET_ADDRESS_INDEXED
    - P03_WALLET_ADDRESS_RECORDS_BUILT
    - P03_FUNDING_LINKS_EXTRACTED
    - P03_BEHAVIOR_FEATURES_BUILT
    - P03_POSITION_FACTS_BUILT
    - P03_TEMPORAL_FEATURES_BUILT
    - P03_AMOUNT_PATTERNS_BUILT
    - P03_ENTITY_RESOLUTION_RUNNING
    - P03_ENTITY_MASTER_BUILT
    - P03_GROUP_CANDIDATES_BUILT
    - P03_ROLE_CANDIDATES_BUILT
    - P03_HISTORY_SEEDS_ATTACHED
    - P03_QUALITY_SCORED
    - P03_GAP_ANALYZED
    - P03_P04_DATA_REQUEST_BUILT
    - P03_READY_FOR_ACCEPTANCE
    - P03_ACCEPTANCE_READY
    - P03_READY_FOR_P04_HANDOFF
    - P03_READY_WITH_GAPS
    - P03_REJECTED
    - P03_BLOCKED

  critical_transitions:
    - from: P03_HANDOFF_READ
      to: P03_INPUT_MANIFEST_BUILT
      condition: p02_handoff_valid == true

    - from: P03_INPUT_MANIFEST_BUILT
      to: P03_WALLET_ADDRESS_INDEXED
      condition: wallet_fact_seed_available == true

    - from: P03_WALLET_ADDRESS_INDEXED
      to: P03_WALLET_ADDRESS_RECORDS_BUILT
      condition: wallet_address_records_created == true

    - from: P03_WALLET_ADDRESS_RECORDS_BUILT
      to: P03_FUNDING_LINKS_EXTRACTED
      condition: funding_link_extraction_attempted == true

    - from: P03_FUNDING_LINKS_EXTRACTED
      to: P03_BEHAVIOR_FEATURES_BUILT
      condition: wallet_token_behavior_records_created == true

    - from: P03_BEHAVIOR_FEATURES_BUILT
      to: P03_ENTITY_RESOLUTION_RUNNING
      condition: behavior_features_available == true

    - from: P03_ENTITY_RESOLUTION_RUNNING
      to: P03_ENTITY_MASTER_BUILT
      condition: wallet_entity_master_records_created == true

    - from: P03_ENTITY_MASTER_BUILT
      to: P03_GROUP_CANDIDATES_BUILT
      condition: same_source_and_sync_group_candidates_created == true

    - from: P03_GROUP_CANDIDATES_BUILT
      to: P03_ROLE_CANDIDATES_BUILT
      condition: wallet_role_candidate_records_created == true

    - from: P03_ROLE_CANDIDATES_BUILT
      to: P03_QUALITY_SCORED
      condition: wallet_entity_quality_record_created == true

    - from: P03_QUALITY_SCORED
      to: P03_GAP_ANALYZED
      condition: p03_gap_report_created == true

    - from: P03_GAP_ANALYZED
      to: P03_P04_DATA_REQUEST_BUILT
      condition: p04_chip_structure_data_request_packet_created == true

    - from: P03_P04_DATA_REQUEST_BUILT
      to: P03_READY_FOR_ACCEPTANCE
      condition: p03_output_contract_ready == true

    - from: P03_READY_FOR_ACCEPTANCE
      to: P03_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P03_ACCEPTANCE_READY
      to: P03_READY_FOR_P04_HANDOFF
      condition: p03_to_p04_handoff_packet_created == true
```

---

# 26. P04 Chip Structure Data Request Packet

P03 必须告诉 P04 筹码结构阶段应该如何使用钱包实体。

```yaml
p04_chip_structure_data_request_packet:
  packet_id: string
  from_controller: P03_WALLET_ENTITY_CONTROLLER
  to_controller: P04_CHIP_STRUCTURE_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  available_inputs_for_p04:
    wallet_entity_master_records_path: string
    wallet_position_fact_records_path: string
    same_source_group_candidates_path: string
    sync_behavior_group_candidates_path: string
    distribution_receiver_candidates_path: string
    profit_collection_candidates_path: string
    counterparty_wallet_candidates_path: string
    wallet_role_candidate_records_path: string
    funding_flow_edges_path: string

  p04_required_processing:
    - chip_concentration_calculation
    - early_wallet_remaining_pct_calculation
    - structural_wallet_holding_pct_calculation
    - group_holding_aggregation
    - chip_transfer_status_detection
    - distribution_progress_estimation
    - counterparty_pressure_calculation
    - dominant_side_chip_retention_status

  usage_limitations:
    - WALLET_ROLE_CANDIDATE_ONLY
    - NO_CONFIRMED_MARKET_MAKER
    - NO_CONFIRMED_CHIP_CONTROL
    - NO_EVIDENCE
    - NO_SCENARIO
    - NO_STRATEGY_GATE
    - LIVE_EXECUTION_FORBIDDEN

  field_usage_permissions:
    full_use_fields: list
    weak_use_only_fields: list
    observe_only_fields: list
    do_not_use_fields: list

  gaps_to_resolve_in_p04:
    missing_group_holding_fields: list
    weak_same_source_candidates: list
    stale_holder_snapshot_candidates: list
    partial_transaction_history_candidates: list
```

---

# 27. P03 to P04 Handoff Packet

```yaml
p03_to_p04_handoff_packet:
  packet_id: string
  packet_type: P03_TO_P04_WALLET_ENTITY_HANDOFF
  generated_at: datetime

  route:
    from_controller: P03_WALLET_ENTITY_CONTROLLER
    to_controller: P04_CHIP_STRUCTURE_CONTROLLER

  upstream_control:
    p02_handoff_packet_id: string
    p03_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    candidate_count_wallet_entity_ready: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  wallet_entity_package:
    wallet_address_records_path: string
    wallet_entity_master_records_path: string
    wallet_entity_resolution_records_path: string
    funding_source_link_records_path: string
    funding_flow_edge_records_path: string
    wallet_token_behavior_records_path: string
    wallet_position_fact_records_path: string
    wallet_temporal_behavior_records_path: string
    wallet_amount_pattern_records_path: string

  group_candidates:
    same_source_group_candidates_path: string
    sync_behavior_group_candidates_path: string
    distribution_receiver_candidates_path: string
    profit_collection_candidates_path: string
    counterparty_wallet_candidates_path: string

  role_candidates:
    wallet_role_candidate_records_path: string
    wallet_history_seed_records_path: string
    role_candidate_summary_path: string

  quality:
    wallet_entity_quality_report_path: string
    entity_resolution_quality_summary: object
    group_candidate_quality_summary: object
    role_candidate_quality_summary: object

  p04_data_request:
    p04_chip_structure_data_request_packet_path: string
    required_p04_tasks: list
    missing_inputs_by_candidate: object

  limitations:
    - WALLET_ROLE_CANDIDATE_ONLY
    - NO_CONFIRMED_DOMINANT_SIDE
    - NO_CONFIRMED_CHIP_CONTROL
    - NO_EVIDENCE
    - NO_SCENARIO
    - NO_STRATEGY_GATE
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P04_CHIP_STRUCTURE_CONTROLLER
    forbidden:
      - P05_EVIDENCE_CONTROLLER
      - P06_SCENARIO_RECOGNITION_CONTROLLER
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p04_must_read_first:
      - p03_to_p04_handoff_packet
      - p04_chip_structure_data_request_packet
      - wallet_entity_master_records
      - wallet_position_fact_records
      - same_source_group_candidates
      - sync_behavior_group_candidates
      - wallet_role_candidate_records
      - wallet_entity_quality_report
      - field_usage_permissions
```

---

# 28. P03 文件体系

## 28.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p03_wallet_entity_controller/
```

必须创建：

```text
p03_wallet_entity_controller.yaml
p03_wallet_entity_context.md
p03_input_contract.yaml
p03_output_contract.yaml
wallet_address_record_schema.yaml
wallet_entity_master_record_schema.yaml
wallet_entity_resolution_record_schema.yaml
funding_source_link_record_schema.yaml
funding_flow_edge_record_schema.yaml
wallet_token_behavior_record_schema.yaml
wallet_position_fact_record_schema.yaml
wallet_temporal_behavior_record_schema.yaml
wallet_amount_pattern_record_schema.yaml
same_source_group_candidate_schema.yaml
sync_behavior_group_candidate_schema.yaml
distribution_receiver_candidate_schema.yaml
profit_collection_candidate_schema.yaml
counterparty_wallet_candidate_schema.yaml
wallet_role_candidate_schema.yaml
wallet_history_seed_schema.yaml
wallet_entity_quality_record_schema.yaml
wallet_role_taxonomy.yaml
entity_resolution_policy.yaml
same_source_scoring_policy.yaml
sync_behavior_scoring_policy.yaml
wallet_role_scoring_policy.yaml
wallet_entity_gap_policy.yaml
wallet_entity_hard_negative_rules.yaml
wallet_entity_state_machine.yaml
wallet_entity_trace_requirements.yaml
p04_chip_structure_data_request_packet_contract.yaml
p03_to_p04_handoff_contract.yaml
p03_acceptance_criteria.md
p03_storage_constitution.md
p03_test_matrix.yaml
p03_report_model.yaml
p03_review_checklist.md
her_p03_execution_protocol.md
```

---

## 28.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p03_wallet_entity/
  input_manifest/
  wallet_address_records/
  wallet_entity_master/
  entity_resolution/
  funding_source_links/
  funding_flow_edges/
  wallet_token_behavior/
  wallet_position_facts/
  wallet_temporal_behavior/
  wallet_amount_patterns/
  same_source_groups/
  sync_behavior_groups/
  distribution_receivers/
  profit_collection/
  counterparty_wallets/
  wallet_role_candidates/
  wallet_history_seed/
  quality/
  gaps/
  conflicts/
  p04_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 29. P03 测试矩阵

```yaml
p03_test_matrix:
  - test_id: P03_TEST_001
    name: 正常 P02 handoff，包含 wallet rows 与交易记录
    expected_status: P03_READY_FOR_P04_HANDOFF

  - test_id: P03_TEST_002
    name: 缺 P02 handoff
    expected_status: P03_BLOCKED

  - test_id: P03_TEST_003
    name: wallet_fact_seed 全部缺失
    expected_status: P03_REJECTED

  - test_id: P03_TEST_004
    name: 有 wallet rows 但 funding source 缺失
    expected_status: P03_READY_WITH_GAPS
    expected_limitation: FUNDING_SOURCE_MISSING

  - test_id: P03_TEST_005
    name: 多钱包共享同一 funding source
    expected_output: same_source_group_candidate_record

  - test_id: P03_TEST_006
    name: 多钱包在短时间窗口同步买入
    expected_output: sync_buy_group_candidate_record

  - test_id: P03_TEST_007
    name: 钱包角色候选强支持但反证存在
    expected_status: P03_READY_WITH_GAPS
    expected_output: wallet_role_candidate_with_counter_facts

  - test_id: P03_TEST_008
    name: P03 输出确认庄家
    expected_status: P03_BLOCKED

  - test_id: P03_TEST_009
    name: P03 输出 chip_control_retained
    expected_status: P03_BLOCKED

  - test_id: P03_TEST_010
    name: P03 请求进入 paper runtime
    expected_status: P03_BLOCKED

  - test_id: P03_TEST_011
    name: 无 trace 的钱包归并
    expected_status: P03_BLOCKED

  - test_id: P03_TEST_012
    name: legacy wallet history only
    expected_status: P03_READY_WITH_GAPS
    expected_limitation: HISTORY_OBSERVE_ONLY
```

---

# 30. P03 报告模型

```yaml
p03_wallet_entity_report:
  report_id: string
  generated_at: datetime
  controller_id: P03_WALLET_ENTITY_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    wallet_address_count: integer
    wallet_entity_count: integer
    same_source_group_candidate_count: integer
    sync_group_candidate_count: integer
    role_candidate_count: integer
    ready_for_p04_count: integer
    ready_with_gaps_count: integer
    rejected_count: integer
    blocked_count: integer

  entity_resolution_summary:
    single_address_entity_count: integer
    multi_address_entity_candidate_count: integer
    conflicted_entity_count: integer
    average_entity_resolution_confidence: number

  funding_summary:
    funding_links_detected_count: integer
    shared_funding_source_count: integer
    profit_collection_candidate_count: integer
    missing_funding_source_count: integer

  behavior_summary:
    early_entry_wallet_count: integer
    partial_seller_count: integer
    full_exit_wallet_count: integer
    holding_wallet_count: integer
    sync_buy_group_count: integer
    sync_sell_group_count: integer

  role_summary:
    role_candidate_distribution: object
    strong_candidate_count: integer
    medium_candidate_count: integer
    weak_candidate_count: integer
    unknown_count: integer

  quality_summary:
    wallet_entity_quality_distribution: object
    entity_resolution_quality_distribution: object
    role_candidate_quality_distribution: object

  gap_summary:
    blocking_gaps: list
    critical_gaps: list
    high_gaps: list
    medium_gaps: list
    low_gaps: list

  p04_handoff_summary:
    p04_handoff_ready: boolean
    p04_limited_candidates: integer
    p04_required_tasks: list

  compliance:
    confirmed_market_maker_claim_generated: false
    chip_control_claim_generated: false
    evidence_generated: false
    scenario_claim_generated: false
    strategy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
```

---

# 31. HER P03 执行协议

```text
HER 执行 P03 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P03 controller context
4. 读取 P02 → P03 handoff packet
5. 读取 p03_wallet_entity_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P03 input_manifest
8. 建立 wallet_address_record
9. 建立 wallet_position_fact_record
10. 抽取 funding_source_link_record
11. 建立 funding_flow_edge_record
12. 建立 wallet_token_behavior_record
13. 建立 wallet_temporal_behavior_record
14. 建立 wallet_amount_pattern_record
15. 执行 wallet_entity_resolution
16. 建立 wallet_entity_master_record
17. 建立 same_source_group_candidate_record
18. 建立 sync_behavior_group_candidate_record
19. 建立 distribution_receiver_candidate_record
20. 建立 profit_collection_candidate_record
21. 建立 counterparty_wallet_candidate_record
22. 建立 wallet_role_candidate_record
23. 附加 wallet_history_seed_record
24. 生成 wallet_entity_quality_record
25. 生成 P03 gap report
26. 生成 p04_chip_structure_data_request_packet
27. 写入 P03 trace
28. 生成 p03_wallet_entity_report
29. 生成 p03_to_p04_handoff_packet
30. 执行 P03 acceptance
31. 只允许 handoff 给 P04
```

禁止：

```text
1. 不允许无 P02 handoff 启动 P03
2. 不允许无 wallet_fact_seed 建立钱包实体
3. 不允许无 trace 合并钱包实体
4. 不允许把同源候选说成确认同源
5. 不允许把角色候选说成确认庄家
6. 不允许输出筹码控制结论
7. 不允许输出 evidence
8. 不允许输出 scenario
9. 不允许输出 strategy signal
10. 不允许进入 paper runtime
11. 不允许任何 live execution
```

---

# 32. 给 HER 的专业化任务书

```text
任务名称：重建 P03 Wallet Entity Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p03_wallet_entity_controller/ 下重建 P03 Wallet Entity Controller。该控制器不是普通钱包分类脚本，也不是确认庄家钱包的模块，而是钱包实体归并、资金来源建模、同步行为候选、角色候选初判与 P04 筹码结构交接控制器。它负责读取 P02 Source Data Fact Controller 输出的钱包事实种子、持有人快照、交易事实种子和数据质量报告，将钱包地址转化为 wallet entity、funding links、behavior features、same-source group candidates、sync behavior candidates、role candidates，并生成 P04 Chip Structure Data Request Packet 与 P03→P04 Handoff Packet。

核心原则：
1. P03 只建立钱包实体、关系候选、行为特征和角色候选。
2. P03 不确认庄家。
3. P03 不确认主导侧。
4. P03 不判断筹码控制。
5. P03 不判断派发完成。
6. P03 不生成证据。
7. P03 不识别场景。
8. P03 不做策略准入。
9. P03 不进入 paper runtime。
10. P03 不允许 live execution。
11. P03 必须生成 P04 Chip Structure Data Request Packet。
12. P03 只能交接给 P04 Chip Structure Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p03_wallet_entity_controller/

需要创建系统文件：
1. p03_wallet_entity_controller.yaml
2. p03_wallet_entity_context.md
3. p03_input_contract.yaml
4. p03_output_contract.yaml
5. wallet_address_record_schema.yaml
6. wallet_entity_master_record_schema.yaml
7. wallet_entity_resolution_record_schema.yaml
8. funding_source_link_record_schema.yaml
9. funding_flow_edge_record_schema.yaml
10. wallet_token_behavior_record_schema.yaml
11. wallet_position_fact_record_schema.yaml
12. wallet_temporal_behavior_record_schema.yaml
13. wallet_amount_pattern_record_schema.yaml
14. same_source_group_candidate_schema.yaml
15. sync_behavior_group_candidate_schema.yaml
16. distribution_receiver_candidate_schema.yaml
17. profit_collection_candidate_schema.yaml
18. counterparty_wallet_candidate_schema.yaml
19. wallet_role_candidate_schema.yaml
20. wallet_history_seed_schema.yaml
21. wallet_entity_quality_record_schema.yaml
22. wallet_role_taxonomy.yaml
23. entity_resolution_policy.yaml
24. same_source_scoring_policy.yaml
25. sync_behavior_scoring_policy.yaml
26. wallet_role_scoring_policy.yaml
27. wallet_entity_gap_policy.yaml
28. wallet_entity_hard_negative_rules.yaml
29. wallet_entity_state_machine.yaml
30. wallet_entity_trace_requirements.yaml
31. p04_chip_structure_data_request_packet_contract.yaml
32. p03_to_p04_handoff_contract.yaml
33. p03_acceptance_criteria.md
34. p03_storage_constitution.md
35. p03_test_matrix.yaml
36. p03_report_model.yaml
37. p03_review_checklist.md
38. her_p03_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p03_wallet_entity/
  input_manifest/
  wallet_address_records/
  wallet_entity_master/
  entity_resolution/
  funding_source_links/
  funding_flow_edges/
  wallet_token_behavior/
  wallet_position_facts/
  wallet_temporal_behavior/
  wallet_amount_patterns/
  same_source_groups/
  sync_behavior_groups/
  distribution_receivers/
  profit_collection/
  counterparty_wallets/
  wallet_role_candidates/
  wallet_history_seed/
  quality/
  gaps/
  conflicts/
  p04_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p03_wallet_entity_controller.yaml：定义 P03 身份、职责、权限、上下游、状态码、禁止事项。
- p03_wallet_entity_context.md：写成 HER 执行前必须读取的 P03 上下文。
- p03_input_contract.yaml：定义 P03 必须读取的 P02 handoff、wallet_fact_seed、holder_snapshot、transaction_fact_seed、field usage permission、limitation tags。
- p03_output_contract.yaml：定义 wallet entity、funding links、group candidates、role candidates、quality、P04 request、handoff 输出。
- wallet_address_record_schema.yaml：定义单地址基础记录。
- wallet_entity_master_record_schema.yaml：定义钱包实体主记录。
- wallet_entity_resolution_record_schema.yaml：定义地址归并和实体解析。
- funding_source_link_record_schema.yaml：定义资金来源链路。
- funding_flow_edge_record_schema.yaml：定义资金流边。
- wallet_token_behavior_record_schema.yaml：定义当前 token 行为特征。
- wallet_position_fact_record_schema.yaml：定义当前持仓、买卖、清仓事实。
- wallet_temporal_behavior_record_schema.yaml：定义时间行为特征。
- wallet_amount_pattern_record_schema.yaml：定义金额模式特征。
- same_source_group_candidate_schema.yaml：定义疑似同源组候选。
- sync_behavior_group_candidate_schema.yaml：定义同步行为组候选。
- distribution_receiver_candidate_schema.yaml：定义分发接收候选。
- profit_collection_candidate_schema.yaml：定义利润归集候选。
- counterparty_wallet_candidate_schema.yaml：定义对手盘 / 接盘钱包候选。
- wallet_role_candidate_schema.yaml：定义钱包角色候选。
- wallet_history_seed_schema.yaml：定义历史地址辅助种子。
- wallet_entity_quality_record_schema.yaml：定义实体归并和角色候选质量评分。
- wallet_role_taxonomy.yaml：定义 P03 允许使用的钱包角色候选分类。
- entity_resolution_policy.yaml：定义地址归并规则，不允许静默合并。
- same_source_scoring_policy.yaml：定义同源候选评分规则。
- sync_behavior_scoring_policy.yaml：定义同步行为评分规则。
- wallet_role_scoring_policy.yaml：定义角色候选评分规则。
- wallet_entity_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- wallet_entity_hard_negative_rules.yaml：定义无 P02 handoff、无 wallet seed、无 trace、确认庄家、输出筹码控制、输出策略、自动实盘等阻断规则。
- wallet_entity_state_machine.yaml：定义 P03 全状态机。
- wallet_entity_trace_requirements.yaml：定义 wallet address trace、entity trace、funding link trace、group trace、role candidate trace、handoff trace。
- p04_chip_structure_data_request_packet_contract.yaml：定义 P03 给 P04 的筹码结构数据请求包。
- p03_to_p04_handoff_contract.yaml：定义 P03_TO_P04 handoff packet。
- p03_acceptance_criteria.md：定义 P03_READY、P03_READY_WITH_GAPS、P03_REJECTED、P03_BLOCKED。
- p03_storage_constitution.md：定义系统文件与运行数据目录。
- p03_test_matrix.yaml：定义至少 12 个测试场景。
- p03_report_model.yaml：定义 P03 人类可读报告。
- p03_review_checklist.md：定义审计清单。
- her_p03_execution_protocol.md：定义 HER 执行 P03 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P03_READY / P03_READY_WITH_GAPS / P03_REJECTED / P03_BLOCKED 判断
4. wallet_address_record 摘要
5. wallet_entity_master_record 摘要
6. wallet_entity_resolution_record 摘要
7. funding_source_link_record 摘要
8. wallet_token_behavior_record 摘要
9. same_source_group_candidate 摘要
10. sync_behavior_group_candidate 摘要
11. wallet_role_candidate 摘要
12. wallet_entity_quality_record 摘要
13. p04_chip_structure_data_request_packet 摘要
14. p03_to_p04_handoff_packet 摘要
15. P03 阻断规则摘要
16. P03 测试矩阵摘要
17. 当前缺口清单
18. 是否达到轻量机构级 P03 v3.0

最终验收标准：
只有当 P03 具备 wallet address record、wallet entity master、entity resolution、funding links、funding flow edges、token behavior、position facts、temporal behavior、amount pattern、same-source candidates、sync behavior candidates、distribution receiver candidates、profit collection candidates、counterparty wallet candidates、wallet role candidates、wallet history seed、entity quality、gap policy、hard negative rules、state machine、trace requirements、P04 data request、P03 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P03 不能确认庄家、不能判断筹码控制、不能生成证据、不能识别场景、不能输出策略、不能进入 paper runtime 或 live execution 时，才允许标记为 P03_READY。
```

---

# 33. 当前是否达到专业化标准

## 判断

这一版 P03 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是钱包分类脚本
```

P03 被明确升级为：

```text
钱包实体主数据层
地址归并与关系候选层
资金路径建模层
当前 token 行为特征层
角色候选初判层
P04 筹码结构分析输入层
```

---

# 34. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Wallet Address Record|已补齐|
|Wallet Entity Master Record|已补齐|
|Entity Resolution|已补齐|
|Funding Source Link|已补齐|
|Funding Flow Edge|已补齐|
|Wallet Token Behavior|已补齐|
|Wallet Position Fact|已补齐|
|Temporal Behavior|已补齐|
|Amount Pattern|已补齐|
|Same Source Group Candidate|已补齐|
|Sync Behavior Group Candidate|已补齐|
|Distribution Receiver Candidate|已补齐|
|Profit Collection Candidate|已补齐|
|Counterparty Wallet Candidate|已补齐|
|Wallet Role Candidate|已补齐|
|Wallet History Seed|已补齐|
|Entity Quality|已补齐|
|P04 Data Request|已补齐|
|P03 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 35. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|实体归并阈值未回测|已定义策略|P09 / P10 校准|
|同源评分权重未校准|已定义模型|需要样本回放|
|历史地址库可能缺失|已定义为辅助种子|后续 Review 积累|
|funding source 可能缺失|已定义 gap|P04 弱使用或观察|
|P03 不能判断筹码控制|已明确边界|P04 处理|
|P03 不能生成证据|已明确边界|P05 处理|
|P03 handoff 未联调|需要 P04|下一阶段展开 P04|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P03 的本质不是钱包分类，而是钱包实体主数据治理。**
    
2. **地址不等于实体。**  
    必须先做 wallet_address → wallet_entity → group_candidate 的分层建模。
    
3. **同源候选不是确认同源。**  
    P03 只能输出 same_source_group_candidate，不能输出 confirmed same source。
    
4. **角色候选不是筹码结论。**  
    早期执行钱包候选、接盘钱包候选、利润归集候选，只是 P04 的输入。
    
5. **P03 必须输出 P04 Chip Structure Data Request Packet。**  
    这是专业系统阶段交接的关键。
    
6. **P03 的核心价值是让 P04 可以计算筹码结构，而不是自己判断筹码控制。**
    
7. **P03 可以 READY_WITH_GAPS。**  
    funding source、历史地址、完整交易记录缺失时，可以弱交接给 P04，但必须传递限制。
    
8. **P03 只能交接给 P04。**  
    任何跳过 P04-P06 直接进入策略或 runtime 的路径都必须阻断。