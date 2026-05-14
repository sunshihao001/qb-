from __future__ import annotations

from typing import Optional

from .quantitative_structure_models import (
    DominantCostZoneResult,
    DistributionProgressResult,
    MarkupMotivationResult,
    StructureInventoryEstimateResult,
)


_POSITIVE_FIELDS = (
    'remaining_inventory_score',
    'unfinished_distribution_score',
    'cost_position_score',
    'pattern_control_score',
    'liquidity_need_score',
    'second_stage_condition_score',
)
_NEGATIVE_FIELDS = (
    'counterparty_pressure_penalty',
    'same_source_exit_penalty',
)


def _clamp_score(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return max(0.0, min(float(value), 1.0))


def _derive_remaining_inventory_score(
    explicit_score: Optional[float],
    inventory: Optional[StructureInventoryEstimateResult],
) -> Optional[float]:
    if explicit_score is not None:
        return _clamp_score(explicit_score)
    if inventory is None or inventory.structure_inventory_remaining_pct is None:
        return None
    return _clamp_score(inventory.structure_inventory_remaining_pct)


def _derive_unfinished_distribution_score(
    explicit_score: Optional[float],
    distribution: Optional[DistributionProgressResult],
) -> Optional[float]:
    if explicit_score is not None:
        return _clamp_score(explicit_score)
    if distribution is None or distribution.structure_sold_pct is None:
        return None
    return _clamp_score(1.0 - distribution.structure_sold_pct)


def _derive_cost_position_score(
    explicit_score: Optional[float],
    dominant_cost_zone: Optional[DominantCostZoneResult],
) -> Optional[float]:
    if explicit_score is not None:
        return _clamp_score(explicit_score)
    if dominant_cost_zone is None or dominant_cost_zone.dominant_cost_deviation_rate is None:
        return None

    deviation = dominant_cost_zone.dominant_cost_deviation_rate
    if deviation < -0.10:
        return 0.20
    if deviation <= 0.20:
        return 1.00
    if deviation <= 0.80:
        return 0.80
    if deviation <= 2.00:
        return 0.40
    return 0.10


def _status_for_score(score: Optional[float]) -> str:
    if score is None:
        return '动机证据不足'
    if score >= 4.0:
        return '继续推进动机强'
    if score >= 2.5:
        return '继续推进动机中等'
    if score >= 1.0:
        return '继续推进动机弱'
    return '更偏向派发退出'


def calculate_markup_motivation(
    *,
    remaining_inventory_score: Optional[float] = None,
    unfinished_distribution_score: Optional[float] = None,
    cost_position_score: Optional[float] = None,
    pattern_control_score: Optional[float] = None,
    liquidity_need_score: Optional[float] = None,
    second_stage_condition_score: Optional[float] = None,
    counterparty_pressure_penalty: Optional[float] = None,
    same_source_exit_penalty: Optional[float] = None,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None,
    distribution_progress: Optional[DistributionProgressResult] = None,
    dominant_cost_zone: Optional[DominantCostZoneResult] = None,
    minimum_evidence_components: int = 4,
) -> MarkupMotivationResult:
    """Calculate continuation / second-stage markup motivation from separable evidence.

    Formula:
    markup_motivation_score =
        remaining inventory + unfinished distribution + reasonable cost deviation
        + controllable pattern + liquidity-taking need + second-stage condition
        - counterparty pressure penalty - same-source synchronized exit penalty
    """
    components = {
        'remaining_inventory_score': _derive_remaining_inventory_score(remaining_inventory_score, structure_inventory_estimate),
        'unfinished_distribution_score': _derive_unfinished_distribution_score(unfinished_distribution_score, distribution_progress),
        'cost_position_score': _derive_cost_position_score(cost_position_score, dominant_cost_zone),
        'pattern_control_score': _clamp_score(pattern_control_score),
        'liquidity_need_score': _clamp_score(liquidity_need_score),
        'second_stage_condition_score': _clamp_score(second_stage_condition_score),
        'counterparty_pressure_penalty': _clamp_score(counterparty_pressure_penalty),
        'same_source_exit_penalty': _clamp_score(same_source_exit_penalty),
    }

    positive_evidence_count = sum(1 for field in _POSITIVE_FIELDS if components[field] is not None)
    if positive_evidence_count < minimum_evidence_components:
        return MarkupMotivationResult(
            **components,
            markup_motivation_score=None,
            markup_motivation_status_zh='动机证据不足',
            markup_motivation_notes_zh='缺少库存、派发、成本、盘型、流动性或二段条件中的足够证据，暂无法判断继续推进动机。',
        )

    positive_total = sum(components[field] or 0.0 for field in _POSITIVE_FIELDS)
    negative_total = sum(components[field] or 0.0 for field in _NEGATIVE_FIELDS)
    score = round(max(0.0, positive_total - negative_total), 4)

    return MarkupMotivationResult(
        **components,
        markup_motivation_score=score,
        markup_motivation_status_zh=_status_for_score(score),
        markup_motivation_notes_zh=(
            '继续推进动机分 = 结构侧未派发库存分 + 派发未完成分 + 成本偏离合理分 + '
            '盘型可控分 + 流动性不足需制造承接分 + 二段扩张条件分 - 对手盘压力扣分 - 同源组同步退出扣分。'
        ),
    )


__all__ = ['calculate_markup_motivation']
