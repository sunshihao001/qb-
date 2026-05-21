import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_strategy_contract_report():
 r=json.load(open(ROOT/'data/gmgn_read_only/latest/strategy_contract_read_report.json'))
 assert 'contract_found' in r; assert r['read_only_no_modification'] is True
 assert set(['EXCLUDE','WATCH','RISK_MONITOR','PAPER_READY_CANDIDATE','PATCH_REQUIRED']).issubset(set(r['allowed_decision_states']))
