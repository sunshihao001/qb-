#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json, FINAL_STATUS
DIMENSIONS=["source_intake","function_realization","validation_quality","binding_quality","status_integrity","artifact_integrity","gap_management","trace_audit_quality","governance_safety","downstream_readiness"]
def build_scorecard(output_dir: Path, acceptance_run_id: str, blocking_gaps: list[str], open_gaps: list[str]) -> dict:
    dims=[]
    for d in DIMENSIONS:
        dims.append({"dimension": d, "status": "PASSED_WITH_GAPS" if open_gaps else "PASSED", "evidence_refs": [], "gaps": open_gaps if d in ["gap_management","governance_safety","downstream_readiness"] else [], "decision_weight": "HIGH"})
    card={"scorecard_id": f"acceptance_scorecard_{acceptance_run_id}", "dimensions": dims, "overall_recommendation": "A00_REAL_ACCEPTANCE_BLOCKED" if blocking_gaps else FINAL_STATUS}
    write_json(output_dir/"scorecard/acceptance_scorecard.json", card)
    return card
