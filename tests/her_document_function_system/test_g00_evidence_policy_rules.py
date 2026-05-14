import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_evidence_policy_plan_not_evidence():
    from g00_policy_rule_builder import static_policies
    evidence=static_policies()[2]
    tested=[r for r in evidence['evidence_rules'] if r['claim']=='TESTED'][0]
    assert 'test_plan' in tested['invalid_evidence']
