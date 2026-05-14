#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml
root=Path(__file__).resolve().parents[2]
errors=[]; warnings=[]
required_registry=['system_manifest.yaml','phase_registry.yaml','atomic_skill_registry.yaml','tool_registry.yaml','schema_registry.yaml','contract_registry.yaml','status_code_registry.yaml','evidence_registry.yaml','hard_negative_registry.yaml','directory_registry.yaml']
for f in required_registry:
    p=root/'00_system_registry'/f
    if not p.exists() or p.stat().st_size==0: errors.append(f'MISSING_OR_EMPTY_REGISTRY:{f}')
    else:
        try: yaml.safe_load(p.read_text())
        except Exception as e: errors.append(f'YAML_PARSE:{f}:{e}')
phase_reg=yaml.safe_load((root/'00_system_registry/phase_registry.yaml').read_text())
required_phase_files=['phase_manifest.yaml','phase_context_pack.md','phase_objective_tree.yaml','phase_input_contract.json','phase_output_contract.json','phase_execution_protocol.md','phase_acceptance_gate.yaml','phase_state.json','phase_handoff_packet.schema.json']
if len(phase_reg.get('phases',[])) != 10: errors.append(f'PHASE_COUNT_NOT_10:{len(phase_reg.get("phases",[]))}')
seen=[]
for phase in phase_reg['phases']:
    seen.append(phase['phase_id'])
    d=root/phase['package_path']
    if not d.exists(): errors.append('MISSING_PHASE_PACKAGE:'+phase['phase_slug']); continue
    for f in required_phase_files:
        p=d/f
        if not p.exists() or p.stat().st_size==0: errors.append(f'MISSING_PHASE_FILE:{phase["phase_id"]}:{f}')
        elif f.endswith('.json'):
            try: json.loads(p.read_text())
            except Exception as e: errors.append(f'JSON_PARSE:{phase["phase_id"]}:{f}:{e}')
        elif f.endswith('.yaml'):
            try: yaml.safe_load(p.read_text())
            except Exception as e: errors.append(f'YAML_PARSE:{phase["phase_id"]}:{f}:{e}')
for pid in [f'P{i:02d}' for i in range(10)]:
    if pid not in seen: errors.append('MISSING_PHASE_ID:'+pid)
# P01 professional requirements
p01=root/'02_phase_controllers/P01_data_fact'
p01_state=json.loads((p01/'phase_state.json').read_text())
if p01_state.get('current_status')!='PHASE_NOT_STARTED': warnings.append('P01_STATE_NOT_FRESH')
p01_out=json.loads((p01/'phase_output_contract.json').read_text())
for required_out in ['phase_01_fact_summary.json','field_source_map.json','phase_01_gap_list.json','phase_01_handoff_packet.json']:
    if required_out not in [x.get('file',x) for x in p01_out.get('required_outputs',[])]: errors.append('P01_OUTPUT_CONTRACT_MISSING:'+required_out)
# safety scan only registry tree text
text='\n'.join(p.read_text(errors='ignore') for p in root.rglob('*') if p.is_file() and p.suffix in ['.yaml','.json','.md'])
for bad in ['real_trade_enabled: true','"real_trade_enabled": true','signing_enabled: true','broadcast_transaction: true','swap_enabled: true']:
    if bad in text: errors.append('UNSAFE_FLAG:'+bad)
# hard negatives
hn=yaml.safe_load((root/'00_system_registry/hard_negative_registry.yaml').read_text())
hn_codes={x.get('code') for x in hn.get('hard_negatives',[])}
for code in ['DATA_INVALID','WALLET_BLOCK','ACTIVE_DISTRIBUTION','STRUCTURE_COLLAPSE','SCENARIO_BLOCK','EXECUTION_BLOCK','REGRESSION_TEST_FAIL']:
    if code not in hn_codes: errors.append('MISSING_HARD_NEGATIVE:'+code)
result={'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'registry_files':len(required_registry),'phase_count':len(phase_reg.get('phases',[])),'phase_ids':seen,'p01_required_package_files':len(required_phase_files)}
out=root/'09_reports/audit_reports/system_registry_validation_result.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not errors else 1)
