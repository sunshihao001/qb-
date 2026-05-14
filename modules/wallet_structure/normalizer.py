
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping

from .constants import ROLE_TO_CODE

_ALIASES = {
    'wallet_address': ['wallet_address', 'address', '钱包地址'],
    'token_address': ['token_address', '代币地址', 'mint'],
    'token_symbol': ['token_symbol', '代币符号', 'symbol'],
    'chain': ['chain', '链'],
    'gmgn_tags': ['gmgn_tags', 'tags', 'GMGN标签'],
    'maker_token_tags': ['maker_token_tags', 'maker_tags'],
    'source_lists': ['source_lists', 'source_list', '来源列表'],
    'addr_type': ['addr_type', 'address_type'],
    'transfer_in': ['transfer_in', '是否转入'],
    'first_buy_time': ['first_buy_time', 'first_buy_timestamp', 'start_holding_at', '首次买入时间'],
    'last_active_time': ['last_active_time', 'last_active_timestamp', '最后活动时间'],
    'wallet_age_days': ['wallet_age_days', 'age_days'],
    'holding_amount': ['holding_amount', 'amount', '持仓数量'],
    'holding_pct': ['holding_pct', 'amount_percentage', '持仓占比'],
    'sold_pct': ['sold_pct', 'sell_amount_percentage', '卖出占比'],
    'buy_usd': ['buy_usd', 'buy_volume_usd', 'total_buy_usd'],
    'sell_usd': ['sell_usd', 'sell_volume_usd', 'total_sell_usd'],
    'roi': ['roi', 'profit_percentage', 'pnl_rate'],
    'pnl': ['pnl', 'profit', 'total_profit'],
    'realized_pnl': ['realized_pnl', 'realized_profit', 'realized_profit_usd'],
    'unrealized_pnl': ['unrealized_pnl', 'unrealized_profit', 'unrealized_profit_usd'],
    'token_source_address': ['token_source_address', 'token_transfer_in.address', 'token_in_address'],
    'token_destination_address': ['token_destination_address', 'token_transfer_out.address', 'token_out_address'],
    'funding_source_address': ['funding_source_address', 'native_transfer.from_address', 'funding_source', 'funding'],
    'funding_source_type': ['funding_source_type'],
    'same_source_group_id': ['same_source_group_id', 'group_id', 'same_source_group'],
    'distribution_path_id': ['distribution_path_id'],
    'backflow_path_id': ['backflow_path_id'],
    'role_name': ['role_name', '当前角色', '最终角色', 'role'],
    'role_code': ['role_code'],
    'evidence_level': ['evidence_level', '证据等级'],
    'risk_level': ['risk_level', '风险等级'],
    'tracking_level': ['tracking_level', '追踪等级'],
    'gmgn_note': ['gmgn_note', 'SIKK备注', 'note'],
    'evidence_chain': ['evidence_chain'],
}

_ROLE_DEFAULT_RISK = {
    '新钱包狙击': 'R1', '临时执行钱包': 'R2', '同源执行组成员': 'R3', '分发接收钱包': 'R2',
    '分发派发钱包': 'R3', '利润回流节点': 'R4', '核心资金源候选': 'R4', '结果钱包': 'R0',
    '接盘鲸鱼': 'R2', '套牢钱包': 'R1', '可疑中转节点': 'R3', 'LP/池子/路由器/基础设施': 'R0',
    '普通交易钱包': 'R0', '噪音钱包': 'R0',
}

_ROLE_DEFAULT_TRACK = {
    '新钱包狙击': 'A3', '临时执行钱包': 'A3', '同源执行组成员': 'A4', '分发接收钱包': 'A3',
    '分发派发钱包': 'A4', '利润回流节点': 'A4', '核心资金源候选': 'A4', '结果钱包': 'A3',
    '接盘鲸鱼': 'A2', '套牢钱包': 'A2', '可疑中转节点': 'A3', 'LP/池子/路由器/基础设施': 'A0',
    '普通交易钱包': 'A1', '噪音钱包': 'A0',
}

def _first_present(row: Mapping[str, Any], keys: Iterable[str], default: Any = None) -> Any:
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

def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ''):
            return default
        return float(str(value).replace('%', '').strip())
    except (TypeError, ValueError):
        return default

def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ''):
        return default
    if isinstance(value, str):
        return value.strip().lower() in {'1', 'true', 'yes', 'y', '是'}
    return bool(value)

def _as_text(value: Any, default: str = '') -> str:
    if value in (None, ''):
        return default
    return str(value)

def _standard_time(value: Any) -> str:
    if value in (None, ''):
        return ''
    if isinstance(value, str) and ('T' in value or value.endswith('Z')):
        return value
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    except (TypeError, ValueError):
        return str(value)

def normalize_wallet_row(row: Mapping[str, Any], token_address: str = '', token_symbol: str = '', chain: str = 'sol') -> Dict[str, Any]:
    base = dict(row)
    role_name = _as_text(_first_present(base, _ALIASES['role_name'], '普通交易钱包'), '普通交易钱包')
    role_code = _as_text(_first_present(base, _ALIASES['role_code'], ROLE_TO_CODE.get(role_name, 'NORMAL')), ROLE_TO_CODE.get(role_name, 'NORMAL'))
    role_code = role_code if role_code else ROLE_TO_CODE.get(role_name, 'NORMAL')
    normalized = {
        'token_address': _as_text(_first_present(base, _ALIASES['token_address'], token_address), token_address),
        'token_symbol': _as_text(_first_present(base, _ALIASES['token_symbol'], token_symbol), token_symbol),
        'chain': _as_text(_first_present(base, _ALIASES['chain'], chain), chain),
        'wallet_address': _as_text(_first_present(base, _ALIASES['wallet_address']), ''),
        'source_lists': list(_first_present(base, _ALIASES['source_lists'], []) or []),
        'gmgn_tags': list(_first_present(base, _ALIASES['gmgn_tags'], []) or []),
        'maker_token_tags': list(_first_present(base, _ALIASES['maker_token_tags'], []) or []),
        'addr_type': _first_present(base, _ALIASES['addr_type'], None),
        'address_base_type': _as_text(_first_present(base, ['address_base_type'], 'wallet'), 'wallet'),
        'transfer_in': _as_bool(_first_present(base, _ALIASES['transfer_in'], False), False),
        'first_buy_time': _standard_time(_first_present(base, _ALIASES['first_buy_time'], '')),
        'last_active_time': _standard_time(_first_present(base, _ALIASES['last_active_time'], '')),
        'wallet_age_days': _as_float(_first_present(base, _ALIASES['wallet_age_days'], None), 0.0) if _first_present(base, _ALIASES['wallet_age_days'], None) is not None else None,
        'holding_amount': _as_float(_first_present(base, _ALIASES['holding_amount'], 0.0), 0.0),
        'holding_pct': _as_float(_first_present(base, _ALIASES['holding_pct'], 0.0), 0.0),
        'sold_pct': _as_float(_first_present(base, _ALIASES['sold_pct'], 0.0), 0.0),
        'buy_usd': _as_float(_first_present(base, _ALIASES['buy_usd'], 0.0), 0.0),
        'sell_usd': _as_float(_first_present(base, _ALIASES['sell_usd'], 0.0), 0.0),
        'roi': _as_float(_first_present(base, _ALIASES['roi'], 0.0), 0.0),
        'pnl': _as_float(_first_present(base, _ALIASES['pnl'], 0.0), 0.0),
        'realized_pnl': _as_float(_first_present(base, _ALIASES['realized_pnl'], 0.0), 0.0),
        'unrealized_pnl': _as_float(_first_present(base, _ALIASES['unrealized_pnl'], 0.0), 0.0),
        'token_source_address': _as_text(_first_present(base, _ALIASES['token_source_address'], ''), ''),
        'token_destination_address': _as_text(_first_present(base, _ALIASES['token_destination_address'], ''), ''),
        'funding_source_address': _as_text(_first_present(base, _ALIASES['funding_source_address'], ''), ''),
        'funding_source_type': _as_text(_first_present(base, _ALIASES['funding_source_type'], 'unknown'), 'unknown'),
        'same_source_group_id': _as_text(_first_present(base, _ALIASES['same_source_group_id'], ''), ''),
        'distribution_path_id': _as_text(_first_present(base, _ALIASES['distribution_path_id'], ''), ''),
        'backflow_path_id': _as_text(_first_present(base, _ALIASES['backflow_path_id'], ''), ''),
        'role_name': role_name,
        'role_code': role_code,
        'evidence_level': _as_text(_first_present(base, _ALIASES['evidence_level'], 'E0'), 'E0'),
        'risk_level': _as_text(_first_present(base, _ALIASES['risk_level'], _ROLE_DEFAULT_RISK.get(role_name, 'R0')), _ROLE_DEFAULT_RISK.get(role_name, 'R0')),
        'tracking_level': _as_text(_first_present(base, _ALIASES['tracking_level'], _ROLE_DEFAULT_TRACK.get(role_name, 'A1')), _ROLE_DEFAULT_TRACK.get(role_name, 'A1')),
        'gmgn_note': _as_text(_first_present(base, _ALIASES['gmgn_note'], ''), ''),
        'evidence_chain': list(_first_present(base, _ALIASES['evidence_chain'], []) or []),
    }
    normalized['missing_fields'] = [k for k, v in normalized.items() if v in (None, '', [], {}) and k not in {'wallet_age_days', 'gmgn_note'}]
    return normalized

def normalize_wallet_rows(rows: Iterable[Mapping[str, Any]], token_address: str = '', token_symbol: str = '', chain: str = 'sol') -> List[Dict[str, Any]]:
    return [normalize_wallet_row(row, token_address=token_address, token_symbol=token_symbol, chain=chain) for row in rows]
