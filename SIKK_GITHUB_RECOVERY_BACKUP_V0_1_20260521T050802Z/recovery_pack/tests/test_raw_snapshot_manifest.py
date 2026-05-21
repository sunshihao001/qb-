import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_raw_manifest():
 p=ROOT/'data/gmgn_read_only/latest/raw_snapshot/raw_snapshot_manifest.json'; assert p.exists()
 d=json.load(open(p)); assert d['token_address']; assert len(d['items'])==5
 for i in d['items']:
  for k in ['source_skill','request_path','response_path','error_path','raw_hash','schema_version']:
   assert k in i
