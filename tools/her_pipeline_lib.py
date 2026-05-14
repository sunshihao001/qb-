from __future__ import annotations
import json, re, hashlib
from pathlib import Path
from datetime import datetime, timezone

FINAL_STATUS = 'HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS'

def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def ensure_dirs(run_dir: Path):
    for d in ['input','k00','f00','v00','a00','h00','u00','g00','o00','recovery']:
        (run_dir/d).mkdir(parents=True, exist_ok=True)

def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path

def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def append_jsonl(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

def trace(run_dir: Path, run_id: str, phase: str, event: str, status: str, **extra):
    data={'timestamp': utcnow(), 'run_id': run_id, 'phase': phase, 'event': event, 'status': status}
    data.update(extra)
    append_jsonl(run_dir/'trace.jsonl', data)

def audit(run_dir: Path, run_id: str, event: str, status: str, **extra):
    data={'timestamp': utcnow(), 'run_id': run_id, 'event': event, 'status': status}
    data.update(extra)
    append_jsonl(run_dir/'audit.jsonl', data)

def text_sections(text: str):
    out=[]
    for idx,m in enumerate(re.finditer(r'^(#{1,3})\s+(.+)$', text, re.M), start=1):
        out.append({'section_id': f'sec_{idx:03d}', 'level': len(m.group(1)), 'title': m.group(2).strip(), 'char_offset': m.start()})
    return out

def infer_key_points(text: str):
    candidates=[]
    for line in text.splitlines():
        s=line.strip('- `')
        if any(k in s for k in ['必须','禁止','safe-mode','K00','F00','V00','A00','H00','U00','G00','O00','READY_WITH_GAPS']):
            if 8 <= len(s) <= 160:
                candidates.append(s)
    return candidates[:20]

def sha256_file(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
