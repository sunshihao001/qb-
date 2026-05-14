# HER_DOC_P01_SYSTEM_ISSUE_PACK_001｜System Review Pack

## 1. Review 目标

先做 HER_DOC_SYSTEM_REVIEW，不直接跑 pipeline。目标是判定：

- P01 相关资产哪些是 canonical。
- 哪些是 legacy / candidate / read-only fallback。
- K00→F00→V00→R00→A00 的控制器链是否闭环。
- 是否允许进入后续 HER_DOC_SYSTEM_AUDIT 与 HER_DOC_PIPELINE。

## 2. 输入证据

- `research_loop/task_packages/pending/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/task_manifest.yaml`
- `data/her_document_function_system/issue_packs/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/issue_pack.yaml`
- `system/her_document_function_system/registry/controller_registry.json`
- `system/her_document_function_system/00_governance/HER_DFAFS_SYSTEM_SPEC_V1.md`
- `system/her_document_function_system/controllers/`
- `sikk_stable_trader_os/06_phase_controllers/P01_data_fact_runtime_connection/`
- `sikk_stable_trader_os/06_phase_controllers/P01_data_fact_controller/`
- `data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/`

## 3. 必须输出

输出到：

`data/her_document_function_system/issue_packs/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/outputs/system_review/`

必须生成：

- `her_doc_system_layer_map.md`
- `phase_dependency_graph.json`
- `canonical_vs_legacy_registry.yaml`
- `p01_phase_inventory.json`
- `p01_phase_gap_register.yaml`
- `p01_phase_completion_status.md`
- `p01_phase_handoff_packet.json`
- `execution_gate_decision.json`

## 4. Review Gate

允许进入 `HER_DOC_SYSTEM_AUDIT` 的最低条件：

- controller_registry 可读。
- K00/F00/V00/R00/A00 至少能定位 manifest 或 controller directory。
- P01 candidate/canonical 路径已列出。
- missing files 不隐藏，写入 gap register。
- execution_gate_decision 不声称 production-ready。

## 5. 禁止事项

- 禁止把聊天上下文作为阶段状态。
- 禁止把旧文档存在等同于 P01 ready。
- 禁止将 review 通过解释为实现完成。
- 禁止 live runtime / wallet signing / auto deploy / production trading。
