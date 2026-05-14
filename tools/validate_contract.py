#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from modules.runtime.contract_validator import ContractValidator


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one SIKK input file against a phase contract")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--contract", required=True)
    args = parser.parse_args()

    result = ContractValidator().validate_file(Path(args.input_file), Path(args.contract))
    print(f"ok={result.ok}")
    print(f"status_code={result.status_code}")
    print(f"missing_fields={result.missing_fields}")
    print(f"hard_negative_trigger={result.hard_negative_trigger}")
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
