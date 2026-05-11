---
artifact_type: control_policy
status: verified
version: v1.1
valid_until: null
---
# Recovery Decision Table

- file_missing → regenerate phase output
- file_empty → regenerate and inspect input
- invalid_json → repair JSON and reverify
- command_failed → log stderr and create retry plan
- permission_violation → BLOCKED and ask user
- task_drift → return to task passport
- context_missing → rebuild active_task_context
- verification_failed → write recovery and do not advance
- unfinished_old_task → resume old task first
