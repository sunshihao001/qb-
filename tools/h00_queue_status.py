#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/her_document_function_system/h00_real_queue_runs")
print(json.dumps({"path": str(p), "exists": p.exists()}, ensure_ascii=False))
