
import pytest


def test_active_buy_wallet_cost_uses_total_buy_usd_over_token_amount():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_wallet_cost

    result = calculate_wallet_cost({
        'wallet_address': 'W_ACTIVE',
        'token_address': 'TokenCost',
        'buy_amount_usd': 1200,
        'buy_token_amount': 300,
        'first_buy_time': '2026-05-05T00:00:00Z',
        'buy_count': 2,
        'sell_amount_usd': 100,
        'sell_token_amount': 20,
        'current_balance': 280,
    })

    assert result.wallet_avg_cost == pytest.approx(4.0)
    assert result.wallet_first_buy_cost == pytest.approx(4.0)
    assert result.wallet_last_buy_cost == pytest.approx(4.0)
    assert result.wallet_cost_confidence > 0
    assert result.wallet_cost_status_zh == '成本可由主动买入估算'
    assert result.cost_source_type_zh == '主动买入成本'


def test_token_transfer_wallet_cost_is_not_confirmed_from_transfer_price():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_wallet_cost

    result = calculate_wallet_cost({
        'wallet_address': 'W_TRANSFER',
        'token_address': 'TokenCost',
        'transfer_in': True,
        'token_source_address': 'SRC',
        'current_balance': 1000,
    })

    assert result.wallet_avg_cost is None
    assert result.wallet_cost_confidence == 0
    assert result.wallet_cost_status_zh == '成本不可直接确认'
    assert result.cost_source_type_zh in {'Token 转入成本未知', '分发接收成本未知'}
    assert '不能直接' in result.wallet_cost_notes_zh or '不能由转入价格确认' in result.wallet_cost_notes_zh


def test_distribution_receiver_wallet_cost_must_be_unknown():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_wallet_cost

    result = calculate_wallet_cost({
        'wallet_address': 'W_RECV',
        'token_address': 'TokenCost',
        'role_name': '疑似 Token 接收钱包',
        'transfer_in': True,
        'token_source_address': 'SRC',
        'current_balance': 800,
    })

    assert result.wallet_avg_cost is None
    assert result.wallet_cost_confidence == 0
    assert result.wallet_cost_status_zh == '成本不可直接确认'
    assert result.cost_source_type_zh == '分发接收成本未知'


def test_dominant_cost_zone_only_uses_active_buy_costs():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'buy_count': 1},
            {'wallet_address': 'W2', 'token_address': 'T', 'buy_amount_usd': 300, 'buy_token_amount': 100, 'buy_count': 2},
            {'wallet_address': 'W3', 'token_address': 'T', 'transfer_in': True, 'token_source_address': 'SRC', 'current_balance': 999999},
        ],
        same_source_groups=[],
        current_price=4.0,
    )

    assert result.dominant_cost_low == pytest.approx(1.0)
    assert result.dominant_cost_high == pytest.approx(3.0)
    assert result.dominant_cost_mid == pytest.approx(2.0)
    assert result.price_to_dominant_cost_pct == pytest.approx(100.0)
    assert result.cost_position_status_zh == '当前价格大幅高于主导侧成本区'
    assert len(result.wallet_costs) == 3
    assert result.wallet_costs[2].wallet_cost_status_zh == '成本不可直接确认'


def test_same_source_group_cost_uses_group_active_buy_totals_and_quartiles():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'G1A', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似临时执行钱包'},
            {'wallet_address': 'G1B', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 300, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似同源执行组成员'},
            {'wallet_address': 'G1C', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 500, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似核心资金源候选'},
            {'wallet_address': 'G1D', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 700, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似结果钱包'},
            {'wallet_address': 'OUT', 'token_address': 'T', 'same_source_group_id': 'G2', 'buy_amount_usd': 900, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似接盘鲸鱼'},
            {'wallet_address': 'G1X', 'token_address': 'T', 'same_source_group_id': 'G1', 'transfer_in': True, 'token_source_address': 'SRC', 'current_balance': 999999, 'role_name': '疑似 Token 接收钱包'},
            {'wallet_address': 'G1Y', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 900, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '疑似接盘鲸鱼'},
            {'wallet_address': 'G1Z', 'token_address': 'T', 'same_source_group_id': 'G1', 'buy_amount_usd': 1100, 'buy_token_amount': 100, 'buy_count': 1, 'role_name': '普通参与者'},
        ],
        same_source_groups=[{'group_id': 'G1', 'wallet_addresses': ['G1A', 'G1B', 'G1C', 'G1D', 'G1X', 'G1Y', 'G1Z']}],
        current_price=6.0,
    )

    # 只纳入早期买入、临时执行、同源组成员、核心持有、结果仍持有；排除接盘鲸鱼、普通散户、token 转入钱包
    assert result.same_source_group_cost_mid == pytest.approx(4.0)
    assert result.same_source_group_cost_low == pytest.approx(2.5)
    assert result.same_source_group_cost_high == pytest.approx(5.5)
    assert result.same_source_group_cost_confidence is not None
    assert result.same_source_group_cost_confidence > 0.7
    assert result.dominant_cost_mid == pytest.approx(4.0)
    assert result.dominant_cost_low_zh == pytest.approx(1.0)
    assert result.dominant_cost_mid_zh == pytest.approx(4.0)
    assert result.dominant_cost_high_zh == pytest.approx(7.0)
    assert result.dominant_cost_confidence_zh is not None
    assert result.dominant_cost_confidence_zh > 0.7


def test_market_cost_proxy_outputs_market_box_and_volume_dense_zone_aliases():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'role_name': '疑似早期买入钱包'},
            {'wallet_address': 'W2', 'token_address': 'T', 'buy_amount_usd': 300, 'buy_token_amount': 100, 'role_name': '疑似同源执行组成员'},
        ],
        same_source_groups=[],
        current_price=4.0,
        market_structure={
            'POC_price': 2.4,
            'VAH_price': 3.0,
            'VAL_price': 1.8,
            'latest_AVWAP': 2.2,
        },
    )

    assert result.market_cost_mid == pytest.approx(2.3333333333)
    assert result.market_cost_mid_zh == pytest.approx(2.3333333333)
    assert result.box_cost_mid == pytest.approx(2.4)
    assert result.box_cost_mid_zh == pytest.approx(2.4)
    assert result.volume_cost_zone_zh == '1.8 ~ 3（POC: 2.4，AVWAP: 2.2）'


def test_market_cost_proxy_can_use_kline_volume_weighted_cost_when_no_market_structure_mid():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100},
        ],
        same_source_groups=[],
        kline_rows=[
            {'close': 1.0, 'volume': 100},
            {'close': 3.0, 'volume': 300},
            {'close': 10.0, 'volume': 0},
        ],
    )

    assert result.market_cost_mid == pytest.approx(2.5)
    assert result.market_cost_mid_zh == pytest.approx(2.5)
    assert result.volume_cost_zone_zh == '1 ~ 3（成交量加权中枢: 2.5）'


@pytest.mark.parametrize(
    ('current_price', 'expected_pct', 'expected_status'),
    [
        (1.9, -5.0, '当前价格跌破主导侧成本区'),
        (2.0, 0.0, '当前价格接近主导侧成本区'),
        (2.1, 5.0, '当前价格接近主导侧成本区'),
        (2.4, 20.0, '当前价格略高于主导侧成本区'),
        (3.0, 50.0, '当前价格大幅高于主导侧成本区'),
    ],
)
def test_cost_position_status_answers_price_distance_to_dominant_cost_zone(current_price, expected_pct, expected_status):
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'role_name': '疑似早期买入钱包'},
            {'wallet_address': 'W2', 'token_address': 'T', 'buy_amount_usd': 300, 'buy_token_amount': 100, 'role_name': '疑似同源执行组成员'},
        ],
        same_source_groups=[],
        current_price=current_price,
    )

    assert result.dominant_cost_mid == pytest.approx(2.0)
    assert result.price_to_dominant_cost_pct == pytest.approx(expected_pct)
    assert result.cost_position_status_zh == expected_status


def test_cost_position_status_is_insufficient_when_no_structure_side_cost_evidence():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'BAG', 'token_address': 'T', 'buy_amount_usd': 1000, 'buy_token_amount': 100, 'role_name': '疑似接盘鲸鱼'},
            {'wallet_address': 'XFER', 'token_address': 'T', 'transfer_in': True, 'token_source_address': 'SRC'},
        ],
        same_source_groups=[],
        current_price=2.0,
    )

    assert result.price_to_dominant_cost_pct is None
    assert result.cost_position_status_zh == '成本区证据不足'


@pytest.mark.parametrize(
    ('current_price', 'expected_deviation', 'expected_status'),
    [
        (1.7, -0.15, '跌破成本区'),
        (1.8, -0.10, '成本附近'),
        (2.0, 0.0, '成本附近'),
        (2.4, 0.20, '成本附近'),
        (3.0, 0.50, '轻度盈利区'),
        (3.6, 0.80, '轻度盈利区'),
        (5.0, 1.50, '明显盈利区'),
        (6.0, 2.0, '明显盈利区'),
        (7.0, 2.50, '高派发风险区'),
    ],
)
def test_dominant_cost_deviation_model_classifies_profit_and_distribution_risk(current_price, expected_deviation, expected_status):
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'role_name': '疑似早期买入钱包'},
            {'wallet_address': 'W2', 'token_address': 'T', 'buy_amount_usd': 300, 'buy_token_amount': 100, 'role_name': '疑似同源执行组成员'},
        ],
        same_source_groups=[],
        current_price=current_price,
    )

    assert result.dominant_cost_mid == pytest.approx(2.0)
    assert result.dominant_cost_deviation_rate == pytest.approx(expected_deviation)
    assert result.dominant_cost_deviation_status_zh == expected_status


def test_dominant_cost_deviation_model_is_insufficient_without_price_or_cost():
    from modules.wallet_structure.dominant_cost_zone_calculator import calculate_dominant_cost_zone

    result = calculate_dominant_cost_zone(
        normalized_rows=[
            {'wallet_address': 'W1', 'token_address': 'T', 'buy_amount_usd': 100, 'buy_token_amount': 100, 'role_name': '疑似早期买入钱包'},
        ],
        same_source_groups=[],
    )

    assert result.dominant_cost_deviation_rate is None
    assert result.dominant_cost_deviation_status_zh == '成本区证据不足'
