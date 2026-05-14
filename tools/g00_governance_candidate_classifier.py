def _ctype(c):
    text=(str(c.get("problem_statement","")+" "+c.get("proposed_change","")+" "+c.get("upgrade_type","")).lower())
    if "policy" in text or "candidate" in text: return "EVIDENCE_RULE"
    if "queue" in text or "status" in text or "upgrade" in text: return "STATUS_RULE"
    if "runner" in text: return "RUNNER_SAFETY_RULE"
    return "GAP_RULE"
def classify_candidates(candidates):
    out=[]
    for i,c in enumerate(candidates,1):
        cid=c.get("candidate_id") or c.get("upgrade_candidate_id") or f"gov_candidate_{i:03d}"
        ct=_ctype(c)
        domain={"STATUS_RULE":"status_code_policy","EVIDENCE_RULE":"evidence_policy","RUNNER_SAFETY_RULE":"runner_safety_policy","GAP_RULE":"gap_policy"}.get(ct,"gap_policy")
        out.append({"candidate_id":cid,"candidate_type":ct,"policy_domain":domain,"recommended_policy_level":"HARD_RULE" if c.get("priority","").startswith("P0") or c.get("requires_governance") else "RULE","requires_conflict_check":True,"requires_versioning":True,"classification_status":"CLASSIFIED","source_candidate":c})
    return {"classification_status":"CLASSIFIED","classified_candidates":out}
