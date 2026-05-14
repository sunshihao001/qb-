from pathlib import Path
import json, csv, re
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "schemas/stable_trader_os/phase_01_data_fact"
CONFIG = ROOT / "configs/stable_trader_os/phase_01_data_fact"
CONTRACT = ROOT / "contracts/stable_trader_os/phase_01_data_fact"
EXAMPLES = ROOT / "examples/stable_trader_os/phase_01_data_fact"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def test_missing_policy_levels_and_actions():
    data = load(CONFIG / "missing_field_policy.json")
    for key in ["fatal_required","phase_02_required","phase_03_required","phase_05_required","warning_allowed","optional"]:
        assert key in data and isinstance(data[key], list)
    assert data["policy"]["fatal_required_missing"] == "BLOCK"
    assert data["policy"]["warning_allowed_missing"] == "PASS_WITH_WARNING"
    assert "token_address" in data["fatal_required"]
    assert "transfer_fact_table" in data["phase_03_required"]
