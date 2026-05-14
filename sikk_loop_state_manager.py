#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Loop state manager for the research loop."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

DEFAULT_LOOP_STATE_DIR = Path("research_loop/loop_state")
VALID_STATES = [
    "WAITING_INPUT",
    "DOCUMENT_CAPTURED",
    "PASSPORT_CREATED",
    "OUTLINE_BUILT",
    "METHOD_ANALYZED",
    "SYSTEM_MAPPED",
    "GAPS_DETECTED",
    "TASK_PACKAGE_CREATED",
    "REPOMIX_CONTEXT_READY",
    "HERMES_EXECUTING",
    "ACCEPTANCE_CHECKED",
    "HANDOFF_WRITTEN",
    "GPT_REVIEW_READY",
    "NEXT_LOOP",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: Path) -> Dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def record_loop_state(*, state: str, loop_id: str, note: str = "", output_root: str | Path = DEFAULT_LOOP_STATE_DIR.parent) -> Dict[str, str]:
    if state not in VALID_STATES:
        raise ValueError(f"invalid loop state: {state}")
    root = Path(output_root)
    state_dir = root / "loop_state"
    state_dir.mkdir(parents=True, exist_ok=True)
    current_path = state_dir / "current_loop.json"
    history_path = state_dir / "loop_history.jsonl"
    previous = _load_json(current_path)
    payload = {
        "loop_id": loop_id,
        "state": state,
        "note": note,
        "updated_at": _utc_now(),
        "previous_state": previous.get("state", ""),
    }
    current_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return {"current_loop_json": str(current_path), "loop_history_jsonl": str(history_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record research loop state")
    parser.add_argument("--state", required=True)
    parser.add_argument("--loop-id", required=True)
    parser.add_argument("--note", default="")
    parser.add_argument("--output-root", default="research_loop")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(record_loop_state(state=args.state, loop_id=args.loop_id, note=args.note, output_root=args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
