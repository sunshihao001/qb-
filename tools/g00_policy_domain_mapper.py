def map_domains(classification):
    mappings=[]
    for c in classification.get("classified_candidates",[]):
        domain=c["policy_domain"]
        mappings.append({"candidate_id":c["candidate_id"],"policy_domain":domain,"target_policy_file":f"policy_rules/{domain}.json","policy_level":c.get("recommended_policy_level","RULE"),"activation_mode":"PENDING_CONFLICT_CHECK"})
    return {"mapping_status":"MAPPED","mappings":mappings}
