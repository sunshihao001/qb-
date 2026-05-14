from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from modules.stable_trader_os.phase_06_strategy_gate_controller.runner import (
    Phase06StrategyGateController,
)
from modules.stable_trader_os.phase_07_execution_risk_controller.runner import (
    Phase07ExecutionRiskController,
)

TASK_ID = "task_3_wave_3_p06_p07_strategy_execution_risk_runtime"
WAVE_ID = "wave_3_p06_p07"
NEXT_ALLOWED_TASK = "task_4_wave_4_p08_p09_review_learning_runtime"
PHASE06_ID = "phase_06_strategy_gate_controller"
PHASE07_ID = "phase_07_execution_risk_controller"
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


def _resolve_path(value: str | Path | None, base: Path) -> Path | None:
    if not value or str(value) == "missing":
        return None
    p = Path(str(value))
    return p if p.is_absolute() else base / p


def _artifact_exists(value: Any) -> bool:
    return bool(value) and Path(str(value)).exists()


def _issue(severity: str, code: str, detail: str, phase: str = WAVE_ID) -> dict[str, Any]:
    return {"severity": severity, "code": code, "detail": detail, "phase": phase}


def _normalize_wave2_handoff(wave2_handoff_file: str | Path) -> dict[str, Any]:
    p = Path(wave2_handoff_file)
    handoff = _read_json(p)
    handoff["_path"] = str(p)
    handoff["_base"] = str(p.parent)
    return handoff


def _find_phase05_handoff(wave2: Mapping[str, Any]) -> Path | None:
    base = Path(str(wave2.get("_base") or "."))
    files = wave2.get("handoff_files", {}) or {}
    candidates: list[Any] = []
    for key in ["phase_05_handoff_packet", "phase05_handoff", "phase_05_handoff"]:
        if key in files:
            candidates.append(files[key])
    for value in files.values():
        if "phase_05" in str(value) and "handoff" in str(value):
            candidates.append(value)
    for candidate in candidates:
        p = _resolve_path(candidate, base)
        if p and p.exists():
            return p
    return None


def _patch_phase05_handoff_for_phase06(phase05_handoff_file: Path, wave2: Mapping[str, Any]) -> None:
    """Attach upstream Wave2 refs for Phase06 without changing Phase05 semantics."""
    phase05 = _read_json(phase05_handoff_file)
    phase05_base = phase05_handoff_file.parent
    phase05_files = dict(phase05.get("handoff_files", {}) or {})
    wave2_files = wave2.get("handoff_files", {}) or {}

    raw_refs = dict(phase05.get("optional_files_for_next_stage", {}) or {})
    refs: dict[str, Any] = {}
    for k, v in raw_refs.items():
        if v and v != "missing" and Path(str(v)).suffix.lower() in {".json", ".csv", ".jsonl"}:
            refs[k] = v
    # Only forward machine-readable JSON/CSV/JSONL artifacts into Phase06.
    # Phase06 attempts to parse every ref; markdown reports stay excluded and
    # remain available through phase-local audit artifacts instead.
    for k, v in phase05_files.items():
        if v and v != "missing" and Path(str(v)).suffix.lower() in {".json", ".csv", ".jsonl"}:
            refs[k] = v

    phase04_path = _resolve_path(wave2_files.get("phase_04_handoff_packet"), Path(str(wave2.get("_base") or ".")))
    phase04 = _read_json(phase04_path) if phase04_path else {}
    for key, value in (phase04.get("handoff_files", {}) or {}).items():
        if value and value != "missing" and Path(str(value)).suffix.lower() in {".json", ".csv", ".jsonl"}:
            refs.setdefault(key, value)
    for key, value in (phase04.get("optional_files_for_next_stage", {}) or {}).items():
        if value and value != "missing" and Path(str(value)).suffix.lower() in {".json", ".csv", ".jsonl"}:
            refs.setdefault(key, value)

    # Phase06 expects all upstream phase handoffs. Wave2 may only expose P04/P05;
    # P04 optional refs carry P01-P03 documents when available, otherwise they
    # stay missing and are handled as gaps instead of guessed facts.
    refs.setdefault("phase_04_handoff_packet", str(phase04_path) if phase04_path else "missing")
    refs.setdefault("phase_05_handoff_packet", str(phase05_handoff_file))
    for key, phase_path in [
        ("phase_01_handoff_packet", refs.get("phase01_handoff_packet") or refs.get("phase_01_handoff")),
        ("phase_02_handoff_packet", refs.get("phase02_handoff_packet") or refs.get("phase_02_handoff")),
        ("phase_03_handoff_packet", refs.get("phase03_handoff_packet") or refs.get("phase_03_handoff")),
    ]:
        if phase_path:
            refs.setdefault(key, phase_path)

    # Forward quote/market paths when P05 omitted them from handoff_files.
    for key in ["quote_security_normalized", "token_market_context", "kline_normalized", "chip_control_summary", "wallet_structure_decision"]:
        if key in phase05_files:
            refs.setdefault(key, phase05_files[key])

    phase05["optional_files_for_next_stage"] = refs
    # Phase06 treats every handoff_files entry as machine-readable input.
    # Keep markdown reports out of the active handoff contract for Wave3.
    phase05["handoff_files"] = {
        k: v for k, v in phase05_files.items()
        if v and v != "missing" and Path(str(v)).suffix.lower() in {".json", ".csv", ".jsonl"}
    }
    phase05_handoff_file.write_text(json.dumps(phase05, ensure_ascii=False, indent=2), encoding="utf-8")


def _patch_phase06_handoff_for_phase07(phase06_handoff_file: Path) -> None:
    """Ensure Phase07 receives paper state defaults and inherited optional refs."""
    handoff = _read_json(phase06_handoff_file)
    required = dict(handoff.get("required_files_for_next_stage", {}) or {})
    base = phase06_handoff_file.parents[1] if len(phase06_handoff_file.parents) > 1 else phase06_handoff_file.parent
    state_dir = base / "07_execution_risk_seed_state"
    state_dir.mkdir(parents=True, exist_ok=True)
    defaults = {
        "paper_positions_open": state_dir / "paper_positions_open.json",
        "paper_positions_closed": state_dir / "paper_positions_closed.json",
        "risk_events": state_dir / "risk_events.jsonl",
    }
    for key, path in defaults.items():
        if key not in required or not required.get(key):
            if path.suffix == ".jsonl":
                path.write_text("", encoding="utf-8")
            else:
                path.write_text("[]", encoding="utf-8")
            required[key] = str(path)
    handoff["required_files_for_next_stage"] = required
    phase06_handoff_file.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")


def _phase_summary(phase_id: str, result: Mapping[str, Any], handoff: Mapping[str, Any], artifacts: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "phase": phase_id,
        "phase_status": result.get("phase_status"),
        "handoff_status": handoff.get("handoff_status", "missing"),
        "allow_next_stage": handoff.get("allow_next_stage", handoff.get("allowed_next_stage", "missing")),
        "block_reason": handoff.get("block_reason", ""),
        "degrade_reason": handoff.get("degrade_reason", ""),
        "hard_negative_triggered": handoff.get("hard_negative_triggered", False),
        "artifact_count": len(artifacts),
    }


def _build_audit(result: Mapping[str, Any]) -> str:
    lines = [
        "# Task 3 / Wave 3 / P06-P07 Runtime Audit",
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
        lines.extend([
            f"- {phase.get('phase')}",
            f"  - phase_status: {phase.get('phase_status')}",
            f"  - handoff_status: {phase.get('handoff_status')}",
            f"  - allow_next_stage: {phase.get('allow_next_stage')}",
            f"  - hard_negative_triggered: {phase.get('hard_negative_triggered')}",
            f"  - degrade_reason: {phase.get('degrade_reason') or 'none'}",
            f"  - block_reason: {phase.get('block_reason') or 'none'}",
        ])
    lines.extend(["", "## Issues"])
    for issue in result.get("issues", []) or [{"severity": "none", "code": "none", "detail": "none"}]:
        lines.append(f"- [{issue.get('severity')}] {issue.get('code')}: {issue.get('detail')}")
    lines.extend(["", "## 下游交接", f"- next_allowed_task: {NEXT_ALLOWED_TASK}"])
    return "\n".join(lines) + "\n"


def run_wave3_p06_p07(*, root: str | Path, wave2_handoff_file: str | Path, output_dir: str | Path, mode: str = "dry-run") -> dict[str, Any]:
    root = Path(root)
    out = Path(output_dir)
    control_dir = out / "wave3_control"
    audit_dir = control_dir / "audit"
    handoff_dir = control_dir / "handoff"
    state_dir = control_dir / "state"
    for d in [out, control_dir, audit_dir, handoff_dir, state_dir]:
        d.mkdir(parents=True, exist_ok=True)

    issues: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    started_at = _now()
    wave2 = _normalize_wave2_handoff(wave2_handoff_file)
    trace.append({"step": "load_wave2_handoff", "status": "PASS", "path": wave2.get("_path")})

    if wave2.get("handoff_status") == "HANDOFF_BLOCKED":
        issues.append(_issue("blocking", "upstream_wave2_blocked", "Wave2 handoff is blocked"))
    elif wave2.get("handoff_status") == "HANDOFF_DEGRADED":
        issues.append(_issue("degraded", "upstream_wave2_degraded", wave2.get("degrade_reason") or "Wave2 degraded but routable"))

    phase05_handoff = _find_phase05_handoff(wave2)
    if not phase05_handoff:
        issues.append(_issue("blocking", "missing_phase05_handoff", "Wave2 did not expose a usable Phase05 handoff"))

    phase06_result: dict[str, Any] = {"phase": PHASE06_ID, "phase_status": "SKIPPED", "artifacts": {}}
    phase07_result: dict[str, Any] = {"phase": PHASE07_ID, "phase_status": "SKIPPED", "artifacts": {}}
    phase06_handoff: dict[str, Any] = {}
    phase07_handoff: dict[str, Any] = {}

    if not any(i["severity"] == "blocking" for i in issues) and phase05_handoff:
        _patch_phase05_handoff_for_phase06(phase05_handoff, wave2)
        trace.append({"step": "patch_phase05_optional_context", "status": "PASS", "source": str(wave2_handoff_file)})

        phase06_result = Phase06StrategyGateController().run(phase05_handoff_file=phase05_handoff, output_dir=out)
        phase06_handoff_path = Path(str(phase06_result["artifacts"].get("handoff_packet")))
        phase06_handoff = _read_json(phase06_handoff_path)
        trace.append({"step": "run_phase06", "status": "PASS", "handoff": str(phase06_handoff_path)})

        _patch_phase06_handoff_for_phase07(phase06_handoff_path)
        phase06_handoff = _read_json(phase06_handoff_path)
        trace.append({"step": "patch_phase06_paper_state_defaults", "status": "PASS", "handoff": str(phase06_handoff_path)})

        phase07_result = Phase07ExecutionRiskController().run(phase06_handoff_file=phase06_handoff_path, output_dir=out / "07_execution_risk")
        phase07_handoff_path = Path(str(phase07_result["artifacts"].get("handoff_packet")))
        phase07_handoff = _read_json(phase07_handoff_path)
        trace.append({"step": "run_phase07", "status": "PASS", "handoff": str(phase07_handoff_path)})

    phase06_artifacts = phase06_result.get("artifacts", {}) or {}
    phase07_artifacts = phase07_result.get("artifacts", {}) or {}
    for key in ["handoff_packet", "output_validation_report", "handoff_validation_report", "audit_report"]:
        if key in phase06_artifacts and not _artifact_exists(phase06_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase06_artifact:{key}", str(phase06_artifacts[key]), PHASE06_ID))
        if key in phase07_artifacts and not _artifact_exists(phase07_artifacts[key]):
            issues.append(_issue("blocking", f"missing_phase07_artifact:{key}", str(phase07_artifacts[key]), PHASE07_ID))

    for phase_id, handoff in [(PHASE06_ID, phase06_handoff), (PHASE07_ID, phase07_handoff)]:
        if not handoff:
            continue
        hs = handoff.get("handoff_status")
        if hs == "HANDOFF_BLOCKED":
            issues.append(_issue("degraded", f"{phase_id}_blocked_positive_path", handoff.get("block_reason") or "blocked/review path", phase_id))
        elif hs not in {"HANDOFF_READY", "HANDOFF_DEGRADED", "HANDOFF_BLOCKED", None}:
            issues.append(_issue("degraded", f"{phase_id}_unexpected_handoff_status", str(hs), phase_id))
        if handoff.get("degrade_reason"):
            issues.append(_issue("degraded", f"{phase_id}_degrade_reason", str(handoff.get("degrade_reason")), phase_id))
        if handoff.get("hard_negative_triggered"):
            issues.append(_issue("degraded", f"{phase_id}_hard_negative", ";".join(handoff.get("hard_negative_reasons", []) or ["hard_negative_triggered"]), phase_id))

    blocking = [i for i in issues if i["severity"] == "blocking"]
    degraded = [i for i in issues if i["severity"] == "degraded"]
    if blocking:
        final_status = "WAVE3_REJECTED"
        handoff_status = "HANDOFF_BLOCKED"
    elif degraded:
        final_status = "WAVE3_READY_WITH_GAPS"
        handoff_status = "HANDOFF_DEGRADED"
    else:
        final_status = "WAVE3_READY"
        handoff_status = "HANDOFF_READY"

    artifacts: dict[str, str] = {}
    if phase06_artifacts.get("handoff_packet"):
        artifacts["phase06_handoff"] = str(phase06_artifacts["handoff_packet"])
    if phase07_artifacts.get("handoff_packet"):
        artifacts["phase07_handoff"] = str(phase07_artifacts["handoff_packet"])
    inherited_gap = (wave2.get("handoff_files", {}) or {}).get("wave2_gap_register")
    if inherited_gap:
        artifacts["inherited_wave2_gap_register"] = str(inherited_gap)

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
            _phase_summary(PHASE06_ID, phase06_result, phase06_handoff, phase06_artifacts),
            _phase_summary(PHASE07_ID, phase07_result, phase07_handoff, phase07_artifacts),
        ],
        "issues": issues,
        "upstream": {"wave2_handoff_file": str(wave2_handoff_file), "phase05_handoff_file": str(phase05_handoff) if phase05_handoff else "missing"},
        "next_allowed_task": NEXT_ALLOWED_TASK,
    }

    gap_register = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "blocking_issues": blocking,
        "degraded_issues": degraded,
        "inherited_wave2_status": wave2.get("handoff_status"),
        "repair_route": "task_4_allowed_with_gap_carry" if not blocking else "patch_and_regression_required",
    }
    artifacts["wave3_gap_register"] = _write_json(audit_dir / "wave3_gap_register.json", gap_register)
    artifacts["wave3_execution_trace"] = _write_json(audit_dir / "wave3_execution_trace.json", {"trace": trace})

    state = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "handoff_status": handoff_status,
        "runtime_contract": RUNTIME_CONTRACT,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "safety_boundary": SAFETY_BOUNDARY,
    }
    artifacts["wave3_state"] = _write_json(state_dir / "wave3_state.json", state)

    wave3_handoff = {
        "current_task": TASK_ID,
        "wave_id": WAVE_ID,
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": NEXT_ALLOWED_TASK if not blocking else "patch_and_regression",
        "handoff_files": {
            "phase_06_handoff_packet": artifacts.get("phase06_handoff", "missing"),
            "phase_07_handoff_packet": artifacts.get("phase07_handoff", "missing"),
            "wave3_result": str(control_dir / "wave3_result.json"),
            "wave3_state": artifacts["wave3_state"],
            "wave3_gap_register": artifacts["wave3_gap_register"],
            "inherited_wave2_gap_register": artifacts.get("inherited_wave2_gap_register", "missing"),
        },
        "phase_summaries": result["phase_summaries"],
        "issues": issues,
        "safety_boundary": SAFETY_BOUNDARY,
    }
    artifacts["wave3_handoff"] = _write_json(handoff_dir / "wave3_p06_p07_handoff_packet.json", wave3_handoff)

    result["artifacts"] = artifacts
    result["wave3_handoff"] = wave3_handoff
    artifacts["wave3_audit"] = str(audit_dir / "wave3_audit.md")
    Path(artifacts["wave3_audit"]).write_text(_build_audit(result), encoding="utf-8")
    artifacts["wave3_result"] = _write_json(control_dir / "wave3_result.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SIKK Stable Trader OS Wave3 P06-P07 runtime bundle")
    parser.add_argument("--root", default=".")
    parser.add_argument("--wave2-handoff-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "replay"])
    args = parser.parse_args()
    result = run_wave3_p06_p07(root=args.root, wave2_handoff_file=args.wave2_handoff_file, output_dir=args.output_dir, mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
