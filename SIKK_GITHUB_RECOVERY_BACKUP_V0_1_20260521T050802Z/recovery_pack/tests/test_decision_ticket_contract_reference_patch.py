import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/decision_ticket_contract_reference_patch_latest.json'


def load_latest_bundle():
    ptr = json.load(open(LATEST, encoding='utf-8'))
    acc = json.load(open(ROOT / ptr['canonical_path'], encoding='utf-8'))
    gate = json.load(open(ROOT / ptr['validation_readiness_gate_path'], encoding='utf-8'))
    sidecar = json.load(open(ROOT / ptr['legacy_sidecar_path'], encoding='utf-8'))
    policy = json.load(open(ROOT / ptr['policy_path'], encoding='utf-8'))
    return ptr, acc, gate, sidecar, policy


def test_decision_ticket_contract_reference_patch_outputs_exist():
    assert LATEST.exists()
    ptr, acc, gate, sidecar, policy = load_latest_bundle()
    for key in ['canonical_path', 'validation_readiness_gate_path', 'legacy_sidecar_path', 'policy_path']:
        assert (ROOT / ptr[key]).exists()
    assert acc['artifact_type'] == 'decision_ticket_contract_reference_patch_acceptance_report'
    assert gate['protocol'] == 'SIKK_VALIDATION_READINESS_GATE_V0_1'
    assert policy['protocol'] == 'SIKK_DECISION_TICKET_CONTRACT_REFERENCE_POLICY_V0_1'


def test_legacy_decision_tickets_marked_without_mutation():
    _, acc, _, sidecar, _ = load_latest_bundle()
    assert sidecar['policy'] == 'Do not mutate old artifacts; mark externally as legacy/not_validation_ready.'
    existing = [x for x in sidecar['legacy_artifacts'] if x['exists']]
    assert existing
    for item in existing:
        assert item['legacy_status'] == 'LEGACY_NOT_VALIDATION_READY'
        assert item['validation_readiness'] == 'NOT_VALIDATION_READY'
        assert item['original_content_modified'] is False
    for item in acc['legacy_hashes_unchanged']:
        if item['exists']:
            assert item['sha256_before'] == item['sha256_after']
            assert item['unchanged'] is True


def test_new_policy_requires_canonical_strategy_contract():
    _, _, _, _, policy = load_latest_bundle()
    assert policy['required_canonical_value'] == 'contracts/strategy_contract.json'
    assert policy['canonical_strategy_contract']['contract_exists'] is True
    assert 'validation readiness without strategy_contract reference' in policy['forbidden']
    assert 'strategy_contract auto-mutation' in policy['forbidden']


def test_validation_readiness_rejects_missing_contract_reference():
    _, acc, gate, _, _ = load_latest_bundle()
    assert gate['rule'] == 'Reject any decision_ticket without canonical strategy_contract reference.'
    not_ready = [r for r in gate['results_sample'] if r['validation_readiness'] == 'NOT_READY']
    assert not_ready
    for result in not_ready:
        assert result['blocked_modes'] == ['paper', 'replay', 'backtest']
    assert acc['runtime_validation_allowed'] == (gate['acceptance_status'] == 'PASS')
    if gate['acceptance_status'] != 'PASS':
        assert acc['blocked_modes'] == ['paper', 'replay', 'backtest']


def test_no_canonical_promotion_or_runtime_execution():
    _, acc, _, _, _ = load_latest_bundle()
    assert acc['promotion_allowed'] is False
    assert acc['canonical_write_performed'] is False
    assert acc['pass_conditions']['no_strategy_contract_mutation'] is True
    assert acc['pass_conditions']['no_paper_replay_backtest_execution'] is True
    assert acc['pass_conditions']['no_live_swap_sign_broadcast'] is True
