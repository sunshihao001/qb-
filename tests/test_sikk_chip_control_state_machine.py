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


def test_okx_cluster_support_strengthens_retained_control_without_trade_authorization():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token555",
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_score": 70,
            "wallet_risk_score": 10,
            "counterparty_pressure_score": 15,
            "data_quality_score": 90,
            "data_quality_status": "OK",
            "max_sync_sell_score": 8,
        },
        lifecycle_row={"dominant_side_lifecycle": "CONTROL_BOX_ACCUMULATION"},
        okx_cluster_decision={
            "okx_cluster_status": "CLUSTER_CONTROL_HOLDING",
            "okx_cluster_control_retention_score": 78,
            "okx_cluster_risk_score": 12,
            "okx_cluster_reason": "横盘控筹阶段前300/最大集群持仓相对稳定。",
        },
    )

    assert decision.chip_control_state == "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
    assert decision.chip_control_action == "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS"
    assert "OKX_CLUSTER_CLUSTER_CONTROL_HOLDING" in decision.reason_codes
    assert any("OKX 前300集群转为同步卖出" in item for item in decision.invalidators)
    assert "okx_cluster_decision.json" in decision.evidence_refs


def test_okx_cluster_distribution_overrides_support_to_control_lost():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token666",
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_score": 74,
            "wallet_risk_score": 10,
            "counterparty_pressure_score": 15,
            "data_quality_score": 90,
            "data_quality_status": "OK",
        },
        okx_cluster_decision={
            "okx_cluster_status": "CLUSTER_DISTRIBUTION_RISK",
            "okx_cluster_distribution_score": 84,
            "cluster_sync_sell_score": 80,
            "largest_cluster_holding_pct_delta": -12,
            "okx_cluster_reason": "前300关联集群出现同步卖出/持仓快速下降。",
        },
    )

    assert decision.chip_control_state == "CONTROL_LOST_TO_DISTRIBUTION"
    assert decision.chip_control_action == "BLOCK_OR_FORCE_PAPER_EXIT"
    assert "OKX_CLUSTER_DISTRIBUTION_RISK" in decision.reason_codes
    assert decision.risk_level == "HIGH"


def test_okx_cluster_counterparty_pressure_migrates_control():
    decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": "Token777",
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_score": 68,
            "wallet_risk_score": 15,
            "counterparty_pressure_score": 15,
            "data_quality_score": 90,
            "data_quality_status": "OK",
        },
        okx_cluster_decision={
            "okx_cluster_status": "CLUSTER_BAGHOLDER_PRESSURE",
            "okx_cluster_risk_score": 76,
            "okx_cluster_reason": "晚期集群买入且 ROI 偏弱，存在套牢/接盘压力。",
        },
    )

    assert decision.chip_control_state == "CONTROL_MIGRATING_TO_COUNTERPARTY"
    assert decision.chip_control_action == "PAUSE_OR_EXIT_MONITOR"
    assert "OKX_CLUSTER_COUNTERPARTY_OR_BAGHOLDER_PRESSURE" in decision.reason_codes
