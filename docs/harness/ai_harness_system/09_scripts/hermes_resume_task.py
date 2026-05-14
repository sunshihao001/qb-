#!/usr/bin/env python3
import json, sys
from pathlib import Path

def main():
    checkpoint = Path(sys.argv[1]) if len(sys.argv)>1 else Path('docs/harness/ai_harness_system/04_task_plans/checkpoints/checkpoint.json')
    if not checkpoint.exists():
        print(json.dumps({'can_resume':False,'reason':'checkpoint not found','checkpoint':str(checkpoint)}, ensure_ascii=False, indent=2)); return 2
    data=json.loads(checkpoint.read_text(encoding='utf-8'))
    can=bool(data.get('verified'))
    print(json.dumps({'can_resume':can,'next_phase':data.get('next_phase'),'resume_command':data.get('resume_command'),'required_context_files':data.get('required_context_files',[])}, ensure_ascii=False, indent=2))
    return 0 if can else 3
if __name__=='__main__': raise SystemExit(main())
