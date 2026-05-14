import json, pathlib, sys
root=pathlib.Path('/root/sikk-gmgn')
osroot=root/'sikk_stable_trader_os'
runners=osroot/'07_runners'
absdir=osroot/'runtime_absorption'
mandatory_runner=['runner_registry.yaml','phase_runner_binding.yaml','validation_runner_registry.yaml','replay_runner_registry.yaml','runner_failure_policy.yaml']
mandatory_abs=['single_token_replay_manifest.json','phase_trace.jsonl','phase_acceptance_report.md','phase_handoff_packet.json','runtime_absorption_issue_registry.md','paper_only_decision_report.md']
# also verify all generated phase handoffs requested by stage mapping
phase_handoffs=['data_fact_handoff_packet.json','wallet_chip_fact_handoff_packet.json','wallet_entity_handoff_packet.json','chip_structure_handoff_packet.json','evidence_control_packet.json','scenario_recognition_packet.json','strategy_gate_decision.json','paper_only_execution_gate.json','failure_attribution_packet.json']
required_trace_fields=['phase_id','input_files','output_files','runner_used','decision','evidence_level','counter_evidence','missing_fields','status','failure_reason','downstream_handoff']
report={'mandatory_runner':{},'mandatory_runtime_absorption':{},'phase_handoffs':{},'trace':{},'gate':{},'issues':{},'acceptance':None,'errors':[]}
for f in mandatory_runner:
    p=runners/f; report['mandatory_runner'][f]={'exists':p.exists(),'size':p.stat().st_size if p.exists() else 0}
    if not p.exists() or p.stat().st_size==0: report['errors'].append(f'missing runner file {f}')
for f in mandatory_abs:
    p=absdir/f; report['mandatory_runtime_absorption'][f]={'exists':p.exists(),'size':p.stat().st_size if p.exists() else 0}
    if not p.exists() or p.stat().st_size==0: report['errors'].append(f'missing absorption file {f}')
for f in phase_handoffs:
    p=absdir/f; report['phase_handoffs'][f]={'exists':p.exists(),'size':p.stat().st_size if p.exists() else 0}
    if not p.exists() or p.stat().st_size==0: report['errors'].append(f'missing handoff {f}')
trace_path=absdir/'phase_trace.jsonl'
if trace_path.exists():
    rows=[json.loads(x) for x in trace_path.read_text(encoding='utf-8').splitlines() if x.strip()]
    report['trace']['count']=len(rows)
    report['trace']['phase_ids']=[r.get('phase_id') for r in rows]
    report['trace']['fields_ok']=all(all(k in r for k in required_trace_fields) for r in rows)
    report['trace']['all_have_handoff']=all(bool(r.get('downstream_handoff')) for r in rows)
    if len(rows)!=9: report['errors'].append(f'trace count expected 9 got {len(rows)}')
    if report['trace']['phase_ids']!=['P01','P02','P03','P04','P05','P06','P07','P08','P09']: report['errors'].append('trace phase order mismatch')
    if not report['trace']['fields_ok']: report['errors'].append('trace fields incomplete')
else:
    report['errors'].append('trace file missing')
# acceptance
try:
    txt=(absdir/'phase_acceptance_report.md').read_text(encoding='utf-8')
    report['acceptance']='PHASE_REPLAY_PASS_WITH_GAPS' if 'PHASE_REPLAY_PASS_WITH_GAPS' in txt else 'UNKNOWN'
except Exception as e: report['errors'].append(f'acceptance read failed {e}')
# gate validations
p07=json.loads((absdir/'strategy_gate_decision.json').read_text(encoding='utf-8'))
p08=json.loads((absdir/'paper_only_execution_gate.json').read_text(encoding='utf-8'))
p09=json.loads((absdir/'failure_attribution_packet.json').read_text(encoding='utf-8'))
report['gate']['p07_decision']=p07.get('decision')
report['gate']['p07_consumed_count']=len(p07.get('consumed_handoffs',[]))
report['gate']['paper_runner_allowed_next']=p07.get('paper_runner_allowed_next')
report['gate']['p08_paper_only_allowed']=p08.get('paper_only_allowed')
report['gate']['p08_no_real_swap']=p08.get('safety_boundary',{}).get('no_real_swap')
report['gate']['p08_no_signing']=p08.get('safety_boundary',{}).get('no_signing')
report['gate']['p08_no_broadcast']=p08.get('safety_boundary',{}).get('no_broadcast')
report['gate']['p09_no_realtime_mutation']=not p09.get('forbidden_mutation_observed')
if p07.get('decision') not in ['PAPER_READY','READY_FOR_CONFIRMATION','WATCH','RISK_MONITOR','RECORD','EXCLUDE']:
    report['errors'].append('P07 decision not recognized')
if not p07.get('consumed_handoffs') or len(p07.get('consumed_handoffs',[]))<6:
    report['errors'].append('P07 did not consume upstream handoffs')
if p08.get('paper_only_allowed') and not p07.get('paper_runner_allowed_next'):
    report['errors'].append('P08 allowed paper without P07 permission')
for k in ['no_real_swap','no_signing','no_broadcast']:
    if not p08.get('safety_boundary',{}).get(k): report['errors'].append(f'P08 safety boundary {k} missing/false')
if p09.get('forbidden_mutation_observed'):
    report['errors'].append('P09 realtime mutation observed')
issue_txt=(absdir/'runtime_absorption_issue_registry.md').read_text(encoding='utf-8')
report['issues']['count']=issue_txt.count('## ISSUE-')
report['issues']['has_realtime_mutation_block']='realtime_rule_mutation_allowed: false' in issue_txt
if report['issues']['count']<1: report['errors'].append('issue registry empty')
if not report['issues']['has_realtime_mutation_block']: report['errors'].append('issue registry missing realtime mutation block')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if report['errors'] else 0)
