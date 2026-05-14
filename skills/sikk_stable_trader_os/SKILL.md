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
