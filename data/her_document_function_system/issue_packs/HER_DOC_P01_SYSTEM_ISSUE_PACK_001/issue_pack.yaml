issue_pack_id: HER_DOC_P01_SYSTEM_ISSUE_PACK_001
scope_phase: P01
source_system: HER_DOC
status: ISSUE_PACK_CREATED
created_at: '2026-05-14T04:02:24Z'
source_refs:
  task_manifest: research_loop/task_packages/pending/HER_DOC_P01_SYSTEM_ISSUE_PACK_001/task_manifest.yaml
  existing_pipeline_run: data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002
  f00_controller: system/her_document_function_system/controllers/F00_function_realization_controller
  controller_registry: system/her_document_function_system/registry/controller_registry.json
trigger_route_sequence:
  - HER_DOC_SYSTEM_REVIEW
  - HER_DOC_SYSTEM_AUDIT
  - HER_DOC_PIPELINE
safety_boundaries:
  - no_live_runtime
  - no_wallet_signing
  - no_auto_deploy
  - no_production_trading
  - no_direct_production_rule_change
  - safe_mode_only
  - manual_trigger_only
status_discipline:
  issue_pack_created_is_not_issue_resolved: true
  mapping_is_not_implementation: true
  test_plan_is_not_tested: true
  binding_plan_is_not_runner_bound: true
  runnable_with_gaps_is_not_production_ready: true
issues:
  - issue_id: HERDOC-P01-001
    title: P01 阶段定义完整性审查
    trigger_route: HER_DOC_SYSTEM_REVIEW
    target_phase: P01
    status: OPEN
    severity: HIGH
    evidence_ref:
      - system/her_document_function_system/registry/controller_registry.json
      - system/her_document_function_system/06_phase_controllers/P01_data_fact_controller/
      - sikk_stable_trader_os/06_phase_controllers/P01_data_fact_runtime_connection/
      - sikk_stable_trader_os/06_phase_controllers/P01_data_fact_controller/
    problem_statement: P01 相关目录存在多套命名与多套资产，需要判定 canonical / legacy / candidate，并检查 9-file phase package 是否齐备。
    required_outputs:
      - outputs/system_review/p01_phase_inventory.json
      - outputs/system_review/p01_phase_gap_register.yaml
      - outputs/system_review/p01_phase_completion_status.md
      - outputs/system_review/p01_phase_handoff_packet.json
    acceptance:
      - 列出每个 P01 候选目录及其文件证据
      - 明确 canonical P01 路径与 legacy fallback 路径
      - 对缺失 manifest/context/objective/input/output/protocol/gate/state/handoff 逐项状态化
      - 不把存在旧文档等同于当前阶段 READY
    handoff_target: HER_DOC_SYSTEM_AUDIT
  - issue_id: HERDOC-P01-002
    title: K00→F00 唯一合法入口校验
    trigger_route: HER_DOC_SYSTEM_AUDIT
    target_phase: K00,F00
    status: OPEN
    severity: CRITICAL
    evidence_ref:
      - system/her_document_function_system/controllers/K00_knowledge_intake_controller/04_k00_input_contract.json
      - system/her_document_function_system/controllers/K00_knowledge_intake_controller/09_k00_handoff_packet.schema.json
      - system/her_document_function_system/controllers/F00_function_realization_controller/04_f00_input_contract.json
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/k00/k00_handoff_packet.json
    problem_statement: F00 必须从 K00 handoff 和 file-backed refs 进入，不能读聊天上下文；缺 document_passport/corpus/system_mapping/gap_detection/execution_boundary/write_policy/repo_root 时必须阻断或降级。
    required_outputs:
      - outputs/system_audit/k00_f00_entry_contract_audit.json
      - outputs/system_audit/f00_missing_input_status_matrix.json
      - outputs/system_audit/chat_context_bypass_findings.md
    acceptance:
      - no_k00_handoff => F00_BLOCKED
      - no_document_passport => F00_BLOCKED
      - no_corpus_index => F00_BLOCKED
      - no_gap_detection => F00_BLOCKED
      - no_execution_boundary => F00_BLOCKED
      - no_write_policy or no_repo_root => DESIGN_ONLY
      - no_kv => KV_GAP but not blocking
    handoff_target: F00_FUNCTION_REALIZATION
  - issue_id: HERDOC-P01-003
    title: F00 功能映射到真实资产闭环
    trigger_route: HER_DOC_SYSTEM_AUDIT
    target_phase: F00
    status: OPEN
    severity: HIGH
    evidence_ref:
      - system/her_document_function_system/controllers/F00_function_realization_controller/outputs/concept_to_function_map.json
      - system/her_document_function_system/controllers/F00_function_realization_controller/outputs/function_asset_plan.json
      - system/her_document_function_system/controllers/F00_function_realization_controller/outputs/f00_acceptance_result.json
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/f00/function_mapping.json
    problem_statement: F00 已有设计/映射/计划类资产，但需要审计哪些是真实写入、哪些只是 task_required 或 plan，避免把 mapping 当 implementation。
    required_outputs:
      - outputs/system_audit/f00_asset_realization_matrix.json
      - outputs/system_audit/f00_gap_register.yaml
      - outputs/system_audit/f00_runner_requirement_list.md
      - outputs/system_audit/f00_function_asset_plan_review.json
    acceptance:
      - 每个 function mapping 必须有 target_controller、required_inputs、required_outputs、artifact_path、status
      - plan / schema_plan / runner_binding_plan 不得算 IMPLEMENTED / TESTED / RUNNER_BOUND
      - unmapped_items 与 gaps 必须进入后续 H00/U00 queue
    handoff_target: V00_VALIDATION_EVIDENCE
  - issue_id: HERDOC-P01-004
    title: V00/R00/A00 证据链防假通过审计
    trigger_route: HER_DOC_SYSTEM_AUDIT
    target_phase: V00,R00,A00
    status: OPEN
    severity: HIGH
    evidence_ref:
      - system/her_document_function_system/controllers/V00_validation_evidence_controller/
      - system/her_document_function_system/controllers/R00_runner_tool_binding_controller/
      - system/her_document_function_system/controllers/A00_acceptance_evidence_controller/04_a00_input_contract.json
      - system/her_document_function_system/controllers/A00_acceptance_evidence_controller/06_a00_execution_protocol.md
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/a00/a00_acceptance_result.json
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/v00/gap_register.json
    problem_statement: 现有 pipeline run 状态为 RUNNABLE_WITH_GAPS，必须验证 A00 没有把 gap 隐藏成 READY，且 R00 runner binding 没有把计划当 dry-run evidence。
    required_outputs:
      - outputs/system_audit/v00_r00_a00_evidence_audit.json
      - outputs/system_audit/acceptance_false_positive_findings.md
      - outputs/system_audit/readiness_debt_register.yaml
      - outputs/system_audit/evidence_chain_status.json
    acceptance:
      - test_plan != TESTED
      - replay_plan != REPLAY_TESTED
      - binding_plan != RUNNER_BOUND
      - READY_WITH_GAPS 不得改写成 READY
      - ready_for_production 必须保持 false 除非有独立证据和人类授权
    handoff_target: A00_ACCEPTANCE_EVIDENCE
  - issue_id: HERDOC-P01-005
    title: HER_DOC 系统设计层与 canonical/legacy 分层梳理
    trigger_route: HER_DOC_SYSTEM_REVIEW
    target_phase: SYSTEM
    status: OPEN
    severity: MEDIUM
    evidence_ref:
      - system/her_document_function_system/registry/controller_registry.json
      - system/her_document_function_system/00_governance/HER_DFAFS_SYSTEM_SPEC_V1.md
      - system/her_document_function_system/controllers/
      - sikk_stable_trader_os/06_phase_controllers/
    problem_statement: 控制器链、旧 phase_controller、candidate、runtime run 产物并存，需要输出 layer map 与 canonical 决策，供后续 pipeline 不盲搜旧目录。
    required_outputs:
      - outputs/system_review/her_doc_system_layer_map.md
      - outputs/system_review/phase_dependency_graph.json
      - outputs/system_review/canonical_vs_legacy_registry.yaml
      - outputs/system_review/execution_gate_decision.json
    acceptance:
      - 每个控制器都有 input/output/acceptance/handoff refs
      - canonical 与 legacy/candidate/read-only fallback 分开
      - 给出是否允许进入 HER_DOC_PIPELINE 的 gate decision
    handoff_target: HER_DOC_PIPELINE
  - issue_id: HERDOC-P01-006
    title: HER_DOC 数据完整性与 trace/audit 可读性审查
    trigger_route: HER_DOC_SYSTEM_AUDIT
    target_phase: DATA
    status: OPEN
    severity: MEDIUM
    evidence_ref:
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/
      - data/knowledge_processing_program/system_rescan/
    problem_statement: passport/corpus/mapping/gap/evidence/handoff/trace/audit/acceptance 必须齐备且 JSON/YAML 可解析；system_rescan 输出数量不足时不能报完成。
    required_outputs:
      - outputs/system_audit/her_doc_data_integrity_matrix.json
      - outputs/system_audit/missing_data_assets_list.md
      - outputs/system_audit/data_readiness_scorecard.md
      - outputs/system_audit/parse_validation_result.json
    acceptance:
      - 所有 JSON/YAML 解析通过或记录失败原因
      - 缺失资产列入 missing_data_assets_list
      - trace.jsonl/audit.jsonl 存在并可读
      - 输出不足 12 项时标记 READY_WITH_GAPS/GAPS_FOUND
    handoff_target: H00_DOWNSTREAM_QUEUE
  - issue_id: HERDOC-P01-007
    title: HER_DOC_PIPELINE 安全执行请求包
    trigger_route: HER_DOC_PIPELINE
    target_phase: O00,K00,F00,V00,A00,H00,U00,G00
    status: OPEN
    severity: HIGH
    evidence_ref:
      - skill:her-doc-function-pipeline
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/o00/run_summary.json
      - data/her_document_function_system/runs/HER-DOC-REAL-20260514-SYSTEM-RESCAN-002/a00/a00_acceptance_result.json
    problem_statement: review/audit 通过后，按 safe-mode 手动触发 HER_DOC_PIPELINE，生成新 run_dir，并保留 gaps，不升级到 production-ready。
    required_outputs:
      - pipeline_run_request.json
      - outputs/pipeline/k00_to_f00_task_pack.yaml
      - outputs/pipeline/pipeline_output_manifest.json
      - outputs/pipeline/final_report.md
      - trace.jsonl
      - audit.jsonl
    acceptance:
      - safe_mode=true
      - manual_trigger_only=true
      - ready_for_production=false
      - final_status 只能是 READY / RUNNABLE_WITH_GAPS / BLOCKED / REJECTED 之一，默认 RUNNABLE_WITH_GAPS
    handoff_target: O00_FINAL_SUMMARY
execution_order:
  - HERDOC-P01-005
  - HERDOC-P01-001
  - HERDOC-P01-002
  - HERDOC-P01-003
  - HERDOC-P01-004
  - HERDOC-P01-006
  - HERDOC-P01-007
