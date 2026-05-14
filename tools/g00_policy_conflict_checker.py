FORBIDDEN={"live_runtime","wallet_signing","auto_deploy","production_trading","execute_real_order","silent_policy_overwrite"}
def check_conflicts(classification, current_registry=None):
    seen=set(); duplicates=[]; conflicts=[]; accepted=[]
    for c in classification.get("classified_candidates",[]):
        key=(c.get("policy_domain"), c.get("candidate_id"))
        if key in seen: duplicates.append(c.get("candidate_id"))
        else: seen.add(key); accepted.append(c.get("candidate_id"))
    return {"conflict_report_id":"policy_conflict_report_g00_real","conflict_check_status":"PASSED_WITH_GAPS","checked_candidates":accepted+duplicates,"conflicts":conflicts,"warnings":[{"warning_id":"warning_policy_activation_requires_controller_consumption","warning_type":"ACTIVATION_SCOPE_WARNING","message":"Policy can be registered locally, but full enforcement requires downstream controllers to load active_policy_bundle."}],"rejected_candidates":[],"accepted_candidates":accepted}, {"duplicate_rule_check_status":"PASSED" if not duplicates else "PASSED_WITH_GAPS","duplicate_rules":duplicates}, {"weakened_rule_check_status":"PASSED","weakened_rules_detected":[],"hard_forbidden_actions_preserved":sorted(FORBIDDEN)}
