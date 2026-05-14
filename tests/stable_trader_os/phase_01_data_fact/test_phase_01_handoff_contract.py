from pathlib import Path
import json, csv, re
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "schemas/stable_trader_os/phase_01_data_fact"
CONFIG = ROOT / "configs/stable_trader_os/phase_01_data_fact"
CONTRACT = ROOT / "contracts/stable_trader_os/phase_01_data_fact"
EXAMPLES = ROOT / "examples/stable_trader_os/phase_01_data_fact"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def test_phase_01_to_phase_02_contract_targets_wallet_structure():
    data = load(CONTRACT / "phase_01_to_phase_02_contract.json")
    assert data["from_phase"] == "phase_01_data_fact_controller"
    assert data["to_phase"] == "phase_02_wallet_structure_controller"
    assert "01_data_fact/normalized/trade_fact_table.csv" in data["required_files"]
    assert "quality_score" in data["phase_02_must_carry_forward"]
    assert "PASS" in data["minimum_gate_status"]

def test_legacy_bridge_read_only():
    data = load(CONFIG / "legacy_bridge_registry.json")
    assert data["policy"] == "read_only_keep_in_place"
    assert data["do_not_move"] is True
    assert data["do_not_delete"] is True
