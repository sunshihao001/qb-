import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_no_useless_expansion_audit_pass():
    p=ROOT/'data/coordination/latest/no_useless_expansion_audit.json'
    assert p.exists()
    a=json.load(open(p))
    assert a['status']=='PASS'
    joined=' '.join(a['detected_controls']+a['findings'])
    assert 'skill-first corrected' in joined
