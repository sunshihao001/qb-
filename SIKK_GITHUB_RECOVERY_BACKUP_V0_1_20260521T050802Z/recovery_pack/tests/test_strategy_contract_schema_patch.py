import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_strategy_patch():
 assert (ROOT/'contracts/strategy_contract_v0_1_schema.json').exists()
 assert (ROOT/'contracts/strategy_contract.json').exists()
 r=json.load(open(ROOT/'data/gmgn_read_only/latest/gap_repair/strategy_contract_schema_patch_report.json'))
 assert r['schema_created'] is True and r['canonical_contract_created'] is True
 assert r['strategy_logic_modified'] is False and r['thresholds_modified'] is False and r['version_changed'] is False
