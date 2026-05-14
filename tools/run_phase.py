#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from modules.runtime.phase_runner import PhaseRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one SIKK HER runtime phase")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    parser.add_argument("--phase", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()

    result = PhaseRunner(Path(args.root)).run(
        phase=args.phase,
        mode=args.mode,
        token=args.token,
        input_file=Path(args.input_file),
    )
    print(f"status_code={result.status_code}")
    print(f"output={result.output_path}")
    print(f"audit={result.audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
