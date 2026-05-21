import json
from pathlib import Path

ROOT = Path('/root/sikk-quant-runner')


def test_skill_protocol_project_rules_embedding():
    text = (ROOT / 'PROJECT_RULES.md').read_text(encoding='utf-8')
    assert 'SIKK_SKILL_INVOCATION_PROTOCOL_V0_1' in text
    assert 'SIKK_SKILL_PROTOCOL_ENVELOPE_V0_1' in text
    assert 'A skill is not a standalone tool' in text
    assert 'downstream_consumer' in text
    assert 'FORBIDDEN' in text


def test_skill_invocation_envelope_professional_fields():
    text = (ROOT / 'docs/protocols/skill_invocation_envelope_template_v0_1.yaml').read_text(encoding='utf-8')
    for term in [
        'SKILL_INVOCATION_ENVELOPE',
        'actual_value_gate',
        'input_contract',
        'output_contract',
        'boundary_control',
        'acceptance_criteria',
        'strategy_contract bypass',
        'decision_ticket bypass',
    ]:
        assert term in text


def test_skill_cards_exist_and_cover_required_capabilities():
    text = (ROOT / 'docs/protocols/sikk_skill_cards_v0_1.yaml').read_text(encoding='utf-8')
    for skill_id in [
        'GMGN_READ_ONLY_DATA_ACQUISITION_SKILL',
        'RAW_FIELD_DISCOVERY_SKILL',
        'SOURCE_TO_CANONICAL_MAPPING_SKILL',
        'FEATURE_ENGINEERING_SKILL',
        'STRUCTURE_ENGINE_SKILL',
        'STRATEGY_CONTRACT_SKILL',
        'DECISION_GATE_SKILL',
        'PAPER_REPLAY_BACKTEST_VALIDATION_SKILL',
        'ATTRIBUTION_UPGRADE_CANDIDATE_SKILL',
        'GBRAIN_MEMORY_CONTEXT_SKILL',
    ]:
        assert skill_id in text
    for required in ['main_chain_position', 'downstream_consumers', 'forbidden_actions', 'acceptance_evidence', 'patch_required_if']:
        assert required in text


def test_skill_boundary_audit_latest_not_blocked():
    report = json.load(open(ROOT / 'data/latest/skill_boundary_audit_latest.json', encoding='utf-8'))
    assert report['acceptance_status'] in ['PASS', 'PATCH_REQUIRED']
    assert report['gmgn_boundary_check']['status'] in ['PASS', 'PATCH_REQUIRED']
    assert report['gmgn_boundary_check']['violations'] == []
    assert report['gbrain_openase_boundary_check']['status'] == 'PASS'
    assert report['skill_card_check']['status'] == 'PASS'
