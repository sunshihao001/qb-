---
artifact_type: workflow_module
status: verified
version: v2.0-stage2
generated_at: 2026-05-07T05:53:01Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Semantic Integration Workflow V2.0 — 固定工作流

## 1. 目标
把 Wallet-Intel 数据语义整合固定为 Hermes workflow，使 Hermes 后续遇到钱包数据采集分析、钱包结构分析、旧目录导入、数据护照、字段字典、handoff、旧路径映射等任务时，自动进入：

```text
wallet_intel_semantic_integration
```

本 workflow 不是普通目录整理流程。它以 token-level understanding 为完成标准，以事实/证据/推断/结论/handoff 分层为核心。

## 2. 全局硬边界

默认禁止，除非任务护照明确授权：

```text
扫描旧数据目录
复制旧数据
移动旧目录
删除旧目录
覆盖旧文件
修改业务代码
触发交易
读取或输出私钥、API key、token
执行 git push
```

## 3. 固定阶段总览

```text
阶段 0：任务护照生成
阶段 1：旧目录只读侦察
阶段 2：文件语义分类
阶段 3：按 token 建立索引
阶段 4：数据分层归属判断
阶段 5：高价值旧数据复制 / 登记
阶段 6：旧新路径映射
阶段 7：字段字典生成
阶段 8：数据护照生成
阶段 9：Hermes 读取入口生成
阶段 10：抽样验证
阶段 11：最终整合报告
阶段 12：记忆候选写入
```

## 4. 阶段规范

### 阶段 0：任务护照生成

- 阶段目标：明确任务范围、权限边界、输入输出、验证方式，防止 Wallet-Intel 被当作普通目录整理。
- 输入：用户任务文本；阶段1路由结果；控制面策略；目标路径声明。
- 允许动作：生成 task passport；列出允许/禁止动作；确认是否允许只读侦察/复制/代码修改；固定交易权限为否。
- 禁止动作：扫描旧目录；复制旧数据；移动/删除/覆盖旧文件；修改业务代码；触发交易。
- 输出物：task_passport.md；scope_boundaries；permission_matrix；checkpoint_00_task_passport。
- 验证标准：护照包含 task_type、范围、权限、输出物、验证方式、禁止事项。
- 失败处理：缺权限或范围不清时停止执行，生成 clarification_required 或 recovery_note。
- checkpoint：`checkpoint_00_task_passport`

### 阶段 1：旧目录只读侦察

- 阶段目标：在授权范围内只读识别旧目录结构与候选数据入口，不进行迁移。
- 输入：任务护照；允许只读侦察的路径白名单；旧目录只读规则。
- 允许动作：只读列目录；记录候选文件；记录疑似 token 数据入口；记录不可读/缺失项。
- 禁止动作：复制；移动；删除；覆盖；批量读取敏感文件；读取私钥/API key/token；越界扫描未授权目录。
- 输出物：legacy_readonly_scout_report.md；candidate_legacy_sources.csv；checkpoint_01_readonly_scout。
- 验证标准：报告能说明侦察范围、候选来源、未读取/跳过原因；没有文件内容迁移副作用。
- 失败处理：发现越权风险立即停止，写 route_failure_recovery_note，回到任务护照补授权。
- checkpoint：`checkpoint_01_readonly_scout`

### 阶段 2：文件语义分类

- 阶段目标：按语义而非旧目录名分类旧数据候选。
- 输入：只读侦察报告；候选文件列表；字段样本；命名/路径上下文。
- 允许动作：给每个候选文件标注语义类别：ingest/facts/evidence/inference/conclusion/handoff/reports/index/unknown。
- 禁止动作：仅按目录名强分类；把事实和推断混为一层；把 unknown 强行归类。
- 输出物：file_semantic_classification.csv；unknown_files_review.md；checkpoint_02_semantic_classification。
- 验证标准：每个文件有 semantic_layer、confidence、reason、source_path、review_flag。
- 失败处理：置信度不足标记 unknown/needs_review，不进入迁移计划。
- checkpoint：`checkpoint_02_semantic_classification`

### 阶段 3：按 token 建立索引

- 阶段目标：建立 token 级索引，使 Hermes 以后按 token 理解数据。
- 输入：语义分类结果；可识别 token_address/token_symbol/analysis_id 的候选文件。
- 允许动作：抽取/登记 token 线索；建立 token -> 文件 -> 语义层索引；标记无法识别 token 的文件。
- 禁止动作：凭猜测补 token；把多个 token 混入同一 passport；覆盖旧索引。
- 输出物：token_index.csv；unresolved_token_sources.md；checkpoint_03_token_index。
- 验证标准：每个 token 能列出候选 facts/evidence/inference/handoff 来源或明确缺失。
- 失败处理：token 无法识别则标记 unresolved，不强行导入。
- checkpoint：`checkpoint_03_token_index`

### 阶段 4：数据分层归属判断

- 阶段目标：将每个 token 的候选数据归入标准语义层。
- 输入：token_index；file_semantic_classification；字段字典候选。
- 允许动作：判定 ingest/facts/evidence/inference/conclusion/handoff/reports/index；标记缺层。
- 禁止动作：事实层写角色判断；推断层无证据等级；结论层无反证/失效条件。
- 输出物：token_layer_assignment.json；layer_gap_report.md；checkpoint_04_layer_assignment。
- 验证标准：每个 token 至少说明已有层、缺失层、争议层、下一步补查。
- 失败处理：冲突或混层时写 layer_conflict_report，停止进入复制/登记。
- checkpoint：`checkpoint_04_layer_assignment`

### 阶段 5：高价值旧数据复制 / 登记

- 阶段目标：在明确授权下 copy-only 导入高价值旧数据；未授权则只登记计划。
- 输入：任务护照复制授权；token_layer_assignment；legacy source；目标标准路径。
- 允许动作：copy-only；登记 checksum/size/source_path/target_path；保留旧目录只读；无授权时只生成 import_plan。
- 禁止动作：移动旧目录；删除旧文件；覆盖目标；未经授权复制；复制敏感密钥。
- 输出物：high_value_import_plan.md；copy_register.csv；checksum_manifest.csv；checkpoint_05_copy_register。
- 验证标准：每条导入有 old_path、new_path、checksum、copy_mode、layer、token_id。
- 失败处理：复制失败写 copy_failure_report；不重试破坏性命令；回到授权/路径检查。
- checkpoint：`checkpoint_05_copy_register`

### 阶段 6：旧新路径映射

- 阶段目标：建立 old_path -> new_path 可追溯映射。
- 输入：copy_register；import_plan；token_layer_assignment。
- 允许动作：生成旧新路径映射；记录转换规则；登记未导入原因。
- 禁止动作：丢失 old_path；只写新路径不写来源；覆盖旧映射无历史。
- 输出物：legacy_path_map.csv；old_to_new_trace.json；checkpoint_06_legacy_mapping。
- 验证标准：任一新文件可追溯到旧路径；未迁移项有 reason。
- 失败处理：缺 old_path 时标记 trace_missing，不允许进入 PASS。
- checkpoint：`checkpoint_06_legacy_mapping`

### 阶段 7：字段字典生成

- 阶段目标：建立字段语义、层级、来源、下游含义。
- 输入：已分类文件；样本字段；旧新路径映射；既有 schema。
- 允许动作：为字段生成 field_name/layer/type/meaning/source_field/downstream_usage。
- 禁止动作：把未知字段强解释；混淆事实字段和推断字段；记录密钥值。
- 输出物：field_dictionary.md/json；unknown_fields.md；checkpoint_07_field_dictionary。
- 验证标准：字段能解释属于哪一层、来自哪里、给谁读、缺失怎么标记。
- 失败处理：未知字段进入 unknown_fields，不阻塞全局但阻塞相关 token PASS。
- checkpoint：`checkpoint_07_field_dictionary`

### 阶段 8：数据护照生成

- 阶段目标：按 token 生成数据护照。
- 输入：token_index；layer_assignment；legacy_path_map；field_dictionary；gap_report。
- 允许动作：为每个 token 写数据分布、来源、事实/证据/推断/交接状态、缺失项。
- 禁止动作：把推断写成事实；把文件存在当理解；省略缺失项。
- 输出物：token_data_passport.md/json；checkpoint_08_data_passport。
- 验证标准：护照能回答该 token 有哪些数据、在哪里、来自哪里、缺什么。
- 失败处理：护照无法解释则 PARTIAL/FAIL，回到索引或字段字典。
- checkpoint：`checkpoint_08_data_passport`

### 阶段 9：Hermes 读取入口生成

- 阶段目标：建立后续模块读取优先级与入口。
- 输入：数据护照；标准目录；字段字典；旧路径映射。
- 允许动作：生成 readme/index/reader_contract；声明新标准入口优先、旧路径 fallback。
- 禁止动作：盲搜旧目录；跳过数据护照；让模块直接读旧目录。
- 输出物：hermes_read_entry.md；reader_contract.json；checkpoint_09_read_entry。
- 验证标准：后续模块能知道先读什么、fallback 何时使用、禁止盲搜。
- 失败处理：入口不完整则阻断后续自动读取。
- checkpoint：`checkpoint_09_read_entry`

### 阶段 10：抽样验证

- 阶段目标：验证 Hermes 是否按 token 理解数据。
- 输入：数据护照；字段字典；旧路径映射；handoff；事实/证据/推断数据。
- 允许动作：随机抽样 3-5 token；回答数据、事实、推断、来源、下游读取、缺失项。
- 禁止动作：只验证文件数量；执行者自证完成；跳过缺失项。
- 输出物：import_after_validation_report.md；sample_token_validation/*.md；checkpoint_10_sampling_validation。
- 验证标准：每个样本给 PASS/PARTIAL/FAIL；全局说明缺口。
- 失败处理：失败则写修复清单，回到对应阶段，不进入最终 PASS。
- checkpoint：`checkpoint_10_sampling_validation`

### 阶段 11：最终整合报告

- 阶段目标：汇总本次 Wallet-Intel 整合结果与边界。
- 输入：所有 checkpoint；验证报告；缺口报告。
- 允许动作：生成最终报告；列明完成/未完成/风险/后续计划。
- 禁止动作：声称迁移完成但无验证；隐藏失败；把 PARTIAL 写成 PASS。
- 输出物：final_integration_report.md；checkpoint_11_final_report。
- 验证标准：报告引用验证结果，边界清楚，可复验。
- 失败处理：验证未通过则最终结论只能 PARTIAL/FAIL。
- checkpoint：`checkpoint_11_final_report`

### 阶段 12：记忆候选写入

- 阶段目标：只将已验证规则写长期记忆，未验证规则写候选记忆。
- 输入：最终报告；验证报告；候选规则；用户确认。
- 允许动作：写 candidate_memory_rules；仅在验证通过且用户需要时写长期 memory/skill。
- 禁止动作：未验证规则直接写长期记忆；写入临时任务进度；写入敏感信息。
- 输出物：candidate_memory_rules.md；memory_write_decision.md；checkpoint_12_candidate_memory。
- 验证标准：区分 verified_rule / candidate_rule / rejected_rule；无敏感信息。
- 失败处理：未验证或用户未确认则只保留候选，不写长期记忆。
- checkpoint：`checkpoint_12_candidate_memory`


## 5. workflow 完成标准

只有满足以下条件，才可声明完成：

```text
任务护照存在；
每阶段 checkpoint 存在；
事实/证据/推断/结论/handoff 已分层；
每个 token 有索引或明确 unresolved；
旧新路径映射可追溯；
字段字典能解释字段；
数据护照能说明 token 数据；
Hermes 读取入口存在；
抽样 3-5 token 验证完成；
最终整合报告明确 PASS/PARTIAL/FAIL；
未验证规则只进入候选记忆。
```
