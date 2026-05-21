import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
E=ROOT/'data/coordination/latest/invocation_evidence'

def test_stub_not_real():
    disc=json.load(open(ROOT/'data/coordination/latest/skill_interface_discovery_report.json'))
    r=json.load(open(ROOT/'data/coordination/latest/real_skill_interface_activation_report.json'))
    if not disc['gbrain_interface_found']:
        assert r['gbrain_real_call_status'] != 'REAL_CALLED'
        assert json.load(open(E/'gbrain_preflight_response.json'))['mode'] == 'STUB_ONLY_INTERFACE_NOT_FOUND'
