#!/usr/bin/env python3
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FILES = [BASE/'03_context_governance/stale_memory.jsonl', BASE/'03_context_governance/superseded_memory.jsonl']

def read_jsonl(p):
    rows=[]
    if not p.exists(): return rows
    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            rows.append({'parse_error':str(e),'line':i,'file':str(p)})
    return rows

def main():
    rows=[]
    for f in FILES: rows.extend(read_jsonl(f))
    summary={'checked_files':[str(f) for f in FILES], 'count':len(rows), 'stale':[r for r in rows if r.get('status')=='stale'], 'superseded':[r for r in rows if r.get('status')=='superseded']}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
if __name__=='__main__': main()
