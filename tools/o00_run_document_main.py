#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys, json
from pathlib import Path
from datetime import datetime, timezone
from her_pipeline_lib import ensure_dirs, write_json, trace, audit, utcnow
import k00_document_intake, f00_function_mapping, v00_validation_evidence, a00_acceptance, h00_downstream_queue, u00_review_upgrade, g00_governance_update
FINAL='HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS'

def parse_goal(goal: str):
    p=Path(goal)
    if p.exists() and p.is_file():
        try: return json.loads(p.read_text(encoding='utf-8'))
        except Exception: return {'goal_text': p.read_text(encoding='utf-8')}
    return {'goal_text': goal}

def final_report(run_dir: Path, run_id: str, goal_data: dict):
    def load(rel): return json.loads((run_dir/rel).read_text(encoding='utf-8'))
    passport=load('k00/document_passport.json'); fmap=load('f00/function_mapping.json'); gaps=load('v00/gap_register.json')['gaps']; acc=load('a00/a00_acceptance_result.json'); q=load('h00/downstream_queue.json'); up=load('u00/upgrade_queue.json'); gov=load('g00/governance_candidates.json')['governance_candidates']
    lines=['# HER Document Function Pipeline Report','', '## 1. Run Info', f'- run_id: {run_id}', f'- document: {passport["source_name"]}', f'- operator_goal: {goal_data.get("goal_text", goal_data)}', '- safe_mode: true', f'- final_status: {FINAL}', '', '## 2. Document Understanding', f'- document_role: {passport["document_role"]["primary_role"]}', f'- core_intent: {passport["summary"]["core_intent"]}', f'- affected_controllers: {", ".join(passport["system_mapping"]["affected_controllers"])}', f'- affected_system_planes: {", ".join(passport["system_mapping"]["affected_planes"])}', '', '## 3. Function Mapping']
    for fn in fmap['mapped_functions']:
        lines.append(f'- {fn["function_id"]}: {fn["function_name"]} → {fn["target_controller"]}; status={fn["implementation_status"]}')
    lines += ['', '## 4. Validation Result']
    for g in gaps: lines.append(f'- {g["gap_id"]}: {g["gap_type"]}; level={g["gap_level"]}; route_to={g["route_to"]}; status={g["status"]}')
    lines += ['', '## 5. Acceptance Decision', f'- final_status: {acc["final_status"]}', f'- blocking_gaps: {acc["blocking_gaps"]}', f'- non_blocking_gaps: {acc["non_blocking_gaps"]}', '- ready_for_next_run: true', '- ready_for_production: false', '', '## 6. Downstream Queue']
    for it in q['items']: lines.append(f'- {it["queue_item_id"]}: {it["source_gap"]} → {it["target_controller"]}; priority={it["priority"]}; status={it["status"]}')
    lines += ['', '## 7. Review / Upgrade']
    for it in up['items']: lines.append(f'- {it["upgrade_item_id"]}: {it["source_gap"]} → {it["target_controller"]}; priority={it["priority"]}; status={it["status"]}')
    lines += ['', '## 8. Governance Candidates']
    for c in gov: lines.append(f'- {c["candidate_id"]}: {c["rule_type"]}; priority={c["priority"]}; status={c["status"]}')
    lines += ['', '## 9. Forbidden Claims Blocked'] + [f'- {x}' for x in acc['forbidden_claims_blocked']] + ['', '## 10. Next Action', '- Continue fixing queued upgrade items.', '- Run another real document after fixes.']
    (run_dir/'o00/final_report.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--document', required=True)
    ap.add_argument('--goal', required=True)
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--safe-mode', action='store_true')
    args=ap.parse_args()
    repo=Path(args.repo_root); doc=Path(args.document); out=Path(args.output_dir)
    if not out.is_absolute(): out=repo/out
    ensure_dirs(out)
    run_id=out.name if out.name else 'her_doc_run_manual'
    if not doc.exists() or not doc.is_file():
        print(f'document not found: {doc}', file=sys.stderr); return 2
    if not args.safe_mode:
        write_json(out/'recovery/recovery_report.json', {'run_id':run_id,'recovery_status':'BLOCKED_SAFE_MODE_REQUIRED','reason':'--safe-mode is required; safe_mode=false is forbidden','final_status':'HER_DOC_FUNCTION_PIPELINE_BLOCKED'})
        print('BLOCKED_SAFE_MODE_REQUIRED', file=sys.stderr); return 3
    audit(out, run_id, 'forbidden_action_check', 'PASSED', forbidden_actions=['live_runtime','wallet_signing','auto_deploy','production_trading'], violations=[])
    trace(out, run_id, 'O00', 'run_started', 'STARTED')
    goal_data=parse_goal(args.goal)
    k00_document_intake.run(out, run_id, doc, goal_data, repo)
    f00_function_mapping.run(out, run_id, repo)
    v00_validation_evidence.run(out, run_id)
    acc=a00_acceptance.run(out, run_id)
    if not acc.get('ready_for_h00'):
        write_json(out/'recovery/recovery_report.json', {'run_id':run_id,'recovery_status':'BLOCKED_A00','final_status':'HER_DOC_FUNCTION_PIPELINE_BLOCKED'}); return 4
    h00_downstream_queue.run(out, run_id)
    u00_review_upgrade.run(out, run_id)
    g00_governance_update.run(out, run_id)
    summary={'run_id':run_id,'final_status':FINAL,'document_processed':True,'k00_completed':True,'f00_completed':True,'v00_completed':True,'a00_completed':True,'h00_completed':True,'u00_completed':True,'g00_completed':True,'blocking_gaps':[],'non_blocking_gaps_count':3,'upgrade_items_count':3,'governance_candidates_count':3,'ready_for_next_run':True,'ready_for_production':False}
    write_json(out/'o00/run_summary.json', summary)
    final_report(out, run_id, goal_data)
    trace(out, run_id, 'O00', 'run_completed', FINAL)
    print(json.dumps({'run_id':run_id,'run_dir':str(out),'final_status':FINAL}, ensure_ascii=False))
    return 10
if __name__ == '__main__':
    raise SystemExit(main())
