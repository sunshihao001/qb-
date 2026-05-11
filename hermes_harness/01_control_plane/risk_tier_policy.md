---
artifact_type: control_policy
status: verified
version: v1.1
valid_until: null
---
# Risk Tier Policy

R0 read-only ALLOW; R1 new docs ALLOW; R2 code change ASK; R3 config change ASK; R4 delete/move/overwrite DENY; R5 external push/secrets/trading/production DENY.
