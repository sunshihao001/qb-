import csv
import json
from pathlib import Path


EXPECTED_MODULES = [
    "candidate_discovery",
    "kline_signal",
    "wallet_structure",
    "okx_cluster",
    "structure_fusion",
    "state_machine",
    "paper_runner",
    "case_file",
    "auto_review",
    "unified_index",
    "telegram",
    "web_dashboard",
    "cli",
    "runtime",
    "audit",
    "harness",
    "repomix_context",
    "hermes_execution",
]


def test_build_system_map_writes_expected_outputs_and_module_list(tmp_path):
    from sikk_system_mapper import build_system_map

    source_text = " ".join(EXPECTED_MODULES) + " 研究 映射 审计 验收 paper-only"
    paths = build_system_map(doc_id="doc_001", source_text=source_text, output_root=tmp_path)

    json_path = Path(paths["sikk_map_json"])
    md_path = Path(paths["sikk_map_md"])
    assert json_path.exists()
    assert md_path.exists()
    assert json_path.name == "doc_001_sikk_map.json"
    assert md_path.name == "doc_001_sikk_map.md"

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["doc_id"] == "doc_001"
    assert [row["module"] for row in payload["modules"]] == EXPECTED_MODULES
    assert all(row["present"] is True for row in payload["modules"])
    assert payload["module_count"] == len(EXPECTED_MODULES)

    md = md_path.read_text(encoding="utf-8")
    assert "SIKK 模块映射" in md
    assert "candidate_discovery" in md
    assert "hermes_execution" in md
    assert "paper-only" in md


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
