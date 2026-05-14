import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_g00_requires_u00_handoff(tmp_path):
    out=tmp_path/'g00_missing'
    r=subprocess.run(['python3', str(TOOLS/'g00_real_policy_registry_executor.py'), '--u00-handoff', str(tmp_path/'missing.json'), '--repo-root', str(REPO), '--output-dir', str(out), '--safe-mode'], text=True, capture_output=True)
    assert r.returncode != 0
    acc=json.loads((out/'acceptance/g00_real_policy_acceptance.json').read_text())
    assert acc['final_status']=='G00_REAL_GOVERNANCE_POLICY_REGISTRY_BLOCKED'
