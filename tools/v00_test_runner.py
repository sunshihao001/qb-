#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import now_iso, parse_pytest_counts, run_command, write_json


def run_tests(test_path: Path, output_dir: Path, repo_root: Path, validation_run_id: str, safe_mode: bool = True, extra_args: list[str] | None = None) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = now_iso()
    command = ["python3", "-m", "pytest", str(test_path), "-q"] + (extra_args or [])
    result = run_command(command, cwd=repo_root, timeout=180)
    ended = now_iso()
    stdout_path = output_dir / "test_stdout.log"
    stderr_path = output_dir / "test_stderr.log"
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    passed, failed, skipped = parse_pytest_counts(result.stdout, result.returncode)
    evidence = {
        "evidence_id": f"test_evidence_{validation_run_id}",
        "validation_run_id": validation_run_id,
        "test_type": "pytest",
        "test_command": " ".join(command),
        "started_at": started,
        "ended_at": ended,
        "exit_code": result.returncode,
        "stdout_path": "test_execution/test_stdout.log",
        "stderr_path": "test_execution/test_stderr.log",
        "passed_count": passed,
        "failed_count": failed,
        "skipped_count": skipped,
        "covered_functions": ["V00_REAL_VALIDATION_EXECUTOR", "V00_STATUS_INTEGRITY"],
        "covered_rules": ["TESTED_REQUIRES_EXIT_CODE", "TEST_PLAN_NOT_TESTED", "NO_RUNNER_BOUND_WITHOUT_R00"],
        "status": "TESTED" if result.returncode == 0 else "TEST_FAILED",
        "failure_reason": None if result.returncode == 0 else "pytest exit_code != 0",
        "safe_mode": safe_mode,
    }
    write_json(output_dir / "test_execution_evidence.json", evidence)
    return evidence


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--test-path", required=True); ap.add_argument("--output-dir", required=True); ap.add_argument("--repo-root", default="."); ap.add_argument("--validation-run-id", default="v00_real_manual"); ap.add_argument("--safe-mode", action="store_true", required=True); args=ap.parse_args()
    ev=run_tests(Path(args.test_path), Path(args.output_dir), Path(args.repo_root), args.validation_run_id, args.safe_mode)
    print(json.dumps(ev, ensure_ascii=False)); return 0 if ev["exit_code"] == 0 else 1
if __name__ == "__main__": raise SystemExit(main())
