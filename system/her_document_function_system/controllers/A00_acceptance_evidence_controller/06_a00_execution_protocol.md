# A00 Execution Protocol

## A00.0 Preflight Gate
Require K00, F00, V00 handoff packets; require R00 handoff when runner_binding_required=true. Require phase_state_refs, gap_report_refs, trace_refs, audit_refs, artifact_refs, execution_boundary, and acceptance_policy. Forbid live runtime, wallet signing, auto deploy, production trading, and direct production rule modification.

## A00.1 Upstream Handoff Loader
Load K00/F00/V00/R00 handoff refs, phase states, gap reports, trace/audit refs, and artifact refs. Missing K00/F00/V00 blocks A00. Missing R00 blocks only when runner binding is required.

## A00.2 Evidence Bundle Builder
Build evidence_bundle containing source_document_evidence, k00_intake_evidence, kv_index_evidence, f00_function_mapping_evidence, f00_field_model_evidence, f00_rule_logic_evidence, f00_asset_plan_evidence, v00_schema_validation_evidence, v00_contract_validation_evidence, v00_test_evidence, v00_replay_evidence, r00_binding_evidence, r00_dry_run_evidence, trace_evidence, audit_evidence, gap_evidence, failure_evidence, and handoff_evidence.

## A00.3 Evidence Integrity Checker
Verify required evidence exists, is referenced by manifest, is not just a plan, and does not contradict phase state. Missing test execution evidence cannot be treated as tested. Missing dry-run evidence cannot be treated as runner bound.

## A00.4 Phase Status Matrix Builder
Create matrix for K00/F00/V00/R00 with reported_status, evidence_status, blocking_gaps, non_blocking_gaps, handoff_status, trace_status, acceptance_status, and a00_interpretation.

## A00.5 Status Consistency Validator
Detect DESIGN_AS_IMPLEMENTED, TEST_PLAN_AS_TESTED, BINDING_PLAN_AS_BOUND, READY_WITH_GAPS_AS_READY, MISSING_TRACE_BUT_ACCEPTED, and MISSING_HANDOFF_BUT_READY. Downgrade inconsistent states.

## A00.6 Artifact Manifest Validator
Validate existence and hashes for raw input, registry, passport, corpus index, system mapping, gap report, KV index, function mapping, field model, rule logic, asset plan, schema, contract, patch evidence, test evidence, replay evidence, binding manifest, command contract, dry-run evidence, trace, audit, handoff packet, and final reports.

## A00.7 Gap Propagation Validator
Ensure K00 gaps propagate to F00 or are resolved; F00 gaps propagate to V00 or are resolved; V00 gaps propagate to R00/A00 or are resolved; R00 gaps propagate to A00/U00 or are resolved. Hidden gaps block acceptance.

## A00.8 Trace / Audit Integrity Validator
Check required events: K00 intake_started/passport_created/handoff_written; F00 function_mapped/field_model_created/handoff_written; V00 validation_started/test_executed/replay_executed/handoff_written; R00 binding_created/dry_run_completed/handoff_written when required; A00 evidence_bundled/decision_made/handoff_written.

## A00.9 Acceptance Gate Replay
Replay gate logic from K00/F00/V00/R00 acceptance results without re-running business implementation. Verify each phase acceptance gate had evidence and no false pass condition.

## A00.10 Acceptance Scorecard Builder
Build dimension status for document_integrity, function_realization, data_model_quality, rule_logic_quality, schema_contract_quality, validation_quality, runner_binding_quality, trace_audit_quality, gap_management_quality, handoff_quality, and governance_safety. Each dimension needs evidence_refs, gap_refs, status, score, and decision_weight.

## A00.11 Readiness Decision Engine
Emit A00_ACCEPTED, A00_READY_WITH_GAPS, A00_BLOCKED, A00_REJECTED, SYSTEM_READY_FOR_HANDOFF, SYSTEM_READY_WITH_GAPS, SYSTEM_BLOCKED, SYSTEM_REJECTED, DESIGN_ONLY, PARTIALLY_IMPLEMENTED, VALIDATED_NOT_BOUND, BOUND_NOT_FULLY_ACCEPTED, or NOT_EXECUTED based on evidence, not prose.

## A00.12 Failure / Recovery Classifier
Classify missing_handoff, missing_evidence, status_inconsistency, artifact_missing, schema_validation_missing, test_evidence_missing, replay_evidence_missing, binding_evidence_missing, trace_missing, gap_hidden, acceptance_gate_invalid, governance_violation, and production_risk_detected. Every failure must enter failure_summary and recovery_report.

## A00.13 Readiness Certificate Writer
Write readiness_certificate with certificate_id, source_doc_ids, accepted_phases, final_status, readiness_level, evidence_bundle_ref, open_gaps, accepted_risks, allowed_next_actions, forbidden_next_actions, issued_at, and issued_by.

## A00.14 Handoff Writer
Write downstream handoff packets to H00/U00/G00 with source_doc_refs, K00/F00/V00/R00 refs, evidence_bundle_refs, phase_status_matrix_refs, artifact_manifest_refs, gap_propagation_refs, trace_audit_refs, acceptance_scorecard_refs, readiness_certificate_refs, failure_refs, recovery_refs, allowed_next_actions, forbidden_next_actions, unresolved_gaps, and accepted_risks.

## False Pass Rules
- No K00 handoff → A00_BLOCKED.
- No F00 handoff → A00_BLOCKED.
- No V00 handoff → A00_BLOCKED.
- Runner required but no R00 handoff → SYSTEM_BLOCKED.
- No evidence bundle → no acceptance pass.
- No artifact manifest → no acceptance pass.
- No trace/audit → no acceptance pass.
- Hidden gap → no acceptance pass.
- BLOCKING_GAP → no A00_ACCEPTED.
- Design only cannot be marked implemented.
- Test plan cannot be marked tested.
- Binding plan cannot be marked runner bound.
- READY_WITH_GAPS cannot be rewritten to READY.
