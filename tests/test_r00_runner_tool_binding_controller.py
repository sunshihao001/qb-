import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn/system/her_document_function_system/controllers/R00_runner_tool_binding_controller')
RUN_ROOT = Path('/root/sikk-gmgn/data/her_document_function_system/r00_runs')

EXPECTED_FILES = ['01_r00_manifest.yaml', '02_r00_context_pack.md', '03_r00_objective_tree.yaml', '04_r00_input_contract.json', '05_r00_output_contract.json', '06_r00_execution_protocol.md', '07_r00_acceptance_gate.yaml', '08_r00_state.json', '09_r00_handoff_packet.schema.json', '10_binding_target_inventory.schema.json', '11_command_contract.schema.json', '12_cli_binding.schema.json', '13_orchestrator_binding.schema.json', '14_tool_binding.schema.json', '15_telegram_binding.schema.json', '16_report_binding.schema.json', '17_dashboard_binding.schema.json', '18_scheduler_binding.schema.json', '19_dry_run_evidence.schema.json', '20_binding_failure_evidence.schema.json', '21_trace_audit_spec.yaml', '22_recovery_policy.md', '23_r00_final_report_template.md']

def test_r00_controller_has_exact_required_file_pack():
    assert ROOT.exists()
    assert RUN_ROOT.exists()
    actual = sorted(p.name for p in ROOT.iterdir() if p.is_file())
    assert actual == sorted(EXPECTED_FILES)

def test_r00_json_assets_parse_and_expose_contract_gates():
    loaded = {p.name: json.loads(p.read_text()) for p in sorted(ROOT.glob('*.json'))}
    input_contract = loaded['04_r00_input_contract.json']
    assert 'v00_handoff_packet' in input_contract['required']
    assert 'validation_evidence' in input_contract['required']
    assert input_contract['properties']['safe_mode']['const'] is True
    boundary = input_contract['properties']['execution_boundary']['properties']
    assert boundary['allow_live_runtime']['const'] is False
    assert boundary['allow_wallet_signing']['const'] is False
    assert boundary['allow_auto_deploy']['const'] is False
    assert boundary['allow_production_trading']['const'] is False

    command_schema = loaded['11_command_contract.schema.json']
    for key in ['command_id', 'command_name', 'command_template', 'required_args', 'input_paths', 'output_paths', 'expected_outputs', 'success_criteria', 'failure_policy']:
        assert key in command_schema['required']

    dry_run_schema = loaded['19_dry_run_evidence.schema.json']
    for key in ['command', 'exit_code', 'stdout_path', 'stderr_path', 'generated_outputs', 'missing_outputs']:
        assert key in dry_run_schema['required']

def test_r00_protocol_covers_all_subphases_and_false_pass_rules():
    protocol = (ROOT / '06_r00_execution_protocol.md').read_text()
    for idx in range(16):
        assert f'R00.{idx}' in protocol
    assert 'Binding plan alone' in protocol
    assert 'No dry-run exit_code' in protocol
    assert 'No stdout/stderr' in protocol
    assert 'Telegram binding design is not Telegram' in protocol
    assert 'Scheduler binding design is not scheduler enabled' in protocol
    assert 'live runtime' in protocol
    assert 'wallet signing' in protocol
    assert 'production trading' in protocol

def test_r00_acceptance_gate_distinguishes_designed_from_bound():
    gate = (ROOT / '07_r00_acceptance_gate.yaml').read_text()
    assert 'binding_plan_only_is_BINDING_DESIGNED_not_RUNNER_BOUND' in gate
    assert 'missing_exit_code_is_not_BINDING_TESTED' in gate
    assert 'missing_stdout_or_stderr_is_not_BINDING_TESTED' in gate
    assert 'missing_generated_outputs_manifest_blocks_R00_ACCEPTED' in gate
    assert 'telegram_design_is_not_telegram_enabled' in gate
    assert 'scheduler_design_is_not_scheduler_enabled' in gate
