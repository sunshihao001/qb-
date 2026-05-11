---
artifact_type: session_reference
status: verified
version: v1.2
valid_until: null
---
# Hermes V1.2 Architecture Session Notes

## Target architecture snapshot

Canonical runtime root:

`/root/sikk-gmgn/hermes_harness/`

Required V1.2 layers:

- `00_startup/`
- `01_control_plane/`
- `02_task_intake/`
- `03_task_runtime/`
- `04_memory/`
- `05_templates/`
- `06_verification/`
- `07_recovery/`
- `08_reports/`
- `09_scripts/`
- `10_audit/`
- `11_workflows/`

## Runtime must-haves

- `03_task_runtime/active_task_state.json`
- `03_task_runtime/active_task_context.md`
- `03_task_runtime/input_governance_queue.jsonl`
- `03_task_runtime/context_budget.json`
- `03_task_runtime/tool_ledger.jsonl`
- `03_task_runtime/recovery_counter.json`
- `03_task_runtime/execution_narrative.md`
- `03_task_runtime/execution_loop_log.jsonl`
- `03_task_runtime/command_log.jsonl`
- `04_memory/memory_verification_log.jsonl`
- `04_memory/stale_memory.jsonl`
- `04_memory/superseded_memory.jsonl`
- `04_memory/verified_memory.jsonl`
- `07_recovery/recovery_reports/`
- `07_recovery/interrupt_reports/`
- `07_recovery/blocked_tasks/`
- `11_workflows/*.workflow.md`

## New policy classes

- input governance
- runtime state
- context budget
- bash risk
- recovery circuit breaker
- interrupt handling
- tool ledger
- execution narrative
- runtime judgment

## Verification scripts

- `hermes_input_governance.py`
- `hermes_context_budget_check.py`
- `hermes_bash_classifier.py`
- `hermes_tool_ledger_check.py`
- `hermes_compact_rebuild.py`
- `hermes_narrative_check.py`
- `hermes_memory_revalidate.py`
- `hermes_recovery_circuit_check.py`
- `hermes_v12_architecture_check.py`
