from sikk_operator_psychology_engine import evaluate_operator_psychology, enrich_status_with_operator_psychology


def test_operator_psychology_maps_distribution_lifecycle_to_specific_cognition():
    status = {
        "token_address": "T1",
        "token_symbol": "AAA",
        "lifecycle": {
            "dominant_side_lifecycle": "ACTIVE_DISTRIBUTION",
            "dominant_side_intent": "ACTIVE_DISTRIBUTION",
            "counterparty_state": "EXIT_LIQUIDITY_FORMING",
            "trap_risk_type": "PUMP_TO_DISTRIBUTE",
        },
        "chip_control": {"chip_control_state": "CONTROL_LOST_TO_DISTRIBUTION_SIDE"},
        "market_cap_context": {"market_cap_change_from_discovery_pct": 520},
        "paper": {"paper_status": "OPEN"},
    }

    result = evaluate_operator_psychology(status)

    assert result["operator_lifecycle_stage"] == "ACTIVE_DISTRIBUTION"
    assert result["operator_psychology"] == "DISTRIBUTE_INTO_DEMAND"
    assert result["counterparty_psychology"] == "EXIT_LIQUIDITY_FORMING"
    assert result["paper_trade_alignment"] == "LATE_IN_DISTRIBUTION"
    assert result["psychology_evidence_level"] in {"E3", "E4"}
    assert "主导侧" in result["psychology_reason"]
    assert "确定庄家" not in result["psychology_reason"]
    assert "不执行真实 swap" in result["scope_note"]


def test_operator_psychology_maps_control_box_to_defense_and_watch():
    status = {
        "token_address": "T2",
        "token_symbol": "BBB",
        "dominant_side_lifecycle": "CONTROL_BOX_ACCUMULATION",
        "dominant_side_intent": "CONTROL",
        "counterparty_state": "NO_COUNTERPARTY_PRESSURE",
        "structure_defense_status": "DEFENDING_CONTROL_BOX",
        "chip_control_state": "CONTROL_RETAINED_BY_STRUCTURE_SIDE",
        "market_cap_change_from_discovery_pct": 42,
    }

    result = evaluate_operator_psychology(status)

    assert result["operator_lifecycle_stage"] == "CONTROL_BOX_ACCUMULATION"
    assert result["operator_psychology"] == "DEFEND_STRUCTURE_LEVEL"
    assert result["paper_trade_alignment"] == "ALIGNED_WITH_ACCUMULATION_OR_CONTROL"
    assert result["next_observation_focus"]
    assert result["invalidation_conditions"]


def test_enrich_status_with_operator_psychology_preserves_existing_status():
    status = {"token_address": "T3", "current_state": "PAPER_READY", "dominant_side_lifecycle": "SECOND_STAGE_EXPANSION", "dominant_side_intent": "MARKUP"}

    enriched = enrich_status_with_operator_psychology(status)

    assert enriched["current_state"] == "PAPER_READY"
    assert "operator_psychology" in enriched
    assert enriched["operator_psychology"]["operator_psychology"] == "CREATE_FOMO_LIQUIDITY"
    assert enriched["operator_lifecycle_stage"] == "SECOND_STAGE_EXPANSION"
    assert enriched["operator_psychology_label"] == "制造追涨流动性 / 推升扩张"
