# Acceptance Plane：验收平面专业版设计 v2.0

## 0. 核心定位

**Acceptance Plane 不是检查清单，也不是“文件是否创建”的形式验收。**

它是 SIKK Stable Trader OS 的**系统裁决平面**，负责判断某个阶段、文件、合约、任务树、Trace 链、工具绑定、纸面运行结果是否真正达到：

```text
READY
READY_WITH_GAPS
REJECTED
BLOCKED
NEEDS_REWORK
```

一句话定义：

> **Trace Plane 记录系统发生了什么。**  
> **Acceptance Plane 判断这些结果是否合格。**  
> **Handoff Plane 只允许交接 Acceptance Plane 通过或带限制通过的结果。**

---

# 1. Acceptance Plane 在专业版建造顺序中的位置

你当前专业版建造顺序应固定为：

```text
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md：系统方法论蓝图
  ↓
P00：系统建造与方法论编译控制器
  ↓
Bootstrap Control Plane：启动控制面
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Full Control Plane：完整控制面
  ↓
Trace Plane：追踪平面
  ↓
Acceptance Plane：验收平面
  ↓
Handoff Plane：交接平面
  ↓
P01-P10 Phase Controller：业务阶段控制器
  ↓
Runner / Tool Binding：执行工具绑定
  ↓
Paper-only Runtime：纸面验证运行
  ↓
Review / Upgrade：复盘与升级
```

Acceptance Plane 的位置非常关键：

```text
Trace Plane 之后
Handoff Plane 之前
```

原因：

```text
没有 Trace，就没有验收依据。
没有 Acceptance，就不能安全交接。
```

---

# 2. Acceptance Plane 的专业定义

```text
Acceptance Plane 是 SIKK Stable Trader OS 的验收裁决平面。

它负责读取 Full Control Plane 的任务树、Trace Plane 的 trace_handoff_packet、各 Plane / Phase Controller 的产物、输入输出合约、状态码、缺口登记和禁止事项，执行结构验收、语义验收、合约验收、追踪验收、安全验收、工具验收、运行验收和复盘验收。

它不负责任务调度，不负责内容生成，不负责数据采集，不负责交接执行，不负责交易判断，不负责工具运行。

它只负责裁决：
当前阶段是否真正合格；
如果不完全合格，是允许带缺口进入下游，还是必须重做，还是必须阻断。
```

---

# 3. Acceptance Plane 解决的核心问题

|问题|没有 Acceptance Plane 的后果|Acceptance Plane 的处理|
|---|---|---|
|文件创建后直接宣称完成|形式完成，实际不可用|文件存在 + 内容结构 + 合约 + trace 同时验收|
|阶段目标是否达成不清|HER 可能跳步|阶段目标对照验收|
|缺口没有影响判断|下游误用不完整结果|缺口分级与下游权限限制|
|Trace 存在但断链|不能复盘|Trace 连续性验收|
|合约字段缺失|下游读取失败|合约完整性验收|
|规则越权|Data / Domain 输出买入信号|权限矩阵验收|
|工具绑定过早|脚本先于系统语义落地|工具绑定条件验收|
|Paper Runtime 无法归因|纸面结果不可复盘|runtime_trace + 输入输出验收|
|Review 升级污染实时规则|系统失控|升级必须受治理验收|

---

# 4. Acceptance Plane 与其他 Plane 的边界

## 4.1 与 Full Control Plane 的区别

|层|负责什么|不负责什么|
|---|---|---|
|Full Control Plane|调度、任务树、状态流、失败恢复|不做最终质量裁决|
|Acceptance Plane|判断产物是否合格、是否允许下游|不调度、不生成任务树|

关系：

```text
Full Control Plane 说：该做什么。
Trace Plane 记录：实际做了什么。
Acceptance Plane 判断：做得是否合格。
```

---

## 4.2 与 Trace Plane 的区别

|层|负责什么|
|---|---|
|Trace Plane|建立追踪链|
|Acceptance Plane|验收追踪链是否完整、可信、可用于下游|

Trace Plane 输出：

```text
trace_handoff_packet
trace_quality_status
trace_error_list
trace_indexes
```

Acceptance Plane 读取后裁决：

```text
是否 TRACE_READY
是否允许 Handoff
是否允许 P01-P10
是否允许 Tool Binding
是否允许 Paper Runtime
```

---

## 4.3 与 Handoff Plane 的区别

|层|负责什么|
|---|---|
|Acceptance Plane|裁决结果是否合格|
|Handoff Plane|把合格结果交接给下游|

Handoff Plane 不能自己决定合格。  
它只能读取 Acceptance Plane 输出的：

```text
acceptance_result_packet
downstream_permission
limitation_tags
forbidden_use
```

---

# 5. Acceptance Plane 的底层系统逻辑

## 5.1 “文件存在”不是验收

低级验收：

```text
文件已经创建，所以完成。
```

专业验收：

```text
文件存在
内容结构完整
字段完整
合约完整
trace 完整
状态码正确
禁止事项未触发
缺口已登记
下游权限明确
可以复盘
```

---

## 5.2 验收是权限裁决，不是意见

Acceptance Plane 的输出不是建议，而是系统权限：

```text
ALLOW_HANDOFF
ALLOW_WITH_LIMITATIONS
REQUIRE_REWORK
BLOCK_DOWNSTREAM
```

这决定后续阶段能不能继续。

---

## 5.3 验收必须分层

专业验收至少分为八类：

```text
结构验收
语义验收
合约验收
Trace 验收
权限验收
缺口验收
工具验收
运行验收
```

每一类都要有明确状态。

---

# 6. Acceptance Plane 可以做什么

```text
1. 定义验收门
2. 定义验收状态码
3. 定义验收对象注册表
4. 定义验收维度
5. 定义阻断规则
6. 定义带缺口通过规则
7. 定义缺口严重性分级
8. 定义下游权限
9. 定义验收报告结构
10. 定义验收结果包
11. 定义 HER 执行验收协议
12. 定义 P01-P10 业务控制器验收标准
13. 定义 Runner / Tool Binding 验收标准
14. 定义 Paper-only Runtime 验收标准
15. 定义 Review / Upgrade 验收标准
```

---

# 7. Acceptance Plane 不能做什么

```text
1. 不能调度任务
2. 不能替代 Trace Plane 写 trace
3. 不能替代 Handoff Plane 做交接
4. 不能创建业务阶段内容
5. 不能采集数据
6. 不能生成交易信号
7. 不能执行工具
8. 不能运行纸面交易
9. 不能绕过 Governance
10. 不能把 REJECTED 强行改成 READY
11. 不能在缺少 trace 的情况下通过验收
12. 不能允许无合约下游交接
```

---

# 8. Acceptance Plane 必须验收的对象

## 8.1 一级验收对象

|验收对象|说明|
|---|---|
|Knowledge Intake|K00 摄取是否完成任务化|
|Methodology Blueprint|方法论蓝图是否可编译|
|P00 Build Controller|是否把方法论转成系统建造任务|
|Bootstrap Plane|系统启动入口、目录、状态是否成立|
|Governance Plane|权限、红线、禁止事项是否完整|
|Domain Plane|领域对象、场景、生命周期、边界是否完整|
|Data Plane|字段、来源、raw、normalized、质量是否完整|
|Full Control Plane|任务树、状态机、合约路由是否完整|
|Trace Plane|trace_id、链路、状态、合约、运行追踪是否完整|
|Acceptance Plane 自身|验收规则是否可执行|
|Handoff Plane|交接包与下游权限是否完整|
|P01-P10 Phase Controller|每个业务阶段控制器是否合格|
|Runner / Tool Binding|工具是否绑定正确、权限是否正确|
|Paper-only Runtime|是否只纸面、可复盘、可归因|
|Review / Upgrade|是否受治理约束、是否可回滚|

---

# 9. Acceptance Plane 文件体系

建议目录：

```text
/root/sikk-gmgn/system/acceptance_plane/
```

必须创建：

```text
acceptance_plane.yaml
acceptance_context.md
acceptance_object_registry.yaml
acceptance_gate_registry.yaml
acceptance_dimension_model.yaml
acceptance_status_code_table.yaml
acceptance_score_model.yaml
acceptance_blocking_rules.yaml
acceptance_gap_policy.yaml
acceptance_trace_dependency.yaml
acceptance_contract_dependency.yaml
acceptance_artifact_check_model.yaml
acceptance_semantic_check_model.yaml
acceptance_permission_check_model.yaml
acceptance_tool_binding_check_model.yaml
acceptance_runtime_check_model.yaml
acceptance_review_upgrade_check_model.yaml
acceptance_result_packet_contract.yaml
acceptance_report_model.yaml
acceptance_storage_constitution.md
acceptance_gap_register.md
acceptance_review_checklist.md
her_acceptance_execution_protocol.md
```

---

# 10. 每个文件的作用

|文件|作用|
|---|---|
|`acceptance_plane.yaml`|验收平面身份、边界、状态码|
|`acceptance_context.md`|HER 执行前读取的验收上下文|
|`acceptance_object_registry.yaml`|注册所有需要验收的对象|
|`acceptance_gate_registry.yaml`|注册所有验收门|
|`acceptance_dimension_model.yaml`|定义验收维度|
|`acceptance_status_code_table.yaml`|验收状态码|
|`acceptance_score_model.yaml`|验收评分模型|
|`acceptance_blocking_rules.yaml`|阻断规则|
|`acceptance_gap_policy.yaml`|缺口分级与下游权限|
|`acceptance_trace_dependency.yaml`|Trace 依赖规则|
|`acceptance_contract_dependency.yaml`|合约依赖规则|
|`acceptance_artifact_check_model.yaml`|文件产物验收模型|
|`acceptance_semantic_check_model.yaml`|语义内容验收模型|
|`acceptance_permission_check_model.yaml`|权限越权验收模型|
|`acceptance_tool_binding_check_model.yaml`|工具绑定验收|
|`acceptance_runtime_check_model.yaml`|纸面运行验收|
|`acceptance_review_upgrade_check_model.yaml`|复盘升级验收|
|`acceptance_result_packet_contract.yaml`|输出给 Handoff Plane 的验收结果包|
|`acceptance_report_model.yaml`|人类可读验收报告|
|`acceptance_storage_constitution.md`|验收数据目录宪法|
|`acceptance_gap_register.md`|验收缺口登记|
|`acceptance_review_checklist.md`|验收平面自检清单|
|`her_acceptance_execution_protocol.md`|HER 如何执行验收|

---

# 11. acceptance_plane.yaml

```yaml
plane_id: ACCEPTANCE_PLANE
plane_name: 验收平面
plane_level: light_institutional
version: v2.0
status: DRAFT_READY_FOR_AUDIT

position_in_build_order:
  previous: TRACE_PLANE
  next: HANDOFF_PLANE

mission:
  primary: 对系统阶段、文件、合约、trace、工具、运行与复盘结果执行专业验收裁决
  secondary:
    - 判断阶段是否达到 READY / READY_WITH_GAPS / REJECTED
    - 判断是否允许进入 Handoff Plane
    - 判断是否允许 P01-P10 Phase Controller 定义
    - 判断是否允许 Runner / Tool Binding
    - 判断是否允许 Paper-only Runtime
    - 阻断无 trace、无合约、无验收、越权、缺口未登记的下游流转

authority:
  can_define:
    - acceptance_gates
    - acceptance_objects
    - acceptance_dimensions
    - acceptance_status_codes
    - acceptance_scores
    - blocking_rules
    - gap_policy
    - downstream_permission
    - acceptance_result_packet

  can_decide:
    - READY
    - READY_WITH_GAPS
    - REJECTED
    - BLOCKED
    - NEEDS_REWORK

  cannot_do:
    - schedule_phase
    - create_phase_content
    - write_trace
    - execute_handoff
    - collect_data
    - generate_strategy_signal
    - run_tools
    - run_paper_runtime
    - approve_live_execution

upstream_inputs:
  - trace_handoff_packet
  - full_control_task_tree
  - phase_artifact_traces
  - contract_traces
  - state_traces
  - gap_registers
  - governance_rules

downstream_outputs:
  - acceptance_result_packet
  - acceptance_report
  - acceptance_gap_register
  - downstream_permission_matrix
  - handoff_permission

status_codes:
  - ACCEPTANCE_UNINITIALIZED
  - ACCEPTANCE_CONTEXT_READY
  - ACCEPTANCE_OBJECTS_REGISTERED
  - ACCEPTANCE_GATES_READY
  - ACCEPTANCE_RUNNING
  - ACCEPTANCE_READY
  - ACCEPTANCE_READY_WITH_GAPS
  - ACCEPTANCE_REJECTED
  - ACCEPTANCE_BLOCKED
  - ACCEPTANCE_NEEDS_REWORK
```

---

# 12. acceptance_object_registry.yaml

```yaml
acceptance_objects:
  - object_type: knowledge_intake_package
    source_stage: K00
    required_trace: KNOWLEDGE_TRACE
    required_gate: GATE_K00_ACCEPTANCE

  - object_type: methodology_blueprint
    source_stage: system_methodology_blueprint
    required_trace: METHODOLOGY_TRACE
    required_gate: GATE_METHODOLOGY_BLUEPRINT_ACCEPTANCE

  - object_type: build_controller_output
    source_stage: P00
    required_trace: BUILD_TRACE
    required_gate: GATE_P00_BUILD_ACCEPTANCE

  - object_type: plane_package
    source_stage:
      - BOOTSTRAP_PLANE
      - GOVERNANCE_PLANE
      - DOMAIN_PLANE
      - DATA_PLANE
      - FULL_CONTROL_PLANE
      - TRACE_PLANE
      - ACCEPTANCE_PLANE
      - HANDOFF_PLANE
    required_trace: PHASE_TRACE
    required_gate: GATE_PLANE_PACKAGE_ACCEPTANCE

  - object_type: phase_controller_package
    source_stage: P01_P10_PHASE_CONTROLLERS
    required_trace: PHASE_TRACE
    required_gate: GATE_PHASE_CONTROLLER_ACCEPTANCE

  - object_type: tool_binding
    source_stage: RUNNER_TOOL_BINDING
    required_trace: TOOL_TRACE
    required_gate: GATE_TOOL_BINDING_ACCEPTANCE

  - object_type: paper_runtime_result
    source_stage: PAPER_ONLY_RUNTIME
    required_trace: RUNTIME_TRACE
    required_gate: GATE_PAPER_RUNTIME_ACCEPTANCE

  - object_type: review_upgrade_package
    source_stage: REVIEW_UPGRADE
    required_trace: REVIEW_TRACE
    required_gate: GATE_REVIEW_UPGRADE_ACCEPTANCE
```

---

# 13. acceptance_dimension_model.yaml

## 13.1 验收维度

```yaml
acceptance_dimensions:
  - dimension_id: STRUCTURAL_COMPLETENESS
    name_cn: 结构完整性
    question: 是否包含阶段目标要求的必要文件、字段、模型、合约、状态码

  - dimension_id: SEMANTIC_ALIGNMENT
    name_cn: 语义一致性
    question: 内容是否符合系统目标、阶段定位和 HER 底层逻辑

  - dimension_id: CONTRACT_VALIDITY
    name_cn: 合约有效性
    question: 输入合约、输出合约、handoff packet 是否完整

  - dimension_id: TRACEABILITY
    name_cn: 可追踪性
    question: 是否具备 trace_id、父子关系、来源与下游引用

  - dimension_id: GOVERNANCE_COMPLIANCE
    name_cn: 治理合规性
    question: 是否违反权限边界、禁止事项、实盘限制

  - dimension_id: GAP_TRANSPARENCY
    name_cn: 缺口透明度
    question: 已知缺口是否登记、分级、传递

  - dimension_id: DOWNSTREAM_READINESS
    name_cn: 下游可用性
    question: 下游是否能读取、理解、使用该阶段输出

  - dimension_id: REPLAYABILITY
    name_cn: 可回放性
    question: 后续是否能重建当时输入、输出、判断和状态变化

  - dimension_id: TOOL_EXECUTABILITY
    name_cn: 工具可执行性
    question: 若涉及工具，是否有输入、输出、权限、测试和 dry-run 记录

  - dimension_id: RUNTIME_SAFETY
    name_cn: 运行安全性
    question: 是否保持 paper-only，是否禁止自动实盘
```

---

# 14. acceptance_status_code_table.yaml

```yaml
acceptance_status_codes:
  ACCEPTANCE_READY:
    meaning: 全部关键验收项通过，可进入 Handoff Plane
    downstream_permission:
      - ALLOW_HANDOFF
      - ALLOW_PHASE_CONTROLLER_BUILD
      - ALLOW_TOOL_BINDING_IF_APPLICABLE

  ACCEPTANCE_READY_WITH_GAPS:
    meaning: 关键验收项通过，但存在非阻断缺口
    downstream_permission:
      - ALLOW_HANDOFF_WITH_LIMITATIONS
      - REQUIRE_GAP_PROPAGATION
      - BLOCK_RUNTIME_IF_GAPS_AFFECT_EXECUTION

  ACCEPTANCE_NEEDS_REWORK:
    meaning: 存在可修复问题，需要返工后重新验收
    downstream_permission:
      - BLOCK_HANDOFF
      - REQUIRE_REWORK_TASKS

  ACCEPTANCE_REJECTED:
    meaning: 阶段目标未达成，不能进入下游
    downstream_permission:
      - BLOCK_HANDOFF
      - BLOCK_PHASE_CONTROLLER_BUILD
      - REQUIRE_REDESIGN

  ACCEPTANCE_BLOCKED:
    meaning: 触发硬阻断规则
    downstream_permission:
      - BLOCK_ALL_DOWNSTREAM
      - REQUIRE_FULL_CONTROL_REVIEW
```

---

# 15. acceptance_score_model.yaml

验收不是简单打分，但评分可以辅助裁决。

```yaml
acceptance_score_model:
  weights:
    structural_completeness: 0.15
    semantic_alignment: 0.15
    contract_validity: 0.15
    traceability: 0.15
    governance_compliance: 0.15
    gap_transparency: 0.10
    downstream_readiness: 0.10
    replayability: 0.05

  score_thresholds:
    ACCEPTANCE_READY:
      min_score: 0.90
      blocking_failures_allowed: 0
      critical_gaps_allowed: 0

    ACCEPTANCE_READY_WITH_GAPS:
      min_score: 0.75
      blocking_failures_allowed: 0
      critical_gaps_allowed: 0
      non_blocking_gaps_allowed: true

    ACCEPTANCE_NEEDS_REWORK:
      min_score: 0.50
      blocking_failures_allowed: 0
      rework_required: true

    ACCEPTANCE_REJECTED:
      min_score: 0.00
      blocking_failures_allowed: true
```

注意：

```text
如果触发 blocking rule，即使分数高，也必须 BLOCK 或 REJECT。
```

---

# 16. acceptance_blocking_rules.yaml

```yaml
acceptance_blocking_rules:
  - rule_id: ABLOCK_001
    name: 无 trace 禁止验收通过
    condition: required_trace_missing == true
    result: ACCEPTANCE_BLOCKED
    reason: 核心对象无 trace，无法审计和复盘

  - rule_id: ABLOCK_002
    name: 输入合约缺失
    condition: required_input_contract_missing == true
    result: ACCEPTANCE_REJECTED
    reason: 阶段缺少上游输入，不能证明执行有效

  - rule_id: ABLOCK_003
    name: 输出合约缺失
    condition: required_output_contract_missing == true
    result: ACCEPTANCE_NEEDS_REWORK
    reason: 无法交接下游

  - rule_id: ABLOCK_004
    name: 阶段越权输出
    condition: forbidden_output_detected == true
    result: ACCEPTANCE_REJECTED
    reason: 当前阶段输出超出权限边界

  - rule_id: ABLOCK_005
    name: 缺口未登记
    condition: known_gap_exists == true and gap_registered == false
    result: ACCEPTANCE_NEEDS_REWORK
    reason: 缺口未登记会污染下游判断

  - rule_id: ABLOCK_006
    name: Handoff 试图绕过 Acceptance
    condition: handoff_requested == true and acceptance_status not in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]
    result: ACCEPTANCE_BLOCKED
    reason: 未通过验收不得交接

  - rule_id: ABLOCK_007
    name: Tool Binding 早于 Phase Controller 合格
    condition: tool_binding_requested == true and phase_controller_acceptance_not_ready == true
    result: ACCEPTANCE_BLOCKED
    reason: 不能先绑定工具再定义控制器

  - rule_id: ABLOCK_008
    name: Paper Runtime 无 tool_trace
    condition: paper_runtime_requested == true and tool_trace_missing == true
    result: ACCEPTANCE_BLOCKED
    reason: 纸面运行必须可追踪

  - rule_id: ABLOCK_009
    name: 自动实盘路径出现
    condition: live_execution_enabled == true
    result: ACCEPTANCE_BLOCKED
    reason: 当前阶段只允许 paper-only 或人工确认，不允许自动实盘

  - rule_id: ABLOCK_010
    name: Review Upgrade 绕过 Governance
    condition: upgrade_rule_change_requested == true and governance_approval_missing == true
    result: ACCEPTANCE_BLOCKED
    reason: 规则升级必须受治理约束
```

---

# 17. acceptance_gap_policy.yaml

缺口不是失败本身，关键是缺口是否阻断下游。

```yaml
gap_severity_policy:
  BLOCKING_GAP:
    meaning: 会导致系统误判、越权、不可复盘或执行风险
    acceptance_result: ACCEPTANCE_BLOCKED
    downstream_permission: BLOCK_ALL_DOWNSTREAM

  CRITICAL_GAP:
    meaning: 关键字段、合约、trace、状态缺失
    acceptance_result: ACCEPTANCE_REJECTED
    downstream_permission: BLOCK_HANDOFF

  HIGH_GAP:
    meaning: 影响阶段质量，但可通过返工修复
    acceptance_result: ACCEPTANCE_NEEDS_REWORK
    downstream_permission: BLOCK_HANDOFF_UNTIL_FIXED

  MEDIUM_GAP:
    meaning: 不阻断当前交接，但必须传递给下游
    acceptance_result: ACCEPTANCE_READY_WITH_GAPS
    downstream_permission: ALLOW_HANDOFF_WITH_LIMITATIONS

  LOW_GAP:
    meaning: 可登记，不影响当前阶段
    acceptance_result: ACCEPTANCE_READY_WITH_GAPS
    downstream_permission: ALLOW_HANDOFF_WITH_NOTE
```

---

# 18. acceptance_trace_dependency.yaml

Acceptance Plane 必须依赖 Trace Plane。

```yaml
trace_dependency_rules:
  - dependency_id: TRACE_DEP_001
    target: all_core_artifacts
    required_trace_type: ARTIFACT_TRACE
    missing_policy: ACCEPTANCE_BLOCKED

  - dependency_id: TRACE_DEP_002
    target: all_contracts
    required_trace_type: CONTRACT_TRACE
    missing_policy: ACCEPTANCE_REJECTED

  - dependency_id: TRACE_DEP_003
    target: all_state_transitions
    required_trace_type: STATE_TRACE
    missing_policy: ACCEPTANCE_REJECTED

  - dependency_id: TRACE_DEP_004
    target: all_handoff_packets
    required_trace_type: HANDOFF_TRACE
    missing_policy: BLOCK_HANDOFF

  - dependency_id: TRACE_DEP_005
    target: all_tool_bindings
    required_trace_type: TOOL_TRACE
    missing_policy: BLOCK_TOOL_BINDING

  - dependency_id: TRACE_DEP_006
    target: paper_runtime
    required_trace_type: RUNTIME_TRACE
    missing_policy: BLOCK_PAPER_RUNTIME
```

---

# 19. acceptance_contract_dependency.yaml

```yaml
contract_dependency_rules:
  - contract_rule_id: ACONTRACT_001
    target_stage: GOVERNANCE_PLANE
    required_contracts:
      - governance_handoff_contract
      - authority_matrix
      - forbidden_claims
    missing_policy: ACCEPTANCE_REJECTED

  - contract_rule_id: ACONTRACT_002
    target_stage: DOMAIN_PLANE
    required_contracts:
      - domain_handoff_contract
      - domain_data_requirement_map
      - reasoning_boundary
    missing_policy: ACCEPTANCE_REJECTED

  - contract_rule_id: ACONTRACT_003
    target_stage: DATA_PLANE
    required_contracts:
      - data_handoff_contract
      - field_dictionary
      - data_quality_model
      - missing_policy
      - conflict_policy
    missing_policy: ACCEPTANCE_REJECTED

  - contract_rule_id: ACONTRACT_004
    target_stage: TRACE_PLANE
    required_contracts:
      - trace_handoff_contract
      - trace_id_policy
      - trace_quality_model
    missing_policy: ACCEPTANCE_REJECTED

  - contract_rule_id: ACONTRACT_005
    target_stage: HANDOFF_PLANE
    required_contracts:
      - handoff_packet_contract
      - downstream_permission_contract
      - limitation_transfer_contract
    missing_policy: BLOCK_HANDOFF
```

---

# 20. acceptance_artifact_check_model.yaml

文件产物验收模型。

```yaml
artifact_acceptance_check:
  artifact_id: string
  file_path: string
  artifact_type:
    - MARKDOWN_DOC
    - YAML_SCHEMA
    - CONTRACT
    - REGISTRY
    - CHECKLIST
    - REPORT
    - SCRIPT
    - TEST_FILE

  required_checks:
    - file_exists
    - file_not_empty
    - required_sections_present
    - schema_valid_if_yaml
    - no_placeholder_only_content
    - has_trace_id
    - has_owner_phase
    - has_downstream_usage
    - has_acceptance_status

  result:
    passed: boolean
    failed_checks: list
    warnings: list
    acceptance_status: string
```

---

# 21. acceptance_semantic_check_model.yaml

语义验收是专业系统和普通文件系统的分水岭。

```yaml
semantic_acceptance_check:
  target_artifact: string
  target_phase: string

  semantic_checks:
    - check_id: SEM_001
      name: 阶段定位一致
      question: 内容是否符合当前 Plane / Controller 的职责边界

    - check_id: SEM_002
      name: 不越权
      question: 是否输出了当前阶段无权输出的结论

    - check_id: SEM_003
      name: 术语一致
      question: 是否使用已定义领域术语，而不是临时解释

    - check_id: SEM_004
      name: 下游可读
      question: 下游是否可以根据该文件继续执行

    - check_id: SEM_005
      name: 缺口诚实
      question: 是否明确列出无法完成或待验证部分

    - check_id: SEM_006
      name: 非空洞内容
      question: 是否包含具体字段、状态码、合约、规则、验收条件
```

---

# 22. acceptance_permission_check_model.yaml

权限验收用于防止系统越权。

```yaml
permission_acceptance_check:
  target_phase: string

  forbidden_outputs_by_phase:
    GOVERNANCE_PLANE:
      - buy_signal
      - execution_order

    DOMAIN_PLANE:
      - buy_signal
      - paper_ready
      - live_trade_permission

    DATA_PLANE:
      - dominant_side_intent_claim
      - strategy_signal
      - execution_permission

    TRACE_PLANE:
      - acceptance_decision
      - handoff_execution
      - trade_signal

    ACCEPTANCE_PLANE:
      - phase_scheduling
      - handoff_execution
      - tool_execution
      - live_trade_permission

    HANDOFF_PLANE:
      - content_generation
      - acceptance_override
      - trade_signal

    RUNNER_TOOL_BINDING:
      - live_trade_without_governance
```

---

# 23. acceptance_tool_binding_check_model.yaml

Runner / Tool Binding 必须单独验收。

```yaml
tool_binding_acceptance_check:
  tool_id: string
  tool_name: string
  binding_phase: string

  required_inputs:
    - phase_controller_acceptance_status
    - tool_trace
    - input_contract
    - output_contract
    - forbidden_actions
    - dry_run_result
    - test_result

  checks:
    tool_exists: boolean
    input_contract_valid: boolean
    output_contract_valid: boolean
    tool_trace_exists: boolean
    dry_run_passed: boolean
    tests_passed: boolean
    live_execution_disabled: boolean

  result:
    acceptance_status:
      - TOOL_BINDING_READY
      - TOOL_BINDING_READY_WITH_GAPS
      - TOOL_BINDING_REJECTED
      - TOOL_BINDING_BLOCKED
```

---

# 24. acceptance_runtime_check_model.yaml

Paper-only Runtime 验收。

```yaml
runtime_acceptance_check:
  runtime_id: string
  runtime_type: PAPER_ONLY

  required_inputs:
    - strategy_gate_acceptance
    - execution_risk_acceptance
    - tool_binding_acceptance
    - runtime_trace
    - risk_controls
    - paper_only_flag

  checks:
    paper_only_enforced: boolean
    live_execution_disabled: boolean
    runtime_trace_exists: boolean
    input_contracts_valid: boolean
    output_files_defined: boolean
    risk_events_logged: boolean
    replay_ready: boolean

  result:
    acceptance_status:
      - PAPER_RUNTIME_READY
      - PAPER_RUNTIME_READY_WITH_GAPS
      - PAPER_RUNTIME_REJECTED
      - PAPER_RUNTIME_BLOCKED
```

---

# 25. acceptance_review_upgrade_check_model.yaml

Review / Upgrade 验收。

```yaml
review_upgrade_acceptance_check:
  review_case_id: string
  upgrade_id: string | null

  required_inputs:
    - review_trace
    - runtime_trace
    - state_trace
    - failure_attribution
    - proposed_upgrade
    - governance_review_status

  checks:
    review_trace_exists: boolean
    failure_attribution_supported: boolean
    upgrade_has_source_evidence: boolean
    governance_approval_required: boolean
    rollback_plan_exists: boolean
    no_direct_runtime_rule_mutation: boolean

  result:
    acceptance_status:
      - REVIEW_READY
      - UPGRADE_READY_FOR_GOVERNANCE
      - UPGRADE_REJECTED
      - UPGRADE_BLOCKED
```

---

# 26. acceptance_result_packet_contract.yaml

Acceptance Plane 的核心输出。

```yaml
acceptance_result_packet:
  packet_id: string
  generated_at: datetime
  acceptance_plane_version: v2.0
  run_id: string

  target:
    target_stage: string
    target_phase_id: string
    target_artifacts: list
    target_trace_ids: list

  inputs:
    trace_handoff_packet_id: string
    full_control_task_tree_id: string
    contract_trace_ids: list
    state_trace_ids: list
    gap_ids: list

  acceptance_summary:
    acceptance_status:
      - ACCEPTANCE_READY
      - ACCEPTANCE_READY_WITH_GAPS
      - ACCEPTANCE_NEEDS_REWORK
      - ACCEPTANCE_REJECTED
      - ACCEPTANCE_BLOCKED
    acceptance_score: number
    blocking_failures: list
    non_blocking_gaps: list
    required_rework_tasks: list

  dimension_results:
    structural_completeness: PASS|WARN|FAIL
    semantic_alignment: PASS|WARN|FAIL
    contract_validity: PASS|WARN|FAIL
    traceability: PASS|WARN|FAIL
    governance_compliance: PASS|WARN|FAIL
    gap_transparency: PASS|WARN|FAIL
    downstream_readiness: PASS|WARN|FAIL
    replayability: PASS|WARN|FAIL

  downstream_permission:
    handoff_allowed: boolean
    handoff_mode:
      - FULL_HANDOFF
      - LIMITED_HANDOFF
      - BLOCK_HANDOFF
    phase_controller_build_allowed: boolean
    tool_binding_allowed: boolean
    paper_runtime_allowed: boolean
    live_runtime_allowed: false

  limitation_tags:
    - GAP_PROPAGATION_REQUIRED
    - WEAK_USE_ONLY
    - MANUAL_REVIEW_REQUIRED
    - RUNTIME_BLOCKED
    - TOOL_BINDING_BLOCKED

  forbidden_actions:
    - HANDOFF_WITHOUT_ACCEPTANCE
    - TOOL_BINDING_WITHOUT_ACCEPTANCE
    - PAPER_RUNTIME_WITHOUT_ACCEPTANCE
    - LIVE_EXECUTION
```

---

# 27. acceptance_report_model.yaml

人类可读报告结构。

```yaml
acceptance_report:
  report_id: string
  target_stage: string
  generated_at: datetime

  executive_summary:
    final_status: string
    main_reason: string
    can_move_to_next_stage: boolean

  passed_checks:
    - check_id: string
      check_name: string
      evidence_trace_ids: list

  failed_checks:
    - check_id: string
      check_name: string
      severity: string
      reason: string
      required_fix: string

  gaps:
    blocking_gaps: list
    non_blocking_gaps: list

  downstream_permission:
    handoff: string
    phase_controller: string
    tool_binding: string
    paper_runtime: string

  next_actions:
    required_rework: list
    optional_improvements: list
```

---

# 28. acceptance_storage_constitution.md

建议目录：

```text
/root/sikk-gmgn/data/acceptance_plane/
  acceptance_results/
  acceptance_reports/
  acceptance_gates/
  acceptance_scores/
  acceptance_gaps/
  acceptance_blocking_events/
  acceptance_rework_tasks/
  handoff_permissions/
  audit/
```

原则：

```text
1. acceptance_results 存机器可读验收结果。
2. acceptance_reports 存人类可读报告。
3. acceptance_gates 存验收门执行记录。
4. acceptance_scores 存评分明细。
5. acceptance_gaps 存缺口登记。
6. acceptance_blocking_events 存阻断事件。
7. acceptance_rework_tasks 存返工任务。
8. handoff_permissions 存下游交接权限。
9. audit 存审计记录。
```

---

# 29. Acceptance Plane 的验收门体系

## 29.1 基础设施层验收门

```yaml
infrastructure_acceptance_gates:
  - GATE_K00_READY
  - GATE_METHODOLOGY_BLUEPRINT_READY
  - GATE_P00_BUILD_READY
  - GATE_BOOTSTRAP_READY
  - GATE_GOVERNANCE_READY
  - GATE_DOMAIN_READY
  - GATE_DATA_READY
  - GATE_FULL_CONTROL_READY
  - GATE_TRACE_READY
  - GATE_ACCEPTANCE_READY
  - GATE_HANDOFF_READY
```

---

## 29.2 业务控制器层验收门

```yaml
phase_controller_acceptance_gates:
  - GATE_P01_CANDIDATE_INTAKE_READY
  - GATE_P02_SOURCE_DATA_FACT_READY
  - GATE_P03_WALLET_ENTITY_READY
  - GATE_P04_CHIP_STRUCTURE_READY
  - GATE_P05_EVIDENCE_CONTROLLER_READY
  - GATE_P06_SCENARIO_RECOGNITION_READY
  - GATE_P07_STRATEGY_GATE_READY
  - GATE_P08_EXECUTION_RISK_READY
  - GATE_P09_REVIEW_REPLAY_READY
  - GATE_P10_SELF_UPGRADE_READY
```

---

## 29.3 运行层验收门

```yaml
runtime_acceptance_gates:
  - GATE_TOOL_BINDING_READY
  - GATE_DRY_RUN_READY
  - GATE_TESTS_READY
  - GATE_PAPER_RUNTIME_READY
  - GATE_PAPER_REPORT_READY
  - GATE_REVIEW_UPGRADE_READY
```

---

# 30. Acceptance Plane 自身验收标准

## 30.1 ACCEPTANCE_READY

必须满足：

```text
1. acceptance_plane.yaml 已完成
2. acceptance_context.md 已完成
3. acceptance_object_registry.yaml 已完成
4. acceptance_gate_registry.yaml 已完成
5. acceptance_dimension_model.yaml 已完成
6. acceptance_status_code_table.yaml 已完成
7. acceptance_score_model.yaml 已完成
8. acceptance_blocking_rules.yaml 已完成
9. acceptance_gap_policy.yaml 已完成
10. acceptance_trace_dependency.yaml 已完成
11. acceptance_contract_dependency.yaml 已完成
12. acceptance_artifact_check_model.yaml 已完成
13. acceptance_semantic_check_model.yaml 已完成
14. acceptance_permission_check_model.yaml 已完成
15. acceptance_tool_binding_check_model.yaml 已完成
16. acceptance_runtime_check_model.yaml 已完成
17. acceptance_review_upgrade_check_model.yaml 已完成
18. acceptance_result_packet_contract.yaml 已完成
19. acceptance_report_model.yaml 已完成
20. acceptance_storage_constitution.md 已完成
21. acceptance_gap_register.md 已完成
22. acceptance_review_checklist.md 已完成
23. her_acceptance_execution_protocol.md 已完成
24. 已定义 READY / READY_WITH_GAPS / REJECTED / BLOCKED / NEEDS_REWORK
25. 已定义阻断规则
26. 已定义下游权限
27. 已定义 Handoff Plane 读取方式
28. 已定义 Tool Binding 和 Paper Runtime 验收方式
29. 不存在无 Trace 即可通过验收的路径
30. 不存在无 Acceptance 即可 Handoff 的路径
```

---

## 30.2 ACCEPTANCE_READY_WITH_GAPS

允许进入 Handoff Plane，但必须带限制：

```text
1. 部分验收门尚未代码化，但规则已定义
2. 部分历史文件没有完整 trace，只能从新体系开始验收
3. 部分工具验收只能 dry-run，未跑真实样本
4. Paper Runtime 验收模型存在，但未真实跑通
5. Review / Upgrade 验收模型存在，但样本不足
6. 部分 acceptance score 权重尚未回测
```

限制：

```text
可以进入 Handoff Plane
可以建立 handoff 草案
可以继续 P01-P10 控制器设计
不允许进入自动 Paper Runtime
不允许启用实盘路径
不允许标记系统全链路完成
```

---

## 30.3 ACCEPTANCE_REJECTED

以下情况必须驳回：

```text
1. Acceptance Plane 只是检查清单
2. 没有验收对象注册表
3. 没有验收门注册表
4. 没有 READY / WITH_GAPS / REJECTED 标准
5. 没有阻断规则
6. 没有 Trace 依赖
7. 没有合约依赖
8. 没有下游权限模型
9. Handoff Plane 可以绕过 Acceptance
10. Runner 可以绕过 Acceptance
11. Paper Runtime 可以绕过 Acceptance
12. 自动实盘路径没有被阻断
13. Review / Upgrade 可以绕过 Governance
```

---

# 31. HER Acceptance 执行协议

文件：

```text
her_acceptance_execution_protocol.md
```

HER 执行验收时必须按这个顺序：

```text
1. 读取 acceptance_context.md
2. 读取 acceptance_object_registry.yaml
3. 读取目标阶段的 trace_handoff_packet
4. 读取 Full Control Plane 的 task_tree
5. 读取目标阶段产物文件列表
6. 读取 contract_trace
7. 读取 state_trace
8. 读取 gap_register
9. 执行 artifact check
10. 执行 semantic check
11. 执行 contract check
12. 执行 traceability check
13. 执行 governance permission check
14. 执行 gap check
15. 执行 downstream readiness check
16. 计算 acceptance_score
17. 检查 blocking rules
18. 输出 acceptance_result_packet
19. 输出 acceptance_report
20. 写入 acceptance_trace
21. 给 Handoff Plane 输出 handoff permission
```

禁止：

```text
1. 不允许未读取 trace_handoff_packet 就验收
2. 不允许只看文件是否存在
3. 不允许忽略缺口
4. 不允许忽略越权输出
5. 不允许未生成 acceptance_result_packet 就进入 Handoff
6. 不允许未验收 Tool Binding 就运行工具
7. 不允许未验收 Paper Runtime 就开始纸面运行
8. 不允许任何自动实盘路径通过验收
```

---

# 32. Full Control Plane 需要同步更新

Acceptance Plane 加入后，Full Control Plane 必须更新：

```yaml
phase_execution_order:
  - K00_KNOWLEDGE_INTAKE
  - SYSTEM_METHODOLOGY_BLUEPRINT
  - P00_BUILD_CONTROLLER
  - BOOTSTRAP_CONTROL_PLANE
  - GOVERNANCE_PLANE
  - DOMAIN_PLANE
  - DATA_PLANE
  - FULL_CONTROL_PLANE
  - TRACE_PLANE
  - ACCEPTANCE_PLANE
  - HANDOFF_PLANE
  - P01_P10_PHASE_CONTROLLERS
  - RUNNER_TOOL_BINDING
  - PAPER_ONLY_RUNTIME
  - REVIEW_UPGRADE
```

新增路由：

```yaml
contract_routes:
  - route_id: ROUTE_TRACE_TO_ACCEPTANCE
    from_stage: TRACE_PLANE
    to_stage: ACCEPTANCE_PLANE
    required_packet: trace_handoff_packet
    missing_policy: BLOCK_ACCEPTANCE

  - route_id: ROUTE_ACCEPTANCE_TO_HANDOFF
    from_stage: ACCEPTANCE_PLANE
    to_stage: HANDOFF_PLANE
    required_packet: acceptance_result_packet
    missing_policy: BLOCK_HANDOFF
```

新增状态码：

```yaml
global_status_codes:
  - ACCEPTANCE_READY
  - ACCEPTANCE_READY_WITH_GAPS
  - ACCEPTANCE_NEEDS_REWORK
  - ACCEPTANCE_REJECTED
  - ACCEPTANCE_BLOCKED
```

新增硬规则：

```yaml
global_hard_negative_rules:
  - Handoff without Acceptance is blocked
  - Tool Binding without Acceptance is blocked
  - Paper Runtime without Acceptance is blocked
  - Live execution remains blocked
```

---

# 33. 给 HER 的可执行任务书

```text
任务名称：建立 Acceptance Plane｜验收平面专业版 v2.0

目标：
在 /root/sikk-gmgn/system/acceptance_plane/ 下建立 SIKK Stable Trader OS 的 Acceptance Plane。该平面不是普通检查清单，也不是文件是否存在检查，而是系统验收裁决平面。它负责读取 Trace Plane 的 trace_handoff_packet、Full Control Plane 的任务树、各阶段产物、输入输出合约、状态码、缺口登记和治理规则，对系统建造阶段、业务 Phase Controller、Runner / Tool Binding、Paper-only Runtime、Review / Upgrade 执行 READY / READY_WITH_GAPS / NEEDS_REWORK / REJECTED / BLOCKED 裁决。

当前专业版建造顺序固定为：
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md：系统方法论蓝图
  ↓
P00：系统建造与方法论编译控制器
  ↓
Bootstrap Control Plane：启动控制面
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Full Control Plane：完整控制面
  ↓
Trace Plane：追踪平面
  ↓
Acceptance Plane：验收平面
  ↓
Handoff Plane：交接平面
  ↓
P01-P10 Phase Controller：业务阶段控制器
  ↓
Runner / Tool Binding：执行工具绑定
  ↓
Paper-only Runtime：纸面验证运行
  ↓
Review / Upgrade：复盘与升级

核心原则：
1. Acceptance Plane 不调度任务，调度属于 Full Control Plane。
2. Acceptance Plane 不写 trace，trace 属于 Trace Plane。
3. Acceptance Plane 不执行交接，交接属于 Handoff Plane。
4. Acceptance Plane 不创建业务内容。
5. Acceptance Plane 不运行工具。
6. Acceptance Plane 不运行纸面交易。
7. Acceptance Plane 不允许自动实盘路径通过。
8. Acceptance Plane 必须读取 trace_handoff_packet。
9. Handoff Plane 不允许绕过 Acceptance Plane。
10. Runner / Tool Binding 不允许绕过 Acceptance Plane。
11. Paper-only Runtime 不允许绕过 Acceptance Plane。
12. Review / Upgrade 不允许绕过 Governance 和 Acceptance。

需要创建目录：
/root/sikk-gmgn/system/acceptance_plane/

需要创建文件：
1. acceptance_plane.yaml
2. acceptance_context.md
3. acceptance_object_registry.yaml
4. acceptance_gate_registry.yaml
5. acceptance_dimension_model.yaml
6. acceptance_status_code_table.yaml
7. acceptance_score_model.yaml
8. acceptance_blocking_rules.yaml
9. acceptance_gap_policy.yaml
10. acceptance_trace_dependency.yaml
11. acceptance_contract_dependency.yaml
12. acceptance_artifact_check_model.yaml
13. acceptance_semantic_check_model.yaml
14. acceptance_permission_check_model.yaml
15. acceptance_tool_binding_check_model.yaml
16. acceptance_runtime_check_model.yaml
17. acceptance_review_upgrade_check_model.yaml
18. acceptance_result_packet_contract.yaml
19. acceptance_report_model.yaml
20. acceptance_storage_constitution.md
21. acceptance_gap_register.md
22. acceptance_review_checklist.md
23. her_acceptance_execution_protocol.md

文件要求：
- acceptance_plane.yaml：定义 Acceptance Plane 的身份、使命、权限、边界、上游输入、下游输出、状态码。
- acceptance_context.md：写成 HER 执行前必须读取的验收上下文。
- acceptance_object_registry.yaml：注册所有验收对象，包括 K00、方法论蓝图、P00、各 Plane、P01-P10、Tool Binding、Paper Runtime、Review / Upgrade。
- acceptance_gate_registry.yaml：注册全部验收门。
- acceptance_dimension_model.yaml：定义结构完整性、语义一致性、合约有效性、可追踪性、治理合规性、缺口透明度、下游可用性、可回放性、工具可执行性、运行安全性。
- acceptance_status_code_table.yaml：定义 ACCEPTANCE_READY、ACCEPTANCE_READY_WITH_GAPS、ACCEPTANCE_NEEDS_REWORK、ACCEPTANCE_REJECTED、ACCEPTANCE_BLOCKED。
- acceptance_score_model.yaml：定义验收评分模型，但必须明确 blocking rule 高于分数。
- acceptance_blocking_rules.yaml：定义无 trace、无合约、阶段越权、缺口未登记、绕过 Acceptance、自动实盘等硬阻断规则。
- acceptance_gap_policy.yaml：定义 BLOCKING_GAP、CRITICAL_GAP、HIGH_GAP、MEDIUM_GAP、LOW_GAP 及下游权限。
- acceptance_trace_dependency.yaml：定义所有核心对象必须依赖 trace。
- acceptance_contract_dependency.yaml：定义每个阶段必须具备的输入输出合约。
- acceptance_artifact_check_model.yaml：定义文件产物验收。
- acceptance_semantic_check_model.yaml：定义语义内容验收。
- acceptance_permission_check_model.yaml：定义权限越权验收。
- acceptance_tool_binding_check_model.yaml：定义工具绑定验收。
- acceptance_runtime_check_model.yaml：定义 Paper-only Runtime 验收。
- acceptance_review_upgrade_check_model.yaml：定义复盘升级验收。
- acceptance_result_packet_contract.yaml：定义 acceptance_result_packet。
- acceptance_report_model.yaml：定义人类可读验收报告。
- acceptance_storage_constitution.md：定义验收数据目录。
- acceptance_gap_register.md：登记当前验收体系缺口。
- acceptance_review_checklist.md：建立验收平面审计清单。
- her_acceptance_execution_protocol.md：定义 HER 如何执行验收。

同时更新 Full Control Plane：
1. 在 phase_execution_order.yaml 中加入 Acceptance Plane。
2. 在 contract_router.yaml 中加入 ROUTE_TRACE_TO_ACCEPTANCE 和 ROUTE_ACCEPTANCE_TO_HANDOFF。
3. 在 global_status_code_table.yaml 中加入 ACCEPTANCE_READY、ACCEPTANCE_READY_WITH_GAPS、ACCEPTANCE_NEEDS_REWORK、ACCEPTANCE_REJECTED、ACCEPTANCE_BLOCKED。
4. 在 acceptance_gate_registry.yaml 或 Full Control registry 中注册 Acceptance Plane 的验收门。
5. 在 global_hard_negative_rules.yaml 中加入：Handoff without Acceptance blocked、Tool Binding without Acceptance blocked、Paper Runtime without Acceptance blocked、Live execution blocked。

验收输出：
1. 文件创建清单
2. 每个文件的核心摘要
3. ACCEPTANCE_READY / ACCEPTANCE_READY_WITH_GAPS / ACCEPTANCE_REJECTED 判断
4. 验收对象注册摘要
5. 验收门摘要
6. 阻断规则摘要
7. Trace 依赖摘要
8. Handoff Plane 如何读取 Acceptance 输出
9. Tool Binding 如何受 Acceptance 限制
10. Paper-only Runtime 如何受 Acceptance 限制
11. 当前缺口清单
12. 是否达到轻量机构级 Acceptance Plane v2.0

最终验收标准：
只有当验收对象、验收门、验收维度、状态码、评分模型、阻断规则、缺口分级、Trace 依赖、合约依赖、文件验收、语义验收、权限验收、工具验收、运行验收、复盘升级验收、acceptance_result_packet、验收报告、存储宪法、HER 验收执行协议全部存在，并且 Handoff / Tool Binding / Paper Runtime 不能绕过 Acceptance 时，才允许标记为 ACCEPTANCE_READY。
```

---

# 34. 当前是否达到轻量机构级专业标准？

## 判断

按这版设计，Acceptance Plane 达到：

```text
轻量机构级 v2.0 设计标准
```

它不再是“检查清单”，而是系统里的**验收裁决基础设施**。

---

## 已经达到的能力

|能力|状态|
|---|---|
|验收对象注册|已设计|
|验收门体系|已设计|
|验收维度|已设计|
|验收状态码|已设计|
|阻断规则|已设计|
|缺口分级|已设计|
|Trace 依赖|已设计|
|合约依赖|已设计|
|文件验收|已设计|
|语义验收|已设计|
|权限验收|已设计|
|工具绑定验收|已设计|
|纸面运行验收|已设计|
|复盘升级验收|已设计|
|验收结果包|已设计|
|HER 验收协议|已设计|
|下游权限控制|已设计|

---

## 还没达到工程级落地的部分

|缺口|原因|后续处理|
|---|---|---|
|acceptance validator 未代码化|当前是模型设计|后续实现 `acceptance_validator.py`|
|验收门还未真实执行|需要 HER 跑文件检查|HER 执行阶段处理|
|score 权重未回测|需要运行样本|Review / Upgrade 校准|
|Tool Binding 验收还没有真实工具样本|Runner 阶段未到|后续接入|
|Paper Runtime 验收未真实跑通|Runtime 阶段未到|后续验证|
|Review / Upgrade 验收样本不足|需要纸面运行积累|后续积累|
|legacy 文件无法全部补 trace|旧文件天然缺失|只做 legacy acceptance with gaps|
|Handoff Plane 尚未设计|下一步|继续展开|

---

# 35. 下一步应该做什么

Acceptance Plane 完成后，下一步应该是：

```text
Handoff Plane：交接平面
```

原因：

```text
Acceptance Plane 只判断是否合格。
Handoff Plane 负责把合格结果按权限交给下游。
```

正确推进顺序：

```text
Trace Plane
  ↓
Acceptance Plane
  ↓
Handoff Plane
  ↓
P01-P10 Phase Controller
```

Handoff Plane 需要读取：

```text
acceptance_result_packet
trace_handoff_packet
gap_register
downstream_permission
limitation_tags
forbidden_actions
```

然后生成：

```text
handoff_packet
handoff_permission
downstream_read_instruction
gap_propagation_packet
```

---

# 本次认知升级点

1. **Acceptance Plane 是裁决平面，不是检查清单。**
    
2. **文件存在不等于阶段完成。**  
    必须同时通过结构、语义、合约、trace、权限、缺口和下游可用性验收。
    
3. **Trace Plane 是 Acceptance Plane 的前置输入。**  
    无 trace 不允许验收通过。
    
4. **Acceptance Plane 输出的是下游权限。**  
    它决定能否 Handoff、能否 Tool Binding、能否 Paper Runtime。
    
5. **Blocking Rule 高于评分。**  
    即使分数高，触发硬阻断也必须 BLOCK。
    
6. **Handoff Plane 必须受 Acceptance Plane 控制。**
    
7. **Runner / Tool Binding 必须受 Acceptance Plane 控制。**
    
8. **Paper-only Runtime 必须经过 Acceptance 验收，且自动实盘必须保持阻断。**
    

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|Handoff Plane 尚未完整设计|下一阶段|继续展开|
|acceptance validator 未实现|模型已定义|工程阶段实现|
|验收门未自动化|先定义规则|后续写脚本|
|legacy 文件验收标准需单独处理|旧系统缺 trace|设置 legacy_with_gaps|
|Tool Binding 样本不足|还未进入工具阶段|后续接入|
|Paper Runtime 样本不足|后续运行验证|Runtime 阶段|
|Review / Upgrade 验收样本不足|需要纸面结果|后续积累|
|score 权重未校准|当前为初版权重|Self-Upgrade 阶段校准|
|Full Control Plane 仍需同步更新 Acceptance 路由|已定义|HER 执行修正|
|Handoff Plane 的权限传递模型未设计|下一步核心|设计 Handoff Plane|