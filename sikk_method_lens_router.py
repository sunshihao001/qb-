#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Method lens router for the research loop."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SUPPORTED_LENSES = [
    "SCAN",
    "DEEP",
    "ANGLE",
    "MIX",
    "HYP",
    "VOICES",
    "CHALLENGE",
    "TIMELINE",
    "STATUS",
    "OVERVIEW",
    "ARTEFACT",
]

DEFAULT_OUTPUT_ROOT = Path("research_loop")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def route_method_lens(*, output_root: str | Path = DEFAULT_OUTPUT_ROOT, passport_json_path: str | Path) -> Dict[str, str]:
    root = Path(output_root)
    passport = _load_json(Path(passport_json_path))
    doc_id = passport.get("doc_id") or Path(passport_json_path).stem.replace("_passport", "")
    summary = " ".join([
        passport.get("title", ""),
        passport.get("core_summary_zh", ""),
        " ".join(passport.get("key_tags", []) or []),
        " ".join(passport.get("usable_mechanisms", []) or []),
    ])
    if "timeline" in summary.lower() or "history" in summary.lower():
        lens = ["TIMELINE", "DEEP", "STATUS"]
    elif "audit" in summary.lower():
        lens = ["SCAN", "ANGLE", "OVERVIEW"]
    elif "review" in summary.lower():
        lens = ["OVERVIEW", "SCAN", "ARTEFACT"]
    else:
        lens = ["OVERVIEW", "SCAN", "ARTEFACT"]
    route = {
        "doc_id": doc_id,
        "passport_json": str(passport_json_path),
        "supported_lenses": SUPPORTED_LENSES,
        "selected_lenses": lens,
        "primary_lens": lens[0],
        "why": f"基于标题/摘要/标签/机制选择 {', '.join(lens)}",
        "acceptance": "输出 route.json 供后续系统映射、gap detector、任务包生成使用",
    }
    out_dir = root / "analysis" / "task_route"
    out_dir.mkdir(parents=True, exist_ok=True)
    route_path = out_dir / f"{doc_id}_route.json"
    route_path.write_text(json.dumps(route, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"route_json": str(route_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Route method lenses")
    parser.add_argument("passport_json_path")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(route_method_lens(output_root=args.output_root, passport_json_path=args.passport_json_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
