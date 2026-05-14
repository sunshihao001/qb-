# Full Control Plane：完整控制面专业化设计

## 0. 核心定位

**Full Control Plane 不是普通总说明、不是阶段表、不是 dashboard，也不是某一个 Skill。**

它是 SIKK Stable Trader OS 的**最高级控制面**，负责把系统目标、阶段目标、任务树、数据合约、Atomic Skill、代码工具、验收门、状态回写、下游交接、失败处理、复盘审计全部接成一个可调度闭环。

一句话定义：

> **Full Control Plane 是系统的运行总控层。**  
> 它不负责替代每个阶段做专业判断，而是保证每个阶段按照正确顺序、正确权限、正确输入、正确输出、正确验收和正确交接运行。

---

# 1. Full Control Plane 与前面几个 Plane 的关系

你前面已经建立了：

```text
Governance Plane：治理平面
负责系统原则、权限边界、风险红线、禁止事项。

Domain Plane：领域平面
负责定义系统到底在判断什么，包括领域对象、场景、生命周期、证据/反证语义。

Data Plane：数据平面
负责把领域需求转成可采集、可校验、可追溯、可交接的数据事实。
```

现在的 **Full Control Plane** 是更高一层：

```text
Full Control Plane
  ↓ 控制
Governance Plane
Domain Plane
Data Plane
Evidence Plane
Scenario Plane
Strategy Gate Plane
Execution Risk Plane
Review / Replay Plane
Self-Upgrade Plane
```

它的职责不是新增一个业务判断阶段，而是建立：

```text
全阶段调度系统
全阶段状态系统
全阶段验收系统
全阶段交接系统
全阶段审计系统
全阶段失败恢复系统
```

---

# 2. Full Control Plane 的专业定义

```text
Full Control Plane 是 SIKK Stable Trader OS 的完整控制面。

它负责接收系统总目标或阶段目标，将目标编译成阶段运行计划，将阶段运行计划拆解成任务树，将任务树绑定到 Phase Controller、输入合约、输出合约、Atomic Skill、代码工具、数据目录、验收门、状态码、审计日志和下游交接包。

它不直接做交易判断，不直接采集数据，不直接生成策略信号，不直接执行交易。

它的核心价值是防止系统变成“文档很多、阶段很多、数据很多，但没有统一运行秩序”的松散工程。
```

---

# 3. Full Control Plane 的阶段目标

## 3.1 总目标

建立一个轻量机构级别的**系统总控运行层**，让 HER / SIKK 后续执行任何任务时都能自动回答：

```text
当前任务属于哪个阶段？
当前阶段是否已经准备好？
需要读取哪些上下文？
需要调用哪些文件？
需要依赖哪些上游合约？
需要生成哪些下游输出？
哪些判断允许做？
哪些判断禁止做？
验收标准是什么？
失败后怎么处理？
状态写回哪里？
下一阶段是什么？
是否允许继续推进？
```

---

## 3.2 最终效果

Full Control Plane 完成后，系统应该具备以下能力：

|能力|目标|
|---|---|
|目标编译|把自然语言目标转成阶段任务树|
|阶段调度|自动判断应该进入哪个 Plane / Phase|
|权限控制|防止阶段越权，比如 Data Plane 直接输出买入信号|
|合约路由|知道每个阶段读取什么、输出什么|
|状态回写|每个阶段完成后写入统一状态|
|验收阻断|未通过验收不得进入下游|
|缺口登记|不能完成时明确登记缺口，而不是假装完成|
|失败恢复|知道失败后重跑、降级、暂停还是阻断|
|审计复盘|后续能追溯每一步为什么推进或停止|
|长时间任务控制|HER 可以分阶段连续执行，而不是跑一会停下|

---

# 4. Full Control Plane 不是做什么

## 4.1 不能做

|禁止事项|原因|
|---|---|
|不能直接替代 Domain Plane 定义场景|否则领域语义会混乱|
|不能直接替代 Data Plane 采集字段|否则数据血缘不清|
|不能直接生成买入信号|策略权限属于 Strategy Gate|
|不能直接执行交易|执行权限属于 Execution Risk|
|不能用“任务完成”代替“验收通过”|完成文件不代表系统可用|
|不能让 AI 自由判断阶段状态|状态必须来自状态码和验收门|
|不能无视缺口继续推进|缺口必须登记、降权或阻断|
|不能让旧目录继续污染新体系|legacy 只能映射，不能混写|
|不能把所有模块塞进一个大文件|必须合约化、分层化、可调度|

---

# 5. Full Control Plane 的底层系统原理

要达到轻量机构水准，Full Control Plane 应该按这些原理设计。

## 5.1 控制论原则

系统不是一次性生成内容，而是持续控制状态变化。

```text
目标 → 输入 → 处理 → 输出 → 验收 → 状态回写 → 下一阶段
```

如果没有状态回写，系统就不知道自己在哪里。

---

## 5.2 契约优先原则

每个阶段必须先定义：

```text
输入合约
输出合约
字段要求
状态码
验收门
失败处理
```

再进入具体实现。

否则会变成：

```text
写了很多文件
但不知道谁读取
不知道谁验证
不知道怎么接下游
```

---

## 5.3 职责隔离原则

Full Control Plane 只控制流程，不抢业务判断权。

```text
Full Control Plane：负责调度与验收
Governance Plane：负责边界与规则
Domain Plane：负责领域语义
Data Plane：负责数据事实
Evidence Plane：负责证据对象
Scenario Plane：负责场景识别
Strategy Gate Plane：负责策略准入
Execution Risk Plane：负责执行风控
Review Plane：负责复盘校准
```

---

## 5.4 失败优先原则

专业系统不是只设计成功路径，还要明确失败路径：

```text
缺字段怎么办
合约不匹配怎么办
验收不通过怎么办
数据过期怎么办
阶段越权怎么办
旧数据路径冲突怎么办
HER 中途停下怎么办
文件生成但内容不合格怎么办
```

---

## 5.5 可审计原则

每个阶段必须留下：

```text
输入来源
处理动作
输出文件
状态码
验收结果
缺口登记
失败原因
下游交接包
```

否则后续无法复盘，也无法让系统自我升级。

---

# 6. Full Control Plane 的核心组成

## 6.1 一张总表

```text
Full Control Plane =
  阶段注册中心
+ 控制上下文
+ Phase Controller 注册表
+ 任务树编译器
+ 合约路由器
+ 状态机
+ 验收门
+ 失败处理器
+ 缺口登记器
+ 审计日志
+ 下游交接系统
+ HER 执行协议
```

---

# 7. Full Control Plane 必须包含的数据

## 7.1 阶段身份证

文件：

```text
/root/sikk-gmgn/system/full_control_plane/full_control_plane.yaml
```

建议结构：

```yaml
plane_id: P00_FULL_CONTROL_PLANE
plane_name: 完整控制面
plane_level: light_institutional
version: v1.0
status: DRAFT_READY_FOR_AUDIT

mission:
  primary: 建立 SIKK Stable Trader OS 的全阶段调度、验收、状态回写和交接控制系统
  secondary:
    - 把系统总目标编译成阶段任务树
    - 把阶段任务绑定到 Phase Controller
    - 管理输入合约、输出合约、验收门和状态码
    - 防止阶段越权
    - 管理失败处理和缺口登记
    - 支持 HER 长时间阶段化执行
    - 支持后续审计、复盘和自我升级

authority:
  can_do:
    - 读取系统总目标
    - 读取阶段上下文
    - 判断当前应进入哪个阶段
    - 生成阶段任务树
    - 调用对应 Phase Controller
    - 检查阶段输入合约
    - 检查阶段输出合约
    - 执行验收门
    - 写入全局状态码
    - 生成下游交接包
    - 登记缺口和失败原因
    - 暂停或阻断不合格阶段

  cannot_do:
    - 直接生成交易信号
    - 直接执行交易
    - 直接伪造数据
    - 直接越过 Governance Plane
    - 直接用缺失字段强判断
    - 直接把未验收阶段标记为完成
    - 直接覆盖 raw 数据
    - 直接删除 legacy 数据

upstream_inputs:
  - user_goal
  - governance_rules
  - domain_models
  - data_models
  - existing_runtime_outputs
  - phase_handoff_packets

downstream_outputs:
  - phase_task_tree
  - phase_execution_plan
  - phase_status_update
  - acceptance_report
  - gap_register_update
  - next_phase_handoff_packet
  - audit_log

global_status_codes:
  - CONTROL_UNINITIALIZED
  - CONTROL_CONTEXT_READY
  - PHASE_SELECTED
  - TASK_TREE_COMPILED
  - INPUT_CONTRACT_VALIDATED
  - PHASE_EXECUTION_RUNNING
  - PHASE_OUTPUT_GENERATED
  - ACCEPTANCE_CHECK_RUNNING
  - PHASE_READY
  - PHASE_READY_WITH_GAPS
  - PHASE_REJECTED
  - PHASE_BLOCKED
  - PHASE_NEEDS_REWORK
  - HANDOFF_READY
  - SYSTEM_PAUSED
  - SYSTEM_RECOVERY_REQUIRED
```

---

# 8. Full Control Plane 的文件体系

建议目录：

```text
/root/sikk-gmgn/system/full_control_plane/
```

必须创建：

```text
full_control_plane.yaml
control_context.md
global_plane_registry.yaml
phase_controller_registry.yaml
phase_dependency_graph.yaml
phase_execution_order.yaml
task_tree_schema.yaml
task_package_contract.yaml
contract_router.yaml
input_contract_registry.yaml
output_contract_registry.yaml
acceptance_gate_registry.yaml
global_status_code_table.yaml
global_hard_negative_rules.yaml
phase_state_machine.yaml
execution_permission_matrix.yaml
skill_tool_registry.yaml
data_path_router.yaml
handoff_packet_registry.yaml
audit_log_model.yaml
gap_register_model.yaml
failure_recovery_policy.yaml
legacy_mapping_policy.yaml
human_override_policy.yaml
control_acceptance_criteria.md
control_review_checklist.md
her_full_control_execution_protocol.md
```

---

# 9. 每个文件的作用

|文件|作用|
|---|---|
|`full_control_plane.yaml`|完整控制面身份证|
|`control_context.md`|HER 运行前必须读取的控制上下文|
|`global_plane_registry.yaml`|全部 Plane 注册表|
|`phase_controller_registry.yaml`|每个阶段的 Controller 注册|
|`phase_dependency_graph.yaml`|阶段依赖关系图|
|`phase_execution_order.yaml`|阶段执行顺序|
|`task_tree_schema.yaml`|任务树结构|
|`task_package_contract.yaml`|阶段任务包合约|
|`contract_router.yaml`|输入/输出合约路由|
|`input_contract_registry.yaml`|输入合约注册表|
|`output_contract_registry.yaml`|输出合约注册表|
|`acceptance_gate_registry.yaml`|验收门注册表|
|`global_status_code_table.yaml`|全局状态码表|
|`global_hard_negative_rules.yaml`|全局硬否定规则|
|`phase_state_machine.yaml`|阶段状态机|
|`execution_permission_matrix.yaml`|各阶段权限矩阵|
|`skill_tool_registry.yaml`|Skill / 工具注册表|
|`data_path_router.yaml`|数据路径路由|
|`handoff_packet_registry.yaml`|交接包注册|
|`audit_log_model.yaml`|审计日志模型|
|`gap_register_model.yaml`|缺口登记模型|
|`failure_recovery_policy.yaml`|失败恢复策略|
|`legacy_mapping_policy.yaml`|旧数据映射规则|
|`human_override_policy.yaml`|人工干预规则|
|`control_acceptance_criteria.md`|控制面验收标准|
|`control_review_checklist.md`|控制面审计清单|
|`her_full_control_execution_protocol.md`|HER 长时间执行协议|

---

# 10. 全局 Plane 注册表

文件：

```text
global_plane_registry.yaml
```

## 10.1 注册内容

```yaml
planes:
  - plane_id: P00_FULL_CONTROL_PLANE
    plane_name: 完整控制面
    responsibility: 全阶段调度、验收、回写、阻断、交接
    input_contracts:
      - user_goal_contract
      - phase_status_contract
    output_contracts:
      - phase_task_tree_contract
      - control_handoff_contract
    can_trigger:
      - P01_GOVERNANCE_PLANE
      - P02_DOMAIN_PLANE
      - P03_DATA_PLANE
      - P04_EVIDENCE_PLANE
      - P05_SCENARIO_RECOGNITION_PLANE
      - P06_STRATEGY_GATE_PLANE
      - P07_EXECUTION_RISK_PLANE
      - P08_REVIEW_REPLAY_PLANE
      - P09_SELF_UPGRADE_PLANE

  - plane_id: P01_GOVERNANCE_PLANE
    plane_name: 治理平面
    responsibility: 定义系统边界、权限、风险红线、禁止事项
    input_contracts:
      - control_handoff_contract
    output_contracts:
      - governance_handoff_contract
    forbidden_outputs:
      - buy_signal
      - execution_order

  - plane_id: P02_DOMAIN_PLANE
    plane_name: 领域平面
    responsibility: 定义领域对象、场景、生命周期、证据语义
    input_contracts:
      - governance_handoff_contract
    output_contracts:
      - domain_handoff_contract
    forbidden_outputs:
      - buy_signal
      - execution_order

  - plane_id: P03_DATA_PLANE
    plane_name: 数据平面
    responsibility: 生成可采集、可校验、可追溯的数据事实体系
    input_contracts:
      - domain_handoff_contract
    output_contracts:
      - data_handoff_contract
    forbidden_outputs:
      - buy_signal
      - dominant_side_intent_claim
```

---

# 11. Phase Controller 注册表

文件：

```text
phase_controller_registry.yaml
```

## 11.1 核心定义

每个阶段都必须有自己的 Phase Controller。

```text
Phase Controller 不是阶段说明文档。

Phase Controller 是一个可调度的阶段运行单元，负责把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。
```

## 11.2 注册格式

```yaml
phase_controllers:
  - controller_id: PC01_GOVERNANCE_CONTROLLER
    plane_id: P01_GOVERNANCE_PLANE
    controller_name: 治理平面控制器
    responsibility:
      - 读取系统总目标
      - 建立权限边界
      - 建立禁止事项
      - 建立治理验收门
    input_required:
      - user_goal
      - system_boundary
    output_required:
      - governance_plane.yaml
      - governance_context.md
      - governance_handoff_contract.yaml
    acceptance_gate:
      - GOVERNANCE_READY
      - GOVERNANCE_READY_WITH_GAPS
      - GOVERNANCE_REJECTED
    downstream:
      - PC02_DOMAIN_CONTROLLER

  - controller_id: PC02_DOMAIN_CONTROLLER
    plane_id: P02_DOMAIN_PLANE
    controller_name: 领域平面控制器
    responsibility:
      - 定义领域对象
      - 定义钱包角色
      - 定义生命周期
      - 定义场景分类
      - 定义证据与反证语义
    input_required:
      - governance_handoff_contract
    output_required:
      - domain_handoff_contract.yaml
    acceptance_gate:
      - DOMAIN_READY
      - DOMAIN_READY_WITH_GAPS
      - DOMAIN_REJECTED
    downstream:
      - PC03_DATA_CONTROLLER
```

---

# 12. 阶段依赖图

文件：

```text
phase_dependency_graph.yaml
```

建议结构：

```yaml
phase_dependencies:
  P01_GOVERNANCE_PLANE:
    depends_on:
      - P00_FULL_CONTROL_PLANE
    unlocks:
      - P02_DOMAIN_PLANE

  P02_DOMAIN_PLANE:
    depends_on:
      - P01_GOVERNANCE_PLANE
    unlocks:
      - P03_DATA_PLANE

  P03_DATA_PLANE:
    depends_on:
      - P02_DOMAIN_PLANE
    unlocks:
      - P04_EVIDENCE_PLANE

  P04_EVIDENCE_PLANE:
    depends_on:
      - P03_DATA_PLANE
    unlocks:
      - P05_SCENARIO_RECOGNITION_PLANE

  P05_SCENARIO_RECOGNITION_PLANE:
    depends_on:
      - P04_EVIDENCE_PLANE
    unlocks:
      - P06_STRATEGY_GATE_PLANE

  P06_STRATEGY_GATE_PLANE:
    depends_on:
      - P05_SCENARIO_RECOGNITION_PLANE
      - P01_GOVERNANCE_PLANE
    unlocks:
      - P07_EXECUTION_RISK_PLANE
      - P08_REVIEW_REPLAY_PLANE

  P07_EXECUTION_RISK_PLANE:
    depends_on:
      - P06_STRATEGY_GATE_PLANE
    unlocks:
      - PAPER_EXECUTION
      - HUMAN_CONFIRMATION_ONLY

  P08_REVIEW_REPLAY_PLANE:
    depends_on:
      - P03_DATA_PLANE
      - P04_EVIDENCE_PLANE
      - P06_STRATEGY_GATE_PLANE
    unlocks:
      - P09_SELF_UPGRADE_PLANE

  P09_SELF_UPGRADE_PLANE:
    depends_on:
      - P08_REVIEW_REPLAY_PLANE
    unlocks:
      - GOVERNED_PARAMETER_UPDATE
```

---

# 13. 阶段执行顺序

文件：

```text
phase_execution_order.yaml
```

## 13.1 标准顺序

```yaml
default_execution_order:
  - step: 0
    plane: P00_FULL_CONTROL_PLANE
    action: 初始化控制上下文

  - step: 1
    plane: P01_GOVERNANCE_PLANE
    action: 验证系统边界和权限

  - step: 2
    plane: P02_DOMAIN_PLANE
    action: 建立领域对象和判断语义

  - step: 3
    plane: P03_DATA_PLANE
    action: 建立数据字段、来源、质量和血缘

  - step: 4
    plane: P04_EVIDENCE_PLANE
    action: 把数据事实转成证据对象

  - step: 5
    plane: P05_SCENARIO_RECOGNITION_PLANE
    action: 识别当前场景候选

  - step: 6
    plane: P06_STRATEGY_GATE_PLANE
    action: 判断是否允许进入策略候选

  - step: 7
    plane: P07_EXECUTION_RISK_PLANE
    action: 执行前风险检查和纸面/确认门控

  - step: 8
    plane: P08_REVIEW_REPLAY_PLANE
    action: 复盘和失败归因

  - step: 9
    plane: P09_SELF_UPGRADE_PLANE
    action: 参数、规则、字段和流程校准
```

---

# 14. 任务树模型

文件：

```text
task_tree_schema.yaml
```

## 14.1 为什么必须有任务树

HER 不能只收到一句：

```text
把系统完善到专业化
```

这样它会随机展开。

Full Control Plane 必须把目标转成任务树：

```text
系统目标
  ↓
阶段目标
  ↓
模块目标
  ↓
文件目标
  ↓
字段目标
  ↓
验收目标
  ↓
状态回写
```

---

## 14.2 任务树结构

```yaml
task_tree:
  task_tree_id: string
  root_goal: string
  target_plane: string
  generated_at: datetime
  control_version: string

  phase_tasks:
    - phase_id: string
      phase_goal: string
      controller_id: string
      required_inputs: list
      required_outputs: list
      subtasks:
        - subtask_id: string
          subtask_name: string
          subtask_type:
            - CONTEXT_BUILD
            - FILE_CREATE
            - SCHEMA_DEFINE
            - CONTRACT_DEFINE
            - VALIDATION
            - AUDIT
            - HANDOFF
          expected_artifacts: list
          acceptance_checks: list
          status:
            - PENDING
            - RUNNING
            - DONE
            - FAILED
            - BLOCKED
            - NEEDS_REWORK

  final_acceptance:
    required_status:
      - PHASE_READY
      - PHASE_READY_WITH_GAPS
    forbidden_status:
      - PHASE_REJECTED
      - PHASE_BLOCKED
```

---

# 15. 阶段任务包合约

文件：

```text
task_package_contract.yaml
```

## 15.1 标准任务包

```yaml
phase_task_package:
  package_id: string
  package_name: string
  target_plane: string
  target_controller: string
  created_at: datetime
  created_by: FULL_CONTROL_PLANE

  input_context:
    user_goal: string
    upstream_handoff_packet: string
    governing_rules: list
    existing_files_to_read: list

  execution_scope:
    must_create_files: list
    must_update_files: list
    must_not_touch_files: list
    allowed_directories: list
    forbidden_directories: list

  task_tree:
    tasks: list

  validation:
    acceptance_gate: string
    required_status_codes: list
    rejection_conditions: list

  output:
    expected_files: list
    expected_handoff_packet: string
    expected_audit_report: string

  recovery:
    on_missing_input: REQUIRE_INPUT_BACKFILL
    on_contract_mismatch: BLOCK_AND_REPORT
    on_acceptance_failure: MARK_NEEDS_REWORK
    on_partial_completion: MARK_READY_WITH_GAPS
```

---

# 16. 合约路由器

文件：

```text
contract_router.yaml
```

## 16.1 作用

Contract Router 负责回答：

```text
当前阶段需要读取哪个合约？
当前阶段应该输出哪个合约？
输出给谁？
如果合约不存在怎么办？
如果合约字段不完整怎么办？
```

## 16.2 路由表

```yaml
contract_routes:
  - route_id: ROUTE_GOVERNANCE_TO_DOMAIN
    from_plane: P01_GOVERNANCE_PLANE
    to_plane: P02_DOMAIN_PLANE
    required_output_contract: governance_handoff_contract.yaml
    required_input_contract: governance_handoff_contract.yaml
    missing_contract_policy: BLOCK_DOMAIN_PLANE

  - route_id: ROUTE_DOMAIN_TO_DATA
    from_plane: P02_DOMAIN_PLANE
    to_plane: P03_DATA_PLANE
    required_output_contract: domain_handoff_contract.yaml
    required_input_contract: data_requirement_from_domain.yaml
    missing_contract_policy: BLOCK_DATA_PLANE

  - route_id: ROUTE_DATA_TO_EVIDENCE
    from_plane: P03_DATA_PLANE
    to_plane: P04_EVIDENCE_PLANE
    required_output_contract: data_handoff_contract.yaml
    required_input_contract: evidence_input_contract.yaml
    missing_contract_policy: BLOCK_EVIDENCE_PLANE
```

---

# 17. 输入合约注册表

文件：

```text
input_contract_registry.yaml
```

```yaml
input_contracts:
  - contract_id: user_goal_contract
    required_by:
      - P00_FULL_CONTROL_PLANE
    required_fields:
      - goal_text
      - target_system
      - desired_level
      - constraints
      - forbidden_actions
    missing_policy: REQUIRE_GOAL_CLARIFICATION_OR_BEST_EFFORT_FORMALIZATION

  - contract_id: governance_handoff_contract
    required_by:
      - P02_DOMAIN_PLANE
    required_fields:
      - system_boundary
      - authority_matrix
      - forbidden_claims
      - risk_red_lines
      - acceptance_policy
    missing_policy: BLOCK_DOMAIN_PLANE

  - contract_id: domain_handoff_contract
    required_by:
      - P03_DATA_PLANE
    required_fields:
      - domain_objects
      - field_requirements
      - evidence_requirements
      - reasoning_boundary
      - hard_negative_rules
    missing_policy: BLOCK_DATA_PLANE
```

---

# 18. 输出合约注册表

文件：

```text
output_contract_registry.yaml
```

```yaml
output_contracts:
  - contract_id: control_handoff_contract
    produced_by: P00_FULL_CONTROL_PLANE
    consumed_by:
      - P01_GOVERNANCE_PLANE
      - ALL_PHASE_CONTROLLERS
    required_sections:
      - target_goal
      - selected_phase
      - task_tree
      - required_inputs
      - expected_outputs
      - acceptance_gate
      - status_writeback

  - contract_id: domain_handoff_contract
    produced_by: P02_DOMAIN_PLANE
    consumed_by:
      - P03_DATA_PLANE
      - P04_EVIDENCE_PLANE
    required_sections:
      - domain_context
      - domain_objects
      - field_requirements
      - evidence_requirements
      - reasoning_boundary
      - downstream_instruction

  - contract_id: data_handoff_contract
    produced_by: P03_DATA_PLANE
    consumed_by:
      - P04_EVIDENCE_PLANE
      - P08_REVIEW_REPLAY_PLANE
    required_sections:
      - source_summary
      - normalized_entities
      - normalized_events
      - snapshots
      - data_quality
      - missing_fields
      - conflict_fields
      - lineage
      - downstream_permission
```

---

# 19. 全局验收门注册表

文件：

```text
acceptance_gate_registry.yaml
```

## 19.1 验收门不是形式检查

验收门必须检查：

```text
文件是否存在
内容是否完整
是否有状态码
是否有输入输出合约
是否有缺口登记
是否有禁止越权
是否能交接下游
是否有审计路径
```

---

## 19.2 验收门结构

```yaml
acceptance_gates:
  - gate_id: GATE_CONTROL_READY
    plane_id: P00_FULL_CONTROL_PLANE
    pass_status:
      - CONTROL_READY
    with_gaps_status:
      - CONTROL_READY_WITH_GAPS
    fail_status:
      - CONTROL_REJECTED
    required_checks:
      - global_plane_registry_exists
      - phase_controller_registry_exists
      - task_tree_schema_exists
      - contract_router_exists
      - acceptance_gate_registry_exists
      - phase_state_machine_exists
      - failure_recovery_policy_exists
      - audit_log_model_exists
      - handoff_packet_registry_exists

  - gate_id: GATE_DOMAIN_READY
    plane_id: P02_DOMAIN_PLANE
    pass_status:
      - DOMAIN_READY
    with_gaps_status:
      - DOMAIN_READY_WITH_GAPS
    fail_status:
      - DOMAIN_REJECTED
    required_checks:
      - domain_objects_defined
      - scenario_taxonomy_defined
      - evidence_model_defined
      - counter_evidence_model_defined
      - reasoning_boundary_defined
      - data_requirement_map_defined
      - domain_handoff_contract_exists

  - gate_id: GATE_DATA_READY
    plane_id: P03_DATA_PLANE
    pass_status:
      - DATA_READY
    with_gaps_status:
      - DATA_READY_WITH_GAPS
    fail_status:
      - DATA_REJECTED
    required_checks:
      - data_source_registry_exists
      - field_dictionary_exists
      - raw_model_exists
      - normalized_model_exists
      - quality_model_exists
      - freshness_model_exists
      - missing_policy_exists
      - conflict_policy_exists
      - lineage_model_exists
      - data_handoff_contract_exists
```

---

# 20. 全局状态码表

文件：

```text
global_status_code_table.yaml
```

## 20.1 状态码分层

```yaml
status_code_groups:
  control_status:
    - CONTROL_UNINITIALIZED
    - CONTROL_CONTEXT_READY
    - CONTROL_READY
    - CONTROL_READY_WITH_GAPS
    - CONTROL_REJECTED

  phase_status:
    - PHASE_NOT_STARTED
    - PHASE_RUNNING
    - PHASE_OUTPUT_GENERATED
    - PHASE_READY
    - PHASE_READY_WITH_GAPS
    - PHASE_REJECTED
    - PHASE_BLOCKED
    - PHASE_NEEDS_REWORK

  contract_status:
    - CONTRACT_READY
    - CONTRACT_MISSING
    - CONTRACT_INCOMPLETE
    - CONTRACT_CONFLICTED
    - CONTRACT_REJECTED

  data_status:
    - DATA_READY
    - DATA_READY_WITH_GAPS
    - DATA_STALE
    - DATA_CONFLICT_DETECTED
    - DATA_REJECTED

  evidence_status:
    - EVIDENCE_READY
    - EVIDENCE_WEAK_ONLY
    - EVIDENCE_CONFLICTED
    - EVIDENCE_REJECTED

  execution_status:
    - PAPER_ONLY
    - HUMAN_CONFIRMATION_REQUIRED
    - EXECUTION_BLOCKED
    - LIVE_EXECUTION_FORBIDDEN
```

---

# 21. 全局硬否定规则

文件：

```text
global_hard_negative_rules.yaml
```

## 21.1 控制面级硬否定

这些规则高于所有阶段。

```yaml
global_hard_negative_rules:
  - rule_id: GHN_001
    name: 阶段越权输出交易信号
    condition: current_plane not in [P06_STRATEGY_GATE_PLANE, P07_EXECUTION_RISK_PLANE] and output_contains_buy_signal == true
    result: PHASE_REJECTED
    reason: 当前阶段没有交易信号权限

  - rule_id: GHN_002
    name: 未通过上游验收却进入下游
    condition: upstream_status not in [PHASE_READY, PHASE_READY_WITH_GAPS] and downstream_started == true
    result: SYSTEM_PAUSED
    reason: 下游执行依赖未满足

  - rule_id: GHN_003
    name: 缺少输入合约仍继续执行
    condition: required_input_contract_missing == true
    result: PHASE_BLOCKED
    reason: 无输入合约不能执行阶段任务

  - rule_id: GHN_004
    name: 输出合约缺失
    condition: required_output_contract_missing == true
    result: PHASE_NEEDS_REWORK
    reason: 无输出合约不能交接下游

  - rule_id: GHN_005
    name: 缺口未登记
    condition: known_gap_exists == true and gap_register_updated == false
    result: PHASE_NEEDS_REWORK
    reason: 已知缺口必须登记

  - rule_id: GHN_006
    name: 直接覆盖 raw 数据
    condition: raw_data_overwrite_detected == true
    result: SYSTEM_PAUSED
    reason: 原始数据不可覆盖

  - rule_id: GHN_007
    name: 实盘执行越权
    condition: live_execution_requested == true and execution_permission != LIVE_ALLOWED_BY_GOVERNANCE
    result: EXECUTION_BLOCKED
    reason: 当前系统阶段不允许自动实盘
```

---

# 22. 阶段状态机

文件：

```text
phase_state_machine.yaml
```

## 22.1 标准状态流

```yaml
phase_state_machine:
  states:
    - PHASE_NOT_STARTED
    - PHASE_INPUT_CHECK
    - PHASE_CONTEXT_LOADED
    - PHASE_TASK_TREE_COMPILED
    - PHASE_EXECUTION_RUNNING
    - PHASE_OUTPUT_GENERATED
    - PHASE_ACCEPTANCE_RUNNING
    - PHASE_READY
    - PHASE_READY_WITH_GAPS
    - PHASE_REJECTED
    - PHASE_NEEDS_REWORK
    - PHASE_BLOCKED
    - HANDOFF_READY

  transitions:
    - from: PHASE_NOT_STARTED
      to: PHASE_INPUT_CHECK
      condition: phase_selected == true

    - from: PHASE_INPUT_CHECK
      to: PHASE_CONTEXT_LOADED
      condition: required_input_contracts_valid == true

    - from: PHASE_CONTEXT_LOADED
      to: PHASE_TASK_TREE_COMPILED
      condition: task_tree_created == true

    - from: PHASE_TASK_TREE_COMPILED
      to: PHASE_EXECUTION_RUNNING
      condition: tasks_ready == true

    - from: PHASE_EXECUTION_RUNNING
      to: PHASE_OUTPUT_GENERATED
      condition: expected_artifacts_created == true

    - from: PHASE_OUTPUT_GENERATED
      to: PHASE_ACCEPTANCE_RUNNING
      condition: acceptance_gate_started == true

    - from: PHASE_ACCEPTANCE_RUNNING
      to: PHASE_READY
      condition: all_required_checks_passed == true

    - from: PHASE_ACCEPTANCE_RUNNING
      to: PHASE_READY_WITH_GAPS
      condition: non_blocking_gaps_exist == true

    - from: PHASE_ACCEPTANCE_RUNNING
      to: PHASE_REJECTED
      condition: blocking_failure_detected == true

    - from: PHASE_READY
      to: HANDOFF_READY
      condition: handoff_packet_generated == true
```

---

# 23. 执行权限矩阵

文件：

```text
execution_permission_matrix.yaml
```

## 23.1 权限矩阵

|Plane|可定义|可判断|可输出|禁止|
|---|---|---|---|---|
|Full Control|阶段、任务、验收、状态|阶段是否可推进|任务包、状态码、交接包|交易信号|
|Governance|权限、红线、禁止事项|是否越权|治理合约|买卖结论|
|Domain|领域对象、场景语义|概念是否成立|领域合约|直接买入|
|Data|数据字段、质量、血缘|数据是否可用|数据合约|推断意图|
|Evidence|证据/反证对象|支持/反驳/未知|证据链|策略执行|
|Scenario|场景分类|当前场景候选|场景状态|自动下单|
|Strategy Gate|策略准入|是否进入候选|PAPER_READY / BLOCK|绕过风控|
|Execution Risk|执行风险|是否允许纸面/确认|执行门控|未授权实盘|
|Review|复盘归因|成败原因|校准建议|实时反向污染|
|Self-Upgrade|参数治理|是否更新规则|升级包|未审计自改|

---

# 24. Skill / Tool 注册表

文件：

```text
skill_tool_registry.yaml
```

## 24.1 作用

让 HER 知道：

```text
哪个任务该调用哪个 Skill
哪个任务该调用哪个脚本
哪个任务只能写文档
哪个任务需要测试
哪个任务需要 replay
```

## 24.2 示例

```yaml
skill_tool_registry:
  - tool_id: HER_FILE_WRITER
    tool_type: HER_INTERNAL
    allowed_planes:
      - P00_FULL_CONTROL_PLANE
      - P01_GOVERNANCE_PLANE
      - P02_DOMAIN_PLANE
      - P03_DATA_PLANE
    allowed_actions:
      - create_markdown
      - create_yaml
      - update_registry
    forbidden_actions:
      - delete_legacy_runtime
      - execute_live_trade

  - tool_id: SIKK_WALLET_STRUCTURE_GATE
    tool_type: PYTHON_MODULE
    path: /root/sikk-gmgn/sikk_wallet_structure_gate.py
    allowed_planes:
      - P04_EVIDENCE_PLANE
      - P05_SCENARIO_RECOGNITION_PLANE
      - P06_STRATEGY_GATE_PLANE
    required_inputs:
      - wallet_structure_decision.json
      - candidate_states.json
    outputs:
      - wallet_gate_status
      - wallet_structure_factor
    forbidden_planes:
      - P02_DOMAIN_PLANE
      - P03_DATA_PLANE

  - tool_id: SIKK_PAPER_LIVE_RUNNER
    tool_type: PYTHON_MODULE
    path: /root/sikk-gmgn/sikk_paper_live_runner.py
    allowed_planes:
      - P07_EXECUTION_RISK_PLANE
      - P08_REVIEW_REPLAY_PLANE
    forbidden_actions:
      - live_trade
```

---

# 25. 数据路径路由器

文件：

```text
data_path_router.yaml
```

## 25.1 作用

解决你之前担心的目录混乱问题。

Full Control Plane 不一定要规定每个微文件放哪里，但必须规定**路径路由原则**。

```yaml
data_path_router:
  canonical_project_root: /root/sikk-gmgn

  system_root:
    path: /root/sikk-gmgn/system
    purpose: 系统设计、阶段控制、合约、规则、上下文

  runtime_data_root:
    path: /root/sikk-gmgn/data
    purpose: 运行数据、标准化数据、快照、报告

  legacy_runtime_root:
    path: /root/sikk-gmgn/data/gmgn_candidates_live_run
    policy: legacy_runtime_keep_in_place
    rule: 保留，不移动，不删除，不作为新写入主路径

  source_wallet_bot_root:
    path: /root/sikk-gmgn/data/source_wallet_bot
    purpose: 钱包事实、GMGN 采集、字段标准化、筹码事实

  intel_bot_root:
    path: /root/sikk-gmgn/data/intel_bot
    purpose: 主导侧行为推断、对手盘、结构结论、解释报告

  full_control_plane_root:
    path: /root/sikk-gmgn/system/full_control_plane
    purpose: 全系统控制面文件

  routing_rules:
    - data_type: raw_wallet_data
      target: /root/sikk-gmgn/data/source_wallet_bot/raw

    - data_type: normalized_wallet_data
      target: /root/sikk-gmgn/data/source_wallet_bot/normalized

    - data_type: behavior_inference
      target: /root/sikk-gmgn/data/intel_bot/behavior_inference

    - data_type: control_contracts
      target: /root/sikk-gmgn/system/full_control_plane

    - data_type: phase_context
      target: /root/sikk-gmgn/system/{plane_name}
```

---

# 26. Handoff Packet 注册表

文件：

```text
handoff_packet_registry.yaml
```

## 26.1 交接包类型

```yaml
handoff_packets:
  - packet_id: control_handoff_packet
    produced_by: P00_FULL_CONTROL_PLANE
    consumed_by:
      - ALL_PHASE_CONTROLLERS
    required_sections:
      - selected_phase
      - phase_goal
      - task_tree
      - required_inputs
      - expected_outputs
      - acceptance_gate
      - status_writeback_path

  - packet_id: governance_handoff_packet
    produced_by: P01_GOVERNANCE_PLANE
    consumed_by:
      - P02_DOMAIN_PLANE
      - P03_DATA_PLANE
      - P06_STRATEGY_GATE_PLANE
    required_sections:
      - authority_matrix
      - forbidden_claims
      - hard_negative_rules
      - system_boundary

  - packet_id: domain_handoff_packet
    produced_by: P02_DOMAIN_PLANE
    consumed_by:
      - P03_DATA_PLANE
      - P04_EVIDENCE_PLANE
    required_sections:
      - domain_objects
      - field_requirements
      - evidence_requirements
      - reasoning_boundary

  - packet_id: data_handoff_packet
    produced_by: P03_DATA_PLANE
    consumed_by:
      - P04_EVIDENCE_PLANE
      - P08_REVIEW_REPLAY_PLANE
    required_sections:
      - normalized_entities
      - normalized_events
      - snapshots
      - data_quality
      - lineage
      - missing_fields
      - conflict_fields
```

---

# 27. 审计日志模型

文件：

```text
audit_log_model.yaml
```

## 27.1 审计日志结构

```yaml
audit_log_record:
  audit_id: string
  timestamp: datetime
  run_id: string
  plane_id: string
  controller_id: string
  task_id: string

  action:
    action_type:
      - PHASE_SELECTED
      - INPUT_VALIDATED
      - FILE_CREATED
      - CONTRACT_GENERATED
      - ACCEPTANCE_CHECKED
      - GAP_REGISTERED
      - STATUS_WRITTEN
      - HANDOFF_CREATED
      - BLOCKED
      - RECOVERY_TRIGGERED
    action_summary: string

  inputs:
    input_contracts: list
    input_files: list
    input_status_codes: list

  outputs:
    output_files: list
    output_contracts: list
    output_status_code: string

  validation:
    acceptance_gate: string
    passed: boolean
    failed_checks: list
    gap_ids: list

  traceability:
    previous_audit_id: string | null
    next_audit_id: string | null
```

---

# 28. 缺口登记模型

文件：

```text
gap_register_model.yaml
```

## 28.1 缺口登记不是备注

缺口必须结构化，否则后续不会被修复。

```yaml
gap_record:
  gap_id: string
  detected_at: datetime
  detected_by_plane: string
  affected_plane: string
  gap_type:
    - MISSING_FILE
    - MISSING_FIELD
    - CONTRACT_INCOMPLETE
    - DATA_SOURCE_UNVERIFIED
    - THRESHOLD_NOT_CALIBRATED
    - TOOL_NOT_IMPLEMENTED
    - TEST_NOT_RUN
    - REPLAY_SAMPLE_INSUFFICIENT
    - GOVERNANCE_UNCLEAR
    - PATH_CONFLICT
  severity:
    - BLOCKING
    - HIGH
    - MEDIUM
    - LOW
  description: string
  impact: string
  required_fix: string
  owner_controller: string
  status:
    - OPEN
    - IN_PROGRESS
    - FIXED
    - ACCEPTED_RISK
    - DEFERRED
  downstream_permission:
    - BLOCK_DOWNSTREAM
    - ALLOW_WITH_GAPS
    - WEAK_EVIDENCE_ONLY
    - OBSERVE_ONLY
```

---

# 29. 失败恢复策略

文件：

```text
failure_recovery_policy.yaml
```

## 29.1 失败分类

|失败类型|处理|
|---|---|
|输入合约缺失|阻断当前阶段，要求补齐|
|输出合约缺失|标记 NEEDS_REWORK|
|文件创建失败|重试一次，仍失败则登记缺口|
|内容不符合验收|标记 REJECTED 或 NEEDS_REWORK|
|上游未完成|暂停下游|
|数据路径冲突|停止写入，要求路径路由|
|legacy 数据混写|阻断并登记|
|工具不可用|降级为设计输出或登记工具缺口|
|测试未运行|不允许标记 READY|
|部分完成|READY_WITH_GAPS，禁止强推进|

## 29.2 恢复策略结构

```yaml
failure_recovery_rules:
  - failure_id: FAIL_MISSING_INPUT_CONTRACT
    condition: required_input_contract_missing == true
    action: BLOCK_PHASE
    required_output:
      - gap_record
      - recovery_instruction
    next_status: PHASE_BLOCKED

  - failure_id: FAIL_ACCEPTANCE_NOT_PASSED
    condition: acceptance_gate_failed == true
    action: MARK_NEEDS_REWORK
    required_output:
      - failed_checks
      - rework_task_list
    next_status: PHASE_NEEDS_REWORK

  - failure_id: FAIL_PARTIAL_COMPLETION
    condition: expected_files_created_partial == true
    action: MARK_READY_WITH_GAPS
    required_output:
      - completed_files
      - missing_files
      - downstream_limitations
    next_status: PHASE_READY_WITH_GAPS
```

---

# 30. Legacy Mapping Policy

文件：

```text
legacy_mapping_policy.yaml
```

## 30.1 目的

你当前系统已经有旧数据目录，例如：

```text
/root/sikk-gmgn/data/gmgn_candidates_live_run/
```

Full Control Plane 必须明确：

```text
旧数据保留
旧数据映射
旧数据吸收
旧数据不混写
旧数据不直接当新标准
```

## 30.2 策略

```yaml
legacy_mapping_policy:
  legacy_roots:
    - path: /root/sikk-gmgn/data/gmgn_candidates_live_run
      status: KEEP_IN_PLACE
      allowed_use:
        - replay_reference
        - historical_runtime_reference
        - migration_source
        - audit_reference
      forbidden_use:
        - new_primary_write_path
        - silent_overwrite
        - direct_schema_authority

  migration_rules:
    - rule_id: LEGACY_001
      name: 旧数据只读扫描
      action: read_only_inventory

    - rule_id: LEGACY_002
      name: 旧数据生成映射表
      action: create_legacy_mapping_index

    - rule_id: LEGACY_003
      name: 旧数据吸收前必须标准化
      action: normalize_before_import

    - rule_id: LEGACY_004
      name: 不允许直接移动旧 runtime
      action: block_move_delete
```

---

# 31. Human Override Policy

文件：

```text
human_override_policy.yaml
```

## 31.1 什么时候允许人工干预

```yaml
human_override_policy:
  allowed_override_cases:
    - governance_rule_update
    - phase_priority_change
    - accepted_risk_marking
    - manual_gap_closure
    - live_execution_approval
    - directory_constitution_change

  forbidden_override_cases:
    - bypass_security_gate
    - bypass_missing_critical_data
    - force_live_trade_without_execution_permission
    - mark_phase_ready_without_acceptance
    - delete_raw_data

  override_record_required:
    - override_id
    - operator
    - timestamp
    - reason
    - affected_plane
    - affected_status
    - risk_acknowledgement
    - rollback_plan
```

---

# 32. HER Full Control 执行协议

文件：

```text
her_full_control_execution_protocol.md
```

## 32.1 HER 执行时必须遵守

```text
1. 先读取 Full Control Plane 的 control_context.md。
2. 再读取 global_plane_registry.yaml。
3. 再读取 phase_controller_registry.yaml。
4. 根据用户目标选择目标 Plane。
5. 检查目标 Plane 的上游依赖是否完成。
6. 检查输入合约是否存在。
7. 编译阶段任务树。
8. 按任务树创建或更新阶段文件。
9. 运行验收门。
10. 写入状态码。
11. 登记缺口。
12. 生成 handoff packet。
13. 输出下一阶段建议。
```

---

## 32.2 HER 不允许做

```text
1. 不允许跳过 Full Control 直接进入代码实现。
2. 不允许文件创建后直接宣称完成。
3. 不允许没有验收门就进入下一阶段。
4. 不允许没有 handoff packet 就交接下游。
5. 不允许把推测当作事实。
6. 不允许把 Data Plane 输出成策略判断。
7. 不允许把 Strategy Gate 输出成执行订单。
8. 不允许删除 legacy runtime 数据。
```

---

# 33. Full Control Plane 的验收标准

文件：

```text
control_acceptance_criteria.md
```

## 33.1 CONTROL_READY

必须满足：

```text
1. full_control_plane.yaml 已完成
2. control_context.md 已完成
3. global_plane_registry.yaml 已完成
4. phase_controller_registry.yaml 已完成
5. phase_dependency_graph.yaml 已完成
6. phase_execution_order.yaml 已完成
7. task_tree_schema.yaml 已完成
8. task_package_contract.yaml 已完成
9. contract_router.yaml 已完成
10. input_contract_registry.yaml 已完成
11. output_contract_registry.yaml 已完成
12. acceptance_gate_registry.yaml 已完成
13. global_status_code_table.yaml 已完成
14. global_hard_negative_rules.yaml 已完成
15. phase_state_machine.yaml 已完成
16. execution_permission_matrix.yaml 已完成
17. skill_tool_registry.yaml 已完成
18. data_path_router.yaml 已完成
19. handoff_packet_registry.yaml 已完成
20. audit_log_model.yaml 已完成
21. gap_register_model.yaml 已完成
22. failure_recovery_policy.yaml 已完成
23. legacy_mapping_policy.yaml 已完成
24. human_override_policy.yaml 已完成
25. her_full_control_execution_protocol.md 已完成
26. 每个阶段都有输入、输出、验收、状态、交接
27. 不存在阶段越权逻辑
28. 不存在跳过验收进入下游的逻辑
29. 不存在自动实盘执行越权
30. 可以生成下一阶段任务包
```

---

## 33.2 CONTROL_READY_WITH_GAPS

允许进入后续建设，但必须登记缺口：

```text
1. 某些 Phase Controller 只有设计，代码未落地
2. 某些验收门尚未自动化，只能人工检查
3. 旧数据映射尚未完成
4. 某些工具注册了但未验证可运行
5. replay 样本不足
6. 状态码尚未接入真实 orchestrator
7. HER 只能按任务包执行，尚未完全自动调度
```

---

## 33.3 CONTROL_REJECTED

以下情况必须驳回：

```text
1. Full Control Plane 只是总说明文档
2. 没有 Phase Controller 注册表
3. 没有任务树模型
4. 没有输入/输出合约
5. 没有验收门
6. 没有状态机
7. 没有失败处理
8. 没有缺口登记
9. 没有审计日志
10. 没有 legacy 策略
11. 阶段可以随意跳转
12. 阶段可以越权输出
13. 未验收也能交接下游
14. HER 无法根据它执行任务
```

---

# 34. 当前是否达到轻量机构级别？

## 34.1 判断

按上面设计，Full Control Plane 可以达到：

```text
轻量机构级 v1.0 控制面标准
```

但它仍不是完整机构级 v2.0。

---

## 34.2 已经达到的部分

|能力|状态|
|---|---|
|全阶段注册|已设计|
|Phase Controller 模型|已设计|
|阶段依赖图|已设计|
|任务树模型|已设计|
|输入/输出合约|已设计|
|合约路由|已设计|
|验收门|已设计|
|全局状态码|已设计|
|硬否定规则|已设计|
|阶段状态机|已设计|
|权限矩阵|已设计|
|路径路由|已设计|
|缺口登记|已设计|
|失败恢复|已设计|
|审计日志|已设计|
|HER 执行协议|已设计|

---

## 34.3 还没达到完整机构级的部分

|缺口|原因|后续补齐方式|
|---|---|---|
|状态机未接真实 orchestrator|当前是设计模型|后续接入 runtime|
|验收门未全部自动化|目前可人工/半自动验收|后续写 validator 脚本|
|Phase Controller 未全部代码化|当前先建立阶段数据|后续逐步实现|
|legacy mapping 未实际扫描|需要 HER 执行目录审计|后续建立 mapping index|
|Skill/tool registry 未真实验证|需要运行检查|后续 tool audit|
|Handoff packet 未真实跑通|需要阶段间联调|后续集成测试|
|状态码未接 Telegram 面板|属于 Ops 层|后续接总控 bot|
|长时间自动执行还需要 harness|需要 HER 任务拆段|后续建立 long-run harness|

结论：

```text
Full Control Plane 当前应该先作为系统总控基座建立。
不要急着把所有 Phase Controller 都写成代码。
先让系统拥有统一的控制秩序、合约秩序、验收秩序和状态秩序。
```

---

# 35. 给 HER 的可执行任务书

下面可以直接复制给 HER。

```text
任务名称：建立 P00 Full Control Plane｜完整控制面专业化阶段数据包

任务目标：
在 /root/sikk-gmgn/system/full_control_plane/ 下建立 SIKK Stable Trader OS 的完整控制面。该阶段不是普通说明文档，不是阶段表，不是 dashboard，也不是单一 Skill，而是全系统最高级的运行控制层。它负责把系统总目标或阶段目标编译成任务树，并绑定到 Phase Controller、输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写、缺口登记、失败处理、审计日志和下游交接包。

核心原则：
1. Full Control Plane 只负责调度、验收、状态回写、阻断和交接，不直接做交易判断。
2. 不允许直接生成买入信号。
3. 不允许直接执行交易。
4. 不允许跳过 Governance Plane。
5. 不允许跳过上游验收进入下游。
6. 不允许没有输入合约就执行阶段。
7. 不允许没有输出合约就交接下游。
8. 不允许把文件创建等同于阶段完成。
9. 不允许删除或移动 legacy runtime 数据。
10. 所有阶段必须有状态码、验收门、缺口登记和 handoff packet。

需要创建目录：
/root/sikk-gmgn/system/full_control_plane/

需要创建文件：
1. full_control_plane.yaml
2. control_context.md
3. global_plane_registry.yaml
4. phase_controller_registry.yaml
5. phase_dependency_graph.yaml
6. phase_execution_order.yaml
7. task_tree_schema.yaml
8. task_package_contract.yaml
9. contract_router.yaml
10. input_contract_registry.yaml
11. output_contract_registry.yaml
12. acceptance_gate_registry.yaml
13. global_status_code_table.yaml
14. global_hard_negative_rules.yaml
15. phase_state_machine.yaml
16. execution_permission_matrix.yaml
17. skill_tool_registry.yaml
18. data_path_router.yaml
19. handoff_packet_registry.yaml
20. audit_log_model.yaml
21. gap_register_model.yaml
22. failure_recovery_policy.yaml
23. legacy_mapping_policy.yaml
24. human_override_policy.yaml
25. control_acceptance_criteria.md
26. control_review_checklist.md
27. her_full_control_execution_protocol.md

每个文件要求：

full_control_plane.yaml：
定义完整控制面的 plane_id、plane_name、version、mission、authority、can_do、cannot_do、upstream_inputs、downstream_outputs、global_status_codes。

control_context.md：
写成 HER 运行前必须读取的控制上下文压缩包。必须说明 Full Control Plane 的定位、边界、运行顺序、禁止事项、验收逻辑和下游交接原则。

global_plane_registry.yaml：
注册所有 Plane，包括 P00_FULL_CONTROL_PLANE、P01_GOVERNANCE_PLANE、P02_DOMAIN_PLANE、P03_DATA_PLANE、P04_EVIDENCE_PLANE、P05_SCENARIO_RECOGNITION_PLANE、P06_STRATEGY_GATE_PLANE、P07_EXECUTION_RISK_PLANE、P08_REVIEW_REPLAY_PLANE、P09_SELF_UPGRADE_PLANE。每个 Plane 必须包含 responsibility、input_contracts、output_contracts、forbidden_outputs。

phase_controller_registry.yaml：
为每个 Plane 注册 Phase Controller。每个 Controller 必须包含 controller_id、plane_id、responsibility、input_required、output_required、acceptance_gate、downstream。

phase_dependency_graph.yaml：
定义各阶段依赖关系。必须防止未通过上游验收直接进入下游。

phase_execution_order.yaml：
定义默认执行顺序：Full Control → Governance → Domain → Data → Evidence → Scenario → Strategy Gate → Execution Risk → Review / Replay → Self-Upgrade。
