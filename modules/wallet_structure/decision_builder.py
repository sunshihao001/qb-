from __future__ import annotations

import csv
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from .constants import OUTPUT_FILENAMES, SCHEMA_VERSION
from .chinese_judgement import zh
from .edge_builder import build_wallet_edges
from .note_generator import generate_gmgn_notes
from .role_classifier import classify_wallet_rows
from .normalizer import normalize_wallet_rows
from .source_reader import collect_wallet_snapshot, write_raw_snapshot_csv

def _as_dict(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, Mapping):
        return dict(obj)
    return dict(obj.__dict__) if hasattr(obj, '__dict__') else {}

def _read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return [dict(row) for row in csv.DictReader(f)]

def _write_csv_rows(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    rows = [dict(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def _decision_from_rows(normalized_rows: List[Dict[str, Any]], classified_rows: List[Dict[str, Any]], edges: Dict[str, List[Dict[str, Any]]], request: Mapping[str, Any], source_meta: Mapping[str, Any], notes_path: str = '') -> Dict[str, Any]:
    try:
        from sikk_wallet_structure_gate import evaluate_wallet_structure_gate
    except Exception as exc:
        raise RuntimeError(f'legacy wallet gate unavailable: {exc}')
    decision_obj = evaluate_wallet_structure_gate(
        token=request.get('token_address', ''),
        symbol=request.get('token_symbol', ''),
        wallet_rows=classified_rows or normalized_rows,
        candidate_groups=edges.get('same_source_groups', []),
    )
    decision = decision_obj.to_dict() if hasattr(decision_obj, 'to_dict') else _as_dict(decision_obj)
    status = str(decision.get('wallet_structure_status') or decision.get('wallet_structure_status') or 'WALLET_UNKNOWN')
    risk_score = float(decision.get('wallet_risk_score', 0) or 0)
    counterparty = float(decision.get('counterparty_pressure_score', 0) or 0)
    source_rows = list(source_meta.get('rows') or []) if isinstance(source_meta, Mapping) else []
    support = []
    pause = []
    block = []
    for reason in decision.get('reasons', []) or []:
        text = str(reason)
        if '阻断' in text or '清仓' in text or '失效' in text:
            block.append(text)
        elif '暂停' in text or '不足' in text or '复核' in text or '降级' in text:
            pause.append(text)
        else:
            support.append(text)
    if status == 'WALLET_SUPPORT' and not support:
        support.append('结构侧支持信号占优')
    if status in {'WALLET_PAUSE', 'WALLET_UNKNOWN'} and not pause:
        pause.append('结构证据不足或数据质量不足')
    if status == 'WALLET_BLOCK' and not block:
        block.append('结构侧强阻断条件触发')
    core_wallet_candidates = [r for r in classified_rows if r.get('role_name') in {'疑似结果钱包', '疑似新钱包狙击', '疑似临时执行钱包', '疑似同源执行组成员'}][:10]
    high_risk_wallets = [r for r in classified_rows if r.get('risk_level') in {'R3', 'R4'}][:10]
    note_file = str(source_meta.get('gmgn_note_table_csv', ''))
    same_source_count = len(edges.get('same_source_groups', []))
    backflow = bool(edges.get('backflow_paths'))
    dist_level = 'HIGH' if status == 'WALLET_BLOCK' or backflow else ('MEDIUM' if same_source_count else 'LOW')
    dominant_side = _dominant_side(classified_rows, decision)
    chip_status = 'CHIP_TOWARD_COUNTERPARTY' if backflow or any(r.get('role_name') == '疑似分发派发钱包' for r in classified_rows) else 'CHIP_RETAINED'
    evidence_chain = _build_evidence_chain(classified_rows, normalized_rows, decision, edges)
    evidence_packet = _build_evidence_packet(
        request=request,
        source_rows=source_rows,
        normalized_rows=normalized_rows,
        classified_rows=classified_rows,
        edges=edges,
        evidence_chain=evidence_chain,
        decision=decision,
    )
    return {
        'token_address': request.get('token_address', ''),
        'token_symbol': request.get('token_symbol', ''),
        'chain': request.get('chain', 'sol'),
        'analysis_time': request.get('analysis_time', ''),
        'wallet_structure_status': status,
        'wallet_structure_status_zh': zh('wallet_structure', status, status),
        'wallet_structure_score': decision.get('wallet_structure_score', 0),
        'wallet_risk_score': risk_score,
        'wallet_risk_level_zh': zh('risk', 'HIGH_RISK' if risk_score >= 70 else 'MEDIUM_RISK' if risk_score >= 35 else 'LIGHT_OBSERVATION' if status == 'WALLET_PAUSE' else 'LOW_RISK', ''),
        'wallet_structure_factor': decision.get('wallet_structure_factor', 1.0),
        # 下列字段仅为旧交易/状态机消费者保留的兼容字段，不属于 Intel Bot 用户可见结论。
        'dominant_side_status': dominant_side,
        'dominant_side_status_zh': '仅供下游模型参考，不由钱包证据包直接裁决',
        'chip_transfer_status': chip_status,
        'chip_transfer_status_zh': '仅保留候选筹码流向证据，不判断派发是否完成',
        'counterparty_pressure_score': counterparty,
        'same_source_group_count': same_source_count,
        'distribution_risk_level': dist_level,
        'distribution_risk_level_zh': '高风险' if dist_level == 'HIGH' else '中度风险' if dist_level == 'MEDIUM' else '低风险',
        'backflow_detected': backflow,
        'core_wallet_candidates': core_wallet_candidates,
        'high_risk_wallets': high_risk_wallets,
        'gmgn_note_file': note_file,
        'bot_scope': 'WALLET_EVIDENCE_PACKET_ONLY',
        'bot_scope_zh': '钱包证据包采集与标准化，不直接判断主导侧动机、对手盘压力或派发完成',
        'evidence_packet': evidence_packet,
        'evidence_chain': evidence_chain,
        'blocking_reasons': block,
        'pause_reasons': pause,
        'supporting_reasons': support,
        'recommended_state_action': _recommended_action(status, risk_score, counterparty, backflow),
        'recommended_state_action_zh': zh('action', _recommended_action(status, risk_score, counterparty, backflow), _recommended_action(status, risk_score, counterparty, backflow)),
        'wallet_evidence_level': decision.get('wallet_evidence_level', 'E0'),
        'wallet_evidence_level_zh': zh('evidence', decision.get('wallet_evidence_level', 'E0'), decision.get('wallet_evidence_level', 'E0')),
        'data_quality_score': decision.get('data_quality_score', 0),
        'data_quality_status': decision.get('data_quality_status', 'UNKNOWN'),
        'data_quality_status_zh': zh('time', 'NEED_REFRESH' if decision.get('data_quality_status', 'UNKNOWN') == 'DEGRADED' else 'TIME_UNKNOWN', decision.get('data_quality_status', 'UNKNOWN')),
        'wallet_gate_result': decision.get('wallet_gate_result', ''),
        'wallet_gate_result_zh': zh('gate', 'ALLOW_PAPER_READY' if status == 'WALLET_SUPPORT' else 'PAUSE_FOR_CONFIRMATION' if status == 'WALLET_PAUSE' else 'BLOCK', ''),
        'paper_gate_effect': decision.get('paper_gate_effect', ''),
        'reason_codes': decision.get('reason_codes', []),
        'decision_meta': {
            'schema_version': SCHEMA_VERSION,
            'source_rows': len(classified_rows),
            'source_files': source_meta,
        },
        'wallet_structure_reason': '；'.join(decision.get('reasons', []) or []),
        'wallet_structure_reason_zh': '；'.join(decision.get('reasons', []) or []) or zh('wallet_structure', status, status),
        'decision_at': decision.get('decision_at', ''),
    }

def _first_present(row: Mapping[str, Any], keys: Sequence[str], default: Any = '') -> Any:
    for key in keys:
        value = row.get(key)
        if value not in (None, '', [], {}):
            return value
    return default

def _count_present(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> int:
    return sum(1 for row in rows if _first_present(row, keys, '') not in (None, '', [], {}))


def _num_value(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, '', [], {}):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _int_value(value: Any, default: int = 0) -> int:
    return int(_num_value(value, float(default)))


def build_holder_snapshot_normalized(*, request: Mapping[str, Any], source_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    snapshot_time = str(request.get('analysis_time') or request.get('snapshot_time') or request.get('discovery_time') or '')
    rows: List[Dict[str, Any]] = []
    for idx, row in enumerate(source_rows, start=1):
        wallet_address = _first_present(row, ['wallet_address', 'address', 'holder_address', 'owner', '钱包地址'], '')
        holding_pct = _num_value(_first_present(row, ['holding_pct', 'amount_percentage', 'hold_pct', 'percentage'], 0), 0)
        item = {
            'token_address': request.get('token_address', '') or _first_present(row, ['token_address'], ''),
            'snapshot_time': _first_present(row, ['snapshot_time', 'updated_at', 'source_time'], snapshot_time),
            'holder_rank': _int_value(_first_present(row, ['holder_rank', 'rank'], idx), idx),
            'wallet_address': wallet_address,
            'holding_amount': _num_value(_first_present(row, ['holding_amount', 'amount', 'balance', 'token_amount'], 0), 0),
            'holding_pct': holding_pct,
            'holding_value_usd': _num_value(_first_present(row, ['holding_value_usd', 'usd_value', 'value_usd', 'holding_usd'], 0), 0),
            'top10_holder_pct': _num_value(_first_present(row, ['top10_holder_pct', 'top_10_holder_rate', 'top10_holder_rate'], 0), 0),
            'top20_holder_pct': _num_value(_first_present(row, ['top20_holder_pct', 'top_20_holder_rate', 'top20_holder_rate'], 0), 0),
            'holder_count': _int_value(_first_present(row, ['holder_count', 'holders', 'holder_num'], 0), 0),
            'holder_delta': _int_value(_first_present(row, ['holder_delta', 'holder_count_delta'], 0), 0),
        }
        missing = [key for key in ['token_address', 'snapshot_time', 'wallet_address'] if item.get(key) in (None, '', [], {})]
        item['source_trace'] = {
            'gmgn_holder': 'gmgn-cli token holders',
            'onchain_holder_snapshot': str(_first_present(row, ['onchain_source', 'snapshot_source'], '')),
            'kryptogo_or_cluster_source': str(_first_present(row, ['cluster_source', 'kryptogo_source'], '')),
        }
        item['field_quality'] = {
            'missing_required_fields': missing,
            'holder_snapshot_status': 'Holder 快照字段完整' if not missing else 'Holder 快照字段缺失',
        }
        rows.append(item)
    rows.sort(key=lambda r: (r.get('holder_rank') or 0, -_num_value(r.get('holding_pct'), 0)))
    return rows


def build_wallet_structure_normalized(*, request: Mapping[str, Any], holder_rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    rows = list(holder_rows)
    top10 = _num_value(rows[0].get('top10_holder_pct') if rows else 0, 0)
    top20 = _num_value(rows[0].get('top20_holder_pct') if rows else 0, 0)
    if not top10:
        top10 = sum(_num_value(r.get('holding_pct'), 0) for r in rows[:10])
    if not top20:
        top20 = sum(_num_value(r.get('holding_pct'), 0) for r in rows[:20])
    return {
        'schema_version': 'sikk_holder_wallet_structure_normalized_v1',
        'token_address': request.get('token_address', ''),
        'snapshot_time': rows[0].get('snapshot_time', '') if rows else str(request.get('analysis_time') or ''),
        'holder_metrics': {
            'holder_count': _int_value(rows[0].get('holder_count') if rows else 0, 0),
            'holder_delta': _int_value(rows[0].get('holder_delta') if rows else 0, 0),
            'top10_holder_pct': top10,
            'top20_holder_pct': top20,
            'top_holder_count': len(rows),
            'top_holder_total_pct': sum(_num_value(r.get('holding_pct'), 0) for r in rows),
        },
        'intel_bot_usage_zh': ['结构侧剩余库存', 'Top Holder 稳定性', '对手盘承接', '筹码迁移'],
        'scope_limits_zh': [
            '本文件只提供 Holder 快照和钱包结构事实层',
            '不直接判断主导侧动机、对手盘压力或派发是否完成',
            '不输出确定庄家，不触发交易',
        ],
        'holders': rows,
    }


def _build_evidence_packet(
    *,
    request: Mapping[str, Any],
    source_rows: List[Dict[str, Any]],
    normalized_rows: List[Dict[str, Any]],
    classified_rows: List[Dict[str, Any]],
    edges: Dict[str, List[Dict[str, Any]]],
    evidence_chain: List[Dict[str, Any]],
    decision: Mapping[str, Any],
) -> Dict[str, Any]:
    row_count = len(normalized_rows)
    raw_count = len(source_rows)
    role_counts: Dict[str, int] = {}
    evidence_counts: Dict[str, int] = {}
    risk_counts: Dict[str, int] = {}
    for row in classified_rows:
        role_counts[str(row.get('role_name') or '角色未知')] = role_counts.get(str(row.get('role_name') or '角色未知'), 0) + 1
        evidence_counts[str(row.get('evidence_level') or 'E0')] = evidence_counts.get(str(row.get('evidence_level') or 'E0'), 0) + 1
        risk_counts[str(row.get('risk_level') or 'R0')] = risk_counts.get(str(row.get('risk_level') or 'R0'), 0) + 1
    time_keys = ['wallet_source_time', 'source_time', 'snapshot_time', 'updated_at', 'last_seen_at', '首次买入时间', 'first_buy_time', 'start_holding_at', 'last_active_timestamp']
    address_keys = ['wallet_address', 'address', '钱包地址']
    token_source_keys = ['token_source_address', 'token_transfer_in.address', 'token_transfer_in', 'current_transfer_in_amount', 'history_transfer_in_amount']
    funding_keys = ['funding_source_address', 'native_transfer.from_address', 'native_transfer', 'funding_source_type']
    pnl_keys = ['profit', 'pnl', 'total_profit', 'realized_profit', 'unrealized_profit']
    tag_keys = ['gmgn_tags', 'tags', 'maker_token_tags', 'wallet_tag_v2']
    same_source_count = len(edges.get('same_source_groups') or [])
    return {
        'packet_type': 'wallet_structure_evidence_packet',
        'packet_type_zh': '钱包结构证据包',
        'scope_limits_zh': [
            '只负责采集、清洗、时间对齐、字段标准化和来源追踪',
            '只输出疑似结构角色，不输出确定庄家',
            '不直接判断主导侧动机、对手盘压力或派发是否完成',
            '所有结论必须回指原始字段、规则依据、证据等级和风险等级',
        ],
        'token_address': request.get('token_address', ''),
        'token_symbol': request.get('token_symbol', ''),
        'chain': request.get('chain', 'sol'),
        'time_alignment': {
            'analysis_time': request.get('analysis_time'),
            'discovery_time': request.get('discovery_time'),
            'analysis_window': request.get('analysis_window', 'CUSTOM'),
            'source_time_field_candidates': time_keys,
            'rows_with_source_time': _count_present(normalized_rows, time_keys),
            'time_alignment_status_zh': '时间字段已保留但需要源数据补齐' if _count_present(normalized_rows, time_keys) < row_count else '时间字段覆盖完整',
        },
        'field_coverage': {
            'raw_wallet_rows': raw_count,
            'standardized_wallet_rows': row_count,
            'classified_wallet_rows': len(classified_rows),
            'rows_with_address': _count_present(normalized_rows, address_keys),
            'rows_with_gmgn_tags': _count_present(normalized_rows, tag_keys),
            'rows_with_pnl': _count_present(normalized_rows, pnl_keys),
            'rows_with_token_source': _count_present(normalized_rows, token_source_keys),
            'rows_with_funding_source': _count_present(normalized_rows, funding_keys),
            'same_source_group_count': same_source_count,
            'funding_edge_count': len(edges.get('wallet_funding_edges') or []),
            'token_flow_edge_count': len(edges.get('wallet_token_flow_edges') or []),
        },
        'address_evidence_summary': {
            'role_counts': role_counts,
            'evidence_level_counts': evidence_counts,
            'risk_level_counts': risk_counts,
        },
        'evidence_files': {
            'raw_snapshot': 'wallet_raw_snapshot.csv',
            'standardized_wallets': 'wallet_normalized.csv',
            'role_candidates': 'wallet_role_classification.csv',
            'funding_edges': 'wallet_funding_edges.csv',
            'token_flow_edges': 'wallet_token_flow_edges.csv',
            'same_source_groups': 'same_source_groups.csv',
            'gmgn_notes': 'gmgn_note_table.csv',
        },
        'traceability': evidence_chain,
        'legacy_gate_observation': {
            'status': decision.get('wallet_structure_status', ''),
            'status_zh': zh('wallet_structure', str(decision.get('wallet_structure_status') or 'WALLET_UNKNOWN'), ''),
            'data_quality_score': decision.get('data_quality_score', 0),
            'evidence_level': decision.get('wallet_evidence_level', 'E0'),
            'note_zh': '此项仅作为证据包质量观察，不作为 Bot 对主导侧/派发/对手盘的裁决。',
        },
    }

def _dominant_side(classified_rows: List[Dict[str, Any]], decision: Mapping[str, Any]) -> str:
    counts = {}
    for row in classified_rows:
        role = str(row.get('role_name') or '普通参与者')
        counts[role] = counts.get(role, 0) + 1
    if counts.get('疑似分发派发钱包', 0) or counts.get('疑似接盘鲸鱼', 0):
        return 'DISTRIBUTION_SIDE'
    if counts.get('疑似结果钱包', 0) or counts.get('疑似同源执行组成员', 0):
        return 'STRUCTURE_SIDE'
    if decision.get('wallet_structure_status') == 'WALLET_BLOCK':
        return 'COUNTERPARTY_SIDE'
    return 'UNKNOWN_SIDE'

def _recommended_action(status: str, risk_score: float, counterparty: float, backflow: bool) -> str:
    if status == 'WALLET_BLOCK' or backflow or risk_score >= 70 or counterparty >= 70:
        return 'BLOCK_TRADE_FLOW'
    if status == 'WALLET_PAUSE':
        return 'PAUSE_FOR_REFRESH'
    if status == 'WALLET_SUPPORT':
        return 'ENTER_NEXT_GATE'
    return 'WATCH'

def _build_evidence_chain(classified_rows: List[Dict[str, Any]], normalized_rows: List[Dict[str, Any]], decision: Mapping[str, Any], edges: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    chain: List[Dict[str, Any]] = []
    for row in classified_rows[:8]:
        chain.append({
            'field': 'role_name',
            'value': row.get('role_name'),
            'source': 'wallet_role_classification.csv',
            'rule': f"role={row.get('role_code')}",
            'meaning': row.get('gmgn_note', ''),
        })
    for edge in (edges.get('wallet_funding_edges') or [])[:5]:
        chain.append({
            'field': 'funding_source_address',
            'value': edge.get('source_address'),
            'source': 'wallet_funding_edges.csv',
            'rule': 'native funding source edge',
            'meaning': edge.get('role_name', ''),
        })
    for edge in (edges.get('wallet_token_flow_edges') or [])[:5]:
        chain.append({
            'field': 'token_flow',
            'value': f"{edge.get('from_address')}→{edge.get('to_address')}",
            'source': 'wallet_token_flow_edges.csv',
            'rule': edge.get('edge_type', ''),
            'meaning': edge.get('role_name', ''),
        })
    chain.append({
        'field': 'wallet_structure_status',
        'value': decision.get('wallet_structure_status', ''),
        'source': 'wallet_structure_decision.json',
        'rule': 'legacy gate summary',
        'meaning': decision.get('wallet_structure_reason', ''),
    })
    return chain

def _decision_rows(decision: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return [dict(decision)]

def _report_md(decision: Mapping[str, Any], normalized_rows: List[Dict[str, Any]], classified_rows: List[Dict[str, Any]], edges: Dict[str, List[Dict[str, Any]]]) -> str:
    packet = decision.get('evidence_packet') or {}
    coverage = packet.get('field_coverage') or {}
    time_alignment = packet.get('time_alignment') or {}
    lines = [
        '# SIKK 钱包结构证据包',
        '',
        f"- 代币地址：{decision.get('token_address', '')}",
        f"- 代币符号：{decision.get('token_symbol', '')}",
        f"- Bot 边界：{decision.get('bot_scope_zh', '只输出钱包证据包')}",
        f"- 标准化钱包行数：{coverage.get('standardized_wallet_rows', len(normalized_rows))}",
        f"- 原始钱包行数：{coverage.get('raw_wallet_rows', 0)}",
        f"- 地址字段覆盖：{coverage.get('rows_with_address', 0)}",
        f"- GMGN 标签覆盖：{coverage.get('rows_with_gmgn_tags', 0)}",
        f"- 盈亏字段覆盖：{coverage.get('rows_with_pnl', 0)}",
        f"- Token 来源字段覆盖：{coverage.get('rows_with_token_source', 0)}",
        f"- 资金来源字段覆盖：{coverage.get('rows_with_funding_source', 0)}",
        f"- 同源组数量：{coverage.get('same_source_group_count', decision.get('same_source_group_count', 0))}",
        f"- 时间对齐状态：{time_alignment.get('time_alignment_status_zh', '时间字段待补')}",
        '',
        '## 边界说明',
        '- 本 Bot 不输出“确定庄家”。',
        '- 本 Bot 不直接判断主导侧动机、对手盘压力或派发是否完成。',
        '- 本 Bot 只把 GMGN / OKX / 链上钱包数据整理成可追踪证据包。',
        '',
        '## 证据包质量观察',
        f"- 钱包结构观察：{decision.get('wallet_structure_status_zh', decision.get('wallet_structure_status', ''))}",
        f"- 证据等级：{decision.get('wallet_evidence_level_zh', decision.get('wallet_evidence_level', ''))}",
        f"- 数据质量：{decision.get('data_quality_status_zh', decision.get('data_quality_status', ''))}",
        '',
        '## 角色明细',
    ]
    for row in classified_rows[:10]:
        lines.append(f"- {row.get('wallet_address', '')}：{row.get('role_name', '')} / {zh('evidence', row.get('evidence_level', 'E0'), row.get('evidence_level', 'E0'))} / {zh('risk', row.get('risk_level', 'R0'), row.get('risk_level', 'R0'))}")
    return '\n'.join(lines) + '\n'

def write_wallet_structure_bundle(
    *,
    request: Mapping[str, Any],
    output_dir: str | Path,
    normalized_rows: List[Dict[str, Any]],
    classified_rows: List[Dict[str, Any]],
    edges: Dict[str, List[Dict[str, Any]]],
    decision: Mapping[str, Any],
    source_rows: List[Dict[str, Any]],
    notes: List[Dict[str, Any]],
) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_csv = out / 'wallet_raw_snapshot.csv'
    normalized_csv = out / 'wallet_normalized.csv'
    classification_csv = out / 'wallet_role_classification.csv'
    funding_edges_csv = out / 'wallet_funding_edges.csv'
    token_flow_edges_csv = out / 'wallet_token_flow_edges.csv'
    same_source_groups_csv = out / 'same_source_groups.csv'
    distribution_paths_csv = out / 'distribution_paths.csv'
    backflow_paths_csv = out / 'backflow_paths.csv'
    gmgn_note_table_csv = out / 'gmgn_note_table.csv'
    decision_json = out / 'wallet_structure_decision.json'
    report_md = out / 'wallet_structure_report.md'
    manifest_json = out / 'bundle_manifest.json'
    holder_snapshot_normalized_json = out / 'holder_snapshot_normalized.json'
    wallet_structure_normalized_json = out / 'wallet_structure_normalized.json'

    holder_snapshot_rows = build_holder_snapshot_normalized(request=request, source_rows=source_rows)
    wallet_structure_normalized = build_wallet_structure_normalized(request=request, holder_rows=holder_snapshot_rows)

    write_raw_snapshot_csv(raw_csv, source_rows)
    _write_csv_rows(normalized_csv, normalized_rows)
    _write_csv_rows(classification_csv, classified_rows)
    _write_csv_rows(funding_edges_csv, edges.get('wallet_funding_edges', []))
    _write_csv_rows(token_flow_edges_csv, edges.get('wallet_token_flow_edges', []))
    _write_csv_rows(same_source_groups_csv, edges.get('same_source_groups', []))
    _write_csv_rows(distribution_paths_csv, edges.get('distribution_paths', []))
    _write_csv_rows(backflow_paths_csv, edges.get('backflow_paths', []))
    _write_csv_rows(gmgn_note_table_csv, notes)
    holder_snapshot_normalized_json.write_text(json.dumps(holder_snapshot_rows, ensure_ascii=False, indent=2), encoding='utf-8')
    wallet_structure_normalized_json.write_text(json.dumps(wallet_structure_normalized, ensure_ascii=False, indent=2), encoding='utf-8')
    decision_payload = dict(decision)
    decision_payload['gmgn_note_file'] = str(gmgn_note_table_csv)
    decision_payload['decision_schema_version'] = SCHEMA_VERSION
    decision_json.write_text(json.dumps(decision_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    report_md.write_text(_report_md(decision_payload, normalized_rows, classified_rows, edges), encoding='utf-8')
    manifest = {
        'token_address': request.get('token_address', ''),
        'token_symbol': request.get('token_symbol', ''),
        'chain': request.get('chain', 'sol'),
        'analysis_time': request.get('analysis_time', ''),
        'schema_version': SCHEMA_VERSION,
        'files': {
            'wallet_raw_snapshot.csv': str(raw_csv),
            'wallet_normalized.csv': str(normalized_csv),
            'wallet_role_classification.csv': str(classification_csv),
            'wallet_funding_edges.csv': str(funding_edges_csv),
            'wallet_token_flow_edges.csv': str(token_flow_edges_csv),
            'same_source_groups.csv': str(same_source_groups_csv),
            'distribution_paths.csv': str(distribution_paths_csv),
            'backflow_paths.csv': str(backflow_paths_csv),
            'gmgn_note_table.csv': str(gmgn_note_table_csv),
            'holder_snapshot_normalized.json': str(holder_snapshot_normalized_json),
            'wallet_structure_normalized.json': str(wallet_structure_normalized_json),
            'wallet_structure_decision.json': str(decision_json),
            'wallet_structure_report.md': str(report_md),
        },
        'wallet_structure_decision': decision_payload,
    }
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return {
        'wallet_raw_snapshot_csv': str(raw_csv),
        'wallet_normalized_csv': str(normalized_csv),
        'wallet_role_classification_csv': str(classification_csv),
        'wallet_funding_edges_csv': str(funding_edges_csv),
        'wallet_token_flow_edges_csv': str(token_flow_edges_csv),
        'same_source_groups_csv': str(same_source_groups_csv),
        'distribution_paths_csv': str(distribution_paths_csv),
        'backflow_paths_csv': str(backflow_paths_csv),
        'gmgn_note_table_csv': str(gmgn_note_table_csv),
        'holder_snapshot_normalized_json': str(holder_snapshot_normalized_json),
        'wallet_structure_normalized_json': str(wallet_structure_normalized_json),
        'wallet_structure_decision_json': str(decision_json),
        'wallet_structure_report_md': str(report_md),
        'bundle_manifest_json': str(manifest_json),
    }

def build_wallet_structure_decision(request: Mapping[str, Any], normalized_rows: List[Dict[str, Any]], classified_rows: List[Dict[str, Any]], edges: Dict[str, List[Dict[str, Any]]], source_meta: Mapping[str, Any], notes_path: str = '') -> Dict[str, Any]:
    return _decision_from_rows(normalized_rows, classified_rows, edges, request, source_meta, notes_path=notes_path)

def build_bundle_from_request(request: Mapping[str, Any], collector=None, output_dir: str | Path = '') -> Dict[str, str]:
    from .normalizer import normalize_wallet_rows
    from .role_classifier import classify_wallet_rows
    from .edge_builder import build_wallet_edges
    from .note_generator import generate_gmgn_notes
    from .source_reader import collect_wallet_snapshot, default_gmgn_wallet_collector

    collector = collector or default_gmgn_wallet_collector
    payload = collect_wallet_snapshot(request, collector=collector)
    source_rows = list(payload.get('rows', []))
    normalized_rows = normalize_wallet_rows(source_rows, token_address=request.get('token_address', ''), token_symbol=request.get('token_symbol', ''), chain=request.get('chain', 'sol'))
    classified_rows = classify_wallet_rows(normalized_rows)
    edges = build_wallet_edges(classified_rows)
    notes = generate_gmgn_notes(classified_rows)
    decision = build_wallet_structure_decision(request, normalized_rows, classified_rows, edges, payload, notes_path='')
    out_dir = Path(output_dir) if output_dir else Path('data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure') / request.get('token_address', 'unknown')
    return write_wallet_structure_bundle(
        request=request,
        output_dir=out_dir,
        normalized_rows=normalized_rows,
        classified_rows=classified_rows,
        edges=edges,
        decision=decision,
        source_rows=source_rows,
        notes=notes,
    )
