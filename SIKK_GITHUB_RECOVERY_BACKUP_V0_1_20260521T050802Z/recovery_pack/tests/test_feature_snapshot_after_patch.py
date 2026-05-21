import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_feature_after_patch():
 f=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/feature_snapshot_after_patch.json'))
 assert f['lineage_after_patch']['gmgn_response_field_inventory']=='data/gmgn_read_only/latest/gap_repair/gmgn_response_field_inventory.json'
 assert f['lineage_after_patch']['fabricated_fields'] is False
 assert 'missing_fields' in f['data_quality']
