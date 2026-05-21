from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = (ROOT / 'data/latest/s01_fresh_run_id.txt').read_text().strip()
BASE = ROOT / 'data/runs' / RUN_ID / 'structure'


def load(name):
    return json.loads((BASE / name).read_text())


def test_s04_structure_artifacts_exist():
    for name in [
        'structure_signal_from_feature_snapshot.json',
        's04_structure_signal_report.json',
        's04_structure_signal_gate.json',
    ]:
        assert (BASE / name).exists(), name


def test_structure_consumes_feature_snapshot_and_lineage_only():
    sig = load('structure_signal_from_feature_snapshot.json')
    assert sig['input_feature_snapshot'].endswith('feature_snapshot_from_canonical_mapping.json')
    assert sig['input_feature_lineage'].endswith('feature_lineage_from_canonical_mapping.json')
    assert sig['input_source_to_canonical_mapping_read'] is False
    assert sig['gmgn_raw_response_read'] is False
    assert sig['stage_metadata']['s_stage'] == 'S04'
    assert sig['stage_metadata']['r_stage'] == ['R05']
    assert sig['stage_metadata']['sr_physical_split_allowed'] is False


def test_missing_reasons_and_security_block_are_preserved():
    sig = load('structure_signal_from_feature_snapshot.json')
    assert sig['counter_evidence']['missing_required_data']
    assert sig['security_structure']['signal'] == 'MISSING'
    assert sig['security_structure']['paper_candidate_block_reason']
    assert sig['paper_candidate_allowed_by_structure'] is False


def test_structure_does_not_emit_decision_or_forbidden_scope():
    sig = load('structure_signal_from_feature_snapshot.json')
    text = json.dumps(sig, ensure_ascii=False)
    for forbidden in ['BUY', 'SELL', 'EXECUTE', 'LIVE_READY', 'SWAP_READY']:
        assert forbidden not in text
    assert sig['decision_state_emitted'] is False
    assert sig['forbidden_decision_terms_emitted'] == []
    assert sig['no_buy_sell_execute'] is True
    assert sig['no_paper_position_created'] is True


def test_s04_gate_blocks_paper_and_routes_to_decision_gate():
    gate = load('s04_structure_signal_gate.json')
    assert gate['feature_snapshot_only'] is True
    assert gate['source_to_canonical_mapping_read'] is False
    assert gate['gmgn_raw_response_read'] is False
    assert gate['security_missing_blocks_paper_candidate'] is True
    assert gate['decision_ticket_created'] is False
    assert gate['paper_readiness_allowed'] is False
    assert gate['paper_runner_allowed'] is False
    assert gate['buy_sell_execute_emitted'] is False
    assert gate['allowed_next_stage'] == 'S05_DECISION_GATE_FROM_CONTRACT_AND_STRUCTURE_RUN'
