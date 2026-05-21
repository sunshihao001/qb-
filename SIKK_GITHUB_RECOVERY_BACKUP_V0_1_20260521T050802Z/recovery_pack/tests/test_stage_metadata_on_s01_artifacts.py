from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()

def test_s01_artifacts_have_stage_metadata():
    rid=run_id()
    paths=[
        ROOT/'data/runs'/rid/'s01_data_source_r02_r03/raw_snapshot/raw_snapshot_manifest.json',
        ROOT/'data/runs'/rid/'s01_data_source_r02_r03/s01_to_s02_handoff.json',
        ROOT/'data/runs'/rid/'s01_data_source_r02_r03/data_availability_report.json',
        ROOT/'data/runs'/rid/'field_inventory/raw_field_inventory.json',
        ROOT/'data/runs'/rid/'field_inventory/source_response_schema.json',
    ]
    for p in paths:
        assert p.exists(), p
        d=json.loads(p.read_text())
        meta=d.get('stage_metadata')
        assert meta, p
        assert meta['s_stage']=='S01'
        assert meta['r_stage']==['R02','R03']
        assert meta['sr_physical_split_allowed'] is False
        assert meta['canonical_path'] == str(p.relative_to(ROOT))
