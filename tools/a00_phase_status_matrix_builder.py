#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json

def build_phase_status_matrix(output_dir: Path, acceptance_run_id: str, evidence: dict, open_gaps: list[str], blocking_gaps: list[str]) -> dict:
    pipeline=evidence.get("o00_pipeline_run", {})
    v00=evidence.get("v00_validation_evidence_bundle", {})
    r00=evidence.get("r00_binding_evidence_bundle", {})
    f00=evidence.get("f00_handoff_packet", {})
    k00=evidence.get("k00_handoff_packet", {})
    phases=[
        ("O00", pipeline.get("system_status_code", pipeline.get("status", "UNKNOWN")), bool(pipeline)),
        ("K00", k00.get("status", "K00_HANDOFF_OPTIONAL_OR_EMBEDDED"), bool(k00)),
        ("F00", f00.get("status", f00.get("handoff_status", "F00_HANDOFF_OPTIONAL_OR_EMBEDDED")), bool(f00)),
        ("V00", v00.get("summary", {}).get("final_validation_status", v00.get("final_status", "UNKNOWN")), bool(v00)),
        ("R00", r00.get("summary", {}).get("final_binding_status", r00.get("final_status", r00.get("status", "UNKNOWN"))), bool(r00)),
    ]
    matrix={"matrix_id": f"phase_status_matrix_{acceptance_run_id}", "phases": [], "matrix_status": "BUILT"}
    for phase, status, present in phases:
        matrix["phases"].append({"phase_id": phase, "reported_status": status, "evidence_status": "PRESENT" if present else "OPTIONAL_MISSING", "blocking_gaps": len(blocking_gaps) if phase in ["O00","V00","R00"] else 0, "non_blocking_gaps": len(open_gaps), "a00_interpretation": "READY_WITH_GAPS" if not blocking_gaps else "BLOCKED"})
    write_json(output_dir/"phase_status/phase_status_matrix.json", matrix)
    return matrix
