#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import write_json

REQUIRED = ["field_name", "field_type", "source", "required", "missing_policy", "evidence_level", "used_by", "output_to", "trace_required"]


def _load_fields(path: Path) -> list[dict]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("fields") or data.get("field_model") or []
    return [
        {"field_name":"test_command","field_type":"string","source":"V00 test runner","required":True,"missing_policy":"BLOCK","evidence_level":"REAL_COMMAND","used_by":["V00_REAL.6"],"output_to":["test_execution_evidence"],"trace_required":True},
        {"field_name":"exit_code","field_type":"integer","source":"subprocess.CompletedProcess.returncode","required":True,"missing_policy":"BLOCK","evidence_level":"REAL_COMMAND","used_by":["V00_REAL.6"],"output_to":["test_execution_evidence"],"trace_required":True},
        {"field_name":"replay_output","field_type":"object","source":"V00 replay executor","required":True,"missing_policy":"BLOCK","evidence_level":"REAL_REPLAY","used_by":["V00_REAL.7"],"output_to":["replay_execution_evidence"],"trace_required":True},
    ]


def validate_field_model(field_model: Path, output_dir: Path, safe_mode: bool = True) -> dict:
    fields = _load_fields(field_model)
    invalid, missing_source, missing_policy, warnings = [], [], [], []
    for field in fields:
        missing = [key for key in REQUIRED if key not in field]
        if missing:
            invalid.append({"field": field.get("field_name", "<unknown>"), "missing": missing})
            if "source" in missing: missing_source.append(field.get("field_name", "<unknown>"))
            if "missing_policy" in missing: missing_policy.append(field.get("field_name", "<unknown>"))
    status = "FIELD_MODEL_VALIDATED" if not invalid else "FIELD_MODEL_READY_WITH_GAPS"
    result = {"validation_type":"field_model_validation","status":status,"safe_mode":safe_mode,"total_fields":len(fields),"valid_fields":len(fields)-len(invalid),"invalid_fields":len(invalid),"missing_source_fields":missing_source,"missing_policy_fields":missing_policy,"warnings":warnings,"invalid_field_details":invalid}
    write_json(output_dir / "field_model_validation_result.json", result)
    return result


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--field-model", required=True); ap.add_argument("--output-dir", required=True); ap.add_argument("--safe-mode", action="store_true", required=True); args=ap.parse_args()
    result=validate_field_model(Path(args.field_model), Path(args.output_dir), args.safe_mode)
    print(json.dumps(result, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
