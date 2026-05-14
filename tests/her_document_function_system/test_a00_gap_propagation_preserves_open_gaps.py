import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_gap_propagation_preserves_open_gaps():
    report = load('gap_review/gap_propagation_report.json')
    assert report['hidden_gaps'] == []
    assert report['open_gaps'] > 0
    gap_ids = {p['gap_id'] for p in report['propagation_paths']}
    assert 'policy_not_active' in gap_ids
    assert 'live_runtime_forbidden' in gap_ids
