# HER_DOC 任务清单实际应用推进状态

## 1. 本次已建立的输入资产
- source_document: `/root/sikk-gmgn/system/her_document_function_system/application_scenarios/trading_system_doc_ops/HER_DOC_TASKLIST_TRADING_SYSTEM.md`
- operator_goal: `/root/sikk-gmgn/system/her_document_function_system/application_scenarios/trading_system_doc_ops/operator_goal.json`

## 2. 本次已执行的自动化管线
- applied pipeline: `tools/o00_run_document_main.py`
- mode: `--safe-mode`
- run_dir: `/root/sikk-gmgn/data/her_document_function_system/applied_runs/HER_DOC_TASKLIST_TRADING_SYSTEM_20260514_070714`
- final_status: `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`

同时执行 O00 CLI run-document 验证：
- cli pipeline_run_id: `o00_run_20260514_070746_120297`
- cli final_status: `PIPELINE_READY_WITH_GAPS`
- cli system_status_code: `O00_RUN_DOCUMENT_READY_WITH_GAPS`

## 3. HER_DOC 阶段完成情况
- K00: 已生成 `document_passport.json`、`system_mapping.json`、`corpus_index.json`、`k00_handoff_packet.json`
- F00: 已生成 `function_mapping.json`、`implementation_task_package.json`、`required_system_assets.json`
- V00: 已生成 `gap_register.json`、`validation_matrix.json`、`evidence_report.json`
- A00: 已生成 `a00_acceptance_result.json`、`acceptance_matrix.json`、`readiness_certificate.json`
- H00: 已生成 `downstream_queue.json`、`routing_decision.json`、`h00_handoff_packets.json`
- U00: 已生成 `upgrade_queue.json`、`root_cause_analysis.json`、`learning_index.json`
- G00: 已生成 `governance_candidates.json`、`policy_rules_update.json`
- O00: 已生成 `run_summary.json`、`final_report.md`、`trace.jsonl`、`audit.jsonl`

## 4. 当前验收状态
- blocking_gaps: `[]`
- non_blocking_gaps:
  - `missing_implementation_evidence`
  - `real_tool_execution_limited_to_safe_mode`
  - `governance_candidate_not_applied`
- ready_for_next_run: `true`
- ready_for_production: `false`

## 5. 已生成的下游队列
- queue_item_001: `gap_001` → `U00`; priority=`P1_HIGH`; task_type=`REVIEW_AND_UPGRADE`
- queue_item_002: `gap_002` → `H00`; priority=`P2_MEDIUM`; task_type=`ROUTED_GAP_REVIEW`
- queue_item_003: `gap_003` → `G00`; priority=`P2_MEDIUM`; task_type=`ROUTED_GAP_REVIEW`

## 6. 转成实际落地任务

### IMPLEMENT-001：补真实实现证据闭环
- 来源 gap: `gap_001`
- 目标：把 F00 产生的任务包与真实控制器/模块/测试文件绑定，区分“任务已生成”和“实现已完成”。
- 交付：实现引用索引、测试引用索引、验收证据 bundle。
- 验收：不能再只停留在 `TASK_REQUIRED_NOT_IMPLEMENTED_EVIDENCE`。

### IMPLEMENT-002：扩展 safe-mode 到真实文档批处理 runner
- 来源 gap: `gap_002`
- 目标：在不触发 live runtime / signing / trading 的边界下，让多个真实文档自动批处理并生成统一索引。
- 交付：batch input manifest、batch run index、per-document final report。
- 验收：每份文档均有 K00-F00-V00-A00-H00-U00-G00 输出与 trace。

### IMPLEMENT-003：治理候选转人工审批包
- 来源 gap: `gap_003`
- 目标：把 governance candidates 生成审批包，但不直接声明 POLICY_ACTIVE。
- 交付：policy_candidate_review.md、approval checklist、rollback notes。
- 验收：未审批前状态保持 `CANDIDATE`。

## 7. 禁止声明
当前只允许声明 `RUNNABLE_WITH_GAPS` / `READY_WITH_GAPS`。不得声明：
- `PRODUCTION_READY`
- `FULLY_AUTOMATED`
- `LIVE_READY`
- `IMPLEMENTED_WITHOUT_EVIDENCE`
- `PIPELINE_ACCEPTED`
- `SYSTEM_FULLY_IMPLEMENTED`
