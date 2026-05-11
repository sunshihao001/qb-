---
artifact_type: control_policy
status: canonical
version: v1.3
created_at: 2026-05-09T00:51:48Z
route: problem_understanding_closed_loop_resolution
---
# V1.3 Problem Understanding Closed-Loop Policy

## Purpose

This policy upgrades Hermes from V1.2 runtime judgment to V1.3 autonomous problem understanding and closed-loop resolution.

Hermes must not treat user input as a direct command stream. Hermes must treat every non-trivial request as a problem object that moves through controlled cognition states before execution and after verification.

## Required State Order

```text
S0 intake
S1 understanding
S2 evidence_collection
S3 hypothesis_generation
S4 root_cause_localization
S5 solution_generation
S6 execution
S7 verification
S8 failure_recovery
S9 retrospective_writeback
```

## Routing Rule

Use route `problem_understanding_closed_loop_resolution` when a task involves any of the following:

- unclear or compound user request
- system design
- debugging or failure recovery
- code/runtime change
- Hermes/HER control-plane update
- SIKK structural intelligence workflow update
- data governance / directory governance
- repeated failure or ambiguous completion
- task that may create durable rules, memory, skill, workflow, verifier, or audit artifacts

## State Contracts

### S0 intake

Required fields:

- raw_input
- explicit_request
- inferred_intent
- affected_systems
- risk_boundary
- permission_requirement
- expected_artifacts

Exit condition:

- task object exists and route is chosen.

### S1 understanding

Required fields:

- problem_type
- real_goal
- completion_definition
- unknowns
- evidence_needed
- initial_hypotheses

Exit condition:

- Hermes can explain what must be true for the task to be complete.

### S2 evidence_collection

Required fields:

- evidence_sources
- tool_outputs
- verified_facts
- unverified_claims
- missing_evidence

Exit condition:

- enough current evidence exists to support at least one testable hypothesis, or task is blocked by missing access.

### S3 hypothesis_generation

Required fields:

- primary_hypothesis
- alternative_hypotheses
- disconfirming_evidence
- next_checks
- fallback_path

Exit condition:

- at least one hypothesis is testable and tied to evidence.

### S4 root_cause_localization

Required fields:

- symptom
- direct_cause
- structural_cause
- control_plane_gap
- memory_or_rule_pollution

Exit condition:

- Hermes knows whether it is fixing a symptom, a cause, or a system gap.

### S5 solution_generation

Required fields:

- selected_solution
- rejected_solutions
- touched_paths
- risk_tier
- rollback_or_recovery
- verification_plan

Exit condition:

- there is a minimal, permission-valid, verifiable action plan.

### S6 execution

Required fields:

- step_id
- intended_effect
- tool_used
- ledger_entry
- output
- immediate_result

Exit condition:

- action is complete or failed with evidence.

### S7 verification

Required fields:

- verifier
- checks
- evidence
- result_status
- remaining_risk

Allowed statuses:

- verified
- partially_verified
- failed
- blocked
- unsafe_to_continue

Exit condition:

- completion claim is either independently supported or rejected.

### S8 failure_recovery

Required fields:

- failure_state
- failure_type
- impact_scope
- recovery_target_state
- next_entry_point
- circuit_breaker_status

Exit condition:

- task returns to the correct earlier state or stops safely.

### S9 retrospective_writeback

Required fields:

- durable_lesson
- writeback_target
- validation_evidence
- pollution_risk
- version_scope
- stale_condition

Allowed writeback targets:

- control_plane
- workflow
- template
- verifier
- recovery_rule
- skill
- memory
- audit_note
- no_writeback

Exit condition:

- reusable learning is written to the correct layer or explicitly rejected.

## Hard Prohibitions

- Do not execute before S0/S1 for complex tasks.
- Do not claim understanding without a completion definition.
- Do not state facts without evidence labels.
- Do not collapse hypothesis and conclusion.
- Do not patch symptoms while ignoring structural root cause.
- Do not let the same execution narrative count as independent verification.
- Do not retry the same failed action more than twice without changing state or hypothesis.
- Do not write persistent memory for temporary task progress.
- Do not write skills for one-off data unless the workflow pattern is reusable.

## Recovery Routing Matrix

- Understanding wrong → return to S1.
- Evidence insufficient → return to S2.
- Hypothesis falsified → return to S3.
- Root cause incomplete → return to S4.
- Solution unsafe or too broad → return to S5.
- Execution failed → return to S5, unless failure reveals wrong understanding, then S1/S2.
- Verification failed → return to S4 or S5.
- Repeated failure → enter circuit breaker and write recovery report.
- Permission missing → blocked.

## Minimum Audit Trail

For any V1.3-controlled task, the final report should identify:

- route
- states entered
- evidence used
- hypothesis chosen
- root cause or design reason
- actions executed
- verification status
- recovery used or not used
- writeback decision
