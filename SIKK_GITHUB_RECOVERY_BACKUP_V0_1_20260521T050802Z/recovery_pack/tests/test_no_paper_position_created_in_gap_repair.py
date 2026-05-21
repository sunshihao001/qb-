import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_no_paper_position():
 t=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/decision_ticket_after_patch.json'))
 a=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/gap_repair_acceptance_report.json'))
 assert t['no_paper_position_created'] is True
 assert a['paper_position_created'] is False
