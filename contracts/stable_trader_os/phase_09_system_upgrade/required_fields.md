# Phase09 Required Fields

## Required Phase08 inputs

- `phase_08_handoff_packet.json`
- `review_learning_summary.json`
- `failure_attribution.jsonl`
- `rule_update_candidates.json` unless it explicitly declares `no_update_required=true`

## Required candidate fields

Each upgrade candidate must include:

- `candidate_id`
- `target_phase`
- `candidate_type`
- `evidence_cases`
- `evidence_refs`
- `reason`

Missing `target_phase` or `evidence_cases` is a Phase09 blocking condition.

## Required package fields

- `package_version`
- `package_status`
- `regression_status`
- `requires_manual_confirmation=true`
- `allow_apply_to_runtime=false`
- `approved_rule_updates`
- `rollback_plan`
- `source_phase08_handoff`
