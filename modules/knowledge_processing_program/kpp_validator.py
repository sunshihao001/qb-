from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STAGES = {
    'K00': ['run_request.json', 'raw_source_manifest.json', 'source_registry_entry.json', 'k00_state.json'],
    'K01': ['document_passport.json', 'document_type_classification.json', 'k01_state.json'],
    'K02': ['semantic_chunk_index.json', 'concept_registry.json', 'method_principle_registry.json', 'k02_state.json'],
    'K03': ['functional_object_registry.json', 'assumption_registry.json', 'constraint_registry.json', 'unknown_gap_registry.json', 'k03_state.json'],
    'K04': ['system_mapping_matrix.json', 'phase_mapping_matrix.json', 'gap_detection_report.json', 'k04_state.json'],
    'K05': ['controller_candidate_packet.json', 'schema_contract_candidate_packet.json', 'candidate_risk_review.json', 'k05_state.json'],
    'K06': ['her_task_package.json', 'execution_plan.json', 'runner_binding_spec.json', 'k06_state.json'],
    'K07': ['knowledge_processing_acceptance_result.json', 'validation_report.json', 'handoff_packet.json', 'k07_state.json'],
    'K08': ['knowledge_memory_index.json', 'governance_queue_entry.json', 'telegram_status_panel.json', 'final_run_summary.md', 'k08_state.json'],
}

REQUIRED_PANEL_FIELDS = [
    'run_id', 'doc_id', 'overall_status', 'current_stage', 'progress_percent',
    'stage_statuses', 'handoff_status', 'governance_queue_status', 'next_action',
    'artifact_index', 'updated_at'
]


def validate_run_root(run_root: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not run_root.exists():
        return False, [f'run_root_missing: {run_root}']
    for stage, files in STAGES.items():
        stage_dir = run_root / stage
        if not stage_dir.exists():
            errors.append(f'stage_dir_missing: {stage}')
            continue
        for name in files:
            if not (stage_dir / name).exists():
                errors.append(f'{stage}/{name}')
    panel_path = run_root / 'K08' / 'telegram_status_panel.json'
    if panel_path.exists():
        try:
            panel = json.loads(panel_path.read_text())
            for field in REQUIRED_PANEL_FIELDS:
                if field not in panel:
                    errors.append(f'telegram_status_panel_missing_field: {field}')
            if panel.get('current_stage') != 'K08':
                errors.append('telegram_status_panel_current_stage_not_K08')
            if len(panel.get('stage_statuses', [])) != 9:
                errors.append('telegram_status_panel_stage_status_count_not_9')
        except json.JSONDecodeError as exc:
            errors.append(f'telegram_status_panel_invalid_json: {exc}')
    queue_path = run_root / 'K08' / 'governance_queue_entry.json'
    if queue_path.exists():
        try:
            entry = json.loads(queue_path.read_text())
            policy = entry.get('governance_policy', {})
            if policy.get('candidate_only') is not True:
                errors.append('governance_policy_candidate_only_not_true')
            if policy.get('manual_review_required') is not True:
                errors.append('governance_policy_manual_review_required_not_true')
            if policy.get('production_mutation_allowed') is not False:
                errors.append('governance_policy_production_mutation_allowed_not_false')
        except json.JSONDecodeError as exc:
            errors.append(f'governance_queue_entry_invalid_json: {exc}')
    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-root', required=True)
    args = parser.parse_args(argv)
    ok, errors = validate_run_root(Path(args.run_root))
    report = {'run_root': args.run_root, 'validator_status': 'PASS' if ok else 'FAIL', 'errors': errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
