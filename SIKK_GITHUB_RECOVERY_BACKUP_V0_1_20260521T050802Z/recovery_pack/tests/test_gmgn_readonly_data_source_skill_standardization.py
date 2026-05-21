import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/gmgn_readonly_data_source_skill_standardization_latest.json'
REQUIRED = [
    'professional_framing',
    'operating_intent',
    'run_context',
    'skill_to_backbone_binding',
    'lineage_inventory',
    'forbidden_scope_check',
    'gmgn_readonly_skill_standard',
    'acceptance_report',
]


def load_bundle():
    ptr = json.load(open(LATEST, encoding='utf-8'))
    artifacts = {}
    for key, path in ptr['artifact_paths'].items():
        if path.endswith('.json'):
            artifacts[key] = json.load(open(ROOT / path, encoding='utf-8'))
    return ptr, artifacts


def test_gmgn_standardization_outputs_exist():
    assert LATEST.exists()
    ptr, artifacts = load_bundle()
    for key in REQUIRED:
        assert key in ptr['artifact_paths']
        assert (ROOT / ptr['artifact_paths'][key]).exists()
    assert ptr['acceptance_status'] in ['PASS', 'PASS_WITH_GAPS']
    assert artifacts['acceptance_report']['artifact_type'] == 'gmgn_readonly_data_source_skill_standardization_acceptance_report'


def test_sequence_and_professional_framing():
    _, artifacts = load_bundle()
    pf = artifacts['professional_framing']
    assert pf['professional_term'] == 'GMGN Read-only Data Source Skill Standardization Run'
    assert pf['stage_position'] == 'raw_evidence / data_source_skill_standardization'
    assert pf['operating_capability'] == 'data_acquisition'
    for key in ['professional_term', 'stage_position', 'real_purpose', 'operating_capability', 'upstream_input', 'downstream_consumer', 'data_objects', 'decision_criteria', 'action_boundary', 'acceptance_evidence']:
        assert key in pf


def test_operating_intent_and_run_context():
    _, artifacts = load_bundle()
    intent = artifacts['operating_intent']
    context = artifacts['run_context']
    assert intent['intent_name'] == 'GMGN_READ_ONLY_DATA_SOURCE_SKILL_STANDARDIZATION_RUN'
    assert intent['expected_backbone_node'] == 'raw_evidence'
    assert context['target_skill'] == 'gmgn_readonly_data_source'
    assert context['acquisition_mode'] in ['existing_evidence_standardization_only_no_new_call', 'fresh_gmgn_read_only_calls_standardized']
    assert context['canonical_write_allowed'] is False
    assert context['promotion_allowed'] is False
    assert context['runtime_validation_allowed'] is False


def test_skill_to_backbone_binding_contracts_and_downstream():
    _, artifacts = load_bundle()
    binding = artifacts['skill_to_backbone_binding']
    assert binding['backbone_position'] == 'raw_evidence'
    assert 'source_to_canonical_mapper' in binding['downstream_consumer']
    assert 'request_path' in binding['output_contract']
    assert 'response_path' in binding['output_contract']
    assert 'error_path' in binding['output_contract']
    assert 'RawSnapshot' in binding['canonical_objects_produced']
    assert 'decision_ticket' in binding['forbidden_role']


def test_lineage_inventory_and_skill_standard():
    _, artifacts = load_bundle()
    inv = artifacts['lineage_inventory']
    std = artifacts['gmgn_readonly_skill_standard']
    assert inv['skill_mapping_exists'] is True
    assert inv['raw_snapshot_manifest_exists'] is True
    assert inv['invocation_evidence_dir_exists'] is True
    assert inv['records_count'] > 0
    assert std['skill_yaml']['skill_name'] == 'gmgn_readonly_data_source'
    assert std['skill_yaml']['backbone_node'] == 'raw_evidence'
    assert 'source_to_canonical_mapper' in std['skill_yaml']['downstream_consumer']
    assert std['runtime_data_rule'] == 'All runtime artifacts must be written to data/operating_backbone/runs/<run_id>/, not to the skill directory.'


def test_forbidden_scope_and_acceptance_safety():
    _, artifacts = load_bundle()
    boundary = artifacts['forbidden_scope_check']
    acc = artifacts['acceptance_report']
    assert boundary['status'] == 'PASS'
    assert boundary['violations'] == []
    assert acc['gmgn_called'] in [False, True]
    assert acc['canonical_write_performed'] is False
    assert acc['runtime_validation_executed'] is False
    assert acc['conditions']['feature_not_computed'] is True
    assert acc['conditions']['structure_signal_not_generated'] is True
    assert acc['conditions']['decision_ticket_not_generated'] is True
    assert acc['conditions']['paper_replay_backtest_not_entered'] is True


def test_next_operational_run_is_mapping_or_repair():
    ptr, artifacts = load_bundle()
    assert ptr['next_operational_run'] in ['SOURCE_TO_CANONICAL_MAPPING_SKILL_RUN', 'GMGN_READ_ONLY_LINEAGE_REPAIR_RUN']
    assert artifacts['acceptance_report']['next_operational_run'] == ptr['next_operational_run']
