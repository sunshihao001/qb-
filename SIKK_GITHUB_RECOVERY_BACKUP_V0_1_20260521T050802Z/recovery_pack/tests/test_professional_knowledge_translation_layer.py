import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/sikk_professional_knowledge_translation_layer_latest.json'
REQUIRED = [
    'cognition_update_summary',
    'professional_terms_registry',
    'task_translation_template',
    'hermes_professional_framing_template',
    'gbrain_usage_boundary',
    'openase_usage_boundary',
    'forbidden_scope_matrix',
    'acceptance_report',
]


def load_bundle():
    ptr = json.load(open(LATEST, encoding='utf-8'))
    artifacts = {}
    for key, path in ptr['artifact_paths'].items():
        if path.endswith('.json'):
            artifacts[key] = json.load(open(ROOT / path, encoding='utf-8'))
    return ptr, artifacts


def test_translation_layer_outputs_exist():
    assert LATEST.exists()
    ptr, artifacts = load_bundle()
    for key in REQUIRED:
        assert key in ptr['artifact_paths']
        assert (ROOT / ptr['artifact_paths'][key]).exists()
    assert (ROOT / ptr['artifact_paths']['markdown_doc']).exists()
    assert (ROOT / ptr['artifact_paths']['protocol_doc']).exists()
    assert artifacts['acceptance_report']['acceptance_status'] == 'PASS'


def test_professional_framing_has_required_10_fields():
    _, artifacts = load_bundle()
    required = artifacts['task_translation_template']['required_fields']
    framing = artifacts['hermes_professional_framing_template']['professional_framing']
    expected = [
        'professional_term',
        'stage_position',
        'real_purpose',
        'operating_capability',
        'upstream_input',
        'downstream_consumer',
        'data_objects',
        'decision_criteria',
        'action_boundary',
        'acceptance_evidence',
    ]
    assert required == expected
    assert sorted(framing.keys()) == sorted(expected)
    assert artifacts['hermes_professional_framing_template']['must_output_before_execution_for_sikk_tasks'] is True


def test_professional_terms_registry_covers_backbone_capabilities():
    _, artifacts = load_bundle()
    terms = artifacts['professional_terms_registry']['terms']
    capabilities = {t['operating_capability'] for t in terms}
    for cap in ['data_acquisition', 'mapping', 'feature_engineering', 'structure_signal', 'strategy_contract', 'decision_gate', 'validation_runner', 'attribution', 'memory_orchestration']:
        assert cap in capabilities
    assert any(t['professional_term'] == 'Decision Gate Run' for t in terms)
    assert any(t['professional_term'] == 'Source-to-Canonical Mapping Run' for t in terms)


def test_gbrain_and_openase_boundaries():
    _, artifacts = load_bundle()
    gbrain = artifacts['gbrain_usage_boundary']
    openase = artifacts['openase_usage_boundary']
    assert gbrain['positioning'] == 'Knowledge Memory Layer'
    assert 'Preflight Lookup for prior context, definitions, previous decisions, stable conventions' in gbrain['allowed_usage']
    assert 'decision_gate' in gbrain['forbidden_usage']
    assert 'PAPER_READY judgment' in gbrain['forbidden_usage']
    assert openase['positioning'] == 'Workflow Orchestration Layer'
    assert 'task ticket' in openase['allowed_usage']
    assert 'PAPER_READY judgment' in openase['forbidden_usage']
    assert 'decision_state裁决' in openase['forbidden_usage']


def test_forbidden_scope_matrix_blocks_runtime_bypass():
    _, artifacts = load_bundle()
    matrix = artifacts['forbidden_scope_matrix']['rows']
    by_scope = {row['scope']: row for row in matrix}
    for scope in [
        'direct colloquial execution',
        'skill as loose tool',
        'GBrain runtime judgment',
        'OpenASE runtime judgment',
        'GMGN swap/cooking/signing/broadcast',
        'strategy_contract bypass',
        'decision_ticket bypass',
        'auto live rule modification',
        'live trading path',
    ]:
        assert by_scope[scope]['status'] == 'FORBIDDEN'
    assert by_scope['no-downstream data generation']['status'] == 'NOT_NOW'


def test_acceptance_safety_boundaries():
    _, artifacts = load_bundle()
    acc = artifacts['acceptance_report']
    conditions = acc['conditions']
    assert acc['promotion_allowed'] is False
    assert acc['canonical_write_performed'] is False
    assert acc['runtime_validation_executed'] is False
    assert acc['gmgn_called'] is False
    assert acc['strategy_contract_modified'] is False
    for value in conditions.values():
        assert value is True
