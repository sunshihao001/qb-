import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn/system/her_document_function_system/controllers/V00_validation_evidence_controller')
RUN_ROOT = Path('/root/sikk-gmgn/data/her_document_function_system/v00_runs')

EXPECTED_FILES = [
    '01_v00_manifest.yaml',
    '02_v00_context_pack.md',
    '03_v00_objective_tree.yaml',
    '04_v00_input_contract.json',
    '05_v00_output_contract.json',
    '06_v00_execution_protocol.md',
    '07_v00_acceptance_gate.yaml',
    '08_v00_state.json',
    '09_v00_handoff_packet.schema.json',
    '10_schema_validation.schema.json',
    '11_contract_validation.schema.json',
    '12_field_model_validation.schema.json',
    '13_rule_logic_test.schema.json',
    '14_function_mapping_validation.schema.json',
    '15_test_evidence.schema.json',
    '16_replay_evidence.schema.json',
    '17_failure_evidence.schema.json',
    '18_trace_audit_spec.yaml',
    '19_recovery_policy.md',
    '20_v00_final_report_template.md',
]


def test_v00_controller_has_exact_required_file_pack():
    assert ROOT.exists()
    assert RUN_ROOT.exists()
    actual = sorted(p.name for p in ROOT.iterdir() if p.is_file())
    assert actual == EXPECTED_FILES


def test_v00_json_assets_parse_and_expose_contract_gates():
    json_files = sorted(ROOT.glob('*.json'))
    assert json_files
    loaded = {p.name: json.loads(p.read_text()) for p in json_files}

    input_contract = loaded['04_v00_input_contract.json']
    assert 'f00_handoff_packet' in input_contract['required']
    assert input_contract['properties']['execution_boundary']['properties']['allow_live_runtime']['const'] is False
    assert input_contract['properties']['execution_boundary']['properties']['allow_wallet_signing']['const'] is False
    assert input_contract['properties']['execution_boundary']['properties']['allow_auto_deploy']['const'] is False

    test_schema = loaded['15_test_evidence.schema.json']
    for key in ['test_command', 'exit_code', 'stdout_path', 'stderr_path', 'passed_count', 'failed_count']:
        assert key in test_schema['required']

    replay_schema = loaded['16_replay_evidence.schema.json']
    for key in ['input_sample', 'output_sample', 'trace_path', 'status']:
        assert key in replay_schema['required']

    failure_schema = loaded['17_failure_evidence.schema.json']
    assert 'failure_reason' in failure_schema['required']
    assert 'gap_level' in failure_schema['required']


def test_v00_protocol_covers_all_subphases_and_false_pass_rules():
    protocol = (ROOT / '06_v00_execution_protocol.md').read_text()
    for idx in range(14):
        assert f'V00.{idx}' in protocol
    assert 'Test plan alone' in protocol
    assert 'Replay plan alone' in protocol
    assert 'live runtime' in protocol
    assert 'wallet signing' in protocol
    assert 'auto deploy' in protocol


def test_v00_acceptance_gate_distinguishes_planned_from_executed():
    gate = (ROOT / '07_v00_acceptance_gate.yaml').read_text()
    assert 'test_plan_only_is_TEST_PLANNED_not_TESTED' in gate
    assert 'replay_plan_only_is_REPLAY_PLANNED_not_REPLAY_TESTED' in gate
    assert 'missing_trace_or_audit_blocks_V00_ACCEPTED' in gate
    assert 'patch_without_modified_files_or_diff_is_not_PATCH_EVIDENCE_VALIDATED' in gate
