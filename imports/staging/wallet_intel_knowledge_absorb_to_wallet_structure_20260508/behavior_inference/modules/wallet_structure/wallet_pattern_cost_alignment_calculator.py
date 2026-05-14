from __future__ import annotations

from typing import Optional

from .quantitative_structure_models import DominantCostZoneResult, DistributionProgressResult, StructureInventoryEstimateResult, WalletPatternCostAlignmentResult


def _score_cost_alignment(dominant_cost_zone: Optional[DominantCostZoneResult]) -> Optional[float]:
    if dominant_cost_zone is None:
        return None
    price = dominant_cost_zone.current_price
    mid = dominant_cost_zone.dominant_cost_mid or dominant_cost_zone.same_source_group_cost_mid
    if price is None or mid in (None, 0):
        return None
    ratio = price / mid
    if 0.9 <= ratio <= 1.1:
        return 90.0
    if 0.75 <= ratio <= 1.25:
        return 75.0
    if 0.6 <= ratio <= 1.4:
        return 55.0
    return 30.0


def _score_behavior_alignment(
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult],
    distribution_progress: Optional[DistributionProgressResult],
) -> Optional[float]:
    if structure_inventory_estimate is None and distribution_progress is None:
        return None
    remaining = None if structure_inventory_estimate is None else structure_inventory_estimate.structure_inventory_remaining_pct
    sold = None if distribution_progress is None else distribution_progress.structure_sold_pct
    if remaining is None and sold is None:
        return None
    remaining = remaining if remaining is not None else 0.5
    sold = sold if sold is not None else 0.5
    return round(max(0.0, min(100.0, remaining * 100.0 * 0.65 + (1.0 - sold) * 100.0 * 0.35)), 2)


def _pattern_type(cost_score: Optional[float], behavior_score: Optional[float], dominant_cost_zone: Optional[DominantCostZoneResult], distribution_progress: Optional[DistributionProgressResult]) -> str:
    sold = None if distribution_progress is None else distribution_progress.structure_sold_pct
    price = None if dominant_cost_zone is None else dominant_cost_zone.current_price
    mid = None if dominant_cost_zone is None else (dominant_cost_zone.dominant_cost_mid or dominant_cost_zone.same_source_group_cost_mid)
    if sold is not None and sold >= 0.7:
        return '结构崩塌'
    if price is not None and mid not in (None, 0) and price <= mid * 0.85 and sold is not None and sold >= 0.5:
        return '主动派发'
    if cost_score is not None and cost_score >= 70 and behavior_score is not None and behavior_score >= 70:
        return '横盘控筹'
    if price is not None and mid not in (None, 0) and price >= mid * 1.2 and (sold or 0) <= 0.3:
        return '二段放量'
    return '匹配度未知'


def _alignment_status(score: Optional[float]) -> str:
    if score is None:
        return '匹配度未知'
    if score >= 75:
        return '匹配度高'
    if score >= 40:
        return '匹配度中'
    return '匹配度低'


def calculate_wallet_pattern_cost_alignment(
    *,
    dominant_cost_zone: Optional[DominantCostZoneResult] = None,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None,
    distribution_progress: Optional[DistributionProgressResult] = None,
) -> WalletPatternCostAlignmentResult:
    """Judge whether cost zone, wallet behavior and market pattern are aligned."""
    cost_score = _score_cost_alignment(dominant_cost_zone)
    behavior_score = _score_behavior_alignment(structure_inventory_estimate, distribution_progress)
    if cost_score is None and behavior_score is None:
        return WalletPatternCostAlignmentResult(
            pattern_type_zh='匹配度未知',
            cost_pattern_match_score=None,
            wallet_behavior_match_score=None,
            alignment_status_zh='匹配度未知',
            alignment_notes_zh='证据不足，无法判断成本区、钱包行为和盘型是否匹配。',
        )

    pattern = _pattern_type(cost_score, behavior_score, dominant_cost_zone, distribution_progress)
    if pattern == '结构崩塌' and cost_score is not None:
        cost_score = min(cost_score, 30.0)
    combined = None
    if cost_score is not None and behavior_score is not None:
        combined = round(cost_score * 0.55 + behavior_score * 0.35 - (15.0 if pattern == '结构崩塌' else 0.0), 2)
    elif cost_score is not None:
        combined = cost_score
    elif behavior_score is not None:
        combined = behavior_score
    return WalletPatternCostAlignmentResult(
        pattern_type_zh=pattern,
        cost_pattern_match_score=cost_score,
        wallet_behavior_match_score=behavior_score,
        alignment_status_zh=_alignment_status(combined),
        alignment_notes_zh='成本区与钱包行为、派发进度共同判断盘型是否属于横盘控筹、二段放量、主动派发或结构崩塌。',
    )


__all__ = ['calculate_wallet_pattern_cost_alignment']
