import json
from pathlib import Path


def test_record_loop_state_writes_current_and_history(tmp_path):
    from sikk_loop_state_manager import record_loop_state

    paths = record_loop_state(state="DOCUMENT_CAPTURED", loop_id="loop_1", note="captured", output_root=tmp_path / "research_loop")
    current = Path(paths["current_loop_json"])
    history = Path(paths["loop_history_jsonl"])
    assert current.exists()
    assert history.exists()

    payload = json.loads(current.read_text(encoding="utf-8"))
    assert payload["loop_id"] == "loop_1"
    assert payload["state"] == "DOCUMENT_CAPTURED"
    assert payload["note"] == "captured"

    lines = [json.loads(line) for line in history.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines[-1]["state"] == "DOCUMENT_CAPTURED"


def test_record_loop_state_rejects_invalid_state(tmp_path):
    from sikk_loop_state_manager import record_loop_state

    try:
        record_loop_state(state="INVALID", loop_id="loop_x", output_root=tmp_path / "research_loop")
    except ValueError as exc:
        assert "invalid loop state" in str(exc)
    else:
        raise AssertionError("expected ValueError")
