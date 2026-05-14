import json
import subprocess
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
CONTROLLER_DIR = REPO_ROOT / 'system/her_document_function_system/controllers/F00_function_realization_controller'
RUNNER = REPO_ROOT / 'tools/her_document_function_system/f00_safe_runner.py'
OUTPUT_DIR = CONTROLLER_DIR / 'outputs'


def run_safe_runner():
    return subprocess.run(
        [
            'python3',
            str(RUNNER),
            '--controller-dir',
            str(CONTROLLER_DIR),
            '--repo-root',
            str(REPO_ROOT),
            '--safe-mode',
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def test_f00_safe_runner_exits_zero_and_accepts():
    result = run_safe_runner()
    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)
    assert summary['status'] == 'F00_ACCEPTED'
    assert summary['final_status'] == 'FUNCTION_IMPLEMENTED_SAFE_MODE'


def test_f00_outputs_exist_and_are_not_placeholders():
    run_safe_runner()
    required = [
        'concept_to_function_map.json',
        'implementation_decision.json',
        'repo_scan_result.json',
        'function_asset_plan.json',
        'field_model.json',
        'rule_logic.json',
        'schema_contract_plan.json',
        'patch_plan.json',
        'test_replay_plan.json',
        'runner_binding_plan.json',
        'f00_acceptance_result.json',
        'f00_to_downstream_handoff_packet.json',
        'f00_final_report.md',
    ]
    for name in required:
        path = OUTPUT_DIR / name
        assert path.exists(), name
        assert path.stat().st_size > 20, name
    acceptance = json.loads((OUTPUT_DIR / 'f00_acceptance_result.json').read_text())
    handoff = json.loads((OUTPUT_DIR / 'f00_to_downstream_handoff_packet.json').read_text())
    assert acceptance['status'] == 'F00_ACCEPTED'
    assert handoff['status'] in {'FUNCTION_MAPPED', 'READY_WITH_GAPS'}


def test_f00_forbidden_runtime_scope_preserved():
    run_safe_runner()
    acceptance = json.loads((OUTPUT_DIR / 'f00_acceptance_result.json').read_text())
    forbidden = set(acceptance['forbidden_runtime_modes_preserved'])
    assert {'live_runtime', 'wallet_signing', 'auto_deploy'} <= forbidden
    runner_binding = json.loads((OUTPUT_DIR / 'runner_binding_plan.json').read_text())
    assert runner_binding['safe_mode'] is True
    assert 'wallet_signing' in runner_binding['forbidden_runtime_modes']


def test_f00_trace_and_audit_written():
    run_safe_runner()
    trace = OUTPUT_DIR / 'f00_trace.jsonl'
    audit = OUTPUT_DIR / 'f00_audit.jsonl'
    assert trace.exists() and trace.read_text().strip()
    assert audit.exists() and audit.read_text().strip()
    assert 'f00_safe_runner_executed' in trace.read_text()
    assert 'safe_scope_audit' in audit.read_text()
