import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_target_token_selection():
 p=ROOT/'data/gmgn_read_only/latest/target_token_selection.json'; assert p.exists()
 d=json.load(open(p)); assert d['selected_token']; assert d['patch_required_if_missing'] is False
