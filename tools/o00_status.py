#!/usr/bin/env python3
"""O00 status helper."""
from pathlib import Path
import json


def read_status(repo_root: str, run_id: str) -> dict:
    p = Path(repo_root) / "data/her_document_function_system/o00_runs" / run_id / "state/pipeline_state.json"
    if not p.exists():
        return {"status": "NOT_FOUND", "path": str(p)}
    return json.loads(p.read_text(encoding="utf-8"))
