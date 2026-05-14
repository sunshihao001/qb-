#!/usr/bin/env python3
"""U00 REAL Review / Upgrade executor for HER.

Consumes an H00→U00 handoff (or O00 sample handoff refs) in safe mode and writes
review evidence, root-cause analysis, upgrade candidates, upgrade queue,
learning index, governance handoff candidates, trace/audit, acceptance, and a
final report.

This executor does not apply upgrades, mutate production rules, start runners,
trade, sign wallets, deploy, or convert READY_WITH_GAPS into accepted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

FORBIDDEN_ACTIONS = [
    "live_runtime",
    "wallet_signing",
    "auto_deploy",
    "production_trading",
    "execute_downstream_task_directly",
    "modify_production_rules_directly",
    "drop_unresolved_gaps",
    "convert_ready_with_gaps_to_ready",
]

REQUIRED_DIRS = [
    "input", "preflight", "evidence", "review_cases", "root_cause", "recurring",
    "patterns", "upgrade_candidates", "upgrade_queue", "learning", "handoffs",
    "trace", "gaps", "recovery", "acceptance", "reports",
]

SCHEMA_DIR = Path("system/her_document_function_system/controllers/U00_review_upgrade_controller")
DATA_DIR = Path("data/her_document_function_system/u00_real_review_runs")


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S_%f")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_jsonl(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + "\n")


def resolve(repo: Path, maybe: str | None) -> Path | None:
    if not maybe:
        return None
    p = Path(maybe)
    return p if p.is_absolute() else repo / p


def ref(path: Path) -> Dict[str, Any]:
    return {"path": str(path), "exists": path.exists()}


def ensure_run_dirs(run_dir: Path) -> None:
    for rel in REQUIRED_DIRS:
        (run_dir / rel).mkdir(parents=True, exist_ok=True)


class U00Run:
    def __init__(self, repo: Path, run_id: str | None = None):
        self.repo = repo
        self.run_id = run_id or f"u00_real_review_{stamp()}"
        self.run_dir = repo / DATA_DIR / self.run_id
        ensure_run_dirs(self.run_dir)
        self.trace_path = self.run_dir / "trace/u00_trace.jsonl"
        self.audit_path = self.run_dir / "trace/u00_audit.jsonl"

    def trace(self, event_type: str, **extra: Any) -> None:
        append_jsonl(self.trace_path, {
            "event_id": f"{event_type}_{stamp()}",
            "timestamp": utcnow(),
            "phase_id": "U00_REAL",
            "run_id": self.run_id,
            "event_type": event_type,
            **extra,
        })

    def audit(self, event_type: str, **extra: Any) -> None:
        append_jsonl(self.audit_path, {
            "timestamp": utcnow(),
            "phase_id": "U00_REAL",
            "run_id": self.run_id,
            "event_type": event_type,
            **extra,
        })


def normalize_gap(gap: Dict[str, Any], idx: int, source_ref: str) -> Dict[str, Any]:
    gap_id = gap.get("gap_id") or gap.get("id") or f"gap_imported_{idx:03d}"
    level = gap.get("gap_level") or ("BLOCKING_GAP" if gap.get("blocking") is True else "NON_BLOCKING_GAP")
    reason = gap.get("reason") or gap.get("failure_reason") or gap.get("message") or gap.get("gap_type") or "unspecified_gap"
    return {
        "case_id": f"review_case_{gap_id}",
        "case_type": "GAP_CASE",
        "source_phase": gap.get("source_phase") or gap.get("phase") or "UNKNOWN",
        "severity": level,
        "symptom": str(reason),
        "affected_assets": gap.get("affected_assets") or ([gap.get("affected_asset")] if gap.get("affected_asset") else []),
        "evidence_refs": [source_ref],
        "gap_refs": [gap_id],
        "current_status": "OPEN",
        "raw_gap": gap,
    }


def load_gap_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(payload.get("gaps"), list):
        return payload["gaps"]
    if isinstance(payload.get("unresolved_gaps"), list):
        items = payload["unresolved_gaps"]
        return [{"gap_id": x, "reason": x, "gap_level": "NON_BLOCKING_GAP"} if isinstance(x, str) else x for x in items]
    if isinstance(payload.get("gap_refs"), list):
        return [{"gap_id": str(x), "reason": str(x), "gap_level": "NON_BLOCKING_GAP"} for x in payload["gap_refs"]]
    if isinstance(payload.get("blocking_gaps"), list) or isinstance(payload.get("non_blocking_gaps"), list):
        items = list(payload.get("blocking_gaps") or []) + list(payload.get("non_blocking_gaps") or [])
        return [{"gap_id": x, "reason": x, "gap_level": "NON_BLOCKING_GAP"} if isinstance(x, str) else x for x in items]
    return []


def collect_inputs(repo: Path, h00_handoff: Path | None, o00_run_id: str | None) -> Tuple[Dict[str, Path], List[Dict[str, Any]]]:
    refs: Dict[str, Path] = {}
    gaps: List[Dict[str, Any]] = []
    if h00_handoff:
        refs["h00_handoff"] = h00_handoff
        if h00_handoff.exists():
            handoff_payload = read_json(h00_handoff)
            for g in load_gap_items(handoff_payload):
                g2 = dict(g)
                g2.setdefault("source_phase", handoff_payload.get("from_phase", "H00_REAL_DOWNSTREAM_QUEUE"))
                g2.setdefault("_source_ref", str(h00_handoff))
                gaps.append(g2)
            h00_run_dir = h00_handoff.parent.parent
            relative_candidates = {
                "h00_routing_decision": h00_run_dir / "routing/routing_decision.json",
                "h00_downstream_queue": h00_run_dir / "queue/downstream_queue.json",
                "h00_report": h00_run_dir / "reports/h00_real_queue_report.md",
            }
            refs.update({k: v for k, v in relative_candidates.items()})
    if o00_run_id:
        root = repo / "data/her_document_function_system/o00_runs" / o00_run_id
        candidates = {
            "h00_handoff": root / "handoffs/h00_to_u00_ref.json",
            "a00_handoff": root / "handoffs/a00_to_h00_ref.json",
            "a00_evidence_bundle": root / "evidence/pipeline_evidence_bundle.json",
            "phase_status_matrix": root / "state/stage_state_matrix.json",
            "queue_state": root / "queue/pipeline_queue.json",
            "gap_report": root / "gaps/pipeline_gap_register.json",
            "unresolved_gaps": root / "gaps/unresolved_gaps.json",
            "accepted_risks": root / "gaps/accepted_risks.json",
            "trace": root / "trace/o00_trace.jsonl",
            "audit": root / "trace/o00_audit.jsonl",
        }
        refs.update({k: v for k, v in candidates.items()})
    for key in ["gap_report", "unresolved_gaps"]:
        path = refs.get(key)
        if path and path.exists():
            for g in load_gap_items(read_json(path)):
                g2 = dict(g)
                g2.setdefault("_source_ref", str(path))
                gaps.append(g2)
    return refs, gaps


def classify_root_cause(case: Dict[str, Any]) -> Dict[str, Any]:
    text = (case.get("symptom", "") + " " + " ".join(case.get("gap_refs", []))).lower()
    if "test" in text and "not_executed" in text:
        cause = "MISSING_TEST_EXECUTION_EVIDENCE"
        fix = "TEST_UPGRADE"
        target = "V00"
    elif "policy" in text or "governance" in text or "g00" in text:
        cause = "GOVERNANCE_POLICY_NOT_ACTIVE"
        fix = "GOVERNANCE_UPGRADE"
        target = "G00"
    elif "runner" in text or "r00" in text:
        cause = "RUNNER_BINDING_NOT_REQUIRED_OR_NOT_BOUND"
        fix = "RUNNER_BINDING_UPGRADE"
        target = "R00"
    elif "handoff" in text:
        cause = "HANDOFF_CONTRACT_OR_PACKET_GAP"
        fix = "HANDOFF_UPGRADE"
        target = "H00"
    else:
        cause = "UNCLASSIFIED_REVIEW_GAP"
        fix = "CONTROLLER_UPGRADE"
        target = case.get("source_phase") or "U00"
    return {
        "root_cause_id": f"rca_{case['case_id']}",
        "review_case_id": case["case_id"],
        "root_cause_type": cause,
        "root_cause_statement": f"{case['symptom']} -> {cause}",
        "causal_chain": [case.get("source_phase", "UNKNOWN"), cause, fix],
        "confidence": "MEDIUM" if cause == "UNCLASSIFIED_REVIEW_GAP" else "HIGH",
        "required_fix_type": fix,
        "recommended_owner": target,
        "evidence_refs": case.get("evidence_refs", []),
    }


def candidate_from_rca(rca: Dict[str, Any], idx: int) -> Dict[str, Any]:
    fix = rca["required_fix_type"]
    target = rca["recommended_owner"]
    priority = "P1_HIGH" if fix in {"TEST_UPGRADE", "GOVERNANCE_UPGRADE", "RUNNER_BINDING_UPGRADE"} else "P2_MEDIUM"
    requires_governance = fix == "GOVERNANCE_UPGRADE"
    return {
        "upgrade_candidate_id": f"uc_u00_real_{idx:03d}",
        "upgrade_type": fix,
        "target_controller": target,
        "target_asset": f"{target.lower()}_controller_or_runtime_assets",
        "problem_statement": rca["root_cause_statement"],
        "proposed_change": f"Create or improve {fix.lower()} evidence/control for {target}; keep existing gap until verified by downstream acceptance.",
        "evidence_refs": rca.get("evidence_refs", []),
        "expected_impact": "Moves recurring READY_WITH_GAPS item toward executable, auditable evidence without bypassing safe-mode boundaries.",
        "priority": priority,
        "requires_governance": requires_governance,
        "handoff_target": "G00" if requires_governance else target,
        "source_root_cause_id": rca["root_cause_id"],
    }


def validate_json_schemas(repo: Path) -> Dict[str, Any]:
    try:
        import jsonschema  # type: ignore
        from jsonschema.validators import validator_for  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"status": "SCHEMA_VALIDATION_SKIPPED", "reason": str(exc), "valid_schemas": [], "invalid_schemas": []}
    valid, invalid = [], []
    for rel in sorted((repo / SCHEMA_DIR).glob("*.schema.json")):
        try:
            schema = read_json(rel)
            validator_cls = validator_for(schema)
            validator_cls.check_schema(schema)
            valid.append(str(rel))
        except Exception as exc:
            invalid.append({"path": str(rel), "error": str(exc)})
    return {"status": "PASSED" if not invalid else "FAILED", "valid_schemas": valid, "invalid_schemas": invalid}


def run(repo: Path, args: argparse.Namespace) -> Tuple[int, Dict[str, Any]]:
    u = U00Run(repo, args.run_id)
    u.trace("u00_real_started", status_after="U00_REAL_STARTED")
    u.audit("safe_mode_boundary", safe_mode=args.safe_mode, forbidden_actions=FORBIDDEN_ACTIONS)
    if not args.safe_mode:
        result = {"status": "U00_REAL_BLOCKED", "reason": "safe_mode_required", "run_id": u.run_id, "run_dir": str(u.run_dir)}
        write_json(u.run_dir / "acceptance/u00_acceptance_result.json", result)
        return 40, result

    h00_path = resolve(repo, args.h00_handoff)
    refs, gap_items = collect_inputs(repo, h00_path, args.o00_run_id)
    for name, path in refs.items():
        write_json(u.run_dir / f"input/{name}_ref.json", ref(path))
    missing_required = [name for name in ["h00_handoff"] if name not in refs or not refs[name].exists()]
    optional_context_missing = [name for name in ["a00_evidence_bundle", "phase_status_matrix", "queue_state", "gap_report"] if name not in refs or not refs[name].exists()]
    preflight_status = "PASSED" if not missing_required else "READY_WITH_GAPS"
    write_json(u.run_dir / "preflight/u00_preflight_result.json", {
        "preflight_status": preflight_status,
        "safe_mode": True,
        "missing_required_inputs": missing_required,
        "optional_context_missing": optional_context_missing,
        "loaded_gap_items": len(gap_items),
        "allowed_modes": ["REVIEW_EVIDENCE", "BUILD_UPGRADE_CANDIDATES", "WRITE_HANDOFF"],
        "forbidden_modes": FORBIDDEN_ACTIONS,
    })
    u.trace("preflight_checked", status_after=preflight_status, evidence_refs=[str(p) for p in refs.values()])

    review_cases = [normalize_gap(g, i + 1, g.get("_source_ref", "unknown")) for i, g in enumerate(gap_items)]
    if not review_cases:
        review_cases.append({
            "case_id": "review_case_no_gap_inputs_loaded",
            "case_type": "READY_WITH_GAPS_CASE",
            "source_phase": "U00_REAL",
            "severity": "HIGH_GAP",
            "symptom": "No gap inputs were loaded; review can only emit recovery/backlog evidence.",
            "affected_assets": [],
            "evidence_refs": [str(p) for p in refs.values()],
            "gap_refs": ["gap_u00_real_missing_gap_inputs"],
            "current_status": "OPEN",
        })
    write_json(u.run_dir / "review_cases/review_cases.json", {"review_cases": review_cases, "total_cases": len(review_cases)})
    u.trace("review_cases_classified", status_after="REVIEW_CASES_READY", case_count=len(review_cases))

    rcas = [classify_root_cause(c) for c in review_cases]
    write_json(u.run_dir / "root_cause/root_cause_analysis.json", {"root_cause_items": rcas, "total_items": len(rcas)})
    u.trace("root_cause_analyzed", status_after="ROOT_CAUSE_READY", root_cause_count=len(rcas))

    recurring = {}
    for rca in rcas:
        recurring.setdefault(rca["root_cause_type"], 0)
        recurring[rca["root_cause_type"]] += 1
    recurring_items = [{"issue_type": k, "frequency": v, "recurring": v > 1} for k, v in sorted(recurring.items())]
    write_json(u.run_dir / "recurring/recurring_issue_report.json", {"recurring_issues": recurring_items})
    write_json(u.run_dir / "patterns/anti_success_pattern_report.json", {
        "anti_patterns": [{"pattern_id": f"anti_{x['issue_type'].lower()}", "pattern": x["issue_type"], "frequency": x["frequency"]} for x in recurring_items],
        "success_patterns": [{"pattern_id": "success_safe_mode_retained", "pattern": "safe_mode_boundary_retained", "evidence_refs": [str(u.audit_path)]}],
    })

    candidates = [candidate_from_rca(rca, i + 1) for i, rca in enumerate(rcas)]
    write_json(u.run_dir / "upgrade_candidates/upgrade_candidates.json", {"upgrade_candidates": candidates, "total_candidates": len(candidates)})
    priority_summary: Dict[str, int] = {}
    for c in candidates:
        priority_summary[c["priority"]] = priority_summary.get(c["priority"], 0) + 1
    queue_items = [{
        "queue_item_id": f"u00_queue_{i+1:03d}",
        "upgrade_candidate_id": c["upgrade_candidate_id"],
        "target_controller": c["target_controller"],
        "handoff_target": c["handoff_target"],
        "priority": c["priority"],
        "status": "QUEUED_FOR_DOWNSTREAM_REVIEW",
        "allowed_actions": ["read_evidence", "validate_contract", "plan_safe_upgrade", "write_downstream_acceptance"],
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "evidence_refs": c["evidence_refs"],
    } for i, c in enumerate(candidates)]
    queue = {"queue_id": f"u00_upgrade_queue_{u.run_id}", "queue_items": queue_items, "priority_summary": priority_summary, "blocked_items": [], "deferred_items": []}
    write_json(u.run_dir / "upgrade_queue/upgrade_queue.json", queue)
    u.trace("upgrade_queue_built", status_after="UPGRADE_QUEUE_READY", queue_items=len(queue_items))

    governance_candidates = [c for c in candidates if c.get("requires_governance")]
    learning_index = {
        "learning_index_id": f"learning_{u.run_id}",
        "entries": [{"entry_id": f"learn_{i+1:03d}", "lesson_type": rca["root_cause_type"], "recommended_owner": rca["recommended_owner"], "evidence_refs": rca.get("evidence_refs", [])} for i, rca in enumerate(rcas)],
    }
    write_json(u.run_dir / "learning/learning_index.json", learning_index)
    write_json(u.run_dir / "handoffs/u00_to_g00_handoff_packet.json", {
        "handoff_id": f"handoff_{u.run_id}_to_g00",
        "from_phase": "U00_REAL",
        "to_phase": "G00",
        "handoff_type": "U00_TO_G00_HANDOFF",
        "governance_candidates": governance_candidates,
        "forbidden_next_actions": FORBIDDEN_ACTIONS,
        "handoff_status": "HANDOFF_READY_WITH_GAPS" if governance_candidates else "HANDOFF_NOT_REQUIRED_NO_GOVERNANCE_CANDIDATES",
    })
    write_json(u.run_dir / "handoffs/u00_to_backlog_handoff_packet.json", {
        "handoff_id": f"handoff_{u.run_id}_to_backlog",
        "from_phase": "U00_REAL",
        "to_phase": "BACKLOG",
        "handoff_type": "U00_TO_BACKLOG_HANDOFF",
        "upgrade_queue_ref": str(u.run_dir / "upgrade_queue/upgrade_queue.json"),
        "unresolved_gap_refs": [g for c in review_cases for g in c.get("gap_refs", [])],
        "forbidden_next_actions": FORBIDDEN_ACTIONS,
        "handoff_status": "HANDOFF_READY_WITH_GAPS",
    })

    schema_result = validate_json_schemas(repo)
    write_json(u.run_dir / "evidence/schema_validation_result.json", schema_result)
    write_json(u.run_dir / "gaps/u00_gap_report.json", {
        "status": "U00_REAL_READY_WITH_GAPS",
        "gaps": [c for c in review_cases],
        "blocking_gaps": [c for c in review_cases if c.get("severity") == "BLOCKING_GAP"],
        "forbidden_actions": FORBIDDEN_ACTIONS,
    })
    write_json(u.run_dir / "recovery/recovery_report.json", {
        "status": "RECOVERY_READY_WITH_GAPS",
        "safe_next_actions": ["dispatch_upgrade_queue_to_backlog_or_g00_after acceptance", "do_not_execute_live_runtime"],
        "forbidden_actions": FORBIDDEN_ACTIONS,
    })
    acceptance = {
        "phase_id": "U00_REAL",
        "run_id": u.run_id,
        "status": "U00_REAL_READY_WITH_GAPS" if preflight_status != "PASSED" or review_cases else "U00_REAL_ACCEPTED",
        "review_cases_written": True,
        "root_cause_written": True,
        "upgrade_candidates_written": True,
        "upgrade_queue_written": True,
        "learning_index_written": True,
        "handoff_written": True,
        "trace_audit_written": True,
        "schema_validation_status": schema_result["status"],
        "accepted": False,
        "ready_with_gaps": True,
        "blocking": False,
        "forbidden_actions": FORBIDDEN_ACTIONS,
    }
    write_json(u.run_dir / "acceptance/u00_acceptance_result.json", acceptance)
    u.trace("acceptance_checked", status_after=acceptance["status"])
    u.audit("u00_real_review_completed", acceptance_status=acceptance["status"], candidates=len(candidates))

    report = f"""# U00 REAL Review Final Report

- run_id: `{u.run_id}`
- status: `{acceptance['status']}`
- safe_mode: `true`
- review_cases: `{len(review_cases)}`
- root_cause_items: `{len(rcas)}`
- upgrade_candidates: `{len(candidates)}`
- governance_candidates: `{len(governance_candidates)}`
- schema_validation_status: `{schema_result['status']}`

## Evidence Paths
- review_cases: `{u.run_dir / 'review_cases/review_cases.json'}`
- root_cause: `{u.run_dir / 'root_cause/root_cause_analysis.json'}`
- upgrade_candidates: `{u.run_dir / 'upgrade_candidates/upgrade_candidates.json'}`
- upgrade_queue: `{u.run_dir / 'upgrade_queue/upgrade_queue.json'}`
- learning_index: `{u.run_dir / 'learning/learning_index.json'}`
- acceptance: `{u.run_dir / 'acceptance/u00_acceptance_result.json'}`
- trace: `{u.trace_path}`

## Boundary
- live_runtime: forbidden
- wallet_signing: forbidden
- auto_deploy: forbidden
- production_trading: forbidden
- queue_created is not task_executed
"""
    write_text(u.run_dir / "reports/u00_final_report.md", report)
    u.trace("u00_real_completed", status_after=acceptance["status"], output_refs=[str(u.run_dir / "reports/u00_final_report.md")])
    result = {"status": acceptance["status"], "run_id": u.run_id, "run_dir": str(u.run_dir), "final_report": str(u.run_dir / "reports/u00_final_report.md"), "review_cases": len(review_cases), "upgrade_candidates": len(candidates)}
    write_json(u.run_dir / "execution_result.json", result)
    return 10, result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="U00 REAL safe-mode review executor")
    p.add_argument("--repo-root", default="/root/sikk-gmgn")
    p.add_argument("--safe-mode", action="store_true")
    p.add_argument("--h00-handoff")
    p.add_argument("--o00-run-id")
    p.add_argument("--run-id")
    return p


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    code, result = run(Path(args.repo_root), args)
    print("U00_REAL_RESULT=" + json.dumps({"exit_code": code, **result}, ensure_ascii=False, separators=(",", ":")))
    print(json.dumps({"exit_code": code, "result": result}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
