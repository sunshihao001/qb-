from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_s01_to_s02_handoff():
    h=json.loads((s01()/'s01_to_s02_handoff.json').read_text())
    assert h['acquisition_mode']=='FRESH_GMGN_SKILL_CALL'
    assert h['raw_snapshot_manifest'].endswith('raw_snapshot_manifest.json')
    assert isinstance(h['recommended_feature_scope'], list)
    # GMGN may return Cloudflare/HTML or fail in this environment; S01 handoff is still
    # valid if gaps are explicit and no cache was mislabeled as fresh.
    assert 'missing_data_types' in h
