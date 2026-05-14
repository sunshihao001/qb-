from modules.source_wallet_bot.models import WalletProfileRecord, WalletTradeRecord
from modules.source_wallet_bot.source_group_engine import build_same_source_groups


def test_build_same_source_groups_by_shared_funding_source():
    profiles = [
        WalletProfileRecord(wallet_address='W1', funding_source_address='FUND'),
        WalletProfileRecord(wallet_address='W2', funding_source_address='FUND'),
        WalletProfileRecord(wallet_address='W3', funding_source_address='OTHER'),
    ]
    groups = build_same_source_groups(profiles, [])
    assert len(groups) == 1
    assert groups[0].evidence_label == '疑似同源执行组'
    assert groups[0].group_wallets == ['W1', 'W2']
    assert groups[0].shared_funding_source == 'FUND'


def test_weak_source_group_evidence_returns_no_group():
    profiles = [WalletProfileRecord(wallet_address='W1'), WalletProfileRecord(wallet_address='W2')]
    assert build_same_source_groups(profiles, []) == []
