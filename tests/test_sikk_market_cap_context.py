from sikk_market_cap_context import build_market_cap_context, merge_market_cap_context


def test_market_cap_context_full_chain_calculates_changes():
    context = build_market_cap_context(
        discovery_row={"token_address": "Token111", "symbol": "AAA", "discovery_market_cap_usd": 80000},
        signal_row={"signal_market_cap_usd": "100000"},
        wallet_row={"wallet_decision_market_cap_usd": 120000},
        paper_row={"paper_entry_market_cap_usd": 130000},
        current_row={"current_market_cap_usd": 160000},
        exit_row={"exit_market_cap_usd": 150000},
    )

    assert context.market_cap_context_quality == "OK"
    assert context.market_cap_change_from_discovery_pct == 100.0
    assert context.market_cap_change_from_signal_pct == 60.0
    assert context.market_cap_change_from_wallet_decision_pct == 33.3333
    assert not context.market_cap_missing_fields


def test_market_cap_context_supports_chinese_fields_and_missing_quality():
    context = build_market_cap_context(
        discovery_row={"代币地址": "Token222", "代币符号": "BBB", "发现市值": "50,000"},
        current_row={"当前市值USD": "$75,000"},
    )

    assert context.token_address == "Token222"
    assert context.discovery_market_cap_usd == 50000
    assert context.current_market_cap_usd == 75000
    assert context.market_cap_context_quality == "PARTIAL"
    assert "signal_market_cap_usd" in context.market_cap_missing_fields


def test_market_cap_context_missing_does_not_fabricate_values():
    context = build_market_cap_context(discovery_row={"token_address": "Token333"})

    assert context.discovery_market_cap_usd is None
    assert context.current_market_cap_usd is None
    assert context.market_cap_context_quality == "MISSING"
    assert set(context.market_cap_missing_fields) >= {"discovery_market_cap_usd", "current_market_cap_usd"}


def test_merge_market_cap_context_into_status():
    context = build_market_cap_context(
        discovery_row={"token_address": "Token444", "discovery_market_cap_usd": 100000},
        current_row={"current_market_cap_usd": 200000},
    )
    status = {"token_address": "Token444"}

    merge_market_cap_context(status, context)

    assert status["market_cap_context"]["discovery_market_cap_usd"] == 100000
    assert status["current_market_cap_usd"] == 200000
    assert status["market_cap_change_from_discovery_pct"] == 100.0
