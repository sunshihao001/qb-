
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def read_jsonl(p):
    rows=[]
    if p.exists():
      for line in p.read_text(encoding='utf-8').splitlines():
        if line.strip(): rows.append(json.loads(line))
    return rows
def main():
    p=parser('Hermes stale memory check'); a=p.parse_args(); base=Path(a.base); stale=read_jsonl(base/'04_memory/stale_memory.jsonl'); sup=read_jsonl(base/'04_memory/superseded_memory.jsonl')
    print(json.dumps({'stale':stale,'superseded':sup,'dry_run':a.dry_run},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
