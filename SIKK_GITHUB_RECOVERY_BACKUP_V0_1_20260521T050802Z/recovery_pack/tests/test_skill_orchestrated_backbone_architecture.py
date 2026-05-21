import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/skill_orchestrated_backbone_architecture_latest.json'
REQUIRED = [
    'recommended_skill_architecture',
    'skill_directory_plan',
    'orchestration_flow',
    'canonical_data_flow',
    'stage_gate_rules',
    'promotion_gate_rules',
    'first_batch_skills_to_build',
    'acceptance_report',
]


def load_bundle():
    ptr = json.load(open(LATEST, encoding='utf-8'))
    artifacts = {}
    for key, path in ptr['artifact_paths'].items():
        if path.endswith('.json'):
            artifacts[key] = json.load(open(ROOT / path, encoding='utf-8'))
    return ptr, artifacts


def test_architecture_outputs_exist():
    assert LATEST.exists()
    ptr, artifacts = load_bundle()
    for key in REQUIRED:
        assert key in ptr['artifact_paths']
        assert (ROOT / ptr['artifact_paths'][key]).exists()
    assert (ROOT / ptr['artifact_paths']['markdown_doc']).exists()
    assert (ROOT / ptr['artifact_paths']['architecture_doc']).exists()
    assert artifacts['acceptance_report']['acceptance_status'] == 'PASS'


def test_recommended_architecture_has_nodes_and_metadata_policy():
    _, artifacts = load_bundle()
    arch = artifacts['recommended_skill_architecture']
    nodes = arch['backbone_nodes']
    for node in ['raw_evidence', 'source_to_canonical_mapping', 'feature_engineering', 'structure_engine', 'strategy_contract', 'decision_ticket', 'validation_lifecycle', 'failure_attribution', 'upgrade_candidate', 'promotion_gate']:
        assert node in nodes
    assert arch['s_r_n_policy']['status'] == 'metadata_only'
    assert 'Do not split S/R/N into separate systems' in arch['s_r_n_policy']['rule']


def test_each_skill_has_required_protocol_fields():
    _, artifacts = load_bundle()
    components = artifacts['recommended_skill_architecture']['components']
    assert len(components) >= 10
    for comp in components:
        for key in ['skill_name', 'professional_term', 'backbone_node', 'input_contract', 'output_contract', 'consumes_canonical_objects', 'produces_canonical_objects', 'forbidden_scope', 'pass_criteria', 'patch_required_criteria', 'blocked_criteria', 'downstream_consumer']:
            assert key in comp
        assert comp['input_contract']
        assert comp['output_contract']
        assert comp['forbidden_scope']
        assert comp['downstream_consumer']


def test_skill_directory_plan_keeps_business_data_out_of_skill_dirs():
    _, artifacts = load_bundle()
    plan = artifacts['skill_directory_plan']
    assert plan['directories']
    for item in plan['directories']:
        assert item['business_data_allowed_here'] is False
        assert item['runtime_data_path'] == 'data/operating_backbone/runs/<run_id>/'
        assert item['canonical_data_path'] == 'data/operating_backbone/canonical/'
        for field in ['skill_name', 'professional_term', 'backbone_node', 'input_contract', 'output_contract', 'forbidden_scope', 'stage_gate', 'acceptance_criteria', 'downstream_consumer']:
            assert field in item['skill_yaml_required_fields']


def test_stage_and_promotion_gates_block_forbidden_paths():
    _, artifacts = load_bundle()
    stage = artifacts['stage_gate_rules']
    promo = artifacts['promotion_gate_rules']
    assert 'BUY' in stage['forbidden_decision_states']
    assert 'SWAP_READY' in stage['forbidden_decision_states']
    assert any(r['gate'] == 'decision_to_validation' and 'PAPER_READY_CANDIDATE' in r['pass_if'] for r in stage['rules'])
    assert promo['hard_requirement'] == 'Only acceptance_status == PASS and promotion_allowed == true may write to canonical.'
    assert any(r['acceptance_status'] == 'BLOCKED' and r['promotion_policy'] == 'quarantine' for r in promo['rules'])


def test_first_batch_and_next_operational_run():
    ptr, artifacts = load_bundle()
    first = artifacts['first_batch_skills_to_build']['first_batch']
    names = [x['skill_name'] for x in first]
    assert names[:3] == ['gmgn_readonly_data_source', 'source_to_canonical_mapper', 'feature_engineering']
    assert first[0]['operational_run'] == 'GMGN_READ_ONLY_DATA_SOURCE_SKILL_STANDARDIZATION_RUN'
    assert ptr['next_operational_run'] == 'GMGN_READ_ONLY_DATA_SOURCE_SKILL_STANDARDIZATION_RUN'


def test_acceptance_safety():
    _, artifacts = load_bundle()
    acc = artifacts['acceptance_report']
    assert acc['promotion_allowed'] is False
    assert acc['canonical_write_performed'] is False
    assert acc['runtime_validation_executed'] is False
    assert acc['gmgn_called'] is False
    assert acc['strategy_contract_modified'] is False
    for value in acc['conditions'].values():
        assert value is True
