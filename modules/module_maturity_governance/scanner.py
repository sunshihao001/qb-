#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module maturity scanner for Wallet Structure Governance.

Classifies important SIKK wallet-structure capabilities into:
- L1: functional code exists
- L2: runtime integrated / runner or tests exist
- L3: standalone submodule with public API / README / tests
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CAPABILITY_CATALOG = [
    {
        'capability': 'wallet_structure_governance',
        'label': '钱包结构治理',
        'module_dir': 'modules/wallet_structure_governance',
        'functional_anchors': ['modules/wallet_structure_governance/cycle.py'],
        'runtime_anchors': ['modules/wallet_structure_governance/integration.py', 'modules/wallet_structure_governance/consumption.py'],
        'test_globs': ['tests/test_wallet_structure_governance_submodule.py', 'tests/test_wallet_structure_module_maturity_scanner.py'],
        'desired_module': 'modules/wallet_structure_governance',
        'importance': 'P0',
    },
    {
        'capability': 'wallet_data_guard',
        'label': '钱包数据防污染',
        'module_dir': 'modules/wallet_data_guard',
        'functional_anchors': ['modules/wallet_data_guard/write_gate.py', 'modules/wallet_data_guard/source_manifest.py'],
        'runtime_anchors': ['sikk_candidate_wallet_structure_pipeline.py', 'modules/source_wallet_bot/gmgn_live_adapter.py'],
        'test_globs': ['tests/test_wallet_data_guard.py'],
        'desired_module': 'modules/wallet_data_guard',
        'importance': 'P0',
    },
    {
        'capability': 'auto_runner',
        'label': '钱包结构自动运行器',
        'module_dir': 'modules/wallet_structure_auto_runner',
        'functional_anchors': ['sikk_wallet_structure_auto_runner.py'],
        'runtime_anchors': ['sikk_wallet_structure_auto_runner.py'],
        'test_globs': ['tests/test_sikk_wallet_structure_auto_runner.py'],
        'desired_module': 'modules/wallet_structure_auto_runner',
        'importance': 'P0',
    },
    {
        'capability': 'system_audit',
        'label': '系统运行能力审计',
        'module_dir': 'modules/wallet_structure_audit',
        'functional_anchors': ['sikk_wallet_structure_system_audit.py'],
        'runtime_anchors': ['sikk_wallet_structure_auto_runner.py::run_system_audit', 'sikk_wallet_structure_auto_runner.py::sikk_wallet_structure_system_audit'],
        'test_globs': ['tests/test_sikk_wallet_structure_auto_runner.py'],
        'desired_module': 'modules/wallet_structure_audit',
        'importance': 'P0',
    },
    {
        'capability': 'path_resolver',
        'label': '受控路径解析',
        'module_dir': 'modules/wallet_path_resolver',
        'functional_anchors': ['modules/source_wallet_bot/path_resolver.py'],
        'runtime_anchors': ['modules/source_wallet_bot/path_resolver.py'],
        'test_globs': ['tests/test_source_wallet_path_resolver.py'],
        'desired_module': 'modules/wallet_path_resolver',
        'importance': 'P1',
    },
    {
        'capability': 'schema_validator',
        'label': '钱包结构 schema/contract 校验',
        'module_dir': 'modules/wallet_schema_validator',
        'functional_anchors': ['modules/source_wallet_bot/schema_validator.py'],
        'runtime_anchors': ['modules/source_wallet_bot/schema_validator.py'],
        'test_globs': ['tests/test_source_wallet_schema_validator.py'],
        'desired_module': 'modules/wallet_schema_validator',
        'importance': 'P1',
    },
    {
        'capability': 'gmgn_live_adapter',
        'label': 'GMGN 只读采集适配',
        'module_dir': 'modules/wallet_collectors',
        'functional_anchors': ['modules/source_wallet_bot/gmgn_live_adapter.py'],
        'runtime_anchors': ['sikk_candidate_wallet_structure_pipeline.py', 'modules/source_wallet_bot/gmgn_live_adapter.py'],
        'test_globs': ['tests/test_source_wallet_gmgn_live_adapter.py'],
        'desired_module': 'modules/wallet_collectors',
        'importance': 'P1',
    },
    {
        'capability': 'candidate_wallet_pipeline',
        'label': '候选币钱包结构 pipeline',
        'module_dir': 'modules/wallet_structure_pipeline',
        'functional_anchors': ['sikk_candidate_wallet_structure_pipeline.py'],
        'runtime_anchors': ['sikk_candidate_wallet_structure_pipeline.py'],
        'test_globs': ['tests/test_sikk_candidate_wallet_structure_pipeline.py'],
        'desired_module': 'modules/wallet_structure_pipeline',
        'importance': 'P1',
    },
    {
        'capability': 'wallet_structure_gate',
        'label': '钱包结构 gate',
        'module_dir': 'modules/wallet_structure_gate',
        'functional_anchors': ['sikk_wallet_structure_gate.py'],
        'runtime_anchors': ['sikk_wallet_structure_gate.py'],
        'test_globs': ['tests/test_sikk_wallet_structure_gate.py'],
        'desired_module': 'modules/wallet_structure_gate',
        'importance': 'P1',
    },
    {
        'capability': 'same_source_grouping',
        'label': '同源钱包分组',
        'module_dir': 'modules/wallet_same_source_grouping',
        'functional_anchors': ['sikk_same_source_grouping.py'],
        'runtime_anchors': ['sikk_same_source_grouping.py'],
        'test_globs': ['tests/test_sikk_same_source_grouping.py'],
        'desired_module': 'modules/wallet_same_source_grouping',
        'importance': 'P1',
    },
    {
        'capability': 'chip_control_state_machine',
        'label': '筹码控制状态机',
        'module_dir': 'modules/wallet_chip_control',
        'functional_anchors': ['sikk_chip_control_state_machine.py'],
        'runtime_anchors': ['sikk_chip_control_state_machine.py'],
        'test_globs': ['tests/test_sikk_chip_control_state_machine.py'],
        'desired_module': 'modules/wallet_chip_control',
        'importance': 'P2',
    },
    {
        'capability': 'candidate_state_machine',
        'label': '候选币状态机',
        'module_dir': 'modules/wallet_candidate_state_machine',
        'functional_anchors': ['sikk_candidate_state_machine.py'],
        'runtime_anchors': ['sikk_live_run.py'],
        'test_globs': ['tests/test_sikk_candidate_state_machine.py'],
        'desired_module': 'modules/wallet_candidate_state_machine',
        'importance': 'P2',
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _exists(root: Path, rel: str) -> bool:
    if '::' in rel:
        path_part, token = rel.split('::', 1)
        path = root / path_part
        return path.exists() and token in path.read_text(encoding='utf-8', errors='ignore')
    return (root / rel).exists()


def _any_exists(root: Path, rels: list[str]) -> bool:
    return any(_exists(root, rel) for rel in rels)


def _has_tests(root: Path, globs: list[str]) -> bool:
    return any((root / pattern).exists() for pattern in globs)


def _classify(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    module_dir = root / spec['module_dir']
    has_module_dir = module_dir.exists() and (module_dir / '__init__.py').exists()
    has_readme = (module_dir / 'README.md').exists()
    has_functional = _any_exists(root, spec['functional_anchors'])
    has_runtime = _any_exists(root, spec['runtime_anchors'])
    has_tests = _has_tests(root, spec['test_globs'])
    public_api = has_module_dir

    if has_module_dir and has_readme and has_tests:
        level = 'L3'
        status = 'OK'
    elif has_functional and has_runtime:
        level = 'L2'
        status = 'PROMOTE_TO_SUBMODULE'
    elif has_functional:
        level = 'L1'
        status = 'NEEDS_RUNTIME_INTEGRATION_AND_SUBMODULE'
    else:
        level = 'L0'
        status = 'MISSING_OR_UNDETECTED'

    if level in {'L0', 'L1'}:
        priority = spec['importance']
    elif level == 'L2':
        priority = spec['importance'] if spec['importance'] == 'P0' else 'P2'
    else:
        priority = 'DONE'

    missing = []
    if not has_module_dir:
        missing.append('standalone_module_dir')
    if not has_readme:
        missing.append('README.md')
    if not public_api:
        missing.append('__init__.py_public_api')
    if not has_tests:
        missing.append('dedicated_tests')
    if not has_runtime:
        missing.append('runtime_anchor')

    return {
        'capability': spec['capability'],
        'label': spec['label'],
        'maturity_level': level,
        'status': status,
        'priority': priority,
        'desired_module': spec['desired_module'],
        'current_anchors': {
            'has_module_dir': has_module_dir,
            'has_readme': has_readme,
            'has_functional_code': has_functional,
            'has_runtime_anchor': has_runtime,
            'has_tests': has_tests,
        },
        'missing_for_L3': missing,
        'recommended_action': _recommended_action(level, spec),
    }


def _recommended_action(level: str, spec: dict[str, Any]) -> dict[str, Any]:
    if level == 'L3':
        action = 'keep_as_standalone_submodule'
    elif level == 'L2':
        action = 'promote_runtime_integrated_capability_to_submodule'
    elif level == 'L1':
        action = 'add_runtime_integration_then_promote_to_submodule'
    else:
        action = 'discover_or_create_capability'
    return {
        'action': action,
        'target_module': spec['desired_module'],
        'safe_mode': 'paper_only_readonly_additive',
        'wrapper_required': True,
        'test_first': True,
    }


def _priority_key(item: dict[str, Any]) -> tuple[int, int, str]:
    p_rank = {'P0': 0, 'P1': 1, 'P2': 2, 'DONE': 9}.get(item['priority'], 8)
    l_rank = {'L0': 0, 'L1': 1, 'L2': 2, 'L3': 3}.get(item['maturity_level'], 9)
    return (p_rank, l_rank, item['capability'])


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _priority_md(report: dict[str, Any]) -> str:
    lines = [
        '# 钱包结构模块成熟化扫描',
        '',
        f"- generated_at: `{report['generated_at']}`",
        f"- total_capabilities: `{report['summary']['total_capabilities']}`",
        f"- L3: `{report['summary']['by_level'].get('L3', 0)}`",
        f"- L2: `{report['summary']['by_level'].get('L2', 0)}`",
        f"- L1: `{report['summary']['by_level'].get('L1', 0)}`",
        f"- L0: `{report['summary']['by_level'].get('L0', 0)}`",
        '',
        '## 按优先级需要补全',
        '',
    ]
    for item in report['prioritized_gaps']:
        lines.append(f"- {item['priority']} / {item['maturity_level']} `{item['capability']}` — {item['label']}")
        lines.append(f"  - target_module: `{item['desired_module']}`")
        lines.append(f"  - action: `{item['recommended_action']['action']}`")
        lines.append(f"  - missing: `{', '.join(item['missing_for_L3']) or 'none'}`")
    return '\n'.join(lines) + '\n'


def build_maturity_design_contract() -> dict[str, Any]:
    return {
        'artifact_type': 'module_maturity_design_contract',
        'version': '1.0',
        'purpose': 'promote important runtime capabilities from scattered functional code to standalone callable submodules',
        'maturity_levels': {
            'L0': 'missing_or_undetected',
            'L1': 'functional_code_exists',
            'L2': 'runtime_integrated',
            'L3': 'standalone_submodule',
        },
        'promotion_gate': {
            'requires_module_dir': True,
            'requires_public_api': True,
            'requires_readme': True,
            'requires_tests': True,
            'requires_verification': True,
            'requires_backward_compatible_wrappers': True,
        },
        'system_design_role': 'HER bottom-level modular maturity governance: function done is not equal to module maturity',
        'safety': {
            'readonly_source_files': True,
            'additive_outputs_only': True,
            'paper_only': True,
            'no_private_key': True,
            'no_signing': True,
            'no_broadcast': True,
            'no_swap': True,
        },
    }


def write_maturity_design_contract(output_dir: str | Path) -> str:
    out = Path(output_dir)
    contract = build_maturity_design_contract()
    return _write_json(out / 'module_maturity_design_contract.json', contract)


def evaluate_capability_maturity(project_root: str | Path, capability_spec: dict[str, Any]) -> dict[str, Any]:
    return _classify(Path(project_root), capability_spec)


def scan_module_maturity(*, project_root: str | Path = '.', output_dir: str | Path | None = None) -> dict[str, Any]:
    root = Path(project_root)
    capabilities = sorted([_classify(root, spec) for spec in CAPABILITY_CATALOG], key=_priority_key)
    by_level: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    for item in capabilities:
        by_level[item['maturity_level']] = by_level.get(item['maturity_level'], 0) + 1
        by_priority[item['priority']] = by_priority.get(item['priority'], 0) + 1
    prioritized_gaps = [item for item in capabilities if item['maturity_level'] != 'L3']
    report = {
        'artifact_type': 'wallet_structure_module_maturity_scan',
        'generated_at': _utc_now(),
        'project_root': str(root),
        'summary': {
            'total_capabilities': len(capabilities),
            'by_level': by_level,
            'by_priority': by_priority,
            'needs_promotion_count': len(prioritized_gaps),
            'standalone_submodule_count': by_level.get('L3', 0),
        },
        'capabilities': capabilities,
        'prioritized_gaps': prioritized_gaps,
        'automation_policy': {
            'readonly_source_files': True,
            'additive_outputs_only': True,
            'paper_only': True,
            'no_private_key': True,
            'no_signing': True,
            'no_broadcast': True,
            'no_swap': True,
        },
        'design_contract': build_maturity_design_contract(),
    }
    if output_dir:
        out = Path(output_dir)
        report['json_path'] = _write_json(out / 'module_maturity_scan.json', report)
        report['priority_md_path'] = str(out / 'module_maturity_priority.md')
        report['design_contract_path'] = write_maturity_design_contract(out)
        (out / 'module_maturity_priority.md').parent.mkdir(parents=True, exist_ok=True)
        (out / 'module_maturity_priority.md').write_text(_priority_md(report), encoding='utf-8')
        _write_json(out / 'module_maturity_scan.json', report)
    return report
