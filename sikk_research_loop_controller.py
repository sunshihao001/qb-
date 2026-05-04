#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Research loop controller.

Coordinates capture → passport → outline → topic map → lens route → system map
→ gap detect → task package → loop report. All operations are paper-only and
local-file based.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from sikk_document_ingestor import ingest_document
from sikk_document_passport_builder import build_document_passport
from sikk_gap_detector import build_gap_report
from sikk_loop_state_manager import record_loop_state
from sikk_method_lens_router import route_method_lens
from sikk_system_mapper import build_system_map
from sikk_task_package_builder import build_task_package
from sikk_topic_map_builder import build_topic_map

DEFAULT_OUTPUT_ROOT = Path("research_loop")

SAFETY_BOUNDARY = {
    "paper_only": True,
    "real_swap_enabled": False,
    "private_key_required": False,
    "signing_enabled": False,
    "broadcast_enabled": False,
}


def _write_json(path: Path, payload: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def run_full_loop(*, input_value: str, output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    loop_id = "loop_0001"
    capture = ingest_document(output_root=root, source=input_value, source_type="url" if input_value.startswith(("http://", "https://")) else "local_path", content=input_value if input_value.startswith(("#", "<", "{")) else input_value, title=None)
    record_loop_state(state="DOCUMENT_CAPTURED", loop_id=loop_id, note="capture complete", output_root=root)
    passport = build_document_passport(output_root=root, raw_doc_path=capture["raw_doc_path"])
    record_loop_state(state="PASSPORT_CREATED", loop_id=loop_id, note="passport complete", output_root=root)
    topic = build_topic_map(output_root=root, passport_json_path=passport["passport_json"])
    record_loop_state(state="OUTLINE_BUILT", loop_id=loop_id, note="outline complete", output_root=root)
    route = route_method_lens(output_root=root, passport_json_path=passport["passport_json"])
    record_loop_state(state="METHOD_ANALYZED", loop_id=loop_id, note="route complete", output_root=root)
    system_map = build_system_map(doc_id=capture["doc_id"], source_text=Path(capture["raw_doc_path"]).read_text(encoding="utf-8"), output_root=root / "mappings" / "sikk_module_maps")
    record_loop_state(state="SYSTEM_MAPPED", loop_id=loop_id, note="system map complete", output_root=root)
    system_map_payload = json.loads(Path(system_map["sikk_map_json"]).read_text(encoding="utf-8"))
    gap = build_gap_report(system_map=system_map_payload, output_root=root / "mappings" / "gap_maps")
    record_loop_state(state="GAPS_DETECTED", loop_id=loop_id, note="gap report complete", output_root=root)
    task = build_task_package(doc_id=capture["doc_id"], gap_matrix_csv=gap["gap_matrix_csv"], output_root=root / "task_packages" / "generated")
    record_loop_state(state="TASK_PACKAGE_CREATED", loop_id=loop_id, note="task package complete", output_root=root)
    report = {
        "loop_id": loop_id,
        "input": input_value,
        "capture": capture,
        "passport": passport,
        "topic_map": topic,
        "route": route,
        "system_map": system_map,
        "gap_report": gap,
        "task_package": task,
        "safety_boundary": SAFETY_BOUNDARY,
    }
    report_path = root / "reports" / "loop_reports" / f"{capture['doc_id']}_loop_report.json"
    _write_json(report_path, report)
    record_loop_state(state="HANDOFF_WRITTEN", loop_id=loop_id, note="report complete", output_root=root)
    return {
        "loop_report_json": str(report_path),
        "current_loop_json": str(root / "loop_state" / "current_loop.json"),
        "loop_history_jsonl": str(root / "loop_state" / "loop_history.jsonl"),
    }


def get_loop_status(*, output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, Any]:
    root = Path(output_root)
    current_path = root / "loop_state" / "current_loop.json"
    history_path = root / "loop_state" / "loop_history.jsonl"
    if not current_path.exists():
        return {
            "status": "missing_state",
            "current_loop": None,
            "current_loop_json": str(current_path),
            "loop_history_jsonl": str(history_path),
            "safety_boundary": SAFETY_BOUNDARY,
        }
    current = json.loads(current_path.read_text(encoding="utf-8"))
    history_count = 0
    if history_path.exists():
        history_count = len([line for line in history_path.read_text(encoding="utf-8").splitlines() if line.strip()])
    return {
        "status": "ok",
        "current_loop": current,
        "current_loop_json": str(current_path),
        "loop_history_jsonl": str(history_path),
        "history_count": history_count,
        "safety_boundary": SAFETY_BOUNDARY,
    }


def _latest_loop_report(root: Path) -> Path | None:
    report_dir = root / "reports" / "loop_reports"
    reports = sorted(report_dir.glob("*_loop_report.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def generate_final_reports(*, output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    report_root = root / "reports" / "research_loop_system"
    report_root.mkdir(parents=True, exist_ok=True)
    status = get_loop_status(output_root=root)
    latest_report_path = _latest_loop_report(root)
    latest_report: Dict[str, Any] = {}
    if latest_report_path and latest_report_path.exists():
        latest_report = json.loads(latest_report_path.read_text(encoding="utf-8"))

    loop_id = (status.get("current_loop") or {}).get("loop_id") or latest_report.get("loop_id") or "unknown"
    task_dir = (latest_report.get("task_package") or {}).get("task_dir", "未生成")
    gap_csv = (latest_report.get("gap_report") or {}).get("gap_matrix_csv", "未生成")

    final_status = report_root / "FINAL_STATUS.md"
    master_report = report_root / "MASTER_REPORT.md"
    next_backlog = report_root / "NEXT_BACKLOG.md"

    final_status.write_text(
        "\n".join([
            "# Research-to-Execution Loop OS v2.0｜FINAL_STATUS",
            "",
            f"- loop_id: `{loop_id}`",
            f"- current_status: `{status['status']}`",
            f"- current_state: `{(status.get('current_loop') or {}).get('state', 'missing_state')}`",
            "- safety_boundary: paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
            f"- latest_loop_report: `{latest_report_path or 'missing'}`",
            f"- task_package: `{task_dir}`",
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    master_report.write_text(
        "\n".join([
            "# MASTER_REPORT｜研究-执行闭环总报告",
            "",
            f"- loop_id: `{loop_id}`",
            f"- gap_matrix_csv: `{gap_csv}`",
            f"- task_package_dir: `{task_dir}`",
            f"- history_count: {status.get('history_count', 0)}",
            "- 边界: 本阶段只生成本地研究、映射、缺口、任务包与回流报告。",
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    next_backlog.write_text(
        "\n".join([
            "# NEXT_BACKLOG｜下一轮任务",
            "",
            "## 下一轮任务",
            "- 将 gap matrix 中的高优先级缺口转成最小代码改动计划。",
            "- 为 TG / Web / CLI 可见性补齐验收测试。",
            "- 继续保持 paper-only / no-secret / no-broadcast 边界。",
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    return {
        "FINAL_STATUS.md": str(final_status),
        "MASTER_REPORT.md": str(master_report),
        "NEXT_BACKLOG.md": str(next_backlog),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Research loop controller")
    parser.add_argument("command", choices=["capture", "passport", "map", "lens", "sikk-map", "gap", "task-package", "full", "review-hermes", "status", "final-reports"])
    parser.add_argument("--input", required=False, default="")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "full":
        print(json.dumps(run_full_loop(input_value=args.input, output_root=args.output_root), ensure_ascii=False, indent=2))
    elif args.command == "status":
        print(json.dumps(get_loop_status(output_root=args.output_root), ensure_ascii=False, indent=2))
    elif args.command == "final-reports":
        print(json.dumps(generate_final_reports(output_root=args.output_root), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "stub", "command": args.command, "input": args.input}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
