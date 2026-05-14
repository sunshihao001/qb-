#!/usr/bin/env python3
"""HER_DOC full system rescan for SIKK Stable Trader OS.

Read-only scanner + report generator. It implements HER_DOC_SYSTEM_REVIEW / HER_DOC_SYSTEM_AUDIT
for the uploaded "交易系统体系再摄取与落地审计方案".

Safety: no trading, no signing, no broadcast, no swap, no deletion/move of legacy data.
Writes only reports under /root/sikk-gmgn/reports/system_rescan/.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ROOT = Path('/root/sikk-gmgn')
OUT = ROOT / 'reports/system_rescan'
SCAN_ROOTS = [
    'docs', 'research_loop', 'knowledge', 'reports', 'audits', 'tasks', 'modules', 'scripts', 'tools',
    'system', 'contracts', 'schemas', 'tests', 'data/knowledge_processing_program',
    'data/her_document_function_system', 'data/gmgn_candidates_live_run', 'data/source_wallet_bot',
    'data/intel_bot', 'data/paper_runtime', 'data/runtime_orchestration', 'skills'
]
TEXT_SUFFIXES = {'.md', '.txt', '.yaml', '.yml', '.json', '.py', '.sh', '.csv'}
DOC_SUFFIXES = {'.md', '.txt', '.yaml', '.yml', '.json'}
IMPORTANT_DOC_SUFFIXES = {'.md', '.txt', '.yaml', '.yml', '.json'}
MAX_FILE_SIZE = 3_000_000
FORBIDDEN_ACTIONS = ['private_key', 'seed_phrase', 'signing', 'broadcast', 'swap', 'real_trade', 'auto_order', 'sendTransaction']
PHASES = [f'P{i:02d}' for i in range(1, 11)]
ALL_STAGE_IDS = [f'K{i:02d}' for i in range(0, 9)] + ['P00'] + PHASES + [f'I{i:02d}' for i in range(1, 6)] + ['R00', 'CPO']
CONTROL_PLANES = ['Bootstrap', 'Governance', 'Domain', 'Data', 'Full Control', 'Trace', 'Acceptance', 'Handoff']
LEGACY_MODULE_NAMES = [
    'run_sikk_gmgn_pipeline.py', 'sikk_live_orchestrator.py', 'sikk_gmgn_token_report.py',
    'sikk_paper_live_runner.py', 'sikk_paper_trading_engine.py', 'sikk_quote_security_review.py',
    'sikk_system_audit.py', 'sikk_knowledge_absorption.py', 'sikk_her_task_router.py',
    'sikk_task_package_builder.py', 'sikk_same_source_grouping.py', 'sikk_operator_psychology_engine.py',
]
RUNTIME_OBJECTS = [
    'runtime_plane_context_manifest', 'runtime_readiness_gate', 'runtime_run_manifest', 'token_case_manifest',
    'phase_execution_plan', 'phase_execution_record', 'handoff_resolution_record', 'p08_permission_gate',
    'paper_runtime_invocation_record', 'p09_review_trigger', 'p10_upgrade_review_trigger',
    'operation_metrics_update', 'sample_library_update', 'full_pipeline_plane_aware_report',
]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def read_text(p: Path, limit: int = 400_000) -> str:
    try:
        return p.read_text(encoding='utf-8', errors='ignore')[:limit]
    except Exception:
        return ''


def sha(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return ''


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + '\n', encoding='utf-8')


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    else:
        dump_json(path, data)


def write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + '\n', encoding='utf-8')


def iter_files() -> list[Path]:
    files: list[Path] = []
    for r in SCAN_ROOTS:
        base = ROOT / r
        if not base.exists():
            continue
        for p in base.rglob('*'):
            if not p.is_file():
                continue
            try:
                if p.stat().st_size > MAX_FILE_SIZE:
                    continue
            except Exception:
                continue
            if p.suffix.lower() in TEXT_SUFFIXES or p.name in LEGACY_MODULE_NAMES:
                files.append(p)
    # Add root-level legacy python/docs without making root a write path
    for p in ROOT.glob('*'):
        if p.is_file() and (p.name in LEGACY_MODULE_NAMES or p.suffix.lower() in {'.md', '.py'}):
            files.append(p)
    return sorted(set(files))


def classify_doc(path: Path, text: str) -> tuple[str, str]:
    low_path = rel(path).lower()
    low = text[:80_000].lower()
    if any(x in low_path for x in ['runtime', 'paper_runtime', 'run_summary', 'report']) and path.suffix.lower() in {'.json', '.md'}:
        dtype = 'RUNTIME_REPORT'
    elif any(x in low_path for x in ['phase_controller', 'controller']) or re.search(r'phase\s*controller|controller', low):
        dtype = 'PHASE_CONTROLLER_DOC'
    elif any(x in low_path for x in ['task', 'plan']) or re.search(r'任务|task package|execution_order', low):
        dtype = 'TASK_INSTRUCTION_DOC'
    elif any(x in low_path for x in ['schema', 'contract', 'field']) or re.search(r'properties|required|schema|contract|字段', low):
        dtype = 'FIELD_MODEL_DOC'
    elif re.search(r'methodology|方法论|principle|底层逻辑|constitution|protocol', low):
        dtype = 'METHODOLOGY_DOC'
    elif re.search(r'system design|系统设计|architecture|blueprint|体系|阶段', low):
        dtype = 'SYSTEM_DESIGN_DOC'
    elif re.search(r'upgrade|proposal|gap|缺口|修复', low):
        dtype = 'UPGRADE_PROPOSAL'
    else:
        dtype = 'EXPLANATORY_DOC'
    if dtype in {'PHASE_CONTROLLER_DOC', 'FIELD_MODEL_DOC', 'SYSTEM_DESIGN_DOC', 'METHODOLOGY_DOC'}:
        route = 'FULL_FUNCTIONALIZATION'
    elif dtype in {'TASK_INSTRUCTION_DOC', 'UPGRADE_PROPOSAL'}:
        route = 'TASK_PACKAGE_GENERATION'
    elif dtype == 'RUNTIME_REPORT':
        route = 'PHASE_MAPPING'
    else:
        route = 'REFERENCE_ONLY'
    return dtype, route


def extract_keywords(text: str) -> dict[str, list[str]]:
    patterns = {
        'mechanism': r'(?:机制|原则|rule|gate|controller|orchestrator|runner|pipeline|cache|handoff|trace|acceptance|schema|contract)[^。\n]{0,80}',
        'control_rule': r'(?:必须|不允许|禁止|required|forbidden|must|shall|only|不得)[^。\n]{0,100}',
        'field_candidate': r'[`\"]?([a-zA-Z][a-zA-Z0-9_]{3,60})[`\"]?\s*:',
        'runner_candidate': r'(?:python\s+-m\s+[^\n`]+|python3?\s+[^\n`]+\.py[^\n`]*)',
        'acceptance_candidate': r'(?:验收|acceptance|PASS|FAIL|BLOCK|PASS_WITH_GAPS)[^。\n]{0,100}',
        'handoff_candidate': r'(?:handoff|交接|downstream|upstream)[^。\n]{0,100}',
    }
    out: dict[str, list[str]] = {}
    for k, pat in patterns.items():
        vals = []
        for m in re.finditer(pat, text[:120_000], re.I):
            val = m.group(1) if k == 'field_candidate' and m.groups() else m.group(0)
            val = re.sub(r'\s+', ' ', str(val)).strip()
            if val and val not in vals:
                vals.append(val[:240])
            if len(vals) >= 12:
                break
        out[k] = vals
    return out


def map_layer(path: Path, text: str) -> list[str]:
    s = (rel(path) + '\n' + text[:50_000]).lower()
    layers = []
    for sid in ALL_STAGE_IDS:
        if sid.lower() in s or sid.replace('0', '').lower() in s:
            layers.append(sid)
    if any(x in s for x in ['k00', 'k01', 'k02', 'k03', 'k04', 'k05', 'k06', 'k07', 'k08', 'knowledge processing']):
        layers.append('K00_K08')
    if any(x in s for x in ['control_plane', 'bootstrap', 'governance', 'trace plane', 'acceptance plane', 'handoff plane']):
        layers.append('CONTROL_PLANE')
    if 'r00' in s or 'orchestrator' in s:
        layers.append('R00')
    if 'cpo' in s or 'continuous paper' in s:
        layers.append('CPO')
    if not layers:
        layers.append('UNMAPPED_REFERENCE')
    return sorted(set(layers))


def current_status(path: Path, text: str) -> str:
    rp = rel(path)
    if any(x in rp for x in ['system/phase_controllers', 'contracts/', 'schemas/', 'modules/', 'tools/']) and re.search(r'runner|schema|contract|acceptance|handoff|def |class ', text[:80_000], re.I):
        if any(x in rp for x in ['runtime_entry.py', 'runner', 'orchestrator']) or re.search(r'python -m|entrypoint|run\(', text[:80_000], re.I):
            return 'CONNECTED_TO_RUNTIME'
        return 'FUNCTIONALIZED_NOT_CONNECTED'
    if re.search(r'schema|contract|acceptance|handoff|runner', text[:80_000], re.I):
        return 'PARTIALLY_FUNCTIONALIZED'
    if 'legacy' in rp.lower() or 'old' in rp.lower():
        return 'OBSOLETE'
    return 'DOCUMENT_ONLY'


def stage_slug(stage: str) -> str:
    return stage.lower() + '_standard_stage'


def exists_any(paths: list[Path]) -> str | None:
    for p in paths:
        if p.exists():
            return rel(p)
    return None


def phase_matrix() -> list[dict[str, Any]]:
    rows = []
    names = {
        'P01': 'Candidate Intake', 'P02': 'Data Fact', 'P03': 'Wallet Entity', 'P04': 'Chip Structure',
        'P05': 'Evidence', 'P06': 'Scenario Recognition', 'P07': 'Strategy Gate', 'P08': 'Execution Risk / Permission Gate',
        'P09': 'Review Replay', 'P10': 'Self Upgrade'
    }
    for ph in PHASES:
        slug = stage_slug(ph)
        assets = {
            'controller': exists_any([ROOT / f'system/phase_controllers/{slug}/controller.json', ROOT / f'system/phase_controllers/{ph.lower()}_candidate_intake_controller/controller.yaml']),
            'schema': exists_any([ROOT / f'schemas/stable_trader_os/{slug}/schema.json']),
            'contract': exists_any([ROOT / f'contracts/stable_trader_os/{slug}/contract.json']),
            'runner': exists_any([ROOT / f'modules/stable_trader_os/{slug}/runtime_entry.py']),
            'trace': exists_any([ROOT / f'system/trace_plane/{slug}/trace_packet_template.json']),
            'acceptance': exists_any([ROOT / f'system/acceptance_plane/{slug}/acceptance_gate.json']),
            'handoff': exists_any([ROOT / f'system/handoff_plane/{slug}/handoff_contract.json']),
        }
        missing = [k for k, v in assets.items() if not v]
        runtime_connected = bool(assets['runner'])
        if not missing and runtime_connected:
            gap = 'LOW'  # structural ready, but semantic/runtime binding still needs evidence
        elif len(missing) <= 2:
            gap = 'MEDIUM'
        else:
            gap = 'HIGH'
        rows.append({
            'phase_id': ph,
            'phase_name': names[ph],
            'required_outputs': ['controller', 'schema', 'contract', 'runner', 'trace', 'acceptance', 'handoff', 'runtime_data_output', 'downstream_read'],
            'existing_documents': [v for k, v in assets.items() if k == 'controller' and v],
            'existing_code_modules': [assets['runner']] if assets['runner'] else [],
            'existing_data_outputs': sorted([rel(p) for p in (ROOT / 'data').rglob(f'*{ph.lower()}*') if p.is_file()][:20]) if (ROOT / 'data').exists() else [],
            'schema_exists': bool(assets['schema']),
            'contract_exists': bool(assets['contract']),
            'runner_exists': bool(assets['runner']),
            'trace_exists': bool(assets['trace']),
            'acceptance_exists': bool(assets['acceptance']),
            'handoff_exists': bool(assets['handoff']),
            'runtime_connected': runtime_connected,
            'source_paths': assets,
            'gap_level': gap,
            'professional_judgement': '标准资产基本齐全；仍需用真实 token/paper-only replay 证明业务语义深度' if gap == 'LOW' else '缺标准资产或 runner binding，不能作为完整运行阶段',
        })
    return rows


def control_plane_matrix() -> list[dict[str, Any]]:
    rows = []
    path_map = {
        'Bootstrap': ['system/stable_trader_os', 'system/phase_controllers/k00_standard_stage'],
        'Governance': ['system/her_document_function_system', 'system/stable_trader_os/legacy_control'],
        'Domain': ['docs', 'research_loop/methodology', 'knowledge'],
        'Data': ['data/source_wallet_bot', 'system/phase_controllers/p02_standard_stage'],
        'Full Control': ['system/phase_controllers/r00_standard_stage', 'modules/stable_trader_os/r00_standard_stage'],
        'Trace': ['system/trace_plane'],
        'Acceptance': ['system/acceptance_plane'],
        'Handoff': ['system/handoff_plane'],
    }
    r00_text = ''
    for p in [ROOT / 'modules/stable_trader_os/r00_standard_stage/runtime_entry.py', ROOT / 'system/phase_controllers/r00_standard_stage/controller.json']:
        r00_text += read_text(p, 100_000) + '\n'
    for plane in CONTROL_PLANES:
        sources = []
        for base in path_map.get(plane, []):
            b = ROOT / base
            if b.exists():
                if b.is_file():
                    sources.append(rel(b))
                else:
                    sources.extend([rel(x) for x in list(b.rglob('*'))[:30] if x.is_file()])
        keywords = [plane.lower().split()[0], plane.replace(' ', '_').lower()]
        runtime_read = any(k in r00_text.lower() for k in keywords) or (plane in ['Trace', 'Acceptance', 'Handoff'] and bool(sources))
        rows.append({
            'control_plane': plane,
            'formal_files_exist': bool(sources),
            'source_paths': sources[:30],
            'r00_or_runner_read_evidence': runtime_read,
            'runtime_binding_status': 'BOUND_OR_REFERENCED' if runtime_read else 'DOCUMENTED_NOT_PROVEN_BOUND',
            'gap': None if runtime_read else f'{plane} plane needs explicit R00/runner read contract and trace evidence',
        })
    return rows


def scan_legacy_modules(files: list[Path]) -> list[dict[str, Any]]:
    rows = []
    byname = defaultdict(list)
    for p in files:
        byname[p.name].append(p)
    # include named matches anywhere
    for name in LEGACY_MODULE_NAMES:
        candidates = byname.get(name, []) + list(ROOT.rglob(name))
        seen = set()
        for p in candidates:
            if p in seen or not p.exists() or not p.is_file():
                continue
            seen.add(p)
            txt = read_text(p, 200_000)
            low = (rel(p) + txt[:50_000]).lower()
            target = 'R00'
            if 'paper' in low:
                target = 'CPO' if 'live_runner' in p.name else 'P08'
            elif 'quote' in low or 'security' in low:
                target = 'P02'
            elif 'same_source' in low or 'wallet' in low:
                target = 'P03'
            elif 'psychology' in low or 'scenario' in low:
                target = 'P06'
            elif 'audit' in low or 'review' in low:
                target = 'P09'
            elif 'knowledge' in low or 'task_router' in low or 'task_package' in low:
                target = 'K00_K08'
            detected = []
            for key in ['runner', 'orchestrator', 'paper', 'quote', 'security', 'same_source', 'audit', 'knowledge', 'task_package', 'wallet']:
                if key in low:
                    detected.append(key)
            has_schema = 'schema' in low
            has_contract = 'contract' in low
            has_trace = 'trace' in low or 'log' in low
            has_acceptance = 'acceptance' in low or '验收' in low
            missing = [k for k, ok in [('schema', has_schema), ('contract', has_contract), ('trace', has_trace), ('acceptance', has_acceptance), ('handoff', 'handoff' in low), ('tests', 'pytest' in low or 'test_' in low)] if not ok]
            if 'data/gmgn_candidates_live_run' in rel(p) or p.name.startswith('sikk_paper'):
                action = 'KEEP_AS_LEGACY_READONLY' if 'paper' not in p.name else 'BIND_TO_R00'
            elif target in {'P02', 'P03', 'P06'}:
                action = 'WRAP_AS_ATOMIC_SKILL'
            else:
                action = 'BIND_TO_R00'
            rows.append({
                'module_path': rel(p), 'module_name': p.name, 'current_role': ','.join(detected) or 'unknown_legacy_script',
                'detected_functions': detected, 'target_layer': target, 'absorption_action': action,
                'missing_requirements': missing, 'source_hash': sha(p)[:16]
            })
    return rows


def runtime_gap_matrix(files: list[Path]) -> list[dict[str, Any]]:
    all_paths = [rel(p) for p in files]
    low_paths = [x.lower() for x in all_paths]
    rows = []
    for obj in RUNTIME_OBJECTS:
        parts = obj.lower().split('_')
        matches = [all_paths[i] for i, lp in enumerate(low_paths) if all(part in lp for part in parts[:2]) or obj.lower() in lp]
        exists = bool(matches)
        blocking = obj in {'runtime_plane_context_manifest', 'runtime_readiness_gate', 'runtime_run_manifest', 'token_case_manifest', 'phase_execution_plan', 'handoff_resolution_record', 'p08_permission_gate'} and not exists
        rows.append({
            'required_runtime_object': obj,
            'exists_now': exists,
            'source_if_exists': matches[:10] if exists else None,
            'missing_reason': None if exists else '未发现同名或等价 runtime artifact；可能仅存在于设计文档，尚未形成标准运行对象',
            'blocking_runtime': blocking,
            'fix_task': f'Create {obj}.json schema + writer in R00 paper-only orchestrator; bind source paths and trace evidence; add pytest acceptance.' if not exists else f'Normalize {obj} into canonical R00 manifest index and verify downstream read.',
        })
    return rows


def data_absorption_matrix(files: list[Path]) -> list[dict[str, Any]]:
    roots = ['data/gmgn_candidates_live_run', 'data/source_wallet_bot', 'data/intel_bot', 'data/paper_runtime', 'data/runtime_orchestration', 'data/knowledge_processing_program']
    rows = []
    for r in roots:
        b = ROOT / r
        if not b.exists():
            rows.append({'data_root': r, 'exists': False, 'role': 'missing', 'absorption_policy': 'CREATE_IF_REQUIRED_BY_R00', 'sample_files': []})
            continue
        sample = [rel(p) for p in list(b.rglob('*')) if p.is_file()][:40]
        if 'gmgn_candidates_live_run' in r:
            policy = 'LEGACY_READ_ONLY_OR_REPLAY_SAMPLE_LIBRARY'
        elif 'source_wallet_bot' in r:
            policy = 'CANONICAL_PHASE01_FACT_CACHE'
        elif 'paper_runtime' in r:
            policy = 'PAPER_ONLY_RUNTIME_REVIEW_INPUT'
        else:
            policy = 'SYSTEM_SUPPORTING_DATA_OR_RUNTIME_CANDIDATE'
        rows.append({'data_root': r, 'exists': True, 'file_count_sampled': len(sample), 'role': policy.lower(), 'absorption_policy': policy, 'sample_files': sample})
    return rows


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    files = iter_files()
    passports = []
    func_objects = []
    doc_matrix = []
    type_counts = Counter()
    status_counts = Counter()

    for p in files:
        suffix = p.suffix.lower()
        if suffix not in IMPORTANT_DOC_SUFFIXES:
            continue
        txt = read_text(p)
        if not txt:
            continue
        dtype, route = classify_doc(p, txt)
        layers = map_layer(p, txt)
        status = current_status(p, txt)
        keys = extract_keywords(txt)
        type_counts[dtype] += 1
        status_counts[status] += 1
        passport = {
            'document_id': hashlib.md5(rel(p).encode()).hexdigest()[:12],
            'title': p.stem,
            'path': rel(p),
            'sha256': sha(p),
            'size': p.stat().st_size,
            'document_type': dtype,
            'processing_route': route,
            'mapped_system_layer': layers,
            'current_status': status,
            'source_path': rel(p),
        }
        passports.append(passport)
        required_action = []
        if status == 'DOCUMENT_ONLY' and route != 'REFERENCE_ONLY':
            required_action += ['CREATE_CONTROLLER_CANDIDATE', 'CREATE_SCHEMA', 'CREATE_CONTRACT']
        if 'runner' in ' '.join(keys.get('runner_candidate', [])).lower() or status == 'PARTIALLY_FUNCTIONALIZED':
            required_action.append('CREATE_RUNNER_BINDING')
        if keys.get('acceptance_candidate'):
            required_action.append('CREATE_ACCEPTANCE')
        if keys.get('handoff_candidate'):
            required_action.append('CREATE_HANDOFF')
        if not required_action:
            required_action = ['ARCHIVE_REFERENCE_ONLY'] if route == 'REFERENCE_ONLY' else ['PHASE_MAPPING']
        doc_matrix.append({
            **{k: passport[k] for k in ['document_id', 'title', 'document_type']},
            'source_path': rel(p),
            'extracted_mechanisms': keys.get('mechanism', [])[:8],
            'mapped_system_layer': layers,
            'current_status': status,
            'required_action': sorted(set(required_action)),
        })
        for category in ['mechanism', 'control_rule', 'field_candidate', 'schema_candidate', 'contract_candidate', 'acceptance_candidate', 'handoff_candidate', 'runner_candidate']:
            vals = keys.get(category, [])
            if not vals:
                continue
            for idx, val in enumerate(vals[:10]):
                owner = layers[0] if layers else 'UNMAPPED'
                func_objects.append({
                    'object_id': f"FO_{hashlib.md5((rel(p)+category+str(idx)+val).encode()).hexdigest()[:12]}",
                    'object_type': category.upper(),
                    'source_path': rel(p),
                    'source_document_id': passport['document_id'],
                    'content': val,
                    'owner_layer': owner,
                    'owner_phase': next((x for x in layers if re.match(r'P\d\d', x)), None),
                    'candidate_status': 'CANDIDATE_NEEDS_GOVERNANCE_REVIEW',
                })

    pmat = phase_matrix()
    cmat = control_plane_matrix()
    legacy = scan_legacy_modules(files)
    dmat = data_absorption_matrix(files)
    rgap = runtime_gap_matrix(files)

    mapping = []
    for fo in func_objects:
        mapping.append({
            'object_id': fo['object_id'],
            'object_type': fo['object_type'],
            'source_path': fo['source_path'],
            'mapped_to': {
                'K00_K08': 'K00_K08' in fo['owner_layer'] or str(fo['owner_layer']).startswith('K'),
                'P00_P10': fo['owner_phase'] or ('P00' if fo['owner_layer'] == 'P00' else None),
                'control_plane': 'CONTROL_PLANE' if fo['owner_layer'] == 'CONTROL_PLANE' else None,
                'I01_I05': fo['owner_layer'] if str(fo['owner_layer']).startswith('I') else None,
                'R00': fo['owner_layer'] == 'R00',
                'CPO': fo['owner_layer'] == 'CPO',
            },
            'mapping_confidence': 'HIGH' if fo.get('owner_phase') else 'MEDIUM',
        })

    summary = {
        'scan_id': 'HER_DOC_SIKK_FULL_SYSTEM_RESCAN',
        'generated_at': ts,
        'root': str(ROOT),
        'output_dir': rel(OUT),
        'file_count_scanned': len(files),
        'document_passport_count': len(passports),
        'functional_object_count': len(func_objects),
        'document_type_counts': dict(type_counts),
        'document_status_counts': dict(status_counts),
        'phase_gap_counts': dict(Counter(r['gap_level'] for r in pmat)),
        'runtime_blocking_gap_count': sum(1 for r in rgap if r['blocking_runtime']),
        'safety_boundary': 'READ_ONLY_RESCAN; no deletion; no legacy move; no real trading; no private keys; no signing; no broadcast; no swap; no auto order',
        'overall_status': 'R00_REQUIRED_WITH_PAPER_ONLY_GAPS' if any(r['blocking_runtime'] for r in rgap) else 'STRUCTURAL_RESCAN_PASS_WITH_SEMANTIC_GAPS',
    }

    dump_yaml(OUT / 'document_passport_index.yaml', {'summary': summary, 'documents': passports})
    dump_yaml(OUT / 'document_functionalization_matrix.yaml', {'summary': summary, 'matrix': doc_matrix})
    dump_yaml(OUT / 'functional_object_registry.yaml', {'summary': summary, 'functional_objects': func_objects})
    dump_yaml(OUT / 'system_mapping_matrix.yaml', {'summary': summary, 'mappings': mapping})
    dump_yaml(OUT / 'phase_implementation_matrix.yaml', {'summary': summary, 'phases': pmat})
    dump_yaml(OUT / 'control_plane_runtime_binding_matrix.yaml', {'summary': summary, 'control_planes': cmat})
    dump_yaml(OUT / 'legacy_module_absorption_matrix.yaml', {'summary': summary, 'legacy_modules': legacy})
    dump_yaml(OUT / 'runtime_data_absorption_matrix.yaml', {'summary': summary, 'runtime_data_roots': dmat})
    dump_yaml(OUT / 'token_runtime_gap_matrix.yaml', {'summary': summary, 'runtime_objects': rgap})

    # R00 fix packet
    blocking = [r for r in rgap if r['blocking_runtime']]
    r00_md = ['# R00 Required Fix Task Packet', '', f'Generated: {ts}', '', '## Safety Boundary', '- paper-only only', '- no private key / signing / broadcast / swap / real trade / auto order', '- legacy data read-only; no move/delete', '', '## Blocking Runtime Objects']
    for r in blocking:
        r00_md += [f"- {r['required_runtime_object']}: {r['fix_task']}"]
    r00_md += ['', '## Files to Create / Normalize', '```text']
    for r in rgap:
        if not r['exists_now']:
            r00_md.append(f"schemas/stable_trader_os/r00_runtime/{r['required_runtime_object']}.schema.json")
            r00_md.append(f"contracts/stable_trader_os/r00_runtime/{r['required_runtime_object']}.contract.json")
    r00_md += ['modules/stable_trader_os/r00_plane_aware_runtime_orchestrator.py', 'tests/stable_trader_os/test_r00_plane_aware_runtime_objects.py', '```', '', '## Single Token Dry-run Acceptance Command', '```bash', 'cd /root/sikk-gmgn', 'PYTHONPATH=/root/sikk-gmgn pytest -q tests/stable_trader_os/test_r00_plane_aware_runtime_objects.py', 'python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --token <TOKEN> --dry-run', '```', '', '## Batch Paper-only Acceptance Command', '```bash', 'python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --batch-candidates --limit 10 --dry-run', '```', '', '## Scheduled Paper Cycle Acceptance Command', '```bash', 'python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --scheduled-cycle --dry-run', '```', '', '## Hard Negative Rules', '- Any attempt to access private keys = FAIL', '- Any signing/broadcast/swap/real_trade flag true = FAIL', '- Missing handoff_resolution_record = BLOCK', '- Missing p08_permission_gate = BLOCK', '- Legacy runtime path used as new primary write root = FAIL', '', '## Acceptance Criteria', '- All runtime objects are written with source_path and trace_id', '- R00 reads control planes before phase execution', '- P01-P10 phase records are linked by handoff IDs', '- P08 permission gate blocks real execution and only permits paper-only invocation', '- P09/P10 triggers exist as review/update candidates, not auto-upgrades']
    write_md(OUT / 'r00_required_fix_task_packet.md', '\n'.join(r00_md))

    next72 = f'''# Next 72h Execution Plan

Generated: {ts}

## Day 1: R00 Runtime Object Closure
- Create canonical schemas/contracts for missing R00 runtime objects.
- Implement paper-only writer for runtime_plane_context_manifest, runtime_readiness_gate, runtime_run_manifest, token_case_manifest, phase_execution_plan, phase_execution_record.
- Add tests proving forbidden actions remain false.

## Day 2: Handoff + P08/P09/P10 Binding
- Bind P01-P10 standard stage outputs into handoff_resolution_record.
- Create p08_permission_gate that blocks real execution and permits paper-only invocation only.
- Create p09_review_trigger and p10_upgrade_review_trigger as candidate-only review records.

## Day 3: Real Token Dry-run + Batch Paper-only Replay
- Run one token through paper-only R00 dry-run.
- Run 10-candidate batch paper-only dry-run.
- Verify operation_metrics_update and sample_library_update.
- Produce full_pipeline_plane_aware_report and acceptance evidence.

## Non-negotiable Boundaries
- No real trading.
- No private keys.
- No signing/broadcast/swap.
- No legacy data move/delete.
- No treating explanatory docs as implemented functions.
'''
    write_md(OUT / 'next_72h_execution_plan.md', next72)

    full_report = f'''# SIKK Full System Rescan Report

Generated: {ts}

## 1. Executive Judgement
当前系统不是“没有设计”，而是已经有较强设计层、标准阶段骨架和部分业务绑定痕迹；但要达到轻量机构水准，仍必须把 HER_DOC / KPP 产生的知识对象统一落成 R00 可运行对象、强制 handoff、trace、acceptance 和 paper-only runtime evidence。

Overall status: `{summary['overall_status']}`

## 2. Scan Scope
- Scanned files: {len(files)}
- Document passports: {len(passports)}
- Functional objects extracted: {len(func_objects)}
- Legacy modules identified: {len(legacy)}
- Blocking runtime gaps: {summary['runtime_blocking_gap_count']}

## 3. HER_DOC Interpretation
- `HER_DOC_PIPELINE`: 文档到功能对象的主流程已可审计，输出 document_passport / functional_object / mapping。
- `HER_DOC_SYSTEM_AUDIT`: 本次已检查缺文件、缺阶段定义、缺 runtime objects、缺旧模块吸收策略。
- `HER_DOC_SYSTEM_REVIEW`: 当前应先补 R00 runtime object 与 handoff/permission/review trigger，再启动真实 token 的 paper-only 全链路。

## 4. Why True Token Full Runtime Cannot Yet Be Declared Complete
真实 token 不能被声明为完整跑通，不是因为缺理论，而是因为以下对象需要标准化并由 R00 硬读取：

{chr(10).join('- ' + r['required_runtime_object'] + ': ' + ('exists' if r['exists_now'] else 'missing/blocking=' + str(r['blocking_runtime'])) for r in rgap)}

## 5. Phase Implementation Summary
{chr(10).join('- ' + r['phase_id'] + ' ' + r['phase_name'] + ': ' + r['gap_level'] + '; runner=' + str(r['runner_exists']) + '; handoff=' + str(r['handoff_exists']) for r in pmat)}

## 6. Control Plane Summary
{chr(10).join('- ' + r['control_plane'] + ': ' + r['runtime_binding_status'] for r in cmat)}

## 7. Legacy Absorption Summary
旧脚本不是废弃资产，统一进入 legacy_module_absorption_matrix；原则是 read-only / wrap / bind，不移动不删除。

## 8. Required Next Action
执行 `r00_required_fix_task_packet.md`，目标不是扩理论，而是补齐：runtime manifest、readiness gate、token case manifest、phase execution records、handoff resolution、P08 permission gate、paper invocation record、P09/P10 triggers、metrics/sample update、full report。

## 9. Output Files
- document_passport_index.yaml
- document_functionalization_matrix.yaml
- functional_object_registry.yaml
- system_mapping_matrix.yaml
- phase_implementation_matrix.yaml
- control_plane_runtime_binding_matrix.yaml
- legacy_module_absorption_matrix.yaml
- runtime_data_absorption_matrix.yaml
- token_runtime_gap_matrix.yaml
- r00_required_fix_task_packet.md
- next_72h_execution_plan.md
'''
    write_md(OUT / 'sikk_full_system_rescan_report.md', full_report)
    dump_json(OUT / 'run_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
