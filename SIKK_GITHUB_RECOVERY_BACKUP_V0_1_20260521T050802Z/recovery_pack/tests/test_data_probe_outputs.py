import json
import subprocess
import sys
from pathlib import Path


def test_probe_outputs_without_config(tmp_path):
    token = "TEST_TOKEN_FOR_NOT_CONFIGURED_PROBE"
    run_id = "test_run"
    result = subprocess.run(
        [sys.executable, "scripts/run_real_data_probe.py", "--token", token, "--chain", "solana", "--run-id", run_id],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=True,
        env={},
    )
    assert "PROBE_FAILED" in result.stdout
    run_root = Path("data/runs") / token / run_id
    raw_root = run_root / "raw"
    expected = [
        raw_root / "gmgn.json",
        raw_root / "okx.json",
        raw_root / "rpc.json",
        raw_root / "error_report.json",
        raw_root / "data_source_coverage_report.json",
        run_root / "run_metadata.json",
    ]
    for path in expected:
        assert path.exists(), path

    metadata = json.loads((run_root / "run_metadata.json").read_text())
    assert metadata["mode"] == "paper_only"
    assert metadata["live_trading_enabled"] is False
    assert metadata["swap_allowed"] is False
    assert metadata["private_key_required"] is False

    gmgn = json.loads((raw_root / "gmgn.json").read_text())
    assert gmgn["source"] == "gmgn"
    assert gmgn["token_address"] == token
    assert gmgn["request_status"] == "not_configured"
    for key in ["fetch_ts", "raw_response", "normalized_probe_summary", "missing_fields", "errors"]:
        assert key in gmgn

    coverage = json.loads((raw_root / "data_source_coverage_report.json").read_text())
    assert coverage["gmgn_available"] is False
    assert coverage["okx_available"] is False
    assert coverage["rpc_available"] is False
    assert coverage["required_fields_present"] is False
    assert coverage["can_build_feature_snapshot"] is False
    assert coverage["recommended_next_status"] == "PROBE_FAILED"
