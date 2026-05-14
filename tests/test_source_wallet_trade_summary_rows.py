from modules.source_wallet_bot.wallet_trade_normalizer import normalize_wallet_trades


def test_normalize_wallet_trades_accepts_gmgn_summary_rows():
    rows = [{
        'token_address': 'TOKEN',
        'wallet_address': 'W1',
        'side': 'summary',
        'timestamp': '2026-05-01T01:00:00Z',
        'first_buy_time': '2026-05-01T00:00:00Z',
        'last_buy_time': '2026-05-01T00:00:00Z',
        'last_sell_time': '',
        'buy_count': 3,
        'sell_count': 0,
        'buy_amount_usd': 1867.10238674221,
        'sell_amount_usd': 0,
        'buy_token_amount': 8383981.379337,
        'sell_token_amount': 0,
        'current_balance': 7106181.379337,
        'sold_pct': 0,
        'remaining_pct': 100,
        'realized_profit': 11.520614031758148,
        'unrealized_profit': 26.09662928929538,
        'total_profit': 37.61724332105353,
        'pnl_multiple': 0.017890384648083794,
        'avg_buy_price': 0.000222698775470069,
    }]
    [record] = normalize_wallet_trades(rows)
    assert record.buy_count == 3
    assert record.sell_count == 0
    assert record.buy_amount_usd == 1867.102387
    assert record.current_balance == 7106181.379337
    assert record.total_profit == 37.617243
    assert record.first_buy_time == '2026-05-01T00:00:00Z'
    assert record.last_sell_time == 'missing'
