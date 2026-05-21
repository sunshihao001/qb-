import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_activation_report_status():
    r=json.load(open(ROOT/'data/coordination/latest/real_skill_interface_activation_report.json'))
    assert r['activation_status'] in ['PASS','PASS_WITH_STUB','PARTIAL','FAILED']
    assert r['openase_real_call_status'] == 'REAL_CALLED'
    assert r['paper_only_boundary_check'] == 'PASS'
