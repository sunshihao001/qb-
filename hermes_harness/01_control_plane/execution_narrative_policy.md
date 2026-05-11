---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Execution Narrative Policy

## Purpose

Hermes runtime must preserve a coherent execution narrative. The agent may not jump between phases, tools, files, and conclusions without leaving an auditable explanation trail.

This policy makes the execution story itself a runtime artifact, not a chat afterthought.

## Required Runtime Artifact

`03_task_runtime/execution_narrative.md`

## Narrative Requirements

Each meaningful execution phase must record:

- why the phase exists
- which rule it follows
- what input it used
- what output it produced
- whether it passed verification
- why it failed
- what state it reached after recovery

## Hard Rules

- No task may be marked `DONE` if its narrative is missing or contradictory.
- Narrative must distinguish plan, execution, verification, recovery, and final report.
- Narrative must not hide failed attempts behind a clean final summary.
- Context compaction must preserve the current narrative entrypoint.
- Recovery must append to the narrative instead of replacing prior failure evidence.

## Verification

Run:

```bash
python3 hermes_harness/09_scripts/hermes_narrative_check.py --base hermes_harness --dry-run
```

Pass condition:

- `narrative_status` is `OK`.
- No required narrative anchors are missing.
