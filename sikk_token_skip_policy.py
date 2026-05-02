#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Runtime loop token skip/cooldown policy."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")

COOLDOWN_SECONDS = {
    "BLOCKED": 6 * 60 * 60,
    "PAUSE": 30 * 60,
    "ERROR": 30 * 60,
    "EXPIRED": 24 * 60 * 60,
    "PAPER_CLOSED": 24 * 60 * 60,
    "CLOSED": 24 * 60 * 60,
}
ALWAYS_PROCESS = {"PAPER_OPEN", "PAPER_READY", "READY_FOR_CONFIRMATION"}
NORMAL_PROCESS = {"WATCHING", "UNKNOWN", "", None}


def _parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        text = str(value)
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _now(value: str | datetime | None = None) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    parsed = _parse_time(value)
    return parsed or datetime.now(timezone.utc)


def _token_address(token: Mapping[str, Any]) -> str:
    return str(token.get("token_address") or token.get("代币地址") or "")


def read_token_status(token_address: str, base_dir: str | Path = DEFAULT_BASE_DIR) -> Dict[str, Any]:
    path = Path(base_dir) / "tokens" / token_address / "token_status.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def should_process_token(
    token: Mapping[str, Any],
    *,
    base_dir: str | Path = DEFAULT_BASE_DIR,
    force: bool = False,
    now: str | datetime | None = None,
) -> Tuple[bool, str]:
    if force:
        return True, "force=True"
    token_address = _token_address(token)
    status = read_token_status(token_address, base_dir=base_dir)
    if not status:
        return True, "no previous status"
    current_state = status.get("current_state")
    if current_state in ALWAYS_PROCESS:
        return True, f"{current_state} requires continuous processing"
    if current_state in NORMAL_PROCESS:
        return True, f"{current_state} normal processing"
    cooldown = COOLDOWN_SECONDS.get(str(current_state))
    if cooldown is None:
        return True, f"no cooldown rule for {current_state}"
    last_update = _parse_time(status.get("last_update"))
    if not last_update:
        return True, "missing last_update"
    elapsed = (_now(now) - last_update).total_seconds()
    if elapsed >= cooldown:
        return True, f"cooldown expired for {current_state}"
    return False, f"skip {current_state}, cooldown remaining {int(cooldown - elapsed)} sec"
