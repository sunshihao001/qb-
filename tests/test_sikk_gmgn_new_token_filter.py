import csv
import json
from pathlib import Path


GOOD_TOKEN = {
    "address": "Good111111111111111111111111111111111111111",
    "symbol": "GOOD",
    "name": "Good Token",
    "usd_market_cap": 180_000,
    "liquidity": 40_000,
    "volume_24h": 180_000,
    "net_buy_24h": 22_000,
    "swaps_24h": 260,
    "buys_24h": 170,
    "sells_24h": 70,
    "top_10_holder_rate": 0.22,
    "creator_balance_rate": 0.018,
    "rat_trader_amount_rate": 0.03,
    "bot_degen_rate": 0.14,
    "whale_hold_rate": 0.12,
    "creator_created_count": 4,
    "smart_degen_count": 2,
    "renowned_count": 1,
    "fresh_wallet_rate": 0.18,
    "sniper_count": 8,
    "bundler_trader_amount_rate": 0.06,
    "rug_ratio": 0.05,
}

RISK_TOKEN = {
    **GOOD_TOKEN,
    "address": "Risk111111111111111111111111111111111111111",
    "symbol": "RISK",
    "top_10_holder_rate": 0.62,
    "creator_balance_rate": 0.20,
    "rug_ratio": 0.42,
}

WEAK_TOKEN = {
    **GOOD_TOKEN,
    "address": "Weak111111111111111111111111111111111111111",
    "symbol": "WEAK",
    "usd_market_cap": 70_000,
    "liquidity": 12_000,
    "volume_24h": 55_000,
    "net_buy_24h": 6_000,
    "swaps_24h": 110,
    "buys_24h": 65,
    "sells_24h": 12,
    "smart_degen_count": 0,
    "renowned_count": 0,
    "fresh_wallet_rate": 0.02,
    "sniper_count": 0,
    "bundler_trader_amount_rate": 0.0,
}


def test_default_config_contains_sikk_gmgn_v1_thresholds():
    from sikk_gmgn_new_token_filter import load_filter_config

    cfg = load_filter_config()

    assert cfg["template_name"] == "SIKK-GMGN 默认筛选 V1"
    assert cfg["thresholds"]["market_cap"]["min"] == 50_000
    assert cfg["thresholds"]["market_cap"]["max"] == 1_500_000
    assert cfg["thresholds"]["liquidity"]["min"] == 10_000
    assert cfg["thresholds"]["liquidity"]["max"] == 300_000
    assert cfg["thresholds"]["volume_24h"]["min"] == 50_000
    assert cfg["thresholds"]["net_buy_24h"]["min"] == 5_000
    assert cfg["thresholds"]["top_10_holder_rate"]["max"] == 0.35
    assert cfg["thresholds"]["creator_balance_rate"]["max"] == 0.05


def test_classifies_good_structure_token_as_s3_candidate():
    from sikk_gmgn_new_token_filter import classify_token, load_filter_config

    result = classify_token(GOOD_TOKEN, load_filter_config())

    assert result["筛选等级"] == "S3_进入SIKK结构分析"
    assert result["是否进入候选池"] is True
    assert result["风险动作"] == "ALLOW_ANALYSIS"
    assert result["结构加分"] >= 2
    assert "Smart钱包>=1" in result["通过条件"]
    assert "KOL人数>=1" in result["通过条件"]


def test_normalized_candidate_preserves_kline_anchor_fields():
    from sikk_gmgn_new_token_filter import classify_token, load_filter_config

    raw = {
        **GOOD_TOKEN,
        "created_timestamp": 1770000000,
        "open_timestamp": 1770000300,
        "total_supply": "1000000000",
        "launchpad_platform": "Pump.fun",
    }
    result = classify_token(raw, load_filter_config())

    assert result["创建时间戳"] == 1770000000
    assert result["开盘时间戳"] == 1770000300
    assert result["总供应量"] == 1_000_000_000
    assert result["发射平台"] == "Pump.fun"


def test_hard_risk_token_is_s0_excluded_even_if_activity_is_high():
    from sikk_gmgn_new_token_filter import classify_token, load_filter_config

    result = classify_token(RISK_TOKEN, load_filter_config())

    assert result["筛选等级"] == "S0_排除"
    assert result["是否进入候选池"] is False
    assert result["风险动作"] == "BLOCK"
    assert any("Top10持仓过高" in reason for reason in result["排除原因"])
    assert any("Dev持仓过高" in reason for reason in result["排除原因"])


def test_weak_but_valid_token_is_s1_observe_not_structure_candidate():
    from sikk_gmgn_new_token_filter import classify_token, load_filter_config

    result = classify_token(WEAK_TOKEN, load_filter_config())

    assert result["筛选等级"] == "S1_普通观察"
    assert result["是否进入候选池"] is True
    assert result["风险动作"] == "OBSERVE_ONLY"
    assert result["结构加分"] == 0


def test_build_readonly_gmgn_trenches_command_uses_filter_thresholds():
    from sikk_gmgn_new_token_filter import build_gmgn_trenches_command, load_filter_config

    cmd = build_gmgn_trenches_command(load_filter_config(), limit=40)
    joined = " ".join(cmd)

    assert cmd[:3] == ["gmgn-cli", "market", "trenches"]
    assert "--chain sol" in joined
    assert "--type completed" in joined
    assert "--min-marketcap 50000" in joined
    assert "--max-marketcap 1500000" in joined
    assert "--min-liquidity 10000" in joined
    assert "--max-liquidity 300000" in joined
    assert "--raw" in cmd
    assert "gmgn-cli swap" not in joined
    assert "gmgn-cli order" not in joined
    assert "order strategy create" not in joined


def test_collect_and_write_candidate_pool_from_fake_runner(tmp_path):
    from sikk_gmgn_new_token_filter import collect_and_write_candidate_pool, load_filter_config

    calls = []

    def fake_runner(cmd):
        calls.append(cmd)
        return {
            "completed": [GOOD_TOKEN, RISK_TOKEN, WEAK_TOKEN],
            "new_creation": [],
            "near_completion": [],
        }

    outputs = collect_and_write_candidate_pool(
        output_dir=tmp_path,
        config=load_filter_config(),
        runner=fake_runner,
        limit=20,
    )

    assert calls
    assert outputs["json_path"].exists()
    assert outputs["csv_path"].exists()

    data = json.loads(outputs["json_path"].read_text(encoding="utf-8"))
    assert data["候选统计"]["总扫描数"] == 3
    assert data["候选统计"]["进入候选池"] == 2
    assert [row["代币符号"] for row in data["候选列表"]] == ["GOOD", "WEAK"]

    with outputs["csv_path"].open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["代币符号"] == "GOOD"
    assert rows[0]["筛选等级"] == "S3_进入SIKK结构分析"
    assert rows[1]["代币符号"] == "WEAK"


def test_candidate_outputs_write_standard_time_anchors_and_first_seen_registry(tmp_path):
    from sikk_gmgn_new_token_filter import collect_and_write_candidate_pool, load_filter_config

    token = {
        **GOOD_TOKEN,
        "address": "Anchor111111111111111111111111111111111111",
        "symbol": "ANCH",
        "created_timestamp": 1770000000,
        "pool_created_at": 1770000123,
        "open_timestamp": 1770000300,
    }

    outputs = collect_and_write_candidate_pool(
        output_dir=tmp_path / "gmgn_new_token_filter",
        config=load_filter_config(),
        runner=lambda cmd: {"completed": [token], "new_creation": [], "near_completion": []},
        limit=1,
        now="2026-05-04T12:00:00Z",
        base_dir=tmp_path,
    )

    payload = json.loads(outputs["json_path"].read_text(encoding="utf-8"))
    row = payload["候选列表"][0]
    assert payload["candidate_batch_id"] == "RUN_20260504_120000"
    assert row["token_address"] == token["address"]
    assert row["token_symbol"] == "ANCH"
    assert row["token_open_time"] == "2026-02-02T02:45:00Z"
    assert row["pool_created_at"] == "2026-02-02T02:42:03Z"
    assert row["discovered_at"] == "2026-05-04T12:00:00Z"
    assert row["first_seen_at"] == "2026-05-04T12:00:00Z"
    assert row["last_seen_at"] == "2026-05-04T12:00:00Z"
    assert row["candidate_snapshot_at"] == "2026-05-04T12:00:00Z"
    assert row["candidate_batch_id"] == "RUN_20260504_120000"
    assert row["candidate_source"] == "gmgn_trenches:completed"

    registry_path = tmp_path / "time_context" / "token_first_seen_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_token = registry["tokens"][token["address"]]
    assert registry_token["first_seen_at"] == "2026-05-04T12:00:00Z"
    assert registry_token["last_seen_at"] == "2026-05-04T12:00:00Z"
    assert registry_token["first_candidate_batch_id"] == "RUN_20260504_120000"
    assert outputs["candidates_normalized_path"].exists()
    assert outputs["token_market_snapshot_path"].exists()
    assert outputs["token_first_seen_registry_path"].exists()
    normalized = json.loads(outputs["candidates_normalized_path"].read_text(encoding="utf-8"))
    assert normalized[0]["token_address"] == token["address"]
    assert normalized[0]["chain"] == "sol"
    assert normalized[0]["candidate_batch_id"] == "RUN_20260504_120000"
    assert "source_trace" in normalized[0]
    assert "field_quality" in normalized[0]
    snapshot = json.loads(outputs["token_market_snapshot_path"].read_text(encoding="utf-8"))
    assert snapshot["candidate_batch_id"] == "RUN_20260504_120000"
    assert snapshot["tokens"][0]["token_address"] == token["address"]

    collect_and_write_candidate_pool(
        output_dir=tmp_path / "gmgn_new_token_filter",
        config=load_filter_config(),
        runner=lambda cmd: {"completed": [token], "new_creation": [], "near_completion": []},
        limit=1,
        now="2026-05-04T12:05:00Z",
        base_dir=tmp_path,
    )
    registry2 = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_token2 = registry2["tokens"][token["address"]]
    assert registry_token2["first_seen_at"] == "2026-05-04T12:00:00Z"
    assert registry_token2["last_seen_at"] == "2026-05-04T12:05:00Z"
    assert registry_token2["last_candidate_batch_id"] == "RUN_20260504_120500"
