import json
from pathlib import Path


def test_build_task_package_writes_expected_files_and_safety_boundary(tmp_path):
    from sikk_task_package_builder import build_task_package

    gap_csv = tmp_path / "research_loop" / "mappings" / "gap_maps" / "doc_001_gap_matrix.csv"
    gap_csv.parent.mkdir(parents=True)
    gap_csv.write_text(
        "doc_id,module,gap_type,detail\n"
        "doc_001,telegram,NOT_VISIBLE_IN_TG,TG missing\n"
        "doc_001,web_dashboard,NOT_VISIBLE_IN_WEB,Web missing\n",
        encoding="utf-8",
    )

    paths = build_task_package(doc_id="doc_001", gap_matrix_csv=gap_csv, output_root=tmp_path / "research_loop" / "task_packages" / "generated")
    task_dir = Path(paths["task_dir"])
    assert task_dir.is_dir()

    for filename in [
        "MASTER_TASK.md",
        "PHASE_PLAN.md",
        "SAFETY_BOUNDARY.md",
        "ACCEPTANCE_CHECKLIST.md",
        "CURRENT_CONTEXT.md",
        "REPOMIX_CONTEXT_PLAN.md",
        "DEERFLOW_METHOD.md",
        "HERMES_START_COMMAND.md",
    ]:
        assert (task_dir / filename).exists()

    safety = (task_dir / "SAFETY_BOUNDARY.md").read_text(encoding="utf-8")
    assert "paper_only: true" in safety
    assert "real_swap_enabled: false" in safety
    assert "broadcast_enabled: false" in safety

    master = (task_dir / "MASTER_TASK.md").read_text(encoding="utf-8")
    assert "Hermes 任务包" in master
    assert "NOT_VISIBLE_IN_TG" in master
    assert "NOT_VISIBLE_IN_WEB" in master

    hermes = (task_dir / "HERMES_START_COMMAND.md").read_text(encoding="utf-8")
    assert "sikk_research_loop_controller.py review-hermes" in hermes


def test_build_task_package_handles_empty_gap_matrix(tmp_path):
    from sikk_task_package_builder import build_task_package

    gap_csv = tmp_path / "empty.csv"
    gap_csv.write_text("doc_id,module,gap_type,detail\n", encoding="utf-8")
    paths = build_task_package(doc_id="doc_empty", gap_matrix_csv=gap_csv, output_root=tmp_path / "research_loop" / "task_packages" / "generated")
    master = Path(paths["MASTER_TASK.md"]).read_text(encoding="utf-8")
    assert "无缺口" in master or "none" in master.lower()
