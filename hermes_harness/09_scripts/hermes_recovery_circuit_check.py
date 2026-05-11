#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
VALID_STATUSES = {"CLOSED", "OPEN_IF_NEXT_FAILS", "OPEN", "HALF_OPEN", "BLOCKED"}


def parser():
    p = argparse.ArgumentParser(description="Hermes recovery circuit breaker check")
    p.add_argument("--base", default=str(BASE), help="Hermes harness root; defaults to this hermes_harness")
    p.add_argument("--dry-run", action="store_true", help="Do not write files")
    return p


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"__json_error__": str(exc)}


def main():
    args = parser().parse_args()
    base = Path(args.base)
    counter_path = base / "03_task_runtime" / "recovery_counter.json"
    findings = []
    status = "PASSED"

    data = load_json(counter_path)
    if data is None:
        findings.append({"severity": "error", "reason": "missing_recovery_counter", "path": str(counter_path)})
    elif "__json_error__" in data:
        findings.append({"severity": "error", "reason": "invalid_json", "detail": data["__json_error__"]})
    else:
        required = ["task_id", "same_error_count", "max_same_error_retry", "recovery_attempts", "circuit_breaker_status"]
        for key in required:
            if key not in data:
                findings.append({"severity": "error", "reason": "missing_key", "key": key})
        circuit_status = data.get("circuit_breaker_status")
        if circuit_status not in VALID_STATUSES:
            findings.append({"severity": "error", "reason": "invalid_circuit_breaker_status", "value": circuit_status})
        same_error_count = data.get("same_error_count", 0)
        max_retry = data.get("max_same_error_retry", 3)
        if isinstance(same_error_count, int) and isinstance(max_retry, int):
            if same_error_count > max_retry and circuit_status != "BLOCKED":
                findings.append({"severity": "error", "reason": "retry_limit_exceeded_without_blocked", "same_error_count": same_error_count, "max_same_error_retry": max_retry})
            elif same_error_count == max_retry and circuit_status not in {"OPEN", "BLOCKED", "OPEN_IF_NEXT_FAILS"}:
                findings.append({"severity": "warn", "reason": "retry_limit_reached_without_open_state", "same_error_count": same_error_count})
        else:
            findings.append({"severity": "error", "reason": "retry_counts_must_be_integers"})
        attempts = data.get("recovery_attempts", [])
        if not isinstance(attempts, list):
            findings.append({"severity": "error", "reason": "recovery_attempts_must_be_list"})
        else:
            for i, attempt in enumerate(attempts, start=1):
                for key in ["error_type", "attempt", "action", "result"]:
                    if key not in attempt:
                        findings.append({"severity": "error", "reason": "attempt_missing_key", "index": i, "key": key})

    if any(f.get("severity") == "error" for f in findings):
        status = "FAILED"
    elif findings:
        status = "WARN"

    out = {
        "recovery_circuit_status": status,
        "counter_path": str(counter_path),
        "findings": findings,
        "dry_run": args.dry_run,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if status in {"PASSED", "WARN"} else 2)


if __name__ == "__main__":
    main()
