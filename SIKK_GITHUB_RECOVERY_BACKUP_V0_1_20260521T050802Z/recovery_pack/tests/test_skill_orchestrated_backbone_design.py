import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/skill_orchestrated_backbone_design_latest.json'


def load_bundle():
    ptr = json.load(open(LATEST, encoding='utf-8'))
    acc = json.load(open(ROOT / ptr['canonical_path'], encoding='utf-8'))
    catalog = json.load(open(ROOT / ptr['capability_catalog_path'], encoding='utf-8'))
    policy = json.load(open(ROOT / ptr['policy_path'], encoding='utf-8'))
    return ptr, acc, catalog, policy


def test_skill_orchestrated_design_outputs_exist():
    assert LATEST.exists()
    ptr, acc, catalog, policy = load_bundle()
    for key in ['canonical_path', 'capability_catalog_path', 'policy_path', 'markdown_path']:
        assert (ROOT / ptr[key]).exists()
    assert acc['artifact_type'] == 'skill_orchestrated_backbone_design_acceptance_report'
    assert policy['protocol'] == 'SIKK_SKILL_ORCHESTRATED_OPERATING_BACKBONE_V0_1'
    assert len(catalog['capabilities']) >= 8


def test_capability_not_stage_oriented():
    _, acc, catalog, policy = load_bundle()
    ids = [x['capability_id'] for x in catalog['capabilities']]
    assert 'DATA_SOURCE_GMGN_READ_ONLY' in ids
    assert 'SOURCE_TO_CANONICAL_MAPPING' in ids
    assert 'FEATURE_ENGINEERING_FROM_CANONICAL' in ids
    assert 'STRUCTURE_SIGNAL' in ids
    assert not any(x in ids for x in ['S01_SKILL', 'S02_SKILL', 'S04_SKILL'])
    assert 'S01_skill/S02_skill/S04_skill mechanical stage split' in policy['wrong_decomposition_rejected']
    assert acc['conditions']['capability_oriented_not_stage_oriented'] is True


def test_every_capability_has_contracts_forbidden_and_downstream():
    _, acc, catalog, _ = load_bundle()
    for cap in catalog['capabilities']:
        assert cap['input_contract']
        assert cap['output_contract']
        assert cap['downstream_consumers']
        assert cap['forbidden_role']
        assert cap['backbone_position']
    assert acc['conditions']['skills_have_input_output_contracts'] is True
    assert acc['conditions']['skills_have_forbidden_roles'] is True
    assert acc['conditions']['skills_have_downstream_consumers'] is True


def test_orchestrator_keeps_control_and_next_skill_is_gmgn_data_source():
    _, acc, _, policy = load_bundle()
    assert 'check stage gate before next node' in policy['orchestrator_responsibilities']
    assert 'formal strategy_contract approval/mutation' in policy['must_remain_control_plane_or_contract']
    assert policy['first_skill_to_standardize'] == 'DATA_SOURCE_GMGN_READ_ONLY'
    assert policy['recommended_next_operational_run'] == 'GMGN_READ_ONLY_DATA_SOURCE_SKILL_STANDARDIZATION_RUN'
    assert acc['first_skill_to_standardize'] == 'DATA_SOURCE_GMGN_READ_ONLY'


def test_design_run_safety_boundaries():
    _, acc, _, _ = load_bundle()
    assert acc['acceptance_status'] == 'PASS'
    assert acc['promotion_allowed'] is False
    assert acc['canonical_write_performed'] is False
    assert acc['runtime_validation_executed'] is False
    assert acc['conditions']['strategy_contract_not_mutated'] is True
    assert acc['conditions']['canonical_not_promoted'] is True
    assert acc['conditions']['forbidden_runtime_scope_not_entered'] is True
    assert acc['conditions']['paper_position_not_created'] is True
