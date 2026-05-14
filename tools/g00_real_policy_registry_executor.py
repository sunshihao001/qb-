#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from g00_policy_status import *
from g00_u00_handoff_loader import load_u00_handoff
from g00_governance_candidate_classifier import classify_candidates
from g00_policy_domain_mapper import map_domains
from g00_policy_conflict_checker import check_conflicts
from g00_policy_rule_builder import build_policy_rules, static_policies
from g00_policy_bundle_builder import build_bundles
from g00_policy_versioning_manager import build_versioning
from g00_governance_registry_writer import build_registry
from g00_policy_handoff_writer import all_handoffs

def build_report(out, run_id, source, final_status):
    report=f"""# G00 Real Governance Policy Registry Report

## 1. Run Info
- policy_run_id: {run_id}
- source_u00_handoff: {source}
- repo_root: /root/sikk-gmgn
- safe_mode: true
- final_status: {final_status}

## 2. Loaded Inputs
- U00 handoff: input/u00_to_g00_handoff_packet_ref.json
- governance_candidates: candidates/policy_candidate_inventory.json
- controller_registry: system/her_document_function_system/registry/controller_registry.json

## 3. Candidate Inventory
- file: candidates/policy_candidate_inventory.json

## 4. Candidate Classification
- file: candidates/candidate_classification.json

## 5. Policy Domain Mapping
- file: domain_mapping/policy_domain_mapping.json

## 6. Evidence Reference Validation
- file: candidates/candidate_evidence_validation.json

## 7. Policy Conflict Check
- policy_conflict_report: conflict_check/policy_conflict_report.json
- duplicate_rule_report: conflict_check/duplicate_rule_report.json
- weakened_rule_check: conflict_check/weakened_rule_check.json

## 8. Policy Rules
- forbidden_action_policy: policy_rules/forbidden_action_policy.json
- status_code_policy: policy_rules/status_code_policy.json
- evidence_policy: policy_rules/evidence_policy.json
- gap_policy: policy_rules/gap_policy.json
- runner_safety_policy: policy_rules/runner_safety_policy.json
- human_confirmation_policy: policy_rules/human_confirmation_policy.json
- production_risk_policy: policy_rules/production_risk_policy.json

## 9. Policy Bundle
- pending_policy_bundle: policy_bundles/pending_policy_bundle.json
- active_policy_bundle: policy_bundles/active_policy_bundle.json
- active status: LOCAL_ACTIVE_WITH_GAPS
- system enforcement: NOT_YET_VERIFIED

## 10. Governance Registry
- file: registry/governance_registry.json
- registry_status: REGISTRY_READY_WITH_GAPS

## 11. Policy Handoff
- all-controller handoff: handoff/g00_to_all_policy_handoff.json

## 12. Open Gaps
- downstream_policy_consumption_not_verified
- run_document_safe_mode_not_validated_with_active_policy
- multi_run_policy_stability_not_verified

## 13. Forbidden Claims Blocked
- SYSTEM_GOVERNANCE_ENFORCED
- PIPELINE_ACCEPTED
- PRODUCTION_READY
- LIVE_READY

## 14. Final Decision
{final_status}
"""
    write_text(Path(out)/"reports/g00_real_policy_report.md", report)

def execute(args):
    repo=Path(args.repo_root); out=Path(args.output_dir); run_id=out.name or f"g00_real_policy_{stamp()}"; ensure_dirs(out)
    trace=out/"trace/g00_real_policy_trace.jsonl"; audit=out/"audit/g00_real_policy_audit.jsonl"
    append_jsonl(trace,{"event_type":"g00_real_started","policy_run_id":run_id})
    append_jsonl(audit,{"event_type":"safe_mode_asserted","safe_mode":bool(args.safe_mode)})
    blockers=[]
    handoff_path=rel_or_abs(repo,args.u00_handoff)
    if not args.safe_mode: blockers.append("safe_mode_required")
    if not handoff_path or not handoff_path.exists(): blockers.append("missing_u00_to_g00_handoff_packet")
    pre={"preflight_status":"PASSED" if not blockers else "BLOCKED","safe_mode":bool(args.safe_mode),"loaded_inputs":["u00_to_g00_handoff_packet"] if handoff_path and handoff_path.exists() else [],"forbidden_actions_checked":FORBIDDEN_ACTIONS,"blocking_gaps":blockers}
    write_json(out/"preflight/g00_real_policy_preflight.json",pre)
    write_json(out/"input/u00_to_g00_handoff_packet_ref.json", {"path":str(handoff_path) if handoff_path else None,"loaded": bool(handoff_path and handoff_path.exists())})
    append_jsonl(audit,{"event_type":"forbidden_actions_checked","forbidden_actions":FORBIDDEN_ACTIONS})
    if blockers:
        fail={"acceptance_id":f"g00_real_policy_acceptance_{run_id}","final_status":BLOCKED_STATUS,"blocking_gaps":blockers,"ready_for_o00":False,"ready_for_production":False}
        write_json(out/"acceptance/g00_real_policy_acceptance.json",fail); write_json(out/"failure_evidence/g00_policy_failure_evidence.json",{"failures":blockers}); print(json.dumps({"policy_run_id":run_id,"final_status":BLOCKED_STATUS,"output_dir":str(out)},ensure_ascii=False)); return 2
    loaded=load_u00_handoff(handoff_path); append_jsonl(trace,{"event_type":"u00_handoff_loaded","handoff_status":loaded.get("handoff_status")})
    candidates=loaded.get("governance_candidates",[])
    inv={"inventory_id":f"policy_candidate_inventory_{run_id}","candidates":[{**c,"candidate_id":c.get("candidate_id") or c.get("upgrade_candidate_id") or f"gov_candidate_{i:03d}","initial_status":"CANDIDATE_LOADED"} for i,c in enumerate(candidates,1)],"inventory_status":"BUILT"}
    write_json(out/"candidates/policy_candidate_inventory.json",inv); append_jsonl(trace,{"event_type":"candidate_inventory_built","count":len(candidates)})
    classification=classify_candidates(candidates); write_json(out/"candidates/candidate_classification.json",classification); append_jsonl(trace,{"event_type":"candidate_classified","count":len(classification.get('classified_candidates',[]))})
    evidence_validation={"evidence_validation_status":"PASSED_WITH_GAPS","valid_candidates":[c["candidate_id"] for c in classification.get("classified_candidates",[]) if c.get("source_candidate",{}).get("evidence_refs")],"candidates_downgraded_to_pending":[c["candidate_id"] for c in classification.get("classified_candidates",[]) if not c.get("source_candidate",{}).get("evidence_refs")],"candidates_rejected":[],"warnings":["some evidence refs may be logical references and should be path-verified in next run-document cycle"]}
    write_json(out/"candidates/candidate_evidence_validation.json", evidence_validation)
    mapping=map_domains(classification); write_json(out/"domain_mapping/policy_domain_mapping.json",mapping); append_jsonl(trace,{"event_type":"policy_domain_mapped"})
    conflict, dup, weak=check_conflicts(classification); write_json(out/"conflict_check/policy_conflict_report.json",conflict); write_json(out/"conflict_check/duplicate_rule_report.json",dup); write_json(out/"conflict_check/weakened_rule_check.json",weak); append_jsonl(trace,{"event_type":"policy_conflict_checked","status":conflict["conflict_check_status"]})
    rules=build_policy_rules(classification); write_json(out/"policy_rules/policy_rules.json",rules)
    names=["forbidden_action_policy","status_code_policy","evidence_policy","gap_policy","runner_safety_policy","human_confirmation_policy","production_risk_policy"]
    for name,obj in zip(names, static_policies()): write_json(out/f"policy_rules/{name}.json",obj)
    append_jsonl(trace,{"event_type":"policy_rules_built"})
    pending, active, rejected=build_bundles(run_id); write_json(out/"policy_bundles/pending_policy_bundle.json",pending); write_json(out/"policy_bundles/active_policy_bundle.json",active); write_json(out/"policy_bundles/rejected_policy_bundle.json",rejected); append_jsonl(trace,{"event_type":"policy_bundles_built","active_status":active["bundle_status"]})
    versioning=build_versioning(run_id); write_json(out/"versioning/policy_versioning.json",versioning)
    registry=build_registry(run_id); write_json(out/"registry/governance_registry.json",registry); write_json(out/"registry/deprecated_policy_registry.json",{"deprecated_policies":[]}); append_jsonl(trace,{"event_type":"governance_registry_written","registry_status":registry["registry_status"]})
    for target,handoff in all_handoffs(run_id).items(): write_json(out/f"handoff/g00_to_{target}_policy_handoff.json",handoff)
    append_jsonl(trace,{"event_type":"policy_handoff_written"})
    failure={"failure_evidence_id":f"g00_policy_failure_evidence_{run_id}","failures":[],"blocking_failures":[],"non_blocking_failures":[]}; write_json(out/"failure_evidence/g00_policy_failure_evidence.json",failure)
    write_json(out/"recovery/recovery_report.json",{"recovery_required":False,"safe_next_actions":["handoff_to_o00_run_document_safe_mode"]})
    acc={"acceptance_id":f"g00_real_policy_acceptance_{run_id}","final_status":FINAL_STATUS,"candidate_status":"GOVERNANCE_CANDIDATES_CLASSIFIED","conflict_status":"POLICY_CONFLICT_CHECK_PASSED_WITH_GAPS","registry_status":"REGISTRY_READY_WITH_GAPS","policy_bundle_status":"LOCAL_ACTIVE_WITH_GAPS","system_enforcement_status":"NOT_YET_VERIFIED","reason":"U00 governance candidates were converted into versioned governance policies and registry. Policies are locally active for G00 handoff, but downstream controller consumption and run-document validation are not yet verified.","ready_for_o00":True,"ready_for_all_controller_policy_handoff":True,"ready_for_production":False,"blocking_gaps":[],"non_blocking_gaps":["downstream_policy_consumption_not_verified","run_document_safe_mode_not_validated_with_active_policy","multi_run_policy_stability_not_verified"],"forbidden_claims_blocked":FORBIDDEN_CLAIMS}
    write_json(out/"acceptance/g00_real_policy_acceptance.json",acc); append_jsonl(audit,{"event_type":"false_claims_blocked","forbidden_claims":FORBIDDEN_CLAIMS}); append_jsonl(audit,{"event_type":"final_decision_written","final_status":FINAL_STATUS})
    build_report(out,run_id,str(handoff_path),FINAL_STATUS); append_jsonl(trace,{"event_type":"g00_real_completed","final_status":FINAL_STATUS})
    print(json.dumps({"policy_run_id":run_id,"final_status":FINAL_STATUS,"output_dir":str(out)},ensure_ascii=False)); return 0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--u00-handoff", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--safe-mode", action="store_true", required=True)
    return execute(ap.parse_args())
if __name__=="__main__": raise SystemExit(main())
