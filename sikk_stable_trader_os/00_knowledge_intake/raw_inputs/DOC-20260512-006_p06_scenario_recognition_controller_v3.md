# P06 Scenario Recognition Controller 专业版 v3.0

## 多模型交易场景识别、场景冲突、否定条件与 P07 策略门控交接控制器

---

## 0. 先修正 P06 的定位

P06 不能被设计成普通的：

```text
看盘型脚本
策略识别器
二段扩张判断器
派发识别器
买点前置模块
```

P06 的专业定位应该是：

```text
把 P05 交接过来的证据束、反证、未知、冲突、替代解释，
转化为可追踪、可冲突处理、可否定、可分级、可交接给 P07 的场景识别系统。
```

一句话定义：

> **P05 负责“证据是否支持或反驳某些假设”。**  
> **P06 负责“这些证据组合更像哪一种交易场景，以及哪些场景被否定、冲突、待观察”。**  
> **P07 才负责“是否允许进入策略门控、观察、暂停、阻断或纸面候选”。**

P06 不能直接输出：

```text
可以买
PAPER_READY
执行许可
开仓
止盈止损
实盘确认
```

P06 只能输出：

```text
场景候选
主场景候选
次级场景候选
冲突场景
被否定场景
场景置信度
场景缺口
场景失效条件
P07 strategy gate data request
P06 → P07 handoff
```

---

# 1. P06 阶段核心目标

P06 必须一次性解决 16 个问题：

|编号|核心问题|P06 必须输出|
|---|---|---|
|1|哪些证据束可以进入场景识别？|`scenario_input_manifest`|
|2|当前可能属于哪些场景？|`scenario_candidate_record`|
|3|哪一个是主场景候选？|`primary_scenario_candidate_record`|
|4|哪些是次级场景候选？|`secondary_scenario_candidate_record`|
|5|哪些场景被明确否定？|`scenario_rejection_record`|
|6|哪些场景之间冲突？|`scenario_conflict_record`|
|7|哪些证据不足导致无法识别？|`scenario_unknown_record`|
|8|场景置信度如何计算？|`scenario_confidence_record`|
|9|场景是否稳定，还是过渡状态？|`scenario_transition_record`|
|10|场景是否需要继续观察？|`scenario_watch_condition_record`|
|11|场景的失效条件是什么？|`scenario_invalidation_record`|
|12|不同盘型对 P04/P05 证据如何解释？|`scenario_context_interpretation_record`|
|13|哪些场景风险会影响 P07？|`scenario_risk_flag_record`|
|14|P07 应该如何做策略门控？|`p07_strategy_gate_data_request_packet`|
|15|哪些输出禁止被策略层强使用？|`scenario_usage_permission_packet`|
|16|是否可以交接给 P07？|`p06_to_p07_handoff_packet`|

---

# 2. P06 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|场景分类官|识别当前候选属于哪些场景|`scenario_candidate_record`|
|反场景审查官|判断哪些场景被反证否定|`scenario_rejection_record`|
|冲突处理官|多个场景同时成立时如何处理|`scenario_conflict_record`|
|过渡状态分析官|判断是稳定场景还是过渡场景|`scenario_transition_record`|
|盘型语境解释官|不同盘型下如何解释证据|`scenario_context_interpretation_record`|
|失效条件官|定义场景失效条件|`scenario_invalidation_record`|
|风险标记官|输出会影响 P07 的风险标签|`scenario_risk_flag_record`|
|下游交接官|把场景候选交给 P07 策略门控|`p07_strategy_gate_data_request_packet`|

---

# 3. P06 底层方法论

## 3.1 场景不是信号

P06 输出的是：

```text
当前结构更像什么场景
```

不是：

```text
是否可以买
```

例如：

```text
二段扩张候选
控盘箱体候选
高位派发候选
下跌派发候选
流动性陷阱候选
```

这些都只是 P07 的输入，不是交易许可。

---

## 3.2 场景必须由证据束驱动

P06 只能读取 P05 交接的：

```text
supporting evidence
counter evidence
unknown evidence
conflict evidence
alternative explanation
evidence bundle
usage permission
```

禁止直接越过 P05 回到 P04 原始筹码状态做主观解释。

---

## 3.3 场景必须同时有“成立条件”和“否定条件”

专业场景识别不能只写：

```text
看起来像二段扩张
```

必须同时输出：

```text
成立条件
反证条件
失效条件
观察条件
冲突场景
替代场景
```

---

## 3.4 场景识别必须允许 UNKNOWN

P06 不应该为了输出结论而强行分类。

当证据不足时，必须输出：

```text
SCENARIO_UNKNOWN
SCENARIO_UNRESOLVED
SCENARIO_CONFLICTED
SCENARIO_OBSERVE_ONLY
```

---

## 3.5 场景与盘型语境绑定

同一个证据，在不同盘型下意义不同。

例如：

```text
早期钱包部分卖出
```

在高位放量阶段可能是派发反证；  
在长横盘控盘箱体中可能是正常轮换；  
在二段扩张前可能是换手吸收；  
在下跌反抽中可能是退出流动性制造。

所以 P06 必须有：

```text
scenario_context_interpretation
pattern_compatibility_check
alternative_explanation_check
```

---

# 4. P06 必须支持的场景体系

## 4.1 一级场景族

```yaml
scenario_families:
  ACCUMULATION_FAMILY:
    name_cn: 吸筹与筹码保留族
    scenarios:
      - EARLY_ACCUMULATION
      - CONTROL_BOX_ACCUMULATION
      - REACCUMULATION
      - LONG_SIDEWAYS_ACCUMULATION

  EXPANSION_FAMILY:
    name_cn: 扩张与拉升族
    scenarios:
      - FIRST_EXPANSION
      - SECOND_STAGE_EXPANSION
      - CONTROL_BOX_BREAKOUT
      - AVWAP_RECLAIM_EXPANSION

  DISTRIBUTION_FAMILY:
    name_cn: 派发与退出族
    scenarios:
      - PARTIAL_DISTRIBUTION
      - ACTIVE_DISTRIBUTION
      - LATE_DISTRIBUTION
      - DOWNWARD_DISTRIBUTION

  TRAP_FAMILY:
    name_cn: 陷阱与诱导流动性族
    scenarios:
      - EXIT_LIQUIDITY_TRAP
      - BULL_TRAP_REBOUND
      - FAKE_SIDEWAYS
      - FAKE_BREAKOUT
      - FINAL_PUMP_DISTRIBUTION

  ROTATION_FAMILY:
    name_cn: 轮换与再组织族
    scenarios:
      - INTERNAL_ROTATION
      - CONTROLLED_PULLBACK
      - SHAKEOUT_BEFORE_EXPANSION
      - FAILED_DISTRIBUTION_REACCUMULATION

  UNCERTAIN_FAMILY:
    name_cn: 未知与冲突族
    scenarios:
      - SCENARIO_UNKNOWN
      - SCENARIO_CONFLICTED
      - DATA_INSUFFICIENT
      - OBSERVE_ONLY
```

---

# 5. P06 核心对象总表

|对象|作用|
|---|---|
|`Scenario Input Manifest`|记录 P06 接收的证据束|
|`Scenario Taxonomy Record`|场景分类体系|
|`Scenario Feature Map Record`|场景需要哪些证据特征|
|`Scenario Candidate Record`|场景候选|
|`Primary Scenario Candidate Record`|主场景候选|
|`Secondary Scenario Candidate Record`|次级场景候选|
|`Scenario Rejection Record`|被否定场景|
|`Scenario Conflict Record`|冲突场景|
|`Scenario Unknown Record`|不足以判断场景|
|`Scenario Confidence Record`|场景置信度|
|`Scenario Transition Record`|场景过渡状态|
|`Scenario Context Interpretation Record`|盘型语境解释|
|`Scenario Invalidation Record`|场景失效条件|
|`Scenario Watch Condition Record`|观察条件|
|`Scenario Risk Flag Record`|给 P07 的风险标签|
|`Scenario Usage Permission Record`|下游使用权限|
|`P07 Strategy Gate Data Request Packet`|给 P07 的策略门控请求|
|`P06 to P07 Handoff Packet`|P06 → P07 交接包|

---

# 6. P06 输入：必须读取什么

```yaml
p06_required_inputs:
  from_p05:
    - p05_to_p06_handoff_packet
    - p06_scenario_data_request_packet
    - evidence_bundle_records
    - supporting_evidence_records
    - counter_evidence_records
    - weak_evidence_records
    - unknown_evidence_records
    - evidence_conflict_records
    - alternative_explanation_records
    - evidence_sufficiency_records
    - evidence_usage_permission_records

  from_p04:
    - chip_structure_quality_records
    - chip_structure_score_records
    - distribution_progress_records
    - counterparty_pressure_records
    - chip_transfer_status_records

  from_p02:
    - market_structure_fact_seed
    - market_fact_records
    - security_fact_records
    - data_quality_report

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - limitation_transfer_packet
    - forbidden_use_policy
    - governance_handoff_packet
    - domain_scenario_taxonomy_handoff

  required_contracts:
    - p06_input_contract
    - p06_output_contract
    - scenario_taxonomy_contract
    - scenario_candidate_contract
    - p07_strategy_gate_input_contract
```

P06 启动前必须确认：

```text
P05 已验收
P05 handoff 已生成
P06 只读取 Handoff 授权字段
P05 输出仍是 evidence，不是 scenario
弱证据不能直接生成强场景
冲突证据必须进入 conflict path
P06 不允许 paper runtime
P06 不允许 live execution
```

---

# 7. Scenario Input Manifest

```yaml
scenario_input_manifest:
  manifest_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  input_sources:
    p05_handoff_packet_id: string
    p06_scenario_data_request_packet_id: string
    evidence_bundle_ids: list
    evidence_usage_permission_ids: list

  evidence_bundle_summary:
    chip_retention_bundle_available: boolean
    distribution_risk_bundle_available: boolean
    counterparty_pressure_bundle_available: boolean
    transfer_risk_bundle_available: boolean
    cost_basis_bundle_available: boolean
    data_uncertainty_bundle_available: boolean
    security_risk_bundle_available: boolean

  input_quality:
    evidence_sufficiency_status: string
    conflict_count: integer
    unknown_count: integer
    weak_evidence_count: integer
    p06_input_quality_status:
      - SCENARIO_INPUT_HIGH_CONFIDENCE
      - SCENARIO_INPUT_USABLE
      - SCENARIO_INPUT_USABLE_WITH_GAPS
      - SCENARIO_INPUT_LOW_CONFIDENCE
      - SCENARIO_INPUT_UNUSABLE

  limitations:
    inherited_limitation_tags: list
    forbidden_uses: list

  trace:
    scenario_input_trace_id: string
    source_evidence_trace_ids: list
```

---

# 8. Scenario Feature Map Record

每个场景必须有输入特征映射。

```yaml
scenario_feature_map_record:
  feature_map_id: string
  scenario_type: string

  required_positive_features:
    - feature_id: string
      source_bundle: string
      description_cn: string
      minimum_strength:
        - STRONG
        - MODERATE
        - WEAK_ALLOWED

  required_negative_filters:
    - filter_id: string
      counter_evidence_type: string
      description_cn: string
      blocking_if_present: boolean

  optional_supporting_features:
    - feature_id: string
      source_bundle: string
      description_cn: string

  required_unknown_checks:
    - unknown_scope: string
      effect_if_unknown:
        - WEAKEN_SCENARIO
        - BLOCK_STRONG_SCENARIO
        - FORCE_OBSERVE_ONLY

  conflict_rules:
    - conflict_type: string
      effect:
        - LOWER_CONFIDENCE
        - MARK_CONFLICTED
        - REJECT_SCENARIO
```

---

# 9. Scenario Candidate Record

```yaml
scenario_candidate_record:
  scenario_candidate_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  scenario:
    scenario_family:
      - ACCUMULATION_FAMILY
      - EXPANSION_FAMILY
      - DISTRIBUTION_FAMILY
      - TRAP_FAMILY
      - ROTATION_FAMILY
      - UNCERTAIN_FAMILY
    scenario_type:
      - EARLY_ACCUMULATION
      - CONTROL_BOX_ACCUMULATION
      - REACCUMULATION
      - LONG_SIDEWAYS_ACCUMULATION
      - FIRST_EXPANSION
      - SECOND_STAGE_EXPANSION
      - CONTROL_BOX_BREAKOUT
      - AVWAP_RECLAIM_EXPANSION
      - PARTIAL_DISTRIBUTION
      - ACTIVE_DISTRIBUTION
      - LATE_DISTRIBUTION
      - DOWNWARD_DISTRIBUTION
      - EXIT_LIQUIDITY_TRAP
      - BULL_TRAP_REBOUND
      - FAKE_SIDEWAYS
      - FAKE_BREAKOUT
      - FINAL_PUMP_DISTRIBUTION
      - INTERNAL_ROTATION
      - CONTROLLED_PULLBACK
      - SHAKEOUT_BEFORE_EXPANSION
      - FAILED_DISTRIBUTION_REACCUMULATION
      - SCENARIO_UNKNOWN
      - SCENARIO_CONFLICTED
      - DATA_INSUFFICIENT
      - OBSERVE_ONLY

  supporting_basis:
    supporting_evidence_ids: list
    evidence_bundle_ids: list
    key_supporting_factors_cn: list

  counter_basis:
    counter_evidence_ids: list
    conflict_ids: list
    unknown_ids: list
    key_counter_factors_cn: list

  scenario_assessment:
    positive_fit_score: number
    counter_pressure_score: number
    conflict_pressure_score: number
    unknown_pressure_score: number
    scenario_confidence_score: number
    scenario_confidence_level:
      - HIGH_CONFIDENCE_CANDIDATE
      - MEDIUM_CONFIDENCE_CANDIDATE
      - LOW_CONFIDENCE_CANDIDATE
      - WEAK_OBSERVATION_ONLY
      - REJECTED

  usage_permission:
    p07_usage_permission:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - DO_NOT_USE
    p07_strategy_gate_allowed: boolean
    paper_runtime_allowed: false
    live_execution_allowed: false

  trace:
    scenario_trace_id: string
    source_evidence_trace_ids: list
```

---

# 10. Primary Scenario Candidate Record

P06 可以输出主场景候选，但仍不是策略结论。

```yaml
primary_scenario_candidate_record:
  primary_scenario_id: string
  candidate_id: string

  selected_primary_scenario:
    scenario_candidate_id: string
    scenario_type: string
    scenario_family: string

  selection_reason:
    strongest_supporting_bundle_ids: list
    weakest_counter_evidence_ids: list
    conflict_level: string
    unknown_level: string
    reason_cn: string

  primary_status:
    - PRIMARY_SCENARIO_HIGH_CONFIDENCE
    - PRIMARY_SCENARIO_MEDIUM_CONFIDENCE
    - PRIMARY_SCENARIO_LOW_CONFIDENCE
    - PRIMARY_SCENARIO_CONFLICTED
    - NO_PRIMARY_SCENARIO

  downstream_limit:
    not_strategy_decision: true
    p07_must_apply_strategy_gate: true
    p07_must_apply_risk_filters: true
```

---

# 11. Secondary Scenario Candidate Record

```yaml
secondary_scenario_candidate_record:
  secondary_record_id: string
  candidate_id: string

  secondary_scenarios:
    - scenario_candidate_id: string
      scenario_type: string
      reason_cn: string
      relationship_to_primary:
        - COMPLEMENTARY
        - COMPETING
        - RISK_OVERLAY
        - TRANSITION_POSSIBILITY
        - WEAK_ALTERNATIVE

  downstream_instruction:
    p07_must_consider_secondary_risks: true
    p07_cannot_ignore_competing_distribution_scenario: true
```

---

# 12. Scenario Rejection Record

P06 必须明确哪些场景被反证否定。

```yaml
scenario_rejection_record:
  rejection_id: string
  candidate_id: string

  rejected_scenario:
    scenario_type: string
    scenario_family: string

  rejection_basis:
    counter_evidence_ids: list
    conflict_ids: list
    unknown_ids: list
    rejection_reason_cn: string

  rejection_strength:
    - STRONG_REJECTION
    - MODERATE_REJECTION
    - WEAK_REJECTION
    - INSUFFICIENT_TO_REJECT

  downstream_effect:
    p07_must_not_use_rejected_scenario_as_entry_basis: true
    scenario_recheck_allowed_after_new_data: boolean
```

---

# 13. Scenario Conflict Record

多个场景同时出现时必须记录冲突。

```yaml
scenario_conflict_record:
  scenario_conflict_id: string
  candidate_id: string

  conflicting_scenarios:
    - scenario_candidate_id: string
      scenario_type: string

  conflict_type:
    - ACCUMULATION_VS_DISTRIBUTION
    - EXPANSION_VS_EXIT_LIQUIDITY_TRAP
    - ROTATION_VS_ACTIVE_DISTRIBUTION
    - REACCUMULATION_VS_FAKE_SIDEWAYS
    - SECOND_STAGE_EXPANSION_VS_FINAL_PUMP_DISTRIBUTION
    - DATA_INSUFFICIENT_CONFLICT

  conflict_basis:
    supporting_evidence_for_each_side: object
    counter_evidence_for_each_side: object
    unresolved_unknowns: list

  conflict_severity:
    - BLOCKING_CONFLICT
    - HIGH_CONFLICT
    - MEDIUM_CONFLICT
    - LOW_CONFLICT

  resolution_status:
    - UNRESOLVED
    - PRIMARY_SELECTED_WITH_LIMITATIONS
    - OBSERVE_ONLY_REQUIRED
    - REJECT_WEAKER_SCENARIO
    - REQUIRE_DATA_REFRESH

  downstream_effect:
    p07_usage_permission:
      - DO_NOT_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
    strategy_gate_must_not_emit_paper_ready_if_blocking: true
```

---

# 14. Scenario Unknown Record

```yaml
scenario_unknown_record:
  unknown_scenario_id: string
  candidate_id: string

  unknown_reason_scope:
    - MISSING_MARKET_STRUCTURE
    - MISSING_KLINE_CONTEXT
    - MISSING_FRESH_HOLDER_SNAPSHOT
    - EVIDENCE_CONFLICT_UNRESOLVED
    - WEAK_WALLET_ENTITY_INPUT
    - TRANSFER_PATH_UNKNOWN
    - SECURITY_FACT_STALE
    - DATA_STALE

  affected_scenarios:
    - scenario_type: string
      effect:
        - WEAKEN_CONFIDENCE
        - BLOCK_HIGH_CONFIDENCE
        - FORCE_OBSERVE_ONLY

  downstream_instruction:
    p07_must_treat_as_risk_or_pause: boolean
    p07_must_not_force_entry: true
```

---

# 15. Scenario Confidence Record

置信度必须拆维度，不能一个分数决定。

```yaml
scenario_confidence_record:
  confidence_id: string
  scenario_candidate_id: string
  candidate_id: string

  dimensions:
    evidence_support_score: number
    counter_evidence_pressure_score: number
    conflict_pressure_score: number
    unknown_pressure_score: number
    trace_quality_score: number
    data_freshness_score: number
    scenario_feature_fit_score: number
    alternative_explanation_pressure_score: number

  confidence_result:
    scenario_confidence_score: number
    scenario_confidence_level:
      - HIGH
      - MEDIUM
      - LOW
      - CONFLICTED
      - UNKNOWN

  no_single_score_policy:
    enabled: true
    reason: P07 必须读取维度，不允许只看总分

  downstream:
    p07_must_read_dimensions: true
```

---

# 16. Scenario Transition Record

场景可能处于转化过程，而非静态状态。

```yaml
scenario_transition_record:
  transition_id: string
  candidate_id: string

  from_scenario_candidate:
    scenario_type: string | null
    confidence: number | null

  to_scenario_candidate:
    scenario_type: string | null
    confidence: number | null

  transition_type:
    - ACCUMULATION_TO_EXPANSION
    - EXPANSION_TO_DISTRIBUTION
    - DISTRIBUTION_TO_REACCUMULATION
    - ROTATION_TO_EXPANSION
    - SIDEWAYS_TO_BREAKOUT
    - BREAKOUT_TO_TRAP
    - UNKNOWN_TRANSITION

  transition_evidence:
    supporting_evidence_ids: list
    counter_evidence_ids: list
    unknown_ids: list

  transition_status:
    - TRANSITION_CONFIRMED_CANDIDATE
    - TRANSITION_IN_PROGRESS
    - TRANSITION_WEAK
    - TRANSITION_CONFLICTED
    - TRANSITION_UNKNOWN

  downstream_effect:
    p07_should_prefer_observe_or_pause_if_transition_uncertain: true
```

---

# 17. Scenario Context Interpretation Record

这部分是专业版关键：不同盘型下解释不同。

```yaml
scenario_context_interpretation_record:
  interpretation_id: string
  candidate_id: string
  scenario_candidate_id: string

  context_frame:
    market_pattern_context:
      - LONG_SIDEWAYS
      - CONTROL_BOX
      - FIRST_EXPANSION
      - SECOND_STAGE_PRECONDITION
      - HIGH_LEVEL_VOLATILITY
      - DOWNWARD_DISTRIBUTION
      - REBOUND_AFTER_DROP
      - UNKNOWN

  evidence_reinterpretation:
    - evidence_id: string
      raw_interpretation_cn: string
      context_adjusted_interpretation_cn: string
      adjustment_reason_cn: string

  examples:
    partial_early_wallet_sell:
      in_control_box: NORMAL_ROTATION_OR_RISK_RELEASE_POSSIBLE
      in_high_level_pump: DISTRIBUTION_RISK_HIGHER
      in_downward_rebound: EXIT_LIQUIDITY_RISK_HIGHER

  downstream_instruction:
    p07_must_read_context_adjusted_interpretation: true
    p07_cannot_use_raw_evidence_without_context: true
```

---

# 18. Scenario Invalidation Record

P06 必须输出场景失效条件，供 P07/P08/P09 使用。

```yaml
scenario_invalidation_record:
  invalidation_id: string
  scenario_candidate_id: string
  candidate_id: string

  invalidation_conditions:
    - condition_id: string
      condition_cn: string
      source_required:
        - MARKET_STRUCTURE
        - WALLET_DELTA
        - HOLDER_SNAPSHOT
        - PRICE_VOLUME
        - SECURITY_CHECK
      severity:
        - HARD_INVALIDATION
        - SOFT_INVALIDATION
        - WATCH_INVALIDATION

  example_conditions:
    for_second_stage_expansion:
      - early_wallet_concentrated_exit
      - structural_group_holding_breakdown
      - high_counterparty_pressure_rising
      - active_distribution_counter_evidence
      - breakout_failure_with_volume

    for_accumulation:
      - early_wallet_full_exit
      - liquidity_removed
      - no_reaccumulation_after_pullback
      - repeated_failed_reclaim

    for_distribution:
      - structural_wallets_reaccumulate
      - counterparty_pressure_falls
      - selling_flow_exhausts
      - support_reclaim_with_retention

  downstream:
    p07_must_include_in_gate: true
    p08_must_monitor_if_runtime: true
```

---

# 19. Scenario Watch Condition Record

```yaml
scenario_watch_condition_record:
  watch_condition_id: string
  candidate_id: string
  scenario_candidate_id: string

  watch_conditions:
    - condition_id: string
      condition_cn: string
      required_data_refresh:
        - WALLET_DELTA
        - HOLDER_SNAPSHOT
        - MARKET_STRUCTURE
        - KLINE_VOLUME
        - QUOTE_SECURITY
      priority:
        - HIGH
        - MEDIUM
        - LOW

  watch_status:
    - WATCH_REQUIRED
    - DATA_REFRESH_REQUIRED
    - MANUAL_REVIEW_REQUIRED
    - NO_WATCH_REQUIRED

  downstream:
    p07_may_output_PAUSE_or_OBSERVE: true
```

---

# 20. Scenario Risk Flag Record

P06 必须给 P07 明确风险标签。

```yaml
scenario_risk_flag_record:
  risk_flag_id: string
  candidate_id: string

  risk_flags:
    - ACTIVE_DISTRIBUTION_RISK
    - EXIT_LIQUIDITY_TRAP_RISK
    - HIGH_COUNTERPARTY_PRESSURE_RISK
    - SCENARIO_CONFLICT_RISK
    - DATA_INSUFFICIENT_RISK
    - WEAK_EVIDENCE_RISK
    - SECURITY_CONTEXT_RISK
    - TRANSITION_UNCERTAINTY_RISK
    - FAKE_BREAKOUT_RISK
    - FINAL_PUMP_DISTRIBUTION_RISK

  risk_flag_sources:
    evidence_ids: list
    scenario_conflict_ids: list
    unknown_ids: list

  downstream_effect:
    p07_must_apply_hard_negative_rules: true
    p07_may_block_or_pause: true
```

---

# 21. Scenario Usage Permission Record

```yaml
scenario_usage_permission_record:
  permission_id: string
  candidate_id: string
  scenario_candidate_id: string

  usage_permission:
    - FULL_USE_IN_P07
    - WEAK_USE_ONLY_IN_P07
    - OBSERVE_ONLY
    - DO_NOT_USE
    - REQUIRE_DATA_REFRESH
    - REQUIRE_MANUAL_REVIEW

  allowed_usage:
    - strategy_gate_input
    - risk_flag_input
    - pause_condition_input
    - observe_condition_input
    - invalidation_input

  forbidden_usage:
    - direct_paper_ready
    - direct_buy_signal
    - live_execution
    - confirmed_market_maker_claim
    - confirmed_dominant_side_claim

  reason_cn: string
```

---

# 22. P06 Gap Policy

```yaml
p06_gap_policy:
  BLOCKING_GAP:
    result: P06_BLOCKED
    examples:
      - p05_handoff_missing
      - trace_missing
      - acceptance_missing
      - live_execution_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P06_REJECTED
    examples:
      - no_evidence_bundles
      - no_scenario_taxonomy
      - no_scenario_feature_map
      - all_evidence_do_not_use
      - output_contract_missing

  HIGH_GAP:
    result: P06_READY_WITH_GAPS
    downstream_permission: P07_LIMITED
    examples:
      - blocking_scenario_conflict
      - missing_market_structure_context
      - unresolved_distribution_vs_expansion_conflict
      - major_unknown_evidence_present
      - scenario_confidence_low

  MEDIUM_GAP:
    result: P06_READY_WITH_GAPS
    downstream_permission: P07_ALLOWED_WITH_LIMITATIONS
    examples:
      - weak_cost_basis_bundle
      - partial_counterparty_pressure
      - stale_security_context
      - transition_state_uncertain

  LOW_GAP:
    result: P06_READY_WITH_GAPS
    downstream_permission: P07_ALLOWED_WITH_NOTE
    examples:
      - optional_historical_scenario_missing
      - minor_evidence_conflict
      - noncritical_context_missing
```

---

# 23. P06 Hard Negative Rules

```yaml
p06_hard_negative_rules:
  - rule_id: P06_BLOCK_001
    name: 未读取 P05 handoff
    condition: p05_to_p06_handoff_packet_missing == true
    result: P06_BLOCKED
    reason: P06 不能绕过 P05 / Handoff 启动

  - rule_id: P06_BLOCK_002
    name: 无证据束输入
    condition: evidence_bundle_records_missing == true
    result: P06_REJECTED
    reason: 无证据束不能识别场景

  - rule_id: P06_BLOCK_003
    name: 无场景分类体系
    condition: scenario_taxonomy_missing == true
    result: P06_REJECTED
    reason: 没有 taxonomy 不能输出场景

  - rule_id: P06_BLOCK_004
    name: 弱证据生成强场景
    condition: weak_evidence_used_for_high_confidence_scenario == true
    result: P06_BLOCKED
    reason: 弱证据不能直接生成高置信场景

  - rule_id: P06_BLOCK_005
    name: 忽略冲突场景
    condition: scenario_conflict_detected == true and scenario_conflict_record_missing == true
    result: P06_BLOCKED
    reason: 冲突场景必须登记

  - rule_id: P06_BLOCK_006
    name: 忽略否定条件
    condition: scenario_candidate_created == true and rejection_check_missing == true
    result: P06_BLOCKED
    reason: 场景识别必须检查反场景与否定条件

  - rule_id: P06_BLOCK_007
    name: 输出策略或纸面准入
    condition: output_contains in [strategy_signal, paper_ready, buy_signal]
    result: P06_BLOCKED
    reason: P06 越权

  - rule_id: P06_BLOCK_008
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P06_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 24. P06 状态机专业版

```yaml
p06_scenario_recognition_state_machine:
  states:
    - P06_UNINITIALIZED
    - P06_CONTEXT_LOADED
    - P06_HANDOFF_READ
    - P06_INPUT_MANIFEST_BUILT
    - P06_SCENARIO_TAXONOMY_LOADED
    - P06_SCENARIO_FEATURE_MAP_BUILT
    - P06_EVIDENCE_BUNDLES_QUALIFIED
    - P06_SCENARIO_CANDIDATES_BUILT
    - P06_REJECTION_CHECKS_BUILT
    - P06_CONFLICT_CHECKS_BUILT
    - P06_UNKNOWN_SCENARIOS_BUILT
    - P06_CONFIDENCE_SCORES_BUILT
    - P06_PRIMARY_SCENARIO_SELECTED
    - P06_SECONDARY_SCENARIOS_BUILT
    - P06_TRANSITION_RECORDS_BUILT
    - P06_CONTEXT_INTERPRETATION_BUILT
    - P06_INVALIDATION_RECORDS_BUILT
    - P06_WATCH_CONDITIONS_BUILT
    - P06_RISK_FLAGS_BUILT
    - P06_USAGE_PERMISSIONS_BUILT
    - P06_GAP_ANALYZED
    - P06_P07_DATA_REQUEST_BUILT
    - P06_READY_FOR_ACCEPTANCE
    - P06_ACCEPTANCE_READY
    - P06_READY_FOR_P07_HANDOFF
    - P06_READY_WITH_GAPS
    - P06_REJECTED
    - P06_BLOCKED

  critical_transitions:
    - from: P06_HANDOFF_READ
      to: P06_INPUT_MANIFEST_BUILT
      condition: p05_handoff_valid == true

    - from: P06_INPUT_MANIFEST_BUILT
      to: P06_SCENARIO_TAXONOMY_LOADED
      condition: scenario_taxonomy_available == true

    - from: P06_SCENARIO_TAXONOMY_LOADED
      to: P06_SCENARIO_FEATURE_MAP_BUILT
      condition: scenario_feature_maps_created == true

    - from: P06_SCENARIO_FEATURE_MAP_BUILT
      to: P06_EVIDENCE_BUNDLES_QUALIFIED
      condition: evidence_bundle_usage_permissions_checked == true

    - from: P06_EVIDENCE_BUNDLES_QUALIFIED
      to: P06_SCENARIO_CANDIDATES_BUILT
      condition: scenario_candidate_records_created == true

    - from: P06_SCENARIO_CANDIDATES_BUILT
      to: P06_REJECTION_CHECKS_BUILT
      condition: scenario_rejection_records_created == true

    - from: P06_REJECTION_CHECKS_BUILT
      to: P06_CONFLICT_CHECKS_BUILT
      condition: scenario_conflict_records_created == true

    - from: P06_CONFLICT_CHECKS_BUILT
      to: P06_CONFIDENCE_SCORES_BUILT
      condition: scenario_confidence_records_created == true

    - from: P06_CONFIDENCE_SCORES_BUILT
      to: P06_PRIMARY_SCENARIO_SELECTED
      condition: primary_scenario_candidate_record_created == true

    - from: P06_PRIMARY_SCENARIO_SELECTED
      to: P06_CONTEXT_INTERPRETATION_BUILT
      condition: context_interpretation_records_created == true

    - from: P06_CONTEXT_INTERPRETATION_BUILT
      to: P06_INVALIDATION_RECORDS_BUILT
      condition: scenario_invalidation_records_created == true

    - from: P06_INVALIDATION_RECORDS_BUILT
      to: P06_RISK_FLAGS_BUILT
      condition: scenario_risk_flag_records_created == true

    - from: P06_RISK_FLAGS_BUILT
      to: P06_P07_DATA_REQUEST_BUILT
      condition: p07_strategy_gate_data_request_packet_created == true

    - from: P06_P07_DATA_REQUEST_BUILT
      to: P06_READY_FOR_ACCEPTANCE
      condition: p06_output_contract_ready == true

    - from: P06_READY_FOR_ACCEPTANCE
      to: P06_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P06_ACCEPTANCE_READY
      to: P06_READY_FOR_P07_HANDOFF
      condition: p06_to_p07_handoff_packet_created == true
```

---

# 25. P07 Strategy Gate Data Request Packet

P06 必须告诉 P07 如何进行策略门控，而不是直接给策略结论。

```yaml
p07_strategy_gate_data_request_packet:
  packet_id: string
  from_controller: P06_SCENARIO_RECOGNITION_CONTROLLER
  to_controller: P07_STRATEGY_GATE_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  scenario_inputs_available:
    primary_scenario_candidate_records_path: string
    secondary_scenario_candidate_records_path: string
    scenario_rejection_records_path: string
    scenario_conflict_records_path: string
    scenario_unknown_records_path: string
    scenario_confidence_records_path: string
    scenario_transition_records_path: string
    scenario_context_interpretation_records_path: string
    scenario_invalidation_records_path: string
    scenario_watch_condition_records_path: string
    scenario_risk_flag_records_path: string
    scenario_usage_permission_records_path: string

  p07_required_gate_tasks:
    - apply_governance_hard_negative_rules
    - apply_scenario_risk_flags
    - apply_scenario_conflict_blocks
    - apply_strategy_pattern_compatibility
    - apply_invalidation_conditions
    - apply_watch_or_pause_conditions
    - determine_OBSERVE_PAUSE_BLOCK_OR_PAPER_CANDIDATE

  usage_limitations:
    - SCENARIO_ONLY
    - NO_DIRECT_PAPER_READY
    - NO_DIRECT_BUY_SIGNAL
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  scenario_usage_permissions:
    full_use_scenario_ids: list
    weak_use_only_scenario_ids: list
    observe_only_scenario_ids: list
    do_not_use_scenario_ids: list

  risk_flags_to_apply:
    risk_flag_ids: list

  invalidation_conditions_to_apply:
    invalidation_ids: list
```

---

# 26. P06 to P07 Handoff Packet

```yaml
p06_to_p07_handoff_packet:
  packet_id: string
  packet_type: P06_TO_P07_SCENARIO_RECOGNITION_HANDOFF
  generated_at: datetime

  route:
    from_controller: P06_SCENARIO_RECOGNITION_CONTROLLER
    to_controller: P07_STRATEGY_GATE_CONTROLLER

  upstream_control:
    p05_handoff_packet_id: string
    p06_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    candidate_count_scenario_ready: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  scenario_package:
    scenario_input_manifest_path: string
    scenario_taxonomy_path: string
    scenario_feature_map_records_path: string
    scenario_candidate_records_path: string
    primary_scenario_candidate_records_path: string
    secondary_scenario_candidate_records_path: string
    scenario_rejection_records_path: string
    scenario_conflict_records_path: string
    scenario_unknown_records_path: string
    scenario_confidence_records_path: string
    scenario_transition_records_path: string
    scenario_context_interpretation_records_path: string
    scenario_invalidation_records_path: string
    scenario_watch_condition_records_path: string
    scenario_risk_flag_records_path: string
    scenario_usage_permission_records_path: string

  p07_data_request:
    p07_strategy_gate_data_request_packet_path: string
    required_p07_tasks: list
    risk_flags_to_apply: list
    invalidation_conditions_to_apply: list

  quality:
    scenario_quality_report_path: string
    scenario_confidence_summary: object
    scenario_conflict_summary: object
    scenario_unknown_summary: object
    scenario_transition_summary: object

  limitations:
    - SCENARIO_RECOGNITION_ONLY
    - NO_STRATEGY_DECISION
    - NO_DIRECT_PAPER_READY
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P07_STRATEGY_GATE_CONTROLLER
    forbidden:
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p07_must_read_first:
      - p06_to_p07_handoff_packet
      - p07_strategy_gate_data_request_packet
      - primary_scenario_candidate_records
      - scenario_conflict_records
      - scenario_rejection_records
      - scenario_risk_flag_records
      - scenario_invalidation_records
      - scenario_usage_permission_records
```

---

# 27. P06 文件体系

## 27.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p06_scenario_recognition_controller/
```

必须创建：

```text
p06_scenario_recognition_controller.yaml
p06_scenario_recognition_context.md
p06_input_contract.yaml
p06_output_contract.yaml
scenario_input_manifest_schema.yaml
scenario_taxonomy.yaml
scenario_feature_map_schema.yaml
scenario_candidate_schema.yaml
primary_scenario_candidate_schema.yaml
secondary_scenario_candidate_schema.yaml
scenario_rejection_schema.yaml
scenario_conflict_schema.yaml
scenario_unknown_schema.yaml
scenario_confidence_schema.yaml
scenario_transition_schema.yaml
scenario_context_interpretation_schema.yaml
scenario_invalidation_schema.yaml
scenario_watch_condition_schema.yaml
scenario_risk_flag_schema.yaml
scenario_usage_permission_schema.yaml
scenario_family_policy.yaml
scenario_feature_mapping_policy.yaml
scenario_rejection_policy.yaml
scenario_conflict_policy.yaml
scenario_confidence_policy.yaml
scenario_transition_policy.yaml
scenario_context_interpretation_policy.yaml
scenario_invalidation_policy.yaml
scenario_gap_policy.yaml
scenario_hard_negative_rules.yaml
scenario_state_machine.yaml
scenario_trace_requirements.yaml
p07_strategy_gate_data_request_packet_contract.yaml
p06_to_p07_handoff_contract.yaml
p06_acceptance_criteria.md
p06_storage_constitution.md
p06_test_matrix.yaml
p06_report_model.yaml
p06_review_checklist.md
her_p06_execution_protocol.md
```

---

## 27.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p06_scenario_recognition/
  input_manifest/
  scenario_taxonomy/
  scenario_feature_maps/
  scenario_candidates/
  primary_scenarios/
  secondary_scenarios/
  rejected_scenarios/
  conflicts/
  unknowns/
  confidence/
  transitions/
  context_interpretation/
  invalidations/
  watch_conditions/
  risk_flags/
  usage_permissions/
  quality/
  gaps/
  p07_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 28. P06 测试矩阵

```yaml
p06_test_matrix:
  - test_id: P06_TEST_001
    name: 证据束支持筹码留存，反证较弱
    expected_output: ACCUMULATION_OR_RETENTION_SCENARIO_CANDIDATE
    expected_status: P06_READY_FOR_P07_HANDOFF

  - test_id: P06_TEST_002
    name: 缺 P05 handoff
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_003
    name: 无 evidence bundle
    expected_status: P06_REJECTED

  - test_id: P06_TEST_004
    name: 弱证据被用于高置信二段扩张
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_005
    name: 筹码留存与主动派发证据冲突
    expected_output: SCENARIO_CONFLICT_RECORD
    expected_status: P06_READY_WITH_GAPS

  - test_id: P06_TEST_006
    name: 高对手盘压力与扩张场景冲突
    expected_output: EXPANSION_VS_EXIT_LIQUIDITY_TRAP_CONFLICT

  - test_id: P06_TEST_007
    name: 数据不足无法识别场景
    expected_output: SCENARIO_UNKNOWN
    expected_status: P06_READY_WITH_GAPS

  - test_id: P06_TEST_008
    name: 长横盘语境下部分早期钱包卖出
    expected_output: CONTEXT_INTERPRETATION_NORMAL_ROTATION_POSSIBLE

  - test_id: P06_TEST_009
    name: 高位放量语境下早期钱包集中卖出
    expected_output: ACTIVE_DISTRIBUTION_OR_FINAL_PUMP_DISTRIBUTION_CANDIDATE

  - test_id: P06_TEST_010
    name: 二段扩张候选但存在高未解释转出
    expected_output: SECOND_STAGE_EXPANSION_WITH_TRANSFER_RISK
    expected_status: P06_READY_WITH_GAPS

  - test_id: P06_TEST_011
    name: P06 输出 paper_ready
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_012
    name: P06 请求 paper runtime
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_013
    name: live execution requested
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_014
    name: 场景候选未生成 rejection check
    expected_status: P06_BLOCKED

  - test_id: P06_TEST_015
    name: primary scenario 与 secondary distribution risk 并存
    expected_output: PRIMARY_SCENARIO_WITH_SECONDARY_RISK_OVERLAY

  - test_id: P06_TEST_016
    name: scenario taxonomy 缺失
    expected_status: P06_REJECTED
```

---

# 29. P06 报告模型

```yaml
p06_scenario_recognition_report:
  report_id: string
  generated_at: datetime
  controller_id: P06_SCENARIO_RECOGNITION_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    scenario_ready_count: integer
    ready_with_gaps_count: integer
    rejected_count: integer
    blocked_count: integer

  scenario_summary:
    primary_scenario_distribution: object
    secondary_scenario_distribution: object
    rejected_scenario_count: integer
    conflict_scenario_count: integer
    unknown_scenario_count: integer

  family_summary:
    accumulation_family_count: integer
    expansion_family_count: integer
    distribution_family_count: integer
    trap_family_count: integer
    rotation_family_count: integer
    uncertain_family_count: integer

  confidence_summary:
    high_confidence_count: integer
    medium_confidence_count: integer
    low_confidence_count: integer
    conflicted_count: integer
    unknown_count: integer

  conflict_summary:
    blocking_conflict_count: integer
    high_conflict_count: integer
    accumulation_vs_distribution_count: integer
    expansion_vs_trap_count: integer
    rotation_vs_distribution_count: integer

  invalidation_summary:
    hard_invalidation_condition_count: integer
    soft_invalidation_condition_count: integer
    watch_invalidation_condition_count: integer

  risk_flag_summary:
    active_distribution_risk_count: integer
    exit_liquidity_trap_risk_count: integer
    high_counterparty_pressure_risk_count: integer
    data_insufficient_risk_count: integer

  p07_handoff_summary:
    p07_handoff_ready: boolean
    p07_limited_candidates: integer
    p07_required_tasks: list

  compliance:
    strategy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
    direct_buy_signal_generated: false
```

---

# 30. HER P06 执行协议

```text
HER 执行 P06 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P06 controller context
4. 读取 P05 → P06 handoff packet
5. 读取 p06_scenario_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P06 scenario_input_manifest
8. 读取 scenario_taxonomy
9. 建立 scenario_feature_map_records
10. 校验 evidence bundle usage permission
11. 生成 scenario_candidate_records
12. 生成 scenario_rejection_records
13. 生成 scenario_conflict_records
14. 生成 scenario_unknown_records
15. 生成 scenario_confidence_records
16. 选择 primary_scenario_candidate
17. 生成 secondary_scenario_candidate_records
18. 生成 scenario_transition_records
19. 生成 scenario_context_interpretation_records
20. 生成 scenario_invalidation_records
21. 生成 scenario_watch_condition_records
22. 生成 scenario_risk_flag_records
23. 生成 scenario_usage_permission_records
24. 生成 P06 gap report
25. 生成 p07_strategy_gate_data_request_packet
26. 写入 P06 trace
27. 生成 p06_scenario_recognition_report
28. 生成 p06_to_p07_handoff_packet
29. 执行 P06 acceptance
30. 只允许 handoff 给 P07
```

禁止：

```text
1. 不允许无 P05 handoff 启动 P06
2. 不允许无 evidence bundle 识别场景
3. 不允许弱证据生成高置信场景
4. 不允许忽略冲突场景
5. 不允许忽略场景否定条件
6. 不允许场景识别直接变成策略准入
7. 不允许输出 buy_signal
8. 不允许输出 paper_ready
9. 不允许进入 paper runtime
10. 不允许任何 live execution
```

---

# 31. 给 HER 的专业化任务书

```text
任务名称：建立 P06 Scenario Recognition Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p06_scenario_recognition_controller/ 下建立 P06 Scenario Recognition Controller。该控制器不是买点判断器，也不是策略准入模块，而是多模型交易场景识别、场景冲突、否定条件、场景置信度、场景风险标签与 P07 策略门控交接控制器。它负责读取 P05 Evidence Controller 输出的证据对象、反证、未知证据、冲突证据、替代解释和证据束，将其转化为 scenario candidates、primary scenario、secondary scenario、rejected scenario、scenario conflict、scenario unknown、scenario invalidation、scenario risk flags，并生成 P07 Strategy Gate Data Request Packet 与 P06→P07 Handoff Packet。

核心原则：
1. P06 只识别场景，不做策略准入。
2. P06 不输出 buy signal。
3. P06 不输出 paper_ready。
4. P06 不进入 paper runtime。
5. P06 不允许 live execution。
6. P06 必须从 P05 evidence bundle 读取输入。
7. P06 必须检查场景否定条件。
8. P06 必须记录场景冲突。
9. P06 必须允许 UNKNOWN / CONFLICTED / OBSERVE_ONLY。
10. P06 必须生成 P07 Strategy Gate Data Request Packet。
11. P06 只能交接给 P07 Strategy Gate Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p06_scenario_recognition_controller/

需要创建系统文件：
1. p06_scenario_recognition_controller.yaml
2. p06_scenario_recognition_context.md
3. p06_input_contract.yaml
4. p06_output_contract.yaml
5. scenario_input_manifest_schema.yaml
6. scenario_taxonomy.yaml
7. scenario_feature_map_schema.yaml
8. scenario_candidate_schema.yaml
9. primary_scenario_candidate_schema.yaml
10. secondary_scenario_candidate_schema.yaml
11. scenario_rejection_schema.yaml
12. scenario_conflict_schema.yaml
13. scenario_unknown_schema.yaml
14. scenario_confidence_schema.yaml
15. scenario_transition_schema.yaml
16. scenario_context_interpretation_schema.yaml
17. scenario_invalidation_schema.yaml
18. scenario_watch_condition_schema.yaml
19. scenario_risk_flag_schema.yaml
20. scenario_usage_permission_schema.yaml
21. scenario_family_policy.yaml
22. scenario_feature_mapping_policy.yaml
23. scenario_rejection_policy.yaml
24. scenario_conflict_policy.yaml
25. scenario_confidence_policy.yaml
26. scenario_transition_policy.yaml
27. scenario_context_interpretation_policy.yaml
28. scenario_invalidation_policy.yaml
29. scenario_gap_policy.yaml
30. scenario_hard_negative_rules.yaml
31. scenario_state_machine.yaml
32. scenario_trace_requirements.yaml
33. p07_strategy_gate_data_request_packet_contract.yaml
34. p06_to_p07_handoff_contract.yaml
35. p06_acceptance_criteria.md
36. p06_storage_constitution.md
37. p06_test_matrix.yaml
38. p06_report_model.yaml
39. p06_review_checklist.md
40. her_p06_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p06_scenario_recognition/
  input_manifest/
  scenario_taxonomy/
  scenario_feature_maps/
  scenario_candidates/
  primary_scenarios/
  secondary_scenarios/
  rejected_scenarios/
  conflicts/
  unknowns/
  confidence/
  transitions/
  context_interpretation/
  invalidations/
  watch_conditions/
  risk_flags/
  usage_permissions/
  quality/
  gaps/
  p07_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p06_scenario_recognition_controller.yaml：定义 P06 身份、职责、权限、上下游、状态码、禁止事项。
- p06_scenario_recognition_context.md：写成 HER 执行前必须读取的 P06 上下文。
- p06_input_contract.yaml：定义 P06 必须读取的 P05 handoff、evidence bundles、counter evidence、unknown evidence、conflicts、alternative explanations、usage permission。
- p06_output_contract.yaml：定义 scenario candidates、primary scenario、secondary scenarios、rejections、conflicts、unknowns、confidence、transitions、invalidations、risk flags、P07 request、handoff 输出。
- scenario_input_manifest_schema.yaml：定义 P06 接收的全部场景输入。
- scenario_taxonomy.yaml：定义 accumulation、expansion、distribution、trap、rotation、uncertain 六大场景族。
- scenario_feature_map_schema.yaml：定义每类场景需要哪些正向特征、反向过滤、未知检查和冲突处理。
- scenario_candidate_schema.yaml：定义标准场景候选。
- primary_scenario_candidate_schema.yaml：定义主场景候选。
- secondary_scenario_candidate_schema.yaml：定义次级场景候选。
- scenario_rejection_schema.yaml：定义被否定场景。
- scenario_conflict_schema.yaml：定义场景冲突。
- scenario_unknown_schema.yaml：定义未知场景。
- scenario_confidence_schema.yaml：定义场景置信度维度。
- scenario_transition_schema.yaml：定义场景过渡。
- scenario_context_interpretation_schema.yaml：定义不同盘型语境下证据解释变化。
- scenario_invalidation_schema.yaml：定义场景失效条件。
- scenario_watch_condition_schema.yaml：定义需要继续观察的条件。
- scenario_risk_flag_schema.yaml：定义传递给 P07 的风险标签。
- scenario_usage_permission_schema.yaml：定义 P07 使用权限。
- scenario_family_policy.yaml：定义场景族与适用边界。
- scenario_feature_mapping_policy.yaml：定义证据束到场景特征的映射。
- scenario_rejection_policy.yaml：定义场景否定规则。
- scenario_conflict_policy.yaml：定义冲突场景处理。
- scenario_confidence_policy.yaml：定义置信度计算，不允许单一总分覆盖维度。
- scenario_transition_policy.yaml：定义场景过渡判断。
- scenario_context_interpretation_policy.yaml：定义盘型语境解释规则。
- scenario_invalidation_policy.yaml：定义失效条件。
- scenario_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- scenario_hard_negative_rules.yaml：定义无 P05 handoff、无证据束、无 taxonomy、弱证据生成强场景、忽略冲突、忽略否定条件、输出策略、自动实盘等阻断。
- scenario_state_machine.yaml：定义 P06 全状态机。
- scenario_trace_requirements.yaml：定义 scenario trace、evidence trace、conflict trace、risk flag trace、handoff trace。
- p07_strategy_gate_data_request_packet_contract.yaml：定义 P06 给 P07 的策略门控数据请求包。
- p06_to_p07_handoff_contract.yaml：定义 P06_TO_P07 handoff packet。
- p06_acceptance_criteria.md：定义 P06_READY、P06_READY_WITH_GAPS、P06_REJECTED、P06_BLOCKED。
- p06_storage_constitution.md：定义系统文件与运行数据目录。
- p06_test_matrix.yaml：定义至少 16 个测试场景。
- p06_report_model.yaml：定义 P06 人类可读报告。
- p06_review_checklist.md：定义审计清单。
- her_p06_execution_protocol.md：定义 HER 执行 P06 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P06_READY / P06_READY_WITH_GAPS / P06_REJECTED / P06_BLOCKED 判断
4. scenario taxonomy 摘要
5. scenario candidate 摘要
6. primary scenario 摘要
7. secondary scenario 摘要
8. scenario rejection 摘要
9. scenario conflict 摘要
10. scenario unknown 摘要
11. scenario confidence 摘要
12. scenario context interpretation 摘要
13. scenario invalidation 摘要
14. scenario risk flag 摘要
15. p07_strategy_gate_data_request_packet 摘要
16. p06_to_p07_handoff_packet 摘要
17. P06 阻断规则摘要
18. P06 测试矩阵摘要
19. 当前缺口清单
20. 是否达到轻量机构级 P06 v3.0

最终验收标准：
只有当 P06 具备 scenario input manifest、scenario taxonomy、scenario feature map、scenario candidate、primary scenario、secondary scenario、rejected scenario、scenario conflict、scenario unknown、scenario confidence、scenario transition、scenario context interpretation、scenario invalidation、scenario watch condition、scenario risk flag、scenario usage permission、family policy、feature mapping policy、rejection policy、conflict policy、confidence policy、transition policy、context interpretation policy、invalidation policy、gap policy、hard negative rules、state machine、trace requirements、P07 data request、P06 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P06 不能输出 buy signal、不能输出 paper_ready、不能进入 paper runtime 或 live execution 时，才允许标记为 P06_READY。
```

---

# 32. 当前是否达到专业化标准

## 判断

这一版 P06 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是买点识别器
不是策略准入器
```

P06 被明确升级为：

```text
场景分类体系层
证据束到场景映射层
主场景 / 次场景识别层
场景冲突层
场景否定层
场景未知层
场景失效条件层
P07 策略门控输入层
```

---

# 33. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Scenario Input Manifest|已补齐|
|Scenario Taxonomy|已补齐|
|Scenario Feature Map|已补齐|
|Scenario Candidate|已补齐|
|Primary Scenario|已补齐|
|Secondary Scenario|已补齐|
|Scenario Rejection|已补齐|
|Scenario Conflict|已补齐|
|Scenario Unknown|已补齐|
|Scenario Confidence|已补齐|
|Scenario Transition|已补齐|
|Scenario Context Interpretation|已补齐|
|Scenario Invalidation|已补齐|
|Scenario Watch Condition|已补齐|
|Scenario Risk Flag|已补齐|
|Scenario Usage Permission|已补齐|
|P07 Strategy Gate Data Request|已补齐|
|P06 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 34. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|scenario feature 权重未回测|已定义结构|P09 / P10 校准|
|P06 需要市场结构更细字段|P02/P04 已给 seed|P07 前可由 Runner 补 market structure|
|二段扩张 vs 最后一拉派发容易冲突|已建 conflict 机制|P07 需要硬否定|
|长横盘语境下卖出的解释仍需样本|已建 context interpretation|Review 后校准|
|P06 不能做策略准入|已明确边界|P07 处理|
|P06 handoff 未联调|需要 P07|下一阶段展开 P07|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P06 的本质不是策略判断，而是场景识别控制器。**
    
2. **场景必须由证据束驱动。**  
    不能绕过 P05 直接拿 P04 筹码状态主观解释。
    
3. **每个场景都必须有成立条件、否定条件、冲突条件和失效条件。**
    
4. **UNKNOWN 是合法场景输出。**  
    证据不足时不能强行分类。
    
5. **同一个证据在不同盘型语境下意义不同。**  
    P06 必须做 context interpretation。
    
6. **P06 输出的是 P07 的策略门控输入，不是策略结论。**
    
7. **P06 必须输出 risk flags 和 invalidation conditions。**  
    这些是 P07 判断 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE 的核心输入。
    
8. **P06 只能交接给 P07。**  
    任何跳过 P07 直接进入 runtime 的路径都必须阻断。