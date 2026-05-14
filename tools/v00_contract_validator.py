#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import collect_json_files, write_json

REQUIRED_MARKERS = {"required_inputs", "required_outputs", "forbidden_actions", "gap_refs", "trace_refs", "acceptance_result", "handoff_refs", "missing_policy"}


def validate_contracts_dir(contracts_dir: Path, output_dir: Path, safe_mode: bool = True) -> dict:
    files = collect_json_files(contracts_dir)
    checked, valid, invalid, missing_fields, errors, warnings = [], [], [], [], [], []
    for path in files:
        name = path.name.lower()
        if "contract" not in name and "handoff" not in name and "config" not in name:
            continue
        checked.append(str(path))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            invalid.append(str(path)); errors.append({"contract": str(path), "error": str(exc)}); continue
        present = set(data.keys())
        # Some existing HER files are schemas/configs, so missing policy markers become gaps, not automatic block.
        missing = sorted(REQUIRED_MARKERS - present)
        if missing:
            missing_fields.append({"contract": str(path), "missing": missing})
            warnings.append({"contract": str(path), "warning": "contract governance markers incomplete", "missing": missing})
        valid.append(str(path))
    status = "CONTRACT_VALIDATED" if checked else "CONTRACT_MISSING"
    if invalid:
        status = "CONTRACT_INVALID"
    elif missing_fields:
        status = "CONTRACT_READY_WITH_GAPS"
    result = {
        "validation_type": "contract_validation",
        "status": status,
        "safe_mode": safe_mode,
        "contracts_checked": checked,
        "valid_contracts": valid,
        "invalid_contracts": invalid,
        "missing_required_fields": missing_fields,
        "errors": errors,
        "warnings": warnings,
    }
    write_json(output_dir / "contract_validation_result.json", result)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contracts-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--safe-mode", action="store_true", required=True)
    args = ap.parse_args()
    result = validate_contracts_dir(Path(args.contracts_dir), Path(args.output_dir), args.safe_mode)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"CONTRACT_VALIDATED", "CONTRACT_READY_WITH_GAPS"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
