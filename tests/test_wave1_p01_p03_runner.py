from pathlib import Path
import json

from modules.runtime.wave1_p01_p03_runner import run_wave1_p01_p03


ROOT = Path(__file__).resolve().parents[1]


def test_wave1_p01_p03_runner_executes_dry_run_and_writes_control_artifacts(tmp_path):
    result = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1", mode="dry-run")

    assert result["task_id"] == "task_1_wave_1_p01_p03_foundation_runtime"
    assert result["wave_id"] == "wave_1_p01_p03"
    assert result["execution_mode"] == "dry-run"
    assert result["safety_boundary"]["real_trade"] == "forbidden"
    assert result["safety_boundary"]["signing"] == "forbidden"
    assert result["safety_boundary"]["broadcast"] == "forbidden"
    assert result["safety_boundary"]["secret_read"] == "forbidden"
    assert result["final_status"] in {"WAVE1_READY", "WAVE1_READY_WITH_GAPS", "WAVE1_REJECTED"}
    assert result["blocking_issue_count"] == 0

    artifacts = result["artifacts"]
    required_keys = {
        "phase01_handoff",
        "phase02_handoff",
        "phase03_handoff",
        "wave1_result",
        "wave1_audit",
        "wave1_state",
        "wave1_handoff",
        "wave1_gap_register",
        "planbook_repository_index",
        "planbook_repository_audit",
    }
    assert required_keys.issubset(artifacts)
    for key in required_keys:
        assert Path(artifacts[key]).exists(), key

    handoff = json.loads(Path(artifacts["wave1_handoff"]).read_text(encoding="utf-8"))
    assert handoff["current_task"] == "task_1_wave_1_p01_p03_foundation_runtime"
    assert handoff["next_allowed_task"] == "task_2_wave_2_p04_p05_scene_position_runtime"
    assert handoff["handoff_status"] in {"HANDOFF_READY", "HANDOFF_DEGRADED", "HANDOFF_BLOCKED"}
    assert handoff["phase_statuses"]["phase_03_chip_control_controller"] in {
        "CONTROL_CONFIRMED",
        "CONTROL_WEAKENING",
        "PARTIAL_DISTRIBUTION",
        "ACTIVE_DISTRIBUTION",
        "TRANSFER_TO_COUNTERPARTY",
        "STRUCTURE_COLLAPSE",
        "UNKNOWN_CONTROL",
    }
    assert "phase_03_handoff_packet" in handoff["handoff_files"]
    assert "planbook_repository_index" in handoff["handoff_files"]
    assert "planbook_repository_audit" in handoff["handoff_files"]

    state = json.loads(Path(artifacts["wave1_state"]).read_text(encoding="utf-8"))
    assert state["task_id"] == result["task_id"]
    assert state["wave_id"] == "wave_1_p01_p03"
    assert state["status"] == result["final_status"]
    assert state["runtime_contract"]["failure_stop"] is True
    assert state["runtime_contract"]["audit_backfill"] is True
    assert state["runtime_contract"]["planbook_repository_read"] is True

    assert result["planbook_repository"]["final_status"] in {"PLANBOOK_REPOSITORY_READY", "PLANBOOK_REPOSITORY_READY_WITH_GAPS", "PLANBOOK_REPOSITORY_REJECTED"}
    assert Path(result["planbook_repository"]["index_path"]).exists()
    assert Path(result["planbook_repository"]["audit_path"]).exists()

    audit_text = Path(artifacts["wave1_audit"]).read_text(encoding="utf-8")
    assert "Task 1 / Wave 1 / P01-P03" in audit_text
    assert "真实交易: 禁止" in audit_text
    assert "phase_01_data_fact_controller" in audit_text
    assert "phase_02_wallet_structure_controller" in audit_text
    assert "phase_03_chip_control_controller" in audit_text
    assert "Planbook Repository" in audit_text


def test_wave1_p01_p03_runner_cli_smoke(tmp_path):
    import subprocess

    cmd = [
        "python3",
        "-m",
        "modules.runtime.wave1_p01_p03_runner",
        "--root",
        str(ROOT),
        "--output-dir",
        str(tmp_path / "cli_wave1"),
        "--mode",
        "dry-run",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    payload = json.loads(completed.stdout)
    assert payload["task_id"] == "task_1_wave_1_p01_p03_foundation_runtime"
    assert payload["final_status"] in {"WAVE1_READY", "WAVE1_READY_WITH_GAPS", "WAVE1_REJECTED"}
    assert Path(payload["artifacts"]["wave1_result"]).exists()
    assert Path(payload["artifacts"]["wave1_handoff"]).exists()
