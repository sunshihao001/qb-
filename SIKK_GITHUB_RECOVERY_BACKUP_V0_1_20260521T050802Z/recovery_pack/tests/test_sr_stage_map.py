from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()

def test_s_to_r_pipeline_map_exists_and_maps_s01():
    p=ROOT/'docs/stage_maps/s_to_r_pipeline_map.yaml'
    assert p.exists()
    txt=p.read_text()
    assert 'S01:' in txt
    assert 'R02' in txt and 'R03' in txt
    assert 'S/R 是两套运行视图，不是两套数据目录' in txt
