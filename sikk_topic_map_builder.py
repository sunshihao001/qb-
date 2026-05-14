#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build topic outlines and topic maps for the research loop."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT_ROOT = Path("research_loop")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _topics(passport: Dict[str, Any]) -> List[str]:
    text = " ".join([
        passport.get("title", ""),
        passport.get("core_summary_zh", ""),
        " ".join(passport.get("key_tags", []) or []),
        " ".join(passport.get("usable_mechanisms", []) or []),
    ])
    candidates = ["input", "passport", "outline", "topic map", "audit", "review", "loop", "paper-only", "task package", "Hermes"]
    return [item for item in candidates if item.lower() in text.lower()]


def build_topic_map(*, output_root: str | Path = DEFAULT_OUTPUT_ROOT, passport_json_path: str | Path) -> Dict[str, str]:
    root = Path(output_root)
    passport_json_path = Path(passport_json_path)
    passport = _load_json(passport_json_path)
    doc_id = passport.get("doc_id") or passport_json_path.stem.replace("_passport", "")
    title = passport.get("title") or doc_id
    topics = _topics(passport)
    topic_count = len(topics)
    hotspots = [
        "paper-only safety boundary",
        "loop state management",
        "task package generation",
        "system mapping / gap detection",
        "hermes execution handoff",
    ]
    if any("audit" in item.lower() for item in topics):
        hotspots.append("audit coverage")
    if any("review" in item.lower() for item in topics):
        hotspots.append("review loop")
    if any("paper-only" in item.lower() for item in topics):
        hotspots.append("paper-only constraint")
    outline = {
        "doc_id": doc_id,
        "title": title,
        "topic_count": topic_count,
        "topics": topics,
        "hotspots": hotspots,
        "信息热点": hotspots,
        "potential_paths": [
            "文档护照 → 主题地图 → 方法镜头 → 系统映射",
            "系统映射 → gap detector → Hermes 任务包",
            "任务包 → 执行回流 → 下一轮循环",
        ],
        "relevance_to_sikk": passport.get("relevance_to_sikk", "unknown"),
    }
    outline_dir = root / "corpus" / "outlines"
    topic_dir = root / "corpus" / "topic_maps"
    outline_dir.mkdir(parents=True, exist_ok=True)
    topic_dir.mkdir(parents=True, exist_ok=True)
    outline_json = outline_dir / f"{doc_id}_outline.json"
    topic_map_md = topic_dir / f"{doc_id}_topic_map.md"
    outline_json.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        f"# {title}｜主题地图",
        "",
        f"- doc_id: `{doc_id}`",
        f"- topic_count: `{topic_count}`",
        "",
        "## 主题结构",
    ]
    md.extend([f"- {topic}" for topic in topics] or ["- 无明显主题，需进一步扫描"])
    md.extend(["", "## 信息热点"])
    md.extend([f"- {item}" for item in hotspots])
    md.extend(["", "## 潜在路径"])
    md.extend([f"- {item}" for item in outline["potential_paths"]])
    topic_map_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"outline_json": str(outline_json), "topic_map_md": str(topic_map_md)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build topic outlines and topic maps")
    parser.add_argument("passport_json_path")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_topic_map(output_root=args.output_root, passport_json_path=args.passport_json_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
