# G00 Execution Protocol

1. Load `04_g00_input_contract.json` and validate governance candidates, A00 evidence bundle, gap reports, trace refs, audit refs, governance policy, and execution boundary.
2. Load U00 governance candidates only through declared refs; do not bypass evidence chain.
3. Classify each governance candidate into a policy domain and risk level.
4. Build forbidden action registry, status code table, execution boundary policy, evidence policy, gap policy, directory policy, contract policy, runner safety policy, human confirmation policy, production risk policy, and versioning policy.
5. Detect policy conflicts and weakenings; reject or defer conflicting candidates.
6. Write active, pending, rejected, and deprecated policy registries.
7. Emit trace and audit logs.
8. Generate downstream handoff for all controllers.
9. Do not mark G00 complete unless the acceptance gate passes.

## G00.0 Preflight Gate
- Missing A00 evidence bundle => G00_BLOCKED
- Missing gap reports => G00_BLOCKED
- Missing trace refs or audit refs => G00_BLOCKED
- Missing governance policy => G00_BLOCKED
- Missing execution boundary => G00_BLOCKED
- No U00 governance candidates => G00_READY_WITH_GAPS or G00_BLOCKED depending on remaining evidence

## G00.1 Governance Evidence Loader
Load candidate refs, evidence bundle, failure evidence, gap reports, trace refs, audit refs, and current registry.

## G00.2 Governance Candidate Classifier
Classify candidates into forbidden action, status, evidence, gap, directory, contract, schema, runner safety, human confirmation, production risk, versioning, deprecation, recovery, or handoff domains.

## G00.3 Policy Domain Mapper
Map each candidate to its target policy file and activation mode.

## G00.4 Forbidden Action Registry Builder
Build hard-block registry for live runtime, wallet signing, auto deploy, production trading, real order execution, direct production mutation, and evidence tampering.

## G00.5 Status Code Table Builder
Define canonical status semantics and required evidence for design, implementation, validation, binding, acceptance, and handoff states.

## G00.6 Execution Boundary Policy Builder
Define phase-by-phase execution modes and forbidden runtime modes.

## G00.7 Evidence Policy Builder
Define the minimum evidence required for TESTED, REPLAY_TESTED, RUNNER_BOUND, IMPLEMENTED, and ACCEPTED claims.

## G00.8 Gap Policy Builder
Define blocking gaps, propagation rules, and downgrade behavior.

## G00.9 Directory / Write Boundary Policy Builder
Define raw append-only, trace/audit append-only, run-scoped writes, and legacy read-only paths.

## G00.10 Contract / Schema Governance Builder
Define required fields for input, output, handoff, and schema artifacts.

## G00.11 Runner Safety Policy Builder
Define safe-dry-run only defaults, scheduler disabled defaults, and live runtime forbiddance.

## G00.12 Human Confirmation Policy Builder
Define situations requiring manual approval.

## G00.13 Production Risk Boundary Builder
Define hard-block production risk boundaries.

## G00.14 Policy Conflict / Versioning Manager
Resolve duplicates, contradictions, weakenings, supersessions, and deprecations with explicit version history.

## G00.15 Governance Registry Writer
Write active, pending, deprecated, and rejected policy registries.

## G00.16 Acceptance Gate
Acceptance requires evidence-backed classification, policy output, conflict checking, registry writes, trace, audit, and handoff.

## G00.17 Handoff Writer
Emit handoff packets for K00, F00, V00, R00, A00, H00, U00, PXX, and IXX consumers.

## Prompt Completeness Enforcement

G00 must reject or downgrade any run that violates these prompt-defined atoms:

- `DESIGN_ONLY` cannot be rewritten as `IMPLEMENTED`.
- `PLANNED_NOT_WRITTEN` cannot be rewritten as `IMPLEMENTED`.
- `test_plan` cannot satisfy `TESTED`.
- `replay_plan` cannot satisfy `REPLAY_TESTED`.
- `binding_plan` cannot satisfy `RUNNER_BOUND`.
- `READY_WITH_GAPS` cannot be rewritten as `READY` or `ACCEPTED` without closing or explicitly accepting every gap.
- Every `BLOCKING_GAP` must use `effect: BLOCK_NEXT_PHASE` and `must_propagate: true`.
- Runner binding permits `SAFE_DRY_RUN` only by default; scheduler is disabled by default; `LIVE_RUNTIME` is forbidden by default.
- Human confirmation is mandatory for `production_rule_change`, `runner_scheduler_enable`, `paper_runtime_enable`, `legacy_path_migration`, `external_api_write`, and `large_scale_batch_change`.
- Production risks `WALLET_SIGNING_RISK`, `AUTO_DEPLOY_RISK`, `LIVE_RUNTIME_RISK`, and `EXTERNAL_API_WRITE_RISK` must not be silently allowed.
