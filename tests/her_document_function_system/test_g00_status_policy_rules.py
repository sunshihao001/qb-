import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_status_ready_with_gaps_not_accepted():
    from g00_policy_rule_builder import static_policies
    status=static_policies()[1]
    rwg=[r for r in status['status_rules'] if r['status_code']=='READY_WITH_GAPS'][0]
    assert 'ACCEPTED' in rwg['forbidden_equivalent_statuses']
