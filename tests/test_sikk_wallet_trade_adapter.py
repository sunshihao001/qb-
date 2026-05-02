import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_load_wallet_decision_missing_returns_unknown_and_stale(tmp_path):
    from sikk_wallet_trade_adapter import load_wallet_decision

    decision = load_wallet_decision("TokenMissing111", tmp_path / "wallet_structure")

    assert decision["wallet_structure_status"] == "WALLET_UNKNOWN"
    assert decision["decision_action"] == "NO_DECISION"
    assert decision["wallet_structure_factor"] == 1.0
    assert decision["is_stale"] is True
    assert decision["reason"] == "wallet_structure_decision_missing"


def test_load_wallet_decision_reads_existing_decision(tmp_path):
    from sikk_wallet_trade_adapter import load_wallet_decision

    token = "TokenExisting111"
    _write_json(
        tmp_path / "wallet_structure" / token / "wallet_structure_decision.json",
        {
            "token_address": token,
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_score": 72,
            "wallet_risk_score": 18,
            "counterparty_pressure_score": 22,
            "wallet_structure_factor": 1.15,
            "reason": "早期钱包仍部分持有",
            "is_stale": False,
        },
    )

    decision = load_wallet_decision(token, tmp_path / "wallet_structure")

    assert decision["token_address"] == token
    assert decision["wallet_structure_status"] == "WALLET_SUPPORT"
    assert decision["wallet_structure_score"] == 72
    assert decision["wallet_structure_factor"] == 1.15
    assert decision["is_stale"] is False


def test_apply_wallet_gate_off_keeps_state_and_marks_off():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate(
        {"state": "PAPER_READY", "当前状态": "PAPER_READY"},
        {"wallet_structure_status": "WALLET_BLOCK", "wallet_risk_score": 99, "reason": "高风险"},
        mode="off",
    )

    assert out["state"] == "PAPER_READY"
    assert out["wallet_gate_effect"] == "OFF"
    assert out["wallet_gate"] == "WALLET_BLOCK"


def test_apply_wallet_gate_observe_records_but_does_not_block():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    status = {"state": "PAPER_READY", "当前状态": "PAPER_READY"}
    decision = {
        "wallet_structure_status": "WALLET_BLOCK",
        "wallet_risk_score": 99,
        "counterparty_pressure_score": 99,
        "reason": "对手盘压力高",
    }

    out = apply_wallet_gate(status, decision, mode="observe")

    assert out["state"] == "PAPER_READY"
    assert out["wallet_gate"] == "WALLET_BLOCK"
    assert out["wallet_gate_effect"] == "OBSERVE_ONLY"
    assert out["would_block"] is True
    assert out["wallet_structure_reason"] == "对手盘压力高"


def test_apply_wallet_gate_soft_blocks_only_high_confidence_risk():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate(
        {"state": "PAPER_READY"},
        {
            "wallet_structure_status": "WALLET_BLOCK",
            "wallet_risk_score": 80,
            "counterparty_pressure_score": 20,
            "reason": "高风险",
        },
        mode="soft",
    )

    assert out["state"] == "BLOCKED"
    assert out["wallet_gate_effect"] == "SOFT_BLOCK"
    assert out["block_reason"] == "高风险"


def test_apply_wallet_gate_soft_low_confidence_records_only():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate(
        {"state": "PAPER_READY"},
        {
            "wallet_structure_status": "WALLET_BLOCK",
            "wallet_risk_score": 40,
            "counterparty_pressure_score": 30,
            "reason": "证据不足",
        },
        mode="soft",
    )

    assert out["state"] == "PAPER_READY"
    assert out["wallet_gate_effect"] == "SOFT_OBSERVE"
    assert out["would_block"] is True


def test_apply_wallet_gate_hard_pauses_missing_or_unknown():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate(
        {"state": "PAPER_READY"},
        {"wallet_structure_status": "WALLET_UNKNOWN", "reason": "missing"},
        mode="hard",
    )

    assert out["state"] == "PAUSE"
    assert out["wallet_gate_effect"] == "HARD_PAUSE_UNKNOWN"
    assert out["pause_reason"] == "missing"


def test_attach_wallet_factor_to_position_copies_decision_fields():
    from sikk_wallet_trade_adapter import attach_wallet_factor_to_position

    position = {"position_id": "p1", "代币地址": "Token111"}
    decision = {
        "wallet_structure_status": "WALLET_SUPPORT",
        "wallet_structure_score": 75,
        "wallet_risk_score": 15,
        "counterparty_pressure_score": 25,
        "wallet_structure_factor": 1.2,
        "reason": "结构侧仍持有",
        "dominant_side_status": "STRUCTURE_HOLDING",
        "chip_transfer_status": "NO_MAJOR_TRANSFER",
        "decision_age_sec": 120,
        "is_stale": False,
    }

    out = attach_wallet_factor_to_position(position, decision)

    assert out["wallet_structure_status"] == "WALLET_SUPPORT"
    assert out["wallet_structure_factor"] == 1.2
    assert out["dominant_side_status"] == "STRUCTURE_HOLDING"
    assert out["chip_transfer_status"] == "NO_MAJOR_TRANSFER"
    assert out["wallet_decision_age_sec"] == 120
    assert out["wallet_decision_stale"] is False


def test_evaluate_wallet_change_for_open_position_handles_dominant_and_chip_exit():
    from sikk_wallet_trade_adapter import evaluate_wallet_change_for_open_position

    dominant = evaluate_wallet_change_for_open_position(
        {"wallet_structure_score": 80, "wallet_risk_score": 20, "counterparty_pressure_score": 20},
        {"wallet_structure_status": "WALLET_SUPPORT", "dominant_side_status": "DISTRIBUTION_ACTIVE"},
    )
    chip = evaluate_wallet_change_for_open_position(
        {"wallet_structure_score": 80, "wallet_risk_score": 20, "counterparty_pressure_score": 20},
        {"wallet_structure_status": "WALLET_SUPPORT", "chip_transfer_status": "DISTRIBUTION_TO_COUNTERPARTY"},
    )

    assert dominant["action"] == "FORCE_PAPER_EXIT"
    assert dominant["failure_type"] == "DISTRIBUTION_ACTIVE"
    assert chip["action"] == "FORCE_PAPER_EXIT"
    assert chip["failure_type"] == "COUNTERPARTY_ABSORBING"


def test_evaluate_wallet_change_for_open_position_monitors_score_deterioration():
    from sikk_wallet_trade_adapter import evaluate_wallet_change_for_open_position

    action = evaluate_wallet_change_for_open_position(
        {"wallet_structure_score": 80, "wallet_risk_score": 20, "counterparty_pressure_score": 20},
        {"wallet_structure_status": "WALLET_SUPPORT", "wallet_structure_score": 55, "wallet_risk_score": 45, "counterparty_pressure_score": 50},
    )

    assert action["action"] == "EXIT_MONITOR"
    assert action["failure_type"] == "STRUCTURE_WEAKENING"
