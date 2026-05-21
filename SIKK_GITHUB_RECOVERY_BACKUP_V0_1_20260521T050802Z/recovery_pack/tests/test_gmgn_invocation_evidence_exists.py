import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_evidence_files_exist():
 m=json.load(open(ROOT/'data/gmgn_read_only/latest/gmgn_read_only_skill_mapping.json'))
 assert (ROOT/'data/gmgn_read_only/latest/invocation_evidence/invocation_log.jsonl').exists()
 for x in m:
  assert (ROOT/x['request_path']).exists(); assert (ROOT/x['response_path']).exists(); assert (ROOT/x['error_path']).exists()
