#!/usr/bin/env python3
from pathlib import Path
import json, yaml, re, sys
root = Path(__file__).resolve().parents[2]
errors=[]; warnings=[]
required_files=['phase_manifest.yaml','phase_context_pack.md','phase_objective_tree.yaml','phase_input_contract.json','phase_output_contract.json','phase_execution_protocol.md','phase_acceptance_gate.yaml','phase_state.json','phase_handoff_packet.schema.json']
core_anchor='Phase Controller 不是阶段说明文档'
registry_path=root/'00_system_registry/phase_registry.yaml'
try:
    phase_reg=yaml.safe_load(registry_path.read_text())
except Exception as e:
    print(json.dumps({'status':'FAIL','errors':[f'PHASE_REGISTRY_PARSE:{e}']},ensure_ascii=False,indent=2)); sys.exit(1)
phases=phase_reg.get('phases',[])
if len(phases)!=10: errors.append(f'PHASE_COUNT_NOT_10:{len(phases)}')
for phase in phases:
    pid=phase.get('phase_id'); d=root/phase.get('package_path','')
    if not d.exists(): errors.append(f'MISSING_PHASE_DIR:{pid}:{d}'); continue
    for f in required_files:
        p=d/f
        if not p.exists() or p.stat().st_size==0:
            errors.append(f'MISSING_OR_EMPTY_PHASE_FILE:{pid}:{f}'); continue
        txt=p.read_text(errors='ignore')
        if f.endswith('.json'):
            try: json.loads(txt)
            except Exception as e: errors.append(f'JSON_PARSE:{pid}:{f}:{e}')
        if f.endswith('.yaml'):
            try: yaml.safe_load(txt)
            except Exception as e: errors.append(f'YAML_PARSE:{pid}:{f}:{e}')
    # semantic anchors
    ctx=(d/'phase_context_pack.md').read_text(errors='ignore') if (d/'phase_context_pack.md').exists() else ''
    proto=(d/'phase_execution_protocol.md').read_text(errors='ignore') if (d/'phase_execution_protocol.md').exists() else ''
    manifest=(d/'phase_manifest.yaml').read_text(errors='ignore') if (d/'phase_manifest.yaml').exists() else ''
    combined='\n'.join([ctx,proto,manifest])
    for anchor in [core_anchor,'OBSERVE_PAPER_ONLY','字段来源','反证','验收','handoff','禁止']:
        if anchor not in combined:
            errors.append(f'MISSING_SEMANTIC_ANCHOR:{pid}:{anchor}')
    if 'placeholder' in combined.lower():
        errors.append(f'PLACEHOLDER_LEFT:{pid}')
    # contract semantics
    try:
        inp=json.loads((d/'phase_input_contract.json').read_text())
        out=json.loads((d/'phase_output_contract.json').read_text())
        gate=yaml.safe_load((d/'phase_acceptance_gate.yaml').read_text())
        state=json.loads((d/'phase_state.json').read_text())
        schema=json.loads((d/'phase_handoff_packet.schema.json').read_text())
        if not inp.get('required_fields'): errors.append(f'INPUT_NO_REQUIRED_FIELDS:{pid}')
        if not out.get('required_outputs'): errors.append(f'OUTPUT_NO_REQUIRED_OUTPUTS:{pid}')
        for req in ['field_source_map_present','counter_evidence_recorded','hard_negative_checked','no_ai_inferred_fact_field']:
            if req not in gate.get('professional_acceptance',{}).get('required',[]): errors.append(f'GATE_MISSING:{pid}:{req}')
        if state.get('state_type')!='runtime_state_not_design_doc': errors.append(f'STATE_NOT_RUNTIME_TYPED:{pid}')
        for key in ['phase_id','phase_status','runtime_boundary','hard_negative_hits','next_phase_allowed','audit_ref']:
            if key not in schema.get('required',[]): errors.append(f'HANDOFF_SCHEMA_MISSING_REQUIRED:{pid}:{key}')
    except Exception as e:
        errors.append(f'SEMANTIC_CHECK_EXCEPTION:{pid}:{e}')
# master skill and planbook
for rel in ['00_methodology/materials/task_packs/phase_controller_data_model_workflow_plan.md','00_methodology/materials/task_packs/phase_controller_data_model_task_manifest.json','01_total_control_skill/SKILL.md','09_runtime_state/current_system_state.json','05_handoff/phase_controller_data_model_handoff_packet.json']:
    p=root/rel
    if not p.exists() or p.stat().st_size==0: errors.append(f'MISSING_CONTROL_ARTIFACT:{rel}')
    elif rel.endswith('.json'):
        try: json.loads(p.read_text())
        except Exception as e: errors.append(f'CONTROL_JSON_PARSE:{rel}:{e}')
if (root/'01_total_control_skill/SKILL.md').exists():
    st=(root/'01_total_control_skill/SKILL.md').read_text(errors='ignore')
    for anchor in [core_anchor,'OBSERVE_PAPER_ONLY','Completion Rule','input contract']:
        if anchor not in st: errors.append(f'MASTER_SKILL_MISSING_ANCHOR:{anchor}')
# safety scan
text='\n'.join(p.read_text(errors='ignore') for p in root.rglob('*') if p.is_file() and p.suffix in ['.yaml','.json','.md'])
unsafe=[]
for pat in ['real_trade_enabled: true','"real_trade_enabled": true','signing_enabled: true','"signing_enabled": true','broadcast_transaction: true','swap_enabled: true','allow_real_trade: true']:
    if pat in text: unsafe.append(pat)
if unsafe: errors.extend([f'UNSAFE_FLAG:{x}' for x in unsafe])
secret_patterns={
 'openrouter_key': r'sk-or-v1-[A-Za-z0-9_-]{20,}',
 'generic_openai_key': r'sk-[A-Za-z0-9]{32,}',
 'telegram_bot_token': r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b'
}
secret_hits={k:len(re.findall(v,text)) for k,v in secret_patterns.items()}
for k,v in secret_hits.items():
    if v: errors.append(f'SECRET_PATTERN_HIT:{k}:{v}')
result={
 'status':'PHASE_CONTROLLER_DATA_MODEL_READY' if not errors else 'PHASE_CONTROLLER_DATA_MODEL_REJECTED',
 'overall': not errors,
 'errors': errors,
 'warnings': warnings,
 'phase_count': len(phases),
 'required_files_per_phase': len(required_files),
 'total_required_phase_files': len(phases)*len(required_files),
 'core_definition_present': core_anchor in text,
 'runtime_boundary':'OBSERVE_PAPER_ONLY',
 'secret_hits': secret_hits,
 'next_phase_allowed': not errors,
 'next_phase':'system_planes_definition_landing' if not errors else None,
 'hard_negative_hits': [] if not errors else ['VALIDATION_ERROR']
}
out=root/'09_reports/acceptance_reports/phase_controller_data_model_acceptance_result.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2))
# update handoff if exists
hp=root/'05_handoff/phase_controller_data_model_handoff_packet.json'
if hp.exists():
    data=json.loads(hp.read_text())
    data['status']='READY' if not errors else 'REJECTED'
    data['next_phase_allowed']=not errors
    data['acceptance_result']=str(out.relative_to(root))
    data['hard_negative_hits']=result['hard_negative_hits']
    hp.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
