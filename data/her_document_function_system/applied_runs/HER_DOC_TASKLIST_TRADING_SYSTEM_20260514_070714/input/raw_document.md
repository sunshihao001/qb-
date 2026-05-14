# HER_DOC-skill 文档处理任务清单：SIKK 交易结构系统落地场景

## 0. 场景定义
- 场景名称：SIKK 交易结构系统文档治理与任务自动化
- 适用系统：HER 总控闭环交易结构系统 / Stable Trader OS / GMGN Runtime / Wallet-Intel
- 当前边界：safe-mode、paper-only、design/runtime document governance；不触发实盘、不签名、不 broadcast。
- 核心目标：把上传/新增/迭代的系统文档自动转为可执行任务清单、系统映射、缺口登记、下游实现队列、验收证据和治理候选。

## 1. HER_DOC 系统体系流程
1. O00 Orchestrator：接收文档与 operator_goal，建立 pipeline run，执行安全边界检查。
2. K00 Knowledge Intake：文档摄取、文档护照、资产分类、系统映射、语料索引。
3. F00 Function Mapping：把文档要求映射到控制器、模块、runner、数据平面、验收平面。
4. V00 Validation Evidence：检查字段、文件、实现、测试、证据缺口，建立 gap register。
5. A00 Acceptance：区分 ACCEPTED / READY_WITH_GAPS / BLOCKED，禁止虚假完成声明。
6. H00 Handoff：把任务拆给下游控制器或实现模块。
7. U00 Review / Upgrade：把缺口转成升级队列和回归验证计划。
8. G00 Governance：把反复出现的问题沉淀为规则、模板、准入门禁候选。

## 2. 文档任务清单

### DOC-TASK-001：新增文档 intake
- 目标：把用户提供的系统/策略/方法论文档登记为标准文档资产。
- 输入：原始 Markdown/PDF/JSON/聊天记录；operator_goal。
- HER_DOC 阶段：O00 → K00。
- 自动化动作：生成 source registry、document passport、corpus index。
- 输出物：`document_passport`、`source_manifest`、`intake_report`。
- 验收标准：文档来源、目标、类型、影响面、限制边界完整。
- 优先级：P0。
- 状态：READY_TO_RUN。

### DOC-TASK-002：六类资产拆解
- 目标：按用户偏好的 6 类资产吸收文档。
- 输入：K00 文档护照与原文。
- HER_DOC 阶段：K00。
- 自动化动作：抽取判断逻辑资产、字段需求资产、反证规则资产、量化模型资产、行为推断资产、输出模板资产。
- 输出物：asset_breakdown.json / methodology_passport.md。
- 验收标准：每类资产至少有 evidence_ref；没有则标为 gap，不硬补。
- 优先级：P0。
- 状态：READY_TO_RUN。

### DOC-TASK-003：系统平面映射
- 目标：明确文档影响 HER 哪些控制器和平面。
- 输入：asset_breakdown、document_passport。
- HER_DOC 阶段：F00。
- 自动化动作：映射到 Methodology Plane、Domain Plane、Data Plane、Trace Plane、Acceptance Plane、Handoff Plane、P01-P10 Controllers。
- 输出物：function_mapping.json、system_mapping.json。
- 验收标准：每条需求都有 target_controller / target_module / evidence_source。
- 优先级：P0。
- 状态：READY_TO_RUN。

### DOC-TASK-004：字段合约与数据缺口生成
- 目标：把文档中的字段需求转为可执行字段合约和缺口。
- 输入：字段需求资产、现有数据目录/模块接口。
- HER_DOC 阶段：F00 → V00。
- 自动化动作：生成 required_fields、optional_fields、field_source_map、missing_fields。
- 输出物：field_contract.json、gap_register.json。
- 验收标准：缺字段必须标记 missing/degraded/blocked；不能用推断值冒充事实。
- 优先级：P0。
- 状态：READY_TO_RUN。

### DOC-TASK-005：规则模板与反证门禁
- 目标：把判断逻辑与反证规则转成可验证规则模板。
- 输入：判断逻辑资产、反证规则资产。
- HER_DOC 阶段：F00 → V00。
- 自动化动作：生成 rule_template、negative_evidence_gate、blocked_claims。
- 输出物：rules/*.yaml、validation_evidence.json。
- 验收标准：每个正向判断必须有至少一个反证路径。
- 优先级：P1。
- 状态：READY_TO_RUN。

### DOC-TASK-006：输出合约与报告模板
- 目标：统一最终报告、handoff、dashboard、Telegram 回调输出格式。
- 输入：输出模板资产、现有 reports/site/index 输出。
- HER_DOC 阶段：F00 → A00。
- 自动化动作：生成 output_contract、report_template、handoff_packet schema。
- 输出物：output_contract.json、final_report_template.md、handoff.schema.json。
- 验收标准：输出必须包含状态、证据、缺口、下一步；不得只输出结论。
- 优先级：P1。
- 状态：READY_TO_RUN。

### DOC-TASK-007：下游实现队列
- 目标：把未落地文档需求分发为模块/控制器实现任务。
- 输入：gap_register、function_mapping、acceptance_result。
- HER_DOC 阶段：H00。
- 自动化动作：生成 downstream_queue，按控制器/模块/优先级排序。
- 输出物：downstream_queue.json、task_package_*.json。
- 验收标准：每个 queue item 有 owner_controller、input_contract、output_contract、acceptance_gate。
- 优先级：P0。
- 状态：READY_TO_RUN。

### DOC-TASK-008：复盘升级与治理沉淀
- 目标：把文档处理过程中反复出现的缺口沉淀为系统规则或 skill 更新。
- 输入：upgrade_queue、governance_candidates、历史 gap。
- HER_DOC 阶段：U00 → G00。
- 自动化动作：生成 governance rule candidate、skill patch candidate、regression guard。
- 输出物：upgrade_queue.json、governance_candidates.json。
- 验收标准：治理候选只能是 candidate，未人工确认不得声明 POLICY_ACTIVE。
- 优先级：P2。
- 状态：READY_TO_RUN。

## 3. 实际应用场景落地：交易系统文档进入可执行闭环

### 场景 A：用户上传“钱包结构新方法论”
- K00：拆成六类资产。
- F00：映射到 Wallet-Fact、Behavior-Inference、P02/P03/P06。
- V00：检查是否已有字段来源、成本区计算、同源组证据。
- H00：把缺失字段派发给 Wallet-Fact，把行为推断规则派给 Behavior-Inference。
- A00：只能 READY_WITH_GAPS，除非字段、规则、测试、报告全部有证据。

### 场景 B：用户上传“P01 数据事实控制器升级文档”
- K00：登记文档来源与目标。
- F00：映射到 Data Plane、Trace Plane、P01 Controller。
- V00：检查 raw/normalized/summary 是否有合约和 trace。
- H00：生成代码实现、测试、迁移任务。

### 场景 C：用户要求“把运行时流程收编到 HER 总控”
- K00：吸收 runtime manifest / sikk_live_run 说明。
- F00：映射 Runtime P0-P10 到 Stable P00-P09/P01-P10。
- V00：检查 run manifest、token_status、process_trace、paper_live、reports 是否满足证据链。
- U00/G00：把缺失 trace、acceptance、handoff 形成升级任务。

## 4. 当前自动化执行目标
- 输入本文档作为 source_document。
- operator_goal：建立 HER_DOC 文档任务清单，并用 HER 文档功能管线处理，产出 READY_WITH_GAPS 证据包。
- 预期状态：HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS 或 O00_RUN_DOCUMENT_READY_WITH_GAPS。
- 禁止声明：TESTED、RUNNER_BOUND、POLICY_ACTIVE、PIPELINE_ACCEPTED、SYSTEM_FULLY_IMPLEMENTED，除非有真实证据。
