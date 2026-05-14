#!/usr/bin/env python3
"""Apply KPP system-rescan autofix package.

This script creates missing standard phase-controller wrapper assets, current phase
contract/schema wrappers, read-only runner validators, tests, and handoff reports.
It does not move/delete legacy files and does not enable paper/live trading.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ROOT = Path('/root/sikk-gmgn')
OUT = ROOT / 'data/knowledge_processing_program/system_rescan'
SYS = ROOT / 'system/knowledge_processing_program/system_rescan'

PHASES = [
    {'phase_id':'P01','controller_dir':'p01_candidate_intake_controller','slug':'phase_01_candidate_intake','name':'Candidate Intake','domain':'candidate_intake','upstream':['K00_KNOWLEDGE_INTAKE','P00_SYSTEM_BOOTSTRAP'],'downstream':['P02_SOURCE_DATA_FACT_CONTROLLER']},
    {'phase_id':'P02','controller_dir':'p02_source_data_fact_controller','slug':'phase_02_source_data_fact','name':'Source Data Fact','domain':'source_data_fact','upstream':['P01_CANDIDATE_INTAKE_CONTROLLER'],'downstream':['P03_WALLET_ENTITY_CONTROLLER']},
    {'phase_id':'P03','controller_dir':'p03_wallet_entity_controller','slug':'phase_03_wallet_entity','name':'Wallet Entity','domain':'wallet_entity','upstream':['P02_SOURCE_DATA_FACT_CONTROLLER'],'downstream':['P04_CHIP_STRUCTURE_CONTROLLER']},
    {'phase_id':'P04','controller_dir':'p04_chip_structure_controller','slug':'phase_04_chip_structure','name':'Chip Structure','domain':'chip_structure','upstream':['P03_WALLET_ENTITY_CONTROLLER'],'downstream':['P05_EVIDENCE_CONTROLLER']},
    {'phase_id':'P05','controller_dir':'p05_evidence_controller','slug':'phase_05_evidence','name':'Evidence','domain':'evidence','upstream':['P04_CHIP_STRUCTURE_CONTROLLER'],'downstream':['P06_SCENARIO_RECOGNITION_CONTROLLER']},
    {'phase_id':'P06','controller_dir':'p06_scenario_recognition_controller','slug':'phase_06_scenario_recognition','name':'Scenario Recognition','domain':'scenario_recognition','upstream':['P05_EVIDENCE_CONTROLLER'],'downstream':['P07_STRATEGY_GATE_CONTROLLER']},
    {'phase_id':'P07','controller_dir':'p07_strategy_gate_controller','slug':'phase_07_strategy_gate','name':'Strategy Gate','domain':'strategy_gate','upstream':['P06_SCENARIO_RECOGNITION_CONTROLLER'],'downstream':['P08_EXECUTION_RISK_CONTROLLER']},
    {'phase_id':'P08','controller_dir':'p08_execution_risk_controller','slug':'phase_08_execution_risk','name':'Execution Risk','domain':'execution_risk','upstream':['P07_STRATEGY_GATE_CONTROLLER'],'downstream':['P09_REVIEW_REPLAY_CONTROLLER']},
    {'phase_id':'P09','controller_dir':'p09_review_replay_controller','slug':'phase_09_review_replay','name':'Review Replay','domain':'review_replay','upstream':['P08_EXECUTION_RISK_CONTROLLER'],'downstream':['P10_SELF_UPGRADE_CONTROLLER']},
    {'phase_id':'P10','controller_dir':'p10_self_upgrade_controller','slug':'phase_10_self_upgrade','name':'Self Upgrade','domain':'self_upgrade','upstream':['P09_REVIEW_REPLAY_CONTROLLER'],'downstream':['GOVERNANCE_REVIEW','IMPLEMENTATION_TASK_QUEUE']},
]

LEGACY_MAP = {
    'phase_01_candidate_intake': 'phase_01_data_fact',
    'phase_02_source_data_fact': 'phase_01_data_fact',
    'phase_03_wallet_entity': 'phase_02_wallet_structure',
    'phase_04_chip_structure': 'phase_03_chip_control',
    'phase_05_evidence': 'phase_05_structure_position',
    'phase_06_scenario_recognition': 'phase_04_scenario_recognition',
    'phase_07_strategy_gate': 'phase_06_strategy_filter',
    'phase_08_execution_risk': 'phase_07_execution_risk',
    'phase_09_review_replay': 'phase_08_review_learning',
    'phase_10_self_upgrade': 'phase_09_system_upgrade',
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def write_json(path: Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def write_yaml(path: Path, obj: Any) -> None:
    if yaml:
        write_text(path, yaml.safe_dump(obj, allow_unicode=True, sort_keys=False))
    else:
        write_json(path, obj)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def schema_for(phase: dict[str, Any], direction: str) -> dict[str, Any]:
    required = ['packet_id','phase_id','domain','status','created_at','evidence_refs','quality_gates','safety_boundary']
    return {
        '$schema':'https://json-schema.org/draft/2020-12/schema',
        '$id':f'sikk://stable_trader_os/{phase["slug"]}/{direction}_contract.schema.json',
        'title':f'{phase["phase_id"]} {phase["name"]} {direction} contract',
        'type':'object',
        'additionalProperties': True,
        'required': required,
        'properties': {
            'packet_id': {'type':'string'},
            'phase_id': {'const': phase['phase_id']},
            'domain': {'const': phase['domain']},
            'status': {'type':'string', 'enum':['READY','READY_WITH_GAPS','BLOCKED','REJECTED','CANDIDATE_ONLY','OBSERVE_ONLY']},
            'created_at': {'type':'string'},
            'upstream_packets': {'type':'array','items':{'type':'string'}},
            'downstream_allowed': {'type':'array','items':{'type':'string'}},
            'evidence_refs': {'type':'array','items':{'type':'string'}},
            'quality_gates': {'type':'array','items':{'type':'object'}},
            'missing_fields': {'type':'array','items':{'type':'string'}},
            'downgrade_reason': {'type':'string'},
            'safety_boundary': {'type':'object','required':['real_trade_enabled','signing_enabled','broadcast_enabled','swap_enabled'], 'properties':{
                'real_trade_enabled': {'const': False},
                'signing_enabled': {'const': False},
                'broadcast_enabled': {'const': False},
                'swap_enabled': {'const': False},
                'runtime_mode': {'enum':['OBSERVE_ONLY','PAPER_ONLY','OBSERVE_PAPER_ONLY']},
            }},
        }
    }


def create_controller_assets(phase: dict[str, Any]) -> list[str]:
    d = ROOT / 'system/phase_controllers' / phase['controller_dir']
    d.mkdir(parents=True, exist_ok=True)
    cid = f"{phase['phase_id']}_{phase['domain'].upper()}_CONTROLLER"
    created=[]
    files = {
        'controller.yaml': {
            'controller_id': cid,
            'phase_id': phase['phase_id'],
            'name': phase['name'],
            'domain': phase['domain'],
            'status': 'STANDARD_WRAPPER_READY_WITH_RUNTIME_BLOCKED',
            'generated_by': 'HER-KPP-SYSTEM-RESCAN-AUTOFIX-20260513',
            'purpose': 'Convert docs-only phase material into standard controller assets with contracts, acceptance, handoff, and read-only validation binding.',
            'upstream_required': phase['upstream'],
            'downstream_allowed': phase['downstream'],
            'runtime_boundary': {'real_trade_enabled':False,'signing_enabled':False,'broadcast_enabled':False,'swap_enabled':False,'business_runtime_allowed':False,'validator_only':True},
            'forbidden': ['live_execution','wallet_signing','transaction_broadcast','swap','auto_order','treat_priority_level_as_buy_signal','skip_acceptance_gate'],
        },
        'task_tree.yaml': {
            'task_tree_id': f"{phase['phase_id']}_{phase['domain']}_standard_task_tree",
            'tasks': [
                {'id':'T01_LOAD_UPSTREAM_HANDOFF','type':'read_only_validation','required':True},
                {'id':'T02_VALIDATE_INPUT_CONTRACT','type':'json_schema_validation','required':True},
                {'id':'T03_EXECUTE_DOMAIN_LOGIC','type':'blocked_until_runtime_module_bound','required':False,'status':'BLOCKED_BY_DESIGN'},
                {'id':'T04_VALIDATE_OUTPUT_CONTRACT','type':'json_schema_validation','required':True},
                {'id':'T05_WRITE_TRACE_AND_HANDOFF','type':'handoff_packet_generation','required':True},
            ]
        },
        'acceptance_gate.yaml': {
            'gate_id': f"{phase['phase_id']}_{phase['domain']}_acceptance_gate",
            'required_checks': ['controller_assets_exist','input_contract_valid_json_schema','output_contract_valid_json_schema','handoff_schema_valid_json_schema','runner_binding_is_validator_only','safety_boundary_false_for_real_trade_signing_broadcast_swap'],
            'pass_status': 'READY_WITH_RUNTIME_BLOCKED',
            'fail_status': 'BLOCKED',
        },
        'runner_binding.yaml': {
            'runner_binding_id': f"{phase['phase_id']}_{phase['domain']}_runner_binding",
            'mode': 'READ_ONLY_VALIDATOR_ONLY',
            'business_runtime': 'BLOCKED_UNTIL_EXPLICIT_MODULE_AND_FIXTURE_ACCEPTANCE',
            'entrypoint': {'command': f"python3 tools/stable_trader_os/validate_phase_controller_contracts.py --phase {phase['phase_id']}", 'workdir': '/root/sikk-gmgn'},
            'forbidden_capabilities': ['private_key_read','sign_transaction','broadcast_transaction','swap','live_order','paper_runtime_start'],
        },
        'state_writeback_policy.yaml': {
            'policy_id': f"{phase['phase_id']}_{phase['domain']}_state_writeback_policy",
            'allowed_writebacks': ['validation_status','gap_status','handoff_status','acceptance_result_path','trace_refs'],
            'forbidden_writebacks': ['live_trade_state','private_key_state','execution_position_state','paper_ready_without_p08_acceptance'],
            'target_state_root': f"data/phase_controllers/{phase['phase_id'].lower()}_{phase['domain']}/",
        },
    }
    for name,obj in files.items():
        write_yaml(d/name, obj); created.append(rel(d/name))
    context = f"""# {phase['phase_id']} {phase['name']} Controller Context\n\nThis standard wrapper was generated by KPP system rescan to convert explanatory/document-only phase material into enforceable controller assets.\n\n## Role\n- Domain: `{phase['domain']}`\n- Upstream required: {', '.join(phase['upstream'])}\n- Downstream allowed: {', '.join(phase['downstream'])}\n\n## Boundary\nOBSERVE/PAPER research only. This controller wrapper cannot enable live trading, signing, broadcasting, swap, auto-order, or paper runtime start. Its runner binding is read-only validation until explicit runtime module + fixtures + acceptance are approved.\n\n## Consumption Rule\nDownstream modules may only consume outputs that pass `output_contract.json` and `handoff_packet.schema.json`. Missing fields must be represented as explicit gaps, not guessed.\n"""
    write_text(d/'context.md', context); created.append(rel(d/'context.md'))
    write_json(d/'input_contract.json', schema_for(phase,'input')); created.append(rel(d/'input_contract.json'))
    write_json(d/'output_contract.json', schema_for(phase,'output')); created.append(rel(d/'output_contract.json'))
    handoff = schema_for(phase,'handoff_packet')
    handoff['title'] = f"{phase['phase_id']} {phase['name']} handoff packet schema"
    handoff['required'] = handoff['required'] + ['from_phase','to_phase']
    handoff['properties']['from_phase'] = {'const': phase['phase_id']}
    handoff['properties']['to_phase'] = {'type':'string'}
    write_json(d/'handoff_packet.schema.json', handoff); created.append(rel(d/'handoff_packet.schema.json'))
    return created


def create_contract_schema_wrappers(phase: dict[str, Any]) -> list[str]:
    created=[]
    legacy = LEGACY_MAP[phase['slug']]
    for root_name, root_dir in [('contracts', ROOT/'contracts/stable_trader_os'), ('schemas', ROOT/'schemas/stable_trader_os')]:
        d = root_dir / phase['slug']
        d.mkdir(parents=True, exist_ok=True)
        wrapper = {
            'asset_id': f"{phase['slug']}_{root_name}_wrapper",
            'phase_id': phase['phase_id'],
            'domain': phase['domain'],
            'status': 'CURRENT_PHASE_WRAPPER_READY',
            'generated_by': 'HER-KPP-SYSTEM-RESCAN-AUTOFIX-20260513',
            'legacy_source_mapping': {'legacy_dir': f'{root_name}/stable_trader_os/{legacy}', 'copy_or_delete_performed': False},
            'canonical_controller_assets': {
                'input_contract': f"system/phase_controllers/{phase['controller_dir']}/input_contract.json",
                'output_contract': f"system/phase_controllers/{phase['controller_dir']}/output_contract.json",
                'handoff_schema': f"system/phase_controllers/{phase['controller_dir']}/handoff_packet.schema.json",
            },
            'safety_boundary': {'real_trade_enabled':False,'signing_enabled':False,'broadcast_enabled':False,'swap_enabled':False},
        }
        write_yaml(d/'index.yaml', wrapper); created.append(rel(d/'index.yaml'))
        if root_name == 'schemas':
            write_json(d/'input_contract.schema.json', schema_for(phase,'input')); created.append(rel(d/'input_contract.schema.json'))
            write_json(d/'output_contract.schema.json', schema_for(phase,'output')); created.append(rel(d/'output_contract.schema.json'))
        else:
            write_json(d/'input_contract.json', schema_for(phase,'input')); created.append(rel(d/'input_contract.json'))
            write_json(d/'output_contract.json', schema_for(phase,'output')); created.append(rel(d/'output_contract.json'))
    return created


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    all_created=[]
    for ph in PHASES:
        all_created.extend(create_controller_assets(ph))
        all_created.extend(create_contract_schema_wrappers(ph))

    # Batch legacy document reprocess task package (not full processing yet; creates automated package).
    write_yaml(OUT/'task_packages/batch_legacy_document_reprocess_task_package.yaml', {
        'task_package_id':'KPP_BATCH_LEGACY_DOCUMENT_REPROCESS_20260513',
        'status':'READY_QUEUED_NOT_EXECUTED',
        'goal':'将旧解释性文档按 K00-K08 全链路重处理为 passport/chunks/mapping/candidates/task_packages/handoff，而不是仅保留说明文档。',
        'input_scope':['sikk_stable_trader_os/**/*.md','docs/**/*.md'],
        'output_root':'data/knowledge_processing_program/batch_legacy_reprocess/',
        'execution_steps':['discover_documents','deduplicate_by_hash','create_document_passport','chunk_and_extract_requirements','map_to_phase_controller_assets','generate_candidate_tasks','write_handoff_packets','run_acceptance'],
        'safety_boundary':['read_only_document_processing','no_runtime_trading','no_file_deletion','candidate_only_until_governance_review'],
    })
    all_created.append('data/knowledge_processing_program/system_rescan/task_packages/batch_legacy_document_reprocess_task_package.yaml')

    # Validator tool.
    validator = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
try:
    import yaml
except Exception:
    yaml = None
ROOT=Path('/root/sikk-gmgn')
PHASES={
'P01':'p01_candidate_intake_controller','P02':'p02_source_data_fact_controller','P03':'p03_wallet_entity_controller','P04':'p04_chip_structure_controller','P05':'p05_evidence_controller','P06':'p06_scenario_recognition_controller','P07':'p07_strategy_gate_controller','P08':'p08_execution_risk_controller','P09':'p09_review_replay_controller','P10':'p10_self_upgrade_controller'}
REQ=['controller.yaml','context.md','input_contract.json','output_contract.json','task_tree.yaml','acceptance_gate.yaml','runner_binding.yaml','state_writeback_policy.yaml','handoff_packet.schema.json']
FORBID=['real_trade_enabled: true','signing_enabled: true','broadcast_enabled: true','swap_enabled: true','live_execution_allowed: true','auto_order_allowed: true']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase', default='ALL'); args=ap.parse_args()
    phases=PHASES if args.phase=='ALL' else {args.phase:PHASES[args.phase]}
    problems=[]
    for pid,dname in phases.items():
        d=ROOT/'system/phase_controllers'/dname
        for f in REQ:
            p=d/f
            if not p.exists(): problems.append(f'{pid}: missing {p}')
            elif f.endswith('.json'):
                try: json.loads(p.read_text())
                except Exception as e: problems.append(f'{pid}: invalid json {p}: {e}')
        rb=d/'runner_binding.yaml'
        txt=rb.read_text(errors='ignore') if rb.exists() else ''
        if 'READ_ONLY_VALIDATOR_ONLY' not in txt: problems.append(f'{pid}: runner binding is not validator-only')
        for bad in FORBID:
            if bad in txt: problems.append(f'{pid}: forbidden enabled term in runner binding: {bad}')
    result={'status':'PASS' if not problems else 'FAIL','problems':problems}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not problems else 1
if __name__=='__main__': sys.exit(main())
'''
    write_text(ROOT/'tools/stable_trader_os/validate_phase_controller_contracts.py', validator)
    all_created.append('tools/stable_trader_os/validate_phase_controller_contracts.py')

    test = r'''from pathlib import Path
import json
import subprocess

ROOT = Path('/root/sikk-gmgn')
PHASE_DIRS = [
'p01_candidate_intake_controller','p02_source_data_fact_controller','p03_wallet_entity_controller','p04_chip_structure_controller','p05_evidence_controller','p06_scenario_recognition_controller','p07_strategy_gate_controller','p08_execution_risk_controller','p09_review_replay_controller','p10_self_upgrade_controller']
REQ = ['controller.yaml','context.md','input_contract.json','output_contract.json','task_tree.yaml','acceptance_gate.yaml','runner_binding.yaml','state_writeback_policy.yaml','handoff_packet.schema.json']
SLUGS = ['phase_01_candidate_intake','phase_02_source_data_fact','phase_03_wallet_entity','phase_04_chip_structure','phase_05_evidence','phase_06_scenario_recognition','phase_07_strategy_gate','phase_08_execution_risk','phase_09_review_replay','phase_10_self_upgrade']

def test_gap_registry_and_task_package_exist():
    assert (ROOT/'data/knowledge_processing_program/system_rescan/gaps/system_rescan_gap_registry.yaml').exists()
    assert (ROOT/'data/knowledge_processing_program/system_rescan/task_packages/her_kpp_system_rescan_autofix_task_package.yaml').exists()

def test_standard_phase_controller_assets_exist_and_json_valid():
    for d in PHASE_DIRS:
        base = ROOT/'system/phase_controllers'/d
        for f in REQ:
            p = base/f
            assert p.exists(), str(p)
            if f.endswith('.json'):
                json.loads(p.read_text())

def test_current_contract_schema_wrappers_exist():
    for slug in SLUGS:
        assert (ROOT/'contracts/stable_trader_os'/slug/'index.yaml').exists()
        assert (ROOT/'schemas/stable_trader_os'/slug/'index.yaml').exists()

def test_validator_passes_and_safety_boundary_kept():
    proc = subprocess.run(['python3','tools/stable_trader_os/validate_phase_controller_contracts.py','--phase','ALL'], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert 'real_trade_enabled: true' not in proc.stdout
'''
    write_text(ROOT/'tests/stable_trader_os/test_kpp_system_rescan_acceptance.py', test)
    all_created.append('tests/stable_trader_os/test_kpp_system_rescan_acceptance.py')

    write_yaml(OUT/'handoff/kpp_system_rescan_autofix_completion_handoff.yaml', {
        'handoff_id':'KPP_SYSTEM_RESCAN_AUTOFIX_COMPLETION_20260513',
        'status':'AUTOFIX_APPLIED_PENDING_VALIDATION',
        'created_at': ts,
        'created_or_updated_count': len(all_created),
        'artifacts': all_created,
        'safety_boundary': {'real_trade_enabled':False,'signing_enabled':False,'broadcast_enabled':False,'swap_enabled':False,'paper_runtime_started':False},
        'next_gate':'pytest tests/stable_trader_os/test_kpp_system_rescan_acceptance.py and validator ALL',
    })
    write_json(OUT/'reports/kpp_system_rescan_autofix_report.json', {'status':'AUTOFIX_APPLIED','created_at':ts,'artifacts':all_created})
    print(json.dumps({'status':'AUTOFIX_APPLIED','artifact_count':len(all_created)}, ensure_ascii=False, indent=2))

if __name__=='__main__':
    main()
