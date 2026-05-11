     1|# 09_scripts
     2|
     3|Runnable helpers and checkers.
     4|# 09 Scripts
     5|
     6|## APUR Loop scripts
     7|
     8|- `hermes_problem_loop_run.py` — APUR safe dry-run runner.
     9|- `hermes_runtime_hook_run.py` — V1.4 runtime hook runner; creates runtime_state, tool_ledger, problem_passport, completion_audit, and memory_write_queue candidate.
    10|- `hermes_problem_intake.py` / `hermes_problem_understand.py` / `hermes_evidence_plan.py` / `hermes_hypothesis_generate.py` / `hermes_root_cause_analyze.py` / `hermes_solution_design.py` / `hermes_resolution_verify.py` / `hermes_failure_attribution.py` / `hermes_learning_writeback.py` — stage-compatible wrappers.
    11|
    12|## V1.4 usable launcher
    13|
    14|- `hermes_runtime_hook_launcher.py` — stable CLI/Gateway/quick-command launcher wrapping `hermes_runtime_hook_run.py`; supports `--problem`, `--dry-run`, `--origin`, `--json`.
    15|- `HER_RUNTIME_HOOK_QUICK_COMMANDS.md` — `/HER_START` / `/HER_SYSTEM_DESIGN` quick command mapping and JSON output contract.
    16|

## V1.6 Judgment Governance

- `hermes_judgment_governance_run.py` — V1.6 judgment governance runner; outputs problem triage, evidence sufficiency, abstention gate, solution cost review, meta verification, anti-self-deception audit, causal graph, memory lifecycle review, operator gate, and judgment error tracking.
