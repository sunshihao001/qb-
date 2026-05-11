---
artifact_type: recovery_rule
status: canonical
version: v1.3
route: problem_understanding_closed_loop_resolution
created_at: 2026-05-09T00:51:48Z
---
# V1.3 Closed-Loop Recovery Rule

## Purpose

V1.3 recovery prevents Hermes from blind retry. Every failure must route back to the layer where the error was introduced.

## Recovery Matrix

| Failure observed | Likely failed layer | Required return state |
|---|---|---|
| User goal misunderstood | Understanding | S1 Understanding |
| Current facts are missing | Evidence | S2 Evidence Collection |
| Main explanation disproved | Hypothesis | S3 Hypothesis Generation |
| Fix targets only symptom | Root cause | S4 Root Cause Localization |
| Plan is too broad or unsafe | Solution | S5 Solution Generation |
| Tool/write/command failed | Execution | S5 or S2 depending on cause |
| Output fails verification | Verification | S4 or S5 |
| Permission not available | Permission boundary | blocked |
| Same failure repeats twice | Recovery governance | circuit_breaker |

## Circuit Breaker

Trigger circuit breaker when:

- same command/tool/write path fails twice without new evidence;
- verification fails twice for the same completion definition;
- missing permission blocks safe progress;
- execution would require irreversible/destructive action;
- context is too polluted to continue safely.

Circuit breaker output must include:

- failure_state
- failure_type
- evidence
- impact_scope
- stopped_action
- safe_next_entry
- human decision needed or not

## Recovery Report Contract

Every recovery report must answer:

1. Where did the failure occur?
2. What type of failure is it?
3. What evidence proves the failure?
4. Which earlier cognitive state should be re-entered?
5. What must change before retry?
6. Is it safe to continue automatically?
