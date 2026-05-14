from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runner import Phase01Runner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Stable Trader OS Phase 01 data-fact runtime.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = Phase01Runner(Path(args.root)).run(Path(args.input), Path(args.output_dir))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
