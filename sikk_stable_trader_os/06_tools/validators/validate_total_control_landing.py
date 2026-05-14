#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, glob
root=Path(__file__).resolve().parents[3]
errors=[]; warnings=[]
required=[
'skills/sikk_stable_trader_os/SKILL.md','skills/sikk_stable_trader_os/README.md',
'docs/00_system_goal/sikk_stable_trader_os_goal.md','docs/01_stage_definitions/full_stage_map.md','docs/02_phase_layer_step_maps/full_phase_layer_step_map.md','docs/03_handoff_flow/phase_handoff_flow.md','docs/04_status_codes/global_status_code_table.md','docs/05_hard_negative_rules/global_hard_negative_rules.md','docs/06_directory_constitution/directory_constitution.md','docs/07_contract_index/contract_index.md','docs/08_schema_index/schema_index.md','docs/09_her_execution_protocol/her_total_control_execution_protocol.md','docs/10_professional_acceptance/professional_baseline_acceptance.md',
'contracts/stable_trader_os/total_control_contract.json','contracts/stable_trader_os/phase_execution_contract.json','contracts/stable_trader_os/handoff_contract.json','contracts/stable_trader_os/status_inheritance_contract.json','contracts/stable_trader_os/safety_boundary_contract.json',
'schemas/stable_trader_os/total_control.schema.json','schemas/stable_trader_os/phase_handoff.schema.json','schemas/stable_trader_os/audit_evidence.schema.json',
'research_loop/total_control/total_control_task_manifest.json',
'reports/system_audit/total_control_audit_report.md','reports/system_audit/professional_baseline_acceptance_report.md','reports/system_audit/missing_gap_register.md','reports/system_audit/phase_handoff_validation_report.md','reports/system_audit/status_code_validation_report.md','reports/system_audit/total_control_validation_evidence.md'
]
phase_names=['phase_00_system_constitution','phase_01_data_fact','phase_02_wallet_structure','phase_03_chip_control','phase_04_scenario_recognition','phase_05_structure_position','phase_06_strategy_gate','phase_07_execution_risk','phase_08_review_learning','phase_09_system_upgrade']
hard_neg=['DATA_INVALID','WALLET_BLOCK','ACTIVE_DISTRIBUTION','TRANSFER_TO_COUNTERPARTY','STRUCTURE_COLLAPSE','SCENARIO_BLOCK','SCENARIO_TRAP_RISK','SCENARIO_DISTRIBUTION_RISK','COMPLETION_FAIL','FATIGUE_BLOCK','POSITION_OVEREXTENDED','STRATEGY_BLOCK','EXECUTION_BLOCK','REGRESSION_TEST_FAIL']
for rel in required:
    p=root/rel
    if not p.exists() or p.stat().st_size==0: errors.append(f'MISSING_OR_EMPTY:{rel}')
    if p.exists() and p.suffix=='.json':
        try: json.loads(p.read_text())
        except Exception as e: errors.append(f'JSON_PARSE:{rel}:{e}')
skill=root/'skills/sikk_stable_trader_os/SKILL.md'
if skill.exists():
    txt=skill.read_text()
    if not txt.startswith('---\n'): errors.append('SKILL_FRONTMATTER_NOT_AT_BYTE_0')
    if '\n---\n' not in txt[4:]: errors.append('SKILL_FRONTMATTER_NOT_CLOSED')
    for k in ['name:','description:','OBSERVE_PAPER_ONLY','not Phase10']:
        if k not in txt: errors.append(f'SKILL_MISSING:{k}')
all_text='\n'.join((root/rel).read_text(errors='ignore') for rel in required if (root/rel).exists())
for ph in phase_names:
    if ph not in all_text: errors.append(f'PHASE_REF_MISSING:{ph}')
for hn in hard_neg:
    if hn not in all_text: errors.append(f'HARD_NEGATIVE_MISSING:{hn}')
for status in ['PHASE_READY','PHASE_WITH_GAPS','PHASE_PAUSED','PHASE_REJECTED','PHASE_ERROR','TOTAL_CONTROL_READY','PASS_WITH_ACCEPTED_GAPS']:
    if status not in all_text: errors.append(f'STATUS_MISSING:{status}')
# phase packages still valid in count
phase_dirs=list((root/'sikk_stable_trader_os/02_phase_controllers').glob('P*_*'))
if len(phase_dirs)!=10: errors.append(f'PHASE_PACKAGE_DIR_COUNT:{len(phase_dirs)}')
for d in phase_dirs:
    for f in ['phase_manifest.yaml','phase_context_pack.md','phase_objective_tree.yaml','phase_input_contract.json','phase_output_contract.json','phase_execution_protocol.md','phase_acceptance_gate.yaml','phase_state.json','phase_handoff_packet.schema.json']:
        if not (d/f).exists(): errors.append(f'PHASE_PACKAGE_FILE_MISSING:{d.name}:{f}')
# phase10 guard: allowed only negated mentions
for rel in required:
    p=root/rel
    if not p.exists(): continue
    for i,line in enumerate(p.read_text(errors='ignore').splitlines(),1):
        if 'Phase10' in line or 'phase_10' in line:
            lower=line.lower()
            if not any(x in lower for x in ['not phase10','no phase10','not a runtime phase','not phase10.', 'no phase10 creation', 'never phase10']):
                errors.append(f'UNSAFE_PHASE10_MENTION:{rel}:{i}:{line[:120]}')
unsafe=[]
for pat in ['real_trade_enabled: true','"real_trade_enabled": true','signing_enabled: true','"signing_enabled": true','broadcast_transaction: true','swap_enabled: true','allow_real_trade: true']:
    if pat in all_text: unsafe.append(pat)
for u in unsafe: errors.append(f'UNSAFE_FLAG:{u}')
secret_patterns={'openrouter_key':r'sk-or-v1-[A-Za-z0-9_-]{20,}','generic_openai_key':r'sk-[A-Za-z0-9]{32,}','telegram_bot_token':r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b'}
secret_hits={k:len(re.findall(v,all_text)) for k,v in secret_patterns.items()}
for k,v in secret_hits.items():
    if v: errors.append(f'SECRET_PATTERN_HIT:{k}:{v}')
result={'status':'TOTAL_CONTROL_READY' if not errors else 'TOTAL_CONTROL_REJECTED','overall':not errors,'errors':errors,'warnings':warnings,'required_files':len(required),'phase_package_dirs':len(phase_dirs),'runtime_boundary':'OBSERVE_PAPER_ONLY','phase10_guard':'PASS' if not any(e.startswith('UNSAFE_PHASE10') for e in errors) else 'FAIL','secret_hits':secret_hits,'accepted_gaps':['Phase00 为系统宪法层，当前由 docs 与总控 Skill 承载，不作为业务 runtime controller。'],'next_step':'total_control_runtime_implementation' if not errors else None}
out=root/'reports/system_audit/total_control_validation_result.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2))
# update reports
status=result['status']
(root/'reports/system_audit/total_control_validation_evidence.md').write_text('# Total Control Validation Evidence\n\nStatus: `'+status+'`\n\n```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n')
(root/'reports/system_audit/total_control_audit_report.md').write_text('# Total Control Audit Report\n\nStatus: `'+status+'`\n\n- required_files: '+str(len(required))+'\n- phase_package_dirs: '+str(len(phase_dirs))+'\n- runtime_boundary: `OBSERVE_PAPER_ONLY`\n- errors: '+str(len(errors))+'\n')
(root/'reports/system_audit/professional_baseline_acceptance_report.md').write_text('# Professional Baseline Acceptance Report\n\nVerdict: `'+('PASS_WITH_ACCEPTED_GAPS' if not errors else 'REJECTED')+'`\n\nAccepted gap: Phase00 为系统宪法层，当前由 docs 与总控 Skill 承载，不作为业务 runtime controller。\n')
(root/'reports/system_audit/phase_handoff_validation_report.md').write_text('# Phase Handoff Validation Report\n\nStatus: `'+('PASS' if not errors else 'FAIL')+'`\n\nP00-P09 handoff schemas exist and are indexed.\n')
(root/'reports/system_audit/status_code_validation_report.md').write_text('# Status Code Validation Report\n\nStatus: `'+('PASS' if not errors else 'FAIL')+'`\n\nGlobal status code table contains ready/gap/pause/reject/error/total-control statuses.\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
