#!/usr/bin/env python3
"""Hermes Harness V2.0 execution policy checker.

Safe, local, no secret reading. It evaluates requested tool/action metadata against
19_exec_policy/exec_policy_rules.jsonl and emits a machine-readable permission decision.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "19_exec_policy/exec_policy_rules.jsonl"
DECISIONS_PATH = ROOT / "19_exec_policy/permission_decisions.jsonl"


def load_policies():
    policies = []
    if POLICY_PATH.exists():
        for line in POLICY_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                policies.append(json.loads(line))
    return policies


def tool_matches(pattern: str, tool: str) -> bool:
    if pattern == "*":
        return True
    return any(part.strip() == tool for part in pattern.split("|"))


def evaluate(tool: str, action: str, path: str = "") -> dict:
    haystack = f"{tool}\n{action}\n{path}".lower()
    matched = None
    for policy in load_policies():
        if not tool_matches(policy.get("match_tool", "*"), tool):
            continue
        needle = str(policy.get("match", "")).lower()
        if needle and re.search(re.escape(needle), haystack):
            matched = policy
            break
    if matched is None:
        if tool in {"read_file", "search_files"}:
            matched = {"policy_id": "exec.default.read", "risk_level": "R1", "decision": "allow", "reason": "default read-only policy"}
        elif tool in {"write_file", "patch"} and str(path).startswith(str(ROOT)):
            matched = {"policy_id": "exec.default.harness_write", "risk_level": "R3", "decision": "allow", "reason": "authorized harness-local write"}
        else:
            matched = {"policy_id": "exec.default.ask", "risk_level": "R2", "decision": "ask", "reason": "no explicit allow/deny policy matched"}
    decision = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "route": "hermes_exec_policy_check_v2",
        "tool": tool,
        "action": action,
        "path": path,
        "decision": matched["decision"],
        "risk_level": matched["risk_level"],
        "matched_policy": f"{matched['policy_id']}:{matched.get('match', '')}" if "policy_id" in matched else str(matched.get("match", "manual")),
        "reason": matched.get("reason", ""),
        "requires_tool_result": True,
    }
    DECISIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DECISIONS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(decision, ensure_ascii=False) + "\n")
    return decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--path", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    decision = evaluate(args.tool, args.action, args.path)
    if args.json:
        print(json.dumps(decision, ensure_ascii=False))
    else:
        print(f"{decision['decision']} {decision['risk_level']} {decision['matched_policy']}: {decision['reason']}")


if __name__ == "__main__":
    main()
