from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()

def test_no_sr_physical_split_directories_created():
    forbidden=[ROOT/'data/s_series', ROOT/'data/r_series', ROOT/'data/S01', ROOT/'data/R03']
    for p in forbidden:
        assert not p.exists(), p
    deprecated=(ROOT/'docs/HERMES_DEPRECATED_COGNITION_LIST.md').read_text()
    assert 'S/R 物理分裂旧认知' in deprecated
