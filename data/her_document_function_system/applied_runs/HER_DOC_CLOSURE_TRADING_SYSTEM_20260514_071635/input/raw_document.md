# HER_DOC-skill 闭环推进任务包：SIKK 交易结构系统文档处理落地

## 0. 本轮闭环目标
- run_id: `HER_DOC_CLOSURE_TRADING_SYSTEM_20260514_071635`
- source: 上一轮 `HER_DOC_TASKLIST_TRADING_SYSTEM` 的 A00/H00/V00/F00 输出
- 主目标：继续按照 HER_DOC-skill 的系统体系流程自动化处理任务，把文档任务从“清单 + READY_WITH_GAPS”推进到“下游缺口闭环任务包 + 可验收应用场景”。
- 边界：safe-mode、paper-only、document-governance only；不触发真实交易、不签名、不 broadcast、不声明 production ready。

## 1. 输入证据
- prior_tasklist: `system/her_document_function_system/application_scenarios/trading_system_doc_ops/HER_DOC_TASKLIST_TRADING_SYSTEM.md`
- prior_status: `system/her_document_function_system/application_scenarios/trading_system_doc_ops/HER_DOC_TASKLIST_EXECUTION_STATUS.md`
- prior_run_dir: `data/her_document_function_system/applied_runs/HER_DOC_TASKLIST_TRADING_SYSTEM_20260514_070714`
- prior_gap_register: `v00/gap_register.json`
- prior_downstream_queue: `h00/downstream_queue.json`
- prior_acceptance: `a00/a00_acceptance_result.json`
- prior_task_package: `f00/implementation_task_package.json`

## 2. HER_DOC 闭环处理流程

### O00：闭环编排
- 接收本文件和 `operator_goal_closure.json`。
- 读取 prior run 的 gap、queue、acceptance、task package。
- 建立新 run，输出本轮 `run_summary`、trace、audit。
- 禁止把上一轮 READY_WITH_GAPS 误标为 ACCEPTED。

### K00：闭环文档摄取
- 将本闭环任务包登记为新的 source document。
- 把上一轮 gap/queue/acceptance 作为 evidence_refs，而不是聊天记忆。
- 生成本轮 document passport、corpus index、system mapping、handoff packet。

### F00：功能实现映射
- 将 3 个 open gaps 转成 3 条可执行实现链：
  1. `gap_001 / missing_implementation_evidence` → IMPLEMENT-001：实现证据索引与测试证据索引。
  2. `gap_002 / real_tool_execution_limited_to_safe_mode` → IMPLEMENT-002：真实文档批处理 safe runner。
  3. `gap_003 / governance_candidate_not_applied` → IMPLEMENT-003：治理候选人工审批包。
- 每条实现链必须有 input_contract、output_contract、acceptance_gate、forbidden_claims。

### V00：验证证据
- 验证本轮是否至少形成：
  - gap-to-task trace
  - task-to-application-scenario trace
  - acceptance criteria
  - downstream handoff queue
  - governance candidate review boundary
- 若没有真实实现代码或测试证据，继续保留 READY_WITH_GAPS。

### A00：验收判断
- 文件级：闭环文档与 goal 存在。
- 结构级：O00/K00/F00/V00/A00/H00/U00/G00 均有输出。
- 语义级：每个 gap 均有下游任务与应用场景。
- 消费级：下游队列已生成，但未执行则不能 ACCEPTED。
- 运行级：只允许 safe-mode run 证据，不允许生产运行声明。

### H00：下游交接
- 生成下一轮闭环队列：
  - H00-CLOSE-001：实现证据索引器/绑定器。
  - H00-CLOSE-002：批量文档 safe-mode runner。
  - H00-CLOSE-003：治理候选审批包生成器。
- 队列状态：`QUEUE_READY_WITH_GAPS`。

### U00：复盘升级
- 把上一轮 gap 的根因转成升级项：
  - 文档任务清单能生成，但缺少 implementation evidence binder。
  - safe-mode 能跑单文档，但缺少批处理/统一索引。
  - governance candidate 能生成，但缺少 approval workflow。

### G00：治理沉淀
- 生成候选规则：任何 HER_DOC 文档任务必须输出 gap-to-task-to-acceptance trace。
- 未人工审批前状态保持 `CANDIDATE`，不得写入 active policy。

## 3. 实际应用场景闭环

### 应用场景 1：钱包结构方法论文档自动入库闭环
- 输入：钱包结构判断逻辑、字段需求、反证规则。
- HER_DOC 处理：K00 六类资产拆解 → F00 映射 Wallet-Fact/Behavior-Inference/P02-P04 → V00 检查字段证据 → H00 派发实现任务。
- 闭环输出：字段合约、规则模板、缺口队列、验收标准。
- 不允许：直接把方法论文档变成买入/卖出结论。

### 应用场景 2：运行时流程收编到 HER 总控闭环
- 输入：`sikk_live_run.py` runtime manifest、paper_live、quote_security、state_machine 输出说明。
- HER_DOC 处理：K00 摄取 runtime 文档 → F00 映射 Runtime P0-P10 到 HER/P01-P10 → V00 查 trace/acceptance/handoff 缺口 → U00/G00 生成升级候选。
- 闭环输出：runner binding 任务、trace matrix 任务、acceptance evidence 任务。
- 不允许：把 paper runtime 独立当成完整系统。

### 应用场景 3：HER_DOC 自身任务治理闭环
- 输入：文档任务清单、operator_goal、gap register、downstream_queue。
- HER_DOC 处理：每轮 run 自动形成下一轮闭环任务包。
- 闭环输出：`READY_WITH_GAPS → 下游任务 → 验证证据 → A00 判断 → 新 gap/候选治理规则`。
- 不允许：没有实现证据就声称 fully automated。

## 4. 本轮输出要求
- 本文件通过 `tools/o00_run_document_main.py --safe-mode` 运行。
- 再通过 `tools/o00_cli.py run-document --safe-mode` 做 O00 验证。
- 检查输出：A00、V00、H00、O00 final report。
- 生成本轮状态文档：`HER_DOC_CLOSURE_EXECUTION_STATUS.md`。

## 5. 预期状态
- 合法预期：`HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS` 或 `O00_RUN_DOCUMENT_READY_WITH_GAPS`。
- 允许声明：闭环任务包已生成、safe-mode 已验证、下一轮下游任务明确。
- 禁止声明：`PRODUCTION_READY`、`FULLY_AUTOMATED`、`POLICY_ACTIVE`、`LIVE_READY`、`PIPELINE_ACCEPTED`、`SYSTEM_FULLY_IMPLEMENTED`。
