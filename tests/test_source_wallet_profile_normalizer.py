from modules.source_wallet_bot.wallet_profile_normalizer import normalize_wallet_profile


def test_normalize_wallet_profile_preserves_tags_as_evidence_hints():
    profile = normalize_wallet_profile({
        'wallet_address': 'W1',
        'wallet_first_seen_time': '2026-04-01T00:00:00Z',
        'wallet_last_active_time': '2026-05-01T00:00:00Z',
        'wallet_age_days': 30,
        'total_token_count': 12,
        'traded_token_count': 8,
        'gmgn_tags': ['smart', 'fresh'],
        'funding_source_address': 'FUND',
    })
    assert profile.wallet_address == 'W1'
    assert profile.gmgn_tags == ['smart', 'fresh']
    assert profile.evidence_level == 'E2'
    assert not profile.missing_fields


def test_normalize_wallet_profile_missing_fields_are_explicit():
    profile = normalize_wallet_profile({'wallet_address': 'W2'})
    assert profile.wallet_first_seen_time == 'missing'
    assert 'wallet_first_seen_time' in profile.missing_fields
    assert profile.wallet_age_days == 'unknown'
