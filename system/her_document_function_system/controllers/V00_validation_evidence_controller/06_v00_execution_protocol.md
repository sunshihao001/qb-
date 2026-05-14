# V00 Execution Protocol

V00 turns F00 design outputs into validation evidence. It must never treat a plan as evidence.

## Global hard gates

- No `f00_handoff_packet` → `V00_BLOCKED`.
- `f00_status == F00_BLOCKED` or missing accepted/gap status → `V00_REJECTED`.
- No execution boundary → `V00_BLOCKED`.
- Any request for live runtime, wallet signing, or auto deploy → `production_risk_detected` + `V00_BLOCKED`.
- No trace/audit output → cannot reach `V00_ACCEPTED`.
- BLOCKING_GAP exists → cannot reach `HANDOFF_READY`.

## V00.0 Preflight Gate

Validate `04_v00_input_contract.json`, F00 status, K00/F00 refs, repo root, test plan, replay plan, and execution boundary. Write `preflight/v00_preflight_result.json` and trace `v00_started`, `preflight_passed` or `v00_blocked`.

## V00.1 Input Evidence Loader

Load file-backed F00 assets: function_mapping, implementation_decision, asset_plan, field_model, rule_logic, schema_contract_plan, patch_refs, test_plan, replay_plan, trace_refs. Missing required assets become explicit gaps.

## V00.2 Function Mapping Validator

Each function mapping record must include `function_id`, `source_doc_id`, `source_concept`, `required_function`, `function_type`, `target_phase`, `input_fields`, `output_fields`, `required_logic`, `required_assets`, and `status`. Pure descriptions without functional objects are rejected.

## V00.3 Field Model Validator

Each field must include `field_name`, `field_type`, `source`, `required`, `missing_policy`, `evidence_level`, `used_by`, `output_to`, and `trace_required`. Missing source or missing policy blocks field validation.

## V00.4 Rule Logic Validator

Each rule must include `rule_id`, `rule_type`, `input_fields`, `calculation_method`, `threshold_or_condition`, `positive_evidence`, `counter_evidence`, `confidence_logic`, `failure_condition`, `output_status`, and `trace_required`. Rules that only say “AI 判断” are rejected.

## V00.5 Schema Validator

Validate all JSON schemas listed by F00 and all V00 validation schemas. Write valid/invalid schema lists and errors. Do not set `SCHEMA_VALIDATED` without actual parser/validator output.

## V00.6 Contract Validator

Validate input, output, and handoff contracts for required inputs/outputs, validation evidence, state enums, gap preservation, unresolved gap handoff, allowed actions, and forbidden actions.

## V00.7 Patch Evidence Validator

If F00 claims implementation, require patch plan, modified_files, diff_summary, change_trace, rollback_plan, and actual file existence/content match. Status must be one of `PATCH_NOT_REQUIRED`, `PATCH_PLANNED_ONLY`, `PATCH_EVIDENCE_VALID`, `PATCH_EVIDENCE_MISSING`, `PATCH_FAILED`.

## V00.8 Test Execution Evidence Collector

A test is evidence only when it records command, type, file, started_at, ended_at, exit_code, stdout_path, stderr_path, passed_count, failed_count, covered_functions, covered_rules, and failure_reason. Test plan alone is `TEST_PLANNED`, not `TESTED`.

## V00.9 Replay Evidence Collector

Replay must produce `replay_input.json`, `replay_output.json`, `replay_trace.jsonl`, `replay_evidence.json`, and `replay_report.md`. Replay plan alone is `REPLAY_PLANNED`, not `REPLAY_TESTED`.

## V00.10 Trace / Audit Validator

Confirm all required events exist: `v00_started`, `f00_handoff_loaded`, `preflight_passed`, `input_evidence_loaded`, `function_mapping_validated`, `field_model_validated`, `rule_logic_validated`, `schema_validated`, `contract_validated`, `patch_evidence_validated`, `test_executed`, `replay_executed`, `failure_evidence_written`, `acceptance_checked`, `handoff_written`, `v00_completed`, and/or `v00_blocked`.

## V00.11 Gap & Failure Evidence Classifier

Classify all missing/failed evidence into gap/failure records with `gap_level`, affected function/asset, evidence path, required fix, and `can_continue`.

## V00.12 Acceptance Precheck

Return one final state: `V00_ACCEPTED`, `V00_READY_WITH_GAPS`, `V00_BLOCKED`, or `V00_REJECTED`. Preserve non-blocking unresolved gaps and block all downstream handoff if a blocking gap exists.

## V00.13 Handoff Writer

Write R00/A00 handoff packets including all validation refs, evidence refs, trace refs, gaps, failures, acceptance refs, allowed next actions, forbidden next actions, and unresolved gaps.
