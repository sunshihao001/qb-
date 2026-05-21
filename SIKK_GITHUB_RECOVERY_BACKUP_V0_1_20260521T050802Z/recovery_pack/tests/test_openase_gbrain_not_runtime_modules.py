import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_openase_gbrain_not_runtime_modules():
    a=json.load(open(ROOT/'data/coordination/latest/skill_call_justification_audit.json'))
    for j in a['justifications']:
        if j['provider'] in ['openase','gbrain','gbrain_file_bridge']:
            assert j['runtime_decision_permission'] is False
            assert j['paper_only_boundary_check']=='PASS'
            forbidden=' '.join(j['forbidden_actions']).lower()
            assert 'runtime' in forbidden or 'strategy' in forbidden or '裁决' in forbidden
