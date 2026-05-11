
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def classify(cmd):
    s=cmd.lower()
    if any(x in s for x in ['private','secret','token','git push','swap','trade','broadcast']): return 'R5','DENY'
    if any(x in s for x in ['rm -rf','mv ','overwrite']): return 'R4','DENY'
    if any(x in s for x in ['config','restart','systemctl']): return 'R3','ASK'
    if any(x in s for x in ['.py','patch','write']): return 'R2','ASK'
    return 'R0','ALLOW'
def main():
    p=parser('Hermes permission check'); p.add_argument('command', nargs='?', default='read'); a=p.parse_args(); r,perm=classify(a.command)
    print(json.dumps({'command':a.command,'risk_tier':r,'permission':perm,'dry_run':a.dry_run},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
