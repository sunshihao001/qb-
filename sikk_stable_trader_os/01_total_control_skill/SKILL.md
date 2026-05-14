---
name: sikk_stable_trader_os
description: Thin HER total-control Skill for SIKK Stable Trader OS. Routes Phase00-09 through contracts, status, hard-negative inheritance, handoff validation, audit, and paper-only acceptance.
version: 2.2.0
---

# SIKK Stable Trader OS Total Control Skill

## Core boundary

Phase Controller 不是阶段说明文档。 Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。 它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

This layer is **not Phase10**. Phase00-09 remain the runtime phases; total control is the HER entry/control plane.

## Mandatory startup order

1. Read `docs/00_system_goal/sikk_stable_trader_os_goal.md`.
2. Read `docs/01_stage_definitions/full_stage_map.md`.
3. Read `docs/03_handoff_flow/phase_handoff_flow.md`.
4. Read `docs/04_status_codes/global_status_code_table.md`.
5. Read `docs/05_hard_negative_rules/global_hard_negative_rules.md`.
6. Read `docs/07_contract_index/contract_index.md` and `docs/08_schema_index/schema_index.md`.
7. Load target `sikk_stable_trader_os/02_phase_controllers/Pxx_*` package.
8. Execute only in `OBSERVE_PAPER_ONLY` unless a future manually approved project changes boundary.


## Knowledge material input routing rule

文档输入不能当普通文档处理。

HER 必须先识别：

- 当前输入不是普通阅读材料。
- 当前输入是系统建设资料。
- 当前输入需要进入知识摄取流程。
- 当前输入需要保存、登记、建模、映射、任务化。
- 当前输入可能影响系统方法论、阶段设计、Atomic Skill、Schema、Contract、Tool、Report、Replay。

禁止 HER 直接做：

- 总结一下文档
- 提炼核心观点
- 泛泛分析
- 直接给建议
- 根据当前上下文继续聊

必须改成：

1. 保存资料。
2. 登记资料。
3. 生成文档护照。
4. 映射系统平面。
5. 映射阶段。
6. 识别缺口。
7. 生成任务包。
8. 进入阶段执行。
9. 验收后继续下一阶段。

Routing: any uploaded document, method wheel, knowledge material, screenshot explanation, legacy system document, GPT link content, or methodology text must route first to `K00_knowledge_intake_taskization_controller` before P00-P09 execution or any advice/reporting.


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

## Knowledge material standard system-entry flow

资料进入系统后的标准流程：

```text
用户输入资料
↓
K00 原始资料保存
↓
K00 文档护照生成
↓
K00 语料索引生成
↓
K00 系统映射
↓
K00 缺口识别
↓
K00 阶段任务执行包生成
↓
P00 系统边界确认
↓
P01 数据事实层
↓
P02-P09 后续阶段
```

该流程是系统建设资料的默认入口路径。任何资料在进入 P00-P09 前，必须先完成 K00 的保存、护照、索引、映射、缺口识别与任务包生成；不得跳过 K00 直接进入总结、建议、执行或下游阶段。

K00 route status 是 PXX / IXX / Phase Controller READY 的前置验收字段：

```text
valid_ready_requires = K00_INTAKE_ACCEPTED | K00_ROUTE_RECOVERY_DOCUMENTED
invalid_ready_if = K00_ROUTE_FAILED | missing_k00_route_status
```

如果用户上传/粘贴系统建设资料后，尚未形成 raw / passport / registry / corpus index / system mapping / phase mapping / gap / task package / phase_state / acceptance / handoff，则不得声明阶段 READY；必须先补 route recovery，并把阶段结论降级为 READY_WITH_RUNTIME_GAPS 或 READY_WITH_K00_ROUTE_RECOVERED，直到 recovery 证据可审计。


## K00 standard output directory model

K00 标准输出根目录：

`/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/`

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

All K00 material-intake artifacts must be written to or referenced from this root. Do not scatter new intake outputs into legacy paths unless a compatibility reader explicitly requires fallback.




## 7.2 02_phase_context_pack.md

作用：

这不是普通说明。这是给 HER 的阶段上下文压缩包。HER 运行时必须先读它，避免把该阶段误做成普通总结或策略判断。

K00 Context Pack 标准结构：

1. 本阶段为什么存在：用户输入的文档、知识资料、方法论文本不能被当成普通文档阅读；HER 必须先保存资料，再建立结构化任务包。
2. 本阶段不做什么：不直接做交易判断；不直接写买入卖出建议；不直接进入 P02-P05；不把聊天上下文当作长期记忆；不只写总结报告后停止。
3. 本阶段必须做什么：保存原始资料；生成文档护照；生成系统映射；识别阶段影响；识别缺口；生成任务执行包；输出 handoff_packet；判断是否进入下一阶段。
4. 本阶段完成标准：只有当原始资料、文档护照、系统映射、缺口列表、任务执行包、handoff_packet 全部生成后，本阶段才能进入 PHASE_READY。

模板路径：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/02_phase_context_pack_TEMPLATE.md`

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

`01_phase_manifest.yaml` 的作用：定义这个阶段是谁、负责什么、权限边界是什么。这是阶段身份证。

阶段任务执行包标准资产路径：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/`

Manifest template：

`00_knowledge_intake/task_packages/phase_task_execution_package_standard/01_phase_manifest_TEMPLATE.yaml`

## K00 文档护照标准

每份进入 K00 的上传资料必须生成一个 YAML 文档护照：

`00_knowledge_intake/document_passports/document_passport_<doc_id>.yaml`

标准命名示例：

`document_passport_DOC-20260511-001.yaml`

文档护照必须至少包含：

- `doc_id`: 文档唯一编号，格式 `DOC-YYYYMMDD-001`。
- `source_type`: 来源类型，例如 `user_uploaded_text`。
- `source_name`: 来源名称或用户给出的资料标题。
- `received_at`: 接收日期，格式 `YYYY-MM-DD`。
- `raw_path`: 对应原始资料路径，必须指向 `00_knowledge_intake/raw_inputs/`。
- `document_role.primary_role`: 资料主角色。
- `document_role.secondary_roles`: 资料副角色列表。
- `summary.core_intent`: 资料进入系统的核心意图。
- `summary.key_points`: 关键点列表。
- `system_mapping.planes`: 影响的系统平面。
- `system_mapping.affected_phases`: 影响的 K00/P00-P09 阶段。
- `required_actions`: 由该资料触发的动作。
- `evidence_level`: 证据等级，枚举 `EVIDENCE_A_STRONG`、`EVIDENCE_B_MEDIUM`、`EVIDENCE_C_WEAK`、`EVIDENCE_D_UNVERIFIED`。
- `status`: 护照状态，枚举 `PASSPORT_READY`、`PASSPORT_DRAFT`、`PASSPORT_REJECTED`、`PASSPORT_SUPERSEDED`。

Schema 路径：

`00_knowledge_intake/document_passports/document_passport.schema.json`

Template 路径：

`00_knowledge_intake/document_passports/document_passport_TEMPLATE.yaml`

## Safety boundary

Allowed: observe, replay, paper-only, manual review ticket, rule proposal.
Forbidden: private key, signing, broadcast, swap execution, auto real trade, uncontrolled runtime mutation.

## Completion Rule

A stage can advance only when: input contract passes or gaps are classified, output contract is written, handoff schema validates, hard negatives are inherited, status mapping is deterministic, and audit evidence is written.


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
