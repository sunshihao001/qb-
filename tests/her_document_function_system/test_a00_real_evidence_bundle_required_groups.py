import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_real_evidence_bundle_required_groups():
    bundle = load('evidence_bundle/real_evidence_bundle.json')
    groups = bundle['evidence_groups']
    for required in ['o00_pipeline','k00_intake','f00_function_realization','v00_real_validation','r00_real_binding','gap_register','trace_audit','governance_policy']:
        assert required in groups
    assert bundle['bundle_status'] == 'BUILT'
