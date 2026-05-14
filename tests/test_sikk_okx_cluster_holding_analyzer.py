import json
from pathlib import Path

from sikk_okx_cluster_holding_analyzer import analyze_okx_cluster_file, analyze_okx_cluster_payload


def test_okx_cluster_support_decision_from_payload():
    decision = analyze_okx_cluster_payload(
        {
            "token_address": "TCLUSTER1",
            "token_symbol": "CL1",
            "snapshot_time": "2026-05-03T00:00:00Z",
            "top300_wallet_count": 300,
            "market_pattern_type": "CONTROL_BOX_ACCUMULATION",
            "top300_total_holding_pct_delta": 1.5,
            "clusters": [
                {
                    "cluster_id": "C1",
                    "cluster_wallet_count": 18,
                    "cluster_holding_pct": 16.5,
                    "cluster_remaining_pct": 72,
                    "cluster_sold_pct": 12,
                    "cluster_sync_buy_score": 74,
                    "cluster_sync_sell_score": 22,
                    "cluster_holding_pct_delta": 0.8,
                    "cluster_avg_roi_pct": 38,
                }
            ],
        }
    )

    assert decision["okx_cluster_status"] == "CLUSTER_CONTROL_HOLDING"
    assert decision["paper_gate_effect"] == "SUPPORT_PAPER_ONLY_IF_OTHER_GATES_PASS"
    assert decision["dominant_cluster_role"] == "CONTROL_HOLDING_CLUSTER"
    assert decision["largest_cluster_holding_pct"] == 16.5
    assert "真实交易" in decision["scope_note"]


def test_okx_cluster_distribution_risk_decision():
    decision = analyze_okx_cluster_payload(
        {
            "token_address": "TCLUSTER2",
            "token_symbol": "CL2",
            "clusters": [
                {
                    "cluster_id": "C2",
                    "cluster_wallet_count": 11,
                    "cluster_holding_pct": 8,
                    "cluster_remaining_pct": 18,
                    "cluster_sold_pct": 82,
                    "cluster_sync_sell_score": 83,
                    "cluster_sold_pct_delta": 24,
                    "cluster_holding_pct_delta": -12,
                    "cluster_avg_roi_pct": 120,
                }
            ],
        }
    )

    assert decision["okx_cluster_status"] == "CLUSTER_DISTRIBUTION_RISK"
    assert decision["paper_gate_effect"] == "PAUSE_OR_EXIT_MONITOR_BY_OKX_CLUSTER"
    assert decision["okx_cluster_distribution_score"] >= 70
    assert decision["risk_flags"]


def test_okx_cluster_missing_is_degraded_not_crash():
    decision = analyze_okx_cluster_payload({"token_address": "TMISSING", "token_symbol": "MISS"})

    assert decision["okx_cluster_status"] == "OKX_CLUSTER_MISSING"
    assert decision["missing_fields"] == ["clusters"]
    assert decision["paper_gate_effect"] == "NO_OKX_CLUSTER_INPUT"


def test_okx_cluster_file_writes_standard_outputs(tmp_path):
    input_path = tmp_path / "cluster.json"
    input_path.write_text(
        json.dumps(
            {
                "token_address": "TFILE",
                "token_symbol": "FILE",
                "market_pattern_type": "SECOND_STAGE_EXPANSION",
                "second_stage_valid": True,
                "largest_cluster_holding_pct_delta": -2,
                "clusters": [
                    {
                        "cluster_id": "C1",
                        "cluster_wallet_count": 20,
                        "cluster_holding_pct": 14,
                        "cluster_remaining_pct": 69,
                        "cluster_sync_sell_score": 31,
                        "cluster_sold_pct_delta": 4,
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    paths = analyze_okx_cluster_file(input_path, tmp_path / "out")
    decision_path = Path(paths["okx_cluster_decision_json"])
    summary_path = Path(paths["okx_cluster_summary_json"])

    assert decision_path.exists()
    assert summary_path.exists()
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    assert decision["okx_cluster_status"] == "CLUSTER_SECOND_STAGE_SUPPORT"
    assert Path(paths["okx_cluster_summary_md"]).read_text(encoding="utf-8").count("paper-only") == 1
