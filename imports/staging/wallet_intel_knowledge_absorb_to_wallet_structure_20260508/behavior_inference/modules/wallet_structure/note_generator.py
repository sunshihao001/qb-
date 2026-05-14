
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping
from .chinese_judgement import zh

_TEMPLATE = {
    '疑似新钱包狙击': ('新狙', '🎯', '{symbol}-新狙-{roi}x-{tag}-{group}', '早期新钱包/狙击'),
    '疑似临时执行钱包': ('临执', '⚡', '{symbol}-临执-{roi}x-{tag}-{group}', '临时执行参与'),
    '疑似同源执行组成员': ('G成员', '🔗', '{symbol}-G{group}成员-{roi}x-{tag}', '同源执行组'),
    '疑似 Token 接收钱包': ('分发接收', '📥', '{symbol}-分发接收-{status}-{source}-{risk}', 'Token 接收'),
    '疑似分发派发钱包': ('分发卖出', '📤', '{symbol}-分发卖出-{status}-{risk}', '高比例派发卖出'),
    '疑似利润回收钱包': ('回流节点', '🔁', '{symbol}-回流节点-{status}-{risk}', '卖后资金回流'),
    '疑似核心资金源候选': ('资金源', '⛽', '{symbol}-资金源-{status}-{group}', '疑似资金源'),
    '疑似结果钱包': ('结果', '🏁', '{symbol}-结果钱包-{roi}x-{tag}', '高结果钱包'),
    '疑似接盘鲸鱼': ('接盘鲸鱼', '🐋', '{symbol}-接盘鲸鱼-{status}-{risk}', '高位接盘'),
    '疑似套牢钱包': ('套牢', '🪤', '{symbol}-套牢-{status}-{risk}', '浮亏持仓'),
    '可疑中转节点': ('中转', '🚧', '{symbol}-中转-{tag}-{risk}', '可疑中转'),
    '基础设施地址': ('基础设施', '🏗️', '{symbol}-基础设施-{type}', '基础设施地址'),
    '普通参与者': ('普通', '👤', '{symbol}-普通-{status}-{tracking}', '普通参与者'),
    '噪音钱包': ('噪音', '🔇', '{symbol}-噪音-低权重', '噪音/低权重'),
}

def _value(row: Mapping[str, Any], *keys: str, default: Any = '') -> Any:
    for key in keys:
        value = row.get(key)
        if value not in (None, '', [], {}):
            return value
    return default

def generate_gmgn_notes(rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    notes: List[Dict[str, Any]] = []
    for row in rows:
        role = str(_value(row, 'role_name', '当前角色', 'role', default='普通参与者'))
        short_name, emoji, template, use_case = _TEMPLATE.get(role, _TEMPLATE['普通参与者'])
        symbol = str(_value(row, 'token_symbol', '代币符号', default=''))
        roi = _value(row, 'roi', 'profit_percentage', 'pnl_rate', default='')
        roi_text = f'{float(roi):.1f}' if isinstance(roi, (int, float)) or str(roi).replace('.', '', 1).isdigit() else str(roi or '0')
        tag = str(_value(row, 'gmgn_tags', default='') or _value(row, 'maker_token_tags', default='') or '单源')
        group = str(_value(row, 'same_source_group_id', 'group_id', default='') or 'G0')
        status = str(_value(row, 'current_status', '当前状态', default='观察') or '观察')
        risk = str(_value(row, 'risk_level', default='R0') or 'R0')
        tracking = str(_value(row, 'tracking_level', default='A1') or 'A1')
        note = template.format(symbol=symbol, roi=roi_text, tag=tag, group=group, status=zh('wallet_structure', status, status), source=zh('funding_source', str(_value(row, 'funding_source_type', default='UNKNOWN_FUND_SOURCE')), str(_value(row, 'funding_source_type', default='UNKNOWN_FUND_SOURCE'))), risk=zh('risk', risk, risk), tracking=zh('tracking', tracking, tracking), type=str(_value(row, 'address_base_type', default='wallet')))
        notes.append({
            'wallet_address': _value(row, 'wallet_address', 'address', default=''),
            'token_address': _value(row, 'token_address', default=''),
            'token_symbol': symbol,
            'role': role,
            'short_name': short_name,
            'emoji': emoji,
            'gmgn_note': note[:36],
            'note_template': template,
            'example': note,
            'max_length': 36,
            'use_case': use_case,
        })
    return notes
