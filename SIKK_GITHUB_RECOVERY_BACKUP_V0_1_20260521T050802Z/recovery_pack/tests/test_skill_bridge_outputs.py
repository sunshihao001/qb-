import json
import subprocess
import sys
from pathlib import Path


def test_skill_bridge_outputs_when_raw_external_missing():
    token = "TEST_TOKEN_BRIDGE_MISSING"
    run_id = "bridge_missing"
    subprocess.run(
        [sys.executable, "scripts/validate_external_raw_probe.py", "--token", token, "--chain", "solana", "--run-id", run_id],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=True,
    )
    raw_root = Path("data/runs") / token / run_id / "raw"
    for name in ["gmgn.json", "okx.json", "rpc.json", "error_report.json", "data_source_coverage_report.json"]:
        assert (raw_root / name).exists()
    gmgn = json.loads((raw_root / "gmgn.json").read_text())
    coverage = json.loads((raw_root / "data_source_coverage_report.json").read_text())
    assert gmgn["request_status"] == "external_raw_missing"
    assert coverage["external_raw_used"] is True
    assert coverage["can_build_feature_snapshot"] is False


def test_skill_bridge_outputs_with_partial_external_success():
    token = "TEST_TOKEN_BRIDGE_PARTIAL"
    run_id = "bridge_partial"
    run_root = Path("data/runs") / token / run_id
    raw_external = run_root / "raw_external"
    raw_external.mkdir(parents=True, exist_ok=True)
    (raw_external / "gmgn_token.json").write_text(json.dumps({
        "source": "gmgn",
        "source_type": "hermes_skill_handoff",
        "actual_skill_used": "gmgn-token",
        "operation_used": "query_token",
        "token_address": token,
        "fetch_ts": "2026-01-01T00:00:00+00:00",
        "request_status": "success",
        "raw_response": {"price_usd": 1},
        "errors": []
    }), encoding="utf-8")
    subprocess.run(
        [sys.executable, "scripts/validate_external_raw_probe.py", "--token", token, "--chain", "solana", "--run-id", run_id],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=True,
    )
    raw_root = run_root / "raw"
    gmgn = json.loads((raw_root / "gmgn.json").read_text())
    coverage = json.loads((raw_root / "data_source_coverage_report.json").read_text())
    assert gmgn["request_status"] == "external_raw_invalid"
    assert coverage["field_coverage_score"] > 0
    assert coverage["can_build_feature_snapshot"] is False
