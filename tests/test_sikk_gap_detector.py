import csv
import json
from pathlib import Path


def test_build_gap_report_writes_matrix_and_report_with_gap_types(tmp_path):
    from sikk_gap_detector import build_gap_report

    system_map = {
        "doc_id": "doc_002",
        "modules": [
            {
                "module": "candidate_discovery",
                "present": False,
                "surface_template": False,
                "runtime_connected": False,
                "visible_in_tg": False,
                "visible_in_web": False,
                "visible_in_cli": False,
                "has_test": False,
                "acceptance_ready": False,
                "source_trace": False,
                "field_missing": ["candidate_index"],
                "safety_risk": False,
                "over_complexity": False,
            },
            {
                "module": "telegram",
                "present": True,
                "surface_template": True,
                "runtime_connected": True,
                "visible_in_tg": False,
                "visible_in_web": True,
                "visible_in_cli": True,
                "has_test": False,
                "acceptance_ready": False,
                "source_trace": False,
                "field_missing": ["telegram_callback_index"],
                "safety_risk": True,
                "over_complexity": True,
            },
        ],
    }

    paths = build_gap_report(system_map=system_map, output_root=tmp_path)
    csv_path = Path(paths["gap_matrix_csv"])
    md_path = Path(paths["gap_report_md"])
    assert csv_path.exists()
    assert md_path.exists()
    assert csv_path.name == "doc_002_gap_matrix.csv"
    assert md_path.name == "doc_002_gap_report.md"

    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    gap_types = {row["gap_type"] for row in rows}
    assert "MISSING_MODULE" in gap_types
    assert "SURFACE_TEMPLATE" in gap_types
    assert "FIELD_MISSING" in gap_types
    assert "NOT_RUNTIME_CONNECTED" in gap_types
    assert "NOT_VISIBLE_IN_TG" in gap_types
    assert "NOT_VISIBLE_IN_WEB" in gap_types
    assert "NOT_VISIBLE_IN_CLI" in gap_types
    assert "NO_TEST" in gap_types
    assert "NO_SOURCE_TRACE" in gap_types
    assert "NO_ACCEPTANCE" in gap_types
    assert "SAFETY_RISK" in gap_types
    assert "OVER_COMPLEXITY" in gap_types

    md = md_path.read_text(encoding="utf-8")
    assert "Gap Detector" in md
    assert "doc_002" in md
    assert "MISSING_MODULE" in md
    assert "SAFETY_RISK" in md


def test_build_gap_report_keeps_paper_only_safety_boundary(tmp_path):
    from sikk_gap_detector import build_gap_report

    system_map = {
        "doc_id": "safety_doc",
        "modules": [
            {
                "module": "paper_runner",
                "present": True,
                "surface_template": True,
                "runtime_connected": True,
                "visible_in_tg": True,
                "visible_in_web": True,
                "visible_in_cli": True,
                "has_test": True,
                "acceptance_ready": True,
                "source_trace": True,
                "field_missing": [],
                "safety_risk": False,
                "over_complexity": False,
            }
        ],
    }
    paths = build_gap_report(system_map=system_map, output_root=tmp_path)
    md = Path(paths["gap_report_md"]).read_text(encoding="utf-8")
    assert "paper-only" in md
    assert "不执行真实 swap" in md
    assert "不读取私钥" in md
    assert "不广播" in md

    with Path(paths["gap_matrix_csv"]).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows == []
