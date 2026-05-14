# P09 Review Replay Controller 专业版 v3.0

## 复盘回放、决策链重建、失败归因、样本校准与 P10 升级候选交接控制器

---

## 0. 先修正 P09 的定位

P09 不能被设计成普通的：

```text
纸面交易日报
盈亏统计脚本
失败原因总结
复盘 Markdown 报告
```

P09 的专业定位应该是：

```text
把 Paper-only Runtime、P08 执行前风控、P07 策略门控、P06 场景识别、P05 证据、P04 筹码结构、P03 钱包实体、P02 数据事实、P01 候选建档的全链路记录，重新回放成可审计、可归因、可校准、可生成升级候选的 Review Replay System。
```

一句话定义：

> **Paper-only Runtime 负责记录纸面运行结果。**  
> **P09 负责把结果倒推回每一个阶段，判断失败或成功到底来自数据、证据、场景、策略、执行风险、运行成本、失效条件还是系统缺口。**  
> **P10 才负责把复盘结论转化为规则、字段、阈值、合约、测试、工具绑定或方法论升级候选。**

P09 可以输出：

```text
review_case
replay_result
failure_attribution
success_attribution
decision_chain_reconstruction
runtime_path_reconstruction
calibration_candidate
p10_upgrade_data_request
```

P09 不能直接输出：

```text
修改策略规则
更新生产阈值
自动部署
实盘许可
直接改变 P07 / P08 决策规则
```

---

# 1. P09 阶段核心目标

P09 必须一次性解决 18 个问题：

|编号|核心问题|P09 必须输出|
|---|---|---|
|1|当前复盘对象是谁？|`review_case_record`|
|2|当时系统读取了哪些输入？|`replay_input_snapshot_record`|
|3|P01-P08 当时决策链是否可重建？|`decision_chain_reconstruction_record`|
|4|Paper Runtime 当时如何进入、持仓、退出？|`runtime_path_reconstruction_record`|
|5|实际纸面结果如何？|`paper_result_record`|
|6|入场判断是否符合当时数据？|`entry_decision_review_record`|
|7|退出或失败是否触发过失效条件？|`exit_invalidation_review_record`|
|8|失败来自哪个阶段？|`failure_attribution_record`|
|9|成功来自哪个阶段？|`success_attribution_record`|
|10|原判断中有哪些误判？|`misclassification_review_record`|
|11|哪些字段、阈值、证据、场景需要校准？|`calibration_candidate_record`|
|12|哪些数据缺口导致误判？|`data_gap_impact_record`|
|13|哪些 hard negative 漏掉了？|`missed_negative_rule_record`|
|14|哪些 paper runtime 模拟不真实？|`runtime_simulation_quality_record`|
|15|样本应该如何进入经验库？|`review_case_library_record`|
|16|是否生成 P10 升级候选？|`p10_upgrade_candidate_data_request_packet`|
|17|哪些结论只能人工复核？|`review_manual_check_record`|
|18|是否可以交接给 P10？|`p09_to_p10_handoff_packet`|

---

# 2. P09 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|回放官|重建当时输入、状态和决策顺序|`replay_input_snapshot_record`|
|决策链审计官|审计 P01-P08 决策是否自洽|`decision_chain_reconstruction_record`|
|运行路径审计官|审计纸面入场、持仓、退出|`runtime_path_reconstruction_record`|
|失败归因官|判断失败来自哪个阶段|`failure_attribution_record`|
|成功归因官|判断成功是否真的来自系统能力|`success_attribution_record`|
|误判分析官|识别场景、证据、筹码、风险误判|`misclassification_review_record`|
|校准官|生成阈值、字段、规则、测试校准候选|`calibration_candidate_record`|
|升级交接官|把可升级事项交给 P10|`p10_upgrade_candidate_data_request_packet`|

---

# 3. P09 底层方法论

## 3.1 复盘不是总结，是重建

普通复盘只问：

```text
赚了还是亏了？
为什么赚？
为什么亏？
```

P09 要问：

```text
当时系统到底看到了什么？
当时哪些字段缺失？
当时证据是否足够？
当时场景是否误识别？
当时策略门控有没有过度放行？
当时执行风控有没有遗漏？
当时纸面成交模型是否失真？
当时失效条件有没有触发但没处理？
```

---

## 3.2 归因必须分阶段

失败不能简单写：

```text
行情不好
庄出货
滑点大
```

必须定位到阶段：

```text
P02 数据事实问题
P03 钱包实体问题
P04 筹码结构问题
P05 证据系统问题
P06 场景识别问题
P07 策略门控问题
P08 执行风控问题
Paper Runtime 模拟问题
Governance 规则缺口
Trace / Handoff / Acceptance 缺口
```

---

## 3.3 复盘不能直接改规则

P09 只能输出：

```text
upgrade_candidate
calibration_candidate
new_test_case_candidate
rule_gap_candidate
schema_gap_candidate
```

不能直接修改：

```text
策略规则
阈值参数
hard negative
状态机
执行风控
paper runtime
```

这些必须交给 P10 Self Upgrade Controller。

---

## 3.4 成功也要归因

只分析失败会导致系统偏差。

P09 必须判断成功是因为：

```text
系统识别正确
策略逻辑有效
行情随机有利
纸面成交模型过于乐观
滑点成本低估
退出条件偶然有效
```

成功样本也可能暴露系统缺陷。

---

## 3.5 Replay 必须锁定历史快照

P09 不能用当前数据回头解释过去。

必须区分：

```text
decision_time_snapshot
runtime_entry_snapshot
runtime_exit_snapshot
review_time_snapshot
```

否则会发生“事后聪明偏差”。

---

# 4. P09 支持的复盘类型

```yaml
p09_review_types:
  PAPER_POSITION_REVIEW:
    name_cn: 单笔纸面持仓复盘
    scope:
      - entry
      - holding
      - exit
      - pnl

  PAPER_CYCLE_REVIEW:
    name_cn: 单轮纸面运行周期复盘
    scope:
      - all_candidates
      - all_decisions
      - all_runtime_events

  FAILED_CANDIDATE_REVIEW:
    name_cn: 失败候选复盘
    scope:
      - blocked
      - paused
      - rejected
      - paper_loss

  MISSED_OPPORTUNITY_REVIEW:
    name_cn: 错过机会复盘
    scope:
      - observe_or_pause_but_later_expanded
      - blocked_but_later_valid

  FALSE_POSITIVE_REVIEW:
    name_cn: 误放行复盘
    scope:
      - paper_candidate_but_failed
      - paper_runtime_allowed_but_immediate_invalidated

  FALSE_NEGATIVE_REVIEW:
    name_cn: 误阻断复盘
    scope:
      - blocked_but_later_structure_validated
      - paused_but_later_expanded

  SYSTEM_HEALTH_REVIEW:
    name_cn: 系统健康复盘
    scope:
      - trace_completeness
      - handoff_integrity
      - data_quality
      - runtime_consistency
```

---

# 5. P09 必须建立的核心对象

|对象|作用|
|---|---|
|`Review Case Record`|复盘案例主记录|
|`Replay Input Snapshot Record`|回放输入快照|
|`Decision Chain Reconstruction Record`|P01-P08 决策链重建|
|`Runtime Path Reconstruction Record`|Paper Runtime 路径重建|
|`Paper Result Record`|纸面运行结果|
|`Entry Decision Review Record`|入场决策复盘|
|`Exit Decision Review Record`|退出决策复盘|
|`Invalidation Trigger Review Record`|失效条件复盘|
|`Failure Attribution Record`|失败归因|
|`Success Attribution Record`|成功归因|
|`Misclassification Review Record`|场景 / 证据 / 筹码误判复盘|
|`Gate Error Review Record`|P07 门控错误复盘|
|`Execution Risk Error Review Record`|P08 执行风控错误复盘|
|`Runtime Simulation Quality Record`|纸面模拟质量复盘|
|`Data Gap Impact Record`|数据缺口影响|
|`Trace Integrity Review Record`|Trace 完整性复盘|
|`Handoff Integrity Review Record`|Handoff 完整性复盘|
|`Acceptance Integrity Review Record`|验收完整性复盘|
|`Calibration Candidate Record`|校准候选|
|`Missed Negative Rule Record`|漏掉的硬否定候选|
|`New Test Case Candidate Record`|新测试样例候选|
|`Review Case Library Record`|复盘案例库索引|
|`P10 Upgrade Candidate Data Request Packet`|给 P10 的升级请求|
|`P09 to P10 Handoff Packet`|P09 → P10 交接包|

---

# 6. P09 输入：必须读取什么

```yaml
p09_required_inputs:
  from_paper_runtime:
    - paper_positions_open
    - paper_positions_closed
    - paper_trades
    - paper_equity_curve
    - paper_runtime_trace
    - paper_runtime_events
    - paper_exit_events
    - strategy_metrics
    - risk_events
    - daily_reports

  from_p08:
    - p08_to_paper_runtime_handoff_packet
    - paper_runtime_permission_records
    - paper_entry_simulation_plans
    - quote_snapshot_records
    - quote_consistency_records
    - liquidity_depth_records
    - slippage_estimation_records
    - execution_cost_model_records
    - security_recheck_records
    - invalidation_precheck_records
    - runtime_risk_limit_records
    - circuit_breaker_records
    - p08_execution_risk_report

  from_p07:
    - strategy_gate_decision_records
    - strategy_candidate_records
    - strategy_pattern_fit_records
    - hard_negative_evaluation_records
    - strategy_invalidation_binding_records
    - strategy_block_reason_records
    - p07_strategy_gate_report

  from_p06:
    - primary_scenario_candidate_records
    - secondary_scenario_candidate_records
    - scenario_conflict_records
    - scenario_rejection_records
    - scenario_invalidation_records
    - scenario_risk_flag_records
    - scenario_confidence_records
    - p06_scenario_recognition_report

  from_p05:
    - evidence_bundle_records
    - supporting_evidence_records
    - counter_evidence_records
    - evidence_conflict_records
    - unknown_evidence_records
    - evidence_sufficiency_records
    - p05_evidence_report

  from_p04:
    - chip_structure_score_records
    - early_wallet_retention_records
    - structural_group_holding_records
    - distribution_progress_records
    - counterparty_pressure_records
    - chip_transfer_status_records
    - chip_structure_quality_records
    - p04_chip_structure_report

  from_p03:
    - wallet_entity_master_records
    - same_source_group_candidates
    - sync_behavior_group_candidates
    - wallet_role_candidate_records
    - wallet_entity_quality_record
    - p03_wallet_entity_report

  from_p02:
    - market_fact_records
    - security_fact_records
    - source_reconciliation_records
    - data_quality_records
    - freshness_records
    - data_conflict_records
    - p02_source_data_fact_report

  from_p01:
    - candidate_master_records
    - discovery_context_records
    - candidate_source_events
    - p01_candidate_intake_report

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - governance_handoff_packet
    - limitation_transfer_packet
    - review_policy_handoff

  required_contracts:
    - p09_input_contract
    - p09_output_contract
    - review_case_contract
    - failure_attribution_contract
    - calibration_candidate_contract
    - p10_upgrade_input_contract
```

P09 启动前必须确认：

```text
Paper Runtime 或 P08 已产生可复盘对象
P09 只读取已 trace / accepted / handoff 的记录
P09 不允许修改上游结论
P09 不允许直接修改策略规则
P09 不允许触发 paper runtime
P09 不允许 live execution
```

---

# 7. Review Case Record

```yaml
review_case_record:
  review_case_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  review_scope:
    review_type:
      - PAPER_POSITION_REVIEW
      - PAPER_CYCLE_REVIEW
      - FAILED_CANDIDATE_REVIEW
      - MISSED_OPPORTUNITY_REVIEW
      - FALSE_POSITIVE_REVIEW
      - FALSE_NEGATIVE_REVIEW
      - SYSTEM_HEALTH_REVIEW

    review_trigger:
      - PAPER_POSITION_CLOSED
      - PAPER_LOSS_THRESHOLD_HIT
      - PAPER_WIN_THRESHOLD_HIT
      - INVALIDATION_TRIGGERED
      - BLOCKED_CANDIDATE_RECHECK
      - DAILY_REVIEW
      - MANUAL_REVIEW_REQUEST
      - SYSTEM_AUDIT

  timeline:
    candidate_discovery_time: datetime | null
    p07_decision_time: datetime | null
    p08_permission_time: datetime | null
    paper_entry_time: datetime | null
    paper_exit_time: datetime | null
    review_time: datetime

  linked_records:
    p01_candidate_id: string
    p02_fact_package_id: string | null
    p03_wallet_entity_package_id: string | null
    p04_chip_structure_package_id: string | null
    p05_evidence_package_id: string | null
    p06_scenario_package_id: string | null
    p07_decision_id: string | null
    p08_permission_id: string | null
    paper_position_id: string | null

  review_status:
    - REVIEW_CREATED
    - REPLAY_READY
    - REPLAY_WITH_GAPS
    - REVIEW_COMPLETED
    - REVIEW_BLOCKED
    - REVIEW_REQUIRES_MANUAL_CHECK

  trace:
    review_case_trace_id: string
    linked_trace_ids: list
```

---

# 8. Replay Input Snapshot Record

P09 必须锁定历史快照，防止事后污染。

```yaml
replay_input_snapshot_record:
  replay_snapshot_id: string
  review_case_id: string
  candidate_id: string

  snapshot_times:
    decision_time_snapshot: datetime | null
    paper_entry_snapshot: datetime | null
    paper_exit_snapshot: datetime | null
    review_time_snapshot: datetime

  snapshot_sources:
    p01_snapshot_path: string | null
    p02_snapshot_path: string | null
    p03_snapshot_path: string | null
    p04_snapshot_path: string | null
    p05_snapshot_path: string | null
    p06_snapshot_path: string | null
    p07_snapshot_path: string | null
    p08_snapshot_path: string | null
    runtime_snapshot_path: string | null

  snapshot_integrity:
    all_required_snapshots_available: boolean
    missing_snapshots: list
    stale_or_overwritten_snapshots: list
    replay_snapshot_quality:
      - REPLAY_SNAPSHOT_COMPLETE
      - REPLAY_SNAPSHOT_USABLE
      - REPLAY_SNAPSHOT_WITH_GAPS
      - REPLAY_SNAPSHOT_LOW_CONFIDENCE
      - REPLAY_SNAPSHOT_UNUSABLE

  restrictions:
    review_time_data_may_not_replace_decision_time_data: true
    current_data_only_allowed_for_post_outcome_context: true
```

---

# 9. Decision Chain Reconstruction Record

```yaml
decision_chain_reconstruction_record:
  decision_chain_id: string
  review_case_id: string
  candidate_id: string

  reconstructed_chain:
    p01_intake_status: string | null
    p02_data_fact_status: string | null
    p03_wallet_entity_status: string | null
    p04_chip_structure_status: string | null
    p05_evidence_status: string | null
    p06_scenario_status: string | null
    p07_strategy_gate_decision: string | null
    p08_paper_runtime_permission: string | null
    paper_runtime_status: string | null

  chain_integrity_checks:
    p01_to_p02_handoff_valid: boolean
    p02_to_p03_handoff_valid: boolean
    p03_to_p04_handoff_valid: boolean
    p04_to_p05_handoff_valid: boolean
    p05_to_p06_handoff_valid: boolean
    p06_to_p07_handoff_valid: boolean
    p07_to_p08_handoff_valid: boolean
    p08_to_runtime_handoff_valid: boolean

  decision_consistency:
    upstream_limitations_respected: boolean
    weak_fields_not_upgraded: boolean
    hard_negative_respected: boolean
    invalidations_bound_correctly: boolean
    runtime_permission_not_bypassed: boolean

  chain_reconstruction_status:
    - CHAIN_RECONSTRUCTED
    - CHAIN_RECONSTRUCTED_WITH_GAPS
    - CHAIN_CONFLICTED
    - CHAIN_BROKEN
    - CHAIN_UNREPLAYABLE

  trace:
    decision_chain_trace_id: string
    stage_trace_ids: list
```

---

# 10. Runtime Path Reconstruction Record

```yaml
runtime_path_reconstruction_record:
  runtime_path_id: string
  review_case_id: string
  candidate_id: string

  runtime_events:
    paper_entry_event_id: string | null
    paper_update_event_ids: list
    paper_exit_event_id: string | null
    risk_event_ids: list

  entry_reconstruction:
    entry_allowed_by_p08: boolean
    entry_price_used_usd: number | null
    reference_quote_price_usd: number | null
    effective_entry_price_usd: number | null
    slippage_applied: boolean
    cost_model_applied: boolean
    entry_trace_id: string | null

  holding_reconstruction:
    position_updates_count: integer
    max_unrealized_gain_pct: number | null
    max_unrealized_loss_pct: number | null
    invalidation_triggered_during_holding: boolean
    risk_events_during_holding: list

  exit_reconstruction:
    exit_time: datetime | null
    exit_reason:
      - TAKE_PROFIT
      - STOP_LOSS
      - INVALIDATION_TRIGGERED
      - TIME_EXIT
      - MANUAL_EXIT
      - RISK_EVENT_EXIT
      - UNKNOWN
    exit_price_used_usd: number | null
    exit_slippage_applied: boolean
    exit_cost_model_applied: boolean

  runtime_path_quality:
    - RUNTIME_PATH_COMPLETE
    - RUNTIME_PATH_USABLE
    - RUNTIME_PATH_WITH_GAPS
    - RUNTIME_PATH_LOW_CONFIDENCE
    - RUNTIME_PATH_UNUSABLE
```

---

# 11. Paper Result Record

```yaml
paper_result_record:
  paper_result_id: string
  review_case_id: string
  candidate_id: string

  pnl:
    gross_pnl_usd: number | null
    gross_pnl_pct: number | null
    net_pnl_usd: number | null
    net_pnl_pct: number | null
    fees_usd: number | null
    slippage_cost_usd: number | null

  trade_result:
    result_status:
      - WIN
      - LOSS
      - BREAKEVEN
      - OPEN
      - INVALID
      - UNKNOWN
    max_favorable_excursion_pct: number | null
    max_adverse_excursion_pct: number | null
    holding_duration_seconds: integer | null

  outcome_context:
    entry_market_cap_usd: number | null
    exit_market_cap_usd: number | null
    market_cap_change_during_position_pct: number | null
    liquidity_change_during_position_pct: number | null
    volume_context: string | null

  result_quality:
    result_data_complete: boolean
    cost_model_applied: boolean
    exit_reason_known: boolean
    result_quality_status:
      - RESULT_HIGH_CONFIDENCE
      - RESULT_USABLE
      - RESULT_WITH_GAPS
      - RESULT_LOW_CONFIDENCE
      - RESULT_UNUSABLE
```

---

# 12. Entry Decision Review Record

```yaml
entry_decision_review_record:
  entry_review_id: string
  review_case_id: string
  candidate_id: string

  p07_decision_review:
    p07_decision: string | null
    strategy_profile: string | null
    gate_decision_reason_cn: string | null
    p07_decision_consistent_with_inputs: boolean | null

  p08_permission_review:
    p08_permission: string | null
    p08_permission_reason_cn: string | null
    p08_permission_consistent_with_execution_data: boolean | null

  entry_quality_checks:
    scenario_still_valid_at_entry: boolean | null
    evidence_still_valid_at_entry: boolean | null
    chip_structure_still_valid_at_entry: boolean | null
    quote_fresh_at_entry: boolean | null
    liquidity_adequate_at_entry: boolean | null
    security_clear_at_entry: boolean | null
    market_position_not_chasing: boolean | null

  entry_review_result:
    - ENTRY_DECISION_VALID
    - ENTRY_DECISION_VALID_WITH_LIMITATIONS
    - ENTRY_DECISION_TOO_EARLY
    - ENTRY_DECISION_TOO_LATE
    - ENTRY_DECISION_CHASING
    - ENTRY_DECISION_INVALIDATED
    - ENTRY_DECISION_UNCLEAR
```

---

# 13. Exit Decision Review Record

```yaml
exit_decision_review_record:
  exit_review_id: string
  review_case_id: string
  candidate_id: string

  exit_context:
    exit_reason: string | null
    exit_time: datetime | null
    exit_price_usd: number | null
    exit_trigger_source:
      - PAPER_RUNTIME
      - INVALIDATION
      - RISK_EVENT
      - MANUAL
      - UNKNOWN

  exit_quality_checks:
    exit_condition_defined_before_entry: boolean
    invalidation_condition_triggered: boolean | null
    stop_loss_or_take_profit_applied: boolean | null
    exit_price_trace_available: boolean
    exit_slippage_applied: boolean

  exit_review_result:
    - EXIT_DECISION_VALID
    - EXIT_TOO_EARLY
    - EXIT_TOO_LATE
    - EXIT_MISSED_INVALIDATION
    - EXIT_RULE_UNDEFINED
    - EXIT_DATA_UNRELIABLE
    - EXIT_UNKNOWN
```

---

# 14. Invalidation Trigger Review Record

```yaml
invalidation_trigger_review_record:
  invalidation_review_id: string
  review_case_id: string
  candidate_id: string

  bound_invalidations:
    invalidation_binding_ids: list
    hard_invalidation_count: integer
    soft_invalidation_count: integer
    watch_invalidation_count: integer

  trigger_review:
    - invalidation_id: string
      condition_cn: string
      triggered: boolean | null
      trigger_time: datetime | null
      detected_by_runtime: boolean
      acted_upon: boolean
      delay_seconds: integer | null

  review_result:
    invalidation_system_worked: boolean
    missed_invalidation_count: integer
    late_detection_count: integer
    false_invalidation_count: integer

  upgrade_implications:
    needs_new_runtime_monitor: boolean
    needs_new_p07_binding: boolean
    needs_new_p08_precheck: boolean
    needs_new_p09_test_case: boolean
```

---

# 15. Failure Attribution Record

这是 P09 的核心输出之一。

```yaml
failure_attribution_record:
  failure_attribution_id: string
  review_case_id: string
  candidate_id: string

  failure_scope:
    failure_type:
      - PAPER_LOSS
      - MISSED_EXIT
      - FALSE_POSITIVE_PAPER_CANDIDATE
      - INVALID_RUNTIME_ALLOWANCE
      - STRATEGY_GATE_FAILURE
      - SCENARIO_MISCLASSIFICATION
      - EVIDENCE_FAILURE
      - CHIP_STRUCTURE_FAILURE
      - WALLET_ENTITY_FAILURE
      - DATA_FACT_FAILURE
      - EXECUTION_SIMULATION_FAILURE
      - SYSTEM_TRACE_FAILURE
      - UNKNOWN_FAILURE

  primary_failure_stage:
    - P01_CANDIDATE_INTAKE
    - P02_SOURCE_DATA_FACT
    - P03_WALLET_ENTITY
    - P04_CHIP_STRUCTURE
    - P05_EVIDENCE
    - P06_SCENARIO_RECOGNITION
    - P07_STRATEGY_GATE
    - P08_EXECUTION_RISK
    - PAPER_RUNTIME
    - GOVERNANCE_CONTROL
    - TRACE_HANDOFF_ACCEPTANCE
    - EXTERNAL_MARKET_RANDOMNESS
    - UNKNOWN

  contributing_failure_stages:
    - stage_id: string
      contribution_level:
        - PRIMARY
        - SECONDARY
        - MINOR
        - UNKNOWN
      reason_cn: string
      source_record_ids: list

  failure_mechanism:
    mechanism_type:
      - DATA_MISSING
      - DATA_STALE
      - FIELD_CONFLICT_IGNORED
      - WEAK_EVIDENCE_OVERUSED
      - COUNTER_EVIDENCE_UNDERWEIGHTED
      - SCENARIO_CONFLICT_IGNORED
      - HARD_NEGATIVE_MISSING
      - STRATEGY_PATTERN_MISMATCH
      - MARKET_POSITION_TOO_LATE
      - QUOTE_SLIPPAGE_UNDERMODELED
      - SECURITY_RISK_UNDETECTED
      - INVALIDATION_MISSED
      - EXIT_RULE_INADEQUATE
      - RUNTIME_STATE_ERROR
      - RANDOM_ADVERSE_MOVE
      - UNKNOWN

  confidence:
    attribution_confidence:
      - HIGH
      - MEDIUM
      - LOW
      - UNKNOWN
    confidence_reason_cn: string

  p10_upgrade_signal:
    upgrade_candidate_required: boolean
    suggested_upgrade_types:
      - FIELD_SCHEMA_UPGRADE
      - DATA_SOURCE_UPGRADE
      - HARD_NEGATIVE_RULE_UPGRADE
      - EVIDENCE_WEIGHT_UPGRADE
      - SCENARIO_POLICY_UPGRADE
      - STRATEGY_GATE_POLICY_UPGRADE
      - EXECUTION_RISK_POLICY_UPGRADE
      - PAPER_RUNTIME_MODEL_UPGRADE
      - TEST_MATRIX_UPGRADE
```

---

# 16. Success Attribution Record

```yaml
success_attribution_record:
  success_attribution_id: string
  review_case_id: string
  candidate_id: string

  success_scope:
    success_type:
      - PAPER_WIN
      - VALID_BLOCK
      - VALID_PAUSE
      - VALID_OBSERVE
      - VALID_HARD_NEGATIVE
      - VALID_SCENARIO_CLASSIFICATION
      - VALID_RISK_REJECTION
      - VALID_RUNTIME_BLOCK

  primary_success_stage:
    - P02_SOURCE_DATA_FACT
    - P03_WALLET_ENTITY
    - P04_CHIP_STRUCTURE
    - P05_EVIDENCE
    - P06_SCENARIO_RECOGNITION
    - P07_STRATEGY_GATE
    - P08_EXECUTION_RISK
    - PAPER_RUNTIME
    - GOVERNANCE_CONTROL
    - UNKNOWN

  success_mechanism:
    mechanism_type:
      - CHIP_RETENTION_CORRECTLY_IDENTIFIED
      - DISTRIBUTION_RISK_CORRECTLY_BLOCKED
      - SCENARIO_RECOGNITION_CORRECT
      - HARD_NEGATIVE_CORRECT
      - EXECUTION_RISK_BLOCK_CORRECT
      - INVALIDATION_MONITOR_WORKED
      - COST_MODEL_REALISTIC
      - MARKET_RANDOMNESS_FAVORABLE
      - UNKNOWN

  validation_quality:
    success_due_to_system_logic: boolean | null
    success_due_to_randomness: boolean | null
    paper_model_overstated_result: boolean | null
    confirmation_needed: boolean

  p10_upgrade_signal:
    reinforce_existing_rule: boolean
    create_regression_test_case: boolean
```

---

# 17. Misclassification Review Record

```yaml
misclassification_review_record:
  misclassification_id: string
  review_case_id: string
  candidate_id: string

  reviewed_layer:
    - WALLET_ROLE
    - CHIP_STRUCTURE
    - EVIDENCE
    - SCENARIO
    - STRATEGY_GATE
    - EXECUTION_RISK

  original_classification:
    source_stage: string
    classification_type: string
    classification_value: string | null
    confidence_level: string | null

  post_outcome_assessment:
    classification_still_valid: boolean | null
    likely_corrected_classification: string | null
    correction_reason_cn: string

  error_type:
    - FALSE_POSITIVE
    - FALSE_NEGATIVE
    - OVERCONFIDENT_WEAK_SIGNAL
    - UNDERWEIGHTED_COUNTER_SIGNAL
    - CONTEXT_MISREAD
    - DATA_STALENESS_ERROR
    - INSUFFICIENT_EVIDENCE
    - UNKNOWN

  p10_upgrade_signal:
    needs_threshold_adjustment: boolean
    needs_new_counter_signal: boolean
    needs_new_context_rule: boolean
    needs_new_test_case: boolean
```

---

# 18. Gate Error Review Record

```yaml
gate_error_review_record:
  gate_error_id: string
  review_case_id: string
  candidate_id: string

  gate_stage:
    - P07_STRATEGY_GATE
    - P08_EXECUTION_RISK

  original_decision:
    decision_record_id: string
    decision_value: string
    decision_reason_cn: string

  review_assessment:
    decision_was_correct_given_available_data: boolean | null
    decision_was_correct_given_later_outcome: boolean | null
    issue_type:
      - CORRECT_DECISION_BAD_OUTCOME
      - WRONG_DECISION_BAD_OUTCOME
      - WRONG_BLOCK_MISSED_OPPORTUNITY
      - CORRECT_BLOCK
      - OVERLY_PERMISSIVE
      - OVERLY_CONSERVATIVE
      - UNKNOWN

  gate_error_mechanism:
    - HARD_NEGATIVE_MISSING
    - HARD_NEGATIVE_TOO_STRICT
    - SCENARIO_CONFLICT_UNDERWEIGHTED
    - MARKET_POSITION_CONTEXT_MISREAD
    - SECURITY_RECHECK_MISSING
    - SLIPPAGE_MODEL_WEAK
    - RISK_LIMIT_NOT_APPLIED
    - INVALIDATION_NOT_BOUND
    - UNKNOWN

  upgrade_candidate_required: boolean
```

---

# 19. Runtime Simulation Quality Record

```yaml
runtime_simulation_quality_record:
  simulation_quality_id: string
  review_case_id: string
  candidate_id: string

  simulation_checks:
    effective_entry_price_used: boolean
    effective_exit_price_used: boolean
    slippage_model_applied: boolean
    fee_model_applied: boolean
    liquidity_capacity_respected: boolean
    sellability_risk_recorded: boolean
    invalidation_monitor_recorded: boolean

  quality_status:
    - SIMULATION_HIGH_CONFIDENCE
    - SIMULATION_USABLE
    - SIMULATION_WITH_GAPS
    - SIMULATION_OVEROPTIMISTIC
    - SIMULATION_UNUSABLE

  distortion_sources:
    - NO_SLIPPAGE
    - NO_FEES
    - PRICE_SOURCE_STALE
    - LIQUIDITY_TOO_THIN
    - EXIT_PRICE_UNRELIABLE
    - SECURITY_OR_SELLABILITY_IGNORED
    - INVALIDATION_NOT_MONITORED

  upgrade_signal:
    improve_cost_model: boolean
    improve_slippage_model: boolean
    improve_exit_model: boolean
    improve_liquidity_model: boolean
```

---

# 20. Data Gap Impact Record

```yaml
data_gap_impact_record:
  data_gap_impact_id: string
  review_case_id: string
  candidate_id: string

  impacted_stage:
    - P02_SOURCE_DATA_FACT
    - P03_WALLET_ENTITY
    - P04_CHIP_STRUCTURE
    - P05_EVIDENCE
    - P06_SCENARIO_RECOGNITION
    - P07_STRATEGY_GATE
    - P08_EXECUTION_RISK
    - PAPER_RUNTIME

  data_gap:
    gap_id: string | null
    missing_or_weak_field: string
    field_source_stage: string
    gap_type:
      - MISSING
      - STALE
      - CONFLICTED
      - WEAK_USE_ONLY
      - TRACE_MISSING
      - LOW_COVERAGE

  impact_assessment:
    affected_decision: string
    likely_impact:
      - CAUSED_FAILURE
      - CONTRIBUTED_TO_FAILURE
      - DID_NOT_MATTER
      - UNKNOWN
    impact_reason_cn: string

  upgrade_signal:
    field_required_upgrade: boolean
    source_priority_upgrade: boolean
    freshness_policy_upgrade: boolean
```

---

# 21. Trace / Handoff / Acceptance Integrity Reviews

```yaml
trace_integrity_review_record:
  trace_review_id: string
  review_case_id: string

  trace_checks:
    every_stage_has_trace: boolean
    every_output_has_source_trace: boolean
    every_decision_has_decision_trace: boolean
    every_handoff_has_handoff_trace: boolean
    runtime_events_have_trace: boolean

  trace_gaps:
    missing_trace_ids: list
    broken_trace_links: list

  trace_integrity_status:
    - TRACE_COMPLETE
    - TRACE_USABLE_WITH_GAPS
    - TRACE_BROKEN
    - TRACE_UNUSABLE
```

```yaml
handoff_integrity_review_record:
  handoff_review_id: string
  review_case_id: string

  handoff_checks:
    p01_to_p02_valid: boolean
    p02_to_p03_valid: boolean
    p03_to_p04_valid: boolean
    p04_to_p05_valid: boolean
    p05_to_p06_valid: boolean
    p06_to_p07_valid: boolean
    p07_to_p08_valid: boolean
    p08_to_runtime_valid: boolean

  limitation_transfer_checks:
    weak_use_limitations_preserved: boolean
    forbidden_uses_preserved: boolean
    gap_tags_preserved: boolean
    no_stage_bypassed: boolean

  handoff_integrity_status:
    - HANDOFF_COMPLETE
    - HANDOFF_USABLE_WITH_GAPS
    - HANDOFF_BROKEN
    - HANDOFF_UNUSABLE
```

```yaml
acceptance_integrity_review_record:
  acceptance_review_id: string
  review_case_id: string

  acceptance_checks:
    every_stage_had_acceptance: boolean
    ready_with_gaps_were_propagated: boolean
    rejected_or_blocked_items_not_used_downstream: boolean
    acceptance_status_not_overridden: boolean

  acceptance_integrity_status:
    - ACCEPTANCE_COMPLETE
    - ACCEPTANCE_WITH_GAPS
    - ACCEPTANCE_BROKEN
    - ACCEPTANCE_UNUSABLE
```

---

# 22. Calibration Candidate Record

P09 的校准建议必须结构化，不能只写“需要优化”。

```yaml
calibration_candidate_record:
  calibration_candidate_id: string
  review_case_id: string
  candidate_id: string

  calibration_target:
    target_stage:
      - P02_SOURCE_DATA_FACT
      - P03_WALLET_ENTITY
      - P04_CHIP_STRUCTURE
      - P05_EVIDENCE
      - P06_SCENARIO_RECOGNITION
      - P07_STRATEGY_GATE
      - P08_EXECUTION_RISK
      - PAPER_RUNTIME
      - GOVERNANCE
      - TRACE_HANDOFF_ACCEPTANCE

    target_type:
      - FIELD_SCHEMA
      - QUALITY_THRESHOLD
      - FRESHNESS_POLICY
      - SCORING_WEIGHT
      - HARD_NEGATIVE_RULE
      - SCENARIO_POLICY
      - STRATEGY_PROFILE
      - SLIPPAGE_MODEL
      - COST_MODEL
      - INVALIDATION_RULE
      - TEST_CASE
      - REPORT_FIELD

  current_behavior:
    current_rule_or_field: string | null
    observed_problem_cn: string

  proposed_calibration:
    proposal_cn: string
    expected_effect_cn: string
    risk_of_change_cn: string

  evidence_basis:
    supporting_review_records: list
    confidence:
      - HIGH
      - MEDIUM
      - LOW
      - NEED_MORE_SAMPLES

  p10_action:
    send_to_p10: boolean
    required_p10_review_type:
      - SCHEMA_UPGRADE_REVIEW
      - RULE_UPGRADE_REVIEW
      - PARAMETER_CALIBRATION_REVIEW
      - TEST_MATRIX_UPGRADE_REVIEW
      - TOOL_BINDING_UPGRADE_REVIEW
      - GOVERNANCE_REVIEW
```

---

# 23. Missed Negative Rule Record

```yaml
missed_negative_rule_record:
  missed_rule_id: string
  review_case_id: string
  candidate_id: string

  missed_risk:
    risk_type:
      - ACTIVE_DISTRIBUTION_NOT_BLOCKED
      - EXIT_LIQUIDITY_TRAP_NOT_BLOCKED
      - HIGH_COUNTERPARTY_PRESSURE_NOT_BLOCKED
      - DATA_STALENESS_NOT_BLOCKED
      - SECURITY_RISK_NOT_BLOCKED
      - SLIPPAGE_RISK_NOT_BLOCKED
      - MARKET_POSITION_CHASING_NOT_BLOCKED
      - INVALIDATION_NOT_BLOCKED

  observed_failure:
    failure_attribution_id: string
    failure_summary_cn: string

  proposed_rule:
    target_stage:
      - P06_SCENARIO_RECOGNITION
      - P07_STRATEGY_GATE
      - P08_EXECUTION_RISK
    proposed_condition_cn: string
    proposed_result:
      - BLOCK
      - PAUSE
      - OBSERVE
      - HUMAN_CONFIRMATION_REQUIRED

  p10_upgrade_required: boolean
```

---

# 24. New Test Case Candidate Record

```yaml
new_test_case_candidate_record:
  test_case_candidate_id: string
  review_case_id: string

  target_test_matrix:
    - P02_TEST_MATRIX
    - P03_TEST_MATRIX
    - P04_TEST_MATRIX
    - P05_TEST_MATRIX
    - P06_TEST_MATRIX
    - P07_TEST_MATRIX
    - P08_TEST_MATRIX
    - PAPER_RUNTIME_TEST_MATRIX

  test_case:
    name_cn: string
    input_condition_cn: string
    expected_output_cn: string
    expected_block_or_allow: string
    reason_cn: string

  priority:
    - HIGH
    - MEDIUM
    - LOW

  p10_upgrade_required: boolean
```

---

# 25. Review Case Library Record

```yaml
review_case_library_record:
  library_record_id: string
  review_case_id: string
  candidate_id: string

  classification:
    case_type:
      - TRUE_POSITIVE
      - FALSE_POSITIVE
      - TRUE_NEGATIVE
      - FALSE_NEGATIVE
      - AMBIGUOUS
      - SYSTEM_FAILURE
      - DATA_FAILURE
      - EXECUTION_SIMULATION_FAILURE

    scenario_family: string | null
    strategy_profile: string | null
    outcome_bucket:
      - LARGE_WIN
      - SMALL_WIN
      - BREAKEVEN
      - SMALL_LOSS
      - LARGE_LOSS
      - BLOCKED_CORRECTLY
      - MISSED_OPPORTUNITY
      - UNKNOWN

  tags:
    - CHIP_RETENTION_CASE
    - DISTRIBUTION_RISK_CASE
    - COUNTERPARTY_PRESSURE_CASE
    - SECOND_STAGE_EXPANSION_CASE
    - EXIT_LIQUIDITY_TRAP_CASE
    - SLIPPAGE_MODEL_CASE
    - DATA_GAP_CASE

  reusable_for:
    - THRESHOLD_CALIBRATION
    - TEST_MATRIX
    - POLICY_REVIEW
    - TRAINING_SAMPLE
    - HUMAN_REVIEW
```

---

# 26. P10 Upgrade Candidate Data Request Packet

```yaml
p10_upgrade_candidate_data_request_packet:
  packet_id: string
  from_controller: P09_REVIEW_REPLAY_CONTROLLER
  to_controller: P10_SELF_UPGRADE_CONTROLLER
  generated_at: datetime

  review_scope:
    review_case_ids: list
    candidate_ids: list
    review_period_start: datetime | null
    review_period_end: datetime | null

  upgrade_inputs_available:
    failure_attribution_records_path: string
    success_attribution_records_path: string
    misclassification_review_records_path: string
    gate_error_review_records_path: string
    runtime_simulation_quality_records_path: string
    data_gap_impact_records_path: string
    missed_negative_rule_records_path: string
    calibration_candidate_records_path: string
    new_test_case_candidate_records_path: string
    review_case_library_records_path: string

  p10_required_upgrade_tasks:
    - evaluate_schema_upgrade_candidates
    - evaluate_rule_upgrade_candidates
    - evaluate_threshold_calibration_candidates
    - evaluate_hard_negative_rule_candidates
    - evaluate_evidence_weight_upgrade_candidates
    - evaluate_scenario_policy_upgrade_candidates
    - evaluate_strategy_gate_policy_upgrade_candidates
    - evaluate_execution_risk_policy_upgrade_candidates
    - evaluate_paper_runtime_model_upgrade_candidates
    - evaluate_test_matrix_upgrade_candidates
    - evaluate_governance_review_required

  restrictions:
    - P09_PROPOSES_ONLY
    - P10_MUST_REVIEW_BEFORE_CHANGE
    - NO_DIRECT_RULE_MUTATION
    - NO_AUTO_DEPLOY
    - LIVE_EXECUTION_FORBIDDEN

  priority:
    high_priority_upgrade_candidates: list
    medium_priority_upgrade_candidates: list
    low_priority_upgrade_candidates: list
```

---

# 27. P09 to P10 Handoff Packet

```yaml
p09_to_p10_handoff_packet:
  packet_id: string
  packet_type: P09_TO_P10_REVIEW_REPLAY_HANDOFF
  generated_at: datetime

  route:
    from_controller: P09_REVIEW_REPLAY_CONTROLLER
    to_controller: P10_SELF_UPGRADE_CONTROLLER

  upstream_control:
    p08_runtime_handoff_packet_id: string | null
    p09_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  review_scope:
    review_case_count_total: integer
    completed_review_count: integer
    review_with_gaps_count: integer
    blocked_review_count: integer
    manual_check_required_count: integer

  review_package:
    review_case_records_path: string
    replay_input_snapshot_records_path: string
    decision_chain_reconstruction_records_path: string
    runtime_path_reconstruction_records_path: string
    paper_result_records_path: string
    entry_decision_review_records_path: string
    exit_decision_review_records_path: string
    invalidation_trigger_review_records_path: string
    failure_attribution_records_path: string
    success_attribution_records_path: string
    misclassification_review_records_path: string
    gate_error_review_records_path: string
    runtime_simulation_quality_records_path: string
    data_gap_impact_records_path: string
    trace_integrity_review_records_path: string
    handoff_integrity_review_records_path: string
    acceptance_integrity_review_records_path: string
    calibration_candidate_records_path: string
    missed_negative_rule_records_path: string
    new_test_case_candidate_records_path: string
    review_case_library_records_path: string

  p10_data_request:
    p10_upgrade_candidate_data_request_packet_path: string
    required_p10_tasks: list
    high_priority_upgrade_candidates: list

  quality:
    review_quality_report_path: string
    attribution_confidence_summary: object
    replay_integrity_summary: object
    runtime_simulation_quality_summary: object
    trace_handoff_acceptance_summary: object

  limitations:
    - REVIEW_REPLAY_ONLY
    - PROPOSE_UPGRADES_ONLY
    - NO_DIRECT_RULE_MUTATION
    - NO_RUNTIME_ACTION
    - NO_LIVE_EXECUTION

  downstream_permission:
    allowed:
      - P10_SELF_UPGRADE_CONTROLLER
    forbidden:
      - DIRECT_STRATEGY_RULE_CHANGE
      - DIRECT_RUNTIME_CHANGE
      - LIVE_EXECUTION

  read_instruction:
    p10_must_read_first:
      - p09_to_p10_handoff_packet
      - p10_upgrade_candidate_data_request_packet
      - failure_attribution_records
      - calibration_candidate_records
      - missed_negative_rule_records
      - new_test_case_candidate_records
      - review_case_library_records
```

---

# 28. P09 Gap Policy

```yaml
p09_gap_policy:
  BLOCKING_GAP:
    result: P09_BLOCKED
    examples:
      - no_review_target
      - trace_missing
      - handoff_missing
      - acceptance_missing
      - live_execution_requested
      - direct_rule_mutation_requested

  CRITICAL_GAP:
    result: P09_REJECTED
    examples:
      - no_runtime_result_and_no_blocked_case_to_review
      - decision_chain_unreplayable
      - paper_result_untraceable
      - all_stage_snapshots_missing
      - output_contract_missing

  HIGH_GAP:
    result: P09_READY_WITH_GAPS
    downstream_permission: P10_LIMITED
    examples:
      - missing_p04_chip_snapshot
      - missing_p05_evidence_bundle
      - missing_p08_quote_snapshot
      - incomplete_runtime_events
      - attribution_confidence_low

  MEDIUM_GAP:
    result: P09_READY_WITH_GAPS
    downstream_permission: P10_ALLOWED_WITH_LIMITATIONS
    examples:
      - cost_model_missing
      - exit_reason_unclear
      - partial_trace_gap
      - missing_historical_context

  LOW_GAP:
    result: P09_READY_WITH_GAPS
    downstream_permission: P10_ALLOWED_WITH_NOTE
    examples:
      - optional_report_metadata_missing
      - minor_runtime_event_gap
      - noncritical_review_tag_missing
```

---

# 29. P09 Hard Negative Rules

```yaml
p09_hard_negative_rules:
  - rule_id: P09_BLOCK_001
    name: 无复盘对象
    condition: no_review_target == true
    result: P09_BLOCKED
    reason: P09 不能在无 review target 时启动

  - rule_id: P09_BLOCK_002
    name: 无可追踪运行或决策记录
    condition: paper_runtime_trace_missing == true and p07_p08_decision_records_missing == true
    result: P09_REJECTED
    reason: 无法回放决策链或运行链

  - rule_id: P09_BLOCK_003
    name: 用当前数据覆盖历史快照
    condition: review_time_data_used_as_decision_time_snapshot == true
    result: P09_BLOCKED
    reason: 回放必须锁定当时快照，禁止事后数据污染

  - rule_id: P09_BLOCK_004
    name: 直接修改策略规则
    condition: p09_attempts_direct_rule_mutation == true
    result: P09_BLOCKED
    reason: P09 只能提出升级候选，不能直接改规则

  - rule_id: P09_BLOCK_005
    name: 直接修改运行状态
    condition: p09_attempts_runtime_state_mutation == true
    result: P09_BLOCKED
    reason: P09 只能复盘，不能改变运行状态

  - rule_id: P09_BLOCK_006
    name: 归因无证据链
    condition: failure_attribution_created == true and source_trace_ids_missing == true
    result: P09_BLOCKED
    reason: 失败归因必须可追踪

  - rule_id: P09_BLOCK_007
    name: 把单个样本直接升级为全局规则
    condition: single_case_auto_promoted_to_global_rule == true
    result: P09_BLOCKED
    reason: 单样本只能生成 upgrade candidate，不能直接变成全局规则

  - rule_id: P09_BLOCK_008
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P09_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 30. P09 状态机专业版

```yaml
p09_review_replay_state_machine:
  states:
    - P09_UNINITIALIZED
    - P09_CONTEXT_LOADED
    - P09_REVIEW_TARGET_SELECTED
    - P09_INPUT_MANIFEST_BUILT
    - P09_REVIEW_CASE_CREATED
    - P09_REPLAY_SNAPSHOTS_LOCKED
    - P09_DECISION_CHAIN_RECONSTRUCTED
    - P09_RUNTIME_PATH_RECONSTRUCTED
    - P09_PAPER_RESULT_BUILT
    - P09_ENTRY_DECISION_REVIEWED
    - P09_EXIT_DECISION_REVIEWED
    - P09_INVALIDATION_REVIEWED
    - P09_FAILURE_ATTRIBUTION_BUILT
    - P09_SUCCESS_ATTRIBUTION_BUILT
    - P09_MISCLASSIFICATION_REVIEWED
    - P09_GATE_ERROR_REVIEWED
    - P09_RUNTIME_SIMULATION_REVIEWED
    - P09_DATA_GAP_IMPACT_ANALYZED
    - P09_TRACE_INTEGRITY_REVIEWED
    - P09_HANDOFF_INTEGRITY_REVIEWED
    - P09_ACCEPTANCE_INTEGRITY_REVIEWED
    - P09_CALIBRATION_CANDIDATES_BUILT
    - P09_MISSED_NEGATIVE_RULES_BUILT
    - P09_NEW_TEST_CASE_CANDIDATES_BUILT
    - P09_REVIEW_LIBRARY_UPDATED
    - P09_P10_DATA_REQUEST_BUILT
    - P09_READY_FOR_ACCEPTANCE
    - P09_ACCEPTANCE_READY
    - P09_READY_FOR_P10_HANDOFF
    - P09_READY_WITH_GAPS
    - P09_REJECTED
    - P09_BLOCKED

  critical_transitions:
    - from: P09_REVIEW_TARGET_SELECTED
      to: P09_INPUT_MANIFEST_BUILT
      condition: review_target_available == true

    - from: P09_INPUT_MANIFEST_BUILT
      to: P09_REVIEW_CASE_CREATED
      condition: review_case_record_created == true

    - from: P09_REVIEW_CASE_CREATED
      to: P09_REPLAY_SNAPSHOTS_LOCKED
      condition: replay_input_snapshot_record_created == true

    - from: P09_REPLAY_SNAPSHOTS_LOCKED
      to: P09_DECISION_CHAIN_RECONSTRUCTED
      condition: decision_chain_reconstruction_record_created == true

    - from: P09_DECISION_CHAIN_RECONSTRUCTED
      to: P09_RUNTIME_PATH_RECONSTRUCTED
      condition: runtime_path_reconstruction_record_created == true

    - from: P09_RUNTIME_PATH_RECONSTRUCTED
      to: P09_PAPER_RESULT_BUILT
      condition: paper_result_record_created == true

    - from: P09_PAPER_RESULT_BUILT
      to: P09_ENTRY_DECISION_REVIEWED
      condition: entry_decision_review_record_created == true

    - from: P09_ENTRY_DECISION_REVIEWED
      to: P09_EXIT_DECISION_REVIEWED
      condition: exit_decision_review_record_created == true

    - from: P09_EXIT_DECISION_REVIEWED
      to: P09_FAILURE_ATTRIBUTION_BUILT
      condition: failure_or_success_attribution_required == true

    - from: P09_FAILURE_ATTRIBUTION_BUILT
      to: P09_MISCLASSIFICATION_REVIEWED
      condition: misclassification_review_records_created == true

    - from: P09_MISCLASSIFICATION_REVIEWED
      to: P09_GATE_ERROR_REVIEWED
      condition: gate_error_review_records_created == true

    - from: P09_GATE_ERROR_REVIEWED
      to: P09_RUNTIME_SIMULATION_REVIEWED
      condition: runtime_simulation_quality_records_created == true

    - from: P09_RUNTIME_SIMULATION_REVIEWED
      to: P09_DATA_GAP_IMPACT_ANALYZED
      condition: data_gap_impact_records_created == true

    - from: P09_DATA_GAP_IMPACT_ANALYZED
      to: P09_CALIBRATION_CANDIDATES_BUILT
      condition: calibration_candidate_records_created == true

    - from: P09_CALIBRATION_CANDIDATES_BUILT
      to: P09_P10_DATA_REQUEST_BUILT
      condition: p10_upgrade_candidate_data_request_packet_created == true

    - from: P09_P10_DATA_REQUEST_BUILT
      to: P09_READY_FOR_ACCEPTANCE
      condition: p09_output_contract_ready == true

    - from: P09_READY_FOR_ACCEPTANCE
      to: P09_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P09_ACCEPTANCE_READY
      to: P09_READY_FOR_P10_HANDOFF
      condition: p09_to_p10_handoff_packet_created == true
```

---

# 31. P09 文件体系

## 31.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p09_review_replay_controller/
```

必须创建：

```text
p09_review_replay_controller.yaml
p09_review_replay_context.md
p09_input_contract.yaml
p09_output_contract.yaml
review_case_schema.yaml
replay_input_snapshot_schema.yaml
decision_chain_reconstruction_schema.yaml
runtime_path_reconstruction_schema.yaml
paper_result_schema.yaml
entry_decision_review_schema.yaml
exit_decision_review_schema.yaml
invalidation_trigger_review_schema.yaml
failure_attribution_schema.yaml
success_attribution_schema.yaml
misclassification_review_schema.yaml
gate_error_review_schema.yaml
runtime_simulation_quality_schema.yaml
data_gap_impact_schema.yaml
trace_integrity_review_schema.yaml
handoff_integrity_review_schema.yaml
acceptance_integrity_review_schema.yaml
calibration_candidate_schema.yaml
missed_negative_rule_schema.yaml
new_test_case_candidate_schema.yaml
review_case_library_schema.yaml
review_type_policy.yaml
replay_snapshot_policy.yaml
failure_attribution_policy.yaml
success_attribution_policy.yaml
misclassification_review_policy.yaml
runtime_simulation_quality_policy.yaml
calibration_candidate_policy.yaml
review_gap_policy.yaml
review_hard_negative_rules.yaml
review_replay_state_machine.yaml
review_trace_requirements.yaml
p10_upgrade_candidate_data_request_packet_contract.yaml
p09_to_p10_handoff_contract.yaml
p09_acceptance_criteria.md
p09_storage_constitution.md
p09_test_matrix.yaml
p09_report_model.yaml
p09_review_checklist.md
her_p09_execution_protocol.md
```

---

## 31.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p09_review_replay/
  input_manifest/
  review_cases/
  replay_snapshots/
  decision_chain/
  runtime_path/
  paper_results/
  entry_reviews/
  exit_reviews/
  invalidation_reviews/
  failure_attribution/
  success_attribution/
  misclassification_reviews/
  gate_error_reviews/
  runtime_simulation_quality/
  data_gap_impact/
  trace_integrity/
  handoff_integrity/
  acceptance_integrity/
  calibration_candidates/
  missed_negative_rules/
  new_test_case_candidates/
  review_case_library/
  p10_data_requests/
  manual_checks/
  quality/
  gaps/
  rejected_reviews/
  blocked_reviews/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 32. P09 测试矩阵

```yaml
p09_test_matrix:
  - test_id: P09_TEST_001
    name: 已关闭纸面仓位，完整 P01-P08 与 runtime trace
    expected_status: P09_READY_FOR_P10_HANDOFF
    expected_outputs:
      - review_case_record
      - failure_or_success_attribution
      - calibration_candidate_record

  - test_id: P09_TEST_002
    name: 缺 review target
    expected_status: P09_BLOCKED

  - test_id: P09_TEST_003
    name: 缺 runtime trace，但有 P07/P08 阻断记录
    expected_status: P09_READY_WITH_GAPS
    expected_review_type: FAILED_CANDIDATE_REVIEW

  - test_id: P09_TEST_004
    name: 用当前数据覆盖 decision_time_snapshot
    expected_status: P09_BLOCKED

  - test_id: P09_TEST_005
    name: PAPER_CANDIDATE 后亏损，发现 P06 场景冲突被低估
    expected_output:
      - failure_attribution_record
      - scenario_policy_calibration_candidate

  - test_id: P09_TEST_006
    name: PAPER_RUNTIME_ALLOWED 后立即触发 hard invalidation
    expected_output:
      - invalidation_trigger_review_record
      - p08_or_runtime_upgrade_candidate

  - test_id: P09_TEST_007
    name: P08 报价一致但纸面成交明显过于乐观
    expected_output:
      - runtime_simulation_quality_record
      - slippage_model_upgrade_candidate

  - test_id: P09_TEST_008
    name: 强反证存在但 P07 仍放行
    expected_output:
      - gate_error_review_record
      - hard_negative_rule_candidate

  - test_id: P09_TEST_009
    name: BLOCK 后 token 后续大幅上涨
    expected_review_type: FALSE_NEGATIVE_REVIEW
    expected_output:
      - missed_opportunity_review
      - overconservative_gate_candidate

  - test_id: P09_TEST_010
    name: PAUSE 后数据刷新证明风险扩大
    expected_output:
      - success_attribution_record
      - reinforce_pause_rule_candidate

  - test_id: P09_TEST_011
    name: 缺 P04 筹码快照
    expected_status: P09_READY_WITH_GAPS
    expected_limitation: ATTRIBUTION_CONFIDENCE_LOW

  - test_id: P09_TEST_012
    name: failure attribution 无 source trace
    expected_status: P09_BLOCKED

  - test_id: P09_TEST_013
    name: 单个失败样本直接修改全局策略
    expected_status: P09_BLOCKED

  - test_id: P09_TEST_014
    name: 成功样本但没有扣除滑点和费用
    expected_output:
      - success_attribution_with_simulation_caveat
      - cost_model_upgrade_candidate

  - test_id: P09_TEST_015
    name: Trace / Handoff / Acceptance 缺失导致无法复盘
    expected_status: P09_REJECTED_OR_READY_WITH_GAPS

  - test_id: P09_TEST_016
    name: live execution requested
    expected_status: P09_BLOCKED
```

---

# 33. P09 报告模型

```yaml
p09_review_replay_report:
  report_id: string
  generated_at: datetime
  controller_id: P09_REVIEW_REPLAY_CONTROLLER

  summary:
    review_case_count_total: integer
    completed_review_count: integer
    ready_with_gaps_count: integer
    blocked_review_count: integer
    rejected_review_count: integer
    manual_check_required_count: integer

  review_type_distribution:
    paper_position_review_count: integer
    failed_candidate_review_count: integer
    missed_opportunity_review_count: integer
    false_positive_review_count: integer
    false_negative_review_count: integer
    system_health_review_count: integer

  outcome_summary:
    win_count: integer
    loss_count: integer
    breakeven_count: integer
    blocked_correctly_count: integer
    missed_opportunity_count: integer
    unknown_outcome_count: integer

  attribution_summary:
    primary_failure_stage_distribution: object
    primary_success_stage_distribution: object
    common_failure_mechanisms: list
    common_success_mechanisms: list

  gate_error_summary:
    p07_gate_error_count: integer
    p08_execution_risk_error_count: integer
    overly_permissive_count: integer
    overly_conservative_count: integer

  runtime_simulation_summary:
    simulation_high_confidence_count: integer
    simulation_with_gaps_count: integer
    simulation_overoptimistic_count: integer
    cost_model_missing_count: integer
    slippage_model_missing_count: integer

  data_gap_impact_summary:
    high_impact_data_gap_count: integer
    most_common_missing_fields: list
    stale_data_failure_count: integer
    conflict_ignored_count: integer

  upgrade_candidate_summary:
    calibration_candidate_count: integer
    missed_negative_rule_count: integer
    new_test_case_candidate_count: integer
    high_priority_upgrade_count: integer

  p10_handoff_summary:
    p10_handoff_ready: boolean
    p10_required_tasks: list
    high_priority_upgrade_candidates: list

  compliance:
    direct_rule_mutation_attempted: false
    runtime_state_mutation_attempted: false
    live_execution_path_detected: false
    review_time_data_used_as_decision_snapshot: false
```

---

# 34. HER P09 执行协议

```text
HER 执行 P09 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P09 controller context
4. 读取 Paper Runtime 输出与 P08 handoff
5. 读取 P07 / P06 / P05 / P04 / P03 / P02 / P01 相关 trace 和 handoff
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P09 input_manifest
8. 选择 review target
9. 建立 review_case_record
10. 锁定 replay_input_snapshot
11. 重建 P01-P08 decision chain
12. 重建 Paper Runtime path
13. 建立 paper_result_record
14. 复盘 entry_decision
15. 复盘 exit_decision
16. 复盘 invalidation trigger
17. 生成 failure_attribution_record
18. 生成 success_attribution_record
19. 生成 misclassification_review_record
20. 生成 gate_error_review_record
21. 生成 runtime_simulation_quality_record
22. 生成 data_gap_impact_record
23. 生成 trace_integrity_review_record
24. 生成 handoff_integrity_review_record
25. 生成 acceptance_integrity_review_record
26. 生成 calibration_candidate_record
27. 生成 missed_negative_rule_record
28. 生成 new_test_case_candidate_record
29. 更新 review_case_library_record
30. 生成 P09 gap report
31. 生成 p10_upgrade_candidate_data_request_packet
32. 写入 P09 trace
33. 生成 p09_review_replay_report
34. 生成 p09_to_p10_handoff_packet
35. 执行 P09 acceptance
36. 只允许 handoff 给 P10
```

禁止：

```text
1. 不允许无 review target 启动 P09
2. 不允许用当前数据覆盖历史决策快照
3. 不允许无 trace 做失败归因
4. 不允许单个样本直接修改全局规则
5. 不允许直接更新策略阈值
6. 不允许直接修改 P07 / P08 / Paper Runtime
7. 不允许触发新的 paper runtime
8. 不允许 live execution
9. 不允许钱包签名
10. 不允许自动部署
```

---

# 35. 给 HER 的专业化任务书

```text
任务名称：建立 P09 Review Replay Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p09_review_replay_controller/ 下建立 P09 Review Replay Controller。该控制器不是纸面日报脚本，也不是简单失败总结模块，而是复盘回放、决策链重建、运行路径重建、失败归因、成功归因、误判分析、数据缺口影响分析、仿真质量评估、校准候选生成与 P10 升级候选交接控制器。它负责读取 Paper-only Runtime 输出、P08 执行风控记录、P07 策略门控记录、P06 场景识别、P05 证据、P04 筹码结构、P03 钱包实体、P02 数据事实和 P01 候选建档，重建当时的输入、决策、运行、退出和结果，并把可升级内容交给 P10 Self Upgrade Controller。

核心原则：
1. P09 只做复盘、回放、归因和升级候选生成。
2. P09 不直接修改策略规则。
3. P09 不直接修改阈值。
4. P09 不直接修改运行状态。
5. P09 不触发新的 paper runtime。
6. P09 不允许 live execution。
7. P09 必须锁定 decision_time_snapshot，禁止用当前数据覆盖历史判断。
8. P09 必须重建 P01-P08 决策链。
9. P09 必须重建 Paper Runtime 路径。
10. P09 必须同时做失败归因和成功归因。
11. P09 必须识别数据缺口、误判、门控错误、仿真失真。
12. P09 必须生成 P10 Upgrade Candidate Data Request Packet。
13. P09 只能交接给 P10 Self Upgrade Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p09_review_replay_controller/

需要创建系统文件：
1. p09_review_replay_controller.yaml
2. p09_review_replay_context.md
3. p09_input_contract.yaml
4. p09_output_contract.yaml
5. review_case_schema.yaml
6. replay_input_snapshot_schema.yaml
7. decision_chain_reconstruction_schema.yaml
8. runtime_path_reconstruction_schema.yaml
9. paper_result_schema.yaml
10. entry_decision_review_schema.yaml
11. exit_decision_review_schema.yaml
12. invalidation_trigger_review_schema.yaml
13. failure_attribution_schema.yaml
14. success_attribution_schema.yaml
15. misclassification_review_schema.yaml
16. gate_error_review_schema.yaml
17. runtime_simulation_quality_schema.yaml
18. data_gap_impact_schema.yaml
19. trace_integrity_review_schema.yaml
20. handoff_integrity_review_schema.yaml
21. acceptance_integrity_review_schema.yaml
22. calibration_candidate_schema.yaml
23. missed_negative_rule_schema.yaml
24. new_test_case_candidate_schema.yaml
25. review_case_library_schema.yaml
26. review_type_policy.yaml
27. replay_snapshot_policy.yaml
28. failure_attribution_policy.yaml
29. success_attribution_policy.yaml
30. misclassification_review_policy.yaml
31. runtime_simulation_quality_policy.yaml
32. calibration_candidate_policy.yaml
33. review_gap_policy.yaml
34. review_hard_negative_rules.yaml
35. review_replay_state_machine.yaml
36. review_trace_requirements.yaml
37. p10_upgrade_candidate_data_request_packet_contract.yaml
38. p09_to_p10_handoff_contract.yaml
39. p09_acceptance_criteria.md
40. p09_storage_constitution.md
41. p09_test_matrix.yaml
42. p09_report_model.yaml
43. p09_review_checklist.md
44. her_p09_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p09_review_replay/
  input_manifest/
  review_cases/
  replay_snapshots/
  decision_chain/
  runtime_path/
  paper_results/
  entry_reviews/
  exit_reviews/
  invalidation_reviews/
  failure_attribution/
  success_attribution/
  misclassification_reviews/
  gate_error_reviews/
  runtime_simulation_quality/
  data_gap_impact/
  trace_integrity/
  handoff_integrity/
  acceptance_integrity/
  calibration_candidates/
  missed_negative_rules/
  new_test_case_candidates/
  review_case_library/
  p10_data_requests/
  manual_checks/
  quality/
  gaps/
  rejected_reviews/
  blocked_reviews/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p09_review_replay_controller.yaml：定义 P09 身份、职责、权限、上下游、状态码、禁止事项。
- p09_review_replay_context.md：写成 HER 执行前必须读取的 P09 上下文。
- p09_input_contract.yaml：定义 P09 必须读取的 Paper Runtime、P08、P07、P06、P05、P04、P03、P02、P01、Trace、Acceptance、Handoff。
- p09_output_contract.yaml：定义 review case、replay、decision chain、runtime path、attribution、calibration、P10 request、handoff 输出。
- review_case_schema.yaml：定义复盘案例主记录。
- replay_input_snapshot_schema.yaml：定义历史快照锁定规则。
- decision_chain_reconstruction_schema.yaml：定义 P01-P08 决策链重建。
- runtime_path_reconstruction_schema.yaml：定义 Paper Runtime 路径重建。
- paper_result_schema.yaml：定义纸面结果。
- entry_decision_review_schema.yaml：定义入场决策复盘。
- exit_decision_review_schema.yaml：定义退出决策复盘。
- invalidation_trigger_review_schema.yaml：定义失效条件触发复盘。
- failure_attribution_schema.yaml：定义失败归因。
- success_attribution_schema.yaml：定义成功归因。
- misclassification_review_schema.yaml：定义误判复盘。
- gate_error_review_schema.yaml：定义 P07 / P08 门控错误复盘。
- runtime_simulation_quality_schema.yaml：定义纸面仿真质量。
- data_gap_impact_schema.yaml：定义数据缺口影响。
- trace_integrity_review_schema.yaml：定义 trace 完整性复盘。
- handoff_integrity_review_schema.yaml：定义 handoff 完整性复盘。
- acceptance_integrity_review_schema.yaml：定义 acceptance 完整性复盘。
- calibration_candidate_schema.yaml：定义校准候选。
- missed_negative_rule_schema.yaml：定义遗漏硬否定候选。
- new_test_case_candidate_schema.yaml：定义新增测试样例候选。
- review_case_library_schema.yaml：定义复盘案例库索引。
- review_type_policy.yaml：定义复盘类型。
- replay_snapshot_policy.yaml：定义历史快照锁定与禁止事后污染。
- failure_attribution_policy.yaml：定义失败归因规则。
- success_attribution_policy.yaml：定义成功归因规则。
- misclassification_review_policy.yaml：定义误判分析规则。
- runtime_simulation_quality_policy.yaml：定义纸面仿真质量规则。
- calibration_candidate_policy.yaml：定义校准候选生成规则。
- review_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- review_hard_negative_rules.yaml：定义无复盘对象、无 trace、用当前数据覆盖历史、直接改规则、单样本升级全局规则、自动实盘等阻断。
- review_replay_state_machine.yaml：定义 P09 全状态机。
- review_trace_requirements.yaml：定义 review trace、replay trace、decision chain trace、runtime trace、attribution trace、handoff trace。
- p10_upgrade_candidate_data_request_packet_contract.yaml：定义 P09 给 P10 的升级候选数据请求包。
- p09_to_p10_handoff_contract.yaml：定义 P09_TO_P10 handoff packet。
- p09_acceptance_criteria.md：定义 P09_READY、P09_READY_WITH_GAPS、P09_REJECTED、P09_BLOCKED。
- p09_storage_constitution.md：定义系统文件与运行数据目录。
- p09_test_matrix.yaml：定义至少 16 个测试场景。
- p09_report_model.yaml：定义 P09 人类可读报告。
- p09_review_checklist.md：定义审计清单。
- her_p09_execution_protocol.md：定义 HER 执行 P09 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P09_READY / P09_READY_WITH_GAPS / P09_REJECTED / P09_BLOCKED 判断
4. review_case 摘要
5. replay_input_snapshot 摘要
6. decision_chain_reconstruction 摘要
7. runtime_path_reconstruction 摘要
8. paper_result 摘要
9. failure_attribution 摘要
10. success_attribution 摘要
11. misclassification_review 摘要
12. gate_error_review 摘要
13. runtime_simulation_quality 摘要
14. data_gap_impact 摘要
15. calibration_candidate 摘要
16. missed_negative_rule 摘要
17. new_test_case_candidate 摘要
18. p10_upgrade_candidate_data_request_packet 摘要
19. p09_to_p10_handoff_packet 摘要
20. P09 阻断规则摘要
21. P09 测试矩阵摘要
22. 当前缺口清单
23. 是否达到轻量机构级 P09 v3.0

最终验收标准：
只有当 P09 具备 review case、replay input snapshot、decision chain reconstruction、runtime path reconstruction、paper result、entry review、exit review、invalidation review、failure attribution、success attribution、misclassification review、gate error review、runtime simulation quality、data gap impact、trace integrity、handoff integrity、acceptance integrity、calibration candidate、missed negative rule、new test case candidate、review case library、P10 data request、P09 handoff contract、gap policy、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P09 不能直接修改规则、不能修改 runtime、不能触发 paper runtime、不能允许 live execution 时，才允许标记为 P09_READY。
```

---

# 36. 当前是否达到专业化标准

## 判断

这一版 P09 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是纸面日报脚本
不是失败总结模块
```

P09 被明确升级为：

```text
复盘案例主数据层
历史快照回放层
决策链重建层
运行路径重建层
失败 / 成功归因层
误判与门控错误分析层
纸面仿真质量评估层
校准候选生成层
P10 升级交接层
```

---

# 37. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Review Case Record|已补齐|
|Replay Input Snapshot|已补齐|
|Decision Chain Reconstruction|已补齐|
|Runtime Path Reconstruction|已补齐|
|Paper Result Record|已补齐|
|Entry Decision Review|已补齐|
|Exit Decision Review|已补齐|
|Invalidation Trigger Review|已补齐|
|Failure Attribution|已补齐|
|Success Attribution|已补齐|
|Misclassification Review|已补齐|
|Gate Error Review|已补齐|
|Runtime Simulation Quality|已补齐|
|Data Gap Impact|已补齐|
|Trace Integrity Review|已补齐|
|Handoff Integrity Review|已补齐|
|Acceptance Integrity Review|已补齐|
|Calibration Candidate|已补齐|
|Missed Negative Rule|已补齐|
|New Test Case Candidate|已补齐|
|Review Case Library|已补齐|
|P10 Upgrade Data Request|已补齐|
|P09 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 38. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|P09 只能提出升级候选|已明确边界|P10 审核与升级|
|归因置信度需要样本积累|已定义 confidence|Review Case Library 长期校准|
|Paper Runtime 成本 / 滑点可能缺失|已定义 simulation quality|P10 升级模型|
|误阻断样本需要外部后续行情|已定义 false negative review|需要后续市场数据回放|
|单样本不能直接变规则|已阻断|P10 做多样本确认|
|P09 handoff 未联调|需要 P10|下一阶段展开 P10|
|工具实现未完成|当前为系统设计|Runner / Tool Binding 阶段|

---

# 本次认知升级点

1. **P09 的本质不是纸面日报，而是复盘回放与归因控制器。**
    
2. **复盘必须锁定当时快照。**  
    不能用现在的数据回头污染当时决策。
    
3. **失败必须分阶段归因。**  
    数据、钱包、筹码、证据、场景、策略、执行、runtime 都要分别审计。
    
4. **成功也必须归因。**  
    成功不一定证明系统正确，可能是纸面模型乐观或市场随机有利。
    
5. **P09 不能直接升级规则。**  
    它只能生成 calibration candidate / missed negative rule / test case candidate。
    
6. **Trace / Handoff / Acceptance 本身也要被复盘。**  
    系统不可复盘，本身就是系统失败。
    
7. **Paper Runtime 仿真质量是 P09 关键职责。**  
    滑点、费用、流动性、可卖性缺失，会让纸面收益失真。
    
8. **P09 只能交接给 P10。**  
    任何直接改策略、改 runtime、触发新交易或实盘路径都必须阻断。