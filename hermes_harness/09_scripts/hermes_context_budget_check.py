#!/usr/bin/env python3
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p = argparse.ArgumentParser(description='Hermes context budget check')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    a=parser().parse_args()
    base=Path(a.base)
    p=base/'03_task_runtime/context_budget.json'
    if not p.exists():
        out={'budget_status':'MISSING','findings':['context_budget.json missing'],'dry_run':a.dry_run}
        print(json.dumps(out,ensure_ascii=False,indent=2))
        raise SystemExit(2)
    data=json.loads(p.read_text(encoding='utf-8'))
    findings=[]
    if data.get('budget_status') not in ('OK','OVER','WARN'):
        findings.append('invalid budget_status')
    if data.get('surfaces',{}).get('execution_log',{}).get('status') == 'admit':
        findings.append('execution_log should not be fully admitted')
    if data.get('surfaces',{}).get('command_log',{}).get('status') == 'admit':
        findings.append('command_log should not be fully admitted')
    if 'preserve_current_state' not in data.get('over_budget_policy',[]):
        findings.append('missing preserve_current_state policy')
    result={'budget_status':'OK' if not findings else 'WARN','findings':findings,'dry_run':a.dry_run}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__':
    main()
