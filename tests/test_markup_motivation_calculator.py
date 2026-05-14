
import pytest


@pytest.mark.parametrize(
    ('components', 'expected_score', 'expected_status'),
    [
        ({
            'remaining_inventory_score': 0.9,
            'unfinished_distribution_score': 0.9,
            'cost_position_score': 0.8,
            'pattern_control_score': 0.8,
            'liquidity_need_score': 0.7,
            'second_stage_condition_score': 0.7,
            'counterparty_pressure_penalty': 0.2,
            'same_source_exit_penalty': 0.1,
        }, 4.5, '继续推进动机强'),
        ({
            'remaining_inventory_score': 0.6,
            'unfinished_distribution_score': 0.6,
            'cost_position_score': 0.5,
            'pattern_control_score': 0.5,
            'liquidity_need_score': 0.4,
            'second_stage_condition_score': 0.4,
            'counterparty_pressure_penalty': 0.2,
            'same_source_exit_penalty': 0.1,
        }, 2.7, '继续推进动机中等'),
        ({
            'remaining_inventory_score': 0.35,
            'unfinished_distribution_score': 0.35,
            'cost_position_score': 0.3,
            'pattern_control_score': 0.25,
            'liquidity_need_score': 0.2,
            'second_stage_condition_score': 0.2,
            'counterparty_pressure_penalty': 0.1,
            'same_source_exit_penalty': 0.05,
        }, 1.5, '继续推进动机弱'),
        ({
            'remaining_inventory_score': 0.1,
            'unfinished_distribution_score': 0.1,
            'cost_position_score': 0.1,
            'pattern_control_score': 0.1,
            'liquidity_need_score': 0.0,
            'second_stage_condition_score': 0.0,
            'counterparty_pressure_penalty': 0.3,
            'same_source_exit_penalty': 0.4,
        }, 0.0, '更偏向派发退出'),
    ],
)
def test_markup_motivation_score_sums_positive_drivers_minus_penalties(components, expected_score, expected_status):
    from modules.wallet_structure.markup_motivation_calculator import calculate_markup_motivation

    result = calculate_markup_motivation(**components)

    assert result.markup_motivation_score == pytest.approx(expected_score)
    assert result.markup_motivation_status_zh == expected_status
    for key, value in components.items():
        assert getattr(result, key) == pytest.approx(value)
    assert '继续推进动机分' in result.markup_motivation_notes_zh


def test_markup_motivation_is_insufficient_when_too_few_evidence_components():
    from modules.wallet_structure.markup_motivation_calculator import calculate_markup_motivation

    result = calculate_markup_motivation(
        remaining_inventory_score=0.9,
        counterparty_pressure_penalty=0.1,
    )

    assert result.markup_motivation_score is None
    assert result.markup_motivation_status_zh == '动机证据不足'


def test_markup_motivation_can_derive_inventory_distribution_and_cost_scores_from_model_outputs():
    from modules.wallet_structure.markup_motivation_calculator import calculate_markup_motivation
    from modules.wallet_structure.quantitative_structure_models import (
        DominantCostZoneResult,
        DistributionProgressResult,
        StructureInventoryEstimateResult,
    )

    result = calculate_markup_motivation(
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.8),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.2),
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_deviation_rate=0.5),
        pattern_control_score=0.6,
        liquidity_need_score=0.5,
        second_stage_condition_score=0.4,
        counterparty_pressure_penalty=0.1,
        same_source_exit_penalty=0.1,
    )

    assert result.remaining_inventory_score == pytest.approx(0.8)
    assert result.unfinished_distribution_score == pytest.approx(0.8)
    assert result.cost_position_score == pytest.approx(0.8)
    assert result.markup_motivation_score == pytest.approx(3.7)
    assert result.markup_motivation_status_zh == '继续推进动机中等'
