# G00 Recovery Policy

- Missing A00 evidence bundle => block.
- Missing gap reports => block.
- Missing trace or audit => block.
- Missing governance policy or execution boundary => block.
- Missing evidence refs for a policy => do not activate; keep pending or reject.
- Conflicting or weakened policy => reject candidate or version as deprecated.
- Never silently overwrite active policy.
- Never claim accepted governance without registry write, trace, audit, and handoff.

## Required downgrades

- Missing test command / exit_code / stdout_path / stderr_path => downgrade TESTED to TEST_PLANNED_ONLY.
- Missing replay input / output / trace / acceptance => downgrade REPLAY_TESTED to REPLAY_PLANNED_ONLY.
- Missing dry-run evidence => downgrade RUNNER_BOUND to BINDING_DESIGNED.
- Missing written file evidence => downgrade IMPLEMENTED to DESIGN_ONLY or PLANNED_NOT_WRITTEN.
- Any BLOCKING_GAP with unresolved status => BLOCK_NEXT_PHASE and must_propagate true.
- Scheduler enablement without human confirmation => BLOCK_ACTION.
- paper_runtime_enable without approval => BLOCK_ACTION.
- legacy_path_migration without approval => BLOCK_ACTION.
- external_api_write without approval => BLOCK_ACTION.
- WALLET_SIGNING_RISK / AUTO_DEPLOY_RISK / LIVE_RUNTIME_RISK => HARD_BLOCK.
