import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_decision_after_patch():
 t=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/decision_ticket_after_patch.json'))
 assert t['decision_state'] in ['WATCH','RISK_MONITOR','PAPER_READY_CANDIDATE','PATCH_REQUIRED']
 assert t['input_feature_snapshot_after_patch']=='data/gmgn_read_only/latest/gap_repair/feature_snapshot_after_patch.json'
 assert t['paper_only_boundary_check']=='PASS'
