import json
from pathlib import Path


TOKEN = "4ZEzC3aX7yLv8VEBiuoT6PgEMPEoxGB7WS3Qt3iPpump"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _snapshot(token: str = TOKEN) -> dict:
    return {
        "token_address": token,
        "token_symbol": "AGI",
        "chain": "sol",
        "price_usd": 0.00070805656,
        "market_cap_usd": 705106.95,
        "liquidity_usd": 85726.82,
        "mint_renounced": True,
        "freeze_renounced": True,
        "buy_tax_pct": 0,
        "sell_tax_pct": 0,
        "lp_burned": True,
        "top10_holder_rate_pct": 15.49,
        "holder_count": 3253,
        "smart_wallet_count": 56,
        "kol_wallet_count": 13,
        "fresh_wallet_count": 1000,
        "bundler_wallet_count": 1000,
        "sniper_wallet_count": 159,
        "whale_wallet_count": 1,
        "bot_degen_rate_pct": 31.61,
        "fresh_wallet_rate_pct": 9.27,
        "top_bundler_trader_percentage_pct": 39.5,
        "top_entrapment_trader_percentage_pct": 8.15,
        "funding_traced": False,
        "sample_wallets": [
            {"address": "Fej6xTZ4w2EgTUtAsDe7Dzdtq3T1oRDfGeQbXeWAw37w", "tags": ["pool"], "holder_pct": 6.09},
            {"address": "7Btw", "tags": ["top_holder", "bundler"], "pnl_usd": -10530, "unrealized_profit_usd": -14634},
            {"address": "4HfU", "tags": ["top_holder", "bundler"], "pnl_usd": 10796, "sold_usd": 0},
            {"address": "4JoE", "tags": ["top_holder", "transfer_in"], "buy_usd": 0, "holding_value_usd": 9143},
        ],
    }


def test_ca_runtime_pipeline_writes_context_ledger_state_live_and_audit(tmp_path):
    from sikk_ca_runtime_pipeline import run_ca_runtime_pipeline

    snapshot_path = tmp_path / "source_wallet_bot" / "live" / TOKEN / "structure_analysis" / "intelligence" / "agi_structural_snapshot.json"
    _write_json(snapshot_path, _snapshot())

    result = run_ca_runtime_pipeline(
        token_address=TOKEN,
        snapshot_path=snapshot_path,
        output_root=tmp_path / "strategy_gate_bot" / "live" / TOKEN,
        mode="live",
    )

    expected_keys = {
        "runtime_context_json",
        "permission_gate_json",
        "stage_ledger_jsonl",
        "ca_consistency_audit_json",
        "trade_gate_summary_json",
        "candidate_states_json",
        "live_state_json",
        "trade_gate_journal_jsonl",
        "completion_audit_json",
        "final_report_md",
        "review_writeback_json",
    }
    assert expected_keys.issubset(result)
    for key in expected_keys:
        assert Path(result[key]).exists(), key

    permission = json.loads(Path(result["permission_gate_json"]).read_text(encoding="utf-8"))
    assert permission["real_trade_enabled"] is False
    assert permission["broadcast_transaction"] is False
    assert permission["permission_status"] == "PAPER_OBSERVE_ONLY"

    audit = json.loads(Path(result["ca_consistency_audit_json"]).read_text(encoding="utf-8"))
    assert audit["overall_passed"] is True
    assert audit["token_address"] == TOKEN

    ledger_rows = [json.loads(line) for line in Path(result["stage_ledger_jsonl"]).read_text(encoding="utf-8").splitlines() if line.strip()]
    stage_names = [row["stage"] for row in ledger_rows]
    assert stage_names[:4] == ["runtime_context", "ca_consistency_audit", "permission_gate", "trade_gate_adapter"]
    assert "state_machine" in stage_names
    assert "completion_audit" in stage_names

    live_state = json.loads(Path(result["live_state_json"]).read_text(encoding="utf-8"))
    status = live_state["tokens"][0]
    assert status["token_address"] == TOKEN
    assert status["trade_gate"]["decision"] == "OBSERVE_ONLY"
    assert status["trade_gate"]["real_trade_enabled"] is False
    assert status["latest_action"] == "STRUCTURE_OBSERVE"

    final_report = Path(result["final_report_md"]).read_text(encoding="utf-8")
    assert "OBSERVE_ONLY" in final_report
    assert "不执行真实 swap" in final_report


def test_ca_runtime_pipeline_blocks_mismatched_snapshot_ca(tmp_path):
    from sikk_ca_runtime_pipeline import run_ca_runtime_pipeline

    requested = TOKEN
    actual = "Different111111111111111111111111111111111111pump"
    snapshot_path = tmp_path / "snapshot.json"
    _write_json(snapshot_path, _snapshot(actual))

    result = run_ca_runtime_pipeline(
        token_address=requested,
        snapshot_path=snapshot_path,
        output_root=tmp_path / "out",
        mode="live",
    )

    permission = json.loads(Path(result["permission_gate_json"]).read_text(encoding="utf-8"))
    audit = json.loads(Path(result["ca_consistency_audit_json"]).read_text(encoding="utf-8"))
    assert audit["overall_passed"] is False
    assert permission["permission_status"] == "CA_MISMATCH_BLOCKED"
    assert permission["real_trade_enabled"] is False
    assert result["status"] == "BLOCKED_CA_MISMATCH"
