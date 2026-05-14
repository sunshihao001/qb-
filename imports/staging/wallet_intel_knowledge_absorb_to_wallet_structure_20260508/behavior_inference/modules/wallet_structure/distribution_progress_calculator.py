from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional, Sequence

from .quantitative_structure_models import DistributionProgressResult
from .structure_inventory_calculator import _as_float, _first_present, _is_structure_inventory_candidate


def _distribution_status(progress: Optional[float]) -> str:
    if progress is None:
        return '派发进度未知'
    if progress < 0.20:
        return '尚未明显派发'
    if progress <= 0.50:
        return '部分派发'
    if progress <= 0.80:
        return '明显派发'
    return '接近派发完成'


def _historical_max_inventory(row: Mapping[str, Any], sold_amount: float) -> float:
    max_inventory = _as_float(
        _first_present(
            row,
            ['historical_max_balance', 'history_max_balance', 'max_balance', 'max_holding_amount', 'structure_max_inventory'],
            None,
        ),
        None,
    )
    if max_inventory is not None:
        return max_inventory
    current = _as_float(_first_present(row, ['current_balance', 'holding_amount', 'balance', 'amount_cur', 'amount'], 0), 0.0) or 0.0
    bought = _as_float(_first_present(row, ['buy_token_amount', 'buy_amount_cur', 'total_buy_token_amount'], None), None)
    if bought is not None:
        return max(bought, current + sold_amount)
    return current + sold_amount


def calculate_distribution_progress(rows: Iterable[Mapping[str, Any]]) -> DistributionProgressResult:
    """Calculate structure-side distribution progress.

    Formula:
    structure_sold_pct = suspicious structure-side sold token amount / suspicious structure-side historical max holdings
    """
    structure_sold_amount = 0.0
    structure_max_inventory = 0.0

    for row in rows:
        if not _is_structure_inventory_candidate(row):
            continue
        sold_amount = _as_float(
            _first_present(row, ['sell_token_amount', 'sell_amount_cur', 'total_sell_token_amount', 'sold_token_amount'], 0),
            0.0,
        ) or 0.0
        structure_sold_amount += sold_amount
        structure_max_inventory += _historical_max_inventory(row, sold_amount) or 0.0

    structure_sold_pct = None
    if structure_max_inventory > 0:
        structure_sold_pct = round(structure_sold_amount / structure_max_inventory, 4)

    status = _distribution_status(structure_sold_pct)
    return DistributionProgressResult(
        structure_sold_pct=structure_sold_pct,
        distribution_progress_score=structure_sold_pct,
        distribution_progress_status_zh=status,
        distribution_notes_zh='派发进度 = 疑似结构侧已卖出数量 / 疑似结构侧历史最大持仓，用于判断主导侧是否已经基本出完。',
    )


__all__ = ['calculate_distribution_progress']
