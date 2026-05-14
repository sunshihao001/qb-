import json

import pytest


def test_token_cluster_analyzer_groups_same_source_distribution_and_counterparty_rows():
    from modules.wallet_structure.token_cluster_analyzer import analyze_token_cluster

    result = analyze_token_cluster([
        {'token_address': 'TOKEN1', 'wallet_address': 'A', 'role_name': '疑似同源执行组成员'},
        {'token_address': 'TOKEN1', 'wallet_address': 'B', 'role_name': '疑似分发派发钱包'},
        {'token_address': 'TOKEN1', 'wallet_address': 'C', 'role_name': '疑似接盘鲸鱼'},
        {'token_address': 'TOKEN1', 'wallet_address': 'D', 'role_name': '普通参与者'},
    ])

    assert result['token_address'] == 'TOKEN1'
    assert result['wallet_count'] == 4
    assert result['same_source_count'] == 1
    assert result['distribution_count'] == 1
    assert result['counterparty_count'] == 1
    assert result['cluster_groups']['same_source'][0]['wallet_address'] == 'A'


def test_dominant_lifecycle_infers_control_when_cost_inventory_and_pattern_align():
    from modules.wallet_structure.token_cluster_analyzer import infer_dominant_lifecycle
    from modules.wallet_structure.quantitative_structure_models import DominantCostZoneResult, DistributionProgressResult, StructureInventoryEstimateResult, WalletPatternCostAlignmentResult

    result = infer_dominant_lifecycle(
        wallet_row={'wallet_structure_status': 'WATCHING', 'wallet_structure_score': 72, 'wallet_risk_score': 20, 'counterparty_pressure_score': 10},
        dominant_cost_zone=DominantCostZoneResult(dominant_cost_mid=1.0, current_price=1.02),
        structure_inventory_estimate=StructureInventoryEstimateResult(structure_inventory_remaining_pct=0.75),
        distribution_progress=DistributionProgressResult(structure_sold_pct=0.12),
        wallet_pattern_cost_alignment=WalletPatternCostAlignmentResult(pattern_type_zh='横盘控筹'),
    )

    assert result['dominant_side_lifecycle'] == 'CONTROL_BOX_ACCUMULATION'
    assert result['dominant_side_intent'] == 'CONTROL'
    assert result['would_block_by_lifecycle'] is False
    assert result['dominant_side_confidence'] >= 0.65


def test_dominant_lifecycle_blocks_when_counterparty_pressure_is_high():
    from modules.wallet_structure.token_cluster_analyzer import infer_dominant_lifecycle

    result = infer_dominant_lifecycle(wallet_row={'wallet_structure_status': 'WATCHING', 'counterparty_pressure_score': 82})

    assert result['dominant_side_lifecycle'] == 'ACTIVE_DISTRIBUTION'
    assert result['dominant_side_intent'] == 'ACTIVE_DISTRIBUTION'
    assert result['would_block_by_lifecycle'] is True
    assert result['counterparty_state'] == 'EXIT_LIQUIDITY_FORMING'


def test_dominant_intent_uses_lifecycle_and_preserves_evidence_breakdown():
    from modules.wallet_structure.token_cluster_analyzer import classify_dominant_intent

    result = classify_dominant_intent(
        holder_cluster={'wallet_count': 4},
        wallet_behavior={'wallet_structure_status': 'WATCHING'},
        lifecycle={'dominant_side_intent': 'CONTROL', 'dominant_side_confidence': 0.72},
        cost_zone={'dominant_cost_mid': 1.0},
        inventory={'structure_inventory_remaining_pct': 0.7},
        distribution_progress={'structure_sold_pct': 0.1},
        counterparty_pressure={'counterparty_pressure_score': 20},
        pattern_alignment={'pattern_type_zh': '横盘控筹'},
    )

    assert result['dominant_intent_code'] == 'CONTROL'
    assert result['dominant_intent_confidence'] == pytest.approx(0.72)
    assert result['intent_evidence_breakdown']['holder_cluster']['wallet_count'] == 4
    assert result['conflict_notes_zh'] == '无明显冲突。'
