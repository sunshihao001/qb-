
from __future__ import annotations
import csv, json, hashlib, shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
MISSING='missing'
PHASE='phase_01_data_fact'
REQUIRED_RAW=['raw_token_basic.json','raw_wallet_trade.json','raw_holder.json','raw_kline.json','raw_quote_security.json']
OPTIONAL_RAW=['raw_top_trader.json','raw_transfer.json','legacy_candidate_snapshot.json']
FORBIDDEN_STATUSES={'WALLET_SUPPORT','CONTROL_RETAINED','SCENARIO_ALLOW','PAPER_READY'}
def utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def parse_time(v):
    if not v or v=='missing': return None
    try: return datetime.fromisoformat(str(v).replace('Z','+00:00'))
    except Exception: return None
def ensure_dirs(run_dir):
    run_dir=Path(run_dir)
    for n in ['raw/copied_raw_files','raw/inventory','field_mapping','normalized','summary','handoff','reports','audit','manifest']:(run_dir/n).mkdir(parents=True,exist_ok=True)
def read_json(p):
    with Path(p).open(encoding='utf-8') as f:return json.load(f)
def write_json(p,data):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
def write_csv(p,rows,fieldnames):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,MISSING) for k in fieldnames})
def sha256_file(p):
    h=hashlib.sha256();
    with Path(p).open('rb') as f:
        for c in iter(lambda:f.read(1048576),b''): h.update(c)
    return h.hexdigest()
def clean_value(v):
    if v is None: return MISSING
    if isinstance(v,str) and v.strip()=='': return MISSING
    return v
def get_any(d,keys,default=MISSING):
    if not isinstance(d,dict): return default
    for k in keys:
        if k in d: return clean_value(d.get(k))
    return default
def listify(raw):
    if isinstance(raw,list): return [x if isinstance(x,dict) else {'value':x} for x in raw]
    if isinstance(raw,dict):
        for k in ['rows','items','data','trades','holders','klines','transfers','top_traders']:
            if isinstance(raw.get(k),list): return [x if isinstance(x,dict) else {'value':x} for x in raw[k]]
        return [raw]
    return []
def token_from_raw(raw,fallback): return str(get_any(raw.get('raw_token_basic.json') or {},['token_address','address','ca','mint'],fallback))
