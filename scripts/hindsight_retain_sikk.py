#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retain selected SIKK project summaries into Hindsight.

安全边界：只写长期记忆；不读取/输出 secrets；Hindsight 不参与真实 swap 授权。
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from hindsight_client import Hindsight

DEFAULT_BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
DEFAULT_BANK_ID = os.environ.get("HINDSIGHT_BANK_ID", "sikk-gmgn-main")
DEFAULT_TAGS = ["project:sikk-gmgn", "scope:project"]


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_text(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n[TRUNCATED_FOR_HINDSIGHT_RETAIN: original_chars={len(text)} max_chars={max_chars}]\n"


def _safe_tags(extra: list[str]) -> list[str]:
    tags = []
    for tag in DEFAULT_TAGS + extra:
        tag = tag.strip()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def retain_file(
    *,
    path: Path,
    base_url: str,
    bank_id: str,
    context: str,
    document_id: str,
    tags: list[str],
    max_chars: int,
    timeout: float,
) -> None:
    if not path.exists():
        raise FileNotFoundError(f"输入文件不存在: {path}")

    content = _read_text(path, max_chars=max_chars)
    client = Hindsight(base_url=base_url, timeout=timeout)
    try:
        # create_bank may fail if bank already exists; retain also auto-creates.
        try:
            client.create_bank(bank_id=bank_id, name="SIKK-GMGN Project Memory")
        except Exception:
            pass
        client.retain(
            bank_id=bank_id,
            content=content,
            context=context,
            timestamp=datetime.now(timezone.utc),
            document_id=document_id,
            metadata={"source": "sikk-gmgn", "path": str(path)},
            tags=_safe_tags(tags),
        )
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="把 SIKK 报告/设计文档写入 Hindsight 长期记忆")
    parser.add_argument("--file", required=True, help="要 retain 的 markdown/json/txt 文件")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--bank-id", default=DEFAULT_BANK_ID)
    parser.add_argument("--context", default="SIKK-GMGN project report or design note")
    parser.add_argument("--document-id", default=None, help="稳定 document_id；不填则使用文件名")
    parser.add_argument("--tag", action="append", default=[], help="额外 tag，可重复")
    parser.add_argument("--max-chars", type=int, default=50000)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args(argv)

    path = Path(args.file).expanduser().resolve()
    document_id = args.document_id or f"sikk-file:{path.name}"

    try:
        retain_file(
            path=path,
            base_url=args.base_url,
            bank_id=args.bank_id,
            context=args.context,
            document_id=document_id,
            tags=args.tag,
            max_chars=args.max_chars,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"HINDSIGHT_RETAIN_FAILED: {exc}", file=sys.stderr)
        print("提示：请确认 Hindsight API 已在 --base-url 启动，且 HINDSIGHT_API_LLM_API_KEY 已在服务端配置。", file=sys.stderr)
        return 2

    print(f"HINDSIGHT_RETAIN_OK bank_id={args.bank_id} document_id={document_id} file={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
