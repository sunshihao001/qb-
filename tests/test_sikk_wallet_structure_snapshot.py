import json
from pathlib import Path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_wallet_structure_snapshot_writes_latest_snapshot_without_delta_on_first_run(tmp_path):
    from sikk_wallet_structure_gate import evaluate_wallet_structure_gate
    from sikk_wallet_structure_snapshot import write_snapshot_and_delta

    decision = evaluate_wallet_structure_gate(
        token="TokenSnapshot11111111111111111111111111111",
        symbol="SNAP",
        wallet_rows=[
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.18, "sell_ratio": 0.05, "evidence_level": "E4"},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.10, "sell_ratio": 0.10, "evidence_level": "E3"},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.08, "sell_ratio": 0.05, "evidence_level": "E3"},
        ],
        candidate_groups=[{"sync_buy_score": 78, "sync_sell_score": 20, "group_remaining_pct": 85, "group_sold_pct": 15}],
    )

    result = write_snapshot_and_delta(
        token_address="TokenSnapshot11111111111111111111111111111",
        token_symbol="SNAP",
        decision=decision,
        market_context={"price": 1.0, "market_cap": 100000, "liquidity": 20000, "holder_count": 120, "top10_holder_pct": 28},
        base_dir=tmp_path / "wallet_structure",
        snapshot_time="2026-05-02T00:00:00Z",
    )

    snapshot_path = Path(result["snapshot_path"])
    latest_snapshot = tmp_path / "wallet_structure" / "TokenSnapshot11111111111111111111111111111" / "snapshots" / "latest_snapshot.json"
    latest_delta = tmp_path / "wallet_structure" / "TokenSnapshot11111111111111111111111111111" / "snapshots" / "latest_delta.json"

    assert snapshot_path.exists()
    assert latest_snapshot.exists()
    assert result["delta_path"] is None
    assert not latest_delta.exists()

    snapshot = _read_json(latest_snapshot)
    assert snapshot["token_address"] == "TokenSnapshot11111111111111111111111111111"
    assert snapshot["wallet_structure_status"] == "WALLET_SUPPORT"
    assert snapshot["wallet_structure_score"] >= 60
    assert snapshot["same_source_sync_buy_score"] == 78
    assert snapshot["same_source_sync_sell_score"] == 20
    assert snapshot["dominant_side_status"] == "STRUCTURE_SIDE"
    assert snapshot["chip_transfer_status"] == "CONTROL_RETAINED_BY_STRUCTURE_SIDE"


def test_wallet_structure_snapshot_second_run_writes_delta_and_interprets_structure_weakening(tmp_path):
    from sikk_wallet_structure_gate import evaluate_wallet_structure_gate
    from sikk_wallet_structure_snapshot import write_snapshot_and_delta

    token = "TokenDelta11111111111111111111111111111111"
    first_decision = evaluate_wallet_structure_gate(
        token=token,
        symbol="DLT",
        wallet_rows=[
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.18, "sell_ratio": 0.05, "evidence_level": "E4"},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.10, "sell_ratio": 0.10, "evidence_level": "E3"},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.08, "sell_ratio": 0.05, "evidence_level": "E3"},
        ],
        candidate_groups=[{"sync_buy_score": 76, "sync_sell_score": 15, "group_remaining_pct": 90, "group_sold_pct": 10}],
    )
    write_snapshot_and_delta(
        token_address=token,
        token_symbol="DLT",
        decision=first_decision,
        market_context={"price": 1.0, "market_cap": 100000, "liquidity": 20000, "holder_count": 100, "top10_holder_pct": 32},
        base_dir=tmp_path / "wallet_structure",
        snapshot_time="2026-05-02T00:00:00Z",
    )

    second_decision = evaluate_wallet_structure_gate(
        token=token,
        symbol="DLT",
        wallet_rows=[
            {"wallet_address": "X1", "role": "EARLY_EXIT", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.92, "evidence_level": "E3"},
            {"wallet_address": "X2", "role": "DISTRIBUTION_SELLER", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.85, "evidence_level": "E4"},
            {"wallet_address": "B1", "role": "BAGHOLDER_WHALE", "game_side": "COUNTERPARTY_SIDE", "holding_ratio": 0.12, "sell_ratio": 0.0, "unrealized_profit_pct": -25, "evidence_level": "R2"},
        ],
        candidate_groups=[{"sync_buy_score": 40, "sync_sell_score": 82, "group_remaining_pct": 35, "group_sold_pct": 65}],
    )
    result = write_snapshot_and_delta(
        token_address=token,
        token_symbol="DLT",
        decision=second_decision,
        market_context={"price": 1.35, "market_cap": 135000, "liquidity": 18000, "holder_count": 130, "top10_holder_pct": 26},
        base_dir=tmp_path / "wallet_structure",
        snapshot_time="2026-05-02T00:10:00Z",
    )

    delta_path = Path(result["delta_path"])
    latest_delta = tmp_path / "wallet_structure" / token / "snapshots" / "latest_delta.json"
    assert delta_path.exists()
    assert latest_delta.exists()

    delta = _read_json(latest_delta)
    assert delta["price_change_pct"] == 35.0
    assert delta["same_source_group_sold_pct_delta"] == 55.0
    assert delta["counterparty_pressure_score_delta"] > 0
    assert delta["chip_transfer_status_to"] in {"CONTROL_MIGRATING_TO_COUNTERPARTY", "CONTROL_LOST_TO_DISTRIBUTION"}
    assert delta["wallet_structure_delta_status"] in {"STRUCTURE_WEAKENING", "COUNTERPARTY_ABSORBING", "SAME_SOURCE_EXIT"}
    assert "同源" in delta["delta_interpretation"] or "对手盘" in delta["delta_interpretation"] or "结构" in delta["delta_interpretation"]
