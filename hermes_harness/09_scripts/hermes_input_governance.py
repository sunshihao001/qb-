#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def parser():
    p = argparse.ArgumentParser(description='Hermes input governance')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    p.add_argument('--input', default='', help='Input text or path to classify')
    return p

def classify(text: str):
    t = text.strip()
    if not t:
        return {'input_type':'empty','length_class':'short','relevance_class':'noise','duplicate_flag':False,'disposition':'discard','target_surface':'none'}
    if len(t) > 4000:
        length='long'
    elif len(t) > 1200:
        length='medium'
    else:
        length='short'
    if any(k in t.lower() for k in ['password','token','secret','private key']):
        return {'input_type':'secret','length_class':length,'relevance_class':'sensitive','duplicate_flag':False,'disposition':'discard','target_surface':'never'}
    if any(k in t.lower() for k in ['remember', 'memory', 'prefer']):
        disp='memory'
        target='04_memory'
    elif any(k in t.lower() for k in ['must', 'always', 'never', 'policy', 'constitution']):
        disp='passport'
        target='02_task_intake'
    elif len(t) > 2000:
        disp='summary'
        target='03_task_runtime'
    else:
        disp='context'
        target='03_task_runtime'
    return {'input_type':'text','length_class':length,'relevance_class':'unknown','duplicate_flag':False,'disposition':disp,'target_surface':target}

def main():
    a = parser().parse_args()
    text = a.input
    if text.startswith('@'):
        p = Path(text[1:])
        if p.exists():
            text = p.read_text(encoding='utf-8')
    result = classify(text)
    result.update({'dry_run': a.dry_run, 'base': str(Path(a.base))})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not a.dry_run and a.input:
        q = Path(a.base)/'03_task_runtime/input_governance_queue.jsonl'
        entry = {'input_id':'auto','input_type':result['input_type'],'length_class':result['length_class'],'relevance_class':result['relevance_class'],'duplicate_flag':result['duplicate_flag'],'disposition':result['disposition'],'target_surface':result['target_surface']}
        with q.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False)+'\n')
if __name__ == '__main__':
    main()
