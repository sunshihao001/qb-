import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_acceptance_report():
 a=json.load(open(ROOT/'data/gmgn_read_only/latest/acceptance_report.json'))
 assert a['acceptance_status'] in ['PASS','PASS_WITH_GAPS']
 assert a['gmgn_real_read_only_call_status']=='REAL_CALLED'
 assert a['paper_only_boundary_status']=='PASS'; assert a['forbidden_scope_detected']==[]
 assert a['next_recommended_stage']
