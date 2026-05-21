import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_main_chain_alignment_report_pass():
    r=json.load(open(ROOT/'data/coordination/latest/main_chain_alignment_report.json'))
    assert r['real_data_to_raw_ready'] is True
    assert r['raw_to_feature_ready'] is True
    assert r['feature_to_strategy_contract_ready'] is True
    assert r['strategy_contract_to_decision_ticket_ready'] is True
    assert r['openase_boundary_status']=='PASS'
    assert r['gbrain_boundary_status']=='PASS'
    assert r['gmgn_read_only_status']=='PASS'
    assert r['no_useless_expansion_status']=='PASS'
    assert r['main_chain_alignment_status']=='PASS'
    assert r['next_recommended_stage']=='GMGN_READ_ONLY_REAL_DATA_TO_RAW_FEATURE_DECISION_PIPELINE_PACK'
