import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_mapping_patch():
 r=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/gmgn_feature_mapping_patch_report.json'))
 assert r['manual_mapping_used'] is False; assert r['fabricated_fields'] is False
 assert 'still_missing_features' in r and isinstance(r['still_missing_features'], list)
