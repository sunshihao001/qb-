#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply Wallet-Structure system gap task packages by priority.

Runs additive runtime adapters for task-package next_actions. Defaults to P0 so
high-priority document-only gaps are processed first.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.wallet_structure_governance.runtime_adapters import apply_gap_action

PRIORITY_RANK = {'P0': 0, 'P1': 1, 'P2': 2}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _load_manifest(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _should_apply(priority: str, max_priority: str) -> bool:
    return PRIORITY_RANK.get(priority, 99) <= PRIORITY_RANK.get(max_priority, 99)


def apply_task_package(
    *,
    project_root: str | Path = '.',
    task_manifest: str | Path,
    max_priority: str = 'P0',
    only_priority: str | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    manifest = _load_manifest(task_manifest)
    tid = task_id or f"apply_{manifest.get('task_id', 'wallet_structure_gap_task')}"
    output_dir = root / 'research_loop' / 'state' / tid
    applied = []
    skipped = []
    for action in manifest.get('next_actions', []):
        priority = action.get('priority', 'P9')
        if only_priority:
            if priority == only_priority:
                applied.append(apply_gap_action(root, action, output_dir=output_dir))
            else:
                skipped.append({
                    'status': 'SKIPPED_BY_ONLY_PRIORITY',
                    'source_file': action.get('source_file'),
                    'priority': priority,
                    'order': action.get('order'),
                })
        elif _should_apply(priority, max_priority):
            applied.append(apply_gap_action(root, action, output_dir=output_dir))
        else:
            skipped.append({
                'status': 'SKIPPED_BY_PRIORITY',
                'source_file': action.get('source_file'),
                'priority': priority,
                'order': action.get('order'),
            })
    apply_manifest = {
        'artifact_type': 'wallet_structure_apply_task_package_manifest',
        'task_id': tid,
        'source_task_manifest': str(task_manifest),
        'generated_at': _utc_now(),
        'max_priority': max_priority,
        'only_priority': only_priority,
        'status': 'COMPLETED',
        'applied_count': len(applied),
        'skipped_count': len(skipped),
        'by_priority': {
            'P0': sum(1 for item in applied if item.get('priority') == 'P0'),
            'P1': sum(1 for item in applied if item.get('priority') == 'P1'),
            'P2': sum(1 for item in applied if item.get('priority') == 'P2'),
        },
        'applied': applied,
        'skipped': skipped,
        'automation_policy': {
            'delete_old_files': False,
            'move_old_files': False,
            'copy_legacy_to_new_layout': True,
            'paper_only': True,
            'no_private_key': True,
            'no_signing': True,
            'no_broadcast': True,
            'no_swap': True,
        },
    }
    apply_manifest_path = output_dir / 'apply_manifest.json'
    _write_json(apply_manifest_path, apply_manifest)
    return {
        'status': 'COMPLETED',
        'task_id': tid,
        'applied_count': len(applied),
        'skipped_count': len(skipped),
        'apply_manifest': str(apply_manifest_path),
        'output_dir': str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Apply Wallet-Structure system gap task package')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--task-manifest', required=True)
    parser.add_argument('--max-priority', choices=['P0', 'P1', 'P2'], default='P0')
    parser.add_argument('--task-id', default='')
    args = parser.parse_args()
    result = apply_task_package(
        project_root=args.project_root,
        task_manifest=args.task_manifest,
        max_priority=args.max_priority,
        task_id=args.task_id or None,
        only_priority=None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
