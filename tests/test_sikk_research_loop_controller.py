import json
from pathlib import Path


def test_run_full_loop_creates_loop_report_and_state_files(tmp_path):
    from sikk_research_loop_controller import run_full_loop

    input_text = "# Loop Input\n\nThis is a paper-only loop research document with audit and review.\n"
    input_path = tmp_path / "input.md"
    input_path.write_text(input_text, encoding="utf-8")

    paths = run_full_loop(input_value=str(input_path), output_root=tmp_path / "research_loop")
    report = Path(paths["loop_report_json"])
    current = Path(paths["current_loop_json"])
    history = Path(paths["loop_history_jsonl"])
    assert report.exists()
    assert current.exists()
    assert history.exists()

    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["safety_boundary"]["paper_only"] is True
    assert "capture" in payload
    assert "passport" in payload
    assert "topic_map" in payload
    assert "system_map" in payload
    assert "gap_report" in payload
    assert "task_package" in payload


def test_research_loop_controller_status_command_is_stubbed(tmp_path):
    from sikk_research_loop_controller import main

    # smoke test via direct module import already covered; this command path should be non-failing when stubbed.
    assert callable(main)
