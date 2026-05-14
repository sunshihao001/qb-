#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a document passport for the research loop.

Input: normalized raw document + metadata written by sikk_document_ingestor.
Output: JSON and Markdown passport under research_loop/corpus/passports.
Paper-only and local-file only.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT_ROOT = Path("research_loop")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _slug_from_raw_path(raw_doc_path: Path) -> str:
    return raw_doc_path.stem


def _title_from_text(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _key_tags(text: str) -> List[str]:
    tags = []
    for token, tag in [
        ("paper-only", "paper-only"),
        ("swap", "swap"),
        ("Hermes", "Hermes"),
        ("SIKK", "SIKK"),
        ("GPT", "GPT"),
        ("Telegram", "Telegram"),
        ("dashboard", "dashboard"),
        ("loop", "loop"),
    ]:
        if token.lower() in text.lower():
            tags.append(tag)
    return sorted(set(tags))


def build_document_passport(*, output_root: str | Path = DEFAULT_OUTPUT_ROOT, raw_doc_path: str | Path) -> Dict[str, str]:
    root = Path(output_root)
    raw_doc_path = Path(raw_doc_path)
    raw_text = raw_doc_path.read_text(encoding="utf-8")
    metadata_path = raw_doc_path.with_name(f"{raw_doc_path.stem}_metadata.json")
    metadata = _load_json(metadata_path) if metadata_path.exists() else {
        "doc_id": raw_doc_path.stem,
        "source_type": "local_path",
        "source_url": "",
        "source_path": str(raw_doc_path),
        "captured_at": "",
        "title": _title_from_text(raw_text, raw_doc_path.stem),
        "content_hash": "",
        "estimated_size": len(raw_text.encode("utf-8")),
        "status": "captured",
    }

    doc_id = metadata.get("doc_id") or raw_doc_path.stem
    title = metadata.get("title") or _title_from_text(raw_text, doc_id)
    source = {
        "source_type": metadata.get("source_type", "local_path"),
        "source_url": metadata.get("source_url", ""),
        "source_path": metadata.get("source_path", str(raw_doc_path)),
        "captured_at": metadata.get("captured_at", ""),
        "content_hash": metadata.get("content_hash", ""),
        "estimated_size": metadata.get("estimated_size", len(raw_text.encode("utf-8"))),
        "status": metadata.get("status", "captured"),
    }
    passport = {
        "doc_id": doc_id,
        "title": title,
        "metadata": metadata,
        "source": source,
        "key_tags": _key_tags(raw_text),
        "core_summary_zh": f"该文档已进入 research loop，强调 paper-only、知识护照、主题地图、系统映射和闭环执行。",
        "tone_assessment": "procedural / research / implementation-oriented",
        "relevance_to_sikk": "high",
        "usable_mechanisms": [
            "原文先归档再吸收",
            "先护照再规则再审计",
            "paper-only 安全边界",
            "模块映射与 gap detector",
            "任务包与执行回流闭环",
        ],
        "risk_notes": [
            "避免把文档摘要当作事实来源",
            "避免引入真实交易动作",
            "避免丢失原文证据",
        ],
        "confidence": 0.82,
    }

    out_dir = root / "corpus" / "passports"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{_slug_from_raw_path(raw_doc_path)}_passport.json"
    md_path = out_dir / f"{_slug_from_raw_path(raw_doc_path)}_passport.md"
    json_path.write_text(json.dumps(passport, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        f"# {title}｜文档护照",
        "",
        f"- doc_id: `{doc_id}`",
        f"- source_type: `{source['source_type']}`",
        f"- source_url: `{source['source_url']}`",
        f"- source_path: `{source['source_path']}`",
        f"- captured_at: `{source['captured_at']}`",
        f"- confidence: `{passport['confidence']}`",
        "",
        "## 核心摘要",
        passport["core_summary_zh"],
        "",
        "## 可用机制",
    ]
    md.extend([f"- {item}" for item in passport["usable_mechanisms"]])
    md.extend([
        "",
        "## 风险说明",
    ])
    md.extend([f"- {item}" for item in passport["risk_notes"]])
    md.extend([
        "",
        "## 关键标签",
        ", ".join(passport["key_tags"]) if passport["key_tags"] else "无",
        "",
    ])
    md_path.write_text("\n".join(md), encoding="utf-8")
    return {"passport_json": str(json_path), "passport_md": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a document passport")
    parser.add_argument("raw_doc_path")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_document_passport(output_root=args.output_root, raw_doc_path=args.raw_doc_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
