from pathlib import Path
import json

from modules.runtime.wave1_p01_p03_runner import run_wave1_p01_p03
from modules.runtime.wave2_p04_p05_runner import run_wave2_p04_p05
from modules.runtime.wave3_p06_p07_runner import run_wave3_p06_p07


ROOT = Path(__file__).resolve().parents[1]


def test_wave3_p06_p07_runner_executes_from_wave2_handoff_and_writes_control_artifacts(tmp_path):
    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2",
        mode="dry-run",
    )

    result = run_wave3_p06_p07(
        root=ROOT,
        wave2_handoff_file=wave2["artifacts"]["wave2_handoff"],
        output_dir=tmp_path / "wave3",
        mode="dry-run",
    )

    assert result["task_id"] == "task_3_wave_3_p06_p07_strategy_execution_risk_runtime"
    assert result["wave_id"] == "wave_3_p06_p07"
    assert result["execution_mode"] == "dry-run"
    assert result["safety_boundary"]["real_trade"] == "forbidden"
    assert result["safety_boundary"]["signing"] == "forbidden"
    assert result["safety_boundary"]["broadcast"] == "forbidden"
    assert result["safety_boundary"]["secret_read"] == "forbidden"
    assert result["final_status"] in {"WAVE3_READY", "WAVE3_READY_WITH_GAPS", "WAVE3_REJECTED"}
    assert result["blocking_issue_count"] == 0

    artifacts = result["artifacts"]
    required_keys = {
        "phase06_handoff",
        "phase07_handoff",
        "wave3_result",
        "wave3_audit",
        "wave3_state",
        "wave3_handoff",
        "wave3_gap_register",
        "wave3_execution_trace",
    }
    assert required_keys.issubset(artifacts)
    for key in required_keys:
        assert Path(artifacts[key]).exists(), key

    handoff = json.loads(Path(artifacts["wave3_handoff"]).read_text(encoding="utf-8"))
    assert handoff["current_task"] == "task_3_wave_3_p06_p07_strategy_execution_risk_runtime"
    assert handoff["next_allowed_task"] == "task_4_wave_4_p08_p09_review_learning_runtime"
    assert handoff["handoff_status"] in {"HANDOFF_READY", "HANDOFF_DEGRADED", "HANDOFF_BLOCKED"}
    assert "phase_06_handoff_packet" in handoff["handoff_files"]
    assert "phase_07_handoff_packet" in handoff["handoff_files"]
    assert "inherited_wave2_gap_register" in handoff["handoff_files"]

    state = json.loads(Path(artifacts["wave3_state"]).read_text(encoding="utf-8"))
    assert state["task_id"] == result["task_id"]
    assert state["wave_id"] == "wave_3_p06_p07"
    assert state["status"] == result["final_status"]
    assert state["runtime_contract"]["failure_stop"] is True
    assert state["runtime_contract"]["audit_backfill"] is True
    assert state["runtime_contract"]["regression_repair"] is True

    audit_text = Path(artifacts["wave3_audit"]).read_text(encoding="utf-8")
    assert "Task 3 / Wave 3 / P06-P07" in audit_text
    assert "真实交易: 禁止" in audit_text
    assert "phase_06_strategy_gate_controller" in audit_text
    assert "phase_07_execution_risk_controller" in audit_text


def test_wave3_p06_p07_runner_cli_smoke(tmp_path):
    import subprocess

    wave1 = run_wave1_p01_p03(root=ROOT, output_dir=tmp_path / "wave1_cli_seed", mode="dry-run")
    wave2 = run_wave2_p04_p05(
        root=ROOT,
        wave1_handoff_file=wave1["artifacts"]["wave1_handoff"],
        output_dir=tmp_path / "wave2_cli_seed",
        mode="dry-run",
    )
    cmd = [
        "python3",
        "-m",
        "modules.runtime.wave3_p06_p07_runner",
        "--root",
        str(ROOT),
        "--wave2-handoff-file",
        wave2["artifacts"]["wave2_handoff"],
        "--output-dir",
        str(tmp_path / "cli_wave3"),
        "--mode",
        "dry-run",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    payload = json.loads(completed.stdout)
    assert payload["task_id"] == "task_3_wave_3_p06_p07_strategy_execution_risk_runtime"
    assert payload["final_status"] in {"WAVE3_READY", "WAVE3_READY_WITH_GAPS", "WAVE3_REJECTED"}
    assert payload["blocking_issue_count"] == 0
    assert Path(payload["artifacts"]["wave3_result"]).exists()
    assert Path(payload["artifacts"]["wave3_handoff"]).exists()
