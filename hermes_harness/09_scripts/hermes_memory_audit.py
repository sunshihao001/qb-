#!/usr/bin/env python3
import json, sys
from pathlib import Path
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('hermes_harness')
mem=base/'04_memory'
findings=[]
summary={}
for name in ['memory_write_queue.jsonl','verified_memory.jsonl','stale_memory.jsonl','superseded_memory.jsonl']:
    p=mem/name
    rows=[]
    if not p.exists():
        findings.append(f'missing:{name}')
    else:
        for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): continue
            try:
                obj=json.loads(line); rows.append(obj)
                text=json.dumps(obj, ensure_ascii=False).lower()
                if any(k in text for k in ['private_key','secret_key','api_key=','token=','password=']):
                    findings.append(f'possible_secret:{name}:{i}')
                if name=='verified_memory.jsonl':
                    for req in ['status','validity','last_verified_at','stale_check_required','superseded_by']:
                        if req not in obj: findings.append(f'missing_field:{name}:{i}:{req}')
                    if obj.get('status')!='verified': findings.append(f'bad_status:{name}:{i}')
            except Exception as e:
                findings.append(f'parse_error:{name}:{i}:{e}')
    summary[name]=len(rows)
print(json.dumps({'passed':not findings,'summary':summary,'findings':findings}, ensure_ascii=False, indent=2))
raise SystemExit(0 if not findings else 2)
