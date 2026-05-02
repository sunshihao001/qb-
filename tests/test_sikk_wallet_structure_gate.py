import json
from pathlib import Path


BASE_TOKEN = "TokenWalletGate111111111111111111111111111"


def _decision(wallet_rows):
    from sikk_wallet_structure_gate import evaluate_wallet_structure_gate

    return evaluate_wallet_structure_gate(token=BASE_TOKEN, symbol="TWG", wallet_rows=wallet_rows)


def test_early_wallet_concentrated_clearout_blocks():
    decision = _decision([
        {"wallet_address": "W1", "role": "EARLY_EXIT", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.95, "evidence_level": "E4"},
        {"wallet_address": "W2", "role": "EARLY_EXIT", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.88, "evidence_level": "E3"},
        {"wallet_address": "W3", "role": "EARLY_BUYER", "game_side": "STRUCTURE_SIDE", "sell_ratio": 0.82, "evidence_level": "E3"},
        {"wallet_address": "W4", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.05, "sell_ratio": 0.76, "evidence_level": "E2"},
    ])

    assert decision.wallet_structure_status == "WALLET_BLOCK"
    assert decision.wallet_structure_factor == 0.0
    assert decision.wallet_risk_score >= 70
    assert decision.counterparty_pressure_score >= 40
    assert decision.chip_control_state == "CONTROL_LOST_TO_DISTRIBUTION"
    assert "早期钱包集中清仓" in "；".join(decision.reasons)


def test_same_source_group_synchronized_selling_blocks():
    decision = _decision([
        {"wallet_address": "G1A", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "G1", "sell_ratio": 0.9, "evidence_level": "E4"},
        {"wallet_address": "G1B", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "G1", "sell_ratio": 0.83, "evidence_level": "E4"},
        {"wallet_address": "G1C", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "G1", "sell_ratio": 0.81, "evidence_level": "E3"},
    ])

    assert decision.wallet_structure_status == "WALLET_BLOCK"
    assert decision.has_same_source_sync_sell is True
    assert decision.chip_control_state == "CONTROL_MIGRATING_TO_COUNTERPARTY"
    assert "同源组同步卖出" in "；".join(decision.reasons)


def test_high_counterparty_pressure_blocks_or_pauses():
    decision = _decision([
        {"wallet_address": "BAG1", "role": "BAGHOLDER_WHALE", "game_side": "COUNTERPARTY_SIDE", "holding_ratio": 0.18, "unrealized_profit_pct": -42, "evidence_level": "R2"},
        {"wallet_address": "BAG2", "role": "BAGHOLDER_WHALE", "game_side": "COUNTERPARTY_SIDE", "holding_ratio": 0.14, "unrealized_profit_pct": -28, "evidence_level": "R2"},
        {"wallet_address": "RET1", "role": "RETAIL_NOISE", "game_side": "COUNTERPARTY_SIDE", "holding_ratio": 0.05, "evidence_level": "E1"},
    ])

    assert decision.wallet_structure_status in {"WALLET_BLOCK", "WALLET_PAUSE"}
    assert decision.counterparty_pressure_score >= 50
    assert decision.chip_control_state in {"CONTROL_MIGRATING_TO_COUNTERPARTY", "CONTROL_UNCLEAR"}
    assert "对手盘压力" in "；".join(decision.reasons)


def test_insufficient_data_pauses():
    decision = _decision([
        {"wallet_address": "U1", "role": "EARLY_BUYER", "game_side": "UNKNOWN_SIDE", "evidence_level": "E0", "funding_status": "资金待查"},
    ])

    assert decision.wallet_structure_status == "WALLET_PAUSE"
    assert decision.data_quality_score < 50
    assert decision.wallet_structure_factor == 0.3
    assert "数据不足" in "；".join(decision.reasons)


def test_structure_side_still_holds_high_result_not_exited_low_risk_supports():
    decision = _decision([
        {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.16, "sell_ratio": 0.1, "realized_profit_usd": 8000, "evidence_level": "E4"},
        {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.10, "sell_ratio": 0.25, "evidence_level": "E3"},
        {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.08, "sell_ratio": 0.05, "evidence_level": "E3"},
    ])

    assert decision.wallet_structure_status == "WALLET_SUPPORT"
    assert decision.wallet_structure_score >= 60
    assert decision.wallet_risk_score < 30
    assert decision.counterparty_pressure_score < 35
    assert decision.chip_control_state == "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
    assert decision.wallet_structure_factor == 1.0


def test_no_obvious_structure_evidence_is_neutral():
    decision = _decision([
        {"wallet_address": "R1", "role": "RETAIL_NOISE", "game_side": "NOISE_SIDE", "holding_ratio": 0.01, "sell_ratio": 0.1, "evidence_level": "E1"},
        {"wallet_address": "R2", "role": "RETAIL_NOISE", "game_side": "NOISE_SIDE", "holding_ratio": 0.02, "sell_ratio": 0.0, "evidence_level": "E1"},
        {"wallet_address": "R3", "role": "RETAIL_NOISE", "game_side": "NOISE_SIDE", "holding_ratio": 0.01, "sell_ratio": 0.2, "evidence_level": "E1"},
    ])

    assert decision.wallet_structure_status == "WALLET_NEUTRAL"
    assert decision.wallet_structure_factor == 0.6
    assert decision.wallet_structure_score < 40
    assert decision.wallet_risk_score < 35
    assert decision.chip_control_state == "CONTROL_UNCLEAR"


def test_wallet_structure_gate_writes_v1_chinese_first_files(tmp_path):
    from sikk_wallet_structure_gate import evaluate_and_write_wallet_structure

    paths = evaluate_and_write_wallet_structure(
        token=BASE_TOKEN,
        symbol="TWG",
        wallet_rows=[
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.16, "sell_ratio": 0.1, "evidence_level": "E4"},
        ],
        output_dir=tmp_path,
    )

    decision = json.loads(Path(paths["wallet_structure_decision_json"]).read_text(encoding="utf-8"))
    classification = Path(paths["wallet_classification_csv"]).read_text(encoding="utf-8-sig")
    notes = Path(paths["gmgn_note_table_csv"]).read_text(encoding="utf-8-sig")

    assert decision["钱包结构结论"] in {"WALLET_SUPPORT", "WALLET_NEUTRAL", "WALLET_PAUSE", "WALLET_BLOCK"}
    assert decision["筹码控制权状态"] == "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
    assert "对手盘压力评分" in decision
    assert "钱包地址,钱包角色,game_side,证据等级" in classification
    assert "address,gmgn_note,reason,action" in notes
