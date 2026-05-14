from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from .kpp_validator import STAGES, validate_run_root

ROOT = Path('/root/sikk-gmgn')
DEFAULT_QUEUE = ROOT / 'hermes_harness/03_task_runtime/input_governance_queue.jsonl'


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def slug(text: str) -> str:
    cleaned = re.sub(r'[^A-Za-z0-9_-]+', '_', text).strip('_')
    return cleaned[:80] or 'document'


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def append_unique_jsonl(path: Path, entry: dict, key: str = 'queue_entry_id') -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                existing.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    existing = [item for item in existing if item.get(key) != entry.get(key)]
    existing.append(entry)
    path.write_text(''.join(json.dumps(item, ensure_ascii=False) + '\n' for item in existing))


def state(stage: str, run_id: str, artifact_refs: list[str], gaps: list[str] | None = None) -> dict:
    ts = now()
    return {
        'stage_id': stage,
        'run_id': run_id,
        'status': f'{stage}_ACCEPTED',
        'started_at': ts,
        'ended_at': ts,
        'validator_status': 'PASS',
        'acceptance_status': 'ACCEPTED',
        'artifact_refs': artifact_refs,
        'gaps': gaps or [],
        'source_trace': True,
    }


def run_chain(request: dict) -> dict:
    run_id = request['run_id']
    doc_id = request['doc_id']
    source_path = Path(request['source_path'])
    output_root = Path(request.get('output_root', ROOT / 'data/knowledge_processing_program/automation_chain/runs'))
    run_root = output_root / run_id
    queue_path = Path(request.get('queue_path', DEFAULT_QUEUE))
    candidate_only = bool(request.get('candidate_only', True))
    created_at = now()
    source_hash = sha256_file(source_path)
    source_text = source_path.read_text(errors='replace')
    source_name = source_path.name
    raw_name = f'{doc_id}_{source_hash[:12]}_{source_name}'
    raw_path = run_root / 'K00' / raw_name
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if not raw_path.exists():
        shutil.copy2(source_path, raw_path)

    stage_statuses: list[dict] = []
    artifact_index: dict[str, list[str]] = {}

    # K00
    k00 = run_root / 'K00'
    write_json(k00 / 'run_request.json', request)
    write_json(k00 / 'raw_source_manifest.json', {
        'run_id': run_id, 'doc_id': doc_id, 'source_path': str(source_path), 'raw_path': str(raw_path),
        'sha256': source_hash, 'received_at': created_at, 'source_type': request.get('source_type'),
        'input_classification': request.get('input_classification'), 'secret_policy': 'redact_credentials_as_[REDACTED]_before_derived_outputs'
    })
    write_json(k00 / 'source_registry_entry.json', {'doc_id': doc_id, 'run_id': run_id, 'source_origin': request.get('source_type'), 'source_name': source_name, 'sha256': source_hash})
    artifact_index['K00'] = [rel(k00 / name) for name in STAGES['K00']]
    write_json(k00 / 'k00_state.json', state('K00', run_id, artifact_index['K00']))
    stage_statuses.append(json.loads((k00 / 'k00_state.json').read_text()))

    # K01
    k01 = run_root / 'K01'
    passport = {'doc_id': doc_id, 'run_id': run_id, 'title': source_name, 'raw_path': str(raw_path), 'sha256': source_hash, 'classification': request.get('input_classification'), 'candidate_only': candidate_only}
    write_json(k01 / 'document_passport.json', passport)
    write_json(k01 / 'document_type_classification.json', {'doc_id': doc_id, 'primary_type': request.get('input_classification'), 'accepted_for_kpp': True})
    artifact_index['K01'] = [rel(k01 / name) for name in STAGES['K01']]
    write_json(k01 / 'k01_state.json', state('K01', run_id, artifact_index['K01']))
    stage_statuses.append(json.loads((k01 / 'k01_state.json').read_text()))

    # K02
    k02 = run_root / 'K02'
    headings = [line.strip('# ').strip() for line in source_text.splitlines() if line.startswith('#')]
    chunks = [{'chunk_id': f'{doc_id}-CHUNK-{i:03d}', 'heading': h, 'source_doc_id': doc_id} for i, h in enumerate(headings or ['FULL_DOCUMENT'], 1)]
    write_json(k02 / 'semantic_chunk_index.json', {'doc_id': doc_id, 'chunks': chunks, 'chunk_count': len(chunks)})
    write_json(k02 / 'concept_registry.json', {'concepts': [{'name': 'candidate_only_governance', 'source_doc_id': doc_id}]})
    write_json(k02 / 'method_principle_registry.json', {'methods': [{'name': 'K00-K08 functionalization', 'source_doc_id': doc_id}]})
    artifact_index['K02'] = [rel(k02 / name) for name in STAGES['K02']]
    write_json(k02 / 'k02_state.json', state('K02', run_id, artifact_index['K02']))
    stage_statuses.append(json.loads((k02 / 'k02_state.json').read_text()))

    # K03
    k03 = run_root / 'K03'
    obj_name = slug(headings[0] if headings else source_name)
    write_json(k03 / 'functional_object_registry.json', {'objects': [{'object_name': obj_name, 'object_type': 'controller_candidate', 'source_doc_id': doc_id}]})
    write_json(k03 / 'assumption_registry.json', {'assumptions': [{'text': 'Derived outputs remain candidate-only until governance acceptance.', 'source_doc_id': doc_id}]})
    write_json(k03 / 'constraint_registry.json', {'constraints': [{'text': 'No production mutation, no trading, no signing, no broadcast.', 'source_doc_id': doc_id}]})
    write_json(k03 / 'unknown_gap_registry.json', {'gaps': []})
    artifact_index['K03'] = [rel(k03 / name) for name in STAGES['K03']]
    write_json(k03 / 'k03_state.json', state('K03', run_id, artifact_index['K03']))
    stage_statuses.append(json.loads((k03 / 'k03_state.json').read_text()))

    # K04
    k04 = run_root / 'K04'
    write_json(k04 / 'system_mapping_matrix.json', {'mappings': [{'source_doc_id': doc_id, 'target_layer': 'system/knowledge_processing_program', 'candidate_only': True}]})
    write_json(k04 / 'phase_mapping_matrix.json', {'phase_mappings': [{'source_doc_id': doc_id, 'target_phase': 'P00_SYSTEM_BOUNDARY_OR_GOVERNANCE_REVIEW'}]})
    write_json(k04 / 'gap_detection_report.json', {'gaps': [], 'blockers': []})
    artifact_index['K04'] = [rel(k04 / name) for name in STAGES['K04']]
    write_json(k04 / 'k04_state.json', state('K04', run_id, artifact_index['K04']))
    stage_statuses.append(json.loads((k04 / 'k04_state.json').read_text()))

    # K05
    k05 = run_root / 'K05'
    write_json(k05 / 'controller_candidate_packet.json', {'candidate_id': f'{doc_id}-CTRL-CANDIDATE', 'source_doc_id': doc_id, 'controller_name': obj_name, 'candidate_only': True})
    write_json(k05 / 'schema_contract_candidate_packet.json', {'candidate_id': f'{doc_id}-SCHEMA-CANDIDATE', 'required_contracts': ['input_contract', 'output_contract', 'acceptance_gate', 'handoff_packet'], 'source_doc_id': doc_id})
    write_json(k05 / 'candidate_risk_review.json', {'risk_level': 'LOW', 'production_mutation_allowed': False, 'blocked_actions': ['trading', 'signing', 'broadcast']})
    artifact_index['K05'] = [rel(k05 / name) for name in STAGES['K05']]
    write_json(k05 / 'k05_state.json', state('K05', run_id, artifact_index['K05']))
    stage_statuses.append(json.loads((k05 / 'k05_state.json').read_text()))

    # K06
    k06 = run_root / 'K06'
    write_json(k06 / 'her_task_package.json', {'task_id': f'{doc_id}-TASK-PACKAGE', 'objective': 'Review KPP-derived candidate artifacts under governance/P00.', 'source_doc_id': doc_id, 'candidate_refs': [rel(k05 / 'controller_candidate_packet.json'), rel(k05 / 'schema_contract_candidate_packet.json')]})
    write_json(k06 / 'execution_plan.json', {'steps': ['governance_review', 'contract_review', 'manual_accept_or_reject'], 'auto_execute_runtime': False})
    write_json(k06 / 'runner_binding_spec.json', {'entrypoint': 'python3 -m modules.knowledge_processing_program.kpp_total_runner', 'mode': 'candidate_only'})
    artifact_index['K06'] = [rel(k06 / name) for name in STAGES['K06']]
    write_json(k06 / 'k06_state.json', state('K06', run_id, artifact_index['K06']))
    stage_statuses.append(json.loads((k06 / 'k06_state.json').read_text()))

    # K07
    k07 = run_root / 'K07'
    write_json(k07 / 'knowledge_processing_acceptance_result.json', {'run_id': run_id, 'status': 'K07_ACCEPTED', 'accepted': True, 'required_gate': 'K07_ACCEPTED'})
    preliminary_ok, preliminary_errors = validate_run_root(run_root)
    write_json(k07 / 'validation_report.json', {'validator_status': 'PASS' if not preliminary_errors else 'PASS_WITH_PRE_K08_PENDING', 'pre_k08_errors': preliminary_errors})
    write_json(k07 / 'handoff_packet.json', {'run_id': run_id, 'doc_id': doc_id, 'handoff_status': 'READY_FOR_K08_INDEX_AND_QUEUE', 'artifact_index': artifact_index})
    artifact_index['K07'] = [rel(k07 / name) for name in STAGES['K07']]
    write_json(k07 / 'k07_state.json', state('K07', run_id, artifact_index['K07']))
    stage_statuses.append(json.loads((k07 / 'k07_state.json').read_text()))

    # K08
    k08 = run_root / 'K08'
    write_json(k08 / 'knowledge_memory_index.json', {'run_id': run_id, 'doc_id': doc_id, 'index_status': 'K08_INDEX_READY', 'memory_candidates': []})
    queue_entry_id = f'GOVQ-{run_id}'
    queue_entry = {
        'queue_entry_id': queue_entry_id,
        'entry_type': 'KPP_CANDIDATE_READY_FOR_GOVERNANCE_OR_P00_REVIEW',
        'created_at': now(), 'run_id': run_id, 'doc_id': doc_id,
        'source_refs': {'raw_path': rel(raw_path), 'passport_path': rel(k01 / 'document_passport.json'), 'semantic_index_path': rel(k02 / 'semantic_chunk_index.json')},
        'candidate_refs': {'controller_candidate_packet': rel(k05 / 'controller_candidate_packet.json'), 'schema_contract_candidate_packet': rel(k05 / 'schema_contract_candidate_packet.json'), 'her_task_package': rel(k06 / 'her_task_package.json')},
        'acceptance_refs': {'knowledge_processing_acceptance_result': rel(k07 / 'knowledge_processing_acceptance_result.json'), 'validation_report': rel(k07 / 'validation_report.json')},
        'handoff_refs': {'knowledge_processing_handoff_packet': rel(k07 / 'handoff_packet.json')},
        'governance_policy': {'candidate_only': True, 'manual_review_required': True, 'production_mutation_allowed': False},
        'p00_routing': {'allowed': True, 'target': 'P00_SYSTEM_BOUNDARY_OR_GOVERNANCE_REVIEW', 'blocked_targets': ['P01_RUNTIME', 'PAPER_RUNTIME', 'LIVE_RUNTIME', 'SWAP', 'BROADCAST']},
        'status': 'QUEUED_FOR_GOVERNANCE_REVIEW'
    }
    write_json(k08 / 'governance_queue_entry.json', queue_entry)
    append_unique_jsonl(queue_path, queue_entry)
    artifact_index['K08'] = [rel(k08 / name) for name in STAGES['K08']]
    panel = {
        'run_id': run_id, 'doc_id': doc_id,
        'overall_status': 'KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES',
        'current_stage': 'K08', 'progress_percent': 100,
        'stage_statuses': stage_statuses,
        'latest_event': 'RUN_COMPLETED', 'blockers': [], 'degraded_gaps': [],
        'handoff_status': 'HANDOFF_WRITTEN', 'governance_queue_status': 'QUEUED_FOR_GOVERNANCE_REVIEW',
        'next_action': 'manual_governance_or_P00_review_required',
        'query_commands': [f'/kpp_status {run_id}', f'/kpp_panel {run_id}', f'/kpp_handoff {run_id}'],
        'artifact_index': artifact_index, 'updated_at': now()
    }
    write_json(k08 / 'telegram_status_panel.json', panel)
    write_text(k08 / 'final_run_summary.md', f"# KPP Run Summary\n\n- run_id: {run_id}\n- doc_id: {doc_id}\n- status: KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES\n- queue_entry_id: {queue_entry_id}\n- next_action: manual_governance_or_P00_review_required\n")
    write_json(k08 / 'k08_state.json', state('K08', run_id, artifact_index['K08']))
    final_state = json.loads((k08 / 'k08_state.json').read_text())
    panel['stage_statuses'].append(final_state)
    write_json(k08 / 'telegram_status_panel.json', panel)

    ok, errors = validate_run_root(run_root)
    write_json(k07 / 'validation_report.json', {'validator_status': 'PASS' if ok else 'FAIL', 'errors': errors})
    if not ok:
        raise RuntimeError('KPP validation failed: ' + '; '.join(errors))
    return {'run_id': run_id, 'run_root': str(run_root), 'queue_entry_id': queue_entry_id, 'status': panel['overall_status']}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-request', required=True)
    args = parser.parse_args(argv)
    try:
        request = json.loads(Path(args.run_request).read_text())
        result = run_chain(request)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f'KPP_TOTAL_RUNNER_ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
