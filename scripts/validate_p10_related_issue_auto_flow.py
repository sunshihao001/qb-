#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path('/root/sikk-gmgn')
TASK_ID='p10_related_issue_auto_flow_20260512_164618'
paths=[
 ROOT/'research_loop/task_packages/pending'/TASK_ID/'task_manifest.json',
 ROOT/'research_loop/task_packages/pending'/TASK_ID/'problem_inventory.json',
 ROOT/'research_loop/task_packages/pending'/TASK_ID/'execution_flow_plan.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/controlled_task_packets'/f'{TASK_ID}_controlled_task_packet.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/upgrade_backlog'/f'{TASK_ID}_upgrade_backlog_record.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/gaps'/f'{TASK_ID}_gap_register.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/trace'/f'{TASK_ID}_trace.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/handoff'/f'{TASK_ID}_handoff_packet.json',
 ROOT/'data/phase_controllers/p10_self_upgrade/acceptance'/f'{TASK_ID}_acceptance_result.json',
 ROOT/'system/phase_controllers/p10_self_upgrade_controller/p10_related_issue_auto_flow_policy.yaml',
]
missing=[str(p) for p in paths if not p.exists()]
if missing:
    print(json.dumps({'status':'FAIL','missing':missing}, ensure_ascii=False, indent=2)); sys.exit(1)
loaded={}
for p in paths:
    if p.suffix=='.json':
        loaded[p.name]=json.loads(p.read_text(encoding='utf-8'))
acc=loaded[f'{TASK_ID}_acceptance_result.json']
manifest=loaded['task_manifest.json']
inv=loaded['problem_inventory.json']
handoff=loaded[f'{TASK_ID}_handoff_packet.json']
violations=[]
if not inv.get('issues') or len(inv['issues']) < 8: violations.append('issue_count_too_low')
for key in ['auto_deploy','live_execution','wallet_signing','modify_production_rules']:
    if manifest.get('permissions',{}).get(key) is not False: violations.append('permission_'+key)
for k,v in acc.get('safety',{}).items():
    if v is not False: violations.append('safety_'+k)
for forbidden in ['LIVE_EXECUTION','AUTO_DEPLOY_WITHOUT_APPROVAL','DIRECT_RULE_MUTATION']:
    if forbidden not in handoff.get('downstream_permission',{}).get('forbidden',[]): violations.append('missing_forbidden_'+forbidden)
status='PASS' if not violations else 'FAIL'
print(json.dumps({'status':status,'task_id':TASK_ID,'checked_paths':len(paths),'issue_count':len(inv.get('issues',[])),'violations':violations,'acceptance_status':acc.get('status')}, ensure_ascii=False, indent=2))
sys.exit(0 if status=='PASS' else 1)
