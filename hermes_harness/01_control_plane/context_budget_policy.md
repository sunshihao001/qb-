---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Context Budget Policy

## Purpose
Context is not a warehouse. It is a budgeted runtime surface.

Hermes must decide what enters context, what stays indexed, and what remains external.

## Budget Layers
- **Startup context**: short, stable, high-priority baseline.
- **Task passport**: medium, current task identity and boundaries.
- **Phase plan**: medium, current phase execution map.
- **Execution log**: do not inject fully; only index and retrieve by need.
- **Command log**: inject only recent errors or relevant closure records.
- **Memory**: inject only verified summaries.
- **Reports**: inject only the portion needed for the current phase.

## Hard Rules
- Long-term rules and temporary dialogue must not be mixed.
- `memory index` is an index, not a diary.
- Session memory should preserve only the skeleton needed to continue work.
- When over budget, preserve `Current State` and `Errors & Corrections` first.
- Do not auto-inject full chat history into the runtime context.

## Required Priority When Over Budget
1. Current State
2. Errors & Corrections
3. Key results
4. Current phase plan
5. Task passport
6. Verified memory summary
7. Recent command errors
8. Optional reports

## Required Records
Context budgeting decisions should record:
- task_id
- current budget estimate
- context surface requested
- context surface admitted
- context surface rejected
- reason for rejection
- compression or truncation action
- timestamp

## Disposition Values
- admit
- index_only
- summarize
- reject
- compress
