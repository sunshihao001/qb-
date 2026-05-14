from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[3]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_goal_passport_aligns_phase01_to_total_goal_without_trading_judgement():
    data = load("contracts/stable_trader_os/phase_01_data_fact/phase_01_goal_passport.json")
    assert "连续剔除低质量" in data["stable_trader_os_total_goal"]
    assert "数据事实层" in data["phase_01_stage_goal"]
    assert data["phase_01_position_in_system"].count("不") >= 1
    drift = " ".join(data["forbidden_goal_drift"])
    assert "买点" in drift
    assert "phase_02_wallet_structure_controller" in str(data)

def test_goal_to_quality_gate_matrix_covers_core_questions():
    data = load("configs/stable_trader_os/phase_01_data_fact/phase_01_goal_to_quality_gate_matrix.json")
    goals = " ".join(item["stage_goal"] for item in data["matrix"])
    for keyword in ["是否能进入 Phase 02", "缺失字段", "旧数据", "交易判断"]:
        assert keyword in goals
