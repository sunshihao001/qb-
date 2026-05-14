# 交易系统体系再摄取与落地审计方案

## 用刚建立的文档自动化处理系统，全面扫描 SIKK / HER / GPT 研究资料是否真正落地

---

## 0. 初步判断

你现在的问题不是“交易系统没有设计”，而是：

```text
大量 GPT 研究资料已经形成解释性认知，
但没有被系统性转化为：
controller / schema / contract / runner / trace / acceptance / handoff / paper runtime / review input。
```

我刚才先检索了一轮你上传过的相关资料，已经能确认三个关键事实：

1. 你已有 `SIKK Stable Trader OS 专业化阶段总表 v1.0`，其中明确系统目标不是寻找机会，而是连续剔除低质量、错误场景、假成交、派发风险、疲劳拖延和错误位置，只保留极少数 `A+P1` 且证据链未被否决的样本。文件里也已经定义了 0-9 阶段、核心输出和下游读取关系。
    
2. 你已有 `/root/sikk-gmgn` 的系统目录清单，里面显示代码、数据、报告、knowledge、research_loop、docs、modules、tests、legacy 数据都已经存在，而且有旧运行数据、paper runner、quote/security、GMGN token report、live orchestrator、knowledge absorption 等脚本基础。
    
3. 你之前已经意识到不能把 10 个阶段机械做成 10 个独立 Skill，而应该是“总控 Skill + Phase Controller + Atomic Skill + 统一 contracts/schemas/status/handoff/audit”。这说明你的方向不是缺概念，而是缺“解释资料 → 功能对象 → 运行链路”的再编译。
    

所以这次不应该继续写一个新的说明文档，而应该启动：

```text
SIKK Knowledge-to-Runtime Full System Rescan
交易系统知识到运行体系全量再扫描
```

---

# 1. 本次扫描的总目标

这次扫描要回答 6 个问题：

```text
1. 之前上传 / 研究的 GPT 资料，到底有哪些核心机制？
2. 哪些已经被落实到代码、schema、contract、runner、报告？
3. 哪些只是写在文档里，没有被系统调用？
4. 哪些字段、目录、合约、handoff、trace、acceptance 缺失？
5. 哪些旧脚本已经存在，但没有纳入新体系？
6. 下一步如何让真实 token 数据跑完整条链？
```

最终输出不是普通总结，而是：

```text
交易系统全量审计报告
文档功能化索引
阶段落地矩阵
缺口矩阵
旧模块吸收计划
R00 可运行任务包
HER 可复制执行指令
```

---

# 2. 正确扫描框架

这次应该按你刚建立的文档处理系统来做：

```text
K00 文档摄取与任务化
  ↓
K01 文档护照与来源登记
  ↓
K02 语义切块与概念抽取
  ↓
K03 功能对象抽取
  ↓
K04 系统映射与阶段对齐
  ↓
K05 Controller / Schema / Contract 候选生成
  ↓
K06 HER 任务包编译
  ↓
K07 验证 / 缺口 / 验收绑定
  ↓
K08 知识索引与复用
```

然后把结果映射到交易系统：

```text
Control Planes
P01-P10 Phase Controllers
I01-I05 Integration Program
R00 Plane-aware Runtime Orchestrator
CPO Continuous Paper-only Operation
```

---

# 3. 本次全量扫描范围

## A. 文档资料层

重点扫描：

```text
GPT 研究资料
ChatGPT 分享链接提取摘要
HER 任务计划
system_methodology_blueprint.md
K00-K08 文档处理体系
P00 / Bootstrap / Governance / Domain / Data / Full Control / Trace / Acceptance / Handoff
P01-P10 Controller 文档
I01-I05 Integration 文档
R00 Runtime Orchestrator 文档
CPO 持续纸面运行文档
```

目标：

```text
判断这些文档是否只是解释性内容，还是已经变成系统对象。
```

---

## B. 代码与模块层

根据目录清单，当前已有旧脚本基础，例如：

```text
run_sikk_gmgn_pipeline.py
sikk_live_orchestrator.py
sikk_gmgn_token_report.py
sikk_paper_live_runner.py
sikk_paper_trading_engine.py
sikk_quote_security_review.py
sikk_system_audit.py
sikk_knowledge_absorption.py
sikk_her_task_router.py
sikk_task_package_builder.py
sikk_same_source_grouping.py
sikk_operator_psychology_engine.py
```

这些不能简单丢弃，也不能继续散落使用。

要逐个判定：

```text
它属于哪个阶段？
是否可升级成 Atomic Skill？
是否可被 Phase Controller 调用？
是否可被 R00 调度？
是否有 schema / contract / trace / acceptance？
是否仍是 legacy compatibility？
```

---

## C. 数据与运行层

重点扫描：

```text
data/gmgn_candidates_live_run/
data/source_wallet_bot/
data/intel_bot/
data/paper_runtime/
data/runtime_orchestration/
旧 paper_live 输出
旧 candidate_signal_outputs
旧 quote/security 输出
旧 token_readiness_result
旧 trade_confirmation_ticket
```

目标：

```text
判断旧数据是否能作为 replay / sample library / P09 复盘输入，
还是只能作为 legacy reference。
```

---

# 4. 这次扫描应该输出的核心矩阵

## 4.1 文档功能化矩阵

```yaml
document_functionalization_matrix:
  document_id: string
  title: string
  document_type:
    - EXPLANATORY_DOC
    - METHODOLOGY_DOC
    - SYSTEM_DESIGN_DOC
    - PHASE_CONTROLLER_DOC
    - TASK_INSTRUCTION_DOC
    - RUNTIME_REPORT
  extracted_mechanisms: list
  mapped_system_layer:
    - K00_K08
    - CONTROL_PLANE
    - P01_P10
    - I01_I05
    - R00
    - CPO
  current_status:
    - DOCUMENT_ONLY
    - PARTIALLY_FUNCTIONALIZED
    - FUNCTIONALIZED_NOT_CONNECTED
    - CONNECTED_TO_RUNTIME
    - OBSOLETE
  required_action:
    - CREATE_CONTROLLER_CANDIDATE
    - CREATE_SCHEMA
    - CREATE_CONTRACT
    - CREATE_RUNNER_BINDING
    - CREATE_ACCEPTANCE
    - CREATE_HANDOFF
    - ARCHIVE_REFERENCE_ONLY
```

---

## 4.2 阶段落地矩阵

```yaml
phase_implementation_matrix:
  phase_id: P01
  phase_name: Candidate Intake / Data Fact / Wallet / Chip / Evidence / Scenario / Strategy / Risk / Review / Upgrade
  required_outputs: list
  existing_documents: list
  existing_code_modules: list
  existing_data_outputs: list
  schema_exists: boolean
  contract_exists: boolean
  runner_exists: boolean
  trace_exists: boolean
  acceptance_exists: boolean
  handoff_exists: boolean
  runtime_connected: boolean
  gap_level:
    - BLOCKING
    - HIGH
    - MEDIUM
    - LOW
    - COMPLETE
```

---

## 4.3 旧模块吸收矩阵

```yaml
legacy_module_absorption_matrix:
  module_path: string
  module_name: string
  current_role: string
  detected_functions: list
  target_layer:
    - P01
    - P02
    - P03
    - P04
    - P05
    - P06
    - P07
    - P08
    - P09
    - P10
    - I04
    - R00
    - CPO
  absorption_action:
    - KEEP_AS_LEGACY_READONLY
    - WRAP_AS_ATOMIC_SKILL
    - MIGRATE_TO_MODULES
    - BIND_TO_PHASE_RUNNER
    - BIND_TO_R00
    - RETIRE_AFTER_REPLAY
  missing_requirements:
    - schema
    - contract
    - trace
    - acceptance
    - handoff
    - tests
```

---

## 4.4 真实 Token 可运行缺口矩阵

```yaml
token_runtime_gap_matrix:
  required_runtime_object:
    - runtime_plane_context_manifest
    - runtime_readiness_gate
    - runtime_run_manifest
    - token_case_manifest
    - phase_execution_plan
    - phase_execution_record
    - handoff_resolution_record
    - p08_permission_gate
    - paper_runtime_invocation_record
    - p09_review_trigger
    - p10_upgrade_review_trigger
    - full_pipeline_report
  exists_now: boolean
  source_if_exists: string | null
  missing_reason: string
  blocking_runtime: boolean
  fix_task: string
```

---

# 5. 当前初步诊断

根据已检索材料，当前状态大概率是：

|模块|状态|判断|
|---|---|---|
|系统目标|已明确|已有 Stable Trader OS 总目标|
|阶段划分|已明确|0-9 / P01-P10 思路成熟|
|目录清单|已有|`/root/sikk-gmgn` 已有全目录 inventory|
|旧代码基础|已有|paper、quote/security、GMGN、live orchestrator、audit 等脚本存在|
|Skill 结构认知|已明确|已从“阶段=Skill”升级为“Phase Controller + Atomic Skill”|
|文档功能化体系|刚建立|需要落地成 K00-K08 runner|
|控制平面|已设计|需要被 R00 runtime 读取|
|I01-I05|已设计|需要确认是否有实际文件和 acceptance|
|R00|已设计|还需要 HER 落地代码骨架|
|真实 token 全流程运行|未完成|缺 R00 plane-aware runtime|
|持续 paper 运行|不能直接启动|必须先有 R00 生成稳定 run/sample/metrics|

核心问题：

```text
系统现在不是“没有体系”，而是“体系没有被重新编译成可运行索引和 R00 执行入口”。
```

---

# 6. 应该怎么全面扫描

建议让 HER 执行 5 轮扫描。

---

## 第 1 轮：文档再摄取

目标：

```text
把所有 GPT / HER / SIKK 研究文档做 document_passport。
```

输出：

```text
document_passport_index.yaml
document_type_classification_report.md
explanatory_doc_list.yaml
methodology_doc_list.yaml
system_design_doc_list.yaml
phase_controller_doc_list.yaml
runtime_report_doc_list.yaml
```

重点判断：

```text
哪些文档只是解释；
哪些可以生成功能对象；
哪些可以生成 controller / schema / contract；
哪些只能 reference-only。
```

---

## 第 2 轮：功能对象抽取

目标：

```text
把文档中的机制抽成 functional_object_candidate。
```

输出：

```text
functional_object_registry.yaml
control_rule_candidate_registry.yaml
field_candidate_registry.yaml
schema_candidate_registry.yaml
contract_candidate_registry.yaml
acceptance_candidate_registry.yaml
handoff_candidate_registry.yaml
```

重点判断：

```text
文档里的认知有没有变成字段、合约、验收、runner、handoff。
```

---

## 第 3 轮：交易系统阶段映射

目标：

```text
把所有文档和功能对象映射到控制平面、P01-P10、I01-I05、R00、CPO。
```

输出：

```text
system_mapping_matrix.yaml
phase_implementation_matrix.yaml
control_plane_mapping_matrix.yaml
runtime_orchestration_mapping_matrix.yaml
cpo_mapping_matrix.yaml
```

重点判断：

```text
哪些阶段文档很多但代码少；
哪些代码存在但没有纳入阶段；
哪些阶段有输出但无 handoff；
哪些模块有功能但无 acceptance。
```

---

## 第 4 轮：代码 / 数据 / 目录落地审计

目标：

```text
把 /root/sikk-gmgn 现有文件和新体系对齐。
```

输出：

```text
legacy_module_absorption_matrix.yaml
runtime_data_absorption_matrix.yaml
canonical_vs_legacy_path_report.md
module_to_phase_binding_report.md
missing_runtime_object_report.md
```

重点判断：

```text
旧脚本是否迁移；
旧数据是否只读；
哪些模块能被 R00 调用；
哪些输出能进入 P09 replay；
哪些数据不能再作为主写路径。
```

---

## 第 5 轮：R00 可运行链路生成

目标：

```text
生成真实 token 全流程运行任务包。
```

输出：

```text
r00_runtime_orchestration_gap_report.md
r00_implementation_task_packet.md
r00_single_token_dry_run_acceptance.md
r00_batch_candidate_acceptance.md
r00_cpo_binding_acceptance.md
```

重点判断：

```text
现在真实 token 为什么不能跑；
缺哪些 runner；
缺哪些 input；
缺哪些 handoff；
缺哪些 paper runtime invocation；
缺哪些 P09/P10 trigger。
```

---

# 7. 这次扫描的最终报告结构

建议最终输出一个总报告：

```text
/root/sikk-gmgn/reports/system_rescan/
  sikk_full_system_rescan_report.md
  document_functionalization_matrix.yaml
  phase_implementation_matrix.yaml
  control_plane_runtime_binding_matrix.yaml
  legacy_module_absorption_matrix.yaml
  token_runtime_gap_matrix.yaml
  r00_required_fix_task_packet.md
  next_72h_execution_plan.md
```

---

# 8. 给 HER 的正式任务书

直接复制给 HER：

```text
任务名称：
SIKK Full System Rescan：基于 Knowledge Processing Program 的交易系统全量再摄取与落地审计

目标：
对 /root/sikk-gmgn 当前交易系统体系进行一次全量再扫描。不要普通总结，不要只看表面文档。必须按照 Knowledge Processing Program 的 K00-K08 流程，把之前 GPT / HER / SIKK 研究资料重新处理为 document_passport、functional_object、system_mapping、controller_candidate、schema_candidate、contract_candidate、runner_binding_candidate、acceptance_candidate、handoff_candidate，并进一步映射到 Control Planes、P01-P10、I01-I05、R00 Plane-aware Runtime Orchestrator、Continuous Paper-only Operation。最终判断哪些内容只是解释性文档，哪些已经落地到代码，哪些存在代码但没有被系统调用，哪些缺 schema / contract / trace / acceptance / handoff，为什么真实 token 数据仍不能跑完整流程。

工作边界：
1. 不允许删除旧数据。
2. 不允许移动 legacy runtime 数据。
3. 不允许修改生产规则。
4. 不允许真实交易。
5. 不允许 wallet signing。
6. 不允许 auto order。
7. 不允许 auto deploy。
8. 本任务只做扫描、映射、审计、候选任务包生成。
9. 所有旧数据只能 read-only 读取。
10. 所有结论必须附 source path。
11. 所有缺口必须给出 fix task。
12. 所有功能候选必须标记 owner layer / owner phase。
13. 不允许把解释性文档直接当作已落地功能。

读取范围：
1. /root/sikk-gmgn/docs/
2. /root/sikk-gmgn/research_loop/
3. /root/sikk-gmgn/knowledge/
4. /root/sikk-gmgn/reports/
5. /root/sikk-gmgn/audits/
6. /root/sikk-gmgn/tasks/
7. /root/sikk-gmgn/modules/
8. /root/sikk-gmgn/scripts/
9. /root/sikk-gmgn/tools/
10. /root/sikk-gmgn/data/gmgn_candidates_live_run/
11. /root/sikk-gmgn/data/source_wallet_bot/
12. /root/sikk-gmgn/data/intel_bot/
13. /root/sikk-gmgn/data/paper_runtime/
14. /root/sikk-gmgn/system/
15. /root/sikk-gmgn/skills/ 如果存在

执行流程：
第一轮：文档护照与分类
- 扫描所有 .md / .txt / .yaml / .json 中的系统设计、研究资料、任务包、报告。
- 输出 document_passport_index.yaml。
- 每份文档标记 document_type：EXPLANATORY_DOC / METHODOLOGY_DOC / SYSTEM_DESIGN_DOC / PHASE_CONTROLLER_DOC / TASK_INSTRUCTION_DOC / RUNTIME_REPORT / UPGRADE_PROPOSAL / FIELD_MODEL_DOC。
- 标记 processing_route：FULL_FUNCTIONALIZATION / PHASE_MAPPING / TASK_PACKAGE_GENERATION / REFERENCE_ONLY。

第二轮：功能对象抽取
- 从每份文档抽取 mechanism、control_rule、field_candidate、schema_candidate、contract_candidate、acceptance_candidate、handoff_candidate、runner_candidate。
- 输出 functional_object_registry.yaml。
- 不允许只生成摘要。

第三轮：系统映射
- 将每个功能对象映射到：
  K00-K08
  P00
  Bootstrap / Governance / Domain / Data / Full Control / Trace / Acceptance / Handoff Plane
  P01-P10
  I01-I05
  R00
  CPO
- 输出 system_mapping_matrix.yaml。

第四轮：阶段落地审计
- 对 P01-P10 分别检查：
  是否有 controller
  是否有 schema
  是否有 contract
  是否有 runner
  是否有 trace
  是否有 acceptance
  是否有 handoff
  是否有 runtime data output
  是否有下游读取
- 输出 phase_implementation_matrix.yaml。

第五轮：控制平面落地审计
- 检查 Bootstrap / Governance / Domain / Data / Full Control / Trace / Acceptance / Handoff Plane 是否有正式文件。
- 检查它们是否被 R00 / runner / CPO 读取。
- 输出 control_plane_runtime_binding_matrix.yaml。

第六轮：旧模块吸收审计
- 扫描 run_sikk_gmgn_pipeline.py、sikk_live_orchestrator.py、sikk_gmgn_token_report.py、sikk_paper_live_runner.py、sikk_quote_security_review.py、sikk_system_audit.py、sikk_knowledge_absorption.py、sikk_her_task_router.py 等旧脚本。
- 判断每个脚本属于哪个阶段或运行层。
- 判断是否应 KEEP_AS_LEGACY_READONLY / WRAP_AS_ATOMIC_SKILL / MIGRATE_TO_MODULES / BIND_TO_R00 / RETIRE_AFTER_REPLAY。
- 输出 legacy_module_absorption_matrix.yaml。

第七轮：真实 token runtime 缺口审计
- 检查是否具备：
  runtime_plane_context_manifest
  runtime_readiness_gate
  runtime_run_manifest
  token_case_manifest
  phase_execution_plan
  phase_execution_record
  handoff_resolution_record
  p08_permission_gate
  paper_runtime_invocation_record
  p09_review_trigger
  p10_upgrade_review_trigger
  operation_metrics_update
  sample_library_update
  full_pipeline_plane_aware_report
- 输出 token_runtime_gap_matrix.yaml。

第八轮：生成 R00 落地任务包
- 根据缺口生成 r00_required_fix_task_packet.md。
- 必须包含：
  文件路径
  需要创建的 schema
  需要创建的 runner
  需要绑定的旧模块
  需要添加的测试
  单 token dry-run 验收命令
  batch paper-only 验收命令
  scheduled-paper-cycle 验收命令
  hard negative rules
  acceptance criteria

输出目录：
/root/sikk-gmgn/reports/system_rescan/

必须输出：
1. sikk_full_system_rescan_report.md
2. document_passport_index.yaml
3. document_functionalization_matrix.yaml
4. functional_object_registry.yaml
5. system_mapping_matrix.yaml
6. phase_implementation_matrix.yaml
7. control_plane_runtime_binding_matrix.yaml
8. legacy_module_absorption_matrix.yaml
9. runtime_data_absorption_matrix.yaml
10. token_runtime_gap_matrix.yaml
11. r00_required_fix_task_packet.md
12. next_72h_execution_plan.md

验收标准：
1. 每份重要文档都有 document_passport。
2. 每个核心机制都被抽成 functional_object。
3. 每个功能对象都映射到系统层或阶段。
4. 每个 P01-P10 阶段都有落地状态。
5. 每个控制平面都有是否被 runtime 读取的判断。
6. 每个旧脚本都有吸收策略。
7. 每个 runtime 缺口都有 fix task。
8. 明确说明为什么当前真实 token 数据不能完整跑。
9. 明确说明 R00 需要补哪些文件和 runner。
10. 明确给出下一步 72 小时执行顺序。
```

---

# 9. 我对当前系统的重新判断

```text
交易系统体系：基本完成设计层
文档自动化处理体系：刚完成设计，需要落地扫描
旧资料理解：不充分，很多仍停留在解释层
旧代码：已有不少可用资产，但没有全部接入新阶段体系
控制平面：已设计，但还没有成为 runtime 硬约束
真实 token 运行：关键缺口仍是 R00 Plane-aware Runtime Orchestrator
持续 paper：需要 R00 先稳定生成 run/sample/metrics
```

最重要的判断：

```text
下一步不是继续扩理论。
下一步是让 HER 做一次 SIKK Full System Rescan，
然后基于扫描结果落地 R00。
```

---

# 10. 本次认知升级点

1. **现在要做的是“再摄取 + 落地审计”，不是继续写新阶段。**
    
2. **之前 GPT 研究资料必须重新经过 K00-K08，转成 functional object。**
    
3. **判断是否落实，不能看有没有文档，要看有没有 schema / contract / runner / trace / acceptance / handoff。**
    
4. **旧脚本不是废弃资产，要通过 legacy_module_absorption_matrix 判断吸收方式。**
    
5. **真实 token 跑不起来的核心不是缺策略，而是缺 R00 runtime 链路。**
    
6. **控制平面必须被 R00 读取，否则只是设计文档。**
    
7. **全系统扫描完成后，才能准确知道哪些资料只是表面落实，哪些真正进入运行体系。**