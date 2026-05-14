import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_readiness_certificate_required_fields():
    cert = load('certificate/readiness_certificate.json')
    for key in ['certificate_id','acceptance_run_id','final_status','readiness_level','allowed_next_actions','forbidden_next_actions','issued_by']:
        assert key in cert
    assert cert['final_status'] == 'A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS'
    assert 'wallet_signing' in cert['forbidden_next_actions']
