import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/gmgn_read_only/latest/structure_engine'

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def test_contract_schema_and_canonical_have_structure_gate():
    schema=load(ROOT/'contracts/strategy_contract_v0_1_schema.json')
    contract=load(ROOT/'contracts/strategy_contract.json')
    assert 'structure_gate' in schema['required']
    assert 'decision_mapping' in schema['required']
    assert contract['structure_gate']['enabled'] is True
    assert contract['structure_gate']['paper_candidate_requirements']['unknown_or_missing_counts_as_support'] is False
    assert contract['structure_gate']['security_missing_policy']['blocks_paper_candidate'] is True
    assert contract['live_trading_enabled'] is False
    assert contract['swap_allowed'] is False

def test_decision_ticket_references_signal_and_contract():
    ticket=load(BASE/'decision_ticket_after_contract_alignment.json')
    assert ticket['input_structure_signal']=='data/gmgn_read_only/latest/structure_engine/structure_signal.json'
    assert ticket['input_strategy_contract']=='contracts/strategy_contract.json'
    assert ticket['strategy_contract_hash']
    assert ticket['structure_gate_used'] is True
    assert ticket['decision_mapping_used'] is True

def test_security_missing_and_unknown_missing_do_not_support_paper():
    sig=load(BASE/'structure_signal.json')
    ticket=load(BASE/'decision_ticket_after_contract_alignment.json')
    assert ticket['unknown_missing_treated_as_support'] is False
    if sig['security_structure']['signal']=='MISSING':
        assert ticket['decision_state']!='PAPER_READY_CANDIDATE'
        assert ticket['security_missing_blocks_paper_candidate'] is True
        assert ticket['paper_candidate_allowed'] is False

def test_decision_state_allowed_and_forbidden_scope():
    report=load(BASE/'structure_contract_alignment_report.json')
    assert report['acceptance_status']=='PASS'
    assert report['decision_state'] in {'EXCLUDE','WATCH','RISK_MONITOR','PAPER_READY_CANDIDATE','PATCH_REQUIRED'}
    assert report['paper_position_created'] is False
    for v in report['forbidden_scope_check'].values():
        assert v is False

def test_trace_exists_and_records_contract_gate():
    trace=load(BASE/'decision_ticket_contract_trace.json')
    assert trace['structure_gate_enabled'] is True
    assert trace['allowed_decision_state'] is True
    assert trace['rule_trace']
