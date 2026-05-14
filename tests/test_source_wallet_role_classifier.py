from modules.source_wallet_bot.models import SourceGroupRecord, WalletProfileRecord, WalletTradeRecord
from modules.source_wallet_bot.role_classifier import classify_wallet


def test_classify_wallet_result_and_whale_candidates_use_evidence_language():
    trade = WalletTradeRecord(
        token_address='TOKEN', wallet_address='W1', buy_amount_usd=100.0,
        current_balance=5000.0, pnl_multiple=3.0, sold_pct=20.0,
    )
    profile = WalletProfileRecord(wallet_address='W1', gmgn_tags=['smart'], funding_source_address='FUND')
    decision = classify_wallet(trade, profile, groups=[])
    assert '疑似结果钱包' in decision.role_candidates
    assert '疑似接盘鲸鱼' in decision.role_candidates
    assert decision.gmgn_note_suggestion.startswith('疑似')
    data = decision.to_dict()
    assert 'PAPER_READY' not in data
    assert 'BLOCKED' not in data


def test_classify_wallet_same_source_member():
    trade = WalletTradeRecord(token_address='TOKEN', wallet_address='W2')
    profile = WalletProfileRecord(wallet_address='W2')
    group = SourceGroupRecord(same_source_group_id='G1', group_wallets=['W2', 'W3'])
    decision = classify_wallet(trade, profile, groups=[group])
    assert '疑似同源执行组' in decision.role_candidates
