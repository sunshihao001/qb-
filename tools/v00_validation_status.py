#!/usr/bin/env python3
"""V00 shared utility functions for safe real validation evidence."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FINAL_STATUS = "V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS"
BLOCKED_STATUS = "V00_REAL_VALIDATION_BLOCKED"
FORBIDDEN_ACTIONS = ["live_runtime", "wallet_signing", "auto_deploy", "production_trading"]
FORBIDDEN_CLAIMS = ["RUNNER_BOUND", "POLICY_ACTIVE", "PIPELINE_ACCEPTED", "PRODUCTION_READY", "LIVE_READY"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": now_iso(), **event}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ensure_dirs(output_dir: Path) -> None:
    for rel in [
        "input", "preflight", "schema_validation", "contract_validation",
        "field_model_validation", "rule_logic_validation", "test_execution",
        "replay_execution", "failure_evidence", "evidence_bundle", "trace",
        "audit", "acceptance", "handoff", "reports",
    ]:
        (output_dir / rel).mkdir(parents=True, exist_ok=True)


def parse_pytest_counts(stdout: str, exit_code: int) -> tuple[int, int, int]:
    passed = failed = skipped = 0
    # Match common pytest summary fragments: "3 passed", "1 failed", "2 skipped".
    for number, kind in re.findall(r"(\d+)\s+(passed|failed|skipped)", stdout):
        if kind == "passed":
            passed += int(number)
        elif kind == "failed":
            failed += int(number)
        elif kind == "skipped":
            skipped += int(number)
    if passed == failed == skipped == 0 and exit_code == 0:
        passed = 1
    return passed, failed, skipped


def run_command(command: list[str], cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def collect_json_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.rglob("*.json") if p.is_file())


def status_from_failures(default_ready_status: str, failures: list[dict[str, Any]]) -> str:
    blocking = [f for f in failures if f.get("gap_level") == "BLOCKING_GAP"]
    return BLOCKED_STATUS if blocking else default_ready_status
