import json
from pathlib import Path


def test_generate_final_reports_writes_final_status_master_and_backlog(tmp_path):
    from sikk_loop_state_manager import record_loop_state
    from sikk_research_loop_controller import generate_final_reports

    report_dir = tmp_path / "reports" / "loop_reports"
    report_dir.mkdir(parents=True)
    loop_report = report_dir / "doc_final_loop_report.json"
    loop_report.write_text(
        json.dumps(
            {
                "loop_id": "loop_final_001",
                "gap_report": {"gap_matrix_csv": str(tmp_path / "mappings" / "gap_maps" / "doc_gap.csv")},
                "task_package": {"task_dir": str(tmp_path / "task_packages" / "generated" / "doc_task")},
                "safety_boundary": {"paper_only": True, "broadcast_enabled": False},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    record_loop_state(state="HANDOFF_WRITTEN", loop_id="loop_final_001", note="done", output_root=tmp_path)

    paths = generate_final_reports(output_root=tmp_path)

    final_status = Path(paths["FINAL_STATUS.md"])
    master_report = Path(paths["MASTER_REPORT.md"])
    next_backlog = Path(paths["NEXT_BACKLOG.md"])

    assert final_status.exists()
    assert master_report.exists()
    assert next_backlog.exists()
    assert "Research-to-Execution Loop OS v2.0" in final_status.read_text(encoding="utf-8")
    assert "paper-only" in final_status.read_text(encoding="utf-8")
    assert "loop_final_001" in master_report.read_text(encoding="utf-8")
    assert "下一轮任务" in next_backlog.read_text(encoding="utf-8")
