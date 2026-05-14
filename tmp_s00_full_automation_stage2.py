from pathlib import Path
import json, yaml, datetime, subprocess, sys, os, ast, re
root=Path('/root/sikk-gmgn')
pack_id='ISSUEPACK-S00-HERDOC-20260514-001'
run_id='RUN-S00-HERDOC-20260514-001'
base=root/'data/her_document_function_system/issue_packs'/pack_id
auto=base/'outputs/automation'
pipe=base/'outputs/pipeline'
app=base/'outputs/application'
now=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
for d in [auto,pipe,app]: d.mkdir(parents=True, exist_ok=True)

def write_json(p,obj):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def write_yaml(p,obj):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False),encoding='utf-8')
def write_md(p,text):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text,encoding='utf-8')
def append_jsonl(p,obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a',encoding='utf-8') as f: f.write(json.dumps(obj,ensure_ascii=False)+'\n')

def safe_cmd(args, timeout=30):
    try:
        cp=subprocess.run(args,cwd=str(root),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout)
        return {'command':' '.join(args),'exit_code':cp.returncode,'stdout_tail':cp.stdout[-2000:],'stderr_tail':cp.stderr[-2000:]}
    except subprocess.TimeoutExpired as e:
        return {'command':' '.join(args),'exit_code':'TIMEOUT','stdout_tail':(e.stdout or '')[-2000:] if isinstance(e.stdout,str) else '', 'stderr_tail':(e.stderr or '')[-2000:] if isinstance(e.stderr,str) else ''}
    except Exception as e:
        return {'command':' '.join(args),'exit_code':'ERROR','error':str(e)}

# pipeline summaries
run_dir=root/'data/her_document_function_system/runs'/run_id
manifest={'run_id':run_id,'run_dir':str(run_dir),'exists':run_dir.exists(),'expected_status':'HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS','safe_mode':True,'outputs':{}}
for p in run_dir.rglob('*') if run_dir.exists() else []:
    if p.is_file(): manifest['outputs'][str(p.relative_to(run_dir))]=p.stat().st_size
write_json(pipe/'pipeline_output_manifest.json', manifest)
write_yaml(pipe/'k00_to_f00_task_pack.yaml', {'generated_at':now,'source_issue_pack':str(base/'issue_pack.yaml'),'pipeline_run':str(run_dir),'route':'K00_TO_F00_SAFE_MODE','status':'TASK_PACK_EXECUTED_WITH_GAPS'})
summary_path=run_dir/'o00/final_report.md'
write_md(pipe/'final_report.md', summary_path.read_text(encoding='utf-8',errors='replace') if summary_path.exists() else 'Pipeline final report missing; see manifest.\n')
append_jsonl(base/'trace.jsonl', {'ts':now,'event':'HER_DOC_PIPELINE_EXECUTED','run_id':run_id,'run_dir':str(run_dir)})

# 1 R00 runner checks: py_compile + --help timeout safe, no live args
runners=[root/'sikk_live_run.py', root/'run_sikk_gmgn_pipeline.py', root/'modules/runtime/full_system_runner.py', root/'modules/runtime/phase_runner.py']
r00=[]
for r in runners:
    item={'runner_id':r.stem.upper(),'path':str(r),'exists':r.exists(),'safe_checks':[],'forbidden_modes':['live_swap','sign','broadcast']}
    if r.exists():
        item['safe_checks'].append(safe_cmd(['python3','-m','py_compile',str(r)],timeout=30))
        item['safe_checks'].append(safe_cmd(['python3',str(r),'--help'],timeout=10))
    item['status']='PASS_WITH_GAPS' if item['exists'] and item['safe_checks'] and item['safe_checks'][0]['exit_code']==0 else 'FAIL'
    r00.append(item)
write_json(auto/'r00_runner_dry_run_matrix.json', {'generated_at':now,'checks':r00,'status':'R00_SAFE_EVIDENCE_RECORDED_WITH_GAPS'})
# update S00 r00 matrix copy
s00_r00=root/'system/unified_standardization/10_validation_r00/r00_runner_dry_run_matrix.yaml'
write_yaml(s00_r00, {'metadata':{'producer':'ISSUEPACK_FULL_AUTOMATION','consumer':['R00','S00'],'version':'0.2.0','status':'active_with_gaps','acceptance':'py_compile must pass; --help may be timeout/nonzero for legacy scripts but must not execute forbidden modes','updated_at':now}, 'runner_checks':r00})

# 2 contract diff legacy outputs
legacy_names=['wallet_structure_decision.json','paper_positions_open.json','strategy_metrics.json','data_fact_handoff_packet.json']
contract=[]
for name in legacy_names:
    found=[p for p in root.rglob(name) if '/.git/' not in str(p)][:10]
    entries=[]
    for p in found[:3]:
        entry={'path':str(p),'exists':True}
        try:
            data=json.loads(p.read_text(encoding='utf-8',errors='replace'))
            entry['json_parse']='PASS'
            if isinstance(data,dict):
                entry['top_level_type']='object'; entry['top_level_keys']=list(data.keys())[:50]; entry['field_count']=len(data)
            elif isinstance(data,list):
                entry['top_level_type']='array'; entry['item_count']=len(data); entry['sample_keys']=list(data[0].keys())[:50] if data and isinstance(data[0],dict) else []
            else: entry['top_level_type']=type(data).__name__
        except Exception as e:
            entry['json_parse']='FAIL'; entry['error']=str(e)
        entries.append(entry)
    contract.append({'output_name':name,'found_count_first10':len(found),'sample_entries':entries,'schema_diff_status':'STRUCTURAL_KEYS_CAPTURED_NEEDS_FORMAL_SCHEMA_MAPPING'})
write_json(auto/'contract_diff_report.json', {'generated_at':now,'reports':contract,'status':'CONTRACT_DIFF_PASS_01_PARTIAL_WITH_GAPS'})
write_yaml(root/'system/unified_standardization/07_schema_contract/legacy_output_contract_diff_index.yaml', {'metadata':{'producer':'ISSUEPACK_FULL_AUTOMATION','version':'0.1.0','status':'active_with_gaps','updated_at':now}, 'contract_diff_report':str(auto/'contract_diff_report.json'), 'outputs':[c['output_name'] for c in contract]})

# 3 P08 gate fixture/scaffold: create pure validator policy, no trading
p08_policy={'allowed_open_status':['PAPER_READY','PAPER_ACTIVE'],'blocked_status':['BLOCKED','WATCH_ONLY','PAPER_ELIGIBLE','EXIT_MONITOR','FORCE_PAPER_EXIT','READY_FOR_CONFIRMATION','REAL_TRADE_FORBIDDEN'], 'forbidden_real_trade':True}
fixtures=[]
for status in ['BLOCKED','WATCH_ONLY','PAPER_READY','PAPER_ACTIVE','REAL_TRADE_FORBIDDEN']:
    fixtures.append({'permission_status':status,'paper_open_allowed':status in p08_policy['allowed_open_status'],'real_trade_allowed':False,'trace_event':'P08_PERMISSION_EVALUATED'})
write_json(auto/'p08_permission_gate_fixture.json', {'generated_at':now,'policy':p08_policy,'fixtures':fixtures,'status':'P08_BINDING_FIXTURE_READY_NOT_RUNTIME_PATCHED'})
write_yaml(root/'system/unified_standardization/11_permission_gate_p08/p08_runtime_binding_fixture.yaml', {'metadata':{'producer':'ISSUEPACK_FULL_AUTOMATION','version':'0.1.0','status':'fixture_ready','acceptance':'paper runner must call equivalent gate before opening paper position','updated_at':now}, 'policy':p08_policy, 'fixtures':fixtures})

# 4 legacy wrapper scaffold contract
wrapper={'wrapper_id':'S00_LEGACY_RUNTIME_TRACE_ACCEPTANCE_HANDOFF_WRAPPER','created_at':now,'mode':'scaffold_safe_mode','wraps':[str(r) for r in runners],'required_outputs':['trace_event.jsonl','acceptance_result.json','handoff_packet.json'],'forbidden':['live_swap','sign','broadcast','private_key_access'],'status':'WRAPPER_CONTRACT_READY_NOT_ATTACHED'}
write_json(auto/'legacy_wrapper_contract.json', wrapper)
write_yaml(root/'system/unified_standardization/14_legacy_absorption/legacy_wrapper_contract.yaml', {'metadata':{'producer':'ISSUEPACK_FULL_AUTOMATION','version':'0.1.0','status':'contract_ready','updated_at':now}, **wrapper})

# 5 regression seed from discovered token outputs
wallet_files=[p for p in root.rglob('wallet_structure_decision.json') if '/.git/' not in str(p)][:5]
samples=[]
for idx,p in enumerate(wallet_files,1):
    token='UNKNOWN'
    parts=p.parts
    for part in parts:
        if part.endswith('pump') and len(part)>20: token=part; break
    samples.append({'sample_id':f'SAMPLE_WALLET_DECISION_{idx:03d}','sample_type':'wallet_structure_decision_existing_output','token_id':'solana:'+token if token!='UNKNOWN' else token,'source_path':str(p),'label_status':'NEEDS_HUMAN_LABEL','regression_use':'schema_parse_and_replay_baseline_candidate'})
write_yaml(auto/'sample_library_seed.yaml', {'generated_at':now,'samples':samples,'status':'REGRESSION_SEED_CREATED_NEEDS_LABELS'})
write_yaml(root/'system/unified_standardization/15_sample_regression_rollback/sample_library_index.yaml', {'metadata':{'producer':'ISSUEPACK_FULL_AUTOMATION','version':'0.2.0','status':'seeded_needs_labels','updated_at':now}, 'samples':samples})
write_json(root/'system/unified_standardization/15_sample_regression_rollback/regression_baseline_result.json', {'generated_at':now,'sample_count':len(samples),'status':'BASELINE_SEEDED_WITHOUT_RULE_ASSERTIONS','blocking_gap':'human/validated labels required before rule promotion'})

# 6 single-token replay manifest/case-file scaffold from best available token
selected=samples[0] if samples else {'token_id':'UNKNOWN','source_path':None}
case={'token_judgment_case_file_id':'TOKEN_CASE_S00_REPLAY_001','created_at':now,'token_id':selected['token_id'],'mode':'safe_mode_manifest_from_existing_output','phase_path':['P01_data_fact','P02_wallet','P03_entity','P04_chip_structure','P05_evidence','P06_scenario','P07_strategy_gate','P08_permission_gate','P09_review','P10_upgrade_candidate'],'source_refs':[selected.get('source_path'), str(root/'data/gmgn_candidates_live_run/p01_data_fact/handoff/SYSTEM_ARCHIVE/data_fact_handoff_packet.json')],'trace_refs':[str(base/'trace.jsonl')],'acceptance_refs':[str(auto/'r00_runner_dry_run_matrix.json'),str(auto/'contract_diff_report.json')],'handoff_refs':[str(base/'outputs/system_review/s00_phase_handoff_packet.json')],'permission_gate_result':'FIXTURE_ONLY_NOT_RUNTIME_DECISION','paper_decision':'NOT_OPENED_SAFE_MODE_ONLY','known_gaps':['not full live replay executed','P08 runtime binding not patched into paper runner','labels required for regression'],'status':'TOKEN_CASE_FILE_SCAFFOLD_READY_WITH_GAPS'}
write_json(auto/'token_judgment_case_file_scaffold.json', case)
write_json(app/'single_token_application_case_file.json', case)

# acceptance and issue status
issue_status=[]
for issue in yaml.safe_load((base/'issue_pack.yaml').read_text())['issues']:
    sid=issue['issue_id']
    status='AUTOMATION_EVIDENCE_CREATED_WITH_GAPS'
    if 'P08' in sid: status='FIXTURE_CREATED_RUNTIME_BINDING_STILL_REQUIRED'
    if 'SINGLE-TOKEN' in sid: status='CASE_FILE_SCAFFOLD_CREATED_FULL_REPLAY_REQUIRED'
    if 'SAMPLE' in sid: status='SEED_CREATED_LABELS_REQUIRED'
    issue_status.append({'issue_id':sid,'automation_status':status,'handoff_target':issue['handoff_target']})
accept={'generated_at':now,'issue_pack_id':pack_id,'safe_mode':True,'production_ready':False,'ready_for_real_trade':False,'issues':issue_status,'overall_status':'S00_AUTOMATION_APPLIED_READY_WITH_GAPS','next_application_gate':'run real safe-mode single token replay after P08 runtime pre-open binding'}
write_json(base/'outputs/final_automation_acceptance.json', accept)
write_md(app/'S00_APPLICATION_LANDING_REPORT.md', f"""# S00 实际应用场景落地报告

生成时间：{now}

## 已自动化落实
- R00 runner 安全检查证据：`outputs/automation/r00_runner_dry_run_matrix.json`
- legacy 输出 contract diff 初步结构报告：`outputs/automation/contract_diff_report.json`
- P08 permission gate fixture：`outputs/automation/p08_permission_gate_fixture.json`
- legacy wrapper contract：`outputs/automation/legacy_wrapper_contract.json`
- sample library seed：`outputs/automation/sample_library_seed.yaml`
- single-token case file scaffold：`outputs/automation/token_judgment_case_file_scaffold.json`

## 应用场景
真实 token 阶段化判断只能走 safe-mode replay → P08 paper-only permission → paper decision → P09/P10 review → regression/rollback。

## 当前状态
`S00_AUTOMATION_APPLIED_READY_WITH_GAPS`

## 仍禁止
live_swap / sign / broadcast / private_key_access / production_trading。
""")
append_jsonl(base/'trace.jsonl', {'ts':now,'event':'ISSUE_AUTOMATION_OUTPUTS_WRITTEN','status':accept['overall_status']})
append_jsonl(base/'audit.jsonl', {'ts':now,'action':'write_automation_evidence','safe_mode':True,'production_ready':False})
print('AUTOMATION_DONE', base)
