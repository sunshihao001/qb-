#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Runtime token process trace logger."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _token_address(token: Mapping[str, Any]) -> str:
    return str(token.get("token_address") or token.get("代币地址") or "")


def _token_symbol(token: Mapping[str, Any]) -> str:
    return str(token.get("token_symbol") or token.get("代币符号") or token.get("symbol") or "")


def read_json_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _nested_status(payload: Mapping[str, Any], section: str, key: str) -> Any:
    value = payload.get(section, {})
    return value.get(key) if isinstance(value, Mapping) else None


def detect_state_change(previous: Mapping[str, Any], current: Mapping[str, Any]) -> Dict[str, Any]:
    prev_state = previous.get("current_state")
    cur_state = current.get("current_state")
    prev_wallet = _nested_status(previous, "wallet_structure", "wallet_structure_status")
    cur_wallet = _nested_status(current, "wallet_structure", "wallet_structure_status")
    prev_paper = _nested_status(previous, "paper", "paper_status")
    cur_paper = _nested_status(current, "paper", "paper_status")
    return {
        "state_changed": prev_state != cur_state,
        "wallet_changed": prev_wallet != cur_wallet,
        "paper_changed": prev_paper != cur_paper,
        "previous_state": prev_state,
        "current_state": cur_state,
        "previous_wallet_status": prev_wallet,
        "current_wallet_status": cur_wallet,
        "previous_paper_status": prev_paper,
        "current_paper_status": cur_paper,
    }


def write_process_trace(
    *,
    token: Mapping[str, Any],
    current_status: Mapping[str, Any],
    module_result: Optional[Mapping[str, Any]] = None,
    base_dir: str | Path = DEFAULT_BASE_DIR,
) -> Path:
    base = Path(base_dir)
    token_address = _token_address(token)
    token_dir = base / "tokens" / token_address
    previous_status = read_json_optional(token_dir / "token_status.json")
    change = detect_state_change(previous_status, current_status)
    row = {
        "time": iso_now(),
        "token_address": token_address,
        "token_symbol": _token_symbol(token),
        **change,
        "latest_action": current_status.get("latest_action"),
        "latest_reason": current_status.get("latest_reason"),
        "wallet_structure": current_status.get("wallet_structure", {}),
        "signal": current_status.get("signal", {}),
        "quote": current_status.get("quote", {}),
        "security": current_status.get("security", {}),
        "paper": current_status.get("paper", {}),
        "module_result": dict(module_result or {}),
    }
    path = token_dir / "process_trace.jsonl"
    append_jsonl(path, row)
    return path
