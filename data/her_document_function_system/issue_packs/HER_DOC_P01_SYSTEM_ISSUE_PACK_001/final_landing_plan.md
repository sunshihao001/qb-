# HER_DOC_P01_SYSTEM_ISSUE_PACK_001｜落地方案

## 当前状态

- issue pack：已创建
- review pack：已创建
- audit request：已创建
- pipeline run request：已创建
- trace/audit：已创建并可解析
- 当前状态不是问题已解决，只是问题已任务化。

## 文件位置

主目录：

`/root/sikk-gmgn/data/her_document_function_system/issue_packs/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/`

已生成文件：

- `issue_pack.yaml`
- `system_review_pack.md`
- `system_audit_request.json`
- `pipeline_run_request.json`
- `trace.jsonl`
- `audit.jsonl`

原始 pending task manifest：

`/root/sikk-gmgn/research_loop/task_packages/pending/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/task_manifest.yaml`

## 三段执行顺序

### 1. HER_DOC_SYSTEM_REVIEW

目的：先确认系统设计与 P01 canonical/legacy 分层。

输入：

- `issue_pack.yaml`
- `system_review_pack.md`
- `controller_registry.json`
- K00/F00/V00/R00/A00 控制器目录
- P01 候选目录

必须输出：

- `outputs/system_review/her_doc_system_layer_map.md`
- `outputs/system_review/phase_dependency_graph.json`
- `outputs/system_review/canonical_vs_legacy_registry.yaml`
- `outputs/system_review/p01_phase_inventory.json`
- `outputs/system_review/p01_phase_gap_register.yaml`
- `outputs/system_review/p01_phase_completion_status.md`
- `outputs/system_review/p01_phase_handoff_packet.json`
- `outputs/system_review/execution_gate_decision.json`

通过条件：

- canonical / legacy / candidate 明确。
- P01 缺失项逐项列出。
- 不把旧文档存在当 P01 READY。
- execution gate 只允许进入 audit，不允许生产/runtime。

### 2. HER_DOC_SYSTEM_AUDIT

目的：审计 K00→F00→V00→R00→A00 证据链与输入合约。

输入：

- `system_audit_request.json`
- `issue_pack.yaml`
- 已有 run：`data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/`
- F00 控制器输出目录

必须输出：

- `outputs/system_audit/k00_f00_entry_contract_audit.json`
- `outputs/system_audit/f00_missing_input_status_matrix.json`
- `outputs/system_audit/chat_context_bypass_findings.md`
- `outputs/system_audit/f00_asset_realization_matrix.json`
- `outputs/system_audit/f00_gap_register.yaml`
- `outputs/system_audit/v00_r00_a00_evidence_audit.json`
- `outputs/system_audit/readiness_debt_register.yaml`
- `outputs/system_audit/her_doc_data_integrity_matrix.json`
- `outputs/system_audit/parse_validation_result.json`

关键规则：

- 无 K00 handoff → `F00_BLOCKED`
- 无 document passport → `F00_BLOCKED`
- 无 corpus index → `F00_BLOCKED`
- 无 gap detection → `F00_BLOCKED`
- 无 execution_boundary → `F00_BLOCKED`
- 无 write_policy / repo_root → `DESIGN_ONLY`
- 无 KV → `KV_GAP`，可继续
- `READY_WITH_GAPS` 不得改写成 `READY`

### 3. HER_DOC_PIPELINE

目的：review + audit 后，再安全执行文档到功能 pipeline。

输入：

- `pipeline_run_request.json`
- 真正的 document path
- goal json/text
- repo root：`/root/sikk-gmgn`

推荐命令模板：

```bash
cd /root/sikk-gmgn
python3 tools/o00_run_document_main.py \
  --document <真实文档路径> \
  --goal <goal_json_or_text> \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/runs/<run_id> \
  --safe-mode
```

允许最终状态：

- `HER_DOC_FUNCTION_PIPELINE_READY`
- `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`
- `HER_DOC_FUNCTION_PIPELINE_BLOCKED`
- `HER_DOC_FUNCTION_PIPELINE_REJECTED`

默认目标状态：

- `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`

禁止声称：

- `PRODUCTION_READY`
- `LIVE_READY`
- `FULLY_AUTOMATED`
- `RUNNER_BOUND_WITHOUT_DRY_RUN`
- `TESTED_WITHOUT_COMMAND_EVIDENCE`

## 安全边界

- safe mode only
- manual trigger only
- no live runtime
- no wallet signing
- no auto deploy
- no production trading
- no direct production rule change

## 验证结果

本轮已验证：

- `issue_pack.yaml`：YAML OK
- `system_audit_request.json`：JSON OK
- `pipeline_run_request.json`：JSON OK
- `trace.jsonl`：JSONL OK
- `audit.jsonl`：JSONL OK
- 缺失文件：0

## 下一步

从 `HER_DOC_SYSTEM_REVIEW` 开始执行，不直接进入 pipeline。执行时必须从 issue pack 文件读取，不从聊天上下文读取。
