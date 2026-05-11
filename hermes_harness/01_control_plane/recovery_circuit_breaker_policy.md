---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Recovery Circuit Breaker Policy

## Purpose
Recovery itself must be governed. Hermes must not retry the same failure endlessly.

## Required Runtime Counter
`03_task_runtime/recovery_counter.json`

## Example Structure
```json
{
  "task_id": "hermes.task.20260506.001",
  "same_error_count": 2,
  "max_same_error_retry": 3,
  "recovery_attempts": [
    {
      "error_type": "json_invalid",
      "attempt": 1,
      "action": "repair_json",
      "result": "failed"
    }
  ],
  "circuit_breaker_status": "OPEN_IF_NEXT_FAILS"
}
```

## Hard Rules
- Same-class errors may be retried at most 3 times.
- After 3 failures, the task must enter `BLOCKED`.
- `BLOCKED` must produce a recovery report.
- Infinite retry must never be disguised as continued execution.
- Recovery attempts must be counted by error class, not only by raw turn count.

## Status Values
- CLOSED
- OPEN_IF_NEXT_FAILS
- OPEN
- HALF_OPEN
- BLOCKED

## Required Recovery Records
Each recovery attempt should record:
- task_id
- error_type
- attempt
- action
- result
- timestamp
- whether the attempt changed state
- whether a human confirmation is required

## Transition Rules
- First failure: record attempt 1.
- Second failure of same class: escalate risk.
- Third failure of same class: set circuit breaker to open or blocked state.
- Fourth attempt on same class: forbidden unless a human explicitly resets the circuit.

## Reporting Rules
Whenever the circuit breaker opens or the task becomes blocked:
- write recovery report
- update runtime state
- do not claim the task is still executing normally
