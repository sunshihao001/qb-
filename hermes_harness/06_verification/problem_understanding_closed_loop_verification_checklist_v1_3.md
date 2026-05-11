---
artifact_type: verification_checklist
status: canonical
version: v1.3
route: problem_understanding_closed_loop_resolution
created_at: 2026-05-09T00:51:48Z
---
# V1.3 Closed-Loop Verification Checklist

Use this checklist before claiming a V1.3-controlled task is complete.

## A. Intake / Understanding

- [ ] Raw user request preserved or summarized without changing intent.
- [ ] Explicit request identified.
- [ ] Inferred intent identified.
- [ ] Affected systems identified.
- [ ] Completion definition written.
- [ ] Risk boundary and permission needs checked.

## B. Evidence

- [ ] File claims verified with file reads/search.
- [ ] Runtime/system claims verified with commands.
- [ ] Historical claims verified with session_search or recorded evidence.
- [ ] Memory claims revalidated before use.
- [ ] Assumptions labeled separately from facts.

## C. Hypothesis / Root Cause

- [ ] Primary hypothesis stated.
- [ ] Alternative hypothesis or rejection reason stated.
- [ ] Disconfirming evidence considered.
- [ ] Symptom/direct cause/structural cause separated.
- [ ] Control-plane gap identified when relevant.

## D. Solution / Execution

- [ ] Selected solution follows minimal-closed-loop principle.
- [ ] Touched paths are within canonical route/directory rules.
- [ ] Risk tier is acceptable.
- [ ] Tool actions have observable outputs.
- [ ] No irreversible action was taken without permission.

## E. Independent Verification

- [ ] Expected files exist.
- [ ] Required anchors are present.
- [ ] JSON/YAML/schema files parse where relevant.
- [ ] README/index points to new version if required.
- [ ] The completion definition is satisfied.
- [ ] Surface-completion risk checked.

## F. Recovery / Writeback

- [ ] Failures, if any, have a recovery route.
- [ ] Repeated failure did not continue blindly.
- [ ] Writeback target chosen or rejected explicitly.
- [ ] Memory write is avoided unless stable and validated.
- [ ] Skill write/update is considered for reusable workflow.

## Verification Result

Allowed final statuses:

- verified
- partially_verified
- failed
- blocked
- unsafe_to_continue
