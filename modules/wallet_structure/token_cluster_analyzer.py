from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional

from .quantitative_structure_models import (
    DominantCostZoneResult,
    DistributionProgressResult,
    StructureInventoryEstimateResult,
    CounterpartyPressureResult,
    WalletPatternCostAlignmentResult,
    to_plain_dict,
)
from .counterparty_pressure_calculator import calculate_counterparty_pressure
from .wallet_pattern_cost_alignment_calculator import calculate_wallet_pattern_cost_alignment


def _num(v: Any, default: float = 0.0) -> float:
    if v in (None, '', [], {}):
        return default
    try:
        return float(v)
    except Exception:
        return default


def _first(row: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row.get(key) not in (None, '', [], {}):
            return row.get(key)
    return default


def analyze_token_cluster(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    """Lightweight token-cluster analysis bundle.

    This is a minimal clustering layer that groups rows into coarse buckets so
    downstream modules can consume cluster evidence without hard-coding source
    formats.
    """
    rows_list = [dict(r) for r in rows]
    groups: Dict[str, List[Dict[str, Any]]] = {'same_source': [], 'distribution': [], 'counterparty': [], 'other': []}
    for row in rows_list:
        role = str(_first(row, 'role_name', 'role', 'role_code', default=''))
        if '同源' in role:
            groups['same_source'].append(row)
        elif any(k in role for k in ('接盘', '鲸鱼', '散户', '浮亏', '晚期', '套牢')):
            groups['counterparty'].append(row)
        elif any(k in role for k in ('分发', '派发', '结果')):
            groups['distribution'].append(row)
        else:
            groups['other'].append(row)
    return {
        'token_address': _first(rows_list[0] if rows_list else {}, 'token_address', default=''),
        'wallet_count': len(rows_list),
        'same_source_count': len(groups['same_source']),
        'distribution_count': len(groups['distribution']),
        'counterparty_count': len(groups['counterparty']),
        'cluster_groups': groups,
    }


def infer_dominant_lifecycle(
    *,
    wallet_row: Mapping[str, Any],
    dominant_cost_zone: Optional[DominantCostZoneResult] = None,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None,
    distribution_progress: Optional[DistributionProgressResult] = None,
    counterparty_pressure: Optional[CounterpartyPressureResult] = None,
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult] = None,
) -> Dict[str, Any]:
    wallet = dict(wallet_row)
    counterparty_pressure = counterparty_pressure or calculate_counterparty_pressure(
        late_large_buyer_score=_num(_first(wallet, 'late_large_buyer_score')) or None,
        whale_bagholder_score=_num(_first(wallet, 'whale_bagholder_score')) or None,
        retailization_score=_num(_first(wallet, 'retailization_score')) or None,
        early_to_late_transfer_score=_num(_first(wallet, 'early_to_late_transfer_score')) or None,
        floating_loss_late_holder_score=_num(_first(wallet, 'floating_loss_late_holder_score')) or None,
    )
    wallet_pattern_cost_alignment = wallet_pattern_cost_alignment or calculate_wallet_pattern_cost_alignment(
        dominant_cost_zone=dominant_cost_zone,
        structure_inventory_estimate=structure_inventory_estimate,
        distribution_progress=distribution_progress,
    )

    structure_status = str(_first(wallet, 'wallet_structure_status', '当前状态', default='WALLET_NEUTRAL'))
    structure_score = _num(_first(wallet, 'wallet_structure_score', default=0))
    risk_score = _num(_first(wallet, 'wallet_risk_score', '钱包风险评分', default=0))
    counterparty_score = _num(_first(wallet, 'counterparty_pressure_score', '对手盘压力评分', default=0))
    sync_sell = _num(_first(wallet, 'same_source_sync_sell_score', default=0))
    pattern = wallet_pattern_cost_alignment.pattern_type_zh
    remaining = None if structure_inventory_estimate is None else structure_inventory_estimate.structure_inventory_remaining_pct
    sold = None if distribution_progress is None else distribution_progress.structure_sold_pct

    if structure_status == 'WALLET_BLOCK' or counterparty_score >= 70 or sync_sell >= 70:
        lifecycle = 'ACTIVE_DISTRIBUTION'
        intent = 'ACTIVE_DISTRIBUTION'
        action = 'BLOCKED'
        reason = '结构侧已出现高风险派发或对手盘压力。'
    elif pattern == '横盘控筹' and (remaining is None or remaining >= 0.4) and (sold is None or sold <= 0.4) and counterparty_score < 55:
        lifecycle = 'CONTROL_BOX_ACCUMULATION'
        intent = 'CONTROL'
        action = 'HIGH_PRIORITY_WATCHING'
        reason = '结构侧库存仍在且盘型符合横盘控筹。'
    elif pattern == '二段放量' and counterparty_score < 55:
        lifecycle = 'SECOND_STAGE_PREPARATION'
        intent = 'BREAKOUT_TEST'
        action = 'HIGH_PRIORITY_WATCHING'
        reason = '盘型进入二段放量准备。'
    elif pattern == '主动派发' or (sold is not None and sold >= 0.6):
        lifecycle = 'ACTIVE_DISTRIBUTION'
        intent = 'ACTIVE_DISTRIBUTION'
        action = 'BLOCKED'
        reason = '派发进度已偏高。'
    elif structure_status == 'WATCHING' and pattern in {'横盘控筹', '二段放量'} and risk_score < 40:
        lifecycle = 'REACTIVATION'
        intent = 'REACTIVATION'
        action = 'REACTIVATED_BY_SECOND_STAGE'
        reason = '观察态结构重新获得二段条件。'
    else:
        lifecycle = 'WASHOUT'
        intent = 'WASHOUT'
        action = 'OBSERVE_ONLY'
        reason = '缺少足够证据或结构侧仍未形成明确生命周期。'

    confidence = 0.55
    if structure_score >= 70 or risk_score >= 70 or counterparty_score >= 70:
        confidence = 0.8
    elif structure_score >= 50 or pattern != '匹配度未知':
        confidence = 0.65

    return {
        'dominant_side_lifecycle': lifecycle,
        'dominant_side_intent': intent,
        'allowed_action': action,
        'counterparty_state': 'EXIT_LIQUIDITY_FORMING' if counterparty_score >= 70 else 'COUNTERPARTY_NORMAL',
        'structure_defense_status': 'DEFENDING_CONTROL_BOX' if lifecycle in {'CONTROL_BOX_ACCUMULATION', 'SECOND_STAGE_PREPARATION'} else 'STRUCTURE_NEUTRAL',
        'chip_control_state': 'CONTROL_RETAINED_BY_STRUCTURE_SIDE' if lifecycle in {'CONTROL_BOX_ACCUMULATION', 'SECOND_STAGE_PREPARATION'} else 'CONTROL_UNCLEAR',
        'would_pause_by_lifecycle': lifecycle in {'SECOND_STAGE_PREPARATION'},
        'would_block_by_lifecycle': action == 'BLOCKED',
        'evidence_level': 'E4' if confidence >= 0.8 else 'E3' if confidence >= 0.65 else 'E2',
        'dominant_side_confidence': confidence,
        'reason_zh': reason,
    }


def classify_dominant_intent(
    *,
    holder_cluster: Mapping[str, Any],
    wallet_behavior: Mapping[str, Any],
    lifecycle: Mapping[str, Any],
    cost_zone: Mapping[str, Any],
    inventory: Mapping[str, Any],
    distribution_progress: Mapping[str, Any],
    counterparty_pressure: Mapping[str, Any],
    pattern_alignment: Mapping[str, Any],
) -> Dict[str, Any]:
    dominant_code = str(lifecycle.get('dominant_side_intent') or lifecycle.get('dominant_side_lifecycle') or 'WASHOUT')
    if dominant_code not in {'ACCUMULATE', 'CONTROL', 'WASHOUT', 'BREAKOUT_TEST', 'MARKUP', 'PARTIAL_DISTRIBUTION', 'ACTIVE_DISTRIBUTION', 'REACCUMULATION', 'REACTIVATION', 'ABANDONMENT'}:
        dominant_code = 'WASHOUT'
    confidence = 0.6
    if lifecycle.get('dominant_side_confidence') is not None:
        confidence = float(lifecycle['dominant_side_confidence'])
    evidence_breakdown = {
        'holder_cluster': dict(holder_cluster),
        'wallet_behavior': dict(wallet_behavior),
        'lifecycle': dict(lifecycle),
        'cost_zone': dict(cost_zone),
        'inventory': dict(inventory),
        'distribution_progress': dict(distribution_progress),
        'counterparty_pressure': dict(counterparty_pressure),
        'pattern_alignment': dict(pattern_alignment),
    }
    conflict_notes = []
    if str(pattern_alignment.get('pattern_type_zh', '')) == '结构崩塌' and dominant_code in {'CONTROL', 'MARKUP', 'REACTIVATION'}:
        conflict_notes.append('盘型已偏向结构崩塌，但生命周期仍指向继续推进，存在冲突。')
    if float(counterparty_pressure.get('counterparty_pressure_score', 0) or 0) >= 70 and dominant_code in {'CONTROL', 'MARKUP', 'REACTIVATION'}:
        conflict_notes.append('对手盘压力较高，但意图仍偏继续推进，需要复核。')
    return {
        'dominant_intent_code': dominant_code,
        'dominant_intent_status_zh': dominant_code,
        'dominant_intent_confidence': confidence,
        'intent_evidence_breakdown': evidence_breakdown,
        'conflict_notes_zh': '；'.join(conflict_notes) if conflict_notes else '无明显冲突。',
    }


__all__ = ['analyze_token_cluster', 'infer_dominant_lifecycle', 'classify_dominant_intent']
