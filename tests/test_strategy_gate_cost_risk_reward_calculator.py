import pytest


def test_cost_risk_reward_ratio_uses_intel_bot_cost_inventory_and_pressure_inputs():
    from modules.strategy_gate.cost_risk_reward_calculator import calculate_cost_risk_reward_ratio
    from modules.wallet_structure.quantitative_structure_models import (
        CounterpartyPressureResult,
        DistributionProgressResult,
        DominantCostZoneResult,
        MarkupMotivationResult,
        StructureInventoryEstimateResult,
        WalletPatternCostAlignmentResult,
    )

    result = calculate_cost_risk_reward_ratio(
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, dominant_cost_low=0.8, dominant_cost_high=1.6, current_price=1.0),
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.8),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.15),
        markup_motivation=MarkupMotivationResult(markup_motivation_score=4.2),
        counterparty_pressure=CounterpartyPressureResult(counterparty_pressure_score=18),
        wallet_pattern_cost_alignment=WalletPatternCostAlignmentResult(pattern_type_zh='横盘控筹'),
    )

    assert result.current_price == pytest.approx(1.0)
    assert result.upper_target_space > 0
    assert result.lower_failure_space > 0
    assert result.cost_risk_reward_ratio is not None
    assert result.risk_reward_status_zh in {'风险收益比合适', '风险收益比一般', '风险收益比不足', '追高接盘风险高'}
    assert 'Strategy Gate Bot' in result.risk_reward_notes_zh


def test_cost_risk_reward_ratio_returns_insufficient_when_current_price_missing():
    from modules.strategy_gate.cost_risk_reward_calculator import calculate_cost_risk_reward_ratio

    result = calculate_cost_risk_reward_ratio()

    assert result.cost_risk_reward_ratio is None
    assert result.risk_reward_status_zh == '风险收益比证据不足'


def test_cost_risk_reward_ratio_flags_poor_rr_when_failure_space_is_large():
    from modules.strategy_gate.cost_risk_reward_calculator import calculate_cost_risk_reward_ratio
    from modules.wallet_structure.quantitative_structure_models import DominantCostZoneResult

    result = calculate_cost_risk_reward_ratio(
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=2.0, dominant_cost_low=1.5, dominant_cost_high=3.0, current_price=2.9),
        possible_distribution_target_price=3.0,
        key_failure_price=1.4,
    )

    assert result.cost_risk_reward_ratio is not None
    assert result.risk_reward_status_zh in {'风险收益比不足', '追高接盘风险高', '风险收益比一般', '风险收益比合适'}
