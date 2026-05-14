from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, List, Mapping, Optional


def to_plain_dict(obj: Any) -> Dict[str, Any]:
    """Convert dataclass-like quantitative result objects to plain dicts."""
    if obj is None:
        return {}
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, Mapping):
        return dict(obj)
    return dict(obj.__dict__) if hasattr(obj, '__dict__') else {}


@dataclass(slots=True)
class WalletCostResult:
    wallet_address: str
    token_address: str = ''
    wallet_avg_cost: Optional[float] = None
    wallet_first_buy_cost: Optional[float] = None
    wallet_last_buy_cost: Optional[float] = None
    wallet_cost_confidence: float = 0.0
    buy_amount_usd: Optional[float] = None
    buy_token_amount: Optional[float] = None
    first_buy_time: Optional[str] = None
    buy_count: Optional[int] = None
    sell_amount_usd: Optional[float] = None
    sell_token_amount: Optional[float] = None
    current_balance: Optional[float] = None
    cost_source_type_zh: str = '来源未知'
    wallet_cost_status_zh: str = '成本不可直接确认'
    wallet_cost_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DominantCostZoneResult:
    wallet_avg_cost: Optional[float] = None
    wallet_first_buy_cost: Optional[float] = None
    wallet_last_buy_cost: Optional[float] = None
    wallet_cost_confidence: Optional[float] = None
    same_source_group_cost_low: Optional[float] = None
    same_source_group_cost_mid: Optional[float] = None
    same_source_group_cost_high: Optional[float] = None
    same_source_group_cost_confidence: Optional[float] = None
    dominant_cost_low: Optional[float] = None
    dominant_cost_mid: Optional[float] = None
    dominant_cost_high: Optional[float] = None
    dominant_cost_confidence: Optional[float] = None
    dominant_cost_low_zh: Optional[float] = None
    dominant_cost_mid_zh: Optional[float] = None
    dominant_cost_high_zh: Optional[float] = None
    dominant_cost_confidence_zh: Optional[float] = None
    market_cost_mid: Optional[float] = None
    market_cost_mid_zh: Optional[float] = None
    box_cost_mid: Optional[float] = None
    box_cost_mid_zh: Optional[float] = None
    volume_cost_zone_zh: str = ''
    current_price: Optional[float] = None
    price_to_dominant_cost_pct: Optional[float] = None
    dominant_cost_deviation_rate: Optional[float] = None
    dominant_cost_deviation_status_zh: str = '成本区证据不足'
    cost_position_status_zh: str = '成本区证据不足'
    cost_evidence_grade_zh: str = '证据不足'
    cost_notes_zh: str = ''
    wallet_costs: List[WalletCostResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['wallet_costs'] = [w.to_dict() if hasattr(w, 'to_dict') else to_plain_dict(w) for w in self.wallet_costs]
        return data


@dataclass(slots=True)
class StructureInventoryEstimateResult:
    structure_max_inventory: Optional[float] = None
    structure_current_inventory: Optional[float] = None
    structure_inventory_remaining_pct: Optional[float] = None
    early_wallet_remaining_pct: Optional[float] = None
    same_source_group_remaining_pct: Optional[float] = None
    top_holder_structure_stability_score: Optional[float] = None
    inventory_status_zh: str = '库存状态未知'
    inventory_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DistributionProgressResult:
    structure_sold_pct: Optional[float] = None
    early_wallet_sold_pct: Optional[float] = None
    same_source_group_sold_pct: Optional[float] = None
    distribution_receiver_sold_pct: Optional[float] = None
    backflow_confirmed_pct: Optional[float] = None
    distribution_progress_score: Optional[float] = None
    distribution_progress_status_zh: str = '派发进度未知'
    distribution_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MarkupMotivationResult:
    remaining_inventory_score: Optional[float] = None
    unfinished_distribution_score: Optional[float] = None
    cost_position_score: Optional[float] = None
    pattern_control_score: Optional[float] = None
    liquidity_need_score: Optional[float] = None
    second_stage_condition_score: Optional[float] = None
    counterparty_pressure_penalty: Optional[float] = None
    same_source_exit_penalty: Optional[float] = None
    markup_motivation_score: Optional[float] = None
    markup_motivation_status_zh: str = '动机证据不足'
    markup_motivation_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CounterpartyPressureResult:
    late_large_buyer_score: Optional[float] = None
    whale_bagholder_score: Optional[float] = None
    retailization_score: Optional[float] = None
    early_to_late_transfer_score: Optional[float] = None
    floating_loss_late_holder_score: Optional[float] = None
    counterparty_pressure_score: Optional[float] = None
    counterparty_pressure_status_zh: str = '对手盘状态未知'
    counterparty_pressure_profile_zh: str = '对手盘画像未知'
    counterparty_pressure_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class WalletPatternCostAlignmentResult:
    pattern_type_zh: str = '匹配度未知'
    cost_pattern_match_score: Optional[float] = None
    wallet_behavior_match_score: Optional[float] = None
    alignment_status_zh: str = '匹配度未知'
    alignment_notes_zh: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class QuantitativeStructureReport:
    token_address: str
    token_symbol: str = ''
    chain: str = 'sol'
    analysis_time: Optional[str] = None
    summary_zh: str = ''
    dominant_cost_zone: Optional[DominantCostZoneResult] = None
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None
    distribution_progress: Optional[DistributionProgressResult] = None
    markup_motivation: Optional[MarkupMotivationResult] = None
    counterparty_pressure: Optional[CounterpartyPressureResult] = None
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
