#!/usr/bin/env python3
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FINAL_STATUS = "A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS"
BLOCKED_STATUS = "A00_REAL_ACCEPTANCE_BLOCKED"
FORBIDDEN_ACTIONS = ["live_runtime", "wallet_signing", "auto_deploy", "production_trading", "execute_real_order"]
FORBIDDEN_CLAIMS = ["PIPELINE_ACCEPTED", "POLICY_ACTIVE", "PRODUCTION_READY", "LIVE_READY"]
REQUIRED_GROUPS = ["o00_pipeline", "k00_intake", "f00_function_realization", "v00_real_validation", "r00_real_binding", "gap_register", "trace_audit", "governance_policy"]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: str | Path) -> Any:
    p=Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def write_json(path: str | Path, data: Any) -> None:
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def append_jsonl(path: str | Path, event: dict[str, Any]) -> None:
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"timestamp": now_iso(), **event}, ensure_ascii=False)+"\n")

def rel_or_abs(repo_root: Path, path: str | None) -> Path | None:
    if not path: return None
    p=Path(path)
    return p if p.is_absolute() else repo_root / p

def ensure_dirs(output_dir: Path) -> None:
    for rel in ["input","preflight","evidence_bundle","phase_status","artifact_manifest","gap_review","trace_audit","scorecard","decision","certificate","failure_summary","recovery","handoff","reports"]:
        (output_dir/rel).mkdir(parents=True, exist_ok=True)

def status_from_blockers(blockers: list[Any]) -> str:
    return BLOCKED_STATUS if blockers else FINAL_STATUS
