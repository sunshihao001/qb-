# R00 Execution Protocol

## R00.0 Preflight Gate
Require V00 handoff, V00_ACCEPTED or V00_READY_WITH_GAPS without BLOCKING_GAP, validation evidence, test evidence, execution boundary, binding policy, repo_root, and safe_mode=true. Forbid live runtime, wallet signing, auto deploy, and production trading.

## R00.1 Validation Evidence Loader
Load V00 handoff, schema_validation_result, contract_validation_result, function_mapping_validation_result, field_model_validation_result, rule_logic_validation_result, test_evidence, replay_evidence, gap_report, failure_evidence when present, and acceptance_result. Missing required evidence blocks binding.

## R00.2 Binding Target Inventory Scanner
Classify suitable targets: CLI, HER_CONTROLLER_CALL, ORCHESTRATOR_STEP, TOOL_BINDING, TELEGRAM_COMMAND_DESIGN, REPORT_GENERATOR, DASHBOARD_FIELD, SCHEDULER_DRY_RUN_JOB, PAPER_ONLY_SAFE_MODE, REVIEW_QUEUE. Exclude live runtime and wallet signing.

## R00.3 Existing Interface Scanner
Scan existing CLI entries, runner scripts, orchestrator steps, Telegram commands, report generators, dashboard fields, scheduler jobs, and legacy runtime paths to prevent conflict and path pollution.

## R00.4 Binding Decision Gate
Emit BIND_CLI, BIND_TOOL, BIND_ORCHESTRATOR, BIND_TELEGRAM_DESIGN_ONLY, BIND_REPORT, BIND_DASHBOARD, BIND_SCHEDULER_DRY_RUN, BIND_REVIEW_QUEUE, DESIGN_ONLY, or blocked states.

## R00.5 Command Contract Builder
Create a command contract with command_id, command_name, entry_type, module, command_template, required_args, optional_args, input_paths, output_paths, allowed_modes, forbidden_modes, expected_outputs, success_criteria, and failure_policy.

## R00.6 CLI Binding Designer
Create CLI binding with script_path, working_dir, safe_mode_required, required_args, output_dir_policy, trace_enabled, audit_enabled, idempotency_required, and lock_required.

## R00.7 HER Tool / Controller Binding Designer
Create tool/controller binding with controller_id, entry_method, input_contract_ref, output_contract_ref, state_update, trace_update, failure_policy, and safe_mode_required.

## R00.8 Orchestrator Binding Designer
Create orchestrator step with after, before, input, output, skip_conditions, failure_action, and safe_mode.

## R00.9 Telegram Binding Designer
Design Telegram command only. Telegram design is not Telegram上线 and must not be treated as enabled bot command. Include permission_level, safe_mode_required, allowed_actions, forbidden_actions, and output template.

## R00.10 Report / Dashboard Binding Designer
Bind generated outputs to report sections and dashboard fields so results are visible, auditable, and reviewable.

## R00.11 Scheduler / Dry-run Job Binding Designer
Design safe dry-run scheduler job only, disabled by default. Scheduler design is not scheduler enabled.

## R00.12 Safe Dry-run Binding Validator
Execute only safe dry-run if allowed. Record dry_run_command, started_at, ended_at, exit_code, stdout_path, stderr_path, generated_outputs, missing_outputs, trace_path, audit_path, and binding_status. Binding plan alone is DESIGN_ONLY, not RUNNER_BOUND. No exit_code means not BINDING_TESTED. No stdout/stderr means not BINDING_TESTED. No generated output manifest means not R00_ACCEPTED.

## R00.13 Trace / Audit Binder
Write trace and audit events for r00_started, v00_handoff_loaded, validation_evidence_loaded, binding_target_inventory_created, interface_scanned, binding_decision_made, command_contract_created, cli_binding_created, tool_binding_created, orchestrator_binding_created, telegram_binding_created, report_binding_created, dashboard_binding_created, scheduler_binding_created, dry_run_started, dry_run_completed, binding_failed, acceptance_checked, handoff_written, r00_completed, r00_blocked.

## R00.14 Gap / Failure Classifier
Classify missing_v00_handoff, validation_not_passed, missing_test_evidence, missing_replay_evidence, missing_binding_policy, missing_execution_boundary, interface_conflict, command_contract_gap, dry_run_failed, missing_trace, missing_audit, production_risk_detected, and governance_violation by severity. Failed binding must remain failed.

## R00.15 Acceptance & Handoff Writer
Emit R00_ACCEPTED only when core binding dry-run passes, generated outputs exist, trace/audit exist, and no blocking gap exists. Emit handoff packets to A00/H00/U00 with validation evidence, binding specs, dry-run evidence, trace, audit, gap, failure, acceptance, allowed next actions, and forbidden next actions.

## False Pass Rules
- No V00 handoff → R00_BLOCKED.
- V00 validation not passed → no binding.
- No validation evidence → no binding.
- No command contract → no runner binding.
- No safe_mode → no dry-run.
- Binding plan alone → DESIGN_ONLY, not RUNNER_BOUND.
- No dry-run exit_code → not BINDING_TESTED.
- No stdout/stderr → not BINDING_TESTED.
- No generated output manifest → not R00_ACCEPTED.
- No trace/audit → not R00_ACCEPTED.
- Telegram binding design is not Telegram上线.
- Scheduler binding design is not scheduler enabled.
- Failed binding cannot be converted to passed.
