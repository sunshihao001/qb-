#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run-dir', required=True); args=ap.parse_args()
    r=Path(args.run_dir)
    summary=r/'o00/run_summary.json'
    if not summary.exists():
        print(json.dumps({'run_dir':str(r),'status':'RUN_NOT_FOUND_OR_INCOMPLETE'}, ensure_ascii=False)); return 1
    data=json.loads(summary.read_text(encoding='utf-8'))
    print(json.dumps({'run_dir':str(r), **data}, ensure_ascii=False, indent=2)); return 0
if __name__ == '__main__':
    raise SystemExit(main())
