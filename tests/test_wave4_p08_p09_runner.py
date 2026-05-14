from pathlib import Path
import json

from modules.runtime.wave1_p01_p03_runner import run_wave1_p01_p03
from modules.runtime.wave2_p04_p05_runner import run_wave2_p04_p05
from modules.runtime.wave3_p06_p07_runner import run_wave3_p06_p07
from modules.runtime.wave4_p08_p09_runner import run_wave4_p08_p09


ROOT = Path(__file__).resolve().parents[1]


def test_wave4_p08_p09_runner_executes_from_wave3_handoff_and_writes_control_artifacts(tmp_path):
    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2",
        mode="dry-run",
    )
    wave3 = run_wave3_p06_p07(
        root=ROOT,
        wave2_handoff_file=wave2["artifacts"]["wave2_handoff"],
        output_dir=tmp_path / "wave3",
        mode="dry-run",
    )

    result = run_wave4_p08_p09(
        root=ROOT,
        wave3_handoff_file=wave3["artifacts"]["wave3_handoff"],
        output_dir=tmp_path / "wave4",
        mode="dry-run",
    )

    assert result["task_id"] == "task_4_wave_4_p08_p09_review_learning_runtime"
    assert result["wave_id"] == "wave_4_p08_p09"
    assert result["execution_mode"] == "dry-run"
    assert result["safety_boundary"]["real_trade"] == "forbidden"
    assert result["safety_boundary"]["signing"] == "forbidden"
    assert result["safety_boundary"]["broadcast"] == "forbidden"
    assert result["safety_boundary"]["secret_read"] == "forbidden"
    assert result["safety_boundary"]["runtime_apply"] == "forbidden"
    assert result["safety_boundary"]["strategy_auto_modify"] == "forbidden"
    assert result["final_status"] in {"WAVE4_READY", "WAVE4_READY_WITH_GAPS", "WAVE4_REJECTED"}
    assert result["blocking_issue_count"] == 0

    artifacts = result["artifacts"]
    required_keys = {
        "phase08_handoff",
        "phase09_handoff",
        "wave4_result",
        "wave4_audit",
        "wave4_state",
        "wave4_handoff",
        "wave4_gap_register",
        "wave4_execution_trace",
    }
    assert required_keys.issubset(artifacts)
    for key in required_keys:
        assert Path(artifacts[key]).exists(), key

    handoff = json.loads(Path(artifacts["wave4_handoff"]).read_text(encoding="utf-8"))
    assert handoff["current_task"] == "task_4_wave_4_p08_p09_review_learning_runtime"
    assert handoff["next_allowed_task"] == "task_5_full_system_e2e_runtime"
    assert handoff["handoff_status"] in {"HANDOFF_READY", "HANDOFF_DEGRADED", "HANDOFF_BLOCKED"}
    assert handoff["runtime_apply_allowed"] is False
    assert handoff["requires_manual_confirmation"] is True
    assert "phase_08_handoff_packet" in handoff["handoff_files"]
    assert "phase_09_handoff_packet" in handoff["handoff_files"]
    assert "inherited_wave3_gap_register" in handoff["handoff_files"]

    phase09_handoff = json.loads(Path(artifacts["phase09_handoff"]).read_text(encoding="utf-8"))
    assert phase09_handoff["allow_apply_to_runtime"] is False
    assert phase09_handoff["requires_manual_confirmation"] is True
    assert phase09_handoff["recommended_apply_mode"] == "SHADOW_MODE_FIRST"

    state = json.loads(Path(artifacts["wave4_state"]).read_text(encoding="utf-8"))
    assert state["task_id"] == result["task_id"]
    assert state["wave_id"] == "wave_4_p08_p09"
    assert state["status"] == result["final_status"]
    assert state["runtime_contract"]["failure_stop"] is True
    assert state["runtime_contract"]["audit_backfill"] is True
    assert state["runtime_contract"]["regression_repair"] is True
    assert state["runtime_contract"]["review_only"] is True

    audit_text = Path(artifacts["wave4_audit"]).read_text(encoding="utf-8")
    assert "Task 4 / Wave 4 / P08-P09" in audit_text
    assert "真实交易: 禁止" in audit_text
    assert "runtime_apply: 禁止" in audit_text
    assert "phase_08_review_learning_controller" in audit_text
    assert "phase_09_system_upgrade_controller" in audit_text


def test_wave4_p08_p09_runner_cli_smoke(tmp_path):
    import subprocess

    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1_cli_seed", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2_cli_seed",
        mode="dry-run",
    )
    wave3 = run_wave3_p06_p07(
        root=ROOT,
        wave2_handoff_file=wave2["artifacts"]["wave2_handoff"],
        output_dir=tmp_path / "wave3_cli_seed",
        mode="dry-run",
    )
    cmd = [
        "python3",
        "-m",
        "modules.runtime.wave4_p08_p09_runner",
        "--root",
        str(ROOT),
        "--wave3-handoff-file",
        wave3["artifacts"]["wave3_handoff"],
        "--output-dir",
        str(tmp_path / "cli_wave4"),
        "--mode",
        "dry-run",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    payload = json.loads(completed.stdout)
    assert payload["task_id"] == "task_4_wave_4_p08_p09_review_learning_runtime"
    assert payload["final_status"] in {"WAVE4_READY", "WAVE4_READY_WITH_GAPS", "WAVE4_REJECTED"}
    assert payload["blocking_issue_count"] == 0
    assert Path(payload["artifacts"]["wave4_result"]).exists()
    assert Path(payload["artifacts"]["wave4_handoff"]).exists()



def test_wave4_p08_p09_runner_materializes_full_phase07_handoff_and_evidence_chain(tmp_path):
    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1_exposure", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2_exposure",
        mode="dry-run",
    )
    wave3 = run_wave3_p06_p07(
        root=ROOT,
        wave2_handoff_file=wave2["artifacts"]["wave2_handoff"],
        output_dir=tmp_path / "wave3_exposure",
        mode="dry-run",
    )

    result = run_wave4_p08_p09(
        root=ROOT,
        wave3_handoff_file=wave3["artifacts"]["wave3_handoff"],
        output_dir=tmp_path / "wave4_exposure",
        mode="dry-run",
    )

    exposed_phase07 = Path(result["upstream"]["phase07_handoff_file"])
    assert exposed_phase07.exists()
    assert exposed_phase07.is_relative_to(tmp_path / "wave4_exposure" / "inputs")
    phase07_handoff = json.loads(exposed_phase07.read_text(encoding="utf-8"))
    required = phase07_handoff["required_files_for_next_stage"]
    expected_upstream_keys = {
        "data_quality_summary",
        "wallet_structure_decision",
        "chip_control_summary",
        "primary_scenario",
        "structure_position_decision",
        "strategy_gate_decision",
        "execution_risk_decision",
        "paper_trade_decision",
        "paper_positions_open",
        "paper_positions_closed",
        "paper_trades",
        "risk_events",
    }
    assert expected_upstream_keys.issubset(required)
    for key in expected_upstream_keys:
        assert Path(required[key]).exists(), key

    phase08_handoff = json.loads(Path(result["artifacts"]["phase08_handoff"]).read_text(encoding="utf-8"))
    evidence_path = Path(phase08_handoff["required_files_for_next_stage"]["evidence_chain_manifest"])
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence["evidence_chain_status"] != "EVIDENCE_CHAIN_BLOCKED"
    assert evidence["required_phase_count"] == 7
    assert evidence["present_phase_count"] >= 7
    assert {link["source_key"] for link in evidence["links"]} >= {
        "data_quality_summary",
        "wallet_structure_decision",
        "chip_control_summary",
        "primary_scenario",
        "structure_position_decision",
        "strategy_gate_decision",
        "execution_risk_decision",
    }
    assert all(Path(link["source_path"]).exists() for link in evidence["links"])
    assert not any(issue.get("code") in {"phase08_degrade_reason", "phase08_missing_fields"} for issue in result["issues"])


def test_wave4_p08_p09_runner_exposes_phase09_known_success_regression_rollback_shadow_artifacts(tmp_path):
    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1_p09", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2_p09",
        mode="dry-run",
    )
    wave3 = run_wave3_p06_p07(
        root=ROOT,
        wave2_handoff_file=wave2["artifacts"]["wave2_handoff"],
        output_dir=tmp_path / "wave3_p09",
        mode="dry-run",
    )

    result = run_wave4_p08_p09(
        root=ROOT,
        wave3_handoff_file=wave3["artifacts"]["wave3_handoff"],
        output_dir=tmp_path / "wave4_p09",
        mode="dry-run",
    )

    assert "phase09_artifacts" in result["artifacts"]
    phase09_artifact_manifest = json.loads(Path(result["artifacts"]["phase09_artifacts"]).read_text(encoding="utf-8"))
    expected_keys = {
        "known_success_preservation_review",
        "regression_validation_report",
        "rollback_validation_plan",
        "shadow_mode_plan",
        "system_upgrade_package",
        "upgrade_input_validation",
    }
    assert expected_keys.issubset(phase09_artifact_manifest)
    for key in expected_keys:
        assert Path(phase09_artifact_manifest[key]).exists(), key

    known_success = json.loads(Path(phase09_artifact_manifest["known_success_preservation_review"]).read_text(encoding="utf-8"))
    regression = json.loads(Path(phase09_artifact_manifest["regression_validation_report"]).read_text(encoding="utf-8"))
    rollback = json.loads(Path(phase09_artifact_manifest["rollback_validation_plan"]).read_text(encoding="utf-8"))
    shadow = json.loads(Path(phase09_artifact_manifest["shadow_mode_plan"]).read_text(encoding="utf-8"))
    assert known_success["known_success_case_count"] >= 1
    assert regression["known_success_case_count"] >= 1
    assert regression["regression_status"] != "REGRESSION_BLOCKED"
    assert rollback["allow_runtime_apply"] is False
    assert shadow["allow_runtime_apply"] is False
    assert not any(issue.get("code") == "phase09_system_upgrade_blocked_gap_aware_progression" for issue in result["issues"])
