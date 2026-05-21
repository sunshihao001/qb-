from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_no_cache_as_fresh():
    sel=json.loads((s01()/'target_token_selection.json').read_text())
    manifest=json.loads((s01()/'raw_snapshot/raw_snapshot_manifest.json').read_text())
    assert sel['acquisition_mode']=='FRESH_GMGN_SKILL_CALL'
    assert sel['legacy_path_used_as_fresh'] is False
    assert manifest['legacy_path_used_as_fresh'] is False
