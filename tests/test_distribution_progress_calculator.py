
import pytest


@pytest.mark.parametrize(
    ('sold_amount', 'max_inventory', 'expected_progress', 'expected_status'),
    [
        (100, 1000, 0.10, '尚未明显派发'),
        (200, 1000, 0.20, '部分派发'),
        (350, 1000, 0.35, '部分派发'),
        (500, 1000, 0.50, '部分派发'),
        (650, 1000, 0.65, '明显派发'),
        (800, 1000, 0.80, '明显派发'),
        (900, 1000, 0.90, '接近派发完成'),
    ],
)
def test_distribution_progress_classifies_structure_side_sell_progress(sold_amount, max_inventory, expected_progress, expected_status):
    from modules.wallet_structure.distribution_progress_calculator import calculate_distribution_progress

    result = calculate_distribution_progress([
        {
            'wallet_address': 'STRUCT',
            'role_name': '疑似早期买入钱包',
            'sell_token_amount': sold_amount,
            'historical_max_balance': max_inventory,
        },
    ])

    assert result.structure_sold_pct == pytest.approx(expected_progress)
    assert result.distribution_progress_score == pytest.approx(expected_progress)
    assert result.distribution_progress_status_zh == expected_status


def test_distribution_progress_sums_only_structure_side_candidate_wallets():
    from modules.wallet_structure.distribution_progress_calculator import calculate_distribution_progress

    result = calculate_distribution_progress([
        {'wallet_address': 'EARLY', 'role_name': '疑似早期买入钱包', 'sell_token_amount': 100, 'historical_max_balance': 500},
        {'wallet_address': 'SAME', 'role_name': '疑似同源执行组成员', 'sell_token_amount': 200, 'historical_max_balance': 300},
        {'wallet_address': 'RESULT', 'role_name': '疑似结果钱包', 'sell_token_amount': 100, 'historical_max_balance': 200},
        {'wallet_address': 'BAG', 'role_name': '疑似接盘鲸鱼', 'sell_token_amount': 9999, 'historical_max_balance': 9999},
        {'wallet_address': 'RETAIL', 'role_name': '普通参与者', 'sell_token_amount': 9999, 'historical_max_balance': 9999},
    ])

    assert result.structure_sold_pct == pytest.approx(0.40)
    assert result.distribution_progress_status_zh == '部分派发'
    assert '派发进度' in result.distribution_notes_zh


def test_distribution_progress_is_unknown_without_valid_structure_max_inventory():
    from modules.wallet_structure.distribution_progress_calculator import calculate_distribution_progress

    result = calculate_distribution_progress([
        {'wallet_address': 'EARLY', 'role_name': '疑似早期买入钱包', 'sell_token_amount': 100, 'historical_max_balance': 0},
    ])

    assert result.structure_sold_pct is None
    assert result.distribution_progress_score is None
    assert result.distribution_progress_status_zh == '派发进度未知'
