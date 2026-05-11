
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    p=parser('Hermes artifact verify'); p.add_argument('paths', nargs='*'); a=p.parse_args(); rows=[]
    for x in a.paths:
        path=Path(x)
        rows.append({'path':x,'structure_verification':'PASSED' if path.exists() and path.stat().st_size>=0 else 'FAILED','content_verification':'PASSED' if path.exists() and (path.is_dir() or path.stat().st_size>0) else 'FAILED','flow_verification':'MANUAL_REQUIRED','risk_verification':'MANUAL_REQUIRED','evidence_verification':'MANUAL_REQUIRED','dry_run':a.dry_run})
    print(json.dumps(rows,ensure_ascii=False,indent=2))
    raise SystemExit(0 if all(r['structure_verification']=='PASSED' and r['content_verification']=='PASSED' for r in rows) else 2)
if __name__=='__main__': main()
