# F00 Recovery Policy

## Recovery triggers

- Missing or invalid K00 handoff
- Missing document passport / corpus index / system mapping
- KV conflict with existing rule, field, schema, or contract
- Required function cannot be mapped to fields or rule logic
- Implementation decision blocked by missing data, production risk, or unknown codebase
- Handoff packet fails schema validation

## Recovery actions

1. Mark F00 state as `FUNCTION_BLOCKED` or `READY_WITH_GAPS`.
2. Write explicit gap references.
3. Preserve all source refs and partial outputs.
4. Do not promote to PATCH_APPLIED, TESTED, REPLAY_TESTED, RUNNER_BOUND, or ACCEPTANCE_PASSED.
5. Generate downstream recovery handoff for K00 / Governance / Review as appropriate.
