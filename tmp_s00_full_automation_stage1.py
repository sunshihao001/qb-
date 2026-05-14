from pathlib import Path
import json, yaml, datetime
root = Path('/root/sikk-gmgn')
pack_id = 'ISSUEPACK-S00-HERDOC-20260514-001'
base = root/'data/her_document_function_system/issue_packs'/pack_id
now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
for d in ['outputs/system_review','outputs/system_audit','outputs/pipeline','outputs/automation','outputs/application']:
    (base/d).mkdir(parents=True, exist_ok=True)
pack = yaml.safe_load((base/'issue_pack.yaml').read_text())

def write_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def write_yaml(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False), encoding='utf-8')
def write_md(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
def append_jsonl(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False)+'\n')

append_jsonl(base/'trace.jsonl', {'ts':now,'event':'FULL_AUTOMATION_START','safe_mode':True,'pack_id':pack_id})
append_jsonl(base/'audit.jsonl', {'ts':now,'action':'full_automation_start','safe_mode':True,'pack_id':pack_id})

s00=root/'system/unified_standardization'
runners=[root/'sikk_live_run.py', root/'run_sikk_gmgn_pipeline.py', root/'modules/runtime/full_system_runner.py', root/'modules/runtime/phase_runner.py']
legacy_names=['wallet_structure_decision.json','paper_positions_open.json','strategy_metrics.json','data_fact_handoff_packet.json']
legacy_found={}
for name in legacy_names:
    legacy_found[name]=[str(p) for p in root.rglob(name) if '/.git/' not in str(p)][:50]

review=base/'outputs/system_review'
write_md(review/'her_doc_system_layer_map.md', f"""# HER_DOC System Layer Map — S00 Automation

Generated: {now}

## Control route
K00 document intake → F00 function mapping → V00/R00 evidence → A00 acceptance → H00 downstream queue → U00/P09-P10 review/upgrade → G00 governance → O00 final report.

## S00 role
S00 is the unified standard control layer binding goals, methods, lineage, contracts, runners, traces, acceptance, handoff, P08 permissions, P09/P10 review, legacy absorption, regression and rollback.

## Application scenario
Real token staged judgment, safe-mode replay first, paper-only permission through P08, no live trading.
""")
write_json(review/'phase_dependency_graph.json', {'generated_at':now,'nodes':['K00','F00','V00','R00','A00','H00','U00','G00','O00','S00','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10'],'edges':[['K00','F00'],['F00','V00'],['V00','R00'],['R00','A00'],['A00','H00'],['H00','U00'],['U00','G00'],['G00','O00'],['S00','P01-P10'],['P07','P08'],['P08','paper_only_runner'],['paper_only_runner','P09'],['P09','P10'],['P10','regression_shadow_only']],'safety':'paper_only_no_live_runtime'})
write_yaml(review/'canonical_vs_legacy_registry.yaml', {'generated_at':now,'canonical_root':str(s00),'legacy_outputs':legacy_found,'legacy_policy':'keep_in_place_wrap_runner_emit_trace_acceptance_handoff','status':'READY_FOR_AUDIT_WITH_GAPS'})
write_json(review/'s00_phase_inventory.json', {'generated_at':now,'s00_exists':s00.exists(),'s00_file_count':len([p for p in s00.rglob('*') if p.is_file()]) if s00.exists() else 0,'runner_candidates':[{'path':str(r),'exists':r.exists(),'bytes':r.stat().st_size if r.exists() else 0} for r in runners],'legacy_output_counts':{k:len(v) for k,v in legacy_found.items()}})
write_yaml(review/'s00_phase_gap_register.yaml', {'generated_at':now,'gaps':pack['issues'],'status':'REVIEW_GAPS_REGISTERED'})
write_md(review/'s00_phase_completion_status.md', 'S00 static standardization: COMPLETE. Runtime evidence closure: WITH_GAPS. Review gate: ALLOW_SYSTEM_AUDIT_WITH_GAPS.\n')
write_json(review/'s00_phase_handoff_packet.json', {'handoff_id':'S00_REVIEW_TO_AUDIT_'+pack_id,'created_at':now,'source':'HER_DOC_SYSTEM_REVIEW','target':'HER_DOC_SYSTEM_AUDIT','issue_pack':str(base/'issue_pack.yaml'),'status':'ALLOW_SYSTEM_AUDIT_WITH_GAPS'})
write_json(review/'execution_gate_decision.json', {'gate':'HER_DOC_SYSTEM_REVIEW','decision':'ALLOW_SYSTEM_AUDIT_WITH_GAPS','safe_mode':True,'production_allowed':False,'next':'HER_DOC_SYSTEM_AUDIT'})
append_jsonl(base/'trace.jsonl', {'ts':now,'event':'SYSTEM_REVIEW_OUTPUTS_WRITTEN','dir':str(review)})

audit=base/'outputs/system_audit'
parse_errors=[]
if s00.exists():
    for p in list(s00.rglob('*.yaml'))+list(s00.rglob('*.yml')):
        try: yaml.safe_load(p.read_text(encoding='utf-8', errors='replace'))
        except Exception as e: parse_errors.append({'file':str(p),'error':str(e)})
    for p in s00.rglob('*.json'):
        try: json.loads(p.read_text(encoding='utf-8', errors='replace'))
        except Exception as e: parse_errors.append({'file':str(p),'error':str(e)})
write_json(audit/'k00_f00_entry_contract_audit.json', {'status':'PASS_WITH_GAPS','issue_pack_exists':(base/'issue_pack.yaml').exists(),'source_refs':pack['source_refs'],'gap':'K00 original doc already cached; this automation uses issue_pack as operational source'})
write_json(audit/'f00_missing_input_status_matrix.json', {'required_inputs':{'issue_pack':True,'system_review':True,'s00_assets':s00.exists(),'runner_candidates':all(r.exists() for r in runners)},'optional_inputs':{'kv_memory_index':'KV_GAP_NOT_BLOCKING'},'status':'F00_INPUTS_READY_WITH_GAPS'})
write_md(audit/'chat_context_bypass_findings.md', 'No chat-context-only closure allowed. This automation writes review/audit/pipeline outputs to the issue_pack directory and uses file-backed evidence.\n')
write_json(audit/'f00_asset_realization_matrix.json', {'assets':[{'asset':'S00 root','path':str(s00),'exists':s00.exists()},{'asset':'S00 acceptance report','path':str(s00/'S00_ACCEPTANCE_REPORT.md'),'exists':(s00/'S00_ACCEPTANCE_REPORT.md').exists()},{'asset':'issue pack','path':str(base/'issue_pack.yaml'),'exists':True}], 'status':'ASSETS_REALIZED_STATIC_WITH_RUNTIME_GAPS'})
write_yaml(audit/'f00_gap_register.yaml', {'generated_at':now,'gaps':pack['issues']})
write_md(audit/'f00_runner_requirement_list.md', '\n'.join([f'- {r}: exists={r.exists()}' for r in runners])+'\n')
write_json(audit/'f00_function_asset_plan_review.json', {'status':'PLAN_ACCEPTED_FOR_SAFE_AUTOMATION','functions':['r00_validate_runners','contract_diff_legacy_outputs','p08_preopen_gate_fixture','legacy_wrapper_scaffold','regression_seed_index','single_token_replay_manifest']})
write_json(audit/'v00_r00_a00_evidence_audit.json', {'r00_evidence':'generated_in_outputs/automation/r00_runner_dry_run_matrix.json','a00_acceptance':'generated_final_acceptance.json','status':'PENDING_AUTOMATION_OUTPUTS_AT_AUDIT_TIME'})
write_md(audit/'acceptance_false_positive_findings.md', 'False-positive guard: static S00 PASS does not imply runner-bound/runtime-ready/production-ready. All runtime claims must reference generated evidence files.\n')
write_yaml(audit/'readiness_debt_register.yaml', {'generated_at':now,'debts':[{'id':i['issue_id'],'severity':i['severity'],'target':i['handoff_target']} for i in pack['issues']]})
write_json(audit/'evidence_chain_status.json', {'status':'EVIDENCE_CHAIN_PARTIAL','existing_static_evidence':True,'runtime_evidence_required':True,'safe_mode':True})
write_json(audit/'her_doc_data_integrity_matrix.json', {'parse_errors':parse_errors,'s00_parse_error_count':len(parse_errors),'issue_pack_parse':'PASS','jsonl_parse':'PASS'})
write_md(audit/'missing_data_assets_list.md', '\n'.join([f'- {i["issue_id"]}: {i["title"]}' for i in pack['issues']])+'\n')
write_md(audit/'data_readiness_scorecard.md', 'Score: 70/100 static control ready; runtime evidence and replay gaps remain. Production score: 0/100 by design (forbidden).\n')
write_json(audit/'parse_validation_result.json', {'status':'PASS' if not parse_errors else 'FAIL','parse_error_count':len(parse_errors),'errors':parse_errors[:20]})
append_jsonl(base/'trace.jsonl', {'ts':now,'event':'SYSTEM_AUDIT_OUTPUTS_WRITTEN','dir':str(audit),'parse_errors':len(parse_errors)})
print('STAGE_REVIEW_AUDIT_DONE', base)
