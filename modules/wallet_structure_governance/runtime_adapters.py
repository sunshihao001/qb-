#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runtime adapters for applying Wallet-Structure system gap task actions.

These adapters turn document-only gap items into governed runtime artifacts.
They are additive only: no deletion, no move, no trading side effects.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore') if path.exists() else ''


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _safe_name(source_file: str) -> str:
    return source_file.replace('/', '__').replace('.', '_').replace(' ', '_')


def _adapter_type(action: dict[str, Any]) -> str:
    source = action.get('source_file', '')
    capability = action.get('capability', '')
    if 'legacy_compat/path_maps' in source:
        return 'legacy_path_map_runtime_adapter'
    if 'legacy_compat/manifests' in source:
        return 'legacy_manifest_runtime_adapter'
    if 'passports' in source:
        return 'wallet_data_passport_runtime_adapter'
    if capability == 'schema_contract':
        return 'schema_contract_runtime_adapter'
    return 'interface_inventory_runtime_adapter'


def _artifact_dir(root: Path, output_dir: Path, adapter_type: str) -> Path:
    return output_dir / 'runtime_adapters' / adapter_type


def apply_gap_action(project_root: str | Path, action: dict[str, Any], *, output_dir: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    out = Path(output_dir)
    source_file = action['source_file']
    source_path = root / source_file
    text = _read_text(source_path)
    adapter_type = _adapter_type(action)
    payload = {
        'artifact_type': 'wallet_structure_gap_runtime_adapter',
        'adapter_type': adapter_type,
        'generated_at': _utc_now(),
        'source_file': source_file,
        'source_exists': source_path.exists(),
        'source_sha256': _sha256_text(text),
        'priority': action.get('priority'),
        'capability': action.get('capability'),
        'action': action.get('action'),
        'target_module': action.get('target_module'),
        'runtime_contract': {
            'read_mode': 'readonly',
            'write_mode': 'additive_adapter_artifact_only',
            'canonical_route_required': True,
            'must_be_rechecked_by_scanner': True,
        },
        'derived_checks': {
            'line_count': len(text.splitlines()),
            'has_json_shape': source_file.endswith('.json'),
            'has_markdown_shape': source_file.endswith('.md'),
            'mentions_wallet': 'wallet' in text.lower() or '钱包' in text,
            'mentions_path': 'path' in text.lower() or '路径' in text,
            'mentions_contract': 'contract' in text.lower() or '合同' in text,
        },
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
        'next_runtime_step': _next_runtime_step(adapter_type),
    }
    target = _artifact_dir(root, out, adapter_type) / f"{_safe_name(source_file)}.runtime_adapter.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return {
        'status': 'APPLIED',
        'source_file': source_file,
        'priority': action.get('priority'),
        'adapter_type': adapter_type,
        'artifact_path': str(target),
    }


def _next_runtime_step(adapter_type: str) -> dict[str, str]:
    mapping = {
        'interface_inventory_runtime_adapter': ('connect_inventory_adapter_to_system_gap_scanner', 'modules/source_wallet_bot/system_gap_scanner.py'),
        'legacy_path_map_runtime_adapter': ('connect_path_map_to_controlled_read_resolver', 'modules/source_wallet_bot/path_resolver.py'),
        'legacy_manifest_runtime_adapter': ('connect_copy_manifest_to_migration_validator', 'modules/source_wallet_bot/path_resolver.py'),
        'wallet_data_passport_runtime_adapter': ('connect_passport_to_wallet_data_guard_manifest', 'modules/wallet_data_guard/source_manifest.py'),
        'schema_contract_runtime_adapter': ('connect_contract_to_schema_validator', 'modules/source_wallet_bot/schema_validator.py'),
    }
    action, target = mapping.get(adapter_type, ('manual_review', 'research_loop/task_packages/'))
    return {'action': action, 'target': target}
