from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from modules.stable_trader_os.phase_04_scenario_recognition_controller.runner import (
    Phase04ScenarioRecognitionController,
)
from modules.stable_trader_os.phase_05_structure_position_controller.runner import (
    Phase05StructurePositionController,
)

TASK_ID = "task_2_wave_2_p04_p05_scenario_position_runtime"
WAVE_ID = "wave_2_p04_p05"
NEXT_ALLOWED_TASK = "task_3_wave_3_p06_p07_strategy_execution_risk_runtime"
PHASE04_ID = "phase_04_scenario_recognition_controller"
PHASE05_ID = "phase_05_structure_position_controller"
SAFETY_BOUNDARY = {
    "real_trade": "forbidden",
    "signing": "forbidden",
    "broadcast": "forbidden",
    "secret_read": "forbidden",
}
RUNTIME_CONTRACT = {
    "bootstrap": True,
    "self_check": True,
    "self_fill": True,
    "wave_execution": True,
    "failure_stop": True,
    "audit_backfill": True,
    "regression_repair": True,
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_json(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _resolve_path(value: str | Path | None, base: Path) -> Path | None:
    if not value or str(value) == "missing":
        return None
    p = Path(str(value))
    return p if p.is_absolute() else base / p


def _artifact_exists(value: Any) -> bool:
    return bool(value) and Path(str(value)).exists()


def _issue(severity: str, code: str, detail: str, phase: str = WAVE_ID) -> dict[str, Any]:
    return {"severity": severity, "code": code, "detail": detail, "phase": phase}


def _safe_status(status: Any) -> str:
    return str(status or "missing")


def _normalize_wave1_handoff(wave1_handoff_file: str | Path) -> dict[str, Any]:
    p = Path(wave1_handoff_file)
    handoff = _read_json(p)
    handoff["_path"] = str(p)
    handoff["_base"] = str(p.parent)
    return handoff


def _find_phase03_handoff(wave1: Mapping[str, Any]) -> Path | None:
    base = Path(str(wave1.get("_base") or "."))
    candidates: list[Any] = []
    files = wave1.get("handoff_files", {}) or {}
    for key in ["phase_03_handoff_packet", "phase03_handoff", "phase_03_handoff"]:
        if key in files:
            candidates.append(files[key])
    for value in files.values():
        if "phase_03" in str(value) and "handoff" in str(value):
            candidates.append(value)
    for candidate in candidates:
        p = _resolve_path(candidate, base)
        if p and p.exists():
            return p
    return None


def _patch_phase04_handoff_for_phase05(phase04_handoff_file: Path, phase03_handoff_file: Path) -> None:
    """Preserve canonical Phase04 output and attach upstream optional refs needed by Phase05.

    Phase04 intentionally emits scenario-level handoff files only. Wave2 owns the
    cross-phase runtime closure, so it forwards Phase03 market/kline/chip refs as
    optional context instead of modifying Phase04 controller semantics.
    """
    phase04 = _read_json(phase04_handoff_file)
    phase03 = _read_json(phase03_handoff_file)
    refs = dict(phase04.get("optional_files_for_next_stage", {}) or {})
    for source_key, target_key in [
        ("kline_normalized", "kline_normalized"),
        ("token_market_context", "token_market_context"),
        ("chip_control_summary", "chip_control_summary"),
        ("wallet_structure_decision", "wallet_structure_decision"),
    ]:
        value = (phase03.get("handoff_files", {}) or {}).get(source_key)
        if value and source_key not in refs:
            refs[target_key] = value
    if refs:
        phase04["optional_files_for_next_stage"] = refs
        phase04_handoff_file.write_text(json.dumps(phase04, ensure_ascii=False, indent=2), encoding="utf-8")


def _phase_summary(phase_id: str, result: Mapping[str, Any], handoff: Mapping[str, Any], artifacts: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "phase": phase_id,
        "phase_status": result.get("phase_status"),
        "handoff_status": handoff.get("handoff_status", "missing"),
        "allowed_next_stage": handoff.get("allowed_next_stage", "missing"),
        "block_reason": handoff.get("block_reason", ""),
        "degrade_reason": handoff.get("degrade_reason", ""),
        "artifact_count": len(artifacts),
    }


def _build_audit(result: Mapping[str, Any]) -> str:
    lines = [
        "# Task 2 / Wave 2 / P04-P05 Runtime Audit",
        "",
        f"- task_id: {result.get('task_id')}",
        f"- wave_id: {result.get('wave_id')}",
        f"- final_status: {result.get('final_status')}",
        f"- handoff_status: {result.get('handoff_status')}",
        f"- blocking_issue_count: {result.get('blocking_issue_count')}",
        f"- degraded_issue_count: {result.get('degraded_issue_count')}",
        "",
        "## 安全边界",
        "- 真实交易: 禁止",
        "- 签名: 禁止",
        "- 广播: 禁止",
        "- 密钥读取: 禁止",
        "",
        "## 阶段摘要",
    ]
    for phase in result.get("phase_summaries", []):
        lines.extend(
            [
                f"- {phase.get('phase')}",
                f"  - phase_status: {phase.get('phase_status')}",
                f"  - handoff_status: {phase.get('handoff_status')}",
                f"  - allowed_next_stage: {phase.get('allowed_next_stage')}",
                f"  - degrade_reason: {phase.get('degrade_reason') or 'none'}",
                f"  - block_reason: {phase.get('block_reason') or 'none'}",
            ]
        )
    lines.extend(["", "## Issues"])
    for issue in result.get("issues", []) or [{"severity": "none", "code": "none", "detail": "none"}]:
        lines.append(f"- [{issue.get('severity')}] {issue.get('code')}: {issue.get('detail')}")
    lines.extend(["", "## 下游交接", f"- next_allowed_task: {NEXT_ALLOWED_TASK}"])
    return "\n".join(lines) + "\n"


def run_wave2_p04_p05(*, root: str | Path, wave1_handoff_file: str | Path, output_dir: str | Path, mode: str = "dry-run") -> dict[str, Any]:
    root = Path(root)
    out = Path(output_dir)
    control_dir = out / "wave2_control"
    audit_dir = control_dir / "audit"
    handoff_dir = control_dir / "handoff"
    state_dir = control_dir / "state"
    for d in [out, control_dir, audit_dir, handoff_dir, state_dir]:
        d.mkdir(parents=True, exist_ok=True)

    issues: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    started_at = _now()
    wave1 = _normalize_wave1_handoff(wave1_handoff_file)
    trace.append({"step": "load_wave1_handoff", "status": "PASS", "path": wave1.get("_path")})

    if wave1.get("handoff_status") == "HANDOFF_BLOCKED":
        issues.append(_issue("blocking", "upstream_wave1_blocked", "Wave1 handoff is blocked"))
    elif wave1.get("handoff_status") == "HANDOFF_DEGRADED":
        issues.append(_issue("degraded", "upstream_wave1_degraded", wave1.get("degrade_reason") or "Wave1 degraded but routable"))

    phase03_handoff = _find_phase03_handoff(wave1)
    if not phase03_handoff:
        issues.append(_issue("blocking", "missing_phase03_handoff", "Wave1 did not expose a usable Phase03 handoff"))

    phase04_result: dict[str, Any] = {"phase": PHASE04_ID, "phase_status": "SKIPPED", "artifacts": {}}
    phase05_result: dict[str, Any] = {"phase": PHASE05_ID, "phase_status": "SKIPPED", "artifacts": {}}
    phase04_handoff: dict[str, Any] = {}
    phase05_handoff: dict[str, Any] = {}

    if not any(i["severity"] == "blocking" for i in issues) and phase03_handoff:
        phase04_result = Phase04ScenarioRecognitionController().run(phase03_handoff_file=phase03_handoff, output_dir=out)
        phase04_handoff_path = Path(str(phase04_result["artifacts"].get("handoff_packet")))
        phase04_handoff = _read_json(phase04_handoff_path)
        trace.append({"step": "run_phase04", "status": "PASS", "handoff": str(phase04_handoff_path)})

        _patch_phase04_handoff_for_phase05(phase04_handoff_path, phase03_handoff)
        phase04_handoff = _read_json(phase04_handoff_path)
        trace.append({"step": "patch_phase04_optional_context", "status": "PASS", "source": str(phase03_handoff)})

        phase05_result = Phase05StructurePositionController().run(phase04_handoff_file=phase04_handoff_path, output_dir=out)
        phase05_handoff_path = Path(str(phase05_result["artifacts"].get("handoff_packet")))
        phase05_handoff = _read_json(phase05_handoff_path)
        trace.append({"step": "run_phase05", "status": "PASS", "handoff": str(phase05_handoff_path)})

    phase04_artifacts = phase04_result.get("artifacts", {}) or {}
    phase05_artifacts = phase05_result.get("artifacts", {}) or {}
    for key in ["handoff_packet", "output_validation_report", "handoff_validation_report", "audit_report"]:
        if key in phase04_artifacts and not _artifact_exists(phase04_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase04_artifact:{key}", str(phase04_artifacts[key]), PHASE04_ID))
        if key in phase05_artifacts and not _artifact_exists(phase05_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase05_artifact:{key}", str(phase05_artifacts[key]), PHASE05_ID))

    for phase_id, handoff in [(PHASE04_ID, phase04_handoff), (PHASE05_ID, phase05_handoff)]:
        hs = handoff.get("handoff_status")
        if hs == "HANDOFF_BLOCKED":
            issues.append(_issue("degraded", f"{phase_id}_blocked_positive_path", handoff.get("block_reason") or "blocked/review path", phase_id))
        elif hs not in {"HANDOFF_READY", "HANDOFF_BLOCKED", None}:
            issues.append(_issue("degraded", f"{phase_id}_unexpected_handoff_status", _safe_status(hs), phase_id))
        if handoff.get("degrade_reason"):
            issues.append(_issue("degraded", f"{phase_id}_degrade_reason", str(handoff.get("degrade_reason")), phase_id))

    blocking = [i for i in issues if i["severity"] == "blocking"]
    degraded = [i for i in issues if i["severity"] == "degraded"]
    if blocking:
        final_status = "WAVE2_REJECTED"
        handoff_status = "HANDOFF_BLOCKED"
    elif degraded:
        final_status = "WAVE2_READY_WITH_GAPS"
        handoff_status = "HANDOFF_DEGRADED"
    else:
        final_status = "WAVE2_READY"
        handoff_status = "HANDOFF_READY"

    artifacts: dict[str, str] = {}
    if phase04_artifacts.get("handoff_packet"):
        artifacts["phase04_handoff"] = str(phase04_artifacts["handoff_packet"])
    if phase05_artifacts.get("handoff_packet"):
        artifacts["phase05_handoff"] = str(phase05_artifacts["handoff_packet"])
    inherited_gap = (wave1.get("handoff_files", {}) or {}).get("wave1_gap_register")
    if inherited_gap:
        artifacts["inherited_wave1_gap_register"] = str(inherited_gap)

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
            _phase_summary(PHASE04_ID, phase04_result, phase04_handoff, phase04_artifacts),
            _phase_summary(PHASE05_ID, phase05_result, phase05_handoff, phase05_artifacts),
        ],
        "issues": issues,
        "upstream": {"wave1_handoff_file": str(wave1_handoff_file), "phase03_handoff_file": str(phase03_handoff) if phase03_handoff else "missing"},
        "next_allowed_task": NEXT_ALLOWED_TASK,
    }

    gap_register = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "blocking_issues": blocking,
        "degraded_issues": degraded,
        "inherited_wave1_status": wave1.get("handoff_status"),
        "repair_route": "task_3_allowed_with_gap_carry" if not blocking else "patch_and_regression_required",
    }
    artifacts["wave2_gap_register"] = _write_json(audit_dir / "wave2_gap_register.json", gap_register)
    artifacts["wave2_execution_trace"] = _write_json(audit_dir / "wave2_execution_trace.json", {"trace": trace})

    state = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "handoff_status": handoff_status,
        "runtime_contract": RUNTIME_CONTRACT,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "safety_boundary": SAFETY_BOUNDARY,
    }
    artifacts["wave2_state"] = _write_json(state_dir / "wave2_state.json", state)

    wave2_handoff = {
        "current_task": TASK_ID,
        "wave_id": WAVE_ID,
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "handoff_files": {
            "phase_04_handoff_packet": artifacts.get("phase04_handoff", "missing"),
            "phase_05_handoff_packet": artifacts.get("phase05_handoff", "missing"),
            "wave2_result": str(control_dir / "wave2_result.json"),
            "wave2_state": artifacts["wave2_state"],
            "wave2_gap_register": artifacts["wave2_gap_register"],
            "inherited_wave1_gap_register": artifacts.get("inherited_wave1_gap_register", "missing"),
        },
        "phase_summaries": result["phase_summaries"],
        "issues": issues,
        "safety_boundary": SAFETY_BOUNDARY,
    }
    artifacts["wave2_handoff"] = _write_json(handoff_dir / "wave2_p04_p05_handoff_packet.json", wave2_handoff)

    result["artifacts"] = artifacts
    result["wave2_handoff"] = wave2_handoff
    artifacts["wave2_audit"] = str(audit_dir / "wave2_audit.md")
    Path(artifacts["wave2_audit"]).write_text(_build_audit(result), encoding="utf-8")
    artifacts["wave2_result"] = _write_json(control_dir / "wave2_result.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SIKK Stable Trader OS Wave2 P04-P05 runtime bundle")
    parser.add_argument("--root", default=".")
    parser.add_argument("--wave1-handoff-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "replay"])
    args = parser.parse_args()
    result = run_wave2_p04_p05(root=args.root, wave1_handoff_file=args.wave1_handoff_file, output_dir=args.output_dir, mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
