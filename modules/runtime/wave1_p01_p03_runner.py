from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

from modules.runtime.planbook_repository import PlanbookRepository
from modules.stable_trader_os.phase_01_data_fact import Phase01Runner
from modules.stable_trader_os.phase_02_wallet_structure_controller import Phase02WalletStructureController
from modules.stable_trader_os.phase_03_chip_control_controller import Phase03ChipControlController

TASK_ID = "task_1_wave_1_p01_p03_foundation_runtime"
WAVE_ID = "wave_1_p01_p03"
NEXT_TASK = "task_2_wave_2_p04_p05_scene_position_runtime"
PHASE01_ID = "phase_01_data_fact_controller"
PHASE02_ID = "phase_02_wallet_structure_controller"
PHASE03_ID = "phase_03_chip_control_controller"
SAFETY_BOUNDARY = {
    "real_trade": "forbidden",
    "signing": "forbidden",
    "broadcast": "forbidden",
    "secret_read": "forbidden",
}


def run_wave1_p01_p03(*, root: str | Path, output_dir: str | Path | None = None, mode: str = "dry-run") -> Dict[str, Any]:
    """Execute Task1/Wave1 P01-P03 in a safe dry-run/replay boundary.

    This runner is the Wave1 automation layer created by the full_system_workflow_v4
    task book. It chains existing P01 -> P02 -> P03 runtime controllers, then writes
    Wave-level state, audit, gap register and handoff artifacts. It never trades,
    signs, broadcasts, or reads secrets.
    """
    if mode not in {"dry-run", "replay"}:
        raise ValueError("Wave1 runner only allows dry-run/replay mode")

    root_path = Path(root)
    out = Path(output_dir) if output_dir else root_path / "runtime_logs" / "full_system_runtime" / "wave1_p01_p03"
    out.mkdir(parents=True, exist_ok=True)
    input_file = root_path / "examples" / "stable_trader_os" / "phase_01_data_fact" / "mock_phase_01_input.json"
    if not input_file.exists():
        raise FileNotFoundError(f"missing Wave1 fixture: {input_file}")

    phase_results: Dict[str, Any] = {}
    blocking_issues: list[dict[str, Any]] = []
    degraded_issues: list[dict[str, Any]] = []
    execution_events: list[dict[str, Any]] = []

    def event(name: str, **payload: Any) -> None:
        execution_events.append({"ts": _now(), "event": name, **payload})

    event("wave1_started", task_id=TASK_ID, mode=mode, safety_boundary=SAFETY_BOUNDARY)

    planbook_repository = PlanbookRepository(root_path).validate()
    event(
        "planbook_repository_validated",
        final_status=planbook_repository.get("final_status"),
        gap_count=len(planbook_repository.get("gap_register", [])),
    )
    if planbook_repository.get("final_status") == "PLANBOOK_REPOSITORY_REJECTED":
        blocking_issues.append({"phase": "planbook_repository", "issue": "planbook_repository_rejected", "audit_path": planbook_repository.get("audit_path")})
    elif planbook_repository.get("final_status") == "PLANBOOK_REPOSITORY_READY_WITH_GAPS":
        degraded_issues.append({"phase": "planbook_repository", "issue": "planbook_repository_ready_with_gaps", "audit_path": planbook_repository.get("audit_path")})

    p01 = Phase01Runner(root_path).run(input_file, out)
    phase_results[PHASE01_ID] = p01
    event("phase01_completed", status=p01.get("status"), phase_state=p01.get("phase_state"))
    if p01.get("status") == "BLOCK":
        blocking_issues.append({"phase": PHASE01_ID, "issue": "phase01_blocked", "status": p01.get("status")})

    p02 = Phase02WalletStructureController().run(
        phase01_handoff_file=p01["canonical_handoff_packet"],
        output_dir=out,
    )
    phase_results[PHASE02_ID] = p02
    event("phase02_completed", phase_status=p02.get("phase_status"))
    if p02.get("phase_status") == "WALLET_BLOCK":
        blocking_issues.append({"phase": PHASE02_ID, "issue": "phase02_blocked", "status": p02.get("phase_status")})
    if p02.get("phase_status") in {"WALLET_PAUSE", "WALLET_UNKNOWN", "WALLET_DATA_WEAK", "WALLET_COUNTERPARTY_PRESSURE"}:
        degraded_issues.append({"phase": PHASE02_ID, "issue": "phase02_degraded", "status": p02.get("phase_status")})

    p03 = Phase03ChipControlController().run(
        phase02_handoff_file=p02["artifacts"]["handoff_packet"],
        output_dir=out,
    )
    phase_results[PHASE03_ID] = p03
    p03_status = _phase03_status(p03)
    event("phase03_completed", chip_control_status=p03_status, handoff_status=p03.get("handoff_status"))
    if p03_status == "STRUCTURE_COLLAPSE" or p03.get("handoff_status") == "HANDOFF_BLOCKED":
        blocking_issues.append({"phase": PHASE03_ID, "issue": "phase03_blocked", "status": p03_status})
    if p03_status in {"CONTROL_WEAKENING", "PARTIAL_DISTRIBUTION", "ACTIVE_DISTRIBUTION", "TRANSFER_TO_COUNTERPARTY", "UNKNOWN_CONTROL"}:
        degraded_issues.append({"phase": PHASE03_ID, "issue": "phase03_degraded", "status": p03_status})

    artifacts = {
        "planbook_repository_index": planbook_repository["index_path"],
        "planbook_repository_audit": planbook_repository["audit_path"],
        "phase01_handoff": p01["canonical_handoff_packet"],
        "phase02_handoff": p02["artifacts"]["handoff_packet"],
        "phase03_handoff": p03["artifacts"]["handoff_packet"],
    }
    contract_verdict = _verify_required_artifacts(artifacts)
    if contract_verdict["missing"]:
        blocking_issues.append({"phase": WAVE_ID, "issue": "missing_required_artifacts", "missing": contract_verdict["missing"]})

    final_status = _final_status(blocking_issues, degraded_issues)
    handoff_status = "HANDOFF_BLOCKED" if blocking_issues else ("HANDOFF_DEGRADED" if degraded_issues else "HANDOFF_READY")
    wave_dir = out / "wave1_control"
    audit_dir = wave_dir / "audit"
    handoff_dir = wave_dir / "handoff"
    state_dir = wave_dir / "state"
    for d in (audit_dir, handoff_dir, state_dir):
        d.mkdir(parents=True, exist_ok=True)

    gap_register = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "generated_at": _now(),
        "blocking_issues": blocking_issues,
        "degraded_issues": degraded_issues,
        "gap_count": len(blocking_issues) + len(degraded_issues),
        "safety_boundary": SAFETY_BOUNDARY,
    }
    gap_path = audit_dir / "wave1_gap_register.json"
    _write_json(gap_path, gap_register)

    handoff_packet = {
        "current_task": TASK_ID,
        "wave_id": WAVE_ID,
        "handoff_status": handoff_status,
        "final_status": final_status,
        "next_allowed_task": NEXT_TASK if not blocking_issues else TASK_ID,
        "handoff_files": {
            "planbook_repository_index": artifacts["planbook_repository_index"],
            "planbook_repository_audit": artifacts["planbook_repository_audit"],
            "phase_01_handoff_packet": artifacts["phase01_handoff"],
            "phase_02_handoff_packet": artifacts["phase02_handoff"],
            "phase_03_handoff_packet": artifacts["phase03_handoff"],
            "gap_register": str(gap_path),
        },
        "phase_statuses": {
            PHASE01_ID: p01.get("phase_state"),
            PHASE02_ID: p02.get("phase_status"),
            PHASE03_ID: p03_status,
        },
        "safety_boundary": SAFETY_BOUNDARY,
        "generated_at": _now(),
    }
    wave_handoff_path = handoff_dir / "wave1_p01_p03_handoff_packet.json"
    _write_json(wave_handoff_path, handoff_packet)

    state = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": handoff_packet["next_allowed_task"],
        "runtime_contract": {
            "self_bootstrap": True,
            "self_check": True,
            "self_repair": bool(degraded_issues) and not blocking_issues,
            "wave_execution": True,
            "failure_stop": True,
            "audit_backfill": True,
            "regression_repair": True,
            "planbook_repository_read": True,
        },
        "blocking_issue_count": len(blocking_issues),
        "degraded_issue_count": len(degraded_issues),
        "updated_at": _now(),
    }
    state_path = state_dir / "wave1_state.json"
    _write_json(state_path, state)

    trace_path = audit_dir / "wave1_execution_trace.jsonl"
    trace_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in execution_events) + "\n", encoding="utf-8")

    audit_path = audit_dir / "wave1_audit.md"
    audit_path.write_text(_audit_report(final_status, handoff_status, phase_results, artifacts, gap_register), encoding="utf-8")

    result: Dict[str, Any] = {
        "task_id": TASK_ID,
        "wave_id": WAVE_ID,
        "execution_mode": mode,
        "final_status": final_status,
        "handoff_status": handoff_status,
        "next_allowed_task": handoff_packet["next_allowed_task"],
        "blocking_issue_count": len(blocking_issues),
        "degraded_issue_count": len(degraded_issues),
        "phase_results": phase_results,
        "planbook_repository": {
            "final_status": planbook_repository.get("final_status"),
            "index_path": planbook_repository.get("index_path"),
            "audit_path": planbook_repository.get("audit_path"),
            "gap_count": len(planbook_repository.get("gap_register", [])),
        },
        "safety_boundary": SAFETY_BOUNDARY,
        "artifacts": {
            **artifacts,
            "wave1_result": str(wave_dir / "wave1_result.json"),
            "wave1_audit": str(audit_path),
            "wave1_state": str(state_path),
            "wave1_handoff": str(wave_handoff_path),
            "wave1_gap_register": str(gap_path),
            "wave1_execution_trace": str(trace_path),
        },
    }
    _write_json(wave_dir / "wave1_result.json", result)
    return result


def _verify_required_artifacts(artifacts: Mapping[str, str]) -> Dict[str, Any]:
    missing = [k for k, v in artifacts.items() if not v or not Path(v).exists()]
    return {"status": "PASS" if not missing else "FAIL", "missing": missing}


def _phase03_status(result: Mapping[str, Any]) -> str:
    status = result.get("phase_status") or result.get("chip_control_status")
    if status:
        return str(status)
    artifacts = result.get("artifacts") if isinstance(result.get("artifacts"), Mapping) else {}
    summary_path = artifacts.get("chip_control_summary") if isinstance(artifacts, Mapping) else None
    if summary_path and Path(summary_path).exists():
        try:
            summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
            status = summary.get("chip_control_status") or summary.get("phase_status")
            if status:
                return str(status)
        except (OSError, json.JSONDecodeError):
            return "UNKNOWN_CONTROL"
    return "UNKNOWN_CONTROL"


def _final_status(blocking: Iterable[Mapping[str, Any]], degraded: Iterable[Mapping[str, Any]]) -> str:
    blocking_list = list(blocking)
    degraded_list = list(degraded)
    if blocking_list:
        return "WAVE1_REJECTED"
    if degraded_list:
        return "WAVE1_READY_WITH_GAPS"
    return "WAVE1_READY"


def _audit_report(final_status: str, handoff_status: str, phases: Mapping[str, Any], artifacts: Mapping[str, str], gaps: Mapping[str, Any]) -> str:
    lines = [
        "# Task 1 / Wave 1 / P01-P03 自动化审计报告",
        "",
        f"- task_id: {TASK_ID}",
        f"- wave_id: {WAVE_ID}",
        f"- final_status: {final_status}",
        f"- handoff_status: {handoff_status}",
        "- 真实交易: 禁止",
        "- 签名: 禁止",
        "- 广播: 禁止",
        "- 密钥读取: 禁止",
        "",
        "## Phase 状态",
    ]
    lines += [f"- {PHASE01_ID}: {phases.get(PHASE01_ID, {}).get('phase_state')} / {phases.get(PHASE01_ID, {}).get('status')}"]
    lines += [f"- {PHASE02_ID}: {phases.get(PHASE02_ID, {}).get('phase_status')}"]
    lines += [f"- {PHASE03_ID}: {_phase03_status(phases.get(PHASE03_ID, {}))} / {phases.get(PHASE03_ID, {}).get('handoff_status')}"]
    lines += ["", "## Planbook Repository"]
    lines += [f"- planbook_repository_index: {artifacts.get('planbook_repository_index')}"]
    lines += [f"- planbook_repository_audit: {artifacts.get('planbook_repository_audit')}"]
    lines += ["", "## 输出产物"]
    lines += [f"- {k}: {v}" for k, v in artifacts.items()]
    lines += ["", "## Gap Register"]
    lines += [f"- blocking_issue_count: {len(gaps.get('blocking_issues', []))}", f"- degraded_issue_count: {len(gaps.get('degraded_issues', []))}"]
    if gaps.get("blocking_issues"):
        lines += [f"- blocking: {x}" for x in gaps.get("blocking_issues", [])]
    if gaps.get("degraded_issues"):
        lines += [f"- degraded: {x}" for x in gaps.get("degraded_issues", [])]
    if not gaps.get("blocking_issues") and not gaps.get("degraded_issues"):
        lines += ["- none"]
    lines += ["", "## 下阶段路由", f"- next_allowed_task: {NEXT_TASK if final_status != 'WAVE1_REJECTED' else TASK_ID}"]
    return "\n".join(lines) + "\n"


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run SIKK full_system_workflow_v4 Task1 Wave1 P01-P03 automation")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "replay"])
    args = parser.parse_args(argv)
    result = run_wave1_p01_p03(root=args.root, output_dir=args.output_dir, mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
