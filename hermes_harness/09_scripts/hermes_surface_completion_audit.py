
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    p=parser('Hermes surface completion audit'); a=p.parse_args(); base=Path(a.base); findings=[]
    for rel in ['03_task_runtime/active_task_state.json','03_task_runtime/command_log.jsonl','08_reports/verification_reports']:
        if not (base/rel).exists(): findings.append('missing:'+rel)
    print(json.dumps({'surface_completion_risk':bool(findings),'findings':findings,'dry_run':a.dry_run},ensure_ascii=False,indent=2))
    raise SystemExit(0 if not findings else 2)
if __name__=='__main__': main()
