import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_decision_ticket_paper_only():
 t=json.load(open(ROOT/'data/gmgn_read_only/latest/decision_ticket/decision_ticket.json'))
 assert t['decision_state'] in ['EXCLUDE','WATCH','RISK_MONITOR','PAPER_READY_CANDIDATE','PATCH_REQUIRED']
 assert t['decision_state'] not in ['BUY','SELL','LIVE_READY','EXECUTE','SWAP_READY']
 assert t['paper_only_boundary_check']=='PASS'; assert t['no_paper_position_created'] is True
