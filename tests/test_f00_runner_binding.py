import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
CONTROLLER_DIR = REPO_ROOT / 'system/her_document_function_system/controllers/F00_function_realization_controller'
REPLAY_FIXTURE = REPO_ROOT / 'tests/fixtures/her_document_function_system/f00_e2e_replay_fixture.json'


def run_module_cli(output_dir: Path):
    return subprocess.run(
        [
            sys.executable,
            '-m',
            'modules.her_document_function_system.f00_runner',
            '--controller-dir',
            str(CONTROLLER_DIR),
            '--repo-root',
            str(REPO_ROOT),
            '--replay-fixture',
            str(REPLAY_FIXTURE),
            '--output-dir',
            str(output_dir),
            '--safe-mode',
            '--upgrade-acceptance',
        ],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_f00_runner_module_exports_public_api():
    from modules.her_document_function_system import f00_runner

    assert 'run_f00_pipeline' in f00_runner.__all__
    assert 'main' in f00_runner.__all__
    assert callable(f00_runner.run_f00_pipeline)


def test_f00_module_cli_runs_schema_contract_validation_e2e_replay_and_binding(tmp_path):
    output_dir = tmp_path / 'f00_outputs'

    result = run_module_cli(output_dir)

    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)
    assert summary['status'] == 'ACCEPTANCE_PASSED'
    assert summary['schema_validation_status'] == 'PASSED'
    assert summary['contract_validation_status'] == 'PASSED'
    assert summary['replay_status'] == 'REPLAY_TESTED'
    assert summary['runner_binding_status'] == 'BINDING_TESTED'
    assert summary['output_dir'] == str(output_dir)

    required_outputs = [
        'concept_to_function_map.json',
        'implementation_decision.json',
        'repo_scan_result.json',
        'function_asset_plan.json',
        'field_model.json',
        'rule_logic.json',
        'schema_contract_plan.json',
        'patch_plan.json',
        'test_replay_evidence.json',
        'runner_binding_evidence.json',
        'replay_output.json',
        'replay_trace.jsonl',
        'replay_report.md',
        'replay_acceptance.json',
        'f00_acceptance_result.json',
        'f00_to_downstream_handoff_packet.json',
        'f00_final_report.md',
    ]
    for name in required_outputs:
        path = output_dir / name
        assert path.exists(), name
        assert path.stat().st_size > 20, name

    acceptance = json.loads((output_dir / 'f00_acceptance_result.json').read_text())
    assert acceptance['status'] == 'ACCEPTANCE_PASSED'
    assert acceptance['previous_status'] in {'READY_WITH_GAPS', 'F00_ACCEPTED', 'ACCEPTANCE_READY_WITH_GAPS'}
    assert acceptance['schema_validation_status'] == 'PASSED'
    assert acceptance['contract_validation_status'] == 'PASSED'
    assert acceptance['test_status'] == 'TESTED'
    assert acceptance['replay_status'] == 'REPLAY_TESTED'
    assert acceptance['runner_binding_status'] == 'BINDING_TESTED'
    assert acceptance['errors'] == []

    replay_acceptance = json.loads((output_dir / 'replay_acceptance.json').read_text())
    assert replay_acceptance['status'] == 'REPLAY_TESTED'
    assert replay_acceptance['input_fixture'] == str(REPLAY_FIXTURE)

    binding = json.loads((output_dir / 'runner_binding_evidence.json').read_text())
    assert binding['status'] == 'BINDING_TESTED'
    assert binding['binding_type'] == 'MODULE_CLI'
    assert 'python' in binding['validated_command'][0]

    handoff = json.loads((output_dir / 'f00_to_downstream_handoff_packet.json').read_text())
    assert handoff['status'] == 'HANDOFF_READY'
    assert str(output_dir / 'replay_acceptance.json') in handoff['replay_refs']
    assert str(output_dir / 'runner_binding_evidence.json') in handoff['runner_binding_refs']


def test_f00_runner_refuses_non_safe_mode(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'modules.her_document_function_system.f00_runner',
            '--controller-dir',
            str(CONTROLLER_DIR),
            '--repo-root',
            str(REPO_ROOT),
            '--replay-fixture',
            str(REPLAY_FIXTURE),
            '--output-dir',
            str(tmp_path / 'out'),
        ],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload['status'] == 'ACCEPTANCE_BLOCKED'
    assert any('SAFE_MODE_REQUIRED' in item for item in payload['errors'])
