import json
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
SYSTEM_ROOT = REPO_ROOT / 'system/her_document_function_system'
DATA_ROOT = REPO_ROOT / 'data/her_document_function_system'
R00_ROOT = SYSTEM_ROOT / 'controllers/R00_runner_tool_binding_controller'
R00_RUN = DATA_ROOT / 'r00_runs/r00_controller_creation_20260513_1500'
CANONICAL_ROUTE = SYSTEM_ROOT / 'CANONICAL_ROUTE.json'
RUNTIME_INDEX = DATA_ROOT / 'runtime_index/her_dfafs_runtime_index.json'


def load_json(path: Path):
    return json.loads(path.read_text())


def test_r00_run_contains_contract_required_evidence_outputs():
    output_contract = load_json(R00_ROOT / '05_r00_output_contract.json')
    required_output_keys = output_contract['required']
    manifest = load_json(R00_RUN / 'run_manifest.json')

    assert manifest['phase_id'] == 'R00'
    assert manifest['run_id'] == R00_RUN.name
    assert manifest['run_root'] == str(R00_RUN)
    assert manifest['final_status'] in {'R00_ACCEPTED', 'R00_READY_WITH_GAPS'}
    assert manifest['source_v00_handoff_refs'], 'R00 must retain upstream V00 handoff refs, not operate as isolated controller creation'

    outputs = manifest['outputs']
    for key in required_output_keys:
        assert key in outputs, key
        path = Path(outputs[key])
        assert path.exists(), f'{key}: {path}'
        if path.suffix not in {'.log', '.jsonl'}:
            assert path.stat().st_size > 20, f'{key}: {path}'


def test_r00_acceptance_records_real_v00_handoff_and_runtime_refs():
    acceptance = load_json(R00_RUN / 'acceptance/r00_acceptance_result.json')

    assert acceptance['phase_id'] == 'R00'
    assert acceptance['acceptance_status'] == 'R00_ACCEPTED'
    assert acceptance['runner_bound'] is True
    assert acceptance['binding_tested_against_real_v00_handoff'] is True
    assert acceptance['blocking_gaps'] == []
    assert acceptance['v00_handoff_refs'], 'acceptance must preserve V00 handoff refs'
    assert acceptance['run_manifest_ref'] == str(R00_RUN / 'run_manifest.json')
    assert acceptance['runtime_index_ref'] == str(RUNTIME_INDEX)


def test_r00_handoff_to_a00_is_runtime_usable_not_controller_asset_only():
    handoff = load_json(R00_RUN / 'handoff/r00_to_a00_handoff_packet.json')

    assert handoff['from_phase'] == 'R00'
    assert handoff['to_phase'] == 'A00'
    assert handoff['handoff_status'] == 'HANDOFF_READY'
    assert handoff['v00_handoff_refs'], 'R00 handoff must carry upstream V00 handoff references'
    assert handoff['run_manifest_refs'] == [str(R00_RUN / 'run_manifest.json')]
    assert handoff['runtime_index_refs'] == [str(RUNTIME_INDEX)]
    assert handoff['acceptance_refs'] == [str(R00_RUN / 'acceptance/r00_acceptance_result.json')]
    assert handoff['unresolved_gaps'] == []
    assert 'live_runtime' in handoff['forbidden_next_actions']
    assert 'wallet_signing' in handoff['forbidden_next_actions']


def test_canonical_route_and_runtime_index_include_k00_f00_v00_r00_chain():
    route = load_json(CANONICAL_ROUTE)
    runtime_index = load_json(RUNTIME_INDEX)

    assert route['canonical_data_root'] == str(DATA_ROOT)
    assert route['canonical_k00_run_root'] == str(DATA_ROOT / 'k00_runs')
    assert route['canonical_f00_run_root'] == str(DATA_ROOT / 'f00_runs')
    assert route['canonical_v00_run_root'] == str(DATA_ROOT / 'v00_runs')
    assert route['canonical_r00_run_root'] == str(DATA_ROOT / 'r00_runs')
    assert route['canonical_runtime_index'] == str(RUNTIME_INDEX)

    assert runtime_index['system'] == 'HER-DFAFS'
    assert runtime_index['canonical_route_ref'] == str(CANONICAL_ROUTE)
    phases = runtime_index['phases']
    for phase in ['K00', 'F00', 'V00', 'R00']:
        assert phase in phases
        assert Path(phases[phase]['run_root']).exists()
        assert phases[phase]['status'] in {'K00_ACCEPTED', 'F00_ACCEPTED', 'V00_ACCEPTED', 'R00_ACCEPTED', 'READY_WITH_GAPS'}
        assert phases[phase]['primary_refs'], phase
    assert runtime_index['handoff_chain'][0]['from_phase'] == 'K00'
    assert runtime_index['handoff_chain'][-1]['to_phase'] == 'A00'
