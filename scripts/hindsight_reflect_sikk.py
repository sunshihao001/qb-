#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reflect over SIKK project memories with Hindsight.

用于复盘/策略设计问答；输出不是交易授权。
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from hindsight_client import Hindsight

DEFAULT_BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
DEFAULT_BANK_ID = os.environ.get("HINDSIGHT_BANK_ID", "sikk-gmgn-main")


def _field(obj: Any, name: str, default: Any = "") -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="让 Hindsight 基于 SIKK 长期记忆综合回答")
    parser.add_argument("query")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--bank-id", default=DEFAULT_BANK_ID)
    parser.add_argument("--budget", choices=["low", "mid", "high"], default="mid")
    parser.add_argument("--context", default="SIKK-GMGN/SIKK-SOL project memory reflection; paper/readiness only, no real swap authorization")
    parser.add_argument("--tag", action="append", default=["project:sikk-gmgn"])
    parser.add_argument("--tags-match", default="any_strict", choices=["any", "all", "any_strict", "all_strict"])
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(argv)

    client = Hindsight(base_url=args.base_url, timeout=args.timeout)
    try:
        answer = client.reflect(
            bank_id=args.bank_id,
            query=args.query,
            budget=args.budget,
            context=args.context,
            tags=args.tag,
            tags_match=args.tags_match,
        )
    except Exception as exc:
        msg = str(exc)
        print(f"HINDSIGHT_REFLECT_FAILED: {exc}", file=sys.stderr)
        if "provider is set to 'none'" in msg or "Reflect requires an LLM provider" in msg:
            print(
                "提示：当前 Hindsight 以 HINDSIGHT_API_LLM_PROVIDER=none 运行，只支持 retain/recall；"
                "reflect 需要配置可用 LLM provider/API key 后重启容器。",
                file=sys.stderr,
            )
        else:
            print("提示：请确认 Hindsight API 已启动，且 bank 内已有相关 SIKK 记忆。", file=sys.stderr)
        return 2
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()

    text = _field(answer, "text") or str(answer)
    print(text)
    print("\n---\n边界：以上为 Hindsight 长期记忆复盘，不构成真实交易授权；仍需 SIKK 状态机、报价安全、纸面验证和人工确认。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
