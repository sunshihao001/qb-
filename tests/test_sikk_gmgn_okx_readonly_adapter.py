import json
import sys
from pathlib import Path

from modules.source_wallet_bot.gmgn_okx_readonly_adapter import (
    build_token_readonly_commands,
    ensure_readonly_command,
    map_raw_snapshot_to_stage_outputs,
    run_readonly_adapter_for_token,
)

TOKEN = "So11111111111111111111111111111111111111112"


def test_command_plan_is_readonly_and_contains_dual_sources():
    commands = build_token_readonly_commands(TOKEN, limit=10)
    flattened = "\n".join(" ".join(item.command) for item in commands)
    assert "gmgn-cli token info" in flattened
    assert "onchainos token price-info" in flattened
    assert "onchainos token cluster-list" in flattened
    assert "swap" not in flattened
    assert "broadcast" not in flattened
    assert "private" not in flattened.lower()
    for item in commands:
        ensure_readonly_command(item.command)


def test_readonly_guard_rejects_trade_or_secret_commands():
    bad_commands = [
        ["gmgn-cli", "swap", "--address", TOKEN],
        ["gmgn-cli", "order", "strategy", "create"],
        ["onchainos", "swap", "execute"],
        ["onchainos", "security", "token-scan", "--private-key", "abc"],
    ]
    for cmd in bad_commands:
        try:
            ensure_readonly_command(cmd)
        except ValueError as exc:
            assert "只允许" in str(exc) or "拒绝" in str(exc) or "白名单" in str(exc)
        else:
            raise AssertionError(f"should reject {cmd}")


def test_raw_snapshot_mapper_creates_valid_stage_outputs():
    snapshot = {
        "manifest": {"token_address": TOKEN, "created_at": "2026-05-07T00:00:00Z", "required_failures": []},
        "records": [
            {"source": "gmgn", "endpoint": "token_info", "exit_code": 0, "parsed": {"symbol": "SOL", "price": "150", "liquidity": "50000", "stat": {"top_10_holder_rate": 0.2}}},
            {"source": "gmgn", "endpoint": "token_security", "exit_code": 0, "parsed": {"rug_ratio": 0.02, "is_honeypot": "no", "renounced_mint": True, "renounced_freeze_account": True}},
            {"source": "gmgn", "endpoint": "token_pool", "exit_code": 0, "parsed": {"liquidity": "51000"}},
            {"source": "gmgn", "endpoint": "token_holders", "exit_code": 0, "parsed": {"list": [{"address": "wallet1"}]}},
            {"source": "gmgn", "endpoint": "token_traders", "exit_code": 0, "parsed": {"list": [{"address": "wallet1"}]}},
            {"source": "okx", "endpoint": "price_info", "exit_code": 0, "parsed": {"marketCap": "200000", "liquidity": "52000", "price": "150"}},
            {"source": "okx", "endpoint": "liquidity", "exit_code": 0, "parsed": {"liquidityUsd": "52000"}},
            {"source": "okx", "endpoint": "advanced_info", "exit_code": 0, "parsed": {"riskControlLevel": "low", "top10HoldPercent": 0.2}},
            {"source": "okx", "endpoint": "top_trader", "exit_code": 0, "parsed": {"list": [{"walletAddress": "wallet1"}]}},
            {"source": "okx", "endpoint": "cluster_overview", "exit_code": 0, "parsed": {"clusterLevel": "low"}},
            {"source": "okx", "endpoint": "cluster_list", "exit_code": 0, "parsed": {"list": [{"clusterId": "c1"}]}},
        ],
    }
    mapped = map_raw_snapshot_to_stage_outputs(snapshot)
    assert mapped["field_summary"]["market_cap"] == 200000.0
    assert mapped["field_summary"]["liquidity_usd"] == 50000.0
    assert len(mapped["stage_outputs"]) >= 6
    assert all(stage["paper_only"] is True for stage in mapped["stage_outputs"])
    assert all(stage["live_disabled"] is True for stage in mapped["stage_outputs"])
    assert all(stage["validation"]["overall_status"] == "PASS" for stage in mapped["stage_outputs"])


def test_adapter_no_network_writes_constitution_paths(tmp_path):
    out = tmp_path / "data" / "source_wallet_bot" / "paper" / TOKEN
    result = run_readonly_adapter_for_token(TOKEN, output_root=out, limit=5, allow_network=False)
    assert Path(result["stage_outputs_path"]).exists()
    manifest = out / "manifest" / "token_output_manifest.json"
    assert manifest.exists()
    payload = json.loads(Path(result["stage_outputs_path"]).read_text(encoding="utf-8"))
    assert payload["token_address"] == TOKEN
    assert payload["stage_outputs"]
    assert not list(out.glob("*.json"))  # no flat root runtime JSON under token dir
