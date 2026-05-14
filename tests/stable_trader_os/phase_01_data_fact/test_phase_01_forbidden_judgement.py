from pathlib import Path
import json, csv, re
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "schemas/stable_trader_os/phase_01_data_fact"
CONFIG = ROOT / "configs/stable_trader_os/phase_01_data_fact"
CONTRACT = ROOT / "contracts/stable_trader_os/phase_01_data_fact"
EXAMPLES = ROOT / "examples/stable_trader_os/phase_01_data_fact"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def test_forbidden_contract_exists():
    path = CONTRACT / "phase_01_forbidden_judgement_contract.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Phase 01 是数据事实层" in text

def test_examples_do_not_emit_forbidden_judgement():
    forbidden = ["确定庄家","可以买","强烈建议买入","吸筹完成","派发完成","主力控盘","二段扩张概率高"]
    for path in EXAMPLES.glob("expected_*"):
        text = path.read_text(encoding="utf-8")
        for word in forbidden:
            assert word not in text, f"{path}:{word}"

def test_output_contract_blocks_trade_execution_fields():
    data = load(CONTRACT / "phase_01_output_contract.json")
    assert "buy_signal" in data["forbidden_outputs"]
    assert "trade_allowed" in data["forbidden_outputs"]
