import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
CLI = REPO_ROOT / 'tools/o00_cli.py'
REGISTRY = REPO_ROOT / 'system/her_document_function_system/registry/controller_registry.json'
CONFIG = REPO_ROOT / 'system/her_document_function_system/config/pipeline_config.full_safe_replay.json'
DOCUMENT = REPO_ROOT / 'system/her_document_function_system/replay/sample_cases/o00_sample_document.md'
GOAL = REPO_ROOT / 'system/her_document_function_system/replay/sample_cases/o00_sample_goal.json'
RUN_ROOT = REPO_ROOT / 'data/her_document_function_system/o00_run_document_runs'
CTRL_ROOT = REPO_ROOT / 'system/her_document_function_system/orchestrator/o00_run_document_safe_mode'

EXPECTED_CONTROLLER_FILES = [
    '01_o00_manifest.yaml',
    '02_o00_context_pack.md',
    '03_o00_objective_tree.yaml',
    '04_o00_input_contract.json',
    '05_o00_output_contract.json',
    '06_o00_execution_protocol.md',
    '07_o00_acceptance_gate.yaml',
    '08_o00_state.json',
    '09_o00_handoff_packet.schema.json',
    '10_o00_run_config.schema.json',
    '11_pipeline_plan.schema.json',
    '12_pipeline_state.schema.json',
    '13_stage_dependency_graph.schema.json',
    '14_stage_result_ref.schema.json',
    '15_cross_phase_trace.schema.json',
    '16_pipeline_evidence_bundle.schema.json',
    '17_pipeline_acceptance.schema.json',
    '18_recovery_policy.schema.json',
    '19_trace_audit_spec.yaml',
    '20_o00_final_report_template.md',
]


def run_cli(*args):
    return subprocess.run([sys.executable, str(CLI), *args], cwd=REPO_ROOT, text=True, capture_output=True)


def marker(stdout: str):
    line = next(line for line in stdout.splitlines() if line.startswith('O00_RUN_RESULT='))
    return json.loads(line.split('=', 1)[1])


def test_o00_run_document_controller_file_pack_exists():
    assert CTRL_ROOT.exists()
    actual = sorted(p.name for p in CTRL_ROOT.iterdir() if p.is_file())
    assert actual == sorted(EXPECTED_CONTROLLER_FILES)
    assert RUN_ROOT.exists()
    input_contract = json.loads((CTRL_ROOT / '04_o00_input_contract.json').read_text())
    assert input_contract['required_inputs']['source_document']['required'] is True
    assert input_contract['required_inputs']['operator_goal']['required'] is True
    gate = (CTRL_ROOT / '07_o00_acceptance_gate.yaml').read_text()
    assert 'RUNNER_BOUND' in gate
    assert 'PIPELINE_ACCEPTED' in gate


def test_run_document_safe_mode_creates_document_run_with_ready_with_gaps_evidence():
    proc = run_cli(
        'run-document',
        '--document', str(DOCUMENT.relative_to(REPO_ROOT)),
        '--goal', str(GOAL.relative_to(REPO_ROOT)),
        '--registry', str(REGISTRY.relative_to(REPO_ROOT)),
        '--config', str(CONFIG.relative_to(REPO_ROOT)),
        '--repo-root', str(REPO_ROOT),
        '--safe-mode',
    )
    assert proc.returncode == 10, proc.stderr
    m = marker(proc.stdout)
    assert m['system_status_code'] == 'O00_RUN_DOCUMENT_READY_WITH_GAPS'
    run_dir = RUN_ROOT / m['pipeline_run_id']
    assert run_dir.exists()
    for rel in [
        'input/sample_document_ref.json',
        'input/operator_goal_ref.json',
        'plan/pipeline_execution_plan.json',
        'state/pipeline_state.json',
        'gaps/pipeline_gap_register.json',
        'evidence/pipeline_evidence_bundle.json',
        'acceptance/o00_acceptance_result.json',
        'trace/o00_trace.jsonl',
        'handoffs/o00_final_handoff.json',
        'reports/o00_final_report.md',
    ]:
        assert (run_dir / rel).exists(), rel
    state = json.loads((run_dir / 'state/pipeline_state.json').read_text())
    acceptance = json.loads((run_dir / 'acceptance/pipeline_acceptance_matrix.json').read_text())
    trace = (run_dir / 'trace/o00_trace.jsonl').read_text()
    assert state['final_status'] == 'PIPELINE_READY_WITH_GAPS'
    assert state['system_status_code'] == 'O00_RUN_DOCUMENT_READY_WITH_GAPS'
    assert acceptance['accepted'] is False
    assert acceptance['ready_with_gaps'] is True
    assert 'TESTED' in acceptance['forbidden_claims_blocked']
    assert 'document_loaded' in trace
    assert 'live_runtime_started' not in trace
    report = (run_dir / 'reports/o00_final_report.md').read_text()
    assert 'command: `run-document`' in report
    assert 'system_status_code: `O00_RUN_DOCUMENT_READY_WITH_GAPS`' in report
    assert 'O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS' not in report


def test_run_document_requires_document_goal_and_safe_mode():
    no_safe = run_cli('run-document', '--document', str(DOCUMENT.relative_to(REPO_ROOT)), '--goal', str(GOAL.relative_to(REPO_ROOT)), '--repo-root', str(REPO_ROOT))
    assert no_safe.returncode == 40
    missing = run_cli('run-document', '--repo-root', str(REPO_ROOT), '--safe-mode')
    assert missing.returncode == 30
    assert 'missing_required_run_document_inputs' in missing.stdout
