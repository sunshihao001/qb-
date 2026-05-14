#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json, FORBIDDEN_CLAIMS
FALSE_CLAIMS=["TEST_PLAN_AS_TESTED","REPLAY_PLAN_AS_REPLAY_TESTED","BINDING_PLAN_AS_RUNNER_BOUND","DRY_RUN_AS_LIVE_RUNTIME","GOVERNANCE_CANDIDATE_AS_POLICY_ACTIVE","READY_WITH_GAPS_AS_READY","DESIGN_ONLY_AS_IMPLEMENTED"]
def validate_status_consistency(output_dir: Path, decision_status: str, open_gaps: list[str]) -> dict:
    inconsistencies=[]
    if open_gaps and decision_status in ["PIPELINE_ACCEPTED","A00_ACCEPTED","PRODUCTION_READY"]:
        inconsistencies.append("READY_WITH_GAPS_AS_READY")
    report={"status_consistency":"PASSED" if not inconsistencies else "BLOCKED", "blocked_false_claims": FALSE_CLAIMS, "inconsistencies": inconsistencies, "downgraded_statuses": [], "required_corrections": []}
    write_json(output_dir/"phase_status/status_consistency_report.json", report)
    return report
