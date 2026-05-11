---
artifact_type: session_reference
status: verified
version: v1.2
valid_until: null
---
# Hermes V1.2 Runtime Judgment Notes

## Session-proven cognitive invariant set

- Input governance comes before context assembly.
- Task routing comes before execution.
- Context budget must be checked before any large assembly step.
- Task state must be the source of truth for execution and recovery.
- Permission checks must happen before tool use.
- Tool calls must be logged in a ledger.
- Execution must keep an auditable narrative.
- Verification must be separated from execution.
- Recovery must trigger before repeated blind retries.
- Compact rebuild must restore working semantics before resuming.
- Memory must be revalidated before reuse.
- Retrospective review is part of the runtime loop.

## Meaning

This is the operational cognition model for Hermes V1.2: not command obedience, but runtime judgment.
