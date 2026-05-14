#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-flow wrapper for Wallet-Structure system-standard gap remediation.

This runner scans document-only/system-standard gaps, writes a prioritized task
package, and produces machine-readable next actions. It is additive only: no
delete, no move, no trading side effects.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.wallet_structure_governance.gap_scanner import scan_wallet_structure_system_gaps


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return str(path)


def _build_next_actions(findings: list[dict[str, Any]], limit: int | None = None) -> list[dict[str, Any]]:
    actions = []
    selected = findings if limit is None else findings[:limit]
    for idx, f in enumerate(selected, 1):
        action = f['recommended_action']['action']
        actions.append({
            'order': idx,
            'priority': f['priority'],
            'source_file': f['file_path'],
            'gap_type': f['gap_type'],
            'capability': f['capability'],
            'action': action,
            'target_module': f['recommended_action']['target_module'],
            'automation_step': {
                'create_test_first': True,
                'suggested_test': f"tests/test_source_wallet_{f['capability']}_integration.py",
                'suggested_runtime_target': f['recommended_action']['target_module'],
                'safe_mode': 'paper_only_readonly_additive',
            },
        })
    return actions


def _build_task_md(manifest: dict[str, Any]) -> str:
    lines = [
        '# 钱包结构系统缺口自动处理任务包',
        '',
        f"- task_id: `{manifest['task_id']}`",
        f"- status: `{manifest['status']}`",
        '',
        '## 自动化处理顺序',
        '',
    ]
    for action in manifest['next_actions']:
        lines.append(f"{action['order']}. {action['priority']} `{action['source_file']}`")
        lines.append(f"   - gap_type: `{action['gap_type']}`")
        lines.append(f"   - action: `{action['action']}`")
        lines.append(f"   - target_module: `{action['target_module']}`")
        lines.append(f"   - test_first: `{action['automation_step']['suggested_test']}`")
    lines.extend([
        '',
        '## 自动化安全边界',
        '',
        '- 不删除旧文件',
        '- 不移动旧文件',
        '- copy-only / additive only',
        '- paper-only / readonly',
        '- no private key / no signing / no broadcast / no swap',
    ])
    return '\n'.join(lines) + '\n'


def run_system_gap_auto_flow(*, project_root: str | Path = '.', task_id: str | None = None) -> dict[str, Any]:
    root = Path(project_root)
    tid = task_id or f"wallet_structure_system_gap_scan_{_utc_stamp()}"
    state_dir = root / 'research_loop' / 'state' / tid
    package_dir = root / 'research_loop' / 'task_packages' / 'pending' / tid
    scan = scan_wallet_structure_system_gaps(project_root=root, output_dir=state_dir)
    next_actions = _build_next_actions(scan['findings'])
    manifest = {
        'artifact_type': 'wallet_structure_system_gap_task_manifest',
        'task_id': tid,
        'status': 'NEEDS_ACTION' if next_actions else 'COMPLETED',
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'scan_json': scan['json_path'],
        'priority_md': scan['priority_md_path'],
        'summary': scan['summary'],
        'next_actions': next_actions,
        'automation_policy': scan['automation_policy'],
    }
    manifest_path = package_dir / 'task_manifest.json'
    task_md_path = package_dir / 'next_actions.md'
    _write_json(manifest_path, manifest)
    _write_text(task_md_path, _build_task_md(manifest))
    return {
        'status': manifest['status'],
        'task_id': tid,
        'scan_json': scan['json_path'],
        'priority_md': scan['priority_md_path'],
        'task_package_dir': str(package_dir),
        'task_manifest': str(manifest_path),
        'next_actions_md': str(task_md_path),
        'summary': scan['summary'],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Run Wallet-Structure system gap auto flow')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--task-id', default='')
    args = parser.parse_args()
    result = run_system_gap_auto_flow(project_root=args.project_root, task_id=args.task_id or None)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
