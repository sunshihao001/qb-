#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Loop review ingestor for the research loop."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT_ROOT = Path("research_loop")


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def ingest_hermes_review(*, loop_id: str, input_paths: List[str | Path], output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    report_dir = root / "reports" / "loop_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    text_parts = []
    for item in input_paths:
        p = Path(item)
        text_parts.append(f"## {p.name}\n\n{_load_text(p)}")
    report_text = "# Hermes Review Ingest\n\n" + "\n\n".join(text_parts) + "\n"
    report_path = report_dir / f"{loop_id}_hermes_review.md"
    report_path.write_text(report_text, encoding="utf-8")
    next_task_dir = root / "task_packages" / "generated" / f"{loop_id}_next"
    next_task_dir.mkdir(parents=True, exist_ok=True)
    (next_task_dir / "README.md").write_text("# Next task placeholder\n\nPaper-only review ingested.\n", encoding="utf-8")
    return {"hermes_review_md": str(report_path), "next_task_dir": str(next_task_dir)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Hermes review artifacts")
    parser.add_argument("--loop-id", required=True)
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(ingest_hermes_review(loop_id=args.loop_id, input_paths=args.input, output_root=args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
