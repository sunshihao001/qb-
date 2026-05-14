from modules.source_wallet_bot.handoff_exporter import build_handoff_packet
from modules.source_wallet_bot.models import WalletDecision, WalletTradeRecord
from modules.source_wallet_bot.schema_validator import validate_handoff_packet


def test_build_handoff_packet_contains_required_sections_and_no_forbidden_fields():
    trade = WalletTradeRecord(token_address='TOKEN', wallet_address='W1', missing_fields=['last_sell_time'])
    decision = WalletDecision(wallet_address='W1', token_address='TOKEN', role_candidates=['疑似结果钱包'])
    packet = build_handoff_packet(
        token_address='TOKEN',
        wallet_trades=[trade],
        wallet_profiles=[],
        source_groups=[],
        decisions=[decision],
    )
    data = packet.to_dict()
    validate_handoff_packet(data)
    assert data['token_address'] == 'TOKEN'
    assert data['evidence_language_only'] is True
    assert data['missing_fields_summary']['W1'] == ['last_sell_time']
    assert not data['forbidden_decision_fields']
