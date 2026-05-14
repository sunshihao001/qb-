#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consume runtime adapter registry through concrete Wallet-Structure runtime targets."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.source_wallet_bot.path_resolver import consume_runtime_adapter_registry as consume_path_registry
from modules.source_wallet_bot.schema_validator import consume_schema_contract_runtime_adapters
from modules.source_wallet_bot.system_gap_scanner import consume_interface_inventory_runtime_adapters
from modules.wallet_data_guard.source_manifest import consume_passport_runtime_adapters


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _load_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise ValueError(f'registry must be json object: {path}')
    return payload


def consume_runtime_registry(*, project_root: str | Path = '.', registry_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    registry = _load_json(registry_path)
    out = Path(output_dir)
    target_consumption = {
        'path_resolver': consume_path_registry(registry),
        'source_manifest': consume_passport_runtime_adapters(registry),
        'schema_validator': consume_schema_contract_runtime_adapters(registry),
        'system_gap_scanner': consume_interface_inventory_runtime_adapters(registry),
    }
    ok = any(item.get('status') == 'PASS' for item in target_consumption.values()) and all(item.get('status') in {'PASS', 'EMPTY'} for item in target_consumption.values())
    report = {
        'artifact_type': 'wallet_structure_runtime_registry_consumption_report',
        'generated_at': _utc_now(),
        'project_root': str(project_root),
        'registry_path': str(registry_path),
        'status': 'PASS' if ok else 'NEEDS_ACTION',
        'target_consumption': target_consumption,
        'automation_policy': {
            'readonly_source_files': True,
            'additive_outputs_only': True,
            'paper_only': True,
            'no_private_key': True,
            'no_signing': True,
            'no_broadcast': True,
            'no_swap': True,
        },
    }
    report_path = _write_json(out / 'runtime_registry_consumption_report.json', report)
    report['report_path'] = report_path
    _write_json(out / 'runtime_registry_consumption_report.json', report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description='Consume Wallet-Structure runtime adapter registry')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--registry-path', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    result = consume_runtime_registry(project_root=args.project_root, registry_path=args.registry_path, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
