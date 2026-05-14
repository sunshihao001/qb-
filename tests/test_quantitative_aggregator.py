import json
from pathlib import Path


def test_quantitative_aggregator_exports_all_intel_bot_entrypoints():
    from modules.wallet_structure import quantitative_aggregator as qa

    for name in [
        'calculate_dominant_cost_zone',
        'calculate_structure_inventory_estimate',
        'calculate_distribution_progress',
        'calculate_counterparty_pressure',
        'calculate_wallet_pattern_cost_alignment',
        'analyze_token_cluster',
        'infer_dominant_lifecycle',
        'classify_dominant_intent',
        'build_quantitative_structure_report',
        'write_quantitative_structure_report',
        'render_quantitative_structure_report_md',
    ]:
        assert hasattr(qa, name), name


def test_build_quantitative_structure_report_returns_serializable_bundle():
    from modules.wallet_structure.quantitative_aggregator import build_quantitative_structure_report
    from modules.wallet_structure.quantitative_structure_models import (
        DominantCostZoneResult,
        DistributionProgressResult,
        StructureInventoryEstimateResult,
    )

    report = build_quantitative_structure_report(
        token_address='TOKEN1',
        token_symbol='TKN',
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, current_price=1.03),
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.8),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.15),
    )

    data = report.to_dict()
    assert data['token_address'] == 'TOKEN1'
    assert data['token_symbol'] == 'TKN'
    assert data['counterparty_pressure']['counterparty_pressure_status_zh'] == '对手盘压力低'
    assert data['wallet_pattern_cost_alignment']['pattern_type_zh'] == '横盘控筹'
    assert '结构分析摘要' in data['summary_zh']
    json.dumps(data, ensure_ascii=False)


def test_write_quantitative_structure_report_keeps_outputs_under_intel_bot_logs(tmp_path):
    from modules.wallet_structure.quantitative_aggregator import build_quantitative_structure_report, write_quantitative_structure_report
    from modules.wallet_structure.quantitative_structure_models import DominantCostZoneResult

    report = build_quantitative_structure_report(
        token_address='TOKEN1',
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, current_price=1.0),
    )

    paths = write_quantitative_structure_report(report, output_root=tmp_path)

    assert paths['json'].name == 'quantitative_structure_report.json'
    assert paths['markdown'].name == 'quantitative_structure_report.md'
    assert paths['json'].is_file()
    assert paths['markdown'].is_file()
    assert paths['json'].parent == tmp_path / 'intel-bot' / 'logs' / 'quantitative_structure' / 'TOKEN1'
    assert '不输出交易动作' in paths['markdown'].read_text(encoding='utf-8')
