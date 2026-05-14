import json, subprocess, sys
from pathlib import Path
REPO=Path('/root/sikk-gmgn')
TOOLS=REPO/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))

def test_candidate_classification_required_fields():
    from g00_governance_candidate_classifier import classify_candidates
    res=classify_candidates([{'upgrade_candidate_id':'uc1','problem_statement':'policy candidate not active','evidence_refs':['x']}])
    c=res['classified_candidates'][0]
    assert c['candidate_id']=='uc1' and c['policy_domain']=='evidence_policy' and c['classification_status']=='CLASSIFIED'
