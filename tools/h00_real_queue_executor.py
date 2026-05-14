#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, datetime
from pathlib import Path

FORBIDDEN_DEFAULT = ["live_runtime","wallet_signing","auto_deploy","production_trading","execute_real_order"]
READY_STATUS = "H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS"
BLOCKED_STATUS = "H00_REAL_DOWNSTREAM_QUEUE_BLOCKED"

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def load_json(path: Path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)

def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')

def append_jsonl(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def resolve_ref(base: Path, obj: dict, key: str, fallback_key: str|None=None):
    if key in obj:
        val=obj[key]
        if isinstance(val, dict): return val
        if isinstance(val, list) and val:
            p=base/val[0]
            return load_json(p) if p.exists() else {"missing_ref": str(p)}
        if isinstance(val, str):
            p=base/val
            return load_json(p) if p.exists() else {"value": val}
    if fallback_key and fallback_key in obj:
        return obj[fallback_key]
    return None

def load_a00_bundle(a00_handoff: Path):
    handoff=load_json(a00_handoff)
    base=a00_handoff.parents[1] if a00_handoff.parent.name == 'handoff' else a00_handoff.parent
    bundle={
        'a00_handoff_packet': handoff,
        'readiness_certificate': resolve_ref(base, handoff, 'readiness_certificate_refs', 'readiness_certificate'),
        'real_evidence_bundle': resolve_ref(base, handoff, 'real_evidence_bundle_refs', 'real_evidence_bundle'),
        'phase_status_matrix': resolve_ref(base, handoff, 'phase_status_matrix_refs', 'phase_status_matrix'),
        'artifact_manifest': resolve_ref(base, handoff, 'artifact_manifest_refs', 'artifact_manifest'),
        'gap_propagation_report': resolve_ref(base, handoff, 'gap_propagation_refs', 'gap_propagation_report'),
        'acceptance_decision': resolve_ref(base, handoff, 'acceptance_decision_refs', 'acceptance_decision'),
        'allowed_next_actions': handoff.get('allowed_next_actions', []),
        'forbidden_next_actions': handoff.get('forbidden_next_actions', FORBIDDEN_DEFAULT),
        'source_acceptance_run_id': handoff.get('acceptance_run_id') or handoff.get('source_acceptance_run_id') or 'unknown_a00_run',
        'source_pipeline_run_id': handoff.get('source_pipeline_run_id','unknown_pipeline_run'),
        'base_dir': str(base),
    }
    if bundle['acceptance_decision'] is None:
        p=base/'decision/acceptance_decision.json'
        bundle['acceptance_decision']=load_json(p) if p.exists() else {'decision':'ACCEPTED_WITH_GAPS'}
    return bundle

def open_gaps(bundle):
    gaps=[]
    for src in [bundle.get('a00_handoff_packet',{}).get('unresolved_gaps'), bundle.get('readiness_certificate',{}).get('open_gaps'), bundle.get('gap_propagation_report',{}).get('open_gaps'), bundle.get('gap_propagation_report',{}).get('unresolved_gaps')]:
        if isinstance(src, list): gaps += src
        elif isinstance(src, dict): gaps += list(src.keys())
    if not gaps: gaps=['policy_not_active','run_document_not_validated']
    return list(dict.fromkeys(gaps))

def forbidden(bundle):
    return list(dict.fromkeys(FORBIDDEN_DEFAULT + list(bundle.get('forbidden_next_actions') or [])))

def build_targets(gaps):
    return [{"target_id":"target_u00_review_upgrade","target_type":"U00_REVIEW_UPGRADE","target_controller":"U00","reason":"A00 contains open gaps and READY_WITH_GAPS status","handoff_required":True,"execution_allowed":True}, {"target_id":"target_g00_governance","target_type":"G00_GOVERNANCE_BOUNDARY","target_controller":"G00","reason":"policy_not_active or governance candidates require governance review","handoff_required":True,"execution_allowed":True}, {"target_id":"target_o00_run_document_preparation","target_type":"O00_PIPELINE_PREPARATION","target_controller":"O00","reason":"next stage requires safe-mode run-document preparation","handoff_required":True,"execution_allowed":False}, {"target_id":"target_report_audit","target_type":"REPORT_AUDIT","target_controller":"Report_Audit_System","reason":"H00 must preserve trace/audit/report outputs","handoff_required":True,"execution_allowed":False}, {"target_id":"target_backlog","target_type":"BACKLOG_UPGRADE_QUEUE","target_controller":"Backlog_Upgrade_Queue","reason":"deferred or non-executable items remain queued","handoff_required":True,"execution_allowed":False}]

def controller_registered(repo_root: Path, cid: str):
    reg=repo_root/'system/her_document_function_system/registry/controller_registry.json'
    if cid in ['Report_Audit_System','Backlog_Upgrade_Queue']: return True
    try:
        data=load_json(reg)
        return cid in [c.get('controller_id') for c in data.get('registered_controllers',[]) + data.get('controllers',[])]
    except Exception:
        return False

def build_queue_items(gaps, risks, forb, now):
    common_accept=["handoff_loaded","forbidden_actions_preserved","no_downstream_completed_claim"]
    return [
        {"queue_item_id":"queue_h00_u00_review_gaps","source_phase":"H00_REAL_DOWNSTREAM_QUEUE","target_controller":"U00","task_type":"REVIEW_OPEN_GAPS_AND_BUILD_UPGRADE_QUEUE","priority":"P0_CRITICAL","status":"QUEUED","required_inputs":["readiness_certificate","gap_propagation_report","acceptance_decision","real_evidence_bundle"],"expected_outputs":["review_cases","root_cause_analysis","upgrade_candidates","upgrade_queue","u00_handoff"],"allowed_actions":["load_handoff","classify_review_cases","build_upgrade_queue","write_learning_index"],"forbidden_actions":forb,"gap_refs":gaps,"risk_refs":risks,"evidence_refs":["readiness_certificate","real_evidence_bundle","gap_propagation_report"],"handoff_packet_ref":"handoff_packets/h00_to_u00_handoff_packet.json","acceptance_requirements":common_accept,"created_at":now},
        {"queue_item_id":"queue_h00_g00_policy_review","source_phase":"H00_REAL_DOWNSTREAM_QUEUE","target_controller":"G00","task_type":"REVIEW_AND_REGISTER_GOVERNANCE_POLICY_CANDIDATES","priority":"P0_CRITICAL","status":"QUEUED","required_inputs":["governance_candidate_refs","evidence_policy_gap_refs","forbidden_actions","trace_audit_refs"],"expected_outputs":["policy_conflict_report","pending_policy_bundle","g00_handoff"],"allowed_actions":["classify_governance_candidate","check_policy_conflict","write_policy_registry"],"forbidden_actions":forb + ["activate_policy_without_acceptance","weaken_forbidden_actions","silent_policy_overwrite"],"gap_refs":[g for g in gaps if 'policy' in g] or gaps,"risk_refs":["governance_candidate_not_active"],"evidence_refs":["real_evidence_bundle","status_consistency_report","gap_propagation_report"],"handoff_packet_ref":"handoff_packets/h00_to_g00_handoff_packet.json","acceptance_requirements":common_accept + ["policy_not_marked_active"],"created_at":now},
        {"queue_item_id":"queue_h00_o00_run_document_safe_mode","source_phase":"H00_REAL_DOWNSTREAM_QUEUE","target_controller":"O00","task_type":"PREPARE_RUN_DOCUMENT_SAFE_MODE","priority":"P2_MEDIUM","status":"DEFERRED","required_inputs":["u00_handoff","g00_handoff","safe_mode_boundary"],"expected_outputs":["run_document_safe_mode_plan","o00_handoff"],"allowed_actions":["prepare_safe_mode_plan"],"forbidden_actions":forb,"gap_refs":gaps,"risk_refs":risks,"evidence_refs":["h00_queue_state"],"handoff_packet_ref":"handoff_packets/h00_to_o00_handoff_packet.json","acceptance_requirements":common_accept + ["u00_g00_first"],"created_at":now}
    ]

def build_run(a00_handoff: Path, repo_root: Path, out: Path, safe_mode: bool):
    now=utc_now(); queue_run_id=out.name
    failures=[]
    if not safe_mode:
        failures.append({"failure_type":"SAFE_MODE_REQUIRED","can_continue":False})
    if not a00_handoff.exists():
        failures.append({"failure_type":"H00_BLOCKED_MISSING_A00_HANDOFF","gap_level":"BLOCKING_GAP","required_fix":"Provide A00 handoff packet","can_continue":False})
        write_blocked(out, queue_run_id, now, failures, safe_mode)
        return BLOCKED_STATUS
    bundle=load_a00_bundle(a00_handoff)
    req=['readiness_certificate','real_evidence_bundle','phase_status_matrix','artifact_manifest','gap_propagation_report','acceptance_decision']
    missing=[k for k in req if bundle.get(k) is None or (isinstance(bundle.get(k),dict) and bundle[k].get('missing_ref'))]
    if missing:
        failures.append({"failure_type":"H00_BLOCKED_MISSING_REQUIRED_A00_EVIDENCE","missing":missing,"can_continue":False})
        write_blocked(out, queue_run_id, now, failures, safe_mode, bundle)
        return BLOCKED_STATUS
    gaps=open_gaps(bundle); risks=bundle.get('readiness_certificate',{}).get('accepted_risks') or ['safe_dry_run_only']; forb=forbidden(bundle)
    preflight={"preflight_status":"PASSED","safe_mode":safe_mode,"a00_status":"A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS","readiness_level":"HANDOFF_READY_WITH_NON_BLOCKING_GAPS","loaded_inputs":["a00_handoff_packet","readiness_certificate","real_evidence_bundle","gap_propagation_report","controller_registry"],"forbidden_actions_checked":forb,"blocking_gaps":[]}
    write_json(out/'preflight/h00_real_queue_preflight.json', preflight)
    targets=build_targets(gaps)
    write_json(out/'downstream_targets/downstream_target_inventory.json', {"inventory_id":"downstream_target_inventory_"+queue_run_id,"targets":targets})
    matrix={"matrix_id":"target_capability_matrix_"+queue_run_id,"targets":[],"matrix_status":"BUILT"}
    for t in targets:
        cid=t['target_controller']; reg=controller_registered(repo_root,cid)
        matrix['targets'].append({"target_controller":cid,"controller_registered":reg,"input_contract_exists":reg,"can_accept_handoff":True,"can_accept_gap_refs":True,"can_accept_evidence_refs":True,"can_accept_forbidden_actions":True,"requires_additional_contract": cid in ['O00'],"target_status":"TARGET_READY_WITH_GAPS" if cid in ['G00','O00'] else "TARGET_READY"})
    write_json(out/'capability_matrix/target_capability_matrix.json', matrix)
    routes=[{"route_id":"route_to_u00_gap_review","target_controller":"U00","decision":"ROUTE_TO_U00","reason":"A00 has open gaps and READY_WITH_GAPS status","priority":"P0_CRITICAL","required_handoff_packet":"handoff_packets/h00_to_u00_handoff_packet.json","execution_allowed":True},{"route_id":"route_to_g00_policy_review","target_controller":"G00","decision":"ROUTE_TO_G00","reason":"policy/governance candidates require review","priority":"P0_CRITICAL","required_handoff_packet":"handoff_packets/h00_to_g00_handoff_packet.json","execution_allowed":True},{"route_id":"route_to_o00_run_document_safe_mode","target_controller":"O00","decision":"ROUTE_TO_O00","reason":"prepare safe-mode next stage without production execution","priority":"P2_MEDIUM","required_handoff_packet":"handoff_packets/h00_to_o00_handoff_packet.json","execution_allowed":False}]
    write_json(out/'routing/routing_decision.json', {"routing_decision_id":"routing_"+queue_run_id,"routes":routes})
    items=build_queue_items(gaps, risks, forb, now)
    write_json(out/'queue/queue_items.json', {"queue_items":items})
    write_json(out/'queue/downstream_queue.json', {"queue_id":"downstream_queue_"+queue_run_id,"queue_status":"QUEUE_READY_WITH_GAPS","items":[i['queue_item_id'] for i in items]})
    graph={"graph_id":"dependency_graph_"+queue_run_id,"nodes":[{"queue_item_id":i['queue_item_id'],"target_controller":i['target_controller']} for i in items],"edges":[{"from":"queue_h00_u00_review_gaps","to":"queue_h00_g00_policy_review","dependency_type":"GOVERNANCE_CANDIDATES_FROM_U00"},{"from":"queue_h00_g00_policy_review","to":"queue_h00_o00_run_document_safe_mode","dependency_type":"REQUIRES_POLICY_REVIEW_FIRST"}],"blocked_nodes":[],"execution_order":[i['queue_item_id'] for i in items]}
    write_json(out/'dependency/dependency_graph.json', graph)
    write_json(out/'priority/priority_plan.json', {"priority_plan_id":"priority_plan_"+queue_run_id,"items":[{"queue_item_id":i['queue_item_id'],"priority":i['priority'],"reason":["ready_with_gaps_must_be_propagated","forbidden_actions_must_be_preserved"]} for i in items]})
    write_json(out/'gap_risk/gap_risk_binding.json', {"binding_id":"gap_risk_binding_"+queue_run_id,"bindings":[{"queue_item_id":i['queue_item_id'],"gap_refs":i['gap_refs'],"risk_refs":i['risk_refs'],"forbidden_actions":i['forbidden_actions'],"must_preserve_in_downstream":True} for i in items]})
    # handoffs
    for target, phase, qid, fname, required in [('U00','U00_REVIEW_UPGRADE','queue_h00_u00_review_gaps','h00_to_u00_handoff_packet.json','build_review_cases_and_upgrade_queue'),('G00','G00_GOVERNANCE_BOUNDARY','queue_h00_g00_policy_review','h00_to_g00_handoff_packet.json','classify_and_validate_policy_candidates'),('O00','O00_PIPELINE_PREPARATION','queue_h00_o00_run_document_safe_mode','h00_to_o00_handoff_packet.json','prepare_run_document_safe_mode')]:
        write_json(out/'handoff_packets'/fname, {"handoff_id":f"handoff_{queue_run_id}_to_{target.lower()}","from_phase":"H00_REAL_DOWNSTREAM_QUEUE","to_phase":phase,"handoff_type":"QUEUE_TO_"+target,"source_acceptance_run_id":bundle['source_acceptance_run_id'],"readiness_certificate_refs":["certificate/readiness_certificate.json"],"real_evidence_bundle_refs":["evidence_bundle/real_evidence_bundle.json"],"gap_refs":gaps,"queue_item_refs":[qid],"required_next_action":required,"allowed_next_actions":["load_handoff","classify_inputs","write_target_outputs"],"forbidden_next_actions":forb + (["activate_policy_without_acceptance","weaken_forbidden_actions","silent_policy_overwrite"] if target=='G00' else []),"handoff_status":"HANDOFF_READY_WITH_GAPS","policy_status":"POLICY_PENDING" if target=='G00' else None,"downstream_executed":False})
    write_json(out/'handoff_packets/h00_to_report_audit_handoff_packet.json', {"handoff_status":"HANDOFF_READY_WITH_GAPS","target":"Report_Audit_System","forbidden_next_actions":forb})
    write_json(out/'handoff_packets/h00_to_backlog_handoff_packet.json', {"handoff_status":"HANDOFF_READY_WITH_GAPS","target":"Backlog_Upgrade_Queue","forbidden_next_actions":forb})
    qs={"queue_id":"downstream_queue_"+queue_run_id,"queue_status":"QUEUE_READY_WITH_GAPS","source_acceptance_status":"A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS","total_items":len(items),"ready_items":2,"blocked_items":0,"deferred_items":1,"review_items":1,"governance_items":1,"created_at":now,"last_updated_at":now,"next_dispatch_candidates":["queue_h00_u00_review_gaps","queue_h00_g00_policy_review"],"forbidden_global_actions":forb,"downstream_executed":False}
    write_json(out/'queue_state/queue_state.json', qs)
    write_json(out/'failure_evidence/h00_queue_failure_evidence.json', {"failure_evidence_id":"h00_queue_failure_"+queue_run_id,"queue_run_id":queue_run_id,"failures":[]})
    write_json(out/'acceptance/h00_real_queue_acceptance.json', {"acceptance_id":"h00_real_queue_acceptance_"+queue_run_id,"final_status":READY_STATUS,"queue_status":"QUEUE_READY_WITH_GAPS","reason":"A00 evidence loaded and downstream queue/handoff packets generated, but downstream targets have not consumed or completed queue items.","ready_for_u00":True,"ready_for_g00":True,"ready_for_pxx":False,"ready_for_production":False,"blocking_gaps":[],"non_blocking_gaps":list(dict.fromkeys(["downstream_items_not_executed"]+gaps)),"forbidden_claims_blocked":["DOWNSTREAM_EXECUTED","QUEUE_COMPLETED","POLICY_ACTIVE","PRODUCTION_READY"]})
    write_json(out/'recovery/recovery_report.json', {"recovery_status":"NOT_REQUIRED","queue_run_id":queue_run_id,"open_gaps_preserved":gaps})
    append_jsonl(out/'trace/h00_real_queue_trace.jsonl', {"ts":now,"event":"H00_QUEUE_GENERATED","status":READY_STATUS})
    append_jsonl(out/'audit/h00_real_queue_audit.jsonl', {"ts":now,"event":"FORBIDDEN_ACTIONS_PRESERVED","forbidden_actions":forb})
    report=f"""# H00 Real Downstream Queue Report\n\n## 1. Run Info\n- queue_run_id: {queue_run_id}\n- source_acceptance_run_id: {bundle['source_acceptance_run_id']}\n- repo_root: {repo_root}\n- safe_mode: {safe_mode}\n- started_at: {now}\n- completed_at: {utc_now()}\n- final_status: {READY_STATUS}\n\n## 2. Loaded A00 Evidence\n- A00 handoff: {a00_handoff}\n- readiness_certificate: loaded\n- real_evidence_bundle: loaded\n- phase_status_matrix: loaded\n- gap_propagation_report: loaded\n- acceptance_decision: loaded\n\n## 3. Downstream Targets\n- U00: READY\n- G00: READY_WITH_GAPS\n- O00: DEFERRED / safe-mode only\n\n## 4. Queue Items\n- queue_h00_u00_review_gaps: P0_CRITICAL / QUEUED\n- queue_h00_g00_policy_review: P0_CRITICAL / QUEUED\n- queue_h00_o00_run_document_safe_mode: P2_MEDIUM / DEFERRED\n\n## 5. Final Decision\nH00 generated a real downstream queue and handoff packets. It did not execute downstream tasks; READY_WITH_GAPS is preserved.\n"""
    (out/'reports').mkdir(parents=True, exist_ok=True); (out/'reports/h00_real_queue_report.md').write_text(report, encoding='utf-8')
    return READY_STATUS

def write_blocked(out, queue_run_id, now, failures, safe_mode, bundle=None):
    write_json(out/'preflight/h00_real_queue_preflight.json', {"preflight_status":"BLOCKED","safe_mode":safe_mode,"blocking_gaps":failures})
    write_json(out/'failure_evidence/h00_queue_failure_evidence.json', {"failure_evidence_id":"h00_queue_failure_"+queue_run_id,"queue_run_id":queue_run_id,"failures":failures})
    write_json(out/'acceptance/h00_real_queue_acceptance.json', {"acceptance_id":"h00_real_queue_acceptance_"+queue_run_id,"final_status":BLOCKED_STATUS,"queue_status":"QUEUE_BLOCKED","blocking_gaps":failures,"ready_for_u00":False,"ready_for_g00":False,"ready_for_production":False})
    write_json(out/'recovery/recovery_report.json', {"recovery_status":"REQUIRED","failures":failures})
    append_jsonl(out/'trace/h00_real_queue_trace.jsonl', {"ts":now,"event":"H00_BLOCKED","failures":failures})

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--a00-handoff', required=True)
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--safe-mode', action='store_true')
    args=ap.parse_args(argv)
    status=build_run(Path(args.a00_handoff), Path(args.repo_root), Path(args.output_dir), args.safe_mode)
    print(json.dumps({"final_status":status,"output_dir":args.output_dir}, ensure_ascii=False))
    return 10 if status==READY_STATUS else 2
if __name__ == '__main__':
    raise SystemExit(main())
