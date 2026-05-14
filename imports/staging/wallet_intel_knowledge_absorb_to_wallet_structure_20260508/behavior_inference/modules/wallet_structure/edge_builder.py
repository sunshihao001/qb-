
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Mapping

def _as_text(value: Any, default: str = '') -> str:
    if value in (None, ''):
        return default
    return str(value)

def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ''):
            return default
        return float(str(value).replace('%', '').strip())
    except (TypeError, ValueError):
        return default

def _role(row: Mapping[str, Any]) -> str:
    return _as_text(row.get('role_name') or row.get('role') or '普通交易钱包', '普通交易钱包')

def _group_id(row: Mapping[str, Any]) -> str:
    return _as_text(row.get('same_source_group_id') or row.get('group_id') or row.get('same_source_group'), '')

def build_wallet_edges(rows: Iterable[Mapping[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    rows = list(rows)
    funding_edges: List[Dict[str, Any]] = []
    token_flow_edges: List[Dict[str, Any]] = []
    same_source_groups: Dict[str, Dict[str, Any]] = {}
    distribution_paths: List[Dict[str, Any]] = []
    backflow_paths: List[Dict[str, Any]] = []

    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        gid = _group_id(row)
        if gid:
            grouped[gid].append(row)

    for row in rows:
        wallet = _as_text(row.get('wallet_address') or row.get('address') or '', '')
        token = _as_text(row.get('token_address') or '', '')
        source = _as_text(row.get('funding_source_address') or row.get('native_transfer.from_address') or '', '')
        token_source = _as_text(row.get('token_source_address') or '', '')
        token_dest = _as_text(row.get('token_destination_address') or '', '')
        sold_pct = _as_float(row.get('sold_pct') or row.get('sell_amount_percentage') or 0.0, 0.0)
        transfer_in = bool(row.get('transfer_in'))
        role = _role(row)
        if source:
            funding_edges.append({
                'token_address': token,
                'wallet_address': wallet,
                'source_address': source,
                'source_type': _as_text(row.get('funding_source_type') or 'unknown', 'unknown'),
                'edge_type': 'funding',
                'amount_usd': _as_float(row.get('buy_usd') or 0.0, 0.0),
                'evidence_level': _as_text(row.get('evidence_level') or 'E0', 'E0'),
                'role_name': role,
            })
        if token_source:
            token_flow_edges.append({
                'token_address': token,
                'from_address': token_source,
                'to_address': wallet,
                'edge_type': 'token_in',
                'amount_usd': _as_float(row.get('buy_usd') or 0.0, 0.0),
                'role_name': role,
                'path_id': _as_text(row.get('distribution_path_id') or '', ''),
            })
        if token_dest:
            token_flow_edges.append({
                'token_address': token,
                'from_address': wallet,
                'to_address': token_dest,
                'edge_type': 'token_out',
                'amount_usd': _as_float(row.get('sell_usd') or 0.0, 0.0),
                'role_name': role,
                'path_id': _as_text(row.get('backflow_path_id') or '', ''),
            })
        if transfer_in and sold_pct >= 0.6:
            distribution_paths.append({
                'token_address': token,
                'wallet_address': wallet,
                'path_type': 'distribution_sell',
                'sold_pct': sold_pct,
                'role_name': role,
                'source_address': token_source or source,
            })
        if _as_float(row.get('pnl') or row.get('profit') or 0.0, 0.0) > 0 and (token_dest or source):
            backflow_paths.append({
                'token_address': token,
                'wallet_address': wallet,
                'path_type': 'profit_backflow_candidate',
                'sold_pct': sold_pct,
                'role_name': role,
                'sink_address': token_dest or source,
            })

    try:
        from sikk_same_source_grouping import build_same_source_groups
    except Exception:
        build_same_source_groups = None
    if build_same_source_groups is not None:
        try:
            built = build_same_source_groups(token_address=rows[0].get('token_address', '') if rows else '', token_symbol=rows[0].get('token_symbol', '') if rows else '', wallet_rows=rows)
        except Exception:
            built = []
        for group in built or []:
            gid = _as_text(group.get('group_id') or group.get('组ID') or group.get('same_source_group_id') or '', '')
            if not gid:
                continue
            same_source_groups[gid] = dict(group)
    for gid, members in grouped.items():
        if gid not in same_source_groups:
            same_source_groups[gid] = {
                'group_id': gid,
                'token_address': _as_text(members[0].get('token_address') if members else '', ''),
                'token_symbol': _as_text(members[0].get('token_symbol') if members else '', ''),
                'member_count': len(members),
                'funding_source_address': _as_text(members[0].get('funding_source_address') if members else '', ''),
                'sync_buy_score': min(100, 40 + len(members) * 10),
                'sync_sell_score': min(100, 20 + sum(1 for m in members if _as_float(m.get('sold_pct') or m.get('sell_amount_percentage') or 0.0, 0.0) >= 0.7) * 15),
                'evidence_level': 'E3' if len(members) >= 2 else 'E2',
            }

    return {
        'wallet_funding_edges': funding_edges,
        'wallet_token_flow_edges': token_flow_edges,
        'same_source_groups': list(same_source_groups.values()),
        'distribution_paths': distribution_paths,
        'backflow_paths': backflow_paths,
    }
