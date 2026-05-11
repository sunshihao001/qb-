#!/usr/bin/env python3
import argparse, json, os
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p=argparse.ArgumentParser(description='Hermes memory revalidation')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def read_jsonl(path):
    rows=[]
    if path.exists():
        for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip():
                continue
            try:
                row=json.loads(line); row['_line']=i; rows.append(row)
            except Exception as e:
                rows.append({'_line':i,'parse_error':str(e),'raw':line})
    return rows

def main():
    a=parser().parse_args()
    base=Path(a.base)
    mem=base/'04_memory/verified_memory.jsonl'
    sup=base/'04_memory/superseded_memory.jsonl'
    log=base/'04_memory/memory_verification_log.jsonl'
    superseded_ids={str(r.get('memory_id') or r.get('id')) for r in read_jsonl(sup) if not r.get('parse_error')}
    findings=[]; checks=[]
    for r in read_jsonl(mem):
        if r.get('parse_error'):
            findings.append(f"line {r['_line']}: invalid_json")
            continue
        mid=str(r.get('memory_id') or r.get('id') or f"line_{r['_line']}")
        kind=r.get('memory_type') or r.get('type') or 'unknown'
        status='verified'
        reason='ok'
        path_val=r.get('path') or r.get('project_path')
        if path_val and not Path(path_val).exists():
            status='stale'; reason='path_missing'; findings.append(f'{mid}: path_missing {path_val}')
        if mid in superseded_ids or r.get('superseded_by'):
            status='superseded'; reason='superseded'; findings.append(f'{mid}: superseded')
        checks.append({'memory_id':mid,'memory_type':kind,'status':status,'reason':reason})
    out={'memory_revalidation_status':'PASSED' if not findings else 'WARN','findings':findings,'checks':checks,'dry_run':a.dry_run}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if not a.dry_run:
        with log.open('a',encoding='utf-8') as f:
            f.write(json.dumps(out,ensure_ascii=False)+'\n')
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__': main()
