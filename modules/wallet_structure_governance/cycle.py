#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-call governance cycle for Wallet Structure Governance."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .gap_scanner import scan_wallet_structure_system_gaps
from .runtime_adapters import apply_gap_action
from .integration import integrate_runtime_adapters
from .consumption import consume_runtime_registry

PRIORITY_RANK = {'P0': 0, 'P1': 1, 'P2': 2}


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _should_apply(priority: str, max_priority: str) -> bool:
    return PRIORITY_RANK.get(priority, 99) <= PRIORITY_RANK.get(max_priority, 99)


def _build_next_actions(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = []
    for idx, f in enumerate(findings, 1):
        actions.append({
            'order': idx,
            'priority': f['priority'],
            'source_file': f['file_path'],
            'gap_type': f['gap_type'],
            'capability': f['capability'],
            'action': f['recommended_action']['action'],
            'target_module': f['recommended_action']['target_module'],
            'automation_step': {
                'create_test_first': True,
                'suggested_runtime_target': f['recommended_action']['target_module'],
                'safe_mode': 'paper_only_readonly_additive',
            },
        })
    return actions


def run_governance_cycle(
    *,
    project_root: str | Path = '.',
    output_root: str | Path | None = None,
    task_id: str | None = None,
    max_priority: str = 'P2',
) -> dict[str, Any]:
    root = Path(project_root)
    tid = task_id or f'wallet_structure_governance_cycle_{_utc_stamp()}'
    out = Path(output_root) if output_root else root / 'research_loop' / 'state' / tid
    scan_dir = out / 'scan'
    apply_dir = out / 'apply'
    integration_dir = out / 'integration'
    consumption_dir = out / 'consumption'

    scan = scan_wallet_structure_system_gaps(project_root=root, output_dir=scan_dir)
    next_actions = _build_next_actions(scan.get('findings', []))
    applied = []
    skipped = []
    for action in next_actions:
        if _should_apply(action.get('priority', 'P9'), max_priority):
            applied.append(apply_gap_action(root, action, output_dir=apply_dir))
        else:
            skipped.append(action)
    apply_manifest = {
        'artifact_type': 'wallet_structure_governance_cycle_apply_manifest',
        'task_id': tid,
        'generated_at': _utc_now(),
        'max_priority': max_priority,
        'applied_count': len(applied),
        'skipped_count': len(skipped),
        'applied': applied,
        'skipped': skipped,
        'automation_policy': scan.get('automation_policy', {}),
    }
    apply_manifest_path = _write_json(apply_dir / 'apply_manifest.json', apply_manifest)
    integration = integrate_runtime_adapters(project_root=root, adapter_state_dir=apply_dir, output_dir=integration_dir)
    consumption = consume_runtime_registry(project_root=root, registry_path=integration['registry_path'], output_dir=consumption_dir)
    final = {
        'artifact_type': 'wallet_structure_governance_cycle_manifest',
        'task_id': tid,
        'generated_at': _utc_now(),
        'status': 'PASS' if consumption.get('status') == 'PASS' else 'NEEDS_ACTION',
        'scan_json': scan['json_path'],
        'priority_md': scan['priority_md_path'],
        'apply_manifest': apply_manifest_path,
        'registry_path': integration['registry_path'],
        'integration_report': integration['report_path'],
        'consumption_report': consumption['report_path'],
        'consumption_status': consumption.get('status'),
        'summary': scan.get('summary', {}),
        'applied_count': len(applied),
        'skipped_count': len(skipped),
    }
    final_path = _write_json(out / 'wallet_structure_governance_cycle_manifest.json', final)
    final['cycle_manifest'] = final_path
    _write_json(out / 'wallet_structure_governance_cycle_manifest.json', final)
    return final
