---
artifact_type: role_policy
status: verified
version: v1.1
valid_until: null
---
# Executor / Verifier Role Policy

## Executor
Performs the planned action within permission boundaries.

## Verifier
Assumes the executor may be wrong and checks independently:
- output exists
- content matches purpose
- state updated
- logs exist
- risk boundary respected
- recovery exists if failed

## Rule
The same response may implement both roles, but must separate execution evidence from verification conclusion.
