# Long-Term Rule Candidates V1

These rules are verified candidates for future Hermes control-plane hardening.

## Candidate 1: Read-only reconnaissance before map creation
- Always inventory first.
- Never migrate before a map exists.

## Candidate 2: Registry before migration
- Build path registry and module registry before any directory move.
- Keep legacy paths in place until canonical destinations are verified.

## Candidate 3: Conflict audit before standardization
- Detect root scatter, stale paths, and module overlap before proposing standard paths.

## Candidate 4: Checkpointed long tasks
- Every long governance task must have phase checkpoints and resume points.

## Candidate 5: Verification before completion
- No governance task is complete without machine-readable inventories and a verification report.
