#!/usr/bin/env python3
"""SIKK compatibility CLI.

`sikkctl.py token LITH` is the mobile-friendly single command entry. It delegates
all reads to sikk_query.py / sikk_dashboard_site_builder.py, so CLI/Web share the
same unified index data and stay paper-only.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import sikk_query

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK read-only control/query CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    board = sub.add_parser("board", help="输出统一总览")
    board.add_argument("--base-dir", default=str(DEFAULT_BASE_DIR))

    token = sub.add_parser("token", help="输出单币完整详情，例如: sikkctl.py token LITH")
    token.add_argument("query", help="代币符号或地址")
    token.add_argument("--base-dir", default=str(DEFAULT_BASE_DIR))

    return parser.parse_args()


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args()
    index = sikk_query.build_query_index(args.base_dir)
    if args.command == "board":
        print(sikk_query.format_board(index))
        return 0
    if args.command == "token":
        detail = sikk_query.get_token_detail(index, args.query)
        print(sikk_query.format_token_detail(detail))
        return 0
    raise SystemExit(f"未知命令: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
