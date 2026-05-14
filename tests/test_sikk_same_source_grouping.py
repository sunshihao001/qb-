from pathlib import Path


def _wallet(address, funding="FUND1", funding_label="private", funding_time="2026-05-02T00:00:00Z", funding_amount=1.0,
            entry_time="2026-05-02T00:01:00Z", entry_rank=10, buy=1000, sell_time="2026-05-02T00:10:00Z",
            sold_pct=10, remaining_pct=90, buy_count=1, sell_count=0, is_top_holder=False):
    return {
        "wallet_address": address,
        "funding_source_address": funding,
        "funding_source_label": funding_label,
        "first_funding_time": funding_time,
        "first_funding_amount_sol": funding_amount,
        "entry_time": entry_time,
        "entry_rank": entry_rank,
        "buy_amount_usd": buy,
        "sell_time": sell_time,
        "sold_pct": sold_pct,
        "remaining_pct": remaining_pct,
        "buy_count": buy_count,
        "sell_count": sell_count,
        "trade_count": buy_count + sell_count,
        "is_top_holder": is_top_holder,
    }


def test_same_source_grouping_creates_strong_group_id_and_scores():
    from sikk_same_source_grouping import build_same_source_groups

    wallets = [
        _wallet("W1", entry_time="2026-05-02T00:01:00Z", entry_rank=10, buy=1000, funding_amount=1.00),
        _wallet("W2", entry_time="2026-05-02T00:01:20Z", entry_rank=14, buy=1050, funding_amount=1.04),
        _wallet("W3", entry_time="2026-05-02T00:01:25Z", entry_rank=17, buy=980, funding_amount=0.98),
        _wallet("NOISE", funding="FUND9", entry_time="2026-05-02T00:20:00Z", entry_rank=180, buy=50),
    ]

    groups = build_same_source_groups(token_address="Token111", token_symbol="TEST", wallet_rows=wallets)

    assert len(groups) == 1
    group = groups[0]
    assert group["group_id"].startswith("SSG_TEST_")
    assert group["group_type"] == "FUNDING_STRONG_GROUP"
    assert group["source_reliability"] == "HIGH"
    assert group["group_size"] == 3
    assert set(group["wallets"].split(";")) == {"W1", "W2", "W3"}
    assert group["sync_buy_score"] >= 80
    assert group["sync_sell_score"] < 40
    assert group["group_evidence_level"] in {"E3", "E4"}


def test_public_cex_source_is_low_reliability_and_ambiguous():
    from sikk_same_source_grouping import build_same_source_groups

    wallets = [
        _wallet("C1", funding="OKX_HOT", funding_label="OKX CEX hot wallet", entry_rank=10),
        _wallet("C2", funding="OKX_HOT", funding_label="OKX CEX hot wallet", entry_rank=12),
        _wallet("C3", funding="OKX_HOT", funding_label="OKX CEX hot wallet", entry_rank=15),
    ]

    groups = build_same_source_groups(token_address="Token222", token_symbol="CEX", wallet_rows=wallets)

    assert len(groups) == 1
    group = groups[0]
    assert group["source_reliability"] == "LOW"
    assert group["group_type"] == "CEX_AMBIGUOUS_GROUP"
    assert group["group_evidence_level"] == "E1"
    assert "不强判同源" in group["reason"]


def test_sync_sell_score_high_marks_group_risk_block():
    from sikk_same_source_grouping import build_same_source_groups

    wallets = [
        _wallet("S1", sell_time="2026-05-02T00:20:00Z", sold_pct=85, remaining_pct=15, sell_count=2, is_top_holder=True),
        _wallet("S2", sell_time="2026-05-02T00:20:40Z", sold_pct=80, remaining_pct=20, sell_count=2),
        _wallet("S3", sell_time="2026-05-02T00:20:50Z", sold_pct=90, remaining_pct=10, sell_count=3),
    ]

    group = build_same_source_groups(token_address="Token333", token_symbol="SELL", wallet_rows=wallets)[0]

    assert group["sync_sell_score"] >= 70
    assert group["group_risk_level"] == "WALLET_BLOCK"
    assert group["group_sold_pct"] >= 80


def test_behavior_sync_group_without_funding_stays_behavior_only():
    from sikk_same_source_grouping import build_same_source_groups

    wallets = [
        _wallet("B1", funding="", entry_time="2026-05-02T00:01:00Z", entry_rank=10, buy=1000, sold_pct=5),
        _wallet("B2", funding="", entry_time="2026-05-02T00:01:30Z", entry_rank=14, buy=1050, sold_pct=8),
        _wallet("B3", funding="", entry_time="2026-05-02T00:01:50Z", entry_rank=16, buy=990, sold_pct=10),
    ]

    group = build_same_source_groups(token_address="Token444", token_symbol="BEH", wallet_rows=wallets)[0]

    assert group["group_type"] == "BEHAVIOR_SYNC_GROUP"
    assert group["source_reliability"] == "UNKNOWN"
    assert group["sync_buy_score"] >= 60
    assert "行为同步" in group["primary_evidence"]


def test_write_candidate_groups_csv_uses_required_headers(tmp_path):
    from sikk_same_source_grouping import build_same_source_groups, write_candidate_groups_csv

    groups = build_same_source_groups(
        token_address="Token555",
        token_symbol="CSV",
        wallet_rows=[
            _wallet("W1", entry_rank=1),
            _wallet("W2", entry_rank=2),
            _wallet("W3", entry_rank=3),
        ],
    )
    out = tmp_path / "candidate_groups.csv"
    write_candidate_groups_csv(out, groups)
    text = out.read_text(encoding="utf-8-sig")

    assert "token_address,group_id,group_type,group_size,wallets,primary_evidence,source_reliability" in text
    assert "sync_buy_score" in text
    assert "sync_sell_score" in text


def test_wallet_structure_gate_uses_sync_sell_group_to_block():
    from sikk_wallet_structure_gate import evaluate_wallet_structure_gate

    group = {
        "group_id": "SSG_SYNC_abc123",
        "sync_buy_score": 82,
        "sync_sell_score": 76,
        "group_sold_pct": 85,
        "group_risk_level": "WALLET_BLOCK",
    }
    decision = evaluate_wallet_structure_gate(
        token="TokenGateGroup",
        symbol="TGG",
        wallet_rows=[
            {"wallet_address": "S1", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "SSG_SYNC_abc123", "sell_ratio": 0.8, "evidence_level": "E4", "same_source_group": group},
            {"wallet_address": "S2", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "SSG_SYNC_abc123", "sell_ratio": 0.75, "evidence_level": "E4", "same_source_group": group},
            {"wallet_address": "S3", "role": "SAME_SOURCE_GROUP", "game_side": "EXECUTION_SIDE", "group_id": "SSG_SYNC_abc123", "sell_ratio": 0.82, "evidence_level": "E3", "same_source_group": group},
        ],
        candidate_groups=[group],
    )

    assert decision.wallet_structure_status == "WALLET_BLOCK"
    assert decision.max_sync_sell_score == 76
    assert decision.has_same_source_sync_sell is True
    assert "sync_sell_score>=70" in "；".join(decision.reasons)


def test_wallet_structure_gate_uses_sync_buy_group_to_support():
    from sikk_wallet_structure_gate import evaluate_wallet_structure_gate

    group = {
        "group_id": "SSG_BUY_def456",
        "sync_buy_score": 88,
        "sync_sell_score": 18,
        "group_sold_pct": 8,
        "group_risk_level": "STRUCTURE_SUPPORT",
    }
    decision = evaluate_wallet_structure_gate(
        token="TokenGateBuy",
        symbol="TGB",
        wallet_rows=[
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.15, "sell_ratio": 0.05, "evidence_level": "E4", "same_source_group": group},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.1, "evidence_level": "E3", "same_source_group": group},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.08, "sell_ratio": 0.05, "evidence_level": "E3", "same_source_group": group},
        ],
        candidate_groups=[group],
    )

    assert decision.wallet_structure_status == "WALLET_SUPPORT"
    assert decision.max_sync_buy_score == 88
    assert decision.wallet_structure_score >= 70
