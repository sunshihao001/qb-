#!/usr/bin/env python3
import json, sys, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
STATE = BASE / '04_task_plans' / 'active_task_state.json'

def main():
    state_exists = STATE.exists()
    state = None
    if state_exists:
        try:
            state = json.loads(STATE.read_text())
        except Exception as e:
            state = {'parse_error': str(e)}
    blocked = bool(state and state.get('blocked'))
    recovery = bool(state and state.get('recovery_required'))
    status = state.get('status') if isinstance(state, dict) else None
    if not state_exists:
        task_mode = 'new'
        allowed = True
    elif blocked:
        task_mode = 'blocked'
        allowed = False
    elif recovery:
        task_mode = 'recovery'
        allowed = False
    elif status in ('DONE','ARCHIVED'):
        task_mode = 'new'
        allowed = True
    else:
        task_mode = 'resume'
        allowed = True
    report = {
        'checked_at': datetime.datetime.utcnow().isoformat()+'Z',
        'state_file': str(STATE),
        'state_exists': state_exists,
        'task_mode': task_mode,
        'has_unfinished_task': state_exists and status not in ('DONE','ARCHIVED'),
        'blocked': blocked,
        'recovery_required': recovery,
        'allowed_to_execute': allowed,
        'need_verify_old_task': task_mode in ('resume','recovery','blocked'),
    }
    out = BASE / '00_startup' / 'startup_check_report.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('# Startup Check Report\n\n```json\n'+json.dumps(report, ensure_ascii=False, indent=2)+'\n```\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if allowed else 2

if __name__ == '__main__':
    raise SystemExit(main())
