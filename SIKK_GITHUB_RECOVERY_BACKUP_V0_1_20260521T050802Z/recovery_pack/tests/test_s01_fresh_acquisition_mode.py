from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_fresh_acquisition_mode():
    rm=json.loads((ROOT/'data/runs'/run_id()/'run_manifest.json').read_text())
    assert rm['acquisition_mode']=='FRESH_GMGN_SKILL_CALL'
    assert rm['stage']=='S01_R02_R03_FRESH_GMGN_ACQUISITION_ALIGNMENT'
