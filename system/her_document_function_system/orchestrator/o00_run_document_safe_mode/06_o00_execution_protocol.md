# O00 Execution Protocol

1. Require `--safe-mode` for `run-document`, `run-sample`, `resume`, `recover`, and config validation.
2. Load source document, operator goal, registry, and safe-mode pipeline config.
3. Block immediately if execution boundary allows live runtime, wallet signing, auto deploy, production trading, or real order execution.
4. Validate O00/K00/F00/V00/R00/A00/H00/U00/G00 controller registration.
5. Create run directory under `data/her_document_function_system/o00_run_document_runs/<run_id>/` for real document safe-mode runs.
6. Build stage plan and dependency graph.
7. Execute only safe-mode/design-level stage binding; do not run live/paper/prod runtime.
8. Write stage refs, simulated/safe handoffs, evidence bundle, gap register, trace/audit, acceptance result, recovery report, and final report.
9. Return `PIPELINE_READY_WITH_GAPS` when evidence exists but downstream real implementation/test/runner/governance proof is absent.
10. Never convert TEST_PLANNED to TESTED, RUNNER_PLANNED to RUNNER_BOUND, POLICY_CANDIDATE to POLICY_ACTIVE, or QUEUE_CREATED to TASK_EXECUTED.

## Subphases
- O00.0 Safe-mode Preflight Gate
- O00.1 Input Evidence Loader
- O00.2 Registry / Config Validator
- O00.3 Pipeline Execution Plan Builder
- O00.4 Stage Dependency Graph Builder
- O00.5 Safe Stage Dispatch Binder
- O00.6 Evidence Bundle Collector
- O00.7 Gap / False-Claim Classifier
- O00.8 Acceptance Calculator
- O00.9 Handoff / Final Report Writer
