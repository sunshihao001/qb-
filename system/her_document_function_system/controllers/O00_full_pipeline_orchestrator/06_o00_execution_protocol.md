# O00 / R99 Execution Protocol

## Non-negotiable guards
- No G00 active policy bundle, no pipeline start.
- No controller registry, no stage dispatch.
- No K00 handoff, no F00.
- No F00 handoff, no V00.
- No V00 handoff, no R00.
- No A00 readiness certificate, no H00.
- DESIGN_ONLY is not IMPLEMENTED.
- test_plan is not TESTED.
- binding_plan is not RUNNER_BOUND.
- Forbidden modes remain forbidden: live_runtime, wallet_signing, auto_deploy, production_trading.

## O00.0 Governance Preflight Gate
Load G00 active policy bundle and block if safe_mode is not true.
## O00.1 Pipeline Run Initializer
Create pipeline_run_id under o00_runs.
## O00.2 Controller Registry Loader
Load G00/K00/F00/V00/R00/A00/H00/U00 registry.
## O00.3 Source Intake Router
Route NEW_DOCUMENT_INTAKE, REPROCESS_EXISTING_DOCUMENT, RESUME_BLOCKED_PIPELINE, REPLAY_SAMPLE_PIPELINE, UPGRADE_EXISTING_CONTROLLER, GOVERNANCE_UPDATE_ONLY, REVIEW_ONLY or REJECT_INPUT.
## O00.4 Pipeline Execution Plan Builder
K00/F00/V00/A00 are not skippable. R00 is optional only by runner_binding_required.
## O00.5 Stage Dependency Graph Builder
Build G00 policy → O00 → K00 → F00 → V00 → R00 → A00 → H00 → U00 → G00.
## O00.6 Stage Queue Builder
Build QUEUED/READY/RUNNING/COMPLETED/COMPLETED_WITH_GAPS/BLOCKED/FAILED/SKIPPED/DEFERRED/RETRY_PENDING queue.
## O00.7 Stage Transition Gate Manager
Check handoff, acceptance, gaps, forbidden actions, input contract and G00 policy.
## O00.8 K00 Dispatch Manager
Dispatch K00 only with source, policy, write boundary and controller.
## O00.9 F00 Dispatch Manager
Dispatch F00 only with accepted K00 handoff.
## O00.10 V00 Dispatch Manager
Dispatch V00 only with F00 handoff and mapping/model/rules/test plan.
## O00.11 R00 Dispatch Manager
Dispatch R00 only when binding is required and V00 evidence exists.
## O00.12 A00 Dispatch Manager
Dispatch A00 only with required handoffs and evidence.
## O00.13 H00 Dispatch Manager
Dispatch H00 only with A00 readiness certificate and evidence bundle.
## O00.14 U00 / G00 Feedback Loop Manager
Route gaps, failures, blocked, design_only, not_executed and governance candidates.
## O00.15 Gap / Failure Propagation Manager
Never delete gaps; resolve, accept risk, defer, invalidate or supersede.
## O00.16 Pipeline Acceptance Matrix Builder
Evaluate Governance, Intake, Function, Validation, Binding, Acceptance, Handoff, Review, Audit, Risk.
## O00.17 Recovery / Retry / Defer Manager
Decide RETRY_STAGE, RETURN_TO_PREVIOUS_STAGE, ROUTE_TO_U00, ROUTE_TO_G00, DEFER_TO_BACKLOG, BLOCK_PIPELINE, REJECT_INPUT, REQUIRE_HUMAN_CONFIRMATION.
## O00.18 Final Report & Handoff Writer
Write true final_pipeline_status; never convert design/plan/gap to implementation claims.
