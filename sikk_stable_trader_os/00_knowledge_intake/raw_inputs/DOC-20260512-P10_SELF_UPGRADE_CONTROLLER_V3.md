# P10 Self Upgrade Controller 专业版 v3.0

## 自我升级审查、规则校准、合约演进、测试扩展、版本发布与回滚控制器

---

## 0. 先修正 P10 的定位

P10 不能被设计成：

```text
自动改规则模块
自动调参模块
自动部署模块
AI 自己修改系统模块
复盘建议执行器
```

P10 的专业定位应该是：

```text
把 P09 Review Replay Controller 交接过来的失败归因、成功归因、误判复盘、校准候选、遗漏硬否定、测试样例候选和仿真质量问题，转化为可审查、可测试、可版本化、可回滚、可发布的受控升级包。
```

一句话定义：

> **P09 负责提出升级候选。**  
> **P10 负责判断这些升级候选是否值得进入系统变更流程。**  
> **P10 不能直接无审查地修改生产规则。**  
> **P10 的最高权限是生成“受控升级包”和“实现任务包”，再交给 Governance / Runner / Tool Binding / 人工确认流程。**

P10 可以输出：

```text
升级候选审查
规则变更提案
字段合约升级提案
阈值校准提案
测试矩阵扩展
回归测试包
版本升级包
发布计划
回滚计划
实现任务包
```

P10 不能直接输出：

```text
自动修改线上规则
自动部署
自动实盘
绕过测试
绕过治理
绕过回滚
单样本直接全局生效
```

---

# 1. P10 阶段核心目标

P10 必须一次性解决 18 个问题：

|编号|核心问题|P10 必须输出|
|---|---|---|
|1|P09 提出的升级候选是否有效？|`upgrade_candidate_review_record`|
|2|是否由足够样本支持？|`sample_support_assessment_record`|
|3|升级影响哪些阶段、字段、规则、测试？|`upgrade_impact_assessment_record`|
|4|是规则升级、字段升级、阈值校准，还是测试升级？|`upgrade_classification_record`|
|5|是否允许进入变更提案？|`upgrade_decision_record`|
|6|需要改哪些 schema / contract / policy？|`contract_schema_upgrade_proposal_record`|
|7|需要改哪些 hard negative / gate policy？|`rule_policy_upgrade_proposal_record`|
|8|需要校准哪些阈值 / 权重？|`parameter_calibration_proposal_record`|
|9|需要补哪些测试样例？|`test_matrix_upgrade_record`|
|10|需要改哪些工具绑定或 runner？|`tool_binding_upgrade_proposal_record`|
|11|升级是否会破坏上游 / 下游交接？|`compatibility_assessment_record`|
|12|升级前需要哪些回归测试？|`regression_test_plan_record`|
|13|升级如何发布、灰度、回滚？|`release_and_rollback_plan_record`|
|14|是否需要人工批准？|`upgrade_approval_requirement_record`|
|15|是否生成实现任务包？|`controlled_upgrade_task_packet`|
|16|是否更新系统版本索引？|`version_change_record`|
|17|升级是否进入待实现队列？|`upgrade_backlog_record`|
|18|是否可交接给实现 / 工具绑定流程？|`p10_to_implementation_handoff_packet`|

---

# 2. P10 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|升级候选审查官|P09 提出的候选是否有效|`upgrade_candidate_review_record`|
|样本证据官|单样本、多样本、重复样本支持程度|`sample_support_assessment_record`|
|影响分析官|升级影响哪些阶段、字段、合约和流程|`upgrade_impact_assessment_record`|
|规则治理官|hard negative / policy 是否需要升级|`rule_policy_upgrade_proposal_record`|
|合约治理官|schema / handoff / acceptance 是否要变|`contract_schema_upgrade_proposal_record`|
|参数校准官|阈值、权重、评分是否要校准|`parameter_calibration_proposal_record`|
|测试治理官|是否补测试矩阵、回归测试、反例测试|`test_matrix_upgrade_record`|
|发布回滚官|控制版本、发布、灰度、回滚和验收|`release_and_rollback_plan_record`|

---

# 3. P10 底层方法论

## 3.1 自我升级不是自我修改

P10 的核心边界：

```text
P10 可以生成升级包。
P10 可以生成实现任务。
P10 可以生成测试计划。
P10 可以生成回滚计划。
P10 不能未经批准直接改生产规则。
```

专业系统必须防止：

```text
AI 看一条失败样本 → 自动改全局规则 → 过拟合 → 系统失真
```

---

## 3.2 单样本只能生成候选，不能生成全局规则

单个复盘案例只能输出：

```text
upgrade_candidate
test_case_candidate
manual_review_required
```

不能直接输出：

```text
global_rule_change_approved
production_threshold_changed
hard_negative_updated
```

除非：

```text
1. 属于安全类硬风险；
2. 有治理规则允许临时保护性阻断；
3. 已绑定回滚和人工复核。
```

---

## 3.3 升级必须分级

P10 不能把所有建议都当成同等级。

必须区分：

```text
字段合约升级
数据源升级
质量阈值升级
证据权重升级
场景规则升级
策略门控升级
执行风控升级
纸面仿真模型升级
测试矩阵升级
报告解释升级
治理规则升级
```

不同升级类型需要不同验收方式。

---

## 3.4 升级必须先测试后发布

任何升级都必须经过：

```text
候选审查
影响分析
兼容性检查
测试矩阵更新
回归测试
灰度 / dry-run
发布决策
回滚准备
```

否则不允许进入实际系统。

---

## 3.5 P10 要防止过拟合

P10 必须检查：

```text
这个升级是否只适合一个样本？
是否会误伤其他场景？
是否会让系统过于保守？
是否会让系统过于宽松？
是否会破坏 P01-P09 的边界？
是否会让弱证据被强使用？
是否会绕过 P08 / paper-only 限制？
```

---

# 4. P10 支持的升级类型

```yaml
p10_upgrade_types:
  FIELD_SCHEMA_UPGRADE:
    name_cn: 字段与 schema 升级
    examples:
      - 新增字段
      - 字段类型修正
      - 字段来源约束
      - 必填 / 可选级别调整

  CONTRACT_UPGRADE:
    name_cn: 输入输出合约升级
    examples:
      - handoff contract 更新
      - data request packet 更新
      - acceptance criteria 更新

  HARD_NEGATIVE_RULE_UPGRADE:
    name_cn: 硬否定规则升级
    examples:
      - 新增阻断条件
      - 强化 PAUSE 条件
      - 新增 live execution 防线

  POLICY_UPGRADE:
    name_cn: 策略政策升级
    examples:
      - 场景冲突处理
      - 证据使用权限
      - 策略 profile 适配规则

  PARAMETER_CALIBRATION:
    name_cn: 阈值与权重校准
    examples:
      - 市值追高阈值
      - 对手盘压力阈值
      - 滑点阈值
      - 证据权重

  TEST_MATRIX_UPGRADE:
    name_cn: 测试矩阵升级
    examples:
      - 新增失败样例
      - 新增反例样例
      - 新增边界条件测试

  TOOL_BINDING_UPGRADE:
    name_cn: 工具绑定升级
    examples:
      - GMGN 字段映射
      - OKX quote / security 映射
      - runner 参数统一

  RUNTIME_MODEL_UPGRADE:
    name_cn: 纸面运行模型升级
    examples:
      - 滑点模型
      - 成本模型
      - 退出模型
      - 持仓更新模型

  REPORT_EXPLANATION_UPGRADE:
    name_cn: 报告解释升级
    examples:
      - 决策理由字段
      - 反证解释
      - 失败归因报告

  GOVERNANCE_UPGRADE:
    name_cn: 治理规则升级
    examples:
      - 审批规则
      - 发布规则
      - 回滚规则
      - 禁止事项
```

---

# 5. P10 必须建立的核心对象

|对象|作用|
|---|---|
|`Upgrade Input Manifest`|记录 P10 接收了哪些 P09 升级候选|
|`Upgrade Candidate Review Record`|审查升级候选是否有效|
|`Sample Support Assessment Record`|判断样本支持程度|
|`Upgrade Classification Record`|升级类型分类|
|`Upgrade Impact Assessment Record`|影响范围分析|
|`Overfit Risk Assessment Record`|过拟合风险评估|
|`Compatibility Assessment Record`|兼容性评估|
|`Contract Schema Upgrade Proposal Record`|合约 / schema 升级提案|
|`Rule Policy Upgrade Proposal Record`|规则 / policy 升级提案|
|`Parameter Calibration Proposal Record`|参数 / 阈值校准提案|
|`Test Matrix Upgrade Record`|测试矩阵升级记录|
|`Tool Binding Upgrade Proposal Record`|工具绑定升级提案|
|`Runtime Model Upgrade Proposal Record`|纸面运行模型升级提案|
|`Report Explanation Upgrade Proposal Record`|报告解释升级提案|
|`Upgrade Decision Record`|是否允许进入升级包|
|`Regression Test Plan Record`|回归测试计划|
|`Release And Rollback Plan Record`|发布与回滚计划|
|`Upgrade Approval Requirement Record`|人工 / 治理审批要求|
|`Controlled Upgrade Package Record`|受控升级包|
|`Controlled Upgrade Task Packet`|给 HER / Runner 的实现任务包|
|`Version Change Record`|版本变更记录|
|`Upgrade Backlog Record`|升级待办队列|
|`P10 Final Upgrade Report`|P10 升级报告|
|`P10 to Implementation Handoff Packet`|P10 → 实现 / 工具绑定交接包|

---

# 6. P10 输入：必须读取什么

```yaml
p10_required_inputs:
  from_p09:
    - p09_to_p10_handoff_packet
    - p10_upgrade_candidate_data_request_packet
    - failure_attribution_records
    - success_attribution_records
    - misclassification_review_records
    - gate_error_review_records
    - runtime_simulation_quality_records
    - data_gap_impact_records
    - missed_negative_rule_records
    - calibration_candidate_records
    - new_test_case_candidate_records
    - review_case_library_records
    - trace_integrity_review_records
    - handoff_integrity_review_records
    - acceptance_integrity_review_records
    - p09_review_replay_report

  from_control_planes:
    - governance_handoff_packet
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - limitation_transfer_packet
    - forbidden_use_policy
    - professional_baseline_acceptance
    - release_policy_handoff
    - rollback_policy_handoff

  from_system_indices:
    - phase_controller_index.yaml
    - contract_index.md
    - schema_index.md
    - global_status_code_table.md
    - global_hard_negative_rules.md
    - professional_build_order.md
    - directory_constitution.md
    - system_methodology_blueprint.md

  from_existing_versions:
    - current_schema_versions
    - current_policy_versions
    - current_test_matrix_versions
    - current_runner_versions
    - current_tool_binding_versions

  required_contracts:
    - p10_input_contract
    - p10_output_contract
    - controlled_upgrade_package_contract
    - regression_test_plan_contract
    - implementation_handoff_contract
```

P10 启动前必须确认：

```text
P09 已验收
P09 handoff 已生成
P10 只读取 P09 交接的升级候选
P10 不允许直接修改生产规则
P10 不允许自动部署
P10 不允许触发 paper runtime
P10 不允许 live execution
```

---

# 7. Upgrade Input Manifest

```yaml
upgrade_input_manifest:
  manifest_id: string
  generated_at: datetime
  p09_handoff_packet_id: string
  p10_data_request_packet_id: string

  received_upgrade_candidates:
    calibration_candidate_ids: list
    missed_negative_rule_ids: list
    new_test_case_candidate_ids: list
    data_gap_impact_ids: list
    gate_error_review_ids: list
    runtime_simulation_quality_ids: list
    misclassification_review_ids: list

  candidate_counts:
    total_candidates_received: integer
    high_priority_candidates: integer
    medium_priority_candidates: integer
    low_priority_candidates: integer

  inherited_restrictions:
    - P09_PROPOSES_ONLY
    - P10_MUST_REVIEW_BEFORE_CHANGE
    - NO_DIRECT_RULE_MUTATION
    - NO_AUTO_DEPLOY
    - LIVE_EXECUTION_FORBIDDEN

  input_quality:
    p09_trace_available: boolean
    p09_attribution_confidence_available: boolean
    review_case_library_available: boolean
    input_quality_status:
      - UPGRADE_INPUT_HIGH_CONFIDENCE
      - UPGRADE_INPUT_USABLE
      - UPGRADE_INPUT_USABLE_WITH_GAPS
      - UPGRADE_INPUT_LOW_CONFIDENCE
      - UPGRADE_INPUT_UNUSABLE

  trace:
    upgrade_input_trace_id: string
    source_trace_ids: list
```

---

# 8. Upgrade Candidate Review Record

```yaml
upgrade_candidate_review_record:
  review_id: string
  upgrade_candidate_id: string
  generated_at: datetime

  candidate_source:
    source_controller: P09_REVIEW_REPLAY_CONTROLLER
    source_record_type:
      - CALIBRATION_CANDIDATE
      - MISSED_NEGATIVE_RULE
      - NEW_TEST_CASE_CANDIDATE
      - DATA_GAP_IMPACT
      - GATE_ERROR_REVIEW
      - RUNTIME_SIMULATION_QUALITY
      - MISCLASSIFICATION_REVIEW
    source_record_id: string
    review_case_ids: list

  review_checks:
    source_trace_complete: boolean
    attribution_confidence_acceptable: boolean
    problem_reproducible: boolean | null
    upgrade_scope_clear: boolean
    expected_effect_clear: boolean
    risk_of_change_declared: boolean
    not_single_case_auto_rule: boolean

  review_result:
    - ACCEPT_FOR_IMPACT_ASSESSMENT
    - ACCEPT_AS_TEST_ONLY
    - ACCEPT_AS_MANUAL_REVIEW_ONLY
    - NEED_MORE_SAMPLES
    - REJECT_DUPLICATE
    - REJECT_LOW_CONFIDENCE
    - REJECT_OUT_OF_SCOPE

  reason_cn: string
  trace:
    review_trace_id: string
    source_trace_ids: list
```

---

# 9. Sample Support Assessment Record

```yaml
sample_support_assessment_record:
  sample_support_id: string
  upgrade_candidate_id: string

  sample_basis:
    review_case_count: integer
    matching_failure_case_count: integer
    matching_success_case_count: integer
    contradictory_case_count: integer
    case_library_ids: list

  support_level:
    - MULTI_CASE_STRONG_SUPPORT
    - MULTI_CASE_MODERATE_SUPPORT
    - SINGLE_CASE_SAFETY_CRITICAL_SUPPORT
    - SINGLE_CASE_WEAK_SUPPORT
    - INSUFFICIENT_SUPPORT
    - CONTRADICTED_BY_CASES

  sample_distribution:
    affected_scenario_families: list
    affected_strategy_profiles: list
    affected_market_contexts: list
    affected_stages: list

  upgrade_permission_effect:
    can_change_global_rule: boolean
    can_create_test_case: boolean
    can_create_watch_rule: boolean
    requires_manual_approval: boolean

  anti_overfit_note_cn: string
```

---

# 10. Upgrade Classification Record

```yaml
upgrade_classification_record:
  classification_id: string
  upgrade_candidate_id: string

  upgrade_class:
    - FIELD_SCHEMA_UPGRADE
    - CONTRACT_UPGRADE
    - HARD_NEGATIVE_RULE_UPGRADE
    - POLICY_UPGRADE
    - PARAMETER_CALIBRATION
    - TEST_MATRIX_UPGRADE
    - TOOL_BINDING_UPGRADE
    - RUNTIME_MODEL_UPGRADE
    - REPORT_EXPLANATION_UPGRADE
    - GOVERNANCE_UPGRADE
    - MANUAL_REVIEW_ONLY

  target_stage:
    - P01_CANDIDATE_INTAKE
    - P02_SOURCE_DATA_FACT
    - P03_WALLET_ENTITY
    - P04_CHIP_STRUCTURE
    - P05_EVIDENCE
    - P06_SCENARIO_RECOGNITION
    - P07_STRATEGY_GATE
    - P08_EXECUTION_RISK
    - P09_REVIEW_REPLAY
    - PAPER_ONLY_RUNTIME
    - GOVERNANCE_PLANE
    - TRACE_HANDOFF_ACCEPTANCE
    - RUNNER_TOOL_BINDING
    - GLOBAL

  priority:
    - CRITICAL
    - HIGH
    - MEDIUM
    - LOW
    - DEFERRED

  upgrade_rationale_cn: string
```

---

# 11. Upgrade Impact Assessment Record

```yaml
upgrade_impact_assessment_record:
  impact_assessment_id: string
  upgrade_candidate_id: string

  affected_artifacts:
    affected_schemas: list
    affected_contracts: list
    affected_policies: list
    affected_state_machines: list
    affected_hard_negative_rules: list
    affected_test_matrices: list
    affected_reports: list
    affected_runner_tools: list
    affected_data_dirs: list

  affected_flow:
    upstream_stages_impacted: list
    downstream_stages_impacted: list
    handoff_packets_impacted: list
    acceptance_criteria_impacted: list
    trace_requirements_impacted: list

  risk_assessment:
    breaking_change: boolean
    backward_compatible: boolean
    migration_required: boolean
    replay_required: boolean
    manual_review_required: boolean

  severity:
    - LOW_IMPACT
    - MEDIUM_IMPACT
    - HIGH_IMPACT
    - SYSTEM_WIDE_IMPACT

  implementation_complexity:
    - SIMPLE_DOC_POLICY_UPDATE
    - SCHEMA_AND_CONTRACT_UPDATE
    - TOOL_BINDING_UPDATE
    - RUNNER_UPDATE_REQUIRED
    - MULTI_STAGE_SYSTEM_UPDATE
```

---

# 12. Overfit Risk Assessment Record

```yaml
overfit_risk_assessment_record:
  overfit_risk_id: string
  upgrade_candidate_id: string

  overfit_checks:
    based_on_single_case: boolean
    case_is_outlier: boolean
    contradicts_success_cases: boolean
    would_block_valid_scenarios: boolean
    would_over_relax_gate: boolean
    would_increase_false_positive_risk: boolean
    would_increase_false_negative_risk: boolean

  overfit_risk_level:
    - LOW
    - MEDIUM
    - HIGH
    - UNACCEPTABLE

  mitigation:
    - REQUIRE_MORE_SAMPLES
    - LIMIT_TO_TEST_CASE
    - LIMIT_TO_OBSERVE_RULE
    - LIMIT_TO_MANUAL_REVIEW
    - APPLY_AS_TEMPORARY_SAFETY_BLOCK
    - REJECT_UPGRADE

  decision_effect:
    can_proceed_to_upgrade_package: boolean
    requires_manual_approval: boolean
```

---

# 13. Compatibility Assessment Record

```yaml
compatibility_assessment_record:
  compatibility_id: string
  upgrade_candidate_id: string

  compatibility_checks:
    p01_to_p02_contract_compatible: boolean | null
    p02_to_p03_contract_compatible: boolean | null
    p03_to_p04_contract_compatible: boolean | null
    p04_to_p05_contract_compatible: boolean | null
    p05_to_p06_contract_compatible: boolean | null
    p06_to_p07_contract_compatible: boolean | null
    p07_to_p08_contract_compatible: boolean | null
    p08_to_paper_runtime_contract_compatible: boolean | null
    p09_to_p10_contract_compatible: boolean | null

  data_compatibility:
    old_records_still_readable: boolean
    migration_required: boolean
    default_values_required: boolean
    legacy_mapping_required: boolean

  result:
    compatibility_status:
      - COMPATIBLE
      - COMPATIBLE_WITH_MIGRATION
      - COMPATIBLE_WITH_DEFAULTS
      - BREAKING_CHANGE_REQUIRES_MAJOR_VERSION
      - INCOMPATIBLE_REJECT

  required_migration_tasks: list
```

---

# 14. Contract Schema Upgrade Proposal Record

```yaml
contract_schema_upgrade_proposal_record:
  proposal_id: string
  upgrade_candidate_id: string

  target:
    target_files:
      - schema_file_path: string
        contract_file_path: string | null
        stage: string

  proposed_changes:
    add_fields:
      - field_name: string
        field_type: string
        required_level:
          - REQUIRED
          - REQUIRED_IF_AVAILABLE
          - OPTIONAL
          - OBSERVE_ONLY
        reason_cn: string

    modify_fields:
      - field_name: string
        old_definition: string
        new_definition: string
        reason_cn: string

    deprecate_fields:
      - field_name: string
        deprecation_reason_cn: string
        replacement_field: string | null

  validation_required:
    schema_validation_required: true
    contract_validation_required: true
    handoff_validation_required: true
    backward_compatibility_check_required: true

  versioning:
    proposed_version_bump:
      - PATCH
      - MINOR
      - MAJOR
```

---

# 15. Rule Policy Upgrade Proposal Record

```yaml
rule_policy_upgrade_proposal_record:
  proposal_id: string
  upgrade_candidate_id: string

  target_policy:
    stage: string
    policy_file_path: string
    rule_file_path: string | null

  proposed_rule_change:
    change_type:
      - ADD_HARD_NEGATIVE
      - MODIFY_HARD_NEGATIVE
      - ADD_PAUSE_RULE
      - ADD_OBSERVE_RULE
      - MODIFY_GATE_POLICY
      - MODIFY_CONFLICT_POLICY
      - MODIFY_UNKNOWN_POLICY
      - MODIFY_USAGE_PERMISSION_POLICY

    condition_cn: string
    condition_machine_readable: object | null
    result:
      - BLOCK
      - PAUSE
      - OBSERVE
      - HUMAN_CONFIRMATION_REQUIRED
      - WEAK_USE_ONLY
      - DO_NOT_USE

    severity:
      - HARD
      - HIGH
      - MEDIUM
      - LOW

  safety_check:
    could_block_valid_cases: boolean
    could_allow_bad_cases: boolean
    requires_regression_test: true
    requires_manual_approval: boolean

  examples_from_review:
    supporting_review_case_ids: list
    contradictory_review_case_ids: list
```

---

# 16. Parameter Calibration Proposal Record

```yaml
parameter_calibration_proposal_record:
  calibration_proposal_id: string
  upgrade_candidate_id: string

  target_parameter:
    stage: string
    parameter_name: string
    current_value: any
    proposed_value: any
    parameter_type:
      - THRESHOLD
      - WEIGHT
      - TIME_WINDOW
      - SCORE_CUTOFF
      - FRESHNESS_LIMIT
      - SLIPPAGE_LIMIT
      - LIQUIDITY_LIMIT

  calibration_basis:
    supporting_review_case_ids: list
    sample_count: integer
    observed_failure_pattern_cn: string
    expected_improvement_cn: string

  validation_plan:
    required_backtest: boolean
    required_replay: boolean
    required_regression_tests: list
    acceptance_threshold_cn: string

  risk:
    overfit_risk_level: string
    false_positive_risk_change:
      - INCREASE
      - DECREASE
      - UNKNOWN
    false_negative_risk_change:
      - INCREASE
      - DECREASE
      - UNKNOWN

  approval:
    auto_apply_allowed: false
    manual_approval_required: true
```

---

# 17. Test Matrix Upgrade Record

```yaml
test_matrix_upgrade_record:
  test_upgrade_id: string
  upgrade_candidate_id: string

  target_test_matrix:
    - P01_TEST_MATRIX
    - P02_TEST_MATRIX
    - P03_TEST_MATRIX
    - P04_TEST_MATRIX
    - P05_TEST_MATRIX
    - P06_TEST_MATRIX
    - P07_TEST_MATRIX
    - P08_TEST_MATRIX
    - P09_TEST_MATRIX
    - P10_TEST_MATRIX
    - PAPER_RUNTIME_TEST_MATRIX
    - INTEGRATION_TEST_MATRIX

  new_test_cases:
    - test_id: string
      name_cn: string
      input_condition_cn: string
      expected_output_cn: string
      expected_status:
        - READY
        - READY_WITH_GAPS
        - REJECTED
        - BLOCKED
        - PAUSE
        - OBSERVE
        - PAPER_CANDIDATE
        - PAPER_RUNTIME_ALLOWED
      reason_cn: string
      source_review_case_ids: list

  test_type:
    - UNIT_SCHEMA_TEST
    - POLICY_TEST
    - STATE_MACHINE_TEST
    - HANDOFF_TEST
    - REGRESSION_TEST
    - ADVERSARIAL_TEST
    - END_TO_END_REPLAY_TEST

  required_before_release: true
```

---

# 18. Tool Binding Upgrade Proposal Record

```yaml
tool_binding_upgrade_proposal_record:
  tool_binding_proposal_id: string
  upgrade_candidate_id: string

  target_tool_or_runner:
    - GMGN_TOOL_BINDING
    - OKX_QUOTE_BINDING
    - OKX_SECURITY_BINDING
    - CHAIN_RAW_BINDING
    - KLINE_PROVIDER_BINDING
    - PAPER_RUNTIME_RUNNER
    - PHASE_CONTROLLER_RUNNER
    - TELEGRAM_PANEL_BINDING

  issue_type:
    - FIELD_MAPPING_MISSING
    - API_RESPONSE_SHAPE_CHANGED
    - STALE_DATA_PULL
    - ERROR_HANDLING_MISSING
    - RETRY_POLICY_WEAK
    - OUTPUT_PATH_INCONSISTENT
    - TRACE_NOT_WRITTEN
    - HANDOFF_NOT_WRITTEN

  proposed_change_cn: string

  required_outputs_after_change:
    - normalized_field_mapping
    - error_handling_policy
    - retry_policy
    - trace_write
    - acceptance_check
    - report_update

  testing_required:
    mock_response_test: boolean
    real_source_dry_run: boolean
    regression_replay_required: boolean
```

---

# 19. Runtime Model Upgrade Proposal Record

```yaml
runtime_model_upgrade_proposal_record:
  runtime_model_upgrade_id: string
  upgrade_candidate_id: string

  target_runtime_model:
    - SLIPPAGE_MODEL
    - FEE_MODEL
    - EXIT_MODEL
    - LIQUIDITY_CAPACITY_MODEL
    - SELLABILITY_MODEL
    - POSITION_UPDATE_MODEL
    - RISK_EVENT_MODEL

  observed_problem:
    problem_cn: string
    source_runtime_simulation_quality_ids: list

  proposed_model_change:
    change_cn: string
    required_inputs: list
    expected_outputs: list

  validation:
    compare_old_vs_new_required: true
    replay_cases_required: list
    acceptance_metric:
      - LOWER_SIMULATION_DISTORTION
      - MORE_CONSERVATIVE_PNL
      - BETTER_EXIT_REALISM
      - BETTER_RISK_EVENT_CAPTURE

  restrictions:
    cannot_enable_live_execution: true
    paper_only: true
```

---

# 20. Report Explanation Upgrade Proposal Record

```yaml
report_explanation_upgrade_proposal_record:
  report_upgrade_id: string
  upgrade_candidate_id: string

  target_report:
    - P02_SOURCE_DATA_FACT_REPORT
    - P03_WALLET_ENTITY_REPORT
    - P04_CHIP_STRUCTURE_REPORT
    - P05_EVIDENCE_REPORT
    - P06_SCENARIO_REPORT
    - P07_STRATEGY_GATE_REPORT
    - P08_EXECUTION_RISK_REPORT
    - P09_REVIEW_REPLAY_REPORT
    - TELEGRAM_STATUS_PANEL
    - DAILY_PAPER_REPORT

  issue:
    - MISSING_REASON_FIELD
    - MISSING_COUNTER_EVIDENCE
    - MISSING_LIMITATION
    - MISSING_TRACE_REFERENCE
    - MISSING_FAILURE_ATTRIBUTION
    - UNCLEAR_DECISION_EXPLANATION

  proposed_report_fields:
    - field_name: string
      description_cn: string
      source_record: string
      required: boolean

  expected_effect_cn: string
```

---

# 21. Upgrade Decision Record

```yaml
upgrade_decision_record:
  decision_id: string
  upgrade_candidate_id: string
  generated_at: datetime

  decision:
    - APPROVE_FOR_CONTROLLED_PACKAGE
    - APPROVE_TEST_ONLY
    - APPROVE_MANUAL_REVIEW_ONLY
    - NEED_MORE_SAMPLES
    - DEFER
    - REJECT

  decision_basis:
    candidate_review_id: string
    sample_support_id: string
    impact_assessment_id: string
    overfit_risk_id: string
    compatibility_assessment_id: string

  decision_reason_cn:
    primary_reason: string
    supporting_reasons: list
    blocking_reasons: list
    unresolved_risks: list

  allowed_next_step:
    - BUILD_CONTROLLED_UPGRADE_PACKAGE
    - BUILD_TEST_CASE_ONLY
    - SEND_TO_MANUAL_REVIEW
    - HOLD_IN_BACKLOG
    - REJECT_NO_ACTION

  restrictions:
    no_direct_production_change: true
    regression_required_before_release: true
    rollback_plan_required: true
```

---

# 22. Regression Test Plan Record

```yaml
regression_test_plan_record:
  regression_plan_id: string
  controlled_upgrade_package_id: string | null
  upgrade_candidate_ids: list

  required_tests:
    schema_tests: list
    contract_tests: list
    policy_tests: list
    state_machine_tests: list
    handoff_tests: list
    trace_tests: list
    replay_tests: list
    integration_tests: list
    paper_runtime_tests: list

  regression_scope:
    affected_stages: list
    required_historical_replay_cases: list
    required_counterexample_cases: list

  pass_criteria:
    all_schema_tests_pass: true
    all_contract_tests_pass: true
    no_handoff_breakage: true
    no_trace_breakage: true
    no_live_execution_path_created: true
    no_paper_runtime_bypass_created: true

  fail_action:
    - BLOCK_RELEASE
    - RETURN_TO_P09_FOR_MORE_REVIEW
    - SEND_TO_MANUAL_REVIEW
```

---

# 23. Release And Rollback Plan Record

```yaml
release_and_rollback_plan_record:
  release_plan_id: string
  controlled_upgrade_package_id: string

  release_type:
    - DOC_POLICY_ONLY
    - SCHEMA_CONTRACT_UPDATE
    - RULE_POLICY_UPDATE
    - PARAMETER_UPDATE
    - TOOL_BINDING_UPDATE
    - RUNTIME_MODEL_UPDATE
    - MULTI_STAGE_RELEASE

  release_mode:
    - DRY_RUN_ONLY
    - SHADOW_MODE
    - PAPER_ONLY_GRADUAL
    - MANUAL_APPROVAL_REQUIRED
    - BLOCKED_FROM_RELEASE

  rollout_plan:
    apply_to:
      - TEST_FIXTURE
      - REPLAY_ONLY
      - PAPER_ONLY_RUNTIME
      - REPORTING_ONLY
    rollout_steps: list

  rollback_plan:
    rollback_required: true
    previous_version_reference: string
    rollback_steps: list
    rollback_trigger_conditions:
      - regression_failure
      - handoff_breakage
      - trace_breakage
      - increased_false_positive_rate
      - increased_false_negative_rate
      - runtime_error_rate_increase

  safety:
    live_execution_allowed: false
    wallet_signing_allowed: false
    auto_deploy_allowed: false
```

---

# 24. Upgrade Approval Requirement Record

```yaml
upgrade_approval_requirement_record:
  approval_requirement_id: string
  upgrade_candidate_id: string

  approval_required:
    manual_approval_required: boolean
    governance_approval_required: boolean
    test_pass_required: boolean
    rollback_plan_required: boolean

  approval_reason:
    - SYSTEM_WIDE_IMPACT
    - BREAKING_CHANGE
    - HARD_NEGATIVE_RULE_CHANGE
    - STRATEGY_GATE_POLICY_CHANGE
    - EXECUTION_RISK_POLICY_CHANGE
    - RUNTIME_MODEL_CHANGE
    - SINGLE_CASE_SUPPORT_ONLY
    - HIGH_OVERFIT_RISK

  allowed_approval_outcomes:
    - APPROVE_DRY_RUN
    - APPROVE_SHADOW_MODE
    - APPROVE_PAPER_ONLY
    - REQUEST_MORE_TESTS
    - REJECT

  restrictions:
    approval_does_not_allow_live_execution: true
    approval_does_not_skip_regression_tests: true
```

---

# 25. Controlled Upgrade Package Record

这是 P10 的核心输出之一。

```yaml
controlled_upgrade_package_record:
  package_id: string
  generated_at: datetime
  package_version: string

  package_scope:
    upgrade_candidate_ids: list
    target_stages: list
    upgrade_types: list
    priority:
      - CRITICAL
      - HIGH
      - MEDIUM
      - LOW

  included_proposals:
    contract_schema_upgrade_proposals: list
    rule_policy_upgrade_proposals: list
    parameter_calibration_proposals: list
    test_matrix_upgrade_records: list
    tool_binding_upgrade_proposals: list
    runtime_model_upgrade_proposals: list
    report_explanation_upgrade_proposals: list

  required_validation:
    regression_test_plan_id: string
    compatibility_assessment_ids: list
    approval_requirement_ids: list
    release_and_rollback_plan_id: string

  package_status:
    - PACKAGE_DRAFT
    - PACKAGE_READY_FOR_REVIEW
    - PACKAGE_APPROVED_FOR_DRY_RUN
    - PACKAGE_APPROVED_FOR_SHADOW_MODE
    - PACKAGE_APPROVED_FOR_PAPER_ONLY
    - PACKAGE_REJECTED
    - PACKAGE_DEFERRED

  restrictions:
    no_auto_deploy: true
    no_live_execution: true
    no_wallet_signing: true
    no_runtime_mutation_without_approval: true

  trace:
    package_trace_id: string
    source_review_trace_ids: list
```

---

# 26. Controlled Upgrade Task Packet

这是给 HER / Runner / Tool Binding 的可执行任务书。

```yaml
controlled_upgrade_task_packet:
  task_packet_id: string
  controlled_upgrade_package_id: string
  generated_at: datetime

  task_scope:
    target_repo_root: /root/sikk-gmgn
    target_system_dirs: list
    target_data_dirs: list
    target_files_to_create_or_modify: list

  implementation_tasks:
    - task_id: string
      task_type:
        - CREATE_FILE
        - UPDATE_SCHEMA
        - UPDATE_CONTRACT
        - UPDATE_POLICY
        - UPDATE_TEST
        - UPDATE_RUNNER
        - UPDATE_REPORT
        - UPDATE_INDEX
      target_file: string
      instruction_cn: string
      acceptance_check_cn: string

  validation_commands:
    - command_cn: string
      command: string
      expected_result_cn: string

  required_reports:
    - changed_files_report
    - test_results_report
    - regression_report
    - compatibility_report
    - rollback_readiness_report

  execution_constraints:
    stop_if_tests_fail: true
    stop_if_trace_breaks: true
    stop_if_handoff_breaks: true
    stop_if_live_execution_path_detected: true
    no_auto_deploy: true
```

---

# 27. Version Change Record

```yaml
version_change_record:
  version_change_id: string
  controlled_upgrade_package_id: string

  version_targets:
    schema_versions: object
    contract_versions: object
    policy_versions: object
    test_matrix_versions: object
    runner_versions: object
    report_versions: object

  version_bump:
    bump_type:
      - PATCH
      - MINOR
      - MAJOR
      - NONE_TEST_ONLY

  changelog:
    summary_cn: string
    changed_artifacts: list
    migration_notes: list
    rollback_notes: list

  compatibility:
    backward_compatible: boolean
    migration_required: boolean
    old_runtime_data_readable: boolean

  release_status:
    - VERSION_DRAFT
    - VERSION_READY_FOR_REVIEW
    - VERSION_APPROVED
    - VERSION_RELEASED
    - VERSION_ROLLED_BACK
```

---

# 28. Upgrade Backlog Record

```yaml
upgrade_backlog_record:
  backlog_id: string
  generated_at: datetime

  backlog_items:
    - backlog_item_id: string
      upgrade_candidate_id: string
      priority:
        - CRITICAL
        - HIGH
        - MEDIUM
        - LOW
        - DEFERRED
      status:
        - NEW
        - REVIEWED
        - APPROVED_FOR_PACKAGE
        - WAITING_FOR_MORE_SAMPLES
        - WAITING_FOR_MANUAL_APPROVAL
        - IN_TASK_PACKET
        - COMPLETED
        - REJECTED
      target_stage: string
      reason_cn: string

  backlog_summary:
    critical_count: integer
    high_count: integer
    medium_count: integer
    low_count: integer
    deferred_count: integer
```

---

# 29. P10 to Implementation Handoff Packet

```yaml
p10_to_implementation_handoff_packet:
  packet_id: string
  packet_type: P10_TO_IMPLEMENTATION_HANDOFF
  generated_at: datetime

  route:
    from_controller: P10_SELF_UPGRADE_CONTROLLER
    to:
      - GOVERNANCE_REVIEW
      - RUNNER_TOOL_BINDING
      - CONTROLLED_IMPLEMENTATION_TASK_QUEUE
      - MANUAL_APPROVAL_QUEUE

  upstream_control:
    p09_handoff_packet_id: string
    p10_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  upgrade_scope:
    total_upgrade_candidates_reviewed: integer
    approved_for_package_count: integer
    test_only_count: integer
    manual_review_count: integer
    deferred_count: integer
    rejected_count: integer

  upgrade_package:
    controlled_upgrade_package_records_path: string
    controlled_upgrade_task_packets_path: string
    regression_test_plan_records_path: string
    release_and_rollback_plan_records_path: string
    version_change_records_path: string
    upgrade_backlog_records_path: string

  implementation_request:
    task_packet_ids: list
    target_files_to_create_or_modify: list
    required_tests: list
    required_reports: list

  approval:
    approval_requirement_records_path: string
    manual_approval_required_items: list
    governance_required_items: list

  restrictions:
    - CONTROLLED_UPGRADE_ONLY
    - NO_AUTO_DEPLOY
    - NO_DIRECT_PRODUCTION_MUTATION
    - NO_LIVE_EXECUTION
    - NO_WALLET_SIGNING
    - REGRESSION_REQUIRED
    - ROLLBACK_REQUIRED

  downstream_permission:
    allowed:
      - GOVERNANCE_REVIEW
      - IMPLEMENTATION_TASK_QUEUE
      - RUNNER_TOOL_BINDING_DRY_RUN
      - TEST_MATRIX_UPDATE
    forbidden:
      - LIVE_EXECUTION
      - AUTO_DEPLOY_WITHOUT_APPROVAL
      - DIRECT_RULE_MUTATION
      - PAPER_RUNTIME_MUTATION_WITHOUT_TEST

  read_instruction:
    implementation_must_read_first:
      - p10_to_implementation_handoff_packet
      - controlled_upgrade_package_records
      - controlled_upgrade_task_packets
      - regression_test_plan_records
      - release_and_rollback_plan_records
      - approval_requirement_records
```

---

# 30. P10 Gap Policy

```yaml
p10_gap_policy:
  BLOCKING_GAP:
    result: P10_BLOCKED
    examples:
      - p09_handoff_missing
      - trace_missing
      - acceptance_missing
      - direct_rule_mutation_requested
      - auto_deploy_requested
      - live_execution_requested

  CRITICAL_GAP:
    result: P10_REJECTED
    examples:
      - no_upgrade_candidates
      - all_candidates_low_confidence
      - no_source_review_records
      - no_upgrade_output_contract
      - compatibility_assessment_missing
      - regression_plan_missing_for_release

  HIGH_GAP:
    result: P10_READY_WITH_GAPS
    downstream_permission: IMPLEMENTATION_LIMITED_OR_MANUAL_REVIEW
    examples:
      - sample_support_insufficient
      - overfit_risk_high
      - breaking_change_requires_major_version
      - manual_approval_required
      - migration_required

  MEDIUM_GAP:
    result: P10_READY_WITH_GAPS
    downstream_permission: DRY_RUN_ONLY
    examples:
      - replay_cases_limited
      - test_coverage_partial
      - compatibility_requires_defaults
      - tool_binding_uncertain

  LOW_GAP:
    result: P10_READY_WITH_GAPS
    downstream_permission: IMPLEMENTATION_ALLOWED_WITH_NOTE
    examples:
      - optional_report_update_missing
      - minor_changelog_metadata_missing
      - noncritical_version_note_missing
```

---

# 31. P10 Hard Negative Rules

```yaml
p10_hard_negative_rules:
  - rule_id: P10_BLOCK_001
    name: 未读取 P09 handoff
    condition: p09_to_p10_handoff_packet_missing == true
    result: P10_BLOCKED
    reason: P10 不能绕过 P09 启动

  - rule_id: P10_BLOCK_002
    name: 无升级候选
    condition: upgrade_candidate_count == 0
    result: P10_REJECTED
    reason: 无升级候选不能生成升级包

  - rule_id: P10_BLOCK_003
    name: 单样本直接全局生效
    condition: single_case_candidate_promoted_to_global_rule_without_safety_exception == true
    result: P10_BLOCKED
    reason: 单样本不能直接改变全局规则

  - rule_id: P10_BLOCK_004
    name: 缺少影响分析
    condition: upgrade_decision_approved == true and impact_assessment_missing == true
    result: P10_BLOCKED
    reason: 任何受控升级必须先做影响分析

  - rule_id: P10_BLOCK_005
    name: 缺少回归测试计划
    condition: controlled_upgrade_package_created == true and regression_test_plan_missing == true
    result: P10_BLOCKED
    reason: 升级包必须绑定回归测试

  - rule_id: P10_BLOCK_006
    name: 缺少回滚计划
    condition: release_plan_created == true and rollback_plan_missing == true
    result: P10_BLOCKED
    reason: 任何发布计划必须具备回滚路径

  - rule_id: P10_BLOCK_007
    name: 破坏 handoff 合约
    condition: compatibility_status == INCOMPATIBLE_REJECT
    result: P10_BLOCKED
    reason: 不能发布破坏交接链的升级

  - rule_id: P10_BLOCK_008
    name: 自动部署请求
    condition: auto_deploy_requested == true
    result: P10_BLOCKED
    reason: P10 不允许自动部署

  - rule_id: P10_BLOCK_009
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P10_BLOCKED
    reason: 当前系统禁止自动实盘

  - rule_id: P10_BLOCK_010
    name: 绕过治理审批
    condition: manual_or_governance_approval_required == true and approval_bypassed == true
    result: P10_BLOCKED
    reason: 需要审批的升级不能绕过治理
```

---

# 32. P10 状态机专业版

```yaml
p10_self_upgrade_state_machine:
  states:
    - P10_UNINITIALIZED
    - P10_CONTEXT_LOADED
    - P10_HANDOFF_READ
    - P10_INPUT_MANIFEST_BUILT
    - P10_CANDIDATES_REGISTERED
    - P10_CANDIDATE_REVIEWS_BUILT
    - P10_SAMPLE_SUPPORT_ASSESSED
    - P10_UPGRADE_CLASSIFIED
    - P10_IMPACT_ASSESSED
    - P10_OVERFIT_RISK_ASSESSED
    - P10_COMPATIBILITY_ASSESSED
    - P10_SCHEMA_CONTRACT_PROPOSALS_BUILT
    - P10_RULE_POLICY_PROPOSALS_BUILT
    - P10_PARAMETER_CALIBRATION_PROPOSALS_BUILT
    - P10_TEST_MATRIX_UPGRADES_BUILT
    - P10_TOOL_BINDING_PROPOSALS_BUILT
    - P10_RUNTIME_MODEL_PROPOSALS_BUILT
    - P10_REPORT_EXPLANATION_PROPOSALS_BUILT
    - P10_UPGRADE_DECISIONS_BUILT
    - P10_REGRESSION_TEST_PLANS_BUILT
    - P10_RELEASE_ROLLBACK_PLANS_BUILT
    - P10_APPROVAL_REQUIREMENTS_BUILT
    - P10_CONTROLLED_UPGRADE_PACKAGES_BUILT
    - P10_CONTROLLED_TASK_PACKETS_BUILT
    - P10_VERSION_CHANGE_RECORDS_BUILT
    - P10_BACKLOG_UPDATED
    - P10_READY_FOR_ACCEPTANCE
    - P10_ACCEPTANCE_READY
    - P10_READY_FOR_IMPLEMENTATION_HANDOFF
    - P10_READY_WITH_GAPS
    - P10_REJECTED
    - P10_BLOCKED

  critical_transitions:
    - from: P10_HANDOFF_READ
      to: P10_INPUT_MANIFEST_BUILT
      condition: p09_handoff_valid == true

    - from: P10_INPUT_MANIFEST_BUILT
      to: P10_CANDIDATES_REGISTERED
      condition: upgrade_candidates_available == true

    - from: P10_CANDIDATES_REGISTERED
      to: P10_CANDIDATE_REVIEWS_BUILT
      condition: upgrade_candidate_review_records_created == true

    - from: P10_CANDIDATE_REVIEWS_BUILT
      to: P10_SAMPLE_SUPPORT_ASSESSED
      condition: sample_support_assessments_created == true

    - from: P10_SAMPLE_SUPPORT_ASSESSED
      to: P10_UPGRADE_CLASSIFIED
      condition: upgrade_classification_records_created == true

    - from: P10_UPGRADE_CLASSIFIED
      to: P10_IMPACT_ASSESSED
      condition: impact_assessment_records_created == true

    - from: P10_IMPACT_ASSESSED
      to: P10_OVERFIT_RISK_ASSESSED
      condition: overfit_risk_assessment_records_created == true

    - from: P10_OVERFIT_RISK_ASSESSED
      to: P10_COMPATIBILITY_ASSESSED
      condition: compatibility_assessment_records_created == true

    - from: P10_COMPATIBILITY_ASSESSED
      to: P10_UPGRADE_DECISIONS_BUILT
      condition: upgrade_decision_records_created == true

    - from: P10_UPGRADE_DECISIONS_BUILT
      to: P10_REGRESSION_TEST_PLANS_BUILT
      condition: approved_candidates_have_regression_plans == true

    - from: P10_REGRESSION_TEST_PLANS_BUILT
      to: P10_RELEASE_ROLLBACK_PLANS_BUILT
      condition: release_and_rollback_plans_created == true

    - from: P10_RELEASE_ROLLBACK_PLANS_BUILT
      to: P10_APPROVAL_REQUIREMENTS_BUILT
      condition: approval_requirement_records_created == true

    - from: P10_APPROVAL_REQUIREMENTS_BUILT
      to: P10_CONTROLLED_UPGRADE_PACKAGES_BUILT
      condition: controlled_upgrade_package_records_created == true

    - from: P10_CONTROLLED_UPGRADE_PACKAGES_BUILT
      to: P10_CONTROLLED_TASK_PACKETS_BUILT
      condition: controlled_upgrade_task_packets_created == true

    - from: P10_CONTROLLED_TASK_PACKETS_BUILT
      to: P10_VERSION_CHANGE_RECORDS_BUILT
      condition: version_change_records_created == true

    - from: P10_VERSION_CHANGE_RECORDS_BUILT
      to: P10_BACKLOG_UPDATED
      condition: upgrade_backlog_records_updated == true

    - from: P10_BACKLOG_UPDATED
      to: P10_READY_FOR_ACCEPTANCE
      condition: p10_output_contract_ready == true

    - from: P10_READY_FOR_ACCEPTANCE
      to: P10_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P10_ACCEPTANCE_READY
      to: P10_READY_FOR_IMPLEMENTATION_HANDOFF
      condition: p10_to_implementation_handoff_packet_created == true
```

---

# 33. P10 文件体系

## 33.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p10_self_upgrade_controller/
```

必须创建：

```text
p10_self_upgrade_controller.yaml
p10_self_upgrade_context.md
p10_input_contract.yaml
p10_output_contract.yaml
upgrade_input_manifest_schema.yaml
upgrade_candidate_review_schema.yaml
sample_support_assessment_schema.yaml
upgrade_classification_schema.yaml
upgrade_impact_assessment_schema.yaml
overfit_risk_assessment_schema.yaml
compatibility_assessment_schema.yaml
contract_schema_upgrade_proposal_schema.yaml
rule_policy_upgrade_proposal_schema.yaml
parameter_calibration_proposal_schema.yaml
test_matrix_upgrade_schema.yaml
tool_binding_upgrade_proposal_schema.yaml
runtime_model_upgrade_proposal_schema.yaml
report_explanation_upgrade_proposal_schema.yaml
upgrade_decision_schema.yaml
regression_test_plan_schema.yaml
release_and_rollback_plan_schema.yaml
upgrade_approval_requirement_schema.yaml
controlled_upgrade_package_schema.yaml
controlled_upgrade_task_packet_schema.yaml
version_change_record_schema.yaml
upgrade_backlog_schema.yaml
p10_to_implementation_handoff_contract.yaml
upgrade_classification_policy.yaml
sample_support_policy.yaml
overfit_control_policy.yaml
impact_assessment_policy.yaml
compatibility_policy.yaml
controlled_release_policy.yaml
rollback_policy.yaml
approval_policy.yaml
self_upgrade_gap_policy.yaml
self_upgrade_hard_negative_rules.yaml
self_upgrade_state_machine.yaml
self_upgrade_trace_requirements.yaml
p10_acceptance_criteria.md
p10_storage_constitution.md
p10_test_matrix.yaml
p10_report_model.yaml
p10_review_checklist.md
her_p10_execution_protocol.md
```

---

## 33.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p10_self_upgrade/
  input_manifest/
  candidate_reviews/
  sample_support/
  classifications/
  impact_assessments/
  overfit_risk/
  compatibility/
  schema_contract_proposals/
  rule_policy_proposals/
  parameter_calibrations/
  test_matrix_upgrades/
  tool_binding_proposals/
  runtime_model_proposals/
  report_explanation_proposals/
  upgrade_decisions/
  regression_test_plans/
  release_rollback_plans/
  approval_requirements/
  controlled_upgrade_packages/
  controlled_task_packets/
  version_changes/
  upgrade_backlog/
  implementation_handoff/
  rejected_candidates/
  blocked_candidates/
  manual_review/
  quality/
  gaps/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 34. P10 测试矩阵

```yaml
p10_test_matrix:
  - test_id: P10_TEST_001
    name: P09 提交多案例支持的硬否定升级候选
    expected_status: P10_READY_FOR_IMPLEMENTATION_HANDOFF
    expected_output:
      - rule_policy_upgrade_proposal
      - regression_test_plan
      - controlled_upgrade_package

  - test_id: P10_TEST_002
    name: 缺 P09 handoff
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_003
    name: 无升级候选
    expected_status: P10_REJECTED

  - test_id: P10_TEST_004
    name: 单个普通失败样本要求全局改规则
    expected_status: P10_BLOCKED
    expected_reason: SINGLE_CASE_CANNOT_GLOBAL_RULE

  - test_id: P10_TEST_005
    name: 单个安全关键样本提出临时保护性阻断
    expected_output:
      - manual_approval_required
      - temporary_safety_rule_candidate
      - rollback_plan_required

  - test_id: P10_TEST_006
    name: 升级候选缺影响分析
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_007
    name: schema 升级会破坏 P04→P05 handoff
    expected_status: P10_BLOCKED_OR_MAJOR_VERSION_REQUIRED

  - test_id: P10_TEST_008
    name: 参数校准存在高过拟合风险
    expected_decision: NEED_MORE_SAMPLES_OR_TEST_ONLY

  - test_id: P10_TEST_009
    name: 新测试样例候选不改生产逻辑
    expected_decision: APPROVE_TEST_ONLY

  - test_id: P10_TEST_010
    name: 工具绑定字段缺失导致 P02 数据缺口
    expected_output:
      - tool_binding_upgrade_proposal
      - mock_response_test
      - dry_run_required

  - test_id: P10_TEST_011
    name: 纸面仿真过度乐观，需要升级滑点模型
    expected_output:
      - runtime_model_upgrade_proposal
      - regression_replay_required

  - test_id: P10_TEST_012
    name: controlled package 缺回归测试计划
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_013
    name: controlled package 缺回滚计划
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_014
    name: 自动部署请求
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_015
    name: live execution requested
    expected_status: P10_BLOCKED

  - test_id: P10_TEST_016
    name: 升级提案只影响报告解释字段
    expected_decision: APPROVE_FOR_CONTROLLED_PACKAGE
    expected_release_type: DOC_POLICY_ONLY_OR_REPORT_UPDATE

  - test_id: P10_TEST_017
    name: hard negative 规则变更需要人工审批
    expected_output:
      - approval_requirement_record
      - release_and_rollback_plan

  - test_id: P10_TEST_018
    name: 回归测试发现 handoff trace 断裂
    expected_status: BLOCK_RELEASE
```

---

# 35. P10 报告模型

```yaml
p10_self_upgrade_report:
  report_id: string
  generated_at: datetime
  controller_id: P10_SELF_UPGRADE_CONTROLLER

  summary:
    upgrade_candidates_received: integer
    candidates_reviewed: integer
    approved_for_package_count: integer
    approved_test_only_count: integer
    manual_review_count: integer
    need_more_samples_count: integer
    deferred_count: integer
    rejected_count: integer
    blocked_count: integer

  upgrade_type_summary:
    field_schema_upgrade_count: integer
    contract_upgrade_count: integer
    hard_negative_rule_upgrade_count: integer
    policy_upgrade_count: integer
    parameter_calibration_count: integer
    test_matrix_upgrade_count: integer
    tool_binding_upgrade_count: integer
    runtime_model_upgrade_count: integer
    report_explanation_upgrade_count: integer
    governance_upgrade_count: integer

  impact_summary:
    low_impact_count: integer
    medium_impact_count: integer
    high_impact_count: integer
    system_wide_impact_count: integer
    breaking_change_count: integer
    migration_required_count: integer

  overfit_summary:
    low_overfit_risk_count: integer
    medium_overfit_risk_count: integer
    high_overfit_risk_count: integer
    rejected_for_overfit_count: integer

  compatibility_summary:
    compatible_count: integer
    compatible_with_migration_count: integer
    major_version_required_count: integer
    incompatible_reject_count: integer

  package_summary:
    controlled_upgrade_package_count: integer
    controlled_task_packet_count: integer
    regression_test_plan_count: integer
    release_rollback_plan_count: integer
    approval_required_count: integer

  implementation_handoff_summary:
    handoff_ready: boolean
    task_packets_ready: integer
    high_priority_tasks: list
    manual_approval_items: list

  compliance:
    direct_rule_mutation_generated: false
    auto_deploy_generated: false
    live_execution_path_detected: false
    regression_plan_missing_for_package: false
    rollback_plan_missing_for_release: false
```

---

# 36. HER P10 执行协议

```text
HER 执行 P10 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P10 controller context
4. 读取 P09 → P10 handoff packet
5. 读取 p10_upgrade_candidate_data_request_packet
6. 读取 Governance / Trace / Acceptance / Handoff 输出
7. 读取 contract_index、schema_index、global_hard_negative_rules、directory_constitution
8. 建立 upgrade_input_manifest
9. 注册所有 P09 upgrade candidates
10. 生成 upgrade_candidate_review_records
11. 生成 sample_support_assessment_records
12. 生成 upgrade_classification_records
13. 生成 upgrade_impact_assessment_records
14. 生成 overfit_risk_assessment_records
15. 生成 compatibility_assessment_records
16. 生成 contract_schema_upgrade_proposal_records
17. 生成 rule_policy_upgrade_proposal_records
18. 生成 parameter_calibration_proposal_records
19. 生成 test_matrix_upgrade_records
20. 生成 tool_binding_upgrade_proposal_records
21. 生成 runtime_model_upgrade_proposal_records
22. 生成 report_explanation_upgrade_proposal_records
23. 生成 upgrade_decision_records
24. 生成 regression_test_plan_records
25. 生成 release_and_rollback_plan_records
26. 生成 upgrade_approval_requirement_records
27. 生成 controlled_upgrade_package_records
28. 生成 controlled_upgrade_task_packets
29. 生成 version_change_records
30. 更新 upgrade_backlog_records
31. 生成 P10 gap report
32. 写入 P10 trace
33. 生成 p10_self_upgrade_report
34. 生成 p10_to_implementation_handoff_packet
35. 执行 P10 acceptance
36. 只允许 handoff 给 Governance Review / Implementation Task Queue / Runner Tool Binding dry-run
```

禁止：

```text
1. 不允许无 P09 handoff 启动 P10
2. 不允许单样本直接改全局规则
3. 不允许无影响分析生成升级包
4. 不允许无回归测试计划发布升级
5. 不允许无回滚计划发布升级
6. 不允许破坏 handoff 合约
7. 不允许绕过 Governance approval
8. 不允许自动部署
9. 不允许触发 paper runtime
10. 不允许 live execution
11. 不允许钱包签名
12. 不允许直接修改生产运行状态
```

---

# 37. 给 HER 的专业化任务书

```text
任务名称：建立 P10 Self Upgrade Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p10_self_upgrade_controller/ 下建立 P10 Self Upgrade Controller。该控制器不是自动改规则模块，不是自动部署模块，也不是 AI 自己修改系统的无限权限模块，而是自我升级审查、规则校准、合约演进、测试扩展、版本发布与回滚控制器。它负责读取 P09 Review Replay Controller 输出的失败归因、成功归因、误判复盘、数据缺口影响、门控错误、仿真质量、校准候选、遗漏硬否定和新测试样例候选，将其转化为可审查、可测试、可版本化、可回滚的 Controlled Upgrade Package，并生成 Controlled Upgrade Task Packet 与 P10→Implementation Handoff Packet。

核心原则：
1. P10 只做受控升级审查与升级包生成。
2. P10 不直接修改生产规则。
3. P10 不自动部署。
4. P10 不触发 paper runtime。
5. P10 不允许 live execution。
6. P10 必须先审查 P09 upgrade candidate。
7. P10 必须评估样本支持程度。
8. P10 必须评估过拟合风险。
9. P10 必须评估影响范围和兼容性。
10. P10 必须生成回归测试计划。
11. P10 必须生成发布与回滚计划。
12. P10 必须生成审批要求。
13. P10 必须生成受控升级包。
14. P10 必须生成实现任务包。
15. P10 只能交接给 Governance Review / Implementation Task Queue / Runner Tool Binding dry-run。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p10_self_upgrade_controller/

需要创建系统文件：
1. p10_self_upgrade_controller.yaml
2. p10_self_upgrade_context.md
3. p10_input_contract.yaml
4. p10_output_contract.yaml
5. upgrade_input_manifest_schema.yaml
6. upgrade_candidate_review_schema.yaml
7. sample_support_assessment_schema.yaml
8. upgrade_classification_schema.yaml
9. upgrade_impact_assessment_schema.yaml
10. overfit_risk_assessment_schema.yaml
11. compatibility_assessment_schema.yaml
12. contract_schema_upgrade_proposal_schema.yaml
13. rule_policy_upgrade_proposal_schema.yaml
14. parameter_calibration_proposal_schema.yaml
15. test_matrix_upgrade_schema.yaml
16. tool_binding_upgrade_proposal_schema.yaml
17. runtime_model_upgrade_proposal_schema.yaml
18. report_explanation_upgrade_proposal_schema.yaml
19. upgrade_decision_schema.yaml
20. regression_test_plan_schema.yaml
21. release_and_rollback_plan_schema.yaml
22. upgrade_approval_requirement_schema.yaml
23. controlled_upgrade_package_schema.yaml
24. controlled_upgrade_task_packet_schema.yaml
25. version_change_record_schema.yaml
26. upgrade_backlog_schema.yaml
27. p10_to_implementation_handoff_contract.yaml
28. upgrade_classification_policy.yaml
29. sample_support_policy.yaml
30. overfit_control_policy.yaml
31. impact_assessment_policy.yaml
32. compatibility_policy.yaml
33. controlled_release_policy.yaml
34. rollback_policy.yaml
35. approval_policy.yaml
36. self_upgrade_gap_policy.yaml
37. self_upgrade_hard_negative_rules.yaml
38. self_upgrade_state_machine.yaml
39. self_upgrade_trace_requirements.yaml
40. p10_acceptance_criteria.md
41. p10_storage_constitution.md
42. p10_test_matrix.yaml
43. p10_report_model.yaml
44. p10_review_checklist.md
45. her_p10_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p10_self_upgrade/
  input_manifest/
  candidate_reviews/
  sample_support/
  classifications/
  impact_assessments/
  overfit_risk/
  compatibility/
  schema_contract_proposals/
  rule_policy_proposals/
  parameter_calibrations/
  test_matrix_upgrades/
  tool_binding_proposals/
  runtime_model_proposals/
  report_explanation_proposals/
  upgrade_decisions/
  regression_test_plans/
  release_rollback_plans/
  approval_requirements/
  controlled_upgrade_packages/
  controlled_task_packets/
  version_changes/
  upgrade_backlog/
  implementation_handoff/
  rejected_candidates/
  blocked_candidates/
  manual_review/
  quality/
  gaps/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p10_self_upgrade_controller.yaml：定义 P10 身份、职责、权限、上下游、状态码、禁止事项。
- p10_self_upgrade_context.md：写成 HER 执行前必须读取的 P10 上下文。
- p10_input_contract.yaml：定义 P10 必须读取的 P09 handoff、upgrade candidates、review records、system indices、Governance / Trace / Acceptance / Handoff。
- p10_output_contract.yaml：定义 upgrade review、impact、proposal、test、release、rollback、task packet、handoff 输出。
- upgrade_input_manifest_schema.yaml：定义 P10 接收的全部升级输入。
- upgrade_candidate_review_schema.yaml：定义升级候选审查。
- sample_support_assessment_schema.yaml：定义样本支持度评估。
- upgrade_classification_schema.yaml：定义升级类型分类。
- upgrade_impact_assessment_schema.yaml：定义影响范围分析。
- overfit_risk_assessment_schema.yaml：定义过拟合风险。
- compatibility_assessment_schema.yaml：定义兼容性评估。
- contract_schema_upgrade_proposal_schema.yaml：定义 schema / contract 升级提案。
- rule_policy_upgrade_proposal_schema.yaml：定义规则 / policy 升级提案。
- parameter_calibration_proposal_schema.yaml：定义参数校准提案。
- test_matrix_upgrade_schema.yaml：定义测试矩阵升级。
- tool_binding_upgrade_proposal_schema.yaml：定义工具绑定升级。
- runtime_model_upgrade_proposal_schema.yaml：定义纸面运行模型升级。
- report_explanation_upgrade_proposal_schema.yaml：定义报告解释升级。
- upgrade_decision_schema.yaml：定义升级决策。
- regression_test_plan_schema.yaml：定义回归测试计划。
- release_and_rollback_plan_schema.yaml：定义发布与回滚计划。
- upgrade_approval_requirement_schema.yaml：定义审批要求。
- controlled_upgrade_package_schema.yaml：定义受控升级包。
- controlled_upgrade_task_packet_schema.yaml：定义 HER / Runner 可执行实现任务包。
- version_change_record_schema.yaml：定义版本变更。
- upgrade_backlog_schema.yaml：定义升级待办队列。
- p10_to_implementation_handoff_contract.yaml：定义 P10_TO_IMPLEMENTATION handoff packet。
- upgrade_classification_policy.yaml：定义升级类型判断规则。
- sample_support_policy.yaml：定义单样本、多样本、安全关键样本处理规则。
- overfit_control_policy.yaml：定义防过拟合规则。
- impact_assessment_policy.yaml：定义影响分析规则。
- compatibility_policy.yaml：定义向后兼容、迁移、breaking change 判断。
- controlled_release_policy.yaml：定义 dry-run、shadow mode、paper-only release 规则。
- rollback_policy.yaml：定义回滚规则。
- approval_policy.yaml：定义人工 / 治理审批规则。
- self_upgrade_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- self_upgrade_hard_negative_rules.yaml：定义无 P09 handoff、无升级候选、单样本全局升级、无影响分析、无回归测试、无回滚、破坏 handoff、自动部署、自动实盘等阻断。
- self_upgrade_state_machine.yaml：定义 P10 全状态机。
- self_upgrade_trace_requirements.yaml：定义 upgrade trace、proposal trace、package trace、task packet trace、handoff trace。
- p10_acceptance_criteria.md：定义 P10_READY、P10_READY_WITH_GAPS、P10_REJECTED、P10_BLOCKED。
- p10_storage_constitution.md：定义系统文件与运行数据目录。
- p10_test_matrix.yaml：定义至少 18 个测试场景。
- p10_report_model.yaml：定义 P10 人类可读报告。
- p10_review_checklist.md：定义审计清单。
- her_p10_execution_protocol.md：定义 HER 执行 P10 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P10_READY / P10_READY_WITH_GAPS / P10_REJECTED / P10_BLOCKED 判断
4. upgrade_input_manifest 摘要
5. upgrade_candidate_review 摘要
6. sample_support_assessment 摘要
7. upgrade_classification 摘要
8. impact_assessment 摘要
9. overfit_risk_assessment 摘要
10. compatibility_assessment 摘要
11. schema / contract upgrade proposal 摘要
12. rule / policy upgrade proposal 摘要
13. parameter_calibration proposal 摘要
14. test_matrix_upgrade 摘要
15. tool_binding_upgrade proposal 摘要
16. runtime_model_upgrade proposal 摘要
17. upgrade_decision 摘要
18. regression_test_plan 摘要
19. release_and_rollback_plan 摘要
20. controlled_upgrade_package 摘要
21. controlled_upgrade_task_packet 摘要
22. version_change_record 摘要
23. p10_to_implementation_handoff_packet 摘要
24. P10 阻断规则摘要
25. P10 测试矩阵摘要
26. 当前缺口清单
27. 是否达到轻量机构级 P10 v3.0

最终验收标准：
只有当 P10 具备 upgrade input manifest、upgrade candidate review、sample support assessment、upgrade classification、impact assessment、overfit risk assessment、compatibility assessment、schema / contract proposal、rule / policy proposal、parameter calibration proposal、test matrix upgrade、tool binding proposal、runtime model upgrade、report explanation upgrade、upgrade decision、regression test plan、release and rollback plan、approval requirement、controlled upgrade package、controlled upgrade task packet、version change、upgrade backlog、P10 implementation handoff、gap policy、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P10 不能直接修改规则、不能自动部署、不能触发 paper runtime、不能允许 live execution 时，才允许标记为 P10_READY。
```

---

# 38. 当前是否达到专业化标准

## 判断

这一版 P10 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是自动改规则模块
不是自动部署模块
```

P10 被明确升级为：

```text
升级候选审查层
样本支持评估层
影响分析层
防过拟合层
兼容性评估层
规则 / 合约 / 参数 / 测试升级提案层
受控升级包层
回归测试层
发布回滚层
实现任务交接层
```

---

# 39. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Upgrade Input Manifest|已补齐|
|Upgrade Candidate Review|已补齐|
|Sample Support Assessment|已补齐|
|Upgrade Classification|已补齐|
|Impact Assessment|已补齐|
|Overfit Risk Assessment|已补齐|
|Compatibility Assessment|已补齐|
|Contract / Schema Upgrade Proposal|已补齐|
|Rule / Policy Upgrade Proposal|已补齐|
|Parameter Calibration Proposal|已补齐|
|Test Matrix Upgrade|已补齐|
|Tool Binding Upgrade Proposal|已补齐|
|Runtime Model Upgrade Proposal|已补齐|
|Report Explanation Upgrade Proposal|已补齐|
|Upgrade Decision|已补齐|
|Regression Test Plan|已补齐|
|Release / Rollback Plan|已补齐|
|Approval Requirement|已补齐|
|Controlled Upgrade Package|已补齐|
|Controlled Upgrade Task Packet|已补齐|
|Version Change Record|已补齐|
|Upgrade Backlog|已补齐|
|P10 Implementation Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 40. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|P10 只生成升级包，不直接落地|已明确边界|后续由 Implementation / Runner / HER 执行|
|样本支持度需要长期积累|已定义 sample support|依赖 P09 Review Case Library|
|阈值校准不能只靠单样本|已设防过拟合|多样本 replay 后再升级|
|breaking change 需要版本迁移|已定义 compatibility / migration|实现任务包处理|
|自动化回归测试 runner 未代码化|已定义 regression plan|Runner / Tool Binding 阶段实现|
|Governance 审批流程未接 Telegram|已定义 approval requirement|后续接 Review Ops / Telegram 面板|
|升级包还没有实际 CI / dry-run 工具|已定义 task packet|Tool Binding 阶段实现|
|不能自动部署|已明确限制|保持受控发布|

---

# 本次认知升级点

1. **P10 的本质不是自动改系统，而是受控升级治理控制器。**
    
2. **P09 提出问题，P10 审查问题。**  
    P09 的 calibration candidate 不能直接变成生产规则。
    
3. **单样本不能直接全局升级。**  
    除非属于安全关键风险，也只能进入临时保护性阻断 + 人工审批 + 回滚计划。
    
4. **升级必须具备影响分析、兼容性评估、回归测试和回滚计划。**
    
5. **防过拟合是 P10 的核心能力。**  
    不能因为一次失败就把系统调得过度保守，也不能因为一次成功就放宽门控。
    
6. **P10 输出的是 Controlled Upgrade Package。**  
    不是直接修改代码、规则或 runner。
    
7. **P10 是 P01-P09 的闭环终点。**  
    它把复盘经验转化为下一轮系统能力，但必须通过治理、测试、版本、回滚来控制风险。
    
8. **P10 之后不应该继续新增业务阶段。**  
    下一步应该进入：  
    `全阶段一致性审计 → 目录与合约索引统一 → Runner / Tool Binding → Paper-only Runtime 联调 → P09/P10 闭环回放`。