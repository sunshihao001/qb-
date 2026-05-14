#!/usr/bin/env python3
"""
SIKK Stable Trader OS KPP gap scanner and auto task package builder.
Read-only scanner: inventories system documents, phase controllers, contracts, schemas, modules, tests,
then writes KPP-compatible gap reports/task packages under data/knowledge_processing_program/system_rescan/.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path('/root/sikk-gmgn')
OUT = ROOT / 'data/knowledge_processing_program/system_rescan'
SYSTEM_OUT = ROOT / 'system/knowledge_processing_program/system_rescan'

SAFETY_FORBIDDEN = [
    'private_key', 'seed_phrase', 'sign_transaction', 'sendTransaction', 'broadcast_transaction',
    'swap_enabled: true', 'real_trade_enabled: true', 'live_execution_allowed: true',
    'auto_order_allowed: true', 'wallet_signing_allowed: true'
]

CURRENT_PHASES = [
    ('P01', 'p01_candidate_intake_controller', 'source_data_fact'),
    ('P02', 'p02_source_data_fact_controller', 'source_data_fact'),
    ('P03', 'p03_wallet_entity_controller', 'wallet_entity'),
    ('P04', 'p04_chip_structure_controller', 'chip_structure'),
    ('P05', 'p05_evidence_controller', 'evidence'),
    ('P06', 'p06_scenario_recognition_controller', 'scenario_recognition'),
    ('P07', 'p07_strategy_gate_controller', 'strategy_gate'),
    ('P08', 'p08_execution_risk_controller', 'execution_risk'),
    ('P09', 'p09_review_replay_controller', 'review_replay'),
    ('P10', 'p10_self_upgrade_controller', 'self_upgrade'),
]

STANDARD_CONTROLLER_FILES = [
    'controller.yaml', 'context.md', 'input_contract.json', 'output_contract.json',
    'task_tree.yaml', 'acceptance_gate.yaml', 'runner_binding.yaml',
    'state_writeback_policy.yaml', 'handoff_packet.schema.json'
]

@dataclass
class Gap:
    gap_id: str
    severity: str
    phase: str
    area: str
    title: str
    evidence: list[str]
    required_action: str
    target_paths: list[str]
    auto_fixable: bool
    safety_boundary: str = 'OBSERVE_PAPER_ONLY_NO_RUNTIME_TRADING'


def read_text(p: Path, limit: int = 2_000_000) -> str:
    try:
        return p.read_text(encoding='utf-8', errors='ignore')[:limit]
    except Exception:
        return ''


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def classify_file(path: Path) -> dict[str, Any]:
    txt = read_text(path, 200_000)
    suffix = path.suffix.lower()
    is_doc = suffix in {'.md', '.txt', '.rst'}
    is_code = suffix in {'.py', '.js', '.ts', '.sh'}
    is_contract = 'contract' in path.name.lower() or 'contracts' in path.parts
    is_schema = suffix == '.json' and ('schema' in path.name.lower() or 'schemas' in path.parts)
    has_yaml = suffix in {'.yaml', '.yml'}
    return {
        'path': rel(path),
        'suffix': suffix,
        'is_doc': is_doc,
        'is_code': is_code,
        'is_contract': is_contract,
        'is_schema': is_schema,
        'is_yaml': has_yaml,
        'size': path.stat().st_size if path.exists() else 0,
        'has_explanatory_language': bool(re.search(r'说明|目标|原则|职责|边界|Purpose|Overview|Context', txt[:20000], re.I)),
        'has_contract_language': bool(re.search(r'input_contract|output_contract|schema|handoff|acceptance|字段|required|properties', txt[:50000], re.I)),
        'has_runner_language': bool(re.search(r'runner|CLI|python -m|entrypoint|execute|运行|执行入口|tool binding', txt[:50000], re.I)),
        'has_acceptance_language': bool(re.search(r'acceptance|验收|PASS|FAIL|gate|quality_gate|验证', txt[:50000], re.I)),
        'forbidden_hits': [s for s in SAFETY_FORBIDDEN if s in txt],
    }


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    SYSTEM_OUT.mkdir(parents=True, exist_ok=True)

    scan_roots = [
        ROOT / 'sikk_stable_trader_os', ROOT / 'system/phase_controllers',
        ROOT / 'system/knowledge_processing_program', ROOT / 'contracts/stable_trader_os',
        ROOT / 'schemas/stable_trader_os', ROOT / 'modules', ROOT / 'tests', ROOT / 'docs'
    ]
    files = []
    for base in scan_roots:
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and p.stat().st_size < 5_000_000:
                    files.append(classify_file(p))

    gaps: list[Gap] = []
    gid = 1

    # Systemic KPP gap: many old docs not reprocessed.
    docs = [f for f in files if f['is_doc'] and ('sikk_stable_trader_os' in f['path'] or f['path'].startswith('docs/'))]
    kpp_processed_raw = list((ROOT / 'data/knowledge_processing_program/raw_documents').glob('*')) if (ROOT / 'data/knowledge_processing_program/raw_documents').exists() else []
    batch_passports = list((ROOT / 'data/knowledge_processing_program/batch_legacy_reprocess/document_passports').glob('*.json')) if (ROOT / 'data/knowledge_processing_program/batch_legacy_reprocess/document_passports').exists() else []
    processed_count = max(len(kpp_processed_raw), len(batch_passports))
    if len(docs) > processed_count + 10:
        gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'HIGH', 'K00-K08', 'knowledge_processing',
                        '旧系统文档未按 K00-K08 批量重处理',
                        [f'candidate_docs={len(docs)}', f'processed_raw_documents={len(kpp_processed_raw)}', f'batch_reprocess_passports={len(batch_passports)}'],
                        '建立旧文档批量 KPP 重处理任务包，输出 passport/chunks/mapping/candidates/task_packages。',
                        ['data/knowledge_processing_program/system_rescan/task_packages/batch_legacy_document_reprocess_task_package.yaml'], True)); gid += 1

    # Phase controller standard file coverage.
    for phase, dname, domain in CURRENT_PHASES:
        d = ROOT / 'system/phase_controllers' / dname
        missing = [x for x in STANDARD_CONTROLLER_FILES if not (d / x).exists()]
        if missing:
            gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'HIGH', phase, 'phase_controller',
                            f'{phase} 正式 controller 标准资产不完整',
                            [f'controller_dir={rel(d)}', f'missing={missing}'],
                            '按 Phase Controller 标准补齐 controller/context/input/output/task_tree/acceptance/runner/state/handoff 资产。',
                            [rel(d / x) for x in missing], True)); gid += 1

    # Contracts/schemas legacy naming mismatch vs current P03-P10 naming.
    current_contract_dirs = {p.name for p in (ROOT / 'contracts/stable_trader_os').iterdir() if p.is_dir()} if (ROOT / 'contracts/stable_trader_os').exists() else set()
    current_schema_dirs = {p.name for p in (ROOT / 'schemas/stable_trader_os').iterdir() if p.is_dir()} if (ROOT / 'schemas/stable_trader_os').exists() else set()
    needed_contract_dirs = {
        'phase_01_candidate_intake','phase_02_source_data_fact','phase_03_wallet_entity','phase_04_chip_structure',
        'phase_05_evidence','phase_06_scenario_recognition','phase_07_strategy_gate','phase_08_execution_risk',
        'phase_09_review_replay','phase_10_self_upgrade'
    }
    missing_contract_dirs = sorted(needed_contract_dirs - current_contract_dirs)
    if missing_contract_dirs:
        gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'HIGH', 'P01-P10', 'contracts',
                        '合约目录仍混用旧 Phase 命名，当前权威链路缺少同名合约目录',
                        [f'existing={sorted(current_contract_dirs)}', f'missing_current={missing_contract_dirs}'],
                        '生成当前权威 P01-P10 同名 contract wrapper/index，映射 legacy contract，不删除旧目录。',
                        [f'contracts/stable_trader_os/{x}/' for x in missing_contract_dirs], True)); gid += 1
    missing_schema_dirs = sorted(needed_contract_dirs - current_schema_dirs)
    if missing_schema_dirs:
        gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'HIGH', 'P01-P10', 'schemas',
                        'Schema 目录仍混用旧 Phase 命名，当前权威链路缺少同名 schema 目录',
                        [f'existing={sorted(current_schema_dirs)}', f'missing_current={missing_schema_dirs}'],
                        '生成当前权威 P01-P10 同名 schema wrapper/index，映射 legacy schema，不删除旧目录。',
                        [f'schemas/stable_trader_os/{x}/' for x in missing_schema_dirs], True)); gid += 1

    # Runner binding missing actual executable references.
    for phase, dname, domain in CURRENT_PHASES:
        rb = ROOT / 'system/phase_controllers' / dname / 'runner_binding.yaml'
        txt = read_text(rb)
        if rb.exists() and not re.search(r'(python\s+-m|module:|entrypoint|command:|script:)', txt, re.I):
            gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'MEDIUM', phase, 'runner_binding',
                            f'{phase} runner_binding 存在但缺少真实入口绑定',
                            [f'runner_binding={rel(rb)}'],
                            '补充 OBSERVE/PAPER 禁用边界下的 read-only validator/contract-check 入口；业务 runtime 继续 blocked。',
                            [rel(rb)], True)); gid += 1

    # Tests gap: current controller acceptance aggregate.
    test_anchor = ROOT / 'tests/stable_trader_os/test_kpp_system_rescan_acceptance.py'
    if not test_anchor.exists():
        gaps.append(Gap(f'KPP_RESCAN_GAP_{gid:03d}', 'MEDIUM', 'KPP_SYSTEM_RESCAN', 'tests',
                        '缺少 KPP 全系统重扫后的统一验收测试',
                        [f'missing={rel(test_anchor)}'],
                        '创建 pytest 验证问题清单、任务包、合约/schema wrapper、安全边界与自动修复产物。',
                        [rel(test_anchor)], True)); gid += 1

    forbidden_files = [f for f in files if f['forbidden_hits']]
    # Only report explicit enabling terms; current docs may mention forbidden words as boundaries, so include as audit info not gap if no true-enable hits beyond scanner list.

    summary = {
        'scan_id': 'KPP_SYSTEM_RESCAN_20260513',
        'generated_at': ts,
        'root': str(ROOT),
        'status': 'GAPS_FOUND' if gaps else 'PASS',
        'file_count': len(files),
        'doc_count': len(docs),
        'gap_count': len(gaps),
        'auto_fixable_gap_count': sum(1 for g in gaps if g.auto_fixable),
        'safety_boundary': 'OBSERVE_PAPER_ONLY; no signing/broadcast/swap/live trading',
        'forbidden_enable_hits': forbidden_files[:50],
    }

    gaps_dict = [asdict(g) for g in gaps]
    dump_json(OUT / 'inventory/system_rescan_file_inventory.json', {'summary': summary, 'files': files})
    dump_yaml(OUT / 'gaps/system_rescan_gap_registry.yaml', {'summary': summary, 'gaps': gaps_dict})

    task_package = {
        'task_package_id': 'HER-KPP-SYSTEM-RESCAN-AUTOFIX-20260513',
        'status': 'READY_FOR_AUTOMATED_EXECUTION',
        'created_at': ts,
        'goal': '按 K00-K08 Knowledge Processing Program 重扫全系统，补齐 docs-only 阶段的 controller/contract/schema/runner-binding/test/handoff 缺口。',
        'safety_boundaries': [
            'do_not_start_runtime_trading', 'do_not_start_paper_runtime', 'do_not_sign', 'do_not_broadcast',
            'do_not_swap', 'do_not_delete_or_move_legacy_files', 'candidate_or_wrapper_assets_only_until_governance_review'
        ],
        'execution_order': [
            'scan_inventory', 'write_gap_registry', 'generate_current_phase_contract_schema_wrappers',
            'patch_runner_bindings_as_readonly_validators', 'create_kpp_system_rescan_acceptance_test',
            'write_handoff_and_landing_report', 'run_validation'
        ],
        'gaps_to_resolve': gaps_dict,
        'output_roots': {
            'system': rel(SYSTEM_OUT),
            'data': rel(OUT),
        }
    }
    dump_yaml(OUT / 'task_packages/her_kpp_system_rescan_autofix_task_package.yaml', task_package)
    dump_yaml(OUT / 'handoff/kpp_system_rescan_handoff_packet.yaml', {
        'handoff_id': 'KPP_SYSTEM_RESCAN_HANDOFF_20260513',
        'from': 'KNOWLEDGE_PROCESSING_PROGRAM_SYSTEM_RESCAN',
        'to': 'P00_GOVERNANCE_P10_REVIEW_FOR_CONSUMPTION',
        'route_status': 'READY_FOR_AUTOFIX_WITH_GAPS',
        'artifacts': [
            rel(OUT / 'inventory/system_rescan_file_inventory.json'),
            rel(OUT / 'gaps/system_rescan_gap_registry.yaml'),
            rel(OUT / 'task_packages/her_kpp_system_rescan_autofix_task_package.yaml'),
        ],
        'constraints': task_package['safety_boundaries'],
    })
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
