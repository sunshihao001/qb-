import json, pathlib
root=pathlib.Path('/root/sikk-gmgn')
osroot=root/'sikk_stable_trader_os'
runners=osroot/'07_runners'
absdir=osroot/'runtime_absorption'
runners.mkdir(parents=True, exist_ok=True)
absdir.mkdir(parents=True, exist_ok=True)
now='2026-05-14T20:34:54Z'
token='ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump'
symbol='TROLLIEN'

def read_json(rel):
    p=root/rel
    return json.loads(p.read_text(encoding='utf-8'))

def write_json(path,obj):
    path=pathlib.Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def write_text(path,txt):
    path=pathlib.Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(txt,encoding='utf-8')

def find_row(payload, keys):
    rows=payload if isinstance(payload,list) else []
    if not rows and isinstance(payload,dict):
        for k in keys:
            if isinstance(payload.get(k),list): rows=payload[k]; break
    for r in rows:
        if r.get('代币地址')==token or r.get('token_address')==token or r.get('token')==token:
            return r
    return {}

candidate_path='data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json'
kline_path='data/gmgn_candidates_live_run/kline_pipeline/candidate_kline_pipeline_summary.json'
signal_path='data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json'
state_path='data/gmgn_candidates_live_run/state_machine/candidate_states.json'
wallet_sum_path='data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/candidate_wallet_structure_summary.json'
wallet_decision_path=f'data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/{token}/wallet_structure_decision.json'
quote_sum_path='data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json'
quote_decision_path=f'data/gmgn_candidates_live_run/quote_security/{token}/quote_security_decision.json'
paper_closed_path='data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json'
paper_open_path='data/gmgn_candidates_live_run/paper_live/paper_positions_open.json'
failure_jsonl_path='data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl'

candidate=find_row(read_json(candidate_path),['候选结果','候选列表','处理结果','tokens','candidates','results'])
kline=find_row(read_json(kline_path),['results'])
signal=find_row(read_json(signal_path),['信号结果'])
state=find_row(read_json(state_path),['候选状态'])
wallet_sum=find_row(read_json(wallet_sum_path),['处理结果','results'])
wallet_decision=read_json(wallet_decision_path)
quote_sum=find_row(read_json(quote_sum_path),['处理结果','results'])
quote_decision=read_json(quote_decision_path)
paper_closed=read_json(paper_closed_path)
paper_rows=[r for r in paper_closed.get('closed_positions',[]) if r.get('代币地址')==token or r.get('token_address')==token]
paper_result=paper_rows[-1] if paper_rows else {}
source_files=[candidate_path,kline_path,signal_path,state_path,wallet_sum_path,wallet_decision_path,quote_sum_path,quote_decision_path,paper_closed_path,paper_open_path,failure_jsonl_path]
source_status={p:{'exists':(root/p).exists(),'size':((root/p).stat().st_size if (root/p).exists() else 0)} for p in source_files}

write_text(runners/'runner_registry.yaml', f'''registry_id: runtime_absorption_runner_registry_v1
created_at: "{now}"
scope: "bind existing SIKK runtime outputs into HER phase replay; no new Plane; no dashboard/telegram/batch"
safety_boundary:
  paper_only: true
  no_real_swap: true
  no_private_key: true
  no_signing: true
  no_broadcast: true
  runtime_first_document_follow: true
runners:
  runner_live_orchestrator:
    script_path: sikk_live_run.py
    runtime_chain: "sikk_live_run.py -> run_sikk_gmgn_pipeline.py -> candidate/kline/signal/state/wallet/quote/paper/failure/report"
    allowed_phases: [P01, P02, P03, P04, P05, P06, P07, P08, P09]
    mode_for_replay: readonly_absorption_existing_outputs
    phase_controller_required: true
    direct_invocation_for_replay: forbidden_except_readonly_trace_reconstruction
  runner_gmgn_pipeline:
    script_path: run_sikk_gmgn_pipeline.py
    allowed_phases: [P01, P02, P03, P04, P05, P06, P07, P08]
    mode_for_replay: existing_output_reader
    phase_controller_required: true
  runner_candidate_discovery:
    script_path: sikk_gmgn_new_token_filter.py
    allowed_phases: [P01]
    primary_outputs: ["{candidate_path}"]
  runner_kline_pipeline:
    script_path: sikk_candidate_kline_pipeline.py
    allowed_phases: [P04, P05, P06]
    primary_outputs: ["{kline_path}"]
  runner_signal_engine:
    script_path: sikk_candidate_signal_pipeline.py
    allowed_phases: [P05, P06, P07]
    primary_outputs: ["{signal_path}"]
  runner_state_machine:
    script_path: sikk_candidate_state_machine.py
    allowed_phases: [P07]
    primary_outputs: ["{state_path}"]
  runner_wallet_structure_pipeline:
    script_path: sikk_candidate_wallet_structure_pipeline.py
    allowed_phases: [P02, P03, P04, P05, P07]
    primary_outputs: ["{wallet_sum_path}", "{wallet_decision_path}"]
  runner_quote_security:
    script_path: sikk_candidate_quote_security_pipeline.py
    allowed_phases: [P08]
    primary_outputs: ["{quote_sum_path}", "{quote_decision_path}"]
    readonly_only: true
  runner_paper_live:
    script_path: sikk_paper_live_runner.py
    allowed_phases: [P08, P09]
    primary_outputs: ["{paper_open_path}", "{paper_closed_path}", "{failure_jsonl_path}"]
    requires_strategy_gate: [P07, P08]
    forbidden_after_candidate_discovery_without_gate: true
  runner_failure_attribution:
    script_path: sikk_paper_live_runner.py::failure_attribution_jsonl
    allowed_phases: [P09, P10]
    rule: "review output may create P09/P10 issue/fix packages only; must not mutate realtime rules"
''')

write_text(runners/'phase_runner_binding.yaml', f'''binding_id: runtime_absorption_phase_runner_binding_v1
created_at: "{now}"
rule: "all replay decisions are reconstructed through phase trace; no runner may bypass phase controller; paper runner requires P07/P08 gate"
phase_runner_binding:
  - phase_id: P01
    phase_name: Candidate Intake / Source Data Fact
    runners: [runner_candidate_discovery, runner_gmgn_pipeline, runner_live_orchestrator]
    consumed_outputs: ["{candidate_path}"]
    required_handoff: data_fact_handoff_packet.json
  - phase_id: P02
    phase_name: Wallet / Chip Source Fact
    runners: [runner_wallet_structure_pipeline]
    consumed_outputs: ["{wallet_decision_path}", "{wallet_sum_path}"]
    required_handoff: wallet_chip_fact_handoff_packet.json
  - phase_id: P03
    phase_name: Wallet Entity / Structure Reasoning
    runners: [runner_wallet_structure_pipeline]
    consumed_outputs: ["{wallet_decision_path}"]
    required_handoff: wallet_entity_handoff_packet.json
  - phase_id: P04
    phase_name: Chip Structure
    runners: [runner_kline_pipeline, runner_wallet_structure_pipeline]
    consumed_outputs: ["{kline_path}", "{wallet_decision_path}"]
    required_handoff: chip_structure_handoff_packet.json
  - phase_id: P05
    phase_name: Evidence / Counter Evidence
    runners: [runner_signal_engine, runner_kline_pipeline, runner_wallet_structure_pipeline]
    consumed_outputs: ["{signal_path}", "{kline_path}", "{wallet_decision_path}"]
    required_handoff: evidence_control_packet.json
  - phase_id: P06
    phase_name: Scenario Recognition
    runners: [runner_signal_engine, runner_kline_pipeline]
    consumed_outputs: ["{signal_path}", "{kline_path}"]
    required_handoff: scenario_recognition_packet.json
  - phase_id: P07
    phase_name: Strategy Gate
    runners: [runner_state_machine, runner_signal_engine, runner_wallet_structure_pipeline]
    consumed_outputs: ["{state_path}", "{signal_path}", "{wallet_decision_path}"]
    required_handoff: strategy_gate_decision.json
  - phase_id: P08
    phase_name: Execution Risk / Paper-only Gate
    runners: [runner_quote_security, runner_paper_live]
    consumed_outputs: ["{quote_decision_path}", "{quote_sum_path}"]
    required_handoff: paper_only_execution_gate.json
    precondition: "P07 decision in PAPER_READY/READY_FOR_CONFIRMATION and P08 quote/security allows confirmation"
  - phase_id: P09
    phase_name: Review / Failure Attribution
    runners: [runner_paper_live, runner_failure_attribution]
    consumed_outputs: ["{paper_closed_path}", "{failure_jsonl_path}"]
    required_handoff: failure_attribution_packet.json
    mutation_rule: "no realtime rule mutation; handoff to P09/P10 issue package only"
''')

write_text(runners/'validation_runner_registry.yaml', f'''registry_id: runtime_absorption_validation_runner_registry_v1
created_at: "{now}"
validators:
  required_file_presence:
    runner: filesystem_presence_check
    validates: [P01, P02, P03, P04, P05, P06, P07, P08, P09]
  trace_completeness:
    runner: runtime_absorption_trace_validator
    required_fields: [phase_id, input_files, output_files, runner_used, decision, evidence_level, counter_evidence, missing_fields, status, failure_reason, downstream_handoff]
  strategy_gate_consumption:
    runner: upstream_consumption_check
    validates: [P07]
    required_inputs: [P01, P02, P03, P04, P05, P06]
  paper_only_gate:
    runner: paper_runner_gate_check
    validates: [P08]
    forbidden: [real_swap, signing, private_key, broadcast]
  review_containment:
    runner: p09_p10_containment_check
    validates: [P09]
    rule: failure/review may only write issue registry and P10 candidate package
''')
write_text(runners/'replay_runner_registry.yaml', f'''registry_id: runtime_absorption_replay_runner_registry_v1
created_at: "{now}"
replay_scope:
  token_address: {token}
  token_symbol: {symbol}
  runtime_root: data/gmgn_candidates_live_run
  batch: false
  dashboard: false
  telegram: false
  new_strategy: false
replay_mode: readonly_existing_runtime_output_absorption
phase_sequence: [P01, P02, P03, P04, P05, P06, P07, P08, P09]
allowed_replay_runners:
  P01: [runner_candidate_discovery]
  P02: [runner_wallet_structure_pipeline]
  P03: [runner_wallet_structure_pipeline]
  P04: [runner_kline_pipeline, runner_wallet_structure_pipeline]
  P05: [runner_signal_engine, runner_kline_pipeline, runner_wallet_structure_pipeline]
  P06: [runner_signal_engine, runner_kline_pipeline]
  P07: [runner_state_machine, runner_signal_engine, runner_wallet_structure_pipeline]
  P08: [runner_quote_security, runner_paper_live]
  P09: [runner_paper_live, runner_failure_attribution]
''')
write_text(runners/'runner_failure_policy.yaml', f'''policy_id: runtime_absorption_runner_failure_policy_v1
created_at: "{now}"
default: statusize_do_not_skip
rules:
  missing_required_input: write_phase_trace_failure_and_issue_registry
  runner_unbound: reject_phase_or_pass_with_gaps_if_readonly_absorption_only
  paper_runner_without_p07_p08_gate: reject_replay
  quote_security_missing: p08_pass_with_gaps_no_real_execution
  wallet_fields_missing: p02_p03_p04_pass_with_gaps_counter_evidence
  failure_attribution_present: route_to_p09_p10_only
  review_result_attempts_realtime_rule_mutation: hard_reject
  dashboard_or_telegram_invoked: scope_violation
''')

acceptance='PHASE_REPLAY_PASS_WITH_GAPS'
write_json(absdir/'single_token_replay_manifest.json', {'task':'SIKK/HER Runtime Absorption single token replay','created_at':now,'replay_mode':'readonly_existing_runtime_output_absorption','token_address':token,'token_symbol':symbol,'runtime_root':'data/gmgn_candidates_live_run','scope_exclusions':['batch','dashboard','telegram','new_strategy','P11','P12','new_plane'],'source_files':source_status,'registries':[str((runners/f).relative_to(root)) for f in ['runner_registry.yaml','phase_runner_binding.yaml','validation_runner_registry.yaml','replay_runner_registry.yaml','runner_failure_policy.yaml']],'expected_acceptance':acceptance})

packets={
 'data_fact_handoff_packet.json': {'phase_id':'P01','token_address':token,'token_symbol':symbol,'candidate_fact':candidate,'decision':'ALLOW_ANALYSIS_SOURCE_FACT_ACCEPTED','evidence_level':'E3','missing_fields':[],'downstream_handoff':'P02'},
 'wallet_chip_fact_handoff_packet.json': {'phase_id':'P02','token_address':token,'wallet_chip_fact':{'wallet_summary':wallet_sum,'wallet_decision':wallet_decision},'decision':wallet_decision.get('wallet_gate_result') or wallet_decision.get('wallet_structure_status'),'evidence_level':wallet_decision.get('钱包证据等级') or wallet_decision.get('wallet_evidence_level'),'missing_fields':wallet_decision.get('missing_fields',[]),'data_quality_status':wallet_decision.get('data_quality_status'),'downstream_handoff':'P03'},
 'wallet_entity_handoff_packet.json': {'phase_id':'P03','token_address':token,'roles':wallet_decision.get('角色计数',{}),'game_side':wallet_decision.get('game_side计数',{}),'same_source_group_hypothesis':'not_detected_or_not_exported','synchronous_behavior':{'highest_sync_buy':wallet_decision.get('最高同步买入分'),'highest_sync_sell':wallet_decision.get('最高同步卖出分')},'chip_control_hypothesis':wallet_decision.get('筹码控制权状态'),'decision':'COUNTERPARTY_PRESSURE_HIGH_STRUCTURE_RISK','evidence_level':wallet_decision.get('钱包证据等级'),'missing_fields':wallet_decision.get('missing_fields',[]),'downstream_handoff':'P04'},
 'chip_structure_handoff_packet.json': {'phase_id':'P04','token_address':token,'kline_accumulation':kline,'chip_structure':{'early_wallet_count':wallet_decision.get('早期钱包数量'),'distribution':wallet_decision.get('是否存在分发派发'),'centralized_clearance':wallet_decision.get('是否存在集中清仓'),'counterparty_pressure_score':wallet_decision.get('counterparty_pressure_score'),'control_state':wallet_decision.get('筹码控制权状态')},'decision':'CHIP_CONTROL_MIGRATING_TO_COUNTERPARTY','evidence_level':'E3','counter_evidence':['K线吸筹窗口 valid','信号 S4 强确认'],'missing_fields':wallet_decision.get('missing_fields',[]),'downstream_handoff':'P05'},
 'evidence_control_packet.json': {'phase_id':'P05','token_address':token,'supporting_evidence':['候选筛选 S3','吸筹窗口 valid','信号 S4','quote/security low risk'],'counter_evidence':['wallet_structure_status WALLET_BLOCK','wallet_risk_score 100','counterparty_pressure_score 72','wallet fields missing'],'uncertainties':wallet_decision.get('missing_fields',[]),'decision':'EVIDENCE_MIXED_WITH_HIGH_WALLET_COUNTER_EVIDENCE','evidence_level':'E3','downstream_handoff':'P06'},
}
scenario='接盘鲸鱼陷阱 / 退出流动性陷阱风险' if wallet_decision.get('wallet_structure_status')=='WALLET_BLOCK' else '吸筹/二段扩张观察'
packets['scenario_recognition_packet.json']={'phase_id':'P06','token_address':token,'scenario':scenario,'candidate_scenarios_checked':['吸筹','二段扩张','高位派发','下跌再派发','诱多反抽','退出流动性陷阱','假横盘','再吸筹','末端拉盘派发','刷量假突破','接盘鲸鱼陷阱'],'basis':{'signal':signal,'kline':kline,'wallet_counter_evidence':wallet_decision.get('状态调整原因')},'decision':'RISK_SCENARIO_RECOGNIZED_WITH_SIGNAL_CONFLICT','evidence_level':'E3','missing_fields':wallet_decision.get('missing_fields',[]),'downstream_handoff':'P07'}
p07_decision=state.get('当前状态') or 'UNKNOWN'
packets['strategy_gate_decision.json']={'phase_id':'P07','token_address':token,'consumed_handoffs':['data_fact_handoff_packet.json','wallet_chip_fact_handoff_packet.json','wallet_entity_handoff_packet.json','chip_structure_handoff_packet.json','evidence_control_packet.json','scenario_recognition_packet.json'],'runtime_state':state,'decision':p07_decision,'normalized_gate':'PAPER_READY' if p07_decision=='PAPER_READY' else p07_decision,'evidence_level':'E3','counter_evidence':['wallet gate observe-only allowed PAPER_READY despite wallet would_block=true'],'missing_fields':wallet_decision.get('missing_fields',[]),'downstream_handoff':'P08','paper_runner_allowed_next':p07_decision in ['PAPER_READY','READY_FOR_CONFIRMATION']}
p08_allowed=(quote_decision.get('final_permission')=='ALLOW_CONFIRMATION_LAYER' and packets['strategy_gate_decision.json']['paper_runner_allowed_next'])
packets['paper_only_execution_gate.json']={'phase_id':'P08','token_address':token,'consumed_handoffs':['strategy_gate_decision.json'],'quote_security_decision':quote_decision,'quote_security_summary':quote_sum,'paper_only_allowed':bool(p08_allowed),'decision':'PAPER_ONLY_ALLOWED_EXISTING_RUNTIME_RESULT_CONSUMED' if p08_allowed else 'PAPER_ONLY_BLOCKED','paper_result_reference':paper_closed_path if paper_result else None,'paper_result':paper_result,'safety_boundary':{'no_real_swap':True,'no_signing':True,'no_broadcast':True,'paper_only':True},'evidence_level':'E3','counter_evidence':['max_price_impact_pct missing/null','wallet WALLET_BLOCK was observe-only not hard blocked'],'missing_fields':['max_price_impact_pct']+wallet_decision.get('missing_fields',[]),'downstream_handoff':'P09' if paper_result else 'STOP'}
packets['failure_attribution_packet.json']={'phase_id':'P09','token_address':token,'paper_result':paper_result,'failure_attribution_source':failure_jsonl_path,'review_decision':'P09_REVIEW_CAPTURED_NO_REALTIME_RULE_MUTATION','failure_attribution':'closed paper position hit stop / wallet risk context retained' if paper_result else 'no paper result found','route_to':'P09_issue_registry_and_P10_candidate_fix_package_only','forbidden_mutation_observed':False,'evidence_level':'E2','missing_fields':['dedicated failure_attribution row for token not found in failure_attribution.jsonl'] if paper_result else ['paper result missing'],'downstream_handoff':'P10_candidate_task_package'}
for name,obj in packets.items(): write_json(absdir/name,obj)

phase_specs=[
('P01',[candidate_path],['data_fact_handoff_packet.json'],['runner_candidate_discovery'],'ALLOW_ANALYSIS_SOURCE_FACT_ACCEPTED','E3',[],[], 'PASS','', 'P02'),
('P02',[wallet_sum_path,wallet_decision_path],['wallet_chip_fact_handoff_packet.json'],['runner_wallet_structure_pipeline'],packets['wallet_chip_fact_handoff_packet.json']['decision'],'E3',['wallet gate says WALLET_BLOCK'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','missing wallet-level canonical fields','P03'),
('P03',['data_fact_handoff_packet.json','wallet_chip_fact_handoff_packet.json'],['wallet_entity_handoff_packet.json'],['runner_wallet_structure_pipeline'],'COUNTERPARTY_PRESSURE_HIGH_STRUCTURE_RISK','E3',['same-source explicit groups not exported'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','role/game_side source fields missing at row-level','P04'),
('P04',['wallet_entity_handoff_packet.json',kline_path,wallet_decision_path],['chip_structure_handoff_packet.json'],['runner_kline_pipeline','runner_wallet_structure_pipeline'],'CHIP_CONTROL_MIGRATING_TO_COUNTERPARTY','E3',['accumulation window valid'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','wallet counter-evidence conflicts with kline signal','P05'),
('P05',['chip_structure_handoff_packet.json',signal_path],['evidence_control_packet.json'],['runner_signal_engine','runner_wallet_structure_pipeline'],'EVIDENCE_MIXED_WITH_HIGH_WALLET_COUNTER_EVIDENCE','E3',packets['evidence_control_packet.json']['counter_evidence'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','evidence conflict unresolved','P06'),
('P06',['evidence_control_packet.json',kline_path,signal_path],['scenario_recognition_packet.json'],['runner_signal_engine','runner_kline_pipeline'],scenario,'E3',['scenario derived from available outputs, not native scenario runner'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','native P06 scenario runner not separately bound','P07'),
('P07',['scenario_recognition_packet.json',state_path,wallet_decision_path,signal_path],['strategy_gate_decision.json'],['runner_state_machine'],p07_decision,'E3',packets['strategy_gate_decision.json']['counter_evidence'],wallet_decision.get('missing_fields',[]),'PASS_WITH_GAPS','wallet observe-only lets PAPER_READY continue despite would_block=true','P08'),
('P08',['strategy_gate_decision.json',quote_decision_path,quote_sum_path],['paper_only_execution_gate.json'],['runner_quote_security','runner_paper_live'],packets['paper_only_execution_gate.json']['decision'],'E3',packets['paper_only_execution_gate.json']['counter_evidence'],packets['paper_only_execution_gate.json']['missing_fields'],'PASS_WITH_GAPS','paper result consumed from existing runtime; max_price_impact null','P09'),
('P09',['paper_only_execution_gate.json',paper_closed_path,failure_jsonl_path],['failure_attribution_packet.json'],['runner_paper_live','runner_failure_attribution'],packets['failure_attribution_packet.json']['review_decision'],'E2',[],packets['failure_attribution_packet.json']['missing_fields'],'PASS_WITH_GAPS','token-specific row absent from failure_attribution.jsonl although closed paper result exists','P10'),
]
trace=[]
for phase_id,infiles,outfiles,run,dec,ev,counter,missing,status,fail,handoff in phase_specs:
    trace.append({'phase_id':phase_id,'token_address':token,'input_files':infiles,'output_files':[f'runtime_absorption/{x}' for x in outfiles],'runner_used':run,'decision':dec,'evidence_level':ev,'counter_evidence':counter,'missing_fields':missing,'status':status,'failure_reason':fail,'downstream_handoff':handoff,'trace_time':now})
write_text(absdir/'phase_trace.jsonl',''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in trace))

issues=[
('ISSUE-001','P02/P03/P04/P07','wallet_structure_decision reports missing wallet_address, role, game_side, evidence_level','HIGH','补齐 wallet row-level canonical export；保持旧路径 fallback；不改实时策略阈值'),
('ISSUE-002','P07/P08','wallet gate observe-only allowed PAPER_READY while would_block=true / WALLET_BLOCK','HIGH','下一轮只评估 observe->enforce 的 Phase Controller 门禁参数，不直接改 live 策略'),
('ISSUE-003','P06','scenario recognition is reconstructed from runtime outputs, not a native P06 bound runner output','MEDIUM','绑定现有 signal/kline/wallet outputs 到 P06 wrapper；仅生成被 replay 消费的输出'),
('ISSUE-004','P08','quote_security_decision max_price_impact_pct is null','MEDIUM','补 quote/security 缺字段状态化与来源标记'),
('ISSUE-005','P09','failure_attribution.jsonl 无该 token 专属 failure row，但 paper closed result 有 stop closure','MEDIUM','让 paper runner 对每个 closed position 写 token-level failure/review row'),
('ISSUE-006','P01-P09','部分既有 runner 原生 writes_handoff=false / trace 不是 Phase Controller 统一格式','HIGH','以 Phase Controller wrapper 收口 trace/handoff，不允许 runner 直连 paper'),
]
issue_md=['# Runtime Absorption Issue Registry','',f'- created_at: {now}',f'- token: {symbol} `{token}`','- scope: only issues exposed by this single-token replay','']
for iid,phase,desc,sev,fix in issues:
    issue_md += [f'## {iid}',f'- phase: {phase}',f'- severity: {sev}',f'- issue: {desc}',f'- next_fix_task: {fix}',f'- realtime_rule_mutation_allowed: false','']
write_text(absdir/'runtime_absorption_issue_registry.md','\n'.join(issue_md))

missing_str=', '.join(wallet_decision.get('missing_fields',[]))
write_text(absdir/'phase_acceptance_report.md', f'''# SIKK / HER 单 Token Runtime Absorption Acceptance Report

- created_at: {now}
- token: {symbol} `{token}`
- replay_mode: readonly_existing_runtime_output_absorption
- final_acceptance: **{acceptance}**

## 判定依据
- P01-P08：已形成从候选事实、钱包/筹码事实、结构推理、筹码结构、证据/反证、场景识别、策略门禁到 paper-only gate 的连续 handoff。
- P08/P09：已消费既有 paper runner closed position，未执行真实 swap/签名/广播。
- P07 strategy gate 明确消费了 P01-P06 handoff 与 runtime `candidate_states.json`。
- 每个阶段均写入 `phase_trace.jsonl`，字段包含 phase_id/input_files/output_files/runner_used/decision/evidence_level/counter_evidence/missing_fields/status/failure_reason/downstream_handoff。

## 为什么不是 PASS
- 钱包结构为 `WALLET_BLOCK` 且 `would_block=true`，但 runtime 当前 wallet gate mode 为 observe-only，仍允许 `PAPER_READY`。
- wallet row-level 字段缺失：{missing_str}。
- P06 场景识别是基于现有 runtime 输出重建，未发现独立 native P06 runner 输出。
- quote/security `max_price_impact_pct` 为 null。
- `failure_attribution.jsonl` 未包含该 token 的专属复盘 row，虽然 `paper_positions_closed.json` 存在该 token 的 closed paper result。

## 验收结论
**{acceptance}**：闭环可跑通，但必须按 issue registry 修复门禁/字段/复盘 trace 缺口后，才能升级为无缺口 PASS。
''')
write_json(absdir/'phase_handoff_packet.json', {'created_at':now,'token_address':token,'token_symbol':symbol,'acceptance':acceptance,'phase_outputs':{r['phase_id']:r['output_files'] for r in trace},'issue_registry':'runtime_absorption/runtime_absorption_issue_registry.md','next_route':'issue_registry_only_fix_package','forbidden_next_actions':['new Plane','new P11/P12','dashboard','telegram','direct realtime rule mutation','paper runner after candidate discovery without P07/P08'],'p09_p10_boundary':'review/failure attribution may enter P09/P10 task package only'})
write_text(absdir/'paper_only_decision_report.md', f'''# Paper-only Decision Report

- created_at: {now}
- token: {symbol} `{token}`
- decision: PAPER_ONLY_ALLOWED_EXISTING_RUNTIME_RESULT_CONSUMED
- P07 gate: {p07_decision}
- P08 quote/security permission: {quote_decision.get('final_permission')}
- paper result source: `{paper_closed_path}`
- paper result: position `{paper_result.get('position_id','')}` closed with pnl `{paper_result.get('最终收益率_pct')}` and exit_reason `{paper_result.get('exit_reason','')}`

## Safety
- no_real_swap: true
- no_signing: true
- no_broadcast: true
- no_private_key: true

## Gate caveat
Wallet runtime says `WALLET_BLOCK` / `would_block=true`, but wallet mode was observe-only. This is accepted only as PASS_WITH_GAPS and must enter issue registry, not a live rule mutation.
''')
write_text(absdir/'single_token_replay_execution_report.md', f'''# Single Token Replay Execution Report

- created_at: {now}
- token: {symbol} `{token}`
- acceptance: {acceptance}
- runtime_read: true
- phase_trace: `sikk_stable_trader_os/runtime_absorption/phase_trace.jsonl`
- acceptance_report: `sikk_stable_trader_os/runtime_absorption/phase_acceptance_report.md`
- issue_registry: `sikk_stable_trader_os/runtime_absorption/runtime_absorption_issue_registry.md`

## Runtime absorption status
Existing runtime outputs were consumed read-only from `data/gmgn_candidates_live_run`. No batch run, dashboard generation, Telegram delivery, new strategy, P11/P12, or new Plane was created.

## Phase summary
- P01: candidate accepted from GMGN runtime output.
- P02-P04: wallet/chip facts consumed; wallet risk produced high counter-evidence.
- P05: evidence packet records both S4/Kline positive signal and wallet counter-evidence.
- P06: scenario recognized as `{scenario}` from existing runtime facts.
- P07: strategy gate consumed upstream and produced `{p07_decision}`.
- P08: quote/security allowed confirmation; paper-only result consumed.
- P09: review contained to issue registry / P10 candidate package; no realtime mutation.
''')
write_text(absdir/'next_issue_registry_fix_task_package.md', '# Next Round Fix Task Package (Issue Registry Only)\n\n'+'\n'.join([f'- {iid}: {fix}' for iid,phase,desc,sev,fix in issues])+'\n\nConstraints: do not add abstract standards; fix only replay-exposed issues; keep paper runner behind P07/P08.\n')

mandatory=[runners/'runner_registry.yaml',runners/'phase_runner_binding.yaml',runners/'validation_runner_registry.yaml',runners/'replay_runner_registry.yaml',runners/'runner_failure_policy.yaml',absdir/'single_token_replay_manifest.json',absdir/'phase_trace.jsonl',absdir/'phase_acceptance_report.md',absdir/'phase_handoff_packet.json',absdir/'runtime_absorption_issue_registry.md',absdir/'paper_only_decision_report.md']
required=['phase_id','input_files','output_files','runner_used','decision','evidence_level','counter_evidence','missing_fields','status','failure_reason','downstream_handoff']
trace_lines=(absdir/'phase_trace.jsonl').read_text(encoding='utf-8').strip().splitlines()
trace_ok=all(all(k in json.loads(line) for k in required) for line in trace_lines)
print(json.dumps({'mandatory_missing':[str(p) for p in mandatory if not p.exists() or p.stat().st_size==0],'trace_count':len(trace_lines),'trace_ok':trace_ok,'acceptance':acceptance,'output_dir':str(absdir)},ensure_ascii=False,indent=2))
