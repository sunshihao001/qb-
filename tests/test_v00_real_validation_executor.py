import json
import subprocess
from pathlib import Path

REPO = Path('/root/sikk-gmgn')
VALIDATION_ROOT = REPO / 'system/her_document_function_system/validation/v00_real_validation'


def test_v00_real_validation_system_files_exist():
    required = [
        '01_v00_real_validation_manifest.yaml',
        '02_v00_real_validation_context_pack.md',
        '03_v00_real_validation_input_contract.json',
        '04_v00_real_validation_output_contract.json',
        '05_v00_real_validation_execution_protocol.md',
        '06_v00_real_validation_acceptance_gate.yaml',
        '07_v00_real_validation_state.json',
        '08_v00_real_validation_handoff.schema.json',
        '09_schema_validation_spec.schema.json',
        '10_contract_validation_spec.schema.json',
        '11_field_model_validation_spec.schema.json',
        '12_rule_logic_validation_spec.schema.json',
        '13_test_execution_evidence.schema.json',
        '14_replay_execution_evidence.schema.json',
        '15_failure_evidence.schema.json',
        '16_validation_evidence_bundle.schema.json',
        '17_trace_audit_spec.yaml',
        '18_recovery_policy.md',
        '19_v00_real_validation_report_template.md',
    ]
    missing = [name for name in required if not (VALIDATION_ROOT / name).exists()]
    assert not missing


def test_v00_tools_exist():
    required = [
        'v00_real_validation_executor.py',
        'v00_schema_validator.py',
        'v00_contract_validator.py',
        'v00_field_model_validator.py',
        'v00_rule_logic_validator.py',
        'v00_test_runner.py',
        'v00_replay_executor.py',
        'v00_evidence_bundle_builder.py',
        'v00_validation_status.py',
    ]
    missing = [name for name in required if not (REPO / 'tools' / name).exists()]
    assert not missing


def test_v00_executor_generates_real_validation_evidence(tmp_path):
    pipeline = REPO / 'data/her_document_function_system/o00_runs/o00_run_20260513_183923_827542/state/pipeline_state.json'
    f00 = REPO / 'data/her_document_function_system/o00_runs/o00_run_20260513_183923_827542/handoffs/f00_to_v00_ref.json'
    out = tmp_path / 'v00_real_validation_run'
    result = subprocess.run([
        'python3', 'tools/v00_real_validation_executor.py',
        '--pipeline-run', str(pipeline),
        '--f00-handoff', str(f00),
        '--repo-root', str(REPO),
        '--output-dir', str(out),
        '--safe-mode',
    ], cwd=REPO, text=True, capture_output=True, timeout=120)

    assert result.returncode == 10, result.stdout + result.stderr

    required_outputs = [
        'preflight/v00_real_validation_preflight.json',
        'schema_validation/schema_validation_result.json',
        'contract_validation/contract_validation_result.json',
        'field_model_validation/field_model_validation_result.json',
        'rule_logic_validation/rule_logic_validation_result.json',
        'test_execution/test_execution_evidence.json',
        'test_execution/test_stdout.log',
        'test_execution/test_stderr.log',
        'replay_execution/replay_execution_evidence.json',
        'replay_execution/replay_input.json',
        'replay_execution/replay_output.json',
        'replay_execution/replay_trace.jsonl',
        'replay_execution/replay_comparison.json',
        'failure_evidence/failure_evidence.json',
        'evidence_bundle/validation_evidence_bundle.json',
        'trace/v00_real_validation_trace.jsonl',
        'audit/v00_real_validation_audit.jsonl',
        'acceptance/v00_real_validation_acceptance.json',
        'handoff/v00_real_validation_to_a00_handoff.json',
        'reports/v00_real_validation_report.md',
    ]
    missing = [rel for rel in required_outputs if not (out / rel).exists()]
    assert not missing

    test_evidence = json.loads((out / 'test_execution/test_execution_evidence.json').read_text())
    for key in ['test_command', 'exit_code', 'stdout_path', 'stderr_path', 'passed_count', 'failed_count']:
        assert key in test_evidence
    assert test_evidence['status'] == 'TESTED'
    assert test_evidence['exit_code'] == 0

    replay = json.loads((out / 'replay_execution/replay_execution_evidence.json').read_text())
    for key in ['replay_input', 'replay_output', 'trace_path', 'replay_comparison']:
        assert key in replay
    assert replay['status'] == 'REPLAY_TESTED'

    bundle = json.loads((out / 'evidence_bundle/validation_evidence_bundle.json').read_text())
    assert bundle['summary']['final_validation_status'] == 'V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS'
    assert bundle['ready_for_a00'] is True
    assert bundle['ready_for_r00'] is False
    forbidden_text = json.dumps(bundle, ensure_ascii=False)
    assert 'RUNNER_BOUND' not in forbidden_text
    assert 'POLICY_ACTIVE' not in forbidden_text
    assert 'PIPELINE_ACCEPTED' not in forbidden_text
