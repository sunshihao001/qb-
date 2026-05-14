import json
import subprocess
from pathlib import Path

ROOT = Path('/root/sikk-gmgn/system/her_document_function_system/controllers/H00_handoff_downstream_queue_controller')
SCRIPT = Path('/root/sikk-gmgn/scripts/her_document_function_system/validate_h00_controller_assets.py')

def test_h00_asset_validator_passes():
    result = subprocess.run(['python3', str(SCRIPT)], text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr + result.stdout
    payload = json.loads(result.stdout)
    assert payload['status'] == 'PASSED'
    assert payload['checked_files'] == 20

def test_h00_input_contract_blocks_unsafe_execution():
    contract = json.loads((ROOT/'04_h00_input_contract.json').read_text())
    boundary = contract['properties']['execution_boundary']['properties']
    assert boundary['allow_live_runtime']['const'] is False
    assert boundary['allow_wallet_signing']['const'] is False
    assert boundary['allow_auto_deploy']['const'] is False
    assert boundary['allow_production_trading']['const'] is False

def test_queue_item_schema_preserves_gap_and_forbidden_actions():
    schema = json.loads((ROOT/'12_queue_item.schema.json').read_text())
    required = set(schema['required'])
    assert {'forbidden_actions', 'gap_refs', 'accepted_risks', 'required_inputs', 'expected_outputs'} <= required
