# Phase09 Handoff Rules

Phase09 handoff is a system-upgrade governance packet, not an apply command.

## Ready handoff

Ready requires:

- Phase08 handoff readable.
- Required Phase08 files readable.
- Candidates have `target_phase` and `evidence_cases`.
- Regression validation passes.
- Rollback plan exists.
- Upgrade package exists.
- `requires_manual_confirmation=true`.
- `allow_apply_to_runtime=false`.
- `recommended_apply_mode=SHADOW_MODE_FIRST`.

## Blocked handoff

Handoff must be blocked when:

- Phase08 handoff is missing.
- Required Phase08 summary/failure/candidate inputs are missing.
- Candidate target phase is missing.
- Candidate evidence cases are missing.
- Regression validation fails.
- Rollback plan is missing.

## Downstream rule

No downstream runtime is allowed to apply Phase09 output directly. It may only read the package for review, shadow-mode testing, manual confirmation, or staged rollout planning.
