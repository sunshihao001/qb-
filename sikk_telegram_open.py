#!/usr/bin/env python3
"""SIKK Telegram open-view renderer.

This module is intentionally side-effect free: it does not talk to Telegram by
itself. Bot glue can call `build_sikk_open_payload()` for `/sikk_open`, render the
returned buttons, then call `build_sikk_token_detail()` for the clicked token.
All content is read from the same unified query/dashboard index.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping

import sikk_query

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def build_sikk_open_payload(base_dir: str | Path = DEFAULT_BASE_DIR, limit: int = 12) -> Dict[str, Any]:
    index = sikk_query.build_query_index(base_dir)
    rows = list(index.get("tokens") or [])
    focus = [r for r in rows if r.get("paper_status") == "OPEN" or r.get("current_state") == "PAPER_OPEN" or r.get("case_quality") == "LOW"]
    if not focus:
        focus = rows
    buttons: List[Dict[str, str]] = []
    for row in focus[:limit]:
        symbol = str(row.get("token_symbol") or "UNKNOWN")
        token = str(row.get("token_address") or "")
        label = f"{symbol}｜{row.get('case_quality') or row.get('current_state') or 'DETAIL'}"
        buttons.append({"text": label, "callback_data": f"sikk_token:{token}"})
    return {
        "text": "SIKK 纸面控制台（只读）\n点击代币查看详情；不执行真实 swap、不签名、不广播。",
        "buttons": buttons,
        "source": str(Path(base_dir) / "site" / "dashboard_data.json"),
        "boundary": sikk_query.QUERY_BOUNDARY,
    }


def build_sikk_token_detail(query: str, base_dir: str | Path = DEFAULT_BASE_DIR) -> str:
    index = sikk_query.build_query_index(base_dir)
    return sikk_query.format_token_detail(sikk_query.get_token_detail(index, query))
