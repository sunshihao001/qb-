import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GAP=ROOT/'data/gmgn_read_only/latest/gap_repair'

def load(name): return json.loads((GAP/name).read_text(encoding='utf-8'))

def test_inventory_and_mapping_report_exist():
    inv=load('response_field_inventory.json')
    rep=load('feature_mapping_repair_report.json')
    assert inv['response_files']
    assert set(['price_change_5m','price_change_1h','volume_5m','volume_1h','liquidity_usd','volatility_window','trend_state_preliminary','smart_holder_count','profitable_trader_count','wallet_profile_tags']).issubset(inv['focus_field_presence'])
    assert rep['fabricated_fields'] is False
    assert rep['default_values_used'] is False

def test_feature_fields_have_source_or_missing_reason():
    fs=load('feature_snapshot_after_mapping_repair.json')
    for section in ['market_features','kline_features','wallet_features']:
        for k,v in fs[section].items():
            if isinstance(v,dict) and 'value' in v:
                assert v.get('source_path') or v.get('missing_reason')
                assert not (v.get('value') in (0,'') and not v.get('source_path'))

def test_structure_and_decision_consume_repaired_artifacts():
    ss=load('structure_signal_after_mapping_repair.json')
    dt=load('decision_ticket_after_mapping_repair.json')
    assert ss['input_feature_snapshot']=='data/gmgn_read_only/latest/gap_repair/feature_snapshot_after_mapping_repair.json'
    assert dt['input_structure_signal']=='data/gmgn_read_only/latest/gap_repair/structure_signal_after_mapping_repair.json'
    assert dt['decision_state'] in {'EXCLUDE','WATCH','RISK_MONITOR','PAPER_READY_CANDIDATE','PATCH_REQUIRED'}

def test_security_missing_blocks_and_forbidden_scope():
    ss=load('structure_signal_after_mapping_repair.json')
    dt=load('decision_ticket_after_mapping_repair.json')
    acc=load('gap_repair_acceptance_report.json')
    if ss['security_structure']['signal']=='MISSING':
        assert dt['decision_state']!='PAPER_READY_CANDIDATE'
        assert dt['security_missing_blocks_paper_candidate'] is True
    assert dt['unknown_missing_treated_as_support'] is False
    for v in acc['forbidden_scope_check'].values(): assert v is False
