---
artifact_type: tool_permission_policy
status: verified
version: v1.1
valid_until: null
---
# Tool Permission Policy V1.1

## Core rule
Tool use must be permission-gated by risk tier before execution.

## ALLOW actions
- Read files
- Search files
- Inspect directory structure
- Generate new reports
- Run local verification scripts that do not mutate production state

## ASK actions
- Modify existing code
- Modify Hermes config
- Restart gateway/service
- Install packages
- Run migrations
- Any action that can interrupt active services

## DENY actions by default
- Delete or move large directories
- Overwrite unknown data
- Read or print secrets/private keys/tokens
- git push / publish / deploy
- Execute trades or financial transfers
- Disable safety controls

## Gateway/service restart rule
Restart is ASK because it can interrupt active agents.

## Secret rule
Secrets are never copied into memory, skill files, reports, or chat summaries. If encountered, redact as `[REDACTED]`.
