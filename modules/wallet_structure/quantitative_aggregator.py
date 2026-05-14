from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from .quantitative_structure_models import (
    DominantCostZoneResult,
    DistributionProgressResult,
    StructureInventoryEstimateResult,
    CounterpartyPressureResult,
    WalletPatternCostAlignmentResult,
    MarkupMotivationResult,
    QuantitativeStructureReport,
    to_plain_dict,
)
from .counterparty_pressure_calculator import calculate_counterparty_pressure
from .wallet_pattern_cost_alignment_calculator import calculate_wallet_pattern_cost_alignment
from .dominant_cost_zone_calculator import calculate_dominant_cost_zone
from .structure_inventory_calculator import calculate_structure_inventory_estimate
from .distribution_progress_calculator import calculate_distribution_progress
from .markup_motivation_calculator import calculate_markup_motivation
from .token_cluster_analyzer import analyze_token_cluster, infer_dominant_lifecycle, classify_dominant_intent


# Backward-compatible aliases so tests/documentation can import explicit names.
calculate_counterparty_pressure_quant = calculate_counterparty_pressure
calculate_wallet_pattern_cost_alignment_quant = calculate_wallet_pattern_cost_alignment


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _as_report_dict(report: QuantitativeStructureReport | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(report, QuantitativeStructureReport):
        data = report.to_dict()
    else:
        data = dict(report)
    for key in [
        'dominant_cost_zone',
        'structure_inventory_estimate',
        'distribution_progress',
        'markup_motivation',
        'counterparty_pressure',
        'wallet_pattern_cost_alignment',
    ]:
        data[key] = to_plain_dict(data.get(key))
    return data


def _summary_zh(data: Mapping[str, Any]) -> str:
    cost = data.get('dominant_cost_zone') or {}
    inv = data.get('structure_inventory_estimate') or {}
    dist = data.get('distribution_progress') or {}
    cp = data.get('counterparty_pressure') or {}
    align = data.get('wallet_pattern_cost_alignment') or {}
    return (
        '结构分析摘要：'
        f"成本区状态={cost.get('cost_position_status_zh') or cost.get('dominant_cost_deviation_status_zh') or '成本区待确认'}；"
        f"库存状态={inv.get('inventory_status_zh') or '库存状态未知'}；"
        f"派发状态={dist.get('distribution_progress_status_zh') or '派发进度未知'}；"
        f"对手盘压力={cp.get('counterparty_pressure_status_zh') or '对手盘状态未知'}；"
        f"盘型匹配={align.get('pattern_type_zh') or '匹配度未知'}。"
    )


def build_quantitative_structure_report(
    *,
    token_address: str,
    token_symbol: str = '',
    chain: str = 'sol',
    analysis_time: Optional[str] = None,
    dominant_cost_zone: Optional[DominantCostZoneResult] = None,
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None,
    distribution_progress: Optional[DistributionProgressResult] = None,
    markup_motivation: Optional[MarkupMotivationResult] = None,
    counterparty_pressure: Optional[CounterpartyPressureResult] = None,
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult] = None,
) -> QuantitativeStructureReport:
    """Build the Intel Bot quantitative report object without mutating trading state."""
    counterparty_pressure = counterparty_pressure or calculate_counterparty_pressure()
    wallet_pattern_cost_alignment = wallet_pattern_cost_alignment or calculate_wallet_pattern_cost_alignment(
        dominant_cost_zone=dominant_cost_zone,
        structure_inventory_estimate=structure_inventory_estimate,
        distribution_progress=distribution_progress,
    )
    provisional = {
        'dominant_cost_zone': to_plain_dict(dominant_cost_zone),
        'structure_inventory_estimate': to_plain_dict(structure_inventory_estimate),
        'distribution_progress': to_plain_dict(distribution_progress),
        'markup_motivation': to_plain_dict(markup_motivation),
        'counterparty_pressure': to_plain_dict(counterparty_pressure),
        'wallet_pattern_cost_alignment': to_plain_dict(wallet_pattern_cost_alignment),
    }
    return QuantitativeStructureReport(
        token_address=token_address,
        token_symbol=token_symbol,
        chain=chain,
        analysis_time=analysis_time or _utc_now(),
        summary_zh=_summary_zh(provisional),
        dominant_cost_zone=dominant_cost_zone,
        structure_inventory_estimate=structure_inventory_estimate,
        distribution_progress=distribution_progress,
        markup_motivation=markup_motivation,
        counterparty_pressure=counterparty_pressure,
        wallet_pattern_cost_alignment=wallet_pattern_cost_alignment,
    )


def render_quantitative_structure_report_md(report: QuantitativeStructureReport | Mapping[str, Any]) -> str:
    data = _as_report_dict(report)
    lines = [
        '# Intel Bot 量化结构报告',
        '',
        f"- token_address: `{data.get('token_address', '')}`",
        f"- token_symbol: `{data.get('token_symbol', '')}`",
        f"- chain: `{data.get('chain', 'sol')}`",
        f"- analysis_time: `{data.get('analysis_time', '')}`",
        '',
        '## 摘要',
        data.get('summary_zh') or _summary_zh(data),
        '',
        '## 关键对象',
    ]
    labels = [
        ('dominant_cost_zone', '主导侧成本区'),
        ('structure_inventory_estimate', '筹码库存'),
        ('distribution_progress', '派发进度'),
        ('markup_motivation', '继续推进动机'),
        ('counterparty_pressure', '对手盘压力'),
        ('wallet_pattern_cost_alignment', '钱包 × 盘型 × 成本区匹配'),
    ]
    for key, title in labels:
        lines.extend(['', f'### {title}', '```json', json.dumps(data.get(key) or {}, ensure_ascii=False, indent=2), '```'])
    lines.extend([
        '',
        '## 边界',
        '- 本报告只用于 Intel Bot 结构分析、钱包画像、筹码结构和同源/分发/接盘/结果钱包判断。',
        '- 不输出交易动作，不修改状态机，不写 PAPER_READY，不写 BLOCKED，不执行实盘。',
    ])
    return '\n'.join(lines) + '\n'


def _resolve_report_dir(*, output_root: str | Path, token_address: str) -> Path:
    root = Path(output_root)
    if root.name == 'logs' and root.parent.name == 'intel-bot':
        return root / 'quantitative_structure' / token_address
    if root.name == 'intel-bot':
        return root / 'logs' / 'quantitative_structure' / token_address
    return root / 'intel-bot' / 'logs' / 'quantitative_structure' / token_address


def write_quantitative_structure_report(
    report: QuantitativeStructureReport | Mapping[str, Any],
    *,
    output_root: str | Path = 'data/gmgn_candidates_live_run',
) -> dict[str, Path]:
    """Write report JSON/Markdown under the Intel Bot logs subtree."""
    data = _as_report_dict(report)
    token = str(data.get('token_address') or 'unknown_token')
    report_dir = _resolve_report_dir(output_root=output_root, token_address=token)
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / 'quantitative_structure_report.json'
    md_path = report_dir / 'quantitative_structure_report.md'
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    md_path.write_text(render_quantitative_structure_report_md(data), encoding='utf-8')
    return {'json': json_path, 'markdown': md_path, 'directory': report_dir}


__all__ = [
    'calculate_counterparty_pressure',
    'calculate_wallet_pattern_cost_alignment',
    'calculate_counterparty_pressure_quant',
    'calculate_wallet_pattern_cost_alignment_quant',
    'calculate_dominant_cost_zone',
    'calculate_structure_inventory_estimate',
    'calculate_distribution_progress',
    'calculate_markup_motivation',
    'analyze_token_cluster',
    'infer_dominant_lifecycle',
    'classify_dominant_intent',
    'build_quantitative_structure_report',
    'render_quantitative_structure_report_md',
    'write_quantitative_structure_report',
    'DominantCostZoneResult',
    'DistributionProgressResult',
    'StructureInventoryEstimateResult',
    'MarkupMotivationResult',
    'CounterpartyPressureResult',
    'WalletPatternCostAlignmentResult',
    'QuantitativeStructureReport',
]
