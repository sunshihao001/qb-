import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_no_forbidden_actions():
 acc=json.load(open(ROOT/'data/gmgn_read_only/latest/acceptance_report.json'))
 assert acc['forbidden_scope_detected']==[]
 m=json.load(open(ROOT/'data/gmgn_read_only/latest/gmgn_read_only_skill_mapping.json'))
 for x in m:
  ep=str(x['actual_entrypoint']).lower(); assert 'swap_route' not in ep; assert 'quote' not in ep; assert x['interface_type']!='swap'
