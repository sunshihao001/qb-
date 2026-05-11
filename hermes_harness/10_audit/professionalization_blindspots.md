---
artifact_type: audit_policy
status: verified
version: v1.1
valid_until: null
---
# Professionalization Blindspots V1.1

## Purpose
Define the 10 most common ways Hermes appears professional while still lacking runtime control.

## Blindspot 1: directory without invocation rules
A directory is not a capability. Every canonical directory must answer:
- who writes?
- who reads?
- when is it read?
- when is it not writable?

## Blindspot 2: startup context without boot verification
Startup context is insufficient unless `hermes_boot_check.py` generates a report proving state was checked.

## Blindspot 3: task passport template without enforcement
Complex tasks without a task passport must not enter execution. This must be enforced by task routing.

## Blindspot 4: permission rules without command inspection
Every command log must record `risk_tier` and `permission`.

## Blindspot 5: file existence without content/flow verification
Professional verification must check:
- file exists
- content is valid
- flow references exist
- state updated
- report is replayable

## Blindspot 6: recovery template without recovery route
Recovery requires a decision table: failure type → recovery action.

## Blindspot 7: memory without staleness handling
Memory without stale/superseded handling becomes pollution.

## Blindspot 8: final report without process logs
Final reports are insufficient without execution_loop_log and command_log.

## Blindspot 9: execution without rationale
Each phase report must explain:
- why this step was done
- which rule justified it
- which input was used
- who/what consumes the output

## Blindspot 10: executor without verifier
Professional Hermes must internally separate roles:
- Executor: performs work
- Verifier: doubts and checks

## Completion rule
A task is not professionalized if any blindspot remains unaddressed.
