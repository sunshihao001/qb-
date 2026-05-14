# I02 Directory & Contract Index Unification 专业版 v1.0

## 目录、合约、Schema、Handoff、运行数据路径与 Legacy 映射统一任务包

---

## 0. I02 的核心定位

I02 不是新的业务阶段，也不是 P12。

它属于：

```text
Integration Program：系统集成落地计划
```

I02 的专业定义：

```text
I02 Directory & Contract Index Unification 是在 I01 全阶段一致性审计之后，对 P01-P10 全部系统目录、合约、schema、handoff、data request、trace、acceptance、report、runtime data path、legacy path 进行统一登记、规范化、索引化和可寻址化的任务包。
```

一句话：

> **I01 负责发现 P01-P10 哪里断、哪里乱、哪里不一致。**  
> **I02 负责把所有阶段文件、目录、合约、schema、handoff、runtime 输出路径统一成 HER / Runner 可读取的索引系统。**

---

# 1. I02 不负责什么

I02 必须避免越权。

```text
I02 不新增 P11 / P12
I02 不修改 P01-P10 业务判断逻辑
I02 不直接写 Runner
I02 不直接绑定 GMGN / OKX / K线工具
I02 不启动 Paper Runtime
I02 不改策略规则
I02 不修正交易阈值
I02 不生成买卖信号
I02 不自动迁移 legacy 数据
I02 不删除旧目录
I02 不自动部署
I02 不允许 live execution
```

I02 只做：

```text
统一目录
统一命名
统一索引
统一路径解析
统一合约登记
统一 schema 登记
统一 handoff 登记
统一 runtime data path
统一 legacy path mapping
生成 I03 Runner / Tool Binding 所需输入
```

---

# 2. I02 的阶段目标

I02 必须一次性解决 18 类问题：

|编号|问题|I02 必须输出|
|---|---|---|
|1|系统主根目录是什么？|`canonical_root_declaration`|
|2|P01-P10 系统文件在哪里？|`phase_controller_file_index`|
|3|P01-P10 运行数据写到哪里？|`runtime_data_path_index`|
|4|每个 schema 文件在哪里？|`schema_index`|
|5|每个 contract 文件在哪里？|`contract_index`|
|6|每个 handoff contract 在哪里？|`handoff_contract_index`|
|7|每个 data request packet contract 在哪里？|`data_request_packet_index`|
|8|每个 trace / acceptance / report model 在哪里？|`control_artifact_index`|
|9|文件命名是否统一？|`file_naming_policy`|
|10|目录命名是否统一？|`directory_naming_policy`|
|11|哪些是 canonical path？|`canonical_path_policy`|
|12|哪些是 legacy path？|`legacy_path_mapping`|
|13|legacy 数据如何只读吸收？|`legacy_readonly_absorption_policy`|
|14|哪些文件缺失但不能伪造？|`index_gap_report`|
|15|哪些路径冲突、重复、过期？|`path_conflict_report`|
|16|HER / Runner 应按什么顺序读取？|`read_order_manifest`|
|17|I03 需要绑定哪些 runner 和工具？|`i03_runner_tool_binding_prerequisite_packet`|
|18|是否可以进入 I03？|`i02_to_i03_handoff_packet`|

---

# 3. I02 的底层方法论

## 3.1 目录不是文件夹，是系统寻址协议

普通项目把目录当文件夹。  
专业系统必须把目录当成：

```text
阶段身份
输入边界
输出边界
权限边界
审计边界
复盘边界
工具绑定边界
```

如果目录不标准，后面会出现：

```text
HER 找不到文件
Runner 读错路径
P09 无法复盘
P10 无法生成升级包
旧数据和新数据混在一起
runtime 输出污染系统文件
```

---

## 3.2 Contract 是阶段之间的法律文本

I02 不能只列文件名。  
它必须建立：

```text
谁输出
谁读取
输出对象是什么
schema 在哪里
contract 在哪里
handoff 在哪里
字段权限是什么
缺口如何传递
是否允许 runtime 使用
```

否则 P01-P10 虽然看起来完整，但无法工程化运行。

---

## 3.3 Schema Index 不是清单，是字段治理入口

Schema Index 必须回答：

```text
哪个对象由哪个阶段生成？
字段定义在哪里？
是否必须有 trace？
是否允许 weak_use？
是否可进入下游？
是否可被 Runner 校验？
```

---

## 3.4 Legacy 目录必须保留但不能污染 canonical path

你现在已有旧运行数据，例如：

```text
/root/sikk-gmgn/data/gmgn_candidates_live_run/
```

专业处理方式不是移动、删除或强行合并，而是：

```text
legacy_runtime_keep_in_place
legacy_readonly
legacy_path_mapping
legacy_absorption_plan
```

也就是：

```text
旧数据保留原地
新系统不把旧路径当主写入路径
Runner 通过 mapping 读取旧数据
新数据写入 canonical runtime path
```

---

## 3.5 I02 可以建立索引，但不能伪造真实存在

如果某个 contract 实际不存在，I02 不能写：

```text
exists: true
```

只能写：

```yaml
exists: false
expected_path: ...
required_before_i03: true
fix_target: I02_OR_P01_P10_PATCH
```

这点非常关键。  
专业系统宁可标记缺失，也不能制造虚假的完整性。

---

# 4. I02 的输入范围

I02 必须读取 I01 输出和系统总索引。

```yaml
i02_required_inputs:
  from_i01:
    - i01_to_i02_handoff_packet
    - full_phase_consistency_audit_report
    - phase_inventory
    - phase_io_alignment_matrix
    - handoff_chain_integrity_report
    - data_request_chain_report
    - schema_contract_coverage_report
    - status_code_consistency_report
    - gap_propagation_report
    - forbidden_use_inheritance_report
    - trace_coverage_report
    - acceptance_coverage_report
    - phase_boundary_violation_report
    - runtime_readiness_precheck_report
    - review_upgrade_readiness_report
    - audit_findings
    - fix_priority_list
    - i01_acceptance_result

  from_system_blueprint:
    - system_methodology_blueprint.md
    - professional_build_order.md
    - phase_controller_index.yaml
    - directory_constitution.md
    - contract_index.md
    - schema_index.md
    - global_status_code_table.md
    - global_hard_negative_rules.md
    - her_total_control_execution_protocol.md
    - professional_baseline_acceptance.md

  from_phase_controllers:
    - P01 system directory
    - P02 system directory
    - P03 system directory
    - P04 system directory
    - P05 system directory
    - P06 system directory
    - P07 system directory
    - P08 system directory
    - P09 system directory
    - P10 system directory

  from_existing_runtime:
    - /root/sikk-gmgn/data/gmgn_candidates_live_run/
    - /root/sikk-gmgn/data/source_wallet_bot/
    - /root/sikk-gmgn/data/intel_bot/
    - existing paper_live outputs
    - existing quote_security outputs
    - existing state_machine outputs
    - existing reports
```

---

# 5. I02 必须建立的核心对象

|对象|作用|
|---|---|
|`I02 Input Manifest`|记录 I02 读取了哪些 I01 和系统文件|
|`Canonical Root Declaration`|定义系统唯一主根目录|
|`Final Directory Constitution`|最终目录宪法|
|`Phase Controller File Index`|P01-P10 文件索引|
|`Runtime Data Path Index`|运行数据路径索引|
|`Artifact Type Registry`|文件类型注册表|
|`Schema Index`|全 schema 索引|
|`Contract Index`|全 contract 索引|
|`Handoff Contract Index`|全 handoff 合约索引|
|`Data Request Packet Index`|全 data request packet 索引|
|`Trace Artifact Index`|trace 文件索引|
|`Acceptance Artifact Index`|acceptance 文件索引|
|`Report Model Index`|report model 索引|
|`Read Order Manifest`|HER / Runner 读取顺序|
|`Write Permission Matrix`|哪些阶段可写哪些目录|
|`Legacy Path Mapping`|旧目录映射|
|`Canonical Path Policy`|新系统标准路径策略|
|`Path Conflict Report`|路径冲突报告|
|`Index Gap Report`|索引缺口报告|
|`I03 Runner Tool Binding Prerequisite Packet`|I03 前置条件包|
|`I02 to I03 Handoff Packet`|I02 → I03 交接包|

---

# 6. I02 运行目录设计

## 6.1 系统目录

```text
/root/sikk-gmgn/system/integration_program/I02_directory_contract_index_unification/
```

必须创建：

```text
i02_directory_contract_index_unification_controller.yaml
i02_directory_contract_index_unification_context.md
i02_input_contract.yaml
i02_output_contract.yaml
i02_input_manifest_schema.yaml
canonical_root_declaration_schema.yaml
final_directory_constitution_schema.yaml
phase_controller_file_index_schema.yaml
runtime_data_path_index_schema.yaml
artifact_type_registry_schema.yaml
schema_index_schema.yaml
contract_index_schema.yaml
handoff_contract_index_schema.yaml
data_request_packet_index_schema.yaml
trace_artifact_index_schema.yaml
acceptance_artifact_index_schema.yaml
report_model_index_schema.yaml
read_order_manifest_schema.yaml
write_permission_matrix_schema.yaml
legacy_path_mapping_schema.yaml
canonical_path_policy_schema.yaml
path_conflict_report_schema.yaml
index_gap_report_schema.yaml
i03_runner_tool_binding_prerequisite_packet_contract.yaml
i02_to_i03_handoff_contract.yaml
i02_unification_policy.yaml
i02_legacy_absorption_policy.yaml
i02_hard_negative_rules.yaml
i02_state_machine.yaml
i02_trace_requirements.yaml
i02_acceptance_criteria.md
i02_storage_constitution.md
i02_test_matrix.yaml
i02_report_model.yaml
i02_review_checklist.md
her_i02_execution_protocol.md
```

---

## 6.2 运行数据目录

```text
/root/sikk-gmgn/data/integration_program/I02_directory_contract_index_unification/
  input_manifest/
  canonical_root/
  directory_constitution/
  phase_file_index/
  runtime_data_path_index/
  artifact_type_registry/
  schema_index/
  contract_index/
  handoff_contract_index/
  data_request_packet_index/
  trace_artifact_index/
  acceptance_artifact_index/
  report_model_index/
  read_order/
  write_permissions/
  legacy_mapping/
  canonical_path_policy/
  path_conflicts/
  index_gaps/
  i03_prerequisites/
  i03_handoff/
  reports/
  audit/
  trace/
  acceptance/
```

---

# 7. Canonical Root Declaration

```yaml
canonical_root_declaration:
  declaration_id: string
  generated_at: datetime

  canonical_root:
    root_path: /root/sikk-gmgn
    status: ACTIVE_CANONICAL_ROOT
    reason_cn: 当前项目代码、系统目录、运行数据、HER 任务包统一归入该根目录

  forbidden_roots_for_new_write:
    - /root/sikk
    - /root/sikk-wallet-intel
    - any_unspecified_temp_root

  allowed_legacy_roots:
    - legacy_root: /root/sikk-gmgn/data/gmgn_candidates_live_run
      status: LEGACY_RUNTIME_KEEP_IN_PLACE
      write_permission: READ_ONLY_UNLESS_LEGACY_COMPAT_RUNNER
      migration_policy: DO_NOT_MOVE_AUTOMATICALLY

    - legacy_root: /root/sikk-gmgn/data/source_wallet_bot
      status: SOURCE_WALLET_LEGACY_AND_TRANSITIONAL
      write_permission: CONTROLLED_BY_MAPPING

    - legacy_root: /root/sikk-gmgn/data/intel_bot
      status: INTEL_BOT_LEGACY_AND_TRANSITIONAL
      write_permission: CONTROLLED_BY_MAPPING

  root_policy:
    new_system_files_must_use: /root/sikk-gmgn/system
    new_runtime_outputs_must_use: /root/sikk-gmgn/data
    new_integration_outputs_must_use: /root/sikk-gmgn/data/integration_program
    no_unregistered_write_paths: true
```

---

# 8. Final Directory Constitution

```yaml
final_directory_constitution:
  constitution_id: string
  generated_at: datetime
  version: v1.0

  top_level_dirs:
    system:
      path: /root/sikk-gmgn/system
      purpose_cn: 系统设计、控制器、合约、schema、策略、集成任务包
      write_policy: CONTROLLED_SYSTEM_WRITE

    data:
      path: /root/sikk-gmgn/data
      purpose_cn: 运行数据、候选数据、阶段输出、runtime 输出、审计输出
      write_policy: CONTROLLED_RUNTIME_WRITE

    schemas:
      path: /root/sikk-gmgn/schemas
      purpose_cn: 全局共享 schema，可选集中式路径
      write_policy: CONTROLLED_SCHEMA_WRITE

    contracts:
      path: /root/sikk-gmgn/contracts
      purpose_cn: 全局共享 handoff / input / output 合约，可选集中式路径
      write_policy: CONTROLLED_CONTRACT_WRITE

    tests:
      path: /root/sikk-gmgn/tests
      purpose_cn: 单元测试、集成测试、回放测试
      write_policy: CONTROLLED_TEST_WRITE

    tools:
      path: /root/sikk-gmgn/tools
      purpose_cn: runner、CLI、工具绑定、trace writer、acceptance runner
      write_policy: CONTROLLED_TOOL_WRITE

    docs:
      path: /root/sikk-gmgn/docs
      purpose_cn: 系统文档、报告、说明、方法论
      write_policy: CONTROLLED_DOC_WRITE

  system_subdirs:
    phase_controllers:
      path: /root/sikk-gmgn/system/phase_controllers
      children:
        - p01_candidate_intake_controller
        - p02_source_data_fact_controller
        - p03_wallet_entity_controller
        - p04_chip_structure_controller
        - p05_evidence_controller
        - p06_scenario_recognition_controller
        - p07_strategy_gate_controller
        - p08_execution_risk_controller
        - p09_review_replay_controller
        - p10_self_upgrade_controller

    integration_program:
      path: /root/sikk-gmgn/system/integration_program
      children:
        - I01_full_phase_consistency_audit
        - I02_directory_contract_index_unification
        - I03_runner_tool_binding
        - I04_paper_runtime_integration
        - I05_review_upgrade_closed_loop

  data_subdirs:
    phase_controllers:
      path: /root/sikk-gmgn/data/phase_controllers
    integration_program:
      path: /root/sikk-gmgn/data/integration_program
    paper_runtime:
      path: /root/sikk-gmgn/data/paper_runtime
    reports:
      path: /root/sikk-gmgn/data/reports
    legacy:
      path: /root/sikk-gmgn/data/legacy_mapping

  hard_rules:
    - system_files_and_runtime_outputs_must_not_mix
    - legacy_paths_must_not_be_deleted_by_i02
    - new_write_paths_must_be_registered
    - runner_must_read_indexes_before_execution
    - every_path_must_have_owner_and_permission
```

---

# 9. Artifact Type Registry

I02 必须把文件类型统一，否则后续 Runner 不知道哪些文件是系统文件、运行数据、合约或报告。

```yaml
artifact_type_registry:
  registry_id: ARTIFACT_TYPE_REGISTRY
  version: v1.0

  artifact_types:
    CONTROLLER_YAML:
      suffix: _controller.yaml
      location: system
      purpose_cn: 阶段身份、职责、权限、上下游、状态码
      runner_read_required: true

    CONTEXT_MD:
      suffix: _context.md
      location: system
      purpose_cn: HER 执行前读取的阶段上下文压缩包
      runner_read_required: true

    INPUT_CONTRACT:
      suffix: _input_contract.yaml
      location: system
      purpose_cn: 阶段输入合约
      runner_read_required: true

    OUTPUT_CONTRACT:
      suffix: _output_contract.yaml
      location: system
      purpose_cn: 阶段输出合约
      runner_read_required: true

    SCHEMA:
      suffix: _schema.yaml
      location: system
      purpose_cn: 输出对象结构定义
      runner_validation_required: true

    HANDOFF_CONTRACT:
      suffix: _handoff_contract.yaml
      location: system
      purpose_cn: 阶段间交接包合约
      runner_validation_required: true

    DATA_REQUEST_PACKET_CONTRACT:
      suffix: _data_request_packet_contract.yaml
      location: system
      purpose_cn: 下游数据请求包合约
      runner_validation_required: true

    STATE_MACHINE:
      suffix: _state_machine.yaml
      location: system
      purpose_cn: 阶段状态机
      runner_read_required: true

    HARD_NEGATIVE_RULES:
      suffix: _hard_negative_rules.yaml
      location: system
      purpose_cn: 阻断规则
      runner_read_required: true

    GAP_POLICY:
      suffix: _gap_policy.yaml
      location: system
      purpose_cn: 缺口分级与传递规则
      runner_read_required: true

    TRACE_REQUIREMENTS:
      suffix: _trace_requirements.yaml
      location: system
      purpose_cn: trace 写入要求
      runner_read_required: true

    ACCEPTANCE_CRITERIA:
      suffix: _acceptance_criteria.md
      location: system
      purpose_cn: 阶段验收标准
      runner_read_required: true

    TEST_MATRIX:
      suffix: _test_matrix.yaml
      location: system
      purpose_cn: 测试矩阵
      runner_or_ci_required: true

    REPORT_MODEL:
      suffix: _report_model.yaml
      location: system
      purpose_cn: 人类可读报告结构
      report_generator_required: true

    RUNTIME_OUTPUT:
      suffix: .yaml_or_json_or_csv_or_md
      location: data
      purpose_cn: 阶段运行输出
      trace_required: true

    HANDOFF_PACKET:
      suffix: _handoff_packet.yaml
      location: data
      purpose_cn: 实际运行交接包
      trace_required: true
```

---

# 10. Phase Controller File Index

```yaml
phase_controller_file_index:
  index_id: PHASE_CONTROLLER_FILE_INDEX
  generated_at: datetime

  phases:
    P01:
      phase_name: Candidate Intake Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller
      required_files:
        controller_yaml:
          expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_candidate_intake_controller.yaml
          exists: boolean
          status: FOUND | MISSING | NEEDS_RENAME
        context_md:
          expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_candidate_intake_context.md
          exists: boolean
        input_contract:
          expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_input_contract.yaml
          exists: boolean
        output_contract:
          expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_output_contract.yaml
          exists: boolean
        state_machine:
          expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/candidate_intake_state_machine.yaml
          exists: boolean
        hard_negative_rules:
          expected_path: string
          exists: boolean
        gap_policy:
          expected_path: string
          exists: boolean
        trace_requirements:
          expected_path: string
          exists: boolean
        acceptance_criteria:
          expected_path: string
          exists: boolean
        test_matrix:
          expected_path: string
          exists: boolean
        report_model:
          expected_path: string
          exists: boolean
        handoff_contract:
          expected_path: string
          exists: boolean
        data_request_packet_contract:
          expected_path: string
          exists: boolean

    P02:
      phase_name: Source Data Fact Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p02_source_data_fact_controller

    P03:
      phase_name: Wallet Entity Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p03_wallet_entity_controller

    P04:
      phase_name: Chip Structure Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p04_chip_structure_controller

    P05:
      phase_name: Evidence Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p05_evidence_controller

    P06:
      phase_name: Scenario Recognition Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p06_scenario_recognition_controller

    P07:
      phase_name: Strategy Gate Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p07_strategy_gate_controller

    P08:
      phase_name: Execution Risk Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p08_execution_risk_controller

    P09:
      phase_name: Review Replay Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p09_review_replay_controller

    P10:
      phase_name: Self Upgrade Controller
      system_dir: /root/sikk-gmgn/system/phase_controllers/p10_self_upgrade_controller

  index_status:
    - COMPLETE
    - COMPLETE_WITH_GAPS
    - MISSING_CRITICAL_FILES
    - UNUSABLE
```

---

# 11. Runtime Data Path Index

```yaml
runtime_data_path_index:
  index_id: RUNTIME_DATA_PATH_INDEX
  generated_at: datetime

  phase_runtime_paths:
    P01:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake
      required_subdirs:
        - input_manifest
        - candidate_master
        - discovery_context
        - source_requests
        - quality
        - gaps
        - trace
        - acceptance
        - handoff
        - reports
        - audit

    P02:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p02_source_data_fact

    P03:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p03_wallet_entity

    P04:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p04_chip_structure

    P05:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p05_evidence

    P06:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p06_scenario_recognition

    P07:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p07_strategy_gate

    P08:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p08_execution_risk

    P09:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p09_review_replay

    P10:
      canonical_data_dir: /root/sikk-gmgn/data/phase_controllers/p10_self_upgrade

  integration_runtime_paths:
    I01:
      canonical_data_dir: /root/sikk-gmgn/data/integration_program/I01_full_phase_consistency_audit
    I02:
      canonical_data_dir: /root/sikk-gmgn/data/integration_program/I02_directory_contract_index_unification
    I03:
      canonical_data_dir: /root/sikk-gmgn/data/integration_program/I03_runner_tool_binding
    I04:
      canonical_data_dir: /root/sikk-gmgn/data/integration_program/I04_paper_runtime_integration
    I05:
      canonical_data_dir: /root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop

  paper_runtime:
    canonical_data_dir: /root/sikk-gmgn/data/paper_runtime
    required_subdirs:
      - positions_open
      - positions_closed
      - trades
      - equity_curve
      - runtime_events
      - exit_events
      - risk_events
      - daily_reports
      - trace
      - acceptance
      - handoff
      - reports

  write_policy:
    phase_controller_outputs_must_write_to_phase_data_dir: true
    integration_outputs_must_write_to_integration_data_dir: true
    legacy_paths_readonly_by_default: true
    no_unregistered_runtime_output: true
```

---

# 12. Schema Index

```yaml
schema_index:
  index_id: SCHEMA_INDEX
  generated_at: datetime

  schema_records:
    - schema_id: candidate_master_record_schema
      owner_phase: P01
      object_name: candidate_master_record
      expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/candidate_master_record_schema.yaml
      exists: boolean
      downstream_consumers:
        - P02
        - P09
      trace_required: true
      acceptance_required: true

    - schema_id: source_data_fact_schema
      owner_phase: P02
      object_name: source_data_fact_record
      downstream_consumers:
        - P03
        - P09

    - schema_id: wallet_entity_master_schema
      owner_phase: P03
      object_name: wallet_entity_master_record
      downstream_consumers:
        - P04
        - P09

    - schema_id: chip_accounting_record_schema
      owner_phase: P04
      object_name: chip_accounting_record
      downstream_consumers:
        - P05
        - P09

    - schema_id: evidence_object_schema
      owner_phase: P05
      object_name: evidence_object_record
      downstream_consumers:
        - P06
        - P09

    - schema_id: scenario_candidate_schema
      owner_phase: P06
      object_name: scenario_candidate_record
      downstream_consumers:
        - P07
        - P09

    - schema_id: strategy_gate_decision_schema
      owner_phase: P07
      object_name: strategy_gate_decision_record
      downstream_consumers:
        - P08
        - P09

    - schema_id: paper_runtime_permission_schema
      owner_phase: P08
      object_name: paper_runtime_permission_record
      downstream_consumers:
        - PAPER_RUNTIME
        - P09

    - schema_id: failure_attribution_schema
      owner_phase: P09
      object_name: failure_attribution_record
      downstream_consumers:
        - P10

    - schema_id: controlled_upgrade_package_schema
      owner_phase: P10
      object_name: controlled_upgrade_package_record
      downstream_consumers:
        - IMPLEMENTATION_TASK_QUEUE

  coverage_summary:
    total_schema_expected: integer
    total_schema_found: integer
    total_schema_missing: integer
    missing_required_before_i03: list
    missing_required_before_i04: list
```

---

# 13. Contract Index

```yaml
contract_index:
  index_id: CONTRACT_INDEX
  generated_at: datetime

  input_contracts:
    - contract_id: p01_input_contract
      owner_phase: P01
      expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_input_contract.yaml
      exists: boolean

    - contract_id: p02_input_contract
      owner_phase: P02

    - contract_id: p03_input_contract
      owner_phase: P03

    - contract_id: p04_input_contract
      owner_phase: P04

    - contract_id: p05_input_contract
      owner_phase: P05

    - contract_id: p06_input_contract
      owner_phase: P06

    - contract_id: p07_input_contract
      owner_phase: P07

    - contract_id: p08_input_contract
      owner_phase: P08

    - contract_id: p09_input_contract
      owner_phase: P09

    - contract_id: p10_input_contract
      owner_phase: P10

  output_contracts:
    - contract_id: p01_output_contract
      owner_phase: P01
    - contract_id: p02_output_contract
      owner_phase: P02
    - contract_id: p03_output_contract
      owner_phase: P03
    - contract_id: p04_output_contract
      owner_phase: P04
    - contract_id: p05_output_contract
      owner_phase: P05
    - contract_id: p06_output_contract
      owner_phase: P06
    - contract_id: p07_output_contract
      owner_phase: P07
    - contract_id: p08_output_contract
      owner_phase: P08
    - contract_id: p09_output_contract
      owner_phase: P09
    - contract_id: p10_output_contract
      owner_phase: P10

  contract_status:
    - CONTRACT_INDEX_COMPLETE
    - CONTRACT_INDEX_WITH_GAPS
    - CONTRACT_INDEX_CRITICAL_GAPS
    - CONTRACT_INDEX_UNUSABLE
```

---

# 14. Handoff Contract Index

```yaml
handoff_contract_index:
  index_id: HANDOFF_CONTRACT_INDEX
  generated_at: datetime

  handoff_contracts:
    - handoff_contract_id: p01_to_p02_handoff_contract
      from_phase: P01
      to_phase: P02
      expected_path: /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/p01_to_p02_handoff_contract.yaml
      runtime_packet_expected_path: /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/handoff/p01_to_p02_handoff_packet.yaml
      exists: boolean
      required_before_i03: true

    - handoff_contract_id: p02_to_p03_handoff_contract
      from_phase: P02
      to_phase: P03

    - handoff_contract_id: p03_to_p04_handoff_contract
      from_phase: P03
      to_phase: P04

    - handoff_contract_id: p04_to_p05_handoff_contract
      from_phase: P04
      to_phase: P05

    - handoff_contract_id: p05_to_p06_handoff_contract
      from_phase: P05
      to_phase: P06

    - handoff_contract_id: p06_to_p07_handoff_contract
      from_phase: P06
      to_phase: P07

    - handoff_contract_id: p07_to_p08_handoff_contract
      from_phase: P07
      to_phase: P08

    - handoff_contract_id: p08_to_paper_runtime_handoff_contract
      from_phase: P08
      to_phase: PAPER_ONLY_RUNTIME

    - handoff_contract_id: p09_to_p10_handoff_contract
      from_phase: P09
      to_phase: P10

    - handoff_contract_id: p10_to_implementation_handoff_contract
      from_phase: P10
      to_phase: IMPLEMENTATION_TASK_QUEUE

  required_common_fields:
    - packet_id
    - packet_type
    - generated_at
    - route
    - upstream_control
    - scope
    - package_paths
    - quality
    - limitations
    - downstream_permission
    - read_instruction
    - trace

  index_status:
    - COMPLETE
    - WITH_GAPS
    - CRITICAL_GAPS
    - UNUSABLE
```

---

# 15. Data Request Packet Index

```yaml
data_request_packet_index:
  index_id: DATA_REQUEST_PACKET_INDEX
  generated_at: datetime

  packet_contracts:
    - packet_contract_id: p02_source_data_request_packet_contract
      from_phase: P01
      to_phase: P02
      purpose_cn: P01 请求 P02 拉取候选所需数据事实

    - packet_contract_id: p03_wallet_entity_data_request_packet_contract
      from_phase: P02
      to_phase: P03

    - packet_contract_id: p04_chip_structure_data_request_packet_contract
      from_phase: P03
      to_phase: P04

    - packet_contract_id: p05_evidence_data_request_packet_contract
      from_phase: P04
      to_phase: P05

    - packet_contract_id: p06_scenario_data_request_packet_contract
      from_phase: P05
      to_phase: P06

    - packet_contract_id: p07_strategy_gate_data_request_packet_contract
      from_phase: P06
      to_phase: P07

    - packet_contract_id: p08_execution_risk_data_request_packet_contract
      from_phase: P07
      to_phase: P08

    - packet_contract_id: paper_runtime_data_request_packet_contract
      from_phase: P08
      to_phase: PAPER_ONLY_RUNTIME

    - packet_contract_id: p10_upgrade_candidate_data_request_packet_contract
      from_phase: P09
      to_phase: P10

  status:
    - DATA_REQUEST_INDEX_COMPLETE
    - DATA_REQUEST_INDEX_WITH_GAPS
    - DATA_REQUEST_INDEX_UNUSABLE
```

---

# 16. Trace / Acceptance / Report Index

## 16.1 Trace Artifact Index

```yaml
trace_artifact_index:
  index_id: TRACE_ARTIFACT_INDEX

  trace_artifacts:
    - phase_id: P01
      trace_requirements_path: string
      runtime_trace_dir: /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/trace
      trace_types:
        - source_trace
        - decision_trace
        - handoff_trace
        - acceptance_trace

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  trace_policy:
    every_runtime_output_requires_trace: true
    every_handoff_requires_handoff_trace: true
    every_acceptance_requires_acceptance_trace: true
    p09_replay_requires_trace_chain: true
```

## 16.2 Acceptance Artifact Index

```yaml
acceptance_artifact_index:
  index_id: ACCEPTANCE_ARTIFACT_INDEX

  acceptance_artifacts:
    - phase_id: P01
      acceptance_criteria_path: string
      runtime_acceptance_dir: /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/acceptance
      expected_acceptance_result_file: p01_acceptance_result.yaml

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08
    - phase_id: P09
    - phase_id: P10

  acceptance_policy:
    rejected_items_must_not_be_used_downstream: true
    blocked_items_must_not_be_used_downstream: true
    ready_with_gaps_must_propagate_limitations: true
```

## 16.3 Report Model Index

```yaml
report_model_index:
  index_id: REPORT_MODEL_INDEX

  report_models:
    - report_model_id: p01_candidate_intake_report_model
      owner_phase: P01
      report_model_path: string
      runtime_report_dir: /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/reports

    - report_model_id: p02_source_data_fact_report_model
      owner_phase: P02

    - report_model_id: p03_wallet_entity_report_model
      owner_phase: P03

    - report_model_id: p04_chip_structure_report_model
      owner_phase: P04

    - report_model_id: p05_evidence_report_model
      owner_phase: P05

    - report_model_id: p06_scenario_report_model
      owner_phase: P06

    - report_model_id: p07_strategy_gate_report_model
      owner_phase: P07

    - report_model_id: p08_execution_risk_report_model
      owner_phase: P08

    - report_model_id: p09_review_replay_report_model
      owner_phase: P09

    - report_model_id: p10_self_upgrade_report_model
      owner_phase: P10
```

---

# 17. Read Order Manifest

HER / Runner 必须按顺序读取，不允许随意读文件。

```yaml
read_order_manifest:
  manifest_id: READ_ORDER_MANIFEST
  generated_at: datetime

  global_read_order:
    - system_methodology_blueprint.md
    - professional_build_order.md
    - directory_constitution_final.md
    - phase_controller_index.yaml
    - phase_controller_file_index.yaml
    - schema_index.yaml
    - contract_index.yaml
    - handoff_contract_index.yaml
    - data_request_packet_index.yaml
    - global_status_code_table.md
    - global_hard_negative_rules.md

  per_phase_read_order:
    - controller_yaml
    - context_md
    - input_contract
    - output_contract
    - schema_files
    - policy_files
    - hard_negative_rules
    - state_machine
    - trace_requirements
    - acceptance_criteria
    - handoff_contract
    - test_matrix
    - report_model

  integration_read_order:
    I03_runner_tool_binding:
      must_read_first:
        - directory_constitution_final.md
        - phase_controller_file_index.yaml
        - runtime_data_path_index.yaml
        - schema_index.yaml
        - contract_index.yaml
        - handoff_contract_index.yaml
        - i02_to_i03_handoff_packet.yaml

  runtime_read_order:
    paper_runtime:
      must_read_first:
        - p08_to_paper_runtime_handoff_packet
        - paper_runtime_data_request_packet
        - paper_runtime_input_contract
        - runtime_data_path_index.yaml
```

---

# 18. Write Permission Matrix

```yaml
write_permission_matrix:
  matrix_id: WRITE_PERMISSION_MATRIX

  write_permissions:
    P01:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p01_candidate_intake
      forbidden_write_dirs:
        - /root/sikk-gmgn/system/phase_controllers/p02_source_data_fact_controller
        - /root/sikk-gmgn/data/phase_controllers/p02_source_data_fact
        - /root/sikk-gmgn/data/paper_runtime
      may_write_handoff_to: P02

    P02:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p02_source_data_fact
      may_write_handoff_to: P03

    P03:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p03_wallet_entity
      may_write_handoff_to: P04

    P04:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p04_chip_structure
      may_write_handoff_to: P05

    P05:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p05_evidence
      may_write_handoff_to: P06

    P06:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p06_scenario_recognition
      may_write_handoff_to: P07

    P07:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p07_strategy_gate
      may_write_handoff_to: P08
      forbidden_write_dirs:
        - /root/sikk-gmgn/data/paper_runtime

    P08:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p08_execution_risk
      may_write_handoff_to: PAPER_ONLY_RUNTIME
      forbidden:
        - wallet_signing
        - live_order

    PAPER_ONLY_RUNTIME:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/paper_runtime
      may_write_to_p09_review_inputs: true

    P09:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p09_review_replay
      may_write_handoff_to: P10
      forbidden:
        - direct_rule_mutation
        - runtime_mutation

    P10:
      allowed_write_dirs:
        - /root/sikk-gmgn/data/phase_controllers/p10_self_upgrade
      may_write_handoff_to:
        - GOVERNANCE_REVIEW
        - IMPLEMENTATION_TASK_QUEUE
      forbidden:
        - auto_deploy
        - live_execution
```

---

# 19. Legacy Path Mapping

```yaml
legacy_path_mapping:
  mapping_id: LEGACY_PATH_MAPPING
  generated_at: datetime

  legacy_roots:
    - legacy_root: /root/sikk-gmgn/data/gmgn_candidates_live_run
      status: LEGACY_RUNTIME_KEEP_IN_PLACE
      policy:
        delete_allowed: false
        move_allowed: false
        default_read_mode: READ_ONLY
        default_write_mode: DISABLED_FOR_NEW_SYSTEM

      mapped_components:
        candidate_signal_outputs:
          legacy_path: /root/sikk-gmgn/data/gmgn_candidates_live_run/candidate_signal_outputs
          maps_to: P06_OR_LEGACY_SIGNAL_OUTPUT_REFERENCE
          canonical_future_path: /root/sikk-gmgn/data/phase_controllers/p06_scenario_recognition

        state_machine:
          legacy_path: /root/sikk-gmgn/data/gmgn_candidates_live_run/state_machine
          maps_to: LEGACY_STATE_MACHINE_REFERENCE
          canonical_future_path: /root/sikk-gmgn/data/phase_controllers/p07_strategy_gate

        quote_security:
          legacy_path: /root/sikk-gmgn/data/gmgn_candidates_live_run/quote_security
          maps_to: P08_QUOTE_SECURITY_REFERENCE
          canonical_future_path: /root/sikk-gmgn/data/phase_controllers/p08_execution_risk

        paper_live:
          legacy_path: /root/sikk-gmgn/data/gmgn_candidates_live_run/paper_live
          maps_to: PAPER_RUNTIME_LEGACY_REFERENCE
          canonical_future_path: /root/sikk-gmgn/data/paper_runtime

        reports:
          legacy_path: /root/sikk-gmgn/data/gmgn_candidates_live_run/reports
          maps_to: LEGACY_REPORT_REFERENCE
          canonical_future_path: /root/sikk-gmgn/data/reports

    - legacy_root: /root/sikk-gmgn/data/source_wallet_bot
      status: TRANSITIONAL_SOURCE_WALLET_DATA
      maps_to:
        P02: source_data_fact
        P03: wallet_entity
        P04: chip_structure

    - legacy_root: /root/sikk-gmgn/data/intel_bot
      status: TRANSITIONAL_INTEL_DATA
      maps_to:
        P05: evidence
        P06: scenario_recognition
        P07: strategy_gate_context

  absorption_policy:
    legacy_data_can_be_read_for_replay: true
    legacy_data_can_be_used_as_seed: true
    legacy_data_must_not_overwrite_canonical_outputs: true
    legacy_data_requires_trace_wrapper: true
    legacy_data_requires_quality_tag: LEGACY_SOURCE
```

---

# 20. Canonical Path Policy

```yaml
canonical_path_policy:
  policy_id: CANONICAL_PATH_POLICY
  version: v1.0

  rules:
    - rule_id: PATH_001
      name: 新系统文件必须写入 system
      condition: artifact_type in [controller, context, schema, contract, policy, state_machine]
      required_path_prefix: /root/sikk-gmgn/system

    - rule_id: PATH_002
      name: 新运行输出必须写入 data
      condition: artifact_type in [runtime_output, report, trace, handoff, acceptance]
      required_path_prefix: /root/sikk-gmgn/data

    - rule_id: PATH_003
      name: phase controller 输出必须写入对应 phase data dir
      condition: phase_id in [P01,P02,P03,P04,P05,P06,P07,P08,P09,P10]
      required_path_prefix: /root/sikk-gmgn/data/phase_controllers/{phase_slug}

    - rule_id: PATH_004
      name: integration 输出必须写入 integration_program
      condition: integration_id in [I01,I02,I03,I04,I05]
      required_path_prefix: /root/sikk-gmgn/data/integration_program/{integration_slug}

    - rule_id: PATH_005
      name: legacy 路径默认只读
      condition: path_prefix in legacy_roots
      write_allowed: false

    - rule_id: PATH_006
      name: 未登记路径禁止写入
      condition: path_not_in_index == true
      result: BLOCK_WRITE

    - rule_id: PATH_007
      name: 不允许系统文件和运行数据混写
      condition: system_file_written_to_data_or_runtime_output_written_to_system
      result: BLOCK_WRITE
```

---

# 21. Path Conflict Report

```yaml
path_conflict_report:
  report_id: PATH_CONFLICT_REPORT
  generated_at: datetime

  conflicts:
    - conflict_id: string
      conflict_type:
        - DUPLICATE_CANONICAL_PATH
        - SAME_ARTIFACT_MULTIPLE_LOCATIONS
        - LEGACY_PATH_USED_AS_CANONICAL
        - SYSTEM_FILE_IN_DATA_DIR
        - RUNTIME_OUTPUT_IN_SYSTEM_DIR
        - UNREGISTERED_WRITE_PATH
        - PHASE_OUTPUT_WRITES_TO_OTHER_PHASE_DIR
      affected_paths: list
      affected_phase: string | null
      severity:
        - BLOCKING
        - HIGH
        - MEDIUM
        - LOW
      recommended_resolution_cn: string

  conflict_summary:
    blocking_conflict_count: integer
    high_conflict_count: integer
    medium_conflict_count: integer
    low_conflict_count: integer
```

---

# 22. Index Gap Report

```yaml
index_gap_report:
  report_id: INDEX_GAP_REPORT
  generated_at: datetime

  gaps:
    - gap_id: string
      gap_type:
        - MISSING_SCHEMA_INDEX_ENTRY
        - MISSING_CONTRACT_INDEX_ENTRY
        - MISSING_HANDOFF_INDEX_ENTRY
        - MISSING_DATA_REQUEST_INDEX_ENTRY
        - MISSING_RUNTIME_PATH
        - MISSING_TRACE_PATH
        - MISSING_ACCEPTANCE_PATH
        - MISSING_REPORT_MODEL_PATH
        - FILE_EXPECTED_BUT_NOT_FOUND
        - FILE_FOUND_BUT_NOT_INDEXED

      affected_phase: string | null
      artifact_name: string
      expected_path: string | null
      observed_path: string | null

      severity:
        - BLOCKING
        - CRITICAL
        - HIGH
        - MEDIUM
        - LOW

      fix_target:
        - FIX_IN_I02_INDEX
        - FIX_IN_P01_P10_SYSTEM_FILE
        - FIX_BEFORE_I03
        - FIX_BEFORE_I04
        - DEFER

      recommended_fix_cn: string

  summary:
    total_gaps: integer
    blocking_gaps: integer
    critical_gaps: integer
    high_gaps: integer
    medium_gaps: integer
    low_gaps: integer
```

---

# 23. I03 Runner Tool Binding Prerequisite Packet

```yaml
i03_runner_tool_binding_prerequisite_packet:
  packet_id: string
  packet_type: I03_RUNNER_TOOL_BINDING_PREREQUISITE_PACKET
  generated_at: datetime

  from: I02_DIRECTORY_CONTRACT_INDEX_UNIFICATION
  to: I03_RUNNER_TOOL_BINDING

  required_i03_inputs:
    - directory_constitution_final_path
    - phase_controller_file_index_path
    - runtime_data_path_index_path
    - schema_index_path
    - contract_index_path
    - handoff_contract_index_path
    - data_request_packet_index_path
    - artifact_type_registry_path
    - read_order_manifest_path
    - write_permission_matrix_path
    - legacy_path_mapping_path
    - canonical_path_policy_path
    - index_gap_report_path
    - path_conflict_report_path

  runner_binding_scope:
    phases_to_bind:
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

    tools_to_bind_later:
      - GMGN
      - OKX_QUOTE
      - OKX_SECURITY
      - KLINE_PROVIDER
      - TRACE_WRITER
      - ACCEPTANCE_RUNNER
      - HANDOFF_WRITER
      - PAPER_RUNTIME_RUNNER

  prerequisites_status:
    directory_index_ready: boolean
    schema_index_ready: boolean
    contract_index_ready: boolean
    handoff_index_ready: boolean
    runtime_path_index_ready: boolean
    legacy_mapping_ready: boolean
    no_blocking_path_conflicts: boolean

  permission_to_enter_i03:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I03_MAY_BIND_RUNNERS
    - I03_MUST_USE_CANONICAL_PATHS
    - I03_MUST_NOT_WRITE_UNREGISTERED_OUTPUTS
    - I03_MUST_RESPECT_LEGACY_READONLY_POLICY
    - NO_PAPER_RUNTIME_YET
    - NO_LIVE_EXECUTION
```

---

# 24. I02 to I03 Handoff Packet

```yaml
i02_to_i03_handoff_packet:
  packet_id: string
  packet_type: I02_TO_I03_DIRECTORY_CONTRACT_INDEX_HANDOFF
  generated_at: datetime

  route:
    from: I02_DIRECTORY_CONTRACT_INDEX_UNIFICATION
    to: I03_RUNNER_TOOL_BINDING

  upstream_control:
    i01_handoff_packet_id: string
    i02_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  package_paths:
    directory_constitution_final_path: string
    canonical_root_declaration_path: string
    phase_controller_file_index_path: string
    runtime_data_path_index_path: string
    artifact_type_registry_path: string
    schema_index_path: string
    contract_index_path: string
    handoff_contract_index_path: string
    data_request_packet_index_path: string
    trace_artifact_index_path: string
    acceptance_artifact_index_path: string
    report_model_index_path: string
    read_order_manifest_path: string
    write_permission_matrix_path: string
    legacy_path_mapping_path: string
    canonical_path_policy_path: string
    path_conflict_report_path: string
    index_gap_report_path: string
    i03_prerequisite_packet_path: string

  i03_required_tasks:
    - bind_phase_runners_to_phase_controller_file_index
    - bind_runtime_outputs_to_runtime_data_path_index
    - bind_schema_validation_to_schema_index
    - bind_contract_validation_to_contract_index
    - bind_handoff_writer_to_handoff_contract_index
    - bind_trace_writer_to_trace_artifact_index
    - bind_acceptance_runner_to_acceptance_artifact_index
    - bind_legacy_readonly_sources_to_legacy_path_mapping
    - block_unregistered_write_paths
    - generate_runner_binding_index
    - generate_tool_binding_index

  permission_to_enter_i03:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I02_INDEX_ONLY
    - I03_RUNNER_BINDING_ALLOWED
    - BUSINESS_LOGIC_CHANGES_FORBIDDEN
    - LEGACY_DELETE_FORBIDDEN
    - PAPER_RUNTIME_NOT_YET
    - LIVE_EXECUTION_FORBIDDEN
```

---

# 25. I02 Gap Policy

```yaml
i02_gap_policy:
  BLOCKING_GAP:
    result: I02_BLOCKED
    examples:
      - i01_handoff_missing
      - canonical_root_undefined
      - phase_controller_file_index_unusable
      - runtime_data_path_index_unusable
      - critical_handoff_contract_unindexed
      - live_execution_path_found
      - legacy_path_marked_as_new_canonical_write_path

  CRITICAL_GAP:
    result: I02_REJECTED_OR_FIX_REQUIRED
    examples:
      - missing_p07_to_p08_handoff_index
      - missing_p08_to_paper_runtime_handoff_index
      - missing_p09_to_p10_handoff_index
      - schema_index_empty
      - contract_index_empty
      - no_write_permission_matrix
      - no_legacy_mapping_for_existing_runtime

  HIGH_GAP:
    result: I02_READY_WITH_GAPS
    examples:
      - noncritical_schema_unindexed
      - report_model_unindexed
      - optional_trace_artifact_missing
      - file_found_but_needs_rename
      - legacy_path_mapping_partial

  MEDIUM_GAP:
    result: I02_READY_WITH_GAPS
    examples:
      - naming_inconsistency
      - optional_metadata_missing
      - old_report_path_not_mapped
      - noncritical_runtime_subdir_missing

  LOW_GAP:
    result: I02_READY_WITH_NOTE
    examples:
      - formatting_inconsistency
      - comment_missing
      - noncritical_description_missing
```

---

# 26. I02 Hard Negative Rules

```yaml
i02_hard_negative_rules:
  - rule_id: I02_BLOCK_001
    name: 未读取 I01 handoff
    condition: i01_to_i02_handoff_packet_missing == true
    result: I02_BLOCKED
    reason: I02 必须基于 I01 审计结果执行

  - rule_id: I02_BLOCK_002
    name: 未定义 canonical root
    condition: canonical_root_missing == true
    result: I02_BLOCKED
    reason: 没有主根目录，无法统一路径

  - rule_id: I02_BLOCK_003
    name: 把 legacy runtime 当成新主写入路径
    condition: legacy_path_marked_as_primary_write_path == true
    result: I02_BLOCKED
    reason: legacy 目录只能映射和只读吸收，不能污染新系统主路径

  - rule_id: I02_BLOCK_004
    name: 关键 handoff 未索引
    condition: critical_handoff_index_missing == true
    result: I02_BLOCKED
    reason: I03 Runner 必须依赖 handoff index

  - rule_id: I02_BLOCK_005
    name: schema_index 为空
    condition: schema_index_empty == true
    result: I02_BLOCKED
    reason: 没有 schema index 无法做验证和工具绑定

  - rule_id: I02_BLOCK_006
    name: contract_index 为空
    condition: contract_index_empty == true
    result: I02_BLOCKED
    reason: 没有 contract index 无法做阶段交接

  - rule_id: I02_BLOCK_007
    name: 未登记写入路径
    condition: unregistered_write_path_allowed == true
    result: I02_BLOCKED
    reason: 专业系统禁止未登记写入

  - rule_id: I02_BLOCK_008
    name: 删除或移动 legacy 数据
    condition: legacy_delete_or_move_requested == true
    result: I02_BLOCKED
    reason: I02 不允许删除或移动 legacy runtime 数据

  - rule_id: I02_BLOCK_009
    name: I02 修改业务逻辑
    condition: business_logic_mutation_requested == true
    result: I02_BLOCKED
    reason: I02 只做索引和目录统一

  - rule_id: I02_BLOCK_010
    name: live execution 路径
    condition: live_execution_allowed == true
    result: I02_BLOCKED
    reason: 当前系统禁止自动实盘
```

---

# 27. I02 状态机

```yaml
i02_directory_contract_index_state_machine:
  states:
    - I02_UNINITIALIZED
    - I02_CONTEXT_LOADED
    - I02_I01_HANDOFF_READ
    - I02_INPUT_MANIFEST_BUILT
    - I02_CANONICAL_ROOT_DECLARED
    - I02_DIRECTORY_CONSTITUTION_BUILT
    - I02_ARTIFACT_TYPE_REGISTRY_BUILT
    - I02_PHASE_FILE_INDEX_BUILT
    - I02_RUNTIME_DATA_PATH_INDEX_BUILT
    - I02_SCHEMA_INDEX_BUILT
    - I02_CONTRACT_INDEX_BUILT
    - I02_HANDOFF_CONTRACT_INDEX_BUILT
    - I02_DATA_REQUEST_PACKET_INDEX_BUILT
    - I02_TRACE_ARTIFACT_INDEX_BUILT
    - I02_ACCEPTANCE_ARTIFACT_INDEX_BUILT
    - I02_REPORT_MODEL_INDEX_BUILT
    - I02_READ_ORDER_MANIFEST_BUILT
    - I02_WRITE_PERMISSION_MATRIX_BUILT
    - I02_LEGACY_PATH_MAPPING_BUILT
    - I02_CANONICAL_PATH_POLICY_BUILT
    - I02_PATH_CONFLICTS_ANALYZED
    - I02_INDEX_GAPS_ANALYZED
    - I02_I03_PREREQUISITE_PACKET_BUILT
    - I02_REPORT_BUILT
    - I02_I03_HANDOFF_BUILT
    - I02_READY_FOR_ACCEPTANCE
    - I02_ACCEPTANCE_READY
    - I02_READY_FOR_I03_HANDOFF
    - I02_READY_WITH_GAPS
    - I02_REJECTED
    - I02_BLOCKED

  critical_transitions:
    - from: I02_CONTEXT_LOADED
      to: I02_I01_HANDOFF_READ
      condition: i01_to_i02_handoff_packet_available == true

    - from: I02_I01_HANDOFF_READ
      to: I02_INPUT_MANIFEST_BUILT
      condition: i01_audit_outputs_available == true

    - from: I02_INPUT_MANIFEST_BUILT
      to: I02_CANONICAL_ROOT_DECLARED
      condition: canonical_root_declaration_created == true

    - from: I02_CANONICAL_ROOT_DECLARED
      to: I02_DIRECTORY_CONSTITUTION_BUILT
      condition: final_directory_constitution_created == true

    - from: I02_DIRECTORY_CONSTITUTION_BUILT
      to: I02_PHASE_FILE_INDEX_BUILT
      condition: phase_controller_file_index_created == true

    - from: I02_PHASE_FILE_INDEX_BUILT
      to: I02_RUNTIME_DATA_PATH_INDEX_BUILT
      condition: runtime_data_path_index_created == true

    - from: I02_RUNTIME_DATA_PATH_INDEX_BUILT
      to: I02_SCHEMA_INDEX_BUILT
      condition: schema_index_created == true

    - from: I02_SCHEMA_INDEX_BUILT
      to: I02_CONTRACT_INDEX_BUILT
      condition: contract_index_created == true

    - from: I02_CONTRACT_INDEX_BUILT
      to: I02_HANDOFF_CONTRACT_INDEX_BUILT
      condition: handoff_contract_index_created == true

    - from: I02_HANDOFF_CONTRACT_INDEX_BUILT
      to: I02_DATA_REQUEST_PACKET_INDEX_BUILT
      condition: data_request_packet_index_created == true

    - from: I02_DATA_REQUEST_PACKET_INDEX_BUILT
      to: I02_READ_ORDER_MANIFEST_BUILT
      condition: read_order_manifest_created == true

    - from: I02_READ_ORDER_MANIFEST_BUILT
      to: I02_WRITE_PERMISSION_MATRIX_BUILT
      condition: write_permission_matrix_created == true

    - from: I02_WRITE_PERMISSION_MATRIX_BUILT
      to: I02_LEGACY_PATH_MAPPING_BUILT
      condition: legacy_path_mapping_created == true

    - from: I02_LEGACY_PATH_MAPPING_BUILT
      to: I02_PATH_CONFLICTS_ANALYZED
      condition: path_conflict_report_created == true

    - from: I02_PATH_CONFLICTS_ANALYZED
      to: I02_INDEX_GAPS_ANALYZED
      condition: index_gap_report_created == true

    - from: I02_INDEX_GAPS_ANALYZED
      to: I02_I03_PREREQUISITE_PACKET_BUILT
      condition: i03_prerequisite_packet_created == true

    - from: I02_I03_PREREQUISITE_PACKET_BUILT
      to: I02_I03_HANDOFF_BUILT
      condition: i02_to_i03_handoff_packet_created == true

    - from: I02_I03_HANDOFF_BUILT
      to: I02_READY_FOR_ACCEPTANCE
      condition: i02_report_created == true
```

---

# 28. I02 Acceptance Criteria

```yaml
i02_acceptance_criteria:
  I02_READY:
    required:
      - i01_handoff_read
      - canonical_root_declared
      - final_directory_constitution_created
      - artifact_type_registry_created
      - phase_controller_file_index_created
      - runtime_data_path_index_created
      - schema_index_created
      - contract_index_created
      - handoff_contract_index_created
      - data_request_packet_index_created
      - trace_artifact_index_created
      - acceptance_artifact_index_created
      - report_model_index_created
      - read_order_manifest_created
      - write_permission_matrix_created
      - legacy_path_mapping_created
      - canonical_path_policy_created
      - path_conflict_report_created
      - index_gap_report_created
      - i03_prerequisite_packet_created
      - i02_to_i03_handoff_created
      - no_blocking_path_conflict
      - no_legacy_delete_or_move
      - no_live_execution_path

  I02_READY_WITH_GAPS:
    allowed_when:
      - noncritical_schema_unindexed
      - noncritical_report_model_missing
      - optional_legacy_mapping_partial
      - file_rename_needed_but_not_blocking
    required:
      - gaps_recorded
      - i03_permission_is_allowed_with_gaps
      - blocking_gaps_absent

  I02_REJECTED:
    triggered_by:
      - schema_index_unusable
      - contract_index_unusable
      - runtime_data_path_index_unusable
      - no_legacy_mapping_for_required_runtime
      - no_i03_prerequisite_packet

  I02_BLOCKED:
    triggered_by:
      - missing_i01_handoff
      - canonical_root_missing
      - critical_handoff_index_missing
      - unregistered_write_path_allowed
      - legacy_delete_or_move_requested
      - business_logic_mutation_requested
      - live_execution_allowed
```

---

# 29. I02 测试矩阵

```yaml
i02_test_matrix:
  - test_id: I02_TEST_001
    name: I01 handoff 存在，P01-P10 文件和路径可索引
    expected_status: I02_READY

  - test_id: I02_TEST_002
    name: 缺 I01 handoff
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_003
    name: canonical root 未定义
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_004
    name: schema_index 为空
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_005
    name: contract_index 为空
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_006
    name: P07_to_P08 handoff contract 未索引
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_007
    name: P08_to_Paper_Runtime handoff contract 未索引
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_008
    name: legacy gmgn_candidates_live_run 被设为新主写入路径
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_009
    name: legacy 路径未映射但不影响 I03
    expected_status: I02_READY_WITH_GAPS

  - test_id: I02_TEST_010
    name: 文件存在但没有 index 登记
    expected_status: I02_READY_WITH_GAPS
    expected_output: index_gap_report

  - test_id: I02_TEST_011
    name: 一个 artifact 出现在多个路径
    expected_status: I02_READY_WITH_GAPS_OR_BLOCKED_DEPENDING_SEVERITY

  - test_id: I02_TEST_012
    name: 未登记写入路径被允许
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_013
    name: P07 运行数据目录指向 paper_runtime
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_014
    name: read_order_manifest 缺失
    expected_status: I02_REJECTED

  - test_id: I02_TEST_015
    name: write_permission_matrix 缺失
    expected_status: I02_REJECTED

  - test_id: I02_TEST_016
    name: I02 尝试修改业务规则
    expected_status: I02_BLOCKED

  - test_id: I02_TEST_017
    name: I03 prerequisite packet 未生成
    expected_status: I02_REJECTED

  - test_id: I02_TEST_018
    name: live execution path detected
    expected_status: I02_BLOCKED
```

---

# 30. I02 报告模型

```yaml
i02_directory_contract_index_unification_report:
  report_id: string
  generated_at: datetime
  controller_id: I02_DIRECTORY_CONTRACT_INDEX_UNIFICATION

  summary:
    canonical_root: string
    phase_count_indexed: integer
    schema_count_indexed: integer
    contract_count_indexed: integer
    handoff_contract_count_indexed: integer
    data_request_packet_count_indexed: integer
    runtime_path_count_indexed: integer
    legacy_path_count_mapped: integer
    blocking_gap_count: integer
    critical_gap_count: integer
    high_gap_count: integer
    medium_gap_count: integer
    low_gap_count: integer

  directory_summary:
    system_dir_ready: boolean
    data_dir_ready: boolean
    phase_controller_dirs_ready: boolean
    integration_program_dirs_ready: boolean
    paper_runtime_dir_ready: boolean

  index_summary:
    phase_controller_file_index_status: string
    runtime_data_path_index_status: string
    schema_index_status: string
    contract_index_status: string
    handoff_contract_index_status: string
    data_request_packet_index_status: string

  legacy_summary:
    legacy_roots_mapped: list
    legacy_readonly_policy_applied: boolean
    legacy_delete_or_move_detected: boolean
    legacy_absorption_notes: list

  path_conflict_summary:
    blocking_conflicts: list
    high_conflicts: list
    duplicate_paths: list
    unregistered_write_paths: list

  index_gap_summary:
    missing_required_before_i03: list
    missing_required_before_i04: list
    deferred_gaps: list

  i03_readiness:
    i03_prerequisite_packet_created: boolean
    permission_to_enter_i03: string
    reasons_if_blocked: list

  compliance:
    business_logic_changed: false
    legacy_data_deleted_or_moved: false
    unregistered_write_path_allowed: false
    live_execution_path_detected: false
```

---

# 31. HER I02 执行协议

```text
HER 执行 I02 时必须按以下顺序：

1. 读取 system_methodology_blueprint.md
2. 读取 professional_build_order.md
3. 读取 I01→I02 handoff packet
4. 读取 I01 full_phase_consistency_audit_report
5. 读取 I01 fix_priority_list
6. 读取 phase_controller_index.yaml
7. 读取 directory_constitution.md
8. 读取 contract_index.md
9. 读取 schema_index.md
10. 扫描 P01-P10 system phase controller directories
11. 扫描 P01-P10 expected data directories
12. 扫描 integration_program directories
13. 扫描 legacy runtime roots，但只能读取，不允许移动或删除
14. 建立 i02_input_manifest
15. 建立 canonical_root_declaration
16. 建立 final_directory_constitution
17. 建立 artifact_type_registry
18. 建立 phase_controller_file_index
19. 建立 runtime_data_path_index
20. 建立 schema_index
21. 建立 contract_index
22. 建立 handoff_contract_index
23. 建立 data_request_packet_index
24. 建立 trace_artifact_index
25. 建立 acceptance_artifact_index
26. 建立 report_model_index
27. 建立 read_order_manifest
28. 建立 write_permission_matrix
29. 建立 legacy_path_mapping
30. 建立 canonical_path_policy
31. 生成 path_conflict_report
32. 生成 index_gap_report
33. 生成 i03_runner_tool_binding_prerequisite_packet
34. 生成 i02_directory_contract_index_unification_report
35. 生成 i02_to_i03_handoff_packet
36. 生成 i02_acceptance_result
37. 只允许 handoff 给 I03
```

禁止：

```text
1. 不允许无 I01 handoff 启动 I02
2. 不允许新增 P11 / P12
3. 不允许修改 P01-P10 业务逻辑
4. 不允许写 Runner
5. 不允许绑定 GMGN / OKX 工具
6. 不允许启动 Paper Runtime
7. 不允许删除或移动 legacy 数据
8. 不允许把 legacy runtime 设为新主写入路径
9. 不允许允许未登记写入路径
10. 不允许 live execution
```

---

# 32. 给 HER 的正式任务书

```text
任务名称：I02 Directory & Contract Index Unification：目录与合约索引统一任务包

目标：
在 /root/sikk-gmgn/system/integration_program/I02_directory_contract_index_unification/ 下建立 I02 目录与合约索引统一任务包，并在 /root/sikk-gmgn/data/integration_program/I02_directory_contract_index_unification/ 下生成运行索引输出。I02 不是 P12，不新增业务判断能力，不修改 P01-P10 业务逻辑。它的目标是在 I01 全阶段一致性审计之后，统一 P01-P10 的系统目录、运行数据目录、schema、contract、handoff contract、data request packet、trace、acceptance、report model、read order、write permission、legacy path mapping 和 canonical path policy，为 I03 Runner / Tool Binding 提供稳定、可读、可验证、可追踪的路径与合约索引。

核心原则：
1. I02 是 Integration Program 第二步，不是新业务阶段。
2. I02 只做目录、路径、schema、contract、handoff、legacy mapping 的统一索引。
3. I02 不修改 P01-P10 业务逻辑。
4. I02 不直接写 Runner。
5. I02 不绑定 GMGN / OKX 工具。
6. I02 不启动 Paper Runtime。
7. I02 不删除、不移动 legacy runtime 数据。
8. I02 不允许把 legacy runtime 设为新系统主写入路径。
9. I02 必须定义 canonical root。
10. I02 必须建立 final directory constitution。
11. I02 必须建立 phase_controller_file_index。
12. I02 必须建立 runtime_data_path_index。
13. I02 必须建立 schema_index。
14. I02 必须建立 contract_index。
15. I02 必须建立 handoff_contract_index。
16. I02 必须建立 data_request_packet_index。
17. I02 必须建立 trace / acceptance / report model index。
18. I02 必须建立 read_order_manifest。
19. I02 必须建立 write_permission_matrix。
20. I02 必须建立 legacy_path_mapping。
21. I02 必须建立 canonical_path_policy。
22. I02 必须输出 path_conflict_report 与 index_gap_report。
23. I02 必须生成 I03 Runner Tool Binding Prerequisite Packet。
24. I02 只能交接给 I03 Runner / Tool Binding。

需要创建系统目录：
/root/sikk-gmgn/system/integration_program/I02_directory_contract_index_unification/

需要创建系统文件：
1. i02_directory_contract_index_unification_controller.yaml
2. i02_directory_contract_index_unification_context.md
3. i02_input_contract.yaml
4. i02_output_contract.yaml
5. i02_input_manifest_schema.yaml
6. canonical_root_declaration_schema.yaml
7. final_directory_constitution_schema.yaml
8. phase_controller_file_index_schema.yaml
9. runtime_data_path_index_schema.yaml
10. artifact_type_registry_schema.yaml
11. schema_index_schema.yaml
12. contract_index_schema.yaml
13. handoff_contract_index_schema.yaml
14. data_request_packet_index_schema.yaml
15. trace_artifact_index_schema.yaml
16. acceptance_artifact_index_schema.yaml
17. report_model_index_schema.yaml
18. read_order_manifest_schema.yaml
19. write_permission_matrix_schema.yaml
20. legacy_path_mapping_schema.yaml
21. canonical_path_policy_schema.yaml
22. path_conflict_report_schema.yaml
23. index_gap_report_schema.yaml
24. i03_runner_tool_binding_prerequisite_packet_contract.yaml
25. i02_to_i03_handoff_contract.yaml
26. i02_unification_policy.yaml
27. i02_legacy_absorption_policy.yaml
28. i02_hard_negative_rules.yaml
29. i02_state_machine.yaml
30. i02_trace_requirements.yaml
31. i02_acceptance_criteria.md
32. i02_storage_constitution.md
33. i02_test_matrix.yaml
34. i02_report_model.yaml
35. i02_review_checklist.md
36. her_i02_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/integration_program/I02_directory_contract_index_unification/
  input_manifest/
  canonical_root/
  directory_constitution/
  phase_file_index/
  runtime_data_path_index/
  artifact_type_registry/
  schema_index/
  contract_index/
  handoff_contract_index/
  data_request_packet_index/
  trace_artifact_index/
  acceptance_artifact_index/
  report_model_index/
  read_order/
  write_permissions/
  legacy_mapping/
  canonical_path_policy/
  path_conflicts/
  index_gaps/
  i03_prerequisites/
  i03_handoff/
  reports/
  audit/
  trace/
  acceptance/

每个文件要求：
- i02_directory_contract_index_unification_controller.yaml：定义 I02 身份、职责、权限、上下游、状态码、禁止事项。
- i02_directory_contract_index_unification_context.md：写成 HER 执行前必须读取的 I02 上下文。
- i02_input_contract.yaml：定义 I02 必须读取的 I01 输出、P01-P10 系统目录、旧索引、legacy runtime。
- i02_output_contract.yaml：定义目录宪法、索引、路径策略、legacy mapping、I03 前置包、I02→I03 handoff 输出。
- i02_input_manifest_schema.yaml：定义 I02 输入清单。
- canonical_root_declaration_schema.yaml：定义 /root/sikk-gmgn 为 canonical root。
- final_directory_constitution_schema.yaml：定义最终目录宪法。
- phase_controller_file_index_schema.yaml：定义 P01-P10 系统文件索引。
- runtime_data_path_index_schema.yaml：定义 P01-P10 与 Integration Program 运行数据路径。
- artifact_type_registry_schema.yaml：定义 controller、context、schema、contract、handoff、trace、acceptance、report、runtime output 文件类型。
- schema_index_schema.yaml：定义全 schema 索引。
- contract_index_schema.yaml：定义全 input / output contract 索引。
- handoff_contract_index_schema.yaml：定义全 handoff contract 索引。
- data_request_packet_index_schema.yaml：定义全 data request packet contract 索引。
- trace_artifact_index_schema.yaml：定义 trace 要求和路径索引。
- acceptance_artifact_index_schema.yaml：定义 acceptance 标准和运行结果路径索引。
- report_model_index_schema.yaml：定义 report model 路径索引。
- read_order_manifest_schema.yaml：定义 HER / Runner 读取顺序。
- write_permission_matrix_schema.yaml：定义每个阶段允许写入和禁止写入的路径。
- legacy_path_mapping_schema.yaml：定义 gmgn_candidates_live_run、source_wallet_bot、intel_bot 等旧路径映射。
- canonical_path_policy_schema.yaml：定义 canonical path、legacy readonly、未登记路径阻断规则。
- path_conflict_report_schema.yaml：定义路径冲突报告。
- index_gap_report_schema.yaml：定义索引缺口报告。
- i03_runner_tool_binding_prerequisite_packet_contract.yaml：定义 I03 绑定前置条件包。
- i02_to_i03_handoff_contract.yaml：定义 I02_TO_I03 handoff packet。
- i02_unification_policy.yaml：定义 I02 统一索引策略。
- i02_legacy_absorption_policy.yaml：定义 legacy 只读吸收策略。
- i02_hard_negative_rules.yaml：定义无 I01 handoff、无 canonical root、legacy 污染、关键 handoff 缺失、空 schema index、空 contract index、未登记写入、修改业务逻辑、live execution 等阻断。
- i02_state_machine.yaml：定义 I02 全状态机。
- i02_trace_requirements.yaml：定义 I02 trace。
- i02_acceptance_criteria.md：定义 I02_READY / READY_WITH_GAPS / REJECTED / BLOCKED。
- i02_storage_constitution.md：定义系统文件和运行数据目录。
- i02_test_matrix.yaml：定义至少 18 个测试场景。
- i02_report_model.yaml：定义 I02 人类可读报告。
- i02_review_checklist.md：定义 I02 审计清单。
- her_i02_execution_protocol.md：定义 HER 执行 I02 的顺序和禁止事项。

运行输出要求：
1. canonical_root_declaration.yaml
2. directory_constitution_final.md
3. phase_controller_file_index.yaml
4. runtime_data_path_index.yaml
5. artifact_type_registry.yaml
6. schema_index.yaml
7. contract_index.md
8. handoff_contract_index.yaml
9. data_request_packet_index.yaml
10. trace_artifact_index.yaml
11. acceptance_artifact_index.yaml
12. report_model_index.yaml
13. read_order_manifest.yaml
14. write_permission_matrix.yaml
15. legacy_path_mapping.yaml
16. canonical_path_policy.md
17. path_conflict_report.yaml
18. index_gap_report.yaml
19. i03_runner_tool_binding_prerequisite_packet.yaml
20. i02_directory_contract_index_unification_report.md
21. i02_to_i03_handoff_packet.yaml
22. i02_acceptance_result.yaml

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. canonical root 摘要
4. directory constitution 摘要
5. phase_controller_file_index 摘要
6. runtime_data_path_index 摘要
7. artifact_type_registry 摘要
8. schema_index 摘要
9. contract_index 摘要
10. handoff_contract_index 摘要
11. data_request_packet_index 摘要
12. trace / acceptance / report model index 摘要
13. read_order_manifest 摘要
14. write_permission_matrix 摘要
15. legacy_path_mapping 摘要
16. canonical_path_policy 摘要
17. path_conflict_report 摘要
18. index_gap_report 摘要
19. I03 prerequisite packet 摘要
20. I02→I03 handoff 摘要
21. 是否允许进入 I03
22. 是否达到轻量机构级 I02 v1.0

最终验收标准：
只有当 I02 具备 canonical root declaration、final directory constitution、phase controller file index、runtime data path index、artifact type registry、schema index、contract index、handoff contract index、data request packet index、trace artifact index、acceptance artifact index、report model index、read order manifest、write permission matrix、legacy path mapping、canonical path policy、path conflict report、index gap report、I03 prerequisite packet、I02→I03 handoff、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且没有 legacy 删除/迁移、没有未登记写入路径、没有业务逻辑变更、没有 live execution path 时，才允许标记为 I02_READY。
```

---

# 33. 当前是否达到专业化 I02 设计标准

## 判断

这一版 I02 达到：

```text
专业化
轻量机构水准
一次性把 I02 应有索引对象补全
不是最小版本
不是简单目录清单
不是继续新增业务阶段
```

I02 被明确设计为：

```text
canonical root 定义层
目录宪法统一层
阶段文件索引层
运行数据路径索引层
schema / contract / handoff 索引层
trace / acceptance / report 索引层
read order 层
write permission 层
legacy path mapping 层
I03 Runner / Tool Binding 前置层
```

---

# 34. I02 完成后下一步

I02 完成后，进入：

```text
I03 Runner / Tool Binding
```

I03 才负责把：

```text
阶段控制器
schema
contract
handoff
trace
acceptance
GMGN
OKX
K线
quote
security
paper runtime
```

绑定到实际可运行的 runner / tool / CLI / 输出路径。

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|P01-P10 实际文件是否已全部存在|I02 会索引并标记 exists|缺失项进入 index_gap_report|
|是否要把旧目录迁移到新目录|不迁移、不删除|建 legacy_path_mapping|
|Runner 具体怎么读 GMGN / OKX|I02 不处理|I03 Tool Binding|
|Paper Runtime 是否已能写仓位|I02 只定义路径|I04 联调|
|旧数据如何进入 P09 回放|I02 只做映射|I05 回放验证|
|schema 内容是否正确|I02 只索引和覆盖检查|I03/I04 测试与 P10 升级处理|

---

# 本次认知升级点

1. **I02 的本质不是建目录，而是建立系统寻址协议。**
    
2. **目录、schema、contract、handoff 必须统一索引后，Runner 才能稳定运行。**
    
3. **legacy 数据不能删除、不能移动、不能直接当新主路径。**  
    正确做法是只读映射和可追踪吸收。
    
4. **I02 不能伪造完整性。**  
    文件不存在就标记 missing，而不是写成 exists。
    
5. **I02 解决的是 HER / Runner “去哪里读、去哪里写、按什么顺序读、哪些路径禁止写”的问题。**
    
6. **I02 完成后才适合进入 I03 Runner / Tool Binding。**  
    否则工具绑定会把路径混乱固化成代码。