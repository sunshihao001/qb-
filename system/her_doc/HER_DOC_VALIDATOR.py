#!/usr/bin/env python3
"""HER_DOC validator.

Validates the HER_DOC project assets and optionally a scan output bundle.

Exit codes:
 0 = PASS
 1 = FAIL
 2 = BLOCKED / missing required artifacts
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

PROJECT_DIR = Path('/root/sikk-gmgn/system/her_doc')
REQUIRED_CORE_FILES = [
    'HER_DOC_PROJECT_CONSTITUTION.md',
    'HER_DOC_EXECUTION_PROTOCOL.md',
    'HER_DOC_INPUT_TYPE_REGISTRY.yaml',
    'HER_DOC_DOCUMENT_PASSPORT_SCHEMA.yaml',
    'HER_DOC_FUNCTIONAL_OBJECT_SCHEMA.yaml',
    'HER_DOC_SYSTEM_MAPPING_SCHEMA.yaml',
    'HER_DOC_EVIDENCE_REQUIREMENT_SCHEMA.yaml',
    'HER_DOC_PHASE_COMPLETENESS_SCHEMA.yaml',
    'HER_DOC_GPT_RESEARCH_QUEUE_SCHEMA.yaml',
    'HER_DOC_HER_BUILD_QUEUE_SCHEMA.yaml',
    'HER_DOC_RUNTIME_BINDING_REVIEW_SCHEMA.yaml',
    'HER_DOC_LEGACY_ABSORPTION_SCHEMA.yaml',
    'HER_DOC_COMPLETION_STATUS_RULES.md',
    'HER_DOC_OVERCLAIM_GUARD.md',
    'HER_DOC_SAFE_RUNTIME_VERIFICATION.md',
    'HER_DOC_NEXT_FULL_SCAN_UPGRADE_PROMPT.md',
]
REQUIRED_KW = [
    'GPT_RESEARCH_FIRST', 'HER_BUILD_DIRECT', 'RUNTIME_BINDING_REVIEW',
    'E4_SAFE_RUNTIME_PROOF', 'FULL_FLOW_ACCEPTED', 'LEGACY_ABSORPTION',
    'P09', 'P10', 'R00', 'FORBIDDEN_REAL_TRADING'
]


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def check_project() -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    files_checked: List[str] = []

    for rel in REQUIRED_CORE_FILES:
        path = PROJECT_DIR / rel
        if not path.exists():
            issues.append({'type': 'missing_file', 'path': str(path)})
            continue
        text = read_text(path)
        files_checked.append(str(path))
        if len(text.strip()) < 50:
            issues.append({'type': 'too_small', 'path': str(path), 'bytes': len(text)})
        if path.suffix in {'.yaml', '.yml'}:
            if yaml is None:
                issues.append({'type': 'yaml_unavailable', 'path': str(path)})
            else:
                try:
                    data = yaml.safe_load(text)
                    if not isinstance(data, dict):
                        issues.append({'type': 'yaml_not_mapping', 'path': str(path)})
                    if 'schema_id' not in data:
                        issues.append({'type': 'yaml_missing_schema_id', 'path': str(path)})
                except Exception as exc:
                    issues.append({'type': 'yaml_parse_error', 'path': str(path), 'error': str(exc)})

    all_text = '\n'.join(read_text(PROJECT_DIR / rel) for rel in REQUIRED_CORE_FILES if (PROJECT_DIR / rel).exists())
    for kw in REQUIRED_KW:
        if kw not in all_text:
            issues.append({'type': 'missing_keyword', 'keyword': kw})

    skill = Path('/root/.hermes/profiles/sunqbfemxbot/skills/software-development/her-doc/SKILL.md')
    if not skill.exists():
        issues.append({'type': 'missing_skill', 'path': str(skill)})
    else:
        skill_text = read_text(skill)
        if 'validator' not in skill_text.lower():
            issues.append({'type': 'skill_missing_validator_reference', 'path': str(skill)})

    status = 'PASS' if not issues else 'FAIL'
    return {
        'status': status,
        'project_dir': str(PROJECT_DIR),
        'files_checked': files_checked,
        'issue_count': len(issues),
        'issues': issues,
    }


def check_bundle(bundle: Path) -> Dict[str, Any]:
    required = [
        'document_passport_matrix.yaml',
        'functional_object_registry.yaml',
        'system_mapping_matrix.yaml',
        'phase_file_evidence_matrix.yaml',
        'evidence_coverage_report.yaml',
        'runtime_binding_verification_matrix.yaml',
        'legacy_script_absorption_matrix.yaml',
        'legacy_data_replay_matrix.yaml',
        'legacy_research_assetization_matrix.yaml',
        'total_goal_gap_matrix.yaml',
        'phase_goal_gap_matrix.yaml',
        'method_loop_gap_matrix.yaml',
        'gpt_research_queue.yaml',
        'her_build_queue.yaml',
        'r00_runtime_blocker_matrix.yaml',
        'full_trading_system_gap_scan_report.md',
        'next_research_batch_prompt.md',
        'next_her_build_task_packet.md',
    ]
    issues: List[Dict[str, Any]] = []
    checked = []
    for rel in required:
        p = bundle / rel
        checked.append(str(p))
        if not p.exists():
            issues.append({'type': 'missing_output', 'path': str(p)})
            continue
        if p.stat().st_size == 0:
            issues.append({'type': 'empty_output', 'path': str(p)})
    status = 'PASS' if not issues else 'FAIL'
    return {
        'status': status,
        'bundle_dir': str(bundle),
        'files_checked': checked,
        'issue_count': len(issues),
        'issues': issues,
    }


def main(argv: List[str]) -> int:
    mode = 'project'
    target = None
    if len(argv) >= 2:
        mode = argv[1]
    if len(argv) >= 3:
        target = Path(argv[2])

    if mode == 'project':
        result = check_project()
    elif mode == 'bundle':
        if target is None:
            print(json.dumps({'status': 'BLOCKED', 'error': 'bundle mode requires target path'}, indent=2, ensure_ascii=False))
            return 2
        result = check_bundle(target)
    else:
        print(json.dumps({'status': 'BLOCKED', 'error': f'unknown mode: {mode}'}, indent=2, ensure_ascii=False))
        return 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result['status'] == 'PASS':
        return 0
    return 1 if result['status'] == 'FAIL' else 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
