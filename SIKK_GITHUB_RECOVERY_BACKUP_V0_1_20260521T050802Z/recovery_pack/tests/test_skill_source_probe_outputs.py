import json
import subprocess
import sys
from pathlib import Path


def test_skill_source_probe_outputs_when_skills_missing():
    token = "TEST_TOKEN_SKILL_SOURCE"
    run_id = "skill_missing"
    subprocess.run(
        [sys.executable, "scripts/run_real_data_probe.py", "--token", token, "--chain", "solana", "--run-id", run_id],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=True,
        env={},
    )
    run_root = Path("data/runs") / token / run_id
    raw_root = run_root / "raw"
    for name in ["gmgn.json", "okx.json", "rpc.json", "error_report.json", "data_source_coverage_report.json"]:
        assert (raw_root / name).exists()
    assert (run_root / "run_metadata.json").exists()

    gmgn = json.loads((raw_root / "gmgn.json").read_text())
    okx = json.loads((raw_root / "okx.json").read_text())
    assert gmgn["source"] == "gmgn"
    assert gmgn["source_type"] == "hermes_skill"
    assert gmgn["actual_skill_used"] == "gmgn-token"
    assert gmgn["request_status"] in {"skill_not_found", "not_configured", "failed", "capability_detected_not_invokable"}
    assert gmgn["request_status"] != "success"
    assert gmgn["operation_used"] == "query_token"
    assert okx["source"] == "okx"
    assert okx["source_type"] == "hermes_skill"
    assert okx["actual_skill_used"] == "okx-dex-token"
    assert okx["request_status"] in {"skill_not_found", "not_configured", "failed", "capability_detected_not_invokable"}
    assert okx["request_status"] != "success"
    assert okx["operation_used"] == "query_token"

    coverage = json.loads((raw_root / "data_source_coverage_report.json").read_text())
    assert "gmgn_source_type" in coverage
    assert "okx_source_type" in coverage
    assert "gmgn_skill_available" in coverage
    assert "okx_skill_available" in coverage
    assert "unsafe_operation_blocked_count" in coverage
    assert coverage["can_build_feature_snapshot"] is False
