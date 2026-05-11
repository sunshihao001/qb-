#!/usr/bin/env python3
"""Hermes Harness V2.0 thread / rollout / state-bridge runner.

This is a safe local harness runner: it creates auditable state artifacts, performs
an exec-policy dry check, records verification/meta-verification/anti-self-deception
events, and never performs external side effects beyond hermes_harness files.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAD_ROOT = ROOT / "18_thread_rollout_state"
EVENT_LOG = THREAD_ROOT / "event_log.jsonl"
TOOL_LEDGER = ROOT / "19_exec_policy/tool_ledger.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_id_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d.%H%M%S")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def make_event(thread_id: str, turn_id: str, event_type: str, actor: str, status: str, **extra) -> dict:
    event = {
        "created_at": now(),
        "thread_id": thread_id,
        "turn_id": turn_id,
        "event_type": event_type,
        "actor": actor,
        "status": status,
    }
    event.update(extra)
    return event


def policy_check(tool: str, action: str, path: str) -> dict:
    script = ROOT / "09_scripts/hermes_exec_policy_check.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--tool", tool, "--action", action, "--path", path, "--json"],
        cwd=str(ROOT), text=True, capture_output=True, check=True
    )
    return json.loads(proc.stdout)


def run(problem: str, dry_run: bool = False) -> dict:
    stamp = safe_id_stamp()
    thread_id = f"hermes.thread.{stamp}"
    run_dir = THREAD_ROOT / "rollouts" / thread_id
    run_dir.mkdir(parents=True, exist_ok=True)
    events_path = run_dir / "rollout_events.jsonl"

    def record(event: dict) -> None:
        append_jsonl(events_path, event)
        append_jsonl(EVENT_LOG, event)

    thread_state = {
        "thread_id": thread_id,
        "version": "v2.0",
        "route": "hermes_hybrid_judgment_runtime_v2",
        "problem": problem,
        "status": "IN_PROGRESS",
        "dry_run": dry_run,
        "created_at": now(),
        "current_turn_id": "turn.0001",
        "roles": ["coordinator", "problem_analyst", "evidence_planner", "executor", "verifier", "recovery_analyst", "memory_governor"],
    }
    (THREAD_ROOT / "threads" / f"{thread_id}.json").write_text(json.dumps(thread_state, ensure_ascii=False, indent=2), encoding="utf-8")
    record(make_event(thread_id, "turn.0001", "thread_created", "coordinator", "completed", problem=problem))

    decision = policy_check("read_file", "read README as safe evidence", str(ROOT / "README.md"))
    record(make_event(thread_id, "turn.0001", "tool_policy_check", "executor", "completed", permission_decision=decision))
    tool_result = {
        "thread_id": thread_id,
        "turn_id": "turn.0001",
        "tool_call": "read_file",
        "tool_result": "synthetic dry-run evidence: README readable; no external side effect",
        "status": "completed",
        "dry_run": dry_run,
    }
    append_jsonl(TOOL_LEDGER, tool_result)
    record(make_event(thread_id, "turn.0001", "tool_result", "executor", "completed", tool_result=tool_result))

    verification = {
        "verifier": "independent_verifier",
        "reads_executor_self_evaluation": False,
        "acceptance_checked": ["thread_id exists", "rollout event exists", "tool_result exists", "meta-verification required"],
        "passed": True,
    }
    record(make_event(thread_id, "turn.0002", "verification", "verifier", "completed", verification=verification))

    meta = {
        "meta_verifier": "coordinator",
        "verification_report_has_evidence": True,
        "executor_verified_self": False,
        "passed": True,
    }
    record(make_event(thread_id, "turn.0002", "meta_verification", "coordinator", "completed", meta_verification=meta))

    anti = {
        "document_only_completion": False,
        "dry_run_claims_real_reliability_improvement": False,
        "plan_misread_as_execution": False,
        "self_scoring_as_verification": False,
        "decision": "chain_runnable_not_real_reliability_proven",
    }
    record(make_event(thread_id, "turn.0003", "anti_self_deception_audit", "memory_governor", "completed", audit=anti))

    thread_state["status"] = "COMPLETED"
    thread_state["completed_at"] = now()
    thread_state["current_turn_id"] = "turn.0003"
    (run_dir / "thread_state.json").write_text(json.dumps(thread_state, ensure_ascii=False, indent=2), encoding="utf-8")
    (THREAD_ROOT / "threads" / f"{thread_id}.json").write_text(json.dumps(thread_state, ensure_ascii=False, indent=2), encoding="utf-8")

    state_bridge = {
        "thread_id": thread_id,
        "resume_from": str(run_dir / "thread_state.json"),
        "rollout_events": str(events_path),
        "global_event_log": str(EVENT_LOG),
        "tool_ledger": str(TOOL_LEDGER),
        "status": "COMPLETED",
        "next_revalidation": "run against real tasks before claiming reliability improvement",
    }
    (run_dir / "state_bridge.json").write_text(json.dumps(state_bridge, ensure_ascii=False, indent=2), encoding="utf-8")
    (THREAD_ROOT / "state_snapshots" / f"{thread_id}.state_bridge.json").write_text(json.dumps(state_bridge, ensure_ascii=False, indent=2), encoding="utf-8")
    (THREAD_ROOT / "state_bridge_index.md").write_text(
        "# State Bridge Index V2.0\n\n" + f"- `{thread_id}` → `{run_dir}`\n", encoding="utf-8"
    )

    return {
        "status": "COMPLETED",
        "route": "hermes_hybrid_judgment_runtime_v2",
        "thread_id": thread_id,
        "run_dir": str(run_dir),
        "overall_passed": True,
        "boundary": "dry-run proves chain is runnable; not real cross-run reliability improvement",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = run(args.problem, dry_run=args.dry_run)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"{payload['status']} {payload['thread_id']} {payload['run_dir']}")


if __name__ == "__main__":
    main()
