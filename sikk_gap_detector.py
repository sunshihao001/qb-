#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK gap detector.

Consumes a system map and emits a CSV gap matrix plus a markdown report.
Paper-only: local analysis only, no trading, no signing, no broadcast.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

GAP_TYPES = [
    "MISSING_MODULE",
    "SURFACE_TEMPLATE",
    "FIELD_MISSING",
    "NOT_RUNTIME_CONNECTED",
    "NOT_VISIBLE_IN_TG",
    "NOT_VISIBLE_IN_WEB",
    "NOT_VISIBLE_IN_CLI",
    "NO_TEST",
    "NO_SOURCE_TRACE",
    "NO_ACCEPTANCE",
    "SAFETY_RISK",
    "OVER_COMPLEXITY",
]

DEFAULT_OUTPUT_ROOT = Path("research_loop/mappings/gap_maps")


def _slug_doc_id(doc_id: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(doc_id).strip())
    return cleaned or "doc"


def _add_gap(rows: List[Dict[str, Any]], doc_id: str, module: str, gap_type: str, detail: str) -> None:
    rows.append({
        "doc_id": doc_id,
        "module": module,
        "gap_type": gap_type,
        "detail": detail,
    })


def _module_gaps(doc_id: str, row: Dict[str, Any]) -> List[Dict[str, Any]]:
    gaps: List[Dict[str, Any]] = []
    module = str(row.get("module", ""))
    present = bool(row.get("present"))
    if not present:
        _add_gap(gaps, doc_id, module, "MISSING_MODULE", "模块在映射中缺失或未接入")
        if not row.get("surface_template", False):
            _add_gap(gaps, doc_id, module, "SURFACE_TEMPLATE", "缺失模块也没有表层模板")
        field_missing = row.get("field_missing") or []
        for field in field_missing:
            _add_gap(gaps, doc_id, module, "FIELD_MISSING", f"缺失字段: {field}")
        if not row.get("runtime_connected", False):
            _add_gap(gaps, doc_id, module, "NOT_RUNTIME_CONNECTED", "未与 runtime 主流程连接")
        if not row.get("visible_in_tg", False):
            _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_TG", "TG 中不可见")
        if not row.get("visible_in_web", False):
            _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_WEB", "Web 中不可见")
        if not row.get("visible_in_cli", False):
            _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_CLI", "CLI 中不可见")
        if not row.get("has_test", False):
            _add_gap(gaps, doc_id, module, "NO_TEST", "缺少对应测试")
        if not row.get("source_trace", False):
            _add_gap(gaps, doc_id, module, "NO_SOURCE_TRACE", "缺少源文件或来源追踪")
        if not row.get("acceptance_ready", False):
            _add_gap(gaps, doc_id, module, "NO_ACCEPTANCE", "缺少验收声明")
        if row.get("safety_risk", False):
            _add_gap(gaps, doc_id, module, "SAFETY_RISK", "存在安全风险")
        if row.get("over_complexity", False):
            _add_gap(gaps, doc_id, module, "OVER_COMPLEXITY", "存在过度复杂化风险")
        return gaps
    if not row.get("surface_template", False):
        _add_gap(gaps, doc_id, module, "SURFACE_TEMPLATE", "有模块但缺少表层模板")
    field_missing = row.get("field_missing") or []
    for field in field_missing:
        _add_gap(gaps, doc_id, module, "FIELD_MISSING", f"缺失字段: {field}")
    if not row.get("runtime_connected", False):
        _add_gap(gaps, doc_id, module, "NOT_RUNTIME_CONNECTED", "未与 runtime 主流程连接")
    if not row.get("visible_in_tg", False):
        _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_TG", "TG 中不可见")
    if not row.get("visible_in_web", False):
        _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_WEB", "Web 中不可见")
    if not row.get("visible_in_cli", False):
        _add_gap(gaps, doc_id, module, "NOT_VISIBLE_IN_CLI", "CLI 中不可见")
    if not row.get("has_test", False):
        _add_gap(gaps, doc_id, module, "NO_TEST", "缺少对应测试")
    if not row.get("source_trace", False):
        _add_gap(gaps, doc_id, module, "NO_SOURCE_TRACE", "缺少源文件或来源追踪")
    if not row.get("acceptance_ready", False):
        _add_gap(gaps, doc_id, module, "NO_ACCEPTANCE", "缺少验收声明")
    if row.get("safety_risk", False):
        _add_gap(gaps, doc_id, module, "SAFETY_RISK", "存在安全风险")
    if row.get("over_complexity", False):
        _add_gap(gaps, doc_id, module, "OVER_COMPLEXITY", "存在过度复杂化风险")
    return gaps


def build_gap_report(*, system_map: Dict[str, Any], output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    doc_id = str(system_map.get("doc_id", "doc"))
    slug = _slug_doc_id(doc_id)
    csv_path = root / f"{slug}_gap_matrix.csv"
    md_path = root / f"{slug}_gap_report.md"

    rows: List[Dict[str, Any]] = []
    modules = system_map.get("modules") or []
    for row in modules:
        if isinstance(row, dict):
            rows.extend(_module_gaps(doc_id, row))

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["doc_id", "module", "gap_type", "detail"])
        writer.writeheader()
        writer.writerows(rows)

    counts: Dict[str, int] = {gap: 0 for gap in GAP_TYPES}
    for row in rows:
        counts[row["gap_type"]] = counts.get(row["gap_type"], 0) + 1

    md_lines = [
        "# SIKK Gap Detector",
        "",
        f"- doc_id: `{doc_id}`",
        f"- gap rows: {len(rows)}",
        "- safety boundary: paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
        "",
        "## Gap Counts",
    ]
    for gap in GAP_TYPES:
        md_lines.append(f"- {gap}: {counts.get(gap, 0)}")
    md_lines.extend(["", "## Matrix Preview"])
    for row in rows[:50]:
        md_lines.append(f"- `{row['module']}` / {row['gap_type']} / {row['detail']}")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {"gap_matrix_csv": str(csv_path), "gap_report_md": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 SIKK gap detector 报告")
    parser.add_argument("--system-map-json", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    system_map = json.loads(Path(args.system_map_json).read_text(encoding="utf-8"))
    print(json.dumps(build_gap_report(system_map=system_map, output_root=args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
