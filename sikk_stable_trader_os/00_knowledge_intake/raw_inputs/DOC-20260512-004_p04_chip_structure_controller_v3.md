# P04 Chip Structure Controller 专业版 v3.0

## 筹码结构、持仓留存、迁移路径、派发进度与对手盘压力控制器

---

## 0. 先修正 P04 的定位

P04 不能被设计成普通的：

```text
筹码集中度计算脚本
早期钱包剩余持仓统计
庄家是否出货判断器
```

P04 的专业定位应该是：

```text
把 P03 交接过来的钱包实体、角色候选、同源组候选、同步行为组、资金边、当前持仓、买卖行为，转化为可追踪、可量化、可分层、可交接的筹码结构状态系统。
```

一句话定义：

> **P03 负责“钱包是谁、像什么角色候选、有哪些关系候选”。**  
> **P04 负责“这些钱包实体和群组当前控制了多少筹码、筹码是否还留在结构侧、是否发生迁移、是否出现派发、对手盘是否在承接”。**  
> **P05 才把这些结构状态转化为证据与反证。**

P04 不能直接输出：

```text
可以买
PAPER_READY
二段扩张成立
确认庄家
确认主控
确认市场意图
```

P04 只能输出：

```text
筹码结构状态
结构钱包留存状态
同源组持仓聚合
早期钱包剩余比例
筹码迁移状态候选
派发进度候选
对手盘压力状态候选
P05 evidence data request
P04 → P05 handoff
```

---

# 1. P04 阶段核心目标

P04 必须一次性解决 14 个问题：

|编号|核心问题|P04 必须输出|
|---|---|---|
|1|哪些钱包/群组属于可用于筹码结构计算的对象？|`chip_participant_universe_record`|
|2|早期钱包 cohort 如何定义？|`early_wallet_cohort_record`|
|3|结构钱包/同源组候选合计持仓多少？|`structural_group_holding_record`|
|4|早期钱包还剩多少筹码？|`early_wallet_retention_record`|
|5|钱包卖出、转出、清仓情况如何？|`chip_exit_flow_record`|
|6|筹码是否从结构侧迁移到接收侧/对手盘？|`chip_transfer_status_record`|
|7|是否存在派发进度候选？|`distribution_progress_record`|
|8|对手盘是否开始承接结构侧筹码？|`counterparty_pressure_record`|
|9|成本区域是否可估算？|`chip_cost_basis_record`|
|10|筹码集中度、分散度、留存度如何？|`chip_concentration_record`|
|11|当前筹码状态是否支持后续证据生成？|`chip_structure_quality_record`|
|12|哪些字段缺失、冲突、只能弱使用？|`p04_gap_report`|
|13|P05 应该如何转化证据？|`p05_evidence_data_request_packet`|
|14|是否可以交接给 P05？|`p04_to_p05_handoff_packet`|

---

# 2. P04 的专业角色模型

P04 应按 8 个角色设计：

|角色|负责问题|输出|
|---|---|---|
|筹码会计官|买入、卖出、剩余、转出如何核算|`chip_accounting_record`|
|cohort 分析官|哪些钱包属于早期/结构/对手盘 cohort|`cohort_definition_record`|
|群组持仓聚合官|同源组、同步组、角色候选如何聚合|`structural_group_holding_record`|
|迁移路径分析官|筹码是否从结构侧流向接收侧|`chip_transfer_status_record`|
|派发进度分析官|部分卖出、清仓、转出、接盘是否构成派发候选|`distribution_progress_record`|
|对手盘压力分析官|后来买入/承接/鲸鱼接盘压力如何|`counterparty_pressure_record`|
|不确定性与缺口官|哪些数据不足、哪些只能弱结论|`chip_structure_quality_record`|
|下游交接官|P05 应如何生成证据和反证|`p05_evidence_data_request_packet`|

---

# 3. P04 底层方法论

## 3.1 筹码守恒原则

P04 的基础不是“猜庄”，而是做筹码会计：

```text
买入筹码
  - 卖出筹码
  - 转出筹码
  + 转入筹码
  = 当前可解释持仓
```

如果账算不平，不能强行判断结构。

必须输出：

```text
accounting_matched
accounting_gap
unexplained_flow
unknown_transfer_target
```

---

## 3.2 cohort 分层原则

P04 不能把所有钱包混在一起算。

必须至少区分：

```text
早期钱包 cohort
结构钱包候选 cohort
同源执行组 cohort
同步行为组 cohort
分发接收候选 cohort
利润归集候选 cohort
对手盘/接盘候选 cohort
普通散户/未知 cohort
```

不同 cohort 的持仓、卖出、转出意义不同。

---

## 3.3 候选结构，不是确定主控原则

P04 可以输出：

```text
structural_side_candidate
chip_retention_status_candidate
distribution_progress_candidate
counterparty_pressure_status
```

不能输出：

```text
确认庄家
确认主控
确认操盘意图
确认二段扩张
确认可以买
```

---

## 3.4 时间分段原则

筹码结构必须结合时间：

```text
开盘初期
发现时
P02 数据采集时
P03 钱包实体建立时
P04 筹码计算时
后续 refresh 时
```

不能用当前持仓倒推过去状态。

---

## 3.5 盘型兼容原则

P04 必须避免把所有卖出都判成派发。

例如：

```text
长横盘 / 控盘箱体 / 二段扩张前
```

部分早期钱包卖出可能是：

```text
正常轮换
风险释放
分仓转移
换手吸收
```

而不是立即派发完成。

因此 P04 输出必须携带：

```text
pattern_context_required: true
scenario_confirmation_required_by_P06: true
```

---

# 4. P04 必须建立的核心对象

|对象|作用|
|---|---|
|`P04 Input Manifest`|从 P03 接收哪些钱包实体和角色候选|
|`Chip Participant Universe Record`|可参与筹码计算的钱包/实体/组范围|
|`Cohort Definition Record`|早期、结构、接收、对手盘等 cohort 定义|
|`Supply Denominator Record`|使用哪个供应量作为分母|
|`Chip Accounting Record`|买入/卖出/转入/转出/当前持仓核算|
|`Early Wallet Cohort Record`|早期钱包 cohort|
|`Early Wallet Retention Record`|早期钱包剩余筹码|
|`Structural Group Holding Record`|结构组聚合持仓|
|`Same Source Group Holding Record`|同源组持仓聚合|
|`Sync Group Holding Record`|同步组持仓聚合|
|`Chip Concentration Record`|筹码集中度|
|`Chip Exit Flow Record`|卖出、清仓、转出流|
|`Chip Transfer Status Record`|筹码迁移状态|
|`Distribution Progress Record`|派发进度候选|
|`Counterparty Pressure Record`|对手盘压力|
|`Chip Cost Basis Record`|成本区域估算|
|`Chip Structure Score Record`|多维结构评分|
|`Chip Structure Quality Record`|数据质量与下游权限|
|`P05 Evidence Data Request Packet`|给 P05 的证据请求包|
|`P04 to P05 Handoff Packet`|P04 → P05 交接包|

---

# 5. P04 输入：必须读取什么

```yaml
p04_required_inputs:
  from_p03:
    - p03_to_p04_handoff_packet
    - p04_chip_structure_data_request_packet
    - wallet_entity_master_records
    - wallet_position_fact_records
    - wallet_token_behavior_records
    - wallet_temporal_behavior_records
    - wallet_amount_pattern_records
    - same_source_group_candidates
    - sync_behavior_group_candidates
    - distribution_receiver_candidates
    - profit_collection_candidates
    - counterparty_wallet_candidates
    - wallet_role_candidate_records
    - funding_flow_edges
    - wallet_entity_quality_report

  from_p02:
    - market_fact_record
    - holder_snapshot_fact
    - transaction_fact_seed
    - market_structure_fact_seed
    - data_quality_report
    - field_usage_permission_packet

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - limitation_transfer_packet
    - forbidden_use_policy
    - governance_handoff_packet
    - domain_chip_structure_model_handoff

  required_contracts:
    - p04_input_contract
    - p04_output_contract
    - chip_structure_schema_contract
    - chip_accounting_contract
    - p05_evidence_input_contract
```

P04 启动前必须确认：

```text
P03 已验收
P03 handoff 已生成
P04 只读取 handoff 授权字段
P03 的角色输出仍是 candidate，不是 confirmed
P04 不允许把 wallet_role_candidate 当成确认主控
P04 不允许进入 paper runtime
P04 不允许 live execution
```

---

# 6. Chip Participant Universe Record

P04 首先要定义哪些对象纳入筹码计算。

```yaml
chip_participant_universe_record:
  universe_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  included_wallet_entities:
    - wallet_entity_id: string
      wallet_addresses: list
      inclusion_reason:
        - EARLY_ENTRY
        - SAME_SOURCE_GROUP_CANDIDATE
        - SYNC_BEHAVIOR_GROUP_CANDIDATE
        - ACCUMULATION_ROLE_CANDIDATE
        - DISTRIBUTION_RECEIVER_CANDIDATE
        - COUNTERPARTY_CANDIDATE
        - TOP_HOLDER
        - UNKNOWN_BUT_MATERIAL_HOLDER
      usage_permission:
        - FULL_USE
        - WEAK_USE_ONLY
        - OBSERVE_ONLY
        - DO_NOT_USE

  excluded_wallet_entities:
    - wallet_entity_id: string
      exclusion_reason:
        - LOW_CONFIDENCE_ENTITY
        - STALE_WALLET_DATA
        - UNTRACEABLE_ADDRESS
        - DUPLICATE_ENTITY
        - INSUFFICIENT_POSITION_DATA

  universe_quality:
    entity_coverage_score: number
    holding_coverage_pct: number | null
    transaction_coverage_score: number
    universe_quality_status:
      - UNIVERSE_HIGH_CONFIDENCE
      - UNIVERSE_USABLE
      - UNIVERSE_USABLE_WITH_GAPS
      - UNIVERSE_LOW_CONFIDENCE
      - UNIVERSE_UNUSABLE

  trace:
    universe_trace_id: string
    source_wallet_entity_trace_ids: list
```

---

# 7. Supply Denominator Record

筹码比例必须先定义分母，否则所有百分比都不可信。

```yaml
supply_denominator_record:
  denominator_id: string
  candidate_id: string
  token_address: string

  supply_sources:
    total_supply:
      value: number | null
      source_id: string | null
      freshness_status: string
    circulating_supply:
      value: number | null
      source_id: string | null
      freshness_status: string
    holder_snapshot_supply:
      value: number | null
      source_id: string | null
      freshness_status: string

  selected_denominator:
    denominator_type:
      - TOTAL_SUPPLY
      - CIRCULATING_SUPPLY
      - HOLDER_SNAPSHOT_SUPPLY
      - UNKNOWN
    selected_value: number | null
    selection_reason: string
    confidence: number

  limitations:
    - SUPPLY_CONFLICT
    - SUPPLY_STALE
    - CIRCULATING_SUPPLY_UNKNOWN
    - USE_PERCENTAGES_WEAKLY

  downstream_permission:
    percentage_metrics_allowed: boolean
    percentage_metrics_usage:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
```

---

# 8. Chip Accounting Record

筹码会计是 P04 的底座。

```yaml
chip_accounting_record:
  accounting_id: string
  candidate_id: string
  wallet_entity_id: string
  token_address: string

  accounting_window:
    start_time: datetime | null
    end_time: datetime | null
    source_snapshot_time: datetime

  inflows:
    buy_amount_token: number | null
    transfer_in_amount_token: number | null
    other_in_amount_token: number | null

  outflows:
    sell_amount_token: number | null
    transfer_out_amount_token: number | null
    other_out_amount_token: number | null

  current_position:
    current_holding_token: number | null
    current_holding_pct_supply: number | null
    current_holding_value_usd: number | null

  accounting_check:
    expected_holding_token: number | null
    observed_holding_token: number | null
    accounting_difference_token: number | null
    accounting_difference_pct: number | null
    accounting_status:
      - ACCOUNTING_MATCHED
      - ACCOUNTING_MINOR_GAP
      - ACCOUNTING_MAJOR_GAP
      - ACCOUNTING_UNUSABLE

  explanation:
    unexplained_transfer_amount_token: number | null
    missing_transaction_rows: boolean
    stale_holder_snapshot: boolean
    known_limitations: list

  trace:
    accounting_trace_id: string
    transaction_trace_ids: list
    wallet_position_trace_ids: list
```

---

# 9. Cohort Definition Record

P04 的所有统计都必须基于 cohort。

```yaml
cohort_definition_record:
  cohort_id: string
  candidate_id: string

  cohort_type:
    - EARLY_WALLET_COHORT
    - STRUCTURAL_WALLET_COHORT
    - SAME_SOURCE_GROUP_COHORT
    - SYNC_BUY_GROUP_COHORT
    - SYNC_SELL_GROUP_COHORT
    - DISTRIBUTION_RECEIVER_COHORT
    - COUNTERPARTY_COHORT
    - UNKNOWN_MATERIAL_HOLDER_COHORT

  inclusion_rules:
    - rule_id: string
      rule_name: string
      source_fields: list
      threshold: object
      reason: string

  members:
    wallet_entity_ids: list
    wallet_addresses: list
    group_ids: list
    member_count: integer

  cohort_metrics:
    total_current_holding_token: number | null
    total_current_holding_pct_supply: number | null
    total_bought_token: number | null
    total_sold_token: number | null
    total_transfer_out_token: number | null
    remaining_ratio_pct: number | null

  quality:
    cohort_confidence: number
    cohort_quality_status:
      - COHORT_HIGH_CONFIDENCE
      - COHORT_USABLE
      - COHORT_USABLE_WITH_GAPS
      - COHORT_LOW_CONFIDENCE
      - COHORT_UNUSABLE
```

---

# 10. Early Wallet Cohort Record

早期钱包必须清楚定义，不能凭感觉。

```yaml
early_wallet_cohort_record:
  early_cohort_id: string
  candidate_id: string
  token_address: string

  early_definition:
    definition_mode:
      - FIRST_N_BUYERS
      - FIRST_X_MINUTES
      - PRE_DISCOVERY_BUYERS
      - BELOW_MARKET_CAP_THRESHOLD
      - HYBRID
    parameters:
      first_n_buyers: integer | null
      time_window_seconds: integer | null
      market_cap_threshold_usd: number | null

  members:
    wallet_entity_ids: list
    wallet_addresses: list
    member_count: integer

  early_entry_metrics:
    earliest_buy_time: datetime | null
    latest_buy_time_in_cohort: datetime | null
    total_early_buy_token: number | null
    total_early_buy_usd: number | null
    average_entry_market_cap_usd: number | null

  quality:
    early_cohort_quality_status:
      - EARLY_COHORT_HIGH_CONFIDENCE
      - EARLY_COHORT_USABLE
      - EARLY_COHORT_WITH_GAPS
      - EARLY_COHORT_LOW_CONFIDENCE
      - EARLY_COHORT_UNUSABLE
    missing_fields: list
```

---

# 11. Early Wallet Retention Record

这是 P04 的关键输出之一。

```yaml
early_wallet_retention_record:
  retention_id: string
  candidate_id: string
  early_cohort_id: string

  aggregate_retention:
    total_early_bought_token: number | null
    total_current_holding_token: number | null
    total_sold_token: number | null
    total_transfer_out_token: number | null
    early_wallet_remaining_pct_of_bought: number | null
    early_wallet_remaining_pct_of_supply: number | null

  member_retention_distribution:
    full_holders_count: integer
    partial_sellers_count: integer
    full_exit_count: integer
    transferred_out_count: integer
    unknown_status_count: integer

  retention_status:
    - EARLY_CHIP_RETAINED_STRONG
    - EARLY_CHIP_RETAINED_MODERATE
    - EARLY_CHIP_PARTIALLY_DISTRIBUTED
    - EARLY_CHIP_MOSTLY_EXITED
    - EARLY_CHIP_UNKNOWN

  interpretation_limit:
    not_evidence_by_itself: true
    requires_p05_evidence_conversion: true
    requires_p06_scenario_context: true

  quality:
    retention_quality_score: number
    retention_quality_status:
      - RETENTION_HIGH_CONFIDENCE
      - RETENTION_USABLE
      - RETENTION_USABLE_WITH_GAPS
      - RETENTION_LOW_CONFIDENCE
      - RETENTION_UNUSABLE
```

---

# 12. Structural Group Holding Record

同源组/同步组/角色候选需要聚合持仓，但必须保留不确定性。

```yaml
structural_group_holding_record:
  structural_holding_id: string
  candidate_id: string

  structural_group_scope:
    included_group_ids: list
    included_wallet_entity_ids: list
    group_basis:
      - SAME_SOURCE_GROUP_CANDIDATE
      - SYNC_BEHAVIOR_GROUP_CANDIDATE
      - EARLY_EXECUTION_ROLE_CANDIDATE
      - ACCUMULATION_ROLE_CANDIDATE
      - HYBRID_STRUCTURAL_CANDIDATE

  holding_metrics:
    total_group_current_holding_token: number | null
    total_group_current_holding_pct_supply: number | null
    total_group_bought_token: number | null
    total_group_sold_token: number | null
    total_group_transfer_out_token: number | null
    group_remaining_ratio_pct: number | null

  distribution_metrics:
    group_partial_seller_count: integer
    group_full_exit_count: integer
    group_holding_count: integer
    group_transfer_out_count: integer

  confidence:
    structural_group_confidence: number
    group_membership_quality: string
    holding_quality: string

  downstream_limit:
    group_is_candidate_not_confirmed_controller: true
    p05_must_convert_to_evidence: true
```

---

# 13. Chip Concentration Record

```yaml
chip_concentration_record:
  concentration_id: string
  candidate_id: string
  token_address: string

  concentration_metrics:
    top_1_holder_pct: number | null
    top_5_holder_pct: number | null
    top_10_holder_pct: number | null
    top_20_holder_pct: number | null
    structural_group_holding_pct: number | null
    early_wallet_holding_pct: number | null
    unknown_large_holder_pct: number | null

  concentration_scores:
    raw_concentration_score: number
    structural_adjusted_concentration_score: number
    unknown_holder_risk_score: number

  concentration_status:
    - STRUCTURALLY_CONCENTRATED
    - MODERATELY_CONCENTRATED
    - DISPERSED
    - UNKNOWN_DUE_TO_DATA_GAPS

  caveats:
    same_source_uncertainty: boolean
    holder_snapshot_stale: boolean
    supply_denominator_uncertain: boolean
```

---

# 14. Chip Exit Flow Record

卖出、清仓、转出必须拆开。

```yaml
chip_exit_flow_record:
  exit_flow_id: string
  candidate_id: string

  cohort_scope:
    cohort_id: string
    cohort_type: string

  sell_flow:
    total_sell_token: number | null
    total_sell_usd: number | null
    sell_ratio_of_bought_pct: number | null
    sell_wallet_count: integer
    full_exit_wallet_count: integer
    partial_sell_wallet_count: integer

  transfer_out_flow:
    total_transfer_out_token: number | null
    transfer_out_ratio_pct: number | null
    known_receiver_count: integer
    unknown_receiver_count: integer

  timing:
    first_exit_time: datetime | null
    latest_exit_time: datetime | null
    exit_cluster_detected: boolean
    exit_cluster_window_seconds: integer | null

  exit_flow_status:
    - LOW_EXIT_FLOW
    - MODERATE_PARTIAL_EXIT
    - HIGH_EXIT_FLOW
    - SYNCHRONIZED_EXIT_CANDIDATE
    - UNKNOWN_EXIT_FLOW

  downstream_note:
    sell_flow_not_equal_distribution_alone: true
    transfer_out_requires_receiver_analysis: true
```

---

# 15. Chip Transfer Status Record

筹码迁移是 P04 的重点。

```yaml
chip_transfer_status_record:
  transfer_status_id: string
  candidate_id: string

  transfer_scope:
    from_cohort:
      - EARLY_WALLET_COHORT
      - STRUCTURAL_WALLET_COHORT
      - SAME_SOURCE_GROUP_COHORT
      - UNKNOWN
    to_cohort:
      - DISTRIBUTION_RECEIVER_COHORT
      - COUNTERPARTY_COHORT
      - UNKNOWN_WALLETS
      - EXCHANGE_LIKE
      - UNKNOWN

  transfer_metrics:
    total_transferred_token: number | null
    transferred_pct_of_structural_bought: number | null
    transferred_pct_of_supply: number | null
    known_receiver_pct: number | null
    unknown_receiver_pct: number | null

  receiver_analysis:
    receiver_wallet_count: integer
    receiver_quick_sell_count: integer
    receiver_holding_count: integer
    receiver_unknown_count: integer

  transfer_status:
    - NO_MATERIAL_TRANSFER
    - INTERNAL_ROTATION_CANDIDATE
    - STRUCTURE_TO_RECEIVER_TRANSFER_CANDIDATE
    - STRUCTURE_TO_COUNTERPARTY_TRANSFER_CANDIDATE
    - UNEXPLAINED_TRANSFER_RISK
    - TRANSFER_STATUS_UNKNOWN

  quality:
    transfer_path_quality: string
    missing_receiver_data: boolean
    traceability_score: number
```

---

# 16. Distribution Progress Record

P04 可以输出“派发进度候选”，不能输出“确认派发完成”。

```yaml
distribution_progress_record:
  distribution_id: string
  candidate_id: string

  distribution_inputs:
    early_wallet_retention_id: string
    structural_group_holding_id: string
    chip_exit_flow_ids: list
    chip_transfer_status_ids: list
    counterparty_pressure_id: string | null

  distribution_metrics:
    early_wallet_exit_ratio_pct: number | null
    structural_group_exit_ratio_pct: number | null
    synchronized_exit_score: number | null
    receiver_sell_through_score: number | null
    unknown_transfer_risk_score: number | null

  distribution_stage_candidate:
    - NO_CLEAR_DISTRIBUTION
    - PARTIAL_DISTRIBUTION_CANDIDATE
    - ACTIVE_DISTRIBUTION_CANDIDATE
    - LATE_DISTRIBUTION_CANDIDATE
    - DISTRIBUTION_UNCLEAR_DUE_TO_GAPS

  counter_interpretation:
    possible_rotation: boolean
    possible_reaccumulation: boolean
    possible_internal_transfer: boolean
    requires_market_structure_context: true

  quality:
    distribution_progress_confidence: number
    distribution_quality_status:
      - DISTRIBUTION_HIGH_CONFIDENCE_CANDIDATE
      - DISTRIBUTION_USABLE_CANDIDATE
      - DISTRIBUTION_WITH_GAPS
      - DISTRIBUTION_LOW_CONFIDENCE
      - DISTRIBUTION_UNUSABLE
```

---

# 17. Counterparty Pressure Record

对手盘压力是 P04 可以计算的重要结构状态，但不能直接作为策略结论。

```yaml
counterparty_pressure_record:
  pressure_id: string
  candidate_id: string

  counterparty_scope:
    counterparty_wallet_candidate_ids: list
    late_buyer_wallet_ids: list
    receiver_wallet_ids: list

  pressure_metrics:
    late_buyer_holding_pct: number | null
    counterparty_whale_holding_pct: number | null
    late_buy_volume_usd: number | null
    structural_sell_to_counterparty_overlap_score: number | null
    unrealized_loss_risk_score: number | null

  pressure_status:
    - LOW_COUNTERPARTY_PRESSURE
    - MODERATE_COUNTERPARTY_PRESSURE
    - HIGH_COUNTERPARTY_PRESSURE
    - EXIT_LIQUIDITY_RISK_CANDIDATE
    - COUNTERPARTY_PRESSURE_UNKNOWN

  interpretation_limit:
    not_strategy_block_alone: true
    p05_must_convert_to_counter_evidence: true
    p07_strategy_gate_must_decide: true

  quality:
    pressure_quality_score: number
    missing_counterparty_fields: list
```

---

# 18. Chip Cost Basis Record

成本区域估算要明确来源和不确定性。

```yaml
chip_cost_basis_record:
  cost_basis_id: string
  candidate_id: string

  cost_basis_scope:
    cohort_id: string
    cohort_type:
      - EARLY_WALLET_COHORT
      - STRUCTURAL_GROUP_COHORT
      - SAME_SOURCE_GROUP_COHORT
      - ALL_TRACKED_WALLETS

  cost_estimates:
    weighted_average_entry_price_usd: number | null
    weighted_average_entry_market_cap_usd: number | null
    median_entry_price_usd: number | null
    median_entry_market_cap_usd: number | null
    estimated_cost_range_low_usd: number | null
    estimated_cost_range_high_usd: number | null

  current_context:
    current_price_usd: number | null
    current_market_cap_usd: number | null
    unrealized_multiple_from_cost: number | null
    distance_to_cost_pct: number | null

  quality:
    cost_basis_quality:
      - COST_BASIS_HIGH_CONFIDENCE
      - COST_BASIS_USABLE
      - COST_BASIS_WITH_GAPS
      - COST_BASIS_LOW_CONFIDENCE
      - COST_BASIS_UNUSABLE
    limitations:
      - ENTRY_PRICE_MISSING
      - MARKET_CAP_MISSING
      - PARTIAL_TRANSACTION_HISTORY
      - TRANSFER_IN_COST_UNKNOWN
```

---

# 19. Chip Structure Score Record

P04 不能输出单一总分，应输出多维结构评分。

```yaml
chip_structure_score_record:
  score_id: string
  candidate_id: string

  score_dimensions:
    chip_retention_score: number
    structural_group_holding_score: number
    concentration_score: number
    exit_flow_risk_score: number
    transfer_risk_score: number
    distribution_progress_score: number
    counterparty_pressure_score: number
    cost_basis_quality_score: number
    data_quality_penalty: number

  status_outputs:
    chip_retention_status: string
    structural_group_status: string
    transfer_status: string
    distribution_status_candidate: string
    counterparty_pressure_status: string

  no_single_total_score_policy:
    enabled: true
    reason: 筹码结构用于多维判断，不允许用一个总分掩盖风险差异

  downstream:
    p05_should_generate_supporting_evidence_from: list
    p05_should_generate_counter_evidence_from: list
    p05_should_mark_unknown_from: list
```

---

# 20. Chip Structure Quality Record

```yaml
chip_structure_quality_record:
  candidate_id: string
  generated_at: datetime

  quality_dimensions:
    wallet_entity_input_quality_score: number
    holder_snapshot_freshness_score: number
    transaction_coverage_score: number
    supply_denominator_quality_score: number
    group_membership_confidence_score: number
    transfer_path_traceability_score: number
    cost_basis_quality_score: number
    accounting_consistency_score: number

  weighted_quality_score: number

  quality_status:
    - CHIP_STRUCTURE_HIGH_CONFIDENCE
    - CHIP_STRUCTURE_USABLE
    - CHIP_STRUCTURE_USABLE_WITH_GAPS
    - CHIP_STRUCTURE_LOW_CONFIDENCE
    - CHIP_STRUCTURE_UNUSABLE

  downstream_permission:
    p05_evidence_allowed: boolean
    p05_usage_mode:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - BLOCKED
    p06_scenario_allowed: false
    p07_strategy_gate_allowed: false
    paper_runtime_allowed: false

  limitations:
    - HOLDER_SNAPSHOT_STALE
    - TRANSACTION_HISTORY_PARTIAL
    - SUPPLY_DENOMINATOR_UNCERTAIN
    - SAME_SOURCE_GROUP_WEAK
    - TRANSFER_PATH_UNKNOWN
    - COST_BASIS_UNCERTAIN
```

---

# 21. P04 Gap Policy

```yaml
p04_gap_policy:
  BLOCKING_GAP:
    result: P04_BLOCKED
    examples:
      - p03_handoff_missing
      - no_wallet_entity_inputs
      - no_trace
      - live_execution_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P04_REJECTED
    examples:
      - no_wallet_position_facts
      - supply_denominator_unavailable
      - all_holder_snapshots_unusable
      - output_contract_missing

  HIGH_GAP:
    result: P04_READY_WITH_GAPS
    downstream_permission: P05_LIMITED
    examples:
      - transaction_history_partial
      - same_source_group_low_confidence
      - transfer_receiver_unknown
      - accounting_major_gap
      - cost_basis_unusable

  MEDIUM_GAP:
    result: P04_READY_WITH_GAPS
    downstream_permission: P05_ALLOWED_WITH_LIMITATIONS
    examples:
      - holder_snapshot_stale
      - partial_funding_edges
      - market_cap_at_entry_missing
      - counterparty_candidate_weak

  LOW_GAP:
    result: P04_READY_WITH_GAPS
    downstream_permission: P05_ALLOWED_WITH_NOTE
    examples:
      - optional_historical_wallet_tags_missing
      - minor_accounting_gap
      - noncritical_group_metadata_missing
```

---

# 22. P04 Hard Negative Rules

```yaml
p04_hard_negative_rules:
  - rule_id: P04_BLOCK_001
    name: 未读取 P03 handoff
    condition: p03_to_p04_handoff_packet_missing == true
    result: P04_BLOCKED
    reason: P04 不能绕过 P03 / Handoff 启动

  - rule_id: P04_BLOCK_002
    name: 无钱包实体输入
    condition: wallet_entity_master_records_missing == true
    result: P04_REJECTED
    reason: 无钱包实体，无法计算筹码结构

  - rule_id: P04_BLOCK_003
    name: 无持仓事实
    condition: wallet_position_fact_records_missing == true
    result: P04_REJECTED
    reason: 无持仓事实，无法做筹码会计

  - rule_id: P04_BLOCK_004
    name: 无供应量分母
    condition: supply_denominator_unavailable == true
    result: P04_REJECTED
    reason: 无法计算持仓比例

  - rule_id: P04_BLOCK_005
    name: 静默聚合弱同源组
    condition: weak_same_source_group_used_as_full_use == true
    result: P04_BLOCKED
    reason: 弱同源组不能被当作强结构组聚合

  - rule_id: P04_BLOCK_006
    name: 输出确认庄家或主控
    condition: output_contains in [confirmed_market_maker, confirmed_dominant_side]
    result: P04_BLOCKED
    reason: P04 只能输出筹码结构状态候选

  - rule_id: P04_BLOCK_007
    name: 输出策略或纸面准入
    condition: output_contains in [buy_signal, strategy_signal, paper_ready]
    result: P04_BLOCKED
    reason: P04 越权

  - rule_id: P04_BLOCK_008
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P04_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 23. P04 状态机专业版

```yaml
p04_chip_structure_state_machine:
  states:
    - P04_UNINITIALIZED
    - P04_CONTEXT_LOADED
    - P04_HANDOFF_READ
    - P04_INPUT_MANIFEST_BUILT
    - P04_PARTICIPANT_UNIVERSE_BUILT
    - P04_SUPPLY_DENOMINATOR_SELECTED
    - P04_CHIP_ACCOUNTING_RUNNING
    - P04_CHIP_ACCOUNTING_BUILT
    - P04_COHORTS_DEFINED
    - P04_EARLY_WALLET_RETENTION_BUILT
    - P04_STRUCTURAL_GROUP_HOLDING_BUILT
    - P04_CONCENTRATION_BUILT
    - P04_EXIT_FLOW_BUILT
    - P04_TRANSFER_STATUS_BUILT
    - P04_DISTRIBUTION_PROGRESS_BUILT
    - P04_COUNTERPARTY_PRESSURE_BUILT
    - P04_COST_BASIS_BUILT
    - P04_STRUCTURE_SCORES_BUILT
    - P04_QUALITY_SCORED
    - P04_GAP_ANALYZED
    - P04_P05_DATA_REQUEST_BUILT
    - P04_READY_FOR_ACCEPTANCE
    - P04_ACCEPTANCE_READY
    - P04_READY_FOR_P05_HANDOFF
    - P04_READY_WITH_GAPS
    - P04_REJECTED
    - P04_BLOCKED

  critical_transitions:
    - from: P04_HANDOFF_READ
      to: P04_INPUT_MANIFEST_BUILT
      condition: p03_handoff_valid == true

    - from: P04_INPUT_MANIFEST_BUILT
      to: P04_PARTICIPANT_UNIVERSE_BUILT
      condition: wallet_entity_inputs_available == true

    - from: P04_PARTICIPANT_UNIVERSE_BUILT
      to: P04_SUPPLY_DENOMINATOR_SELECTED
      condition: supply_denominator_record_created == true

    - from: P04_SUPPLY_DENOMINATOR_SELECTED
      to: P04_CHIP_ACCOUNTING_RUNNING
      condition: wallet_position_facts_available == true

    - from: P04_CHIP_ACCOUNTING_RUNNING
      to: P04_CHIP_ACCOUNTING_BUILT
      condition: chip_accounting_records_created == true

    - from: P04_CHIP_ACCOUNTING_BUILT
      to: P04_COHORTS_DEFINED
      condition: cohort_definition_records_created == true

    - from: P04_COHORTS_DEFINED
      to: P04_EARLY_WALLET_RETENTION_BUILT
      condition: early_wallet_retention_record_created == true

    - from: P04_EARLY_WALLET_RETENTION_BUILT
      to: P04_STRUCTURAL_GROUP_HOLDING_BUILT
      condition: structural_group_holding_record_created == true

    - from: P04_STRUCTURAL_GROUP_HOLDING_BUILT
      to: P04_TRANSFER_STATUS_BUILT
      condition: chip_transfer_status_record_created == true

    - from: P04_TRANSFER_STATUS_BUILT
      to: P04_DISTRIBUTION_PROGRESS_BUILT
      condition: distribution_progress_record_created == true

    - from: P04_DISTRIBUTION_PROGRESS_BUILT
      to: P04_COUNTERPARTY_PRESSURE_BUILT
      condition: counterparty_pressure_record_created == true

    - from: P04_COUNTERPARTY_PRESSURE_BUILT
      to: P04_STRUCTURE_SCORES_BUILT
      condition: chip_structure_score_record_created == true

    - from: P04_STRUCTURE_SCORES_BUILT
      to: P04_QUALITY_SCORED
      condition: chip_structure_quality_record_created == true

    - from: P04_QUALITY_SCORED
      to: P04_P05_DATA_REQUEST_BUILT
      condition: p05_evidence_data_request_packet_created == true

    - from: P04_P05_DATA_REQUEST_BUILT
      to: P04_READY_FOR_ACCEPTANCE
      condition: p04_output_contract_ready == true

    - from: P04_READY_FOR_ACCEPTANCE
      to: P04_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P04_ACCEPTANCE_READY
      to: P04_READY_FOR_P05_HANDOFF
      condition: p04_to_p05_handoff_packet_created == true
```

---

# 24. P05 Evidence Data Request Packet

P04 必须告诉 P05：哪些结构状态可以转成支持证据，哪些必须转成反证，哪些只能 unknown。

```yaml
p05_evidence_data_request_packet:
  packet_id: string
  from_controller: P04_CHIP_STRUCTURE_CONTROLLER
  to_controller: P05_EVIDENCE_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  evidence_inputs_available:
    early_wallet_retention_records_path: string
    structural_group_holding_records_path: string
    chip_concentration_records_path: string
    chip_exit_flow_records_path: string
    chip_transfer_status_records_path: string
    distribution_progress_records_path: string
    counterparty_pressure_records_path: string
    chip_cost_basis_records_path: string
    chip_structure_score_records_path: string
    chip_structure_quality_records_path: string

  p05_required_evidence_tasks:
    supporting_evidence_candidates:
      - early_chip_retention_support
      - structural_group_holding_support
      - controlled_rotation_support
      - cost_basis_support_if_quality_high

    counter_evidence_candidates:
      - active_distribution_risk
      - early_wallet_full_exit_risk
      - structure_to_counterparty_transfer_risk
      - high_counterparty_pressure_risk
      - unexplained_transfer_risk

    unknown_or_weak_evidence_candidates:
      - weak_same_source_group
      - stale_holder_snapshot
      - uncertain_supply_denominator
      - cost_basis_low_confidence

  usage_limitations:
    - CHIP_STRUCTURE_STATUS_ONLY
    - NO_SCENARIO_CLAIM
    - NO_STRATEGY_GATE
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  field_usage_permissions:
    full_use_fields: list
    weak_use_only_fields: list
    observe_only_fields: list
    do_not_use_fields: list
```

---

# 25. P04 to P05 Handoff Packet

```yaml
p04_to_p05_handoff_packet:
  packet_id: string
  packet_type: P04_TO_P05_CHIP_STRUCTURE_HANDOFF
  generated_at: datetime

  route:
    from_controller: P04_CHIP_STRUCTURE_CONTROLLER
    to_controller: P05_EVIDENCE_CONTROLLER

  upstream_control:
    p03_handoff_packet_id: string
    p04_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    candidate_count_chip_structure_ready: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  chip_structure_package:
    participant_universe_records_path: string
    supply_denominator_records_path: string
    chip_accounting_records_path: string
    cohort_definition_records_path: string
    early_wallet_retention_records_path: string
    structural_group_holding_records_path: string
    chip_concentration_records_path: string
    chip_exit_flow_records_path: string
    chip_transfer_status_records_path: string
    distribution_progress_records_path: string
    counterparty_pressure_records_path: string
    chip_cost_basis_records_path: string
    chip_structure_score_records_path: string
    chip_structure_quality_records_path: string

  p05_data_request:
    p05_evidence_data_request_packet_path: string
    required_p05_tasks: list
    missing_inputs_by_candidate: object

  quality:
    chip_structure_quality_report_path: string
    accounting_quality_summary: object
    transfer_path_quality_summary: object
    distribution_progress_quality_summary: object
    counterparty_pressure_quality_summary: object

  limitations:
    - CHIP_STRUCTURE_STATUS_ONLY
    - NO_CONFIRMED_MARKET_MAKER
    - NO_CONFIRMED_DOMINANT_SIDE
    - NO_EVIDENCE_OBJECT_YET
    - NO_SCENARIO
    - NO_STRATEGY_GATE
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P05_EVIDENCE_CONTROLLER
    forbidden:
      - P06_SCENARIO_RECOGNITION_CONTROLLER
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p05_must_read_first:
      - p04_to_p05_handoff_packet
      - p05_evidence_data_request_packet
      - chip_structure_quality_records
      - early_wallet_retention_records
      - structural_group_holding_records
      - chip_transfer_status_records
      - distribution_progress_records
      - counterparty_pressure_records
      - field_usage_permissions
```

---

# 26. P04 文件体系

## 26.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p04_chip_structure_controller/
```

必须创建：

```text
p04_chip_structure_controller.yaml
p04_chip_structure_context.md
p04_input_contract.yaml
p04_output_contract.yaml
chip_participant_universe_schema.yaml
supply_denominator_schema.yaml
chip_accounting_record_schema.yaml
cohort_definition_schema.yaml
early_wallet_cohort_schema.yaml
early_wallet_retention_schema.yaml
structural_group_holding_schema.yaml
same_source_group_holding_schema.yaml
sync_group_holding_schema.yaml
chip_concentration_schema.yaml
chip_exit_flow_schema.yaml
chip_transfer_status_schema.yaml
distribution_progress_schema.yaml
counterparty_pressure_schema.yaml
chip_cost_basis_schema.yaml
chip_structure_score_schema.yaml
chip_structure_quality_schema.yaml
chip_accounting_policy.yaml
cohort_definition_policy.yaml
chip_retention_policy.yaml
distribution_progress_policy.yaml
counterparty_pressure_policy.yaml
cost_basis_policy.yaml
chip_structure_gap_policy.yaml
chip_structure_hard_negative_rules.yaml
chip_structure_state_machine.yaml
chip_structure_trace_requirements.yaml
p05_evidence_data_request_packet_contract.yaml
p04_to_p05_handoff_contract.yaml
p04_acceptance_criteria.md
p04_storage_constitution.md
p04_test_matrix.yaml
p04_report_model.yaml
p04_review_checklist.md
her_p04_execution_protocol.md
```

---

## 26.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p04_chip_structure/
  input_manifest/
  participant_universe/
  supply_denominator/
  chip_accounting/
  cohort_definitions/
  early_wallet_cohorts/
  early_wallet_retention/
  structural_group_holding/
  same_source_group_holding/
  sync_group_holding/
  concentration/
  exit_flow/
  transfer_status/
  distribution_progress/
  counterparty_pressure/
  cost_basis/
  structure_scores/
  quality/
  gaps/
  conflicts/
  p05_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 27. P04 测试矩阵

```yaml
p04_test_matrix:
  - test_id: P04_TEST_001
    name: 正常 P03 handoff，包含钱包实体、持仓、交易事实
    expected_status: P04_READY_FOR_P05_HANDOFF

  - test_id: P04_TEST_002
    name: 缺 P03 handoff
    expected_status: P04_BLOCKED

  - test_id: P04_TEST_003
    name: 无钱包实体输入
    expected_status: P04_REJECTED

  - test_id: P04_TEST_004
    name: 无供应量分母
    expected_status: P04_REJECTED

  - test_id: P04_TEST_005
    name: 早期钱包高留存
    expected_output: EARLY_CHIP_RETAINED_STRONG

  - test_id: P04_TEST_006
    name: 早期钱包大量清仓
    expected_output: EARLY_CHIP_MOSTLY_EXITED

  - test_id: P04_TEST_007
    name: 结构组部分卖出但仍高持仓
    expected_output: PARTIAL_DISTRIBUTION_CANDIDATE_OR_ROTATION_REQUIRED

  - test_id: P04_TEST_008
    name: 弱同源组被当强同源组聚合
    expected_status: P04_BLOCKED

  - test_id: P04_TEST_009
    name: 大量未知转出
    expected_status: P04_READY_WITH_GAPS
    expected_limitation: UNEXPLAINED_TRANSFER_RISK

  - test_id: P04_TEST_010
    name: 高对手盘承接压力
    expected_output: HIGH_COUNTERPARTY_PRESSURE

  - test_id: P04_TEST_011
    name: P04 输出 buy_signal
    expected_status: P04_BLOCKED

  - test_id: P04_TEST_012
    name: P04 请求 paper runtime
    expected_status: P04_BLOCKED

  - test_id: P04_TEST_013
    name: holder snapshot stale
    expected_status: P04_READY_WITH_GAPS

  - test_id: P04_TEST_014
    name: accounting major gap
    expected_status: P04_READY_WITH_GAPS_OR_REJECTED_DEPENDING_SEVERITY
```

---

# 28. P04 报告模型

```yaml
p04_chip_structure_report:
  report_id: string
  generated_at: datetime
  controller_id: P04_CHIP_STRUCTURE_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    chip_structure_ready_count: integer
    ready_with_gaps_count: integer
    rejected_count: integer
    blocked_count: integer

  participant_summary:
    wallet_entity_count: integer
    structural_group_count: integer
    early_wallet_count: integer
    counterparty_candidate_count: integer
    distribution_receiver_count: integer

  retention_summary:
    average_early_wallet_remaining_pct: number | null
    strong_retention_count: integer
    partial_distribution_count: integer
    mostly_exited_count: integer
    unknown_retention_count: integer

  structural_group_summary:
    average_structural_group_holding_pct: number | null
    high_structural_holding_count: integer
    weak_group_membership_count: integer

  transfer_summary:
    material_transfer_count: integer
    internal_rotation_candidate_count: integer
    unexplained_transfer_risk_count: integer

  distribution_summary:
    no_clear_distribution_count: integer
    partial_distribution_candidate_count: integer
    active_distribution_candidate_count: integer
    unclear_distribution_count: integer

  counterparty_summary:
    high_counterparty_pressure_count: integer
    moderate_counterparty_pressure_count: integer
    low_counterparty_pressure_count: integer
    unknown_pressure_count: integer

  quality_summary:
    chip_structure_quality_distribution: object
    accounting_quality_distribution: object
    supply_denominator_quality_distribution: object
    transfer_path_quality_distribution: object

  gap_summary:
    blocking_gaps: list
    critical_gaps: list
    high_gaps: list
    medium_gaps: list
    low_gaps: list

  p05_handoff_summary:
    p05_handoff_ready: boolean
    p05_limited_candidates: integer
    p05_required_tasks: list

  compliance:
    confirmed_market_maker_claim_generated: false
    evidence_generated: false
    scenario_claim_generated: false
    strategy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
```

---

# 29. HER P04 执行协议

```text
HER 执行 P04 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P04 controller context
4. 读取 P03 → P04 handoff packet
5. 读取 p04_chip_structure_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P04 input_manifest
8. 建立 chip_participant_universe_record
9. 建立 supply_denominator_record
10. 执行 chip_accounting_record
11. 建立 cohort_definition_record
12. 建立 early_wallet_cohort_record
13. 建立 early_wallet_retention_record
14. 建立 structural_group_holding_record
15. 建立 same_source_group_holding_record
16. 建立 sync_group_holding_record
17. 建立 chip_concentration_record
18. 建立 chip_exit_flow_record
19. 建立 chip_transfer_status_record
20. 建立 distribution_progress_record
21. 建立 counterparty_pressure_record
22. 建立 chip_cost_basis_record
23. 建立 chip_structure_score_record
24. 生成 chip_structure_quality_record
25. 生成 P04 gap report
26. 生成 p05_evidence_data_request_packet
27. 写入 P04 trace
28. 生成 p04_chip_structure_report
29. 生成 p04_to_p05_handoff_packet
30. 执行 P04 acceptance
31. 只允许 handoff 给 P05
```

禁止：

```text
1. 不允许无 P03 handoff 启动 P04
2. 不允许无钱包实体输入计算筹码结构
3. 不允许无供应量分母计算持仓比例
4. 不允许静默聚合弱同源组
5. 不允许把筹码结构状态说成确认庄家
6. 不允许生成 evidence object
7. 不允许输出 scenario
8. 不允许输出 strategy signal
9. 不允许进入 paper runtime
10. 不允许任何 live execution
```

---

# 30. 给 HER 的专业化任务书

```text
任务名称：建立 P04 Chip Structure Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p04_chip_structure_controller/ 下建立 P04 Chip Structure Controller。该控制器不是普通筹码统计脚本，也不是确认庄家或买点判断模块，而是筹码结构、持仓留存、迁移路径、派发进度与对手盘压力控制器。它负责读取 P03 Wallet Entity Controller 输出的钱包实体、同源组候选、同步行为组、角色候选、资金边、持仓事实和行为特征，将其转化为可追踪、可量化、可交接的 chip structure records，并生成 P05 Evidence Data Request Packet 与 P04→P05 Handoff Packet。

核心原则：
1. P04 只判断筹码结构状态，不确认庄家。
2. P04 不确认主导侧身份。
3. P04 不生成 evidence object。
4. P04 不识别交易场景。
5. P04 不做策略准入。
6. P04 不进入 paper runtime。
7. P04 不允许 live execution。
8. P04 必须先建立 chip participant universe。
9. P04 必须明确 supply denominator。
10. P04 必须执行 chip accounting。
11. P04 必须区分 early cohort、structural cohort、receiver cohort、counterparty cohort。
12. P04 必须生成 P05 Evidence Data Request Packet。
13. P04 只能交接给 P05 Evidence Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p04_chip_structure_controller/

需要创建系统文件：
1. p04_chip_structure_controller.yaml
2. p04_chip_structure_context.md
3. p04_input_contract.yaml
4. p04_output_contract.yaml
5. chip_participant_universe_schema.yaml
6. supply_denominator_schema.yaml
7. chip_accounting_record_schema.yaml
8. cohort_definition_schema.yaml
9. early_wallet_cohort_schema.yaml
10. early_wallet_retention_schema.yaml
11. structural_group_holding_schema.yaml
12. same_source_group_holding_schema.yaml
13. sync_group_holding_schema.yaml
14. chip_concentration_schema.yaml
15. chip_exit_flow_schema.yaml
16. chip_transfer_status_schema.yaml
17. distribution_progress_schema.yaml
18. counterparty_pressure_schema.yaml
19. chip_cost_basis_schema.yaml
20. chip_structure_score_schema.yaml
21. chip_structure_quality_schema.yaml
22. chip_accounting_policy.yaml
23. cohort_definition_policy.yaml
24. chip_retention_policy.yaml
25. distribution_progress_policy.yaml
26. counterparty_pressure_policy.yaml
27. cost_basis_policy.yaml
28. chip_structure_gap_policy.yaml
29. chip_structure_hard_negative_rules.yaml
30. chip_structure_state_machine.yaml
31. chip_structure_trace_requirements.yaml
32. p05_evidence_data_request_packet_contract.yaml
33. p04_to_p05_handoff_contract.yaml
34. p04_acceptance_criteria.md
35. p04_storage_constitution.md
36. p04_test_matrix.yaml
37. p04_report_model.yaml
38. p04_review_checklist.md
39. her_p04_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p04_chip_structure/
  input_manifest/
  participant_universe/
  supply_denominator/
  chip_accounting/
  cohort_definitions/
  early_wallet_cohorts/
  early_wallet_retention/
  structural_group_holding/
  same_source_group_holding/
  sync_group_holding/
  concentration/
  exit_flow/
  transfer_status/
  distribution_progress/
  counterparty_pressure/
  cost_basis/
  structure_scores/
  quality/
  gaps/
  conflicts/
  p05_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p04_chip_structure_controller.yaml：定义 P04 身份、职责、权限、上下游、状态码、禁止事项。
- p04_chip_structure_context.md：写成 HER 执行前必须读取的 P04 上下文。
- p04_input_contract.yaml：定义 P04 必须读取的 P03 handoff、wallet entities、group candidates、position facts、behavior facts、field usage permission、limitation tags。
- p04_output_contract.yaml：定义 chip accounting、cohorts、retention、concentration、transfer、distribution、counterparty、cost basis、quality、P05 request、handoff 输出。
- chip_participant_universe_schema.yaml：定义参与筹码计算的钱包实体和排除规则。
- supply_denominator_schema.yaml：定义总供应量、流通供应量、holder snapshot supply 的分母选择规则。
- chip_accounting_record_schema.yaml：定义买入、卖出、转入、转出、当前持仓的会计核算。
- cohort_definition_schema.yaml：定义 early / structural / same-source / sync / receiver / counterparty cohort。
- early_wallet_cohort_schema.yaml：定义早期钱包 cohort。
- early_wallet_retention_schema.yaml：定义早期钱包剩余筹码。
- structural_group_holding_schema.yaml：定义结构组聚合持仓。
- same_source_group_holding_schema.yaml：定义同源组持仓聚合。
- sync_group_holding_schema.yaml：定义同步组持仓聚合。
- chip_concentration_schema.yaml：定义筹码集中度。
- chip_exit_flow_schema.yaml：定义卖出、清仓、转出流。
- chip_transfer_status_schema.yaml：定义筹码迁移状态。
- distribution_progress_schema.yaml：定义派发进度候选。
- counterparty_pressure_schema.yaml：定义对手盘压力。
- chip_cost_basis_schema.yaml：定义结构侧成本区域估算。
- chip_structure_score_schema.yaml：定义多维结构评分，不允许单一总分。
- chip_structure_quality_schema.yaml：定义筹码结构质量与下游权限。
- chip_accounting_policy.yaml：定义筹码会计规则和账差处理。
- cohort_definition_policy.yaml：定义 cohort 纳入、排除和弱使用规则。
- chip_retention_policy.yaml：定义 early wallet remaining pct、structural holding pct 的判断规则。
- distribution_progress_policy.yaml：定义部分派发、主动派发、未知迁移、内部轮换的区分。
- counterparty_pressure_policy.yaml：定义对手盘压力计算规则。
- cost_basis_policy.yaml：定义成本区域估算规则和限制。
- chip_structure_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- chip_structure_hard_negative_rules.yaml：定义无 P03 handoff、无钱包实体、无持仓事实、无供应量分母、静默聚合弱同源组、确认庄家、输出策略、自动实盘等阻断规则。
- chip_structure_state_machine.yaml：定义 P04 全状态机。
- chip_structure_trace_requirements.yaml：定义 participant、accounting、cohort、retention、transfer、distribution、counterparty、handoff trace。
- p05_evidence_data_request_packet_contract.yaml：定义 P04 给 P05 的证据数据请求包。
- p04_to_p05_handoff_contract.yaml：定义 P04_TO_P05 handoff packet。
- p04_acceptance_criteria.md：定义 P04_READY、P04_READY_WITH_GAPS、P04_REJECTED、P04_BLOCKED。
- p04_storage_constitution.md：定义系统文件与运行数据目录。
- p04_test_matrix.yaml：定义至少 14 个测试场景。
- p04_report_model.yaml：定义 P04 人类可读报告。
- p04_review_checklist.md：定义审计清单。
- her_p04_execution_protocol.md：定义 HER 执行 P04 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P04_READY / P04_READY_WITH_GAPS / P04_REJECTED / P04_BLOCKED 判断
4. chip_participant_universe 摘要
5. supply_denominator 摘要
6. chip_accounting 摘要
7. early_wallet_retention 摘要
8. structural_group_holding 摘要
9. chip_concentration 摘要
10. chip_transfer_status 摘要
11. distribution_progress 摘要
12. counterparty_pressure 摘要
13. chip_cost_basis 摘要
14. chip_structure_quality 摘要
15. p05_evidence_data_request_packet 摘要
16. p04_to_p05_handoff_packet 摘要
17. P04 阻断规则摘要
18. P04 测试矩阵摘要
19. 当前缺口清单
20. 是否达到轻量机构级 P04 v3.0

最终验收标准：
只有当 P04 具备 chip participant universe、supply denominator、chip accounting、cohort definition、early wallet cohort、early wallet retention、structural group holding、same-source group holding、sync group holding、chip concentration、exit flow、transfer status、distribution progress、counterparty pressure、cost basis、structure score、structure quality、gap policy、hard negative rules、state machine、trace requirements、P05 data request、P04 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P04 不能确认庄家、不能生成 evidence、不能识别 scenario、不能输出 strategy、不能进入 paper runtime 或 live execution 时，才允许标记为 P04_READY。
```

---

# 31. 当前是否达到专业化标准

## 判断

这一版 P04 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是筹码统计脚本
```

P04 被明确升级为：

```text
筹码会计层
cohort 分析层
结构组持仓聚合层
筹码留存与迁移层
派发进度候选层
对手盘压力层
成本区域估算层
P05 证据转化输入层
```

---

# 32. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Chip Participant Universe|已补齐|
|Supply Denominator|已补齐|
|Chip Accounting|已补齐|
|Cohort Definition|已补齐|
|Early Wallet Cohort|已补齐|
|Early Wallet Retention|已补齐|
|Structural Group Holding|已补齐|
|Same Source Group Holding|已补齐|
|Sync Group Holding|已补齐|
|Chip Concentration|已补齐|
|Chip Exit Flow|已补齐|
|Chip Transfer Status|已补齐|
|Distribution Progress|已补齐|
|Counterparty Pressure|已补齐|
|Chip Cost Basis|已补齐|
|Chip Structure Score|已补齐|
|Chip Structure Quality|已补齐|
|P05 Evidence Data Request|已补齐|
|P04 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 33. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|early cohort 阈值未回测|已定义多种模式|P09 / P10 校准|
|supply denominator 可能冲突|已定义质量与限制|P05 转 evidence 时弱化|
|成本区域估算可能缺 entry price|已定义 cost_basis_quality|P05 标记不确定|
|内部轮换 vs 派发仍需场景上下文|P04 只给候选|P06 结合场景确认|
|对手盘压力不是策略阻断|已明确边界|P07 Strategy Gate 裁决|
|P04 不能生成 evidence object|已明确边界|P05 处理|
|P04 handoff 未联调|需要 P05|下一阶段展开 P05|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P04 的本质不是“筹码集中度脚本”，而是筹码结构会计与迁移状态控制器。**
    
2. **所有筹码百分比必须先定义供应量分母。**  
    没有 denominator，不能严肃计算持仓比例。
    
3. **早期钱包、结构钱包、对手盘钱包必须分 cohort。**  
    不同 cohort 的卖出、转出、持仓意义完全不同。
    
4. **P04 可以判断筹码结构状态，但不能生成证据对象。**  
    Evidence Object 属于 P05。
    
5. **部分卖出不等于派发完成。**  
    需要区分内部轮换、风险释放、接收方迁移、真实分发和未知转出。
    
6. **对手盘压力可以计算，但不能直接作为策略阻断。**  
    P07 才做最终策略门控。
    
7. **P04 必须输出 P05 Evidence Data Request Packet。**  
    这是从“结构状态”进入“证据系统”的关键交接。
    
8. **P04 只能交接给 P05。**  
    任何跳过 P05/P06/P07 直接进入 runtime 的路径都必须阻断。