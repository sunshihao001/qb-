# K00 Knowledge Intake Standard Output Directory

该目录是 `K00_knowledge_intake_taskization_controller` 的标准输出根目录。

所有上传文档、方法轮、知识资料、截图说明、旧系统文档、GPT 链接内容、方法论文本进入 SIKK Stable Trader OS 前，必须先由 K00 写入或登记到本目录结构。

## 标准目录结构

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

## 目录职责

- `raw_inputs/`: 保存原始上传资料，不修改。
- `source_registry/`: 记录资料来源、时间、类型、用途。
- `document_passports/`: 每份资料的护照。
- `corpus_index/`: 建立语料索引。
- `system_mapping/`: 映射到九大系统平面和 P00-P09。
- `gap_detection/`: 识别系统缺口。
- `task_packages/`: 生成阶段任务执行包。
- `intake_reports/`: 人类可读报告。
- `handoff_packets/`: 交接给 P00/P01 或其他阶段。



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

## 写入原则

1. `raw_inputs/` 只保存原始资料或原始资料指针，不允许用总结覆盖原文。
2. `source_registry/` 是资料来源登记层，必须先于建模与任务化生成。
3. `document_passports/` 与 `corpus_index/` 是 K00 进入系统映射前的最低可读资产。
4. `system_mapping/` 必须同时标注九大系统平面与 P00-P09 影响。
5. `gap_detection/` 必须记录 blocker、degraded、followup、human_confirmation_required。
6. `task_packages/` 是下游阶段执行单位，不是聊天总结。
7. `handoff_packets/` 必须可被 P00/P01 或目标阶段读取，并引用对应 task package、gap register 与 audit/intake report。


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
