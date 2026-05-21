from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID='bootstrap_directory_realign_v0_1'

def test_strategy_contract_registry_layout():
    assert (ROOT/'contracts/strategy_contracts').exists()
    registry=json.loads((ROOT/'data/registry/strategy_contract_registry.json').read_text())
    item=registry['strategy_contracts'][0]
    assert item['logic_modified'] is False
    if (ROOT/'contracts/strategy_contract.json').exists():
        assert (ROOT/item['canonical_path']).exists()
        assert item['legacy_sha256']==item['canonical_sha256']
