#!/usr/bin/env python3
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p = argparse.ArgumentParser(description='Hermes tool ledger closure check')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def load_jsonl(path):
    rows=[]
    if not path.exists():
        return rows
    for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip():
            continue
        try:
            row=json.loads(line)
            row['_line']=i
            rows.append(row)
        except Exception as e:
            rows.append({'_line':i,'parse_error':str(e),'raw':line})
    return rows

def main():
    a=parser().parse_args()
    base=Path(a.base)
    ledger=base/'03_task_runtime/tool_ledger.jsonl'
    rows=load_jsonl(ledger)
    findings=[]
    for r in rows:
        prefix=f"line {r.get('_line')} {r.get('tool_call_id','unknown')}: "
        if 'parse_error' in r:
            findings.append(prefix+'invalid_json')
            continue
        status=r.get('status')
        if not r.get('result_recorded'):
            findings.append(prefix+'missing_result_record')
        if status in ('PENDING','RUNNING'):
            findings.append(prefix+'open_tool_call')
        if r.get('interrupted') and not r.get('synthetic_result'):
            findings.append(prefix+'interrupted_without_synthetic_result')
        if status == 'FAILED' and not r.get('failure_reason'):
            findings.append(prefix+'failed_without_failure_reason')
    result={'tool_ledger_status':'BALANCED' if not findings else 'UNBALANCED','findings':findings,'records':len(rows),'dry_run':a.dry_run}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__':
    main()
