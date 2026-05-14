# P05 Evidence Controller 专业版 v3.0

## 证据对象、反证对象、冲突证据、未知证据与 P06 场景识别交接控制器

---

## 0. 先修正 P05 的定位

P05 不能被设计成普通的：

```text
证据摘要模块
打分模块
结论生成器
策略解释器
```

P05 的专业定位应该是：

```text
把 P02 数据事实、P03 钱包实体候选、P04 筹码结构状态，转化为可追踪、可分级、可反驳、可冲突登记、可交接给 P06 的 Evidence Object System。
```

一句话定义：

> **P04 负责输出筹码结构状态。**  
> **P05 负责把事实与结构状态转成“支持证据 / 反证 / 冲突 / 未知 / 弱证据 / 证据束”。**  
> **P06 才负责基于证据识别交易场景。**

P05 不能直接输出：

```text
这是二段扩张
这是高位派发
可以买
PAPER_READY
策略准入
确认庄家
确认主控
```

P05 只能输出：

```text
某事实支持某假设
某事实反驳某假设
某事实存在冲突
某字段不足以形成证据
某证据只能弱使用
某证据束可交接给 P06 场景识别
```

---

# 1. P05 阶段核心目标

P05 必须一次性解决 15 个问题：

|编号|核心问题|P05 必须输出|
|---|---|---|
|1|哪些事实可以进入证据系统？|`evidence_input_manifest`|
|2|每条证据支持什么、反驳什么？|`evidence_object_record`|
|3|哪些事实只能弱使用？|`weak_evidence_record`|
|4|哪些事实构成反证？|`counter_evidence_record`|
|5|哪些证据之间冲突？|`evidence_conflict_record`|
|6|哪些问题因数据不足只能标记未知？|`unknown_evidence_record`|
|7|哪些证据可组成证据束？|`evidence_bundle_record`|
|8|证据强度、可靠性、相关性如何？|`evidence_weight_record`|
|9|证据是否足够进入 P06？|`evidence_sufficiency_record`|
|10|证据链是否可追踪？|`evidence_chain_record`|
|11|有哪些替代解释？|`alternative_explanation_record`|
|12|有哪些缺口和限制？|`p05_gap_report`|
|13|P06 应该识别哪些场景候选？|`p06_scenario_data_request_packet`|
|14|哪些证据禁止下游强使用？|`evidence_usage_permission_packet`|
|15|是否可以交接给 P06？|`p05_to_p06_handoff_packet`|

---

# 2. P05 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|证据登记官|哪些输入能成为证据|`evidence_input_manifest`|
|证据建模官|事实如何转为证据对象|`evidence_object_record`|
|反证官|哪些事实反驳原假设|`counter_evidence_record`|
|冲突裁剪官|多条证据之间是否冲突|`evidence_conflict_record`|
|不确定性官|哪些问题只能 UNKNOWN|`unknown_evidence_record`|
|证据权重官|可靠性、相关性、新鲜度、强度|`evidence_weight_record`|
|替代解释官|同一事实还能解释成什么|`alternative_explanation_record`|
|下游交接官|P06 应如何使用证据|`p06_scenario_data_request_packet`|

---

# 3. P05 底层方法论

## 3.1 事实 ≠ 证据

P02 / P03 / P04 的输出是事实或结构状态。

例如：

```text
早期钱包剩余 62%
同源候选组仍持有 18%
未知转出占结构组买入 25%
对手盘鲸鱼承接 12%
```

这些还不是完整结论。

P05 要把它们转成：

```text
支持证据
反证
冲突证据
未知证据
弱证据
证据束
```

---

## 3.2 证据必须对应假设

P05 每条证据必须回答：

```text
它支持哪个假设？
它反驳哪个假设？
它是否也支持替代解释？
它的强度是多少？
它能不能被下游强使用？
```

没有目标假设的材料，只能叫事实，不能叫证据。

---

## 3.3 证据必须有反证通道

专业系统不能只堆支持材料。

每个正向证据都要检查：

```text
有没有反向证据？
有没有冲突字段？
有没有替代解释？
有没有数据缺口？
有没有时效问题？
```

---

## 3.4 证据强度不能只靠分数

P05 不允许只输出一个总分。

必须至少拆成：

```text
来源可靠性
trace 完整性
字段新鲜度
相关性
直接性
一致性
可重复性
反证压力
替代解释压力
下游可用性
```

---

## 3.5 P05 只生成证据，不识别场景

P05 可以输出：

```text
支持“结构侧筹码留存”的证据束
反驳“结构侧仍控筹”的反证
支持“派发风险”的证据
支持“对手盘压力”的反证材料
```

但不能输出：

```text
当前是二段扩张
当前是主动派发
当前可以买
```

这些属于 P06 / P07。

---

# 4. P05 必须建立的核心对象

|对象|作用|
|---|---|
|`Evidence Input Manifest`|记录 P05 接收了哪些事实和结构状态|
|`Evidence Subject Registry`|证据作用对象：token / wallet / cohort / group / event|
|`Hypothesis Frame Record`|可被证据支持或反驳的假设框架|
|`Evidence Object Record`|标准证据对象|
|`Supporting Evidence Record`|支持证据|
|`Counter Evidence Record`|反证|
|`Weak Evidence Record`|弱证据|
|`Unknown Evidence Record`|未知 / 不足以判断|
|`Evidence Conflict Record`|冲突证据|
|`Alternative Explanation Record`|替代解释|
|`Evidence Chain Record`|证据链|
|`Evidence Weight Record`|证据权重|
|`Evidence Bundle Record`|证据束|
|`Evidence Sufficiency Record`|证据充分性|
|`Evidence Usage Permission Record`|下游使用权限|
|`P06 Scenario Data Request Packet`|给 P06 的场景识别请求|
|`P05 to P06 Handoff Packet`|P05 → P06 交接包|

---

# 5. P05 输入：必须读取什么

```yaml
p05_required_inputs:
  from_p04:
    - p04_to_p05_handoff_packet
    - p05_evidence_data_request_packet
    - chip_participant_universe_records
    - early_wallet_retention_records
    - structural_group_holding_records
    - chip_concentration_records
    - chip_exit_flow_records
    - chip_transfer_status_records
    - distribution_progress_records
    - counterparty_pressure_records
    - chip_cost_basis_records
    - chip_structure_score_records
    - chip_structure_quality_records

  from_p03:
    - wallet_entity_master_records
    - wallet_role_candidate_records
    - same_source_group_candidates
    - sync_behavior_group_candidates
    - funding_flow_edges
    - wallet_entity_quality_report

  from_p02:
    - market_fact_records
    - security_fact_records
    - holder_snapshot_fact
    - transaction_fact_seed
    - data_quality_report
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
    - domain_evidence_model_handoff

  required_contracts:
    - p05_input_contract
    - p05_output_contract
    - evidence_object_contract
    - counter_evidence_contract
    - evidence_bundle_contract
    - p06_scenario_input_contract
```

P05 启动前必须确认：

```text
P04 已验收
P04 handoff 已生成
P05 只读取 handoff 授权字段
所有 P04 结构状态仍是 evidence input，不是 scenario conclusion
弱字段不能升级为强证据
P05 不允许进入 paper runtime
P05 不允许 live execution
```

---

# 6. Hypothesis Frame Record

P05 必须先定义证据要支持或反驳什么。

```yaml
hypothesis_frame_record:
  hypothesis_id: string
  candidate_id: string
  hypothesis_family:
    - CHIP_RETENTION
    - STRUCTURAL_GROUP_STABILITY
    - DISTRIBUTION_RISK
    - COUNTERPARTY_PRESSURE
    - COST_BASIS_SUPPORT
    - TRANSFER_RISK
    - DATA_UNCERTAINTY
    - SECURITY_RISK
    - MARKET_CONTEXT

  hypothesis_statement_cn: string

  allowed_evidence_types:
    - SUPPORTING
    - COUNTER
    - WEAK
    - UNKNOWN
    - CONFLICT

  example_hypotheses:
    - STRUCTURAL_SIDE_CHIP_RETAINED
    - EARLY_WALLETS_MOSTLY_EXITED
    - ACTIVE_DISTRIBUTION_RISK_PRESENT
    - COUNTERPARTY_PRESSURE_HIGH
    - STRUCTURAL_GROUP_HOLDING_SUPPORTIVE
    - CHIP_TRANSFER_UNEXPLAINED
    - COST_BASIS_SUPPORT_USABLE
    - DATA_INSUFFICIENT_FOR_STRONG_CLAIM

  downstream:
    p06_can_use_for_scenario_recognition: true
    p07_strategy_gate_allowed: false
```

---

# 7. Evidence Object Record

这是 P05 的核心资产。

```yaml
evidence_object_record:
  evidence_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  evidence_type:
    - SUPPORTING_EVIDENCE
    - COUNTER_EVIDENCE
    - WEAK_EVIDENCE
    - UNKNOWN_EVIDENCE
    - CONFLICT_EVIDENCE

  evidence_subject:
    subject_type:
      - TOKEN
      - WALLET_ENTITY
      - WALLET_GROUP
      - COHORT
      - CHIP_STRUCTURE
      - TRANSFER_PATH
      - DISTRIBUTION_STATE
      - COUNTERPARTY
      - MARKET_CONTEXT
    subject_id: string

  hypothesis_link:
    supports_hypothesis_ids: list
    counters_hypothesis_ids: list
    unknown_for_hypothesis_ids: list

  source_material:
    source_controller:
      - P02_SOURCE_DATA_FACT_CONTROLLER
      - P03_WALLET_ENTITY_CONTROLLER
      - P04_CHIP_STRUCTURE_CONTROLLER
    source_record_ids: list
    source_trace_ids: list
    field_trace_ids: list

  observation:
    observation_summary_cn: string
    key_values: object
    observed_at: datetime | null
    snapshot_time: datetime | null

  interpretation:
    permitted_interpretation_cn: string
    prohibited_interpretations:
      - CONFIRMED_MARKET_MAKER
      - CONFIRMED_DOMINANT_SIDE
      - CONFIRMED_SCENARIO
      - BUY_SIGNAL
      - PAPER_READY

  quality:
    evidence_relevance_score: number
    evidence_reliability_score: number
    evidence_directness_score: number
    evidence_freshness_score: number
    trace_quality_score: number
    counter_evidence_pressure_score: number
    alternative_explanation_pressure_score: number

  strength:
    evidence_strength:
      - STRONG
      - MODERATE
      - WEAK
      - UNKNOWN
      - CONFLICTED
    strength_reason_cn: string

  downstream_permission:
    p06_usage_permission:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - DO_NOT_USE
    p07_strategy_gate_allowed: false
    paper_runtime_allowed: false
    live_execution_allowed: false
```

---

# 8. Supporting Evidence Record

```yaml
supporting_evidence_record:
  supporting_evidence_id: string
  evidence_id: string
  candidate_id: string

  support_category:
    - EARLY_CHIP_RETENTION_SUPPORT
    - STRUCTURAL_GROUP_HOLDING_SUPPORT
    - LOW_EXIT_FLOW_SUPPORT
    - INTERNAL_ROTATION_SUPPORT
    - COST_BASIS_SUPPORT
    - LOW_COUNTERPARTY_PRESSURE_SUPPORT
    - DATA_QUALITY_SUPPORT

  support_target_hypothesis: string

  support_basis:
    source_records: list
    key_metrics:
      early_wallet_remaining_pct: number | null
      structural_group_holding_pct: number | null
      group_remaining_ratio_pct: number | null
      counterparty_pressure_status: string | null
      cost_basis_quality: string | null

  support_strength:
    - STRONG_SUPPORT
    - MODERATE_SUPPORT
    - WEAK_SUPPORT
    - SUPPORT_INSUFFICIENT

  caveats:
    - requires_scenario_context
    - requires_market_structure_confirmation
    - requires_counter_evidence_check
    - weak_due_to_data_gap
```

---

# 9. Counter Evidence Record

```yaml
counter_evidence_record:
  counter_evidence_id: string
  evidence_id: string
  candidate_id: string

  counter_category:
    - EARLY_WALLET_EXIT_COUNTER
    - STRUCTURAL_GROUP_EXIT_COUNTER
    - ACTIVE_DISTRIBUTION_COUNTER
    - UNKNOWN_TRANSFER_COUNTER
    - HIGH_COUNTERPARTY_PRESSURE_COUNTER
    - COST_BASIS_UNUSABLE_COUNTER
    - STALE_DATA_COUNTER
    - SECURITY_RISK_COUNTER

  counters_hypothesis: string

  counter_basis:
    source_records: list
    key_metrics:
      early_wallet_exit_ratio_pct: number | null
      structural_group_exit_ratio_pct: number | null
      unknown_transfer_risk_score: number | null
      counterparty_pressure_score: number | null
      accounting_gap_pct: number | null

  counter_strength:
    - STRONG_COUNTER
    - MODERATE_COUNTER
    - WEAK_COUNTER
    - COUNTER_INSUFFICIENT

  downstream_effect:
    p06_must_consider_as_counter_scenario_input: true
    p07_strategy_gate_allowed: false
```

---

# 10. Unknown Evidence Record

P05 必须有“不知道”的专业表达，不能强行结论化。

```yaml
unknown_evidence_record:
  unknown_id: string
  candidate_id: string

  unknown_scope:
    - CHIP_RETENTION_UNKNOWN
    - TRANSFER_PATH_UNKNOWN
    - COUNTERPARTY_PRESSURE_UNKNOWN
    - COST_BASIS_UNKNOWN
    - SUPPLY_DENOMINATOR_UNKNOWN
    - WALLET_ENTITY_UNKNOWN
    - SOURCE_CONFLICT_UNKNOWN

  reason:
    missing_fields: list
    stale_fields: list
    conflicted_fields: list
    trace_gaps: list
    insufficient_coverage: boolean

  downstream_instruction:
    p06_must_not_generate_strong_scenario_from_this: true
    p06_allowed_usage:
      - uncertainty_tag
      - weak_context
      - scenario_blocking_condition_if_critical
```

---

# 11. Evidence Conflict Record

```yaml
evidence_conflict_record:
  conflict_id: string
  candidate_id: string

  conflict_type:
    - SUPPORT_COUNTER_CONFLICT
    - SOURCE_VALUE_CONFLICT
    - TIME_CONTEXT_CONFLICT
    - WALLET_ENTITY_CONFLICT
    - CHIP_ACCOUNTING_CONFLICT
    - QUALITY_CONFLICT

  conflicting_evidence_ids: list
  conflicting_source_record_ids: list

  conflict_description_cn: string

  conflict_severity:
    - BLOCKING_CONFLICT
    - HIGH_CONFLICT
    - MEDIUM_CONFLICT
    - LOW_CONFLICT

  resolution_status:
    - UNRESOLVED
    - RESOLVED_BY_SOURCE_PRIORITY
    - RESOLVED_BY_FRESHNESS
    - RESOLVED_BY_TRACE_QUALITY
    - CANNOT_RESOLVE

  downstream_effect:
    p06_usage_permission:
      - DO_NOT_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
    must_propagate_conflict: true
```

---

# 12. Alternative Explanation Record

同一个事实可能有多个解释。

```yaml
alternative_explanation_record:
  alternative_id: string
  candidate_id: string
  evidence_id: string

  observed_fact: string

  primary_interpretation_candidate: string

  alternative_explanations:
    - explanation_id: string
      explanation_cn: string
      plausibility_score: number
      supporting_facts: list
      required_followup: list

  examples:
    partial_early_wallet_sell:
      possible_explanations:
        - ACTIVE_DISTRIBUTION
        - NORMAL_ROTATION
        - RISK_RELEASE
        - INTERNAL_TRANSFER
        - REACCUMULATION_PREPARATION

    high_counterparty_buy:
      possible_explanations:
        - EXIT_LIQUIDITY
        - ORGANIC_WHALE_ENTRY
        - STRUCTURE_SIDE_REABSORPTION
        - BOT_VOLUME_NOISE

  downstream_instruction:
    p06_must_consider_alternatives: true
    p06_must_not_single_path_reason: true
```

---

# 13. Evidence Weight Record

```yaml
evidence_weight_record:
  weight_id: string
  evidence_id: string
  candidate_id: string

  dimensions:
    source_reliability_score: number
    trace_completeness_score: number
    data_freshness_score: number
    directness_score: number
    relevance_score: number
    consistency_score: number
    uniqueness_score: number
    repeatability_score: number
    counter_evidence_pressure_score: number
    alternative_explanation_pressure_score: number

  weighted_result:
    evidence_weight_class:
      - HIGH_WEIGHT
      - MEDIUM_WEIGHT
      - LOW_WEIGHT
      - UNKNOWN_WEIGHT
      - CONFLICTED_WEIGHT

  no_single_total_policy:
    enabled: true
    reason: evidence must preserve dimension-level reasoning

  downstream:
    p06_usage_mode:
      - FULL_USE
      - WEAK_USE_ONLY
      - OBSERVE_ONLY
      - DO_NOT_USE
```

---

# 14. Evidence Bundle Record

单条证据不能直接推动场景识别，P06 应读取证据束。

```yaml
evidence_bundle_record:
  bundle_id: string
  candidate_id: string

  bundle_type:
    - CHIP_RETENTION_BUNDLE
    - DISTRIBUTION_RISK_BUNDLE
    - COUNTERPARTY_PRESSURE_BUNDLE
    - TRANSFER_RISK_BUNDLE
    - COST_BASIS_BUNDLE
    - DATA_UNCERTAINTY_BUNDLE
    - SECURITY_RISK_BUNDLE

  included_evidence_ids: list
  included_counter_evidence_ids: list
  included_unknown_ids: list
  included_conflict_ids: list

  bundle_summary:
    supporting_count: integer
    counter_count: integer
    unknown_count: integer
    conflict_count: integer

  bundle_assessment:
    support_pressure:
      - STRONG_SUPPORT_PRESSURE
      - MODERATE_SUPPORT_PRESSURE
      - WEAK_SUPPORT_PRESSURE
      - NO_SUPPORT
    counter_pressure:
      - STRONG_COUNTER_PRESSURE
      - MODERATE_COUNTER_PRESSURE
      - WEAK_COUNTER_PRESSURE
      - NO_COUNTER
    conflict_pressure:
      - HIGH_CONFLICT
      - MEDIUM_CONFLICT
      - LOW_CONFLICT
      - NO_CONFLICT

  downstream_permission:
    p06_can_use_for_scenario_recognition: boolean
    p06_usage_limitations: list
```

---

# 15. Evidence Sufficiency Record

P05 要判断“证据是否足以进入 P06”，但不是判断场景。

```yaml
evidence_sufficiency_record:
  sufficiency_id: string
  candidate_id: string

  sufficiency_scope:
    - CHIP_RETENTION
    - DISTRIBUTION_RISK
    - COUNTERPARTY_PRESSURE
    - TRANSFER_RISK
    - COST_BASIS
    - DATA_QUALITY

  sufficiency_checks:
    minimum_supporting_evidence_present: boolean
    counter_evidence_checked: boolean
    conflict_checked: boolean
    unknowns_registered: boolean
    trace_complete: boolean
    quality_above_threshold: boolean

  sufficiency_status:
    - SUFFICIENT_FOR_P06
    - SUFFICIENT_WITH_LIMITATIONS
    - INSUFFICIENT_WEAK_ONLY
    - BLOCK_P06_USE

  limitations:
    - WEAK_USE_ONLY
    - REQUIRE_SCENARIO_CONTEXT
    - REQUIRE_MARKET_STRUCTURE_CONFIRMATION
    - REQUIRE_DATA_REFRESH
    - REQUIRE_MANUAL_REVIEW
```

---

# 16. Evidence Usage Permission Record

```yaml
evidence_usage_permission_record:
  permission_id: string
  candidate_id: string
  evidence_id: string

  usage_permission:
    - FULL_USE_IN_P06
    - WEAK_USE_ONLY_IN_P06
    - OBSERVE_ONLY
    - DO_NOT_USE
    - REQUIRE_REFRESH
    - REQUIRE_MANUAL_REVIEW

  allowed_usage:
    - scenario_input
    - scenario_counter_input
    - uncertainty_tag
    - conflict_tag
    - review_reference

  forbidden_usage:
    - strategy_gate_direct_input
    - paper_ready_decision
    - live_execution
    - confirmed_market_maker_claim
    - confirmed_dominant_side_claim

  reason_cn: string
```

---

# 17. P05 Gap Policy

```yaml
p05_gap_policy:
  BLOCKING_GAP:
    result: P05_BLOCKED
    examples:
      - p04_handoff_missing
      - trace_missing
      - acceptance_missing
      - live_execution_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P05_REJECTED
    examples:
      - no_chip_structure_inputs
      - no_evidence_object_contract
      - source_records_untraceable
      - all_evidence_inputs_unusable

  HIGH_GAP:
    result: P05_READY_WITH_GAPS
    downstream_permission: P06_LIMITED
    examples:
      - counter_evidence_missing
      - evidence_conflict_unresolved
      - major_unknowns_present
      - stale_chip_structure_inputs
      - weak_same_source_inputs

  MEDIUM_GAP:
    result: P05_READY_WITH_GAPS
    downstream_permission: P06_ALLOWED_WITH_LIMITATIONS
    examples:
      - cost_basis_low_confidence
      - partial_transfer_path_unknown
      - counterparty_pressure_weak
      - security_fact_stale

  LOW_GAP:
    result: P05_READY_WITH_GAPS
    downstream_permission: P06_ALLOWED_WITH_NOTE
    examples:
      - optional_historical_context_missing
      - minor_freshness_delay
      - noncritical_evidence_metadata_missing
```

---

# 18. P05 Hard Negative Rules

```yaml
p05_hard_negative_rules:
  - rule_id: P05_BLOCK_001
    name: 未读取 P04 handoff
    condition: p04_to_p05_handoff_packet_missing == true
    result: P05_BLOCKED
    reason: P05 不能绕过 P04 / Handoff 启动

  - rule_id: P05_BLOCK_002
    name: 无 trace 生成证据
    condition: evidence_created == true and source_trace_ids_missing == true
    result: P05_BLOCKED
    reason: 证据必须可追踪

  - rule_id: P05_BLOCK_003
    name: 无证据输入
    condition: all_evidence_inputs_missing == true
    result: P05_REJECTED
    reason: 无输入不能生成 evidence object

  - rule_id: P05_BLOCK_004
    name: 把事实直接当结论
    condition: fact_record_promoted_to_scenario_or_strategy == true
    result: P05_BLOCKED
    reason: P05 只能生成证据，不生成场景或策略

  - rule_id: P05_BLOCK_005
    name: 忽略反证
    condition: supporting_evidence_created == true and counter_evidence_check_missing == true
    result: P05_BLOCKED
    reason: 专业证据系统必须检查反证

  - rule_id: P05_BLOCK_006
    name: 忽略冲突
    condition: conflict_detected == true and conflict_record_missing == true
    result: P05_BLOCKED
    reason: 冲突必须显式登记

  - rule_id: P05_BLOCK_007
    name: 弱证据升级为强证据
    condition: weak_source_used_as_strong_evidence == true
    result: P05_BLOCKED
    reason: 弱字段不能无验收升级

  - rule_id: P05_BLOCK_008
    name: 输出场景或策略
    condition: output_contains in [scenario_claim, strategy_signal, paper_ready]
    result: P05_BLOCKED
    reason: P05 越权

  - rule_id: P05_BLOCK_009
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P05_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 19. P05 状态机专业版

```yaml
p05_evidence_state_machine:
  states:
    - P05_UNINITIALIZED
    - P05_CONTEXT_LOADED
    - P05_HANDOFF_READ
    - P05_INPUT_MANIFEST_BUILT
    - P05_HYPOTHESIS_FRAMES_BUILT
    - P05_EVIDENCE_SUBJECTS_REGISTERED
    - P05_SOURCE_MATERIAL_QUALIFIED
    - P05_SUPPORTING_EVIDENCE_BUILT
    - P05_COUNTER_EVIDENCE_BUILT
    - P05_UNKNOWN_EVIDENCE_BUILT
    - P05_CONFLICT_EVIDENCE_BUILT
    - P05_ALTERNATIVE_EXPLANATIONS_BUILT
    - P05_EVIDENCE_WEIGHTS_BUILT
    - P05_EVIDENCE_BUNDLES_BUILT
    - P05_SUFFICIENCY_CHECKED
    - P05_USAGE_PERMISSIONS_BUILT
    - P05_GAP_ANALYZED
    - P05_P06_DATA_REQUEST_BUILT
    - P05_READY_FOR_ACCEPTANCE
    - P05_ACCEPTANCE_READY
    - P05_READY_FOR_P06_HANDOFF
    - P05_READY_WITH_GAPS
    - P05_REJECTED
    - P05_BLOCKED

  critical_transitions:
    - from: P05_HANDOFF_READ
      to: P05_INPUT_MANIFEST_BUILT
      condition: p04_handoff_valid == true

    - from: P05_INPUT_MANIFEST_BUILT
      to: P05_HYPOTHESIS_FRAMES_BUILT
      condition: hypothesis_frames_created == true

    - from: P05_HYPOTHESIS_FRAMES_BUILT
      to: P05_SOURCE_MATERIAL_QUALIFIED
      condition: source_material_has_trace_and_permission == true

    - from: P05_SOURCE_MATERIAL_QUALIFIED
      to: P05_SUPPORTING_EVIDENCE_BUILT
      condition: supporting_evidence_candidates_processed == true

    - from: P05_SUPPORTING_EVIDENCE_BUILT
      to: P05_COUNTER_EVIDENCE_BUILT
      condition: counter_evidence_checked == true

    - from: P05_COUNTER_EVIDENCE_BUILT
      to: P05_CONFLICT_EVIDENCE_BUILT
      condition: conflicts_checked == true

    - from: P05_CONFLICT_EVIDENCE_BUILT
      to: P05_ALTERNATIVE_EXPLANATIONS_BUILT
      condition: alternative_explanations_checked == true

    - from: P05_ALTERNATIVE_EXPLANATIONS_BUILT
      to: P05_EVIDENCE_WEIGHTS_BUILT
      condition: evidence_weights_created == true

    - from: P05_EVIDENCE_WEIGHTS_BUILT
      to: P05_EVIDENCE_BUNDLES_BUILT
      condition: evidence_bundles_created == true

    - from: P05_EVIDENCE_BUNDLES_BUILT
      to: P05_SUFFICIENCY_CHECKED
      condition: evidence_sufficiency_records_created == true

    - from: P05_SUFFICIENCY_CHECKED
      to: P05_P06_DATA_REQUEST_BUILT
      condition: p06_scenario_data_request_packet_created == true

    - from: P05_P06_DATA_REQUEST_BUILT
      to: P05_READY_FOR_ACCEPTANCE
      condition: p05_output_contract_ready == true

    - from: P05_READY_FOR_ACCEPTANCE
      to: P05_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P05_ACCEPTANCE_READY
      to: P05_READY_FOR_P06_HANDOFF
      condition: p05_to_p06_handoff_packet_created == true
```

---

# 20. P06 Scenario Data Request Packet

P05 必须告诉 P06：哪些证据束可用于哪些场景识别方向。

```yaml
p06_scenario_data_request_packet:
  packet_id: string
  from_controller: P05_EVIDENCE_CONTROLLER
  to_controller: P06_SCENARIO_RECOGNITION_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  scenario_input_bundles:
    chip_retention_bundle_path: string
    distribution_risk_bundle_path: string
    counterparty_pressure_bundle_path: string
    transfer_risk_bundle_path: string
    cost_basis_bundle_path: string
    data_uncertainty_bundle_path: string
    security_risk_bundle_path: string

  p06_required_scenario_tasks:
    - accumulation_or_retention_scenario_check
    - active_distribution_scenario_check
    - partial_distribution_or_rotation_check
    - counterparty_exit_liquidity_check
    - second_stage_expansion_precondition_check
    - data_insufficient_scenario_block_check

  usage_limitations:
    - EVIDENCE_ONLY
    - NO_STRATEGY_GATE
    - NO_PAPER_RUNTIME
    - NO_CONFIRMED_MARKET_MAKER
    - LIVE_EXECUTION_FORBIDDEN

  evidence_usage_permissions:
    full_use_evidence_ids: list
    weak_use_only_evidence_ids: list
    observe_only_evidence_ids: list
    do_not_use_evidence_ids: list

  conflicts_to_propagate:
    conflict_ids: list

  unknowns_to_propagate:
    unknown_ids: list
```

---

# 21. P05 to P06 Handoff Packet

```yaml
p05_to_p06_handoff_packet:
  packet_id: string
  packet_type: P05_TO_P06_EVIDENCE_HANDOFF
  generated_at: datetime

  route:
    from_controller: P05_EVIDENCE_CONTROLLER
    to_controller: P06_SCENARIO_RECOGNITION_CONTROLLER

  upstream_control:
    p04_handoff_packet_id: string
    p05_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    candidate_count_evidence_ready: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  evidence_package:
    evidence_input_manifest_path: string
    hypothesis_frame_records_path: string
    evidence_object_records_path: string
    supporting_evidence_records_path: string
    counter_evidence_records_path: string
    weak_evidence_records_path: string
    unknown_evidence_records_path: string
    evidence_conflict_records_path: string
    alternative_explanation_records_path: string
    evidence_weight_records_path: string
    evidence_bundle_records_path: string
    evidence_sufficiency_records_path: string
    evidence_usage_permission_records_path: string

  p06_data_request:
    p06_scenario_data_request_packet_path: string
    required_p06_tasks: list
    scenario_input_bundle_paths: list

  quality:
    evidence_quality_report_path: string
    evidence_sufficiency_summary: object
    counter_evidence_summary: object
    conflict_summary: object
    unknown_summary: object

  limitations:
    - EVIDENCE_OBJECTS_ONLY
    - NO_SCENARIO_CLAIM
    - NO_STRATEGY_GATE
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P06_SCENARIO_RECOGNITION_CONTROLLER
    forbidden:
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p06_must_read_first:
      - p05_to_p06_handoff_packet
      - p06_scenario_data_request_packet
      - evidence_bundle_records
      - counter_evidence_records
      - evidence_conflict_records
      - unknown_evidence_records
      - evidence_usage_permission_records
```

---

# 22. P05 文件体系

## 22.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p05_evidence_controller/
```

必须创建：

```text
p05_evidence_controller.yaml
p05_evidence_context.md
p05_input_contract.yaml
p05_output_contract.yaml
evidence_input_manifest_schema.yaml
evidence_subject_registry_schema.yaml
hypothesis_frame_schema.yaml
evidence_object_schema.yaml
supporting_evidence_schema.yaml
counter_evidence_schema.yaml
weak_evidence_schema.yaml
unknown_evidence_schema.yaml
evidence_conflict_schema.yaml
alternative_explanation_schema.yaml
evidence_chain_schema.yaml
evidence_weight_schema.yaml
evidence_bundle_schema.yaml
evidence_sufficiency_schema.yaml
evidence_usage_permission_schema.yaml
evidence_taxonomy.yaml
evidence_conversion_policy.yaml
counter_evidence_policy.yaml
conflict_resolution_policy.yaml
unknown_evidence_policy.yaml
alternative_explanation_policy.yaml
evidence_weighting_policy.yaml
evidence_sufficiency_policy.yaml
evidence_gap_policy.yaml
evidence_hard_negative_rules.yaml
evidence_state_machine.yaml
evidence_trace_requirements.yaml
p06_scenario_data_request_packet_contract.yaml
p05_to_p06_handoff_contract.yaml
p05_acceptance_criteria.md
p05_storage_constitution.md
p05_test_matrix.yaml
p05_report_model.yaml
p05_review_checklist.md
her_p05_execution_protocol.md
```

---

## 22.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p05_evidence/
  input_manifest/
  evidence_subjects/
  hypothesis_frames/
  evidence_objects/
  supporting_evidence/
  counter_evidence/
  weak_evidence/
  unknown_evidence/
  conflicts/
  alternative_explanations/
  evidence_chains/
  evidence_weights/
  evidence_bundles/
  sufficiency/
  usage_permissions/
  quality/
  gaps/
  p06_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 23. P05 测试矩阵

```yaml
p05_test_matrix:
  - test_id: P05_TEST_001
    name: 正常 P04 handoff，筹码留存强，反证弱
    expected_status: P05_READY_FOR_P06_HANDOFF
    expected_output: CHIP_RETENTION_BUNDLE

  - test_id: P05_TEST_002
    name: 缺 P04 handoff
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_003
    name: 无 trace 的证据输入
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_004
    name: 早期钱包大量清仓
    expected_output: EARLY_WALLET_EXIT_COUNTER

  - test_id: P05_TEST_005
    name: 高对手盘压力
    expected_output: COUNTERPARTY_PRESSURE_COUNTER_EVIDENCE

  - test_id: P05_TEST_006
    name: 同时存在高留存与未知大额转出
    expected_output: EVIDENCE_CONFLICT_RECORD

  - test_id: P05_TEST_007
    name: 供应量分母不确定
    expected_output: UNKNOWN_EVIDENCE_RECORD
    expected_limitation: WEAK_USE_ONLY

  - test_id: P05_TEST_008
    name: 弱同源组输入被当强证据
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_009
    name: 支持证据生成但未检查反证
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_010
    name: P05 输出 scenario claim
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_011
    name: P05 输出 paper_ready
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_012
    name: live execution requested
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_013
    name: 成本区域质量低但被强使用
    expected_status: P05_BLOCKED

  - test_id: P05_TEST_014
    name: evidence conflicts unresolved
    expected_status: P05_READY_WITH_GAPS
    expected_limitation: CONFLICT_PROPAGATION_REQUIRED
```

---

# 24. P05 报告模型

```yaml
p05_evidence_report:
  report_id: string
  generated_at: datetime
  controller_id: P05_EVIDENCE_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    evidence_ready_count: integer
    ready_with_gaps_count: integer
    rejected_count: integer
    blocked_count: integer

  evidence_summary:
    total_evidence_objects: integer
    supporting_evidence_count: integer
    counter_evidence_count: integer
    weak_evidence_count: integer
    unknown_evidence_count: integer
    conflict_evidence_count: integer

  bundle_summary:
    chip_retention_bundle_count: integer
    distribution_risk_bundle_count: integer
    counterparty_pressure_bundle_count: integer
    transfer_risk_bundle_count: integer
    data_uncertainty_bundle_count: integer

  quality_summary:
    strong_evidence_count: integer
    moderate_evidence_count: integer
    weak_evidence_count: integer
    conflicted_evidence_count: integer
    unknown_evidence_count: integer

  counter_evidence_summary:
    strong_counter_count: integer
    moderate_counter_count: integer
    weak_counter_count: integer

  conflict_summary:
    blocking_conflict_count: integer
    high_conflict_count: integer
    unresolved_conflict_ids: list

  unknown_summary:
    unknown_scope_distribution: object
    major_unknowns: list

  p06_handoff_summary:
    p06_handoff_ready: boolean
    p06_limited_candidates: integer
    p06_required_tasks: list

  compliance:
    scenario_claim_generated: false
    strategy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
    weak_evidence_upgraded_without_permission: false
```

---

# 25. HER P05 执行协议

```text
HER 执行 P05 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P05 controller context
4. 读取 P04 → P05 handoff packet
5. 读取 p05_evidence_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P05 input_manifest
8. 建立 evidence_subject_registry
9. 建立 hypothesis_frame_records
10. 校验 source material trace 和 field usage permission
11. 生成 evidence_object_records
12. 生成 supporting_evidence_records
13. 生成 counter_evidence_records
14. 生成 weak_evidence_records
15. 生成 unknown_evidence_records
16. 生成 evidence_conflict_records
17. 生成 alternative_explanation_records
18. 生成 evidence_chain_records
19. 生成 evidence_weight_records
20. 生成 evidence_bundle_records
21. 执行 evidence_sufficiency_check
22. 生成 evidence_usage_permission_records
23. 生成 P05 gap report
24. 生成 p06_scenario_data_request_packet
25. 写入 P05 trace
26. 生成 p05_evidence_report
27. 生成 p05_to_p06_handoff_packet
28. 执行 P05 acceptance
29. 只允许 handoff 给 P06
```

禁止：

```text
1. 不允许无 P04 handoff 启动 P05
2. 不允许无 trace 生成 evidence object
3. 不允许事实直接升级为场景结论
4. 不允许只生成支持证据而不检查反证
5. 不允许忽略冲突证据
6. 不允许弱证据升级为强证据
7. 不允许输出 scenario
8. 不允许输出 strategy signal
9. 不允许输出 paper_ready
10. 不允许进入 paper runtime
11. 不允许任何 live execution
```

---

# 26. 给 HER 的专业化任务书

```text
任务名称：建立 P05 Evidence Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p05_evidence_controller/ 下建立 P05 Evidence Controller。该控制器不是普通证据摘要模块，也不是场景判断模块，而是证据对象、反证对象、冲突证据、未知证据、证据束和 P06 场景识别交接控制器。它负责读取 P04 Chip Structure Controller 输出的筹码结构状态，以及 P02 / P03 / P04 的可追踪事实，把它们转化为 evidence objects、counter evidence、unknown evidence、conflict evidence、alternative explanations、evidence bundles、evidence sufficiency records，并生成 P06 Scenario Data Request Packet 与 P05→P06 Handoff Packet。

核心原则：
1. P05 只生成证据对象，不识别场景。
2. P05 不做策略准入。
3. P05 不进入 paper runtime。
4. P05 不允许 live execution。
5. 每条证据必须绑定 hypothesis frame。
6. 每条证据必须有 source trace 和 field trace。
7. 支持证据必须检查反证。
8. 冲突证据必须显式登记。
9. 弱证据不能被无权限升级为强证据。
10. P05 必须生成 P06 Scenario Data Request Packet。
11. P05 只能交接给 P06 Scenario Recognition Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p05_evidence_controller/

需要创建系统文件：
1. p05_evidence_controller.yaml
2. p05_evidence_context.md
3. p05_input_contract.yaml
4. p05_output_contract.yaml
5. evidence_input_manifest_schema.yaml
6. evidence_subject_registry_schema.yaml
7. hypothesis_frame_schema.yaml
8. evidence_object_schema.yaml
9. supporting_evidence_schema.yaml
10. counter_evidence_schema.yaml
11. weak_evidence_schema.yaml
12. unknown_evidence_schema.yaml
13. evidence_conflict_schema.yaml
14. alternative_explanation_schema.yaml
15. evidence_chain_schema.yaml
16. evidence_weight_schema.yaml
17. evidence_bundle_schema.yaml
18. evidence_sufficiency_schema.yaml
19. evidence_usage_permission_schema.yaml
20. evidence_taxonomy.yaml
21. evidence_conversion_policy.yaml
22. counter_evidence_policy.yaml
23. conflict_resolution_policy.yaml
24. unknown_evidence_policy.yaml
25. alternative_explanation_policy.yaml
26. evidence_weighting_policy.yaml
27. evidence_sufficiency_policy.yaml
28. evidence_gap_policy.yaml
29. evidence_hard_negative_rules.yaml
30. evidence_state_machine.yaml
31. evidence_trace_requirements.yaml
32. p06_scenario_data_request_packet_contract.yaml
33. p05_to_p06_handoff_contract.yaml
34. p05_acceptance_criteria.md
35. p05_storage_constitution.md
36. p05_test_matrix.yaml
37. p05_report_model.yaml
38. p05_review_checklist.md
39. her_p05_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p05_evidence/
  input_manifest/
  evidence_subjects/
  hypothesis_frames/
  evidence_objects/
  supporting_evidence/
  counter_evidence/
  weak_evidence/
  unknown_evidence/
  conflicts/
  alternative_explanations/
  evidence_chains/
  evidence_weights/
  evidence_bundles/
  sufficiency/
  usage_permissions/
  quality/
  gaps/
  p06_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p05_evidence_controller.yaml：定义 P05 身份、职责、权限、上下游、状态码、禁止事项。
- p05_evidence_context.md：写成 HER 执行前必须读取的 P05 上下文。
- p05_input_contract.yaml：定义 P05 必须读取的 P04 handoff、chip structure records、P03 wallet entity records、P02 data facts、field usage permission、limitation tags。
- p05_output_contract.yaml：定义 evidence objects、counter evidence、unknown evidence、conflict evidence、evidence bundles、P06 request、handoff 输出。
- evidence_input_manifest_schema.yaml：定义 P05 接收的全部证据输入。
- evidence_subject_registry_schema.yaml：定义证据作用对象。
- hypothesis_frame_schema.yaml：定义证据支持或反驳的假设框架。
- evidence_object_schema.yaml：定义标准证据对象。
- supporting_evidence_schema.yaml：定义支持证据。
- counter_evidence_schema.yaml：定义反证。
- weak_evidence_schema.yaml：定义弱证据。
- unknown_evidence_schema.yaml：定义未知证据。
- evidence_conflict_schema.yaml：定义冲突证据。
- alternative_explanation_schema.yaml：定义替代解释。
- evidence_chain_schema.yaml：定义证据链。
- evidence_weight_schema.yaml：定义证据权重，不允许单一总分覆盖维度。
- evidence_bundle_schema.yaml：定义证据束。
- evidence_sufficiency_schema.yaml：定义证据充分性。
- evidence_usage_permission_schema.yaml：定义 P06 使用权限。
- evidence_taxonomy.yaml：定义所有证据类型。
- evidence_conversion_policy.yaml：定义事实和结构状态如何转成证据。
- counter_evidence_policy.yaml：定义反证检查规则。
- conflict_resolution_policy.yaml：定义冲突证据处理。
- unknown_evidence_policy.yaml：定义 UNKNOWN 的专业表达。
- alternative_explanation_policy.yaml：定义替代解释生成规则。
- evidence_weighting_policy.yaml：定义证据权重规则。
- evidence_sufficiency_policy.yaml：定义是否足够进入 P06。
- evidence_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- evidence_hard_negative_rules.yaml：定义无 P04 handoff、无 trace、忽略反证、忽略冲突、弱证据升级、输出场景、输出策略、自动实盘等阻断。
- evidence_state_machine.yaml：定义 P05 全状态机。
- evidence_trace_requirements.yaml：定义 evidence trace、source trace、field trace、bundle trace、handoff trace。
- p06_scenario_data_request_packet_contract.yaml：定义 P05 给 P06 的场景识别数据请求包。
- p05_to_p06_handoff_contract.yaml：定义 P05_TO_P06 handoff packet。
- p05_acceptance_criteria.md：定义 P05_READY、P05_READY_WITH_GAPS、P05_REJECTED、P05_BLOCKED。
- p05_storage_constitution.md：定义系统文件与运行数据目录。
- p05_test_matrix.yaml：定义至少 14 个测试场景。
- p05_report_model.yaml：定义 P05 人类可读报告。
- p05_review_checklist.md：定义审计清单。
- her_p05_execution_protocol.md：定义 HER 执行 P05 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P05_READY / P05_READY_WITH_GAPS / P05_REJECTED / P05_BLOCKED 判断
4. hypothesis_frame 摘要
5. evidence_object 摘要
6. supporting_evidence 摘要
7. counter_evidence 摘要
8. unknown_evidence 摘要
9. conflict_evidence 摘要
10. alternative_explanation 摘要
11. evidence_bundle 摘要
12. evidence_sufficiency 摘要
13. evidence_usage_permission 摘要
14. p06_scenario_data_request_packet 摘要
15. p05_to_p06_handoff_packet 摘要
16. P05 阻断规则摘要
17. P05 测试矩阵摘要
18. 当前缺口清单
19. 是否达到轻量机构级 P05 v3.0

最终验收标准：
只有当 P05 具备 evidence input manifest、evidence subject registry、hypothesis frame、evidence object、supporting evidence、counter evidence、weak evidence、unknown evidence、conflict evidence、alternative explanation、evidence chain、evidence weight、evidence bundle、evidence sufficiency、usage permission、evidence taxonomy、conversion policy、counter evidence policy、conflict policy、unknown policy、alternative explanation policy、weighting policy、sufficiency policy、gap policy、hard negative rules、state machine、trace requirements、P06 data request、P05 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P05 不能识别 scenario、不能输出 strategy、不能进入 paper runtime 或 live execution 时，才允许标记为 P05_READY。
```

---

# 27. 当前是否达到专业化标准

## 判断

这一版 P05 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是证据摘要脚本
```

P05 被明确升级为：

```text
证据对象层
反证系统层
冲突证据层
未知证据层
替代解释层
证据权重层
证据束层
P06 场景识别输入层
```

---

# 28. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Evidence Input Manifest|已补齐|
|Evidence Subject Registry|已补齐|
|Hypothesis Frame|已补齐|
|Evidence Object|已补齐|
|Supporting Evidence|已补齐|
|Counter Evidence|已补齐|
|Weak Evidence|已补齐|
|Unknown Evidence|已补齐|
|Evidence Conflict|已补齐|
|Alternative Explanation|已补齐|
|Evidence Chain|已补齐|
|Evidence Weight|已补齐|
|Evidence Bundle|已补齐|
|Evidence Sufficiency|已补齐|
|Usage Permission|已补齐|
|P06 Scenario Data Request|已补齐|
|P05 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 29. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|evidence weighting 权重未回测|已定义维度|P09 / P10 校准|
|hypothesis frame 需要与 P06 场景体系对齐|已定义输入|P06 展开时校准|
|替代解释生成规则需要样本验证|已定义模型|Review / Replay 后校准|
|冲突证据 resolution 阈值未定|已定义状态|P10 升级|
|P05 不能识别场景|已明确边界|P06 处理|
|P05 不能策略准入|已明确边界|P07 处理|
|P05 handoff 未联调|需要 P06|下一阶段展开 P06|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P05 的本质不是证据摘要，而是证据对象系统。**
    
2. **每条证据必须绑定假设框架。**  
    没有支持或反驳对象的材料，不是证据，只是事实。
    
3. **支持证据必须配反证检查。**  
    只堆正向材料会导致系统自我确认偏差。
    
4. **未知也是一种专业输出。**  
    数据不足时必须输出 UNKNOWN，而不是强行解释。
    
5. **冲突证据必须显式保留。**  
    多源冲突、事实冲突、时间冲突不能被静默覆盖。
    
6. **替代解释是防止误判的核心。**  
    例如部分卖出既可能是派发，也可能是轮换、风险释放或内部转移。
    
7. **P05 只能交接给 P06。**  
    任何跳过 P06 直接进入策略或 runtime 的路径都必须阻断。
    
8. **P05 的输出是 P06 的场景识别材料，不是策略结论。**