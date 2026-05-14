import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_handoff_targets_cover_required_controllers():
    from g00_policy_handoff_writer import all_handoffs
    handoffs=all_handoffs('run')
    for t in ['o00','k00','f00','v00','r00','a00','h00','u00','all']:
        assert t in handoffs
    assert 'wallet_signing' in handoffs['all']['forbidden_next_actions']
