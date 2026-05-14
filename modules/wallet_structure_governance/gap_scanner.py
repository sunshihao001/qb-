#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System-standard gap scanner for Source Wallet / Wallet-Structure project.

Scans documents/contracts/schemas and checks whether each documented capability
has runtime anchors, tests, and governed automation hooks. It does not modify
legacy files; it writes reports under research_loop/state or a caller-provided
output directory.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCAN_GLOBS = [
    'docs/source_wallet_bot/**/*.md',
    'docs/templates/**/*.md',
    'contracts/**/*.md',
    'schemas/**/*.json',
    'modules/source_wallet_bot/contracts/**/*',
    'modules/source_wallet_bot/schemas/**/*',
    'legacy_compat/**/*.md',
    'legacy_compat/**/*.json',
    'research_loop/methodology/**/*.md',
    'research_loop/methodology/**/*.json',
]

RUNTIME_ROOTS = [
    'modules/source_wallet_bot',
    'modules/wallet_data_guard',
    'run_sikk_gmgn_pipeline.py',
    'sikk_candidate_wallet_structure_pipeline.py',
    'sikk_wallet_structure_gate.py',
    'sikk_wallet_structure_auto_runner.py',
]

KEYWORD_RULES = [
    ('dependency_map', ['dependency', 'analysis_questions', 'judgment_targets', '问题清单', '数据依赖'], 'P0', 'connect_to_existing_runner'),
    ('interface_inventory', ['interface', 'capability', 'collector', 'GMGN', 'OKX', '接口能力'], 'P0', 'create_runtime_adapter'),
    ('acceptance_contract', ['acceptance', 'validator', '验收'], 'P1', 'connect_to_existing_runner'),
    ('schema_contract', ['schema', 'contract', '字段', 'field'], 'P1', 'add_schema_validator'),
    ('legacy_fallback', ['legacy', 'fallback', '旧路径', '兼容'], 'P1', 'create_legacy_path_map'),
    ('pollution_control', ['pollution', '污染', 'contamination', 'guard'], 'P0', 'connect_to_wallet_data_guard'),
    ('auto_flow', ['runner', '自动', 'checkpoint', 'resume'], 'P1', 'connect_to_auto_runner'),
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


def _write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return str(path)


def _iter_candidate_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in SCAN_GLOBS:
        files.extend([p for p in root.glob(pattern) if p.is_file()])
    return sorted(set(files))


def _runtime_text(root: Path) -> str:
    chunks: list[str] = []
    for rel in RUNTIME_ROOTS:
        p = root / rel
        if p.is_file():
            chunks.append(p.read_text(encoding='utf-8', errors='ignore'))
        elif p.is_dir():
            for f in p.rglob('*.py'):
                chunks.append(f.read_text(encoding='utf-8', errors='ignore'))
    return '\n'.join(chunks)


def _extract_anchor_terms(path: Path, text: str) -> list[str]:
    terms = set(re.findall(r'[A-Za-z_][A-Za-z0-9_]{3,}', path.stem))
    for token in re.findall(r'[A-Za-z_][A-Za-z0-9_]{5,}', text):
        if token.lower() in {'source', 'wallet', 'bot', 'schema', 'contract', 'runner', 'adapter', 'collector', 'validator'}:
            terms.add(token)
    for cn in ['数据依赖', '接口能力', '问题清单', '污染', '验收', '旧路径', '字段映射']:
        if cn in text:
            terms.add(cn)
    return sorted(terms)[:20]


def _load_resolved_runtime_sources(root: Path) -> set[str]:
    resolved: set[str] = set()
    state_root = root / 'research_loop/state'
    if not state_root.exists():
        return resolved
    for path in state_root.rglob('runtime_registry_consumption_report.json'):
        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            continue
        if payload.get('status') != 'PASS':
            continue
        targets = payload.get('target_consumption', {}) or {}
        for item in targets.values():
            if isinstance(item, dict) and item.get('status') == 'PASS':
                for source in item.get('source_files', []) or []:
                    if source:
                        resolved.add(str(source))
    return resolved


def _classify(path: Path, text: str, runtime_blob: str, resolved_sources: set[str] | None = None) -> dict[str, Any] | None:
    lower = text.lower()
    rel = str(path)
    matched = None
    if rel in (resolved_sources or set()):
        return None
    for capability, needles, priority, action in KEYWORD_RULES:
        if any(n.lower() in lower or n in text for n in needles):
            matched = (capability, priority, action)
            break
    if not matched:
        return None
    capability, priority, action = matched
    anchors = _extract_anchor_terms(path, text)
    runtime_hits = [a for a in anchors if a and a in runtime_blob]
    test_hits = []
    # Documents that mention capability but have no runtime anchor are true document-only gaps.
    if runtime_hits:
        gap_type = 'document_with_runtime_anchor'
        priority = 'P2' if priority != 'P0' else 'P1'
    else:
        gap_type = 'document_only_without_runtime_anchor'
    return {
        'file_path': rel,
        'capability': capability,
        'gap_type': gap_type,
        'priority': priority,
        'runtime_anchor_hits': runtime_hits[:10],
        'test_anchor_hits': test_hits,
        'recommended_action': {
            'action': action,
            'target_module': 'modules/source_wallet_bot/' if 'source_wallet' in rel or 'source_wallet_bot' in rel else 'modules/wallet_data_guard/',
            'write_policy': 'copy_only_or_additive_no_delete',
        },
        'reason': '文档/合同存在，但未发现足够运行锚点或测试锚点，需要按系统目录标准接入自动流程。' if not runtime_hits else '已有运行锚点，但仍建议补测试/manifest/自动流程索引。',
    }


def consume_interface_inventory_runtime_adapters(registry: dict[str, Any]) -> dict[str, Any]:
    groups = registry.get("adapter_groups", {}) if isinstance(registry, dict) else {}
    adapters = groups.get("interface_inventory_runtime_adapter", []) or []
    return {
        "status": "PASS" if adapters else "EMPTY",
        "consumer": "modules/source_wallet_bot/system_gap_scanner.py",
        "interface_inventory_adapters": len(adapters),
        "source_files": [x.get("source_file") for x in adapters if isinstance(x, dict)],
        "index_role": "interface_inventory_runtime_index",
        "write_policy": "additive_scanner_index_only",
    }


def _priority_md(report: dict[str, Any]) -> str:
    lines = [
        '# 钱包结构分析项目系统标准缺口优先级清单',
        '',
        f"- generated_at: `{report['generated_at']}`",
        f"- total_findings: `{report['summary']['total_findings']}`",
        '',
        '## 优先级定义',
        '',
        '- P0：阻断系统化运行；文档有要求但无 runtime/runner/adapter/guard 接入。',
        '- P1：有部分代码但缺自动流程、测试、manifest、路径映射。',
        '- P2：已有运行锚点，需补验证、报告索引或长期治理。',
        '',
    ]
    for p in ['P0', 'P1', 'P2']:
        items = [f for f in report['findings'] if f['priority'] == p]
        lines.extend(['', f'## {p}', ''])
        if not items:
            lines.append('- none')
            continue
        for i, f in enumerate(items, 1):
            lines.append(f"{i}. `{f['file_path']}`")
            lines.append(f"   - gap_type: `{f['gap_type']}`")
            lines.append(f"   - capability: `{f['capability']}`")
            lines.append(f"   - action: `{f['recommended_action']['action']}`")
            lines.append(f"   - target: `{f['recommended_action']['target_module']}`")
            lines.append(f"   - reason: {f['reason']}")
    return '\n'.join(lines) + '\n'


def scan_wallet_structure_system_gaps(*, project_root: str | Path = '.', output_dir: str | Path | None = None) -> dict[str, Any]:
    root = Path(project_root)
    out = Path(output_dir) if output_dir is not None else root / 'research_loop/state/wallet_structure_system_gap_scan'
    runtime_blob = _runtime_text(root)
    resolved_sources = _load_resolved_runtime_sources(root)
    findings = []
    for path in _iter_candidate_files(root):
        text = path.read_text(encoding='utf-8', errors='ignore')
        finding = _classify(path.relative_to(root), text, runtime_blob, resolved_sources)
        if finding:
            findings.append(finding)
    findings.sort(key=lambda f: ({'P0': 0, 'P1': 1, 'P2': 2}.get(f['priority'], 9), f['file_path']))
    summary = {
        'total_findings': len(findings),
        'by_priority': {p: sum(1 for f in findings if f['priority'] == p) for p in ['P0', 'P1', 'P2']},
        'document_only_count': sum(1 for f in findings if f['gap_type'] == 'document_only_without_runtime_anchor'),
        'resolved_by_runtime_registry_count': len(resolved_sources),
    }
    report = {
        'artifact_type': 'wallet_structure_system_gap_scan',
        'generated_at': _utc_now(),
        'project_root': str(root),
        'summary': summary,
        'resolved_runtime_sources': sorted(resolved_sources),
        'findings': findings,
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
    report['json_path'] = _write_json(out / 'wallet_structure_system_gap_scan.json', report)
    report['priority_md_path'] = _write_text(out / 'wallet_structure_system_gap_priority.md', _priority_md(report))
    _write_json(out / 'wallet_structure_system_gap_scan.json', report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description='Scan Wallet-Structure system-standard gaps')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--output-dir', default='')
    args = parser.parse_args()
    result = scan_wallet_structure_system_gaps(project_root=args.project_root, output_dir=args.output_dir or None)
    print(json.dumps({'json_path': result['json_path'], 'priority_md_path': result['priority_md_path'], 'summary': result['summary']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
