import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_conflict_checker_preserves_forbidden_actions():
    from g00_policy_conflict_checker import check_conflicts
    conflict, dup, weak=check_conflicts({'classified_candidates':[{'candidate_id':'a','policy_domain':'status_code_policy'}]})
    assert conflict['conflict_check_status']=='PASSED_WITH_GAPS'
    assert weak['weakened_rule_check_status']=='PASSED'
    assert 'wallet_signing' in weak['hard_forbidden_actions_preserved']
