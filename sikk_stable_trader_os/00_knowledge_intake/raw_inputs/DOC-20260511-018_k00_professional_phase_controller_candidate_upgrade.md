下面按 **K00 阶段专业化升级版** 输出。这里的核心升级是：

```text
K00 不再只是“知识摄取 / 文档建档”阶段。
K00 升级为：

知识摄取
  +
知识资产化
  +
方法论要求抽取
  +
Phase Controller 候选任务化
  +
K00 → P00 系统建造交接
```

但边界必须保持：

```text
K00 只生成候选规格。
P00 才负责正式注册、接入控制平面、生成正式 Phase Controller。
```

---

# K00 阶段专业化定义 v2.0

建议文件名：

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/context.md
```

---

````markdown
# K00 知识摄取与 Phase Controller 候选任务化阶段

文件编号：K00-CONTEXT-002  
阶段编号：K00_knowledge_intake_taskization  
阶段名称：知识摄取与 Phase Controller 候选任务化  
版本：v2.0-light-institutional  
状态：REQUIRED_BEFORE_P00  
适用系统：SIKK Stable Trader OS  
安全边界：paper-only，禁止真实交易  
下游阶段：P00_system_bootstrap_controller  

---

## 1. 阶段定位

K00 不是普通文档读取阶段。

K00 是 SIKK Stable Trader OS 的知识入口、资产化入口、方法论抽取入口和 Phase Controller 候选任务化入口。

K00 的核心职责是：

1. 接收用户输入、文档、旧系统资料、方法论文本、交易逻辑、系统设计。
2. 将输入资料保存为知识资产。
3. 为每份资产生成 passport、索引、摘要、主题标签和缺口报告。
4. 从资料中抽取系统目标、阶段目标、任务结构、输入输出要求、验收要求、状态回写要求和下游交接关系。
5. 将这些内容整理成 `Phase Controller Candidate Spec`。
6. 将候选规格交给 P00 系统建造控制器。
7. 由 P00 决定是否正式注册为 Phase Controller、是否写入 phase registry、是否接入 control plane。

K00 不直接运行交易系统，不直接裁决阶段状态，不直接注册正式 Phase Controller，不直接进入 P01-P10 业务阶段。

---

## 2. Phase Controller 核心定义

Phase Controller 不是阶段说明文档。

Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。

它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

在 SIKK Stable Trader OS 中，任何阶段如果只是说明“这个阶段做什么”，但没有绑定输入、输出、任务树、验收门、状态回写和 handoff packet，都不能被视为真正的 Phase Controller。

---

## 3. K00 对 Phase Controller 的职责边界

K00 的职责不是正式创建 Phase Controller。

K00 的职责是把输入资料转化为 Phase Controller 的候选构建材料。

边界如下：

| 项目 | K00 权限 | P00 权限 |
|---|---|---|
| 保存输入资料 | 负责 | 读取 |
| 生成 document passport | 负责 | 读取 |
| 抽取系统目标 | 负责 | 审核 |
| 抽取阶段目标 | 负责 | 编译 |
| 生成任务树候选 | 负责 | 规范化 |
| 生成输入合约候选 | 负责 | 正式落盘 |
| 生成输出合约候选 | 负责 | 正式落盘 |
| 识别 Atomic Skill 需求 | 负责 | 注册 / 绑定 |
| 识别代码工具需求 | 负责 | runner 绑定 |
| 生成验收门候选 | 负责 | 正式绑定 |
| 生成状态回写候选 | 负责 | 接入 control plane |
| 生成 handoff 候选 | 负责 | 正式接入 handoff registry |
| 创建正式 controller.yaml | 不负责 | 负责 |
| 写入 phase_registry.yaml | 不负责 | 负责 |
| 裁决下一合法阶段 | 只能建议 | 负责 |
| 启动 P01-P10 | 不允许 | 按控制平面裁决 |

---

## 4. K00 阶段目标

K00 的阶段目标是：

> 将任何输入资料从“可读文本”转化为“可被系统建造层消费的结构化候选资产”。

具体来说，K00 必须把资料转成以下系统材料：

1. 知识资产。
2. 文档 passport。
3. 方法论要求索引。
4. 领域对象候选。
5. 阶段目标候选。
6. 任务树候选。
7. 输入合约候选。
8. 输出合约候选。
9. Atomic Skill 候选。
10. 代码工具 / runner 候选。
11. 验收门候选。
12. 状态回写候选。
13. 下游 handoff 候选。
14. blocking gaps。
15. non-blocking gaps。
16. K00 → P00 handoff packet。

---

## 5. K00 不负责什么

K00 不负责：

1. 不直接建立正式 Phase Controller。
2. 不直接生成正式 phase registry。
3. 不直接生成正式 current system state。
4. 不直接裁决 P01 可以启动。
5. 不直接执行交易系统。
6. 不判断 token 是否可以买。
7. 不判断钱包是否一定属于主导侧。
8. 不生成真实交易指令。
9. 不绕过 P00。
10. 不把文档存在当成系统消费完成。

---

## 6. K00 核心问题树

K00 处理任何资料时，必须回答以下问题：

### 6.1 资料识别问题

1. 这份资料是什么类型？
2. 它属于系统方法论、治理、领域、数据、控制、阶段、runner、验收、复盘还是升级？
3. 它是否是旧系统资料？
4. 它是否包含可复用规则？
5. 它是否包含字段、文件、命令、阶段、判断逻辑或验收标准？

### 6.2 系统目标抽取问题

1. 资料中是否包含系统总目标？
2. 是否包含阶段目标？
3. 是否包含业务目标？
4. 是否包含安全边界？
5. 是否包含“禁止事项”？
6. 是否包含系统缺口？

### 6.3 Phase Controller 候选问题

1. 这份资料是否应该生成一个新的 Phase Controller 候选？
2. 它应该归属于已有阶段，还是建议新增阶段？
3. 它的阶段目标是什么？
4. 它的任务树是什么？
5. 它需要哪些输入？
6. 它必须输出什么？
7. 它需要哪些 Atomic Skill？
8. 它需要哪些代码工具或 runner？
9. 它的验收门是什么？
10. 它失败时如何处理？
11. 它如何写回状态？
12. 它应该交给哪个下游阶段？

### 6.4 缺口识别问题

1. 是否缺少数据来源？
2. 是否缺少字段定义？
3. 是否缺少输入合约？
4. 是否缺少输出合约？
5. 是否缺少验收标准？
6. 是否缺少 runner？
7. 是否缺少下游消费者？
8. 是否存在状态分裂？
9. 是否存在“文档已存在但系统未消费”？
10. 是否存在“任务包存在但未执行”？

---

## 7. K00 输入标准

K00 可以接收以下输入：

```yaml
allowed_inputs:
  - user_text_goal
  - uploaded_document
  - old_system_file
  - method_wheel_text
  - trading_logic_note
  - wallet_structure_note
  - market_structure_note
  - governance_rule_note
  - data_schema_note
  - phase_design_note
  - runner_design_note
  - acceptance_rule_note
````

禁止输入：

```yaml
forbidden_inputs:
  - real_trade_execution_instruction
  - private_key
  - seed_phrase
  - unverified_live_trade_signal
  - direct_buy_sell_order
```

---

## 8. K00 输出标准

K00 必须输出以下文件类型：

```yaml
required_outputs:
  - raw_input_copy
  - document_passport
  - knowledge_asset_index_entry
  - methodology_requirement_extract
  - phase_goal_candidate
  - task_tree_candidate
  - input_contract_candidate
  - output_contract_candidate
  - atomic_skill_candidate
  - tool_binding_candidate
  - acceptance_gate_candidate
  - state_writeback_candidate
  - handoff_packet_candidate
  - phase_controller_candidate_spec
  - gap_report
  - k00_to_p00_handoff_packet
```

---

## 9. K00 标准处理流程

K00 必须按照以下顺序执行：

```text
Step 1：保存输入资料
Step 2：生成资料 passport
Step 3：判断资料类型
Step 4：抽取系统目标
Step 5：抽取阶段目标
Step 6：抽取任务树
Step 7：抽取输入要求
Step 8：抽取输出要求
Step 9：抽取 Atomic Skill 需求
Step 10：抽取代码工具 / runner 需求
Step 11：抽取验收门
Step 12：抽取状态回写要求
Step 13：抽取下游 handoff 对象
Step 14：识别 blocking gaps
Step 15：识别 non-blocking gaps
Step 16：生成 Phase Controller Candidate Spec
Step 17：生成 K00 → P00 handoff packet
Step 18：更新知识资产索引
Step 19：写入 K00 runtime state
Step 20：等待 P00 消费
```

---

## 10. Phase Controller Candidate Spec 标准

K00 必须生成以下候选规格文件：

```text
00_knowledge_intake/phase_controller_candidates/<asset_id>_phase_controller_candidate_spec.yaml
```

候选规格不是正式 Phase Controller。

它只能作为 P00 编译输入。

---

## 11. K00 验收标准

K00 阶段完成必须满足：

1. 输入资料已保存。
2. document passport 已生成。
3. 资料类型已识别。
4. 系统目标已抽取。
5. 阶段目标候选已抽取。
6. 任务树候选已生成。
7. 输入合约候选已生成。
8. 输出合约候选已生成。
9. Atomic Skill 需求已识别。
10. 代码工具 / runner 需求已识别。
11. 验收门候选已生成。
12. 状态回写候选已生成。
13. 下游 handoff 候选已生成。
14. gap report 已生成。
15. phase_controller_candidate_spec 已生成。
16. k00_to_p00_handoff_packet 已生成。
17. K00 输出没有越权注册正式 Phase Controller。
18. P00 被标记为下游消费者。
19. paper_only=true。
20. real_trade_enabled=false。

---

## 12. K00 阻断条件

出现以下情况，K00 不得标记为完成：

1. 输入资料未保存。
2. document passport 缺失。
3. 无法确定资料类型。
4. 无法抽取任何系统目标。
5. 无法判断下游阶段。
6. phase_controller_candidate_spec 缺失。
7. handoff packet 缺失。
8. 验收门候选缺失。
9. 输出文件不可解析。
10. K00 尝试直接注册 Phase Controller。
11. K00 尝试直接启动 P01。
12. K00 尝试进入真实交易。

---

## 13. K00 输出状态

K00 合法输出状态包括：

```yaml
valid_status:
  - INPUT_RECEIVED
  - ASSET_SAVED
  - PASSPORT_CREATED
  - REQUIREMENTS_EXTRACTED
  - PHASE_CONTROLLER_CANDIDATE_CREATED
  - HANDOFF_TO_P00_READY
  - WAITING_P00_CONSUMPTION
  - BLOCKED_BY_MISSING_INPUT
  - BLOCKED_BY_INVALID_OUTPUT
  - BLOCKED_BY_NO_DOWNSTREAM_TARGET
```

K00 不能输出：

```yaml
invalid_status:
  - P01_READY
  - SYSTEM_READY
  - TRADE_READY
  - REAL_TRADE_ENABLED
  - PHASE_CONTROLLER_REGISTERED
```

---

## 14. K00 与系统完整链路

K00 在系统中的位置：

```text
用户输入 / 文档 / 旧系统资料
  ↓
K00：知识摄取与 Phase Controller 候选任务化
  ↓
phase_controller_candidate_spec.yaml
  ↓
k00_to_p00_handoff_packet.json
  ↓
P00：系统建造与方法论编译
  ↓
正式 Phase Controller
  ↓
phase_registry.yaml
  ↓
current_system_state.json
  ↓
Data Plane / Control Plane
  ↓
P01-P10 业务阶段
```

---

## 15. K00 最终判断原则

K00 的最终判断不是：

```text
这份资料我读完了。
```

而是：

```text
这份资料是否已经被转化为可被 P00 编译的系统建造材料？
```

K00 的成功标准不是摘要质量，而是：

```text
资料是否具备进入系统体系的结构化入口。
```

````

---

# K00 controller.yaml 专业化版本

建议保存为：

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/controller.yaml
````

```yaml
controller_id: K00_knowledge_intake_taskization
controller_name_cn: 知识摄取与 Phase Controller 候选任务化控制器
version: v2.0-light-institutional
status: REQUIRED_BEFORE_P00
controller_type: knowledge_assetization_and_phase_controller_candidate_extraction

authority_scope:
  can:
    - 保存输入资料
    - 生成 document passport
    - 抽取方法论要求
    - 抽取系统目标
    - 抽取阶段目标候选
    - 生成任务树候选
    - 生成输入合约候选
    - 生成输出合约候选
    - 识别 Atomic Skill 需求
    - 识别代码工具需求
    - 生成验收门候选
    - 生成状态回写候选
    - 生成下游 handoff 候选
    - 生成 phase_controller_candidate_spec
    - 生成 k00_to_p00_handoff_packet

  cannot:
    - 正式注册 Phase Controller
    - 写入正式 phase_registry
    - 裁决 P01 可以运行
    - 启动 P01-P10 业务阶段
    - 执行交易
    - 修改真实交易系统
    - 生成真实买卖指令
    - 绕过 P00_system_bootstrap_controller

primary_goal: >
  将输入资料从普通文本或文件转化为可被 P00 系统建造控制器消费的结构化候选资产，
  包括系统目标、阶段目标、任务树、输入合约、输出合约、Atomic Skill 需求、
  工具绑定需求、验收门、状态回写和下游 handoff。

non_goals:
  - 不直接运行交易系统
  - 不直接生成交易判断
  - 不直接注册正式阶段控制器
  - 不直接进入 P01 数据事实层
  - 不以文件存在代表系统接入完成

upstream_dependencies:
  - user_input
  - uploaded_documents
  - existing_project_files
  - methodology_notes
  - old_system_assets

downstream_consumers:
  - P00_system_bootstrap_controller
  - 00_methodology
  - 00_governance
  - 00_domain
  - 00_data
  - 00_control
  - 00_trace

required_inputs:
  - input_asset
  - source_metadata

optional_inputs:
  - user_goal
  - target_stage_hint
  - existing_system_context
  - related_file_paths

forbidden_inputs:
  - private_key
  - seed_phrase
  - direct_real_trade_instruction
  - unverified_live_buy_signal

core_objects:
  - knowledge_asset
  - document_passport
  - methodology_requirement
  - phase_goal_candidate
  - task_tree_candidate
  - input_contract_candidate
  - output_contract_candidate
  - atomic_skill_candidate
  - tool_binding_candidate
  - acceptance_gate_candidate
  - state_writeback_candidate
  - handoff_packet_candidate
  - phase_controller_candidate_spec

processing_steps:
  - step_id: K00_STEP_01
    name_cn: 保存输入资料
    output: raw_input_copy

  - step_id: K00_STEP_02
    name_cn: 生成文档护照
    output: document_passport

  - step_id: K00_STEP_03
    name_cn: 识别资料类型
    output: asset_type_classification

  - step_id: K00_STEP_04
    name_cn: 抽取方法论要求
    output: methodology_requirement_extract

  - step_id: K00_STEP_05
    name_cn: 抽取系统目标
    output: system_goal_extract

  - step_id: K00_STEP_06
    name_cn: 抽取阶段目标候选
    output: phase_goal_candidate

  - step_id: K00_STEP_07
    name_cn: 生成任务树候选
    output: task_tree_candidate

  - step_id: K00_STEP_08
    name_cn: 生成输入输出合约候选
    output: input_output_contract_candidates

  - step_id: K00_STEP_09
    name_cn: 识别 Atomic Skill 与工具绑定需求
    output: skill_and_tool_binding_candidates

  - step_id: K00_STEP_10
    name_cn: 生成验收门候选
    output: acceptance_gate_candidate

  - step_id: K00_STEP_11
    name_cn: 生成状态回写候选
    output: state_writeback_candidate

  - step_id: K00_STEP_12
    name_cn: 生成下游交接候选
    output: handoff_packet_candidate

  - step_id: K00_STEP_13
    name_cn: 识别缺口
    output: gap_report

  - step_id: K00_STEP_14
    name_cn: 生成 Phase Controller 候选规格
    output: phase_controller_candidate_spec

  - step_id: K00_STEP_15
    name_cn: 生成 K00 到 P00 交接包
    output: k00_to_p00_handoff_packet

required_outputs:
  - raw_input_copy
  - document_passport
  - knowledge_asset_index_entry
  - methodology_requirement_extract
  - phase_controller_candidate_spec
  - task_tree_candidate
  - input_output_contract_candidates
  - acceptance_gate_candidate
  - gap_report
  - k00_to_p00_handoff_packet

output_paths:
  raw_inputs: 00_knowledge_intake/raw_inputs/
  passports: 00_knowledge_intake/passports/
  methodology_extracts: 00_knowledge_intake/methodology_extracts/
  phase_controller_candidates: 00_knowledge_intake/phase_controller_candidates/
  task_packages: 00_knowledge_intake/task_packages/
  gap_reports: 00_knowledge_intake/gap_reports/
  handoff_packets: 00_knowledge_intake/handoff_packets/
  intake_reports: 00_knowledge_intake/intake_reports/

acceptance_gate:
  file_level:
    - raw_input_copy_exists
    - document_passport_exists
    - phase_controller_candidate_spec_exists
    - k00_to_p00_handoff_packet_exists

  structure_level:
    - candidate_spec_has_phase_goal
    - candidate_spec_has_task_tree
    - candidate_spec_has_input_contract
    - candidate_spec_has_output_contract
    - candidate_spec_has_acceptance_gate
    - candidate_spec_has_state_writeback
    - candidate_spec_has_downstream_handoff

  semantic_level:
    - system_goal_extracted
    - phase_goal_extracted
    - authority_boundary_defined
    - non_goals_defined
    - blocking_gaps_identified
    - downstream_consumer_identified

  consumption_level:
    - handoff_target_is_P00
    - candidate_status_is_READY_FOR_P00_COMPILATION
    - registration_status_is_NOT_REGISTERED

  safety_level:
    - paper_only_true
    - real_trade_enabled_false
    - no_private_key_stored
    - no_real_trade_instruction_executed

blocking_conditions:
  - input_not_saved
  - passport_missing
  - asset_type_unknown
  - no_system_goal_extracted
  - no_phase_goal_candidate
  - no_acceptance_gate_candidate
  - no_downstream_handoff
  - candidate_spec_invalid
  - k00_attempted_formal_registration
  - p01_marked_ready_without_p00
  - real_trade_instruction_detected

state_writeback:
  required: true
  allowed_targets:
    - 00_knowledge_intake/runtime/k00_runtime_state.json
    - 00_knowledge_intake/index/knowledge_asset_index.json
    - 00_knowledge_intake/handoff_packets/
  forbidden_targets:
    - 00_control/current_system_state.json
    - 00_control/phase_registry.yaml
    - real_trade_runtime_state

handoff:
  source_stage: K00_knowledge_intake_taskization
  target_stage: P00_system_bootstrap_controller
  handoff_packet_required: true
  handoff_status_after_success: HANDOFF_TO_P00_READY

security_policy:
  paper_only: true
  real_trade_enabled: false
  private_key_allowed: false
  seed_phrase_allowed: false
  auto_order_allowed: false
```

---

# Phase Controller Candidate Spec 模板

建议保存为：

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/phase_controller_candidates/phase_controller_candidate_spec.template.yaml
```

```yaml
candidate_id: ""
source_asset_id: ""
source_file_path: ""
source_asset_type: ""
created_by_stage: "K00_knowledge_intake_taskization"
target_compiler_stage: "P00_system_bootstrap_controller"
created_at: ""

phase_controller_candidate:
  proposed_phase_id: ""
  proposed_phase_name_cn: ""
  proposed_phase_type: ""
  proposed_status: "CANDIDATE_ONLY"
  proposed_authority_scope: ""
  proposed_primary_goal: ""
  proposed_non_goals: []

system_goal_decomposition:
  system_goal: ""
  phase_goal: ""
  sub_goals: []
  decision_questions: []
  expected_system_effect: ""

task_tree_candidate:
  root_task: ""
  task_nodes:
    - task_id: ""
      task_name_cn: ""
      task_type: ""
      description: ""
      required_inputs: []
      required_outputs: []
      depends_on: []
      acceptance_gate: []
      failure_policy: ""
      downstream_handoff: ""

input_contract_candidate:
  required_inputs: []
  optional_inputs: []
  forbidden_inputs: []
  missing_input_policy: ""
  source_requirements: []

output_contract_candidate:
  required_outputs: []
  optional_outputs: []
  output_format_requirements: []
  schema_required: true
  validation_rules: []

atomic_skill_requirements:
  required_atomic_skills:
    - skill_name_candidate: ""
      skill_purpose: ""
      input_needed: []
      output_expected: []
      can_be_stub: true
      required_for_v1: false

tool_binding_requirements:
  code_tools_needed: []
  runner_needed: false
  cli_needed: false
  validation_tool_needed: true
  replay_needed: false

acceptance_gate_candidate:
  file_level_acceptance: []
  structure_level_acceptance: []
  semantic_level_acceptance: []
  consumption_level_acceptance: []
  runtime_level_acceptance: []
  blocking_conditions: []

state_writeback_candidate:
  required: true
  writeback_targets:
    - "00_knowledge_intake/runtime/k00_runtime_state.json"
    - "00_knowledge_intake/index/knowledge_asset_index.json"
  forbidden_writeback_targets:
    - "00_control/current_system_state.json"
    - "00_control/phase_registry.yaml"

handoff_packet_candidate:
  source_stage: "K00_knowledge_intake_taskization"
  target_stage: "P00_system_bootstrap_controller"
  required_handoff_fields:
    - handoff_id
    - source_asset_id
    - extracted_requirements
    - phase_controller_candidate
    - known_gaps
    - blocking_gaps
    - non_blocking_gaps
    - next_recommended_stage

evidence_and_contradiction_requirements:
  field_source_required: true
  evidence_level_required: true
  contradiction_record_required: true
  failure_policy_required: true
  review_path_required: true

gap_assessment:
  blocking_gaps: []
  non_blocking_gaps: []
  unresolved_questions: []
  p00_review_required: true

status:
  candidate_status: "READY_FOR_P00_COMPILATION"
  registration_status: "NOT_REGISTERED"
  runner_binding_status: "NOT_BOUND"
  downstream_consumption_status: "WAITING_P00"
  paper_only: true
  real_trade_enabled: false
```

---

# K00 → P00 Handoff Packet 模板

建议保存为：

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/handoff_packets/k00_to_p00_handoff_packet.template.json
```

```json
{
  "handoff_id": "",
  "source_stage": "K00_knowledge_intake_taskization",
  "target_stage": "P00_system_bootstrap_controller",
  "source_asset_id": "",
  "source_file_path": "",
  "handoff_type": "phase_controller_candidate_compilation",

  "included_assets": {
    "raw_input_copy": "",
    "document_passport": "",
    "methodology_requirement_extract": "",
    "phase_controller_candidate_spec": "",
    "gap_report": ""
  },

  "extracted_requirements": {
    "system_goal": "",
    "phase_goal_candidates": [],
    "task_tree_candidates": [],
    "input_contract_candidates": [],
    "output_contract_candidates": [],
    "atomic_skill_candidates": [],
    "tool_binding_candidates": [],
    "acceptance_gate_candidates": [],
    "state_writeback_candidates": [],
    "handoff_candidates": []
  },

  "known_gaps": [],
  "blocking_gaps": [],
  "non_blocking_gaps": [],

  "k00_decision": {
    "assetization_status": "COMPLETED",
    "phase_controller_candidate_created": true,
    "ready_for_p00_compilation": true,
    "formal_registration_allowed_by_k00": false
  },

  "required_p00_actions": [
    "review_phase_controller_candidate_spec",
    "validate_authority_boundary",
    "decide_existing_phase_or_new_phase",
    "compile_formal_controller_yaml_if_approved",
    "register_in_phase_registry_if_approved",
    "update_current_system_state_if_approved",
    "write_consumption_log"
  ],

  "next_recommended_stage": "P00_system_bootstrap_controller",

  "safety_boundary": {
    "paper_only": true,
    "real_trade_enabled": false,
    "private_key_included": false,
    "seed_phrase_included": false,
    "auto_order_allowed": false
  },

  "consumption_status": {
    "consumed_by_p00": false,
    "consumed_at": null,
    "p00_decision": "PENDING"
  }
}
```

---

# K00 专业化后的系统位置

更新后的体系链路应该固定为：

```text
输入资料 / 用户目标 / 旧系统文件 / 方法论文本
  ↓
K00：知识摄取与 Phase Controller 候选任务化
  ↓
phase_controller_candidate_spec.yaml
  ↓
k00_to_p00_handoff_packet.json
  ↓
P00：系统建造与方法论编译
  ↓
正式 controller.yaml
  ↓
phase_registry.yaml
  ↓
current_system_state.json
  ↓
governance / domain / data / control / trace
  ↓
P01-P10 可调度运行
```

---

# 这版 K00 解决的问题

这次升级后，K00 不再只是：

```text
文档保存
摘要生成
任务包生成
```

而是变成：

```text
文档保存
  ↓
系统目标抽取
  ↓
阶段目标抽取
  ↓
任务树抽取
  ↓
输入输出合约候选生成
  ↓
Atomic Skill / 工具需求识别
  ↓
验收门候选生成
  ↓
状态回写候选生成
  ↓
handoff 候选生成
  ↓
Phase Controller 候选规格生成
  ↓
交给 P00 正式编译
```

这就解决了你之前最关键的问题：

```text
文档进来了，但没有真正进入系统体系。
```

更新后变成：

```text
文档进来后，必须被任务化成可被 P00 编译的 Phase Controller 候选材料。
```

---

# 给 HER 的执行任务书

下面这段可以直接发给 HER：

```text
任务名称：
K00_PROFESSIONAL_PHASE_CONTROLLER_CANDIDATE_UPGRADE

任务类型：
K00 阶段专业化升级任务。
不是交易功能开发。
不是 P01 数据事实运行。
不是真实交易任务。

目标：
将 K00 从“知识摄取与文档资产化阶段”升级为“知识摄取 + 方法论抽取 + Phase Controller 候选任务化阶段”。

核心认知：
Phase Controller 不是阶段说明文档。
Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。
它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

K00 的新职责：
1. 保存输入资料。
2. 生成 document passport。
3. 抽取系统目标。
4. 抽取阶段目标候选。
5. 生成任务树候选。
6. 生成输入合约候选。
7. 生成输出合约候选。
8. 识别 Atomic Skill 需求。
9. 识别代码工具 / runner 需求。
10. 生成验收门候选。
11. 生成状态回写候选。
12. 生成下游 handoff 候选。
13. 生成 phase_controller_candidate_spec。
14. 生成 k00_to_p00_handoff_packet。
15. 等待 P00 消费。

K00 禁止事项：
1. 禁止直接注册正式 Phase Controller。
2. 禁止直接写入正式 phase_registry。
3. 禁止直接裁决 P01 可以运行。
4. 禁止启动 P01-P10。
5. 禁止执行真实交易。
6. 禁止把候选规格当作正式控制器。
7. 禁止把文件存在当作系统消费完成。

必须创建或更新的文件：
1. /root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/context.md
2. /root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/controller.yaml
3. /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/phase_controller_candidates/phase_controller_candidate_spec.template.yaml
4. /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/handoff_packets/k00_to_p00_handoff_packet.template.json

如果目录不存在，必须创建：
- /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/phase_controller_candidates/
- /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/handoff_packets/
- /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/runtime/
- /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/index/

验收标准：
1. context.md 已明确 K00 新定位。
2. context.md 已包含 Phase Controller 核心定义。
3. controller.yaml 已定义 K00 权限边界。
4. controller.yaml 已明确 K00 不能正式注册 Phase Controller。
5. controller.yaml 已包含 required_outputs。
6. controller.yaml 已包含 acceptance_gate。
7. controller.yaml 已包含 blocking_conditions。
8. phase_controller_candidate_spec.template.yaml 已创建。
9. k00_to_p00_handoff_packet.template.json 已创建。
10. 所有 YAML / JSON 可解析。
11. K00 输出状态不能包含 P01_READY。
12. K00 handoff target 必须是 P00_system_bootstrap_controller。
13. paper_only=true。
14. real_trade_enabled=false。

最终输出：
1. 修改文件清单。
2. 新增文件清单。
3. K00 新职责摘要。
4. K00 / P00 权限边界。
5. 当前是否允许进入 P01：必须回答否。
6. 下一合法阶段：P00_system_bootstrap_controller。
```

---

# 最终结论

这版 K00 的专业化标准是：

```text
K00 不再只是“读文档”。
K00 是把输入资料转化为系统建造材料的入口。
```

它的核心产物不再只是摘要和任务包，而是：

```text
phase_controller_candidate_spec
+
k00_to_p00_handoff_packet
```

这样后续 P00 才能真正把资料编译进：

```text
governance plane
domain plane
data plane
control plane
phase registry
phase controller
trace matrix
acceptance gate
```

当前阶段完成后，**仍然不能进入 P01**。

下一合法阶段是：

```text
P00_system_bootstrap_controller
```