import pytest


def test_counterparty_pressure_score_reflects_mixed_late_stage_pressure():
    from modules.wallet_structure.counterparty_pressure_calculator import calculate_counterparty_pressure

    result = calculate_counterparty_pressure(
        late_large_buyer_score=0.8,
        whale_bagholder_score=0.7,
        retailization_score=0.6,
        early_to_late_transfer_score=0.5,
        floating_loss_late_holder_score=0.4,
    )

    assert result.counterparty_pressure_score == pytest.approx(67.5)
    assert result.counterparty_pressure_status_zh == '对手盘压力高'
    assert result.late_large_buyer_score == pytest.approx(0.8)
    assert result.whale_bagholder_score == pytest.approx(0.7)
    assert result.retailization_score == pytest.approx(0.6)
    assert result.early_to_late_transfer_score == pytest.approx(0.5)
    assert result.floating_loss_late_holder_score == pytest.approx(0.4)
    assert '对手盘压力总分' in result.counterparty_pressure_notes_zh


def test_counterparty_pressure_score_is_low_when_no_pressure_signals():
    from modules.wallet_structure.counterparty_pressure_calculator import calculate_counterparty_pressure

    result = calculate_counterparty_pressure()

    assert result.counterparty_pressure_score == pytest.approx(0.0)
    assert result.counterparty_pressure_status_zh == '对手盘压力低'


def test_wallet_pattern_cost_alignment_identifies_control_box_accumulation():
    from modules.wallet_structure.wallet_pattern_cost_alignment_calculator import calculate_wallet_pattern_cost_alignment
    from modules.wallet_structure.quantitative_structure_models import DominantCostZoneResult, DistributionProgressResult, StructureInventoryEstimateResult

    result = calculate_wallet_pattern_cost_alignment(
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, current_price=1.03),
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.78),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.12),
    )

    assert result.pattern_type_zh == '横盘控筹'
    assert result.alignment_status_zh == '匹配度高'
    assert result.cost_pattern_match_score >= 70
    assert result.wallet_behavior_match_score >= 70
    assert '横盘控筹' in result.alignment_notes_zh


def test_wallet_pattern_cost_alignment_identifies_distribution_breakdown():
    from modules.wallet_structure.wallet_pattern_cost_alignment_calculator import calculate_wallet_pattern_cost_alignment
    from modules.wallet_structure.quantitative_structure_models import DominantCostZoneResult, DistributionProgressResult, StructureInventoryEstimateResult

    result = calculate_wallet_pattern_cost_alignment(
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, current_price=0.82),
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.18),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.76),
    )

    assert result.pattern_type_zh == '结构崩塌'
    assert result.alignment_status_zh == '匹配度低'
    assert result.cost_pattern_match_score <= 35
    assert result.wallet_behavior_match_score <= 35
