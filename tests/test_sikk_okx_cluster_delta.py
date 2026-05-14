import json
from pathlib import Path

from sikk_okx_cluster_delta import (
    build_okx_cluster_delta,
    build_okx_cluster_failure_attribution_event,
    write_okx_cluster_delta_outputs,
)


def _support_snapshot():
    return {
        "token_address": "TDELTA1",
        "token_symbol": "DLT",
        "snapshot_time": "2026-05-03T00:00:00Z",
        "okx_cluster_status": "CLUSTER_CONTROL_HOLDING",
        "largest_cluster_holding_pct": 18.0,
        "top300_total_holding_pct": 52.0,
        "cluster_total_holding_pct": 31.0,
        "cluster_sync_sell_score": 18,
        "okx_cluster_distribution_score": 20,
        "okx_cluster_control_retention_score": 88,
        "okx_cluster_risk_score": 12,
    }


def test_okx_cluster_delta_detects_distribution_risk_from_multi_snapshots():
    delta = build_okx_cluster_delta(
        _support_snapshot(),
        {
            "token_address": "TDELTA1",
            "token_symbol": "DLT",
            "snapshot_time": "2026-05-03T00:05:00Z",
            "okx_cluster_status": "CLUSTER_DISTRIBUTION_RISK",
            "largest_cluster_holding_pct": 8.5,
            "top300_total_holding_pct": 39.0,
            "cluster_total_holding_pct": 18.0,
            "cluster_sync_sell_score": 76,
            "okx_cluster_distribution_score": 82,
            "okx_cluster_control_retention_score": 41,
            "okx_cluster_risk_score": 85,
        },
        observed_at="2026-05-03T00:06:00Z",
    )

    assert delta["token_address"] == "TDELTA1"
    assert delta["previous_okx_cluster_status"] == "CLUSTER_CONTROL_HOLDING"
    assert delta["current_okx_cluster_status"] == "CLUSTER_DISTRIBUTION_RISK"
    assert delta["largest_cluster_holding_pct_delta_round"] == -9.5
    assert delta["top300_total_holding_pct_delta_round"] == -13.0
    assert "OKX_CLUSTER_STATUS_FLIPPED_FROM_SUPPORT_TO_RISK" in delta["okx_cluster_delta_flags"]
    assert "CLUSTER_SYNC_SELL_SCORE_SPIKED" in delta["okx_cluster_delta_flags"]
    assert delta["okx_cluster_failure_type"] == "CLUSTER_DISTRIBUTION_ACTIVE"
    assert delta["recommended_paper_action"] == "FORCE_PAPER_EXIT"
    assert "真实交易" in delta["scope_note"]


def test_okx_cluster_delta_no_risk_keeps_hold_for_paper_only():
    delta = build_okx_cluster_delta(
        _support_snapshot(),
        {
            **_support_snapshot(),
            "snapshot_time": "2026-05-03T00:05:00Z",
            "largest_cluster_holding_pct": 18.4,
            "top300_total_holding_pct": 52.6,
            "cluster_sync_sell_score": 20,
            "okx_cluster_distribution_score": 22,
            "okx_cluster_control_retention_score": 90,
        },
    )

    assert delta["okx_cluster_delta_flags"] == []
    assert delta["okx_cluster_failure_type"] == "NO_OKX_CLUSTER_FAILURE"
    assert delta["recommended_paper_action"] == "HOLD"


def test_failure_attribution_event_uses_okx_cluster_delta_without_real_sell():
    delta = build_okx_cluster_delta(
        _support_snapshot(),
        {
            **_support_snapshot(),
            "snapshot_time": "2026-05-03T00:07:00Z",
            "okx_cluster_status": "CLUSTER_COUNTERPARTY_ABSORBING",
            "largest_cluster_holding_pct": 15.0,
            "cluster_sync_sell_score": 25,
            "okx_cluster_distribution_score": 28,
            "okx_cluster_control_retention_score": 62,
        },
        observed_at="2026-05-03T00:08:00Z",
    )
    event = build_okx_cluster_failure_attribution_event(delta, event_time="2026-05-03T00:08:30Z")

    assert event["事件类型"] == "EXIT_MONITOR"
    assert event["failure_type"] == "COUNTERPARTY_ABSORBING"
    assert event["okx_cluster_failure_type"] == "COUNTERPARTY_ABSORBING"
    assert event["current_okx_cluster_status"] == "CLUSTER_COUNTERPARTY_ABSORBING"
    assert "真实卖出" in event["scope_note"]


def test_okx_cluster_delta_outputs_are_written(tmp_path):
    prev = tmp_path / "prev.json"
    cur = tmp_path / "cur.json"
    prev.write_text(json.dumps(_support_snapshot(), ensure_ascii=False), encoding="utf-8")
    cur.write_text(
        json.dumps(
            {
                **_support_snapshot(),
                "snapshot_time": "2026-05-03T00:05:00Z",
                "okx_cluster_status": "CLUSTER_DISTRIBUTION_RISK",
                "largest_cluster_holding_pct": 8.0,
                "cluster_sync_sell_score": 80,
                "okx_cluster_distribution_score": 86,
                "okx_cluster_control_retention_score": 35,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    paths = write_okx_cluster_delta_outputs(prev, cur, tmp_path / "out", observed_at="2026-05-03T00:10:00Z")

    assert Path(paths["okx_cluster_delta_json"]).exists()
    assert Path(paths["okx_cluster_failure_attribution_jsonl"]).exists()
    summary = json.loads(Path(paths["okx_cluster_delta_summary_json"]).read_text(encoding="utf-8"))
    assert summary["paper_only"] is True
    event_line = Path(paths["okx_cluster_failure_attribution_jsonl"]).read_text(encoding="utf-8").strip()
    assert "CLUSTER_DISTRIBUTION_ACTIVE" in event_line
