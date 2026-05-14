
import pytest


@pytest.mark.parametrize(
    ('current_inventory', 'max_inventory', 'expected_remaining_pct', 'expected_status'),
    [
        (800, 1000, 0.80, '库存充足'),
        (700, 1000, 0.70, '库存中等'),
        (500, 1000, 0.50, '库存中等'),
        (400, 1000, 0.40, '库存中等'),
        (300, 1000, 0.30, '库存偏低'),
        (200, 1000, 0.20, '库存偏低'),
        (100, 1000, 0.10, '库存接近出清'),
    ],
)
def test_structure_inventory_remaining_ratio_classifies_chip_control_capacity(current_inventory, max_inventory, expected_remaining_pct, expected_status):
    from modules.wallet_structure.structure_inventory_calculator import calculate_structure_inventory_estimate

    result = calculate_structure_inventory_estimate([
        {
            'wallet_address': 'STRUCT',
            'role_name': '疑似早期买入钱包',
            'current_balance': current_inventory,
            'historical_max_balance': max_inventory,
        },
    ])

    assert result.structure_current_inventory == pytest.approx(current_inventory)
    assert result.structure_max_inventory == pytest.approx(max_inventory)
    assert result.structure_inventory_remaining_pct == pytest.approx(expected_remaining_pct)
    assert result.inventory_status_zh == expected_status


def test_structure_inventory_estimate_sums_only_structure_side_candidate_wallets():
    from modules.wallet_structure.structure_inventory_calculator import calculate_structure_inventory_estimate

    result = calculate_structure_inventory_estimate([
        {'wallet_address': 'EARLY', 'role_name': '疑似早期买入钱包', 'current_balance': 300, 'historical_max_balance': 500},
        {'wallet_address': 'SAME', 'role_name': '疑似同源执行组成员', 'current_balance': 200, 'historical_max_balance': 300},
        {'wallet_address': 'RESULT', 'role_name': '疑似结果钱包', 'current_balance': 100, 'historical_max_balance': 200},
        {'wallet_address': 'BAG', 'role_name': '疑似接盘鲸鱼', 'current_balance': 9999, 'historical_max_balance': 9999},
        {'wallet_address': 'RETAIL', 'role_name': '普通参与者', 'current_balance': 9999, 'historical_max_balance': 9999},
    ])

    assert result.structure_current_inventory == pytest.approx(600)
    assert result.structure_max_inventory == pytest.approx(1000)
    assert result.structure_inventory_remaining_pct == pytest.approx(0.60)
    assert result.inventory_status_zh == '库存中等'
    assert '结构侧未派发库存比例' in result.inventory_notes_zh


def test_structure_inventory_estimate_is_unknown_without_valid_max_inventory():
    from modules.wallet_structure.structure_inventory_calculator import calculate_structure_inventory_estimate

    result = calculate_structure_inventory_estimate([
        {'wallet_address': 'EARLY', 'role_name': '疑似早期买入钱包', 'current_balance': 100, 'historical_max_balance': 0},
    ])

    assert result.structure_current_inventory == pytest.approx(100)
    assert result.structure_max_inventory == 0
    assert result.structure_inventory_remaining_pct is None
    assert result.inventory_status_zh == '库存状态未知'
