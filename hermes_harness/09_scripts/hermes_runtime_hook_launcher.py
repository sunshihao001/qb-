#!/usr/bin/env python3
"""HER/Hermes runtime hook launcher.

Stable usable entrypoint for CLI, Gateway quick command, shell scripts, and
mobile-safe copy/paste usage. It wraps the V1.4 runtime hook runner and emits
a compact machine-readable contract for downstream callers.

No secrets are accepted, read, or printed.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "09_scripts" / "hermes_runtime_hook_run.py"
ROUTE = "hermes_runtime_hook_autonomous_problem_loop"

def build_parser():
    p = argparse.ArgumentParser(
        description="HER runtime hook launcher for CLI/Gateway quick command usage"
    )
    p.add_argument("--problem", required=True, help="User problem/request text. Do not include secrets.")
    p.add_argument("--dry-run", action="store_true", help="Run without external side effects; writes only harness artifacts.")
    p.add_argument("--json", action="store_true", help="Print compact JSON output for quick command / gateway callers.")
    p.add_argument("--origin", default="local", choices=["local", "cli", "gateway", "quick_command", "script"], help="Caller surface for audit metadata.")
    return p

def run(args):
    cmd = [sys.executable, str(RUNNER), "--problem", args.problem]
    if args.dry_run:
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        payload = {
            "status": "FAILED",
            "route": ROUTE,
            "dry_run": bool(args.dry_run),
            "origin": args.origin,
            "returncode": proc.returncode,
            "stderr": proc.stderr.strip()[-2000:],
            "stdout": proc.stdout.strip()[-2000:],
        }
        return payload, proc.returncode
    try:
        inner = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as exc:
        payload = {
            "status": "FAILED",
            "route": ROUTE,
            "dry_run": bool(args.dry_run),
            "origin": args.origin,
            "returncode": proc.returncode,
            "error": f"runner output was not JSON: {exc}",
            "stdout": proc.stdout.strip()[-2000:],
        }
        return payload, 1
    payload = {
        "status": inner.get("status", "UNKNOWN"),
        "route": ROUTE,
        "dry_run": bool(args.dry_run),
        "origin": args.origin,
        "runtime_run_id": inner.get("runtime_run_id"),
        "run_dir": inner.get("run_dir"),
        "overall_passed": bool(inner.get("overall_passed")),
        "entrypoint": str(Path(__file__).resolve()),
        "runner": str(RUNNER),
        "contract": {
            "runtime_state": "runtime_state.json",
            "tool_ledger": "tool_ledger.jsonl",
            "problem_passport": "problem_passport.md",
            "completion_audit": "runtime_completion_audit.md",
        },
    }
    return payload, 0 if payload["status"] == "COMPLETED" and payload["overall_passed"] else 1

def main():
    args = build_parser().parse_args()
    payload, code = run(args)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"HER runtime hook launcher: {payload['status']}")
        print(f"route: {payload['route']}")
        print(f"runtime_run_id: {payload.get('runtime_run_id')}")
        print(f"run_dir: {payload.get('run_dir')}")
        print(f"overall_passed: {payload.get('overall_passed')}")
    raise SystemExit(code)

if __name__ == "__main__":
    main()
