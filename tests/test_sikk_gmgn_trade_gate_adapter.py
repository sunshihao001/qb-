import json
from pathlib import Path


def test_convert_agi_structural_snapshot_to_trade_gate_observe_only():
    from sikk_gmgn_trade_gate_adapter import convert_structural_snapshot

    snapshot = {
        "token_address": "4ZEzC3aX7yLv8VEBiuoT6PgEMPEoxGB7WS3Qt3iPpump",
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

    result = convert_structural_snapshot(snapshot)

    assert result["token_intake"]["token_address"] == snapshot["token_address"]
    assert result["structural_intel"]["early_execution_strength"] == "STRONG"
    assert result["structural_intel"]["structure_activity_score"] >= 70
    assert result["evidence_bundle"]["funding_status"] == "资金待查"
    assert "资金层跳过" in result["evidence_bundle"]["missing_evidence"]
    assert result["trade_gate_decision"]["decision"] == "OBSERVE_ONLY"
    assert result["trade_gate_decision"]["final_status"] == "OBSERVE"
    assert result["trade_gate_decision"]["signal_level"] == "S1"
    assert result["trade_gate_decision"]["contract_permission"] == "PAUSE_NEED_CONFIRM_需要人工确认"
    assert result["trade_gate_decision"]["permission"] == "BLOCK_REAL_TRADE"
    assert result["trade_gate_decision"]["real_trade_enabled"] is False
    assert result["risk_control_profile"]["real_trade_allowed"] is False
    assert result["wallet_decision"]["wallet_structure_status"] in {"WALLET_PAUSE", "WALLET_BLOCK"}
    assert result["wallet_decision"]["wallet_structure_factor"] <= 1.0
    assert result["execution_intent"]["mode"] == "paper_only"
    assert result["execution_intent"]["real_order"] is False


def test_adapter_writes_runtime_contract_files(tmp_path):
    from sikk_gmgn_trade_gate_adapter import convert_structural_snapshot, write_runtime_outputs

    snapshot = {
        "token_address": "Token111",
        "token_symbol": "TOK",
        "chain": "sol",
        "liquidity_usd": 100000,
        "mint_renounced": True,
        "freeze_renounced": True,
        "buy_tax_pct": 0,
        "sell_tax_pct": 0,
        "lp_burned": True,
        "bundler_wallet_count": 20,
        "sniper_wallet_count": 2,
        "fresh_wallet_count": 5,
        "holder_count": 1000,
        "funding_traced": True,
    }
    result = convert_structural_snapshot(snapshot)
    paths = write_runtime_outputs(result, tmp_path)

    expected = {
        "token_intake.json",
        "structural_intel_result.json",
        "evidence_bundle.json",
        "trade_gate_decision.json",
        "risk_control_profile.json",
        "execution_intent.json",
        "review_writeback.json",
        "wallet_structure_decision.json",
    }
    assert expected.issubset({Path(p).name for p in paths.values()})
    gate = json.loads(Path(paths["trade_gate_decision"]).read_text(encoding="utf-8"))
    assert gate["token_address"] == "Token111"
    assert gate["decision"] in {"PAPER_READY", "OBSERVE_ONLY", "BLOCK"}
