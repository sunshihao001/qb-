
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from .constants import CANONICAL_ROLE_BY_CODE, CODE_TO_ROLE, ROLE_TO_CODE
from .chinese_judgement import zh
from .models import WalletRoleResult
from .normalizer import _as_float, _as_text

def _evidence_from(row: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, '', [], {}):
            return str(value)
    return 'E0'

def _risk_from_role(role_name: str) -> str:
    return {
        '疑似新钱包狙击': 'R1', '疑似临时执行钱包': 'R2', '疑似同源执行组成员': 'R3', '疑似 Token 接收钱包': 'R2',
        '疑似分发派发钱包': 'R3', '疑似利润回收钱包': 'R4', '疑似核心资金源候选': 'R4', '疑似结果钱包': 'R0',
        '疑似接盘鲸鱼': 'R2', '疑似套牢钱包': 'R1', '可疑中转节点': 'R3', '基础设施地址': 'R0',
        '普通参与者': 'R0', '噪音钱包': 'R0',
    }.get(role_name, 'R0')

def _tracking_from_role(role_name: str) -> str:
    return {
        '疑似新钱包狙击': 'A3', '疑似临时执行钱包': 'A3', '疑似同源执行组成员': 'A4', '疑似 Token 接收钱包': 'A3',
        '疑似分发派发钱包': 'A4', '疑似利润回收钱包': 'A4', '疑似核心资金源候选': 'A4', '疑似结果钱包': 'A3',
        '疑似接盘鲸鱼': 'A2', '疑似套牢钱包': 'A2', '可疑中转节点': 'A3', '基础设施地址': 'A0',
        '普通参与者': 'A1', '噪音钱包': 'A0',
    }.get(role_name, 'A1')

def classify_wallet_row(row: Mapping[str, Any]) -> WalletRoleResult:
    role_name_raw = _as_text(row.get('role_name') or row.get('当前角色') or row.get('最终角色') or row.get('role') or '普通参与者', '普通参与者')
    role_name = role_name_raw if role_name_raw in ROLE_TO_CODE else CODE_TO_ROLE.get(role_name_raw, '普通参与者')
    if role_name not in ROLE_TO_CODE:
        role_name = '普通参与者'
    role_code = ROLE_TO_CODE[role_name]
    role_name = CANONICAL_ROLE_BY_CODE.get(role_code, role_name)
    sell_pct = _as_float(row.get('sold_pct') or row.get('sell_amount_percentage') or row.get('卖出占比'), 0.0)
    hold_pct = _as_float(row.get('holding_pct') or row.get('amount_percentage') or row.get('持仓占比'), 0.0)
    pnl = _as_float(row.get('pnl') or row.get('profit') or row.get('total_profit'), 0.0)
    tags = list(row.get('gmgn_tags') or row.get('tags') or [])
    maker_tags = list(row.get('maker_token_tags') or [])
    signal_text = ','.join([str(t) for t in tags + maker_tags if t])
    signals: List[str] = []
    if signal_text:
        signals.append(f'tags={signal_text}')
    if row.get('transfer_in'):
        signals.append('transfer_in')
    if hold_pct:
        signals.append(f'hold={hold_pct:.4f}')
    if sell_pct:
        signals.append(f'sell={sell_pct:.4f}')
    if pnl:
        signals.append(f'pnl={pnl:.2f}')
    evidence = _evidence_from(row, 'evidence_level', 'wallet_evidence_level', '证据等级')
    if role_name in {'疑似分发派发钱包', '疑似利润回收钱包', '疑似核心资金源候选'} and evidence in {'E0', 'E1'}:
        evidence = 'E3'
    if role_name == '疑似结果钱包' and pnl > 0 and evidence in {'E0', 'E1'}:
        evidence = 'E3'
    risk_level = _risk_from_role(role_name)
    tracking_level = _tracking_from_role(role_name)
    note = _as_text(row.get('gmgn_note') or row.get('SIKK备注') or '', '')
    if not note:
        symbol = _as_text(row.get('token_symbol') or row.get('代币符号') or '', '')
        group = _as_text(row.get('same_source_group_id') or row.get('group_id') or '', '')
        note = f"{symbol}-{role_name}-{zh('evidence', evidence, evidence)}-{group or zh('risk', risk_level, risk_level)}"
    return WalletRoleResult(
        wallet_address=_as_text(row.get('wallet_address') or row.get('address') or row.get('钱包地址') or '', ''),
        role_name=role_name,
        role_code=role_code,
        evidence_level=evidence,
        risk_level=risk_level,
        tracking_level=tracking_level,
        gmgn_note=note,
        note_template='',
        score=max(0.0, min(100.0, pnl + hold_pct * 100.0 - sell_pct * 50.0)),
        signals=signals,
    )

def classify_wallet_rows(rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [classify_wallet_row(row).to_row() for row in rows]
