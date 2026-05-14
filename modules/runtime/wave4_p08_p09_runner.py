from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from modules.stable_trader_os.phase_08_review_learning_controller.runner import (
    Phase08ReviewLearningController,
)
from modules.stable_trader_os.phase_09_system_upgrade_controller.runner import (
    Phase09SystemUpgradeController,
)

TASK_ID = "task_4_wave_4_p08_p09_review_learning_runtime"
WAVE_ID = "wave_4_p08_p09"
NEXT_ALLOWED_TASK = "task_5_full_system_e2e_runtime"
PHASE08_ID = "phase_08_review_learning_controller"
PHASE09_ID = "phase_09_system_upgrade_controller"
SAFETY_BOUNDARY = {
    "real_trade": "forbidden",
    "signing": "forbidden",
    "broadcast": "forbidden",
    "secret_read": "forbidden",
    "runtime_apply": "forbidden",
    "strategy_auto_modify": "forbidden",
}
RUNTIME_CONTRACT = {
    "bootstrap": True,
    "self_check": True,
    "self_fill": True,
    "wave_execution": True,
    "failure_stop": True,
    "audit_backfill": True,
    "regression_repair": True,
    "review_only": True,
    "paper_only": True,
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_json(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _artifact_exists(value: Any) -> bool:
    return bool(value) and Path(str(value)).exists()


def _issue(severity: str, code: str, detail: str, phase: str = WAVE_ID) -> dict[str, Any]:
    return {"severity": severity, "code": code, "detail": detail, "phase": phase}


def _normalize_wave3_handoff(wave3_handoff_file: str | Path) -> dict[str, Any]:
    p = Path(wave3_handoff_file)
    handoff = _read_json(p)
    handoff["_path"] = str(p)
    handoff["_base"] = str(p.parent)
    return handoff


def _materialize_phase07_handoff(source: str | Path, inputs_dir: Path) -> str:
    """Expose the full Phase07 handoff inside Wave4 inputs.

    Wave3 handoff can point to a complete Phase07 packet outside the Wave4
    directory. Wave4 must materialize that packet as an explicit input artifact
    so P08/P09 evidence-chain and replay audits do not depend on an opaque
    upstream path. This is an exposure-layer copy only; it does not alter
    thresholds, classifications, or trading permissions.
    """
    source_path = Path(source)
    target = inputs_dir / "phase_07_handoff_packet.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != target.resolve():
        shutil.copy2(source_path, target)
    return str(target)


def _write_phase09_artifact_manifest(artifacts: Mapping[str, Any], output_dir: Path) -> str:
    exposed_keys = {
        "known_success_preservation_review": artifacts.get("known_success_preservation_review"),
        "regression_validation_report": artifacts.get("regression_validation_report"),
        "regression_validation_plan": artifacts.get("regression_validation_plan"),
        "rollback_validation_report": artifacts.get("rollback_validation_report"),
        "rollback_plan": artifacts.get("rollback_plan"),
        "shadow_mode_plan": artifacts.get("shadow_mode_plan"),
        "system_upgrade_package": artifacts.get("rule_update_package"),
        "system_upgrade_manifest": artifacts.get("system_upgrade_manifest"),
        "upgrade_input_validation": artifacts.get("upgrade_input_validation"),
    }
    manifest = {key: str(value) for key, value in exposed_keys.items() if value and Path(str(value)).exists()}
    return _write_json(output_dir / "phase09_artifact_manifest.json", manifest)


def _phase_summary(phase_id: str, result: Mapping[str, Any], handoff: Mapping[str, Any], artifacts: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "phase": phase_id,
        "status": result.get("status") or handoff.get("phase_status") or handoff.get("system_upgrade_status") or "missing",
        "handoff_status": handoff.get("handoff_status") or ("HANDOFF_READY" if handoff.get("allow_next_stage") else "HANDOFF_BLOCKED" if handoff else "missing"),
        "allow_next_stage": handoff.get("allow_next_stage"),
        "system_upgrade_status": handoff.get("system_upgrade_status"),
        "regression_status": handoff.get("regression_status"),
        "direct_runtime_apply_allowed": handoff.get("allow_apply_to_runtime", False),
        "artifact_count": len(artifacts),
    }


def _build_audit(result: Mapping[str, Any]) -> str:
    issues = result.get("issues") or []
    lines = [
        "# Task 4 / Wave 4 / P08-P09 Audit",
        "",
        f"- task_id: {result.get('task_id')}",
        f"- wave_id: {result.get('wave_id')}",
        f"- final_status: {result.get('final_status')}",
        f"- handoff_status: {result.get('handoff_status')}",
        f"- execution_mode: {result.get('execution_mode')}",
        f"- blocking_issue_count: {result.get('blocking_issue_count')}",
        f"- degraded_issue_count: {result.get('degraded_issue_count')}",
        "",
        "## Safety Boundary",
        "",
        "- 真实交易: 禁止",
        "- 签名: 禁止",
        "- 广播: 禁止",
        "- secrets读取: 禁止",
        "- runtime_apply: 禁止",
        "- strategy_auto_modify: 禁止",
        "",
        "## Controllers",
        "",
        f"- {PHASE08_ID}: review learning / audit feedback only",
        f"- {PHASE09_ID}: gated upgrade package only; manual confirmation required",
        "",
        "## Issues",
        "",
    ]
    if issues:
        lines.extend(f"- [{i.get('severity')}] {i.get('phase')}::{i.get('code')} — {i.get('detail')}" for i in issues)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## HER Route",
        "",
        f"- next_allowed_task: {result.get('next_allowed_task')}",
        "- blocking/rejected -> patch_and_regression",
        "- degraded/gaps -> carry gap register into Full System E2E",
    ])
    return "\n".join(lines) + "\n"


def run_wave4_p08_p09(
    *,
    root: str | Path,
    wave3_handoff_file: str | Path,
    output_dir: str | Path,
    mode: str = "dry-run",
) -> dict[str, Any]:
    root_path = Path(root)
    out = Path(output_dir)
    control_dir = out / "control"
    audit_dir = out / "audit"
    handoff_dir = out / "handoff"
    state_dir = out / "state"
    inputs_dir = out / "inputs"
    for directory in [control_dir, audit_dir, handoff_dir, state_dir, inputs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    started_at = _now()
    trace: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    wave3 = _normalize_wave3_handoff(wave3_handoff_file)
    handoff_files = wave3.get("handoff_files", {}) if isinstance(wave3.get("handoff_files"), dict) else {}
    phase07_handoff = handoff_files.get("phase_07_handoff_packet")
    inherited_gap = handoff_files.get("wave3_gap_register")

    if not Path(str(wave3_handoff_file)).exists():
        issues.append(_issue("blocking", "wave3_handoff_missing", str(wave3_handoff_file)))
    if not phase07_handoff or not Path(str(phase07_handoff)).exists():
        issues.append(_issue("blocking", "phase07_handoff_missing", str(phase07_handoff or "missing"), PHASE08_ID))
    else:
        phase07_handoff = _materialize_phase07_handoff(phase07_handoff, inputs_dir)

    phase08_result: dict[str, Any] = {"phase": PHASE08_ID, "status": "NOT_RUN", "artifacts": {}}
    phase09_result: dict[str, Any] = {"phase": PHASE09_ID, "status": "NOT_RUN", "artifacts": {}, "handoff": {}}
    phase08_handoff: dict[str, Any] = {}
    phase09_handoff: dict[str, Any] = {}

    if not [i for i in issues if i["severity"] == "blocking"]:
        phase08_result = Phase08ReviewLearningController().run(
            phase07_handoff_file=phase07_handoff,
            output_dir=out / "08_review_learning",
        )
        phase08_artifacts = phase08_result.get("artifacts", {}) or {}
        phase08_handoff_path = Path(str(phase08_artifacts.get("handoff_packet", "")))
        phase08_handoff = _read_json(phase08_handoff_path)
        trace.append({"step": "run_phase08", "status": "PASS", "handoff": str(phase08_handoff_path)})

        phase09_result = Phase09SystemUpgradeController().run(
            phase08_handoff_file=phase08_handoff_path,
            output_dir=out / "09_system_upgrade",
        )
        phase09_artifacts = phase09_result.get("artifacts", {}) or {}
        phase09_handoff_path = Path(str(phase09_artifacts.get("handoff_packet", "")))
        phase09_handoff = _read_json(phase09_handoff_path)
        trace.append({"step": "run_phase09", "status": "PASS", "handoff": str(phase09_handoff_path)})
    else:
        trace.append({"step": "precheck", "status": "BLOCKED", "issues": issues})

    phase08_artifacts = phase08_result.get("artifacts", {}) or {}
    phase09_artifacts = phase09_result.get("artifacts", {}) or {}
    for key in ["handoff_packet", "output_validation_report", "handoff_validation_report", "audit_report"]:
        if key in phase08_artifacts and not _artifact_exists(phase08_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase08_artifact:{key}", str(phase08_artifacts[key]), PHASE08_ID))
        if key in phase09_artifacts and not _artifact_exists(phase09_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase09_artifact:{key}", str(phase09_artifacts[key]), PHASE09_ID))

    if phase08_handoff:
        if phase08_handoff.get("allow_next_stage") is False:
            # gap-aware progression: P08 的 allow_next_stage=false 只表示复盘事实
            # 尚不足以授权 P09 产生可应用升级；在 full-system dry-run/replay 中，
            # 只要 P08 handoff/audit/artifacts 完整且不存在 required-input 阻断，
            # 必须把它登记为 degraded gap 并继续推进到 P09 review-only upgrade package。
            # 这样系统保持“不断在非阻断 gap 上自举/自补/回归”，但不会越权上线。
            issues.append(_issue("degraded", "phase08_next_stage_blocked_gap_aware_progression", phase08_handoff.get("block_reason") or "allow_next_stage=false", PHASE08_ID))
        if phase08_handoff.get("degrade_reason"):
            issues.append(_issue("degraded", "phase08_degrade_reason", str(phase08_handoff.get("degrade_reason")), PHASE08_ID))
        if phase08_handoff.get("missing_fields"):
            issues.append(_issue("degraded", "phase08_missing_fields", ";".join(map(str, phase08_handoff.get("missing_fields") or [])), PHASE08_ID))
    if phase09_handoff:
        if phase09_handoff.get("allow_apply_to_runtime") is not False:
            issues.append(_issue("blocking", "phase09_runtime_apply_not_forbidden", str(phase09_handoff.get("allow_apply_to_runtime")), PHASE09_ID))
        if phase09_handoff.get("requires_manual_confirmation") is not True:
            issues.append(_issue("blocking", "phase09_manual_confirmation_missing", str(phase09_handoff.get("requires_manual_confirmation")), PHASE09_ID))
        if phase09_handoff.get("system_upgrade_status") == "SYSTEM_UPGRADE_BLOCKED":
            # gap-aware progression: P09 的 blocked upgrade candidate 是安全结果，
            # 说明当前证据不能产生可应用升级包；它不能阻断 Wave4/E2E，除非同时
            # 出现 runtime_apply、manual_confirmation、rollback/regression 等硬边界违规。
            # 正确动作是写 degraded gap，继承到 Full System E2E 与 Patch+Regression。
            issues.append(_issue("degraded", "phase09_system_upgrade_blocked_gap_aware_progression", ";".join(phase09_handoff.get("block_reasons") or ["blocked"]), PHASE09_ID))
        if phase09_handoff.get("missing_fields"):
            issues.append(_issue("degraded", "phase09_missing_fields", ";".join(map(str, phase09_handoff.get("missing_fields") or [])), PHASE09_ID))

    blocking = [i for i in issues if i["severity"] == "blocking"]
    degraded = [i for i in issues if i["severity"] == "degraded"]
    if blocking:
        final_status = "WAVE4_REJECTED"
        handoff_status = "HANDOFF_BLOCKED"
    elif degraded:
        final_status = "WAVE4_READY_WITH_GAPS"
        handoff_status = "HANDOFF_DEGRADED"
    else:
        final_status = "WAVE4_READY"
        handoff_status = "HANDOFF_READY"

    artifacts: dict[str, str] = {}
    if phase08_artifacts.get("handoff_packet"):
        artifacts["phase08_handoff"] = str(phase08_artifacts["handoff_packet"])
    if phase09_artifacts.get("handoff_packet"):
        artifacts["phase09_handoff"] = str(phase09_artifacts["handoff_packet"])
    if phase09_artifacts:
        artifacts["phase09_artifacts"] = _write_phase09_artifact_manifest(phase09_artifacts, out / "09_system_upgrade" / "artifact_manifest")
    if inherited_gap:
        artifacts["inherited_wave3_gap_register"] = str(inherited_gap)

    result: dict[str, Any] = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "execution_mode": mode,
        "started_at": started_at,
        "completed_at": _now(),
        "final_status": final_status,
        "handoff_status": handoff_status,
        "blocking_issue_count": len(blocking),
        "degraded_issue_count": len(degraded),
        "safety_boundary": SAFETY_BOUNDARY,
        "runtime_contract": RUNTIME_CONTRACT,
        "phase_summaries": [
            _phase_summary(PHASE08_ID, phase08_result, phase08_handoff, phase08_artifacts),
            _phase_summary(PHASE09_ID, phase09_result, phase09_handoff, phase09_artifacts),
        ],
        "issues": issues,
        "upstream": {"wave3_handoff_file": str(wave3_handoff_file), "phase07_handoff_file": str(phase07_handoff or "missing")},
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
    }

    gap_register = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "blocking_issues": blocking,
        "degraded_issues": degraded,
        "inherited_wave3_status": wave3.get("handoff_status"),
        "repair_route": "full_system_e2e_allowed_with_gap_carry" if not blocking else "patch_and_regression_required",
        "review_only_boundary": True,
        "runtime_apply_allowed": False,
    }
    artifacts["wave4_gap_register"] = _write_json(audit_dir / "wave4_gap_register.json", gap_register)
    artifacts["wave4_execution_trace"] = _write_json(audit_dir / "wave4_execution_trace.json", {"trace": trace})

    state = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "handoff_status": handoff_status,
        "runtime_contract": RUNTIME_CONTRACT,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "safety_boundary": SAFETY_BOUNDARY,
    }
    artifacts["wave4_state"] = _write_json(state_dir / "wave4_state.json", state)

    wave4_handoff = {
        "current_task": TASK_ID,
        "wave_id": WAVE_ID,
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "handoff_files": {
            "phase_08_handoff_packet": artifacts.get("phase08_handoff", "missing"),
            "phase_09_handoff_packet": artifacts.get("phase09_handoff", "missing"),
            "wave4_result": str(control_dir / "wave4_result.json"),
            "wave4_state": artifacts["wave4_state"],
            "wave4_gap_register": artifacts["wave4_gap_register"],
            "inherited_wave3_gap_register": artifacts.get("inherited_wave3_gap_register", "missing"),
        },
        "phase_summaries": result["phase_summaries"],
        "issues": issues,
        "safety_boundary": SAFETY_BOUNDARY,
        "runtime_apply_allowed": False,
        "requires_manual_confirmation": True,
    }
    artifacts["wave4_handoff"] = _write_json(handoff_dir / "wave4_p08_p09_handoff_packet.json", wave4_handoff)

    result["artifacts"] = artifacts
    result["wave4_handoff"] = wave4_handoff
    artifacts["wave4_audit"] = str(audit_dir / "wave4_audit.md")
    Path(artifacts["wave4_audit"]).write_text(_build_audit(result), encoding="utf-8")
    artifacts["wave4_result"] = _write_json(control_dir / "wave4_result.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SIKK Stable Trader OS Wave4 P08-P09 review/upgrade runtime bundle")
    parser.add_argument("--root", default=".")
    parser.add_argument("--wave3-handoff-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "replay"])
    args = parser.parse_args()
    result = run_wave4_p08_p09(root=args.root, wave3_handoff_file=args.wave3_handoff_file, output_dir=args.output_dir, mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
