from sikk_chip_control_state_machine import evaluate_chip_control_state


def test_control_retained_by_structure_side_requires_other_gates():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token111",
            "symbol": "TST",
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_score": 72,
            "wallet_risk_score": 12,
            "counterparty_pressure_score": 18,
            "data_quality_score": 88,
            "data_quality_status": "OK",
            "max_sync_buy_score": 82,
            "max_sync_sell_score": 10,
        },
        lifecycle_row={"dominant_side_lifecycle": "CONTROL_BOX_ACCUMULATION"},
        market_context={"discovery_market_cap_usd": 80000, "current_market_cap_usd": 110000},
    )

    assert decision.chip_control_state == "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
    assert decision.chip_control_action == "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS"
    assert "STRUCTURE_SIDE_RETAINED" in decision.reason_codes
    assert any("quote/security 未通过" in item for item in decision.invalidators)


def test_same_source_sell_migrates_to_counterparty():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token222",
            "wallet_structure_status": "WALLET_PAUSE",
            "wallet_structure_score": 48,
            "wallet_risk_score": 42,
            "counterparty_pressure_score": 55,
            "data_quality_score": 82,
            "data_quality_status": "OK",
            "max_sync_sell_score": 72,
            "has_same_source_sync_sell": True,
        }
    )

    assert decision.chip_control_state == "CONTROL_MIGRATING_TO_COUNTERPARTY"
    assert decision.chip_control_action == "PAUSE_OR_EXIT_MONITOR"
    assert "SAME_SOURCE_SYNC_SELL" in decision.reason_codes


def test_active_distribution_loses_control():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token333",
            "wallet_structure_status": "WALLET_BLOCK",
            "wallet_structure_score": 25,
            "wallet_risk_score": 90,
            "counterparty_pressure_score": 78,
            "data_quality_score": 90,
            "data_quality_status": "OK",
            "has_distribution": True,
        },
        lifecycle_row={"dominant_side_lifecycle": "ACTIVE_DISTRIBUTION"},
    )

    assert decision.chip_control_state == "CONTROL_LOST_TO_DISTRIBUTION"
    assert decision.chip_control_action == "BLOCK_OR_FORCE_PAPER_EXIT"
    assert decision.risk_level == "HIGH"
    assert "LIFECYCLE_ACTIVE_DISTRIBUTION" in decision.reason_codes


def test_missing_wallet_decision_is_data_quality_fail():
    decision = evaluate_chip_control_state(wallet_decision=None)

    assert decision.chip_control_state == "DATA_QUALITY_FAIL"
    assert decision.chip_control_action == "OBSERVE_DATA_REPAIR"
    assert "wallet_decision" in decision.missing_fields


def test_open_paper_position_gets_exit_monitor_when_control_migrates():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token444",
            "wallet_structure_status": "WALLET_PAUSE",
            "wallet_structure_score": 44,
            "wallet_risk_score": 48,
            "counterparty_pressure_score": 68,
            "data_quality_score": 80,
            "data_quality_status": "OK",
        },
        paper_row={"paper_status": "OPEN"},
    )

    assert decision.chip_control_state == "CONTROL_MIGRATING_TO_COUNTERPARTY"
    assert "PAPER_OPEN_REQUIRES_EXIT_MONITOR" in decision.reason_codes
    assert any("EXIT_MONITOR" in item for item in decision.invalidators)
