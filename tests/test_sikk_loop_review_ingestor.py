import json
from pathlib import Path


def test_ingest_hermes_review_writes_review_report_and_next_task(tmp_path):
    from sikk_loop_review_ingestor import ingest_hermes_review

    final = tmp_path / "FINAL_STATUS.md"
    master = tmp_path / "MASTER_REPORT.md"
    failed = tmp_path / "FAILED_ITEMS.md"
    backlog = tmp_path / "NEXT_ENGINEERING_BACKLOG.md"
    for idx, path in enumerate([final, master, failed, backlog], start=1):
        path.write_text(f"# doc {idx}\ncontent {idx}\n", encoding="utf-8")

    paths = ingest_hermes_review(loop_id="loop_9", input_paths=[final, master, failed, backlog], output_root=tmp_path / "research_loop")
    review_path = Path(paths["hermes_review_md"])
    next_dir = Path(paths["next_task_dir"])
    assert review_path.exists()
    assert next_dir.is_dir()
    assert (next_dir / "README.md").exists()

    text = review_path.read_text(encoding="utf-8")
    assert "Hermes Review Ingest" in text
    assert "FINAL_STATUS.md" in text
    assert "NEXT_ENGINEERING_BACKLOG.md" in text
