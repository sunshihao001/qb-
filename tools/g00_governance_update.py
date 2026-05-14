from pathlib import Path
from her_pipeline_lib import write_json, read_json, trace

def run(run_dir: Path, run_id: str):
    trace(run_dir, run_id, 'G00', 'phase_started', 'STARTED')
    candidates=[
      {'candidate_id':'gov_no_ready_without_evidence','rule_type':'STATUS_RULE','rule_statement':'READY must not be claimed when only task package or mapping exists without execution evidence.','priority':'P1_HIGH','source_gap':'gap_001','status':'CANDIDATE'},
      {'candidate_id':'gov_no_raw_only_k00_completion','rule_type':'PROCESS_RULE','rule_statement':'K00 cannot be marked complete when only raw document is saved.','priority':'P1_HIGH','status':'CANDIDATE'},
      {'candidate_id':'gov_safe_mode_not_production','rule_type':'SAFETY_RULE','rule_statement':'SAFE_MODE output must never be labeled production ready.','priority':'P1_HIGH','status':'CANDIDATE'}]
    update={'policy_rules_update':[{'rule_id':c['candidate_id'],'operation':'CANDIDATE_ONLY_NOT_APPLIED','status':'QUEUED_FOR_REVIEW'} for c in candidates], 'status':'POLICY_RULES_UPDATE_CANDIDATE_WITH_GAPS'}
    write_json(run_dir/'g00/governance_candidates.json', {'governance_candidates':candidates})
    write_json(run_dir/'g00/policy_rules_update.json', update)
    trace(run_dir, run_id, 'G00', 'phase_completed', 'GOVERNANCE_CANDIDATES_READY_WITH_GAPS')
    return candidates
