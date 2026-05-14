# I03 Runner / Tool Binding 专业版 v1.0

## 阶段运行器、工具绑定、字段映射、Trace / Acceptance / Handoff Writer 与 Dry-run 验证任务包

---

## 0. I03 的核心定位

I03 不是新的业务阶段，也不是 P13。

它属于：

```text
Integration Program：系统集成落地计划
```

I03 的专业定义：

```text
I03 Runner / Tool Binding 是在 I02 完成目录、合约、schema、handoff、runtime path 统一索引之后，
把 P01-P10 的阶段控制器、schema、contract、trace、acceptance、handoff、工具输入输出、runner 参数、错误处理、dry-run 验证统一绑定成可执行工程入口的任务包。
```

一句话：

> **I02 解决“去哪里读、去哪里写、按什么合约读写”。**  
> **I03 解决“由哪个 runner 执行、调用哪个工具、字段如何映射、错误如何处理、trace 如何写、acceptance 如何跑、handoff 如何生成”。**

---

# 1. I03 不负责什么

I03 不能越权。

```text
I03 不新增 P11 / P12 / P13
I03 不修改 P01-P10 业务逻辑
I03 不改变策略判断规则
I03 不改证据权重
I03 不直接启动 Paper Runtime
I03 不做真实交易
I03 不做钱包签名
I03 不自动部署
I03 不删除 legacy 数据
I03 不把 legacy 数据写成 canonical 输出
I03 不允许 live execution
```

I03 只做：

```text
绑定 runner
绑定工具
绑定字段映射
绑定 schema 校验
绑定 contract 校验
绑定 trace writer
绑定 acceptance runner
绑定 handoff writer
绑定 path guard
绑定 dry-run
绑定错误处理
绑定 I04 Paper-only Runtime 联调前置条件
```

---

# 2. I03 的阶段目标

I03 必须一次性解决 20 类问题：

|编号|问题|I03 必须输出|
|---|---|---|
|1|每个阶段由哪个 runner 执行？|`phase_runner_binding_index`|
|2|runner 如何读取 I02 索引？|`runner_read_protocol`|
|3|runner 如何写入 canonical data path？|`runner_write_protocol`|
|4|如何阻断未登记路径写入？|`path_guard_binding`|
|5|如何做 schema 校验？|`schema_validator_binding`|
|6|如何做 contract 校验？|`contract_validator_binding`|
|7|如何生成 trace？|`trace_writer_binding`|
|8|如何生成 acceptance result？|`acceptance_runner_binding`|
|9|如何生成 handoff packet？|`handoff_writer_binding`|
|10|GMGN 字段如何绑定？|`gmgn_tool_binding`|
|11|OKX quote 如何绑定？|`okx_quote_binding`|
|12|OKX security 如何绑定？|`okx_security_binding`|
|13|K线 / 市场结构如何绑定？|`kline_provider_binding`|
|14|legacy 数据如何只读读取？|`legacy_reader_binding`|
|15|runner 失败如何处理？|`runner_error_policy`|
|16|工具失败如何重试？|`tool_retry_policy`|
|17|dry-run 如何验证？|`dry_run_validation_matrix`|
|18|CLI / HER 如何调用 runner？|`runner_cli_command_registry`|
|19|哪些 runner 可进入 I04？|`i04_paper_runtime_prerequisite_packet`|
|20|是否可以交接给 I04？|`i03_to_i04_handoff_packet`|

---

# 3. I03 的底层方法论

## 3.1 Runner 不是脚本，而是阶段执行协议

普通脚本只关心：

```text
输入文件
输出文件
运行命令
```

专业 runner 必须关心：

```text
读取顺序
输入合约
输出合约
schema 校验
trace 写入
acceptance 验收
handoff 生成
错误处理
权限边界
路径守卫
dry-run 结果
```

所以 I03 的重点不是“写一个脚本”，而是建立：

```text
Phase Runner Execution Contract
```

---

## 3.2 Tool Binding 不是 API 调用，而是字段治理

工具绑定不能只写：

```text
调用 GMGN
调用 OKX
读取 K线
```

必须写清楚：

```text
工具返回什么字段
字段映射到哪个 canonical object
字段质量如何标记
字段是否可作为 strong evidence
字段是否需要 trace
字段缺失怎么处理
字段冲突怎么处理
字段过期怎么处理
```

---

## 3.3 I03 只允许 dry-run，不进入真实 runtime

I03 可以做：

```text
schema dry-run
contract dry-run
mock tool dry-run
legacy read-only dry-run
handoff generation dry-run
trace writing dry-run
acceptance dry-run
```

I03 不允许：

```text
真实纸面开仓
真实持仓更新
真实下单
钱包签名
自动部署
```

Paper Runtime 联调属于 I04。

---

## 3.4 所有 runner 必须先读 I02 索引

I03 后的任何 runner 都不能自己猜路径。

必须先读取：

```text
directory_constitution_final
phase_controller_file_index
runtime_data_path_index
schema_index
contract_index
handoff_contract_index
data_request_packet_index
read_order_manifest
write_permission_matrix
legacy_path_mapping
canonical_path_policy
```

否则会重新制造目录混乱。

---

# 4. I03 输入范围

```yaml
i03_required_inputs:
  from_i02:
    - i02_to_i03_handoff_packet
    - i03_runner_tool_binding_prerequisite_packet
    - canonical_root_declaration
    - directory_constitution_final
    - phase_controller_file_index
    - runtime_data_path_index
    - artifact_type_registry
    - schema_index
    - contract_index
    - handoff_contract_index
    - data_request_packet_index
    - trace_artifact_index
    - acceptance_artifact_index
    - report_model_index
    - read_order_manifest
    - write_permission_matrix
    - legacy_path_mapping
    - canonical_path_policy
    - path_conflict_report
    - index_gap_report
    - i02_acceptance_result

  from_phase_controllers:
    - P01 controller / contracts / schemas / policies
    - P02 controller / contracts / schemas / policies
    - P03 controller / contracts / schemas / policies
    - P04 controller / contracts / schemas / policies
    - P05 controller / contracts / schemas / policies
    - P06 controller / contracts / schemas / policies
    - P07 controller / contracts / schemas / policies
    - P08 controller / contracts / schemas / policies
    - P09 controller / contracts / schemas / policies
    - P10 controller / contracts / schemas / policies

  from_existing_tools:
    - GMGN data tools or skill outputs
    - OKX quote/security outputs
    - Kline provider outputs
    - existing paper runner references
    - existing state machine outputs
    - legacy reports
    - legacy paper_live outputs

  required_system_rules:
    - global_hard_negative_rules
    - global_status_code_table
    - forbidden_use_policy
    - trace_policy
    - acceptance_policy
    - handoff_policy
```

---

# 5. I03 必须建立的核心对象

|对象|作用|
|---|---|
|`I03 Input Manifest`|记录 I03 读取了哪些索引、合约、工具信息|
|`Runner Capability Registry`|当前可用 runner 能力注册|
|`Phase Runner Binding Index`|P01-P10 每阶段 runner 绑定|
|`Tool Binding Index`|GMGN / OKX / K线 / legacy / writer 工具绑定|
|`Phase Runner Contract`|每阶段 runner 输入输出执行合约|
|`Global Runner Orchestrator Contract`|总控 runner 编排合约|
|`Runner CLI Command Registry`|HER / CLI 可调用命令表|
|`Environment Config Registry`|环境变量、路径、只读权限、dry-run 配置|
|`Tool Credential Policy`|凭证和密钥使用边界|
|`GMGN Tool Binding`|GMGN 字段映射与错误处理|
|`OKX Quote Binding`|OKX 报价绑定|
|`OKX Security Binding`|OKX 安全扫描绑定|
|`Kline Provider Binding`|K线 / 市场结构输入绑定|
|`Legacy Reader Binding`|旧数据只读读取绑定|
|`Schema Validator Binding`|schema 校验器绑定|
|`Contract Validator Binding`|contract 校验器绑定|
|`Trace Writer Binding`|trace 写入器绑定|
|`Acceptance Runner Binding`|acceptance 验收器绑定|
|`Handoff Writer Binding`|handoff packet 写入器绑定|
|`Path Guard Binding`|未登记路径写入阻断|
|`Runner Error Policy`|runner 错误处理规则|
|`Tool Retry Policy`|工具失败重试规则|
|`Dry-run Validation Matrix`|dry-run 验证矩阵|
|`I04 Paper Runtime Prerequisite Packet`|I04 前置条件包|
|`I03 to I04 Handoff Packet`|I03 → I04 交接包|

---

# 6. I03 运行目录设计

## 6.1 系统目录

```text
/root/sikk-gmgn/system/integration_program/I03_runner_tool_binding/
```

必须创建：

```text
i03_runner_tool_binding_controller.yaml
i03_runner_tool_binding_context.md
i03_input_contract.yaml
i03_output_contract.yaml
i03_input_manifest_schema.yaml
runner_capability_registry_schema.yaml
phase_runner_binding_index_schema.yaml
tool_binding_index_schema.yaml
phase_runner_contract_schema.yaml
global_runner_orchestrator_contract_schema.yaml
runner_cli_command_registry_schema.yaml
environment_config_registry_schema.yaml
tool_credential_policy_schema.yaml
gmgn_tool_binding_schema.yaml
okx_quote_binding_schema.yaml
okx_security_binding_schema.yaml
kline_provider_binding_schema.yaml
legacy_reader_binding_schema.yaml
schema_validator_binding_schema.yaml
contract_validator_binding_schema.yaml
trace_writer_binding_schema.yaml
acceptance_runner_binding_schema.yaml
handoff_writer_binding_schema.yaml
path_guard_binding_schema.yaml
runner_error_policy_schema.yaml
tool_retry_policy_schema.yaml
dry_run_validation_matrix_schema.yaml
i04_paper_runtime_prerequisite_packet_contract.yaml
i03_to_i04_handoff_contract.yaml
i03_binding_policy.yaml
i03_hard_negative_rules.yaml
i03_state_machine.yaml
i03_trace_requirements.yaml
i03_acceptance_criteria.md
i03_storage_constitution.md
i03_test_matrix.yaml
i03_report_model.yaml
i03_review_checklist.md
her_i03_execution_protocol.md
```

---

## 6.2 运行数据目录

```text
/root/sikk-gmgn/data/integration_program/I03_runner_tool_binding/
  input_manifest/
  runner_capabilities/
  phase_runner_binding/
  tool_binding/
  phase_runner_contracts/
  orchestrator_contract/
  cli_registry/
  env_config/
  credential_policy/
  gmgn_binding/
  okx_quote_binding/
  okx_security_binding/
  kline_binding/
  legacy_reader_binding/
  schema_validator/
  contract_validator/
  trace_writer/
  acceptance_runner/
  handoff_writer/
  path_guard/
  error_policy/
  retry_policy/
  dry_run/
  i04_prerequisites/
  i04_handoff/
  reports/
  audit/
  trace/
  acceptance/
```

---

# 7. Runner Capability Registry

```yaml
runner_capability_registry:
  registry_id: RUNNER_CAPABILITY_REGISTRY
  generated_at: datetime
  version: v1.0

  runner_types:
    PHASE_RUNNER:
      purpose_cn: 执行 P01-P10 单阶段控制器
      required_capabilities:
        - read_i02_indexes
        - load_phase_context
        - validate_input_contract
        - validate_output_schema
        - write_runtime_outputs
        - write_trace
        - run_acceptance
        - write_handoff_packet

    GLOBAL_ORCHESTRATOR:
      purpose_cn: 按阶段顺序编排 P01-P10
      required_capabilities:
        - resolve_phase_order
        - check_previous_handoff
        - stop_on_blocked
        - propagate_gaps
        - enforce_forbidden_use
        - produce_cycle_report

    TOOL_ADAPTER:
      purpose_cn: 调用 GMGN / OKX / K线 / legacy source
      required_capabilities:
        - normalize_tool_response
        - map_fields
        - attach_source_trace
        - handle_missing_fields
        - handle_conflicts
        - handle_retries

    VALIDATOR:
      purpose_cn: schema / contract / handoff 校验
      required_capabilities:
        - validate_schema
        - validate_contract
        - validate_required_fields
        - validate_status_code
        - validate_forbidden_use

    WRITER:
      purpose_cn: trace / acceptance / handoff / report 写入
      required_capabilities:
        - write_trace
        - write_acceptance_result
        - write_handoff_packet
        - write_report

  execution_modes:
    - DRY_RUN
    - MOCK_TOOL_RUN
    - LEGACY_READONLY_RUN
    - PAPER_ONLY_PRECHECK
    - LIVE_EXECUTION_FORBIDDEN

  registry_status:
    - COMPLETE
    - COMPLETE_WITH_GAPS
    - UNUSABLE
```

---

# 8. Phase Runner Binding Index

```yaml
phase_runner_binding_index:
  index_id: PHASE_RUNNER_BINDING_INDEX
  generated_at: datetime

  phases:
    P01:
      phase_name: Candidate Intake Controller
      runner_id: p01_candidate_intake_runner
      runner_entrypoint: tools/runners/p01_candidate_intake_runner.py
      execution_mode_allowed:
        - DRY_RUN
        - PAPER_PIPELINE_RUN
      required_inputs:
        - candidate_source_input
        - p01_input_contract
        - candidate_master_record_schema
      required_outputs:
        - candidate_master_records
        - discovery_context_records
        - p02_source_data_request_packet
        - p01_to_p02_handoff_packet
      required_writers:
        - trace_writer
        - acceptance_runner
        - handoff_writer
      forbidden:
        - wallet_classification
        - chip_structure_judgment
        - strategy_gate
        - paper_runtime
        - live_execution

    P02:
      phase_name: Source Data Fact Controller
      runner_id: p02_source_data_fact_runner
      runner_entrypoint: tools/runners/p02_source_data_fact_runner.py
      required_tools:
        - gmgn_tool_adapter
        - okx_security_adapter_optional
        - kline_provider_optional
      required_outputs:
        - normalized_source_fact_records
        - data_quality_report
        - security_fact_records
        - p03_wallet_entity_data_request_packet
        - p02_to_p03_handoff_packet

    P03:
      phase_name: Wallet Entity Controller
      runner_id: p03_wallet_entity_runner
      required_tools:
        - gmgn_wallet_adapter
        - legacy_source_wallet_reader_optional
      required_outputs:
        - wallet_entity_master_records
        - same_source_group_candidates
        - sync_behavior_group_candidates
        - wallet_role_candidate_records
        - p04_chip_structure_data_request_packet
        - p03_to_p04_handoff_packet

    P04:
      phase_name: Chip Structure Controller
      runner_id: p04_chip_structure_runner
      required_outputs:
        - early_wallet_retention_records
        - structural_group_holding_records
        - chip_transfer_status_records
        - distribution_progress_records
        - counterparty_pressure_records
        - p05_evidence_data_request_packet
        - p04_to_p05_handoff_packet

    P05:
      phase_name: Evidence Controller
      runner_id: p05_evidence_runner
      required_outputs:
        - evidence_object_records
        - counter_evidence_records
        - unknown_evidence_records
        - evidence_bundle_records
        - p06_scenario_data_request_packet
        - p05_to_p06_handoff_packet

    P06:
      phase_name: Scenario Recognition Controller
      runner_id: p06_scenario_recognition_runner
      required_outputs:
        - scenario_candidate_records
        - primary_scenario_candidate_records
        - scenario_conflict_records
        - scenario_invalidation_records
        - scenario_risk_flag_records
        - p07_strategy_gate_data_request_packet
        - p06_to_p07_handoff_packet

    P07:
      phase_name: Strategy Gate Controller
      runner_id: p07_strategy_gate_runner
      required_outputs:
        - strategy_gate_decision_records
        - strategy_candidate_records
        - strategy_usage_permission_records
        - p08_execution_risk_data_request_packet
        - p07_to_p08_handoff_packet
      forbidden:
        - paper_runtime_started
        - live_execution
        - wallet_signing

    P08:
      phase_name: Execution Risk Controller
      runner_id: p08_execution_risk_runner
      required_tools:
        - okx_quote_adapter
        - okx_security_adapter
        - liquidity_provider_adapter
      required_outputs:
        - paper_runtime_permission_records
        - paper_entry_simulation_plans
        - paper_runtime_data_request_packet
        - p08_to_paper_runtime_handoff_packet
      forbidden:
        - live_order
        - wallet_signing
        - real_swap

    P09:
      phase_name: Review Replay Controller
      runner_id: p09_review_replay_runner
      required_inputs:
        - paper_runtime_outputs
        - p01_to_p08_trace_chain
      required_outputs:
        - failure_attribution_records
        - success_attribution_records
        - calibration_candidate_records
        - p10_upgrade_candidate_data_request_packet
        - p09_to_p10_handoff_packet

    P10:
      phase_name: Self Upgrade Controller
      runner_id: p10_self_upgrade_runner
      required_outputs:
        - controlled_upgrade_package_records
        - controlled_upgrade_task_packets
        - regression_test_plan_records
        - release_and_rollback_plan_records
        - p10_to_implementation_handoff_packet
      forbidden:
        - auto_deploy
        - direct_production_mutation
        - live_execution

  binding_status:
    - COMPLETE
    - COMPLETE_WITH_GAPS
    - CRITICAL_RUNNER_MISSING
    - UNUSABLE
```

---

# 9. Tool Binding Index

```yaml
tool_binding_index:
  index_id: TOOL_BINDING_INDEX
  generated_at: datetime

  tools:
    GMGN_TOOL_BINDING:
      owner_stages:
        - P02
        - P03
        - P04
      adapter_id: gmgn_tool_adapter
      output_types:
        - token_basic_fact
        - holder_snapshot
        - wallet_rows
        - wallet_trade_rows
        - top_holder_rows
        - smart_money_rows
      requires_trace: true
      failure_policy: RETRY_THEN_MARK_PARTIAL

    OKX_QUOTE_BINDING:
      owner_stages:
        - P08
      adapter_id: okx_quote_adapter
      output_types:
        - quote_snapshot
        - quote_consistency_record
      requires_trace: true
      failure_policy: BLOCK_IF_QUOTE_UNAVAILABLE

    OKX_SECURITY_BINDING:
      owner_stages:
        - P02
        - P08
      adapter_id: okx_security_adapter
      output_types:
        - security_fact_record
        - security_recheck_record
      requires_trace: true
      failure_policy: BLOCK_OR_PAUSE_IF_SECURITY_UNKNOWN

    KLINE_PROVIDER_BINDING:
      owner_stages:
        - P02
        - P06
        - P07
      adapter_id: kline_provider_adapter
      output_types:
        - kline_fact_record
        - market_structure_fact_seed
      requires_trace: true
      failure_policy: PAUSE_IF_REQUIRED_CONTEXT_MISSING

    LEGACY_READER_BINDING:
      owner_stages:
        - P09
        - I04
        - I05
      adapter_id: legacy_readonly_reader
      output_types:
        - legacy_paper_positions
        - legacy_signal_outputs
        - legacy_quote_security_outputs
      requires_trace_wrapper: true
      write_permission: READ_ONLY

    TRACE_WRITER_BINDING:
      owner_stages:
        - P01_TO_P10
        - I01_TO_I05
      adapter_id: trace_writer

    ACCEPTANCE_RUNNER_BINDING:
      owner_stages:
        - P01_TO_P10
        - I01_TO_I05
      adapter_id: acceptance_runner

    HANDOFF_WRITER_BINDING:
      owner_stages:
        - P01_TO_P10
        - I01_TO_I05
      adapter_id: handoff_writer

  binding_status:
    - TOOL_BINDING_COMPLETE
    - TOOL_BINDING_WITH_GAPS
    - TOOL_BINDING_BLOCKED
```

---

# 10. Phase Runner Contract

```yaml
phase_runner_contract:
  contract_id: PHASE_RUNNER_CONTRACT
  version: v1.0

  common_required_steps:
    - load_i02_indexes
    - resolve_phase_paths
    - load_phase_controller
    - load_phase_context
    - validate_upstream_handoff
    - validate_input_contract
    - execute_phase_logic_or_dry_run
    - validate_output_schema
    - enforce_forbidden_use
    - write_outputs_to_canonical_data_dir
    - write_trace
    - run_acceptance
    - write_handoff_packet
    - write_phase_report

  required_inputs:
    i02_indexes:
      - phase_controller_file_index
      - runtime_data_path_index
      - schema_index
      - contract_index
      - handoff_contract_index
      - read_order_manifest
      - write_permission_matrix
      - canonical_path_policy

    phase_specific_inputs:
      - upstream_handoff_packet
      - upstream_runtime_outputs
      - phase_input_contract
      - phase_context
      - phase_policy
      - phase_schemas

  required_outputs:
    - phase_runtime_outputs
    - phase_trace
    - phase_acceptance_result
    - downstream_data_request_packet
    - downstream_handoff_packet
    - phase_report

  hard_requirements:
    no_unregistered_write_path: true
    no_business_logic_mutation: true
    no_live_execution: true
    no_wallet_signing: true
    blocked_items_not_used_downstream: true
    ready_with_gaps_must_propagate: true
```

---

# 11. Global Runner Orchestrator Contract

```yaml
global_runner_orchestrator_contract:
  contract_id: GLOBAL_RUNNER_ORCHESTRATOR_CONTRACT
  version: v1.0

  orchestration_scope:
    allowed_phases:
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

    integration_allowed:
      - I01
      - I02
      - I03
      - I04
      - I05

  execution_order:
    standard_pipeline:
      - P01
      - P02
      - P03
      - P04
      - P05
      - P06
      - P07
      - P08
      - PAPER_ONLY_RUNTIME
      - P09
      - P10

  stop_conditions:
    - upstream_handoff_missing
    - acceptance_blocked
    - hard_negative_triggered
    - forbidden_use_detected
    - schema_validation_failed
    - contract_validation_failed
    - unregistered_write_path
    - live_execution_path_detected

  gap_policy:
    ready_with_gaps_allowed_to_continue_if_downstream_permission_allows: true
    high_gap_requires_limitation_tag: true
    critical_gap_blocks_downstream: true

  runtime_boundary:
    P07_must_not_start_paper_runtime: true
    P08_must_not_start_live_execution: true
    paper_runtime_requires_P08_permission: true
```

---

# 12. Runner CLI Command Registry

```yaml
runner_cli_command_registry:
  registry_id: RUNNER_CLI_COMMAND_REGISTRY
  version: v1.0

  global_commands:
    dry_run_all:
      command: "python3 tools/runners/sikk_phase_orchestrator.py --mode dry-run --read-indexes data/integration_program/I02_directory_contract_index_unification/i03_prerequisites/i03_runner_tool_binding_prerequisite_packet.yaml"
      purpose_cn: 按索引 dry-run 全阶段，不启动 Paper Runtime

    validate_indexes:
      command: "python3 tools/validators/validate_i02_indexes.py --i02-handoff data/integration_program/I02_directory_contract_index_unification/i03_handoff/i02_to_i03_handoff_packet.yaml"
      purpose_cn: 校验 I02 索引是否可被 runner 读取

    validate_contracts:
      command: "python3 tools/validators/validate_contracts.py --contract-index data/integration_program/I02_directory_contract_index_unification/contract_index/contract_index.yaml"
      purpose_cn: 校验 contract index

    validate_schemas:
      command: "python3 tools/validators/validate_schemas.py --schema-index data/integration_program/I02_directory_contract_index_unification/schema_index/schema_index.yaml"
      purpose_cn: 校验 schema index

  phase_commands:
    p01_dry_run:
      command: "python3 tools/runners/p01_candidate_intake_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p02_dry_run:
      command: "python3 tools/runners/p02_source_data_fact_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p03_dry_run:
      command: "python3 tools/runners/p03_wallet_entity_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p04_dry_run:
      command: "python3 tools/runners/p04_chip_structure_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p05_dry_run:
      command: "python3 tools/runners/p05_evidence_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p06_dry_run:
      command: "python3 tools/runners/p06_scenario_recognition_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p07_dry_run:
      command: "python3 tools/runners/p07_strategy_gate_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"
    p08_dry_run:
      command: "python3 tools/runners/p08_execution_risk_runner.py --mode dry-run --index-root data/integration_program/I02_directory_contract_index_unification"

  restrictions:
    live_execution_commands_registered: false
    wallet_signing_commands_registered: false
    auto_deploy_commands_registered: false
```

---

# 13. Environment Config Registry

```yaml
environment_config_registry:
  registry_id: ENVIRONMENT_CONFIG_REGISTRY
  version: v1.0

  required_env:
    SIKK_ROOT:
      default: /root/sikk-gmgn
      required: true

    SIKK_MODE:
      allowed_values:
        - dry_run
        - mock_tool
        - legacy_readonly
        - paper_only
      forbidden_values:
        - live_trade
        - auto_swap

    SIKK_INDEX_ROOT:
      default: /root/sikk-gmgn/data/integration_program/I02_directory_contract_index_unification

    SIKK_OUTPUT_ROOT:
      default: /root/sikk-gmgn/data

    SIKK_LEGACY_READONLY:
      default: "true"
      required: true

    SIKK_LIVE_EXECUTION_ALLOWED:
      default: "false"
      required: true

    SIKK_WALLET_SIGNING_ALLOWED:
      default: "false"
      required: true

  optional_env:
    GMGN_API_MODE:
      allowed_values:
        - mock
        - readonly
    OKX_QUOTE_MODE:
      allowed_values:
        - mock
        - readonly
    OKX_SECURITY_MODE:
      allowed_values:
        - mock
        - readonly

  hard_env_rules:
    - live_execution_env_must_be_false
    - wallet_signing_env_must_be_false
    - legacy_readonly_must_be_true
    - unregistered_output_root_forbidden
```

---

# 14. Tool Credential Policy

```yaml
tool_credential_policy:
  policy_id: TOOL_CREDENTIAL_POLICY
  version: v1.0

  allowed_credential_usage:
    GMGN:
      allowed_mode:
        - readonly
        - mock
      secret_storage_policy: DO_NOT_WRITE_SECRETS_TO_REPO
      trace_secret_values: false

    OKX:
      allowed_mode:
        - readonly_quote
        - readonly_security
        - mock
      trading_permission_required: false
      secret_storage_policy: DO_NOT_WRITE_SECRETS_TO_REPO
      trace_secret_values: false

  forbidden_credential_usage:
    - private_key
    - seed_phrase
    - wallet_signing_key
    - auto_trade_api_key
    - live_order_permission

  hard_rules:
    - never_print_secrets
    - never_write_secrets_to_report
    - never_enable_trading_permission
    - readonly_tools_only
```

---

# 15. GMGN Tool Binding

```yaml
gmgn_tool_binding:
  binding_id: GMGN_TOOL_BINDING
  version: v1.0

  owner_stages:
    - P02_SOURCE_DATA_FACT
    - P03_WALLET_ENTITY
    - P04_CHIP_STRUCTURE

  input_modes:
    - token_address
    - candidate_batch
    - wallet_address
    - holder_snapshot
    - wallet_trade_rows

  canonical_outputs:
    token_basic_fact:
      maps_to_stage: P02
      fields:
        - token_address
        - chain
        - symbol
        - name
        - creation_time
        - market_cap_usd
        - liquidity_usd
        - holder_count
        - volume_5m
        - volume_1h
        - price_usd

    holder_snapshot_fact:
      maps_to_stage: P02
      fields:
        - holder_address
        - holder_rank
        - holding_amount
        - holding_pct
        - pnl
        - first_seen_time

    wallet_entity_seed:
      maps_to_stage: P03
      fields:
        - wallet_address
        - funding_source
        - token_source
        - buy_time
        - sell_time
        - holding_duration
        - realized_pnl
        - current_holding

    chip_structure_seed:
      maps_to_stage: P04
      fields:
        - early_wallet_remaining_pct
        - structural_group_holding_pct
        - distribution_flow
        - counterparty_wallets
        - transfer_paths

  quality_tags:
    - GMGN_SOURCE
    - TOOL_READONLY
    - FIELD_MISSING_ALLOWED_IF_TAGGED
    - TRACE_REQUIRED

  failure_policy:
    if_tool_unavailable: P02_READY_WITH_GAPS_OR_PAUSE
    if_required_field_missing: MARK_FIELD_GAP
    if_response_conflict: CREATE_DATA_CONFLICT_RECORD
    retry_allowed: true
```

---

# 16. OKX Quote Binding

```yaml
okx_quote_binding:
  binding_id: OKX_QUOTE_BINDING
  version: v1.0

  owner_stage:
    - P08_EXECUTION_RISK

  canonical_outputs:
    quote_snapshot_record:
      fields:
        - token_address
        - quote_source
        - price_usd
        - bid_price_usd
        - ask_price_usd
        - spread_pct
        - liquidity_usd
        - source_latency_ms
        - quote_time

    quote_consistency_record:
      fields:
        - gmgn_price_usd
        - okx_quote_price_usd
        - chain_estimated_price_usd
        - max_source_deviation_pct
        - quote_consistency_status

  required_trace:
    - quote_request_trace
    - quote_response_trace
    - quote_selection_trace

  failure_policy:
    quote_unavailable: BLOCK_P08_RUNTIME_PERMISSION
    quote_major_deviation: BLOCK_P08_RUNTIME_PERMISSION
    quote_minor_deviation: ALLOW_WITH_LIMITATION
    quote_stale: REQUIRE_REFRESH
```

---

# 17. OKX Security Binding

```yaml
okx_security_binding:
  binding_id: OKX_SECURITY_BINDING
  version: v1.0

  owner_stages:
    - P02_SOURCE_DATA_FACT
    - P08_EXECUTION_RISK

  canonical_outputs:
    security_fact_record:
      maps_to_stage: P02
      fields:
        - mint_authority_status
        - freeze_authority_status
        - blacklist_risk
        - transfer_restriction_risk
        - honeypot_risk
        - liquidity_lock_status
        - tax_risk

    security_recheck_record:
      maps_to_stage: P08
      fields:
        - checked_at
        - security_status
        - hard_block_reasons
        - sellability_status

  failure_policy:
    security_risk_detected: BLOCK
    security_unknown_for_required_check: PAUSE_OR_BLOCK
    security_stale: REQUIRE_REFRESH
```

---

# 18. Kline Provider Binding

```yaml
kline_provider_binding:
  binding_id: KLINE_PROVIDER_BINDING
  version: v1.0

  owner_stages:
    - P02_SOURCE_DATA_FACT
    - P06_SCENARIO_RECOGNITION
    - P07_STRATEGY_GATE

  canonical_outputs:
    kline_fact_record:
      fields:
        - timestamp
        - open
        - high
        - low
        - close
        - volume
        - timeframe

    market_structure_fact_seed:
      fields:
        - avwap_status
        - poc_status
        - control_box_status
        - higher_low_status
        - breakout_status
        - pullback_status
        - volume_expansion_status

  failure_policy:
    kline_missing_for_required_scenario: P06_READY_WITH_GAPS_OR_OBSERVE
    market_structure_missing_for_p07: PAUSE_OR_OBSERVE
    stale_kline: REQUIRE_REFRESH
```

---

# 19. Legacy Reader Binding

```yaml
legacy_reader_binding:
  binding_id: LEGACY_READER_BINDING
  version: v1.0

  allowed_legacy_roots:
    - /root/sikk-gmgn/data/gmgn_candidates_live_run
    - /root/sikk-gmgn/data/source_wallet_bot
    - /root/sikk-gmgn/data/intel_bot

  allowed_usage:
    - replay_reference
    - migration_reference
    - seed_reference
    - comparison_reference

  forbidden_usage:
    - overwrite_canonical_output
    - treat_legacy_as_current_without_quality_tag
    - delete_legacy_data
    - move_legacy_data
    - write_new_runtime_to_legacy_path

  required_tags:
    - LEGACY_SOURCE
    - READ_ONLY
    - TRACE_WRAPPED
    - QUALITY_REVIEW_REQUIRED

  trace_wrapper:
    required: true
    output_trace_type: legacy_read_trace
```

---

# 20. Schema / Contract Validator Binding

```yaml
schema_validator_binding:
  binding_id: SCHEMA_VALIDATOR_BINDING
  version: v1.0

  inputs:
    - schema_index
    - runtime_output_paths
    - artifact_type_registry

  validation_targets:
    - phase_runtime_outputs
    - handoff_packets
    - data_request_packets
    - acceptance_results
    - reports_if_structured

  failure_policy:
    required_schema_missing: BLOCK_PHASE
    validation_failed_required_field: BLOCK_PHASE
    validation_failed_optional_field: READY_WITH_GAPS
    weak_use_field_missing: PROPAGATE_GAP
```

```yaml
contract_validator_binding:
  binding_id: CONTRACT_VALIDATOR_BINDING
  version: v1.0

  inputs:
    - contract_index
    - handoff_contract_index
    - data_request_packet_index

  validation_targets:
    - input_contracts
    - output_contracts
    - handoff_contracts
    - data_request_packet_contracts

  failure_policy:
    input_contract_invalid: BLOCK_PHASE
    output_contract_invalid: BLOCK_PHASE
    handoff_contract_invalid: BLOCK_HANDOFF
    data_request_contract_invalid: BLOCK_DOWNSTREAM
```

---

# 21. Trace / Acceptance / Handoff Writer Binding

```yaml
trace_writer_binding:
  binding_id: TRACE_WRITER_BINDING
  version: v1.0

  required_trace_types:
    - source_trace
    - field_trace
    - decision_trace
    - validation_trace
    - error_trace
    - acceptance_trace
    - handoff_trace

  write_policy:
    trace_dir_resolved_from_trace_artifact_index: true
    every_output_has_trace_id: true
    every_handoff_has_handoff_trace_id: true
    every_error_has_error_trace: true

  failure_policy:
    trace_write_failed: BLOCK_PHASE
```

```yaml
acceptance_runner_binding:
  binding_id: ACCEPTANCE_RUNNER_BINDING
  version: v1.0

  inputs:
    - phase_acceptance_criteria
    - hard_negative_rules
    - validation_results
    - gap_records
    - trace_records

  outputs:
    - acceptance_result
    - acceptance_trace

  possible_results:
    - READY
    - READY_WITH_GAPS
    - REJECTED
    - BLOCKED

  failure_policy:
    acceptance_not_run: BLOCK_HANDOFF
    blocked_item_used_downstream: HARD_BLOCK
```

```yaml
handoff_writer_binding:
  binding_id: HANDOFF_WRITER_BINDING
  version: v1.0

  inputs:
    - handoff_contract_index
    - phase_output_records
    - acceptance_result
    - trace_records
    - downstream_permission

  outputs:
    - handoff_packet
    - handoff_trace

  failure_policy:
    handoff_missing_required_field: BLOCK_DOWNSTREAM
    handoff_trace_missing: BLOCK_DOWNSTREAM
```

---

# 22. Path Guard Binding

```yaml
path_guard_binding:
  binding_id: PATH_GUARD_BINDING
  version: v1.0

  inputs:
    - canonical_path_policy
    - write_permission_matrix
    - runtime_data_path_index
    - legacy_path_mapping

  checks:
    - output_path_is_registered
    - output_path_belongs_to_current_phase
    - system_file_not_written_to_data_dir
    - runtime_output_not_written_to_system_dir
    - legacy_path_not_written
    - paper_runtime_not_written_before_i04
    - live_execution_path_absent

  failure_policy:
    unregistered_write_path: BLOCK_WRITE
    cross_phase_write: BLOCK_WRITE
    legacy_write_attempt: BLOCK_WRITE
    live_execution_path: HARD_BLOCK
```

---

# 23. Runner Error Policy

```yaml
runner_error_policy:
  policy_id: RUNNER_ERROR_POLICY
  version: v1.0

  error_classes:
    INPUT_MISSING:
      action: BLOCK_PHASE
      trace_required: true

    SCHEMA_VALIDATION_FAILED:
      action: BLOCK_OR_READY_WITH_GAPS_DEPENDING_REQUIRED_LEVEL
      trace_required: true

    CONTRACT_VALIDATION_FAILED:
      action: BLOCK_PHASE
      trace_required: true

    TOOL_UNAVAILABLE:
      action: RETRY_THEN_READY_WITH_GAPS_OR_BLOCK
      trace_required: true

    TOOL_RESPONSE_PARTIAL:
      action: MARK_FIELD_GAPS
      trace_required: true

    PATH_GUARD_FAILED:
      action: HARD_BLOCK
      trace_required: true

    FORBIDDEN_USE_DETECTED:
      action: HARD_BLOCK
      trace_required: true

    ACCEPTANCE_FAILED:
      action: BLOCK_HANDOFF
      trace_required: true

    HANDOFF_WRITE_FAILED:
      action: BLOCK_DOWNSTREAM
      trace_required: true

  common_policy:
    no_silent_failure: true
    every_error_must_have_trace: true
    every_error_must_have_recovery_instruction: true
```

---

# 24. Tool Retry Policy

```yaml
tool_retry_policy:
  policy_id: TOOL_RETRY_POLICY
  version: v1.0

  retry_rules:
    GMGN:
      max_retries: 3
      retry_on:
        - timeout
        - temporary_unavailable
        - partial_response
      no_retry_on:
        - invalid_token_address
        - forbidden
        - malformed_request

    OKX_QUOTE:
      max_retries: 3
      retry_on:
        - timeout
        - stale_quote
        - temporary_unavailable
      no_retry_on:
        - unsupported_token
        - security_block

    OKX_SECURITY:
      max_retries: 2
      retry_on:
        - timeout
        - temporary_unavailable
      no_retry_on:
        - confirmed_security_risk

    KLINE_PROVIDER:
      max_retries: 3
      retry_on:
        - timeout
        - incomplete_candles
      no_retry_on:
        - unsupported_pair

  after_retry_failure:
    required:
      - write_tool_error_trace
      - mark_data_gap
      - propagate_limitation
      - run_acceptance_with_gap
```

---

# 25. Dry-run Validation Matrix

```yaml
dry_run_validation_matrix:
  matrix_id: DRY_RUN_VALIDATION_MATRIX
  version: v1.0

  validation_groups:
    index_reading:
      tests:
        - read_directory_constitution
        - read_phase_controller_file_index
        - read_runtime_data_path_index
        - read_schema_index
        - read_contract_index
        - read_handoff_contract_index

    path_guard:
      tests:
        - block_unregistered_write_path
        - block_legacy_write
        - block_cross_phase_write
        - block_live_execution_path

    schema_contract:
      tests:
        - validate_sample_p01_output
        - validate_sample_p05_evidence_object
        - validate_sample_p07_strategy_gate_decision
        - validate_sample_p08_paper_runtime_permission
        - validate_handoff_packet_common_fields

    tool_binding:
      tests:
        - gmgn_mock_response_maps_to_p02_fact
        - gmgn_wallet_rows_map_to_p03_wallet_entity
        - okx_quote_mock_maps_to_p08_quote_snapshot
        - okx_security_mock_maps_to_p08_security_recheck
        - kline_mock_maps_to_market_structure_seed

    writer_binding:
      tests:
        - trace_writer_creates_trace
        - acceptance_runner_creates_acceptance_result
        - handoff_writer_creates_handoff_packet

    forbidden_use:
      tests:
        - p07_cannot_write_paper_runtime
        - p08_cannot_live_execute
        - p09_cannot_mutate_rules
        - p10_cannot_auto_deploy

  pass_criteria:
    all_blocking_tests_pass: true
    all_live_execution_paths_absent: true
    all_required_indexes_readable: true
    all_required_writers_bound: true
```

---

# 26. I04 Paper Runtime Prerequisite Packet

```yaml
i04_paper_runtime_prerequisite_packet:
  packet_id: string
  packet_type: I04_PAPER_RUNTIME_PREREQUISITE_PACKET
  generated_at: datetime

  from: I03_RUNNER_TOOL_BINDING
  to: I04_PAPER_RUNTIME_INTEGRATION

  prerequisites:
    p08_runner_bound: boolean
    p08_to_paper_runtime_handoff_writer_bound: boolean
    paper_runtime_data_request_packet_contract_bound: boolean
    paper_runtime_permission_schema_bound: boolean
    quote_binding_ready: boolean
    security_binding_ready: boolean
    slippage_cost_model_binding_ready: boolean
    trace_writer_ready: boolean
    acceptance_runner_ready: boolean
    path_guard_ready: boolean
    dry_run_passed: boolean

  required_i04_inputs:
    - p08_to_paper_runtime_handoff_contract
    - paper_runtime_data_request_packet_contract
    - paper_runtime_permission_schema
    - paper_entry_simulation_plan_schema
    - runtime_data_path_index
    - path_guard_binding
    - trace_writer_binding
    - acceptance_runner_binding
    - handoff_writer_binding
    - dry_run_validation_report

  permission_to_enter_i04:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I04_MAY_INTEGRATE_PAPER_RUNTIME
    - PAPER_ONLY
    - NO_LIVE_EXECUTION
    - NO_WALLET_SIGNING
    - NO_AUTO_ORDER
```

---

# 27. I03 to I04 Handoff Packet

```yaml
i03_to_i04_handoff_packet:
  packet_id: string
  packet_type: I03_TO_I04_RUNNER_TOOL_BINDING_HANDOFF
  generated_at: datetime

  route:
    from: I03_RUNNER_TOOL_BINDING
    to: I04_PAPER_RUNTIME_INTEGRATION

  upstream_control:
    i02_handoff_packet_id: string
    i03_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  package_paths:
    runner_capability_registry_path: string
    phase_runner_binding_index_path: string
    tool_binding_index_path: string
    phase_runner_contracts_path: string
    global_runner_orchestrator_contract_path: string
    runner_cli_command_registry_path: string
    environment_config_registry_path: string
    tool_credential_policy_path: string
    gmgn_tool_binding_path: string
    okx_quote_binding_path: string
    okx_security_binding_path: string
    kline_provider_binding_path: string
    legacy_reader_binding_path: string
    schema_validator_binding_path: string
    contract_validator_binding_path: string
    trace_writer_binding_path: string
    acceptance_runner_binding_path: string
    handoff_writer_binding_path: string
    path_guard_binding_path: string
    runner_error_policy_path: string
    tool_retry_policy_path: string
    dry_run_validation_matrix_path: string
    dry_run_validation_report_path: string
    i04_prerequisite_packet_path: string

  i04_required_tasks:
    - bind_paper_runtime_to_p08_handoff
    - create_paper_runtime_input_contract
    - create_paper_position_schema
    - create_paper_trade_schema
    - create_paper_equity_curve_schema
    - create_paper_runtime_event_schema
    - enforce_paper_only_mode
    - apply_slippage_and_cost_model
    - write_paper_runtime_trace
    - generate_paper_runtime_acceptance
    - produce_p09_review_inputs

  permission_to_enter_i04:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I03_BINDING_ONLY
    - I04_PAPER_ONLY_RUNTIME_INTEGRATION_ALLOWED
    - LIVE_EXECUTION_FORBIDDEN
    - WALLET_SIGNING_FORBIDDEN
    - AUTO_ORDER_FORBIDDEN
```

---

# 28. I03 Gap Policy

```yaml
i03_gap_policy:
  BLOCKING_GAP:
    result: I03_BLOCKED
    examples:
      - i02_handoff_missing
      - phase_runner_binding_index_unusable
      - path_guard_missing
      - trace_writer_missing
      - handoff_writer_missing
      - live_execution_path_detected
      - unregistered_write_allowed
      - p08_to_paper_runtime_binding_missing

  CRITICAL_GAP:
    result: I03_REJECTED_OR_FIX_REQUIRED
    examples:
      - schema_validator_missing
      - contract_validator_missing
      - acceptance_runner_missing
      - p07_runner_can_write_paper_runtime
      - p08_runner_can_wallet_sign
      - gmgn_required_mapping_missing
      - okx_quote_required_mapping_missing_for_p08

  HIGH_GAP:
    result: I03_READY_WITH_GAPS
    examples:
      - kline_provider_binding_partial
      - legacy_reader_mapping_partial
      - optional_report_writer_missing
      - retry_policy_incomplete
      - mock_fixture_missing_for_noncritical_tool

  MEDIUM_GAP:
    result: I03_READY_WITH_GAPS
    examples:
      - cli_registry_partial
      - env_config_optional_missing
      - noncritical_field_mapping_missing

  LOW_GAP:
    result: I03_READY_WITH_NOTE
    examples:
      - naming_inconsistency
      - optional_description_missing
      - report_comment_missing
```

---

# 29. I03 Hard Negative Rules

```yaml
i03_hard_negative_rules:
  - rule_id: I03_BLOCK_001
    name: 未读取 I02 handoff
    condition: i02_to_i03_handoff_packet_missing == true
    result: I03_BLOCKED
    reason: I03 必须基于 I02 索引执行

  - rule_id: I03_BLOCK_002
    name: 未绑定 path guard
    condition: path_guard_binding_missing == true
    result: I03_BLOCKED
    reason: 没有路径守卫会重新制造目录混乱

  - rule_id: I03_BLOCK_003
    name: 未绑定 trace writer
    condition: trace_writer_binding_missing == true
    result: I03_BLOCKED
    reason: 无 trace 无法支持 P09 回放

  - rule_id: I03_BLOCK_004
    name: 未绑定 handoff writer
    condition: handoff_writer_binding_missing == true
    result: I03_BLOCKED
    reason: 无 handoff writer 无法推进阶段链

  - rule_id: I03_BLOCK_005
    name: 未绑定 acceptance runner
    condition: acceptance_runner_binding_missing == true
    result: I03_BLOCKED
    reason: 无 acceptance 不能允许下游读取

  - rule_id: I03_BLOCK_006
    name: Runner 允许未登记路径写入
    condition: runner_allows_unregistered_write_path == true
    result: I03_BLOCKED
    reason: 未登记写入必须阻断

  - rule_id: I03_BLOCK_007
    name: P07 runner 可写入 Paper Runtime
    condition: p07_runner_can_write_paper_runtime == true
    result: I03_BLOCKED
    reason: P07 只能输出 PAPER_CANDIDATE，不能启动 runtime

  - rule_id: I03_BLOCK_008
    name: P08 runner 支持钱包签名
    condition: p08_runner_wallet_signing_enabled == true
    result: I03_BLOCKED
    reason: P08 不能签名或真实下单

  - rule_id: I03_BLOCK_009
    name: Tool Binding 使用实盘权限
    condition: tool_binding_uses_live_trade_permission == true
    result: I03_BLOCKED
    reason: 当前只允许 readonly / mock

  - rule_id: I03_BLOCK_010
    name: live execution 路径
    condition: live_execution_allowed == true
    result: I03_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 30. I03 状态机

```yaml
i03_runner_tool_binding_state_machine:
  states:
    - I03_UNINITIALIZED
    - I03_CONTEXT_LOADED
    - I03_I02_HANDOFF_READ
    - I03_INPUT_MANIFEST_BUILT
    - I03_RUNNER_CAPABILITY_REGISTRY_BUILT
    - I03_PHASE_RUNNER_BINDING_BUILT
    - I03_TOOL_BINDING_INDEX_BUILT
    - I03_PHASE_RUNNER_CONTRACTS_BUILT
    - I03_GLOBAL_ORCHESTRATOR_CONTRACT_BUILT
    - I03_CLI_REGISTRY_BUILT
    - I03_ENV_CONFIG_REGISTRY_BUILT
    - I03_CREDENTIAL_POLICY_BUILT
    - I03_GMGN_BINDING_BUILT
    - I03_OKX_QUOTE_BINDING_BUILT
    - I03_OKX_SECURITY_BINDING_BUILT
    - I03_KLINE_BINDING_BUILT
    - I03_LEGACY_READER_BINDING_BUILT
    - I03_SCHEMA_VALIDATOR_BOUND
    - I03_CONTRACT_VALIDATOR_BOUND
    - I03_TRACE_WRITER_BOUND
    - I03_ACCEPTANCE_RUNNER_BOUND
    - I03_HANDOFF_WRITER_BOUND
    - I03_PATH_GUARD_BOUND
    - I03_ERROR_POLICY_BUILT
    - I03_RETRY_POLICY_BUILT
    - I03_DRY_RUN_VALIDATION_BUILT
    - I03_DRY_RUN_VALIDATED
    - I03_I04_PREREQUISITE_PACKET_BUILT
    - I03_REPORT_BUILT
    - I03_I04_HANDOFF_BUILT
    - I03_READY_FOR_ACCEPTANCE
    - I03_ACCEPTANCE_READY
    - I03_READY_FOR_I04_HANDOFF
    - I03_READY_WITH_GAPS
    - I03_REJECTED
    - I03_BLOCKED

  critical_transitions:
    - from: I03_CONTEXT_LOADED
      to: I03_I02_HANDOFF_READ
      condition: i02_to_i03_handoff_packet_available == true

    - from: I03_I02_HANDOFF_READ
      to: I03_INPUT_MANIFEST_BUILT
      condition: i02_indexes_available == true

    - from: I03_INPUT_MANIFEST_BUILT
      to: I03_RUNNER_CAPABILITY_REGISTRY_BUILT
      condition: runner_capability_registry_created == true

    - from: I03_RUNNER_CAPABILITY_REGISTRY_BUILT
      to: I03_PHASE_RUNNER_BINDING_BUILT
      condition: phase_runner_binding_index_created == true

    - from: I03_PHASE_RUNNER_BINDING_BUILT
      to: I03_TOOL_BINDING_INDEX_BUILT
      condition: tool_binding_index_created == true

    - from: I03_TOOL_BINDING_INDEX_BUILT
      to: I03_SCHEMA_VALIDATOR_BOUND
      condition: schema_validator_binding_created == true

    - from: I03_SCHEMA_VALIDATOR_BOUND
      to: I03_CONTRACT_VALIDATOR_BOUND
      condition: contract_validator_binding_created == true

    - from: I03_CONTRACT_VALIDATOR_BOUND
      to: I03_TRACE_WRITER_BOUND
      condition: trace_writer_binding_created == true

    - from: I03_TRACE_WRITER_BOUND
      to: I03_ACCEPTANCE_RUNNER_BOUND
      condition: acceptance_runner_binding_created == true

    - from: I03_ACCEPTANCE_RUNNER_BOUND
      to: I03_HANDOFF_WRITER_BOUND
      condition: handoff_writer_binding_created == true

    - from: I03_HANDOFF_WRITER_BOUND
      to: I03_PATH_GUARD_BOUND
      condition: path_guard_binding_created == true

    - from: I03_PATH_GUARD_BOUND
      to: I03_DRY_RUN_VALIDATION_BUILT
      condition: dry_run_validation_matrix_created == true

    - from: I03_DRY_RUN_VALIDATION_BUILT
      to: I03_DRY_RUN_VALIDATED
      condition: dry_run_validation_report_created == true

    - from: I03_DRY_RUN_VALIDATED
      to: I03_I04_PREREQUISITE_PACKET_BUILT
      condition: i04_prerequisite_packet_created == true

    - from: I03_I04_PREREQUISITE_PACKET_BUILT
      to: I03_I04_HANDOFF_BUILT
      condition: i03_to_i04_handoff_packet_created == true

    - from: I03_I04_HANDOFF_BUILT
      to: I03_READY_FOR_ACCEPTANCE
      condition: i03_report_created == true
```

---

# 31. I03 Acceptance Criteria

```yaml
i03_acceptance_criteria:
  I03_READY:
    required:
      - i02_handoff_read
      - runner_capability_registry_created
      - phase_runner_binding_index_created
      - tool_binding_index_created
      - phase_runner_contracts_created
      - global_runner_orchestrator_contract_created
      - runner_cli_command_registry_created
      - environment_config_registry_created
      - tool_credential_policy_created
      - gmgn_tool_binding_created
      - okx_quote_binding_created
      - okx_security_binding_created
      - kline_provider_binding_created
      - legacy_reader_binding_created
      - schema_validator_binding_created
      - contract_validator_binding_created
      - trace_writer_binding_created
      - acceptance_runner_binding_created
      - handoff_writer_binding_created
      - path_guard_binding_created
      - runner_error_policy_created
      - tool_retry_policy_created
      - dry_run_validation_matrix_created
      - dry_run_validation_report_created
      - i04_prerequisite_packet_created
      - i03_to_i04_handoff_created
      - no_unregistered_write_path
      - no_live_execution_path
      - no_wallet_signing

  I03_READY_WITH_GAPS:
    allowed_when:
      - optional_tool_binding_partial
      - noncritical_kline_mapping_missing
      - optional_report_writer_missing
      - legacy_reader_partial
    required:
      - gaps_recorded
      - i04_permission_is_allowed_with_gaps
      - blocking_gaps_absent

  I03_REJECTED:
    triggered_by:
      - phase_runner_binding_index_unusable
      - tool_binding_index_unusable
      - schema_validator_unusable
      - contract_validator_unusable
      - dry_run_validation_unusable

  I03_BLOCKED:
    triggered_by:
      - i02_handoff_missing
      - path_guard_missing
      - trace_writer_missing
      - handoff_writer_missing
      - acceptance_runner_missing
      - unregistered_write_allowed
      - p07_can_write_paper_runtime
      - p08_wallet_signing_enabled
      - live_execution_allowed
```

---

# 32. I03 测试矩阵

```yaml
i03_test_matrix:
  - test_id: I03_TEST_001
    name: I02 handoff 存在，runner 与工具绑定完整
    expected_status: I03_READY

  - test_id: I03_TEST_002
    name: 缺 I02 handoff
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_003
    name: phase_runner_binding_index 缺失
    expected_status: I03_REJECTED

  - test_id: I03_TEST_004
    name: path_guard 未绑定
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_005
    name: trace_writer 未绑定
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_006
    name: handoff_writer 未绑定
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_007
    name: acceptance_runner 未绑定
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_008
    name: schema_validator 校验失败
    expected_status: I03_REJECTED_OR_BLOCKED

  - test_id: I03_TEST_009
    name: contract_validator 校验失败
    expected_status: I03_REJECTED_OR_BLOCKED

  - test_id: I03_TEST_010
    name: GMGN mock 字段可映射到 P02/P03/P04
    expected_status: I03_READY

  - test_id: I03_TEST_011
    name: OKX quote mock 字段可映射到 P08
    expected_status: I03_READY

  - test_id: I03_TEST_012
    name: OKX security mock 返回高风险
    expected_output: SECURITY_BLOCK_OR_PAUSE_POLICY_VALIDATED

  - test_id: I03_TEST_013
    name: legacy path 尝试写入
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_014
    name: P07 runner 试图写 paper_runtime
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_015
    name: P08 runner 支持 wallet signing
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_016
    name: live execution command registered
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_017
    name: dry-run 未生成 trace
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_018
    name: dry-run 未生成 handoff
    expected_status: I03_BLOCKED

  - test_id: I03_TEST_019
    name: I04 prerequisite packet 未生成
    expected_status: I03_REJECTED

  - test_id: I03_TEST_020
    name: optional kline binding 缺部分字段
    expected_status: I03_READY_WITH_GAPS
```

---

# 33. I03 报告模型

```yaml
i03_runner_tool_binding_report:
  report_id: string
  generated_at: datetime
  controller_id: I03_RUNNER_TOOL_BINDING

  summary:
    phase_runner_count_bound: integer
    tool_binding_count_bound: integer
    validator_count_bound: integer
    writer_count_bound: integer
    dry_run_tests_total: integer
    dry_run_tests_passed: integer
    dry_run_tests_failed: integer
    blocking_gap_count: integer
    critical_gap_count: integer
    high_gap_count: integer
    medium_gap_count: integer
    low_gap_count: integer

  phase_runner_summary:
    p01_bound: boolean
    p02_bound: boolean
    p03_bound: boolean
    p04_bound: boolean
    p05_bound: boolean
    p06_bound: boolean
    p07_bound: boolean
    p08_bound: boolean
    p09_bound: boolean
    p10_bound: boolean

  tool_binding_summary:
    gmgn_binding_status: string
    okx_quote_binding_status: string
    okx_security_binding_status: string
    kline_binding_status: string
    legacy_reader_binding_status: string

  validator_writer_summary:
    schema_validator_ready: boolean
    contract_validator_ready: boolean
    trace_writer_ready: boolean
    acceptance_runner_ready: boolean
    handoff_writer_ready: boolean
    path_guard_ready: boolean

  dry_run_summary:
    index_reading_passed: boolean
    path_guard_passed: boolean
    schema_contract_validation_passed: boolean
    writer_binding_passed: boolean
    forbidden_use_tests_passed: boolean

  i04_readiness:
    i04_prerequisite_packet_created: boolean
    permission_to_enter_i04: string
    reasons_if_blocked: list

  compliance:
    business_logic_changed: false
    legacy_data_deleted_or_moved: false
    unregistered_write_path_allowed: false
    p07_writes_paper_runtime: false
    p08_wallet_signing_enabled: false
    live_execution_path_detected: false
```

---

# 34. HER I03 执行协议

```text
HER 执行 I03 时必须按以下顺序：

1. 读取 system_methodology_blueprint.md
2. 读取 professional_build_order.md
3. 读取 I02→I03 handoff packet
4. 读取 I03 prerequisite packet
5. 读取 directory_constitution_final
6. 读取 phase_controller_file_index
7. 读取 runtime_data_path_index
8. 读取 schema_index
9. 读取 contract_index
10. 读取 handoff_contract_index
11. 读取 data_request_packet_index
12. 读取 read_order_manifest
13. 读取 write_permission_matrix
14. 读取 legacy_path_mapping
15. 读取 canonical_path_policy
16. 建立 i03_input_manifest
17. 建立 runner_capability_registry
18. 建立 phase_runner_binding_index
19. 建立 tool_binding_index
20. 建立 phase_runner_contracts
21. 建立 global_runner_orchestrator_contract
22. 建立 runner_cli_command_registry
23. 建立 environment_config_registry
24. 建立 tool_credential_policy
25. 建立 GMGN tool binding
26. 建立 OKX quote binding
27. 建立 OKX security binding
28. 建立 Kline provider binding
29. 建立 legacy reader binding
30. 建立 schema validator binding
31. 建立 contract validator binding
32. 建立 trace writer binding
33. 建立 acceptance runner binding
34. 建立 handoff writer binding
35. 建立 path guard binding
36. 建立 runner_error_policy
37. 建立 tool_retry_policy
38. 建立 dry_run_validation_matrix
39. 执行 dry-run validation，输出 dry_run_validation_report
40. 生成 i04_paper_runtime_prerequisite_packet
41. 生成 i03_runner_tool_binding_report
42. 生成 i03_to_i04_handoff_packet
43. 生成 i03_acceptance_result
44. 只允许 handoff 给 I04
```

禁止：

```text
1. 不允许无 I02 handoff 启动 I03
2. 不允许新增 P11 / P12 / P13
3. 不允许修改 P01-P10 业务逻辑
4. 不允许启动 Paper Runtime
5. 不允许删除或移动 legacy 数据
6. 不允许写入 legacy runtime path
7. 不允许未登记路径写入
8. 不允许 P07 写入 Paper Runtime
9. 不允许 P08 钱包签名
10. 不允许注册 live execution 命令
11. 不允许自动部署
12. 不允许 live execution
```

---

# 35. 给 HER 的正式任务书

```text
任务名称：I03 Runner / Tool Binding：阶段运行器与工具绑定任务包

目标：
在 /root/sikk-gmgn/system/integration_program/I03_runner_tool_binding/ 下建立 I03 Runner / Tool Binding 任务包，并在 /root/sikk-gmgn/data/integration_program/I03_runner_tool_binding/ 下生成运行绑定输出。I03 不是 P13，不新增业务判断能力，不修改 P01-P10 业务逻辑。它的目标是在 I02 完成目录、schema、contract、handoff、runtime path、legacy mapping 统一索引之后，把 P01-P10 阶段控制器绑定到可执行 runner，把 GMGN、OKX Quote、OKX Security、Kline、Legacy Reader、Schema Validator、Contract Validator、Trace Writer、Acceptance Runner、Handoff Writer、Path Guard 绑定到标准执行协议，并通过 dry-run 验证后生成 I04 Paper-only Runtime Integration 的前置条件包。

核心原则：
1. I03 是 Integration Program 第三步，不是新业务阶段。
2. I03 只做 runner / tool / validator / writer / path guard 绑定。
3. I03 不修改 P01-P10 业务逻辑。
4. I03 不启动 Paper Runtime。
5. I03 不真实下单。
6. I03 不钱包签名。
7. I03 不自动部署。
8. I03 不删除或移动 legacy 数据。
9. I03 必须读取 I02 handoff 和 I02 索引。
10. I03 必须建立 phase_runner_binding_index。
11. I03 必须建立 tool_binding_index。
12. I03 必须建立 schema_validator_binding。
13. I03 必须建立 contract_validator_binding。
14. I03 必须建立 trace_writer_binding。
15. I03 必须建立 acceptance_runner_binding。
16. I03 必须建立 handoff_writer_binding。
17. I03 必须建立 path_guard_binding。
18. I03 必须建立 GMGN / OKX / Kline / Legacy Reader 绑定。
19. I03 必须建立 runner_error_policy 和 tool_retry_policy。
20. I03 必须执行 dry-run validation。
21. I03 必须生成 I04 Paper Runtime Prerequisite Packet。
22. I03 只能交接给 I04 Paper-only Runtime Integration。
23. I03 必须全局阻断 live execution、wallet signing、auto order。

需要创建系统目录：
/root/sikk-gmgn/system/integration_program/I03_runner_tool_binding/

需要创建系统文件：
1. i03_runner_tool_binding_controller.yaml
2. i03_runner_tool_binding_context.md
3. i03_input_contract.yaml
4. i03_output_contract.yaml
5. i03_input_manifest_schema.yaml
6. runner_capability_registry_schema.yaml
7. phase_runner_binding_index_schema.yaml
8. tool_binding_index_schema.yaml
9. phase_runner_contract_schema.yaml
10. global_runner_orchestrator_contract_schema.yaml
11. runner_cli_command_registry_schema.yaml
12. environment_config_registry_schema.yaml
13. tool_credential_policy_schema.yaml
14. gmgn_tool_binding_schema.yaml
15. okx_quote_binding_schema.yaml
16. okx_security_binding_schema.yaml
17. kline_provider_binding_schema.yaml
18. legacy_reader_binding_schema.yaml
19. schema_validator_binding_schema.yaml
20. contract_validator_binding_schema.yaml
21. trace_writer_binding_schema.yaml
22. acceptance_runner_binding_schema.yaml
23. handoff_writer_binding_schema.yaml
24. path_guard_binding_schema.yaml
25. runner_error_policy_schema.yaml
26. tool_retry_policy_schema.yaml
27. dry_run_validation_matrix_schema.yaml
28. i04_paper_runtime_prerequisite_packet_contract.yaml
29. i03_to_i04_handoff_contract.yaml
30. i03_binding_policy.yaml
31. i03_hard_negative_rules.yaml
32. i03_state_machine.yaml
33. i03_trace_requirements.yaml
34. i03_acceptance_criteria.md
35. i03_storage_constitution.md
36. i03_test_matrix.yaml
37. i03_report_model.yaml
38. i03_review_checklist.md
39. her_i03_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/integration_program/I03_runner_tool_binding/
  input_manifest/
  runner_capabilities/
  phase_runner_binding/
  tool_binding/
  phase_runner_contracts/
  orchestrator_contract/
  cli_registry/
  env_config/
  credential_policy/
  gmgn_binding/
  okx_quote_binding/
  okx_security_binding/
  kline_binding/
  legacy_reader_binding/
  schema_validator/
  contract_validator/
  trace_writer/
  acceptance_runner/
  handoff_writer/
  path_guard/
  error_policy/
  retry_policy/
  dry_run/
  i04_prerequisites/
  i04_handoff/
  reports/
  audit/
  trace/
  acceptance/

每个文件要求：
- i03_runner_tool_binding_controller.yaml：定义 I03 身份、职责、权限、上下游、状态码、禁止事项。
- i03_runner_tool_binding_context.md：写成 HER 执行前必须读取的 I03 上下文。
- i03_input_contract.yaml：定义 I03 必须读取的 I02 handoff、I02 indexes、phase controller files、legacy mapping。
- i03_output_contract.yaml：定义 runner binding、tool binding、validator binding、writer binding、dry-run、I04 prerequisite、handoff 输出。
- i03_input_manifest_schema.yaml：定义 I03 输入清单。
- runner_capability_registry_schema.yaml：定义 runner 能力注册。
- phase_runner_binding_index_schema.yaml：定义 P01-P10 每阶段 runner 绑定。
- tool_binding_index_schema.yaml：定义 GMGN / OKX / Kline / Legacy / Writer 工具绑定。
- phase_runner_contract_schema.yaml：定义阶段 runner 的通用执行合约。
- global_runner_orchestrator_contract_schema.yaml：定义总控 runner 编排合约。
- runner_cli_command_registry_schema.yaml：定义 HER / CLI 可调用命令。
- environment_config_registry_schema.yaml：定义环境变量、模式、路径、readonly 限制。
- tool_credential_policy_schema.yaml：定义工具凭证和密钥边界，只允许 readonly / mock。
- gmgn_tool_binding_schema.yaml：定义 GMGN 字段映射、质量标签、错误处理。
- okx_quote_binding_schema.yaml：定义 OKX quote 到 P08 quote snapshot / consistency 的映射。
- okx_security_binding_schema.yaml：定义 OKX security 到 P02 / P08 安全记录的映射。
- kline_provider_binding_schema.yaml：定义 K线和市场结构字段映射。
- legacy_reader_binding_schema.yaml：定义 legacy 只读读取与 trace wrapper。
- schema_validator_binding_schema.yaml：定义 schema validator。
- contract_validator_binding_schema.yaml：定义 contract validator。
- trace_writer_binding_schema.yaml：定义 trace writer。
- acceptance_runner_binding_schema.yaml：定义 acceptance runner。
- handoff_writer_binding_schema.yaml：定义 handoff writer。
- path_guard_binding_schema.yaml：定义路径守卫。
- runner_error_policy_schema.yaml：定义 runner 错误处理。
- tool_retry_policy_schema.yaml：定义工具失败重试。
- dry_run_validation_matrix_schema.yaml：定义 dry-run 验证矩阵。
- i04_paper_runtime_prerequisite_packet_contract.yaml：定义 I04 前置条件包。
- i03_to_i04_handoff_contract.yaml：定义 I03_TO_I04 handoff packet。
- i03_binding_policy.yaml：定义 I03 绑定政策。
- i03_hard_negative_rules.yaml：定义无 I02 handoff、无 path guard、无 trace writer、无 handoff writer、无 acceptance runner、P07 写 Paper Runtime、P08 钱包签名、live execution 等阻断。
- i03_state_machine.yaml：定义 I03 全状态机。
- i03_trace_requirements.yaml：定义 I03 trace。
- i03_acceptance_criteria.md：定义 I03_READY / READY_WITH_GAPS / REJECTED / BLOCKED。
- i03_storage_constitution.md：定义系统文件和运行数据目录。
- i03_test_matrix.yaml：定义至少 20 个测试场景。
- i03_report_model.yaml：定义 I03 人类可读报告。
- i03_review_checklist.md：定义 I03 审计清单。
- her_i03_execution_protocol.md：定义 HER 执行 I03 的顺序和禁止事项。

运行输出要求：
1. i03_input_manifest.yaml
2. runner_capability_registry.yaml
3. phase_runner_binding_index.yaml
4. tool_binding_index.yaml
5. phase_runner_contract.yaml
6. global_runner_orchestrator_contract.yaml
7. runner_cli_command_registry.yaml
8. environment_config_registry.yaml
9. tool_credential_policy.yaml
10. gmgn_tool_binding.yaml
11. okx_quote_binding.yaml
12. okx_security_binding.yaml
13. kline_provider_binding.yaml
14. legacy_reader_binding.yaml
15. schema_validator_binding.yaml
16. contract_validator_binding.yaml
17. trace_writer_binding.yaml
18. acceptance_runner_binding.yaml
19. handoff_writer_binding.yaml
20. path_guard_binding.yaml
21. runner_error_policy.yaml
22. tool_retry_policy.yaml
23. dry_run_validation_matrix.yaml
24. dry_run_validation_report.md
25. i04_paper_runtime_prerequisite_packet.yaml
26. i03_runner_tool_binding_report.md
27. i03_to_i04_handoff_packet.yaml
28. i03_acceptance_result.yaml

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. runner_capability_registry 摘要
4. phase_runner_binding_index 摘要
5. tool_binding_index 摘要
6. phase_runner_contract 摘要
7. global_runner_orchestrator_contract 摘要
8. runner_cli_command_registry 摘要
9. environment_config_registry 摘要
10. credential policy 摘要
11. GMGN binding 摘要
12. OKX quote binding 摘要
13. OKX security binding 摘要
14. Kline binding 摘要
15. Legacy reader binding 摘要
16. Schema / Contract validator 摘要
17. Trace / Acceptance / Handoff writer 摘要
18. Path guard 摘要
19. Error / Retry policy 摘要
20. Dry-run validation 摘要
21. I04 prerequisite packet 摘要
22. I03→I04 handoff 摘要
23. 是否允许进入 I04
24. 是否达到轻量机构级 I03 v1.0

最终验收标准：
只有当 I03 具备 runner capability registry、phase runner binding index、tool binding index、phase runner contract、global runner orchestrator contract、runner CLI command registry、environment config registry、tool credential policy、GMGN binding、OKX quote binding、OKX security binding、Kline provider binding、legacy reader binding、schema validator、contract validator、trace writer、acceptance runner、handoff writer、path guard、runner error policy、tool retry policy、dry-run validation matrix、dry-run validation report、I04 prerequisite packet、I03→I04 handoff、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且没有未登记路径写入、没有 P07 绕过 P08、没有 P08 钱包签名、没有 live execution path 时，才允许标记为 I03_READY。
```

---

# 36. 当前是否达到专业化 I03 设计标准

## 判断

这一版 I03 达到：

```text
专业化
轻量机构水准
一次性把 I03 应有绑定对象补全
不是最小版本
不是普通脚本清单
不是继续新增业务阶段
```

I03 被明确设计为：

```text
阶段 runner 绑定层
工具 adapter 绑定层
字段映射层
schema / contract 校验层
trace / acceptance / handoff writer 层
path guard 层
error / retry policy 层
dry-run validation 层
I04 Paper Runtime 前置层
```

---

# 37. I03 完成后下一步

I03 完成后进入：

```text
I04 Paper-only Runtime Integration
```

I04 才负责：

```text
Paper Runtime 读取 P08 handoff
创建纸面仓位
应用有效入场价
应用滑点与费用模型
写入 paper trades
写入 open / closed positions
写入 equity curve
写入 runtime events
写入 risk events
为 P09 生成 review replay 输入
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|runner 是否已经真实存在|I03 建立绑定和 dry-run 要求|实现任务中创建或补齐 runner|
|GMGN / OKX 实际字段是否完全匹配|I03 建字段映射|dry-run / mock / real readonly 校验|
|Paper Runtime 是否能写仓位|I03 不启动 runtime|I04 联调|
|滑点与费用模型是否真实|I03 只绑定模型接口|I04 / P09 / P10 校准|
|legacy 数据是否能被 P09 使用|I03 建只读 reader|I05 回放验证|
|Telegram 面板是否接入|I03 不处理面板|后续 Runner / Ops 层扩展|
|自动部署是否允许|不允许|P10 受控升级后仍需审批|

---

# 本次认知升级点

1. **I03 的本质不是写脚本，而是建立阶段执行协议。**
    
2. **Runner 必须绑定 schema、contract、trace、acceptance、handoff。**  
    只会读写文件的脚本不具备机构级系统能力。
    
3. **Tool Binding 的核心是字段治理，不是 API 调用。**
    
4. **所有 runner 必须先读取 I02 索引。**  
    不能自己猜路径、猜 schema、猜合约。
    
5. **Path Guard 是 I03 的硬门。**  
    没有路径守卫，目录混乱会再次发生。
    
6. **I03 只能 dry-run，不进入 Paper Runtime。**
    
7. **P07 → P08 → Paper Runtime 的边界必须在 runner 层强制阻断。**
    
8. **I03 完成后，系统才具备进入 I04 Paper-only Runtime 联调的工程条件。**