from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_no_forbidden_gmgn_calls():
    plan=json.loads((s01()/'skill_call_plan.json').read_text())
    text=(s01()/'invocation_log.jsonl').read_text().lower()
    for bad in ['gmgn-swap','gmgn_cooking','private_key','signing','broadcast','route_quote','order_quote']:
        assert bad not in text
    for item in plan:
        b=item['forbidden_boundary_check']
        assert b['swap'] is False and b['private_key'] is False and b['signing'] is False and b['broadcast'] is False
