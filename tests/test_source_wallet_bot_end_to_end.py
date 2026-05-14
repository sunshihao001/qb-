from modules.source_wallet_bot.handoff_exporter import build_handoff_packet
from modules.source_wallet_bot.role_classifier import classify_wallet
from modules.source_wallet_bot.schema_validator import validate_handoff_packet
from modules.source_wallet_bot.source_group_engine import build_same_source_groups
from modules.source_wallet_bot.wallet_profile_normalizer import normalize_wallet_profile
from modules.source_wallet_bot.wallet_trade_normalizer import normalize_wallet_trades


def test_end_to_end_source_wallet_bot_contract_flow():
    raw_trades = [
        {'token_address': 'TOKEN', 'wallet_address': 'W1', 'side': 'buy', 'timestamp': '2026-05-01T00:00:00Z', 'amount_usd': 100, 'token_amount': 1000},
        {'token_address': 'TOKEN', 'wallet_address': 'W2', 'side': 'buy', 'timestamp': '2026-05-01T00:01:00Z', 'amount_usd': 120, 'token_amount': 1200},
    ]
    trades = normalize_wallet_trades(raw_trades, current_prices_usd={('TOKEN', 'W1'): 0.2, ('TOKEN', 'W2'): 0.2})
    profiles = [
        normalize_wallet_profile({'wallet_address': 'W1', 'funding_source_address': 'FUND', 'gmgn_tags': ['fresh']}),
        normalize_wallet_profile({'wallet_address': 'W2', 'funding_source_address': 'FUND', 'gmgn_tags': ['fresh']}),
    ]
    groups = build_same_source_groups(profiles, trades)
    decisions = [classify_wallet(trade, next(p for p in profiles if p.wallet_address == trade.wallet_address), groups) for trade in trades]
    packet = build_handoff_packet(token_address='TOKEN', wallet_trades=trades, wallet_profiles=profiles, source_groups=groups, decisions=decisions)
    data = packet.to_dict()
    validate_handoff_packet(data)
    assert groups[0].evidence_label == '疑似同源执行组'
    assert all(decision.role_candidates for decision in decisions)
    assert data['evidence_language_only'] is True
    assert not data['forbidden_decision_fields']
