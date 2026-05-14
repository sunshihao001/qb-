#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from v00_validation_status import FINAL_STATUS, read_json, write_json


def build_bundle(output_dir: Path, validation_run_id: str, source_pipeline_run_id: str, failures: list[dict[str, Any]] | None = None) -> dict:
    failures = failures or []
    def load(rel: str) -> dict:
        path = output_dir / rel
        return read_json(path) if path.exists() else {}
    schema = load("schema_validation/schema_validation_result.json")
    contract = load("contract_validation/contract_validation_result.json")
    field = load("field_model_validation/field_model_validation_result.json")
    rule = load("rule_logic_validation/rule_logic_validation_result.json")
    test = load("test_execution/test_execution_evidence.json")
    replay = load("replay_execution/replay_execution_evidence.json")
    blocking = [f for f in failures if f.get("gap_level") == "BLOCKING_GAP"]
    bundle = {
        "bundle_id": f"validation_evidence_bundle_{validation_run_id}",
        "validation_run_id": validation_run_id,
        "source_pipeline_run_id": source_pipeline_run_id,
        "evidence_groups": {
            "schema_validation": ["schema_validation/schema_validation_result.json"],
            "contract_validation": ["contract_validation/contract_validation_result.json"],
            "field_model_validation": ["field_model_validation/field_model_validation_result.json"],
            "rule_logic_validation": ["rule_logic_validation/rule_logic_validation_result.json"],
            "test_execution": ["test_execution/test_execution_evidence.json", "test_execution/test_stdout.log", "test_execution/test_stderr.log"],
            "replay_execution": ["replay_execution/replay_execution_evidence.json", "replay_execution/replay_input.json", "replay_execution/replay_output.json", "replay_execution/replay_trace.jsonl", "replay_execution/replay_comparison.json"],
            "failure_evidence": ["failure_evidence/failure_evidence.json"],
            "trace_audit": ["trace/v00_real_validation_trace.jsonl", "audit/v00_real_validation_audit.jsonl"],
        },
        "summary": {
            "schema_status": schema.get("status"),
            "contract_status": contract.get("status"),
            "field_model_status": field.get("status"),
            "rule_logic_status": rule.get("status"),
            "test_status": test.get("status"),
            "replay_status": replay.get("status"),
            "final_validation_status": "V00_REAL_VALIDATION_BLOCKED" if blocking else FINAL_STATUS,
        },
        "open_gaps": [f for f in failures if f.get("gap_level") != "BLOCKING_GAP"],
        "blocking_gaps": blocking,
        "ready_for_a00": not blocking,
        "ready_for_r00": False,
    }
    write_json(output_dir / "evidence_bundle/validation_evidence_bundle.json", bundle)
    return bundle


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output-dir", required=True); ap.add_argument("--validation-run-id", required=True); ap.add_argument("--source-pipeline-run-id", required=True); args=ap.parse_args()
    b=build_bundle(Path(args.output_dir), args.validation_run_id, args.source_pipeline_run_id)
    print(json.dumps(b, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
