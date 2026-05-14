# I01 Full Phase Consistency Audit 专业版 v1.0

## P01-P10 全阶段一致性审计任务包

---

## 0. I01 的核心定位

I01 不是新的业务阶段，也不是 P11。

它属于：

```text
Integration Program：系统集成落地计划
```

I01 的专业定义：

```text
I01 Full Phase Consistency Audit 是 P01-P10 进入 Runner / Tool Binding 之前的全链路一致性审计任务包。
它负责检查 P01-P10 的职责边界、输入输出、handoff、schema、contract、状态码、trace、acceptance、gap、forbidden use、下游权限是否一致，防止错误设计被 Runner 固化成代码。
```

一句话：

> **P01-P10 负责设计业务判断系统。**  
> **I01 负责审计这套业务判断系统是否真的能被串起来、跑起来、验收起来、复盘起来、升级起来。**

---

# 1. I01 不负责什么

I01 禁止做以下事情：

```text
不新增 P11
不修改 P01-P10 业务逻辑
不直接写 Runner
不直接绑定 GMGN / OKX 工具
不直接进入 Paper Runtime
不直接调整策略规则
不直接升级 schema
不自动修复文件
不自动部署
不允许 live execution
```

I01 只做：

```text
审计
发现断点
记录冲突
输出修复优先级
生成 I02 目录与合约索引统一请求
```

---

# 2. I01 阶段目标

I01 必须一次性完成 16 类审计：

|编号|审计对象|必须回答|
|---|---|---|
|1|阶段职责边界|P01-P10 有没有越权、重叠、缺位|
|2|输入输出链|上一阶段输出是否能被下一阶段读取|
|3|Handoff 链|P01→P10 的 handoff 是否连续|
|4|Data Request 链|每个阶段是否明确向下游请求什么|
|5|Schema 链|每个输出对象是否有 schema|
|6|Contract 链|每个输入输出是否有 contract|
|7|状态码链|READY / GAPS / BLOCKED / REJECTED 是否统一|
|8|Gap 传递|上游缺口是否被下游继承|
|9|Forbidden Use 继承|禁止事项是否逐级保留|
|10|Trace 完整性|每个对象、决策、handoff 是否可追踪|
|11|Acceptance 完整性|每个阶段是否有验收标准|
|12|权限边界|哪些阶段能交给谁，不能跳转哪里|
|13|Paper-only 边界|是否严格阻断 live execution|
|14|Runtime 前置条件|P08 是否真的能把候选交给 Paper Runtime|
|15|P09/P10 回放条件|前面阶段是否足够支持复盘与升级|
|16|修复优先级|哪些断点必须先修，哪些可延后|

---

# 3. I01 的输入范围

I01 要读取 P01-P10 已有设计文件与总控索引。

```yaml
i01_required_inputs:
  system_blueprint:
    - system_methodology_blueprint.md
    - professional_build_order.md
    - phase_controller_index.yaml
    - global_status_code_table.md
    - global_hard_negative_rules.md
    - directory_constitution.md
    - contract_index.md
    - schema_index.md
    - her_total_control_execution_protocol.md
    - professional_baseline_acceptance.md

  phase_controllers:
    - P01 Candidate Intake Controller
    - P02 Source Data Fact Controller
    - P03 Wallet Entity Controller
    - P04 Chip Structure Controller
    - P05 Evidence Controller
    - P06 Scenario Recognition Controller
    - P07 Strategy Gate Controller
    - P08 Execution Risk Controller
    - P09 Review Replay Controller
    - P10 Self Upgrade Controller

  required_from_each_phase:
    - controller_yaml
    - context_md
    - input_contract
    - output_contract
    - state_machine
    - hard_negative_rules
    - gap_policy
    - trace_requirements
    - acceptance_criteria
    - handoff_contract
    - data_request_packet_contract
    - test_matrix
    - report_model
    - her_execution_protocol

  integration_context:
    - Bootstrap Control Plane
    - Governance Plane
    - Domain Plane
    - Data Plane
    - Full Control Plane
    - Trace Plane
    - Acceptance Plane
    - Handoff Plane
```

---

# 4. I01 必须建立的审计对象

|对象|作用|
|---|---|
|`I01 Audit Input Manifest`|记录审计读取了哪些文件和阶段|
|`Phase Inventory Record`|P01-P10 阶段清单|
|`Phase Responsibility Boundary Matrix`|阶段职责边界矩阵|
|`Phase IO Alignment Matrix`|输入输出对齐矩阵|
|`Handoff Chain Integrity Record`|Handoff 链完整性|
|`Data Request Chain Record`|Data Request 链完整性|
|`Schema Contract Coverage Record`|Schema / Contract 覆盖情况|
|`Status Code Consistency Record`|状态码一致性|
|`Gap Propagation Record`|Gap 是否正确传递|
|`Forbidden Use Inheritance Record`|禁止事项是否继承|
|`Trace Coverage Record`|Trace 覆盖情况|
|`Acceptance Coverage Record`|Acceptance 覆盖情况|
|`Phase Boundary Violation Record`|阶段越权记录|
|`Downstream Permission Record`|下游权限一致性|
|`Runtime Readiness Precheck Record`|Runtime 前置条件审计|
|`Review Upgrade Readiness Record`|P09/P10 闭环条件审计|
|`Audit Finding Record`|审计发现项|
|`Fix Priority Record`|修复优先级|
|`I01 to I02 Handoff Packet`|交给 I02 的目录与索引统一请求|

---

# 5. I01 运行目录设计

## 5.1 系统目录

```text
/root/sikk-gmgn/system/integration_program/I01_full_phase_consistency_audit/
```

必须创建：

```text
i01_full_phase_consistency_audit_controller.yaml
i01_full_phase_consistency_audit_context.md
i01_input_contract.yaml
i01_output_contract.yaml
i01_audit_input_manifest_schema.yaml
phase_inventory_schema.yaml
phase_responsibility_boundary_matrix_schema.yaml
phase_io_alignment_matrix_schema.yaml
handoff_chain_integrity_schema.yaml
data_request_chain_schema.yaml
schema_contract_coverage_schema.yaml
status_code_consistency_schema.yaml
gap_propagation_schema.yaml
forbidden_use_inheritance_schema.yaml
trace_coverage_schema.yaml
acceptance_coverage_schema.yaml
phase_boundary_violation_schema.yaml
downstream_permission_schema.yaml
runtime_readiness_precheck_schema.yaml
review_upgrade_readiness_schema.yaml
audit_finding_schema.yaml
fix_priority_schema.yaml
i01_to_i02_handoff_contract.yaml
i01_audit_policy.yaml
i01_hard_negative_rules.yaml
i01_state_machine.yaml
i01_trace_requirements.yaml
i01_acceptance_criteria.md
i01_storage_constitution.md
i01_test_matrix.yaml
i01_report_model.yaml
i01_review_checklist.md
her_i01_execution_protocol.md
```

---

## 5.2 运行数据目录

```text
/root/sikk-gmgn/data/integration_program/I01_full_phase_consistency_audit/
  input_manifest/
  phase_inventory/
  responsibility_boundary/
  io_alignment/
  handoff_chain/
  data_request_chain/
  schema_contract_coverage/
  status_code_consistency/
  gap_propagation/
  forbidden_use_inheritance/
  trace_coverage/
  acceptance_coverage/
  boundary_violations/
  downstream_permissions/
  runtime_readiness/
  review_upgrade_readiness/
  findings/
  fix_priority/
  i02_handoff/
  reports/
  audit/
  trace/
  acceptance/
```

---

# 6. I01 核心审计模型

## 6.1 Phase Inventory Record

```yaml
phase_inventory_record:
  inventory_id: string
  generated_at: datetime

  phases:
    - phase_id: P01
      phase_name: Candidate Intake Controller
      expected_role: 候选接收与候选主档建立
      system_dir: string
      data_dir: string
      controller_file_exists: boolean
      input_contract_exists: boolean
      output_contract_exists: boolean
      handoff_contract_exists: boolean
      state_machine_exists: boolean
      acceptance_criteria_exists: boolean
      trace_requirements_exists: boolean

    - phase_id: P02
      phase_name: Source Data Fact Controller
      expected_role: 数据事实采集、标准化、质量检查

    - phase_id: P03
      phase_name: Wallet Entity Controller
      expected_role: 钱包实体、地址归并、角色候选

    - phase_id: P04
      phase_name: Chip Structure Controller
      expected_role: 筹码结构、留存、迁移、对手盘压力

    - phase_id: P05
      phase_name: Evidence Controller
      expected_role: 证据对象、反证、冲突、未知证据

    - phase_id: P06
      phase_name: Scenario Recognition Controller
      expected_role: 场景候选、冲突场景、失效条件

    - phase_id: P07
      phase_name: Strategy Gate Controller
      expected_role: 策略门控、观察、暂停、阻断、纸面候选

    - phase_id: P08
      phase_name: Execution Risk Controller
      expected_role: 执行前风控、纸面运行许可

    - phase_id: P09
      phase_name: Review Replay Controller
      expected_role: 复盘回放、失败归因、校准候选

    - phase_id: P10
      phase_name: Self Upgrade Controller
      expected_role: 受控升级审查、升级包、回滚计划

  inventory_status:
    - INVENTORY_COMPLETE
    - INVENTORY_WITH_GAPS
    - INVENTORY_INCOMPLETE
    - INVENTORY_UNUSABLE
```

---

## 6.2 Phase Responsibility Boundary Matrix

```yaml
phase_responsibility_boundary_matrix:
  matrix_id: string

  boundary_checks:
    P01:
      allowed:
        - candidate_master_record
        - discovery_context_record
        - p02_data_request_packet
      forbidden:
        - wallet_entity_judgment
        - chip_structure_judgment
        - strategy_signal
        - paper_runtime

    P02:
      allowed:
        - source_data_fact
        - normalized_fact
        - data_quality
        - security_fact_seed
      forbidden:
        - wallet_role_confirmation
        - chip_control_claim
        - evidence_object
        - scenario_claim
        - strategy_gate

    P03:
      allowed:
        - wallet_entity_candidate
        - same_source_candidate
        - wallet_role_candidate
      forbidden:
        - confirmed_market_maker
        - chip_control_status
        - evidence
        - scenario
        - strategy_signal

    P04:
      allowed:
        - chip_retention_status
        - distribution_progress_candidate
        - counterparty_pressure_status
      forbidden:
        - evidence_object
        - scenario_claim
        - strategy_gate
        - runtime

    P05:
      allowed:
        - evidence_object
        - counter_evidence
        - unknown_evidence
        - evidence_bundle
      forbidden:
        - scenario_claim
        - strategy_signal
        - runtime

    P06:
      allowed:
        - scenario_candidate
        - scenario_conflict
        - invalidation_condition
        - risk_flag
      forbidden:
        - strategy_decision
        - paper_ready
        - runtime

    P07:
      allowed:
        - OBSERVE
        - PAUSE
        - BLOCK
        - PAPER_CANDIDATE
        - HUMAN_CONFIRMATION_REQUIRED
      forbidden:
        - paper_runtime_started
        - live_execution
        - wallet_signing

    P08:
      allowed:
        - PAPER_RUNTIME_ALLOWED
        - PAPER_RUNTIME_BLOCKED
        - execution_risk_decision
      forbidden:
        - live_execution_allowed
        - wallet_signing
        - real_order

    P09:
      allowed:
        - review_case
        - failure_attribution
        - calibration_candidate
        - p10_upgrade_request
      forbidden:
        - direct_rule_mutation
        - runtime_mutation
        - deployment

    P10:
      allowed:
        - controlled_upgrade_package
        - regression_test_plan
        - rollback_plan
        - implementation_task_packet
      forbidden:
        - auto_deploy
        - direct_production_mutation
        - live_execution

  output:
    boundary_violation_count: integer
    boundary_violation_records_path: string
```

---

# 7. 输入输出链审计

## 7.1 Phase IO Alignment Matrix

```yaml
phase_io_alignment_matrix:
  matrix_id: string
  generated_at: datetime

  links:
    - link_id: P01_TO_P02
      upstream_phase: P01
      downstream_phase: P02
      required_upstream_outputs:
        - candidate_master_records
        - discovery_context_records
        - p02_source_data_request_packet
        - p01_to_p02_handoff_packet
      required_downstream_inputs:
        - p01_to_p02_handoff_packet
        - candidate_master_records
        - discovery_context_records
      alignment_status:
        - ALIGNED
        - ALIGNED_WITH_GAPS
        - FIELD_MISMATCH
        - MISSING_OUTPUT
        - MISSING_INPUT
        - BROKEN

    - link_id: P02_TO_P03
      required_upstream_outputs:
        - wallet_fact_seed_records
        - holder_snapshot_fact
        - transaction_fact_seed
        - p03_wallet_entity_data_request_packet
        - p02_to_p03_handoff_packet
      required_downstream_inputs:
        - p02_to_p03_handoff_packet
        - wallet_fact_seed_records
        - holder_snapshot_fact
        - transaction_fact_seed

    - link_id: P03_TO_P04
      required_upstream_outputs:
        - wallet_entity_master_records
        - wallet_position_fact_records
        - same_source_group_candidates
        - sync_behavior_group_candidates
        - wallet_role_candidate_records
        - p04_chip_structure_data_request_packet
        - p03_to_p04_handoff_packet

    - link_id: P04_TO_P05
      required_upstream_outputs:
        - early_wallet_retention_records
        - structural_group_holding_records
        - chip_transfer_status_records
        - distribution_progress_records
        - counterparty_pressure_records
        - p05_evidence_data_request_packet
        - p04_to_p05_handoff_packet

    - link_id: P05_TO_P06
      required_upstream_outputs:
        - evidence_bundle_records
        - counter_evidence_records
        - unknown_evidence_records
        - evidence_conflict_records
        - p06_scenario_data_request_packet
        - p05_to_p06_handoff_packet

    - link_id: P06_TO_P07
      required_upstream_outputs:
        - primary_scenario_candidate_records
        - secondary_scenario_candidate_records
        - scenario_conflict_records
        - scenario_invalidation_records
        - scenario_risk_flag_records
        - p07_strategy_gate_data_request_packet
        - p06_to_p07_handoff_packet

    - link_id: P07_TO_P08
      required_upstream_outputs:
        - strategy_gate_decision_records
        - strategy_candidate_records
        - strategy_usage_permission_records
        - strategy_invalidation_binding_records
        - p08_execution_risk_data_request_packet
        - p07_to_p08_handoff_packet

    - link_id: P08_TO_PAPER_RUNTIME
      required_upstream_outputs:
        - paper_runtime_permission_records
        - paper_entry_simulation_plans
        - paper_runtime_data_request_packet
        - p08_to_paper_runtime_handoff_packet

    - link_id: PAPER_RUNTIME_TO_P09
      required_upstream_outputs:
        - paper_positions_open
        - paper_positions_closed
        - paper_trades
        - paper_equity_curve
        - paper_runtime_trace
        - risk_events

    - link_id: P09_TO_P10
      required_upstream_outputs:
        - failure_attribution_records
        - success_attribution_records
        - calibration_candidate_records
        - missed_negative_rule_records
        - p10_upgrade_candidate_data_request_packet
        - p09_to_p10_handoff_packet

  matrix_result:
    aligned_links_count: integer
    gap_links_count: integer
    broken_links_count: integer
    critical_broken_links: list
```

---

# 8. Handoff 链审计

## 8.1 Handoff Chain Integrity Record

```yaml
handoff_chain_integrity_record:
  record_id: string
  generated_at: datetime

  handoff_chain:
    - handoff_id: p01_to_p02_handoff_packet
      expected_exists: true
      upstream: P01
      downstream: P02
      has_route: boolean
      has_scope: boolean
      has_package_paths: boolean
      has_limitations: boolean
      has_downstream_permission: boolean
      has_read_instruction: boolean
      has_trace_id: boolean
      status:
        - VALID
        - VALID_WITH_GAPS
        - MISSING
        - INVALID

    - handoff_id: p02_to_p03_handoff_packet
    - handoff_id: p03_to_p04_handoff_packet
    - handoff_id: p04_to_p05_handoff_packet
    - handoff_id: p05_to_p06_handoff_packet
    - handoff_id: p06_to_p07_handoff_packet
    - handoff_id: p07_to_p08_handoff_packet
    - handoff_id: p08_to_paper_runtime_handoff_packet
    - handoff_id: p09_to_p10_handoff_packet
    - handoff_id: p10_to_implementation_handoff_packet

  chain_checks:
    no_stage_skipped: boolean
    no_unauthorized_jump: boolean
    limitations_preserved: boolean
    downstream_permissions_preserved: boolean
    forbidden_uses_preserved: boolean
    trace_chain_complete: boolean

  result:
    handoff_chain_status:
      - HANDOFF_CHAIN_COMPLETE
      - HANDOFF_CHAIN_WITH_GAPS
      - HANDOFF_CHAIN_BROKEN
      - HANDOFF_CHAIN_UNUSABLE
```

---

# 9. Data Request 链审计

## 9.1 Data Request Chain Record

```yaml
data_request_chain_record:
  record_id: string

  data_request_packets:
    - packet_id: p02_source_data_request_packet
      from_phase: P01
      to_phase: P02
      exists: boolean
      requested_outputs_clear: boolean

    - packet_id: p03_wallet_entity_data_request_packet
      from_phase: P02
      to_phase: P03

    - packet_id: p04_chip_structure_data_request_packet
      from_phase: P03
      to_phase: P04

    - packet_id: p05_evidence_data_request_packet
      from_phase: P04
      to_phase: P05

    - packet_id: p06_scenario_data_request_packet
      from_phase: P05
      to_phase: P06

    - packet_id: p07_strategy_gate_data_request_packet
      from_phase: P06
      to_phase: P07

    - packet_id: p08_execution_risk_data_request_packet
      from_phase: P07
      to_phase: P08

    - packet_id: paper_runtime_data_request_packet
      from_phase: P08
      to_phase: PAPER_ONLY_RUNTIME

    - packet_id: p10_upgrade_candidate_data_request_packet
      from_phase: P09
      to_phase: P10

  request_chain_status:
    - DATA_REQUEST_CHAIN_COMPLETE
    - DATA_REQUEST_CHAIN_WITH_GAPS
    - DATA_REQUEST_CHAIN_BROKEN
```

---

# 10. Schema / Contract 覆盖审计

## 10.1 Schema Contract Coverage Record

```yaml
schema_contract_coverage_record:
  record_id: string

  per_phase_coverage:
    - phase_id: P01
      required_schemas: list
      existing_schemas: list
      missing_schemas: list
      required_contracts: list
      existing_contracts: list
      missing_contracts: list
      coverage_score: number
      coverage_status:
        - COMPLETE
        - WITH_GAPS
        - INCOMPLETE
        - UNUSABLE

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  global_coverage:
    total_required_schemas: integer
    total_existing_schemas: integer
    total_missing_schemas: integer
    total_required_contracts: integer
    total_existing_contracts: integer
    total_missing_contracts: integer

  critical_missing:
    - missing_item: string
      phase_id: string
      severity:
        - BLOCKING
        - HIGH
        - MEDIUM
        - LOW
      reason_cn: string
```

---

# 11. 状态码一致性审计

## 11.1 Status Code Consistency Record

```yaml
status_code_consistency_record:
  record_id: string

  global_status_classes:
    - READY
    - READY_WITH_GAPS
    - REJECTED
    - BLOCKED
    - PAUSED
    - OBSERVE
    - ALLOWED
    - ALLOWED_WITH_LIMITATIONS

  per_phase_status_check:
    - phase_id: P01
      declared_statuses: list
      unmapped_statuses: list
      conflicting_statuses: list
      status_consistency:
        - CONSISTENT
        - CONSISTENT_WITH_GAPS
        - INCONSISTENT
        - UNMAPPED

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  status_mapping_required:
    - local_status: string
      global_status_class: string
      phase_id: string
      action:
        - KEEP
        - MAP
        - RENAME
        - DEPRECATE
```

---

# 12. Gap 传递审计

## 12.1 Gap Propagation Record

```yaml
gap_propagation_record:
  record_id: string

  gap_classes:
    - BLOCKING_GAP
    - CRITICAL_GAP
    - HIGH_GAP
    - MEDIUM_GAP
    - LOW_GAP

  propagation_checks:
    - source_phase: P02
      downstream_phase: P03
      inherited_gap_tags_preserved: boolean
      weak_use_only_fields_preserved: boolean
      do_not_use_fields_preserved: boolean
      gap_downgrade_without_reason: boolean

    - source_phase: P03
      downstream_phase: P04

    - source_phase: P04
      downstream_phase: P05

    - source_phase: P05
      downstream_phase: P06

    - source_phase: P06
      downstream_phase: P07

    - source_phase: P07
      downstream_phase: P08

    - source_phase: P08
      downstream_phase: PAPER_ONLY_RUNTIME

    - source_phase: P09
      downstream_phase: P10

  violations:
    - violation_id: string
      source_phase: string
      downstream_phase: string
      gap_tag: string
      violation_type:
        - GAP_DROPPED
        - WEAK_USE_UPGRADED
        - DO_NOT_USE_IGNORED
        - BLOCKED_ITEM_USED_DOWNSTREAM
      severity: string
```

---

# 13. Forbidden Use 继承审计

## 13.1 Forbidden Use Inheritance Record

```yaml
forbidden_use_inheritance_record:
  record_id: string

  global_forbidden_uses:
    - LIVE_EXECUTION
    - WALLET_SIGNING
    - AUTO_ORDER
    - BYPASS_HANDOFF
    - BYPASS_ACCEPTANCE
    - BYPASS_TRACE
    - DIRECT_PAPER_RUNTIME_BEFORE_P08
    - DIRECT_RULE_MUTATION_BEFORE_P10
    - AUTO_DEPLOY

  inheritance_checks:
    - phase_id: P01
      forbiddens_declared: list
      missing_global_forbiddens: list
      inheritance_status:
        - COMPLETE
        - WITH_GAPS
        - BROKEN

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  critical_violations:
    - phase_id: string
      missing_forbidden_use: string
      severity: HARD_BLOCK
      reason_cn: string
```

---

# 14. Trace / Acceptance 覆盖审计

## 14.1 Trace Coverage Record

```yaml
trace_coverage_record:
  record_id: string

  required_trace_types:
    - source_trace
    - field_trace
    - decision_trace
    - handoff_trace
    - acceptance_trace
    - runtime_trace
    - review_trace
    - upgrade_trace

  per_phase_trace_coverage:
    - phase_id: P01
      required_trace_types: list
      declared_trace_types: list
      missing_trace_types: list
      trace_coverage_status:
        - TRACE_COMPLETE
        - TRACE_WITH_GAPS
        - TRACE_INCOMPLETE
        - TRACE_UNUSABLE

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  critical_trace_gaps:
    - phase_id: string
      missing_trace_type: string
      downstream_risk_cn: string
```

---

## 14.2 Acceptance Coverage Record

```yaml
acceptance_coverage_record:
  record_id: string

  per_phase_acceptance:
    - phase_id: P01
      acceptance_criteria_exists: boolean
      ready_defined: boolean
      ready_with_gaps_defined: boolean
      rejected_defined: boolean
      blocked_defined: boolean
      hard_negative_integrated: boolean
      test_matrix_linked: boolean
      acceptance_status:
        - ACCEPTANCE_COMPLETE
        - ACCEPTANCE_WITH_GAPS
        - ACCEPTANCE_INCOMPLETE
        - ACCEPTANCE_UNUSABLE

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10
```

---

# 15. 阶段越权审计

## 15.1 Phase Boundary Violation Record

```yaml
phase_boundary_violation_record:
  violation_id: string
  detected_at: datetime

  phase_id: string
  violation_type:
    - OUTPUTS_DOWNSTREAM_DECISION
    - SKIPS_REQUIRED_PHASE
    - CONFIRMS_CANDIDATE_WHEN_ONLY_CANDIDATE_ALLOWED
    - GENERATES_STRATEGY_TOO_EARLY
    - ENTERS_RUNTIME_TOO_EARLY
    - MUTATES_RULES_TOO_EARLY
    - LIVE_EXECUTION_PATH
    - HANDOFF_BYPASS

  example_output_or_claim: string
  expected_boundary_cn: string
  severity:
    - HARD_BLOCK
    - HIGH
    - MEDIUM
    - LOW

  required_fix:
    fix_type:
      - REMOVE_OUTPUT
      - MOVE_TO_DOWNSTREAM_PHASE
      - ADD_LIMITATION
      - ADD_FORBIDDEN_USE
      - MODIFY_HANDOFF
      - MODIFY_ACCEPTANCE
      - MODIFY_TEST_MATRIX
```

---

# 16. Runtime Readiness 审计

## 16.1 Runtime Readiness Precheck Record

```yaml
runtime_readiness_precheck_record:
  record_id: string

  checks:
    p07_outputs_paper_candidate_not_paper_ready: boolean
    p08_receives_only_paper_candidate: boolean
    p08_generates_paper_runtime_permission: boolean
    p08_generates_paper_runtime_data_request: boolean
    p08_to_paper_runtime_handoff_defined: boolean
    paper_runtime_required_inputs_defined: boolean
    live_execution_forbidden_preserved: boolean
    wallet_signing_forbidden_preserved: boolean

  readiness_status:
    - RUNTIME_INTEGRATION_READY
    - RUNTIME_INTEGRATION_READY_WITH_GAPS
    - RUNTIME_INTEGRATION_NOT_READY
    - RUNTIME_INTEGRATION_BLOCKED

  gaps:
    - missing_item: string
      severity: string
      required_before_i04: boolean
```

---

# 17. P09/P10 闭环就绪审计

## 17.1 Review Upgrade Readiness Record

```yaml
review_upgrade_readiness_record:
  record_id: string

  p09_readiness_checks:
    paper_runtime_outputs_available_as_contract: boolean
    p08_records_traceable: boolean
    p07_decision_traceable: boolean
    p06_scenario_traceable: boolean
    p05_evidence_traceable: boolean
    p04_chip_traceable: boolean
    p03_wallet_traceable: boolean
    p02_fact_traceable: boolean
    p01_candidate_traceable: boolean
    decision_time_snapshot_policy_defined: boolean

  p10_readiness_checks:
    p09_generates_calibration_candidates: boolean
    p09_generates_missed_negative_rules: boolean
    p09_generates_new_test_cases: boolean
    p10_reviews_candidates_before_change: boolean
    p10_generates_regression_plan: boolean
    p10_generates_rollback_plan: boolean
    p10_blocks_auto_deploy: boolean

  readiness_status:
    - REVIEW_UPGRADE_LOOP_READY
    - REVIEW_UPGRADE_LOOP_READY_WITH_GAPS
    - REVIEW_UPGRADE_LOOP_NOT_READY
    - REVIEW_UPGRADE_LOOP_BLOCKED
```

---

# 18. Audit Finding Record

```yaml
audit_finding_record:
  finding_id: string
  generated_at: datetime

  finding_scope:
    affected_phase: string
    affected_link: string | null
    affected_artifact: string | null

  finding_type:
    - MISSING_FILE
    - MISSING_SCHEMA
    - MISSING_CONTRACT
    - IO_MISMATCH
    - HANDOFF_GAP
    - STATUS_CODE_CONFLICT
    - GAP_PROPAGATION_FAILURE
    - FORBIDDEN_USE_MISSING
    - TRACE_GAP
    - ACCEPTANCE_GAP
    - BOUNDARY_VIOLATION
    - RUNTIME_READINESS_GAP
    - REVIEW_LOOP_GAP

  severity:
    - BLOCKING
    - CRITICAL
    - HIGH
    - MEDIUM
    - LOW

  finding_summary_cn: string
  evidence:
    source_files: list
    source_sections: list
    observed_issue_cn: string

  recommended_fix:
    fix_summary_cn: string
    target_i_stage:
      - I02_DIRECTORY_CONTRACT_INDEX_UNIFICATION
      - I03_RUNNER_TOOL_BINDING
      - I04_PAPER_RUNTIME_INTEGRATION
      - I05_REVIEW_UPGRADE_CLOSED_LOOP
      - P01_P10_DESIGN_PATCH
    priority:
      - FIX_BEFORE_I02
      - FIX_IN_I02
      - FIX_BEFORE_I03
      - FIX_IN_I03
      - FIX_BEFORE_I04
      - FIX_BEFORE_I05
      - DEFER
```

---

# 19. Fix Priority Record

```yaml
fix_priority_record:
  priority_id: string
  generated_at: datetime

  priority_groups:
    must_fix_before_i02:
      - finding_id: string
        reason_cn: string

    fix_in_i02:
      - finding_id: string
        reason_cn: string

    must_fix_before_i03:
      - finding_id: string
        reason_cn: string

    fix_in_i03:
      - finding_id: string
        reason_cn: string

    must_fix_before_i04:
      - finding_id: string
        reason_cn: string

    must_fix_before_i05:
      - finding_id: string
        reason_cn: string

    deferred:
      - finding_id: string
        reason_cn: string

  blocking_summary:
    has_blocking_findings: boolean
    can_enter_i02: boolean
    can_enter_i03: boolean
    can_enter_i04: boolean
    can_enter_i05: boolean
```

---

# 20. I01 输出文件清单

I01 完成后必须输出：

```text
full_phase_consistency_audit_report.md
phase_inventory.yaml
phase_responsibility_boundary_matrix.yaml
phase_io_alignment_matrix.yaml
handoff_chain_integrity_report.yaml
data_request_chain_report.yaml
schema_contract_coverage_report.yaml
status_code_consistency_report.yaml
gap_propagation_report.yaml
forbidden_use_inheritance_report.yaml
trace_coverage_report.yaml
acceptance_coverage_report.yaml
phase_boundary_violation_report.yaml
downstream_permission_report.yaml
runtime_readiness_precheck_report.yaml
review_upgrade_readiness_report.yaml
audit_findings.yaml
fix_priority_list.yaml
i01_to_i02_handoff_packet.yaml
i01_acceptance_result.yaml
```

---

# 21. I01 to I02 Handoff Packet

```yaml
i01_to_i02_handoff_packet:
  packet_id: string
  packet_type: I01_TO_I02_CONSISTENCY_AUDIT_HANDOFF
  generated_at: datetime

  route:
    from: I01_FULL_PHASE_CONSISTENCY_AUDIT
    to: I02_DIRECTORY_CONTRACT_INDEX_UNIFICATION

  audit_scope:
    audited_phases:
      - P01
      - P02
      - P03
      - P04
      - P05
      - P06
      - P07
      - P08
      - P09
      - P10

  audit_outputs:
    phase_inventory_path: string
    phase_io_alignment_matrix_path: string
    handoff_chain_integrity_report_path: string
    schema_contract_coverage_report_path: string
    status_code_consistency_report_path: string
    gap_propagation_report_path: string
    forbidden_use_inheritance_report_path: string
    trace_coverage_report_path: string
    acceptance_coverage_report_path: string
    phase_boundary_violation_report_path: string
    fix_priority_list_path: string

  i02_required_tasks:
    - create_final_directory_constitution
    - create_contract_index
    - create_schema_index
    - create_handoff_contract_index
    - create_phase_controller_file_index
    - create_runtime_data_path_index
    - create_legacy_path_mapping
    - create_canonical_path_policy
    - resolve_missing_contract_paths
    - resolve_schema_index_gaps
    - standardize_phase_file_names
    - preserve_legacy_runtime_keep_in_place

  blocking_findings:
    has_blocking_findings: boolean
    blocking_finding_ids: list

  permission_to_enter_i02:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I01_AUDIT_ONLY
    - I02_MAY_INDEX_AND_STANDARDIZE
    - I02_MUST_NOT_CHANGE_BUSINESS_LOGIC
    - NO_RUNNER_BINDING_YET
    - NO_PAPER_RUNTIME
    - NO_LIVE_EXECUTION
```

---

# 22. I01 Gap Policy

```yaml
i01_gap_policy:
  BLOCKING_GAP:
    result: I01_BLOCKED
    examples:
      - phase_controller_index_missing
      - p01_to_p10_not_defined
      - no_handoff_concept
      - live_execution_allowed_in_any_phase
      - p07_or_p08_runtime_boundary_broken

  CRITICAL_GAP:
    result: I01_REJECTED_OR_FIX_REQUIRED
    examples:
      - missing_p03_to_p04_handoff
      - missing_p04_to_p05_handoff
      - missing_p07_to_p08_handoff
      - missing_p08_to_paper_runtime_handoff
      - p09_cannot_read_runtime_outputs
      - p10_allows_direct_rule_mutation

  HIGH_GAP:
    result: I01_READY_WITH_GAPS
    examples:
      - schema_contract_missing_for_noncritical_objects
      - status_code_inconsistent
      - gap_propagation_incomplete
      - trace_coverage_partial
      - acceptance_criteria_incomplete

  MEDIUM_GAP:
    result: I01_READY_WITH_GAPS
    examples:
      - report_model_incomplete
      - optional_test_matrix_missing
      - directory_path_not_canonical
      - legacy_path_mapping_missing

  LOW_GAP:
    result: I01_READY_WITH_NOTE
    examples:
      - naming_inconsistency
      - optional_metadata_missing
      - noncritical_document_format_gap
```

---

# 23. I01 Hard Negative Rules

```yaml
i01_hard_negative_rules:
  - rule_id: I01_BLOCK_001
    name: P01-P10 阶段索引缺失
    condition: phase_controller_index_missing == true
    result: I01_BLOCKED
    reason: 无阶段索引无法做全阶段一致性审计

  - rule_id: I01_BLOCK_002
    name: 任一阶段允许 live execution
    condition: any_phase_live_execution_allowed == true
    result: I01_BLOCKED
    reason: 当前体系为 paper-only 验证阶段，live execution 必须全局阻断

  - rule_id: I01_BLOCK_003
    name: P07 直接启动 Paper Runtime
    condition: p07_outputs_paper_runtime_allowed_or_started == true
    result: I01_BLOCKED
    reason: P07 只能输出 PAPER_CANDIDATE，必须经过 P08

  - rule_id: I01_BLOCK_004
    name: P08 允许 wallet signing
    condition: p08_wallet_signing_allowed == true
    result: I01_BLOCKED
    reason: P08 只能允许 Paper Runtime，不能签名或实盘

  - rule_id: I01_BLOCK_005
    name: P09 直接修改规则
    condition: p09_direct_rule_mutation_allowed == true
    result: I01_BLOCKED
    reason: P09 只能提出升级候选

  - rule_id: I01_BLOCK_006
    name: P10 自动部署
    condition: p10_auto_deploy_allowed == true
    result: I01_BLOCKED
    reason: P10 必须受控升级，不能自动部署

  - rule_id: I01_BLOCK_007
    name: Handoff 链断裂
    condition: critical_handoff_missing == true
    result: I01_BLOCKED
    reason: 无关键 handoff，无法进入 Runner / Tool Binding

  - rule_id: I01_BLOCK_008
    name: Trace 链不可复盘
    condition: trace_chain_unusable == true
    result: I01_BLOCKED
    reason: 无 trace 无法支持 P09 复盘和 P10 升级
```

---

# 24. I01 状态机

```yaml
i01_full_phase_consistency_audit_state_machine:
  states:
    - I01_UNINITIALIZED
    - I01_CONTEXT_LOADED
    - I01_INPUT_MANIFEST_BUILT
    - I01_PHASE_INVENTORY_BUILT
    - I01_RESPONSIBILITY_BOUNDARY_AUDITED
    - I01_IO_ALIGNMENT_AUDITED
    - I01_HANDOFF_CHAIN_AUDITED
    - I01_DATA_REQUEST_CHAIN_AUDITED
    - I01_SCHEMA_CONTRACT_COVERAGE_AUDITED
    - I01_STATUS_CODE_CONSISTENCY_AUDITED
    - I01_GAP_PROPAGATION_AUDITED
    - I01_FORBIDDEN_USE_INHERITANCE_AUDITED
    - I01_TRACE_COVERAGE_AUDITED
    - I01_ACCEPTANCE_COVERAGE_AUDITED
    - I01_PHASE_BOUNDARY_VIOLATIONS_AUDITED
    - I01_DOWNSTREAM_PERMISSION_AUDITED
    - I01_RUNTIME_READINESS_AUDITED
    - I01_REVIEW_UPGRADE_READINESS_AUDITED
    - I01_FINDINGS_BUILT
    - I01_FIX_PRIORITY_BUILT
    - I01_REPORT_BUILT
    - I01_I02_HANDOFF_BUILT
    - I01_READY_FOR_ACCEPTANCE
    - I01_ACCEPTANCE_READY
    - I01_READY_FOR_I02_HANDOFF
    - I01_READY_WITH_GAPS
    - I01_REJECTED
    - I01_BLOCKED

  critical_transitions:
    - from: I01_CONTEXT_LOADED
      to: I01_INPUT_MANIFEST_BUILT
      condition: required_system_blueprint_files_available == true

    - from: I01_INPUT_MANIFEST_BUILT
      to: I01_PHASE_INVENTORY_BUILT
      condition: p01_to_p10_phase_list_available == true

    - from: I01_PHASE_INVENTORY_BUILT
      to: I01_RESPONSIBILITY_BOUNDARY_AUDITED
      condition: phase_responsibility_matrix_created == true

    - from: I01_RESPONSIBILITY_BOUNDARY_AUDITED
      to: I01_IO_ALIGNMENT_AUDITED
      condition: phase_io_alignment_matrix_created == true

    - from: I01_IO_ALIGNMENT_AUDITED
      to: I01_HANDOFF_CHAIN_AUDITED
      condition: handoff_chain_integrity_record_created == true

    - from: I01_HANDOFF_CHAIN_AUDITED
      to: I01_SCHEMA_CONTRACT_COVERAGE_AUDITED
      condition: schema_contract_coverage_record_created == true

    - from: I01_SCHEMA_CONTRACT_COVERAGE_AUDITED
      to: I01_STATUS_CODE_CONSISTENCY_AUDITED
      condition: status_code_consistency_record_created == true

    - from: I01_STATUS_CODE_CONSISTENCY_AUDITED
      to: I01_GAP_PROPAGATION_AUDITED
      condition: gap_propagation_record_created == true

    - from: I01_GAP_PROPAGATION_AUDITED
      to: I01_FORBIDDEN_USE_INHERITANCE_AUDITED
      condition: forbidden_use_inheritance_record_created == true

    - from: I01_FORBIDDEN_USE_INHERITANCE_AUDITED
      to: I01_TRACE_COVERAGE_AUDITED
      condition: trace_coverage_record_created == true

    - from: I01_TRACE_COVERAGE_AUDITED
      to: I01_ACCEPTANCE_COVERAGE_AUDITED
      condition: acceptance_coverage_record_created == true

    - from: I01_ACCEPTANCE_COVERAGE_AUDITED
      to: I01_RUNTIME_READINESS_AUDITED
      condition: runtime_readiness_precheck_record_created == true

    - from: I01_RUNTIME_READINESS_AUDITED
      to: I01_REVIEW_UPGRADE_READINESS_AUDITED
      condition: review_upgrade_readiness_record_created == true

    - from: I01_REVIEW_UPGRADE_READINESS_AUDITED
      to: I01_FINDINGS_BUILT
      condition: audit_findings_created == true

    - from: I01_FINDINGS_BUILT
      to: I01_FIX_PRIORITY_BUILT
      condition: fix_priority_list_created == true

    - from: I01_FIX_PRIORITY_BUILT
      to: I01_I02_HANDOFF_BUILT
      condition: i01_to_i02_handoff_packet_created == true

    - from: I01_I02_HANDOFF_BUILT
      to: I01_READY_FOR_ACCEPTANCE
      condition: full_phase_consistency_audit_report_created == true
```

---

# 25. I01 Acceptance Criteria

```yaml
i01_acceptance_criteria:
  I01_READY:
    required:
      - phase_inventory_complete
      - responsibility_boundary_audited
      - io_alignment_matrix_complete
      - handoff_chain_integrity_checked
      - data_request_chain_checked
      - schema_contract_coverage_checked
      - status_code_consistency_checked
      - gap_propagation_checked
      - forbidden_use_inheritance_checked
      - trace_coverage_checked
      - acceptance_coverage_checked
      - runtime_readiness_checked
      - review_upgrade_readiness_checked
      - findings_created
      - fix_priority_created
      - i01_to_i02_handoff_created
      - no_blocking_gap
      - no_live_execution_path

  I01_READY_WITH_GAPS:
    allowed_when:
      - noncritical_schema_missing
      - report_model_incomplete
      - optional_test_matrix_gap
      - directory_path_needs_i02_standardization
    required:
      - gaps_are_recorded
      - fix_priority_created
      - i02_handoff_allowed_with_gaps

  I01_REJECTED:
    triggered_by:
      - critical_phase_missing
      - critical_handoff_missing
      - schema_contract_chain_unusable
      - review_loop_unreplayable

  I01_BLOCKED:
    triggered_by:
      - live_execution_allowed
      - wallet_signing_allowed
      - p07_bypasses_p08
      - p09_direct_rule_mutation
      - p10_auto_deploy
      - trace_chain_unusable
```

---

# 26. I01 测试矩阵

```yaml
i01_test_matrix:
  - test_id: I01_TEST_001
    name: P01-P10 文件齐全，handoff 连续
    expected_status: I01_READY

  - test_id: I01_TEST_002
    name: phase_controller_index 缺失
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_003
    name: P03_to_P04 handoff 缺失
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_004
    name: P07 输出 PAPER_READY 而不是 PAPER_CANDIDATE
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_005
    name: P08 输出 live_execution_allowed
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_006
    name: P09 可直接修改规则
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_007
    name: P10 缺回滚计划但允许发布
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_008
    name: 状态码命名不一致但可映射
    expected_status: I01_READY_WITH_GAPS

  - test_id: I01_TEST_009
    name: schema 存在但 contract_index 未登记
    expected_status: I01_READY_WITH_GAPS
    next_step: I02_FIX_INDEX

  - test_id: I01_TEST_010
    name: weak_use_only 在下游被升级为 full_use
    expected_status: I01_BLOCKED_OR_HIGH_GAP

  - test_id: I01_TEST_011
    name: P05 evidence 缺 counter_evidence 检查
    expected_status: I01_READY_WITH_GAPS_OR_BLOCKED_DEPENDING_SEVERITY

  - test_id: I01_TEST_012
    name: P08_to_Paper_Runtime handoff 定义存在，但 Paper Runtime input contract 缺失
    expected_status: I01_READY_WITH_GAPS
    next_step: I04_REQUIRED

  - test_id: I01_TEST_013
    name: P10 implementation handoff 存在，但 auto_deploy 未阻断
    expected_status: I01_BLOCKED

  - test_id: I01_TEST_014
    name: Trace requirements 缺部分 object trace
    expected_status: I01_READY_WITH_GAPS

  - test_id: I01_TEST_015
    name: P09 无法读取 P08 quote snapshot
    expected_status: I01_READY_WITH_GAPS
    next_step: I03_OR_I04_FIX

  - test_id: I01_TEST_016
    name: 所有阶段禁止 live execution 且 handoff 连续
    expected_status: I01_READY
```

---

# 27. I01 报告模型

```yaml
i01_full_phase_consistency_audit_report:
  report_id: string
  generated_at: datetime
  controller_id: I01_FULL_PHASE_CONSISTENCY_AUDIT

  summary:
    audited_phase_count: integer
    audited_link_count: integer
    ready_status: string
    blocking_findings_count: integer
    critical_findings_count: integer
    high_findings_count: integer
    medium_findings_count: integer
    low_findings_count: integer

  phase_inventory_summary:
    complete_phase_count: integer
    phase_with_gaps_count: integer
    missing_phase_count: integer

  io_alignment_summary:
    aligned_link_count: integer
    aligned_with_gaps_count: integer
    broken_link_count: integer
    critical_broken_links: list

  handoff_summary:
    valid_handoff_count: integer
    missing_handoff_count: integer
    invalid_handoff_count: integer

  schema_contract_summary:
    total_required_schemas: integer
    missing_schemas: list
    total_required_contracts: integer
    missing_contracts: list

  status_code_summary:
    consistent_phase_count: integer
    inconsistent_phase_count: integer
    unmapped_statuses: list

  gap_forbidden_trace_summary:
    gap_propagation_failures: integer
    forbidden_use_missing_count: integer
    trace_gaps_count: integer

  boundary_violation_summary:
    hard_boundary_violations: integer
    high_boundary_violations: integer
    examples: list

  runtime_readiness_summary:
    runtime_readiness_status: string
    paper_runtime_prerequisites_missing: list
    live_execution_path_detected: boolean

  review_upgrade_readiness_summary:
    p09_readiness_status: string
    p10_readiness_status: string
    review_loop_gaps: list

  fix_priority_summary:
    must_fix_before_i02: list
    fix_in_i02: list
    must_fix_before_i03: list
    fix_in_i03: list
    must_fix_before_i04: list
    must_fix_before_i05: list
    deferred: list

  i02_handoff:
    i01_to_i02_handoff_packet_path: string
    permission_to_enter_i02: string

  compliance:
    p07_bypasses_p08: false
    p08_live_execution_allowed: false
    p09_direct_rule_mutation_allowed: false
    p10_auto_deploy_allowed: false
    trace_chain_unusable: false
```

---

# 28. HER I01 执行协议

```text
HER 执行 I01 时必须按以下顺序：

1. 读取 system_methodology_blueprint.md
2. 读取 professional_build_order.md
3. 读取 phase_controller_index.yaml
4. 读取 global_status_code_table.md
5. 读取 global_hard_negative_rules.md
6. 读取 directory_constitution.md
7. 读取 contract_index.md
8. 读取 schema_index.md
9. 读取 P01-P10 每个阶段的 controller / context / contract / schema / state_machine / hard_negative / gap_policy / trace / acceptance / handoff / test_matrix / report_model
10. 建立 i01_audit_input_manifest
11. 建立 phase_inventory_record
12. 审计 phase responsibility boundary
13. 审计 phase IO alignment
14. 审计 handoff chain integrity
15. 审计 data request chain
16. 审计 schema / contract coverage
17. 审计 status code consistency
18. 审计 gap propagation
19. 审计 forbidden use inheritance
20. 审计 trace coverage
21. 审计 acceptance coverage
22. 审计 phase boundary violation
23. 审计 downstream permission
24. 审计 runtime readiness
25. 审计 review / upgrade readiness
26. 生成 audit_findings.yaml
27. 生成 fix_priority_list.yaml
28. 生成 full_phase_consistency_audit_report.md
29. 生成 i01_to_i02_handoff_packet.yaml
30. 生成 i01_acceptance_result.yaml
31. 只允许 handoff 给 I02
```

禁止：

```text
1. 不允许新增 P11
2. 不允许修改 P01-P10 业务逻辑
3. 不允许直接写 Runner
4. 不允许直接绑定工具
5. 不允许启动 Paper Runtime
6. 不允许修改策略规则
7. 不允许自动部署
8. 不允许 live execution
```

---

# 29. 给 HER 的正式任务书

```text
任务名称：I01 Full Phase Consistency Audit：P01-P10 全阶段一致性审计任务包

目标：
在 /root/sikk-gmgn/system/integration_program/I01_full_phase_consistency_audit/ 下建立 I01 全阶段一致性审计任务包，并在 /root/sikk-gmgn/data/integration_program/I01_full_phase_consistency_audit/ 下生成运行审计输出。I01 不是 P11，不新增业务判断能力，不修改 P01-P10 业务逻辑。它的目标是在 Runner / Tool Binding 之前，对 P01-P10 的职责边界、输入输出、handoff、data request、schema、contract、状态码、gap、forbidden use、trace、acceptance、runtime readiness、P09/P10 review upgrade readiness 做全链路一致性审计，发现断点、冲突、越权和缺口，并生成修复优先级与 I01→I02 handoff packet。

核心原则：
1. I01 是 Integration Program 的第一步，不是新业务阶段。
2. I01 只审计，不修复。
3. I01 不新增 P11。
4. I01 不直接写 Runner。
5. I01 不绑定 GMGN / OKX 工具。
6. I01 不启动 Paper Runtime。
7. I01 不修改策略规则。
8. I01 不自动部署。
9. I01 必须检查 P01-P10 全部阶段。
10. I01 必须检查 handoff 链是否连续。
11. I01 必须检查 schema / contract 是否覆盖。
12. I01 必须检查状态码是否统一。
13. I01 必须检查 gap 和 forbidden use 是否继承。
14. I01 必须检查 trace 和 acceptance 是否完整。
15. I01 必须检查 P07 不得绕过 P08。
16. I01 必须检查 P08 不得产生 live execution。
17. I01 必须检查 P09 不得直接改规则。
18. I01 必须检查 P10 不得自动部署。
19. I01 必须输出 fix_priority_list。
20. I01 必须生成 i01_to_i02_handoff_packet，只允许交接给 I02。

需要创建系统目录：
/root/sikk-gmgn/system/integration_program/I01_full_phase_consistency_audit/

需要创建系统文件：
1. i01_full_phase_consistency_audit_controller.yaml
2. i01_full_phase_consistency_audit_context.md
3. i01_input_contract.yaml
4. i01_output_contract.yaml
5. i01_audit_input_manifest_schema.yaml
6. phase_inventory_schema.yaml
7. phase_responsibility_boundary_matrix_schema.yaml
8. phase_io_alignment_matrix_schema.yaml
9. handoff_chain_integrity_schema.yaml
10. data_request_chain_schema.yaml
11. schema_contract_coverage_schema.yaml
12. status_code_consistency_schema.yaml
13. gap_propagation_schema.yaml
14. forbidden_use_inheritance_schema.yaml
15. trace_coverage_schema.yaml
16. acceptance_coverage_schema.yaml
17. phase_boundary_violation_schema.yaml
18. downstream_permission_schema.yaml
19. runtime_readiness_precheck_schema.yaml
20. review_upgrade_readiness_schema.yaml
21. audit_finding_schema.yaml
22. fix_priority_schema.yaml
23. i01_to_i02_handoff_contract.yaml
24. i01_audit_policy.yaml
25. i01_hard_negative_rules.yaml
26. i01_state_machine.yaml
27. i01_trace_requirements.yaml
28. i01_acceptance_criteria.md
29. i01_storage_constitution.md
30. i01_test_matrix.yaml
31. i01_report_model.yaml
32. i01_review_checklist.md
33. her_i01_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/integration_program/I01_full_phase_consistency_audit/
  input_manifest/
  phase_inventory/
  responsibility_boundary/
  io_alignment/
  handoff_chain/
  data_request_chain/
  schema_contract_coverage/
  status_code_consistency/
  gap_propagation/
  forbidden_use_inheritance/
  trace_coverage/
  acceptance_coverage/
  boundary_violations/
  downstream_permissions/
  runtime_readiness/
  review_upgrade_readiness/
  findings/
  fix_priority/
  i02_handoff/
  reports/
  audit/
  trace/
  acceptance/

每个文件要求：
- i01_full_phase_consistency_audit_controller.yaml：定义 I01 身份、职责、权限、上下游、状态码、禁止事项。
- i01_full_phase_consistency_audit_context.md：写成 HER 执行前必须读取的 I01 上下文。
- i01_input_contract.yaml：定义 I01 必须读取的系统蓝图、P01-P10 阶段文件、总索引、治理规则。
- i01_output_contract.yaml：定义 I01 必须输出的审计报告、矩阵、发现项、修复优先级和 I02 handoff。
- i01_audit_input_manifest_schema.yaml：定义审计输入清单。
- phase_inventory_schema.yaml：定义 P01-P10 阶段清单。
- phase_responsibility_boundary_matrix_schema.yaml：定义职责边界矩阵。
- phase_io_alignment_matrix_schema.yaml：定义阶段输入输出对齐矩阵。
- handoff_chain_integrity_schema.yaml：定义 handoff 链完整性。
- data_request_chain_schema.yaml：定义 data request packet 链完整性。
- schema_contract_coverage_schema.yaml：定义 schema / contract 覆盖审计。
- status_code_consistency_schema.yaml：定义状态码一致性审计。
- gap_propagation_schema.yaml：定义 gap 传递审计。
- forbidden_use_inheritance_schema.yaml：定义 forbidden use 继承审计。
- trace_coverage_schema.yaml：定义 trace 覆盖审计。
- acceptance_coverage_schema.yaml：定义 acceptance 覆盖审计。
- phase_boundary_violation_schema.yaml：定义阶段越权记录。
- downstream_permission_schema.yaml：定义下游权限审计。
- runtime_readiness_precheck_schema.yaml：定义 P08 → Paper Runtime 就绪度审计。
- review_upgrade_readiness_schema.yaml：定义 P09/P10 闭环就绪度审计。
- audit_finding_schema.yaml：定义审计发现项。
- fix_priority_schema.yaml：定义修复优先级。
- i01_to_i02_handoff_contract.yaml：定义 I01→I02 handoff packet。
- i01_audit_policy.yaml：定义 I01 审计策略。
- i01_hard_negative_rules.yaml：定义 live execution、P07 绕过 P08、P08 钱包签名、P09 直接改规则、P10 自动部署等阻断。
- i01_state_machine.yaml：定义 I01 全状态机。
- i01_trace_requirements.yaml：定义 I01 审计 trace。
- i01_acceptance_criteria.md：定义 I01_READY / READY_WITH_GAPS / REJECTED / BLOCKED。
- i01_storage_constitution.md：定义系统文件和运行数据目录。
- i01_test_matrix.yaml：定义至少 16 个测试场景。
- i01_report_model.yaml：定义 I01 人类可读报告。
- i01_review_checklist.md：定义 I01 审计清单。
- her_i01_execution_protocol.md：定义 HER 执行 I01 的顺序和禁止事项。

运行输出要求：
1. full_phase_consistency_audit_report.md
2. phase_inventory.yaml
3. phase_responsibility_boundary_matrix.yaml
4. phase_io_alignment_matrix.yaml
5. handoff_chain_integrity_report.yaml
6. data_request_chain_report.yaml
7. schema_contract_coverage_report.yaml
8. status_code_consistency_report.yaml
9. gap_propagation_report.yaml
10. forbidden_use_inheritance_report.yaml
11. trace_coverage_report.yaml
12. acceptance_coverage_report.yaml
13. phase_boundary_violation_report.yaml
14. downstream_permission_report.yaml
15. runtime_readiness_precheck_report.yaml
16. review_upgrade_readiness_report.yaml
17. audit_findings.yaml
18. fix_priority_list.yaml
19. i01_to_i02_handoff_packet.yaml
20. i01_acceptance_result.yaml

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P01-P10 阶段清单摘要
4. 阶段职责边界审计摘要
5. 输入输出对齐矩阵摘要
6. Handoff 链完整性摘要
7. Data Request 链完整性摘要
8. Schema / Contract 覆盖摘要
9. 状态码一致性摘要
10. Gap 传递摘要
11. Forbidden Use 继承摘要
12. Trace 覆盖摘要
13. Acceptance 覆盖摘要
14. 阶段越权记录摘要
15. Runtime Readiness 摘要
16. Review / Upgrade Readiness 摘要
17. Audit Findings 摘要
18. Fix Priority 摘要
19. I01→I02 Handoff 摘要
20. 是否允许进入 I02
21. 是否达到轻量机构级 I01 v1.0

最终验收标准：
只有当 I01 具备 phase inventory、responsibility boundary matrix、IO alignment matrix、handoff chain integrity、data request chain、schema contract coverage、status code consistency、gap propagation、forbidden use inheritance、trace coverage、acceptance coverage、boundary violation detection、runtime readiness precheck、review upgrade readiness、audit findings、fix priority、I01→I02 handoff、hard negative rules、state machine、trace requirements、acceptance criteria、test matrix、report model、HER execution protocol，并且没有 live execution path、没有 P07 绕过 P08、没有 P08 钱包签名、没有 P09 直接改规则、没有 P10 自动部署时，才允许标记为 I01_READY。
```

---

# 30. 当前是否达到专业化 I01 设计标准

## 判断

这一版 I01 达到：

```text
专业化
轻量机构水准
一次性把 I01 应有审计对象补全
不是最小版本
不是简单检查清单
不是继续新增业务阶段
```

I01 被明确设计为：

```text
全阶段一致性审计层
输入输出链审计层
Handoff 链完整性审计层
Schema / Contract 覆盖审计层
状态码一致性审计层
Gap / Forbidden Use 继承审计层
Trace / Acceptance 覆盖审计层
Runtime Readiness 审计层
P09/P10 闭环就绪审计层
I02 交接准备层
```

---

# 31. I01 完成后下一步

I01 完成后，不要直接进入 Runner。

应进入：

```text
I02 Directory & Contract Index Unification
```

I02 负责根据 I01 的审计结果，统一：

```text
目录宪法
contract_index
schema_index
handoff_contract_index
phase_controller_file_index
runtime_data_path_index
legacy_path_mapping
canonical_path_policy
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|P01-P10 实际文件是否已经全部存在|I01 会审计|缺失项进入 fix_priority|
|schema / contract 是否已按统一命名落地|I01 会发现|I02 统一索引|
|legacy 运行目录如何映射|I01 只识别缺口|I02 建 legacy_path_mapping|
|Runner 绑定哪些脚本|I01 不处理|I03 处理|
|Paper Runtime 是否已能读取 P08 handoff|I01 只审计 readiness|I04 联调|
|P09/P10 是否能跑闭环|I01 只审计前置条件|I05 回放验证|

---

# 本次认知升级点

1. **I01 不是 P11，而是 Integration Program 的第一道审计门。**
    
2. **I01 不修复系统，只发现断点并排序。**
    
3. **Runner / Tool Binding 之前必须先做 I01。**  
    否则代码会把设计断点固化成工程错误。
    
4. **I01 的重点不是“有没有文件”，而是“阶段之间能不能接起来”。**
    
5. **P07 / P08 / Paper Runtime 的边界必须在 I01 强审计。**  
    `PAPER_CANDIDATE → P08 → PAPER_RUNTIME_ALLOWED → Paper Runtime` 不能被跳过。
    
6. **P09 / P10 是否能闭环，取决于前面所有 trace / handoff / acceptance 是否完整。**
    
7. **I01 的最终产物不是代码，而是 `fix_priority_list` 与 `i01_to_i02_handoff_packet`。**