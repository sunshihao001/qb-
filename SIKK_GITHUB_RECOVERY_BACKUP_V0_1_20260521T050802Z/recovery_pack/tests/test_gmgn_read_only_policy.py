import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_gmgn_read_only_policy():
    txt=(ROOT/'docs/GMGN_SKILL_READ_ONLY_USAGE_POLICY.md').read_text(encoding='utf-8')
    assert '只允许 GMGN read-only' in txt
    assert 'gmgn-swap' in txt and 'gmgn-cooking' in txt
    a=json.load(open(ROOT/'data/coordination/latest/skill_call_justification_audit.json'))
    gmgn=[j for j in a['justifications'] if j['provider']=='gmgn']
    assert gmgn
    for j in gmgn:
        assert j['runtime_decision_permission'] is False
        assert 'gmgn-swap' in ' '.join(j['forbidden_actions'])
        assert 'gmgn-cooking' in ' '.join(j['forbidden_actions'])
