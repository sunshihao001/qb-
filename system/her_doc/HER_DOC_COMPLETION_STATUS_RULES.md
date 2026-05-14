# HER_DOC Completion Status Rules

## Status Ladder

- `NOT_STARTED`: no file-backed source or scope exists.
- `SOURCE_REGISTERED`: source or missing-source record exists.
- `PASSPORT_READY`: document passport exists and meets minimum schema.
- `MAPPED_WITH_GAPS`: functional/system mapping exists and gaps are preserved.
- `EVIDENCE_READY_WITH_GAPS`: evidence requirements are assigned, available evidence checked, unresolved gaps queued.
- `RUNTIME_BINDING_REVIEWED_WITH_GAPS`: safe binding review was attempted and blockers are explicit.
- `VALIDATOR_PROJECT_GATE_PASSED`: `HER_DOC_VALIDATOR.py project` returned `status=PASS` and `issue_count=0`.
- `VALIDATOR_BUNDLE_GATE_PASSED`: `HER_DOC_VALIDATOR.py bundle <output_dir>` returned `status=PASS` and `issue_count=0`.
- `ACCEPTED_FOR_DOWNSTREAM`: downstream handoff/acceptance packet exists and cites evidence.
- `FULL_FLOW_ACCEPTED`: all protocol steps passed, project validator passed, bundle validator passed, evidence thresholds passed, and downstream handoff exists.
- `BLOCKED_VALIDATOR_PROJECT_GATE`: HER_DOC control project validator failed; business/deep scan must not start.
- `BLOCKED_VALIDATOR_BUNDLE_GATE`: scan outputs failed validator bundle gate; do not claim full scan completed.
- `BLOCKED`: required source, safety boundary, schema, or evidence is missing.
- `REJECTED`: evidence contradicts claim or violates policy.

## Evidence Coverage Gate

- `<50%`: `HER_DOC_ASSET_SCAN_ONLY`
- `50%-79%`: `HER_DOC_ASSET_SCAN_COMPLETED_WITH_DEEP_SCAN_GAPS`
- `80%-94%`: `HER_DOC_EVIDENCE_SCAN_COMPLETED_WITH_GAPS`
- `95%+ plus validator gates plus runtime/handoff proof`: `HER_DOC_EVIDENCE_SCAN_ACCEPTED`

## Validator Gate Rules

- Full trading system deep scan cannot begin unless project validator passes.
- Full scan output cannot be called complete unless bundle validator passes.
- Bundle validator pass only proves output artifact completeness; it does not prove evidence coverage, runtime readiness, P09 readiness, P10 readiness, or downstream acceptance.
- Validator result JSON must be preserved in the scan output directory when applicable.

## Non-Equivalence Rules

- Report written ≠ execution complete.
- Queue created ≠ work completed.
- Plan drafted ≠ implementation built.
- File exists ≠ schema valid.
- Schema valid ≠ runtime tested.
- Validator bundle pass ≠ evidence accepted.
- Dry run passed ≠ live binding approved.
- HER_DOC accepted ≠ trading/runtime accepted.

## Minimum Evidence Per Claim

- `PRESENT`: E2 + file-read or schema proof.
- `READY`: E3 + required field completeness.
- `RUNTIME_READY`: E4 safe runtime proof.
- `DOWNSTREAM_ACCEPTED`: E5 handoff/acceptance proof.

Default non-trivial completion state: `EVIDENCE_READY_WITH_GAPS`.
