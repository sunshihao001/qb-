---
artifact_type: startup_protocol
status: verified
version: v1.1
valid_until: null
---
# Hermes Boot Sequence V1.1

## Purpose
Hermes must not execute before it knows whether the current request is a new task, a resume task, a recovery task, or a blocked task.

## Required order
1. Run startup check.
2. Read boot sequence.
3. Read control-plane files.
4. Read verified memory only.
5. Check `03_task_runtime/active_task_state.json`.
6. Decide task mode:
   - new
   - resume
   - recovery
   - blocked
7. Generate or update startup check report.
8. Continue only if `allowed_to_execute=true`.

## Required questions before execution
- Is this a new task?
- Is there an unfinished task?
- Is the current state blocked?
- Is recovery required?
- Is execution allowed?
- Must an old task be verified first?

## Deny conditions
Hermes must not continue execution when:
- `blocked=true`
- `recovery_required=true` and no recovery report exists
- active task state is invalid JSON
- user requests a high-risk action without permission
- current task cannot be mapped to a task passport

## Output
Every serious task must leave or update:
- `03_task_runtime/active_task_state.json`
- `08_reports/verification_reports/*`
- `08_reports/recovery_reports/*` when failed
