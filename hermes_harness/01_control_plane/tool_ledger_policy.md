---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Tool Ledger Policy

## Purpose
Every Hermes tool call must be closed by a corresponding result record. Tool calls cannot remain suspended, invisible, or implied.

## Required Runtime Ledger
Tool records live in:

`03_task_runtime/tool_ledger.jsonl`

## Required Fields
Each record should include:

```json
{
  "tool_call_id": "tool.0001",
  "task_id": "hermes.task.20260506.001",
  "phase_id": "phase_02",
  "tool": "bash",
  "command": "mkdir -p hermes_harness/01_control_plane",
  "permission": "ALLOW",
  "status": "COMPLETED",
  "result_recorded": true,
  "synthetic_result": false,
  "interrupted": false
}
```

## Status Values
- PENDING
- RUNNING
- COMPLETED
- FAILED
- INTERRUPTED
- SYNTHETIC_CLOSED

## Hard Rules
- Every tool call must have a result record.
- If interrupted, the ledger must include `synthetic_result=true`.
- If failed, the ledger must include `failure_reason`.
- If `result_recorded=false`, the task cannot be marked DONE.
- If any PENDING/RUNNING record remains, the ledger is unbalanced.
- Without a balanced tool ledger, completion is forbidden.

## Synthetic Result Semantics
Synthetic results are not success claims. They are closure records used to prevent dangling tool calls when interruption occurs.

A synthetic result should record:
- interruption reason
- last known status
- whether retry is safe
- required recovery entry

## State Integration
`active_task_state.json.tool_ledger_status` must be:
- `BALANCED` only when every call is closed
- `UNBALANCED` when there are pending, running, or missing results
- `FAILED` when failures exist without recovery
