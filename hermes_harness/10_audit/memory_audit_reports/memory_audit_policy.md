---
artifact_type: memory_audit_policy
status: verified
version: v1.1
valid_until: null
---
# Memory Audit Policy

## Audit questions
- Is the memory durable?
- Is it verified?
- Is it free of secrets?
- Is it not temporary progress?
- Does it have source evidence?
- Does it have last_verified_at?
- Does it require stale check?
- Is it superseded by a newer rule?

## Deny conditions
Reject memory if:
- it contains credentials, tokens, private keys, wallet secrets
- it is only task progress
- it is a guess or unverified conclusion
- it duplicates or conflicts with verified memory
- it belongs in a skill/procedure instead of memory
