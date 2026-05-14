#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json, FINAL_STATUS, FORBIDDEN_ACTIONS
def write_certificate(output_dir: Path, acceptance_run_id: str, source_pipeline_run_id: str, final_status: str, open_gaps: list[str]) -> dict:
    cert={"certificate_id": f"readiness_certificate_{acceptance_run_id}", "acceptance_run_id": acceptance_run_id, "source_pipeline_run_id": source_pipeline_run_id, "final_status": final_status, "readiness_level": "HANDOFF_READY_WITH_NON_BLOCKING_GAPS" if final_status==FINAL_STATUS else "BLOCKED", "accepted_phases":["O00","K00","F00","V00","R00"], "evidence_bundle_ref":"evidence_bundle/real_evidence_bundle.json", "open_gaps": open_gaps, "accepted_risks":["safe_dry_run_only","telegram_binding_design_only"], "allowed_next_actions":["handoff_to_H00","route_gaps_to_U00","route_policy_candidates_to_G00","prepare_run_document_safe_mode"], "forbidden_next_actions": FORBIDDEN_ACTIONS + ["mark_policy_active_without_g00_acceptance","mark_pipeline_accepted_without_closing_gaps"], "issued_by":"A00_real_acceptance_executor"}
    write_json(output_dir/"certificate/readiness_certificate.json", cert)
    return cert
