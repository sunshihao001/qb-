import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_cognition_patch_report_pass():
    p=ROOT/'data/coordination/latest/cognition_patch_report.json'
    assert p.exists()
    r=json.load(open(p))
    assert r['main_chain_alignment_status']=='PASS'
    assert r['skill_scope_alignment_status']=='PASS'
    assert r['no_useless_expansion_status']=='PASS'
    assert r['paper_only_boundary_status']=='PASS'
    assert r['remaining_gaps']==[]
