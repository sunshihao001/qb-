import json
from pathlib import Path


def test_status_command_returns_current_loop_state(tmp_path):
    from sikk_loop_state_manager import record_loop_state
    from sikk_research_loop_controller import get_loop_status

    record_loop_state(state="HANDOFF_WRITTEN", loop_id="loop_status_001", note="ready", output_root=tmp_path)
    status = get_loop_status(output_root=tmp_path)

    assert status["status"] == "ok"
    assert status["current_loop"]["state"] == "HANDOFF_WRITTEN"
    assert status["current_loop"]["loop_id"] == "loop_status_001"
    assert status["safety_boundary"]["paper_only"] is True
    assert status["safety_boundary"]["broadcast_enabled"] is False


def test_status_command_handles_missing_state(tmp_path):
    from sikk_research_loop_controller import get_loop_status

    status = get_loop_status(output_root=tmp_path)
    assert status["status"] == "missing_state"
    assert status["current_loop"] is None
    assert status["safety_boundary"]["private_key_required"] is False
