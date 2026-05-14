#!/usr/bin/env python3
"""HER_DOC runtime binding review.

Safe/read-only scanner that classifies each HER_DOC controller by runner/runtime
binding depth. It never enables live runtime, signing, deploy, policy-active, or
production trading.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTROLLERS = [
    ('K00', 'K00_knowledge_intake_controller'),
    ('F00', 'F00_function_realization_controller'),
    ('V00', 'V00_validation_controller'),
    ('R00', 'R00_runtime_replay_controller'),
    ('A00', 'A00_acceptance_evidence_controller'),
    ('H00', 'H00_handoff_controller'),
    ('U00', 'U00_update_learning_controller'),
    ('G00', 'G00_governance_boundary_controller'),
    ('O00', 'O00_full_pipeline_orchestrator'),
]

RUNNER_HINTS = {
    'K00': ['tools/k00_document_intake.py'],
    'F00': ['modules/her_document_function_system/f00_runner.py', 'tools/her_document_function_system/f00_safe_runner.py'],
    'V00': ['tools/v00_real_validation_executor.py', 'tools/v00_replay_executor.py', 'tools/v00_test_runner.py'],
    'R00': ['tools/r00_real_runtime_executor.py', 'tools/o00_replay_runner.py'],
    'A00': ['tools/a00_real_acceptance_executor.py'],
    'H00': ['tools/h00_real_queue_executor.py'],
    'U00': ['tools/u00_real_review_executor.py'],
    'G00': ['tools/g00_real_policy_registry_executor.py'],
    'O00': ['tools/o00_cli.py', 'tools/o00_pipeline_orchestrator.py', 'tools/o00_run_document_main.py'],
}

EVIDENCE_HINTS = {
    'F00': ['data/her_document_function_system/f00_runs/F00-RUN-20260513-PASSED/runner_binding_evidence.json'],
    'V00': ['data/her_document_function_system/v00_real_validation_runs/V00-P01-AUTO-FULL-20260514-001/acceptance/v00_real_validation_acceptance.json'],
    'A00': ['data/her_document_function_system/a00_real_acceptance_runs/A00-P01-AUTO-FULL-20260514-001/decision/acceptance_decision.json'],
    'H00': ['data/her_document_function_system/h00_real_queue_runs/H00-P01-AUTO-FULL-20260514-001/acceptance/h00_real_queue_acceptance.json'],
    'U00': ['data/her_document_function_system/u00_real_review_runs/U00-P01-AUTO-FULL-20260514-005/acceptance/u00_acceptance_result.json'],
    'G00': ['data/her_document_function_system/g00_real_policy_runs/G00-P01-AUTO-FULL-20260514-001/acceptance/g00_real_policy_acceptance.json'],
    'O00': ['data/her_document_function_system/o00_run_document_runs/o00_run_20260514_102849_788851/reports/o00_final_report.md'],
}

FORBIDDEN = ['live_runtime', 'wallet_signing', 'auto_deploy', 'production_trading', 'execute_real_order', 'broadcast', 'private_key', 'policy_active']
ALLOWED_RUNTIME_STATUS = {'SAFE_MODE_BOUND', 'DESIGN_LEVEL_REPLAY_ONLY', 'READ_ONLY_VALIDATOR_BOUND', 'ACCEPTANCE_REVIEW_BOUND', 'QUEUE_REVIEW_BOUND', 'GOVERNANCE_CANDIDATE_BOUND'}


def now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def exists(repo: Path, rel: str) -> bool:
    return (repo / rel).exists()


def classify(phase: str, runner_files: list[str], evidence_files: list[str]) -> tuple[str, str]:
    has_runner = bool(runner_files)
    has_evidence = bool(evidence_files)
    if phase == 'R00':
        if has_runner and has_evidence:
            return 'DESIGN_LEVEL_REPLAY_ONLY', 'R00 has replay tooling but no production runtime activation evidence; keep safe-mode.'
        return 'DESIGN_LEVEL_REPLAY_ONLY', 'R00 real runtime binding is not proven; replay/design-level only.'
    if phase == 'F00' and has_runner and has_evidence:
        return 'SAFE_MODE_BOUND', 'F00 module CLI binding evidence exists and is marked safe-mode.'
    if phase == 'V00' and has_runner and has_evidence:
        return 'READ_ONLY_VALIDATOR_BOUND', 'V00 validation executor evidence exists; read-only validation only.'
    if phase == 'A00' and has_runner and has_evidence:
        return 'ACCEPTANCE_REVIEW_BOUND', 'A00 acceptance executor evidence exists; acceptance review only.'
    if phase == 'H00' and has_runner and has_evidence:
        return 'QUEUE_REVIEW_BOUND', 'H00 handoff/queue evidence exists; queue handoff only.'
    if phase == 'U00' and has_runner and has_evidence:
        return 'ACCEPTANCE_REVIEW_BOUND', 'U00 review executor evidence exists; review/update candidates only.'
    if phase == 'G00' and has_runner and has_evidence:
        return 'GOVERNANCE_CANDIDATE_BOUND', 'G00 policy registry evidence exists; candidate policy only, not policy active.'
    if phase == 'O00' and has_runner and has_evidence:
        return 'DESIGN_LEVEL_REPLAY_ONLY', 'O00 safe-mode orchestration evidence exists; final state remains READY_WITH_GAPS.'
    if has_runner:
        return 'RUNNER_FILE_ONLY_NO_ACCEPTANCE_EVIDENCE', 'Runner file exists but acceptance/runtime evidence is missing.'
    return 'NOT_BOUND', 'No runner file or runtime evidence located by review scanner.'


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='/root/sikk-gmgn')
    ap.add_argument('--run-id', default='runtime_binding_review_20260514_1038')
    args = ap.parse_args()
    repo = Path(args.repo_root)
    out = repo / 'data/her_document_function_system/runtime_binding_review' / args.run_id
    rows = []
    gaps = []
    for phase, controller in CONTROLLERS:
        controller_dir = repo / 'system/her_document_function_system/controllers' / controller
        runner_files = [p for p in RUNNER_HINTS.get(phase, []) if exists(repo, p)]
        evidence_files = [p for p in EVIDENCE_HINTS.get(phase, []) if exists(repo, p)]
        status, reason = classify(phase, runner_files, evidence_files)
        row = {
            'phase': phase,
            'controller': controller,
            'controller_exists': controller_dir.exists(),
            'runner_files': runner_files,
            'evidence_files': evidence_files,
            'runtime_binding_status': status,
            'reason': reason,
            'allowed_scope': 'safe-mode/read-only/design-level/candidate-only',
            'forbidden_runtime_modes': FORBIDDEN,
            'can_claim_policy_active': False,
            'can_claim_production_ready': False,
        }
        rows.append(row)
        if status not in ALLOWED_RUNTIME_STATUS:
            gaps.append({
                'gap_id': f'RUNTIME_BINDING_GAP_{phase}',
                'phase': phase,
                'status': status,
                'reason': reason,
                'required_next_evidence': ['runner_binding_evidence', 'contract_test_result', 'semantic_replay_result', 'handoff_consumption_trace'],
                'safety_policy': 'Do not upgrade to live runtime; keep safe-mode until explicit acceptance.'
            })
    summary_status = 'RUNTIME_BINDING_REVIEW_READY_WITH_GAPS' if gaps else 'RUNTIME_BINDING_REVIEW_SAFE_BOUND'
    result = {
        'review_id': args.run_id,
        'created_at': now(),
        'repo_root': str(repo),
        'system': 'HER_DOC_RUNTIME_BINDING_REVIEW',
        'summary_status': summary_status,
        'safe_mode': True,
        'forbidden_actions': FORBIDDEN,
        'controller_runtime_binding_matrix': rows,
        'gap_count': len(gaps),
        'gaps': gaps,
        'final_claims': {
            'full_runtime_ready': False,
            'policy_active': False,
            'production_ready': False,
            'real_trading_ready': False,
            'safe_mode_review_complete': True,
        }
    }
    write_json(out / 'runtime_binding_matrix.json', result)
    write_json(out / 'runtime_binding_gap_register.json', {'review_id': args.run_id, 'gap_count': len(gaps), 'gaps': gaps})
    task_package = {
        'task_package_id': f'{args.run_id}_task_package',
        'status': 'READY_WITH_GAPS' if gaps else 'READY',
        'tasks': [
            {'task_id': 'RB-001', 'title': 'Bind K00 intake runner evidence or explicitly keep K00 as document-intake only', 'phase': 'K00', 'priority': 'P1', 'status': 'OPEN' if any(g['phase']=='K00' for g in gaps) else 'NOT_REQUIRED'},
            {'task_id': 'RB-002', 'title': 'Create R00 replay/runtime boundary evidence without enabling live runtime', 'phase': 'R00', 'priority': 'P0', 'status': 'OPEN' if any(g['phase']=='R00' for g in gaps) else 'DESIGN_LEVEL_ONLY'},
            {'task_id': 'RB-003', 'title': 'Add semantic replay/contract tests for all safe-bound executors', 'phase': 'ALL', 'priority': 'P1', 'status': 'OPEN'},
            {'task_id': 'RB-004', 'title': 'Produce phase-to-phase handoff consumption trace for bound runners', 'phase': 'H00/O00', 'priority': 'P1', 'status': 'OPEN'},
        ],
        'forbidden_actions': FORBIDDEN,
    }
    write_json(out / 'runtime_binding_task_package.json', task_package)
    report_lines = [
        '# HER_DOC Runtime Binding Review Report', '',
        f'- review_id: `{args.run_id}`',
        f'- summary_status: `{summary_status}`',
        f'- gap_count: `{len(gaps)}`',
        '- scope: safe-mode/read-only/design-level/candidate-only',
        '- forbidden: live_runtime, wallet_signing, auto_deploy, production_trading, execute_real_order, broadcast, private_key, policy_active',
        '', '## Controller Matrix'
    ]
    for row in rows:
        report_lines.append(f"- {row['phase']} / {row['controller']}: `{row['runtime_binding_status']}` — {row['reason']}")
    report_lines.extend(['', '## Gaps'])
    if gaps:
        for gap in gaps:
            report_lines.append(f"- {gap['gap_id']}: {gap['status']} — {gap['reason']}")
    else:
        report_lines.append('- none')
    report_lines.extend(['', '## Final Decision', '', '`RUNTIME_BINDING_REVIEW_READY_WITH_GAPS` — 不升级为 production runtime；只允许 safe-mode/read-only/design-level/candidate-only。'])
    (out / 'runtime_binding_review_report.md').write_text('\n'.join(report_lines) + '\n', encoding='utf-8')
    print(json.dumps({'status': summary_status, 'out_dir': str(out), 'gap_count': len(gaps)}, ensure_ascii=False))
    return 10 if gaps else 0

if __name__ == '__main__':
    raise SystemExit(main())
