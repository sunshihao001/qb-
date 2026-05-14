from g00_policy_status import read_json
def load_u00_handoff(path):
    data=read_json(path)
    candidates=data.get("governance_candidates") or data.get("governance_candidate_refs") or []
    return {"loader_status":"LOADED","handoff_status":data.get("handoff_status","HANDOFF_READY_WITH_GAPS"),"governance_candidates":candidates,"governance_candidates_loaded":bool(candidates),"forbidden_next_actions":data.get("forbidden_next_actions",[]),"raw_handoff":data,"blocking_gaps":[] if candidates else ["missing_governance_candidates"]}
