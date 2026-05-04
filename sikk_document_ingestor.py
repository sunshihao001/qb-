#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Document ingestor for the SIKK research loop.

Accepts URL / markdown / local report / Hermes output / case file / log inputs
and stores a normalized raw document plus metadata. Paper-only: local file IO only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

DEFAULT_OUTPUT_ROOT = Path("research_loop")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slug(value: str, fallback: str = "doc") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    cleaned = cleaned.strip("_")
    return cleaned or fallback


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _guess_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _infer_source_type(source: str | Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    source_str = str(source)
    parsed = urlparse(source_str)
    if parsed.scheme in {"http", "https"}:
        return "url"
    return "local_path"


def _read_source(source: str | Path, source_type: str, content: str | None) -> str:
    if content is not None:
        return content
    if source_type == "url":
        raise ValueError("URL source requires explicit content in paper-only mode")
    return Path(source).read_text(encoding="utf-8")


def ingest_document(
    *,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    source: str | Path,
    source_type: str | None = None,
    content: str | None = None,
    title: str | None = None,
) -> Dict[str, str]:
    root = Path(output_root)
    raw_dir = root / "corpus" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    inferred_type = _infer_source_type(source, source_type)
    text = _read_source(source, inferred_type, content)
    now = _utc_now()
    base_name = _slug(Path(str(source)).stem if str(source) else "doc")
    doc_id = f"{base_name}_{_content_hash(text)[:12]}"
    raw_path = raw_dir / f"{doc_id}.md"
    metadata_path = raw_dir / f"{doc_id}_metadata.json"
    doc_title = title or _guess_title(text, base_name.replace("_", " ").title())
    source_url = str(source) if inferred_type == "url" else ""
    source_path = str(source) if inferred_type != "url" else ""
    metadata = {
        "doc_id": doc_id,
        "source_type": inferred_type,
        "source_url": source_url,
        "source_path": source_path,
        "captured_at": now,
        "title": doc_title,
        "content_hash": _content_hash(text),
        "estimated_size": len(text.encode("utf-8")),
        "status": "captured",
    }
    raw_path.write_text(text, encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "doc_id": doc_id,
        "raw_doc_path": str(raw_path),
        "metadata_path": str(metadata_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest a document into the SIKK research loop")
    parser.add_argument("source")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--source-type", default=None)
    parser.add_argument("--content", default=None)
    parser.add_argument("--title", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(ingest_document(output_root=args.output_root, source=args.source, source_type=args.source_type, content=args.content, title=args.title), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
