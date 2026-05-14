from modules.source_wallet_bot.gmgn_live_adapter import (
    collect_and_build_source_wallet_packet,
    gmgn_holder_rows_to_profile_rows,
    gmgn_holder_rows_to_trade_rows,
)


def test_gmgn_holder_rows_to_trade_rows_maps_existing_gmgn_fields():
    rows = [{
        'address': 'W1',
        'buy_tx_count_cur': 2,
        'sell_tx_count_cur': 1,
        'buy_volume_cur': 100.0,
        'sell_volume_cur': 60.0,
        'buy_amount_cur': 1000.0,
        'sell_amount_cur': 500.0,
        'amount_cur': 500.0,
        'sell_amount_percentage': 0.5,
        'profit': 10.0,
        'realized_profit': 5.0,
        'unrealized_profit': 5.0,
        'start_holding_at': 1777971486,
        'last_active_timestamp': 1777975086,
        'avg_cost': 0.1,
        'avg_sold': 0.12,
    }]
    [trade] = gmgn_holder_rows_to_trade_rows('TOKEN', rows)
    assert trade['token_address'] == 'TOKEN'
    assert trade['wallet_address'] == 'W1'
    assert trade['side'] == 'summary'
    assert trade['buy_count'] == 2
    assert trade['sell_count'] == 1
    assert trade['buy_amount_usd'] == 100.0
    assert trade['sell_amount_usd'] == 60.0
    assert trade['current_balance'] == 500.0
    assert trade['sold_pct'] == 50.0


def test_gmgn_holder_rows_to_profile_rows_maps_tags_and_funding():
    rows = [{
        'address': 'W1',
        'created_at': 1775565027,
        'last_active_timestamp': 1777992003,
        'tags': ['smart'],
        'maker_token_tags': ['top_holder'],
        'native_transfer': {'from_address': 'FUND'},
    }]
    [profile] = gmgn_holder_rows_to_profile_rows(rows)
    assert profile['wallet_address'] == 'W1'
    assert profile['funding_source_address'] == 'FUND'
    assert profile['gmgn_tags'] == ['smart', 'top_holder']


def test_collect_packet_writes_standard_layout_as_primary_outputs(monkeypatch, tmp_path):
    token = 'TOKEN'

    def fake_collect(token_address, *, limit=30):
        assert token_address == token
        return {
            'raw_payloads': [],
            'wallet_rows': [{
                'address': 'W1',
                'buy_tx_count_cur': 1,
                'sell_tx_count_cur': 0,
                'buy_volume_cur': 100.0,
                'buy_amount_cur': 1000.0,
                'amount_cur': 1000.0,
                'sell_amount_percentage': 0,
                'profit': 0.0,
                'realized_profit': 0.0,
                'unrealized_profit': 0.0,
                'start_holding_at': 1777971486,
                'last_active_timestamp': 1777975086,
                'tags': ['fresh_wallet'],
                'native_transfer': {'from_address': 'FUND'},
            }],
        }

    monkeypatch.setattr('modules.source_wallet_bot.gmgn_live_adapter.collect_gmgn_token_wallet_rows', fake_collect)

    result = collect_and_build_source_wallet_packet(token, tmp_path, limit=1)

    assert (tmp_path / 'wallet_data/raw/gmgn_wallet_rows_raw.json').exists()
    assert (tmp_path / 'wallet_data/raw/gmgn_wallet_trade_input.json').exists()
    assert (tmp_path / 'wallet_data/raw/gmgn_wallet_profile_input.json').exists()
    assert (tmp_path / 'wallet_data/normalized/wallet_trade_normalized.json').exists()
    assert (tmp_path / 'wallet_data/normalized/wallet_entity_profile_normalized.json').exists()
    assert (tmp_path / 'structure_analysis/intelligence/same_source_evidence_normalized.json').exists()
    assert (tmp_path / 'structure_analysis/intelligence/wallet_intelligence_decision.json').exists()
    assert (tmp_path / 'structure_analysis/handoff/bot2_handoff_packet.json').exists()
    assert not (tmp_path / 'wallet_trade_normalized.json').exists()
    assert not (tmp_path / 'wallet_intelligence_decision.json').exists()
    assert result['wallet_trade_normalized'].endswith('wallet_data/normalized/wallet_trade_normalized.json')
    assert result['bot2_handoff_packet'].endswith('structure_analysis/handoff/bot2_handoff_packet.json')
    assert result['primary_write_layout'] == 'standard_source_wallet_token_layout'
    assert (tmp_path / 'manifest/wallet_data_guard_source_manifest.json').exists()
    assert (tmp_path / 'verification/wallet_data_guard_contamination_scan.json').exists()
    assert result['wallet_data_guard_manifest'].endswith('manifest/wallet_data_guard_source_manifest.json')
    assert result['wallet_data_guard_scan_report'].endswith('verification/wallet_data_guard_contamination_scan.json')
    assert result['wallet_data_guard_status'] == 'PASS'
