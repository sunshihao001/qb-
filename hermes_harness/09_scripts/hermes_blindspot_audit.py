#!/usr/bin/env python3
import json, sys
from pathlib import Path
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('hermes_harness')
checks={
 'directory_invocation_policy': base/'01_control_plane/directory_invocation_policy.md',
 'boot_check_script': base/'09_scripts/hermes_boot_check.py',
 'task_routing_policy': base/'01_control_plane/task_routing_policy.md',
 'command_log': base/'03_task_runtime/command_log.jsonl',
 'advanced_verification': base/'06_verification/verification_policy_advanced.md',
 'recovery_decision_table': base/'01_control_plane/recovery_decision_table.md',
 'stale_memory': base/'04_memory/stale_memory.jsonl',
 'execution_loop_log': base/'03_task_runtime/execution_loop_log.jsonl',
 'phase_report_template': base/'05_templates/phase_report_template.md',
 'executor_verifier_policy': base/'10_audit/executor_verifier_role_policy.md',
}
findings=[]
for name,path in checks.items():
    if not path.exists(): findings.append(f'missing:{name}:{path}')
# content spot checks
content_checks={
 'command_log_has_risk_permission': (base/'03_task_runtime/command_log.jsonl', ['risk_tier','permission']),
 'phase_report_has_rationale': (base/'05_templates/phase_report_template.md', ['Why this step','Rule basis','Output consumer']),
 'task_routing_mentions_passport': (base/'01_control_plane/task_routing_policy.md', ['passport','任务护照']),
}
for name,(path,terms) in content_checks.items():
    txt=path.read_text(encoding='utf-8') if path.exists() else ''
    if not all(t in txt for t in terms): findings.append(f'content_gap:{name}')
print(json.dumps({'passed':not findings,'findings':findings}, ensure_ascii=False, indent=2))
raise SystemExit(0 if not findings else 2)
