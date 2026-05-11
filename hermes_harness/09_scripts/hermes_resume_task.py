
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    p=parser('Hermes resume task'); p.add_argument('checkpoint', nargs='?', default=None); a=p.parse_args(); cp=Path(a.checkpoint) if a.checkpoint else Path(a.base)/'03_task_runtime/checkpoints/checkpoint.json'
    if not cp.exists(): out={'can_resume':False,'reason':'checkpoint not found','dry_run':a.dry_run}
    else:
        data=json.loads(cp.read_text(encoding='utf-8')); out={'can_resume':bool(data.get('verified')),'next_phase':data.get('next_phase'),'resume_command':data.get('resume_command'),'required_context_files':data.get('required_context_files',[]),'dry_run':a.dry_run}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
