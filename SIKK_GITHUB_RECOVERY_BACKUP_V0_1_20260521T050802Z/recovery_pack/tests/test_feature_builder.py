from __future__ import annotations

from pathlib import Path

from core.feature_builder import build_feature_snapshot

RUN_DIR = Path("data/runs/4pMsh7JF5wXjkx8sK6gJgv14xkBy1kUoMv4ixN8npump/skill_raw_handoff_probe")


def test_build_feature_snapshot_from_real_raw():
    snapshot, build_report, dq = build_feature_snapshot(RUN_DIR)
    assert snapshot["token_identity"]["address"]["value"] == "4pMsh7JF5wXjkx8sK6gJgv14xkBy1kUoMv4ixN8npump"
    assert snapshot["token_identity"]["symbol"]["value"] == "PIGEON"
    assert snapshot["market_snapshot"]["price_usd"]["missing"] is False
    assert snapshot["data_quality"]["required_fields_present"] is True
    assert snapshot["data_quality"]["feature_quality_score"] > 0
    assert snapshot["data_quality"]["can_generate_decision_ticket"] is True
    assert build_report["used_sources"]["rpc"] == "not_configured"
    assert "rpc.not_configured" in build_report["non_blocking_failures"]
    assert dq["rpc_status"] == "not_configured"


def test_gmgn_track_not_counted_as_token_specific_smart_wallet_count():
    snapshot, _, _ = build_feature_snapshot(RUN_DIR)
    smart = snapshot["wallet_basic"]["smart_wallet_count"]
    assert smart["source"] == "gmgn"
    assert smart["source_path"].endswith("raw/gmgn.json")
    assert smart["value"] is not None
