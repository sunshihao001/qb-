---
artifact_type: runtime_state
status: verified
version: v1.2
valid_until: null
---
# Execution Narrative

## Purpose
Execution narrative is a separate runtime artifact that explains what the system attempted, why it failed or succeeded, which recovery route was used, and what state it is in now.

## Required Fields Per Phase
Each phase entry must include:
- why the phase exists
- which rule it follows
- what input it used
- what output it produced
- whether it passed verification
- why it failed, if it failed
- what state it reached after recovery

## Hard Rules
- If a file exists but there is no narrative, the task is not professionally complete.
- Narrative must explain intent, rule, input, output, verification, failure, and recovery.
- Narrative must stay synchronized with runtime state and reports.
- Narrative must make it clear whether the system should continue, stop, or switch tracks.

## Required Narrative Questions
For each phase answer:
1. Why does this phase exist?
2. Which rule or policy justifies it?
3. What input did it use?
4. What output did it produce?
5. Did it pass verification?
6. If it failed, why did it fail?
7. After recovery, what state is it in now?

## Outcome
This artifact protects execution narrative consistency: the system must always be able to explain what it tried, why it tried it, what happened, and what to do next.
