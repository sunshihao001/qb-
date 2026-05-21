import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_no_forbidden_security():
 r=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/security_read_only_source_review.json'))
 a=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/gap_repair_acceptance_report.json'))
 assert r['forbidden_scope_detected']==[]; assert a['forbidden_scope_detected']==[]
 for s in r.get('candidate_sources',[]):
  ep=str(s).lower(); assert 'quote' not in ep and 'route' not in ep and 'swap' not in ep
