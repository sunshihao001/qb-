from pathlib import Path
import json, csv, re
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "schemas/stable_trader_os/phase_01_data_fact"
CONFIG = ROOT / "configs/stable_trader_os/phase_01_data_fact"
CONTRACT = ROOT / "contracts/stable_trader_os/phase_01_data_fact"
EXAMPLES = ROOT / "examples/stable_trader_os/phase_01_data_fact"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def decide(score, fatal_missing_count):
    if fatal_missing_count > 0:
        return "BLOCK"
    if score >= 90:
        return "PASS"
    if score >= 75:
        return "PASS_WITH_WARNING"
    if score >= 40:
        return "PAUSE"
    return "BLOCK"

def test_quality_gate_rules_cover_all_statuses():
    data = load(CONFIG / "quality_gate_rules.json")
    statuses = {r["gate_status"] for r in data["gate_rules"]}
    assert statuses == {"PASS","PASS_WITH_WARNING","PAUSE","BLOCK"}
    assert decide(95,0) == "PASS"
    assert decide(80,0) == "PASS_WITH_WARNING"
    assert decide(60,0) == "PAUSE"
    assert decide(30,0) == "BLOCK"
    assert decide(99,1) == "BLOCK"

def test_expected_mock_quality_gate():
    data = load(EXAMPLES / "expected_phase_01_quality_gate.json")
    assert data["phase_01_gate_status"] == "PASS_WITH_WARNING"
    assert data["next_phase"] == "phase_02_wallet_structure_controller"
