import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_status_consistency_no_false_ready():
    report = load('phase_status/status_consistency_report.json')
    assert report['status_consistency'] == 'PASSED'
    assert 'READY_WITH_GAPS_AS_READY' in report['blocked_false_claims']
    decision = load('decision/acceptance_decision.json')
    assert decision['final_status'] != 'PIPELINE_ACCEPTED'
    assert decision['ready_for_production'] is False
