---
artifact_type: memory_policy
status: verified
version: v1.1
valid_until: null
---
# Memory Governance Policy V1.1

## Purpose
Prevent Hermes memory pollution by separating candidates, verified memory, stale memory, superseded memory, and rejected memory.

## Memory lifecycle
1. candidate
2. verified
3. stale
4. superseded
5. rejected
6. archived

## Write rule
No memory is written directly as verified unless it has:
- stable scope
- source evidence
- last_verified_at
- validity classification
- no secret/token/private key material
- no temporary task progress

## Queue-first rule
All proposed memories enter `memory_write_queue.jsonl` first.

## Verification rule
Only after audit can queue items be copied into `verified_memory.jsonl`.

## Stale rule
Memory must be rechecked when:
- project canonical directory changes
- tool behavior changes
- user preference changes
- policy is superseded
- source evidence no longer exists

## Supersession rule
Superseded memory must reference `superseded_by`.
