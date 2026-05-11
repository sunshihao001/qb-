---
artifact_type: memory_policy
status: verified
version: v1.2
valid_until: null
---
# Memory Revalidation Policy

## Purpose
Verification applies not only to code and files, but also to memories and recommendations.

Before using memory to recommend or execute an action, Hermes must verify current state.

## Required Script
`09_scripts/hermes_memory_revalidate.py`

## Required Log
`04_memory/memory_verification_log.jsonl`

## Hard Rules
- Any project-path memory must verify the path still exists before execution.
- Any rule memory must check whether it has been superseded.
- Any old task state must check whether it is stale before resume.
- Memory that fails revalidation must not be treated as current truth.
- Revalidation results must be logged.

## Solves
This prevents old directories, old tasks, and old system rules from mixing into current execution as if still valid.
