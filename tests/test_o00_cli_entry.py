import json
import subprocess
import sys
from pathlib import Path

REPO = Path('/root/sikk-gmgn')
CLI = REPO / 'tools/o00_cli.py'
REGISTRY = 'system/her_document_function_system/registry/controller_registry.json'
CONFIG = 'system/her_document_function_system/config/pipeline_config.full_safe_replay.json'
SAMPLE = 'system/her_document_function_system/replay/sample_cases/sample_001_document_to_function/run/replay_run_config.json'


def run_cli(*args):
    return subprocess.run([sys.executable, str(CLI), *args], cwd=REPO, text=True, capture_output=True)


def latest_run():
    runs = sorted((REPO / 'data/her_document_function_system/o00_runs').glob('o00_run_*'), key=lambda p: p.stat().st_mtime)
    assert runs
    return runs[-1]


def test_validate_config_passes():
    proc = run_cli('validate-config', '--registry', REGISTRY, '--config', CONFIG, '--repo-root', str(REPO), '--safe-mode')
    assert proc.returncode == 0
    cli_runs = sorted((REPO / 'data/her_document_function_system/cli_runs').glob('cli_run_validate-config_*'), key=lambda p: p.stat().st_mtime)
    result = json.loads((cli_runs[-1] / 'config_validation_result.json').read_text())
    assert result['status'] == 'CONFIG_VALIDATED'
    assert result['blocking_gaps'] == []


def test_run_sample_ready_with_gaps_and_blocks_false_claims():
    proc = run_cli('run-sample', '--sample', SAMPLE, '--registry', REGISTRY, '--config', CONFIG, '--repo-root', str(REPO), '--safe-mode')
    assert proc.returncode == 10
    run = latest_run()
    state = json.loads((run / 'state/pipeline_state.json').read_text())
    acceptance = json.loads((run / 'acceptance/pipeline_acceptance_matrix.json').read_text())
    report = (run / 'reports/o00_final_report.md').read_text()
    assert state['current_status'] == 'PIPELINE_READY_WITH_GAPS'
    assert acceptance['false_tested_blocked'] is True
    assert acceptance['false_runner_bound_blocked'] is True
    assert acceptance['false_policy_active_blocked'] is True
    assert 'final_status: `PIPELINE_READY_WITH_GAPS`' in report
    assert 'TESTED`' not in report
    assert (run / 'trace/o00_trace.jsonl').exists()
    assert (run / 'trace/o00_audit.jsonl').exists()


def test_status_show_report_show_gaps_and_recover():
    proc = run_cli('run-sample', '--sample', SAMPLE, '--registry', REGISTRY, '--config', CONFIG, '--repo-root', str(REPO), '--safe-mode')
    assert proc.returncode == 10
    run_id = latest_run().name
    assert run_cli('status', '--run-id', run_id, '--repo-root', str(REPO)).returncode == 0
    assert run_cli('show-report', '--run-id', run_id, '--repo-root', str(REPO)).returncode == 0
    assert run_cli('show-gaps', '--run-id', run_id, '--repo-root', str(REPO)).returncode == 0
    assert run_cli('recover', '--run-id', run_id, '--repo-root', str(REPO), '--safe-mode').returncode == 70
    assert (REPO / 'data/her_document_function_system/o00_runs' / run_id / 'recovery/recovery_report.json').exists()


def test_run_sample_requires_safe_mode():
    proc = run_cli('run-sample', '--sample', SAMPLE, '--registry', REGISTRY, '--config', CONFIG, '--repo-root', str(REPO))
    assert proc.returncode == 40
