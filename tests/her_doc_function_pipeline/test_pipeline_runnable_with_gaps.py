import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
DOC = REPO_ROOT / 'sikk_stable_trader_os/00_knowledge_intake/raw_inputs/HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS.md'


def run_pipeline(tmp_path, extra_args=None):
    out = tmp_path / 'her_doc_run_test'
    cmd = [
        sys.executable,
        str(REPO_ROOT / 'tools/o00_run_document_main.py'),
        '--document', str(DOC),
        '--goal', '测试 HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS 主链路',
        '--repo-root', str(REPO_ROOT),
        '--output-dir', str(out),
    ]
    if extra_args:
        cmd += extra_args
    proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
    return proc, out


def load(run_dir, rel):
    return json.loads((run_dir / rel).read_text(encoding='utf-8'))


def test_o00_run_document_requires_real_document(tmp_path):
    out = tmp_path / 'missing_doc_run'
    proc = subprocess.run([
        sys.executable, str(REPO_ROOT / 'tools/o00_run_document_main.py'),
        '--document', str(tmp_path / 'missing.md'), '--goal', 'x', '--repo-root', str(REPO_ROOT), '--output-dir', str(out), '--safe-mode'
    ], cwd=REPO_ROOT, text=True, capture_output=True)
    assert proc.returncode != 0
    assert 'document' in (proc.stderr + proc.stdout).lower()


def test_o00_run_document_safe_mode_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=[])
    assert proc.returncode != 0
    recovery = out / 'recovery/recovery_report.json'
    assert recovery.exists()
    assert load(out, 'recovery/recovery_report.json')['recovery_status'] == 'BLOCKED_SAFE_MODE_REQUIRED'


def test_k00_outputs_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    for rel in ['k00/document_passport.json','k00/corpus_index.json','k00/system_mapping.json','k00/k00_handoff_packet.json']:
        assert (out / rel).exists()
    assert load(out, 'k00/document_passport.json')['status'] == 'K00_READY_WITH_GAPS'


def test_f00_function_mapping_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    mapping = load(out, 'f00/function_mapping.json')
    assert mapping['status'] == 'F00_FUNCTION_MAPPING_READY_WITH_GAPS'
    assert mapping['mapped_functions']
    for fn in mapping['mapped_functions']:
        assert fn['target_controller']
        assert fn['required_inputs']
        assert fn['required_outputs']
        assert fn['required_files']
        assert fn['required_tools']
        assert fn['implementation_status'] == 'TASK_REQUIRED'


def test_v00_gap_register_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    gaps = load(out, 'v00/gap_register.json')['gaps']
    assert gaps
    for gap in gaps:
        assert gap['gap_level']
        assert gap['route_to']
        assert gap['status'] == 'OPEN'


def test_a00_acceptance_result_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    result = load(out, 'a00/a00_acceptance_result.json')
    assert result['final_status'] == 'HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS'
    assert result['ready_for_h00'] is True
    assert result['ready_for_production'] is False
    assert 'PRODUCTION_READY' in result['forbidden_claims_blocked']


def test_h00_downstream_queue_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    queue = load(out, 'h00/downstream_queue.json')
    assert queue['queue_status'] == 'QUEUE_READY_WITH_GAPS'
    assert queue['items']
    assert all(item['target_controller'] for item in queue['items'])
    assert (out / 'h00/routing_decision.json').exists()


def test_u00_upgrade_queue_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    assert load(out, 'u00/review_cases.json')['review_cases']
    assert load(out, 'u00/root_cause_analysis.json')['root_causes']
    assert load(out, 'u00/upgrade_queue.json')['items']
    assert load(out, 'u00/learning_index.json')['lessons']


def test_g00_governance_candidates_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    assert load(out, 'g00/governance_candidates.json')['governance_candidates']
    assert load(out, 'g00/policy_rules_update.json')['policy_rules_update']


def test_trace_audit_required(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    assert (out / 'trace.jsonl').exists()
    assert (out / 'audit.jsonl').exists()
    assert len((out / 'trace.jsonl').read_text(encoding='utf-8').splitlines()) >= 8
    assert 'forbidden_action_check' in (out / 'audit.jsonl').read_text(encoding='utf-8')


def test_no_production_ready_claim(tmp_path):
    proc, out = run_pipeline(tmp_path, extra_args=['--safe-mode'])
    assert proc.returncode == 10, proc.stdout + proc.stderr
    summary = load(out, 'o00/run_summary.json')
    assert summary['final_status'] == 'HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS'
    assert summary['ready_for_production'] is False
    generated_files = [p for p in out.rglob('*') if p.is_file() and p.suffix in {'.json', '.md', '.jsonl'} and 'input' not in p.parts]
    all_text = '\n'.join(p.read_text(encoding='utf-8') for p in generated_files)
    assert 'PRODUCTION_READY": true' not in all_text
    assert summary['final_status'] != 'HER_DOC_FUNCTION_PIPELINE_READY'
