#!/usr/bin/env python3
import json, datetime, re, sys
slug = sys.argv[1] if len(sys.argv)>1 else 'new_task'
slug = re.sub(r'[^a-zA-Z0-9_]+','_',slug).strip('_').lower() or 'new_task'
tid = 'hermes.task.'+datetime.datetime.utcnow().strftime('%Y%m%d.%H%M%S')+'.'+slug
print(json.dumps({'task_id':tid,'status':'RECEIVED'}, ensure_ascii=False, indent=2))
