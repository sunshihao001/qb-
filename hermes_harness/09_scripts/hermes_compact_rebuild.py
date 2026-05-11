#!/usr/bin/env python3
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p = argparse.ArgumentParser(description='Hermes compact rebuild')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    a=parser().parse_args()
    base=Path(a.base)
    snap=base/'03_task_runtime/compact_snapshots'
    boundary=snap/'compact_boundary.json'
    summary=snap/'compact_summary.md'
    post=snap/'post_compact_context.md'
    findings=[]
    for p in [boundary, summary, post]:
        if not p.exists():
            findings.append(f'missing:{p.name}')
    if post.exists():
        text=post.read_text(encoding='utf-8')
        required=['Current Task ID','Current Phase','Completed Phases','Key Files','Current Errors','Pending Verification Items','Next Action','Forbidden Actions','Recovery Entry']
        for r in required:
            if r not in text:
                findings.append(f'post_compact_missing:{r}')
    out={'compact_status':'OK' if not findings else 'WARN','findings':findings,'dry_run':a.dry_run}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__':
    main()
