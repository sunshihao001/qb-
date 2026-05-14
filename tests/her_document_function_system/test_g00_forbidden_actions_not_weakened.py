import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_forbidden_actions_hard_blocked():
    from g00_policy_rule_builder import static_policies
    forbidden=static_policies()[0]
    actions={r['action']:r for r in forbidden['rules']}
    for a in ['live_runtime','wallet_signing','auto_deploy','production_trading']:
        assert actions[a]['policy_level']=='HARD_FORBIDDEN' and actions[a]['allowed_exception'] is False
