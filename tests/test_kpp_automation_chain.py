import json
import subprocess
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')
FIXTURE = ROOT / 'tests/fixtures/kpp/sample_system_design_doc.md'
OUT = ROOT / 'data/knowledge_processing_program/automation_chain/test_e2e_run'
QUEUE = ROOT / 'hermes_harness/03_task_runtime/input_governance_queue.jsonl'


def run_kpp(tmp_path):
    run_request = tmp_path / 'run_request.json'
    run_request.write_text(json.dumps({
        'run_id': 'TEST-KPP-AUTOCHAIN-E2E',
        'doc_id': 'TEST-KPP-DOC-001',
        'source_type': 'manual_file_path',
        'source_path': str(FIXTURE),
        'input_classification': 'system_building_material',
        'output_root': str(OUT),
        'queue_path': str(QUEUE),
        'telegram_panel': True,
        'candidate_only': True,
    }, ensure_ascii=False, indent=2))
    return subprocess.run(
        ['python3', '-m', 'modules.knowledge_processing_program.kpp_total_runner', '--run-request', str(run_request)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_kpp_total_runner_processes_fixture_to_governance_queue_and_panel(tmp_path):
    proc = run_kpp(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    run_root = OUT / 'TEST-KPP-AUTOCHAIN-E2E'
    assert (run_root / 'K00/raw_source_manifest.json').exists()
    assert (run_root / 'K01/document_passport.json').exists()
    assert (run_root / 'K02/semantic_chunk_index.json').exists()
    assert (run_root / 'K05/controller_candidate_packet.json').exists()
    assert (run_root / 'K06/her_task_package.json').exists()
    assert (run_root / 'K07/handoff_packet.json').exists()
    assert (run_root / 'K08/telegram_status_panel.json').exists()
    assert (run_root / 'K08/final_run_summary.md').exists()

    panel = json.loads((run_root / 'K08/telegram_status_panel.json').read_text())
    assert panel['overall_status'] == 'KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES'
    assert panel['current_stage'] == 'K08'
    assert panel['governance_queue_status'] == 'QUEUED_FOR_GOVERNANCE_REVIEW'
    assert len(panel['stage_statuses']) == 9
    assert all(stage['acceptance_status'] == 'ACCEPTED' for stage in panel['stage_statuses'])

    queue_entry = json.loads((run_root / 'K08/governance_queue_entry.json').read_text())
    assert queue_entry['entry_type'] == 'KPP_CANDIDATE_READY_FOR_GOVERNANCE_OR_P00_REVIEW'
    assert queue_entry['governance_policy']['candidate_only'] is True
    assert queue_entry['governance_policy']['manual_review_required'] is True
    assert queue_entry['governance_policy']['production_mutation_allowed'] is False
    assert queue_entry['p00_routing']['target'] == 'P00_SYSTEM_BOUNDARY_OR_GOVERNANCE_REVIEW'

    queue_lines = [json.loads(line) for line in QUEUE.read_text().splitlines() if line.strip()]
    assert any(line.get('queue_entry_id') == queue_entry['queue_entry_id'] for line in queue_lines)


def test_kpp_validator_blocks_missing_required_stage_output(tmp_path):
    proc = run_kpp(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    run_root = OUT / 'TEST-KPP-AUTOCHAIN-E2E'
    (run_root / 'K05/controller_candidate_packet.json').unlink()

    validate = subprocess.run(
        ['python3', '-m', 'modules.knowledge_processing_program.kpp_validator', '--run-root', str(run_root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert validate.returncode != 0
    assert 'controller_candidate_packet.json' in (validate.stdout + validate.stderr)
