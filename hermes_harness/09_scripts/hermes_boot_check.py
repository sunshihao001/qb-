
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    p=parser('Hermes boot check'); a=p.parse_args(); base=Path(a.base)
    state=base/'03_task_runtime/active_task_state.json'
    out={'state_exists':state.exists(),'allowed_to_execute':True,'blocked':False,'recovery_required':False,'dry_run':a.dry_run}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
