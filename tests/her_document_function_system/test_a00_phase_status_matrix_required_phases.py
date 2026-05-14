import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_phase_status_matrix_required_phases():
    matrix = load('phase_status/phase_status_matrix.json')
    phases = {p['phase_id'] for p in matrix['phases']}
    assert {'O00','K00','F00','V00','R00'} <= phases
    assert matrix['matrix_status'] == 'BUILT'
