#!/usr/bin/env python3
import json, sys
from pathlib import Path

def verify(path):
    p = Path(path)
    content = p.read_text(encoding='utf-8', errors='ignore') if p.exists() and p.is_file() else ''
    return {
        'path': str(p),
        'structure_verification': 'PASSED' if p.exists() else 'FAILED',
        'content_verification': 'PASSED' if content.strip() else 'FAILED',
        'flow_verification': 'MANUAL_REQUIRED',
        'risk_verification': 'MANUAL_REQUIRED',
        'evidence_verification': 'MANUAL_REQUIRED',
    }

if __name__ == '__main__':
    paths = sys.argv[1:]
    print(json.dumps([verify(p) for p in paths], ensure_ascii=False, indent=2))
