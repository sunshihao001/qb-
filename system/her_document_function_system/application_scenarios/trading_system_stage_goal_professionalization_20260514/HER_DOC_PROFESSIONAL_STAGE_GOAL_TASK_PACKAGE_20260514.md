# HER_DOC Professional Stage Goal Completion Task Package 20260514

## Operator Intent

Use the HER_DOC system workflow to understand the SIKK trading-structure system as one HER-controlled system, then build a professional problem-list task package, automatically process repair/application tasks, and land the results into actual application artifacts. The target quality is lightweight institutional standard in one pass: complete stage goals, data requirements, issue inventory, repair tasks, application scenario files, and completeness judgment. If any stage cannot be completed, define why and how to complete it.

## Non-negotiable Boundaries

- Paper/observe only.
- No real swap.
- No signing.
- No private key read/write.
- No broadcast.
- Do not mark READY_WITH_GAPS as ACCEPTED.
- Wallet support is never a buy signal.
- Missing wallet structure data is DEGRADED_OR_NOT_CONNECTED, not safe.
- Review output creates candidates only, never active policy.

## Required HER_DOC Thinking Flow

1. O00: understand operator goal and classify task as system-build + actual-application safe-mode repair.
2. K00: preserve and assetize prior gap scan, stage matrix, GPT research package, runtime file-state evidence.
3. A00: acceptance view: file, structure, semantic, consumption, runtime.
4. V00: produce gap register by system layer and P01-P10 business phase.
5. H00: produce downstream task queue with legal next actions.
6. U00: produce upgrade-candidate package only for review/shadow/approval.
7. Apply safe-mode outputs into project application scenario artifacts.
8. Verify all JSON, paths, statuses, and paper-only boundary.

## Existing Evidence Inputs

- data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514/full_trading_system_gap_matrix.json
- data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514/stage_goal_preparation_gap_report.json
- data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514/gpt_research_request_pack.json
- data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514/methodology_total_goal_gap_summary.json
- data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514/her_doc_full_gap_scan_verification.json
- sikk_live_run.py
- run_sikk_gmgn_pipeline.py
- sikk_candidate_wallet_structure_pipeline.py
- data/gmgn_candidates_live_run/
- sikk_stable_trader_os/00_methodology/
- sikk_stable_trader_os/00_governance/
- sikk_stable_trader_os/00_domain/
- sikk_stable_trader_os/00_data/
- sikk_stable_trader_os/00_control/
- sikk_stable_trader_os/00_trace/
- sikk_stable_trader_os/08_acceptance/
- sikk_stable_trader_os/09_handoff/
- sikk_stable_trader_os/02_phase_controllers/

## Required Problem List Classes

### CLASS-01 Total Control Consumption
Problem: operator goal, total goal, and stage goal are preserved but not fully consumed by runtime.
Required data:
- goal_id
- goal_text
- legal_stage_route
- phase_mapping
- runner_mapping
- artifact_mapping
- trace_event
- acceptance_result
- consumption_status

### CLASS-02 Runner / Tool Binding
Problem: runner binding layer is incomplete or missing; current runtime can bypass HER control semantics.
Required data:
- runner_id
- script_path
- allowed_mode
- forbidden_actions
- input_contract
- output_contract
- phase_binding
- validation_command
- evidence_output
- failure_policy

### CLASS-03 Phase Output Index
Problem: runtime outputs exist but are not fully written into HER phase_output_index.
Required data:
- phase_id
- token_or_run_id
- output_artifact
- artifact_type
- produced_by_runner
- json_validity
- consumer_phase
- handoff_packet
- missing_policy

### CLASS-04 Handoff Consumption
Problem: handoff packets exist but downstream consumption proof is incomplete.
Required data:
- handoff_id
- source_phase
- target_phase
- packet_path
- required_fields
- consumed_by
- consumed_at
- consumption_result
- gap_propagation

### CLASS-05 Evidence / Acceptance
Problem: file-level artifacts exist but semantic/consumption/runtime acceptance is incomplete.
Required data:
- acceptance_id
- artifact_path
- file_level_status
- structure_level_status
- semantic_level_status
- consumption_level_status
- runtime_level_status
- blocker_reason
- remediation_task

### CLASS-06 Wallet Structure Runtime Gap
Problem: wallet_structure runtime summary is missing or not connected in current live-run evidence.
Required data:
- token_address
- wallet_fact_bundle_path
- wallet_structure_summary_path
- entity_groups
- same_source_groups
- chip_distribution
- dominant_side_cost_zone
- distribution_progress
- evidence_level
- missing_policy

### CLASS-07 Data Completeness by P01-P10
Problem: each business phase needs a complete data requirement list, source, quality, missing policy, and completion judgment.
Required data:
- phase_id
- phase_goal
- required_fields
- optional_fields
- source_module
- current_artifacts
- completeness_score
- missing_fields
- blocking_fields
- repair_tasks

### CLASS-08 Review / Upgrade Closed Loop
Problem: paper review does not yet fully create controlled upgrade candidates with shadow validation and approval package.
Required data:
- review_case_id
- failure_type
- proposed_rule_change
- affected_phase
- shadow_validation_plan
- rollback_plan
- manual_approval_required
- candidate_status

## Required Auto-Repair / Application Tasks

- PROF-REPAIR-001: Create professional stage goal issue register.
- PROF-REPAIR-002: Create P01-P10 stage data completeness matrix.
- PROF-REPAIR-003: Create runner binding application pack under safe-mode.
- PROF-REPAIR-004: Create phase output index seed from existing runtime outputs.
- PROF-REPAIR-005: Create handoff consumption queue for unresolved gaps.
- PROF-REPAIR-006: Create wallet-structure gap repair queue and degraded policy.
- PROF-REPAIR-007: Create acceptance status matrix distinguishing READY_WITH_GAPS from ACCEPTED.
- PROF-REPAIR-008: Create review/upgrade candidate package with shadow validation only.
- PROF-REPAIR-009: Create professional application scenario index and final verification.

## Expected Applied Artifacts

Write actual files to:

data/her_document_function_system/system_review/trading_system_stage_goal_professionalization_20260514/

Expected files:
- professional_stage_goal_issue_register.json/md
- p01_p10_stage_data_completeness_matrix.json/md
- runner_binding_application_pack.json/md
- phase_output_index_seed.json/md
- handoff_consumption_repair_queue.json/md
- wallet_structure_gap_repair_queue.json/md
- acceptance_status_matrix.json/md
- review_upgrade_candidate_package.json/md
- professional_application_scenario_index.json/md
- professionalization_verification.json

## Completion Rule

Final status must be READY_WITH_GAPS unless every file, structure, semantic, consumption, and runtime acceptance passes with real consumption evidence. Missing data must be explicitly listed with how to complete it.
