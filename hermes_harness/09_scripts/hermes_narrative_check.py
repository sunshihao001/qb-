#!/usr/bin/env python3
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p = argparse.ArgumentParser(description='Hermes execution narrative check')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    a=parser().parse_args()
    p=Path(a.base)/'03_task_runtime/execution_narrative.md'
    findings=[]
    if not p.exists():
        findings.append('execution_narrative missing')
    else:
        text=p.read_text(encoding='utf-8')
        required=['why the phase exists','which rule it follows','what input it used','what output it produced','whether it passed verification','why it failed','what state it reached after recovery']
        for r in required:
            if r not in text:
                findings.append(f'missing:{r}')
    out={'narrative_status':'OK' if not findings else 'WARN','findings':findings,'dry_run':a.dry_run}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__':
    main()
