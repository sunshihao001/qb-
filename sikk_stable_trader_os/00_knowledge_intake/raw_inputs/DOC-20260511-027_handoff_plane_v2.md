# Handoff Plane：交接平面专业版设计 v2.0

## 0. 核心定位

**Handoff Plane 不是“把文件发给下一阶段”。**

它是 SIKK Stable Trader OS 的**阶段交接控制平面**，负责把已经通过 Acceptance Plane 验收的阶段产物，转换成下游可读取、可限制使用、可追踪、可复盘、可回退的标准交接包。

一句话定义：

> **Trace Plane 证明系统链路可追踪。**  
> **Acceptance Plane 裁决阶段是否合格。**  
> **Handoff Plane 决定合格产物如何交给下游、下游能怎么用、哪些不能用、哪些只能弱使用、哪些缺口必须继续传递。**

---

# 1. Handoff Plane 在专业版建造顺序中的位置

当前专业版建造顺序应固定为：

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

Handoff Plane 位于：

```text
Acceptance Plane 之后
P01-P10 Phase Controller 之前
```

它的核心价值是防止下游阶段靠上下文猜测上游结果。

---

# 2. Handoff Plane 的专业定义

```text
Handoff Plane 是 SIKK Stable Trader OS 的交接平面。

它负责读取 Acceptance Plane 输出的 acceptance_result_packet、Trace Plane 输出的 trace_handoff_packet、Full Control Plane 的任务树和合约路由、上游阶段产物、缺口登记、限制标签、禁止事项和下游权限，生成标准化 handoff_packet、downstream_read_instruction、gap_propagation_packet、limitation_transfer_packet 和 forbidden_use_policy。

它不负责调度，不负责验收，不负责追踪，不负责生成业务内容，不负责运行工具，不负责交易判断。

它只负责把“已验收的阶段结果”安全、完整、有边界地传递给下游。
```

---

# 3. Handoff Plane 解决的核心问题

|问题|没有 Handoff Plane 的后果|Handoff Plane 的处理|
|---|---|---|
|上游文件很多，下游不知道读哪个|下游靠猜，容易读错|生成 downstream_read_instruction|
|上游有缺口，下游不知道|缺口被隐藏，判断污染|生成 gap_propagation_packet|
|上游是 WITH_GAPS，下游当成 READY|风险放大|传递 limitation_tags|
|字段只能弱使用，下游强使用|错误证据、错误场景|定义 field_usage_permission|
|某阶段越权输出，下游继续吃|越权污染系统|传递 forbidden_use_policy|
|合约不完整仍交接|下游断链|handoff precheck 阻断|
|Trace 断链仍交接|无法复盘|要求 trace_handoff_packet|
|Acceptance 未通过仍交接|阶段跳步|必须读取 acceptance_result_packet|
|工具绑定提前|脚本污染系统|工具交接权限限制|
|纸面运行无交接包|结果不可归因|runtime handoff 标准化|

---

# 4. Handoff Plane 与其他 Plane 的边界

## 4.1 与 Acceptance Plane 的区别

|层|职责|
|---|---|
|Acceptance Plane|判断是否通过、带缺口通过、返工、驳回、阻断|
|Handoff Plane|根据验收结果决定如何交接、交接给谁、怎么限制使用|

关系：

```text
Acceptance Plane 输出：
  acceptance_result_packet

Handoff Plane 读取：
  acceptance_result_packet

Handoff Plane 输出：
  handoff_packet
  downstream_read_instruction
  limitation_transfer_packet
  gap_propagation_packet
```

Handoff Plane **不能推翻 Acceptance Plane 的裁决**。

---

## 4.2 与 Trace Plane 的区别

|层|职责|
|---|---|
|Trace Plane|记录来源、链路、状态、合约、产物、运行过程|
|Handoff Plane|传递 trace 引用和使用权限|

Trace Plane 负责：

```text
这个对象从哪里来？
经过了什么？
能不能追踪？
```

Handoff Plane 负责：

```text
这个对象能不能交给下游？
下游可以怎么使用？
哪些 trace 必须继续传递？
```

---

## 4.3 与 Full Control Plane 的区别

|层|职责|
|---|---|
|Full Control Plane|调度阶段、生成任务树、控制流程|
|Handoff Plane|执行阶段之间的标准化交接|

Full Control Plane 决定：

```text
下一阶段是什么
```

Handoff Plane 决定：

```text
下一阶段应该读取什么
哪些可以用
哪些不能用
哪些必须保留限制
```

---

# 5. Handoff Plane 的底层逻辑

## 5.1 交接不是复制，而是权限转移

专业系统里，交接包不只是文件路径，而是：

```text
内容 + 权限 + 限制 + 缺口 + trace + 状态 + 下游动作边界
```

也就是说，Handoff Plane 输出的是一种**受控上下文**。

---

## 5.2 交接必须携带“不完整性”

很多系统失败不是因为没有数据，而是因为：

```text
上游知道不完整
下游不知道不完整
```

所以 Handoff Plane 必须传递：

```text
missing_fields
non_blocking_gaps
blocking_gaps
weak_use_only_fields
forbidden_claims
manual_review_required
runtime_blocked
```

---

## 5.3 下游只能在授权范围内使用上游结果

例如：

```text
Acceptance 状态 = READY_WITH_GAPS
Trace 状态 = TRACE_USABLE_WITH_GAPS
Data 状态 = DATA_READY_WITH_GAPS
```

则 Handoff Plane 不能交接成：

```text
FULL_HANDOFF
```

只能交接成：

```text
LIMITED_HANDOFF
```

并附带：

```text
WEAK_USE_ONLY
NO_STRONG_EVIDENCE
NO_PAPER_RUNTIME
GAP_PROPAGATION_REQUIRED
```

---

# 6. Handoff Plane 可以做什么

```text
1. 定义交接对象
2. 定义交接包格式
3. 定义下游读取指令
4. 定义字段使用权限
5. 定义缺口传递规则
6. 定义限制标签传递规则
7. 定义禁止使用规则
8. 定义交接模式
9. 定义交接状态码
10. 定义交接前置检查
11. 定义交接失败处理
12. 定义交接审计记录
13. 定义 P01-P10 Controller 接收规则
14. 定义 Runner / Tool Binding 接收规则
15. 定义 Paper-only Runtime 接收规则
16. 定义 Review / Upgrade 回传规则
```

---

# 7. Handoff Plane 不能做什么

```text
1. 不能调度阶段
2. 不能替代 Acceptance Plane 裁决 READY / REJECTED
3. 不能替代 Trace Plane 创建 trace
4. 不能修改上游产物
5. 不能隐藏缺口
6. 不能删除限制标签
7. 不能把 READY_WITH_GAPS 改成 READY
8. 不能把 weak_use_only 改成 strong_use_allowed
9. 不能允许未验收结果进入下游
10. 不能允许自动实盘路径
11. 不能绕过 Governance
12. 不能让下游读取未授权文件
```

---

# 8. Handoff Plane 必须交接的对象

## 8.1 一级交接对象

|交接对象|作用|
|---|---|
|Build Order Handoff|专业建造顺序交接|
|Methodology Handoff|方法论蓝图交接|
|Plane Handoff|各基础 Plane 产物交接|
|Trace Handoff|trace 链路交接|
|Acceptance Handoff|验收结果交接|
|Contract Handoff|输入 / 输出合约交接|
|Artifact Handoff|文件产物交接|
|Gap Handoff|缺口传递|
|Limitation Handoff|使用限制传递|
|Permission Handoff|下游权限传递|
|Phase Controller Handoff|P01-P10 控制器交接|
|Tool Binding Handoff|工具绑定交接|
|Runtime Handoff|纸面运行交接|
|Review Handoff|复盘结果交接|
|Upgrade Handoff|升级建议交接|

---

# 9. Handoff Plane 文件体系

建议目录：

```text
/root/sikk-gmgn/system/handoff_plane/
```

必须创建：

```text
handoff_plane.yaml
handoff_context.md
handoff_object_registry.yaml
handoff_mode_policy.yaml
handoff_status_code_table.yaml
handoff_precheck_model.yaml
handoff_packet_contract.yaml
downstream_read_instruction_model.yaml
gap_propagation_policy.yaml
limitation_transfer_policy.yaml
field_usage_permission_model.yaml
forbidden_use_policy.yaml
contract_handoff_model.yaml
artifact_handoff_model.yaml
phase_controller_handoff_model.yaml
tool_binding_handoff_model.yaml
runtime_handoff_model.yaml
review_upgrade_handoff_model.yaml
handoff_trace_dependency.yaml
handoff_acceptance_dependency.yaml
handoff_failure_policy.yaml
handoff_report_model.yaml
handoff_storage_constitution.md
handoff_gap_register.md
handoff_review_checklist.md
her_handoff_execution_protocol.md
```

---

# 10. 每个文件的作用

|文件|作用|
|---|---|
|`handoff_plane.yaml`|交接平面身份、边界、权限、状态码|
|`handoff_context.md`|HER 执行前读取的交接上下文|
|`handoff_object_registry.yaml`|注册所有可交接对象|
|`handoff_mode_policy.yaml`|定义 FULL / LIMITED / BLOCKED 等交接模式|
|`handoff_status_code_table.yaml`|交接状态码|
|`handoff_precheck_model.yaml`|交接前置检查|
|`handoff_packet_contract.yaml`|标准 handoff_packet 合约|
|`downstream_read_instruction_model.yaml`|下游读取指令|
|`gap_propagation_policy.yaml`|缺口传递规则|
|`limitation_transfer_policy.yaml`|限制标签传递规则|
|`field_usage_permission_model.yaml`|字段使用权限|
|`forbidden_use_policy.yaml`|禁止使用规则|
|`contract_handoff_model.yaml`|合约交接模型|
|`artifact_handoff_model.yaml`|文件产物交接模型|
|`phase_controller_handoff_model.yaml`|P01-P10 控制器交接模型|
|`tool_binding_handoff_model.yaml`|工具绑定交接模型|
|`runtime_handoff_model.yaml`|纸面运行交接模型|
|`review_upgrade_handoff_model.yaml`|复盘升级交接模型|
|`handoff_trace_dependency.yaml`|Handoff 对 Trace 的依赖|
|`handoff_acceptance_dependency.yaml`|Handoff 对 Acceptance 的依赖|
|`handoff_failure_policy.yaml`|交接失败处理|
|`handoff_report_model.yaml`|人类可读交接报告|
|`handoff_storage_constitution.md`|交接数据目录宪法|
|`handoff_gap_register.md`|交接缺口登记|
|`handoff_review_checklist.md`|交接平面审计清单|
|`her_handoff_execution_protocol.md`|HER 如何执行交接|

---

# 11. handoff_plane.yaml

```yaml
plane_id: HANDOFF_PLANE
plane_name: 交接平面
plane_level: light_institutional
version: v2.0
status: DRAFT_READY_FOR_AUDIT

position_in_build_order:
  previous: ACCEPTANCE_PLANE
  next:
    - P01_P10_PHASE_CONTROLLERS
    - RUNNER_TOOL_BINDING
    - PAPER_ONLY_RUNTIME
    - REVIEW_UPGRADE

mission:
  primary: 将通过验收的阶段产物转化为可供下游读取、可限制使用、可追踪、可复盘的标准交接包
  secondary:
    - 读取 acceptance_result_packet
    - 读取 trace_handoff_packet
    - 生成 handoff_packet
    - 生成 downstream_read_instruction
    - 传递缺口、限制、禁止事项和字段使用权限
    - 防止未验收、无 trace、无合约、越权产物进入下游
    - 为 P01-P10、Runner、Paper Runtime、Review / Upgrade 提供标准输入

authority:
  can_define:
    - handoff_objects
    - handoff_modes
    - handoff_status_codes
    - handoff_packets
    - downstream_read_instructions
    - gap_propagation_rules
    - limitation_transfer_rules
    - field_usage_permissions
    - forbidden_use_rules
    - handoff_reports

  can_decide:
    - FULL_HANDOFF
    - LIMITED_HANDOFF
    - HANDOFF_BLOCKED
    - HANDOFF_NEEDS_REWORK

  cannot_do:
    - schedule_phase
    - accept_or_reject_phase
    - create_trace
    - modify_upstream_artifacts
    - remove_gaps
    - remove_limitation_tags
    - override_acceptance_result
    - generate_strategy_signal
    - run_tools
    - run_paper_runtime
    - approve_live_execution

upstream_inputs:
  - acceptance_result_packet
  - trace_handoff_packet
  - full_control_task_tree
  - contract_trace_ids
  - artifact_trace_ids
  - state_trace_ids
  - gap_register
  - governance_rules

downstream_outputs:
  - handoff_packet
  - downstream_read_instruction
  - gap_propagation_packet
  - limitation_transfer_packet
  - field_usage_permission_packet
  - forbidden_use_policy
  - handoff_report

status_codes:
  - HANDOFF_UNINITIALIZED
  - HANDOFF_CONTEXT_READY
  - HANDOFF_PRECHECK_RUNNING
  - HANDOFF_READY
  - HANDOFF_READY_WITH_LIMITATIONS
  - HANDOFF_BLOCKED
  - HANDOFF_NEEDS_REWORK
  - HANDOFF_REJECTED
```

---

# 12. handoff_object_registry.yaml

```yaml
handoff_objects:
  - object_type: methodology_blueprint_handoff
    source_stage: system_methodology_blueprint
    required_acceptance_status:
      - ACCEPTANCE_READY
      - ACCEPTANCE_READY_WITH_GAPS
    target_stage: P00_BUILD_CONTROLLER

  - object_type: plane_package_handoff
    source_stage:
      - BOOTSTRAP_PLANE
      - GOVERNANCE_PLANE
      - DOMAIN_PLANE
      - DATA_PLANE
      - FULL_CONTROL_PLANE
      - TRACE_PLANE
      - ACCEPTANCE_PLANE
    required_acceptance_status:
      - ACCEPTANCE_READY
      - ACCEPTANCE_READY_WITH_GAPS
    target_stage:
      - HANDOFF_PLANE
      - P01_P10_PHASE_CONTROLLERS

  - object_type: phase_controller_handoff
    source_stage: P01_P10_PHASE_CONTROLLERS
    required_acceptance_status:
      - ACCEPTANCE_READY
      - ACCEPTANCE_READY_WITH_GAPS
    target_stage: RUNNER_TOOL_BINDING

  - object_type: tool_binding_handoff
    source_stage: RUNNER_TOOL_BINDING
    required_acceptance_status:
      - TOOL_BINDING_READY
      - TOOL_BINDING_READY_WITH_GAPS
    target_stage: PAPER_ONLY_RUNTIME

  - object_type: runtime_handoff
    source_stage: PAPER_ONLY_RUNTIME
    required_acceptance_status:
      - PAPER_RUNTIME_READY
      - PAPER_RUNTIME_READY_WITH_GAPS
    target_stage: REVIEW_UPGRADE

  - object_type: review_upgrade_handoff
    source_stage: REVIEW_UPGRADE
    required_acceptance_status:
      - REVIEW_READY
      - UPGRADE_READY_FOR_GOVERNANCE
    target_stage:
      - GOVERNANCE_PLANE
      - FULL_CONTROL_PLANE
      - SELF_UPGRADE_CONTROLLER
```

---

# 13. handoff_mode_policy.yaml

## 13.1 交接模式

```yaml
handoff_modes:
  FULL_HANDOFF:
    meaning: 上游已完全通过验收，下游可按完整权限读取和使用
    required_acceptance_status:
      - ACCEPTANCE_READY
    required_trace_status:
      - TRACE_HIGH_CONFIDENCE
      - TRACE_USABLE
    downstream_permission:
      - FULL_READ
      - FULL_USE_WITHIN_PHASE_AUTHORITY
      - PHASE_CONTROLLER_BUILD_ALLOWED

  LIMITED_HANDOFF:
    meaning: 上游带非阻断缺口通过，下游必须带限制使用
    required_acceptance_status:
      - ACCEPTANCE_READY_WITH_GAPS
    downstream_permission:
      - READ_WITH_LIMITATIONS
      - WEAK_USE_ONLY
      - GAP_PROPAGATION_REQUIRED
      - MANUAL_REVIEW_IF_ESCALATING

  OBSERVE_ONLY_HANDOFF:
    meaning: 上游信息可供观察，但不能支撑强判断或运行
    required_conditions:
      - trace_quality_low_or_gaps_high
    downstream_permission:
      - OBSERVE_ONLY
      - NO_STRONG_CLAIM
      - NO_RUNTIME

  HANDOFF_NEEDS_REWORK:
    meaning: 上游未完全合格，但可返工
    downstream_permission:
      - BLOCK_DOWNSTREAM
      - REQUIRE_REWORK_TASKS

  HANDOFF_BLOCKED:
    meaning: 触发硬阻断，不允许交接
    downstream_permission:
      - BLOCK_ALL_DOWNSTREAM
      - FULL_CONTROL_REVIEW_REQUIRED
```

---

# 14. handoff_status_code_table.yaml

```yaml
handoff_status_codes:
  HANDOFF_READY:
    meaning: 完整交接可执行
    downstream_effect:
      - target_stage_can_start
      - downstream_may_consume_full_packet

  HANDOFF_READY_WITH_LIMITATIONS:
    meaning: 可交接，但必须携带缺口和限制
    downstream_effect:
      - target_stage_can_start_with_limits
      - weak_use_only_constraints_apply
      - gap_propagation_required

  HANDOFF_NEEDS_REWORK:
    meaning: 交接前需要返工
    downstream_effect:
      - block_target_stage
      - generate_rework_tasks

  HANDOFF_BLOCKED:
    meaning: 交接被硬阻断
    downstream_effect:
      - block_all_downstream
      - notify_full_control_plane

  HANDOFF_REJECTED:
    meaning: 交接对象不符合要求
    downstream_effect:
      - reject_handoff_packet
      - require_acceptance_rerun
```

---

# 15. handoff_precheck_model.yaml

交接前置检查必须在生成 handoff_packet 前执行。

```yaml
handoff_precheck:
  required_inputs:
    - acceptance_result_packet
    - trace_handoff_packet
    - upstream_output_contract
    - gap_register
    - governance_rules

  checks:
    - check_id: HPRE_001
      name: Acceptance 结果存在
      condition: acceptance_result_packet_exists == true
      failure_policy: HANDOFF_BLOCKED

    - check_id: HPRE_002
      name: Acceptance 状态允许交接
      allowed_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS
      failure_policy: HANDOFF_BLOCKED

    - check_id: HPRE_003
      name: Trace 包存在
      condition: trace_handoff_packet_exists == true
      failure_policy: HANDOFF_BLOCKED

    - check_id: HPRE_004
      name: 输出合约存在
      condition: upstream_output_contract_exists == true
      failure_policy: HANDOFF_NEEDS_REWORK

    - check_id: HPRE_005
      name: 缺口已登记
      condition: all_known_gaps_registered == true
      failure_policy: HANDOFF_NEEDS_REWORK

    - check_id: HPRE_006
      name: 禁止事项未触发
      condition: forbidden_output_detected == false
      failure_policy: HANDOFF_BLOCKED

    - check_id: HPRE_007
      name: 自动实盘路径未启用
      condition: live_execution_enabled == false
      failure_policy: HANDOFF_BLOCKED
```

---

# 16. handoff_packet_contract.yaml

这是 Handoff Plane 的核心输出。

```yaml
handoff_packet:
  packet_id: string
  packet_type:
    - PLANE_HANDOFF
    - PHASE_CONTROLLER_HANDOFF
    - TOOL_BINDING_HANDOFF
    - RUNTIME_HANDOFF
    - REVIEW_UPGRADE_HANDOFF

  generated_at: datetime
  handoff_plane_version: v2.0
  run_id: string

  route:
    from_stage: string
    to_stage: string
    from_controller: string | null
    to_controller: string | null

  upstream_acceptance:
    acceptance_result_packet_id: string
    acceptance_status: string
    acceptance_score: number
    blocking_failures: list
    non_blocking_gaps: list

  upstream_trace:
    trace_handoff_packet_id: string
    trace_quality_status: string
    required_trace_ids: list
    missing_trace_ids: list

  artifacts:
    required_artifacts:
      - artifact_id: string
        file_path: string
        artifact_type: string
        usage_permission: string
        trace_id: string

    optional_artifacts:
      - artifact_id: string
        file_path: string
        usage_permission: string

  contracts:
    input_contracts_for_downstream: list
    output_contracts_from_upstream: list
    contract_trace_ids: list

  permissions:
    handoff_mode:
      - FULL_HANDOFF
      - LIMITED_HANDOFF
      - OBSERVE_ONLY_HANDOFF
      - HANDOFF_NEEDS_REWORK
      - HANDOFF_BLOCKED

    downstream_allowed_actions: list
    downstream_forbidden_actions: list
    weak_use_only_items: list
    manual_review_required_items: list

  gaps:
    propagated_gaps: list
    blocking_gaps: list
    accepted_risks: list

  limitations:
    limitation_tags: list
    forbidden_claims: list
    forbidden_runtime_actions: list

  downstream_read_instruction_id: string
  gap_propagation_packet_id: string
  limitation_transfer_packet_id: string

  audit:
    handoff_trace_id: string
    handoff_report_path: string
```

---

# 17. downstream_read_instruction_model.yaml

下游读取指令用于告诉下一阶段如何读取上游产物。

```yaml
downstream_read_instruction:
  instruction_id: string
  target_stage: string
  target_controller: string | null

  read_order:
    - step: 1
      file_or_packet: acceptance_result_packet
      purpose: 确认上游验收状态与限制

    - step: 2
      file_or_packet: trace_handoff_packet
      purpose: 确认 trace 完整性与可追踪链路

    - step: 3
      file_or_packet: handoff_packet
      purpose: 读取正式交接内容

    - step: 4
      file_or_packet: gap_propagation_packet
      purpose: 继承上游缺口

    - step: 5
      file_or_packet: limitation_transfer_packet
      purpose: 继承使用限制

    - step: 6
      file_or_packet: upstream_output_contract
      purpose: 读取可用字段、产物和合约

  read_rules:
    - rule_id: READ_001
      rule: 下游必须先读取 acceptance_result_packet，再读取业务产物

    - rule_id: READ_002
      rule: 若 handoff_mode 为 LIMITED_HANDOFF，下游必须继承 limitation_tags

    - rule_id: READ_003
      rule: weak_use_only_items 不得生成强判断

    - rule_id: READ_004
      rule: forbidden_claims 不得在下游报告中出现

    - rule_id: READ_005
      rule: 若 HANDOFF_BLOCKED，不允许目标阶段启动
```

---

# 18. gap_propagation_policy.yaml

## 18.1 缺口必须向下游传递

```yaml
gap_propagation_policy:
  gap_types:
    - MISSING_FIELD
    - MISSING_TRACE
    - CONTRACT_INCOMPLETE
    - SEMANTIC_AMBIGUITY
    - TOOL_NOT_TESTED
    - RUNTIME_NOT_VERIFIED
    - LEGACY_MAPPING_INCOMPLETE
    - THRESHOLD_NOT_CALIBRATED
    - DATA_SOURCE_UNVERIFIED

  propagation_rules:
    - rule_id: GAP_PROP_001
      gap_severity: BLOCKING_GAP
      downstream_effect: BLOCK_HANDOFF

    - rule_id: GAP_PROP_002
      gap_severity: CRITICAL_GAP
      downstream_effect: BLOCK_TARGET_STAGE

    - rule_id: GAP_PROP_003
      gap_severity: HIGH_GAP
      downstream_effect: REQUIRE_REWORK_BEFORE_RUNTIME

    - rule_id: GAP_PROP_004
      gap_severity: MEDIUM_GAP
      downstream_effect: ALLOW_WITH_LIMITATION_TAG

    - rule_id: GAP_PROP_005
      gap_severity: LOW_GAP
      downstream_effect: ALLOW_WITH_NOTE
```

## 18.2 gap_propagation_packet

```yaml
gap_propagation_packet:
  packet_id: string
  generated_at: datetime
  from_stage: string
  to_stage: string

  gaps:
    - gap_id: string
      gap_type: string
      severity: string
      description: string
      upstream_status: string
      downstream_impact: string
      required_downstream_action:
        - BLOCK_USE
        - WEAK_USE_ONLY
        - MANUAL_REVIEW
        - REGISTER_AND_CONTINUE
        - REWORK_REQUIRED

  inherited_by_downstream: boolean
```

---

# 19. limitation_transfer_policy.yaml

限制标签必须随交接传递，不能在下游消失。

```yaml
limitation_transfer_policy:
  limitation_tags:
    - WEAK_USE_ONLY
    - NO_STRONG_EVIDENCE
    - NO_STRONG_SCENARIO_CLAIM
    - NO_STRATEGY_GATE_DECISION
    - NO_TOOL_BINDING
    - NO_PAPER_RUNTIME
    - MANUAL_REVIEW_REQUIRED
    - TRACE_REPAIR_REQUIRED
    - ACCEPTANCE_RERUN_REQUIRED
    - GOVERNANCE_REVIEW_REQUIRED
    - LIVE_EXECUTION_FORBIDDEN

  transfer_rules:
    - tag: WEAK_USE_ONLY
      downstream_behavior: 下游可以读取，但不能生成强结论

    - tag: NO_STRONG_EVIDENCE
      downstream_behavior: Evidence Controller 只能生成弱证据或 UNKNOWN

    - tag: NO_STRATEGY_GATE_DECISION
      downstream_behavior: Strategy Gate 不允许输出 PAPER_READY

    - tag: NO_TOOL_BINDING
      downstream_behavior: 不允许绑定 Runner / Tool

    - tag: NO_PAPER_RUNTIME
      downstream_behavior: 不允许进入纸面运行

    - tag: LIVE_EXECUTION_FORBIDDEN
      downstream_behavior: 所有阶段必须保持自动实盘阻断
```

---

# 20. field_usage_permission_model.yaml

字段使用权限是 Handoff Plane 的关键能力。

```yaml
field_usage_permission:
  field_key: string
  source_stage: string
  target_stage: string
  trace_id: string
  data_quality_status: string
  acceptance_status: string

  permission:
    - FULL_USE
    - WEAK_USE_ONLY
    - OBSERVE_ONLY
    - DO_NOT_USE
    - REQUIRE_REFRESH
    - REQUIRE_MANUAL_REVIEW

  allowed_usage:
    - context_reference
    - weak_evidence
    - strong_evidence
    - scenario_input
    - strategy_gate_input
    - runtime_input
    - review_input

  forbidden_usage:
    - strong_claim
    - paper_ready_decision
    - execution_permission
    - live_runtime

  reason: string
```

示例：

```yaml
field_usage_permission_example:
  field_key: early_wallet_remaining_pct
  permission: WEAK_USE_ONLY
  reason: 钱包快照 trace 完整，但数据源新鲜度不足
  allowed_usage:
    - context_reference
    - weak_evidence
  forbidden_usage:
    - strong_evidence
    - strategy_gate_input
    - paper_ready_decision
```

---

# 21. forbidden_use_policy.yaml

```yaml
forbidden_use_policy:
  global_forbidden_uses:
    - use_unaccepted_artifact
    - use_untraced_artifact
    - use_rejected_phase_output
    - use_blocked_handoff
    - remove_gap_tags
    - remove_limitation_tags
    - convert_weak_to_strong_without_acceptance
    - generate_paper_ready_from_limited_handoff
    - bind_tool_without_tool_acceptance
    - start_paper_runtime_without_runtime_handoff
    - enable_live_execution

  phase_specific_forbidden_uses:
    DOMAIN_PLANE:
      - generate_buy_signal
      - generate_paper_ready
      - approve_runtime

    DATA_PLANE:
      - infer_dominant_side_intent
      - generate_evidence_strength
      - approve_strategy_gate

    TRACE_PLANE:
      - accept_phase
      - execute_handoff
      - approve_tool_binding

    ACCEPTANCE_PLANE:
      - execute_handoff
      - run_tool
      - run_runtime

    HANDOFF_PLANE:
      - override_acceptance
      - modify_upstream_output
      - remove_gap
```

---

# 22. contract_handoff_model.yaml

```yaml
contract_handoff:
  contract_handoff_id: string
  from_stage: string
  to_stage: string

  contracts:
    - contract_id: string
      contract_type:
        - INPUT_CONTRACT
        - OUTPUT_CONTRACT
        - HANDOFF_PACKET
        - TOOL_BINDING_CONTRACT
        - RUNTIME_CONTRACT
      file_path: string
      trace_id: string
      acceptance_status: string
      usage_permission: string

  validation:
    all_required_contracts_present: boolean
    incomplete_contracts: list
    rejected_contracts: list

  downstream_instruction:
    required_contract_read_order: list
    forbidden_contract_usage: list
```

---

# 23. artifact_handoff_model.yaml

```yaml
artifact_handoff:
  artifact_handoff_id: string
  from_stage: string
  to_stage: string

  artifacts:
    - artifact_id: string
      artifact_type:
        - CONTEXT_DOC
        - YAML_SCHEMA
        - CONTRACT
        - REGISTRY
        - CHECKLIST
        - REPORT
        - SCRIPT
        - TEST_FILE
      file_path: string
      trace_id: string
      acceptance_status: string
      usage_permission:
        - FULL_USE
        - WEAK_USE_ONLY
        - OBSERVE_ONLY
        - DO_NOT_USE

  required_artifacts_missing: list
  optional_artifacts_missing: list

  downstream_rules:
    must_read_first: list
    can_reference: list
    cannot_reference: list
```

---

# 24. phase_controller_handoff_model.yaml

P01-P10 业务控制器必须通过 Handoff Plane 接收基础系统能力。

```yaml
phase_controller_handoff:
  handoff_id: string
  target_phase_controller: string

  required_inputs:
    - professional_build_order
    - system_methodology_blueprint
    - governance_rules
    - domain_models
    - data_models
    - full_control_task_tree
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet

  inherited_constraints:
    - forbidden_claims
    - limitation_tags
    - gap_ids
    - trace_requirements
    - acceptance_requirements
    - paper_only_constraints

  controller_build_permission:
    allowed: boolean
    mode:
      - FULL_CONTROLLER_BUILD
      - LIMITED_CONTROLLER_BUILD
      - OBSERVE_ONLY
      - BLOCKED

  required_outputs_from_controller:
    - controller_yaml
    - controller_context_md
    - input_contract
    - output_contract
    - controller_acceptance_criteria
    - controller_handoff_packet
```

---

# 25. tool_binding_handoff_model.yaml

Runner / Tool Binding 不能直接读取业务文档，必须读取控制器交接包。

```yaml
tool_binding_handoff:
  handoff_id: string
  source_phase_controller: string
  target_tool_or_runner: string

  required_preconditions:
    - phase_controller_acceptance_ready
    - tool_binding_acceptance_ready
    - input_contract_ready
    - output_contract_ready
    - trace_requirements_ready
    - live_execution_forbidden

  tool_input_permission:
    allowed_input_files: list
    forbidden_input_files: list
    required_trace_ids: list

  tool_output_requirement:
    expected_output_files: list
    required_output_trace: true
    required_runtime_log: true
    required_error_trace: true

  execution_mode:
    - DRY_RUN_ONLY
    - TEST_ONLY
    - PAPER_ONLY
    - HUMAN_CONFIRMATION_REQUIRED
    - LIVE_FORBIDDEN
```

---

# 26. runtime_handoff_model.yaml

Paper-only Runtime 必须接收受控交接。

```yaml
runtime_handoff:
  handoff_id: string
  runtime_type: PAPER_ONLY
  from_stage: RUNNER_TOOL_BINDING
  to_stage: PAPER_ONLY_RUNTIME

  required_inputs:
    - accepted_phase_controller_packet
    - accepted_tool_binding_packet
    - execution_risk_acceptance
    - paper_only_flag
    - runtime_trace_requirement
    - risk_control_contract

  runtime_permissions:
    paper_entry_allowed: boolean
    paper_exit_allowed: boolean
    live_execution_allowed: false
    human_confirmation_required: boolean

  runtime_forbidden_actions:
    - live_market_order
    - live_limit_order
    - auto_wallet_signing
    - bypass_risk_control
    - bypass_runtime_trace

  required_outputs:
    - paper_positions_open
    - paper_positions_closed
    - paper_trades
    - paper_equity_curve
    - risk_events
    - runtime_trace
    - runtime_handoff_back_to_review
```

---

# 27. review_upgrade_handoff_model.yaml

复盘升级不能直接改实时规则，必须交接给 Governance / Full Control。

```yaml
review_upgrade_handoff:
  handoff_id: string
  from_stage: REVIEW_UPGRADE
  to_stage:
    - GOVERNANCE_PLANE
    - FULL_CONTROL_PLANE
    - SELF_UPGRADE_CONTROLLER

  required_inputs:
    - review_trace
    - runtime_trace
    - failure_attribution
    - proposed_upgrade
    - affected_rules
    - rollback_plan

  upgrade_permission:
    direct_runtime_mutation_allowed: false
    governance_review_required: true
    full_control_routing_required: true
    acceptance_rerun_required: true

  downstream_actions:
    - REGISTER_UPGRADE_CANDIDATE
    - REQUIRE_GOVERNANCE_REVIEW
    - REQUIRE_ACCEPTANCE_RERUN
    - BLOCK_DIRECT_RULE_MUTATION
```

---

# 28. handoff_trace_dependency.yaml

Handoff 必须依赖 Trace。

```yaml
handoff_trace_dependency:
  required_trace_types:
    - ARTIFACT_TRACE
    - CONTRACT_TRACE
    - STATE_TRACE
    - ACCEPTANCE_TRACE
    - HANDOFF_TRACE

  dependency_rules:
    - rule_id: HTRACE_001
      target: all_handoff_packets
      required_trace: HANDOFF_TRACE
      missing_policy: HANDOFF_BLOCKED

    - rule_id: HTRACE_002
      target: all_artifacts_in_handoff
      required_trace: ARTIFACT_TRACE
      missing_policy: HANDOFF_NEEDS_REWORK

    - rule_id: HTRACE_003
      target: all_contracts_in_handoff
      required_trace: CONTRACT_TRACE
      missing_policy: HANDOFF_BLOCKED

    - rule_id: HTRACE_004
      target: all_state_transitions
      required_trace: STATE_TRACE
      missing_policy: HANDOFF_BLOCKED

    - rule_id: HTRACE_005
      target: all_acceptance_results
      required_trace: ACCEPTANCE_TRACE
      missing_policy: HANDOFF_BLOCKED
```

---

# 29. handoff_acceptance_dependency.yaml

Handoff 必须依赖 Acceptance。

```yaml
handoff_acceptance_dependency:
  accepted_statuses:
    - ACCEPTANCE_READY
    - ACCEPTANCE_READY_WITH_GAPS

  blocked_statuses:
    - ACCEPTANCE_NEEDS_REWORK
    - ACCEPTANCE_REJECTED
    - ACCEPTANCE_BLOCKED

  rules:
    - rule_id: HACC_001
      condition: acceptance_result_packet_missing == true
      result: HANDOFF_BLOCKED

    - rule_id: HACC_002
      condition: acceptance_status in [ACCEPTANCE_REJECTED, ACCEPTANCE_BLOCKED]
      result: HANDOFF_BLOCKED

    - rule_id: HACC_003
      condition: acceptance_status == ACCEPTANCE_NEEDS_REWORK
      result: HANDOFF_NEEDS_REWORK

    - rule_id: HACC_004
      condition: acceptance_status == ACCEPTANCE_READY_WITH_GAPS
      result: HANDOFF_READY_WITH_LIMITATIONS

    - rule_id: HACC_005
      condition: acceptance_status == ACCEPTANCE_READY
      result: HANDOFF_READY
```

---

# 30. handoff_failure_policy.yaml

```yaml
handoff_failure_policy:
  failure_types:
    - MISSING_ACCEPTANCE_PACKET
    - MISSING_TRACE_PACKET
    - MISSING_OUTPUT_CONTRACT
    - MISSING_REQUIRED_ARTIFACT
    - UNREGISTERED_GAP
    - FORBIDDEN_OUTPUT_DETECTED
    - DOWNSTREAM_TARGET_UNKNOWN
    - ROUTE_NOT_REGISTERED
    - LIMITATION_TAG_DROPPED
    - LIVE_EXECUTION_PATH_DETECTED

  failure_rules:
    - failure_type: MISSING_ACCEPTANCE_PACKET
      result: HANDOFF_BLOCKED
      required_action: RUN_ACCEPTANCE_FIRST

    - failure_type: MISSING_TRACE_PACKET
      result: HANDOFF_BLOCKED
      required_action: REPAIR_TRACE

    - failure_type: MISSING_OUTPUT_CONTRACT
      result: HANDOFF_NEEDS_REWORK
      required_action: CREATE_OUTPUT_CONTRACT

    - failure_type: UNREGISTERED_GAP
      result: HANDOFF_NEEDS_REWORK
      required_action: REGISTER_GAP_AND_RERUN_ACCEPTANCE

    - failure_type: LIMITATION_TAG_DROPPED
      result: HANDOFF_BLOCKED
      required_action: REBUILD_HANDOFF_PACKET

    - failure_type: LIVE_EXECUTION_PATH_DETECTED
      result: HANDOFF_BLOCKED
      required_action: REMOVE_LIVE_EXECUTION_PATH
```

---

# 31. handoff_report_model.yaml

```yaml
handoff_report:
  report_id: string
  generated_at: datetime
  from_stage: string
  to_stage: string

  summary:
    handoff_status: string
    handoff_mode: string
    can_downstream_start: boolean
    main_limitation: string | null

  packets:
    handoff_packet_id: string
    acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    gap_propagation_packet_id: string
    limitation_transfer_packet_id: string

  transferred_artifacts:
    full_use: list
    weak_use_only: list
    observe_only: list
    do_not_use: list

  propagated_gaps:
    blocking: list
    high: list
    medium: list
    low: list

  downstream_instructions:
    read_order: list
    allowed_actions: list
    forbidden_actions: list
    required_next_checks: list
```

---

# 32. handoff_storage_constitution.md

建议目录：

```text
/root/sikk-gmgn/data/handoff_plane/
  handoff_packets/
  downstream_read_instructions/
  gap_propagation/
  limitation_transfer/
  field_usage_permissions/
  forbidden_use/
  contract_handoff/
  artifact_handoff/
  phase_controller_handoff/
  tool_binding_handoff/
  runtime_handoff/
  review_upgrade_handoff/
  handoff_reports/
  handoff_failures/
  audit/
```

目录原则：

```text
1. handoff_packets 存机器可读交接包。
2. downstream_read_instructions 存下游读取顺序。
3. gap_propagation 存缺口传递包。
4. limitation_transfer 存限制标签传递。
5. field_usage_permissions 存字段使用权限。
6. forbidden_use 存禁止使用规则。
7. contract_handoff 存合约交接记录。
8. artifact_handoff 存文件产物交接记录。
9. phase_controller_handoff 存业务控制器交接。
10. tool_binding_handoff 存工具绑定交接。
11. runtime_handoff 存纸面运行交接。
12. review_upgrade_handoff 存复盘升级回传。
13. handoff_reports 存人类可读报告。
14. handoff_failures 存交接失败记录。
15. audit 存审计记录。
```

---

# 33. HER Handoff 执行协议

文件：

```text
her_handoff_execution_protocol.md
```

HER 执行 Handoff 时必须按此顺序：

```text
1. 读取 handoff_context.md。
2. 读取 handoff_object_registry.yaml。
3. 读取 Acceptance Plane 的 acceptance_result_packet。
4. 读取 Trace Plane 的 trace_handoff_packet。
5. 读取 Full Control Plane 的 contract_router 和 phase_execution_order。
6. 检查目标下游阶段是否已注册。
7. 执行 handoff_precheck。
8. 判断 handoff_mode。
9. 生成 handoff_packet。
10. 生成 downstream_read_instruction。
11. 生成 gap_propagation_packet。
12. 生成 limitation_transfer_packet。
13. 生成 field_usage_permission_packet。
14. 生成 forbidden_use_policy。
15. 写入 handoff_trace。
16. 输出 handoff_report。
17. 将 handoff_status 写回 Full Control Plane。
```

禁止：

```text
1. 不允许未读取 acceptance_result_packet 就交接。
2. 不允许未读取 trace_handoff_packet 就交接。
3. 不允许交接 ACCEPTANCE_REJECTED 或 ACCEPTANCE_BLOCKED 的结果。
4. 不允许删除 gap。
5. 不允许删除 limitation_tags。
6. 不允许把 LIMITED_HANDOFF 改成 FULL_HANDOFF。
7. 不允许下游绕过 downstream_read_instruction。
8. 不允许无 Tool Binding Acceptance 进入 Runner。
9. 不允许无 Runtime Handoff 进入 Paper-only Runtime。
10. 不允许任何自动实盘路径通过 Handoff。
```

---

# 34. Full Control Plane 需要同步更新

Handoff Plane 加入后，Full Control Plane 必须更新：

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
  - route_id: ROUTE_ACCEPTANCE_TO_HANDOFF
    from_stage: ACCEPTANCE_PLANE
    to_stage: HANDOFF_PLANE
    required_packet: acceptance_result_packet
    missing_policy: BLOCK_HANDOFF

  - route_id: ROUTE_HANDOFF_TO_PHASE_CONTROLLERS
    from_stage: HANDOFF_PLANE
    to_stage: P01_P10_PHASE_CONTROLLERS
    required_packet: handoff_packet
    missing_policy: BLOCK_PHASE_CONTROLLER_BUILD

  - route_id: ROUTE_HANDOFF_TO_TOOL_BINDING
    from_stage: HANDOFF_PLANE
    to_stage: RUNNER_TOOL_BINDING
    required_packet: tool_binding_handoff
    missing_policy: BLOCK_TOOL_BINDING

  - route_id: ROUTE_HANDOFF_TO_PAPER_RUNTIME
    from_stage: HANDOFF_PLANE
    to_stage: PAPER_ONLY_RUNTIME
    required_packet: runtime_handoff
    missing_policy: BLOCK_PAPER_RUNTIME
```

新增全局状态码：

```yaml
global_status_codes:
  - HANDOFF_READY
  - HANDOFF_READY_WITH_LIMITATIONS
  - HANDOFF_NEEDS_REWORK
  - HANDOFF_BLOCKED
  - HANDOFF_REJECTED
```

新增全局硬规则：

```yaml
global_hard_negative_rules:
  - Handoff without Acceptance is blocked
  - Handoff without Trace is blocked
  - Limited Handoff cannot be upgraded to Full Handoff without re-acceptance
  - Tool Binding without Handoff is blocked
  - Paper Runtime without Runtime Handoff is blocked
  - Live execution remains forbidden
```

---

# 35. Handoff Plane 自身验收标准

## 35.1 HANDOFF_READY

必须满足：

```text
1. handoff_plane.yaml 已完成
2. handoff_context.md 已完成
3. handoff_object_registry.yaml 已完成
4. handoff_mode_policy.yaml 已完成
5. handoff_status_code_table.yaml 已完成
6. handoff_precheck_model.yaml 已完成
7. handoff_packet_contract.yaml 已完成
8. downstream_read_instruction_model.yaml 已完成
9. gap_propagation_policy.yaml 已完成
10. limitation_transfer_policy.yaml 已完成
11. field_usage_permission_model.yaml 已完成
12. forbidden_use_policy.yaml 已完成
13. contract_handoff_model.yaml 已完成
14. artifact_handoff_model.yaml 已完成
15. phase_controller_handoff_model.yaml 已完成
16. tool_binding_handoff_model.yaml 已完成
17. runtime_handoff_model.yaml 已完成
18. review_upgrade_handoff_model.yaml 已完成
19. handoff_trace_dependency.yaml 已完成
20. handoff_acceptance_dependency.yaml 已完成
21. handoff_failure_policy.yaml 已完成
22. handoff_report_model.yaml 已完成
23. handoff_storage_constitution.md 已完成
24. handoff_gap_register.md 已完成
25. handoff_review_checklist.md 已完成
26. her_handoff_execution_protocol.md 已完成
27. 已定义 FULL_HANDOFF / LIMITED_HANDOFF / OBSERVE_ONLY / BLOCKED
28. 已定义 gap propagation
29. 已定义 limitation transfer
30. 已定义 field usage permission
31. 已定义 forbidden use
32. 已定义 P01-P10 接收规则
33. 已定义 Runner / Tool Binding 接收规则
34. 已定义 Paper-only Runtime 接收规则
35. 已定义 Review / Upgrade 回传规则
36. 不存在无 Acceptance 即可 Handoff 的路径
37. 不存在无 Trace 即可 Handoff 的路径
38. 不存在 Handoff 允许自动实盘的路径
```

---

## 35.2 HANDOFF_READY_WITH_LIMITATIONS

允许进入 P01-P10 草案设计，但必须限制：

```text
1. 部分历史文件没有完整 trace，只能 limited handoff
2. 部分 legacy 产物只能 observe_only
3. 部分工具尚未接受 Tool Binding 验收
4. Paper Runtime handoff 只定义模型，未真实运行
5. Review / Upgrade 回传链尚未有样本
6. handoff validator 尚未代码化
```

限制：

```text
可以进入 P01-P10 Phase Controller 设计
可以生成 Controller 草案
可以传递 gap 和 limitation
不允许进入自动 Paper Runtime
不允许进入任何自动实盘路径
不允许把 WITH_LIMITATIONS 当成 FULL_HANDOFF
```

---

## 35.3 HANDOFF_REJECTED

以下情况必须驳回：

```text
1. Handoff Plane 只是文件列表
2. 没有 handoff_packet_contract
3. 没有 downstream_read_instruction
4. 没有 gap propagation
5. 没有 limitation transfer
6. 没有 field usage permission
7. 没有 forbidden use policy
8. 没有 Acceptance 依赖
9. 没有 Trace 依赖
10. 下游可以绕过 Handoff 读取上游文件
11. Runner 可以绕过 Handoff 绑定工具
12. Paper Runtime 可以绕过 Handoff 运行
13. 自动实盘路径没有被明确阻断
```

---

# 36. 给 HER 的可执行任务书

```text
任务名称：建立 Handoff Plane｜交接平面专业版 v2.0

目标：
在 /root/sikk-gmgn/system/handoff_plane/ 下建立 SIKK Stable Trader OS 的 Handoff Plane。该平面不是文件列表，也不是简单把上游结果交给下游，而是系统交接控制平面。它负责读取 Acceptance Plane 输出的 acceptance_result_packet、Trace Plane 输出的 trace_handoff_packet、Full Control Plane 的合约路由和任务树，将已验收产物转换成下游可读取、可限制使用、可追踪、可复盘的标准 handoff_packet，并传递缺口、限制、字段权限、禁止事项和下游读取指令。

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
1. Handoff Plane 不调度任务，调度属于 Full Control Plane。
2. Handoff Plane 不做验收裁决，裁决属于 Acceptance Plane。
3. Handoff Plane 不创建 trace，trace 属于 Trace Plane。
4. Handoff Plane 不修改上游产物。
5. Handoff Plane 不隐藏缺口。
6. Handoff Plane 不删除限制标签。
7. Handoff Plane 不允许把 READY_WITH_GAPS 或 LIMITED_HANDOFF 改成 FULL_HANDOFF。
8. Handoff Plane 不生成交易信号。
9. Handoff Plane 不执行工具。
10. Handoff Plane 不运行纸面交易。
11. Handoff Plane 不允许任何自动实盘路径通过。
12. 下游阶段必须读取 Handoff Plane 输出的 downstream_read_instruction。

需要创建目录：
/root/sikk-gmgn/system/handoff_plane/

需要创建文件：
1. handoff_plane.yaml
2. handoff_context.md
3. handoff_object_registry.yaml
4. handoff_mode_policy.yaml
5. handoff_status_code_table.yaml
6. handoff_precheck_model.yaml
7. handoff_packet_contract.yaml
8. downstream_read_instruction_model.yaml
9. gap_propagation_policy.yaml
10. limitation_transfer_policy.yaml
11. field_usage_permission_model.yaml
12. forbidden_use_policy.yaml
13. contract_handoff_model.yaml
14. artifact_handoff_model.yaml
15. phase_controller_handoff_model.yaml
16. tool_binding_handoff_model.yaml
17. runtime_handoff_model.yaml
18. review_upgrade_handoff_model.yaml
19. handoff_trace_dependency.yaml
20. handoff_acceptance_dependency.yaml
21. handoff_failure_policy.yaml
22. handoff_report_model.yaml
23. handoff_storage_constitution.md
24. handoff_gap_register.md
25. handoff_review_checklist.md
26. her_handoff_execution_protocol.md

文件要求：
- handoff_plane.yaml：定义 Handoff Plane 的身份、使命、权限、边界、上游输入、下游输出、状态码。
- handoff_context.md：写成 HER 执行前必须读取的交接上下文。
- handoff_object_registry.yaml：注册所有交接对象，包括方法论、Plane、Phase Controller、Tool Binding、Runtime、Review / Upgrade。
- handoff_mode_policy.yaml：定义 FULL_HANDOFF、LIMITED_HANDOFF、OBSERVE_ONLY_HANDOFF、HANDOFF_NEEDS_REWORK、HANDOFF_BLOCKED。
- handoff_status_code_table.yaml：定义 HANDOFF_READY、HANDOFF_READY_WITH_LIMITATIONS、HANDOFF_NEEDS_REWORK、HANDOFF_BLOCKED、HANDOFF_REJECTED。
- handoff_precheck_model.yaml：定义交接前置检查，包括 Acceptance、Trace、Output Contract、Gap、Governance、Live Execution 禁止检查。
- handoff_packet_contract.yaml：定义标准 handoff_packet。
- downstream_read_instruction_model.yaml：定义下游读取顺序和读取规则。
- gap_propagation_policy.yaml：定义缺口传递规则和 gap_propagation_packet。
- limitation_transfer_policy.yaml：定义限制标签传递规则。
- field_usage_permission_model.yaml：定义字段使用权限，包括 FULL_USE、WEAK_USE_ONLY、OBSERVE_ONLY、DO_NOT_USE、REQUIRE_REFRESH、REQUIRE_MANUAL_REVIEW。
- forbidden_use_policy.yaml：定义全局禁止使用和阶段特定禁止使用。
- contract_handoff_model.yaml：定义合约交接。
- artifact_handoff_model.yaml：定义文件产物交接。
- phase_controller_handoff_model.yaml：定义 P01-P10 控制器接收基础系统产物的规则。
- tool_binding_handoff_model.yaml：定义 Runner / Tool Binding 的交接前置条件和执行模式。
- runtime_handoff_model.yaml：定义 Paper-only Runtime 的交接条件、权限和禁止动作。
- review_upgrade_handoff_model.yaml：定义 Review / Upgrade 回传 Governance / Full Control / Self-Upgrade 的规则。
- handoff_trace_dependency.yaml：定义 Handoff 对 Trace 的依赖。
- handoff_acceptance_dependency.yaml：定义 Handoff 对 Acceptance 的依赖。
- handoff_failure_policy.yaml：定义交接失败处理。
- handoff_report_model.yaml：定义人类可读交接报告。
- handoff_storage_constitution.md：定义交接数据目录。
- handoff_gap_register.md：登记当前交接体系缺口。
- handoff_review_checklist.md：建立交接平面审计清单。
- her_handoff_execution_protocol.md：定义 HER 如何执行交接。

同时更新 Full Control Plane：
1. 在 phase_execution_order.yaml 中加入 Handoff Plane，位于 Acceptance Plane 后、P01-P10 Phase Controller 前。
2. 在 contract_router.yaml 中加入 ROUTE_ACCEPTANCE_TO_HANDOFF、ROUTE_HANDOFF_TO_PHASE_CONTROLLERS、ROUTE_HANDOFF_TO_TOOL_BINDING、ROUTE_HANDOFF_TO_PAPER_RUNTIME。
3. 在 global_status_code_table.yaml 中加入 HANDOFF_READY、HANDOFF_READY_WITH_LIMITATIONS、HANDOFF_NEEDS_REWORK、HANDOFF_BLOCKED、HANDOFF_REJECTED。
4. 在 global_hard_negative_rules.yaml 中加入 Handoff without Acceptance blocked、Handoff without Trace blocked、Tool Binding without Handoff blocked、Paper Runtime without Runtime Handoff blocked、Live execution forbidden。
5. 在 handoff_packet_registry.yaml 中注册 handoff_packet、gap_propagation_packet、limitation_transfer_packet、field_usage_permission_packet。

验收输出：
1. 文件创建清单
2. 每个文件的核心摘要
3. HANDOFF_READY / HANDOFF_READY_WITH_LIMITATIONS / HANDOFF_REJECTED 判断
4. 交接对象注册摘要
5. 交接模式摘要
6. handoff_packet 合约摘要
7. downstream_read_instruction 摘要
8. gap propagation 摘要
9. limitation transfer 摘要
10. field usage permission 摘要
11. P01-P10 如何接收 Handoff
12. Runner / Tool Binding 如何接收 Handoff
13. Paper-only Runtime 如何接收 Handoff
14. Review / Upgrade 如何回传 Handoff
15. 当前缺口清单
16. 是否达到轻量机构级 Handoff Plane v2.0

最终验收标准：
只有当交接对象、交接模式、交接状态码、交接前置检查、handoff_packet、downstream_read_instruction、gap propagation、limitation transfer、field usage permission、forbidden use、contract handoff、artifact handoff、phase controller handoff、tool binding handoff、runtime handoff、review upgrade handoff、Trace 依赖、Acceptance 依赖、失败处理、报告模型、存储宪法、HER 交接协议全部存在，并且下游不能绕过 Handoff、Runner 不能绕过 Handoff、Paper Runtime 不能绕过 Handoff、自动实盘路径被明确阻断时，才允许标记为 HANDOFF_READY。
```

---

# 37. 当前是否达到轻量机构级专业标准？

## 判断

按这版设计，Handoff Plane 达到：

```text
轻量机构级 v2.0 设计标准
```

它不是文件传递层，而是系统级**交接权限控制层**。

---

## 已经达到的能力

|能力|状态|
|---|---|
|交接对象注册|已设计|
|交接模式|已设计|
|交接状态码|已设计|
|交接前置检查|已设计|
|handoff_packet 合约|已设计|
|下游读取指令|已设计|
|缺口传递|已设计|
|限制标签传递|已设计|
|字段使用权限|已设计|
|禁止使用规则|已设计|
|合约交接|已设计|
|文件产物交接|已设计|
|P01-P10 控制器交接|已设计|
|Runner / Tool Binding 交接|已设计|
|Paper Runtime 交接|已设计|
|Review / Upgrade 回传|已设计|
|Trace 依赖|已设计|
|Acceptance 依赖|已设计|
|失败处理|已设计|
|HER 交接协议|已设计|

---

## 还没达到工程级落地的部分

|缺口|原因|后续处理|
|---|---|---|
|handoff validator 未代码化|当前是模型设计|后续实现 `handoff_validator.py`|
|handoff packet 尚未真实生成|需要 HER 执行|Handoff 执行阶段|
|legacy 文件交接需特殊处理|旧文件缺 trace / acceptance|legacy limited handoff|
|P01-P10 尚未建立|下一阶段|建立 Phase Controller Index|
|Tool Binding 尚未进入|需要控制器验收后|后续接入|
|Paper Runtime 尚未运行|需要工具绑定后|后续验证|
|Review / Upgrade 回传链无样本|需要纸面运行积累|后续补齐|
|limitation tag 权限还未代码化|规则已定义|validator 阶段实现|
|Full Control Plane 需同步更新路由|已定义|HER 执行修正|
|自动化交接审计未落地|需要脚本|工程阶段实现|

---

# 38. 下一步应该做什么

Handoff Plane 完成后，才进入：

```text
P01-P10 Phase Controller：业务阶段控制器
```

但不是直接写十个业务模块，而是先建立：

```text
phase_controller_index.yaml
```

也就是 P01-P10 的总索引，先定义每个业务控制器：

```text
负责什么
读取什么 handoff
输出什么合约
需要什么 trace
需要什么 acceptance
能不能绑定工具
能不能进入 paper runtime
禁止什么
```

推荐下一步：

```text
P01-P10 Phase Controller Index：业务阶段控制器总索引
```

之后再逐个展开：

```text
P01 Candidate Intake Controller
P02 Source Data Fact Controller
P03 Wallet Entity Controller
P04 Chip Structure Controller
P05 Evidence Controller
P06 Scenario Recognition Controller
P07 Strategy Gate Controller
P08 Execution Risk Controller
P09 Review Replay Controller
P10 Self Upgrade Controller
```

---

# 本次认知升级点

1. **Handoff Plane 是交接权限控制层，不是文件传递层。**
    
2. **Handoff 必须读取 Acceptance 和 Trace。**  
    无验收、无追踪，不能交接。
    
3. **交接包必须携带缺口、限制、禁止事项和字段使用权限。**
    
4. **READY_WITH_GAPS 不能被下游当成 READY 使用。**
    
5. **字段级权限很重要。**  
    某些字段可以观察，不能生成强证据；某些字段可以生成弱证据，不能进入策略门控。
    
6. **下游必须按 downstream_read_instruction 读取，不允许自由读取上游文件。**
    
7. **Runner / Tool Binding 必须通过 Handoff 接收输入，不允许直接读业务文档。**
    
8. **Paper-only Runtime 必须通过 runtime_handoff，自动实盘继续阻断。**
    
9. **Review / Upgrade 必须通过回传 Handoff 返回 Governance / Full Control，不能直接修改实时规则。**
    

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|P01-P10 Phase Controller Index 尚未建立|下一步核心|先做总索引|
|handoff validator 未实现|模型已定义|工程阶段实现|
|Handoff 包尚未真实生成|需要 HER 执行|执行阶段处理|
|legacy 产物交接标准需单独处理|旧文件缺 trace / acceptance|设为 LIMITED / OBSERVE_ONLY|
|Tool Binding 交接还没有真实样本|后续阶段|Runner 阶段验证|
|Paper Runtime 交接未跑通|后续阶段|Paper-only Runtime 验证|
|Review / Upgrade 回传链未验证|需要运行样本|复盘后补齐|
|Full Control 路由需同步更新|已定义|HER 执行修正|
|下游限制标签如何代码化|规则已定义|validator / runner 阶段实现|
|字段使用权限需要与 Data / Trace 联动|当前为模型|P01-P10 与 Data 工程阶段打通|