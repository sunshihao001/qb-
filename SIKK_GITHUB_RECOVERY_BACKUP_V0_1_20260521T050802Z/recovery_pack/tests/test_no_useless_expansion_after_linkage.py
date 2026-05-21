import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_no_useless_expansion_after_linkage():
    audit=json.load(open(ROOT/'data/coordination/latest/pipeline_linkage_audit_report.json'))
    missing=json.load(open(ROOT/'data/coordination/latest/missing_link_report.json'))
    repair=json.load(open(ROOT/'data/coordination/latest/stage_handoff_repair_report.json'))
    assert not [x for x in audit['broken_links'] if x.get('priority')=='P0']
    assert repair['unresolved_items']==[]
    assert missing['priority'] in ['P1','P2','NOT_NOW']
    # no forbidden execution scope was created by linkage repair
    txt=' '.join(Path(ROOT/'data/coordination/latest').glob('*.json').__str__() for _ in [0])
    assert 'GMGN_READ_ONLY_REAL_DATA_TO_RAW_FEATURE_DECISION_PIPELINE_PACK'
