# P07 Strategy Gate Controller 专业版 v3.0

## 策略准入、阻断、暂停、观察、纸面候选与 P08 执行风控交接控制器

---

## 0. 先修正 P07 的定位

P07 不能被设计成普通的：

```text
买入信号模块
策略打分模块
交易触发器
纸面交易启动器
实盘确认器
```

P07 的专业定位应该是：

```text
把 P06 场景识别结果、P05 证据束、P04 筹码结构、P03 钱包实体候选、P02 数据质量和 Governance 硬规则，
转化为策略层的 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED 裁决。
```

一句话定义：

> **P06 负责识别当前更像什么场景。**  
> **P07 负责判断这个场景是否允许进入策略候选层。**  
> **P08 才负责执行前风控、报价、安全、滑点、纸面运行许可。**

P07 可以输出：

```text
OBSERVE
PAUSE
BLOCK
PAPER_CANDIDATE
HUMAN_CONFIRMATION_REQUIRED
STRATEGY_GATE_REJECTED
```

P07 不能输出：

```text
实盘买入
自动下单
钱包签名
PAPER_RUNTIME_STARTED
LIVE_EXECUTION_ALLOWED
```

---

# 1. P07 阶段核心目标

P07 必须一次性解决 17 个问题：

|编号|核心问题|P07 必须输出|
|---|---|---|
|1|P06 场景是否允许进入策略评估？|`scenario_gate_evaluation_record`|
|2|P05 证据是否足够支撑策略候选？|`evidence_gate_evaluation_record`|
|3|P04 筹码结构是否支持或阻断策略？|`chip_structure_gate_evaluation_record`|
|4|是否触发治理硬否定规则？|`hard_negative_evaluation_record`|
|5|是否存在场景冲突或 UNKNOWN 风险？|`scenario_conflict_gate_record`|
|6|是否适配某个策略模板？|`strategy_pattern_fit_record`|
|7|当前是否太早、太晚、追高、接盘？|`market_position_context_gate_record`|
|8|是否需要观察、暂停、阻断或进入纸面候选？|`strategy_gate_decision_record`|
|9|如果进入候选，进入哪类策略候选？|`strategy_candidate_record`|
|10|如果暂停，等待什么条件？|`pause_condition_record`|
|11|如果观察，观察什么数据？|`observe_condition_record`|
|12|如果阻断，阻断原因是什么？|`strategy_block_reason_record`|
|13|是否需要人工确认？|`human_confirmation_requirement_record`|
|14|需要 P08 检查哪些执行风险？|`p08_execution_risk_data_request_packet`|
|15|P07 不能直接运行的限制是什么？|`strategy_usage_permission_record`|
|16|如何向 P08 交接？|`p07_to_p08_handoff_packet`|
|17|当前决策是否可复盘？|`strategy_gate_audit_record`|

---

# 2. P07 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|策略准入官|是否允许进入策略候选|`strategy_gate_decision_record`|
|硬否定审查官|是否有一票否决|`hard_negative_evaluation_record`|
|证据审查官|证据是否足够、是否有反证|`evidence_gate_evaluation_record`|
|场景适配官|场景是否适配策略模板|`strategy_pattern_fit_record`|
|筹码风险官|筹码结构是否支持或阻断|`chip_structure_gate_evaluation_record`|
|位置上下文官|当前是否早、晚、追高或接盘|`market_position_context_gate_record`|
|暂停观察官|未成熟样本如何观察|`pause_condition_record` / `observe_condition_record`|
|执行交接官|交给 P08 检查报价、安全、滑点、纸面许可|`p08_execution_risk_data_request_packet`|

---

# 3. P07 底层方法论

## 3.1 Gate 不是 Signal

P07 输出的是策略门控裁决，不是交易执行信号。

```text
PAPER_CANDIDATE ≠ PAPER_RUNTIME_ALLOWED
PAPER_CANDIDATE ≠ BUY_SIGNAL
PAPER_CANDIDATE ≠ LIVE_TRADE
```

P07 只能说：

```text
这个样本是否值得交给 P08 做执行前风控检查。
```

---

## 3.2 先否定，再准入

专业策略门控必须先检查硬否定：

```text
先看不能做什么
再看是否值得观察
最后才看是否能进入纸面候选
```

顺序必须是：

```text
Governance hard negative
  ↓
Handoff / Trace / Acceptance 检查
  ↓
P06 场景风险检查
  ↓
P05 证据充分性检查
  ↓
P04 筹码结构风险检查
  ↓
P02/P03 数据质量检查
  ↓
策略模板适配
  ↓
位置上下文
  ↓
P07 裁决
```

---

## 3.3 策略适配不能只看场景

例如 P06 输出：

```text
SECOND_STAGE_EXPANSION_CANDIDATE
```

仍然不能直接进入纸面候选。

还必须检查：

```text
证据是否足够
反证是否可接受
筹码是否未明显派发
对手盘压力是否不过高
场景冲突是否可控
位置是否不是明显追高
P08 是否可以继续检查报价、安全和滑点
```

---

## 3.4 UNKNOWN 与 CONFLICT 是策略风险，不是空值

P07 对 UNKNOWN 的处理必须明确：

```text
UNKNOWN 不能默认通过
CONFLICT 不能默认忽略
WEAK_USE_ONLY 不能默认强使用
```

UNKNOWN 可以导致：

```text
OBSERVE
PAUSE
HUMAN_CONFIRMATION_REQUIRED
BLOCK
```

---

## 3.5 轻量机构级 Gate 必须保留决策原因

每一次 P07 裁决都必须能回答：

```text
为什么观察？
为什么暂停？
为什么阻断？
为什么进入纸面候选？
哪些证据支持？
哪些反证存在？
哪些条件失效后要退出？
P08 还必须检查什么？
```

---

# 4. P07 必须支持的策略裁决状态

```yaml
strategy_gate_decision_statuses:
  OBSERVE:
    meaning: 可以继续观察，但当前不允许进入 P08
    downstream: NO_P08_RUNTIME_CHECK

  PAUSE:
    meaning: 当前结构可能有价值，但存在关键缺口、冲突或等待条件
    downstream: WAIT_FOR_REFRESH_OR_CONDITION

  BLOCK:
    meaning: 触发硬否定或关键风险，不允许继续
    downstream: STOP_DOWNSTREAM

  PAPER_CANDIDATE:
    meaning: 允许交给 P08 做执行前风控与纸面运行许可检查
    downstream: P08_EXECUTION_RISK_REQUIRED

  HUMAN_CONFIRMATION_REQUIRED:
    meaning: 系统无法自动裁决，需要人工确认后才可继续
    downstream: P08_OR_MANUAL_REVIEW_DEPENDS_ON_APPROVAL

  STRATEGY_GATE_REJECTED:
    meaning: 不符合当前策略系统目标
    downstream: STOP_DOWNSTREAM
```

---

# 5. P07 必须建立的核心对象

|对象|作用|
|---|---|
|`Strategy Gate Input Manifest`|记录 P07 接收的场景、证据、筹码、限制|
|`Strategy Policy Registry`|策略门控规则注册|
|`Hard Negative Evaluation Record`|一票否决检查|
|`Scenario Gate Evaluation Record`|场景是否可用于策略|
|`Evidence Gate Evaluation Record`|证据是否足够支撑策略候选|
|`Chip Structure Gate Evaluation Record`|筹码结构是否支持或阻断|
|`Data Quality Gate Evaluation Record`|数据质量能否支撑门控|
|`Scenario Conflict Gate Record`|场景冲突如何处理|
|`Market Position Context Gate Record`|早晚、追高、接盘上下文|
|`Strategy Pattern Fit Record`|策略模板适配结果|
|`Strategy Risk Flag Evaluation Record`|风险标签处理|
|`Strategy Invalidation Binding Record`|失效条件绑定|
|`Pause Condition Record`|暂停条件|
|`Observe Condition Record`|观察条件|
|`Strategy Block Reason Record`|阻断原因|
|`Strategy Candidate Record`|纸面候选策略对象|
|`Human Confirmation Requirement Record`|人工确认要求|
|`Strategy Gate Decision Record`|P07 最终裁决|
|`Strategy Usage Permission Record`|下游使用权限|
|`P08 Execution Risk Data Request Packet`|给 P08 的执行风控请求|
|`P07 to P08 Handoff Packet`|P07 → P08 交接包|

---

# 6. P07 输入：必须读取什么

```yaml
p07_required_inputs:
  from_p06:
    - p06_to_p07_handoff_packet
    - p07_strategy_gate_data_request_packet
    - primary_scenario_candidate_records
    - secondary_scenario_candidate_records
    - scenario_rejection_records
    - scenario_conflict_records
    - scenario_unknown_records
    - scenario_confidence_records
    - scenario_transition_records
    - scenario_context_interpretation_records
    - scenario_invalidation_records
    - scenario_watch_condition_records
    - scenario_risk_flag_records
    - scenario_usage_permission_records

  from_p05:
    - evidence_bundle_records
    - counter_evidence_records
    - evidence_conflict_records
    - unknown_evidence_records
    - evidence_sufficiency_records
    - evidence_usage_permission_records

  from_p04:
    - chip_structure_score_records
    - chip_structure_quality_records
    - early_wallet_retention_records
    - structural_group_holding_records
    - distribution_progress_records
    - counterparty_pressure_records
    - chip_transfer_status_records
    - chip_cost_basis_records

  from_p02:
    - market_fact_records
    - market_structure_fact_seed
    - security_fact_records
    - data_quality_report
    - freshness_report
    - data_conflict_report

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - limitation_transfer_packet
    - forbidden_use_policy
    - governance_handoff_packet
    - domain_strategy_policy_handoff

  required_contracts:
    - p07_input_contract
    - p07_output_contract
    - strategy_gate_decision_contract
    - strategy_candidate_contract
    - p08_execution_risk_input_contract
```

P07 启动前必须确认：

```text
P06 已验收
P06 handoff 已生成
P07 只读取 Handoff 授权字段
P06 输出是 scenario，不是 strategy decision
P05 输出是 evidence，不是 strategy permission
P04 输出是 chip structure，不是 buy signal
P07 不允许 paper runtime
P07 不允许 live execution
```

---

# 7. Strategy Gate Input Manifest

```yaml
strategy_gate_input_manifest:
  manifest_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  upstream_packets:
    p06_handoff_packet_id: string
    p07_strategy_gate_data_request_packet_id: string
    trace_handoff_packet_id: string
    acceptance_result_packet_id: string

  input_availability:
    primary_scenario_available: boolean
    scenario_conflict_available: boolean
    scenario_invalidation_available: boolean
    evidence_bundle_available: boolean
    chip_structure_available: boolean
    market_context_available: boolean
    security_context_available: boolean

  inherited_limitations:
    limitation_tags: list
    forbidden_uses: list
    weak_use_only_items: list
    observe_only_items: list
    do_not_use_items: list

  input_quality:
    scenario_input_quality_status: string
    evidence_input_quality_status: string
    chip_structure_quality_status: string
    data_quality_status: string
    overall_gate_input_quality:
      - GATE_INPUT_HIGH_CONFIDENCE
      - GATE_INPUT_USABLE
      - GATE_INPUT_USABLE_WITH_GAPS
      - GATE_INPUT_LOW_CONFIDENCE
      - GATE_INPUT_UNUSABLE

  trace:
    strategy_gate_input_trace_id: string
    upstream_trace_ids: list
```

---

# 8. Strategy Policy Registry

P07 必须有策略政策注册，而不是硬写一个判断。

```yaml
strategy_policy_registry:
  registry_id: STRATEGY_POLICY_REGISTRY
  version: v3.0

  supported_strategy_profiles:
    - strategy_profile_id: SIKK_B_CONTROL_BOX_BREAKOUT_PULLBACK
      name_cn: 控盘箱体突破回踩纸面候选策略
      allowed_scenario_inputs:
        - CONTROL_BOX_ACCUMULATION
        - CONTROL_BOX_BREAKOUT
        - SECOND_STAGE_EXPANSION
        - SHAKEOUT_BEFORE_EXPANSION
      hard_block_scenarios:
        - ACTIVE_DISTRIBUTION
        - EXIT_LIQUIDITY_TRAP
        - FINAL_PUMP_DISTRIBUTION
      required_supporting_bundles:
        - CHIP_RETENTION_BUNDLE
        - STRUCTURAL_GROUP_HOLDING_SUPPORT
      required_negative_checks:
        - high_counterparty_pressure_not_present
        - active_distribution_not_present
        - scenario_conflict_not_blocking

    - strategy_profile_id: SIKK_R_REACCUMULATION_REACTIVATION
      name_cn: 再吸筹 / 再激活纸面候选策略
      allowed_scenario_inputs:
        - REACCUMULATION
        - FAILED_DISTRIBUTION_REACCUMULATION
        - INTERNAL_ROTATION
      hard_block_scenarios:
        - LATE_DISTRIBUTION
        - DOWNWARD_DISTRIBUTION
        - EXIT_LIQUIDITY_TRAP
      required_supporting_bundles:
        - retention_or_reaccumulation_support
        - distribution_risk_not_dominant

    - strategy_profile_id: SIKK_OBSERVE_ONLY_HIGH_CONFLICT
      name_cn: 高冲突观察策略
      allowed_scenario_inputs:
        - SCENARIO_CONFLICTED
        - DATA_INSUFFICIENT
        - OBSERVE_ONLY
      output_decision_allowed:
        - OBSERVE
        - PAUSE
        - BLOCK
      paper_candidate_allowed: false

  global_strategy_constraints:
    live_execution_allowed: false
    paper_runtime_requires_p08: true
    strategy_gate_not_execution_layer: true
```

---

# 9. Hard Negative Evaluation Record

硬否定必须优先执行。

```yaml
hard_negative_evaluation_record:
  hard_negative_eval_id: string
  candidate_id: string
  evaluated_at: datetime

  checks:
    - check_id: GOV_LIVE_EXECUTION_FORBIDDEN
      source: GOVERNANCE_PLANE
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: TRACE_OR_HANDOFF_MISSING
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: ACTIVE_DISTRIBUTION_RISK
      source: P06_SCENARIO_RISK_FLAG
      triggered: boolean
      severity: HARD_BLOCK_OR_PAUSE

    - check_id: EXIT_LIQUIDITY_TRAP_RISK
      source: P06_SCENARIO_RISK_FLAG
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: BLOCKING_SCENARIO_CONFLICT
      source: P06_SCENARIO_CONFLICT
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: STRONG_COUNTER_EVIDENCE
      source: P05_COUNTER_EVIDENCE
      triggered: boolean
      severity: HARD_BLOCK_OR_PAUSE

    - check_id: CHIP_STRUCTURE_UNUSABLE
      source: P04_CHIP_STRUCTURE_QUALITY
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: DATA_FACT_UNUSABLE
      source: P02_DATA_QUALITY
      triggered: boolean
      severity: HARD_BLOCK

    - check_id: SECURITY_CRITICAL_RISK
      source: P02_SECURITY_FACT
      triggered: boolean
      severity: HARD_BLOCK_UNTIL_P08_RECHECK

  result:
    hard_negative_triggered: boolean
    triggered_rules: list
    hard_negative_result:
      - NO_HARD_NEGATIVE
      - BLOCK
      - PAUSE
      - HUMAN_CONFIRMATION_REQUIRED

  downstream_effect:
    if_blocked_no_p08_handoff: boolean
    if_pause_requires_watch_conditions: boolean

  trace:
    hard_negative_trace_id: string
    source_trace_ids: list
```

---

# 10. Scenario Gate Evaluation Record

```yaml
scenario_gate_evaluation_record:
  scenario_gate_eval_id: string
  candidate_id: string

  primary_scenario:
    scenario_type: string | null
    scenario_confidence_level: string | null
    p07_usage_permission: string

  secondary_scenarios:
    - scenario_type: string
      relationship_to_primary: string
      risk_overlay: boolean

  rejected_scenarios:
    rejected_scenario_ids: list

  scenario_eval:
    scenario_allowed_for_strategy_gate: boolean
    scenario_requires_pause: boolean
    scenario_requires_observe: boolean
    scenario_blocks_strategy: boolean

  reasons:
    allowed_reason_cn: string | null
    pause_reason_cn: string | null
    block_reason_cn: string | null

  limitations:
    weak_use_only_scenarios: list
    observe_only_scenarios: list
    do_not_use_scenarios: list

  trace:
    scenario_gate_trace_id: string
    scenario_trace_ids: list
```

---

# 11. Evidence Gate Evaluation Record

```yaml
evidence_gate_evaluation_record:
  evidence_gate_eval_id: string
  candidate_id: string

  evidence_inputs:
    supporting_bundle_ids: list
    counter_evidence_ids: list
    unknown_evidence_ids: list
    conflict_ids: list
    sufficiency_record_ids: list

  evidence_eval:
    supporting_evidence_sufficient: boolean
    counter_evidence_acceptable: boolean
    conflicts_acceptable: boolean
    unknowns_acceptable: boolean
    evidence_usage_permission_valid: boolean

  evidence_status:
    - EVIDENCE_SUPPORTS_GATE
    - EVIDENCE_SUPPORTS_WITH_LIMITATIONS
    - EVIDENCE_WEAK_OBSERVE_ONLY
    - EVIDENCE_CONFLICTED_PAUSE
    - EVIDENCE_BLOCKS_GATE

  evidence_gate_score_dimensions:
    support_strength_score: number
    counter_pressure_score: number
    conflict_pressure_score: number
    unknown_pressure_score: number
    trace_quality_score: number

  no_single_score_policy:
    enabled: true

  downstream_effect:
    may_enter_paper_candidate: boolean
    must_pause: boolean
    must_observe: boolean
    must_block: boolean
```

---

# 12. Chip Structure Gate Evaluation Record

```yaml
chip_structure_gate_evaluation_record:
  chip_gate_eval_id: string
  candidate_id: string

  chip_inputs:
    early_wallet_retention_id: string | null
    structural_group_holding_id: string | null
    distribution_progress_id: string | null
    counterparty_pressure_id: string | null
    transfer_status_id: string | null
    cost_basis_id: string | null

  chip_support_checks:
    early_wallet_retention_supportive: boolean | null
    structural_group_holding_supportive: boolean | null
    chip_transfer_risk_acceptable: boolean | null
    distribution_progress_acceptable: boolean | null
    counterparty_pressure_acceptable: boolean | null
    cost_basis_usable: boolean | null

  chip_gate_status:
    - CHIP_SUPPORTS_GATE
    - CHIP_SUPPORTS_WITH_LIMITATIONS
    - CHIP_NEUTRAL_OBSERVE
    - CHIP_RISK_PAUSE
    - CHIP_BLOCKS_GATE
    - CHIP_UNKNOWN

  risk_reasons:
    - EARLY_WALLET_MOSTLY_EXITED
    - STRUCTURAL_GROUP_HOLDING_WEAK
    - ACTIVE_DISTRIBUTION_CANDIDATE
    - HIGH_COUNTERPARTY_PRESSURE
    - UNEXPLAINED_TRANSFER_RISK
    - COST_BASIS_UNUSABLE
    - CHIP_DATA_STALE

  downstream_effect:
    may_enter_paper_candidate: boolean
    p08_must_recheck_wallet_delta: boolean
    p08_must_recheck_holder_snapshot: boolean
```

---

# 13. Data Quality Gate Evaluation Record

```yaml
data_quality_gate_evaluation_record:
  data_gate_eval_id: string
  candidate_id: string

  inputs:
    p02_data_quality_status: string
    p03_wallet_entity_quality_status: string
    p04_chip_structure_quality_status: string
    p05_evidence_quality_status: string
    p06_scenario_quality_status: string

  quality_checks:
    trace_complete: boolean
    freshness_acceptable: boolean
    major_conflicts_absent: boolean
    weak_use_only_not_overused: boolean
    required_fields_available: boolean

  data_gate_status:
    - DATA_SUPPORTS_GATE
    - DATA_SUPPORTS_WITH_LIMITATIONS
    - DATA_REQUIRES_REFRESH
    - DATA_OBSERVE_ONLY
    - DATA_BLOCKS_GATE

  required_refresh:
    - WALLET_DELTA
    - HOLDER_SNAPSHOT
    - QUOTE
    - SECURITY_SCAN
    - KLINE
    - MARKET_CAP
    - LIQUIDITY
```

---

# 14. Scenario Conflict Gate Record

```yaml
scenario_conflict_gate_record:
  conflict_gate_id: string
  candidate_id: string

  scenario_conflicts:
    conflict_ids: list
    conflict_types: list
    conflict_severity_max:
      - BLOCKING_CONFLICT
      - HIGH_CONFLICT
      - MEDIUM_CONFLICT
      - LOW_CONFLICT
      - NO_CONFLICT

  gate_action:
    - ALLOW_WITH_RISK_FLAG
    - PAUSE_UNTIL_RESOLVED
    - OBSERVE_ONLY
    - BLOCK

  examples:
    second_stage_vs_final_pump_distribution:
      action_if_high_conflict: PAUSE_UNTIL_RESOLVED
      action_if_blocking_conflict: BLOCK

    accumulation_vs_active_distribution:
      action_if_unresolved: BLOCK_OR_PAUSE

    rotation_vs_distribution:
      action_if_context_missing: OBSERVE_ONLY

  downstream_note:
    p08_should_not_receive_if_blocking_conflict: true
```

---

# 15. Market Position Context Gate Record

这是 P07 需要比 P06 更接近策略层的关键判断，但仍不是执行。

```yaml
market_position_context_gate_record:
  market_position_gate_id: string
  candidate_id: string

  market_context_inputs:
    discovery_market_cap_usd: number | null
    current_market_cap_usd: number | null
    market_cap_change_from_discovery_pct: number | null
    current_liquidity_usd: number | null
    current_price_usd: number | null
    token_age_seconds: integer | null

  position_context:
    entry_context_status:
      - EARLY_CONTEXT
      - ACCEPTABLE_CONTEXT
      - LATE_CONTEXT
      - CHASING_CONTEXT
      - EXIT_LIQUIDITY_RISK_CONTEXT
      - UNKNOWN_CONTEXT

  checks:
    market_cap_not_too_extended: boolean | null
    liquidity_adequate_for_paper: boolean | null
    discovery_to_current_move_acceptable: boolean | null
    token_age_context_compatible: boolean | null
    scenario_position_compatible: boolean | null

  gate_effect:
    - SUPPORTS_PAPER_CANDIDATE
    - REQUIRES_PAUSE
    - OBSERVE_ONLY
    - BLOCK_AS_CHASING
    - BLOCK_AS_EXIT_LIQUIDITY_RISK

  downstream:
    p08_must_recheck_quote_and_slippage: true
```

---

# 16. Strategy Pattern Fit Record

```yaml
strategy_pattern_fit_record:
  pattern_fit_id: string
  candidate_id: string

  evaluated_strategy_profiles:
    - strategy_profile_id: string
      fit_status:
        - FIT
        - FIT_WITH_LIMITATIONS
        - PARTIAL_FIT
        - NOT_FIT
        - BLOCKED_BY_RISK
      fit_reasons: list
      missing_requirements: list
      blocking_reasons: list

  selected_strategy_profile:
    strategy_profile_id: string | null
    selection_confidence:
      - HIGH
      - MEDIUM
      - LOW
      - NONE

  fit_dimensions:
    scenario_fit_score: number
    evidence_fit_score: number
    chip_structure_fit_score: number
    market_position_fit_score: number
    risk_flag_penalty_score: number
    data_quality_penalty_score: number

  no_single_score_policy:
    enabled: true

  downstream:
    selected_profile_can_be_sent_to_p08: boolean
    p08_required_checks: list
```

---

# 17. Strategy Risk Flag Evaluation Record

```yaml
strategy_risk_flag_evaluation_record:
  risk_eval_id: string
  candidate_id: string

  risk_flags_from_p06:
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

  evaluation:
    hard_block_flags: list
    pause_flags: list
    observe_flags: list
    p08_recheck_flags: list

  risk_action:
    - NO_RISK_BLOCK
    - OBSERVE
    - PAUSE
    - BLOCK
    - HUMAN_CONFIRMATION_REQUIRED
```

---

# 18. Strategy Invalidation Binding Record

P07 必须绑定 P06 的失效条件，交给 P08/P09 使用。

```yaml
strategy_invalidation_binding_record:
  binding_id: string
  candidate_id: string
  strategy_profile_id: string | null

  bound_invalidation_conditions:
    - invalidation_id: string
      source_scenario_id: string
      severity:
        - HARD_INVALIDATION
        - SOFT_INVALIDATION
        - WATCH_INVALIDATION
      p08_monitor_required: boolean
      p09_review_required_if_triggered: boolean

  strategy_specific_invalidations:
    for_control_box_breakout_pullback:
      - control_box_low_break
      - avwap_break_with_volume
      - poc_break_with_volume
      - early_wallet_concentrated_exit
      - active_distribution_risk_rises
      - high_counterparty_pressure_rises
      - no_higher_low_or_higher_high_after_pullback

  downstream:
    p08_must_include_in_runtime_precheck: true
    p09_must_use_for_failure_attribution: true
```

---

# 19. Observe Condition Record

```yaml
observe_condition_record:
  observe_id: string
  candidate_id: string

  observe_reason:
    - EARLY_BUT_NOT_READY
    - DATA_INCOMPLETE
    - SCENARIO_WEAK
    - EVIDENCE_WEAK
    - CHIP_STRUCTURE_NEEDS_REFRESH
    - MARKET_POSITION_NOT_READY
    - WAIT_FOR_CONFIRMATION_STRUCTURE

  observe_conditions:
    - condition_id: string
      condition_cn: string
      required_refresh:
        - WALLET_DELTA
        - HOLDER_SNAPSHOT
        - KLINE_VOLUME
        - MARKET_CAP
        - QUOTE
        - SECURITY
      priority:
        - HIGH
        - MEDIUM
        - LOW

  allowed_next_status:
    - CONTINUE_OBSERVE
    - PAUSE
    - BLOCK
    - PAPER_CANDIDATE_AFTER_REFRESH
```

---

# 20. Pause Condition Record

```yaml
pause_condition_record:
  pause_id: string
  candidate_id: string

  pause_reason:
    - SCENARIO_CONFLICT_UNRESOLVED
    - COUNTER_EVIDENCE_PRESSURE_HIGH
    - DATA_REFRESH_REQUIRED
    - SECURITY_CONTEXT_STALE
    - MARKET_POSITION_EXTENDED
    - TRANSITION_UNCERTAIN
    - P08_PRECHECK_NOT_ALLOWED_YET

  resume_conditions:
    - condition_id: string
      condition_cn: string
      required_source:
        - P02_REFRESH
        - P03_WALLET_DELTA
        - P04_CHIP_REFRESH
        - P05_EVIDENCE_RERUN
        - P06_SCENARIO_RERUN
      required_status: string

  expiry_policy:
    pause_expires_after_seconds: integer | null
    if_expired:
      - BLOCK
      - OBSERVE
      - REQUIRE_REVIEW
```

---

# 21. Strategy Block Reason Record

```yaml
strategy_block_reason_record:
  block_reason_id: string
  candidate_id: string

  block_type:
    - GOVERNANCE_BLOCK
    - TRACE_OR_HANDOFF_BLOCK
    - SCENARIO_BLOCK
    - EVIDENCE_BLOCK
    - CHIP_STRUCTURE_BLOCK
    - DATA_QUALITY_BLOCK
    - SECURITY_BLOCK
    - MARKET_POSITION_BLOCK
    - LIVE_EXECUTION_BLOCK

  block_reasons:
    - reason_id: string
      reason_cn: string
      source_record_id: string
      source_controller: string
      severity:
        - HARD
        - HIGH
        - MEDIUM

  reentry_allowed: boolean
  reentry_conditions: list

  downstream:
    p08_handoff_allowed: false
    review_required: boolean
```

---

# 22. Strategy Candidate Record

P07 的正向输出应叫 PAPER_CANDIDATE，不叫 PAPER_READY。

```yaml
strategy_candidate_record:
  strategy_candidate_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  candidate_type:
    - PAPER_CANDIDATE
    - HUMAN_CONFIRMATION_REQUIRED_CANDIDATE
    - OBSERVE_CANDIDATE
    - PAUSE_CANDIDATE

  selected_strategy_profile:
    strategy_profile_id: string
    strategy_profile_name_cn: string

  basis:
    primary_scenario_id: string
    supporting_evidence_bundle_ids: list
    chip_structure_record_ids: list
    market_position_context_id: string
    hard_negative_eval_id: string

  required_next_step:
    - P08_EXECUTION_RISK_CHECK
    - HUMAN_CONFIRMATION
    - DATA_REFRESH
    - OBSERVE_ONLY

  not_allowed:
    - direct_paper_runtime
    - direct_buy_signal
    - live_execution

  limitations:
    limitation_tags: list
    p08_required_checks: list

  trace:
    strategy_candidate_trace_id: string
    source_trace_ids: list
```

---

# 23. Human Confirmation Requirement Record

```yaml
human_confirmation_requirement_record:
  confirmation_id: string
  candidate_id: string

  trigger_reason:
    - HIGH_VALUE_BUT_CONFLICTED
    - STRONG_SCENARIO_WITH_CRITICAL_UNKNOWN
    - PAPER_CANDIDATE_WITH_HIGH_RISK_FLAG
    - GOVERNANCE_REQUIRES_CONFIRMATION
    - LEGACY_OR_LOW_TRACE_INPUT

  required_human_checks:
    - check_id: string
      check_cn: string
      source_records_to_review: list

  allowed_outcomes:
    - APPROVE_P08_CHECK_ONLY
    - KEEP_PAUSED
    - BLOCK
    - REQUEST_REFRESH

  restrictions:
    approval_does_not_allow_live_execution: true
    approval_does_not_bypass_p08: true
```

---

# 24. Strategy Gate Decision Record

这是 P07 的核心输出。

```yaml
strategy_gate_decision_record:
  decision_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  final_decision:
    - OBSERVE
    - PAUSE
    - BLOCK
    - PAPER_CANDIDATE
    - HUMAN_CONFIRMATION_REQUIRED
    - STRATEGY_GATE_REJECTED

  decision_basis:
    hard_negative_eval_id: string
    scenario_gate_eval_id: string
    evidence_gate_eval_id: string
    chip_gate_eval_id: string
    data_gate_eval_id: string
    market_position_gate_id: string
    pattern_fit_id: string
    risk_flag_eval_id: string

  decision_reason_cn:
    primary_reason: string
    supporting_reasons: list
    counter_reasons: list
    unresolved_risks: list

  next_step:
    if_observe:
      observe_condition_id: string | null
    if_pause:
      pause_condition_id: string | null
    if_block:
      block_reason_id: string | null
    if_paper_candidate:
      p08_execution_risk_data_request_packet_id: string | null
    if_human_confirmation:
      human_confirmation_requirement_id: string | null

  downstream_permission:
    p08_execution_risk_check_allowed: boolean
    paper_runtime_allowed: false
    live_execution_allowed: false

  invalidation_bindings:
    invalidation_binding_ids: list

  audit:
    strategy_gate_trace_id: string
    source_trace_ids: list
    report_path: string
```

---

# 25. Strategy Usage Permission Record

```yaml
strategy_usage_permission_record:
  permission_id: string
  candidate_id: string
  decision_id: string

  usage_permission:
    - SEND_TO_P08
    - OBSERVE_ONLY
    - PAUSE_ONLY
    - BLOCKED
    - HUMAN_REVIEW_ONLY

  allowed_usage:
    - p08_execution_risk_check
    - review_reference
    - telegram_status_display
    - paper_candidate_queue_if_p08_approves

  forbidden_usage:
    - direct_paper_runtime
    - live_execution
    - auto_order
    - wallet_signing
    - bypass_p08
    - bypass_execution_risk

  reason_cn: string
```

---

# 26. P08 Execution Risk Data Request Packet

P07 必须告诉 P08 需要检查什么，而不是直接启动纸面运行。

```yaml
p08_execution_risk_data_request_packet:
  packet_id: string
  from_controller: P07_STRATEGY_GATE_CONTROLLER
  to_controller: P08_EXECUTION_RISK_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  p07_decisions:
    strategy_gate_decision_records_path: string
    strategy_candidate_records_path: string
    strategy_usage_permission_records_path: string

  required_p08_checks:
    quote_checks:
      - current_quote_available
      - quote_deviation_check
      - current_price_vs_gate_context
      - liquidity_depth_check

    security_checks:
      - okx_security_recheck
      - mint_freeze_authority_recheck
      - blacklist_or_transfer_restriction_recheck
      - honeypot_or_sellability_recheck

    execution_cost_checks:
      - slippage_estimation
      - fee_model
      - minimum_liquidity_threshold
      - max_price_impact_threshold

    runtime_safety_checks:
      - paper_only_flag
      - no_live_execution
      - no_wallet_signing
      - daily_loss_limit
      - consecutive_failure_limit
      - one_token_one_position_rule

    freshness_checks:
      - market_data_refresh
      - wallet_delta_refresh_if_required
      - holder_snapshot_refresh_if_required
      - scenario_invalidation_refresh_if_required

  inherited_invalidations:
    invalidation_binding_records_path: string
    hard_invalidation_conditions: list
    soft_invalidation_conditions: list
    watch_invalidation_conditions: list

  limitations:
    - STRATEGY_GATE_ONLY
    - P08_MUST_APPROVE_BEFORE_PAPER_RUNTIME
    - NO_DIRECT_PAPER_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  output_required_from_p08:
    - execution_risk_decision_record
    - quote_security_decision_record
    - paper_runtime_permission_record
    - p08_to_paper_runtime_handoff_packet
```

---

# 27. P07 to P08 Handoff Packet

```yaml
p07_to_p08_handoff_packet:
  packet_id: string
  packet_type: P07_TO_P08_STRATEGY_GATE_HANDOFF
  generated_at: datetime

  route:
    from_controller: P07_STRATEGY_GATE_CONTROLLER
    to_controller: P08_EXECUTION_RISK_CONTROLLER

  upstream_control:
    p06_handoff_packet_id: string
    p07_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    observe_count: integer
    pause_count: integer
    block_count: integer
    paper_candidate_count: integer
    human_confirmation_required_count: integer
    rejected_count: integer

  strategy_gate_package:
    input_manifest_path: string
    hard_negative_evaluation_records_path: string
    scenario_gate_evaluation_records_path: string
    evidence_gate_evaluation_records_path: string
    chip_structure_gate_evaluation_records_path: string
    data_quality_gate_evaluation_records_path: string
    scenario_conflict_gate_records_path: string
    market_position_context_gate_records_path: string
    strategy_pattern_fit_records_path: string
    strategy_risk_flag_evaluation_records_path: string
    strategy_invalidation_binding_records_path: string
    observe_condition_records_path: string
    pause_condition_records_path: string
    block_reason_records_path: string
    strategy_candidate_records_path: string
    human_confirmation_requirement_records_path: string
    strategy_gate_decision_records_path: string
    strategy_usage_permission_records_path: string

  p08_data_request:
    p08_execution_risk_data_request_packet_path: string
    required_p08_checks: list
    candidates_allowed_for_p08_check: list

  quality:
    strategy_gate_report_path: string
    decision_distribution: object
    hard_negative_summary: object
    risk_flag_summary: object

  limitations:
    - STRATEGY_GATE_DECISION_ONLY
    - PAPER_CANDIDATE_NOT_PAPER_READY
    - P08_REQUIRED
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P08_EXECUTION_RISK_CONTROLLER
    forbidden:
      - PAPER_ONLY_RUNTIME_WITHOUT_P08
      - LIVE_EXECUTION

  read_instruction:
    p08_must_read_first:
      - p07_to_p08_handoff_packet
      - p08_execution_risk_data_request_packet
      - strategy_gate_decision_records
      - strategy_candidate_records
      - invalidation_binding_records
      - strategy_usage_permission_records
      - hard_negative_evaluation_records
```

---

# 28. P07 Gap Policy

```yaml
p07_gap_policy:
  BLOCKING_GAP:
    result: P07_BLOCKED
    examples:
      - p06_handoff_missing
      - trace_missing
      - acceptance_missing
      - live_execution_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P07_REJECTED
    examples:
      - no_primary_scenario
      - all_scenarios_do_not_use
      - no_strategy_policy_registry
      - no_strategy_gate_decision_contract
      - output_contract_missing

  HIGH_GAP:
    result: P07_READY_WITH_GAPS
    downstream_permission: P08_LIMITED_OR_PAUSE
    examples:
      - blocking_scenario_conflict
      - evidence_conflict_unresolved
      - chip_structure_risk_high
      - market_position_chasing_context
      - security_context_stale
      - scenario_confidence_low

  MEDIUM_GAP:
    result: P07_READY_WITH_GAPS
    downstream_permission: P08_ALLOWED_WITH_RECHECK
    examples:
      - cost_basis_low_confidence
      - counterparty_pressure_moderate
      - market_data_needs_refresh
      - transition_state_uncertain

  LOW_GAP:
    result: P07_READY_WITH_GAPS
    downstream_permission: P08_ALLOWED_WITH_NOTE
    examples:
      - optional_historical_context_missing
      - minor_data_freshness_gap
      - noncritical_strategy_metadata_missing
```

---

# 29. P07 Hard Negative Rules

```yaml
p07_hard_negative_rules:
  - rule_id: P07_BLOCK_001
    name: 未读取 P06 handoff
    condition: p06_to_p07_handoff_packet_missing == true
    result: P07_BLOCKED
    reason: P07 不能绕过 P06 / Handoff 启动

  - rule_id: P07_BLOCK_002
    name: 无场景输入
    condition: primary_scenario_missing == true and secondary_scenarios_missing == true
    result: P07_REJECTED
    reason: 无场景输入不能做策略门控

  - rule_id: P07_BLOCK_003
    name: 无策略政策注册
    condition: strategy_policy_registry_missing == true
    result: P07_REJECTED
    reason: 没有策略政策不能裁决

  - rule_id: P07_BLOCK_004
    name: 阻断级场景冲突
    condition: blocking_scenario_conflict_present == true
    result: P07_BLOCKED
    reason: 场景冲突未解决，不能进入 P08

  - rule_id: P07_BLOCK_005
    name: 主场景被否定
    condition: primary_scenario_rejected == true
    result: P07_BLOCKED
    reason: 被否定场景不能作为策略候选基础

  - rule_id: P07_BLOCK_006
    name: 强反证存在
    condition: strong_counter_evidence_present == true
    result: P07_BLOCKED
    reason: 强反证阻断策略候选

  - rule_id: P07_BLOCK_007
    name: 筹码结构高风险
    condition: chip_gate_status == CHIP_BLOCKS_GATE
    result: P07_BLOCKED
    reason: 筹码结构风险阻断策略候选

  - rule_id: P07_BLOCK_008
    name: 追高 / 接盘上下文
    condition: market_position_context in [CHASING_CONTEXT, EXIT_LIQUIDITY_RISK_CONTEXT]
    result: P07_BLOCKED
    reason: 位置上下文不允许进入纸面候选

  - rule_id: P07_BLOCK_009
    name: 直接输出买入或纸面运行
    condition: output_contains in [buy_signal, paper_runtime_started, live_execution_allowed]
    result: P07_BLOCKED
    reason: P07 不是执行层

  - rule_id: P07_BLOCK_010
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P07_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 30. P07 状态机专业版

```yaml
p07_strategy_gate_state_machine:
  states:
    - P07_UNINITIALIZED
    - P07_CONTEXT_LOADED
    - P07_HANDOFF_READ
    - P07_INPUT_MANIFEST_BUILT
    - P07_STRATEGY_POLICY_LOADED
    - P07_HARD_NEGATIVE_CHECKED
    - P07_SCENARIO_GATE_EVALUATED
    - P07_EVIDENCE_GATE_EVALUATED
    - P07_CHIP_GATE_EVALUATED
    - P07_DATA_QUALITY_GATE_EVALUATED
    - P07_SCENARIO_CONFLICT_GATE_EVALUATED
    - P07_MARKET_POSITION_CONTEXT_EVALUATED
    - P07_STRATEGY_PATTERN_FIT_EVALUATED
    - P07_RISK_FLAGS_EVALUATED
    - P07_INVALIDATIONS_BOUND
    - P07_OBSERVE_CONDITIONS_BUILT
    - P07_PAUSE_CONDITIONS_BUILT
    - P07_BLOCK_REASONS_BUILT
    - P07_STRATEGY_CANDIDATES_BUILT
    - P07_HUMAN_CONFIRMATION_REQUIREMENTS_BUILT
    - P07_DECISIONS_BUILT
    - P07_USAGE_PERMISSIONS_BUILT
    - P07_GAP_ANALYZED
    - P07_P08_DATA_REQUEST_BUILT
    - P07_READY_FOR_ACCEPTANCE
    - P07_ACCEPTANCE_READY
    - P07_READY_FOR_P08_HANDOFF
    - P07_READY_WITH_GAPS
    - P07_REJECTED
    - P07_BLOCKED

  critical_transitions:
    - from: P07_HANDOFF_READ
      to: P07_INPUT_MANIFEST_BUILT
      condition: p06_handoff_valid == true

    - from: P07_INPUT_MANIFEST_BUILT
      to: P07_STRATEGY_POLICY_LOADED
      condition: strategy_policy_registry_available == true

    - from: P07_STRATEGY_POLICY_LOADED
      to: P07_HARD_NEGATIVE_CHECKED
      condition: hard_negative_evaluation_records_created == true

    - from: P07_HARD_NEGATIVE_CHECKED
      to: P07_SCENARIO_GATE_EVALUATED
      condition: no_immediate_hard_block_or_block_record_created == true

    - from: P07_SCENARIO_GATE_EVALUATED
      to: P07_EVIDENCE_GATE_EVALUATED
      condition: scenario_gate_evaluation_records_created == true

    - from: P07_EVIDENCE_GATE_EVALUATED
      to: P07_CHIP_GATE_EVALUATED
      condition: evidence_gate_evaluation_records_created == true

    - from: P07_CHIP_GATE_EVALUATED
      to: P07_DATA_QUALITY_GATE_EVALUATED
      condition: chip_gate_evaluation_records_created == true

    - from: P07_DATA_QUALITY_GATE_EVALUATED
      to: P07_MARKET_POSITION_CONTEXT_EVALUATED
      condition: data_quality_gate_records_created == true

    - from: P07_MARKET_POSITION_CONTEXT_EVALUATED
      to: P07_STRATEGY_PATTERN_FIT_EVALUATED
      condition: market_position_context_gate_records_created == true

    - from: P07_STRATEGY_PATTERN_FIT_EVALUATED
      to: P07_RISK_FLAGS_EVALUATED
      condition: strategy_pattern_fit_records_created == true

    - from: P07_RISK_FLAGS_EVALUATED
      to: P07_INVALIDATIONS_BOUND
      condition: risk_flag_evaluation_records_created == true

    - from: P07_INVALIDATIONS_BOUND
      to: P07_DECISIONS_BUILT
      condition: invalidation_binding_records_created == true

    - from: P07_DECISIONS_BUILT
      to: P07_USAGE_PERMISSIONS_BUILT
      condition: strategy_gate_decision_records_created == true

    - from: P07_USAGE_PERMISSIONS_BUILT
      to: P07_P08_DATA_REQUEST_BUILT
      condition: p08_execution_risk_data_request_packet_created == true

    - from: P07_P08_DATA_REQUEST_BUILT
      to: P07_READY_FOR_ACCEPTANCE
      condition: p07_output_contract_ready == true

    - from: P07_READY_FOR_ACCEPTANCE
      to: P07_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P07_ACCEPTANCE_READY
      to: P07_READY_FOR_P08_HANDOFF
      condition: p07_to_p08_handoff_packet_created == true
```

---

# 31. P07 文件体系

## 31.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p07_strategy_gate_controller/
```

必须创建：

```text
p07_strategy_gate_controller.yaml
p07_strategy_gate_context.md
p07_input_contract.yaml
p07_output_contract.yaml
strategy_gate_input_manifest_schema.yaml
strategy_policy_registry.yaml
hard_negative_evaluation_schema.yaml
scenario_gate_evaluation_schema.yaml
evidence_gate_evaluation_schema.yaml
chip_structure_gate_evaluation_schema.yaml
data_quality_gate_evaluation_schema.yaml
scenario_conflict_gate_schema.yaml
market_position_context_gate_schema.yaml
strategy_pattern_fit_schema.yaml
strategy_risk_flag_evaluation_schema.yaml
strategy_invalidation_binding_schema.yaml
observe_condition_schema.yaml
pause_condition_schema.yaml
strategy_block_reason_schema.yaml
strategy_candidate_schema.yaml
human_confirmation_requirement_schema.yaml
strategy_gate_decision_schema.yaml
strategy_usage_permission_schema.yaml
strategy_gate_policy.yaml
hard_negative_policy.yaml
strategy_pattern_fit_policy.yaml
market_position_context_policy.yaml
pause_observe_policy.yaml
human_confirmation_policy.yaml
strategy_gate_gap_policy.yaml
strategy_gate_hard_negative_rules.yaml
strategy_gate_state_machine.yaml
strategy_gate_trace_requirements.yaml
p08_execution_risk_data_request_packet_contract.yaml
p07_to_p08_handoff_contract.yaml
p07_acceptance_criteria.md
p07_storage_constitution.md
p07_test_matrix.yaml
p07_report_model.yaml
p07_review_checklist.md
her_p07_execution_protocol.md
```

---

## 31.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p07_strategy_gate/
  input_manifest/
  policy_registry/
  hard_negative_evaluations/
  scenario_gate/
  evidence_gate/
  chip_gate/
  data_quality_gate/
  scenario_conflict_gate/
  market_position_context/
  strategy_pattern_fit/
  risk_flags/
  invalidation_bindings/
  observe_conditions/
  pause_conditions/
  block_reasons/
  strategy_candidates/
  human_confirmation/
  decisions/
  usage_permissions/
  quality/
  gaps/
  p08_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 32. P07 测试矩阵

```yaml
p07_test_matrix:
  - test_id: P07_TEST_001
    name: 二段扩张候选，证据充分，筹码支持，无硬否定
    expected_decision: PAPER_CANDIDATE
    expected_next_step: P08_EXECUTION_RISK_CHECK

  - test_id: P07_TEST_002
    name: 缺 P06 handoff
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_003
    name: 无策略政策注册
    expected_status: P07_REJECTED

  - test_id: P07_TEST_004
    name: 主场景为 ACTIVE_DISTRIBUTION
    expected_decision: BLOCK

  - test_id: P07_TEST_005
    name: 场景冲突为 SECOND_STAGE_EXPANSION vs FINAL_PUMP_DISTRIBUTION
    expected_decision: PAUSE_OR_BLOCK_DEPENDING_SEVERITY

  - test_id: P07_TEST_006
    name: 证据支持但强反证存在
    expected_decision: BLOCK_OR_PAUSE

  - test_id: P07_TEST_007
    name: 筹码结构高留存但数据新鲜度不足
    expected_decision: PAUSE
    expected_required_refresh: HOLDER_SNAPSHOT_OR_WALLET_DELTA

  - test_id: P07_TEST_008
    name: 市值从发现时已大幅扩张，进入追高上下文
    expected_decision: BLOCK_AS_CHASING

  - test_id: P07_TEST_009
    name: 场景弱但无重大风险
    expected_decision: OBSERVE

  - test_id: P07_TEST_010
    name: 高价值候选但存在关键 UNKNOWN
    expected_decision: HUMAN_CONFIRMATION_REQUIRED

  - test_id: P07_TEST_011
    name: P07 输出 buy_signal
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_012
    name: P07 启动 paper runtime
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_013
    name: live execution requested
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_014
    name: PAPER_CANDIDATE 但未生成 P08 request
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_015
    name: 弱场景被当成强策略适配
    expected_status: P07_BLOCKED

  - test_id: P07_TEST_016
    name: P08 required security recheck missing
    expected_status: P07_READY_WITH_GAPS_OR_BLOCKED
```

---

# 33. P07 报告模型

```yaml
p07_strategy_gate_report:
  report_id: string
  generated_at: datetime
  controller_id: P07_STRATEGY_GATE_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    observe_count: integer
    pause_count: integer
    block_count: integer
    paper_candidate_count: integer
    human_confirmation_required_count: integer
    rejected_count: integer
    blocked_count: integer

  decision_distribution:
    OBSERVE: integer
    PAUSE: integer
    BLOCK: integer
    PAPER_CANDIDATE: integer
    HUMAN_CONFIRMATION_REQUIRED: integer
    STRATEGY_GATE_REJECTED: integer

  hard_negative_summary:
    hard_negative_triggered_count: integer
    most_common_hard_negative_rules: list

  scenario_gate_summary:
    accepted_scenario_count: integer
    rejected_scenario_count: integer
    conflicted_scenario_count: integer
    observe_only_scenario_count: integer

  evidence_gate_summary:
    evidence_supports_count: integer
    evidence_weak_count: integer
    evidence_conflicted_count: integer
    evidence_blocks_count: integer

  chip_gate_summary:
    chip_supports_count: integer
    chip_risk_pause_count: integer
    chip_blocks_count: integer
    chip_unknown_count: integer

  market_position_summary:
    early_context_count: integer
    acceptable_context_count: integer
    late_context_count: integer
    chasing_context_count: integer
    exit_liquidity_risk_context_count: integer

  p08_handoff_summary:
    p08_handoff_ready: boolean
    p08_candidate_count: integer
    p08_required_checks: list

  compliance:
    buy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
    p08_bypassed: false
```

---

# 34. HER P07 执行协议

```text
HER 执行 P07 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P07 controller context
4. 读取 P06 → P07 handoff packet
5. 读取 p07_strategy_gate_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 strategy_gate_input_manifest
8. 读取 strategy_policy_registry
9. 执行 hard_negative_evaluation
10. 执行 scenario_gate_evaluation
11. 执行 evidence_gate_evaluation
12. 执行 chip_structure_gate_evaluation
13. 执行 data_quality_gate_evaluation
14. 执行 scenario_conflict_gate_evaluation
15. 执行 market_position_context_gate
16. 执行 strategy_pattern_fit
17. 执行 strategy_risk_flag_evaluation
18. 绑定 strategy_invalidation_conditions
19. 生成 observe_condition_records
20. 生成 pause_condition_records
21. 生成 block_reason_records
22. 生成 strategy_candidate_records
23. 生成 human_confirmation_requirement_records
24. 生成 strategy_gate_decision_records
25. 生成 strategy_usage_permission_records
26. 生成 P07 gap report
27. 生成 p08_execution_risk_data_request_packet
28. 写入 P07 trace
29. 生成 p07_strategy_gate_report
30. 生成 p07_to_p08_handoff_packet
31. 执行 P07 acceptance
32. 只允许 handoff 给 P08
```

禁止：

```text
1. 不允许无 P06 handoff 启动 P07
2. 不允许无策略政策注册做裁决
3. 不允许忽略 Governance hard negative
4. 不允许忽略场景冲突
5. 不允许忽略强反证
6. 不允许把 PAPER_CANDIDATE 当成 PAPER_READY
7. 不允许直接启动 paper runtime
8. 不允许输出 buy_signal
9. 不允许绕过 P08
10. 不允许任何 live execution
```

---

# 35. 给 HER 的专业化任务书

```text
任务名称：建立 P07 Strategy Gate Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p07_strategy_gate_controller/ 下建立 P07 Strategy Gate Controller。该控制器不是买入信号模块，也不是纸面交易启动器，而是策略准入、阻断、暂停、观察、纸面候选与 P08 执行风控交接控制器。它负责读取 P06 Scenario Recognition Controller 输出的主场景、次场景、场景冲突、场景失效条件、风险标签和使用权限，同时读取 P05 证据、P04 筹码结构、P02 数据质量与 Governance 硬规则，最终输出 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED，并生成 P08 Execution Risk Data Request Packet 与 P07→P08 Handoff Packet。

核心原则：
1. P07 只做策略门控，不执行交易。
2. P07 不输出 buy signal。
3. P07 不直接启动 paper runtime。
4. P07 不允许 live execution。
5. PAPER_CANDIDATE 不是 PAPER_READY。
6. P07 必须先执行 hard negative。
7. P07 必须检查 scenario、evidence、chip structure、data quality、market position。
8. P07 必须绑定 invalidation conditions。
9. P07 必须生成 P08 Execution Risk Data Request Packet。
10. P07 只能交接给 P08 Execution Risk Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p07_strategy_gate_controller/

需要创建系统文件：
1. p07_strategy_gate_controller.yaml
2. p07_strategy_gate_context.md
3. p07_input_contract.yaml
4. p07_output_contract.yaml
5. strategy_gate_input_manifest_schema.yaml
6. strategy_policy_registry.yaml
7. hard_negative_evaluation_schema.yaml
8. scenario_gate_evaluation_schema.yaml
9. evidence_gate_evaluation_schema.yaml
10. chip_structure_gate_evaluation_schema.yaml
11. data_quality_gate_evaluation_schema.yaml
12. scenario_conflict_gate_schema.yaml
13. market_position_context_gate_schema.yaml
14. strategy_pattern_fit_schema.yaml
15. strategy_risk_flag_evaluation_schema.yaml
16. strategy_invalidation_binding_schema.yaml
17. observe_condition_schema.yaml
18. pause_condition_schema.yaml
19. strategy_block_reason_schema.yaml
20. strategy_candidate_schema.yaml
21. human_confirmation_requirement_schema.yaml
22. strategy_gate_decision_schema.yaml
23. strategy_usage_permission_schema.yaml
24. strategy_gate_policy.yaml
25. hard_negative_policy.yaml
26. strategy_pattern_fit_policy.yaml
27. market_position_context_policy.yaml
28. pause_observe_policy.yaml
29. human_confirmation_policy.yaml
30. strategy_gate_gap_policy.yaml
31. strategy_gate_hard_negative_rules.yaml
32. strategy_gate_state_machine.yaml
33. strategy_gate_trace_requirements.yaml
34. p08_execution_risk_data_request_packet_contract.yaml
35. p07_to_p08_handoff_contract.yaml
36. p07_acceptance_criteria.md
37. p07_storage_constitution.md
38. p07_test_matrix.yaml
39. p07_report_model.yaml
40. p07_review_checklist.md
41. her_p07_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p07_strategy_gate/
  input_manifest/
  policy_registry/
  hard_negative_evaluations/
  scenario_gate/
  evidence_gate/
  chip_gate/
  data_quality_gate/
  scenario_conflict_gate/
  market_position_context/
  strategy_pattern_fit/
  risk_flags/
  invalidation_bindings/
  observe_conditions/
  pause_conditions/
  block_reasons/
  strategy_candidates/
  human_confirmation/
  decisions/
  usage_permissions/
  quality/
  gaps/
  p08_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p07_strategy_gate_controller.yaml：定义 P07 身份、职责、权限、上下游、状态码、禁止事项。
- p07_strategy_gate_context.md：写成 HER 执行前必须读取的 P07 上下文。
- p07_input_contract.yaml：定义 P07 必须读取的 P06 handoff、场景记录、P05 证据、P04 筹码、P02 数据质量、Governance 硬规则。
- p07_output_contract.yaml：定义 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED 输出。
- strategy_gate_input_manifest_schema.yaml：定义 P07 接收的所有门控输入。
- strategy_policy_registry.yaml：定义可支持的策略 profile，例如 SIKK_B_CONTROL_BOX_BREAKOUT_PULLBACK、SIKK_R_REACCUMULATION_REACTIVATION、SIKK_OBSERVE_ONLY_HIGH_CONFLICT。
- hard_negative_evaluation_schema.yaml：定义一票否决检查。
- scenario_gate_evaluation_schema.yaml：定义场景门控。
- evidence_gate_evaluation_schema.yaml：定义证据门控。
- chip_structure_gate_evaluation_schema.yaml：定义筹码结构门控。
- data_quality_gate_evaluation_schema.yaml：定义数据质量门控。
- scenario_conflict_gate_schema.yaml：定义场景冲突门控。
- market_position_context_gate_schema.yaml：定义早晚、追高、接盘上下文。
- strategy_pattern_fit_schema.yaml：定义策略模板适配。
- strategy_risk_flag_evaluation_schema.yaml：定义风险标签评估。
- strategy_invalidation_binding_schema.yaml：定义失效条件绑定。
- observe_condition_schema.yaml：定义观察条件。
- pause_condition_schema.yaml：定义暂停条件。
- strategy_block_reason_schema.yaml：定义阻断原因。
- strategy_candidate_schema.yaml：定义 PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED_CANDIDATE。
- human_confirmation_requirement_schema.yaml：定义人工确认要求。
- strategy_gate_decision_schema.yaml：定义最终门控裁决。
- strategy_usage_permission_schema.yaml：定义下游使用权限。
- strategy_gate_policy.yaml：定义 P07 门控整体政策。
- hard_negative_policy.yaml：定义硬否定优先级。
- strategy_pattern_fit_policy.yaml：定义策略适配规则。
- market_position_context_policy.yaml：定义市值、流动性、发现以来涨幅、是否追高的判断。
- pause_observe_policy.yaml：定义 PAUSE 与 OBSERVE 规则。
- human_confirmation_policy.yaml：定义人工确认触发条件。
- strategy_gate_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- strategy_gate_hard_negative_rules.yaml：定义无 P06 handoff、无场景、无策略注册、阻断级冲突、强反证、筹码阻断、追高、输出买入、自动实盘等阻断。
- strategy_gate_state_machine.yaml：定义 P07 全状态机。
- strategy_gate_trace_requirements.yaml：定义 gate trace、decision trace、risk flag trace、handoff trace。
- p08_execution_risk_data_request_packet_contract.yaml：定义 P07 给 P08 的执行风控数据请求包。
- p07_to_p08_handoff_contract.yaml：定义 P07_TO_P08 handoff packet。
- p07_acceptance_criteria.md：定义 P07_READY、P07_READY_WITH_GAPS、P07_REJECTED、P07_BLOCKED。
- p07_storage_constitution.md：定义系统文件与运行数据目录。
- p07_test_matrix.yaml：定义至少 16 个测试场景。
- p07_report_model.yaml：定义 P07 人类可读报告。
- p07_review_checklist.md：定义审计清单。
- her_p07_execution_protocol.md：定义 HER 执行 P07 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P07_READY / P07_READY_WITH_GAPS / P07_REJECTED / P07_BLOCKED 判断
4. strategy_policy_registry 摘要
5. hard_negative_evaluation 摘要
6. scenario_gate_evaluation 摘要
7. evidence_gate_evaluation 摘要
8. chip_structure_gate_evaluation 摘要
9. data_quality_gate_evaluation 摘要
10. market_position_context_gate 摘要
11. strategy_pattern_fit 摘要
12. strategy_gate_decision 摘要
13. strategy_candidate 摘要
14. p08_execution_risk_data_request_packet 摘要
15. p07_to_p08_handoff_packet 摘要
16. P07 阻断规则摘要
17. P07 测试矩阵摘要
18. 当前缺口清单
19. 是否达到轻量机构级 P07 v3.0

最终验收标准：
只有当 P07 具备 strategy gate input manifest、strategy policy registry、hard negative evaluation、scenario gate evaluation、evidence gate evaluation、chip structure gate evaluation、data quality gate evaluation、scenario conflict gate、market position context gate、strategy pattern fit、risk flag evaluation、invalidation binding、observe conditions、pause conditions、block reasons、strategy candidate、human confirmation requirement、strategy gate decision、usage permission、gap policy、hard negative rules、state machine、trace requirements、P08 data request、P07 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P07 不能输出 buy signal、不能直接启动 paper runtime、不能绕过 P08、不能允许 live execution 时，才允许标记为 P07_READY。
```

---

# 36. 当前是否达到专业化标准

## 判断

这一版 P07 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是买入信号模块
不是纸面交易启动器
```

P07 被明确升级为：

```text
策略门控层
硬否定优先层
证据 / 场景 / 筹码 / 数据质量综合裁决层
观察 / 暂停 / 阻断 / 纸面候选裁决层
P08 执行风控输入层
```

---

# 37. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Strategy Gate Input Manifest|已补齐|
|Strategy Policy Registry|已补齐|
|Hard Negative Evaluation|已补齐|
|Scenario Gate Evaluation|已补齐|
|Evidence Gate Evaluation|已补齐|
|Chip Structure Gate Evaluation|已补齐|
|Data Quality Gate Evaluation|已补齐|
|Scenario Conflict Gate|已补齐|
|Market Position Context Gate|已补齐|
|Strategy Pattern Fit|已补齐|
|Risk Flag Evaluation|已补齐|
|Invalidation Binding|已补齐|
|Observe Condition|已补齐|
|Pause Condition|已补齐|
|Block Reason|已补齐|
|Strategy Candidate|已补齐|
|Human Confirmation Requirement|已补齐|
|Strategy Gate Decision|已补齐|
|Usage Permission|已补齐|
|P08 Execution Risk Request|已补齐|
|P07 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 38. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|策略 profile 权重未回测|已定义结构|P09 / P10 校准|
|市值追高阈值未定|已定义上下文门控|Review 后用样本校准|
|PAPER_CANDIDATE 到 PAPER_RUNTIME 之间仍缺 P08|已明确边界|下一阶段 P08|
|P07 不做报价 / 滑点 / 安全最终确认|已明确边界|P08 处理|
|人工确认流程未接 Telegram|已定义数据结构|Runner / Tool Binding 阶段|
|P07 handoff 未联调|需要 P08|下一阶段展开 P08|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P07 的本质不是买入信号，而是策略门控裁决器。**
    
2. **PAPER_CANDIDATE 不是 PAPER_READY。**  
    P07 只能把样本交给 P08 做执行前风控。
    
3. **P07 必须先否定，再准入。**  
    硬否定优先于任何策略适配。
    
4. **场景、证据、筹码、数据质量、市场位置必须同时过门。**  
    任何一个维度出现硬阻断，都不能进入 P08。
    
5. **市场位置上下文是 P07 的关键能力。**  
    当前是否追高、是否正在变成退出流动性，必须在 P07 阶段处理。
    
6. **P07 的输出必须可复盘。**  
    每个 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE 都必须有来源证据、反证、风险标签和下游要求。
    
7. **P07 必须把失效条件绑定给 P08 / P09。**  
    否则纸面运行和复盘无法解释为什么失败。
    
8. **P07 只能交接给 P08。**  
    任何绕过 P08 直接进入 paper runtime 或 live execution 的路径都必须阻断。