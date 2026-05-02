#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recall SIKK project memories from Hindsight.

默认严格限定 project:sikk-gmgn，避免跨项目记忆污染。
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from hindsight_client import Hindsight

DEFAULT_BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
DEFAULT_BANK_ID = os.environ.get("HINDSIGHT_BANK_ID", "sikk-gmgn-main")


def _extract_results(resp: Any) -> list[Any]:
    if hasattr(resp, "results"):
        return list(resp.results or [])
    if isinstance(resp, dict):
        return list(resp.get("results") or [])
    if isinstance(resp, list):
        return resp
    return []


def _field(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从 Hindsight 检索 SIKK 长期记忆")
    parser.add_argument("query", help="检索问题")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--bank-id", default=DEFAULT_BANK_ID)
    parser.add_argument("--budget", choices=["low", "mid", "high"], default="mid")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--tag", action="append", default=["project:sikk-gmgn"], help="过滤 tag，可重复")
    parser.add_argument("--tags-match", default="any_strict", choices=["any", "all", "any_strict", "all_strict"])
    parser.add_argument("--include-chunks", action="store_true")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args(argv)

    client = Hindsight(base_url=args.base_url, timeout=args.timeout)
    try:
        resp = client.recall(
            bank_id=args.bank_id,
            query=args.query,
            budget=args.budget,
            max_tokens=args.max_tokens,
            tags=args.tag,
            tags_match=args.tags_match,
            include_chunks=args.include_chunks,
        )
    except Exception as exc:
        print(f"HINDSIGHT_RECALL_FAILED: {exc}", file=sys.stderr)
        print("提示：请确认 Hindsight API 已启动，或先用 scripts/hindsight_retain_sikk.py 写入记忆。", file=sys.stderr)
        return 2
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()

    results = _extract_results(resp)[: args.limit]
    print(f"# Hindsight Recall: {args.query}\n")
    if not results:
        print("未检索到匹配记忆。")
        return 0

    for idx, item in enumerate(results, 1):
        text = _field(item, "text") or _field(item, "content") or str(item)
        typ = _field(item, "type", "")
        score = _field(item, "score", "")
        print(f"## {idx}. {typ} score={score}")
        print(str(text).strip())
        chunks = _field(item, "chunks", None)
        if chunks:
            first = chunks[0]
            ctext = _field(first, "text", "")
            if ctext:
                print("\n来源片段：")
                print(str(ctext)[:500].strip())
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
