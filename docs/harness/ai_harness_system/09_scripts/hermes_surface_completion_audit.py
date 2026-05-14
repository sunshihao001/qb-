#!/usr/bin/env python3
import json, sys
from pathlib import Path

def audit(base):
    base=Path(base)
    findings=[]
    checks=[
      ('verification_report_missing', not (base/'verification_report.md').exists()),
      ('active_state_missing', not (base/'04_task_plans/active_task_state.json').exists()),
      ('audit_policy_missing', not (base/'08_audit/audit_independence_policy.md').exists()),
    ]
    for name,failed in checks:
        if failed: findings.append(name)
    return {'base':str(base),'surface_completion_risk':bool(findings),'findings':findings}
if __name__=='__main__':
    base=sys.argv[1] if len(sys.argv)>1 else 'docs/harness/ai_harness_system'
    print(json.dumps(audit(base), ensure_ascii=False, indent=2))
