import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_mapping_real_calls():
 m=json.load(open(ROOT/'data/gmgn_read_only/latest/gmgn_read_only_skill_mapping.json'))
 assert len([x for x in m if x['required_for_p0']])==5
 assert [x for x in m if x['status']=='REAL_CALLED']
 for x in m:
  assert x['status'] in ['REAL_CALLED','NOT_AVAILABLE','FAILED']
  assert 'swap' not in str(x['request_payload']).lower() or 'forbidden' in x['request_payload']
