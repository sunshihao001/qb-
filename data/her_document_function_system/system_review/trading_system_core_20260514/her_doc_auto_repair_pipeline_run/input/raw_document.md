# HER_DOC Auto Repair Task Package — Trading System Runtime 收编

- doc_id: `HER_DOC_AUTO_REPAIR_TASK_PACKAGE_20260514`
- created_at: `2026-05-14T09:59:45+00:00`
- scenario: `trading_system_runtime_repair_20260514`
- system_identity: 一套 HER 总控闭环交易结构系统；`sikk_live_run.py` 是 paper-only runtime 执行层，不是第二套系统。
- safety_boundary: safe-mode / paper-only / no real swap / no private key / no signature / no broadcast

## 目标

根据“HER 总控 + 已运行 paper runtime 不是两套系统，而是一套系统的控制层与执行层”的目标，建立自动修复任务包，并通过 HER_DOC O00→K00→F00→V00→A00→H00→U00→G00 流程处理，落到实际应用场景：

```text
真实代币数据 → runtime artifact → HER 阶段验收 → V00 evidence bundle → H00 downstream queue → U00 review/upgrade candidate
```

## 已知证据

- issue_package: `data/her_document_function_system/system_review/trading_system_core_20260514/trading_system_core_task_issue_package.json`
- runtime_audit: `data/her_document_function_system/system_review/trading_system_core_20260514/runtime_data_integrity_audit.json`
- p02_p03_mapping: `data/her_document_function_system/system_review/trading_system_core_20260514/p02_p03_runtime_field_mapping.json`
- paper_boundary: `data/her_document_function_system/system_review/trading_system_core_20260514/paper_only_boundary_acceptance.json`
- runtime_root: `data/gmgn_candidates_live_run/`

## 当前状态摘要

- runtime_data_integrity: `RUNTIME_DATA_INTEGRITY_PASS_WITH_GAPS`
- p02_p03_mapping: `P02_P03_MAPPING_READY_WITH_GAPS`
- paper_only_boundary: `PAPER_ONLY_BOUNDARY_ACCEPTANCE_READY`
- remaining_open_issue_ids: `['HER-TS-002']`

## 自动修复任务清单

### AUTO-REPAIR-001 — V00 实现证据包绑定

- source_issue: `HER-TS-002`
- problem: safe-mode HER_DOC 管线已有执行证据，但 F00/V00/H00 仍缺生产实现证据或 live/paper runtime 证据闭环。
- HER_DOC_stage: `F00 → V00 → A00`
- automation_action: 生成 `v00_runtime_evidence_bundle.json/md`，把命令、输入、输出、退出码、runtime 文件存在性、安全边界、READY_WITH_GAPS 规则绑定成一个可验证证据包。
- application_scenario: 当前 `gmgn_candidates_live_run` 真实候选、信号、状态机、quote/security、paper_live 输出。
- acceptance: 文件存在、JSON 可读、列出每个 runtime artifact 的 file_exists/json_ok/sample_count；A00 不把 safe-mode 等同生产 ACCEPTED。
- status: `TASK_READY_FOR_SAFE_APPLY`

### AUTO-REPAIR-002 — 钱包结构 P02/P03 runtime 缺口落队列

- source_gap: `runtime_P3_wallet_structure_missing_or_invalid`
- HER_DOC_stage: `V00 → H00 → U00`
- automation_action: 生成 `h00_runtime_repair_downstream_queue.json`，把缺失 `wallet_structure/candidate_wallet_structure_summary.json` 转成 H00 下游修复任务；要求缺失时标记 `DEGRADED_OR_NOT_CONNECTED`，不得作为 `WALLET_SUPPORT`。
- application_scenario: P02 钱包结构 / P03 筹码控制接入 runtime summary。
- acceptance: queue item 包含 owner_phase、target_path、blocking_policy、required_fields、safe_apply_allowed。
- status: `TASK_READY_FOR_SAFE_APPLY`

### AUTO-REPAIR-003 — Phase-runtime 应用索引

- source_goal: 控制层收编执行层，不再视为两套系统。
- HER_DOC_stage: `F00 → V00 → A00 → H00`
- automation_action: 生成 `phase_runtime_application_index.json/md`，把 P01-P10 / P00-P09 控制器与当前 runtime artifact 一一映射，并标注 evidence status、consumer、missing policy。
- application_scenario: 每轮 `sikk_live_run.py` 后，HER_DOC 可读取该索引决定哪些阶段 PASS_WITH_GAPS、哪些进入 H00。
- acceptance: 覆盖候选、信号、状态机、钱包结构、quote/security、paper_live、review/report、升级候选。
- status: `TASK_READY_FOR_SAFE_APPLY`

### AUTO-REPAIR-004 — Review-to-upgrade 安全升级候选包

- source_goal: 真实代币数据 → 纸面结果 → 复盘升级，但复盘不能直接改实时规则。
- HER_DOC_stage: `U00 → G00`
- automation_action: 生成 `u00_review_upgrade_candidate_package.json/md`，将 open gaps、paper evidence、wallet_structure 缺口转成升级候选、shadow validation、rollback、manual approval checklist。
- application_scenario: P09/P10 复盘升级闭环。
- acceptance: 所有升级项状态为 `CANDIDATE`，不是 `POLICY_ACTIVE`；包含 rollback 和 manual approval 字段。
- status: `TASK_READY_FOR_SAFE_APPLY`

## 禁止声明

- 不声明 `PRODUCTION_READY`
- 不声明 `LIVE_READY`
- 不声明 `FULLY_ACCEPTED`
- 不声明 `POLICY_ACTIVE`
- 不触发真实交易、不签名、不广播、不读取私钥

## 预期 HER_DOC 处理结果

- O00/K00/F00/V00/A00/H00/U00/G00 可生成 safe-mode 处理产物。
- 最终状态允许是 `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`。
- 实际应用落地产物写入系统 review 目录，作为后续 runtime 收编和钱包结构接入的执行依据。
