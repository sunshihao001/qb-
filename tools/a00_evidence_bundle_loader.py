#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import read_json

def load_upstream_evidence(repo_root: Path, pipeline_run: Path, v00_evidence: Path, r00_evidence: Path, k00_handoff: Path|None=None, f00_handoff: Path|None=None, v00_handoff: Path|None=None, r00_handoff: Path|None=None, governance_policy: Path|None=None) -> dict:
    return {
        "o00_pipeline_run": read_json(pipeline_run),
        "k00_handoff_packet": read_json(k00_handoff) if k00_handoff else {},
        "f00_handoff_packet": read_json(f00_handoff) if f00_handoff else {},
        "v00_validation_evidence_bundle": read_json(v00_evidence),
        "v00_handoff_packet": read_json(v00_handoff) if v00_handoff else {},
        "r00_binding_evidence_bundle": read_json(r00_evidence),
        "r00_handoff_packet": read_json(r00_handoff) if r00_handoff else {},
        "governance_policy_bundle": read_json(governance_policy) if governance_policy else {},
    }

def build_real_evidence_bundle(output_dir: Path, acceptance_run_id: str, evidence: dict) -> dict:
    pipeline=evidence.get("o00_pipeline_run", {})
    v00=evidence.get("v00_validation_evidence_bundle", {})
    r00=evidence.get("r00_binding_evidence_bundle", {})
    bundle={
        "bundle_id": f"real_evidence_bundle_{acceptance_run_id}",
        "acceptance_run_id": acceptance_run_id,
        "source_pipeline_run_id": pipeline.get("pipeline_run_id", pipeline.get("source_pipeline_run_id", "UNKNOWN_PIPELINE_RUN")),
        "evidence_groups": {
            "o00_pipeline": ["input/o00_pipeline_run_ref.json"],
            "k00_intake": ["input/k00_handoff_packet_ref.json"],
            "f00_function_realization": ["input/f00_handoff_packet_ref.json"],
            "v00_real_validation": ["input/v00_validation_evidence_bundle_ref.json"],
            "r00_real_binding": ["input/r00_binding_evidence_bundle_ref.json"],
            "gap_register": ["gap_review/unresolved_gaps.json"],
            "trace_audit": ["trace_audit/a00_real_acceptance_trace.jsonl", "trace_audit/a00_real_acceptance_audit.jsonl"],
            "governance_policy": ["input/governance_policy_bundle_ref.json"],
        },
        "summary": {
            "o00_status": pipeline.get("system_status_code", pipeline.get("status", "UNKNOWN")),
            "v00_status": v00.get("summary", {}).get("final_validation_status", v00.get("final_status", "UNKNOWN")),
            "r00_status": r00.get("summary", {}).get("final_binding_status", r00.get("final_status", r00.get("status", "UNKNOWN"))),
            "a00_input_integrity": "READY",
        },
        "bundle_status": "BUILT",
    }
    from a00_acceptance_status import write_json
    write_json(output_dir/"evidence_bundle/real_evidence_bundle.json", bundle)
    return bundle
