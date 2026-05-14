#!/usr/bin/env python3
"""HER-DFAFS system self-audit runner.

Fixed command semantics:
- HER_DOC_SYSTEM_AUDIT
- HER_DOC_SYSTEM_REVIEW

This runner audits structure and contracts only. It does not claim production readiness.
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path('/root/sikk-gmgn/system/her_document_function_system')
REQUIRED_CONTROLLERS = [
    'G00_governance_boundary_controller',
    'K00_knowledge_intake_controller',
    'F00_function_realization_controller',
    'V00_validation_evidence_controller',
    'R00_runner_tool_binding_controller',
    'A00_acceptance_evidence_controller',
    'H00_handoff_downstream_queue_controller',
    'U00_review_upgrade_controller',
    'O00_full_pipeline_orchestrator',
]
SEMANTIC_ASSETS = {
    'manifest': [r'01_.*manifest\.ya?ml$', r'01_manifest\.ya?ml$'],
    'context_pack': [r'02_.*context_pack\.md$', r'02_context_pack\.md$'],
    'objective_tree': [r'03_.*objective_tree\.ya?ml$', r'03_objective_tree\.ya?ml$'],
    'input_contract': [r'04_.*input_contract\.json$', r'04_input_contract\.json$', r'03_.*input_contract\.json$'],
    'output_contract': [r'05_.*output_contract\.json$', r'04_.*output_contract\.json$'],
    'execution_protocol': [r'06_.*execution_protocol\.md$', r'05_.*execution_protocol\.md$'],
    'acceptance_gate': [r'07_.*acceptance_gate\.ya?ml$', r'06_.*acceptance_gate\.ya?ml$'],
    'state': [r'08_.*state\.json$', r'07_.*state\.json$'],
    'handoff_schema': [r'09_.*handoff.*\.schema\.json$', r'08_.*handoff.*\.schema\.json$'],
    'trace_audit': [r'.*trace.*audit.*\.(yaml|yml|json)$'],
    'recovery_policy': [r'.*recovery_policy.*\.(md|json|yaml|yml)$'],
    'report_template': [r'.*report_template\.md$'],
}
CORE_ASSETS = ['manifest','context_pack','input_contract','output_contract','execution_protocol','acceptance_gate','state','handoff_schema']


def find_semantic_assets(controller_dir: Path):
    files = [p.name for p in controller_dir.iterdir() if p.is_file()]
    result = {}
    for key, patterns in SEMANTIC_ASSETS.items():
        result[key] = [f for f in files if any(re.match(p, f) for p in patterns)]
    return result


def load_json_status(path: Path):
    try:
        json.loads(path.read_text(encoding='utf-8'))
        return 'JSON_OK'
    except Exception as exc:
        return f'JSON_ERROR: {exc}'


def audit(root: Path):
    controllers_root = root / 'controllers'
    audit_dir = root / 'system_audit'
    controller_reports = []
    gaps = []

    for name in REQUIRED_CONTROLLERS:
        cdir = controllers_root / name
        if not cdir.exists():
            severity = 'HIGH' if name == 'K00_knowledge_intake_controller' else 'MEDIUM'
            gaps.append({
                'gap_id': f'GAP-MISSING-{name}',
                'severity': severity,
                'description': f'Missing canonical controller directory: {cdir}',
                'status': 'OPEN',
            })
            controller_reports.append({'controller': name, 'exists': False, 'status': 'MISSING', 'missing_core_assets': CORE_ASSETS})
            continue
        assets = find_semantic_assets(cdir)
        missing = [k for k in CORE_ASSETS if not assets.get(k)]
        status = 'CORE_COMPLETE' if not missing else 'READY_WITH_GAPS'
        if missing:
            gaps.append({
                'gap_id': f'GAP-ASSET-{name}',
                'severity': 'MEDIUM',
                'description': f'Controller has missing semantic core assets: {missing}',
                'status': 'OPEN',
            })
        controller_reports.append({
            'controller': name,
            'exists': True,
            'status': status,
            'file_count': len([p for p in cdir.iterdir() if p.is_file()]),
            'semantic_assets': assets,
            'missing_core_assets': missing,
        })

    json_checks = {}
    for rel in ['CANONICAL_ROUTE.json', 'registry/controller_registry.json']:
        p = root / rel
        json_checks[rel] = load_json_status(p) if p.exists() else 'MISSING'
        if not p.exists():
            gaps.append({'gap_id': f'GAP-MISSING-{rel}', 'severity': 'HIGH', 'description': f'Missing {rel}', 'status': 'OPEN'})

    if not (root / 'system_audit').exists():
        gaps.append({'gap_id':'GAP-SYSTEM-AUDIT-ENTRYPOINT','severity':'MEDIUM','description':'Missing system_audit directory','status':'OPEN'})

    high_open = [g for g in gaps if g['severity'] == 'HIGH']
    system_status = 'HER_DFAFS_SYSTEM_BLOCKED' if any('K00_knowledge_intake_controller' in g['gap_id'] for g in high_open) else ('HER_DFAFS_SYSTEM_READY_WITH_GAPS' if gaps else 'HER_DFAFS_SYSTEM_READY')

    return {
        'audit_id': 'HER_DOC_SYSTEM_AUDIT_AUTO',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'canonical_root': str(root),
        'system_status': system_status,
        'fixed_commands': ['HER_DOC_PIPELINE','HER_DOC_SYSTEM_AUDIT','HER_DOC_SYSTEM_REVIEW'],
        'json_checks': json_checks,
        'gap_count': len(gaps),
        'gaps': gaps,
        'controller_report': controller_reports,
        'status_policy': {
            'missing_k00_handoff': 'F00_BLOCKED',
            'missing_document_passport': 'F00_BLOCKED',
            'missing_corpus_index': 'F00_BLOCKED',
            'missing_system_mapping': 'F00_READY_WITH_GAPS_OR_BLOCKED',
            'missing_gap_detection': 'F00_BLOCKED',
            'missing_kv': 'KV_GAP_CONTINUE_ALLOWED',
            'missing_repo_root': 'DESIGN_ONLY',
            'missing_write_policy': 'DESIGN_ONLY_NO_FILE_WRITES',
            'missing_execution_boundary': 'F00_BLOCKED',
        },
    }


def main():
    ap = argparse.ArgumentParser(description='Run HER-DFAFS self-audit.')
    ap.add_argument('--root', default=str(DEFAULT_ROOT))
    ap.add_argument('--write', action='store_true', help='write result into system_audit/audit_result_auto.json')
    args = ap.parse_args()
    root = Path(args.root)
    result = audit(root)
    if args.write:
        out = root / 'system_audit' / 'audit_result_auto.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        result['written_to'] = str(out)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 10 if result['system_status'].endswith('READY_WITH_GAPS') or result['system_status'].endswith('BLOCKED') else 0

if __name__ == '__main__':
    raise SystemExit(main())
