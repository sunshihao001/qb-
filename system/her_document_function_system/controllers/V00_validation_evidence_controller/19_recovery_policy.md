# V00 Recovery Policy

V00 failures are evidence, not embarrassment. Failed checks must be recorded, classified, and handed off.

## missing F00 handoff

- status: `V00_BLOCKED`
- failure_type: `missing_f00_handoff`
- gap_level: `BLOCKING_GAP`
- required_fix: rerun or repair F00 and provide a file-backed `f00_handoff_packet`.
- can_continue: false

## schema invalid

- status: `SCHEMA_INVALID`
- failure_type: `invalid_schema`
- gap_level: `BLOCKING_GAP` when schema is required by contract; otherwise `HIGH_GAP`.
- required_fix: fix schema syntax/structure and rerun V00.5.

## contract invalid

- status: `CONTRACT_INVALID`
- failure_type: `invalid_contract`
- gap_level: `BLOCKING_GAP`
- required_fix: align input/output/handoff contracts and preserve unresolved gaps.

## test failed

- status: `TEST_FAILED`
- failure_type: `test_failed`
- gap_level: `BLOCKING_GAP` for required functional tests.
- required_fix: fix root cause, do not hide failed tests, rerun same command, keep stdout/stderr evidence.

## replay failed

- status: `REPLAY_FAILED`
- failure_type: `replay_failed`
- gap_level: `BLOCKING_GAP` for professional-grade acceptance.
- required_fix: repair sample chain or explicitly downgrade to `V00_READY_WITH_GAPS` if non-blocking and accepted by downstream policy.

## trace missing

- status: `TRACE_MISSING`
- failure_type: `missing_trace` or `missing_audit`
- gap_level: `BLOCKING_GAP`
- required_fix: generate immutable trace/audit records for all executed validation steps.

## production risk detected

- status: `V00_BLOCKED`
- failure_type: `production_risk_detected`
- gap_level: `BLOCKING_GAP`
- required_fix: remove live runtime, wallet signing, auto deploy, production rule mutation, or source deletion request from the run boundary.
