from pathlib import Path
import os, json, re, datetime
try:
    import yaml
except Exception:
    yaml=None

root=Path('/root/sikk-gmgn')
out=root/'reports/her_doc_full_system_gap_scan'
out.mkdir(parents=True, exist_ok=True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
scan_scope=['system','docs','research_loop','knowledge','modules','tools','scripts','data','reports','tests']
files=[]
for sub in scan_scope:
    p=root/sub
    if not p.exists():
        continue
    for dp,dns,fns in os.walk(p):
        dns[:] = [d for d in dns if d not in ['.git','__pycache__','.pytest_cache','node_modules','.venv']]
        for fn in fns:
            fp=Path(dp)/fn
            try: sz=fp.stat().st_size
            except Exception: sz=0
            files.append({'path':str(fp),'rel':str(fp.relative_to(root)),'name':fn,'size':sz})

def exists(rel): return (root/rel).exists()
def glob(pattern): return sorted(root.glob(pattern))
def rels(paths, limit=20): return [str(p.relative_to(root)) for p in paths[:limit]]
def grep_paths(words, limit=40):
    outp=[]
    for f in files:
        low=f['rel'].lower()
        if all(w.lower() in low for w in words):
            outp.append(f['rel'])
    return outp[:limit]

legacy_scripts=[f['rel'] for f in files if f['rel'].startswith('scripts/')]
root_runtime_scripts=[p.name for p in root.glob('*.py') if any(k in p.name.lower() for k in ['sikk','paper','runtime','wallet','ca','gmgn'])]
legacy_data_roots=[]
for d in ['runtime_outputs','data/gmgn_candidates_live_run','data/stable_trader_os/replay_evidence','data/source_wallet_bot','data/operational_program/continuous_paper_operation','knowledge','research_loop']:
    if (root/d).exists(): legacy_data_roots.append(d)
existing_reports=grep_paths(['reports'],80)

plane_dirs={
 'Bootstrap Control Plane': ['system/stable_trader_os','sikk_stable_trader_os/00_methodology','sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller'],
 'Governance Plane': ['system/her_document_function_system','system/knowledge_processing_program','system/stable_trader_os/governance_plane'],
 'Domain Plane': ['system/stable_trader_os/domain_plane','system/data_interfaces','modules/source_wallet_bot'],
 'Data Plane': ['system/data_plane','modules/source_wallet_bot','data/source_wallet_bot'],
 'Full Control Plane': ['system/full_control_plane','system/phase_controllers','sikk_stable_trader_os/06_phase_controllers'],
 'Trace Plane': ['system/trace_plane','data/stable_trader_os/replay_evidence'],
 'Acceptance Plane': ['system/acceptance_plane','reports/stable_trader_os/standard_stage_closure/ACCEPTANCE_REPORT.md'],
 'Handoff Plane': ['system/handoff_plane','modules/stable_trader_os/handoff_translator.py']
}
plane_status=[]
for name, ps in plane_dirs.items():
    present=[p for p in ps if exists(p)]
    plane_status.append({'plane':name,'present_assets':present,'status':'PARTIAL' if present else 'MISSING','gap':'plane exists but business-runtime binding must be proven by R00 token dry-run' if present else 'missing plane directory/assets'})

phase_defs={
 'P01':('Candidate Intake Controller','候选接入：把真实 token/candidate batch 固定为可审计 case manifest，不做买入判断'),
 'P02':('Source Data Fact Controller','源数据事实：GMGN/OKX/on-chain 只读事实采集、标准化、质量门禁'),
 'P03':('Wallet Entity Controller','钱包实体：钱包画像、同源候选、资金/回流/历史复现，不做确定庄家'),
 'P04':('Chip Structure Controller','筹码结构：集中度、保留/转移/派发进度、对手盘压力模型'),
 'P05':('Evidence Counter-Evidence Controller','证据与反证控制：证据链、反证、降级、硬负面规则'),
 'P06':('Scenario Recognition Controller','场景识别：阶段/形态/主导侧生命周期候选与替代假设'),
 'P07':('Strategy Gate Controller','策略门禁：EXCLUDE/RECORD/RISK_MONITOR/WATCH/PAPER_READY/READY_FOR_CONFIRMATION'),
 'P08':('Execution Risk / Paper Permission Controller','执行风控：只允许 paper-only，禁止真实 swap/sign/broadcast'),
 'P09':('Review Replay Controller','复盘回放：paper/runtime/历史 token 可回放、偏差归因、样本入库'),
 'P10':('Controlled Upgrade Controller','受控升级：候选规则/模型进入治理审查，不自动改正式规则')
}
check_specs={
 'controller':['system/phase_controllers/{idlow}*','sikk_stable_trader_os/06_phase_controllers/{id}*','sikk_stable_trader_os/02_phase_controllers/{id}*'],
 'input_contract':['**/{id}*/**/*input*contract*','**/{idlow}*/**/*input*contract*'],
 'output_contract':['**/{id}*/**/*output*contract*','**/{idlow}*/**/*output*contract*'],
 'schema':['**/{id}*/**/*schema*','**/{idlow}*/**/*schema*','schemas/**/{idlow}*'],
 'runtime_output_model':['modules/stable_trader_os/{idlow}_standard_stage/runtime_entry.py','runtime_outputs/*/phase_evidence/{id}*/*'],
 'runner_binding':['modules/stable_trader_os/{idlow}_standard_stage/runtime_entry.py','modules/stable_trader_os/phase_*{short}*/*runner*','tests/**/*{idlow}*','tests/**/*{id}*runner*'],
 'trace_requirements':['system/trace_plane/{idlow}_standard_stage/*','runtime_outputs/*/phase_evidence/{id}*/evidence.json','runtime_outputs/*/phase_evidence/{id}*/audit.json'],
 'acceptance_criteria':['system/acceptance_plane/{idlow}_standard_stage/*','**/{id}*/**/*acceptance*','**/{idlow}*/**/*acceptance*'],
 'handoff_contract':['system/handoff_plane/{idlow}_standard_stage/*','**/{id}*/**/*handoff*','**/{idlow}*/**/*handoff*'],
}
def find_phase_assets(pid):
    idlow=pid.lower(); short=pid[1:]
    result={}
    for ck,pats in check_specs.items():
        hits=[]
        for pat in pats:
            hits += rels(glob(pat.format(id=pid,idlow=idlow,short=short)), 30)
        result[ck]=list(dict.fromkeys(hits))
    return result, grep_paths([pid],40)

semantic_gaps={
 'P01':['candidate intake exists mostly as older live-run/root scripts; missing canonical token_case_manifest accepted by R00','candidate source ranking/watchlist-to-case contract not proven','candidate batch dedupe/snapshot-time rule needs hard schema'],
 'P02':['Phase01/source_wallet_bot assets exist, but final P02 mapping differs from older P01_data_fact naming','real provider freshness/provenance/field completeness gates not bound into R00 full chain','downstream restricted_models propagation needs dry-run proof'],
 'P03':['wallet entity/same-source logic exists in source_wallet_bot and wallet_structure modules, but P03 final schema must separate entity facts from chip inference','GMGN tag + funding/backflow evidence weights need research-grade model','history recurrence query absorption from legacy reports needs replay index'],
 'P04':['chip structure is core blocking methodology gap: distribution progress, retention, transfer, counterparty pressure not yet a proven business-bound runtime','snapshot-delta model and holder/trade/transfer reconciliation need GPT research','acceptance must test semantic chip conclusions, not only schema presence'],
 'P05':['evidence/counter-evidence plane exists structurally but phase-specific hard negatives and downgrade rules are incomplete','alternative hypothesis format not proven consumed by P06/P07','counter-evidence fields missing in many legacy/runtime outputs'],
 'P06':['scenario recognition exists in older P04/P05 naming; final P06 needs stable taxonomy and transition rules','needs mapping from wallet/chip/evidence facts to scenario without trading leakage','hard negatives and confidence downgrade need GPT research'],
 'P07':['strategy gate must produce six allowed final outputs only; older outputs contain WATCH/PAPER_READY-like terms in paper systems but need canonical gate schema','gate thresholds and no-buy/no-confirm rules need GPT research','must prove P07 consumes P06 only via handoff, not raw reports'],
 'P08':['paper-only safety present, but permission gate/paper runtime invoker must be bound to R00 token_case_manifest and handoff_resolution_record','real execution blockers must fail closed in tests','CPO scheduler not enabled and sample cycles are zero real cycles'],
 'P09':['replay evidence assets exist but full token lifecycle replay from P01-P08 standard outputs is not proven','legacy data can be used read-only but needs absorption matrix and fixture index','review metrics/update candidates must be machine-readable for P10'],
 'P10':['controlled upgrade docs/assets exist but must stay candidate-only; no direct rule mutation','requires governance queue from P09 with evidence bundle/schema diff/acceptance delta','upgrade acceptance must prevent auto-deploy/auto-rule-mutation']
}
research_topics={pid:[] for pid in phase_defs}
research_topics.update({
 'P01':['真实 token/candidate 接入 case manifest 与候选去重/快照冻结模型'],
 'P02':['GMGN/OKX/on-chain 源数据事实字段优先级、缺失降级、污染控制研究'],
 'P03':['钱包实体、同源候选、资金来源/回流/历史复现证据权重模型'],
 'P04':['主导侧筹码结构与派发/保留/转移进度量化模型','holder/trade/transfer/snapshot-delta 一致性与对手盘压力模型'],
 'P05':['证据与反证控制、硬负面规则、替代假设与降级机制'],
 'P06':['交易结构场景识别 taxonomy、阶段转移与反证触发模型'],
 'P07':['paper-only 策略门禁六状态判定规则、阈值、禁止确认条件'],
 'P08':['paper-only 执行风控、权限门、失败关闭和 runtime invocation 模型'],
 'P09':['P01-P08 全链路 replay 字段、偏差归因和样本沉淀模型'],
 'P10':['受控升级候选包、治理审查、规则版本化与防自动突变模型']})
phase_matrix=[]
for pid,(name,goal) in phase_defs.items():
    assets,docs=find_phase_assets(pid)
    block = pid in ['P04','P07','P08']
    phase_matrix.append({
        'phase_id':pid,'phase_name':name,'phase_goal':goal,
        'current_assets':{'documents':docs[:12],'schemas':assets['schema'][:12],'contracts':(assets['input_contract']+assets['output_contract']+assets['handoff_contract'])[:18],'runners':assets['runner_binding'][:12],'data_outputs':assets['runtime_output_model'][:12],'reports':[r for r in existing_reports if pid.lower() in r.lower() or pid in r][:8]},
        'checklist':{'has_phase_goal':'YES' if assets['controller'] or docs else 'NO','has_controller':'YES' if assets['controller'] else 'NO','has_input_contract':'YES' if assets['input_contract'] else 'NO','has_output_contract':'YES' if assets['output_contract'] else 'NO','has_schema':'YES' if assets['schema'] else 'NO','has_runtime_output_model':'YES' if assets['runtime_output_model'] else 'NO','has_runner_binding':'YES' if assets['runner_binding'] else 'NO','has_trace_requirements':'YES' if assets['trace_requirements'] else 'NO','has_acceptance_criteria':'YES' if assets['acceptance_criteria'] else 'NO','has_handoff_contract':'YES' if assets['handoff_contract'] else 'NO','r00_schedulable':'NO_PROOF','downstream_consumable':'PARTIAL_STRUCTURAL_PROOF_ONLY','p09_replay_ready':'PARTIAL_REPLAY_ASSETS_EXIST_NOT_FULL_CHAIN_PROVEN'},
        'missing_preparation':{'methodology_missing':semantic_gaps[pid][:2],'data_model_missing':[g for g in semantic_gaps[pid] if 'model' in g.lower() or '模型' in g],'field_missing':['phase-specific required/optional/forbidden field catalog with provenance and missing policy'],'schema_missing':[] if assets['schema'] else ['canonical schema file'],'contract_missing':[] if assets['input_contract'] and assets['output_contract'] else ['input/output contract'],'runner_missing':['business-bound runner binding proof in R00 full token dry-run'] + ([] if assets['runner_binding'] else ['phase runner']),'trace_missing':['trace id propagation from input -> output -> handoff -> P09 replay'],'acceptance_missing':['semantic acceptance fixtures proving output correctness, not only file existence'],'handoff_missing':['R00 handoff_resolution_record binding and downstream consumption evidence'],'p09_review_missing':['phase output replay fixture and review metrics mapping'],'p10_upgrade_missing':['candidate-only upgrade packet fields and governance queue binding']},
        'gpt_research_needed':[{'research_topic':t,'reason':'methodology/semantic model is not safely inferable from wrapper files','expected_output':'methodology_summary, field_model, calculation_logic, evidence_rules, counter_evidence_rules, schema_candidate, acceptance_candidate, Pxx patch suggestion'} for t in research_topics[pid]],
        'her_build_needed':[{'task':f'Complete {pid} canonical schema/contract/runner/trace/acceptance/handoff binding after research where needed','target_file':f'/root/sikk-gmgn/system/phase_controllers/{pid.lower()}_* and modules/stable_trader_os/{pid.lower()}_*','acceptance':'pytest + R00 paper-only dry-run writes standard handoff and P09 replay packet'}],
        'stage_status':'STAGE_BLOCKED' if block else 'STAGE_READY_WITH_GAPS'
    })

capabilities=[
 ('REAL_TOKEN_INPUT','PARTIAL','token candidates/runtime_outputs exist but canonical R00 token_case_manifest is blocking','GPT_RESEARCH_001','HER_BUILD_001','BLOCKING'),
 ('STAGED_FACT_COLLECTION','PARTIAL','source_wallet_bot/Phase01 exists; final P02 naming and R00 binding need proof','GPT_RESEARCH_002','HER_BUILD_002','HIGH'),
 ('WALLET_STRUCTURE_REASONING','PARTIAL','wallet facts/intel exist; entity vs inference boundary and replay absorption need hard contracts','GPT_RESEARCH_003','HER_BUILD_003','HIGH'),
 ('CHIP_STRUCTURE_REASONING','DOCUMENT_ONLY','core semantic chip lifecycle/distribution-progress model not proven business-bound','GPT_RESEARCH_004','HER_BUILD_004','BLOCKING'),
 ('EVIDENCE_COUNTER_EVIDENCE_CONTROL','PARTIAL','generic evidence assets exist; phase-specific counter-evidence not fully wired','GPT_RESEARCH_005','HER_BUILD_005','BLOCKING'),
 ('SCENARIO_RECOGNITION','PARTIAL','scenario runners/wrappers exist; stable taxonomy and semantic replay missing','GPT_RESEARCH_006','HER_BUILD_006','HIGH'),
 ('STRATEGY_GATE_DECISION','PARTIAL','gate assets exist but final six-output schema/thresholds/negative rules need research and tests','GPT_RESEARCH_007','HER_BUILD_007','BLOCKING'),
 ('PAPER_ONLY_EXECUTION_RISK','PARTIAL','safety audit PASS but paper runtime invoker and permission gate not fully R00-bound','GPT_RESEARCH_008','HER_BUILD_008','BLOCKING'),
 ('REVIEW_REPLAY','PARTIAL','replay evidence exists; full P01-P08 lifecycle replay and legacy fixture index missing','GPT_RESEARCH_009','HER_BUILD_009','HIGH'),
 ('CONTROLLED_SELF_UPGRADE','PARTIAL','P10 assets exist; candidate-only governance queue and no-auto-upgrade tests need proof','GPT_RESEARCH_010','HER_BUILD_010','HIGH'),
 ('R00_RUNTIME_ORCHESTRATION','NOT_CONNECTED','known blockers: token_case_manifest and handoff_resolution_record; no full real-token paper dry-run proof','GPT_RESEARCH_011','HER_BUILD_011','BLOCKING'),
 ('CPO_SAMPLE_ACCUMULATION','NOT_CONNECTED','CPO_READY_WITH_GAPS: scheduler not enabled, zero real cycles, I05 not live verified','GPT_RESEARCH_012','HER_BUILD_012','BLOCKING')]
total_goal_gap_matrix={'generated_at':now,'scan_root':str(root),'total_goal':'真实代币数据在 HER 总控闭环下按 P01-P10 完成阶段化事实、结构推理、证据反证、场景、策略门禁、paper-only runtime、P09复盘、P10受控升级，最终输出 EXCLUDE/RECORD/RISK_MONITOR/WATCH/PAPER_READY/READY_FOR_CONFIRMATION。','safety_boundary':['read-only scan except writing reports','no real trading','no wallet signing','no auto order','no auto deploy','legacy data read-only'],'scanned_scope':{s:sum(1 for f in files if f['rel'].startswith(s+'/')) for s in scan_scope},'required_capability':[{'capability':c,'current_status':st,'missing_parts':[miss],'required_gpt_research':[gpt],'required_her_build':[her],'priority':pri} for c,st,miss,gpt,her,pri in capabilities], 'control_plane_status':plane_status, 'overall_status':'R00_REQUIRED_WITH_PAPER_ONLY_GAPS'}

method_loop_gap_matrix={'generated_at':now,'method_loop_gap_matrix':[
 {'method_loop_step':'GOAL_DEFINITION','current_status':'COMPLETE','missing_reason':'final goal now explicit but must be persisted into R00 acceptance context','required_research_topic':'None','required_system_patch':'bind total_goal into R00/P00 acceptance context'},
 {'method_loop_step':'STRUCTURE_BREAKDOWN','current_status':'PARTIAL','missing_reason':'P01-P10 exists but older phase naming conflicts with final target mapping','required_research_topic':'phase mapping normalization research','required_system_patch':'create phase_alias_map and migration note'},
 {'method_loop_step':'MECHANISM_EXTRACTION','current_status':'WEAK','missing_reason':'core chip/scenario/gate mechanisms are not fully extracted into formulas and hard negatives','required_research_topic':'P04/P05/P06/P07 deep research','required_system_patch':'convert research into field/schema/contracts'},
 {'method_loop_step':'PHASE_MAPPING','current_status':'PARTIAL','missing_reason':'K/I/R/CPO mappings exist but final P01-P10 business flow not fully R00-bound','required_research_topic':'R00 runtime chain research','required_system_patch':'R00 stage chain manifest'},
 {'method_loop_step':'DATA_OBJECTIZATION','current_status':'WEAK','missing_reason':'token_case_manifest/handoff_resolution_record missing; many docs not objectized','required_research_topic':'case/handoff/replay object model research','required_system_patch':'schemas + writers + validators'},
 {'method_loop_step':'SYSTEM_IMPLEMENTATION','current_status':'PARTIAL','missing_reason':'standard-stage wrappers exist; semantic business-bound runners incomplete','required_research_topic':'runner binding research','required_system_patch':'business runner adapters and tests'},
 {'method_loop_step':'ACCEPTANCE_FEEDBACK','current_status':'PARTIAL','missing_reason':'file-existence acceptance exists; semantic acceptance and sample-cycle proof weak','required_research_topic':'semantic acceptance methodology','required_system_patch':'fixtures and acceptance evidence packets'},
 {'method_loop_step':'REVIEW_UPGRADE','current_status':'PARTIAL','missing_reason':'P09/P10 candidate docs exist; full replay-to-governance loop unproven','required_research_topic':'review/upgrade governance research','required_system_patch':'P09 metrics -> P10 queue writer'}]}

queue_titles=[
('GPT_RESEARCH_001','R00_token_case_manifest_and_handoff_resolution_blocker','R00 真实 token paper-only 全链路运行对象模型研究','如何定义 token_case_manifest、handoff_resolution_record、phase_chain_manifest、P08 permission gate 与 P09 trigger，使 R00 能安全跑真实 token 的 paper-only dry-run？','BLOCKING'),
('GPT_RESEARCH_002','P04_chip_structure_missing_distribution_progress_model','主导侧筹码结构与派发进度量化模型研究','如何根据 GMGN 钱包、成交、持仓、价格、成交量、transfer/snapshot delta 构建筹码保留、转移、派发进度、对手盘压力判断模型？','BLOCKING'),
('GPT_RESEARCH_003','P05_counter_evidence_control_missing','证据与反证控制模型研究','如何为钱包/筹码/场景/门禁建立证据、反证、替代假设、硬负面与降级机制？','BLOCKING'),
('GPT_RESEARCH_004','P07_strategy_gate_six_status_model_missing','paper-only 策略门禁六状态模型研究','如何从 P01-P06 标准输出生成 EXCLUDE/RECORD/RISK_MONITOR/WATCH/PAPER_READY/READY_FOR_CONFIRMATION，并定义禁止确认条件？','BLOCKING'),
('GPT_RESEARCH_005','P08_paper_permission_and_risk_runtime_missing','P08 paper-only 权限与执行风控模型研究','如何让 paper runtime 只能在权限门内运行，并对真实交易字段 fail-closed？','BLOCKING'),
('GPT_RESEARCH_006','P02_source_data_fact_quality_model','源数据事实质量门禁与污染控制研究','如何定义 GMGN/OKX/on-chain 字段优先级、缺失降级、快照时间、restricted_models？','HIGH'),
('GPT_RESEARCH_007','P03_wallet_entity_same_source_model','钱包实体与同源候选证据模型研究','如何结合 funding、backflow、GMGN tag、历史地址复现输出钱包实体候选与置信度？','HIGH'),
('GPT_RESEARCH_008','P06_scenario_recognition_taxonomy','交易结构场景识别 taxonomy 研究','如何从钱包实体、筹码结构、证据反证映射到可复盘场景候选？','HIGH'),
('GPT_RESEARCH_009','P09_review_replay_field_model','P09 全链路复盘回放字段模型研究','P01-P08 哪些字段必须进入 replay，如何做偏差归因和样本沉淀？','HIGH'),
('GPT_RESEARCH_010','P10_controlled_upgrade_governance_model','P10 受控升级治理模型研究','如何把 P09 复盘结果变成候选升级包并禁止自动突变正式规则？','HIGH'),
('GPT_RESEARCH_011','CPO_stable_sample_accumulation_model','CPO 稳定连续 paper-only 样本积累模型研究','如何定义 scheduler、cycle manifest、sample library、I05 readiness 与停止条件？','BLOCKING')]
gpt_queue=[]
for rid,source,title,q,pri in queue_titles:
    gpt_queue.append({'research_id':rid,'source_gap':source,'research_title':title,'research_question':q,'expected_gpt_output':['methodology_summary','field_model','calculation_logic','evidence_rules','counter_evidence_rules','schema_candidate','contract_candidate','acceptance_candidate','hard_negative_rules','runner_R00_binding_suggestion','P09_replay_fields','P10_upgrade_candidate_fields','HER_build_task_book'],'priority':pri})
gpt_research_queue={'generated_at':now,'gpt_research_queue':gpt_queue}

her_queue=[]
for i,item in enumerate(gpt_queue,1):
    layer='R00' if 'R00' in item['source_gap'] else item['source_gap'].split('_')[0]
    her_queue.append({'task_id':f'HER_BUILD_{i:03d}','source_research_id':item['research_id'],'target_layer':layer,'target_files':[f'/root/sikk-gmgn/system/phase_controllers/{layer.lower()}_*/',f'/root/sikk-gmgn/schemas/stable_trader_os/{layer.lower()}_runtime/*.schema.json',f'/root/sikk-gmgn/contracts/stable_trader_os/{layer.lower()}_runtime/*.contract.json',f'/root/sikk-gmgn/modules/stable_trader_os/{layer.lower()}_*/runtime_entry.py',f'/root/sikk-gmgn/tests/stable_trader_os/test_{layer.lower()}_*.py'], 'build_action':['create_or_update_schema','update_contract','bind_runner','add_trace_writer','add_acceptance_fixture','bind_handoff','bind_p09_replay'], 'acceptance_command':'cd /root/sikk-gmgn && PYTHONPATH=/root/sikk-gmgn pytest -q tests/stable_trader_os/ && python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --token <TOKEN> --dry-run'})
her_build_queue={'generated_at':now,'her_build_queue':her_queue}

r00_runtime_blocker_matrix={'generated_at':now,'r00_runtime_blocker_matrix':[
 {'blocker_id':'R00-BLOCKER-001','blocker_type':'MISSING_PHASE_RUNNER','affected_flow':['SINGLE_TOKEN_ANALYSIS','BATCH_CANDIDATE_RANKING'],'severity':'BLOCKING','evidence':['reports/system_rescan/r00_required_fix_task_packet.md lines 10-12'],'why_blocks':'R00 cannot create token_case_manifest for real token/candidate batch, so downstream phases lack frozen case identity and source paths.','fix_route':'R00_IMPLEMENTATION'},
 {'blocker_id':'R00-BLOCKER-002','blocker_type':'MISSING_HANDOFF','affected_flow':['SINGLE_TOKEN_ANALYSIS','REVIEW_UPGRADE'],'severity':'BLOCKING','evidence':['reports/system_rescan/r00_required_fix_task_packet.md lines 10-12'],'why_blocks':'handoff_resolution_record is missing, so R00 cannot prove which phase output is consumed by which downstream phase or by P09.','fix_route':'HER_BUILD_DIRECT'},
 {'blocker_id':'R00-BLOCKER-003','blocker_type':'MISSING_SCHEMA','affected_flow':['SINGLE_TOKEN_ANALYSIS','BATCH_CANDIDATE_RANKING'],'severity':'HIGH','evidence':['token_case_manifest and handoff_resolution schema listed as files to create'],'why_blocks':'standard objects have no enforced fields for source_path, trace_id, phase_id, snapshot_time, permission status.','fix_route':'STAGE_COMPLETION_PROGRAM'},
 {'blocker_id':'R00-BLOCKER-004','blocker_type':'MISSING_P08_PERMISSION_GATE','affected_flow':['CURRENT_GMGN_POOL','SINGLE_TOKEN_ANALYSIS'],'severity':'BLOCKING','evidence':['CPO validation status CPO_READY_WITH_GAPS; P08 invoker not proven in full R00 chain'],'why_blocks':'paper-only permission may exist as wrapper but not proven as fail-closed gate before runtime invocation.','fix_route':'GPT_RESEARCH_FIRST'},
 {'blocker_id':'R00-BLOCKER-005','blocker_type':'MISSING_PAPER_RUNTIME_INVOKER','affected_flow':['CURRENT_GMGN_POOL','BATCH_CANDIDATE_RANKING'],'severity':'BLOCKING','evidence':['CPO non_blocking_gaps: scheduler runner not enabled, sample library zero real cycles'],'why_blocks':'CPO cannot continuously accumulate stable paper samples without scheduler/cycle manifest and paper invoker binding.','fix_route':'R00_IMPLEMENTATION'},
 {'blocker_id':'R00-BLOCKER-006','blocker_type':'MISSING_P09_TRIGGER','affected_flow':['REVIEW_UPGRADE'],'severity':'HIGH','evidence':['P09 replay assets exist but no full P01-P08 lifecycle replay proof'],'why_blocks':'paper outcomes cannot reliably enter replay/review and P10 upgrade queue.','fix_route':'STAGE_COMPLETION_PROGRAM'},
 {'blocker_id':'R00-BLOCKER-007','blocker_type':'MISSING_CPO_UPDATE','affected_flow':['CURRENT_GMGN_POOL'],'severity':'BLOCKING','evidence':['data/operational_program/continuous_paper_operation/acceptance/cpo_validation_result.yaml status CPO_READY_WITH_GAPS'],'why_blocks':'I05 readiness not live-verified, scheduler disabled, zero real paper cycles.','fix_route':'GPT_RESEARCH_FIRST'}],
 'answer_current_r00_cannot_run_real_token':'Because token_case_manifest and handoff_resolution_record are missing, P08 permission/paper invoker are not proven in the R00 chain, semantic P04/P05/P07 outputs are not research-complete, and P09/P10 triggers are not full-chain replay-bound.',
 'answer_cpo_cannot_stable_paper_only':'Because CPO is READY_WITH_GAPS: scheduler runner not enabled, I05 readiness not live verified, sample library has zero real cycles, and paper runtime invocation is not attached to R00 case/handoff objects.'}

legacy_absorption={
 'old_scripts_should_absorb':[
   {'path':'sikk_paper_live_runner.py','absorb_to':'P08/CPO paper runtime invoker','mode':'read-only reference then adapter wrapper','risk':'root legacy script; do not make new primary root'},
   {'path':'sikk_paper_trading_engine.py','absorb_to':'P08 paper-only execution model','mode':'extract paper order/state fields only; forbid real trade fields','risk':'paper-only extraction; must not expose real execution'},
   {'path':'sikk_ca_runtime_pipeline.py','absorb_to':'R00 candidate/token pipeline','mode':'extract candidate intake and phase ledger concepts','risk':'legacy compat only; no new root runtime writes'},
   {'path':'sikk_wallet_structure_consume_runtime_registry.py','absorb_to':'P03/P04 wallet/chip runtime binding','mode':'extract registry mapping and consume policies','risk':'must keep wallet facts separate from behavior inference'},
   {'path':'scripts/backup_* and migrate_intel_bot_legacy_data.py','absorb_to':'P09 legacy replay fixture index','mode':'read-only legacy data importer/indexer','risk':'do not overwrite legacy data'},
   {'path':'scripts/validate_p10_related_issue_auto_flow.py','absorb_to':'P10 controlled upgrade acceptance','mode':'extract governance/issue automation checks; no auto deploy','risk':'candidate-only governance; no auto mutation'}],
 'old_data_can_replay':[
   {'path':'runtime_outputs/*/phase_evidence/','use':'P01-P10 phase replay fixtures and trace completeness checks','condition':'read-only; validate against new contracts'},
   {'path':'data/stable_trader_os/replay_evidence/A03_A06_A08_20260514/','use':'semantic replay baseline for P02-P10/I stages','condition':'read-only fixture'},
   {'path':'data/source_wallet_bot/','use':'P02/P03 source wallet facts and data quality fixtures','condition':'must run index-fact-store; no inference contamination'},
   {'path':'data/gmgn_candidates_live_run','use':'legacy candidate/paper runtime observation corpus','condition':'legacy compat only; not new primary write root'},
   {'path':'knowledge/extracted_rules and passports','use':'K00-K08 candidate research/material assets','condition':'must go through K00 assetization before system patch'},
   {'path':'reports/stable_trader_os/*','use':'audit evidence and gap regression checks','condition':'do not treat report prose as implemented function'}]}

def dump_yaml(obj, path):
    if yaml:
        path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False), encoding='utf-8')
    else:
        path.write_text(json.dumps(obj,ensure_ascii=False,indent=2), encoding='utf-8')

dump_yaml(total_goal_gap_matrix,out/'total_goal_gap_matrix.yaml')
dump_yaml({'generated_at':now,'phase_goal_gap_matrix':phase_matrix},out/'phase_goal_gap_matrix.yaml')
dump_yaml(method_loop_gap_matrix,out/'method_loop_gap_matrix.yaml')
dump_yaml(gpt_research_queue,out/'gpt_research_queue.yaml')
dump_yaml(her_build_queue,out/'her_build_queue.yaml')
dump_yaml(r00_runtime_blocker_matrix,out/'r00_runtime_blocker_matrix.yaml')

(out/'next_research_batch_prompt.md').write_text("""# Next GPT Research Batch Prompt

任务：根据 HER_DOC Full Trading System Goal Gap Scan 输出的 BLOCKING 缺口，进行可落地深研。不要总结，不要泛泛建议，必须输出可进入 K00 资产化的系统资料。

优先批次：
1. GPT_RESEARCH_001 — R00 token_case_manifest + handoff_resolution_record + paper-only runtime chain
2. GPT_RESEARCH_002 — P04 主导侧筹码结构与派发/保留/转移进度模型
3. GPT_RESEARCH_003 — P05 证据与反证控制模型
4. GPT_RESEARCH_004 — P07 六状态 strategy gate 模型
5. GPT_RESEARCH_005 — P08 paper-only 权限门与执行风控模型
6. GPT_RESEARCH_011 — CPO 连续 paper-only 样本积累模型

每个研究题必须输出：
- 核心机制
- 判断逻辑
- 字段模型
- 数据来源
- 计算方法
- 证据规则
- 反证规则
- schema candidate
- contract candidate
- acceptance candidate
- hard negative rules
- runner / R00 binding 建议
- P09 复盘字段
- P10 升级候选字段
- HER 落地任务书

安全边界：paper-only；禁止真实交易、私钥、签名、broadcast、swap、auto order、auto deploy。

引用输入文件：/root/sikk-gmgn/reports/her_doc_full_system_gap_scan/gpt_research_queue.yaml
""",encoding='utf-8')
(out/'next_her_build_task_packet.md').write_text("""# Next HER Build Task Packet

任务：只在 GPT 深研回填并完成 K00 资产化后，按 Stage Completion Program 补系统对象。当前不要直接补交易逻辑。

优先落地顺序：
1. R00 runtime objects: token_case_manifest.schema/contract/writer + handoff_resolution_record.schema/contract/writer
2. R00 plane-aware paper-only dry-run: phase_chain_manifest + P08 permission gate + P09 trigger candidate
3. P04 chip_structure schema/contract/semantic fixture after GPT research
4. P05 evidence_counter_evidence schema/contract/hard-negative fixture
5. P07 six-status strategy_gate schema/acceptance fixture
6. P08 paper-only invoker fail-closed tests
7. P09 replay packet + legacy fixture index
8. CPO cycle_manifest + scheduler dry-run + sample library writer

禁止：真实交易、wallet signing、auto order、auto deploy、把解释性文档当落地、把 legacy runtime 设为新主写路径。

验收命令候选：
```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn pytest -q tests/stable_trader_os/
python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --token <TOKEN> --dry-run
python -m modules.stable_trader_os.r00_plane_aware_runtime_orchestrator --mode paper_only --batch-candidates --limit 10 --dry-run
```

引用输入文件：
- /root/sikk-gmgn/reports/her_doc_full_system_gap_scan/her_build_queue.yaml
- /root/sikk-gmgn/reports/her_doc_full_system_gap_scan/r00_runtime_blocker_matrix.yaml
""",encoding='utf-8')

report=f"""# HER_DOC Full Trading System Goal Gap Scan Report

Generated: {now}
Scan root: `/root/sikk-gmgn`
Output dir: `{out}`

## Safety Boundary
- This was a read-only system scan except writing this report package.
- No real trading, wallet signing, broadcast, swap, auto order, or auto deploy was performed.
- Legacy scripts/data/reports are treated as read-only sources for absorption/replay planning.
- Explanatory documents are not counted as implemented runtime unless a schema/contract/runner/output/acceptance path is also present.

## Scan Coverage
- system: {total_goal_gap_matrix['scanned_scope'].get('system',0)} files
- docs: {total_goal_gap_matrix['scanned_scope'].get('docs',0)} files
- research_loop: {total_goal_gap_matrix['scanned_scope'].get('research_loop',0)} files
- knowledge: {total_goal_gap_matrix['scanned_scope'].get('knowledge',0)} files
- modules: {total_goal_gap_matrix['scanned_scope'].get('modules',0)} files
- tools: {total_goal_gap_matrix['scanned_scope'].get('tools',0)} files
- scripts: {total_goal_gap_matrix['scanned_scope'].get('scripts',0)} files
- data: {total_goal_gap_matrix['scanned_scope'].get('data',0)} files
- reports: {total_goal_gap_matrix['scanned_scope'].get('reports',0)} files
- tests: {total_goal_gap_matrix['scanned_scope'].get('tests',0)} files

## Overall Decision
Current full-system status: **R00_REQUIRED_WITH_PAPER_ONLY_GAPS**.

The system has substantial standard-stage closure assets, phase controllers, contracts, schemas, replay evidence, and paper-only safety boundaries. However it is not yet ready for stable real-token paper-only operation because the final target requires business-bound semantic runtime, not only wrapper/file completeness.

## Direct Answers to Final Acceptance Questions

### 1. 总目标还差哪些准备？
- R00 must create and validate `token_case_manifest` for real token/candidate batches.
- R00 must create `handoff_resolution_record` proving which phase output feeds each downstream phase.
- P04/P05/P07 semantic models need GPT research before safe implementation: chip structure, counter-evidence, six-state strategy gate.
- P08 paper-only permission gate must be fail-closed and bound before paper runtime invocation.
- P09 must replay the full P01-P08 lifecycle from standard outputs, not reports.
- P10 must accept only candidate upgrade packets through governance, with no auto-rule mutation.
- CPO needs scheduler/cycle manifest/sample library; current status is READY_WITH_GAPS.

### 2. 每个阶段目标还差哪些准备？
See `phase_goal_gap_matrix.yaml`. Summary:
- P01: missing canonical candidate/token case manifest and batch dedupe/snapshot freeze.
- P02: source data facts exist but final P02/R00 binding and restricted model propagation need proof.
- P03: wallet entity/same-source model must separate fact, candidate entity, and chip inference.
- P04: blocking chip structure/distribution progress semantic model missing.
- P05: phase-specific evidence/counter-evidence hard negatives and downgrade schema incomplete.
- P06: scenario taxonomy and transition rules need semantic research and replay acceptance.
- P07: final six-status gate schema, thresholds, and hard negative rules incomplete.
- P08: paper-only safety exists, but permission gate + runtime invoker + R00 binding incomplete.
- P09: replay assets exist, but full standard-output lifecycle replay is unproven.
- P10: upgrade assets exist, but candidate-only governance queue and no-auto-mutation tests need proof.

### 3. 哪些缺口需要 GPT 深研？
See `gpt_research_queue.yaml`. Blocking research first:
- R00 token case/handoff/paper runtime chain.
- P04 chip structure and distribution progress.
- P05 evidence/counter-evidence.
- P07 strategy gate six-status decision model.
- P08 paper-only permission and execution risk.
- CPO continuous paper sample accumulation.

### 4. 哪些缺口可以 HER 直接落地？
See `her_build_queue.yaml`. Direct HER work after research/K00 as needed:
- Create schemas/contracts/writers for token_case_manifest and handoff_resolution_record.
- Bind R00 paper-only dry-run to P01-P10 phase chain manifest.
- Add trace writers, handoff validators, and P09 replay packet writers.
- Add semantic acceptance fixtures once GPT supplies field/rule candidates.
- Add CPO cycle manifest/sample library writer and scheduler dry-run guard.

### 5. 哪些旧脚本应该吸收？
"""
for x in legacy_absorption['old_scripts_should_absorb']:
    report += f"- `{x['path']}` → {x['absorb_to']}; mode: {x['mode']}; risk: {x['risk']}\n"
report += "\n### 6. 哪些旧数据可以复盘使用？\n"
for x in legacy_absorption['old_data_can_replay']:
    report += f"- `{x['path']}` → {x['use']}; condition: {x['condition']}\n"
report += """

### 7. R00 真实 token 运行被什么阻断？
- `MISSING_PHASE_RUNNER/token_case_manifest`: no canonical real-token case object.
- `MISSING_HANDOFF/handoff_resolution_record`: downstream consumption cannot be proven.
- `MISSING_P08_PERMISSION_GATE`: paper-only permission must be bound into R00 before invocation.
- `MISSING_PAPER_RUNTIME_INVOKER`: paper runtime is not stable continuous R00 chain.
- `MISSING_P09_TRIGGER`: full lifecycle replay/update trigger not proven.
- Semantic blockers: P04 chip, P05 counter-evidence, P07 gate rules are not yet research-complete.

### 8. 下一批应该发给 GPT 研究的题目是什么？
Use `next_research_batch_prompt.md`. First batch: R00 runtime objects, P04 chip structure, P05 evidence/counter-evidence, P07 strategy gate, P08 paper-only risk, CPO sample accumulation.

### 9. 下一批应该发给 HER 落地的任务是什么？
Use `next_her_build_task_packet.md`. First build packet: R00 token_case_manifest + handoff_resolution_record + paper-only dry-run chain; then P04/P05/P07/P08/P09/CPO after GPT/K00 assetization.

## Why R00 Cannot Run Real Token Now
R00 has safety wrappers and standard-stage assets, but a real token run needs a frozen `token_case_manifest`, explicit source paths, trace ids, phase chain ordering, handoff resolution, P08 permission decision, paper runtime invocation, P09 replay packet, and P10 candidate-upgrade handoff. The existing `reports/system_rescan/r00_required_fix_task_packet.md` already identifies `token_case_manifest` and `handoff_resolution_record` as blocking runtime objects. Therefore real token paper-only runtime must remain blocked until those objects and semantic phase outputs are proven.

## Why CPO Cannot Stable Continuous Paper-only Now
The CPO validation file reports `CPO_READY_WITH_GAPS`: I05 readiness is not live-verified, scheduler runner is not enabled, and sample library has zero real cycles. That means CPO can be designed/validated structurally, but cannot yet claim stable continuous paper-only sample accumulation.

## Output Files
- `total_goal_gap_matrix.yaml`
- `phase_goal_gap_matrix.yaml`
- `method_loop_gap_matrix.yaml`
- `gpt_research_queue.yaml`
- `her_build_queue.yaml`
- `r00_runtime_blocker_matrix.yaml`
- `full_trading_system_gap_scan_report.md`
- `next_research_batch_prompt.md`
- `next_her_build_task_packet.md`

## Recommended Next Loop
HER_DOC scan → GPT deep research → K00 assetization → stage_completion_program → R00 paper-only validation.
"""
(out/'full_trading_system_gap_scan_report.md').write_text(report,encoding='utf-8')
summary={'generated_at':now,'output_dir':str(out),'files_written':[p.name for p in sorted(out.iterdir()) if p.is_file()],'scan_file_count':len(files),'legacy_scripts_count':len(legacy_scripts),'root_runtime_scripts':root_runtime_scripts[:30],'legacy_data_roots':legacy_data_roots,'status':'COMPLETED_WITH_R00_AND_CPO_BLOCKERS'}
(out/'run_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
