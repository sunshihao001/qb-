from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional, Sequence

from .quantitative_structure_models import StructureInventoryEstimateResult


_STRUCTURE_ROLE_NAMES = {
    '疑似早期买入钱包',
    '疑似临时执行钱包',
    '疑似同源执行组成员',
    '疑似核心资金源候选',
    '疑似结果钱包',
    '疑似新钱包狙击',
}
_EXCLUDED_ROLE_NAMES = {'疑似接盘鲸鱼', '噪音钱包', '基础设施地址', '普通参与者'}
_EXCLUDED_ROLE_CODES = {'BAG_WHALE', 'NOISE', 'INFRA'}


def _first_present(row: Mapping[str, Any], keys: Sequence[str], default: Any = None) -> Any:
    for key in keys:
        if '.' in key:
            value: Any = row
            ok = True
            for part in key.split('.'):
                if isinstance(value, Mapping) and part in value:
                    value = value[part]
                else:
                    ok = False
                    break
            if ok and value not in (None, '', [], {}):
                return value
            continue
        value = row.get(key)
        if value not in (None, '', [], {}):
            return value
    return default


def _as_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value in (None, ''):
            return default
        return float(str(value).replace('%', '').replace(',', '').strip())
    except (TypeError, ValueError):
        return default


def _is_structure_inventory_candidate(row: Mapping[str, Any]) -> bool:
    role_name = str(row.get('role_name') or row.get('role') or row.get('role_code') or '')
    role_code = str(row.get('role_code') or '')
    address_base_type = str(row.get('address_base_type') or '').lower()
    note = str(row.get('gmgn_note') or '').lower()

    if role_name in _EXCLUDED_ROLE_NAMES or role_code in _EXCLUDED_ROLE_CODES:
        return False
    if any(marker in address_base_type for marker in ['exchange', 'router', 'infra', 'lp']):
        return False
    if any(marker in note for marker in ['交易所', '路由', '基础设施', '接盘']):
        return False
    if role_name in _STRUCTURE_ROLE_NAMES:
        return True
    if not role_name and _first_present(row, ['current_balance', 'holding_amount', 'balance', 'amount_cur', 'amount'], None) is not None:
        return True
    return False


def _inventory_status(remaining_ratio: Optional[float]) -> str:
    if remaining_ratio is None:
        return '库存状态未知'
    if remaining_ratio > 0.70:
        return '库存充足'
    if remaining_ratio >= 0.40:
        return '库存中等'
    if remaining_ratio >= 0.20:
        return '库存偏低'
    return '库存接近出清'


def calculate_structure_inventory_estimate(rows: Iterable[Mapping[str, Any]]) -> StructureInventoryEstimateResult:
    """Estimate undistributed inventory ratio for suspicious structure-side wallets.

    Formula:
    structure_inventory_remaining_pct = suspicious structure-side current holdings / suspicious structure-side historical max holdings
    """
    structure_current_inventory = 0.0
    structure_max_inventory = 0.0

    for row in rows:
        if not _is_structure_inventory_candidate(row):
            continue
        current = _as_float(_first_present(row, ['current_balance', 'holding_amount', 'balance', 'amount_cur', 'amount'], 0), 0.0) or 0.0
        max_inventory = _as_float(
            _first_present(
                row,
                ['historical_max_balance', 'history_max_balance', 'max_balance', 'max_holding_amount', 'structure_max_inventory'],
                None,
            ),
            None,
        )
        if max_inventory is None:
            bought = _as_float(_first_present(row, ['buy_token_amount', 'buy_amount_cur', 'total_buy_token_amount'], None), None)
            sold = _as_float(_first_present(row, ['sell_token_amount', 'sell_amount_cur', 'total_sell_token_amount'], 0), 0.0) or 0.0
            if bought is not None:
                max_inventory = max(bought, current + sold)
            else:
                max_inventory = current

        structure_current_inventory += current
        structure_max_inventory += max_inventory or 0.0

    remaining_pct = None
    if structure_max_inventory > 0:
        remaining_pct = round(structure_current_inventory / structure_max_inventory, 4)

    status = _inventory_status(remaining_pct)
    return StructureInventoryEstimateResult(
        structure_max_inventory=structure_max_inventory,
        structure_current_inventory=structure_current_inventory,
        structure_inventory_remaining_pct=remaining_pct,
        inventory_status_zh=status,
        inventory_notes_zh='结构侧未派发库存比例 = 疑似结构侧当前剩余持仓 / 疑似结构侧历史最大持仓，用于判断结构侧是否仍握有足够筹码继续做盘。',
    )


__all__ = ['calculate_structure_inventory_estimate']
