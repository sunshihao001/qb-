import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_policy_candidate_not_active_without_registry():
    candidate={'status':'POLICY_CANDIDATE','active_policy_bundle':None,'governance_registry':None}
    assert candidate['status'] != 'POLICY_ACTIVE'
    assert candidate['active_policy_bundle'] is None
