import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
REGISTRY = REPO_ROOT / 'system/her_document_function_system/registry/controller_registry.json'
CONFIG = REPO_ROOT / 'system/her_document_function_system/config/pipeline_config.full_safe_replay.json'
SAMPLE = REPO_ROOT / 'system/her_document_function_system/replay/sample_cases/sample_001_document_to_function/run/replay_run_config.json'
CLI = REPO_ROOT / 'tools/o00_cli.py'
CLI_RUNS = REPO_ROOT / 'data/her_document_function_system/cli_runs'
O00_RUNS = REPO_ROOT / 'data/her_document_function_system/o00_runs'


def run_cli(args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_json(path: Path):
    return json.loads(path.read_text())


def test_validate_config_reads_registry_config_and_enforces_safe_mode():
    result = run_cli([
        'validate-config',
        '--registry', str(REGISTRY.relative_to(REPO_ROOT)),
        '--config', str(CONFIG.relative_to(REPO_ROOT)),
        '--repo-root', str(REPO_ROOT),
        '--safe-mode',
    ])

    assert result.returncode == 0, result.stderr
    assert 'CONFIG_VALIDATED' in result.stdout
    assert 'SAFE_MODE_FALSE' not in result.stdout
    assert 'FORBIDDEN_ACTION_DETECTED' not in result.stdout


def test_run_sample_creates_cli_and_pipeline_runs_with_ready_with_gaps_status():
    result = run_cli([
        'run-sample',
        '--sample', str(SAMPLE.relative_to(REPO_ROOT)),
        '--registry', str(REGISTRY.relative_to(REPO_ROOT)),
        '--config', str(CONFIG.relative_to(REPO_ROOT)),
        '--repo-root', str(REPO_ROOT),
        '--safe-mode',
    ])

    assert result.returncode == 10, result.stderr
    assert 'PIPELINE_READY_WITH_GAPS' in result.stdout
    assert 'CLI_SAMPLE_REPLAY_COMPLETED_WITH_GAPS' in result.stdout
    assert 'O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS' in result.stdout

    marker_line = next(line for line in result.stdout.splitlines() if line.startswith('O00_RUN_RESULT='))
    marker = json.loads(marker_line.split('=', 1)[1])
    cli_dir = CLI_RUNS / marker['cli_run_id']
    pipeline_dir = O00_RUNS / marker['pipeline_run_id']

    for rel in [
        'command.json',
        'command_normalized.json',
        'preflight_result.json',
        'execution_result.json',
        'stdout.log',
        'stderr.log',
        'exit_code.json',
        'cli_trace.jsonl',
        'cli_audit.jsonl',
        'final_cli_report.md',
    ]:
        assert (cli_dir / rel).exists(), rel

    for rel in [
        'input/sample_document_ref.json',
        'input/operator_goal_ref.json',
        'input/replay_run_config_ref.json',
        'input/controller_registry_ref.json',
        'input/pipeline_config_ref.json',
        'preflight/o00_preflight_result.json',
        'preflight/governance_policy_check.json',
        'preflight/execution_boundary_check.json',
        'plan/pipeline_execution_plan.json',
        'plan/stage_dependency_graph.json',
        'plan/controller_registry_snapshot.json',
        'state/pipeline_state.json',
        'state/stage_state_matrix.json',
        'state/pipeline_status_history.json',
        'stage_refs/k00_run_ref.json',
        'stage_refs/f00_run_ref.json',
        'stage_refs/v00_run_ref.json',
        'stage_refs/r00_run_ref.json',
        'stage_refs/a00_run_ref.json',
        'stage_refs/h00_run_ref.json',
        'stage_refs/u00_run_ref.json',
        'stage_refs/g00_run_ref.json',
        'handoffs/k00_to_f00_ref.json',
        'handoffs/f00_to_v00_ref.json',
        'handoffs/v00_to_a00_ref.json',
        'handoffs/a00_to_h00_ref.json',
        'handoffs/h00_to_u00_ref.json',
        'handoffs/u00_to_g00_ref.json',
        'handoffs/o00_final_handoff.json',
        'gaps/pipeline_gap_register.json',
        'gaps/gap_propagation_matrix.json',
        'gaps/unresolved_gaps.json',
        'gaps/accepted_risks.json',
        'evidence/pipeline_evidence_bundle.json',
        'evidence/phase_evidence_refs.json',
        'evidence/replay_result.json',
        'evidence/expected_vs_actual_check.json',
        'acceptance/pipeline_acceptance_matrix.json',
        'acceptance/o00_acceptance_result.json',
        'recovery/recovery_report.json',
        'trace/o00_trace.jsonl',
        'trace/o00_audit.jsonl',
        'trace/cross_phase_trace_index.json',
        'reports/o00_final_report.md',
        'reports/pipeline_summary.md',
    ]:
        assert (pipeline_dir / rel).exists(), rel

    exit_code = load_json(cli_dir / 'exit_code.json')
    assert exit_code['exit_code'] == 10
    assert exit_code['exit_name'] == 'READY_WITH_GAPS'
    assert exit_code['final_status'] == 'PIPELINE_READY_WITH_GAPS'
    assert exit_code['blocking'] is False


def test_sample_replay_blocks_false_completion_statuses_and_preserves_expected_gaps():
    result = run_cli([
        'run-sample',
        '--sample', str(SAMPLE.relative_to(REPO_ROOT)),
        '--registry', str(REGISTRY.relative_to(REPO_ROOT)),
        '--config', str(CONFIG.relative_to(REPO_ROOT)),
        '--repo-root', str(REPO_ROOT),
        '--safe-mode',
    ])
    assert result.returncode == 10, result.stderr
    marker_line = next(line for line in result.stdout.splitlines() if line.startswith('O00_RUN_RESULT='))
    marker = json.loads(marker_line.split('=', 1)[1])
    pipeline_dir = O00_RUNS / marker['pipeline_run_id']

    state = load_json(pipeline_dir / 'state/pipeline_state.json')
    matrix = load_json(pipeline_dir / 'state/stage_state_matrix.json')
    acceptance = load_json(pipeline_dir / 'acceptance/pipeline_acceptance_matrix.json')
    gaps = load_json(pipeline_dir / 'gaps/pipeline_gap_register.json')
    final_report = (pipeline_dir / 'reports/o00_final_report.md').read_text()
    trace = (pipeline_dir / 'trace/o00_trace.jsonl').read_text()

    assert state['final_status'] == 'PIPELINE_READY_WITH_GAPS'
    assert state['system_status_code'] == 'O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS'
    assert matrix['V00']['status'] == 'V00_READY_WITH_GAPS'
    assert matrix['R00']['status'] == 'SKIPPED_WITH_REASON'
    assert matrix['G00']['status'] == 'G00_READY_WITH_GAPS'
    assert 'TESTED' in acceptance['forbidden_claims_blocked']
    assert 'RUNNER_BOUND' in acceptance['forbidden_claims_blocked']
    assert 'POLICY_ACTIVE' in acceptance['forbidden_claims_blocked']
    assert 'PIPELINE_ACCEPTED' in acceptance['forbidden_claims_blocked']
    assert {gap['gap_id'] for gap in gaps['gaps']} >= {
        'gap_sample_001_v00_test_not_executed',
        'gap_sample_001_g00_policy_not_active',
        'gap_sample_001_r00_not_required',
    }

    forbidden_phrases = [
        'final_status: PIPELINE_ACCEPTED',
        'SYSTEM_FULLY_IMPLEMENTED',
        'FUNCTION_IMPLEMENTED',
        'POLICY_ACTIVE: true',
        'RUNNER_BOUND: true',
        'TESTED: true',
    ]
    for phrase in forbidden_phrases:
        assert phrase not in final_report
    for event in [
        'cli_started',
        'safe_mode_checked',
        'registry_loaded',
        'config_loaded',
        'sample_loaded',
        'pipeline_run_created',
        'v00_simulated_with_gaps',
        'r00_skipped_with_reason',
        'g00_simulated_with_gaps',
        'pipeline_acceptance_built',
        'gap_register_written',
        'final_report_written',
        'exit_code_written',
        'cli_completed_with_gaps',
    ]:
        assert event in trace
    for forbidden_event in [
        'live_runtime_started',
        'wallet_signing_requested',
        'auto_deploy_started',
        'production_trade_executed',
        'test_plan_marked_as_tested',
        'runner_bound_without_dry_run',
        'policy_marked_active_without_acceptance',
    ]:
        assert forbidden_event not in trace
