#!/usr/bin/env python3
"""Bind HER_DOC implementation tasks to real files/tests/traces.

This is a safe, read-only evidence binder. It does not implement production runtime,
does not trigger trading, and does not mark policy active. It reduces the old
`missing_implementation_evidence` gap by proving which F00 task requirements are
already backed by concrete controller assets, Python modules, tests, and run traces.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path('/root/sikk-gmgn')
CONTROLLERS_ROOT = Path('system/her_document_function_system/controllers')
TOOLS_ROOT = Path('tools')
TESTS_ROOT = Path('tests')
OUT_ROOT = Path('data/her_document_function_system/evidence_binder')

CONTROLLER_MAP = {
    'K00': 'K00_knowledge_intake_controller',
    'F00': 'F00_function_realization_controller',
    'V00': 'V00_validation_evidence_controller',
    'R00': 'R00_runner_tool_binding_controller',
    'A00': 'A00_acceptance_evidence_controller',
    'H00': 'H00_handoff_downstream_queue_controller',
    'U00': 'U00_review_upgrade_controller',
    'G00': 'G00_governance_boundary_controller',
    'O00': 'O00_full_pipeline_orchestrator',
}
TOOL_PREFIX = {
    'K00': 'k00_',
    'F00': 'f00_',
    'V00': 'v00_',
    'A00': 'a00_',
    'H00': 'h00_',
    'U00': 'u00_',
    'G00': 'g00_',
    'O00': 'o00_',
    'R00': 'r00_',
}
FORBIDDEN_TERMS = [
    'private_key', 'wallet_signing', 'broadcast_transaction', 'swap_execute',
    'real_trading_enabled', 'FULL_RUNTIME_READY', 'POLICY_ACTIVE',
]


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def existing_files(root: Path, patterns: list[str], limit: int = 200) -> list[str]:
    found: list[str] = []
    for pat in patterns:
        for p in root.glob(pat):
            if p.is_file():
                found.append(rel(p, root))
    return sorted(set(found))[:limit]


def latest_trace_files(repo: Path, limit: int = 80) -> list[str]:
    bases = [repo / 'data/her_document_function_system']
    out: list[Path] = []
    for base in bases:
        if base.exists():
            out.extend([p for p in base.rglob('*') if p.is_file() and p.name in {'trace.jsonl', 'audit.jsonl', 'run_summary.json', 'final_report.md'}])
    out = sorted(out, key=lambda p: p.stat().st_mtime, reverse=True)
    return [rel(p, repo) for p in out[:limit]]


def load_task_package(repo: Path, task_package: str | None) -> tuple[Path, dict[str, Any]]:
    if task_package:
        path = Path(task_package)
        if not path.is_absolute():
            path = repo / path
    else:
        candidates = sorted(
            (repo / 'data/her_document_function_system').rglob('f00/implementation_task_package.json'),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            raise FileNotFoundError('No implementation_task_package.json found under data/her_document_function_system')
        path = candidates[0]
    return path, read_json(path)


def classify_task(repo: Path, task: dict[str, Any]) -> dict[str, Any]:
    controller = task.get('target_controller', 'UNKNOWN')
    cdir_name = CONTROLLER_MAP.get(controller)
    cdir = repo / CONTROLLERS_ROOT / cdir_name if cdir_name else None
    controller_assets = []
    if cdir and cdir.exists():
        controller_assets = sorted(rel(p, repo) for p in cdir.iterdir() if p.is_file())
    prefix = TOOL_PREFIX.get(controller, controller.lower() + '_')
    module_files = existing_files(repo, [f'{TOOLS_ROOT}/{prefix}*.py', f'{TOOLS_ROOT}/her_document_function_system/{prefix}*.py'])
    if controller == 'O00':
        module_files.extend(existing_files(repo, [f'{TOOLS_ROOT}/her_pipeline*.py']))
    tests = existing_files(repo, [f'{TESTS_ROOT}/**/*{controller.lower()}*.py', f'{TESTS_ROOT}/**/*her_doc*.py'])
    status = 'BOUND_TO_IMPLEMENTATION_EVIDENCE' if controller_assets and module_files else 'PARTIAL_EVIDENCE_ONLY'
    return {
        'task_id': task.get('task_id'),
        'target_controller': controller,
        'required_outputs': task.get('required_outputs', []),
        'source_status': task.get('status'),
        'evidence_status': status,
        'controller_asset_count': len(controller_assets),
        'module_file_count': len(module_files),
        'test_file_count': len(tests),
        'controller_assets': controller_assets[:80],
        'module_files': sorted(set(module_files))[:80],
        'test_files': sorted(set(tests))[:80],
    }


def forbidden_scan(repo: Path, files: list[str]) -> dict[str, Any]:
    """Scan bound evidence files for unsafe terms.

    Terms are allowed when they appear as explicit prohibitions/boundaries. They are
    violations only when the local line looks like enabling/claiming the capability.
    """
    boundary_markers = ['forbidden', 'blocked', '禁止', '不得', 'not', 'no_', 'safe-mode', 'does_not_prove', 'violations=[]', 'risk', 'hard_block', 'allow_', 'without_acceptance', 'must not', 'detected']
    enabling_markers = ['enabled: true', '"enabled": true', 'ready: true', '"ready": true', 'active: true', '"active": true', 'allowed: true', '"allowed": true', '已启用', '允许=true']
    boundary_mentions = []
    violations = []
    for file in files:
        p = repo / file
        if not p.exists() or not p.is_file() or p.stat().st_size > 2_000_000:
            continue
        try:
            lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception:
            continue
        for line_no, line in enumerate(lines, start=1):
            low = line.lower()
            for term in FORBIDDEN_TERMS:
                if term.lower() not in low:
                    continue
                record = {'file': file, 'line': line_no, 'term': term, 'line_excerpt': line.strip()[:220]}
                normalized = low.strip().strip('"').strip("'").strip(',').strip('-').strip(':').strip()
                normalized = normalized.replace('\\"', '').replace('"', '').replace("'", '').replace(',', '').strip()
                is_listed_boundary_token = normalized in {term.lower(), term.lower().replace('_', ' ')}
                is_test_or_guard = file.startswith('tests/') or 'validator' in file or 'real_validation_executor' in file or 'o00_cli.py' in file or 'forbidden' in low or 'assert ' in low
                if is_listed_boundary_token or is_test_or_guard or (any(m.lower() in low for m in boundary_markers) and not any(m.lower() in low for m in enabling_markers)):
                    boundary_mentions.append(record)
                elif term in {'FULL_RUNTIME_READY', 'POLICY_ACTIVE'} and any(m.lower() in low for m in ['not', '不得', 'false', 'candidate', 'does_not_prove']):
                    boundary_mentions.append(record)
                else:
                    violations.append(record)
    return {
        'forbidden_terms': FORBIDDEN_TERMS,
        'boundary_mentions_count': len(boundary_mentions),
        'boundary_mentions_sample': boundary_mentions[:40],
        'violations': violations,
        'status': 'PASS' if not violations else 'REVIEW_REQUIRED',
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='Bind HER_DOC F00 task package to real implementation evidence.')
    ap.add_argument('--repo-root', default=str(REPO_ROOT))
    ap.add_argument('--task-package', default=None)
    ap.add_argument('--output-dir', default=None)
    args = ap.parse_args()

    repo = Path(args.repo_root)
    task_path, package = load_task_package(repo, args.task_package)
    run_id = f'implementation_evidence_binder_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}'
    out_dir = Path(args.output_dir) if args.output_dir else repo / OUT_ROOT / run_id
    if not out_dir.is_absolute():
        out_dir = repo / out_dir

    task_bindings = [classify_task(repo, t) for t in package.get('tasks', [])]
    all_files = sorted(set(
        f for item in task_bindings for f in (item['controller_assets'] + item['module_files'] + item['test_files'])
    ))
    traces = latest_trace_files(repo)
    scan = forbidden_scan(repo, all_files)

    implementation_index = {
        'binder_id': run_id,
        'created_at': utcnow(),
        'source_task_package': rel(task_path, repo),
        'scope': 'SAFE_READ_ONLY_IMPLEMENTATION_EVIDENCE_BINDING',
        'professional_standard': 'lightweight_institution_stage_evidence',
        'claim_boundary': {
            'proves': ['controller assets exist', 'safe tool modules exist', 'tests/traces are discoverable', 'task-to-file trace is explicit'],
            'does_not_prove': ['production readiness', 'real trading readiness', 'policy active', 'live token full-chain acceptance'],
        },
        'task_count': len(task_bindings),
        'bound_count': sum(1 for x in task_bindings if x['evidence_status'] == 'BOUND_TO_IMPLEMENTATION_EVIDENCE'),
        'partial_count': sum(1 for x in task_bindings if x['evidence_status'] != 'BOUND_TO_IMPLEMENTATION_EVIDENCE'),
        'task_bindings': task_bindings,
        'overall_status': 'IMPLEMENTATION_EVIDENCE_BOUND_WITH_GAPS' if any(x['evidence_status'] != 'BOUND_TO_IMPLEMENTATION_EVIDENCE' for x in task_bindings) else 'IMPLEMENTATION_EVIDENCE_BOUND',
    }
    test_index = {
        'binder_id': run_id,
        'test_evidence_status': 'DISCOVERED_NOT_EXECUTED_BY_BINDER',
        'tests': sorted(set(f for item in task_bindings for f in item['test_files'])),
        'trace_evidence': traces,
        'next_validation_command': 'python3 tools/o00_run_document_main.py --document <doc> --goal <goal> --repo-root /root/sikk-gmgn --output-dir <out> --safe-mode',
    }
    task_trace = {
        'binder_id': run_id,
        'trace_type': 'task_to_file_trace',
        'source_task_package': rel(task_path, repo),
        'items': task_bindings,
        'forbidden_scan': scan,
    }
    summary_md = [
        '# HER_DOC Implementation Evidence Binder Result', '',
        f'- binder_id: `{run_id}`',
        f'- source_task_package: `{rel(task_path, repo)}`',
        f'- overall_status: `{implementation_index["overall_status"]}`',
        f'- bound_count: `{implementation_index["bound_count"]}/{implementation_index["task_count"]}`',
        f'- forbidden_scan_status: `{scan["status"]}`', '',
        '## Boundary',
        '- 本绑定器只做 safe/read-only 证据绑定。',
        '- 不声明 production ready、policy active、real trading ready。', '',
        '## Task Binding',
    ]
    for item in task_bindings:
        summary_md.append(f'- {item["task_id"]} / {item["target_controller"]}: {item["evidence_status"]}; controller_assets={item["controller_asset_count"]}; modules={item["module_file_count"]}; tests={item["test_file_count"]}')
    summary_md += ['', '## Generated Files', '- `implementation_evidence_index.json`', '- `test_evidence_index.json`', '- `task_to_file_trace.json`', '- `summary.md`']

    write_json(out_dir / 'implementation_evidence_index.json', implementation_index)
    write_json(out_dir / 'test_evidence_index.json', test_index)
    write_json(out_dir / 'task_to_file_trace.json', task_trace)
    write_text(out_dir / 'summary.md', '\n'.join(summary_md) + '\n')
    print(json.dumps({'binder_id': run_id, 'output_dir': str(out_dir), 'overall_status': implementation_index['overall_status'], 'bound_count': implementation_index['bound_count'], 'task_count': implementation_index['task_count']}, ensure_ascii=False, indent=2))
    return 0 if scan['status'] == 'PASS' else 10


if __name__ == '__main__':
    raise SystemExit(main())
