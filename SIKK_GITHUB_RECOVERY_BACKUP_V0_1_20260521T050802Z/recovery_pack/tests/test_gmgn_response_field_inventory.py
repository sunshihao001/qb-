import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_inventory():
 p=ROOT/'data/gmgn_read_only/latest/gap_repair/gmgn_response_field_inventory.json'; assert p.exists()
 d=json.load(open(p)); assert d['target_token']; assert d['response_files_checked']
 for k in ['symbol','name','price_usd','market_cap_usd','liquidity_usd','volume_5m','volume_1h','price_change_5m','price_change_1h','top_holder_count','top_holder_concentration_pct','lp_holder_pct']:
  assert k in d['field_alias_candidates']; assert k in d['mapping_confidence']
