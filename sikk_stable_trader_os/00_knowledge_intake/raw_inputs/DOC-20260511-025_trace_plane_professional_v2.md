# Trace Plane：追踪平面专业版设计 v2.0

## 0. 核心修正

你现在要的 **Trace Plane**，已经不再是之前那个简单的：

```text
Data Plane → Trace Plane → Evidence Plane
```

中间层。

在你新的专业版建造顺序里，Trace Plane 应该升级为：

```text
全系统建造链路 + 阶段运行链路 + 数据证据链路 + 验收交接链路 + 复盘升级链路
```

也就是说：

> **Trace Plane 是 SIKK Stable Trader OS 的全链路追踪平面。**  
> 它负责让系统中每一个文件、字段、任务、阶段、合约、状态、验收、交接、工具调用、纸面运行和复盘结论，都能被追溯、审计、回放、归因。

---

# 1. Trace Plane 在专业版建造顺序中的位置

你的新顺序应固定为：

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

在这个位置里，Trace Plane 的作用不是生成业务判断，而是给后面所有阶段提供：

```text
可追踪性
可审计性
可验收性
可交接性
可回放性
可失败归因性
```

---

# 2. Trace Plane 的专业定义

```text
Trace Plane 是系统追踪平面。

它负责为 SIKK Stable Trader OS 的知识摄取、方法论编译、启动控制、治理规则、领域模型、数据模型、完整控制面、阶段任务树、输入输出合约、状态迁移、验收门、交接包、业务 Phase Controller、工具绑定、纸面运行、复盘升级建立统一 trace_id、追踪模型、引用链、审计链和回放链。

它不直接生成策略判断，不直接采集数据，不直接验收阶段，不直接交接下游，不直接执行工具，而是为这些动作提供可追溯的结构骨架。
```

简化理解：

```text
Full Control Plane 决定系统怎么调度。
Trace Plane 记录系统怎么发生。
Acceptance Plane 判断是否通过。
Handoff Plane 决定如何交接。
P01-P10 执行业务阶段。
```

---

# 3. Trace Plane 需要解决的核心问题

|问题|没有 Trace Plane 的后果|Trace Plane 的专业处理|
|---|---|---|
|HER 创建了文件，但不知道为什么创建|文件堆积，无法审计|建立任务 → 文件 trace|
|阶段完成了，但不知道是否符合目标|文件完成 ≠ 阶段完成|建立阶段输出 trace|
|Data Plane 字段被下游使用，但来源不清|证据不可复核|建立字段血缘 trace|
|状态从 WATCHING 变成 BLOCKED，但原因不清|无法复盘|建立状态迁移 trace|
|Acceptance Plane 验收失败，但失败点不清|无法修复|建立验收失败 trace|
|Handoff 包交给下游，但缺口没传递|下游误用数据|建立交接 trace|
|Runner 调用了脚本，但输入输出不清|运行不可复现|建立工具调用 trace|
|纸面交易失败，但不知道错在哪一层|无法升级系统|建立失败归因 trace|
|Review 提出升级，但不知道改动依据|规则污染|建立升级建议 trace|

---

# 4. Trace Plane 的边界

## 4.1 Trace Plane 可以做

```text
1. 定义 trace_id 体系
2. 定义阶段追踪模型
3. 定义任务树追踪模型
4. 定义文件产物追踪模型
5. 定义字段血缘追踪模型
6. 定义合约追踪模型
7. 定义状态迁移追踪模型
8. 定义验收追踪模型
9. 定义交接追踪模型
10. 定义工具调用追踪模型
11. 定义纸面运行追踪模型
12. 定义复盘回放追踪模型
13. 定义失败归因追踪模型
14. 定义升级建议追踪模型
15. 输出 trace_handoff_packet
```

---

## 4.2 Trace Plane 不能做

```text
1. 不能替代 Full Control Plane 做调度
2. 不能替代 Acceptance Plane 做通过 / 驳回裁决
3. 不能替代 Handoff Plane 做下游交接
4. 不能替代 Data Plane 采集数据
5. 不能替代 Evidence Controller 生成证据判断
6. 不能替代 Strategy Gate 输出 PAPER_READY
7. 不能替代 Runner 执行工具
8. 不能修改 raw 数据
9. 不能静默丢弃缺口
10. 不能让无 trace 的内容进入验收与交接
```

---

# 5. Trace Plane 的底层逻辑模型

## 5.1 HER 系统视角

HER 不是只需要“读文档”，而是要知道：

```text
我正在执行哪个阶段？
这个阶段来自哪个方法论目标？
当前任务属于哪个任务树？
输入是什么？
输出是什么？
生成了哪些文件？
这些文件被谁使用？
有没有通过验收？
失败点在哪里？
下一阶段能不能读取？
```

所以 Trace Plane 必须服务于 HER 的长期自动化执行。

---

## 5.2 情报链路视角

专业系统不能只说：

```text
这个判断成立。
```

而要能回答：

```text
这个判断基于哪个字段？
字段来自哪个 raw？
raw 来自哪个数据源？
什么时候采集？
经过什么标准化？
被哪个阶段引用？
是否存在反证？
是否通过验收？
是否被交接给下游？
后续运行结果如何？
```

---

## 5.3 控制论视角

系统是状态机，不是文档集合。

每一次状态变化都必须有 trace：

```text
输入状态
  ↓
触发条件
  ↓
处理阶段
  ↓
引用证据
  ↓
输出状态
  ↓
验收结果
  ↓
下游权限
```

---

## 5.4 审计视角

Trace Plane 必须让系统可以被审计：

```text
谁创建了这个文件？
为什么创建？
它对应哪个阶段？
是否满足合约？
是否有验收记录？
是否被下游引用？
后续是否导致失败？
```

---

# 6. Trace Plane 必须追踪的对象

## 6.1 一级追踪对象

|追踪对象|作用|
|---|---|
|Knowledge Trace|追踪 K00 摄取的知识来源|
|Methodology Trace|追踪方法论蓝图如何形成|
|Build Trace|追踪 P00 如何把方法论编译成系统建造任务|
|Bootstrap Trace|追踪启动控制面的目录、状态、入口|
|Governance Trace|追踪治理规则、权限、禁止事项|
|Domain Trace|追踪领域对象、术语、生命周期、场景语义|
|Data Trace|追踪字段、raw、normalized、质量、缺失、冲突|
|Full Control Trace|追踪任务树、阶段调度、状态回写|
|Phase Trace|追踪 P01-P10 每个业务控制器|
|Contract Trace|追踪输入合约、输出合约、handoff packet|
|Acceptance Trace|追踪验收门、失败项、READY / WITH_GAPS / REJECTED|
|Handoff Trace|追踪上下游交接、字段权限、缺口传递|
|Tool Trace|追踪 Runner / Tool Binding 调用|
|Runtime Trace|追踪 Paper-only Runtime 的运行过程|
|Review Trace|追踪复盘、失败归因、升级建议|
|Upgrade Trace|追踪规则、字段、参数、方法论升级路径|

---

# 7. Trace Plane 文件体系

建议目录：

```text
/root/sikk-gmgn/system/trace_plane/
```

必须创建：

```text
trace_plane.yaml
trace_context.md
trace_id_policy.yaml
trace_object_registry.yaml
knowledge_trace_model.yaml
methodology_trace_model.yaml
build_trace_model.yaml
phase_trace_model.yaml
task_tree_trace_model.yaml
artifact_trace_model.yaml
field_lineage_model.yaml
contract_trace_model.yaml
state_trace_model.yaml
acceptance_trace_model.yaml
handoff_trace_model.yaml
tool_binding_trace_model.yaml
runtime_trace_model.yaml
review_trace_model.yaml
upgrade_trace_model.yaml
error_trace_model.yaml
trace_quality_model.yaml
trace_storage_constitution.md
trace_handoff_contract.yaml
trace_acceptance_criteria.md
trace_gap_register.md
trace_review_checklist.md
her_trace_execution_protocol.md
```

---

# 8. 文件作用表

|文件|作用|
|---|---|
|`trace_plane.yaml`|追踪平面阶段身份证|
|`trace_context.md`|HER 执行前读取的追踪上下文|
|`trace_id_policy.yaml`|全系统 trace_id 规则|
|`trace_object_registry.yaml`|注册所有需要追踪的对象类型|
|`knowledge_trace_model.yaml`|K00 知识摄取追踪|
|`methodology_trace_model.yaml`|方法论蓝图形成过程追踪|
|`build_trace_model.yaml`|P00 系统建造编译追踪|
|`phase_trace_model.yaml`|各 Plane / Phase Controller 追踪|
|`task_tree_trace_model.yaml`|任务树追踪|
|`artifact_trace_model.yaml`|文件、Schema、合约等产物追踪|
|`field_lineage_model.yaml`|字段血缘追踪|
|`contract_trace_model.yaml`|输入输出合约追踪|
|`state_trace_model.yaml`|状态迁移追踪|
|`acceptance_trace_model.yaml`|验收过程追踪|
|`handoff_trace_model.yaml`|交接过程追踪|
|`tool_binding_trace_model.yaml`|工具绑定与调用追踪|
|`runtime_trace_model.yaml`|纸面运行追踪|
|`review_trace_model.yaml`|复盘归因追踪|
|`upgrade_trace_model.yaml`|升级建议追踪|
|`error_trace_model.yaml`|缺失、冲突、断链、越权追踪|
|`trace_quality_model.yaml`|Trace 完整性评分|
|`trace_storage_constitution.md`|追踪数据目录宪法|
|`trace_handoff_contract.yaml`|输出给 Acceptance / Handoff / P01-P10 的追踪包|
|`trace_acceptance_criteria.md`|Trace Plane 自身验收标准|
|`trace_gap_register.md`|追踪缺口登记|
|`trace_review_checklist.md`|追踪平面审计清单|
|`her_trace_execution_protocol.md`|HER 如何写入和读取 trace|

---

# 9. trace_plane.yaml 阶段身份证

```yaml
plane_id: TRACE_PLANE
plane_name: 追踪平面
plane_level: light_institutional
version: v2.0
status: DRAFT_READY_FOR_AUDIT

position_in_build_order:
  previous: FULL_CONTROL_PLANE
  next:
    - ACCEPTANCE_PLANE
    - HANDOFF_PLANE
    - P01_P10_PHASE_CONTROLLERS

mission:
  primary: 建立 SIKK Stable Trader OS 的全系统追踪链路
  secondary:
    - 追踪知识摄取到方法论蓝图的来源
    - 追踪方法论蓝图到系统建造任务的编译过程
    - 追踪每个 Plane / Phase Controller 的输入、输出、状态、合约、验收、交接
    - 追踪字段、事件、快照、证据、判断、工具调用、纸面运行、复盘升级
    - 为 Acceptance Plane 提供验收依据
    - 为 Handoff Plane 提供交接依据
    - 为 Review / Upgrade 提供失败归因依据

authority:
  can_define:
    - trace_id_policy
    - trace_object_registry
    - task_trace
    - artifact_trace
    - field_lineage_trace
    - contract_trace
    - state_trace
    - acceptance_trace
    - handoff_trace
    - tool_trace
    - runtime_trace
    - review_trace
    - upgrade_trace
    - error_trace
    - trace_quality

  cannot_do:
    - schedule_phase
    - accept_or_reject_phase
    - execute_handoff
    - collect_raw_data
    - generate_strategy_signal
    - execute_trade
    - modify_raw_data
    - bypass_acceptance
    - bypass_governance

status_codes:
  - TRACE_UNINITIALIZED
  - TRACE_CONTEXT_READY
  - TRACE_ID_POLICY_READY
  - TRACE_OBJECTS_REGISTERED
  - TRACE_MODELS_READY
  - TRACE_CHAIN_READY
  - TRACE_READY
  - TRACE_READY_WITH_GAPS
  - TRACE_REJECTED
  - TRACE_INCOMPLETE
  - TRACE_BROKEN
  - TRACE_REPLAY_READY
```

---

# 10. trace_id_policy.yaml

Trace ID 是系统可审计能力的最小单位。

```yaml
trace_id_policy:
  format: "{trace_type}_{scope}_{object_short}_{timestamp}_{hash}"

  trace_types:
    - KNOWLEDGE_TRACE
    - METHODOLOGY_TRACE
    - BUILD_TRACE
    - BOOTSTRAP_TRACE
    - GOVERNANCE_TRACE
    - DOMAIN_TRACE
    - DATA_TRACE
    - FULL_CONTROL_TRACE
    - PHASE_TRACE
    - TASK_TRACE
    - ARTIFACT_TRACE
    - FIELD_TRACE
    - CONTRACT_TRACE
    - STATE_TRACE
    - ACCEPTANCE_TRACE
    - HANDOFF_TRACE
    - TOOL_TRACE
    - RUNTIME_TRACE
    - REVIEW_TRACE
    - UPGRADE_TRACE
    - ERROR_TRACE
    - AUDIT_TRACE

  requirements:
    global_unique: true
    deterministic_when_possible: true
    timestamp_required: true
    hash_required: true
    parent_trace_supported: true
    child_trace_supported: true

  relation_types:
    - CREATED_FROM
    - DEPENDS_ON
    - PRODUCES
    - CONSUMES
    - VALIDATES
    - REJECTS
    - HANDS_OFF_TO
    - TRIGGERS
    - BLOCKS
    - UPGRADES
```

---

# 11. trace_object_registry.yaml

```yaml
trace_objects:
  - object_type: knowledge_source
    source_stage: K00
    must_have_trace: true
    trace_model: knowledge_trace_model

  - object_type: methodology_blueprint
    source_stage: system_methodology_blueprint
    must_have_trace: true
    trace_model: methodology_trace_model

  - object_type: phase_controller_candidate
    source_stage: K00
    must_have_trace: true
    trace_model: build_trace_model

  - object_type: plane_file
    source_stage: ALL_PLANES
    must_have_trace: true
    trace_model: artifact_trace_model

  - object_type: input_contract
    source_stage: ALL_PLANES
    must_have_trace: true
    trace_model: contract_trace_model

  - object_type: output_contract
    source_stage: ALL_PLANES
    must_have_trace: true
    trace_model: contract_trace_model

  - object_type: status_transition
    source_stage: FULL_CONTROL_AND_RUNTIME
    must_have_trace: true
    trace_model: state_trace_model

  - object_type: acceptance_result
    source_stage: ACCEPTANCE_PLANE
    must_have_trace: true
    trace_model: acceptance_trace_model

  - object_type: handoff_packet
    source_stage: HANDOFF_PLANE
    must_have_trace: true
    trace_model: handoff_trace_model

  - object_type: tool_execution
    source_stage: RUNNER_TOOL_BINDING
    must_have_trace: true
    trace_model: tool_binding_trace_model

  - object_type: paper_runtime_event
    source_stage: PAPER_ONLY_RUNTIME
    must_have_trace: true
    trace_model: runtime_trace_model
```

---

# 12. Knowledge Trace：知识摄取追踪

对应：

```text
K00：知识摄取与 Phase Controller 候选任务化
```

```yaml
knowledge_trace_record:
  trace_id: string
  source_id: string
  source_type:
    - USER_INPUT
    - UPLOADED_FILE
    - GPT_LINK
    - METHOD_NOTE
    - PRIOR_SYSTEM_DOC
    - RUNTIME_REPORT
  source_title: string
  source_location: string | null
  received_at: datetime

  extraction:
    extracted_topics: list
    extracted_constraints: list
    extracted_phase_candidates: list
    extracted_data_requirements: list
    extracted_acceptance_requirements: list
    extracted_handoff_requirements: list

  taskization:
    phase_controller_candidates: list
    priority: HIGH|MEDIUM|LOW
    requires_methodology_compile: boolean

  downstream:
    methodology_trace_ids: list
    build_trace_ids: list
```

作用：

```text
保证 HER 不是把知识当普通文档读，而是把知识转成可建造任务。
```

---

# 13. Methodology Trace：方法论蓝图追踪

对应：

```text
system_methodology_blueprint.md
```

```yaml
methodology_trace_record:
  trace_id: string
  blueprint_id: string
  blueprint_file_path: string
  created_at: datetime
  source_knowledge_trace_ids: list

  methodology_sections:
    - section_id: string
      section_name: string
      purpose: string
      source_trace_ids: list
      derived_phase_candidates: list

  assumptions:
    explicit_assumptions: list
    unresolved_questions: list
    risk_notes: list

  downstream:
    build_trace_ids: list
    phase_controller_candidates: list
```

作用：

```text
保证系统方法论不是凭空生成，而是能追踪到知识来源和推导过程。
```

---

# 14. Build Trace：P00 系统建造追踪

对应：

```text
P00：系统建造与方法论编译控制器
```

```yaml
build_trace_record:
  trace_id: string
  build_controller_id: string
  methodology_trace_id: string
  build_task_id: string
  created_at: datetime

  compile_result:
    target_plane: string
    target_files: list
    target_contracts: list
    target_acceptance_gates: list
    target_handoff_packets: list

  task_tree:
    task_tree_id: string
    parent_task_id: string | null
    child_task_ids: list

  output_artifacts:
    artifact_trace_ids: list

  validation:
    build_scope_complete: boolean
    missing_build_parts: list
    ready_for_bootstrap_or_plane_build: boolean
```

作用：

```text
保证 P00 把方法论编译成系统文件、合约、验收门、交接包，而不是只写说明。
```

---

# 15. Phase Trace：阶段追踪

覆盖：

```text
Bootstrap / Governance / Domain / Data / Full Control / Trace / Acceptance / Handoff / P01-P10
```

```yaml
phase_trace_record:
  trace_id: string
  phase_id: string
  phase_name: string
  phase_type:
    - INFRASTRUCTURE_PLANE
    - BUSINESS_PHASE_CONTROLLER
    - RUNTIME_STAGE
    - REVIEW_STAGE

  started_at: datetime
  finished_at: datetime | null

  upstream:
    required_input_contract_ids: list
    required_handoff_packet_ids: list
    parent_trace_ids: list

  execution:
    controller_id: string
    task_tree_id: string
    created_artifacts: list
    updated_artifacts: list
    tool_invocations: list

  output:
    output_contract_ids: list
    handoff_packet_ids: list
    status_code: string

  acceptance:
    acceptance_trace_id: string | null
    acceptance_status:
      - READY
      - READY_WITH_GAPS
      - REJECTED
      - NOT_RUN

  downstream:
    allowed_next_phases: list
    blocked_next_phases: list
```

---

# 16. Task Tree Trace：任务树追踪

```yaml
task_tree_trace_record:
  trace_id: string
  task_tree_id: string
  root_goal: string
  target_phase: string
  created_by: FULL_CONTROL_PLANE
  created_at: datetime

  tasks:
    - task_id: string
      task_name: string
      task_type:
        - FILE_CREATE
        - FILE_UPDATE
        - CONTRACT_DEFINE
        - SCHEMA_DEFINE
        - ACCEPTANCE_DEFINE
        - HANDOFF_DEFINE
        - TOOL_BIND
        - RUNTIME_TEST
      parent_task_id: string | null
      status:
        - PENDING
        - RUNNING
        - DONE
        - FAILED
        - BLOCKED
      artifact_trace_ids: list
      error_trace_ids: list

  completion:
    completed_task_count: integer
    failed_task_count: integer
    blocked_task_count: integer
    completion_status: COMPLETE|PARTIAL|FAILED
```

---

# 17. Artifact Trace：文件产物追踪

```yaml
artifact_trace_record:
  trace_id: string
  artifact_id: string
  artifact_type:
    - MARKDOWN_DOC
    - YAML_SCHEMA
    - JSON_SCHEMA
    - CONTRACT
    - REGISTRY
    - CHECKLIST
    - REPORT
    - PYTHON_SCRIPT
    - TEST_FILE

  file_path: string
  created_at: datetime
  updated_at: datetime | null
  produced_by_phase: string
  produced_by_task_id: string

  content_role:
    - CONTEXT
    - POLICY
    - MODEL
    - CONTRACT
    - ACCEPTANCE
    - HANDOFF
    - TRACE
    - RUNTIME

  validation:
    file_exists: boolean
    required_sections_present: boolean
    missing_sections: list
    checksum: string

  downstream_usage:
    consumed_by_phases: list
    consumed_by_contracts: list
    consumed_by_tools: list
```

---

# 18. Field Lineage：字段血缘追踪

这个部分承接 Data Plane。

```yaml
field_lineage_record:
  trace_id: string
  field_key: string
  field_name_cn: string
  domain_object: string

  source:
    source_id: string
    raw_record_id: string | null
    raw_file_path: string | null
    normalized_record_id: string | null
    normalized_file_path: string | null
    collected_at: datetime | null

  transformation:
    transformation_steps: list
    normalizer_version: string | null

  quality:
    completeness_status: COMPLETE|PARTIAL|MISSING
    freshness_status: FRESH|STALE|EXPIRED|UNKNOWN
    conflict_status: NO_CONFLICT|CONFLICTED|UNKNOWN
    quality_score: number

  downstream_usage:
    evidence_controller_allowed: boolean
    scenario_controller_allowed: boolean
    strategy_gate_allowed: boolean
    usage_limitations: list
```

---

# 19. Contract Trace：合约追踪

```yaml
contract_trace_record:
  trace_id: string
  contract_id: string
  contract_type:
    - INPUT_CONTRACT
    - OUTPUT_CONTRACT
    - HANDOFF_PACKET
    - TOOL_BINDING_CONTRACT
    - ACCEPTANCE_CONTRACT

  produced_by_phase: string
  consumed_by_phase: string
  contract_file_path: string
  produced_at: datetime
  consumed_at: datetime | null

  validation:
    required_fields_present: boolean
    missing_fields: list
    invalid_fields: list
    contract_status:
      - CONTRACT_READY
      - CONTRACT_READY_WITH_GAPS
      - CONTRACT_REJECTED

  trace_links:
    producer_phase_trace_id: string
    consumer_phase_trace_id: string | null
    acceptance_trace_id: string | null
```

---

# 20. State Trace：状态迁移追踪

```yaml
state_trace_record:
  trace_id: string
  state_machine_name: string
  object_id: string
  object_type:
    - PHASE
    - TOKEN
    - TASK
    - CONTRACT
    - RUNTIME_POSITION
    - REVIEW_CASE

  transition:
    from_state: string
    to_state: string
    transition_time: datetime
    triggered_by_phase: string
    triggered_by_rule: string | null

  reason:
    reason_summary_cn: string
    supporting_trace_ids: list
    blocking_trace_ids: list
    uncertainty_tags: list

  validation:
    transition_allowed: boolean
    governance_checked: boolean
    acceptance_required: boolean
    handoff_required: boolean
```

---

# 21. Acceptance Trace：验收追踪

Trace Plane 不负责验收，但必须记录验收过程。

```yaml
acceptance_trace_record:
  trace_id: string
  acceptance_id: string
  target_phase: string
  target_artifact_ids: list
  acceptance_gate_id: string
  executed_at: datetime

  checks:
    - check_id: string
      check_name: string
      result: PASS|WARN|FAIL
      reason: string
      related_trace_ids: list

  result:
    acceptance_status:
      - READY
      - READY_WITH_GAPS
      - REJECTED
    blocking_failures: list
    non_blocking_gaps: list

  downstream_permission:
    allow_handoff: boolean
    allow_runner_binding: boolean
    allow_paper_runtime: boolean
```

---

# 22. Handoff Trace：交接追踪

```yaml
handoff_trace_record:
  trace_id: string
  handoff_packet_id: string
  from_phase: string
  to_phase: string
  created_at: datetime

  packet:
    packet_file_path: string
    packet_schema_version: string
    checksum: string

  transmitted_content:
    output_contract_ids: list
    artifact_trace_ids: list
    field_trace_ids: list
    state_trace_ids: list
    gap_ids: list
    limitation_tags: list

  downstream_rules:
    allowed_use: list
    forbidden_use: list
    weak_use_only: list

  consumption:
    consumed: boolean
    consumed_at: datetime | null
    consumer_phase_trace_id: string | null
```

---

# 23. Tool Binding Trace：工具绑定追踪

对应：

```text
Runner / Tool Binding
```

```yaml
tool_binding_trace_record:
  trace_id: string
  tool_id: string
  tool_name: string
  tool_type:
    - PYTHON_SCRIPT
    - HER_COMMAND
    - API_SKILL
    - VALIDATOR
    - REPORT_GENERATOR
    - PAPER_RUNNER

  binding_phase: string
  bound_at: datetime

  input_contracts:
    required_inputs: list
    input_paths: list
    input_trace_ids: list

  outputs:
    expected_outputs: list
    output_paths: list
    output_trace_ids: list

  permissions:
    allowed_actions: list
    forbidden_actions: list
    paper_only: boolean
    live_execution_allowed: false

  validation:
    tool_exists: boolean
    dry_run_passed: boolean
    test_passed: boolean
    binding_status:
      - TOOL_BOUND
      - TOOL_BOUND_WITH_GAPS
      - TOOL_REJECTED
```

---

# 24. Runtime Trace：纸面运行追踪

对应：

```text
Paper-only Runtime
```

```yaml
runtime_trace_record:
  trace_id: string
  runtime_id: string
  runtime_type: PAPER_ONLY
  token_address: string
  started_at: datetime
  finished_at: datetime | null

  inputs:
    phase_controller_trace_ids: list
    strategy_gate_trace_id: string
    execution_risk_trace_id: string
    tool_binding_trace_ids: list

  runtime_events:
    - event_id: string
      event_type:
        - PAPER_ENTRY
        - PAPER_EXIT
        - PAPER_BLOCK
        - RISK_EVENT
        - PRICE_UPDATE
        - POSITION_UPDATE
      event_time: datetime
      related_trace_ids: list

  result:
    paper_position_id: string | null
    pnl_pct: number | null
    exit_reason: string | null
    runtime_status:
      - PAPER_OPEN
      - PAPER_CLOSED
      - PAPER_BLOCKED
      - PAPER_ERROR

  review:
    review_trace_id: string | null
```

---

# 25. Review Trace：复盘归因追踪

```yaml
review_trace_record:
  trace_id: string
  review_case_id: string
  token_address: string
  reviewed_at: datetime

  reviewed_chain:
    knowledge_trace_ids: list
    methodology_trace_ids: list
    phase_trace_ids: list
    field_trace_ids: list
    contract_trace_ids: list
    state_trace_ids: list
    runtime_trace_ids: list

  attribution:
    failure_or_success:
      - SUCCESS
      - FAILURE
      - MIXED
      - UNKNOWN
    primary_attribution_plane:
      - DATA_PLANE
      - TRACE_PLANE
      - ACCEPTANCE_PLANE
      - HANDOFF_PLANE
      - PHASE_CONTROLLER
      - TOOL_BINDING
      - RUNTIME
      - STRATEGY_LOGIC
      - MARKET_NOISE
    attribution_reason_cn: string

  upgrade_recommendation:
    upgrade_required: boolean
    upgrade_trace_id: string | null
```

---

# 26. Upgrade Trace：升级追踪

```yaml
upgrade_trace_record:
  trace_id: string
  upgrade_id: string
  proposed_at: datetime
  proposed_by: REVIEW_UPGRADE

  upgrade_type:
    - FIELD_ADDITION
    - CONTRACT_UPDATE
    - ACCEPTANCE_GATE_UPDATE
    - TRACE_MODEL_UPDATE
    - STRATEGY_RULE_UPDATE
    - TOOL_BINDING_UPDATE
    - GOVERNANCE_RULE_UPDATE

  source:
    review_trace_ids: list
    failure_case_ids: list
    supporting_data: list

  governance:
    requires_governance_approval: true
    approval_status:
      - PENDING
      - APPROVED
      - REJECTED

  implementation:
    target_files: list
    target_phase: string
    rollback_plan: string
```

---

# 27. Error Trace：错误追踪

```yaml
error_trace_record:
  trace_id: string
  error_id: string
  detected_at: datetime
  detected_by_phase: string

  error_type:
    - MISSING_TRACE
    - BROKEN_LINEAGE
    - MISSING_CONTRACT
    - CONTRACT_MISMATCH
    - ACCEPTANCE_WITHOUT_TRACE
    - HANDOFF_WITHOUT_ACCEPTANCE
    - TOOL_WITHOUT_BINDING
    - RUNTIME_WITHOUT_GATE
    - STATE_TRANSITION_UNEXPLAINED
    - RAW_DATA_OVERWRITTEN
    - LIVE_EXECUTION_VIOLATION
    - REVIEW_WITHOUT_RUNTIME_TRACE

  severity:
    - BLOCKING
    - HIGH
    - MEDIUM
    - LOW

  affected_objects:
    phase_ids: list
    artifact_ids: list
    contract_ids: list
    state_ids: list
    tool_ids: list

  required_action:
    - BLOCK_DOWNSTREAM
    - REQUIRE_TRACE_REPAIR
    - REQUIRE_ACCEPTANCE_RERUN
    - REQUIRE_HANDOFF_REBUILD
    - REGISTER_GAP_ONLY

  status:
    - OPEN
    - IN_PROGRESS
    - FIXED
    - ACCEPTED_RISK
```

---

# 28. Trace Quality Model：追踪质量模型

```yaml
trace_quality_score_model:
  completeness_weight: 0.20
  continuity_weight: 0.20
  contract_trace_weight: 0.15
  state_trace_weight: 0.15
  acceptance_trace_weight: 0.10
  handoff_trace_weight: 0.10
  runtime_replayability_weight: 0.10

trace_quality_status:
  - TRACE_HIGH_CONFIDENCE
  - TRACE_USABLE
  - TRACE_USABLE_WITH_GAPS
  - TRACE_LOW_CONFIDENCE
  - TRACE_UNUSABLE

downstream_permission:
  TRACE_HIGH_CONFIDENCE:
    acceptance: FULL_ACCEPTANCE_ALLOWED
    handoff: FULL_HANDOFF_ALLOWED
    runtime: PAPER_RUNTIME_ALLOWED

  TRACE_USABLE:
    acceptance: ACCEPTANCE_ALLOWED
    handoff: HANDOFF_ALLOWED
    runtime: PAPER_RUNTIME_ALLOWED_WITH_MONITORING

  TRACE_USABLE_WITH_GAPS:
    acceptance: ACCEPTANCE_WITH_GAPS_ONLY
    handoff: HANDOFF_WITH_LIMITATIONS
    runtime: PAPER_RUNTIME_RESTRICTED

  TRACE_LOW_CONFIDENCE:
    acceptance: MANUAL_REVIEW_REQUIRED
    handoff: BLOCK_OR_WEAK_HANDOFF
    runtime: PAPER_RUNTIME_BLOCKED

  TRACE_UNUSABLE:
    acceptance: BLOCK_ACCEPTANCE
    handoff: BLOCK_HANDOFF
    runtime: BLOCK_RUNTIME
```

---

# 29. Trace Storage Constitution

建议数据目录：

```text
/root/sikk-gmgn/data/trace_plane/
  knowledge_trace/
  methodology_trace/
  build_trace/
  phase_trace/
  task_tree_trace/
  artifact_trace/
  field_lineage/
  contract_trace/
  state_trace/
  acceptance_trace/
  handoff_trace/
  tool_binding_trace/
  runtime_trace/
  review_trace/
  upgrade_trace/
  error_trace/
  quality/
  handoff/
  reports/
```

原则：

```text
1. Trace 数据不替代业务数据。
2. Trace 数据不修改 raw。
3. Trace 数据记录引用关系。
4. Trace 数据必须可增量写入。
5. Trace 数据必须支持按 token、phase、run_id、trace_id 回查。
6. Trace 数据必须支持 Review / Replay 复盘。
7. Trace 数据必须向 Acceptance Plane 和 Handoff Plane 提供输入。
```

---

# 30. trace_handoff_contract.yaml

Trace Plane 输出给 Acceptance / Handoff / P01-P10 的标准交接包。

```yaml
trace_handoff_packet:
  packet_id: string
  generated_at: datetime
  trace_plane_version: v2.0
  run_id: string

  build_order_context:
    current_build_stage: TRACE_PLANE
    previous_stage: FULL_CONTROL_PLANE
    next_stage:
      - ACCEPTANCE_PLANE
      - HANDOFF_PLANE

  trace_summary:
    trace_quality_status: string
    trace_quality_score: number
    trace_chain_complete: boolean
    blocking_trace_errors: list
    non_blocking_trace_gaps: list

  trace_indexes:
    knowledge_trace_index_path: string
    methodology_trace_index_path: string
    build_trace_index_path: string
    phase_trace_index_path: string
    artifact_trace_index_path: string
    contract_trace_index_path: string
    state_trace_index_path: string
    acceptance_trace_index_path: string
    handoff_trace_index_path: string
    tool_trace_index_path: string
    runtime_trace_index_path: string
    review_trace_index_path: string

  acceptance_input:
    acceptance_allowed: boolean
    acceptance_limitations: list
    acceptance_required_checks: list

  handoff_input:
    handoff_allowed: boolean
    handoff_limitations: list
    required_handoff_trace_fields: list

  downstream_permission:
    phase_controller_definition_allowed: boolean
    runner_binding_allowed: boolean
    paper_runtime_allowed: boolean
    live_runtime_allowed: false

  forbidden_actions:
    - ACCEPTANCE_WITHOUT_TRACE
    - HANDOFF_WITHOUT_TRACE
    - RUNNER_BINDING_WITHOUT_PHASE_TRACE
    - PAPER_RUNTIME_WITHOUT_TOOL_TRACE
    - LIVE_EXECUTION
```

---

# 31. Trace Plane 验收标准

## 31.1 TRACE_READY

必须满足：

```text
1. trace_plane.yaml 已完成
2. trace_context.md 已完成
3. trace_id_policy.yaml 已完成
4. trace_object_registry.yaml 已完成
5. knowledge_trace_model.yaml 已完成
6. methodology_trace_model.yaml 已完成
7. build_trace_model.yaml 已完成
8. phase_trace_model.yaml 已完成
9. task_tree_trace_model.yaml 已完成
10. artifact_trace_model.yaml 已完成
11. field_lineage_model.yaml 已完成
12. contract_trace_model.yaml 已完成
13. state_trace_model.yaml 已完成
14. acceptance_trace_model.yaml 已完成
15. handoff_trace_model.yaml 已完成
16. tool_binding_trace_model.yaml 已完成
17. runtime_trace_model.yaml 已完成
18. review_trace_model.yaml 已完成
19. upgrade_trace_model.yaml 已完成
20. error_trace_model.yaml 已完成
21. trace_quality_model.yaml 已完成
22. trace_storage_constitution.md 已完成
23. trace_handoff_contract.yaml 已完成
24. her_trace_execution_protocol.md 已完成
25. 已定义 Acceptance Plane 如何读取 trace
26. 已定义 Handoff Plane 如何读取 trace
27. 已定义 P01-P10 如何继承 trace
28. 已定义 Runner / Tool Binding 如何写入 trace
29. 已定义 Paper-only Runtime 如何写入 trace
30. 不存在无 trace 的核心阶段产物
```

---

## 31.2 TRACE_READY_WITH_GAPS

允许进入 Acceptance Plane，但必须限制：

```text
1. 部分历史文件没有 trace，但新建文件 trace 完整
2. legacy runtime 还没有完整映射
3. 部分 Runner 工具尚未绑定 trace
4. Paper Runtime trace 尚未真实跑通
5. Review / Upgrade trace 只有模型，暂无样本
6. trace validator 尚未代码化
```

限制：

```text
可以进入 Acceptance Plane
可以进入 Handoff Plane 草案
不允许进入自动 Paper Runtime
不允许标记系统全链路完成
不允许启用任何实盘相关路径
```

---

## 31.3 TRACE_REJECTED

以下情况必须驳回：

```text
1. Trace Plane 只是日志说明
2. 没有 trace_id 体系
3. 没有任务树 trace
4. 没有文件产物 trace
5. 没有合约 trace
6. 没有状态迁移 trace
7. 没有验收 trace
8. 没有交接 trace
9. Runner 可以绕过 trace 绑定
10. Paper Runtime 可以无 trace 运行
11. Review 无法追溯到 runtime / phase / contract
12. Acceptance Plane 可以不读取 trace 就验收
13. Handoff Plane 可以不读取 trace 就交接
```

---

# 32. HER 执行协议

文件：

```text
her_trace_execution_protocol.md
```

HER 执行任何系统建造任务时，必须按这个顺序写 trace：

```text
1. 读取当前任务目标
2. 生成或读取 task_tree_id
3. 为当前任务创建 TASK_TRACE
4. 每创建一个文件，创建 ARTIFACT_TRACE
5. 每生成一个合约，创建 CONTRACT_TRACE
6. 每改变一个阶段状态，创建 STATE_TRACE
7. 每执行验收，创建 ACCEPTANCE_TRACE
8. 每生成交接包，创建 HANDOFF_TRACE
9. 每绑定工具，创建 TOOL_TRACE
10. 每运行纸面任务，创建 RUNTIME_TRACE
11. 每次复盘，创建 REVIEW_TRACE
12. 每次升级建议，创建 UPGRADE_TRACE
13. 如果出现缺失、冲突、断链、越权，创建 ERROR_TRACE
```

禁止：

```text
1. 不允许无 trace 创建核心文件
2. 不允许无 trace 进入验收
3. 不允许无 acceptance_trace 交接
4. 不允许无 handoff_trace 进入下游
5. 不允许无 tool_trace 绑定 Runner
6. 不允许无 runtime_trace 执行纸面运行
7. 不允许无 review_trace 做升级
```

---

# 33. 给 HER 的可执行任务书

```text
任务名称：建立 Trace Plane｜追踪平面专业版 v2.0

目标：
在 /root/sikk-gmgn/system/trace_plane/ 下建立 SIKK Stable Trader OS 的 Trace Plane。该 Trace Plane 必须符合新的专业版建造顺序，不再只是 Data Plane 到 Evidence Plane 的中间层，而是全系统建造、控制、任务、文件、字段、合约、状态、验收、交接、工具、纸面运行、复盘升级的全链路追踪平面。

专业版建造顺序固定为：
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
1. Trace Plane 不做调度，调度属于 Full Control Plane。
2. Trace Plane 不做验收裁决，裁决属于 Acceptance Plane。
3. Trace Plane 不做交接执行，交接属于 Handoff Plane。
4. Trace Plane 不做交易判断，不输出策略信号，不执行交易。
5. Trace Plane 负责记录所有核心对象的 trace_id、来源、父子关系、输入、输出、状态、合约、验收、交接、工具调用、运行结果、复盘归因。
6. Acceptance Plane 不允许绕过 Trace Plane。
7. Handoff Plane 不允许绕过 Trace Plane。
8. Runner / Tool Binding 不允许无 trace 绑定。
9. Paper-only Runtime 不允许无 trace 运行。
10. Review / Upgrade 不允许无 trace 升级规则。

需要创建目录：
/root/sikk-gmgn/system/trace_plane/

需要创建文件：
1. trace_plane.yaml
2. trace_context.md
3. trace_id_policy.yaml
4. trace_object_registry.yaml
5. knowledge_trace_model.yaml
6. methodology_trace_model.yaml
7. build_trace_model.yaml
8. phase_trace_model.yaml
9. task_tree_trace_model.yaml
10. artifact_trace_model.yaml
11. field_lineage_model.yaml
12. contract_trace_model.yaml
13. state_trace_model.yaml
14. acceptance_trace_model.yaml
15. handoff_trace_model.yaml
16. tool_binding_trace_model.yaml
17. runtime_trace_model.yaml
18. review_trace_model.yaml
19. upgrade_trace_model.yaml
20. error_trace_model.yaml
21. trace_quality_model.yaml
22. trace_storage_constitution.md
23. trace_handoff_contract.yaml
24. trace_acceptance_criteria.md
25. trace_gap_register.md
26. trace_review_checklist.md
27. her_trace_execution_protocol.md

文件要求：
- trace_plane.yaml：定义 Trace Plane 的身份、权限、边界、状态码、上下游关系。
- trace_context.md：写成 HER 执行前必须读取的追踪上下文。
- trace_id_policy.yaml：定义全系统 trace_id 规则。
- trace_object_registry.yaml：注册所有需要追踪的对象类型。
- knowledge_trace_model.yaml：追踪 K00 知识摄取与任务化。
- methodology_trace_model.yaml：追踪 system_methodology_blueprint.md 的形成过程。
- build_trace_model.yaml：追踪 P00 如何把方法论编译成系统建造任务。
- phase_trace_model.yaml：追踪所有 Plane 和 P01-P10 Phase Controller。
- task_tree_trace_model.yaml：追踪 Full Control Plane 生成的任务树。
- artifact_trace_model.yaml：追踪所有文件、Schema、合约、报告、脚本。
- field_lineage_model.yaml：追踪 Data Plane 字段血缘。
- contract_trace_model.yaml：追踪输入合约、输出合约、handoff packet。
- state_trace_model.yaml：追踪状态迁移原因。
- acceptance_trace_model.yaml：追踪 Acceptance Plane 的验收过程。
- handoff_trace_model.yaml：追踪 Handoff Plane 的交接过程。
- tool_binding_trace_model.yaml：追踪 Runner / Tool Binding。
- runtime_trace_model.yaml：追踪 Paper-only Runtime。
- review_trace_model.yaml：追踪复盘与失败归因。
- upgrade_trace_model.yaml：追踪升级建议与治理审批。
- error_trace_model.yaml：追踪缺失、冲突、断链、越权、无 trace 运行。
- trace_quality_model.yaml：定义追踪质量评分和下游权限。
- trace_storage_constitution.md：定义追踪数据目录宪法。
- trace_handoff_contract.yaml：定义 Trace Plane 输出给 Acceptance / Handoff / P01-P10 的 trace_handoff_packet。
- trace_acceptance_criteria.md：定义 TRACE_READY / TRACE_READY_WITH_GAPS / TRACE_REJECTED。
- trace_gap_register.md：登记当前无法完全解决的 trace 缺口。
- trace_review_checklist.md：建立追踪平面审计清单。
- her_trace_execution_protocol.md：定义 HER 每次执行如何写入 trace。

同时更新 Full Control Plane：
1. 在 global_plane_registry.yaml 中加入 TRACE_PLANE。
2. 在 phase_execution_order.yaml 中确认 Trace Plane 位于 Full Control Plane 之后、Acceptance Plane 之前。
3. 在 contract_router.yaml 中加入 FULL_CONTROL_TO_TRACE、TRACE_TO_ACCEPTANCE、TRACE_TO_HANDOFF。
4. 在 acceptance_gate_registry.yaml 中加入 GATE_TRACE_READY。
5. 在 global_status_code_table.yaml 中加入 TRACE_READY、TRACE_READY_WITH_GAPS、TRACE_REJECTED、TRACE_BROKEN。
6. 在 handoff_packet_registry.yaml 中加入 trace_handoff_packet。

验收输出：
1. 文件创建清单
2. 每个文件的核心摘要
3. TRACE_READY / TRACE_READY_WITH_GAPS / TRACE_REJECTED 判断
4. Trace ID 体系摘要
5. 全系统追踪对象摘要
6. Acceptance Plane 如何读取 trace
7. Handoff Plane 如何读取 trace
8. P01-P10 如何继承 trace
9. Runner / Tool Binding 如何写入 trace
10. Paper-only Runtime 如何写入 trace
11. 当前缺口清单
12. 是否达到轻量机构级 Trace Plane v2.0

最终验收标准：
只有当知识摄取、方法论蓝图、P00 建造编译、Plane、Phase Controller、任务树、文件产物、字段血缘、合约、状态、验收、交接、工具绑定、纸面运行、复盘升级、错误追踪、质量评分、handoff contract、HER trace protocol 全部具备追踪模型时，才允许标记为 TRACE_READY。
```

---

# 34. 当前是否达到轻量机构级专业标准？

## 判断

按这版设计，Trace Plane 达到：

```text
轻量机构级 v2.0 设计标准
```

但注意：

```text
设计标准已达到
工程落地尚未完成
```

---

## 已经达到的能力

|能力|状态|
|---|---|
|全系统 trace_id 体系|已设计|
|K00 知识摄取追踪|已设计|
|方法论蓝图追踪|已设计|
|P00 建造编译追踪|已设计|
|Plane / Phase 追踪|已设计|
|任务树追踪|已设计|
|文件产物追踪|已设计|
|字段血缘追踪|已设计|
|合约追踪|已设计|
|状态迁移追踪|已设计|
|验收追踪|已设计|
|交接追踪|已设计|
|工具绑定追踪|已设计|
|纸面运行追踪|已设计|
|复盘归因追踪|已设计|
|升级建议追踪|已设计|
|错误追踪|已设计|
|Trace 质量评分|已设计|
|HER 执行协议|已设计|

---

## 还没达到的部分

|缺口|原因|后续处理|
|---|---|---|
|trace_id 生成器未代码化|当前是模型|后续实现 `trace_id_generator.py`|
|trace validator 未代码化|当前是验收规则|后续实现 `trace_validator.py`|
|HER 自动写 trace 未接入|需要 HER 执行协议落地|后续接入每次任务执行|
|legacy 数据无完整 trace|旧数据天然缺 trace|建立 legacy_trace_mapping|
|Runner 工具尚未绑定 trace|需要工具绑定阶段|Runner / Tool Binding 处理|
|Paper Runtime 尚未写入 trace|需要 runtime 接入|Paper-only Runtime 处理|
|Review / Upgrade 无真实样本|需要运行后积累|Review 阶段处理|
|Acceptance Plane 尚未展开|下一层|下一步设计|
|Handoff Plane 尚未展开|Acceptance 后|后续设计|

---

# 35. 下一步应该做什么

按照你的专业版顺序，Trace Plane 后面不应该直接进入业务阶段。

下一步应该是：

```text
Acceptance Plane：验收平面
```

因为 Trace Plane 只负责追踪，不负责裁决是否通过。

正确推进链路是：

```text
Trace Plane 完成
  ↓
TRACE_READY / TRACE_READY_WITH_GAPS
  ↓
Acceptance Plane 读取 trace_handoff_packet
  ↓
判断每个阶段、文件、合约、状态、交接是否真正合格
  ↓
再进入 Handoff Plane
```

---

# 本次认知升级点

1. **新版 Trace Plane 是全系统追踪层，不再只是 Data → Evidence 中间层。**
    
2. **Trace Plane 的核心不是日志，而是 trace_id + 引用关系 + 状态链 + 验收链 + 交接链。**
    
3. **HER 执行系统任务时，必须把每个任务、文件、合约、状态变化都写入 trace。**
    
4. **Acceptance Plane 必须读取 Trace Plane，不能直接看文件是否存在就验收。**
    
5. **Handoff Plane 必须读取 Trace Plane，不能无 trace 交接下游。**
    
6. **Runner / Tool Binding 必须后置，并且每个工具绑定都要有 tool_trace。**
    
7. **Paper-only Runtime 必须写 runtime_trace，防止纸面交易结果无法归因。**
    
8. **Review / Upgrade 必须通过 review_trace 和 upgrade_trace，不能直接污染实时系统。**
    

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|Acceptance Plane 尚未完整设计|Trace 后的下一步|下一阶段展开|
|Handoff Plane 尚未完整设计|Acceptance 后处理|后续展开|
|trace_id 自动生成器未实现|模型已定义|工程阶段实现|
|trace validator 未实现|验收逻辑已定义|工程阶段实现|
|HER 如何自动写 trace 仍需落地|协议已定义|HER 执行包实现|
|legacy runtime 如何补 trace|尚未扫描|建立 legacy_trace_mapping|
|工具绑定 trace 尚无真实案例|等 Runner 阶段|后续接入|
|Paper Runtime trace 尚未跑通|等纸面运行阶段|后续验证|
|Review / Upgrade trace 尚无样本|需要运行数据|后续积累|
|Full Control Plane 需要同步更新 Trace 路由|已定义需要|后续 HER 执行修正|