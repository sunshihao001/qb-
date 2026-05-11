---
artifact_type: directory_invocation_policy
status: verified
version: v1.1
valid_until: null
---
# Directory Invocation Policy

## Required fields for every canonical directory
- writer
- reader
- read timing
- write timing
- non-writable states
- artifact types accepted
- verification required

## Non-writable states
A canonical directory must not be written when:
- task_id is missing
- active_task_state is BLOCKED or RECOVERING without recovery report
- permission class is ASK and user has not authorized
- artifact contract is missing
- source input is unverified

## Rule
Directories are interfaces, not storage dumps.
