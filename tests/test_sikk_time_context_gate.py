from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_evaluate_time_context_gate_acceptance_rules():
    from sikk_time_context_gate import evaluate_time_context_gate

    now = "2026-05-04T10:00:00Z"
    synced = {
        "token_address": "ALLOW1",
        "token_symbol": "ALW",
        "time_bucket": "D1_ACTIVE",
        "token_open_time": "2026-05-04T09:56:59Z",
        "discovered_at": "2026-05-04T09:59:00Z",
        "candidate_snapshot_at": "2026-05-04T09:59:10Z",
        "latest_kline_time": "2026-05-04T09:59:20Z",
        "pattern_created_at": "2026-05-04T09:59:30Z",
        "wallet_decision_created_at": "2026-05-04T09:59:35Z",
        "alignment_created_at": "2026-05-04T09:59:40Z",
        "lifecycle_created_at": "2026-05-04T09:59:45Z",
        "intent_created_at": "2026-05-04T09:59:50Z",
        "quote_time": "2026-05-04T09:59:55Z",
        "security_scan_time": "2026-05-04T09:59:55Z",
        "final_gate_created_at": "2026-05-04T09:59:56Z",
        "signal_level": "S4",
        "signal_stale": False,
        "quote_stale": False,
    }
    out = evaluate_time_context_gate(synced, now=now)
    assert out["time_context_gate"] == "time_context_gate"
    assert out["temporal_sync_status"] == "TEMPORAL_SYNCED"
    assert out["temporal_gate"] == "TEMPORAL_ALLOW"
    assert out["time_context_score"] > 80
    assert out["requires_pattern_review"] is False

    d0 = dict(synced, token_address="D0", time_bucket="D0_SCOUT_ONLY", token_open_time="2026-05-04T09:59:50Z")
    assert evaluate_time_context_gate(d0, now=now)["temporal_gate"] == "TEMPORAL_WATCH"

    d4 = dict(synced, token_address="D4", time_bucket="D4_OLD_TOKEN", token_open_time="2026-05-03T20:00:00Z")
    d4_out = evaluate_time_context_gate(d4, now=now)
    assert d4_out["requires_pattern_review"] is True
    assert d4_out["temporal_gate"] != "TEMPORAL_BLOCK"

    quote_expired = dict(synced, token_address="QUOTE", quote_stale=True)
    assert evaluate_time_context_gate(quote_expired, now=now)["temporal_gate"] == "TEMPORAL_EXPIRED"

    stale_signal = dict(synced, token_address="SIG", signal_level="S3", signal_stale=True)
    assert evaluate_time_context_gate(stale_signal, now=now)["temporal_gate"] == "TEMPORAL_EXPIRED"

    desync = dict(synced, token_address="DESYNC", wallet_decision_created_at="2026-05-04T09:00:00Z")
    desync_out = evaluate_time_context_gate(desync, now=now)
    assert desync_out["temporal_sync_status"] == "TEMPORAL_DESYNC"
    assert desync_out["temporal_gate"] == "TEMPORAL_PAUSE"


def test_run_time_context_gate_writes_outputs_and_missing_stage_fields(tmp_path):
    from sikk_time_context_gate import run_time_context_gate

    base = tmp_path / "live"
    base.mkdir()
    live_state = {
        "last_update": "2026-05-04T10:00:00Z",
        "tokens": [
            {
                "token_address": "T1",
                "token_symbol": "ONE",
                "time_bucket": "D1_ACTIVE",
                "token_open_time": "2026-05-04T09:56:59Z",
                "discovered_at": "2026-05-04T09:59:00Z",
                "latest_kline_time": "2026-05-04T09:59:20Z",
                "wallet_structure": {"wallet_decision_created_at": "2026-05-04T09:59:35Z"},
                "quote": {"quote_time": "2026-05-04T09:59:55Z", "quote_stale": False},
                "security": {"security_scan_time": "2026-05-04T09:59:55Z"},
                "signal": {"signal_level": "S4", "signal_stale": False},
            },
            {
                "token_address": "T2",
                "token_symbol": "TWO",
                "time_bucket": "D4_OLD_TOKEN",
                "token_open_time": "2026-05-03T20:00:00Z",
                "discovered_at": "2026-05-04T08:00:00Z",
                "quote": {"quote_stale": True},
                "signal": {"signal_level": "S3", "signal_stale": False},
            },
        ],
    }
    (base / "live_state.json").write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")

    result = run_time_context_gate(base_dir=base, now="2026-05-04T10:00:00Z")
    out_dir = base / "time_context"
    for name in [
        "time_context_summary.json",
        "time_context_summary.csv",
        "time_context_report.md",
        "time_context_schema.json",
        "time_context_input_audit.json",
        "time_context_input_audit.md",
    ]:
        assert (out_dir / name).exists(), name

    payload = json.loads((out_dir / "time_context_summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["token_count"] == 2
    assert "stage_stale_counts" in payload["summary"]
    assert len(payload["tokens"]) == 2
    for row in payload["tokens"]:
        assert row["time_context_gate"] == "time_context_gate"
        assert row["temporal_gate"]
        assert isinstance(row["time_context_score"], (int, float))
        assert "stage_missing_fields" in row
    assert payload["tokens"][1]["requires_pattern_review"] is True
    assert payload["tokens"][1]["temporal_gate"] == "TEMPORAL_EXPIRED"

    audit = json.loads((out_dir / "time_context_input_audit.json").read_text(encoding="utf-8"))
    assert "token_before_dedup" in audit
    assert "field_availability" in audit

    with (out_dir / "time_context_summary.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["token_address"] == "T1"
    assert "stage_missing_fields_json" in rows[0]


def test_missing_candidates_json_does_not_crash(tmp_path):
    from sikk_time_context_gate import run_time_context_gate

    base = tmp_path / "live"
    base.mkdir()
    live_state = {
        "last_update": "2026-05-04T10:00:00Z",
        "tokens": [
            {
                "token_address": "A1",
                "token_symbol": "AAA",
                "time_bucket": "D1_ACTIVE",
                "token_open_time": "2026-05-04T09:56:59Z",
                "discovered_at": "2026-05-04T09:59:00Z",
                "signal": {"signal_level": "S4", "signal_stale": False},
            }
        ],
    }
    (base / "live_state.json").write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")

    result = run_time_context_gate(base_dir=base, now="2026-05-04T10:00:00Z")
    assert result["summary"]["token_count"] == 1
    assert (base / "time_context" / "time_context_summary.json").exists()


def test_missing_wallet_structure_decision_json_does_not_crash(tmp_path):
    from sikk_time_context_gate import run_time_context_gate

    base = tmp_path / "live"
    base.mkdir()
    (base / "live_state.json").write_text(
        json.dumps(
            {
                "last_update": "2026-05-04T10:00:00Z",
                "tokens": [
                    {
                        "token_address": "B1",
                        "token_symbol": "BBB",
                        "time_bucket": "D1_ACTIVE",
                        "token_open_time": "2026-05-04T09:56:59Z",
                        "discovered_at": "2026-05-04T09:59:00Z",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = run_time_context_gate(base_dir=base, now="2026-05-04T10:00:00Z")
    assert result["summary"]["token_count"] == 1
    assert (base / "time_context" / "time_context_summary.json").exists()
