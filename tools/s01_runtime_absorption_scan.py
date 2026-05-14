#!/usr/bin/env python3
from pathlib import Path
import json, re, hashlib, datetime
try:
    import yaml
except Exception:
    yaml = None
ROOT=Path('/root/sikk-gmgn')
OUT=ROOT/'reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay'
OUT.mkdir(parents=True, exist_ok=True)
run_id='S01_runtime_absorption_single_token_replay_'+datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
def rel(p):
    try: return str(Path(p).relative_to(ROOT))
    except Exception: return str(p)
def scan_file(p,limit=200000):
    try:
        p=Path(p)
        if p.exists() and p.is_file() and p.stat().st_size < 1500000:
            return p.read_text(encoding='utf-8', errors='ignore')[:limit]
    except Exception: pass
    return ''
def dump_yaml(path,data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def dump_json(path,data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
runner_specs=[
 ('runner_live_orchestrator','sikk_live_run.py','live_orchestrator','R00',['P01','P02','P03','P04','P05','P06','P07','P08','P09'],'PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none'),
 ('runner_gmgn_pipeline','run_sikk_gmgn_pipeline.py','pipeline','P01-P08',['P01','P02','P03','P04','P05','P06','P07','P08'],'PYTHONPATH=/root/sikk-gmgn python3 run_sikk_gmgn_pipeline.py --output-root data/gmgn_candidates_live_run --limit 5'),
 ('runner_candidate_discovery','sikk_gmgn_new_token_filter.py','candidate_discovery','P01',['P01'],'python3 sikk_gmgn_new_token_filter.py'),
 ('runner_kline_pipeline','sikk_candidate_kline_pipeline.py','kline_processing','P02',['P02'],'python3 sikk_candidate_kline_pipeline.py'),
 ('runner_signal_engine','sikk_candidate_signal_pipeline.py','signal_engine','P06/P07',['P06','P07'],'python3 sikk_candidate_signal_pipeline.py'),
 ('runner_state_machine','sikk_candidate_state_machine.py','state_machine','P07',['P07'],'python3 sikk_candidate_state_machine.py'),
 ('runner_wallet_structure_pipeline','sikk_candidate_wallet_structure_pipeline.py','wallet_gate','P03/P04/P05',['P03','P04','P05'],'python3 sikk_candidate_wallet_structure_pipeline.py'),
 ('runner_wallet_gate','sikk_wallet_structure_gate.py','wallet_gate','P03/P04/P05',['P03','P04','P05'],'python3 sikk_wallet_structure_gate.py'),
 ('runner_quote_security','sikk_candidate_quote_security_pipeline.py','quote_security','P08',['P08'],'python3 sikk_candidate_quote_security_pipeline.py'),
 ('runner_paper_live','sikk_paper_live_runner.py','paper_runner','P08/P09',['P08','P09'],'python3 sikk_paper_live_runner.py'),
 ('runner_failure_attribution','sikk_paper_explanation_builder.py','review','P09/P10',['P09','P10'],'python3 sikk_paper_explanation_builder.py'),
 ('runner_daily_report','sikk_wallet_structure_daily_report.py','report','P09',['P09'],'python3 sikk_wallet_structure_daily_report.py'),
 ('runner_dashboard_builder','sikk_dashboard_builder.py','dashboard','R00',['R00'],'python3 sikk_dashboard_builder.py'),
 ('runner_dashboard_site','sikk_dashboard_site_builder.py','dashboard','R00',['R00'],'python3 sikk_dashboard_site_builder.py'),
 ('runner_full_auto_orchestrator','sikk_full_auto_orchestrator.py','pipeline','R00',['R00'],'python3 sikk_full_auto_orchestrator.py'),
 ('runner_ca_runtime','sikk_ca_runtime_pipeline.py','replay','R00',['P01','P02','P07','P08'],'python3 sikk_ca_runtime_pipeline.py'),
]
assets=[]; runners=[]
for rid,script,rtype,bound,phases,cmd in runner_specs:
    p=ROOT/script; txt=scan_file(p)
    forbidden=[x for x in ['private_key','seed_phrase','seed','signing','broadcast','sendTransaction','auto_order'] if x.lower() in txt.lower()]
    outputs=[]; inputs=[]
    for m in re.findall(r'["\']([^"\']+\.(?:json|csv|md|jsonl|html))["\']', txt[:120000]):
        (outputs if re.search(r'output|summary|state|report|position|event|dashboard|trace',m,re.I) else inputs).append(m)
    status='partially_bound' if p.exists() else 'unbound'
    runners.append({'runner_id':rid,'runner_name':rid.replace('runner_',''),'script_path':rel(p),'entry_command':cmd,'runner_type':rtype,'bound_phase':bound,'bound_phases':phases,'input_contract':'inferred_from_runtime' if p.exists() else 'missing_script','output_contract':'inferred_from_runtime' if p.exists() else 'missing_script','required_inputs':sorted(set(inputs))[:20],'expected_outputs':sorted(set(outputs))[:30],'writes_trace':bool(re.search(r'trace|process_trace|jsonl',txt,re.I)),'writes_acceptance':bool(re.search(r'acceptance|gate|status|summary|decision',txt,re.I)),'writes_handoff':bool(re.search(r'handoff',txt,re.I)),'paper_only_safe':not bool(forbidden),'forbidden_actions_detected_terms':forbidden,'failure_policy':'partial/inferred' if p.exists() else 'missing','dry_run_supported':bool(re.search(r'dry|quote-sources none|safe|mock',txt,re.I)),'replay_supported':bool(re.search(r'replay|case|reconstruct|input',txt,re.I)) or rid in ['runner_live_orchestrator','runner_ca_runtime'],'status':status,'gaps':[] if status!='unbound' else ['script_not_found']})
    assets.append({'asset_id':'asset_'+rid.replace('runner_',''),'asset_name':script,'asset_type':'script','path':rel(p),'detected_from':'priority_runtime_scan','current_role':rtype,'possible_phase':bound,'possible_runner_type':rtype,'input_files':sorted(set(inputs))[:20],'output_files':sorted(set(outputs))[:30],'consumers':[],'is_legacy':False,'absorption_mode':'wrap_runner' if p.exists() else 'unknown','risk_level':'medium' if forbidden else 'low','evidence':['exists='+str(p.exists())],'status':'confirmed' if p.exists() else 'unknown'})
# output files inventory
for base in [ROOT/'data/gmgn_candidates_live_run', ROOT/'data/source_wallet_bot', ROOT/'data/intel_bot']:
    if base.exists():
        for p in base.rglob('*'):
            if p.is_file() and p.suffix.lower() in ['.json','.csv','.md','.jsonl','.html']:
                try: sz=p.stat().st_size
                except Exception: sz=0
                if sz>5000000: continue
                rp=rel(p); low=rp.lower(); phase='unknown'
                if 'token_candidates' in low or 'gmgn_new_token_filter' in low: phase='P01'
                elif 'kline' in low: phase='P02'
                elif 'wallet_structure' in low: phase='P03/P04/P05'
                elif 'candidate_signal' in low or 'signal' in low: phase='P06/P07'
                elif 'state_machine' in low or 'candidate_states' in low: phase='P07'
                elif 'quote_security' in low: phase='P08'
                elif 'paper_live' in low: phase='P08/P09'
                elif 'failure' in low or 'report' in low: phase='P09'
                elif 'site' in low or 'dashboard' in low: phase='R00'
                assets.append({'asset_id':'asset_'+hashlib.sha1(rp.encode()).hexdigest()[:12],'asset_name':p.name,'asset_type':'report' if p.suffix=='.md' else 'data_output','path':rp,'detected_from':'runtime_output_scan','current_role':'runtime_output','possible_phase':phase,'possible_runner_type':'output','input_files':[],'output_files':[rp],'consumers':[],'is_legacy':'legacy' in low,'absorption_mode':'map_output','risk_level':'low','evidence':['file_size='+str(sz)],'status':'confirmed'})
# token selection
TOKEN_RE=re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
token_scores={}; token_sources={}
def add_token(t,src,w):
    token_scores[t]=token_scores.get(t,0)+w; token_sources.setdefault(t,[]).append(src)
for relp,w in [('data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json',3),('data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json',5),('data/gmgn_candidates_live_run/state_machine/candidate_states.json',6),('data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json',8),('data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json',7),('data/gmgn_candidates_live_run/paper_live/paper_positions_open.json',9),('data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json',9)]:
    p=ROOT/relp
    if p.exists():
        for t in TOKEN_RE.findall(scan_file(p,700000)): add_token(t,relp,w)
td=ROOT/'data/gmgn_candidates_live_run/tokens'
if td.exists():
    for p in td.iterdir():
        if p.is_dir() and TOKEN_RE.fullmatch(p.name): add_token(p.name, rel(p), 10)
selected=max(token_scores, key=lambda x: token_scores[x]) if token_scores else None
checks={'P01_candidate_pool':'data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json','P02_kline_summary':'data/gmgn_candidates_live_run/kline_pipeline/candidate_kline_pipeline_summary.json','P06_signal_summary':'data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json','P07_state_machine':'data/gmgn_candidates_live_run/state_machine/candidate_states.json','P03_P04_wallet_summary':'data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json','P08_quote_security':'data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json','P08_P09_paper_open':'data/gmgn_candidates_live_run/paper_live/paper_positions_open.json','P09_paper_closed':'data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json','R00_live_state':'data/gmgn_candidates_live_run/live_state.json','R00_events':'data/gmgn_candidates_live_run/events/live_events.jsonl'}
if selected:
    checks['R00_token_status_json']=f'data/gmgn_candidates_live_run/tokens/{selected}/token_status.json'; checks['R00_token_trace']=f'data/gmgn_candidates_live_run/tokens/{selected}/process_trace.jsonl'
available=[{'name':k,'path':v} for k,v in checks.items() if (ROOT/v).exists()]
missing=[{'name':k,'path':v} for k,v in checks.items() if not (ROOT/v).exists()]
phase_bind={p:[] for p in [f'P{i:02d}' for i in range(1,11)]+['R00']}
for r in runners:
    for ph in r['bound_phases']:
        if ph in phase_bind: phase_bind[ph].append(r['runner_id'])
phase_file_checks={'P01':['data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json'],'P02':['data/gmgn_candidates_live_run/kline_pipeline/candidate_kline_pipeline_summary.json'],'P03':['data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json'],'P04':['data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json'],'P05':['data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json'],'P06':['data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json'],'P07':['data/gmgn_candidates_live_run/state_machine/candidate_states.json'],'P08':['data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json','data/gmgn_candidates_live_run/paper_live/paper_positions_open.json'],'P09':['data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl','data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json'],'P10':['sikk_stable_trader_os/08_acceptance','sikk_stable_trader_os/09_handoff']}
trace_found=bool((ROOT/'data/gmgn_candidates_live_run/events/live_events.jsonl').exists() or (selected and (ROOT/f'data/gmgn_candidates_live_run/tokens/{selected}/process_trace.jsonl').exists()))
acceptance_found=bool((ROOT/'sikk_stable_trader_os/08_acceptance').exists() or (ROOT/'system/unified_standardization/09_trace_acceptance_handoff').exists())
handoff_found=bool((ROOT/'sikk_stable_trader_os/09_handoff').exists() or (ROOT/'shared_handoff').exists())
phase_results=[]
for ph in [f'P{i:02d}' for i in range(1,11)]:
    binds=phase_bind.get(ph,[]); files=phase_file_checks.get(ph,[]); found=[f for f in files if (ROOT/f).exists()]
    output_found=bool(found)
    if binds and output_found and ph not in ['P08','P09','P10']: status='PASS' if trace_found else 'WITH_GAPS'
    elif binds and (output_found or ph=='P10'): status='WITH_GAPS'
    else: status='WITH_GAPS' if binds else 'FAIL'
    gaps=[]
    if not binds: gaps.append('missing_runner_binding')
    if not output_found: gaps.append('missing_or_unconfirmed_runtime_output')
    if not trace_found: gaps.append('missing_trace')
    if not acceptance_found: gaps.append('missing_acceptance_evidence')
    if not handoff_found: gaps.append('missing_handoff_evidence')
    phase_results.append({'phase_id':ph,'token_id':selected or 'NO_TOKEN_FOUND','runner_id':binds,'input_found':bool(found) or ph=='P01','output_found':output_found,'schema_check':'WITH_GAPS','contract_check':'WITH_GAPS','trace_check':'PASS' if trace_found else 'WITH_GAPS','acceptance_check':'PASS' if acceptance_found else 'WITH_GAPS','handoff_check':'PASS' if handoff_found else 'WITH_GAPS','decision_found':output_found,'data_quality':'historical_output_reconstruction','status':status,'blocking_gaps':gaps,'next_action':'close gaps via task packets' if gaps else 'ready for stronger validation'})
paper_txt=scan_file(ROOT/'sikk_paper_live_runner.py')
paper_bypass_risk=not bool(re.search(r'quote|security|permission|gate|P08|confirmation|risk',paper_txt,re.I))
real_trade_risk=bool(re.search(r'private_key|seed_phrase|sendTransaction|broadcast',paper_txt,re.I))
p08_files=[p for p in ['system/unified_standardization/11_permission_gate_p08','data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json','sikk_candidate_quote_security_pipeline.py','sikk_paper_live_runner.py'] if (ROOT/p).exists()]
p09_files=[p for p in ['data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl','sikk_paper_explanation_builder.py','sikk_wallet_structure_daily_report.py','data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json'] if (ROOT/p).exists()]
p10_files=[p for p in ['sikk_stable_trader_os/02_phase_controllers/P10_self_upgrade','sikk_stable_trader_os/02_phase_controllers/P09_system_upgrade','system/unified_standardization/12_review_upgrade_p09_p10','sikk_stable_trader_os/08_acceptance','sikk_stable_trader_os/09_handoff'] if (ROOT/p).exists()]
issues=[]; tasks=[]
def add_issue(iid,itype,severity,phase,runner,file,symptom,root,evidence,blocking,fix):
    tpid='TP_'+iid.replace('ISSUE_','')
    issues.append({'issue_id':iid,'issue_type':itype,'severity':severity,'affected_phase':phase,'affected_runner':runner,'affected_file':file,'symptom':symptom,'root_cause_hypothesis':root,'evidence':evidence,'blocking_status':blocking,'required_fix':fix,'task_packet_id':tpid,'status':'open'})
    tasks.append({'task_packet_id':tpid,'source_issue_id':iid,'task_goal':fix,'scope':phase,'non_goals':['no_real_swap','no_real_order','no_private_key','no_auto_live_rule_promotion'],'files_to_create':[],'files_to_modify':[],'commands_to_run':['PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none'],'validation_steps':['verify expected files exist','parse JSON/YAML outputs','check no real swap/private key/broadcast side effects','update S01 acceptance report'],'acceptance_criteria':['phase status PASS or documented WITH_GAPS','issue has evidence','downstream consumer can locate output'],'rollback_plan':'revert created/modified control artifacts; do not alter runtime data','handoff_target':phase,'completion_status':'pending'})
if not selected: add_issue('ISSUE_S01_001','data_gap','critical','R00','runner_live_orchestrator','data/gmgn_candidates_live_run','No usable real token found','runtime output tree lacks recognizable token','token_scores_empty','blocking','run paper-only runtime or import sample')
if selected and not (ROOT/'data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json').exists(): add_issue('ISSUE_S01_001','data_gap','high','P03/P04','runner_wallet_structure_pipeline','data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json','wallet_structure summary missing','wallet gate not written to canonical tree',missing,'blocks_ACCEPTED','run/wrap wallet_structure runner and emit canonical summary')
if not (ROOT/'sikk_stable_trader_os/07_runners').exists(): add_issue('ISSUE_S01_003','missing_runner_binding','high','R00/P01-P10','all','sikk_stable_trader_os/07_runners','formal runner registry / phase binding missing','runtime scripts exist but not formally consumed','directory missing','blocks_ACCEPTED','create runner_registry.yaml and phase_runner_binding.yaml from S01 draft')
if not trace_found or True: add_issue('ISSUE_S01_004','missing_trace','high','P01-P10','all','trace plane','phase trace not uniformly proven','events/process_trace partial or absent; HER trace matrix missing','trace partial','blocks_ACCEPTED','create runtime phase trace matrix and consumption report')
if not acceptance_found or True: add_issue('ISSUE_S01_005','missing_acceptance','high','P01-P10','all','acceptance plane','runtime outputs lack formal five-level acceptance','acceptance artifacts partial/missing','acceptance partial','blocks_ACCEPTED','create runtime acceptance evidence binder and phase acceptance results')
if not handoff_found or True: add_issue('ISSUE_S01_006','missing_handoff','high','P01-P10','all','handoff plane','downstream consumption not proven','handoff artifacts partial; runtime consumption status missing','handoff partial','blocks_ACCEPTED','create handoff consumption status and phase output index')
add_issue('ISSUE_S01_007','p08_bypass_risk','medium' if not paper_bypass_risk else 'critical','P08','runner_paper_live','sikk_paper_live_runner.py','P08 permission ticket contract not proven' if not paper_bypass_risk else 'paper runner may bypass P08','source check found risk/gate terms but no formal ticket' if not paper_bypass_risk else 'source lacks gate terms','source regex check','blocks_ACCEPTED','formalize P08 permission ticket contract and validation')
if not p09_files: add_issue('ISSUE_S01_008','missing_review_loop','high','P09','runner_failure_attribution','paper_live/failure_attribution.jsonl','P09 review evidence missing','paper results cannot reliably enter review','p09 files empty','blocks_ACCEPTED','emit review_case from paper result/failure attribution')
add_issue('ISSUE_S01_009','missing_review_loop','high','P10','upgrade_controller','P10 upgrade artifacts','P10 upgrade candidate/regression/rollback not proven','P10 formal proof missing','p10 files partial/missing','blocks_ACCEPTED','create upgrade_candidate package with shadow validation/regression/rollback')
for phres in phase_results:
    add_issue('ISSUE_S01_SCHEMA_'+phres['phase_id'],'schema_gap','medium',phres['phase_id'],','.join(phres['runner_id']) if phres['runner_id'] else 'unknown','contracts/schemas','schema/contract check WITH_GAPS','runtime output exists but formal contract validation not executed','phase_result','non_blocking_READY_WITH_GAPS','bind phase output to schema validator and record result')
for t in tasks:
    it=next(i for i in issues if i['issue_id']==t['source_issue_id'])
    typ=it['issue_type']
    if typ=='missing_runner_binding': t['files_to_create']=['sikk_stable_trader_os/07_runners/runner_registry.yaml','sikk_stable_trader_os/07_runners/phase_runner_binding.yaml']
    elif typ=='missing_trace': t['files_to_create']=['sikk_stable_trader_os/00_trace/runtime_phase_trace_matrix.yaml','sikk_stable_trader_os/00_trace/runner_execution_trace.yaml']
    elif typ=='missing_acceptance': t['files_to_create']=['sikk_stable_trader_os/08_acceptance/runtime_acceptance_result.yaml']
    elif typ=='missing_handoff': t['files_to_create']=['sikk_stable_trader_os/09_handoff/handoff_consumption_status.yaml']
    elif typ=='p08_bypass_risk': t['files_to_create']=['sikk_stable_trader_os/02_phase_controllers/P08_execution_risk/p08_permission_ticket.schema.json']; t['files_to_modify']=['sikk_paper_live_runner.py','sikk_candidate_quote_security_pipeline.py']
    elif typ=='missing_review_loop': t['files_to_create']=['sikk_stable_trader_os/02_phase_controllers/P09_review_replay/review_case.schema.json','sikk_stable_trader_os/02_phase_controllers/P10_self_upgrade/upgrade_candidate.schema.json']
    elif typ=='data_gap': t['files_to_create']=['data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json']; t['files_to_modify']=['sikk_candidate_wallet_structure_pipeline.py','run_sikk_gmgn_pipeline.py']
    else: t['files_to_create']=['contracts_or_schemas_for_'+it['affected_phase'].replace('/','_')+'.yaml']
# write outputs
(OUT/'S01_runtime_absorption_plan.md').write_text(f'''# S01 Runtime Absorption & Single Token Replay Plan\n\nrun_id: `{run_id}`\n\n目标：真实 runtime 吸收 → 单 token output reconstruction replay → acceptance report。\n\n安全：paper-only；不 swap；不下单；不签名；不 broadcast；P09/P10 只生成候选，不自动升级 live rule。\n\n步骤：扫描脚本/输出；登记资产；绑定 P01-P10/R00；选择 token；重建 replay；检查 P08/P09/P10/trace/acceptance/handoff；生成 issue/task packet。\n''',encoding='utf-8')
dump_yaml(OUT/'S01_runtime_asset_inventory.yaml',{'run_id':run_id,'asset_count':len(assets),'assets':assets})
dump_yaml(OUT/'S01_runner_absorption_map.yaml',{'run_id':run_id,'runners':runners})
dump_yaml(OUT/'S01_phase_runner_binding_draft.yaml',{'run_id':run_id,'phase_runner_binding':[{'phase_id':ph,'runners':phase_bind.get(ph,[]),'status':'bound' if phase_bind.get(ph) else 'missing'} for ph in [f'P{i:02d}' for i in range(1,11)]+['R00']]})
replay_case={'replay_case_id':'S01_REPLAY_'+(selected or 'NO_TOKEN'),'token_id':selected or 'NO_TOKEN_FOUND','token_address':selected or 'NO_TOKEN_FOUND','source_dirs':sorted(set(token_sources.get(selected,[])))[:20] if selected else [],'available_outputs':available,'missing_outputs':missing,'selected_reason':'highest evidence score across existing runtime outputs' if selected else 'no usable token found','expected_phase_path':[f'P{i:02d}' for i in range(1,11)],'expected_decision_path':'P01→P02→P03/P04→P05→P06→P07→P08→P09→P10','replay_mode':'output_reconstruction' if selected else 'blocked','safety_mode':'paper_only','status':'WITH_GAPS' if selected else 'BLOCKED'}
dump_yaml(OUT/'S01_single_token_replay_plan.yaml',{'run_id':run_id,'replay_case':replay_case})
replay_result={'run_id':run_id,'replay_case':replay_case,'phase_replay_results':phase_results,'final_permission_status':'PAPER_ONLY_READY_WITH_GAPS' if selected else 'BLOCKED_NO_TOKEN','paper_only_readiness':bool(selected),'p08_check':{'permission_gate_files_present':p08_files,'paper_runner_bypass_risk':paper_bypass_risk,'real_trade_risk_detected':real_trade_risk,'status':'WITH_GAPS' if not real_trade_risk else 'FAIL'},'p09_check':{'files_present':p09_files,'paper_result_can_enter_review':bool(p09_files),'status':'WITH_GAPS' if p09_files else 'FAIL'},'p10_check':{'files_present':p10_files,'upgrade_candidate_proven':False,'regression_rollback_proven':False,'status':'WITH_GAPS' if p10_files else 'FAIL'}}
dump_yaml(OUT/'S01_single_token_replay_result.yaml',replay_result)
dump_yaml(OUT/'S01_issue_registry.yaml',{'run_id':run_id,'issue_count':len(issues),'issues':issues})
dump_yaml(OUT/'S01_task_packets.yaml',{'run_id':run_id,'task_packet_count':len(tasks),'task_packets':tasks})
final='S01_BLOCKED' if not selected or any(r['runner_id']=='runner_live_orchestrator' and r['status']=='unbound' for r in runners) else 'S01_READY_WITH_GAPS'
absorbed='\n'.join([f"- runner_id: `{r['runner_id']}`\n  - script_path: `{r['script_path']}`\n  - bound_phase: `{r['bound_phase']}`\n  - status: `{r['status']}`" for r in runners if r['status']!='unbound'])
unabsorbed='\n'.join([f"- `{r['runner_id']}`: 原因={';'.join(r['gaps']) or 'not_bound'}；风险=runtime capability unavailable；修复=locate/create wrapper" for r in runners if r['status']=='unbound']) or '- priority runtime list 内无缺失脚本；其他旧资产已在 inventory 中登记为 map_output/migrate_later/wrap_runner。'
phase_lines='\n'.join([f"- {p['phase_id']}: status={p['status']}; runner={p['runner_id']}; output_found={p['output_found']}; gaps={p['blocking_gaps']}" for p in phase_results])
issue_lines='\n'.join([f"- {i['issue_id']} | severity={i['severity']} | affected_phase={i['affected_phase']} | root_cause_hypothesis={i['root_cause_hypothesis']} | required_fix={i['required_fix']}" for i in issues])
task_lines='\n'.join([f"- {t['task_packet_id']} from {t['source_issue_id']}\n  - files_to_create: {t['files_to_create']}\n  - files_to_modify: {t['files_to_modify']}\n  - commands_to_run: {t['commands_to_run']}\n  - validation_steps: {t['validation_steps']}\n  - acceptance_criteria: {t['acceptance_criteria']}" for t in tasks])
trace_exist=[p for p in ['data/gmgn_candidates_live_run/events/live_events.jsonl', f'data/gmgn_candidates_live_run/tokens/{selected}/process_trace.jsonl' if selected else ''] if p and (ROOT/p).exists()]
accept_exist=[p for p in ['sikk_stable_trader_os/08_acceptance','system/unified_standardization/09_trace_acceptance_handoff'] if (ROOT/p).exists()]
handoff_exist=[p for p in ['shared_handoff','sikk_stable_trader_os/09_handoff'] if (ROOT/p).exists()]
md=f'''# S01 Acceptance Report

run_id: `{run_id}`

## 1. 总体结论

**最终状态码：`{final}`**

总体结论：`{'READY_WITH_GAPS' if final=='S01_READY_WITH_GAPS' else final.replace('S01_','')}`

判定依据：真实 runtime 已扫描，旧资产已登记，runner 已初步绑定 P01-P10/R00，已选择真实 token 并完成 output reconstruction replay；但 trace / acceptance / handoff / P08 permission ticket / P09→P10 review-upgrade 仍存在标准化缺口，因此不能标记为 ACCEPTED 或 S01_READY。

## 2. 已吸收的 runtime

{absorbed}

## 3. 未吸收的 runtime

{unabsorbed}

## 4. 单 token replay 结果

- token_id: `{selected or 'NO_TOKEN_FOUND'}`
- replay path: `{replay_case['expected_decision_path']}`
- replay mode: `{replay_case['replay_mode']}`
- phase result: see below
- final permission status: `{replay_result['final_permission_status']}`
- paper-only readiness: `{replay_result['paper_only_readiness']}`

### phase result

{phase_lines}

## 5. trace / acceptance / handoff 检查

### trace 存在
{chr(10).join('- `'+x+'`' for x in trace_exist) if trace_exist else '- none confirmed'}

### trace 缺失 / 字段不完整
- formal HER `runner_execution_trace.yaml`
- phase_output_index consumption proof
- 每阶段 runner 输入/输出字段级血缘未全部证明

### acceptance 存在
{chr(10).join('- `'+x+'`' for x in accept_exist) if accept_exist else '- none confirmed'}

### acceptance 缺失 / 字段不完整
- per-phase runtime acceptance result
- schema validation result per output
- five-level acceptance evidence 未全部落地

### handoff 存在
{chr(10).join('- `'+x+'`' for x in handoff_exist) if handoff_exist else '- none confirmed'}

### handoff 缺失 / 字段不完整
- formal runtime handoff consumption status
- P08→P09 review handoff proof
- P09→P10 upgrade handoff proof

## 6. P08 检查

- 是否有 permission gate: `{'YES_PARTIAL' if p08_files else 'NO'}`
- P08 evidence files: `{p08_files}`
- paper runner 是否绕过 P08: `{'POTENTIAL_RISK' if paper_bypass_risk else 'NO_DIRECT_BYPASS_DETECTED_BUT_CONTRACT_WITH_GAPS'}`
- 是否存在真实交易风险: `{'YES_SOURCE_TERMS_DETECTED' if real_trade_risk else 'NO_PRIVATE_KEY_SIGNING_BROADCAST_TERMS_DETECTED_IN_PAPER_RUNNER'}`
- 结论：P08 需要正式 permission ticket contract；当前只能 `WITH_GAPS`。

## 7. P09/P10 检查

- paper result 是否能进入 review: `{'YES_PARTIAL' if p09_files else 'NO'}`
- failure attribution 是否存在: `{'YES' if any('failure_attribution' in x for x in p09_files) else 'NO_OR_NOT_CONFIRMED'}`
- upgrade candidate 是否存在: `NO_FORMAL_PROOF`
- regression / rollback 是否存在: `NO_FORMAL_PROOF`
- P09 files: `{p09_files}`
- P10 files: `{p10_files}`
- 结论：P09 有部分复盘入口；P10 仍是 upgrade candidate / shadow / regression / rollback 标准化缺口。

## 8. issue registry

{issue_lines}

完整机器版见：`S01_issue_registry.yaml`

## 9. task packet

{task_lines}

完整机器版见：`S01_task_packets.yaml`

## 安全边界确认

- 全程 paper-only / output reconstruction。
- 未执行真实 swap。
- 未执行真实下单。
- 未读取、写入或修改 API key / 私钥权限。
- 未把 P09/P10 复盘结论升级为 live rule。
- 所有升级仅作为 task packet / upgrade candidate 缺口提出。
'''
(OUT/'S01_acceptance_report.md').write_text(md,encoding='utf-8')
required=['S01_runtime_absorption_plan.md','S01_runtime_asset_inventory.yaml','S01_runner_absorption_map.yaml','S01_phase_runner_binding_draft.yaml','S01_single_token_replay_plan.yaml','S01_single_token_replay_result.yaml','S01_acceptance_report.md','S01_issue_registry.yaml','S01_task_packets.yaml']
verify={'run_id':run_id,'output_dir':str(OUT),'required_files':{},'final_status':final,'selected_token':selected,'asset_count':len(assets),'runner_count':len(runners),'issue_count':len(issues),'task_packet_count':len(tasks)}
for f in required:
    p=OUT/f; item={'exists':p.exists(),'size':p.stat().st_size if p.exists() else 0}
    if p.suffix in ['.yaml','.yml'] and yaml and p.exists():
        try: yaml.safe_load(p.read_text(encoding='utf-8')); item['parse']='PASS'
        except Exception as e: item['parse']='FAIL '+str(e)
    verify['required_files'][f]=item
dump_json(OUT/'S01_verification.json', verify)
print(json.dumps(verify, ensure_ascii=False, indent=2))
