import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_feature_snapshot_schema():
 f=json.load(open(ROOT/'data/gmgn_read_only/latest/feature_snapshot/feature_snapshot.json'))
 for k in ['token_identity','market_features','security_features','holder_features','kline_features','data_quality']:
  assert k in f
 assert 'missing_fields' in f['data_quality']; assert 'feature_quality_score' in f['data_quality']
