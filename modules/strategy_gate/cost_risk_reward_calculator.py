from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from modules.wallet_structure.quantitative_structure_models import (
    CounterpartyPressureResult,
    DistributionProgressResult,
    DominantCostZoneResult,
    MarkupMotivationResult,
    StructureInventoryEstimateResult,
    WalletPatternCostAlignmentResult,
)


@dataclass(slots=True)
class StrategyGateRiskRewardResult:
    current_price: Optional[float] = None
    target_price: Optional[float] = None
    failure_price: Optional[float] = None
    upper_target_space: Optional[float] = None
    lower_failure_space: Optional[float] = None
    cost_risk_reward_ratio: Optional[float] = None
    target_space_pct: Optional[float] = None
    failure_space_pct: Optional[float] = None
    target_source_zh: str = '目标空间证据不足'
    failure_source_zh: str = '失效空间证据不足'
    risk_reward_status_zh: str = '风险收益比证据不足'
    risk_reward_notes_zh: str = ''
    handoff_note_zh: str = '仅供 Strategy Gate Bot 参与点筛选，不直接触发交易。'

    def to_dict(self) -> dict:
        return {
            'current_price': self.current_price,
            'target_price': self.target_price,
            'failure_price': self.failure_price,
            'upper_target_space': self.upper_target_space,
            'lower_failure_space': self.lower_failure_space,
            'cost_risk_reward_ratio': self.cost_risk_reward_ratio,
            'target_space_pct': self.target_space_pct,
            'failure_space_pct': self.failure_space_pct,
            'target_source_zh': self.target_source_zh,
            'failure_source_zh': self.failure_source_zh,
            'risk_reward_status_zh': self.risk_reward_status_zh,
            'risk_reward_notes_zh': self.risk_reward_notes_zh,
            'handoff_note_zh': self.handoff_note_zh,
        }


def _clamp(value: Optional[float], minimum: float, maximum: float) -> Optional[float]:
    if value is None:
        return None
    return max(minimum, min(maximum, float(value)))


def _num(value: Optional[float], default: float = 0.0) -> float:
    if value in (None, ''):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _current_price(dominant_cost_zone: Optional[DominantCostZoneResult], explicit: Optional[float]) -> Optional[float]:
    if explicit is not None:
        return float(explicit)
    if dominant_cost_zone is None:
        return None
    return dominant_cost_zone.current_price


def _target_anchor(dominant_cost_zone: Optional[DominantCostZoneResult]) -> tuple[Optional[float], str]:
    if dominant_cost_zone is None:
        return None, '目标空间需要由 Strategy Gate Bot 设定。'
    for value, source in [
        (dominant_cost_zone.dominant_cost_high, '主导侧成本上沿'),
        (dominant_cost_zone.same_source_group_cost_high, '同源组成本上沿'),
        (dominant_cost_zone.market_cost_mid, '市场成本中枢'),
        (dominant_cost_zone.dominant_cost_mid, '主导侧成本中枢'),
    ]:
        if value is not None:
            return float(value), f'目标锚点取自{source}。'
    return None, '目标空间缺少成本锚点。'


def _failure_anchor(dominant_cost_zone: Optional[DominantCostZoneResult]) -> tuple[Optional[float], str]:
    if dominant_cost_zone is None:
        return None, '失效空间需要由 Strategy Gate Bot 设定。'
    for value, source in [
        (dominant_cost_zone.dominant_cost_low, '主导侧成本下沿'),
        (dominant_cost_zone.same_source_group_cost_low, '同源组成本下沿'),
        (dominant_cost_zone.box_cost_mid, '控盘箱体中枢'),
        (dominant_cost_zone.market_cost_mid, '市场成本中枢'),
        (dominant_cost_zone.dominant_cost_mid, '主导侧成本中枢'),
    ]:
        if value is not None:
            return float(value), f'失效锚点取自{source}。'
    return None, '失效空间缺少成本锚点。'


def _target_multiplier(
    *,
    markup_motivation: Optional[MarkupMotivationResult],
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult],
) -> float:
    multiplier = 1.0
    motivation_score = _num(None if markup_motivation is None else markup_motivation.markup_motivation_score, 0.0)
    multiplier += min(max(motivation_score, 0.0), 6.0) * 0.05
    pattern = '' if wallet_pattern_cost_alignment is None else wallet_pattern_cost_alignment.pattern_type_zh
    if pattern == '二段放量':
        multiplier += 0.20
    elif pattern == '横盘控筹':
        multiplier += 0.12
    elif pattern == '主动派发':
        multiplier -= 0.10
    elif pattern == '结构崩塌':
        multiplier -= 0.25
    return _clamp(multiplier, 0.5, 2.5) or 1.0


def _failure_multiplier(
    *,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult],
    distribution_progress: Optional[DistributionProgressResult],
    counterparty_pressure: Optional[CounterpartyPressureResult],
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult],
) -> float:
    multiplier = 1.0
    remaining = _num(None if structure_inventory_estimate is None else structure_inventory_estimate.structure_inventory_remaining_pct, 0.5)
    sold = _num(None if distribution_progress is None else distribution_progress.structure_sold_pct, 0.5)
    pressure = _num(None if counterparty_pressure is None else counterparty_pressure.counterparty_pressure_score, 0.0)
    multiplier += (1.0 - remaining) * 0.20
    multiplier += sold * 0.25
    multiplier += min(max(pressure, 0.0), 100.0) / 100.0 * 0.25
    pattern = '' if wallet_pattern_cost_alignment is None else wallet_pattern_cost_alignment.pattern_type_zh
    if pattern == '主动派发':
        multiplier += 0.10
    elif pattern == '结构崩塌':
        multiplier += 0.25
    return _clamp(multiplier, 0.5, 3.0) or 1.0


def _risk_reward_status(ratio: Optional[float], upper_space: Optional[float], lower_space: Optional[float]) -> str:
    if ratio is None or upper_space is None or lower_space is None:
        return '风险收益比证据不足'
    if upper_space <= 0 or lower_space <= 0:
        return '追高接盘风险高'
    if ratio >= 3.0:
        return '风险收益比合适'
    if ratio >= 1.5:
        return '风险收益比一般'
    if ratio >= 0.8:
        return '风险收益比不足'
    return '追高接盘风险高'


def calculate_cost_risk_reward_ratio(
    *,
    dominant_cost_zone: Optional[DominantCostZoneResult] = None,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None,
    distribution_progress: Optional[DistributionProgressResult] = None,
    markup_motivation: Optional[MarkupMotivationResult] = None,
    counterparty_pressure: Optional[CounterpartyPressureResult] = None,
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult] = None,
    current_price: Optional[float] = None,
    possible_distribution_target_price: Optional[float] = None,
    key_failure_price: Optional[float] = None,
) -> StrategyGateRiskRewardResult:
    """Quantify the Strategy Gate participation risk/reward ratio.

    Formula:
    - upper_target_space = possible_distribution_target_price - current_price
    - lower_failure_space = current_price - key_failure_price
    - cost_risk_reward_ratio = upper_target_space / lower_failure_space

    The target and failure prices are derived from Intel Bot cost / inventory / distribution
    outputs when they are not passed explicitly.
    """
    current = _current_price(dominant_cost_zone, current_price)
    if current is None:
        return StrategyGateRiskRewardResult(
            risk_reward_status_zh='风险收益比证据不足',
            risk_reward_notes_zh='缺少当前价格，无法量化风险收益比。',
        )

    target_anchor, target_source = _target_anchor(dominant_cost_zone)
    failure_anchor, failure_source = _failure_anchor(dominant_cost_zone)
    target_multiplier = _target_multiplier(
        markup_motivation=markup_motivation,
        wallet_pattern_cost_alignment=wallet_pattern_cost_alignment,
    )
    failure_multiplier = _failure_multiplier(
        structure_inventory_estimate=structure_inventory_estimate,
        distribution_progress=distribution_progress,
        counterparty_pressure=counterparty_pressure,
        wallet_pattern_cost_alignment=wallet_pattern_cost_alignment,
    )

    base_target = float(possible_distribution_target_price) if possible_distribution_target_price is not None else max(current, target_anchor or current)
    base_failure = float(key_failure_price) if key_failure_price is not None else min(current, failure_anchor or current)

    target_price = base_target * target_multiplier
    failure_price = base_failure / failure_multiplier if failure_multiplier > 0 else base_failure

    upper_target_space = max(0.0, target_price - current)
    lower_failure_space = max(0.0, current - failure_price)
    ratio = None
    if lower_failure_space > 0:
        ratio = round(upper_target_space / lower_failure_space, 4)

    target_space_pct = round(upper_target_space / current, 4) if current > 0 else None
    failure_space_pct = round(lower_failure_space / current, 4) if current > 0 else None
    status = _risk_reward_status(ratio, upper_target_space, lower_failure_space)

    notes = [
        f'上方目标空间 = {target_price:g} - {current:g}。',
        f'下方失效空间 = {current:g} - {failure_price:g}。',
        target_source,
        failure_source,
        '该模型属于 Strategy Gate Bot，用于参与点门禁，不属于 Intel Bot 核心输出。',
    ]
    return StrategyGateRiskRewardResult(
        current_price=current,
        target_price=round(target_price, 6),
        failure_price=round(failure_price, 6),
        upper_target_space=round(upper_target_space, 6),
        lower_failure_space=round(lower_failure_space, 6),
        cost_risk_reward_ratio=ratio,
        target_space_pct=target_space_pct,
        failure_space_pct=failure_space_pct,
        target_source_zh=target_source,
        failure_source_zh=failure_source,
        risk_reward_status_zh=status,
        risk_reward_notes_zh=' '.join(notes),
    )


__all__ = ['StrategyGateRiskRewardResult', 'calculate_cost_risk_reward_ratio']
