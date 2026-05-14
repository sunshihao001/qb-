from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

TASK_ID = "task_6_patch_regression_loop"
WAVE_ID = "patch_and_regression"
SAFETY_BOUNDARY = {
    "real_trade": "forbidden",
    "signing": "forbidden",
    "broadcast": "forbidden",
    "secret_read": "forbidden",
    "runtime_apply": "forbidden",
    "strategy_auto_modify": "forbidden",
}
RESUME_CONTRACT = {
    "supports_resume_from_checkpoint": True,
    "supports_skip_completed_phase": True,
    "supports_rerun_failed_wave": True,
    "supports_freeze_downstream_on_blocking": True,
    "idempotent_artifact_writes": True,
    "requires_manual_confirmation_for_runtime_apply": True,
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(path)


def _normalize_severity(issue: Mapping[str, Any]) -> str:
    severity = str(issue.get("severity") or "degraded").lower()
    if severity in {"blocker", "blocking", "rejected", "critical"}:
        return "blocking"
    return "degraded"


def _target_from_issue(issue: Mapping[str, Any]) -> str:
    issue_id = str(issue.get("issue_id") or issue.get("code") or "unknown_issue").lower()
    phase = str(issue.get("phase") or "").lower()
    combined = f"{issue_id} {phase}"
    for idx in range(1, 10):
        token = f"phase_{idx:02d}"
        if token in combined or f"p{idx:02d}" in combined:
            return token
    if "wave4" in combined or "wave_04" in combined or "p08" in combined or "p09" in combined:
        return "wave_04_p08_p09"
    if "wave3" in combined or "wave_03" in combined or "p06" in combined or "p07" in combined:
        return "wave_03_p06_p07"
    if "wave2" in combined or "wave_02" in combined or "p04" in combined or "p05" in combined:
        return "wave_02_p04_p05"
    if "wave1" in combined or "wave_01" in combined or "p01" in combined or "p02" in combined or "p03" in combined:
        return "wave_01_p01_p03"
    return "full_system_e2e"


def _build_regression_plan(issues: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for issue in issues:
        severity = _normalize_severity(issue)
        target = _target_from_issue(issue)
        if target.startswith("phase_"):
            rerun_scope = "single_phase_then_downstream_wave_replay"
        elif target.startswith("wave_"):
            rerun_scope = target
        else:
            rerun_scope = "full_system_e2e"
        plan.append(
            {
                "issue_id": issue.get("issue_id") or issue.get("code") or "UNKNOWN_ISSUE",
                "severity": severity,
                "target": target,
                "repair_action": "manual_or_safe_patch_required" if severity == "blocking" else "carry_gap_and_rerun_regression",
                "rerun_scope": rerun_scope,
                "rerun_targets": _expand_rerun_targets(target),
                "checkpoint_policy": "freeze_downstream_until_manual_review" if severity == "blocking" else "reuse_upstream_and_rerun_affected_scope",
                "status": "blocked_pending_manual_review" if severity == "blocking" else "planned_gap_aware_regression",
                "reason": issue.get("reason") or issue.get("detail") or "missing",
            }
        )
    return plan


def _expand_rerun_targets(target: str) -> list[str]:
    if target.startswith("phase_"):
        try:
            start = int(target.split("_")[1])
        except (IndexError, ValueError):
            return ["full_system_e2e"]
        return [f"phase_{idx:02d}" for idx in range(start, 10)] + ["full_system_e2e", "patch_and_regression"]
    if target.startswith("wave_"):
        return [target, "full_system_e2e", "patch_and_regression"]
    return ["full_system_e2e", "patch_and_regression"]


def _build_gap_closure_package(regression_plan: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    blocking_items = [item for item in regression_plan if item.get("severity") == "blocking"]
    degraded_items = [item for item in regression_plan if item.get("severity") == "degraded"]
    return {
        "package_id": "gap_closure_patch_regression_v1",
        "closure_status": "blocked" if blocking_items else ("open_with_gaps" if degraded_items else "closed"),
        "blocking_count": len(blocking_items),
        "degraded_count": len(degraded_items),
        "safe_auto_patch_allowed": False,
        "runtime_apply_allowed": False,
        "manual_review_required": bool(blocking_items),
        "closure_items": [
            {
                "issue_id": item.get("issue_id"),
                "target": item.get("target"),
                "rerun_scope": item.get("rerun_scope"),
                "rerun_targets": item.get("rerun_targets"),
                "checkpoint_policy": item.get("checkpoint_policy"),
                "acceptance_gate": "targeted_regression_then_full_system_e2e",
                "evidence_required": [
                    "positive_evidence",
                    "negative_evidence_or_counter_evidence",
                    "audit_ref",
                    "handoff_ref",
                ],
            }
            for item in regression_plan
        ],
    }


def _build_audit(result: Mapping[str, Any]) -> str:
    lines = [
        "# Patch + Regression Loop Audit",
        "",
        f"- task_id: {result.get('task_id')}",
        f"- wave_id: {result.get('wave_id')}",
        f"- final_status: {result.get('final_status')}",
        f"- blocking_issue_count: {result.get('blocking_issue_count')}",
        f"- degraded_issue_count: {result.get('degraded_issue_count')}",
        f"- next_allowed_task: {result.get('next_allowed_task')}",
        "- boundary: paper-only / no real trade / no signing / no broadcast / no secrets / no runtime apply",
        "",
        "## Resume Contract",
    ]
    for key, value in (result.get("resume_contract") or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Gap Closure Package"])
    package = result.get("gap_closure_package") or {}
    lines.append(f"- closure_status: {package.get('closure_status')}")
    lines.append(f"- safe_auto_patch_allowed: {package.get('safe_auto_patch_allowed')}")
    lines.append(f"- runtime_apply_allowed: {package.get('runtime_apply_allowed')}")
    lines.extend(["", "## Regression Plan"])
    for item in result.get("regression_plan") or []:
        lines.append(f"- {item.get('issue_id')}｜{item.get('severity')}｜{item.get('target')}｜{item.get('status')}")
    if not result.get("regression_plan"):
        lines.append("- none")
    return "\n".join(lines) + "\n"


def run_patch_and_regression(
    *,
    root: str | Path,
    issues: Sequence[Mapping[str, Any]],
    output_dir: str | Path,
    mode: str = "dry-run",
    source_result_path: str | None = None,
) -> dict[str, Any]:
    out = Path(output_dir)
    control_dir = out / "control"
    audit_dir = out / "audit"
    handoff_dir = out / "handoff"
    state_dir = out / "state"
    for directory in [control_dir, audit_dir, handoff_dir, state_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    started_at = _now()
    normalized_issues = [dict(issue, severity=_normalize_severity(issue)) for issue in issues]
    blocking = [issue for issue in normalized_issues if issue["severity"] == "blocking"]
    degraded = [issue for issue in normalized_issues if issue["severity"] == "degraded"]
    regression_plan = _build_regression_plan(normalized_issues)
    gap_closure_package = _build_gap_closure_package(regression_plan)

    if blocking:
        final_status = "PATCH_REGRESSION_REJECTED"
        next_allowed_task = "manual_review_required"
        handoff_status = "HANDOFF_BLOCKED"
    elif degraded:
        final_status = "PATCH_REGRESSION_READY_WITH_GAPS"
        next_allowed_task = "rerun_failed_wave_or_full_system_e2e"
        handoff_status = "HANDOFF_DEGRADED"
    else:
        final_status = "PATCH_REGRESSION_READY"
        next_allowed_task = "FULL_SYSTEM_AUTOMATION_READY"
        handoff_status = "HANDOFF_READY"

    result: dict[str, Any] = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "mode": mode,
        "started_at": started_at,
        "completed_at": _now(),
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": next_allowed_task,
        "source_result_path": source_result_path or "missing",
        "blocking_issue_count": len(blocking),
        "degraded_issue_count": len(degraded),
        "issues": normalized_issues,
        "regression_plan": regression_plan,
        "gap_closure_package": gap_closure_package,
        "safety_boundary": SAFETY_BOUNDARY,
        "resume_contract": RESUME_CONTRACT,
        "runtime_apply_allowed": False,
        "requires_manual_confirmation": True,
    }

    gap_register = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "blocking_issues": blocking,
        "degraded_issues": degraded,
        "regression_plan": regression_plan,
        "gap_closure_package": gap_closure_package,
        "repair_route": next_allowed_task,
    }
    state = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "next_allowed_task": next_allowed_task,
        "resume_contract": RESUME_CONTRACT,
        "gap_closure_package": gap_closure_package,
        "runtime_apply_allowed": False,
    }
    handoff = {
        "current_task": TASK_ID,
        "wave_id": WAVE_ID,
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": next_allowed_task,
        "regression_plan": regression_plan,
        "gap_closure_package": gap_closure_package,
        "runtime_apply_allowed": False,
        "requires_manual_confirmation": True,
        "safety_boundary": SAFETY_BOUNDARY,
    }

    artifacts = {
        "patch_gap_register": _write_json(audit_dir / "patch_regression_gap_register.json", gap_register),
        "gap_closure_package": _write_json(control_dir / "gap_closure_package.json", gap_closure_package),
        "patch_state": _write_json(state_dir / "patch_regression_state.json", state),
        "patch_handoff": _write_json(handoff_dir / "patch_regression_handoff_packet.json", handoff),
    }
    result["artifacts"] = artifacts
    artifacts["patch_audit"] = str(audit_dir / "patch_regression_audit.md")
    Path(artifacts["patch_audit"]).write_text(_build_audit(result), encoding="utf-8")
    artifacts["patch_result"] = _write_json(control_dir / "patch_regression_result.json", result)
    return result


def _load_issues(path: str | Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    payload = json.loads(p.read_text(encoding="utf-8"))
    return list(payload.get("blocking_issues") or []) + list(payload.get("degraded_issues") or [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HER Patch + Regression loop in dry-run/replay mode")
    parser.add_argument("--root", default=".")
    parser.add_argument("--issues-file")
    parser.add_argument("--source-result-path")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "replay"])
    args = parser.parse_args()
    issues = _load_issues(args.issues_file or args.source_result_path)
    result = run_patch_and_regression(
        root=args.root,
        issues=issues,
        output_dir=args.output_dir,
        mode=args.mode,
        source_result_path=args.source_result_path,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
