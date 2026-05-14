issue_pack_id: ISSUEPACK-S00-HERDOC-20260514-001
created_at: '2026-05-14T13:40:44Z'
scope_phase: S00_unified_system_standardization_after_static_landing
source_refs:
- /root/sikk-gmgn/system/unified_standardization/S00_ACCEPTANCE_REPORT.md
- /root/sikk-gmgn/system/unified_standardization/
- /root/.hermes/cache/documents/doc_8fbc86c33789_全体系统一标准化模块_v2_0：专业级别统一化数据模型.md
trigger_route:
- HER_DOC_SYSTEM_REVIEW
- HER_DOC_SYSTEM_AUDIT
- HER_DOC_PIPELINE
safety_boundaries:
  safe_mode: true
  paper_only: true
  forbidden:
  - live_swap
  - sign
  - broadcast
  - private_key_access
  - auto_deploy
  - production_trading
  - direct_live_rule_modification
system_scan_summary:
  s00_files: 98
  s00_yaml: 95
  s00_yaml_errors: 0
  runner_candidates: 4
  legacy_outputs_found:
    wallet_structure_decision.json: '>=20'
    paper_positions_open.json: 3
    strategy_metrics.json: 3
    data_fact_handoff_packet.json: 1
issues:
- issue_id: S00-R00-DRYRUN-GAP-001
  title: R00 runner dry-run/import/help evidence missing
  target_phase: R00_validation
  severity: HIGH_GAP
  evidence_ref: system_scan.runner_candidates_exist_without_dryrun_evidence
  required_outputs:
  - r00_runner_dry_run_matrix populated with command evidence
  - r00_failure_report_schema instances for failures
  - runner trace events
  acceptance:
  - each registered runner has safe-mode dry-run/import/help result
  - no live_swap/sign/broadcast executed
  handoff_target: R00_VALIDATION_PASS_01
  status: QUEUED
- issue_id: S00-CONTRACT-DIFF-GAP-001
  title: Existing runtime outputs not diffed against S00 schema/contract
  target_phase: P01-P10_contracts
  severity: HIGH_GAP
  evidence_ref: system_scan.output_search_found_legacy_json_without_schema_diff
  required_outputs:
  - contract_diff_report.json
  - per-output schema compatibility result
  - field lineage/permission missing-field list
  acceptance:
  - wallet_structure_decision/paper_positions_open/strategy_metrics/data_fact_handoff_packet
    checked
  - blocking incompatible fields registered
  handoff_target: CONTRACT_DIFF_PASS_01
  status: QUEUED
- issue_id: S00-P08-RUNTIME-BIND-GAP-001
  title: P08 permission gate defined but not proven as paper runner pre-open hard
    gate
  target_phase: P08_permission_gate
  severity: CRITICAL_GAP
  evidence_ref: S00_ACCEPTANCE_REPORT.with_gaps.p08_binding
  required_outputs:
  - paper runner pre-open gate check
  - P08 risk event output
  - permission denial trace fixture
  acceptance:
  - paper entry path cannot open without PAPER_READY/PAPER_ACTIVE permission
  - real_trade remains forbidden
  handoff_target: P08_BINDING_PASS_01
  status: QUEUED
- issue_id: S00-LEGACY-WRAPPER-GAP-001
  title: Legacy runtime registered but trace/acceptance/handoff wrapper not attached
  target_phase: legacy_absorption_runtime
  severity: HIGH_GAP
  evidence_ref: S00_ACCEPTANCE_REPORT.with_gaps.legacy_wrapper
  required_outputs:
  - wrapper contract
  - trace writer
  - acceptance writer
  - handoff writer
  acceptance:
  - legacy runner execution emits trace/acceptance/handoff artifacts under S00 indexes
  handoff_target: LEGACY_WRAPPER_PASS_01
  status: QUEUED
- issue_id: S00-SAMPLE-REGRESSION-GAP-001
  title: Sample library empty; regression cannot validate rule upgrades
  target_phase: P09_P10_regression
  severity: HIGH_GAP
  evidence_ref: S00 anchors sample_library empty_with_gap
  required_outputs:
  - sample_library_index seed cases
  - labeled_token_case entries
  - regression baseline result
  acceptance:
  - at least one real token case labeled for replay baseline
  - regression suite can run in safe-mode
  handoff_target: REGRESSION_SEED_PASS_01
  status: QUEUED
- issue_id: S00-SINGLE-TOKEN-REPLAY-GAP-001
  title: No complete single-token replay case file yet
  target_phase: P01-P10_replay
  severity: CRITICAL_GAP
  evidence_ref: S00 next-step.single_token_replay_missing
  required_outputs:
  - token_judgment_case_file
  - phase_path evidence
  - trace/acceptance/handoff refs
  - P08 permission result
  acceptance:
  - one real token can traverse P01-P10 in replay/paper-only safe mode and produce
    case file
  handoff_target: SINGLE_TOKEN_REPLAY_PASS_01
  status: QUEUED
execution_order:
- HER_DOC_SYSTEM_REVIEW
- HER_DOC_SYSTEM_AUDIT
- R00_VALIDATION_PASS_01
- CONTRACT_DIFF_PASS_01
- P08_BINDING_PASS_01
- LEGACY_WRAPPER_PASS_01
- REGRESSION_SEED_PASS_01
- SINGLE_TOKEN_REPLAY_PASS_01
- P09_P10_REVIEW_PASS_01
status: ISSUE_PACK_READY_FOR_SAFE_AUTOMATION_WITH_GAPS
