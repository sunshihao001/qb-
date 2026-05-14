import json
import subprocess
import sys


def test_full_system_runner_cli_is_canonical_automation_entry_and_writes_acceptance_handoff(tmp_path):
    root = tmp_path / "repo"
    token = "Token111"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "modules.runtime.full_system_runner",
            "--root",
            str(root),
            "--mode",
            "replay",
            "--token",
            token,
        ],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    stdout = json.loads(result.stdout)
    assert stdout["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert "canonical_command" in stdout
    assert "python3 -m modules.runtime.full_system_runner" in stdout["canonical_command"]
    assert stdout["acceptance_path"].endswith("reports/system_audit/full_system_automation_acceptance.json")
    assert stdout["handoff_path"].endswith("handoffs/stable_trader_os/full_system_runtime_handoff.json")

    acceptance = json.loads((root / "reports/system_audit/full_system_automation_acceptance.json").read_text())
    handoff = json.loads((root / "handoffs/stable_trader_os/full_system_runtime_handoff.json").read_text())
    current_state = json.loads((root / "sikk_stable_trader_os/09_runtime_state/current_system_state.json").read_text())
    journal = (root / "research_loop/total_control/execution_journal.md").read_text()

    assert acceptance["acceptance_status"] == "PASS_WITH_DEGRADED_GAPS"
    assert acceptance["automation_result_path"] == "reports/system_audit/full_system_automation_result.json"
    assert acceptance["required_runtime_artifacts_verified"] is True
    assert handoff["handoff_status"] == "READY_WITH_DEGRADED_GAPS"
    assert handoff["next_runtime_step"] == "live_input_adapter_or_business_logic_integration"
    assert current_state["runtime_automation_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert current_state["runtime_boundary"] == "OBSERVE_PAPER_ONLY"
    assert "Full System Automation Runtime Replay" in journal
