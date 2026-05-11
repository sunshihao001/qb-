---
artifact_type: workflow
status: canonical
version: v1.3
route: problem_understanding_closed_loop_resolution
created_at: 2026-05-09T00:51:48Z
---
# problem_understanding_closed_loop_resolution.workflow

## Trigger

Use this workflow when Hermes/HER needs to solve, debug, design, recover, or professionalize a task rather than merely answer a simple question.

## Workflow States

### 1. Intake

Create a task passport with:

- raw input
- explicit request
- inferred intent
- affected systems
- expected artifacts
- risk boundary
- permission requirement
- verification method

### 2. Understand

Produce a problem model:

- task type
- real goal
- completion definition
- unknowns
- evidence needed
- initial hypotheses

### 3. Collect Evidence

Gather current evidence using tools where applicable:

- read files for file claims
- inspect logs for runtime claims
- run commands for system state
- search sessions for past-context claims
- revalidate memory before using it

Mark each item as:

- verified_fact
- user_claim
- assumption
- missing

### 4. Generate Hypotheses

Write:

- primary hypothesis
- alternatives
- what would disprove each
- which check will decide

### 5. Localize Root Cause

Classify issue layer:

- symptom
- direct cause
- structural cause
- control-plane gap
- stale memory / rule pollution

### 6. Generate Solution

Pick the smallest verifiable solution:

- files/modules touched
- risk tier
- permission needed
- expected effect
- rollback/recovery path
- verification plan

### 7. Execute

Execute one bounded step at a time.

Record:

- tool used
- reason for tool
- output handle
- immediate result
- deviation from plan

### 8. Verify

Use independent checks:

- existence checks
- anchor checks
- schema checks
- command/test checks
- route/index checks
- completion-definition checks

Set status:

- verified
- partially_verified
- failed
- blocked
- unsafe_to_continue

### 9. Recover if Failed

Route back based on failure:

- wrong understanding → Understand
- missing evidence → Collect Evidence
- falsified hypothesis → Generate Hypotheses
- weak root cause → Localize Root Cause
- bad solution → Generate Solution
- execution error → Generate Solution or Collect Evidence
- repeated failures → circuit breaker

### 10. Write Back

Decide writeback target:

- no_writeback for one-off output
- audit note for observed risk
- verifier for repeatable checks
- recovery rule for repeated failure pattern
- workflow for recurring process
- skill for reusable operational method
- memory only for stable, compact, validated facts

## Output Contract

Final response/report must include:

- what changed
- where it was written
- verification status
- recovery status
- writeback decision
- next recommended module if any
