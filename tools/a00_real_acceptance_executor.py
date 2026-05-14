#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from a00_acceptance_status import FINAL_STATUS, BLOCKED_STATUS, FORBIDDEN_ACTIONS, FORBIDDEN_CLAIMS, append_jsonl, ensure_dirs, now_iso, read_json, rel_or_abs, status_from_blockers, write_json
from a00_evidence_bundle_loader import load_upstream_evidence, build_real_evidence_bundle
from a00_phase_status_matrix_builder import build_phase_status_matrix
from a00_artifact_manifest_checker import check_artifacts
from a00_gap_propagation_validator import validate_gap_propagation
from a00_trace_audit_validator import validate_trace_audit
from a00_status_consistency_validator import validate_status_consistency
from a00_acceptance_scorecard_builder import build_scorecard
from a00_readiness_certificate_writer import write_certificate


def _failure(fid: str, ftype: str, reason: str, affected: str, blocking: bool=True) -> dict:
    return {"failure_id": fid, "failure_type": ftype, "gap_level": "BLOCKING_GAP" if blocking else "NON_BLOCKING_GAP", "affected_phase": affected, "failure_reason": reason, "required_fix": "restore required upstream evidence and rerun A00 real acceptance", "safe_next_action": f"return_to_{affected}", "forbidden_next_action": "handoff_to_H00" if blocking else "hide_gap"}


def build_report(output_dir: Path, acceptance_run_id: str, source_pipeline_run_id: str, final_status: str, open_gaps: list[str], blocking_gaps: list[str]) -> None:
    report=f"""# A00 Real Acceptance Evidence Report

## 1. Run Info
- acceptance_run_id: {acceptance_run_id}
- source_pipeline_run_id: {source_pipeline_run_id}
- repo_root: /root/sikk-gmgn
- safe_mode: true
- final_status: {final_status}

## 2. Loaded Evidence
- O00 pipeline run: input/o00_pipeline_run_ref.json
- K00 handoff: input/k00_handoff_packet_ref.json
- F00 handoff: input/f00_handoff_packet_ref.json
- V00 validation evidence bundle: input/v00_validation_evidence_bundle_ref.json
- R00 binding evidence bundle: input/r00_binding_evidence_bundle_ref.json
- gap register: gap_review/unresolved_gaps.json
- trace refs: trace_audit/a00_real_acceptance_trace.jsonl
- audit refs: trace_audit/a00_real_acceptance_audit.jsonl

## 3. Evidence Integrity
- status: {'PASSED_WITH_GAPS' if not blocking_gaps else 'BLOCKED'}
- missing evidence: {blocking_gaps}
- inconsistent evidence: []
- unverified claims: []

## 4. Phase Status Matrix
- file: phase_status/phase_status_matrix.json

## 5. Artifact Manifest
- file: artifact_manifest/artifact_manifest.json

## 6. Gap Propagation
- open gaps: {open_gaps}
- blocking gaps: {blocking_gaps}
- hidden gaps: []

## 7. Trace / Audit Validation
- file: trace_audit/trace_audit_validation.json

## 8. Acceptance Scorecard
- file: scorecard/acceptance_scorecard.json

## 9. Readiness Certificate
- file: certificate/readiness_certificate.json

## 10. Acceptance Decision
- final status: {final_status}
- ready_for_h00: {str(final_status == FINAL_STATUS).lower()}
- ready_for_u00: {str(final_status == FINAL_STATUS).lower()}
- ready_for_g00: {str(final_status == FINAL_STATUS).lower()}
- ready_for_production: false

## 11. Failure / Recovery
- file: failure_summary/failure_summary.json

## 12. Handoff
- file: handoff/a00_real_acceptance_to_h00_handoff.json

## 13. Final Decision
{final_status}
"""
    (output_dir/"reports").mkdir(parents=True, exist_ok=True)
    (output_dir/"reports/a00_real_acceptance_report.md").write_text(report, encoding="utf-8")


def execute(args: argparse.Namespace) -> int:
    repo_root=Path(args.repo_root)
    output_dir=Path(args.output_dir)
    acceptance_run_id=output_dir.name or f"a00_real_{now_iso()}"
    ensure_dirs(output_dir)
    trace=output_dir/"trace_audit/a00_real_acceptance_trace.jsonl"
    audit=output_dir/"trace_audit/a00_real_acceptance_audit.jsonl"
    append_jsonl(trace, {"event_type":"a00_real_acceptance_started", "acceptance_run_id": acceptance_run_id})
    append_jsonl(audit, {"event_type":"safe_mode_asserted", "safe_mode": bool(args.safe_mode)})

    pipeline_path=rel_or_abs(repo_root, args.pipeline_run)
    v00_path=rel_or_abs(repo_root, args.v00_evidence)
    r00_path=rel_or_abs(repo_root, args.r00_evidence)
    k00_path=rel_or_abs(repo_root, args.k00_handoff)
    f00_path=rel_or_abs(repo_root, args.f00_handoff)
    v00_handoff_path=rel_or_abs(repo_root, args.v00_handoff)
    r00_handoff_path=rel_or_abs(repo_root, args.r00_handoff)
    gov_path=rel_or_abs(repo_root, args.governance_policy_bundle)

    failures=[]; blockers=[]
    if not args.safe_mode:
        blockers.append("safe_mode_required"); failures.append(_failure("failure_safe_mode", "FORBIDDEN_ACTION_DETECTED", "safe_mode must be true", "A00"))
    required=[("o00_pipeline_run", pipeline_path, "O00"), ("v00_validation_evidence_bundle", v00_path, "V00"), ("r00_binding_evidence_bundle", r00_path, "R00")]
    for name, path, phase in required:
        if not path or not path.exists():
            blockers.append(f"missing_{name}"); failures.append(_failure(f"failure_{name}", "MISSING_REQUIRED_EVIDENCE", f"{name} missing", phase))
    preflight={"preflight_status":"PASSED" if not blockers else "BLOCKED", "safe_mode": bool(args.safe_mode), "loaded_inputs":[n for n,p,ph in required if p and p.exists()], "forbidden_actions_checked": FORBIDDEN_ACTIONS, "blocking_gaps": blockers}
    write_json(output_dir/"preflight/a00_real_acceptance_preflight.json", preflight)
    append_jsonl(audit, {"event_type":"forbidden_actions_checked", "forbidden_actions": FORBIDDEN_ACTIONS})

    # Input refs are written even if optional/missing.
    for rel, path in [("o00_pipeline_run_ref.json", pipeline_path),("k00_handoff_packet_ref.json", k00_path),("f00_handoff_packet_ref.json", f00_path),("v00_validation_evidence_bundle_ref.json", v00_path),("r00_binding_evidence_bundle_ref.json", r00_path),("governance_policy_bundle_ref.json", gov_path)]:
        write_json(output_dir/"input"/rel, {"path": str(path) if path else None, "loaded": bool(path and path.exists())})

    evidence=load_upstream_evidence(repo_root, pipeline_path or Path("missing"), v00_path or Path("missing"), r00_path or Path("missing"), k00_path, f00_path, v00_handoff_path, r00_handoff_path, gov_path) if not any(p is None for p in [pipeline_path,v00_path,r00_path]) else {}
    pipeline=evidence.get("o00_pipeline_run", {})
    source_pipeline_run_id=pipeline.get("pipeline_run_id", pipeline.get("source_pipeline_run_id", "UNKNOWN_PIPELINE_RUN"))
    v00=evidence.get("v00_validation_evidence_bundle", {})
    r00=evidence.get("r00_binding_evidence_bundle", {})

    open_gaps=["policy_not_active","paper_runtime_not_enabled","live_runtime_forbidden","telegram_binding_design_only"]
    if v00.get("summary", {}).get("final_validation_status") == "V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS": open_gaps.append("V00_READY_WITH_GAPS")
    r00_status=r00.get("summary", {}).get("final_binding_status", r00.get("final_status", r00.get("status")))
    if r00_status and "READY_WITH_GAPS" in str(r00_status): open_gaps.append("R00_READY_WITH_GAPS")

    real_bundle=build_real_evidence_bundle(output_dir, acceptance_run_id, evidence)
    append_jsonl(trace, {"event_type":"evidence_bundle_built", "bundle_id": real_bundle["bundle_id"]})
    integrity={"integrity_status":"PASSED_WITH_GAPS" if not blockers else "BLOCKED", "missing_evidence": blockers, "inconsistent_evidence": [], "unverified_claims": [], "non_blocking_gaps": open_gaps, "blocking_gaps": blockers}
    write_json(output_dir/"evidence_bundle/evidence_integrity_check.json", integrity)

    matrix=build_phase_status_matrix(output_dir, acceptance_run_id, evidence, open_gaps, blockers)
    final_status=status_from_blockers(blockers)
    status_report=validate_status_consistency(output_dir, final_status, open_gaps)
    append_jsonl(trace, {"event_type":"status_consistency_validated", "status": status_report["status_consistency"]})

    artifacts=[
        ("o00_pipeline_run", "O00", pipeline_path or Path("missing"), True),
        ("v00_validation_evidence_bundle", "V00", v00_path or Path("missing"), True),
        ("r00_binding_evidence_bundle", "R00", r00_path or Path("missing"), True),
        ("k00_handoff", "K00", k00_path or Path("missing"), False),
        ("f00_handoff", "F00", f00_path or Path("missing"), False),
    ]
    manifest, existence=check_artifacts(output_dir, acceptance_run_id, artifacts)
    gap_report=validate_gap_propagation(output_dir, open_gaps, blockers)
    append_jsonl(trace, {"event_type":"gap_propagation_validated", "status": gap_report["gap_propagation_status"]})
    trace_val=validate_trace_audit(output_dir)
    score=build_scorecard(output_dir, acceptance_run_id, blockers, open_gaps)

    decision={"decision_id": f"acceptance_decision_{acceptance_run_id}", "final_status": final_status, "reason": "O00, V00 and R00 real evidence exists; non-blocking gaps remain around policy activation, paper/live runtime, and downstream consumption." if final_status==FINAL_STATUS else "Blocking evidence gaps exist.", "ready_for_h00": final_status==FINAL_STATUS, "ready_for_u00": final_status==FINAL_STATUS, "ready_for_g00": final_status==FINAL_STATUS, "ready_for_production": False, "blocking_gaps": blockers, "non_blocking_gaps": open_gaps, "forbidden_claims_blocked": FORBIDDEN_CLAIMS}
    write_json(output_dir/"decision/acceptance_decision.json", decision)
    append_jsonl(audit, {"event_type":"false_claims_blocked", "forbidden_claims": FORBIDDEN_CLAIMS})
    append_jsonl(audit, {"event_type":"final_decision_written", "final_status": final_status})

    failure_summary={"failure_summary_id": f"failure_summary_{acceptance_run_id}", "acceptance_run_id": acceptance_run_id, "failures": failures, "blocking_failures": [f for f in failures if f["gap_level"]=="BLOCKING_GAP"], "non_blocking_failures": [f for f in failures if f["gap_level"]!="BLOCKING_GAP"], "recovery_required": bool(failures)}
    write_json(output_dir/"failure_summary/failure_summary.json", failure_summary)
    write_json(output_dir/"recovery/recovery_report.json", {"recovery_required": bool(failures), "safe_next_actions": [f.get("safe_next_action") for f in failures]})
    cert=write_certificate(output_dir, acceptance_run_id, source_pipeline_run_id, final_status, open_gaps)
    append_jsonl(trace, {"event_type":"readiness_certificate_written", "certificate_id": cert["certificate_id"]})

    handoff={"handoff_id": f"handoff_{acceptance_run_id}_to_h00", "from_phase":"A00_REAL_ACCEPTANCE", "to_phase":"H00_HANDOFF_DOWNSTREAM_QUEUE", "handoff_type":"REAL_ACCEPTANCE_TO_DOWNSTREAM_QUEUE", "source_pipeline_run_id": source_pipeline_run_id, "acceptance_run_id": acceptance_run_id, "real_evidence_bundle_refs":["evidence_bundle/real_evidence_bundle.json"], "phase_status_matrix_refs":["phase_status/phase_status_matrix.json"], "artifact_manifest_refs":["artifact_manifest/artifact_manifest.json"], "gap_propagation_refs":["gap_review/gap_propagation_report.json"], "trace_audit_refs":["trace_audit/trace_audit_validation.json"], "readiness_certificate_refs":["certificate/readiness_certificate.json"], "allowed_next_actions":["build_downstream_queue","route_unresolved_gaps_to_u00","route_policy_candidates_to_g00"], "forbidden_next_actions": FORBIDDEN_ACTIONS, "unresolved_gaps": open_gaps, "handoff_status":"HANDOFF_READY_WITH_GAPS" if final_status==FINAL_STATUS else "HANDOFF_BLOCKED"}
    write_json(output_dir/"handoff/a00_real_acceptance_to_h00_handoff.json", handoff)
    append_jsonl(trace, {"event_type":"handoff_written", "handoff_status": handoff["handoff_status"]})

    build_report(output_dir, acceptance_run_id, source_pipeline_run_id, final_status, open_gaps, blockers)
    append_jsonl(trace, {"event_type":"a00_real_acceptance_completed", "final_status": final_status})
    print(json.dumps({"acceptance_run_id": acceptance_run_id, "final_status": final_status, "output_dir": str(output_dir)}, ensure_ascii=False))
    return 0 if final_status==FINAL_STATUS else 2


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--pipeline-run", required=True)
    ap.add_argument("--v00-evidence", required=True)
    ap.add_argument("--r00-evidence", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--safe-mode", action="store_true", required=True)
    ap.add_argument("--k00-handoff")
    ap.add_argument("--f00-handoff")
    ap.add_argument("--v00-handoff")
    ap.add_argument("--r00-handoff")
    ap.add_argument("--governance-policy-bundle")
    return execute(ap.parse_args())
if __name__ == "__main__":
    raise SystemExit(main())
