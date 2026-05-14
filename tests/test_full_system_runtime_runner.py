import json
from pathlib import Path

from modules.runtime.full_system_runner import FullSystemRuntimeRunner


def test_full_system_runner_replays_p01_to_p09_and_updates_waves(tmp_path):
    root = tmp_path / "repo"
    token = "Token111"
    result = FullSystemRuntimeRunner(root).run(mode="replay", token=token)

    assert result["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert result["paper_only"] is True
    assert result["real_trade_actions"] == []
    assert [wave["wave_id"] for wave in result["waves"]] == [
        "wave_01_p01_p03",
        "wave_02_p04_p05",
        "wave_03_p06_p07",
        "wave_04_p08_p09",
        "full_system_e2e",
        "patch_and_regression",
    ]
    assert result["full_e2e"]["wave4_runtime_integrated"] is True
    assert result["full_e2e"]["patch_regression_integrated"] is True
    assert result["resume_contract"]["resume_from_checkpoint_supported"] is True
    assert "wave4_p08_p09" in result["wave_runtime_artifacts"]
    assert "patch_and_regression" in result["wave_runtime_artifacts"]

    for phase_no in range(1, 10):
        phase = f"phase_{phase_no:02d}"
        handoff = root / "shared_handoff" / phase / token / f"{phase}_handoff_packet.json"
        assert handoff.exists(), f"missing shared handoff for {phase}"
        payload = json.loads(handoff.read_text())
        assert payload["token_address"] == token
        assert payload["source_files"]
        assert payload["handoff_to"]
        assert "real_trade" not in json.dumps(payload).lower()

    wave_state = json.loads((root / "runtime_logs/full_system_runtime/wave_state.json").read_text())
    assert wave_state["patch_and_regression"] == "READY_WITH_GAPS"

    result_path = root / "reports/system_audit/full_system_automation_result.json"
    audit_path = root / "reports/system_audit/full_system_automation_result.md"
    assert result_path.exists()
    assert audit_path.exists()
    assert json.loads(result_path.read_text())["final_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert "纸面验证" in audit_path.read_text()


def test_full_system_runner_resume_skips_completed_phase_chain_and_records_reused_artifacts(tmp_path):
    root = tmp_path / "repo"
    token = "Token111"
    first = FullSystemRuntimeRunner(root).run(mode="replay", token=token)
    first_phase_01_path = Path(first["phases"][0]["output_path"])
    first_phase_01_payload = json.loads(first_phase_01_path.read_text())

    resumed = FullSystemRuntimeRunner(root).run(mode="replay", token=token, resume_from_checkpoint=True)

    assert resumed["resume_from_checkpoint"] is True
    assert resumed["resume_cursor"] == "patch_and_regression"
    assert resumed["resume_contract"]["actual_skipped_phases"] == [f"phase_{idx:02d}" for idx in range(1, 10)]
    assert all(item["execution_mode"] == "reused_from_checkpoint" for item in resumed["phases"])
    assert json.loads(first_phase_01_path.read_text()) == first_phase_01_payload
    checkpoint = json.loads((root / "runtime_logs/full_system_runtime/checkpoint_state.json").read_text())
    assert checkpoint["previous_checkpoint_status"] == "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
    assert checkpoint["resume_stats"]["skipped_phase_count"] == 9
