# K00 知识资料摄取与任务化｜Context Pack

## 1. 本阶段为什么存在

用户输入的文档、知识资料、方法论文本不能被当成普通文档阅读。
它们可能是系统建设资料、阶段设计资料、规则升级资料、Atomic Skill 资料或旧系统迁移资料。

HER 必须先保存资料，再建立结构化任务包。

## 2. 本阶段不做什么

- 不直接做交易判断
- 不直接写买入卖出建议
- 不直接进入 P02-P05
- 不把聊天上下文当作长期记忆
- 不只写总结报告后停止

## 3. 本阶段必须做什么

- 保存原始资料
- 生成文档护照
- 生成系统映射
- 识别阶段影响
- 识别缺口
- 生成任务执行包
- 输出 handoff_packet
- 判断是否进入下一阶段

## 4. 本阶段完成标准

只有当原始资料、文档护照、系统映射、缺口列表、任务执行包、handoff_packet 全部生成后，本阶段才能进入 PHASE_READY。

## Runtime Boundary

- `runtime_boundary`: `OBSERVE_PAPER_ONLY`
- 禁止真实交易、私钥、签名、broadcast、swap。
- 禁止把资料中的预测、观点或建议直接转成交易执行。
- 禁止把 GPT 链接摘要当成原始事实；必须保存可追溯内容或标记不可验证。
- 禁止绕过字段来源、反证、验收与 handoff。

## K00 标准输出目录

K00 的标准输出根目录：

`/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/`

目录结构：

```text
00_knowledge_intake/
  raw_inputs/            # 保存原始上传资料，不修改
  source_registry/       # 记录资料来源、时间、类型、用途
  document_passports/    # 每份资料的护照
  corpus_index/          # 建立语料索引
  system_mapping/        # 映射到九大系统平面和 P00-P09
  gap_detection/         # 识别系统缺口
  task_packages/         # 生成阶段任务执行包
  intake_reports/        # 人类可读报告
  handoff_packets/       # 交接给 P00/P01 或其他阶段
```

## K00 文档护照标准

每份进入 K00 的上传资料必须生成一个 YAML 文档护照：

`00_knowledge_intake/document_passports/document_passport_<doc_id>.yaml`

Schema 路径：

`00_knowledge_intake/document_passports/document_passport.schema.json`

Template 路径：

`00_knowledge_intake/document_passports/document_passport_TEMPLATE.yaml`

## 阶段任务执行包标准

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

`02_phase_context_pack.md` 的作用：这不是普通说明。这是给 HER 的阶段上下文压缩包。HER 运行时必须先读它，避免把该阶段误做成普通总结或策略判断。

Context Pack template：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/02_phase_context_pack_TEMPLATE.md`

## Field Source / 字段来源 Rule

所有 K00 输出字段必须记录 `field_source_map`：

- `raw_user_material`: 用户直接输入文本、文档、截图说明、方法论文本。
- `gpt_link_content`: GPT 分享链接解析内容，必须保留抓取/人工粘贴来源状态。
- `legacy_system_document`: 旧系统文档或旧目录资料。
- `existing_repo_artifact`: 仓库已有 registry、phase、skill、schema、contract、audit。
- `derived_model`: 从原文抽取的模型，必须链接 source span。
- `gap_inference`: 缺口判断，必须链接期望 contract 与实际资料。
- `human_confirmation_required`: 无法由资料验证的判断。

## System Plane Mapping

K00 必须判断资料属于哪个系统平面：

- governance_plane
- control_plane
- data_plane
- execution_plane
- verification_plane
- phase_controller
- skill_layer
- module_layer
- contract_schema_layer
- runtime_state_layer
- recovery_gap_layer
- memory_knowledge_layer
- report_audit_layer

## P00-P09 Impact Mapping

K00 必须标明资料影响哪些阶段：

- K00_knowledge_intake
- P00_system_boundary
- P01_data_fact
- P02_wallet_structure
- P03_chip_control
- P04_scenario_detection
- P05_strategy_gate
- P06_execution_risk
- P07_runtime_monitoring
- P08_review
- P09_self_upgrade

## Counter Evidence / 反证 Rule

每个正向映射必须检查反证：

- 是否缺少原文依据？
- 是否与现有系统规则冲突？
- 是否只有方法描述但没有合约字段？
- 是否会污染 P00-P09 事实、推理、策略、执行边界？
- 是否绕过 runtime state、acceptance gate 或 handoff？

## Acceptance / 验收 Meaning

K00 验收通过不代表 P00-P09 已执行，也不代表交易系统功能已实现。K00 验收通过只代表：资料已保存、清单已建立、护照已生成、系统映射已完成、阶段影响已识别、缺口列表已生成、任务执行包已生成、phase_state 与 handoff_packet 已可被下游读取。

## Handoff Position

K00 的默认下游是 `P00_system_boundary`。如果资料属于局部修复或独立任务，也可 handoff 给 HER task router 或 gap closure planner，但必须在 handoff_packet 中说明原因。


## 7.3 03_phase_objective_tree.yaml｜目标树标准

作用：让 HER 知道目标层级。它比 Markdown 模板更专业，因为它能让 HER 按任务树推进，而不是自由发挥。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/03_phase_objective_tree.yaml`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/03_phase_objective_tree_TEMPLATE.yaml`。

运行要求：
- 必须以 `objective_tree` 为根。
- 必须包含 `phase_id`、`level_1_goal`、`level_2_sub_goals`、`level_3_tasks`。
- `level_3_tasks[].parent` 必须指向已存在的 `level_2_sub_goals[].id`。
- 每个任务必须声明 `action` 与 `output`。
- K00 必须覆盖 raw input、source registry、document passport、system plane mapping、phase mapping、gap detection、task package、handoff_packet 八类输出。

## 7.4 04_phase_input_contract.json｜输入合约标准

作用：定义阶段输入。HER 不允许使用未声明输入。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/04_phase_input_contract.json`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/04_phase_input_contract_TEMPLATE.json`。

K00 输入合约要求：
- 必需输入：`user_input_content`，类型 `text`，缺失动作 `PHASE_REJECTED`。
- 可选输入：`uploaded_file_paths`，类型 `array`，缺失动作 `CONTINUE_WITH_TEXT_ONLY`。
- 可选输入：`legacy_system_paths`，类型 `array`，缺失动作 `MARK_AS_GAP`。

运行规则：
- 所有输入必须先保存，不允许只在上下文中引用。
- 所有输入必须生成 `doc_id`。
- 所有输入必须进入 `source_registry`。
- 未保存的资料不能作为长期判断依据。

## 7.5 05_phase_output_contract.json｜输出合约标准

作用：定义阶段必须输出什么。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/05_phase_output_contract.json`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/05_phase_output_contract_TEMPLATE.json`。

K00 必需输出：
- `raw_inputs/<doc_id>.md`：保存原始资料。
- `source_registry/source_registry.json`：资料来源登记。
- `document_passports/document_passport_<doc_id>.yaml`：文档护照。
- `system_mapping/plane_mapping_<doc_id>.json`：九大系统平面映射。
- `system_mapping/phase_mapping_<doc_id>.json`：P00-P09 阶段映射。
- `gap_detection/gap_detection_<doc_id>.json`：系统缺口识别。
- `task_packages/task_execution_package_<doc_id>.json`：阶段任务执行包。
- `handoff_packets/k00_handoff_packet_<doc_id>.json`：交接包。

运行规则：K00 未生成所有 required outputs 时不得进入 `K00_READY`；缺失非阻断但可恢复资料时只能进入 `K00_READY_WITH_GAPS` 并写入 gap_detection；缺失原始资料、来源登记、文档护照或 handoff_packet 时必须阻断。
## 7.6 06_phase_execution_protocol.md｜执行协议标准

作用：告诉 HER 怎么运行，不是描述阶段；这是 HER 长任务运行的核心。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/06_phase_execution_protocol.md`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/06_phase_execution_protocol_TEMPLATE.md`。

K00 执行总原则：HER 不得把用户输入资料当作普通文档阅读，必须把输入资料转化为系统可执行任务包。

执行顺序硬约束：
1. 接收用户输入资料
2. 为资料生成 doc_id
3. 将原始资料保存到 raw_inputs/
4. 更新 source_registry
5. 生成 document_passport
6. 分析资料属于九大系统平面的哪几类
7. 分析资料影响 P00-P09 哪些阶段
8. 提取资料中的系统目标、阶段目标、规则、约束、缺口、任务
9. 生成 gap_detection
10. 生成 task_execution_package
11. 生成 K00 handoff_packet
12. 更新 phase_state
13. 判断是否进入下一阶段
14. 如果通过 acceptance_gate，则自动进入下一阶段，不停止

自动继续规则：当 K00 输出 `PHASE_READY` 时，按资料影响路由到 `P00_system_boundary`、`P01_data_fact`、`P09_self_upgrade` 或 `governance_plane / system_methodology_blueprint` 更新流程。

中断恢复规则：HER 每完成一个 `task_id` 必须更新 `phase_state.json`；中断后必须读取 `phase_state.json` 继续未完成任务，不得重新自由理解。

禁止行为：禁止只总结文档、只输出分析建议、不保存资料、不生成任务包、没有 handoff_packet 就进入下一阶段、依赖聊天上下文作为唯一系统记忆。
## 7.7 07_phase_acceptance_gate.yaml｜验收门标准

作用：这是专业化关键。没有验收门，HER 会以为“写完文档 = 完成”。这个文件决定 HER 什么时候能说“完成”。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/07_phase_acceptance_gate.yaml`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/07_phase_acceptance_gate_TEMPLATE.yaml`。

K00 最低验收：必须完成 raw_input_saved、doc_id_generated、source_registry_updated、document_passport_generated、plane_mapping_generated、phase_mapping_generated、task_execution_package_generated、handoff_packet_generated、phase_state_updated。

K00 专业验收：必须确认 system_gap_detected_or_marked_none、affected_phases_identified、next_phase_recommendation_generated、no_context_only_dependency、not_treated_as_plain_document、task_package_has_objective_tree、task_package_has_acceptance_gate、task_package_has_state_update_rule。

拒绝条件：raw_input_not_saved、no_doc_id、no_document_passport、no_task_execution_package、only_summary_without_system_mapping、handoff_packet_missing、used_chat_context_as_only_memory。

状态映射：全部专业验收通过为 `PHASE_READY`；最低通过但有小缺口为 `PHASE_WITH_GAPS`；可恢复缺失输出为 `PHASE_PAUSED`；关键输出缺失为 `PHASE_REJECTED`；运行错误为 `PHASE_ERROR`。

下一阶段规则：当 `phase_status == PHASE_READY` 且 affected_phase 包含对应阶段时，自动路由到 `P00_system_boundary`、`P01_data_fact` 或 `P09_self_upgrade`。
## 7.8 08_phase_state.json｜阶段运行状态标准

作用：这是运行状态，不是设计文档。HER 每跑一步都要回写这个文件。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/08_phase_state.json`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/08_phase_state_TEMPLATE.json`。

K00 初始状态：
- `current_status`: `PHASE_NOT_STARTED`
- `current_doc_id`: `null`
- `current_task_id`: `null`
- `completed_tasks`: `[]`
- `failed_tasks`: `[]`
- `generated_files`: `[]`
- `missing_files`: `[]`
- `gap_list`: `[]`
- `hard_negative_hits`: `[]`
- `affected_planes`: `[]`
- `affected_phases`: `[]`
- `next_phase_recommendation`: `null`
- `last_error`: `null`
- `next_action`: `start_knowledge_intake`
- `updated_at`: `null`

运行规则：HER 每完成一个步骤、生成一个文件、发现一个缺口、命中一个 hard negative、发生一次错误、或完成一次 handoff 判断，都必须回写 `08_phase_state.json`。中断恢复必须先读取该文件，再从 `current_task_id` / `completed_tasks` / `failed_tasks` / `next_action` 继续，不得重新自由理解。
## 7.9 09_phase_handoff_packet.schema.json｜阶段交接包 Schema 标准

作用：这是交接包结构，不是随便写 JSON。HER 生成 `handoff_packets/k00_handoff_packet_<doc_id>.json` 时必须受该 schema 约束。

标准位置：`06_phase_controllers/K00_knowledge_intake_taskization/09_phase_handoff_packet.schema.json`。
模板位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/09_phase_handoff_packet.schema_TEMPLATE.json`。

K00 handoff_packet 必需字段：
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

运行规则：handoff_packet 是下游阶段读取 K00 结果的唯一结构化交接入口；HER 不得随便写 JSON，不得缺少 required 字段；`phase_status` 必须来自 `07_phase_acceptance_gate.yaml` 的状态映射；`next_phase_allowed` 必须来自验收门判断；`next_phase_recommendation` 必须与 `affected_phases` 和 `next_phase_rules` 一致。
## 8. 阶段任务执行包数据模型｜task_execution_package_<doc_id>.json

K00 最重要的产物是 `task_packages/task_execution_package_<doc_id>.json`。

它不是文档摘要，而是 HER 可调度、可续跑、可验收、可交接的阶段任务数据模型。

标准位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/task_execution_package_TEMPLATE.json`。  
Schema 位置：`00_knowledge_intake/task_packages/phase_task_execution_package_standard/task_execution_package.schema.json`。

K00 生成 task_execution_package 时必须包含：

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

运行规则：task_execution_package 必须证明输入资料不是普通文档，必须声明受影响系统平面和阶段，必须包含目标树，必须引用 9 个 Phase Package 标准文件，必须强制继续执行、验收判断、状态回写和 handoff 生成。
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

自动继续判断：HER 每完成一个阶段，必须判断当前阶段是否 `PHASE_READY`、是否存在 `BLOCKER gap`、是否存在 `next_phase_recommendation`、下一个阶段是否有输入、是否允许继续。若允许继续，HER 必须继续进入下一个阶段。

停止条件：HER 只能在 `PHASE_REJECTED`、`PHASE_ERROR`、缺少关键输入、命中 `BLOCKER gap`、用户明确要求停止、下一阶段不存在、下一阶段需要人工补充资料时停止。
## 10. 如何落实到自动化交易流程工作流

K00 的文档知识输入自动化不是直接交易自动化。它的职责是把交易系统建设资料转化为可索引、可验证、可交接、可复用的系统资产，并让资料进入系统方法论、阶段控制器、Atomic Skill、数据模型、状态机、验收门和交易流程。

最终交易工作流：

1. K00 知识资料摄取
2. P00 系统边界确认
3. P01 数据事实层
4. P02 市场场景识别
5. P03 钱包结构识别
6. P04 筹码控制判断
7. P05 策略门禁
8. P06 风险控制
9. P07 纸面执行 / 人工确认
10. P08 复盘归因
11. P09 系统升级提案

K00 保证所有新资料不会停留在聊天上下文里，而是变成系统资产。K00 不允许直接生成真实交易动作，不允许跳过 P00 边界确认，不允许跳过 P05/P06/P07 门禁。

## 11. 总控 Skill 路由规则锚点

当输入属于文档、知识资料、方法论、系统设计、旧系统说明、GPT 链接内容或截图转述内容时，HER 必须由总控 Skill 强制进入 `K00_knowledge_intake_taskization_controller`。

K00 不允许把此类输入处理成普通阅读任务；必须按 14 条核心规则完成：保存原始资料、生成 `doc_id`、生成 `document_passport`、映射九大系统平面、映射 `P00-P09`、识别系统缺口、生成 `task_execution_package`、生成 `handoff_packet`、更新 `phase_state`，并在 `acceptance_gate` 通过后自动进入下一阶段。

禁止项：普通文档阅读后结束、只输出总结、只输出建议、依赖聊天上下文作为系统记忆、无任务包或无交接包进入下游。

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
