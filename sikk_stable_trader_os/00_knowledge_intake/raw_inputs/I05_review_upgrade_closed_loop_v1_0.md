# I05 Review / Upgrade Closed Loop 专业版 v1.0

## P09 复盘回放、P10 受控升级、闭环验收、系统成熟度判定与下一轮运行任务包

---

## 0. I05 的核心定位

I05 不是新的业务阶段，也不是 P15。

它属于：

```text
Integration Program：系统集成落地计划
```

I05 的专业定义：

```text
I05 Review / Upgrade Closed Loop 是在 I04 Paper-only Runtime Integration 完成后，
用真实 paper runtime 输出反向验证 P09 Review Replay Controller 与 P10 Self Upgrade Controller 是否能够形成完整闭环的集成验收任务包。
```

一句话：

> **I04 负责产生可回放的纸面运行账本。**  
> **I05 负责验证这套账本能否被 P09 复盘、归因、生成升级候选，再被 P10 审查、打包、测试、回滚、交接。**

---

# 1. I05 不负责什么

I05 必须避免越权：

```text
I05 不新增 P11 / P12 / P13 / P14 / P15
I05 不修改 P01-P10 业务逻辑
I05 不直接修改策略规则
I05 不直接修改 schema / contract / policy
I05 不直接部署 P10 升级包
I05 不真实下单
I05 不钱包签名
I05 不启动 live execution
I05 不把单个复盘样本直接变成生产规则
I05 不绕过 P10 受控升级
I05 不删除 legacy 数据
I05 不自动发布升级
```

I05 只做：

```text
闭环回放
闭环验证
复盘能力验收
归因能力验收
升级候选验收
P10 升级包验收
回归测试计划验收
回滚计划验收
系统成熟度评分
缺口归档
下一轮运行建议
```

---

# 2. I05 阶段目标

I05 必须一次性解决 22 类问题：

|编号|问题|I05 必须输出|
|---|---|---|
|1|I04 输出是否可被 P09 读取？|`i04_runtime_output_ingestion_record`|
|2|P09 能否重建 P01-P08 决策链？|`p09_decision_chain_replay_validation_record`|
|3|P09 能否重建 Paper Runtime 路径？|`p09_runtime_path_replay_validation_record`|
|4|P09 能否生成失败归因？|`failure_attribution_validation_record`|
|5|P09 能否生成成功归因？|`success_attribution_validation_record`|
|6|P09 能否识别误判 / 门控错误？|`misclassification_gate_review_validation_record`|
|7|P09 能否发现数据缺口影响？|`data_gap_impact_validation_record`|
|8|P09 能否生成校准候选？|`calibration_candidate_validation_record`|
|9|P09 能否生成遗漏硬否定候选？|`missed_negative_rule_validation_record`|
|10|P09 能否生成 P10 数据请求包？|`p10_data_request_validation_record`|
|11|P10 能否读取 P09 升级候选？|`p10_upgrade_input_ingestion_record`|
|12|P10 能否审查升级候选？|`upgrade_candidate_review_validation_record`|
|13|P10 能否评估样本支持与过拟合？|`sample_support_overfit_validation_record`|
|14|P10 能否生成受控升级包？|`controlled_upgrade_package_validation_record`|
|15|P10 能否生成回归测试计划？|`regression_plan_validation_record`|
|16|P10 能否生成发布 / 回滚计划？|`release_rollback_validation_record`|
|17|P10 是否阻断自动部署和实盘路径？|`upgrade_safety_boundary_validation_record`|
|18|P01-P10 + I01-I04 trace 是否闭合？|`closed_loop_trace_integrity_record`|
|19|Handoff 是否完整闭合？|`closed_loop_handoff_integrity_record`|
|20|Acceptance 是否完整闭合？|`closed_loop_acceptance_integrity_record`|
|21|系统是否进入可持续 paper 运行？|`paper_operation_readiness_record`|
|22|是否完成集成闭环验收？|`i05_closed_loop_acceptance_result`|

---

# 3. I05 的底层方法论

## 3.1 闭环不是“跑通一次”

普通系统说闭环，只是：

```text
有输入
有输出
有报告
```

专业系统的闭环必须证明：

```text
输入有来源
判断有证据
执行有许可
纸面有账本
结果可回放
失败可归因
升级可审查
变更可测试
发布可回滚
```

I05 的任务就是验证这条链是否成立。

---

## 3.2 I05 的核心不是收益，而是系统学习能力

I05 不判断：

```text
这次 paper 盈利多少
这次是不是抓到好币
这个策略是不是无敌
```

I05 判断：

```text
系统能不能从 paper 结果中学习？
系统能不能知道自己哪里错？
系统能不能把错误转成升级候选？
系统能不能防止错误升级污染系统？
系统能不能持续 paper-only 验证？
```

---

## 3.3 P09/P10 必须分权

I05 要强审计：

```text
P09 只能提出复盘结论和升级候选
P10 只能审查候选并生成受控升级包
实现层才可以根据审批执行变更
```

不能出现：

```text
P09 直接改规则
P10 直接部署
P10 绕过回归测试
单样本直接全局升级
```

---

## 3.4 闭环输出必须服务下一轮运行

I05 最终不是生成漂亮报告，而是决定：

```text
是否可以进入持续 paper-only runtime
哪些缺口必须先修
哪些升级候选进入 backlog
哪些 runner / schema / contract / policy 需要实现补丁
哪些测试要加入回归矩阵
下一轮 paper 验证应该如何运行
```

---

# 4. I05 输入范围

```yaml
i05_required_inputs:
  from_i04:
    - i04_to_i05_handoff_packet
    - p09_review_replay_input_packet
    - paper_runtime_input_manifest
    - p08_permission_ingestion_records
    - runtime_permission_gate_records
    - paper_candidate_queue_records
    - paper_position_open_records
    - paper_trade_records
    - paper_position_update_records
    - paper_mark_to_market_records
    - runtime_invalidation_monitor_records
    - paper_exit_rule_evaluation_records
    - paper_exit_event_records
    - paper_position_close_records
    - paper_equity_curve_records
    - paper_runtime_risk_event_records
    - paper_runtime_snapshot_records
    - i04_paper_runtime_integration_report
    - i04_acceptance_result

  from_p09:
    - p09_review_replay_controller
    - p09_input_contract
    - p09_output_contract
    - p09_acceptance_criteria
    - p09_test_matrix
    - p09_to_p10_handoff_contract
    - p10_upgrade_candidate_data_request_packet_contract

  from_p10:
    - p10_self_upgrade_controller
    - p10_input_contract
    - p10_output_contract
    - p10_acceptance_criteria
    - p10_test_matrix
    - controlled_upgrade_package_schema
    - controlled_upgrade_task_packet_schema
    - p10_to_implementation_handoff_contract

  from_i03:
    - trace_writer_binding
    - acceptance_runner_binding
    - handoff_writer_binding
    - schema_validator_binding
    - contract_validator_binding
    - path_guard_binding
    - runner_error_policy

  from_i02:
    - runtime_data_path_index
    - schema_index
    - contract_index
    - handoff_contract_index
    - read_order_manifest
    - write_permission_matrix
    - canonical_path_policy

  from_control_planes:
    - governance_handoff_packet
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - forbidden_use_policy
    - global_hard_negative_rules
    - global_status_code_table
```

I05 启动前必须确认：

```text
I04 已验收
I04→I05 handoff 已生成
P09 review replay input packet 已生成
P09 / P10 的 controller、contract、schema、acceptance 可读取
Trace / Acceptance / Handoff writer 可用
live execution 全局关闭
wallet signing 全局关闭
auto deploy 全局关闭
```

---

# 5. I05 必须建立的核心对象

|对象|作用|
|---|---|
|`I05 Closed Loop Input Manifest`|记录 I05 接收的 I04 / P09 / P10 输入|
|`I04 Runtime Output Ingestion Record`|验证 I04 输出是否可被 P09 读取|
|`Review Case Selection Record`|选择哪些 paper case 进入 P09|
|`P09 Replay Execution Record`|记录 P09 是否成功运行|
|`P09 Decision Chain Replay Validation Record`|验证 P09 决策链重建|
|`P09 Runtime Path Replay Validation Record`|验证 P09 runtime 路径重建|
|`Attribution Validation Record`|验证 failure / success attribution|
|`Calibration Candidate Validation Record`|验证校准候选生成|
|`P09 to P10 Data Request Validation Record`|验证 P09 → P10 数据请求|
|`P10 Upgrade Input Ingestion Record`|验证 P10 接收升级候选|
|`Upgrade Candidate Review Validation Record`|验证 P10 审查升级候选|
|`Sample Support Overfit Validation Record`|验证样本支持与过拟合控制|
|`Controlled Upgrade Package Validation Record`|验证受控升级包|
|`Regression Plan Validation Record`|验证回归测试计划|
|`Release Rollback Validation Record`|验证发布与回滚计划|
|`Upgrade Safety Boundary Validation Record`|验证 P10 没有越权|
|`Closed Loop Trace Integrity Record`|验证 trace 全链闭合|
|`Closed Loop Handoff Integrity Record`|验证 handoff 全链闭合|
|`Closed Loop Acceptance Integrity Record`|验证 acceptance 全链闭合|
|`Closed Loop Defect Record`|闭环缺陷记录|
|`System Maturity Scorecard`|系统成熟度评分|
|`Paper Operation Readiness Record`|是否可进入持续 paper 运行|
|`Next Iteration Task Packet`|下一轮修复 / 运行任务包|
|`I05 Closed Loop Acceptance Result`|I05 验收结果|
|`I05 Final Integration Report`|最终集成闭环报告|

---

# 6. I05 运行目录设计

## 6.1 系统目录

```text
/root/sikk-gmgn/system/integration_program/I05_review_upgrade_closed_loop/
```

必须创建：

```text
i05_review_upgrade_closed_loop_controller.yaml
i05_review_upgrade_closed_loop_context.md
i05_input_contract.yaml
i05_output_contract.yaml
i05_closed_loop_input_manifest_schema.yaml
i04_runtime_output_ingestion_schema.yaml
review_case_selection_schema.yaml
p09_replay_execution_schema.yaml
p09_decision_chain_replay_validation_schema.yaml
p09_runtime_path_replay_validation_schema.yaml
attribution_validation_schema.yaml
calibration_candidate_validation_schema.yaml
p09_to_p10_data_request_validation_schema.yaml
p10_upgrade_input_ingestion_schema.yaml
upgrade_candidate_review_validation_schema.yaml
sample_support_overfit_validation_schema.yaml
controlled_upgrade_package_validation_schema.yaml
regression_plan_validation_schema.yaml
release_rollback_validation_schema.yaml
upgrade_safety_boundary_validation_schema.yaml
closed_loop_trace_integrity_schema.yaml
closed_loop_handoff_integrity_schema.yaml
closed_loop_acceptance_integrity_schema.yaml
closed_loop_defect_schema.yaml
system_maturity_scorecard_schema.yaml
paper_operation_readiness_schema.yaml
next_iteration_task_packet_contract.yaml
i05_closed_loop_acceptance_result_schema.yaml
i05_final_integration_report_schema.yaml
i05_closed_loop_policy.yaml
i05_hard_negative_rules.yaml
i05_state_machine.yaml
i05_trace_requirements.yaml
i05_acceptance_criteria.md
i05_storage_constitution.md
i05_test_matrix.yaml
i05_report_model.yaml
i05_review_checklist.md
her_i05_execution_protocol.md
```

---

## 6.2 运行数据目录

```text
/root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop/
  input_manifest/
  i04_runtime_ingestion/
  review_case_selection/
  p09_replay_execution/
  decision_chain_validation/
  runtime_path_validation/
  attribution_validation/
  calibration_validation/
  p09_to_p10_validation/
  p10_upgrade_ingestion/
  upgrade_candidate_review_validation/
  sample_support_overfit_validation/
  controlled_upgrade_package_validation/
  regression_plan_validation/
  release_rollback_validation/
  upgrade_safety_boundary/
  trace_integrity/
  handoff_integrity/
  acceptance_integrity/
  closed_loop_defects/
  maturity_scorecard/
  paper_operation_readiness/
  next_iteration_tasks/
  final_reports/
  audit/
  trace/
  acceptance/
```

---

# 7. I05 Closed Loop Input Manifest

```yaml
i05_closed_loop_input_manifest:
  manifest_id: string
  generated_at: datetime

  upstream_packets:
    i04_to_i05_handoff_packet_id: string
    p09_review_replay_input_packet_id: string
    i04_acceptance_result_id: string
    trace_handoff_packet_id: string | null

  i04_runtime_inputs:
    paper_positions_open_path: string
    paper_positions_closed_path: string
    paper_trades_path: string
    paper_equity_curve_path: string
    paper_runtime_events_path: string
    paper_exit_events_path: string
    paper_risk_events_path: string
    paper_runtime_snapshots_path: string
    paper_runtime_trace_path: string

  p09_assets:
    p09_controller_path: string
    p09_input_contract_path: string
    p09_output_contract_path: string
    p09_acceptance_criteria_path: string
    p09_test_matrix_path: string

  p10_assets:
    p10_controller_path: string
    p10_input_contract_path: string
    p10_output_contract_path: string
    p10_acceptance_criteria_path: string
    p10_test_matrix_path: string

  quality:
    i04_outputs_readable: boolean
    p09_assets_readable: boolean
    p10_assets_readable: boolean
    trace_writer_available: boolean
    acceptance_runner_available: boolean
    handoff_writer_available: boolean
    closed_loop_input_quality:
      - HIGH_CONFIDENCE
      - USABLE
      - USABLE_WITH_GAPS
      - LOW_CONFIDENCE
      - UNUSABLE

  restrictions:
    review_only: true
    no_runtime_mutation: true
    no_direct_rule_mutation: true
    no_auto_deploy: true
    no_live_execution: true
    no_wallet_signing: true
```

---

# 8. I04 Runtime Output Ingestion Record

```yaml
i04_runtime_output_ingestion_record:
  ingestion_id: string
  generated_at: datetime

  required_outputs_checked:
    paper_positions_open_available: boolean
    paper_positions_closed_available: boolean
    paper_trades_available: boolean
    equity_curve_available: boolean
    runtime_events_available: boolean
    exit_events_available: boolean
    risk_events_available: boolean
    runtime_snapshots_available: boolean
    p09_review_input_packet_available: boolean
    runtime_trace_available: boolean

  p09_readiness:
    has_reviewable_cases: boolean
    has_closed_positions: boolean
    has_open_positions_for_update_review: boolean
    has_risk_events_for_review: boolean
    has_decision_context_links: boolean
    has_cost_slippage_records: boolean
    has_invalidation_monitor_records: boolean

  ingestion_status:
    - I04_OUTPUTS_READY_FOR_P09
    - I04_OUTPUTS_READY_WITH_GAPS
    - I04_OUTPUTS_NOT_REVIEWABLE
    - I04_OUTPUTS_UNUSABLE

  gaps:
    - gap_id: string
      missing_output: string
      severity:
        - BLOCKING
        - HIGH
        - MEDIUM
        - LOW
      effect_on_p09_cn: string
```

---

# 9. Review Case Selection Record

```yaml
review_case_selection_record:
  selection_id: string
  generated_at: datetime

  selection_scope:
    review_period_start: datetime | null
    review_period_end: datetime | null
    include_closed_positions: boolean
    include_open_positions: boolean
    include_risk_events: boolean
    include_blocked_runtime_attempts: boolean

  selected_cases:
    - review_case_candidate_id: string
      candidate_id: string
      token_address: string
      paper_position_id: string | null
      case_type:
        - CLOSED_POSITION_REVIEW
        - OPEN_POSITION_REVIEW
        - RISK_EVENT_REVIEW
        - INVALIDATION_REVIEW
        - FAILED_RUNTIME_ATTEMPT_REVIEW
      priority:
        - HIGH
        - MEDIUM
        - LOW
      selection_reason_cn: string

  selection_quality:
    selected_case_count: integer
    has_win_cases: boolean
    has_loss_cases: boolean
    has_risk_cases: boolean
    has_invalidation_cases: boolean
    case_selection_status:
      - REVIEW_CASES_SELECTED
      - REVIEW_CASES_SELECTED_WITH_GAPS
      - NO_REVIEWABLE_CASES
```

---

# 10. P09 Replay Execution Record

```yaml
p09_replay_execution_record:
  p09_execution_id: string
  generated_at: datetime

  execution_mode:
    - REPLAY_DRY_RUN
    - REVIEW_REPLAY_ON_I04_OUTPUTS
    - LEGACY_COMPARISON_REPLAY

  inputs:
    p09_review_replay_input_packet_id: string
    selected_review_case_ids: list
    runtime_outputs_path: string
    upstream_decision_context_path: string

  execution_checks:
    p09_input_contract_valid: boolean
    review_case_records_created: boolean
    replay_input_snapshots_created: boolean
    decision_chain_reconstruction_created: boolean
    runtime_path_reconstruction_created: boolean
    paper_result_records_created: boolean
    attribution_records_created: boolean
    calibration_candidates_created: boolean
    p10_data_request_created: boolean

  execution_status:
    - P09_REPLAY_SUCCESS
    - P09_REPLAY_SUCCESS_WITH_GAPS
    - P09_REPLAY_FAILED
    - P09_REPLAY_BLOCKED

  failure_reasons:
    - reason_id: string
      reason_cn: string
      source_gap: string | null
```

---

# 11. P09 Decision Chain Replay Validation Record

```yaml
p09_decision_chain_replay_validation_record:
  validation_id: string
  generated_at: datetime

  chain_checks:
    p01_candidate_trace_reconstructed: boolean
    p02_fact_trace_reconstructed: boolean
    p03_wallet_trace_reconstructed: boolean
    p04_chip_trace_reconstructed: boolean
    p05_evidence_trace_reconstructed: boolean
    p06_scenario_trace_reconstructed: boolean
    p07_strategy_gate_trace_reconstructed: boolean
    p08_execution_risk_trace_reconstructed: boolean
    paper_runtime_trace_reconstructed: boolean

  reconstruction_quality:
    missing_stage_traces: list
    broken_links: list
    replay_conflicts: list
    decision_chain_quality:
      - CHAIN_FULLY_RECONSTRUCTED
      - CHAIN_RECONSTRUCTED_WITH_GAPS
      - CHAIN_PARTIAL
      - CHAIN_BROKEN
      - CHAIN_UNREPLAYABLE

  effect_on_closed_loop:
    p09_can_review_decision_quality: boolean
    p10_can_trust_upgrade_candidate: boolean
```

---

# 12. P09 Runtime Path Replay Validation Record

```yaml
p09_runtime_path_replay_validation_record:
  validation_id: string
  generated_at: datetime

  runtime_path_checks:
    entry_event_reconstructed: boolean
    entry_price_model_reconstructed: boolean
    slippage_application_reconstructed: boolean
    cost_application_reconstructed: boolean
    position_updates_reconstructed: boolean
    invalidation_monitor_reconstructed: boolean
    exit_rule_reconstructed: boolean
    exit_event_reconstructed: boolean
    close_record_reconstructed: boolean
    equity_curve_reconstructed: boolean
    risk_events_reconstructed: boolean

  runtime_path_quality:
    - RUNTIME_PATH_FULLY_RECONSTRUCTED
    - RUNTIME_PATH_RECONSTRUCTED_WITH_GAPS
    - RUNTIME_PATH_PARTIAL
    - RUNTIME_PATH_BROKEN
    - RUNTIME_PATH_UNREPLAYABLE

  missing_runtime_components:
    - component_name: string
      effect_on_attribution_cn: string
      severity:
        - BLOCKING
        - HIGH
        - MEDIUM
        - LOW
```

---

# 13. Attribution Validation Record

```yaml
attribution_validation_record:
  validation_id: string
  generated_at: datetime

  failure_attribution_checks:
    failure_attribution_records_created: boolean
    primary_failure_stage_identified: boolean
    contributing_failure_stages_identified: boolean
    failure_mechanism_identified: boolean
    source_trace_attached: boolean
    attribution_confidence_declared: boolean

  success_attribution_checks:
    success_attribution_records_created: boolean
    primary_success_stage_identified: boolean
    success_mechanism_identified: boolean
    randomness_or_model_distortion_checked: boolean
    source_trace_attached: boolean

  validation_status:
    - ATTRIBUTION_VALID
    - ATTRIBUTION_VALID_WITH_GAPS
    - ATTRIBUTION_LOW_CONFIDENCE
    - ATTRIBUTION_UNUSABLE

  p10_effect:
    can_generate_upgrade_candidates: boolean
    can_create_regression_samples: boolean
    needs_manual_review: boolean
```

---

# 14. Calibration Candidate Validation Record

```yaml
calibration_candidate_validation_record:
  validation_id: string
  generated_at: datetime

  calibration_outputs:
    calibration_candidate_count: integer
    missed_negative_rule_candidate_count: integer
    new_test_case_candidate_count: integer
    data_gap_upgrade_candidate_count: integer
    runtime_model_upgrade_candidate_count: integer

  quality_checks:
    every_candidate_has_source_review_case: boolean
    every_candidate_has_evidence_basis: boolean
    every_candidate_has_risk_of_change: boolean
    every_candidate_has_p10_action: boolean
    no_candidate_directly_changes_rule: boolean

  validation_status:
    - CALIBRATION_CANDIDATES_VALID
    - CALIBRATION_CANDIDATES_VALID_WITH_GAPS
    - CALIBRATION_CANDIDATES_LOW_CONFIDENCE
    - CALIBRATION_CANDIDATES_UNUSABLE
```

---

# 15. P09 to P10 Data Request Validation Record

```yaml
p09_to_p10_data_request_validation_record:
  validation_id: string
  generated_at: datetime

  packet_checks:
    p10_upgrade_candidate_data_request_packet_exists: boolean
    p09_to_p10_handoff_packet_exists: boolean
    failure_attribution_path_included: boolean
    calibration_candidate_path_included: boolean
    missed_negative_rule_path_included: boolean
    new_test_case_candidate_path_included: boolean
    review_case_library_path_included: boolean
    restrictions_preserved: boolean

  restrictions_check:
    p09_proposes_only: boolean
    no_direct_rule_mutation: boolean
    no_runtime_mutation: boolean
    no_live_execution: boolean

  validation_status:
    - P09_TO_P10_HANDOFF_VALID
    - P09_TO_P10_HANDOFF_VALID_WITH_GAPS
    - P09_TO_P10_HANDOFF_BROKEN
```

---

# 16. P10 Upgrade Input Ingestion Record

```yaml
p10_upgrade_input_ingestion_record:
  ingestion_id: string
  generated_at: datetime

  p10_input_checks:
    p09_to_p10_handoff_read: boolean
    upgrade_candidate_data_request_read: boolean
    failure_attribution_records_read: boolean
    calibration_candidates_read: boolean
    missed_negative_rules_read: boolean
    new_test_cases_read: boolean
    review_case_library_read: boolean

  input_quality:
    candidate_count_received: integer
    high_priority_candidate_count: integer
    low_confidence_candidate_count: integer
    input_quality_status:
      - P10_INPUT_READY
      - P10_INPUT_READY_WITH_GAPS
      - P10_INPUT_LOW_CONFIDENCE
      - P10_INPUT_UNUSABLE
```

---

# 17. Upgrade Candidate Review Validation Record

```yaml
upgrade_candidate_review_validation_record:
  validation_id: string
  generated_at: datetime

  p10_review_checks:
    upgrade_candidate_reviews_created: boolean
    sample_support_assessments_created: boolean
    upgrade_classifications_created: boolean
    impact_assessments_created: boolean
    compatibility_assessments_created: boolean
    overfit_assessments_created: boolean
    upgrade_decisions_created: boolean

  review_quality:
    no_single_case_global_rule: boolean
    low_confidence_candidates_rejected_or_deferred: boolean
    safety_critical_candidates_marked_for_approval: boolean
    unsupported_candidates_not_approved: boolean

  validation_status:
    - UPGRADE_REVIEW_VALID
    - UPGRADE_REVIEW_VALID_WITH_GAPS
    - UPGRADE_REVIEW_LOW_CONFIDENCE
    - UPGRADE_REVIEW_UNUSABLE
```

---

# 18. Sample Support / Overfit Validation Record

```yaml
sample_support_overfit_validation_record:
  validation_id: string
  generated_at: datetime

  support_checks:
    sample_support_record_created: boolean
    case_count_recorded: boolean
    contradictory_cases_checked: boolean
    affected_scenario_families_recorded: boolean
    affected_strategy_profiles_recorded: boolean

  overfit_checks:
    single_case_detected: boolean
    outlier_case_detected: boolean
    false_positive_risk_checked: boolean
    false_negative_risk_checked: boolean
    overfit_mitigation_declared: boolean

  validation_result:
    - OVERFIT_CONTROL_VALID
    - OVERFIT_CONTROL_VALID_WITH_GAPS
    - OVERFIT_RISK_HIGH_REQUIRES_MANUAL_REVIEW
    - OVERFIT_CONTROL_FAILED
```

---

# 19. Controlled Upgrade Package Validation Record

```yaml
controlled_upgrade_package_validation_record:
  validation_id: string
  generated_at: datetime

  package_checks:
    controlled_upgrade_package_created: boolean
    included_proposals_declared: boolean
    target_stages_declared: boolean
    required_validation_declared: boolean
    package_status_declared: boolean
    no_auto_deploy: boolean
    no_live_execution: boolean
    no_wallet_signing: boolean

  proposal_checks:
    schema_contract_proposals_valid: boolean
    rule_policy_proposals_valid: boolean
    parameter_calibration_proposals_valid: boolean
    test_matrix_upgrades_valid: boolean
    runtime_model_upgrades_valid: boolean
    report_explanation_upgrades_valid: boolean

  validation_status:
    - CONTROLLED_PACKAGE_VALID
    - CONTROLLED_PACKAGE_VALID_WITH_GAPS
    - CONTROLLED_PACKAGE_INCOMPLETE
    - CONTROLLED_PACKAGE_BLOCKED
```

---

# 20. Regression Plan Validation Record

```yaml
regression_plan_validation_record:
  validation_id: string
  generated_at: datetime

  regression_checks:
    regression_test_plan_created: boolean
    schema_tests_declared: boolean
    contract_tests_declared: boolean
    policy_tests_declared: boolean
    state_machine_tests_declared: boolean
    handoff_tests_declared: boolean
    trace_tests_declared: boolean
    replay_tests_declared: boolean
    integration_tests_declared: boolean
    paper_runtime_tests_declared: boolean

  pass_criteria_checks:
    no_handoff_breakage_required: boolean
    no_trace_breakage_required: boolean
    no_live_execution_path_required: boolean
    rollback_on_failure_declared: boolean

  validation_status:
    - REGRESSION_PLAN_VALID
    - REGRESSION_PLAN_VALID_WITH_GAPS
    - REGRESSION_PLAN_INCOMPLETE
    - REGRESSION_PLAN_UNUSABLE
```

---

# 21. Release / Rollback Validation Record

```yaml
release_rollback_validation_record:
  validation_id: string
  generated_at: datetime

  release_checks:
    release_plan_created: boolean
    release_mode_declared: boolean
    dry_run_or_shadow_mode_declared: boolean
    paper_only_release_declared: boolean
    manual_approval_required_if_needed: boolean

  rollback_checks:
    rollback_plan_created: boolean
    previous_version_reference_declared: boolean
    rollback_steps_declared: boolean
    rollback_trigger_conditions_declared: boolean

  safety:
    auto_deploy_allowed: false
    live_execution_allowed: false
    wallet_signing_allowed: false

  validation_status:
    - RELEASE_ROLLBACK_VALID
    - RELEASE_ROLLBACK_VALID_WITH_GAPS
    - RELEASE_ROLLBACK_INCOMPLETE
    - RELEASE_ROLLBACK_BLOCKED
```

---

# 22. Upgrade Safety Boundary Validation Record

```yaml
upgrade_safety_boundary_validation_record:
  validation_id: string
  generated_at: datetime

  safety_checks:
    p10_does_not_directly_mutate_rules: boolean
    p10_does_not_auto_deploy: boolean
    p10_does_not_enable_live_execution: boolean
    p10_does_not_enable_wallet_signing: boolean
    p10_requires_regression_before_release: boolean
    p10_requires_rollback_before_release: boolean
    p10_requires_approval_for_high_impact_change: boolean

  violation_records:
    - violation_id: string
      violation_type:
        - DIRECT_RULE_MUTATION
        - AUTO_DEPLOY
        - LIVE_EXECUTION_PATH
        - WALLET_SIGNING_PATH
        - REGRESSION_BYPASS
        - ROLLBACK_BYPASS
        - APPROVAL_BYPASS
      severity:
        - BLOCKING
        - CRITICAL
        - HIGH

  safety_status:
    - UPGRADE_BOUNDARY_SAFE
    - UPGRADE_BOUNDARY_SAFE_WITH_GAPS
    - UPGRADE_BOUNDARY_VIOLATED
    - UPGRADE_BOUNDARY_BLOCKED
```

---

# 23. Closed Loop Trace / Handoff / Acceptance Integrity

```yaml
closed_loop_trace_integrity_record:
  record_id: string
  generated_at: datetime

  trace_chain:
    p01_trace_available: boolean
    p02_trace_available: boolean
    p03_trace_available: boolean
    p04_trace_available: boolean
    p05_trace_available: boolean
    p06_trace_available: boolean
    p07_trace_available: boolean
    p08_trace_available: boolean
    paper_runtime_trace_available: boolean
    p09_review_trace_available: boolean
    p10_upgrade_trace_available: boolean

  integrity_status:
    - TRACE_CHAIN_COMPLETE
    - TRACE_CHAIN_COMPLETE_WITH_GAPS
    - TRACE_CHAIN_BROKEN
    - TRACE_CHAIN_UNUSABLE
```

```yaml
closed_loop_handoff_integrity_record:
  record_id: string
  generated_at: datetime

  handoff_chain:
    p01_to_p02_valid: boolean
    p02_to_p03_valid: boolean
    p03_to_p04_valid: boolean
    p04_to_p05_valid: boolean
    p05_to_p06_valid: boolean
    p06_to_p07_valid: boolean
    p07_to_p08_valid: boolean
    p08_to_paper_runtime_valid: boolean
    i04_to_i05_valid: boolean
    p09_to_p10_valid: boolean
    p10_to_implementation_valid: boolean

  integrity_status:
    - HANDOFF_CHAIN_COMPLETE
    - HANDOFF_CHAIN_COMPLETE_WITH_GAPS
    - HANDOFF_CHAIN_BROKEN
    - HANDOFF_CHAIN_UNUSABLE
```

```yaml
closed_loop_acceptance_integrity_record:
  record_id: string
  generated_at: datetime

  acceptance_chain:
    p01_acceptance_valid: boolean
    p02_acceptance_valid: boolean
    p03_acceptance_valid: boolean
    p04_acceptance_valid: boolean
    p05_acceptance_valid: boolean
    p06_acceptance_valid: boolean
    p07_acceptance_valid: boolean
    p08_acceptance_valid: boolean
    i04_acceptance_valid: boolean
    p09_acceptance_valid: boolean
    p10_acceptance_valid: boolean

  blocked_items_not_used_downstream: boolean
  ready_with_gaps_limitations_preserved: boolean

  integrity_status:
    - ACCEPTANCE_CHAIN_COMPLETE
    - ACCEPTANCE_CHAIN_COMPLETE_WITH_GAPS
    - ACCEPTANCE_CHAIN_BROKEN
    - ACCEPTANCE_CHAIN_UNUSABLE
```

---

# 24. Closed Loop Defect Record

```yaml
closed_loop_defect_record:
  defect_id: string
  generated_at: datetime

  defect_scope:
    affected_layer:
      - P01_TO_P10_PHASE_CONTROLLER
      - I01_I05_INTEGRATION_PROGRAM
      - PAPER_RUNTIME
      - P09_REVIEW_REPLAY
      - P10_SELF_UPGRADE
      - TRACE_HANDOFF_ACCEPTANCE
      - RUNNER_TOOL_BINDING
      - DIRECTORY_CONTRACT_INDEX

  defect_type:
    - MISSING_RUNTIME_OUTPUT
    - UNREPLAYABLE_DECISION_CHAIN
    - UNREPLAYABLE_RUNTIME_PATH
    - ATTRIBUTION_LOW_CONFIDENCE
    - P09_TO_P10_HANDOFF_BROKEN
    - P10_UPGRADE_PACKAGE_INCOMPLETE
    - REGRESSION_PLAN_MISSING
    - ROLLBACK_PLAN_MISSING
    - TRACE_CHAIN_BROKEN
    - ACCEPTANCE_CHAIN_BROKEN
    - LIVE_EXECUTION_BOUNDARY_RISK
    - PATH_GUARD_FAILURE

  severity:
    - BLOCKING
    - CRITICAL
    - HIGH
    - MEDIUM
    - LOW

  fix_target:
    - FIX_IN_P01_P10
    - FIX_IN_I01
    - FIX_IN_I02
    - FIX_IN_I03
    - FIX_IN_I04
    - FIX_IN_P09
    - FIX_IN_P10
    - FIX_IN_RUNNER
    - FIX_IN_TEST_MATRIX

  recommended_fix_cn: string
  blocks_continuous_paper_operation: boolean
```

---

# 25. System Maturity Scorecard

```yaml
system_maturity_scorecard:
  scorecard_id: string
  generated_at: datetime

  dimensions:
    phase_chain_integrity:
      score_0_to_100: number
      status:
        - STRONG
        - USABLE
        - WEAK
        - BLOCKED

    runtime_replayability:
      score_0_to_100: number
      status: string

    attribution_quality:
      score_0_to_100: number
      status: string

    upgrade_governance_quality:
      score_0_to_100: number
      status: string

    trace_handoff_acceptance_integrity:
      score_0_to_100: number
      status: string

    paper_runtime_realism:
      score_0_to_100: number
      status: string

    safety_boundary_strength:
      score_0_to_100: number
      status: string

  overall_maturity_level:
    - DESIGN_ONLY
    - INTEGRATION_READY_WITH_GAPS
    - PAPER_RUNTIME_READY
    - CLOSED_LOOP_READY
    - LIGHT_INSTITUTIONAL_PAPER_READY
    - BLOCKED

  maturity_summary_cn: string
```

---

# 26. Paper Operation Readiness Record

```yaml
paper_operation_readiness_record:
  readiness_id: string
  generated_at: datetime

  readiness_checks:
    p01_to_p08_pipeline_reachable: boolean
    p08_to_paper_runtime_reachable: boolean
    paper_runtime_outputs_reviewable: boolean
    p09_replay_successful: boolean
    p10_upgrade_review_successful: boolean
    trace_chain_usable: boolean
    handoff_chain_usable: boolean
    acceptance_chain_usable: boolean
    no_live_execution_path: boolean
    no_wallet_signing_path: boolean
    no_auto_deploy_path: boolean

  readiness_status:
    - CONTINUOUS_PAPER_OPERATION_ALLOWED
    - CONTINUOUS_PAPER_OPERATION_ALLOWED_WITH_GAPS
    - PAPER_OPERATION_REQUIRES_FIXES
    - PAPER_OPERATION_BLOCKED

  allowed_next_mode:
    - DRY_RUN_ONLY
    - SINGLE_CYCLE_PAPER_RUN
    - SCHEDULED_PAPER_RUN
    - PAPER_WITH_MANUAL_REVIEW
    - BLOCKED

  required_before_scheduled_operation:
    - item_id: string
      item_cn: string
      priority:
        - BLOCKING
        - HIGH
        - MEDIUM
        - LOW
```

---

# 27. Next Iteration Task Packet

```yaml
next_iteration_task_packet:
  packet_id: string
  generated_at: datetime

  next_iteration_scope:
    target:
      - FIX_BLOCKING_DEFECTS
      - STABILIZE_PAPER_RUNTIME
      - IMPROVE_P09_ATTRIBUTION
      - IMPROVE_P10_UPGRADE_PACKAGE
      - ADD_REGRESSION_TESTS
      - START_SCHEDULED_PAPER_RUN

  task_groups:
    blocking_fixes:
      - task_id: string
        source_defect_id: string
        target_layer: string
        instruction_cn: string
        acceptance_check_cn: string

    high_priority_fixes:
      - task_id: string
        source_defect_id: string
        target_layer: string
        instruction_cn: string

    test_matrix_updates:
      - test_case_candidate_id: string
        target_test_matrix: string
        instruction_cn: string

    runtime_improvements:
      - improvement_id: string
        target_runtime_component: string
        instruction_cn: string

    p10_backlog_items:
      - upgrade_candidate_id: string
        target_stage: string
        required_p10_action: string

  restrictions:
    no_auto_deploy: true
    no_live_execution: true
    no_wallet_signing: true
    all_changes_must_pass_regression: true
```

---

# 28. I05 Closed Loop Acceptance Result

```yaml
i05_closed_loop_acceptance_result:
  acceptance_id: string
  generated_at: datetime

  final_status:
    - I05_READY
    - I05_READY_WITH_GAPS
    - I05_REJECTED
    - I05_BLOCKED

  required_checks:
    i04_outputs_ingested: boolean
    review_cases_selected: boolean
    p09_replay_executed: boolean
    p09_decision_chain_validated: boolean
    p09_runtime_path_validated: boolean
    attribution_validated: boolean
    calibration_candidates_validated: boolean
    p09_to_p10_handoff_validated: boolean
    p10_input_ingested: boolean
    p10_upgrade_review_validated: boolean
    controlled_upgrade_package_validated: boolean
    regression_plan_validated: boolean
    release_rollback_validated: boolean
    safety_boundary_validated: boolean
    trace_integrity_validated: boolean
    handoff_integrity_validated: boolean
    acceptance_integrity_validated: boolean
    paper_operation_readiness_created: boolean

  blocking_reasons:
    - reason_id: string
      reason_cn: string

  permission_after_i05:
    - ENTER_CONTINUOUS_PAPER_OPERATION
    - ENTER_SINGLE_CYCLE_PAPER_RUN
    - RETURN_TO_I04_FIX
    - RETURN_TO_P09_FIX
    - RETURN_TO_P10_FIX
    - RETURN_TO_I03_FIX
    - BLOCKED
```

---

# 29. I05 Gap Policy

```yaml
i05_gap_policy:
  BLOCKING_GAP:
    result: I05_BLOCKED
    examples:
      - i04_handoff_missing
      - p09_review_input_missing
      - p09_cannot_replay_runtime
      - p10_cannot_read_p09_candidates
      - live_execution_path_detected
      - p10_auto_deploy_detected
      - trace_chain_unusable

  CRITICAL_GAP:
    result: I05_REJECTED_OR_FIX_REQUIRED
    examples:
      - runtime_path_unreplayable
      - decision_chain_unreplayable
      - attribution_records_missing
      - p09_to_p10_handoff_missing
      - controlled_upgrade_package_missing
      - regression_plan_missing
      - rollback_plan_missing

  HIGH_GAP:
    result: I05_READY_WITH_GAPS
    examples:
      - attribution_confidence_low
      - sample_support_insufficient
      - slippage_model_default_used
      - cost_model_default_used
      - partial_runtime_snapshot

  MEDIUM_GAP:
    result: I05_READY_WITH_GAPS
    examples:
      - optional_report_missing
      - review_case_library_partial
      - noncritical_test_case_missing

  LOW_GAP:
    result: I05_READY_WITH_NOTE
    examples:
      - optional_metadata_missing
      - formatting_gap
      - noncritical_description_missing
```

---

# 30. I05 Hard Negative Rules

```yaml
i05_hard_negative_rules:
  - rule_id: I05_BLOCK_001
    name: 未读取 I04 handoff
    condition: i04_to_i05_handoff_packet_missing == true
    result: I05_BLOCKED
    reason: I05 必须基于 I04 runtime 输出执行

  - rule_id: I05_BLOCK_002
    name: P09 review input 缺失
    condition: p09_review_replay_input_packet_missing == true
    result: I05_BLOCKED
    reason: 无 P09 输入包无法闭环回放

  - rule_id: I05_BLOCK_003
    name: P09 无法重建 runtime path
    condition: p09_runtime_path_unreplayable == true
    result: I05_BLOCKED
    reason: Paper Runtime 输出不可复盘

  - rule_id: I05_BLOCK_004
    name: P09 无法生成 P10 数据请求
    condition: p10_upgrade_candidate_data_request_missing == true
    result: I05_BLOCKED
    reason: 复盘无法进入升级闭环

  - rule_id: I05_BLOCK_005
    name: P10 绕过候选审查
    condition: p10_skips_upgrade_candidate_review == true
    result: I05_BLOCKED
    reason: P10 必须先审查 P09 升级候选

  - rule_id: I05_BLOCK_006
    name: 单样本直接全局升级
    condition: single_case_promoted_to_global_rule == true
    result: I05_BLOCKED
    reason: 单样本不能直接改变全局规则

  - rule_id: I05_BLOCK_007
    name: 缺少回归测试计划
    condition: controlled_upgrade_package_created == true and regression_plan_missing == true
    result: I05_BLOCKED
    reason: 无回归测试不得进入实现

  - rule_id: I05_BLOCK_008
    name: 缺少回滚计划
    condition: release_plan_created == true and rollback_plan_missing == true
    result: I05_BLOCKED
    reason: 无回滚计划不得发布

  - rule_id: I05_BLOCK_009
    name: 自动部署路径
    condition: auto_deploy_detected == true
    result: I05_BLOCKED
    reason: 当前系统禁止自动部署

  - rule_id: I05_BLOCK_010
    name: live execution 路径
    condition: live_execution_detected == true
    result: I05_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 31. I05 状态机

```yaml
i05_review_upgrade_closed_loop_state_machine:
  states:
    - I05_UNINITIALIZED
    - I05_CONTEXT_LOADED
    - I05_I04_HANDOFF_READ
    - I05_INPUT_MANIFEST_BUILT
    - I05_I04_OUTPUTS_INGESTED
    - I05_REVIEW_CASES_SELECTED
    - I05_P09_REPLAY_EXECUTED
    - I05_P09_DECISION_CHAIN_VALIDATED
    - I05_P09_RUNTIME_PATH_VALIDATED
    - I05_ATTRIBUTION_VALIDATED
    - I05_CALIBRATION_CANDIDATES_VALIDATED
    - I05_P09_TO_P10_DATA_REQUEST_VALIDATED
    - I05_P10_INPUT_INGESTED
    - I05_UPGRADE_CANDIDATE_REVIEW_VALIDATED
    - I05_SAMPLE_SUPPORT_OVERFIT_VALIDATED
    - I05_CONTROLLED_UPGRADE_PACKAGE_VALIDATED
    - I05_REGRESSION_PLAN_VALIDATED
    - I05_RELEASE_ROLLBACK_VALIDATED
    - I05_UPGRADE_SAFETY_BOUNDARY_VALIDATED
    - I05_TRACE_INTEGRITY_VALIDATED
    - I05_HANDOFF_INTEGRITY_VALIDATED
    - I05_ACCEPTANCE_INTEGRITY_VALIDATED
    - I05_DEFECTS_BUILT
    - I05_MATURITY_SCORECARD_BUILT
    - I05_PAPER_OPERATION_READINESS_BUILT
    - I05_NEXT_ITERATION_TASK_PACKET_BUILT
    - I05_FINAL_REPORT_BUILT
    - I05_READY_FOR_ACCEPTANCE
    - I05_ACCEPTANCE_READY
    - I05_CLOSED_LOOP_READY
    - I05_READY_WITH_GAPS
    - I05_REJECTED
    - I05_BLOCKED

  critical_transitions:
    - from: I05_CONTEXT_LOADED
      to: I05_I04_HANDOFF_READ
      condition: i04_to_i05_handoff_packet_available == true

    - from: I05_I04_HANDOFF_READ
      to: I05_INPUT_MANIFEST_BUILT
      condition: p09_review_replay_input_packet_available == true

    - from: I05_INPUT_MANIFEST_BUILT
      to: I05_I04_OUTPUTS_INGESTED
      condition: i04_runtime_output_ingestion_record_created == true

    - from: I05_I04_OUTPUTS_INGESTED
      to: I05_REVIEW_CASES_SELECTED
      condition: review_case_selection_record_created == true

    - from: I05_REVIEW_CASES_SELECTED
      to: I05_P09_REPLAY_EXECUTED
      condition: p09_replay_execution_record_created == true

    - from: I05_P09_REPLAY_EXECUTED
      to: I05_P09_DECISION_CHAIN_VALIDATED
      condition: p09_decision_chain_replay_validation_created == true

    - from: I05_P09_DECISION_CHAIN_VALIDATED
      to: I05_P09_RUNTIME_PATH_VALIDATED
      condition: p09_runtime_path_replay_validation_created == true

    - from: I05_P09_RUNTIME_PATH_VALIDATED
      to: I05_ATTRIBUTION_VALIDATED
      condition: attribution_validation_record_created == true

    - from: I05_ATTRIBUTION_VALIDATED
      to: I05_P09_TO_P10_DATA_REQUEST_VALIDATED
      condition: p09_to_p10_data_request_validation_created == true

    - from: I05_P09_TO_P10_DATA_REQUEST_VALIDATED
      to: I05_P10_INPUT_INGESTED
      condition: p10_upgrade_input_ingestion_record_created == true

    - from: I05_P10_INPUT_INGESTED
      to: I05_UPGRADE_CANDIDATE_REVIEW_VALIDATED
      condition: upgrade_candidate_review_validation_created == true

    - from: I05_UPGRADE_CANDIDATE_REVIEW_VALIDATED
      to: I05_CONTROLLED_UPGRADE_PACKAGE_VALIDATED
      condition: controlled_upgrade_package_validation_created == true

    - from: I05_CONTROLLED_UPGRADE_PACKAGE_VALIDATED
      to: I05_REGRESSION_PLAN_VALIDATED
      condition: regression_plan_validation_created == true

    - from: I05_REGRESSION_PLAN_VALIDATED
      to: I05_RELEASE_ROLLBACK_VALIDATED
      condition: release_rollback_validation_created == true

    - from: I05_RELEASE_ROLLBACK_VALIDATED
      to: I05_UPGRADE_SAFETY_BOUNDARY_VALIDATED
      condition: upgrade_safety_boundary_validation_created == true

    - from: I05_UPGRADE_SAFETY_BOUNDARY_VALIDATED
      to: I05_MATURITY_SCORECARD_BUILT
      condition: system_maturity_scorecard_created == true

    - from: I05_MATURITY_SCORECARD_BUILT
      to: I05_PAPER_OPERATION_READINESS_BUILT
      condition: paper_operation_readiness_record_created == true

    - from: I05_PAPER_OPERATION_READINESS_BUILT
      to: I05_NEXT_ITERATION_TASK_PACKET_BUILT
      condition: next_iteration_task_packet_created == true

    - from: I05_NEXT_ITERATION_TASK_PACKET_BUILT
      to: I05_FINAL_REPORT_BUILT
      condition: final_integration_report_created == true

    - from: I05_FINAL_REPORT_BUILT
      to: I05_READY_FOR_ACCEPTANCE
      condition: i05_closed_loop_acceptance_result_created == true
```

---

# 32. I05 Acceptance Criteria

```yaml
i05_acceptance_criteria:
  I05_READY:
    required:
      - i04_handoff_read
      - p09_review_input_read
      - i04_runtime_outputs_ingested
      - review_cases_selected
      - p09_replay_executed
      - p09_decision_chain_validated
      - p09_runtime_path_validated
      - attribution_validated
      - calibration_candidates_validated
      - p09_to_p10_handoff_validated
      - p10_input_ingested
      - p10_upgrade_candidate_review_validated
      - sample_support_overfit_validated
      - controlled_upgrade_package_validated
      - regression_plan_validated
      - release_rollback_validated
      - upgrade_safety_boundary_validated
      - trace_integrity_validated
      - handoff_integrity_validated
      - acceptance_integrity_validated
      - maturity_scorecard_created
      - paper_operation_readiness_created
      - next_iteration_task_packet_created
      - no_live_execution_path
      - no_wallet_signing_path
      - no_auto_deploy_path

  I05_READY_WITH_GAPS:
    allowed_when:
      - attribution_confidence_low_but_trace_present
      - sample_support_insufficient_but_p10_deferred
      - cost_slippage_default_used_but_recorded
      - partial_review_case_library
    required:
      - gaps_recorded
      - safety_boundary_intact
      - p09_to_p10_chain_usable
      - no_blocking_gap

  I05_REJECTED:
    triggered_by:
      - p09_replay_failed
      - p10_upgrade_review_failed
      - controlled_upgrade_package_unusable
      - regression_plan_unusable
      - release_rollback_unusable

  I05_BLOCKED:
    triggered_by:
      - missing_i04_handoff
      - missing_p09_review_input
      - runtime_path_unreplayable
      - trace_chain_unusable
      - p10_auto_deploy_detected
      - live_execution_detected
      - wallet_signing_detected
```

---

# 33. I05 测试矩阵

```yaml
i05_test_matrix:
  - test_id: I05_TEST_001
    name: I04 输出完整，P09/P10 闭环成功
    expected_status: I05_READY

  - test_id: I05_TEST_002
    name: 缺 I04 handoff
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_003
    name: 缺 P09 review input packet
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_004
    name: I04 有 paper trades 但无 runtime trace
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_005
    name: P09 无法重建 P08 permission
    expected_status: I05_REJECTED

  - test_id: I05_TEST_006
    name: P09 能复盘但 attribution confidence 低
    expected_status: I05_READY_WITH_GAPS

  - test_id: I05_TEST_007
    name: P09 未生成 P10 upgrade data request
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_008
    name: P10 无法读取 P09 handoff
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_009
    name: P10 将单样本直接升级为全局规则
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_010
    name: P10 生成升级包但缺 regression plan
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_011
    name: P10 生成 release plan 但缺 rollback plan
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_012
    name: P10 只批准 test-only 升级
    expected_status: I05_READY

  - test_id: I05_TEST_013
    name: P09 生成 missed negative rule，P10 标记 manual review
    expected_status: I05_READY

  - test_id: I05_TEST_014
    name: trace chain 部分缺失但可定位缺口
    expected_status: I05_READY_WITH_GAPS

  - test_id: I05_TEST_015
    name: handoff chain 断裂
    expected_status: I05_BLOCKED_OR_REJECTED

  - test_id: I05_TEST_016
    name: acceptance chain 中 BLOCKED item 被下游使用
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_017
    name: live execution path detected
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_018
    name: wallet signing path detected
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_019
    name: auto deploy detected
    expected_status: I05_BLOCKED

  - test_id: I05_TEST_020
    name: 全链路通过但样本数量不足以持续运行
    expected_status: I05_READY_WITH_GAPS
    expected_next_mode: SINGLE_CYCLE_PAPER_RUN
```

---

# 34. I05 报告模型

```yaml
i05_final_integration_report:
  report_id: string
  generated_at: datetime
  controller_id: I05_REVIEW_UPGRADE_CLOSED_LOOP

  summary:
    closed_loop_status: string
    review_cases_selected: integer
    p09_replay_success_count: integer
    p09_replay_failed_count: integer
    p10_upgrade_candidates_received: integer
    p10_candidates_approved_for_package: integer
    p10_candidates_deferred: integer
    p10_candidates_rejected: integer
    blocking_defect_count: integer
    high_defect_count: integer
    medium_defect_count: integer
    low_defect_count: integer

  p09_validation_summary:
    decision_chain_replay_status: string
    runtime_path_replay_status: string
    attribution_validation_status: string
    calibration_candidate_status: string
    p09_to_p10_handoff_status: string

  p10_validation_summary:
    upgrade_input_status: string
    candidate_review_status: string
    sample_support_overfit_status: string
    controlled_package_status: string
    regression_plan_status: string
    release_rollback_status: string
    safety_boundary_status: string

  closed_loop_integrity_summary:
    trace_integrity_status: string
    handoff_integrity_status: string
    acceptance_integrity_status: string

  maturity_summary:
    overall_maturity_level: string
    phase_chain_integrity_score: number
    runtime_replayability_score: number
    attribution_quality_score: number
    upgrade_governance_score: number
    safety_boundary_score: number

  paper_operation_readiness:
    readiness_status: string
    allowed_next_mode: string
    required_before_scheduled_operation: list

  next_iteration:
    next_iteration_task_packet_path: string
    blocking_fixes: list
    high_priority_fixes: list
    p10_backlog_items: list

  compliance:
    live_execution_path_detected: false
    wallet_signing_path_detected: false
    auto_deploy_path_detected: false
    direct_rule_mutation_detected: false
    single_case_global_upgrade_detected: false
```

---

# 35. HER I05 执行协议

```text
HER 执行 I05 时必须按以下顺序：

1. 读取 system_methodology_blueprint.md
2. 读取 professional_build_order.md
3. 读取 I04→I05 handoff packet
4. 读取 P09 review replay input packet
5. 读取 I04 paper runtime outputs
6. 读取 P09 controller / input contract / output contract / acceptance / test matrix
7. 读取 P10 controller / input contract / output contract / acceptance / test matrix
8. 读取 I03 trace / acceptance / handoff writer binding
9. 读取 I02 schema / contract / handoff / runtime path indexes
10. 建立 i05_closed_loop_input_manifest
11. 建立 i04_runtime_output_ingestion_record
12. 建立 review_case_selection_record
13. 执行 P09 replay validation
14. 验证 P09 decision chain reconstruction
15. 验证 P09 runtime path reconstruction
16. 验证 failure / success attribution
17. 验证 calibration candidate / missed negative rule / test case candidate
18. 验证 P09→P10 data request packet
19. 执行 P10 upgrade input ingestion
20. 验证 P10 upgrade candidate review
21. 验证 sample support / overfit assessment
22. 验证 controlled upgrade package
23. 验证 regression test plan
24. 验证 release / rollback plan
25. 验证 upgrade safety boundary
26. 验证 closed loop trace integrity
27. 验证 closed loop handoff integrity
28. 验证 closed loop acceptance integrity
29. 生成 closed_loop_defect_records
30. 生成 system_maturity_scorecard
31. 生成 paper_operation_readiness_record
32. 生成 next_iteration_task_packet
33. 生成 i05_final_integration_report
34. 生成 i05_closed_loop_acceptance_result
35. 只允许进入下一轮 paper-only 修复 / 运行 / 受控升级，不允许 live execution
```

禁止：

```text
1. 不允许无 I04 handoff 启动 I05
2. 不允许无 P09 review input 启动闭环
3. 不允许跳过 P09 直接进入 P10
4. 不允许 P09 直接修改规则
5. 不允许 P10 自动部署
6. 不允许单样本直接变全局规则
7. 不允许缺 regression plan 的升级进入实现
8. 不允许缺 rollback plan 的发布进入实现
9. 不允许 live execution
10. 不允许 wallet signing
11. 不允许 auto order
12. 不允许删除 legacy 数据
```

---

# 36. 给 HER 的正式任务书

```text
任务名称：I05 Review / Upgrade Closed Loop：复盘升级闭环验证任务包

目标：
在 /root/sikk-gmgn/system/integration_program/I05_review_upgrade_closed_loop/ 下建立 I05 Review / Upgrade Closed Loop 任务包，并在 /root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop/ 下生成闭环验证输出。I05 不是 P15，不新增业务判断能力，不修改 P01-P10 业务逻辑。它的目标是在 I04 Paper-only Runtime Integration 完成后，用 I04 生成的 paper runtime outputs 和 P09 review replay input packet，验证 P09 是否能重建 P01-P08 决策链、Paper Runtime 路径、失败/成功归因、误判复盘、校准候选与 P10 数据请求；再验证 P10 是否能读取 P09 升级候选，完成候选审查、样本支持、过拟合控制、影响分析、受控升级包、回归测试计划、发布回滚计划和实现交接包。

核心原则：
1. I05 是 Integration Program 第五步，不是新业务阶段。
2. I05 只做闭环验证、成熟度判断、缺口归档和下一轮任务包。
3. I05 不修改 P01-P10 业务逻辑。
4. I05 不直接修改策略规则。
5. I05 不直接部署升级包。
6. I05 不允许 live execution。
7. I05 不允许 wallet signing。
8. I05 不允许 auto order。
9. I05 必须读取 I04→I05 handoff。
10. I05 必须读取 P09 review replay input packet。
11. I05 必须验证 P09 决策链重建能力。
12. I05 必须验证 P09 runtime path 重建能力。
13. I05 必须验证 P09 failure / success attribution。
14. I05 必须验证 P09 calibration candidate / missed negative rule / new test case candidate。
15. I05 必须验证 P09→P10 handoff。
16. I05 必须验证 P10 upgrade candidate review。
17. I05 必须验证 P10 sample support / overfit control。
18. I05 必须验证 P10 controlled upgrade package。
19. I05 必须验证 regression test plan。
20. I05 必须验证 release / rollback plan。
21. I05 必须验证 trace / handoff / acceptance 全链完整性。
22. I05 必须生成 system maturity scorecard。
23. I05 必须生成 paper operation readiness。
24. I05 必须生成 next iteration task packet。
25. I05 必须生成 i05_closed_loop_acceptance_result。

需要创建系统目录：
/root/sikk-gmgn/system/integration_program/I05_review_upgrade_closed_loop/

需要创建系统文件：
1. i05_review_upgrade_closed_loop_controller.yaml
2. i05_review_upgrade_closed_loop_context.md
3. i05_input_contract.yaml
4. i05_output_contract.yaml
5. i05_closed_loop_input_manifest_schema.yaml
6. i04_runtime_output_ingestion_schema.yaml
7. review_case_selection_schema.yaml
8. p09_replay_execution_schema.yaml
9. p09_decision_chain_replay_validation_schema.yaml
10. p09_runtime_path_replay_validation_schema.yaml
11. attribution_validation_schema.yaml
12. calibration_candidate_validation_schema.yaml
13. p09_to_p10_data_request_validation_schema.yaml
14. p10_upgrade_input_ingestion_schema.yaml
15. upgrade_candidate_review_validation_schema.yaml
16. sample_support_overfit_validation_schema.yaml
17. controlled_upgrade_package_validation_schema.yaml
18. regression_plan_validation_schema.yaml
19. release_rollback_validation_schema.yaml
20. upgrade_safety_boundary_validation_schema.yaml
21. closed_loop_trace_integrity_schema.yaml
22. closed_loop_handoff_integrity_schema.yaml
23. closed_loop_acceptance_integrity_schema.yaml
24. closed_loop_defect_schema.yaml
25. system_maturity_scorecard_schema.yaml
26. paper_operation_readiness_schema.yaml
27. next_iteration_task_packet_contract.yaml
28. i05_closed_loop_acceptance_result_schema.yaml
29. i05_final_integration_report_schema.yaml
30. i05_closed_loop_policy.yaml
31. i05_hard_negative_rules.yaml
32. i05_state_machine.yaml
33. i05_trace_requirements.yaml
34. i05_acceptance_criteria.md
35. i05_storage_constitution.md
36. i05_test_matrix.yaml
37. i05_report_model.yaml
38. i05_review_checklist.md
39. her_i05_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop/
  input_manifest/
  i04_runtime_ingestion/
  review_case_selection/
  p09_replay_execution/
  decision_chain_validation/
  runtime_path_validation/
  attribution_validation/
  calibration_validation/
  p09_to_p10_validation/
  p10_upgrade_ingestion/
  upgrade_candidate_review_validation/
  sample_support_overfit_validation/
  controlled_upgrade_package_validation/
  regression_plan_validation/
  release_rollback_validation/
  upgrade_safety_boundary/
  trace_integrity/
  handoff_integrity/
  acceptance_integrity/
  closed_loop_defects/
  maturity_scorecard/
  paper_operation_readiness/
  next_iteration_tasks/
  final_reports/
  audit/
  trace/
  acceptance/

运行输出要求：
1. i05_closed_loop_input_manifest.yaml
2. i04_runtime_output_ingestion_record.yaml
3. review_case_selection_record.yaml
4. p09_replay_execution_record.yaml
5. p09_decision_chain_replay_validation_record.yaml
6. p09_runtime_path_replay_validation_record.yaml
7. attribution_validation_record.yaml
8. calibration_candidate_validation_record.yaml
9. p09_to_p10_data_request_validation_record.yaml
10. p10_upgrade_input_ingestion_record.yaml
11. upgrade_candidate_review_validation_record.yaml
12. sample_support_overfit_validation_record.yaml
13. controlled_upgrade_package_validation_record.yaml
14. regression_plan_validation_record.yaml
15. release_rollback_validation_record.yaml
16. upgrade_safety_boundary_validation_record.yaml
17. closed_loop_trace_integrity_record.yaml
18. closed_loop_handoff_integrity_record.yaml
19. closed_loop_acceptance_integrity_record.yaml
20. closed_loop_defect_records.yaml
21. system_maturity_scorecard.yaml
22. paper_operation_readiness_record.yaml
23. next_iteration_task_packet.yaml
24. i05_final_integration_report.md
25. i05_closed_loop_acceptance_result.yaml

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. I04 runtime output ingestion 摘要
4. review case selection 摘要
5. P09 replay execution 摘要
6. P09 decision chain replay validation 摘要
7. P09 runtime path replay validation 摘要
8. attribution validation 摘要
9. calibration candidate validation 摘要
10. P09→P10 validation 摘要
11. P10 input ingestion 摘要
12. upgrade candidate review validation 摘要
13. sample support / overfit validation 摘要
14. controlled upgrade package validation 摘要
15. regression plan validation 摘要
16. release / rollback validation 摘要
17. upgrade safety boundary validation 摘要
18. trace / handoff / acceptance integrity 摘要
19. closed loop defect 摘要
20. system maturity scorecard 摘要
21. paper operation readiness 摘要
22. next iteration task packet 摘要
23. 是否允许进入持续 paper-only operation
24. 是否达到轻量机构级 I05 v1.0

最终验收标准：
只有当 I05 具备 closed loop input manifest、I04 runtime ingestion、review case selection、P09 replay execution、decision chain replay validation、runtime path replay validation、attribution validation、calibration candidate validation、P09→P10 data request validation、P10 input ingestion、upgrade candidate review validation、sample support / overfit validation、controlled upgrade package validation、regression plan validation、release / rollback validation、upgrade safety boundary validation、trace integrity、handoff integrity、acceptance integrity、closed loop defect records、system maturity scorecard、paper operation readiness、next iteration task packet、final integration report、closed loop acceptance result，并且没有 live execution、没有 wallet signing、没有 auto deploy、没有 single-case global upgrade、没有 trace chain unusable 时，才允许标记为 I05_READY。
```

---

# 37. 当前是否达到专业化 I05 设计标准

## 判断

这一版 I05 达到：

```text
专业化
轻量机构水准
一次性把 I05 应有闭环对象补全
不是最小版本
不是普通复盘报告
不是继续新增业务阶段
```

I05 被明确设计为：

```text
I04 runtime 输出摄取层
P09 replay 验证层
决策链重建验收层
runtime 路径重建验收层
失败 / 成功归因验收层
P09→P10 handoff 验收层
P10 升级候选审查验收层
受控升级包验收层
回归测试 / 回滚计划验收层
Trace / Handoff / Acceptance 全链闭合层
系统成熟度评分层
持续 paper operation 就绪判断层
下一轮任务包生成层
```

---

# 38. I05 完成后的正确下一步

I05 完成后，不应该继续新增 I06。

下一步应该根据 I05 的验收结果分流：

## 情况 A：I05_READY

进入：

```text
Continuous Paper-only Operation：持续纸面验证运行
```

重点是：

```text
定时运行
多轮样本积累
P09 日复盘
P10 周期性升级候选审查
失败样本归因
回归测试扩展
```

---

## 情况 B：I05_READY_WITH_GAPS

进入：

```text
Targeted Fix Sprint：定向缺口修复
```

优先修：

```text
blocking / high defects
P09 replay confidence
P10 package completeness
slippage / cost model realism
trace / handoff gaps
```

---

## 情况 C：I05_REJECTED / BLOCKED

回退到对应层修复：

```text
I04 runtime 输出不可复盘 → 回 I04
P09 不能复盘 → 回 P09
P10 不能打包升级 → 回 P10
trace / handoff / acceptance 断裂 → 回 I01-I03
目录 / 合约路径问题 → 回 I02
runner / writer 绑定问题 → 回 I03
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|I05 是否已有真实 paper 样本|I05 定义验证标准|需要 I04 生成样本|
|P09 是否能真正复盘|I05 验证|不通过则修 P09 / trace|
|P10 是否能生成升级包|I05 验证|不通过则修 P10|
|是否能进入定时 paper 运行|由 `paper_operation_readiness_record` 判断|READY 后再进入|
|是否可以实盘|仍然不允许|当前阶段只到 paper-only|
|是否能自动部署升级|不允许|必须 P10 + governance + regression + rollback|
|样本数量是否足够调参|多数初期不足|先积累多轮 paper 样本|
|是否需要 dashboard / Telegram|I05 不处理|可在 paper 稳定后接 Ops 层|

---

# 本次认知升级点

1. **I05 的本质不是复盘报告，而是系统闭环验收层。**
    
2. **I05 验证的是“系统是否具备学习能力”。**  
    不是看单次 paper 盈亏，而是看能不能复盘、归因、生成升级候选、受控升级。
    
3. **P09 和 P10 必须严格分权。**  
    P09 提出问题，P10 审查升级，不能让复盘直接污染生产规则。
    
4. **闭环验收必须同时检查 trace、handoff、acceptance。**  
    没有这些，系统无法审计，也无法复盘。
    
5. **I05_READY 才意味着系统可以进入持续 paper-only operation。**
    
6. **I05 完成后不应该继续新增阶段。**  
    应该进入“持续纸面运行 + 定向修复 + P09/P10 周期性闭环”。
    
7. **当前体系仍然不能实盘。**  
    实盘需要另一个受控执行安全体系，不应混入当前 paper-only 闭环。