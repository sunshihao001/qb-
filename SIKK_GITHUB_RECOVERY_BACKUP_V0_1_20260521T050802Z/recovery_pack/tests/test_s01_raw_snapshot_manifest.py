from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_raw_snapshot_manifest():
    p=s01()/'raw_snapshot/raw_snapshot_manifest.json'
    d=json.loads(p.read_text())
    assert d['acquisition_mode']=='FRESH_GMGN_SKILL_CALL'
    assert d['valid_for_current_decision'] is True
    assert d['legacy_path_used_as_fresh'] is False
    assert d['request_files'] and d['response_files'] and d['error_files']
