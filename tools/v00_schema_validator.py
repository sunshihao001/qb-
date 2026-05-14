#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import collect_json_files, write_json


def validate_schema_dir(schema_dir: Path, output_dir: Path, safe_mode: bool = True) -> dict:
    schemas = collect_json_files(schema_dir)
    valid, invalid, errors, warnings = [], [], [], []
    for path in schemas:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and ("type" in data or "$schema" in data or "properties" in data or "required" in data or "controller_id" in data or "phase_id" in data):
                valid.append(str(path))
            else:
                warnings.append({"schema": str(path), "warning": "json parsed but schema markers are weak"})
                valid.append(str(path))
        except Exception as exc:  # noqa: BLE001
            invalid.append(str(path))
            errors.append({"schema": str(path), "error": str(exc)})
    status = "SCHEMA_INVALID" if invalid else ("SCHEMA_VALIDATED" if schemas else "SCHEMA_MISSING")
    result = {
        "validation_type": "schema_validation",
        "status": status,
        "safe_mode": safe_mode,
        "schemas_checked": [str(p) for p in schemas],
        "valid_schemas": valid,
        "invalid_schemas": invalid,
        "errors": errors,
        "warnings": warnings,
    }
    write_json(output_dir / "schema_validation_result.json", result)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--safe-mode", action="store_true", required=True)
    args = ap.parse_args()
    result = validate_schema_dir(Path(args.schema_dir), Path(args.output_dir), args.safe_mode)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"SCHEMA_VALIDATED", "SCHEMA_READY_WITH_GAPS"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
