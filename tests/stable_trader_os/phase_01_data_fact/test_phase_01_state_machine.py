from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[3]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_state_machine_blocks_before_downstream_on_bad_data():
    data = load("configs/stable_trader_os/phase_01_data_fact/phase_01_state_machine.json")
    states = {s["state"]: s for s in data["states"]}
    assert data["initial_state"] == "P01_INIT"
    assert states["P01_BLOCKED"]["terminal"] is True
    assert states["P01_COMPLETE"]["allowed_next"] == ["phase_02_wallet_structure_controller"]
    rules = " ".join(data["hard_rules"])
    assert "fatal_required" in rules
    assert "forbidden judgement" in rules

def test_acceptance_matrix_requires_goal_passport_and_tests():
    data = load("contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json")
    items = {x["id"]: x for x in data["acceptance_items"]}
    assert items["A08"]["required"] is True
    assert items["A10"]["required"] is True
    assert data["completion_status_if_all_required_pass"] == "PHASE_01_SYSTEM_DATA_COMPLETE"
