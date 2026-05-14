import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_no_pipeline_accepted_with_open_gaps():
    decision = load('decision/acceptance_decision.json')
    assert decision['non_blocking_gaps']
    assert decision['final_status'] == 'A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS'
    assert decision['final_status'] != 'PIPELINE_ACCEPTED'
