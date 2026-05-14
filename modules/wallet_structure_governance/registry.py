#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runtime adapter registry for Wallet-Structure system-standard integration.

Reads generated runtime adapter artifacts and builds a system-readable registry
that can be validated by Source Wallet Bot schema governance.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INTEGRATION_TARGETS: dict[str, dict[str, str]] = {
    'legacy_path_map_runtime_adapter': {
        'target': 'modules/source_wallet_bot/path_resolver.py',
        'integration_role': 'controlled_read_resolver_input',
    },
    'legacy_manifest_runtime_adapter': {
        'target': 'modules/source_wallet_bot/path_resolver.py',
        'integration_role': 'copy_only_migration_manifest_input',
    },
    'wallet_data_passport_runtime_adapter': {
        'target': 'modules/wallet_data_guard/source_manifest.py',
        'integration_role': 'semantic_passport_manifest_input',
    },
    'schema_contract_runtime_adapter': {
        'target': 'modules/source_wallet_bot/schema_validator.py',
        'integration_role': 'schema_contract_validation_input',
    },
    'interface_inventory_runtime_adapter': {
        'target': 'modules/source_wallet_bot/system_gap_scanner.py',
        'integration_role': 'interface_inventory_runtime_index',
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _iter_adapter_files(adapter_state_dir: Path) -> list[Path]:
    base = adapter_state_dir / 'runtime_adapters'
    if not base.exists():
        return []
    return sorted(base.rglob('*.runtime_adapter.json')) + sorted(base.rglob('*.json'))


def build_runtime_adapter_registry(
    *,
    project_root: str | Path = '.',
    adapter_state_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(project_root)
    adapter_dir = Path(adapter_state_dir)
    out = Path(output_dir)
    groups: dict[str, list[dict[str, Any]]] = {}
    seen: set[str] = set()
    invalid: list[dict[str, str]] = []
    for path in _iter_adapter_files(adapter_dir):
        if str(path) in seen:
            continue
        seen.add(str(path))
        payload = _load_json(path)
        if not payload or payload.get('artifact_type') != 'wallet_structure_gap_runtime_adapter':
            invalid.append({'path': str(path), 'reason': 'invalid_or_non_adapter_json'})
            continue
        adapter_type = payload.get('adapter_type', 'unknown')
        record = {
            'artifact_path': str(path),
            'adapter_type': adapter_type,
            'source_file': payload.get('source_file'),
            'priority': payload.get('priority'),
            'source_exists': payload.get('source_exists'),
            'next_runtime_step': payload.get('next_runtime_step'),
            'automation_policy': payload.get('automation_policy', {}),
        }
        groups.setdefault(adapter_type, []).append(record)
    by_type = {k: len(v) for k, v in sorted(groups.items())}
    registry = {
        'artifact_type': 'wallet_structure_runtime_adapter_registry',
        'generated_at': _utc_now(),
        'project_root': str(root),
        'adapter_state_dir': str(adapter_dir),
        'status': 'PASS' if groups else 'EMPTY',
        'total_adapters': sum(by_type.values()),
        'by_adapter_type': by_type,
        'adapter_groups': groups,
        'invalid_files': invalid,
        'integration_targets': INTEGRATION_TARGETS,
        'automation_policy': {
            'delete_old_files': False,
            'move_old_files': False,
            'readonly_source_files': True,
            'additive_outputs_only': True,
            'paper_only': True,
            'no_private_key': True,
            'no_signing': True,
            'no_broadcast': True,
            'no_swap': True,
        },
    }
    registry_path = _write_json(out / 'runtime_adapter_registry.json', registry)
    registry['registry_path'] = registry_path
    _write_json(out / 'runtime_adapter_registry.json', registry)
    return registry
