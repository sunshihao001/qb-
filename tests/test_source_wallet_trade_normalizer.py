from modules.source_wallet_bot.wallet_trade_normalizer import normalize_wallet_trades


def test_normalize_wallet_trades_calculates_trade_metrics():
    raw = [
        {'token_address': 'TOKEN', 'wallet_address': 'W1', 'side': 'buy', 'timestamp': '2026-05-01T00:00:00Z', 'amount_sol': 1.0, 'amount_usd': 100.0, 'token_amount': 1000.0},
        {'token_address': 'TOKEN', 'wallet_address': 'W1', 'side': 'buy', 'timestamp': '2026-05-01T00:10:00Z', 'amount_sol': 2.0, 'amount_usd': 220.0, 'token_amount': 2000.0},
        {'token_address': 'TOKEN', 'wallet_address': 'W1', 'side': 'sell', 'timestamp': '2026-05-01T01:00:00Z', 'amount_sol': 1.5, 'amount_usd': 180.0, 'token_amount': 1500.0},
    ]
    [record] = normalize_wallet_trades(raw, current_prices_usd={('TOKEN', 'W1'): 0.12})
    assert record.token_address == 'TOKEN'
    assert record.wallet_address == 'W1'
    assert record.first_buy_time == '2026-05-01T00:00:00Z'
    assert record.last_buy_time == '2026-05-01T00:10:00Z'
    assert record.last_sell_time == '2026-05-01T01:00:00Z'
    assert record.buy_count == 2
    assert record.sell_count == 1
    assert record.buy_amount_sol == 3.0
    assert record.buy_amount_usd == 320.0
    assert record.buy_token_amount == 3000.0
    assert record.sell_token_amount == 1500.0
    assert record.avg_buy_price == 0.106667
    assert record.avg_sell_price == 0.12
    assert record.current_balance == 1500.0
    assert record.sold_pct == 50.0
    assert record.remaining_pct == 50.0
    assert record.realized_profit == 20.0
    assert record.unrealized_profit == 20.0
    assert record.total_profit == 40.0
    assert record.pnl_multiple == 1.125
    assert record.holding_duration_seconds == 3600
    assert record.is_partial_exit is True
    assert record.is_full_exit is False


def test_normalize_wallet_trades_collects_missing_fields_without_fabrication():
    raw = [{'token_address': 'TOKEN', 'wallet_address': 'W2', 'side': 'buy'}]
    [record] = normalize_wallet_trades(raw)
    assert record.first_buy_time == 'missing'
    assert 'timestamp' in record.missing_fields
    assert record.current_balance == 'missing'
    assert 'current_price_usd' in record.requires_followup_fields
