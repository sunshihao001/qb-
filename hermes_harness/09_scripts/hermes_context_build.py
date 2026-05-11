#!/usr/bin/env python3
import json, sys
from pathlib import Path
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('hermes_harness')
refs=['01_control_plane/hermes_constitution.md','03_task_runtime/active_task_state.json','03_task_runtime/active_task_context.md']
print(json.dumps({'base':str(base),'context_refs':[str(base/r) for r in refs if (base/r).exists()]}, ensure_ascii=False, indent=2))
