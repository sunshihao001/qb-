# U00 Execution Protocol

1. Load `04_u00_input_contract.json`.
2. Validate H00 handoff and A00 evidence bundle as mandatory upstream artifacts.
3. Classify all incoming failures, gaps, blocked items, READY_WITH_GAPS items, DESIGN_ONLY items, NOT_EXECUTED items, and governance risks into review cases.
4. Normalize issues into canonical phase-neutral records.
5. Run root cause analysis and preserve causal chains.
6. Detect recurring issues and anti-patterns.
7. Build upgrade candidates for controllers, schemas, contracts, tests, replay, runner binding, and governance.
8. Convert upgrade candidates into queue items and backlog items.
9. Write learning index entries for stable lessons and anti-patterns.
10. Emit trace and audit logs.
11. Produce downstream handoff packets.
12. Do not claim acceptance unless the acceptance gate passes.

## U00.0 Preflight Gate
- H00 handoff missing => U00_BLOCKED
- A00 evidence bundle missing => U00_BLOCKED
- gap reports missing => U00_BLOCKED
- queue state missing => U00_READY_WITH_GAPS or U00_BLOCKED depending on severity
- trace/audit missing => U00_READY_WITH_GAPS or U00_BLOCKED
- upgrade policy missing => U00_BLOCKED

## U00.1 Evidence & Queue Loader
Load H00 handoff, A00 evidence bundle, phase status matrix, gap reports, failure evidence, queue state, trace refs, and audit refs.

## U00.2 Review Case Classifier
Classify issues into GAP_CASE, FAILURE_CASE, BLOCKED_CASE, READY_WITH_GAPS_CASE, DESIGN_ONLY_CASE, NOT_EXECUTED_CASE, TEST_FAILED_CASE, REPLAY_FAILED_CASE, BINDING_FAILED_CASE, HANDOFF_FAILED_CASE, GOVERNANCE_RISK_CASE, RECURRING_ISSUE_CASE, SUCCESS_PATTERN_CASE.

## U00.3 Failure / Gap Normalizer
Normalize issue records into source_phase, severity, symptom, affected_assets, evidence_refs, and current_status.

## U00.4 Root Cause Analysis Engine
Derive root_cause_type, root_cause_statement, causal_chain, confidence, required_fix_type, and recommended_owner.

## U00.5 Recurring Issue Detector
Aggregate frequency across phases, assets, and failure modes.

## U00.6 Anti-pattern / Success-pattern Extractor
Record repeatable failure patterns and repeatable success patterns.

## U00.7 Upgrade Candidate Builder
Create upgrade candidates with target_controller, target_asset, proposed_change, priority, and evidence_refs.

## U00.8 Controller Upgrade Mapper
Map each candidate to K00/F00/V00/R00/A00/H00/G00 or backlog.

## U00.9 Schema / Contract / Test Upgrade Mapper
Map candidates to schema, contract, test, replay, and validation assets.

## U00.10 Runner / Tool Upgrade Mapper
Map candidates to CLI, orchestrator, Telegram, scheduler, dashboard, and dry-run bindings.

## U00.11 Governance Candidate Extractor
Convert systemic policy issues into governance candidates for G00.

## U00.12 Upgrade Queue Builder
Prioritize P0_CRITICAL, P1_HIGH, P2_MEDIUM, P3_LOW, P4_BACKLOG items.

## U00.13 Learning Index Writer
Persist anti-patterns, success patterns, recurring gaps, and controller upgrade rules.

## U00.14 Trace / Audit Binder
Write event logs for every transition.

## U00.15 Acceptance Gate
Acceptance requires evidence-backed review cases, root cause analysis, upgrade candidates, queue items, learning index, trace, audit, and handoff.

## U00.16 Handoff Writer
Emit handoff packets to K00, F00, V00, R00, G00, and backlog targets.
