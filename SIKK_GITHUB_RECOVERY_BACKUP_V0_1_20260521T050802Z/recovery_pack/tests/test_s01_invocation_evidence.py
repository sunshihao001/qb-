from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_invocation_evidence():
    logs=[json.loads(x) for x in (s01()/'invocation_log.jsonl').read_text().splitlines() if x.strip()]
    assert len(logs)>=8
    for l in logs:
        assert (ROOT/l['request_path']).exists()
        assert (ROOT/l['response_path']).exists()
        assert (ROOT/l['error_path']).exists()
