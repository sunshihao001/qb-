# A00 Recovery Policy

## Missing handoff
- missing_k00_handoff / missing_f00_handoff / missing_v00_handoff: status A00_BLOCKED; safe_next_action: return to missing upstream phase and write formal handoff.
- missing_r00_handoff when runner_binding_required=true: status SYSTEM_BLOCKED; safe_next_action: return to R00.

## Missing evidence
- Missing evidence_bundle, artifact_manifest, test_evidence, replay_evidence, trace, or audit blocks A00_ACCEPTED.
- Test plan is not test evidence; binding plan is not dry-run evidence; design is not implementation.

## Status inconsistency
- If reported status is READY but evidence has non-blocking gaps, downgrade to READY_WITH_GAPS.
- If reported status is TESTED but no command/stdout/stderr/exit_code exists, downgrade to BLOCKED or DESIGN_ONLY.

## Hidden gap
- Any hidden_gap_detected blocks acceptance.
- Required fix: restore original gap refs, classify status, and propagate to final report/handoff/U00.

## Production risk
- Any live runtime, wallet signing, auto deploy, production trading, or direct production rule modification attempt is governance violation and blocks A00.

## Recovery outputs
Every failure must be written to failure_summary and recovery_report with affected_phase, affected_asset, required_fix, safe_next_action, forbidden_next_action, and current_status.
