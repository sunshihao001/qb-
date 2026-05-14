import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_local_active_not_system_enforced():
    from g00_policy_bundle_builder import build_bundles
    _, active, _=build_bundles('run')
    assert active['bundle_status']=='LOCAL_ACTIVE_WITH_GAPS'
    assert active['system_enforcement_status']=='NOT_YET_VERIFIED'
