#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import write_json

REQUIRED = ["rule_id", "rule_type", "input_fields", "calculation_method", "threshold_or_condition", "positive_evidence", "counter_evidence", "failure_condition", "output_status", "trace_required"]


def _load_rules(path: Path) -> list[dict]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list): return data
        if isinstance(data, dict): return data.get("rules") or data.get("rule_logic") or []
    return [
        {"rule_id":"V00_TESTED_REQUIRES_COMMAND_EVIDENCE","rule_type":"status_integrity","input_fields":["test_command","exit_code","stdout_path","stderr_path","passed_count","failed_count"],"calculation_method":"deterministic_required_fields","threshold_or_condition":"all required fields present and exit_code == 0","positive_evidence":["test_execution_evidence.json"],"counter_evidence":["test_plan_only"],"failure_condition":"missing command/exit/stdout/stderr/counts or exit_code != 0","output_status":"TESTED","trace_required":True},
        {"rule_id":"V00_REPLAY_TESTED_REQUIRES_IO_TRACE_COMPARISON","rule_type":"replay_integrity","input_fields":["replay_input","replay_output","trace_path","replay_comparison"],"calculation_method":"deterministic_required_files","threshold_or_condition":"all replay artifacts exist","positive_evidence":["replay_execution_evidence.json"],"counter_evidence":["replay_plan_only"],"failure_condition":"missing replay artifacts","output_status":"REPLAY_TESTED","trace_required":True},
    ]


def validate_rule_logic(rule_logic: Path, output_dir: Path, safe_mode: bool = True) -> dict:
    rules = _load_rules(rule_logic)
    invalid, blocked, warnings = [], [], []
    for rule in rules:
        missing = [key for key in REQUIRED if key not in rule]
        ai_only = str(rule.get("calculation_method", "")).strip() in {"AI 判断", "AI judgment"}
        if missing or ai_only:
            detail = {"rule_id": rule.get("rule_id", "<unknown>"), "missing": missing, "ai_only": ai_only}
            invalid.append(detail)
            if "input_fields" in missing or "output_status" in missing or ai_only:
                blocked.append(detail)
    status = "RULE_LOGIC_VALIDATED" if not invalid else ("RULE_LOGIC_INVALID" if blocked else "RULE_LOGIC_READY_WITH_GAPS")
    result = {"validation_type":"rule_logic_validation","status":status,"safe_mode":safe_mode,"total_rules":len(rules),"valid_rules":len(rules)-len(invalid),"invalid_rules":len(invalid),"blocked_rules":blocked,"warnings":warnings,"invalid_rule_details":invalid}
    write_json(output_dir / "rule_logic_validation_result.json", result)
    return result


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--rule-logic", required=True); ap.add_argument("--output-dir", required=True); ap.add_argument("--safe-mode", action="store_true", required=True); args=ap.parse_args()
    result=validate_rule_logic(Path(args.rule_logic), Path(args.output_dir), args.safe_mode)
    print(json.dumps(result, ensure_ascii=False)); return 0 if result["status"] != "RULE_LOGIC_INVALID" else 1
if __name__ == "__main__": raise SystemExit(main())
