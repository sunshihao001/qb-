# Hermes 方法轮补全清单 v1

## 0. 定位

本文是 `/root/sikk-gmgn/docs/harness/ai_harness_system/` 中 `method_wheel` 任务类型的补全路线图。

方法轮不是摘要流程，而是 Hermes / HER Harness 的正式运行任务类型：

```text
输入材料 / 长文档 / 对话沉淀 / 复杂需求
↓
文档护照
↓
核心机制提炼
↓
问题识别
↓
系统映射
↓
缺口检测
↓
任务包生成
↓
验证审计
↓
复盘写回
```

本清单回答三个问题：

1. 还有哪些方法轮相关文档需要补全。
2. 每个文档应补什么内容。
3. 按 Hermes 受控运行方式，补完后如何验收。

---

## 1. 当前缺口总览

### 1.1 已存在但需要增强的文件

| 文件 | 当前状态 | 需要补全 |
|---|---|---|
| `00_control_plane/method_wheel_policy.md` | 已有 task_type 和 9 阶段 | 补输入/输出契约、失败处理、禁止事项、复盘写回条件 |
| `10_templates/method_wheel_task_template.md` | 已有阶段名 | 补每阶段输入、输出、验证、失败处理、下一阶段入口 |
| `02_research_loop/README.md` | 已有任务分解说明 | 补子目录职责、文件命名、产物分层、方法轮完成定义 |
| `11_hermes_bot_invocation/core_workflows_v1.md` | 已有“文章/书籍→方法轮”粗流程 | 补目录映射、产物映射、命令映射、验证入口 |
| `11_hermes_bot_invocation/chinese_command_system.md` | 已有命令列表 | 补 `/方法轮执行` 的输入格式、输出格式、失败流转 |
| `06_verification/v1_acceptance_criteria.md` | 已有 V1 验收项 | 补 method_wheel 专项验收标准 |

### 1.2 建议新增的文件

| 新文件 | 作用 |
|---|---|
| `02_research_loop/method_wheel_output_contract.md` | 定义方法轮输出合同 |
| `02_research_loop/method_wheel_directory_contract.md` | 定义 intake/passports/theme_maps/gap_detection/synthesis 的目录职责 |
| `06_verification/method_wheel_verification_checklist.md` | 方法轮专项验收清单 |
| `07_recovery/method_wheel_recovery_playbook.md` | 方法轮失败恢复手册 |
| `11_hermes_bot_invocation/method_wheel_command_contract.md` | 中文命令和 method_wheel task_type 的绑定合同 |

---

## 2. 补全原则

### 2.1 不允许只做摘要

方法轮输出不得只有“总结 / 摘要 / 观点”。必须至少包含：

- 文档护照
- 核心机制
- 问题清单
- 系统映射
- 缺口检测
- 可执行任务包
- 验收标准
- 复盘写回建议

### 2.2 不允许跳过系统映射

如果没有把材料映射到现有系统目录、代码、合同、控制面或任务状态，不能进入任务包生成。

### 2.3 不允许未验证写回记忆

方法轮中的结论只有在通过验证后，才允许进入：

- `03_context_governance/`
- 长期 memory
- skill
- control plane

未验证内容只能保留在 `02_research_loop/`。

### 2.4 任务包必须可执行

方法轮生成的任务包必须能回答：

- 要改哪个文件
- 为什么改
- 输入是什么
- 输出是什么
- 怎么验证
- 失败如何恢复

---

## 3. 文件级补全方案

## 3.1 `00_control_plane/method_wheel_policy.md`

### 需要补的章节

1. `适用范围`
   - 文章、书籍、长文档、ChatGPT 分享链接、系统设计材料、复杂用户需求。

2. `不适用范围`
   - 简单问答、单步命令、无需沉淀的临时解释、已明确执行路径的代码小修。

3. `输入契约`
   - 原始材料路径 / URL / 文本片段。
   - 来源说明。
   - 是否完整。
   - 是否需要切片。
   - 是否含敏感信息。

4. `输出契约`
   - document passport
   - mechanism extraction
   - problem list
   - system map
   - gap report
   - task packages
   - acceptance criteria
   - retrospective writeback proposal

5. `阶段门禁`
   - PHASE_1 未完成不得进入 PHASE_2。
   - PHASE_5 系统映射未完成不得生成任务包。
   - PHASE_8 验证失败不得进入 PHASE_9。

6. `禁止事项`
   - 禁止只做摘要。
   - 禁止直接把未验证结论写 memory。
   - 禁止把方法轮产物写进业务 runtime 数据目录。
   - 禁止把旧材料当成当前事实，不做时间戳和来源标注。

7. `完成定义`
   - 每阶段产物存在。
   - 每阶段有验证记录。
   - 任务包可执行。
   - 复盘写回候选有证据。

---

## 3.2 `10_templates/method_wheel_task_template.md`

### 需要补的结构

每个阶段必须固定为：

```yaml
phase_id:
phase_name:
phase_goal:
input_sources:
required_actions:
output_artifacts:
verification:
failure_handling:
next_phase_entry:
```

### 9 个阶段应补的最小合同

#### PHASE_1 文档接收

- 输入：原文、文件、URL、对话链接。
- 输出：`02_research_loop/intake/<task_id>_raw_input.md`
- 验证：来源可读、内容未空、敏感信息标注。

#### PHASE_2 文档护照

- 输出：`02_research_loop/passports/<task_id>_document_passport.md`
- 必含：来源、主题、完整度、适用范围、风险、时间戳、后续用途。

#### PHASE_3 核心机制提炼

- 输出：`02_research_loop/synthesis/<task_id>_mechanism_extraction.md`
- 必含：机制、因果链、前提、边界、反例。

#### PHASE_4 问题识别

- 输出：`02_research_loop/gap_detection/<task_id>_problem_list.md`
- 必含：问题、影响、需要补的数据/代码/规则。

#### PHASE_5 系统映射

- 输出：`02_research_loop/theme_maps/<task_id>_system_mapping.md`
- 必含：对应目录、对应文件、对应控制面、对应 workflow。

#### PHASE_6 缺口检测

- 输出：`02_research_loop/gap_detection/<task_id>_gap_report.md`
- 必含：缺失文件、缺失合同、缺失测试、缺失路由、缺失验证。

#### PHASE_7 任务包生成

- 输出：`04_task_plans/execution_packets/<task_id>_task_packet.md`
- 必含：任务列表、修改路径、验收命令、失败恢复。

#### PHASE_8 验证审计

- 输出：`06_verification/verification_reports/<task_id>_method_wheel_verification.md`
- 必含：文件存在、内容锚点、路由连接、验收标准。

#### PHASE_9 复盘写回

- 输出：`09_reports/final_reports/<task_id>_method_wheel_final_report.md`
- 必含：完成内容、未完成内容、可写 memory/skill/control-plane 候选。

---

## 3.3 `02_research_loop/README.md`

### 需要补的目录职责

```text
02_research_loop/
├── intake/          # 原始材料接收，不改写原意
├── passports/       # 文档护照，说明来源/范围/风险
├── method_lenses/   # 方法视角，定义从哪个角度看材料
├── theme_maps/      # 系统映射，材料 → 系统目录/模块/合同
├── gap_detection/   # 问题与缺口检测
├── synthesis/       # 核心机制综合提炼
└── outputs/         # 方法轮最终产物，可进入任务包或报告
```

### 需要补的规则

- `intake/` 保留原始材料或摘录，不做结论。
- `passports/` 只描述材料，不做任务决策。
- `synthesis/` 可以提出机制，但必须标注证据来源。
- `gap_detection/` 只记录缺口，不直接修改系统。
- `theme_maps/` 是进入执行计划前的强制门禁。
- `outputs/` 只能放通过 PHASE_8 验证后的方法轮最终产物。

---

## 3.4 `11_hermes_bot_invocation/core_workflows_v1.md`

### 工作流 2 应补成这样

```text
用户提供文章 / 书籍 / 长文档 / share 链接
↓
PHASE_1 写入 intake
↓
PHASE_2 生成 document passport
↓
PHASE_3 提炼 core mechanism
↓
PHASE_4 生成 problem list
↓
PHASE_5 生成 system mapping
↓
PHASE_6 生成 gap report
↓
PHASE_7 生成 execution packet
↓
PHASE_8 生成 verification report
↓
PHASE_9 生成 final report + writeback candidate
```

### 必须补目录映射

| 阶段 | 目录 |
|---|---|
| PHASE_1 | `02_research_loop/intake/` |
| PHASE_2 | `02_research_loop/passports/` |
| PHASE_3 | `02_research_loop/synthesis/` |
| PHASE_4 | `02_research_loop/gap_detection/` |
| PHASE_5 | `02_research_loop/theme_maps/` |
| PHASE_6 | `02_research_loop/gap_detection/` |
| PHASE_7 | `04_task_plans/execution_packets/` |
| PHASE_8 | `06_verification/verification_reports/` |
| PHASE_9 | `09_reports/final_reports/` |

---

## 3.5 `11_hermes_bot_invocation/chinese_command_system.md`

### `/方法轮执行` 应补的命令合同

```text
命令：/方法轮执行
任务类型：method_wheel
输入：文档路径 / URL / 原始文本 / 对话链接 / 已导入材料 ID
输出：方法轮 task_id、当前阶段、下一步入口
禁止：只输出摘要、跳过护照、跳过系统映射、直接写 memory
失败：进入 /错误恢复
验证：进入 /验证结果
复盘：进入 /生成复盘
```

### 命令流转

```text
/目标登记
↓
/方法轮执行
↓
/执行一轮
↓
/验证结果
↓
失败：/错误恢复
通过：/生成复盘
↓
如有验证后规则：/写入记忆
```

---

## 3.6 `06_verification/v1_acceptance_criteria.md`

### 需要新增 method_wheel 验收项

- method_wheel task_type 已在控制面定义。
- 9 阶段模板完整。
- 每阶段有输入、输出、验证、失败处理、下一阶段入口。
- `02_research_loop/` 子目录职责清晰。
- `/方法轮执行` 已绑定 method_wheel。
- 方法轮产物不能只做摘要。
- 任务包能进入 `04_task_plans/execution_packets/`。
- 验证报告能进入 `06_verification/verification_reports/`。
- 复盘报告能进入 `09_reports/final_reports/`。
- 只有验证后的规则才能进入 memory / skill / control plane。

---

## 4. 补全顺序

### 第一优先级：控制闭环

1. `00_control_plane/method_wheel_policy.md`
2. `10_templates/method_wheel_task_template.md`
3. `02_research_loop/README.md`

目标：让方法轮从“概念”变成“受控 task_type”。

### 第二优先级：入口闭环

4. `11_hermes_bot_invocation/chinese_command_system.md`
5. `11_hermes_bot_invocation/core_workflows_v1.md`
6. `11_hermes_bot_invocation/method_wheel_command_contract.md`

目标：让用户能通过命令稳定触发方法轮。

### 第三优先级：验证闭环

7. `06_verification/method_wheel_verification_checklist.md`
8. `07_recovery/method_wheel_recovery_playbook.md`
9. `06_verification/v1_acceptance_criteria.md`

目标：防止方法轮表面完成。

---

## 5. 最小可验收版本

如果只做最小可用版本，必须完成：

- `method_wheel_policy.md` 有输入/输出/门禁/禁止事项。
- `method_wheel_task_template.md` 有 9 阶段完整字段。
- `02_research_loop/README.md` 有子目录职责。
- `/方法轮执行` 有命令合同。
- 有一份 `method_wheel_verification_checklist.md`。

---

## 6. 完成后的 Hermes 行为标准

当用户说：

- “把这个链接做方法轮”
- “分析这篇文章”
- “把这个 ChatGPT 分享落到系统里”
- “这段规则应该怎么变成 Hermes 能执行的系统”

Hermes 应该自动走：

```text
目标护照
↓
method_wheel task_type
↓
PHASE_1 ~ PHASE_9
↓
验证报告
↓
复盘报告
↓
可选记忆 / skill / control-plane 写回
```

而不是只给一段总结。

---

## 7. 下一步建议

下一步应直接执行“第一优先级控制闭环”：

1. 补 `00_control_plane/method_wheel_policy.md`
2. 补 `10_templates/method_wheel_task_template.md`
3. 补 `02_research_loop/README.md`
4. 生成 `06_verification/method_wheel_verification_checklist.md`

完成后再补命令入口和 recovery。