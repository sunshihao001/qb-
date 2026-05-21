import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/sikk_skill_protocol_bootstrap_latest.json'


def test_skill_protocol_bootstrap_outputs_exist():
    assert LATEST.exists()
    report = json.load(open(LATEST, encoding='utf-8'))
    assert report['skill_protocol_summary']['protocol'] == 'SIKK_SKILL_INVOCATION_PROTOCOL_V0_1'
    for key in [
        'skill_inventory_table',
        'skill_to_backbone_binding',
        'skill_boundary_matrix',
        'forbidden_scope_matrix',
        'hermes_active_cognition_update',
        'acceptance_report',
    ]:
        assert key in report


def test_each_skill_has_binding_contract_and_boundary():
    report = json.load(open(LATEST, encoding='utf-8'))
    required = [
        'skill_name',
        'capability_type',
        'main_chain_position',
        'upstream_input',
        'downstream_consumer',
        'allowed_role',
        'forbidden_role',
        'input_contract',
        'output_contract',
        'acceptance_evidence',
        'forbidden_scope',
        'handoff_target',
    ]
    for skill in report['skill_inventory_table']:
        for field in required:
            assert field in skill
            assert skill[field] not in [None, '', [], {}]
        assert skill['runtime_decision_permission'] is False


def test_support_layers_are_reference_only_or_patch_not_runtime():
    report = json.load(open(LATEST, encoding='utf-8'))
    for skill in report['skill_inventory_table']:
        if skill['provider'] in ['gbrain', 'openase']:
            assert skill['main_chain_position'] == 'support_layer'
            assert skill['runtime_decision_permission'] is False
            assert 'feature_builder' in skill['forbidden_role']
            assert 'decision_gate' in skill['forbidden_role']


def test_gmgn_first_version_read_only_boundary():
    report = json.load(open(LATEST, encoding='utf-8'))
    gmgn = [s for s in report['skill_inventory_table'] if s['provider'] == 'gmgn']
    assert gmgn
    for skill in gmgn:
        assert skill['capability_type'] == 'data_acquisition'
        assert skill['main_chain_position'] == 'raw_evidence'
        assert skill['runtime_decision_permission'] is False
        assert 'route/quote/swap/sign/broadcast/cook' in skill['forbidden_role']
        assert skill['disposition'] in ['EXECUTABLE', 'PATCH_REQUIRED', 'NOT_NOW']
        assert skill['disposition'] != 'FORBIDDEN'


def test_acceptance_status_not_blocked_and_expected_patch_required():
    report = json.load(open(LATEST, encoding='utf-8'))
    acc = report['acceptance_report']
    assert acc['acceptance_status'] in ['PASS', 'PATCH_REQUIRED']
    assert acc['forbidden_skills'] == []
    assert 'gmgn_security_read' in acc['patch_required_skills']
    assert acc['promotion_allowed'] is False
    assert acc['canonical_write_performed'] is False
