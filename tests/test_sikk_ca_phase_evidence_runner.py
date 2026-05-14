import json
from pathlib import Path

from tests.test_sikk_ca_runtime_pipeline import TOKEN, _snapshot, _write_json


def test_ca_phase_evidence_runner_writes_p01_p09_packages(tmp_path):
    from sikk_ca_phase_evidence_runner import run_ca_phase_evidence

    token_root = tmp_path / "data" / "source_wallet_bot" / "live" / TOKEN
    snapshot_path = token_root / "structure_analysis" / "intelligence" / "agi_structural_snapshot.json"
    _write_json(snapshot_path, _snapshot())

    result = run_ca_phase_evidence(
        token_address=TOKEN,
        snapshot_path=snapshot_path,
        output_root=token_root / "phase_runtime" / "test_run",
        mode="live",
        run_id="test_run",
        project_root=tmp_path,
    )

    assert result["status"] in {"OK", "READY_WITH_GAPS"}
    expected_keys = {
        "master_phase_ledger_jsonl",
        "gap_register_json",
        "completion_audit_json",
        "final_phase_report_md",
    }
    assert expected_keys.issubset(result)
    for key in expected_keys:
        assert Path(result[key]).exists(), key

    root = Path(result["output_root"])
    phases = result["phases"]
    assert len(phases) == 9
    for phase in phases:
        phase_dir = root / phase["phase_id"]
        assert phase_dir.exists(), phase["phase_id"]
        for filename in ["input.json", "output.json", "evidence.json", "handoff_packet.json", "audit.json"]:
            path = phase_dir / filename
            assert path.exists(), f"{phase['phase_id']} {filename}"
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["token_address"] == TOKEN
            assert payload["safety_boundary"]["real_trade_enabled"] is False

    ledger_rows = [json.loads(line) for line in Path(result["master_phase_ledger_jsonl"]).read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(ledger_rows) == 9
    assert ledger_rows[0]["phase_id"] == "P01_data_fact"
    assert ledger_rows[-1]["phase_id"] == "P09_system_upgrade"

    gaps = json.loads(Path(result["gap_register_json"]).read_text(encoding="utf-8"))
    gap_ids = {gap["gap_id"] for gap in gaps["gaps"]}
    assert "P01_FUNDING_PATH_MISSING" in gap_ids
    assert "P05_POSITION_DATA_MISSING" in gap_ids

    completion = json.loads(Path(result["completion_audit_json"]).read_text(encoding="utf-8"))
    assert completion["phase_count"] == 9
    assert completion["ca_consistency_passed"] is True
    assert completion["safety_boundary_passed"] is True
    assert completion["overall_passed"] is True

    report = Path(result["final_phase_report_md"]).read_text(encoding="utf-8")
    assert "P01-P09" in report
    assert "真实交易：禁止" in report
    assert "资金路径缺失" in report


def test_ca_phase_evidence_runner_blocks_mismatched_ca(tmp_path):
    from sikk_ca_phase_evidence_runner import run_ca_phase_evidence

    actual = "Different111111111111111111111111111111111111pump"
    snapshot_path = tmp_path / "snapshot.json"
    _write_json(snapshot_path, _snapshot(actual))

    result = run_ca_phase_evidence(
        token_address=TOKEN,
        snapshot_path=snapshot_path,
        output_root=tmp_path / "phase_runtime" / "bad",
        mode="live",
        run_id="bad",
        project_root=tmp_path,
    )

    assert result["status"] == "BLOCKED_CA_MISMATCH"
    completion = json.loads(Path(result["completion_audit_json"]).read_text(encoding="utf-8"))
    assert completion["overall_passed"] is False
    assert completion["ca_consistency_passed"] is False
    permission = json.loads(Path(result["permission_gate_json"]).read_text(encoding="utf-8"))
    assert permission["real_trade_enabled"] is False
    assert permission["permission_status"] == "CA_MISMATCH_BLOCKED"
