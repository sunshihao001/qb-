import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_security_review():
 r=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/security_read_only_source_review.json'))
 assert r['gmgn_security_read_previous_status']=='NOT_AVAILABLE'
 assert r['recommended_status'] in ['NOT_AVAILABLE','SAFE_READ_ONLY_AVAILABLE','PATCH_REQUIRED']
 assert 'route_quote' in r['must_not_call']; assert r['forbidden_scope_detected']==[]
