#!/usr/bin/env python3
import json, sys
from pathlib import Path
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('hermes_harness')
required=['03_task_runtime/active_task_state.json','03_task_runtime/command_log.jsonl','03_task_runtime/checkpoints/checkpoint.json']
missing=[r for r in required if not (base/r).exists()]
print(json.dumps({'passed':not missing,'missing':missing}, ensure_ascii=False, indent=2))
raise SystemExit(0 if not missing else 2)
