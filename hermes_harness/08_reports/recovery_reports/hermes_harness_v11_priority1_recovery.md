---
artifact_type: recovery_report
status: verified
version: v1.1
valid_until: null
---
# Hermes Harness V1.1 Priority 1 Recovery Report

## Status
No active recovery required.

## Recovery policy
If any of the six stability files fail verification:
- startup protocol missing → restore `00_startup/HERMES_BOOT_SEQUENCE.md`
- task passport missing → regenerate task passport from user goal
- permission policy missing → block high-risk tool use until restored
- active task state invalid → repair JSON or rebuild from latest checkpoint
- verification report missing → do not mark task DONE
- recovery report missing after failure → stay in RECOVERING/BLOCKED

## Current result
`recovery_required=false`.
