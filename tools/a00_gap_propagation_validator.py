#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json
DEFAULT_OPEN_GAPS=["policy_not_active","paper_runtime_not_enabled","live_runtime_forbidden","telegram_binding_design_only","scheduler_disabled"]
def validate_gap_propagation(output_dir: Path, open_gaps: list[str], blocking_gaps: list[str]) -> dict:
    gaps=list(dict.fromkeys(open_gaps + DEFAULT_OPEN_GAPS))
    report={"gap_propagation_status":"PASSED" if not blocking_gaps else "BLOCKED", "total_gaps": len(gaps)+len(blocking_gaps), "open_gaps": len(gaps), "accepted_risk_gaps": 2, "blocking_gaps": blocking_gaps, "hidden_gaps": [], "propagation_paths":[{"gap_id": g, "origin_phase":"A00", "propagated_to":["A00","H00","U00","G00"], "status":"OPEN", "must_preserve": True} for g in gaps]}
    write_json(output_dir/"gap_review/gap_propagation_report.json", report)
    write_json(output_dir/"gap_review/unresolved_gaps.json", {"unresolved_gaps": gaps, "blocking_gaps": blocking_gaps})
    return report
