import json
import subprocess
import sys
from pathlib import Path

from modules.runtime.full_system_runner import FullSystemRuntimeRunner
from modules.runtime.wave_state_controller import WaveStateController


def _write_contract(root: Path, phase: str, fields: list[str]) -> None:
    contract_dir = root / "contracts" / phase
    contract_dir.mkdir(parents=True, exist_ok=True)
    (contract_dir / "input_contract.json").write_text(json.dumps({"required_fields": fields}))


def test_phase_runner_module_cli_is_canonical_replay_command(tmp_path):
    root = tmp_path / "repo"
    input_file = root / "tests" / "fixtures" / "phase_01" / "ready.json"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    input_file.write_text(json.dumps({"token_address": "Token111", "wallet_rows": []}))
    _write_contract(root, "phase_01", ["token_address", "wallet_rows"])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "modules.runtime.phase_runner",
            "--root",
            str(root),
            "--phase",
            "phase_01",
            "--mode",
            "replay",
            "--token",
            "Token111",
            "--replay",
            str(input_file),
        ],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "canonical_command=" in result.stdout
    assert "python3 -m modules.runtime.phase_runner --phase phase_01 --replay" in result.stdout
    output = root / "data" / "runtime" / "replay" / "Token111" / "phase_01" / "phase_01_handoff_packet.json"
    shared = root / "shared_handoff" / "phase_01" / "Token111" / "phase_01_handoff_packet.json"
    audit = root / "reports" / "runtime" / "replay" / "Token111" / "phase_01" / "audit_report.md"
    assert output.exists()
    assert shared.exists()
    assert audit.exists()
    assert json.loads(output.read_text())["current_phase"] == "phase_01_data_fact_layer"


def test_wave_state_controller_unlocks_next_wave_on_ready(tmp_path):
    root = tmp_path / "repo"
    controller = WaveStateController(root)

    result = controller.apply_wave_result(
        wave_id="wave_01_p01_p03",
        status="READY_WITH_GAPS",
        blocking_issues=[],
        degraded_issues=[{"issue_id": "OPTIONAL_GAP", "severity": "degraded"}],
    )

    wave_state = json.loads((root / "runtime_logs" / "full_system_runtime" / "wave_state.json").read_text())
    runtime_state = json.loads((root / "runtime_logs" / "full_system_runtime" / "runtime_task_state.json").read_text())
    assert result.next_allowed_task == "WAVE_02_P04_P05_SCENARIO_POSITION_RUNTIME"
    assert wave_state["wave_01_p01_p03"] == "READY_WITH_GAPS"
    assert wave_state["wave_02_p04_p05"] == "PENDING"
    assert runtime_state["next_allowed_task"] == "WAVE_02_P04_P05_SCENARIO_POSITION_RUNTIME"
    assert runtime_state["current_allowed_task"] == "WAVE_02_P04_P05_SCENARIO_POSITION_RUNTIME"


def test_wave_state_controller_preserves_already_completed_later_waves(tmp_path):
    root = tmp_path / "repo"
    runtime_dir = root / "runtime_logs" / "full_system_runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    (runtime_dir / "wave_state.json").write_text(
        json.dumps(
            {
                "wave_01_p01_p03": "READY_WITH_GAPS",
                "wave_02_p04_p05": "PENDING",
                "wave_03_p06_p07": "READY_WITH_GAPS",
                "wave_04_p08_p09": "READY_WITH_GAPS",
                "full_system_e2e": "READY_WITH_GAPS",
                "patch_and_regression": "READY_WITH_GAPS",
            }
        )
    )
    controller = WaveStateController(root)

    result = controller.apply_wave_result(
        wave_id="wave_02_p04_p05",
        status="READY_WITH_GAPS",
        blocking_issues=[],
        degraded_issues=[{"issue_id": "OPTIONAL_GAP", "severity": "degraded"}],
    )

    wave_state = json.loads((runtime_dir / "wave_state.json").read_text())
    assert result.next_allowed_task == "WAVE_03_P06_P07_STRATEGY_EXECUTION_RUNTIME"
    assert wave_state["wave_02_p04_p05"] == "READY_WITH_GAPS"
    assert wave_state["wave_03_p06_p07"] == "PENDING"
    assert wave_state["wave_04_p08_p09"] == "READY_WITH_GAPS"
    assert wave_state["full_system_e2e"] == "READY_WITH_GAPS"
    assert wave_state["patch_and_regression"] == "READY_WITH_GAPS"


def test_wave_state_controller_rejects_and_blocks_next_task(tmp_path):
    root = tmp_path / "repo"
    controller = WaveStateController(root)

    result = controller.apply_wave_result(
        wave_id="wave_01_p01_p03",
        status="REJECTED",
        blocking_issues=[{"issue_id": "PYTEST_FAILED", "severity": "blocker"}],
    )

    wave_state = json.loads((root / "runtime_logs" / "full_system_runtime" / "wave_state.json").read_text())
    runtime_state = json.loads((root / "runtime_logs" / "full_system_runtime" / "runtime_task_state.json").read_text())
    blocking = json.loads((root / "runtime_logs" / "full_system_runtime" / "current_blocking_issues.json").read_text())
    assert result.next_allowed_task == "FIX_CURRENT_BLOCKING_ISSUES"
    assert wave_state["wave_01_p01_p03"] == "REJECTED"
    assert wave_state["wave_02_p04_p05"] == "LOCKED"
    assert runtime_state["next_allowed_task"] == "FIX_CURRENT_BLOCKING_ISSUES"
    assert blocking[0]["issue_id"] == "PYTEST_FAILED"


def test_full_system_runner_syncs_runtime_state_and_reports_final_status(tmp_path):
    root = tmp_path / "repo"
    token = "Token111"

    result = FullSystemRuntimeRunner(root).run(mode="replay", token=token)

    runtime_state = json.loads((root / "runtime_logs" / "full_system_runtime" / "runtime_task_state.json").read_text())
    automation_result = json.loads((root / "reports" / "system_audit" / "full_system_automation_result.json").read_text())
    audit_text = (root / "reports" / "system_audit" / "full_system_automation_result.md").read_text()

    assert result["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert runtime_state["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert runtime_state["current_allowed_task"] == "FULL_SYSTEM_AUTOMATION_READY"
    assert runtime_state["next_allowed_task"] == "FULL_SYSTEM_AUTOMATION_READY"
    assert automation_result["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert automation_result["paper_only"] is True
    assert automation_result["real_trade_actions"] == []
    assert result["full_e2e"]["wave4_runtime_integrated"] is True
    assert result["full_e2e"]["patch_regression_integrated"] is True
    checkpoint = json.loads((root / "runtime_logs" / "full_system_runtime" / "checkpoint_state.json").read_text())
    assert checkpoint["resume_contract"]["checkpoint_controls_execution"] is True
    assert checkpoint["completed_waves"][-1] == "patch_and_regression"
    assert "paper_only" in audit_text or "纸面验证" in audit_text
    assert (root / "reports" / "system_audit" / "missing_gap_register.md").exists()

