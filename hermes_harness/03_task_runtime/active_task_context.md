---
artifact_type: active_task_context
status: verified
version: v1.1
valid_until: null
---
# Active Task Context

## task_id
hermes.task.20260506.140632.hermes_harness_v11

## task_mode
resume_capable

## task_type
system_design

## current_goal
Canonicalize the V1.1 runtime foundation so Hermes can resume long tasks safely.

## control_plane_refs
- `01_control_plane/hermes_constitution.md`
- `01_control_plane/task_routing_policy.md`
- `01_control_plane/input_contract_policy.md`
- `01_control_plane/artifact_contract_policy.md`
- `01_control_plane/risk_tier_policy.md`
- `01_control_plane/tool_permission_policy.md`
- `01_control_plane/verification_policy.md`
- `01_control_plane/recovery_policy.md`

## verified_memory_refs
- `04_memory/verified_memory.jsonl`
- `04_memory/system_memory.jsonl`

## input_contract
- only structured, verifiable inputs may enter runtime processing
- file paths are read-only unless permission says otherwise
- logs are parsed before transformation

## risk_boundary
- no destructive file moves or deletes
- no secrets/tokens/private keys
- no external push/deploy

## current_phase
phase_02_resume_foundation

## next_action
ensure checkpoint and command log are present for future resume flows
