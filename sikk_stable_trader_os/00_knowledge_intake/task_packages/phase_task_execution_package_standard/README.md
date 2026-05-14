# Phase Task Execution Package Standard

## 7. 阶段任务执行包标准

每一个 Phase Controller 都必须是一个阶段任务执行包，不是单个说明文档。

标准结构：

```text
PXX_phase_name/
  01_phase_manifest.yaml
  02_phase_context_pack.md
  03_phase_objective_tree.yaml
  04_phase_input_contract.json
  05_phase_output_contract.json
  06_phase_execution_protocol.md
  07_phase_acceptance_gate.yaml
  08_phase_state.json
  09_phase_handoff_packet.schema.json
```

### 文件职责

- `01_phase_manifest.yaml`: 阶段身份证，定义阶段是谁、负责什么、权限边界是什么。
- `02_phase_context_pack.md`: 阶段上下文包，定义背景、边界、术语、已知输入、依赖与风险。
- `03_phase_objective_tree.yaml`: 阶段目标树，定义系统目标到阶段目标、任务节点、完成标准的拆解。
- `04_phase_input_contract.json`: 输入合约，定义阶段允许读取、必须读取、禁止依赖的输入。
- `05_phase_output_contract.json`: 输出合约，定义阶段必须产出的结构化资产。
- `06_phase_execution_protocol.md`: 执行协议，定义执行顺序、工具调用、失败处理、恢复路径。
- `07_phase_acceptance_gate.yaml`: 验收门，定义完成判断、阻断条件、降级条件与复核规则。
- `08_phase_state.json`: 阶段状态，记录运行状态、当前步、输出路径、错误、重试与下游许可。
- `09_phase_handoff_packet.schema.json`: 下游交接包 schema，定义交给下一阶段的最小必要信息。

## 7.1 01_phase_manifest.yaml

作用：

定义这个阶段是谁、负责什么、权限边界是什么。这是阶段身份证。

示例：

```yaml
phase_manifest:
  phase_id: "K00"
  phase_key: "K00_knowledge_intake_taskization"
  phase_name: "知识资料摄取与任务化控制器"
  phase_type: "pre_phase_controller"
  mission:
    primary: "将用户输入的文档、知识资料、方法论文本转化为 HER 可执行的阶段任务执行包"
    secondary:
      - "保存原始资料"
      - "生成文档护照"
      - "建立语料索引"
      - "映射系统平面"
      - "识别系统缺口"
      - "生成任务执行包"
      - "输出 handoff_packet"
  authority:
    can_do:
      - "读取用户输入资料"
      - "保存资料"
      - "生成资料登记"
      - "建立任务包"
      - "识别系统影响"
      - "生成下一阶段建议"
    cannot_do:
      - "不能直接输出交易判断"
      - "不能直接改写实时规则"
      - "不能跳过 P00"
      - "不能把资料当普通文档总结后结束"
      - "不能依赖聊天上下文作为唯一依据"
  upstream:
    required:
      - "user_input"
    optional:
      - "uploaded_files"
      - "previous_system_docs"
      - "legacy_runtime_outputs"
  downstream:
    next_phase_candidates:
      - "P00_system_boundary"
      - "P01_data_fact"
      - "P09_self_upgrade"
    handoff_required: true
```


## 7.2 02_phase_context_pack.md

作用：

这不是普通说明。这是给 HER 的阶段上下文压缩包。HER 运行时必须先读它，避免把该阶段误做成普通总结或策略判断。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/02_phase_context_pack_TEMPLATE.md`

K00 标准 Context Pack 必须包含四个一级判断块：

1. 本阶段为什么存在
2. 本阶段不做什么
3. 本阶段必须做什么
4. 本阶段完成标准

完成标准硬门槛：只有当原始资料、文档护照、系统映射、缺口列表、任务执行包、handoff_packet 全部生成后，本阶段才能进入 PHASE_READY。

## 7.3 03_phase_objective_tree.yaml

作用：

让 HER 知道目标层级。比 Markdown 模板专业，因为它能让 HER 按任务树推进，而不是自由发挥。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/03_phase_objective_tree_TEMPLATE.yaml`

K00 标准 Objective Tree 必须包含：

- `objective_tree.phase_id`：阶段编号。
- `level_1_goal`：本阶段一级目标。
- `level_2_sub_goals`：必需子目标清单。
- `level_3_tasks`：可执行任务节点，必须通过 `parent` 绑定到 level_2_sub_goals。
- 每个任务必须声明 `action` 与 `output`，让 HER 按任务树推进并产出可验证文件。

K00 的 8 个必需任务输出路径必须覆盖：`raw_inputs/`、`source_registry/`、`document_passports/`、`system_mapping/`、`gap_detection/`、`task_packages/`、`handoff_packets/`。

## 7.4 04_phase_input_contract.json

作用：

定义阶段输入。HER 不允许使用未声明输入。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/04_phase_input_contract_TEMPLATE.json`

K00 标准 Input Contract 必须包含：

- `phase_id`: 阶段编号，K00 固定为 `K00`。
- `required_inputs`: 必需输入；缺失时必须触发 `missing_action`。
- `optional_inputs`: 可选输入；缺失时不得静默忽略，必须按 `missing_action` 处理。
- `input_rules`: 输入治理规则。

核心运行规则：HER 不允许使用未声明输入；所有输入必须先保存，不允许只在上下文中引用；所有输入必须生成 `doc_id`；所有输入必须进入 `source_registry`；未保存的资料不能作为长期判断依据。

## 7.5 05_phase_output_contract.json

作用：

定义阶段必须输出什么。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/05_phase_output_contract_TEMPLATE.json`

K00 标准 Output Contract 必须包含：

- `phase_id`: 阶段编号，K00 固定为 `K00`。
- `required_outputs`: 阶段必需输出清单。
- 每个输出必须声明 `file`、`type`、`required`、`purpose`。

K00 必需输出：

- `raw_inputs/<doc_id>.md`: 保存原始资料。
- `source_registry/source_registry.json`: 资料来源登记。
- `document_passports/document_passport_<doc_id>.yaml`: 文档护照。
- `system_mapping/plane_mapping_<doc_id>.json`: 九大系统平面映射。
- `system_mapping/phase_mapping_<doc_id>.json`: P00-P09 阶段映射。
- `gap_detection/gap_detection_<doc_id>.json`: 系统缺口识别。
- `task_packages/task_execution_package_<doc_id>.json`: 阶段任务执行包。
- `handoff_packets/k00_handoff_packet_<doc_id>.json`: 交接包。

核心运行规则：K00 未生成所有 required outputs 时不得进入 `K00_READY`；缺失非阻断但可恢复资料时只能进入 `K00_READY_WITH_GAPS` 并写入 gap_detection；缺失原始资料、来源登记、文档护照或 handoff_packet 时必须阻断。

## 7.6 06_phase_execution_protocol.md

作用：

告诉 HER 怎么运行，不是描述阶段。这是 HER 长任务运行的核心。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/06_phase_execution_protocol_TEMPLATE.md`

K00 标准 Execution Protocol 必须包含：

- `执行总原则`: HER 不得把用户输入资料当作普通文档阅读，必须转化为系统可执行任务包。
- `执行顺序`: 从接收用户输入、生成 doc_id、保存 raw_inputs、更新 source_registry、生成 document_passport、系统平面映射、P00-P09 阶段映射、抽取目标/规则/约束/缺口/任务、生成 gap_detection、task_execution_package、handoff_packet、phase_state，到 acceptance_gate 自动进入下一阶段。
- `自动继续规则`: K00 输出 `PHASE_READY` 后必须按资料影响路由到 P00/P01/P09/governance_plane，不得停止在文档总结。
- `中断恢复`: 每完成一个 task_id 必须更新 `phase_state.json`；中断后必须读取 phase_state 继续未完成任务，不得重新自由理解。
- `禁止行为`: 禁止只总结文档、只输出分析建议、不保存资料、不生成任务包、无 handoff_packet 进入下一阶段、依赖聊天上下文作为唯一系统记忆。

## 7.7 07_phase_acceptance_gate.yaml

作用：

这是专业化关键。没有验收门，HER 会以为“写完文档 = 完成”。这个文件决定 HER 什么时候能说“完成”。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/07_phase_acceptance_gate_TEMPLATE.yaml`

K00 标准 Acceptance Gate 必须包含：

- `acceptance_gate.phase_id`: K00。
- `gate_id`: `K00-ACCEPTANCE-GATE`。
- `minimum_acceptance.required`: raw input、doc_id、source_registry、document_passport、plane_mapping、phase_mapping、task_execution_package、handoff_packet、phase_state 九项最低验收。
- `professional_acceptance.required`: gap、affected_phases、next_phase_recommendation、非上下文依赖、非普通文档处理、任务包目标树、任务包验收门、状态更新规则八项专业验收。
- `reject_conditions`: 原文未保存、无 doc_id、无文档护照、无任务包、只有总结无系统映射、缺失 handoff_packet、把聊天上下文当唯一记忆。
- `status_mapping`: `PHASE_READY`、`PHASE_WITH_GAPS`、`PHASE_PAUSED`、`PHASE_REJECTED`、`PHASE_ERROR`。
- `next_phase_rules`: 通过验收后按 affected_phase 自动路由到 P00/P01/P09。

核心运行规则：HER 只有通过 acceptance gate 才能声明阶段完成；写完文档不等于完成；没有 handoff_packet 或 task_execution_package 时不得进入下一阶段。

## 7.8 08_phase_state.json

作用：

这是运行状态，不是设计文档。HER 每跑一步都要回写这个文件。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/08_phase_state_TEMPLATE.json`

K00 标准 Phase State 必须包含：

- `phase_id`: 阶段编号，K00 固定为 `K00`。
- `phase_key`: 阶段键，K00 固定为 `K00_knowledge_intake_taskization`。
- `current_status`: 当前阶段运行状态，初始为 `PHASE_NOT_STARTED`。
- `current_doc_id`: 当前正在处理的资料 doc_id，未开始时为 `null`。
- `current_task_id`: 当前正在执行的 task_id，未开始时为 `null`。
- `completed_tasks`: 已完成任务列表。
- `failed_tasks`: 失败任务列表。
- `generated_files`: 已生成文件路径列表。
- `missing_files`: 缺失文件路径列表。
- `gap_list`: 已识别缺口列表。
- `hard_negative_hits`: 命中的硬负面/阻断项。
- `affected_planes`: 资料影响的系统平面。
- `affected_phases`: 资料影响的 P00-P09 阶段。
- `next_phase_recommendation`: 下一阶段建议，未判断时为 `null`。
- `last_error`: 最近错误，未报错时为 `null`。
- `next_action`: 下一步动作，初始为 `start_knowledge_intake`。
- `updated_at`: 最近更新时间，未运行时为 `null`。

核心运行规则：`08_phase_state.json` 是运行状态文件，不是设计文档；HER 每完成一个步骤、生成一个文件、发现一个缺口、命中一个 hard negative、发生一次错误、或完成一次 handoff 判断，都必须回写该文件；中断恢复必须先读取该文件再继续，不得重新自由理解。

## 7.9 09_phase_handoff_packet.schema.json

作用：

这是交接包结构，不是随便写 JSON。HER 生成 `handoff_packets/k00_handoff_packet_<doc_id>.json` 时必须受该 schema 约束。

内容结构模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/09_phase_handoff_packet.schema_TEMPLATE.json`

K00 标准 Handoff Packet Schema 必须包含：

- `type`: `object`。
- `required`: 12 个必需字段。
- `properties`: 每个必需字段的类型约束。
- `phase_status.enum`: 只能是 `PHASE_READY`、`PHASE_WITH_GAPS`、`PHASE_PAUSED`、`PHASE_REJECTED`、`PHASE_ERROR`。

必需字段：

- `phase_id`
- `phase_status`
- `doc_id`
- `raw_input_path`
- `document_passport_path`
- `task_execution_package_path`
- `affected_planes`
- `affected_phases`
- `gap_list`
- `next_phase_allowed`
- `next_phase_recommendation`
- `generated_at`

核心运行规则：handoff_packet 是下游阶段读取 K00 结果的唯一结构化交接入口；HER 不得随便写 JSON，不得缺少 required 字段，不得使用 acceptance gate 未定义的状态枚举；`next_phase_allowed` 必须来自 acceptance gate 判断，`next_phase_recommendation` 必须与 affected_phases / next_phase_rules 一致。

## Runtime rule

A directory that lacks these 9 files is not a complete Phase Controller package. It may be a note, draft, or reference, but it is not schedulable as a phase runtime unit.

## 8. 阶段任务执行包数据模型

K00 最重要的产物是：

`task_execution_package_<doc_id>.json`

作用：把用户输入的系统设计资料转化为 HER 可调度、可续跑、可验收、可交接的阶段任务。

标准模板：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/task_execution_package_TEMPLATE.json`

Schema：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/task_execution_package.schema.json`

示例：

`00_knowledge_intake/task_packages/task_execution_package_EXAMPLE.json`

必需根字段：

- `task_package_id`
- `source_doc_id`
- `package_type`
- `created_for`
- `purpose`
- `system_understanding`
- `affected_system_planes`
- `affected_phases`
- `main_objective`
- `objective_tree`
- `required_phase_package_files`
- `execution_policy`
- `acceptance_policy`
- `next_action`

核心运行规则：task_execution_package 不是摘要结果，而是 K00 的最重要产物；它必须证明输入资料不是普通文档，必须声明受影响系统平面和阶段，必须包含目标树，必须引用 9 个 Phase Package 标准文件，必须强制执行继续、验收、状态回写和 handoff 策略。

## 9. 自动化长任务执行逻辑

HER 需要执行的是多步骤长任务，不是单次回答。

标准循环：

1. 读取 `phase_state`
2. 找到 `current_task_id`
3. 执行当前 task
4. 生成对应输出
5. 更新 `phase_state`
6. 检查 `acceptance_gate`
7. 如果未完成，继续下一个 task
8. 如果完成，生成 `handoff_packet`
9. 根据 `next_phase_rules` 进入下一阶段
10. 重复执行

自动继续规则：

每完成一个阶段，不允许自动停止。HER 必须先判断：

1. 当前阶段是否 `PHASE_READY`
2. 是否存在 `BLOCKER gap`
3. 是否存在 `next_phase_recommendation`
4. 下一个阶段是否有输入
5. 是否允许继续

如果允许继续，HER 必须继续进入下一个阶段。

停止条件：

HER 只有在以下情况才能停止：

1. `PHASE_REJECTED`
2. `PHASE_ERROR`
3. 缺少关键输入
4. 命中 `BLOCKER gap`
5. 用户明确要求停止
6. 下一阶段不存在
7. 下一阶段需要人工补充资料

运行约束：自动化长任务执行必须由 `08_phase_state.json` 驱动，由 `07_phase_acceptance_gate.yaml` 判定阶段完成，由 `09_phase_handoff_packet.schema.json` 约束交接，由 `next_phase_rules` 决定下游路由。HER 不得在 `PHASE_READY` 且允许继续时停在当前阶段。

## 10. 如何落实到自动化交易流程工作流

需要分清楚：**文档知识输入自动化不是直接交易自动化**。

K00 的作用是让交易系统建设资料能够进入：

- 系统方法论
- 阶段控制器
- Atomic Skill
- 数据模型
- 状态机
- 验收门
- 交易流程

最终交易工作流应是：

1. `K00_knowledge_intake`：知识资料摄取
2. `P00_system_boundary`：系统边界确认
3. `P01_data_fact`：数据事实层
4. `P02_market_scenario`：市场场景识别
5. `P03_wallet_structure`：钱包结构识别
6. `P04_chip_control`：筹码控制判断
7. `P05_strategy_gate`：策略门禁
8. `P06_risk_control`：风险控制
9. `P07_paper_execution_human_confirmation`：纸面执行 / 人工确认
10. `P08_review_attribution`：复盘归因
11. `P09_self_upgrade_proposal`：系统升级提案

K00 保证所有新资料不会停留在聊天上下文里，而是变成系统资产。

边界规则：K00 不做直接交易自动化，不生成真实买卖指令，不跳过 P00/P05/P06/P07，不把聊天上下文当长期系统资产，不在未经验收时改写交易流程。

## 11. 总控 Skill：K00 文档知识输入强制路由核心规则

当用户输入文档、知识资料、方法论、系统设计、旧系统说明、GPT 链接内容、截图转述内容时，总控 Skill 必须把它识别为系统建设资料输入，而不是普通阅读、总结或建议任务。

触发输入类型：

- 文档
- 知识资料
- 方法论
- 系统设计
- 旧系统说明
- GPT 链接内容
- 截图转述内容

强制核心规则：

1. 不允许当作普通文档阅读后结束。
2. 必须进入 `K00_knowledge_intake_taskization_controller`。
3. 必须保存原始资料。
4. 必须生成 `doc_id`。
5. 必须生成 `document_passport`。
6. 必须映射到九大系统平面。
7. 必须映射到 `P00-P09` 阶段。
8. 必须识别系统缺口。
9. 必须生成 `task_execution_package`。
10. 必须生成 `handoff_packet`。
11. 必须更新 `phase_state`。
12. 如果 `acceptance_gate` 通过，必须自动进入下一阶段。
13. 不能依赖聊天上下文作为系统记忆。
14. 不能只输出总结或建议。

总控执行边界：

- 资料进入系统后，必须先由 K00 完成保存、登记、建模、系统映射、缺口识别、任务执行包生成和 handoff，再允许 P00-P09 或 HER task router 消费。
- 聊天上下文只允许作为临时输入缓冲，不允许作为系统记忆、验收证据或下游交接依据。
- `task_execution_package` 与 `handoff_packet` 是进入下游阶段的结构化凭证；缺失任一项时不得声称 K00 完成。
- 当 `07_phase_acceptance_gate.yaml` 判定 `PHASE_READY` 且无停止条件时，总控必须按 `next_phase_rules` 自动进入下一阶段，不得停在总结或建议。
- 本规则不授权直接交易自动化；K00 仍保持 `OBSERVE_PAPER_ONLY`，不得生成真实买卖指令、签名交易、广播交易或私钥材料。

## 12. 给 HER 的正式任务书：建立 K00 知识资料摄取与阶段任务执行包控制器


## 任务名称

建立 K00 知识资料摄取与阶段任务执行包控制器

## 任务目标

当用户输入文档、知识资料、方法论文本、系统设计内容、旧系统资料、GPT 链接内容或截图转述内容时，HER 不得将其当成普通文档阅读后总结。

HER 必须先将资料保存为系统资产，并转化为可调度、可续跑、可验收、可交接的阶段任务执行包。

## 核心原则

1. HER 不能依赖聊天上下文作为系统记忆。
2. HER 必须保存输入资料。
3. HER 必须生成文档护照。
4. HER 必须生成系统平面映射。
5. HER 必须生成 P00-P09 阶段映射。
6. HER 必须识别系统缺口。
7. HER 必须生成阶段任务执行包。
8. HER 必须生成 phase_state。
9. HER 必须生成 handoff_packet。
10. HER 必须通过 acceptance_gate 判断阶段是否完成。
11. 当前阶段完成后，如果允许进入下一阶段，不得停止，必须继续推进。

## 必须建立目录

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/
  raw_inputs/
  source_registry/
  document_passports/
  corpus_index/
  system_mapping/
  gap_detection/
  task_packages/
  intake_reports/
  handoff_packets/
```

## 必须建立 K00 Phase Package

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/
  01_phase_manifest.yaml
  02_phase_context_pack.md
  03_phase_objective_tree.yaml
  04_phase_input_contract.json
  05_phase_output_contract.json
  06_phase_execution_protocol.md
  07_phase_acceptance_gate.yaml
  08_phase_state.json
  09_phase_handoff_packet.schema.json
```

## 每个文件职责

1. `01_phase_manifest.yaml`：定义阶段是谁、负责什么、权限边界是什么。这是阶段身份证。
2. `02_phase_context_pack.md`：给 HER 的阶段上下文压缩包。HER 运行时必须先读它，避免把资料当普通文档总结。
3. `03_phase_objective_tree.yaml`：定义目标层级和任务树，让 HER 按任务树推进，而不是自由发挥。
4. `04_phase_input_contract.json`：定义阶段输入，禁止使用未声明输入。
5. `05_phase_output_contract.json`：定义阶段必须输出什么。
6. `06_phase_execution_protocol.md`：告诉 HER 怎么运行，不是描述阶段。这是 HER 长任务运行核心。
7. `07_phase_acceptance_gate.yaml`：定义完成、暂停、拒绝、错误的判定。没有验收门，不允许说完成。
8. `08_phase_state.json`：运行状态文件。HER 每完成一步都必须回写。
9. `09_phase_handoff_packet.schema.json`：定义交接包结构，禁止随便写 JSON。

## 执行要求

1. 接收输入资料后，生成 doc_id。
2. 保存原始资料到 raw_inputs。
3. 更新 source_registry。
4. 生成 document_passport。
5. 生成 plane_mapping。
6. 生成 phase_mapping。
7. 生成 gap_detection。
8. 生成 task_execution_package。
9. 生成 k00_handoff_packet。
10. 更新 phase_state。
11. 检查 acceptance_gate。
12. 如果 K00 = PHASE_READY，自动进入下一阶段。
13. 如果下一个阶段是 P00_system_boundary，则创建或更新 P00 阶段包。
14. 如果下一个阶段是 P01_data_fact，则创建或更新 P01 阶段包。
15. 如果下一个阶段是 P09_self_upgrade，则生成升级提案。
16. 中间阶段完成后不得停止，必须根据 next_phase_rules 继续推进，直到遇到 BLOCKER、ERROR、REJECTED 或需要人工输入。

## 禁止事项

1. 禁止只总结文档。
2. 禁止只输出建议。
3. 禁止不保存资料。
4. 禁止不生成任务包。
5. 禁止没有 phase_state。
6. 禁止没有 acceptance_gate。
7. 禁止没有 handoff_packet。
8. 禁止依赖聊天上下文作为唯一记忆。
9. 禁止当前阶段未验收就进入下一阶段。
10. 禁止把知识资料直接变成交易判断。

## 验收标准

1. K00 目录存在。
2. K00 Phase Package 9 个文件全部存在。
3. 原始资料保存机制存在。
4. document_passport 机制存在。
5. plane_mapping 机制存在。
6. phase_mapping 机制存在。
7. gap_detection 机制存在。
8. task_execution_package 机制存在。
9. phase_state 可更新。
10. acceptance_gate 可判断状态。
11. handoff_packet schema 存在。
12. K00 完成后可自动进入 P00 / P01 / P09。
13. HER 不再把输入资料当普通文档阅读。

## 运行边界

本任务书不授权真实交易自动化。K00 的职责是知识资料资产化与任务化；不得生成真实买卖指令、签名交易、广播交易或私钥材料。

## 13. 更新后的系统建设顺序

现在 SIKK Stable Trader OS / HER 的系统建设顺序固定为：

1. 第一步：建立 `system_methodology_blueprint.md`。
2. 第二步：建立 `K00_knowledge_intake_taskization_controller`。
3. 第三步：更新总控 Skill，加入“文档输入必须任务化”规则。
4. 第四步：建立 `P00_system_boundary`。
5. 第五步：建立 `P01_data_fact`。
6. 第六步：建立 `P02-P09` 阶段控制器。
7. 第七步：建立 Atomic Skill。
8. 第八步：接入工具 / schema / contract / replay。
9. 第九步：跑纸面交易与复盘。
10. 第十步：进入规则升级闭环。

顺序约束：K00 必须位于 P00 之前；总控 Skill 的文档输入任务化规则必须位于 P00/P01/P02-P09 执行之前；纸面交易与复盘必须位于工具/schema/contract/replay 接入之后；规则升级闭环必须基于复盘结果，而不是基于聊天上下文。

## 14. 本次版本更新的核心结论

HER 输入文档 / 知识资料时，不能再当作普通文档阅读。

必须新增 K00 知识资料摄取与任务化控制器。

K00 的作用是把所有输入资料变成：

- 原始资料保存
- 文档护照
- 系统平面映射
- 阶段映射
- 缺口识别
- 阶段任务执行包
- `phase_state`
- `acceptance_gate`
- `handoff_packet`

这样 HER 才能不依赖聊天上下文，而是依赖系统数据执行长任务。

### 本次认知升级点

1. 上传资料不是普通文档，而是系统建设输入。
2. HER 不能只读文档、总结文档，必须先保存和任务化。
3. 必须新增 K00 知识摄取与任务化控制器。
4. Phase Controller 必须是阶段运行单元，不是阶段说明文档。
5. 每个阶段必须有 9 个核心文件：manifest、context、objective_tree、input_contract、output_contract、execution_protocol、acceptance_gate、state、handoff_schema。
6. HER 长任务不能完成一个阶段就停，必须通过 acceptance_gate 决定是否进入下一阶段。
7. 系统不能依靠上下文，必须依靠文件化系统数据、状态回写和 handoff。

### 版本边界

本次更新是 HER / SIKK Stable Trader OS 的系统建设顺序与知识输入治理升级，不授权真实交易执行、签名、broadcast、swap 或私钥材料处理。K00 只负责知识资料资产化、任务化、验收与交接。
