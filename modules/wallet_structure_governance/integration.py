#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrate generated runtime adapters into system-readable validation indexes.

This is an additive HER integration layer. It does not mutate legacy source files;
it writes an integration report and registry that existing validators can consume.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.wallet_structure_governance.registry import build_runtime_adapter_registry
from modules.source_wallet_bot.schema_validator import validate_runtime_adapter_registry


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def integrate_runtime_adapters(
    *,
    project_root: str | Path = '.',
    adapter_state_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(project_root)
    out = Path(output_dir)
    registry = build_runtime_adapter_registry(project_root=root, adapter_state_dir=adapter_state_dir, output_dir=out)
    validation = validate_runtime_adapter_registry(registry)
    integration_plan = []
    for adapter_type, target in registry.get('integration_targets', {}).items():
        count = registry.get('by_adapter_type', {}).get(adapter_type, 0)
        if count <= 0:
            continue
        integration_plan.append({
            'adapter_type': adapter_type,
            'adapter_count': count,
            'target': target.get('target'),
            'integration_role': target.get('integration_role'),
            'status': 'READY_FOR_RUNTIME_CONSUMPTION',
            'write_policy': 'additive_index_only',
        })
    report = {
        'artifact_type': 'wallet_structure_runtime_adapter_integration_report',
        'generated_at': _utc_now(),
        'project_root': str(root),
        'status': 'PASS' if validation.get('ok') else 'NEEDS_ACTION',
        'registry_path': registry.get('registry_path'),
        'validation': validation,
        'integration_plan': integration_plan,
        'automation_policy': registry.get('automation_policy', {}),
    }
    report_path = _write_json(out / 'runtime_adapter_integration_report.json', report)
    report['report_path'] = report_path
    _write_json(out / 'runtime_adapter_integration_report.json', report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description='Integrate runtime adapter registry')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--adapter-state-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    result = integrate_runtime_adapters(project_root=args.project_root, adapter_state_dir=args.adapter_state_dir, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
