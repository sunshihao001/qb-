---
artifact_type: runtime_policy
status: verified
version: v1.2
valid_until: null
---
# Compact Rebuild Policy

## Purpose
Compact is not a summary. It is a controlled restart of a runnable context.

After compaction, Hermes must be able to continue work with preserved plan, files, skills, tools, and work semantics.

## Required Snapshot Directory
`03_task_runtime/compact_snapshots/`

## Required Snapshot Artifacts
Each compact event must generate:
- `compact_boundary.json`
- `compact_summary.md`
- `post_compact_context.md`

## Required Post-Compact Context Fields
`post_compact_context.md` must include:
- current task ID
- current phase
- completed phases
- key files
- current errors
- pending verification items
- next action
- forbidden actions
- recovery entry

## Hard Rules
- Summary is not the goal.
- Continuing execution is the goal.
- Compact must preserve work semantics, not only text.
- If post-compact context cannot resume execution, compact failed.
- Compaction must record the boundary that triggered it.
- Compaction must preserve the current state and errors first.

## Required Boundary Record
`compact_boundary.json` should record:
- task_id
- phase_id
- turn_count
- budget state
- reason for compact
- preserved surfaces
- truncated surfaces
- resume readiness

## Required Summary Record
`compact_summary.md` should be a continuation aid, not a generic summary. It should point to the next action and recovery entry.
