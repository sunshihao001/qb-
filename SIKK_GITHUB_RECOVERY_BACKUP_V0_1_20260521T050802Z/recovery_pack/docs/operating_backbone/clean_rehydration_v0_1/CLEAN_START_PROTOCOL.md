# SIKK Clean Rehydration Protocol v0.1

## Purpose
Prevent historical artifacts, legacy runs, old schemas, deprecated decision tickets, or quarantine/archive data from becoming current operating truth during a new Hermes/GPT/OpenASE session.

## Professional term
Operating State Rehydration and State Contamination Prevention.

## Core rule
File existence is not authority. Current authority comes only from `data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json` plus approved contracts and manifests referenced by that pointer.

## Clean start sequence
1. Load SIKK governance doctrine.
2. Read `data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json`.
3. Validate the pointer contract.
4. Validate referenced approved backbone, invocation contracts, skill registry, and storage policy paths exist.
5. Validate any latest approved run is explicitly referenced by pointer; never discover by mtime.
6. Apply `READ_ALLOWLIST_POLICY.json` before opening project data.
7. Run `CONTAMINATION_CHECKLIST.json`.
8. Produce Operational Brief and Intake Gate for the new task.
9. Create a new isolated run for any action.

## Forbidden defaults
- Do not glob `data/operating_backbone/runs/*` to infer latest or current truth.
- Do not read `quarantine/` or `archive/` as current truth.
- Do not use mtime, filename latest, or old stage labels as authority.
- Do not consume old raw/feature/structure/decision/paper artifacts unless the current pointer or explicit task packet authorizes them.
- Do not enter GMGN acquisition, feature, structure, decision, paper, or attribution without the relevant gate.

## Status model
- `APPROVED_CURRENT`: default current entrypoint.
- `APPROVED_HISTORICAL`: auditable but not current.
- `CANDIDATE`: may be reviewed, not consumed by runtime/downstream.
- `PATCH_REQUIRED`: incomplete but recoverable.
- `BLOCKED`: unsafe or boundary-violating.
- `DEPRECATED`: preserved historical artifact, not current.
- `QUARANTINED`: cannot be default-read.
- `UNKNOWN_LINEAGE`: cannot enter downstream.
