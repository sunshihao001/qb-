---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Runtime State Policy

## Purpose
`active_task_state.json` is not an auxiliary file. It is the primary runtime business object of Hermes Harness.

Hermes must treat task state as the source of truth for execution, recovery, verification, compaction, and transition decisions.

## Required Runtime State Fields
The runtime state should include at least:

```json
{
  "task_id": "hermes.task.20260506.001",
  "status": "EXECUTING",
  "turn_count": 7,
  "current_phase": "phase_03_execution",
  "context_budget_status": "OK",
  "tool_ledger_status": "BALANCED",
  "recovery_attempts": 0,
  "last_transition_reason": "verification_passed",
  "pending_tool_calls": [],
  "pending_verification": true,
  "compact_required": false,
  "abort_requested": false,
  "next_action": "run verification"
}
```

## Runtime Responsibilities
The state file must track:
- messages or message references
- tool-use context
- context budget status
- auto/micro compaction requirements
- recovery attempt count
- turn count
- pending tool calls
- pending verification
- transition reason
- abort or interruption status

## State Transition Rules
- Every phase transition must update `last_transition_reason`.
- Every tool call must update or confirm `tool_ledger_status`.
- Every turn must increment or preserve `turn_count` according to execution semantics.
- Every failed verification must increment or annotate `recovery_attempts`.
- If `compact_required=true`, context assembly must run before the next model call.
- If `abort_requested=true`, no execution may continue until recovery or user confirmation.

## Hard Rules
- Do not treat state as a passive report.
- Do not declare DONE unless `pending_tool_calls=[]` and `pending_verification=false`.
- Do not continue execution if `tool_ledger_status` is unbalanced.
- Do not hide recovery loops; count and report them.
- Runtime state must be updated before final reports.

## Status Values
- RECEIVED
- GOVERNING_INPUT
- PLANNING
- EXECUTING
- VERIFYING
- RECOVERING
- BLOCKED
- DONE
- ARCHIVED
