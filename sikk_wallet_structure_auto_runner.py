#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Long-running Wallet-Intel auto task runner.

Runs the existing canonical SIKK-GMGN pipeline repeatedly with checkpointing,
system audit, guard status aggregation, and paper-only safety boundaries.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from run_sikk_gmgn_pipeline import run_full_pipeline
from modules.source_wallet_bot.schema_validator import validate_source_wallet_design_package
from sikk_wallet_structure_system_audit import audit_wallet_structure_system


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_stamp(value: str) -> str:
    return value.replace("-", "").replace(":", "").replace("T", "_").replace("Z", "")


def _read_json(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _wallet_structure_status(pipeline_manifest: dict[str, Any]) -> str:
    stats = pipeline_manifest.get("阶段统计", {}).get("钱包结构门禁", {})
    guard = stats.get("wallet_data_guard") if isinstance(stats, dict) else None
    if isinstance(guard, dict) and guard.get("status"):
        return str(guard.get("status"))
    if isinstance(stats, dict) and stats.get("状态") == "skipped":
        return "SKIPPED"
    if isinstance(stats, dict) and (stats.get("成功数量", 0) or stats.get("处理数量", 0)):
        return "PASS"
    return "UNKNOWN"


def _run_acceptance(project_root: Path) -> dict[str, Any]:
    try:
        result = validate_source_wallet_design_package(project_root)
    except Exception as exc:  # pragma: no cover - defensive runtime reporting
        return {"status": "FAIL", "error": str(exc)}
    return {
        "status": "PASS" if result.get("ok") else "FAIL",
        "details": result,
    }


def _load_existing_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        return {}
    return _read_json(manifest_path)


def _build_guard_trend_index(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    records = []
    for cycle in cycles:
        status = str(cycle.get("wallet_structure_status") or "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1
        records.append({
            "cycle": cycle.get("cycle"),
            "started_at": cycle.get("started_at"),
            "status": status,
            "pipeline_manifest": cycle.get("pipeline_manifest"),
        })
    return {
        "artifact_type": "wallet_data_guard_trend_index",
        "generated_at": _utc_now(),
        "cycles_total": len(cycles),
        "status_counts": status_counts,
        "records": records,
    }


def run_wallet_structure_auto_task(
    *,
    output_root: str | Path = "data/source_wallet_bot/auto_tasks/wallet_structure_longrun",
    cycles: int = 3,
    interval_seconds: float = 60.0,
    pipeline_runner: Callable[..., dict[str, str]] = run_full_pipeline,
    now_sequence: Sequence[str] | None = None,
    limit: int | None = None,
    include_s2: bool = False,
    run_quote_security: bool = False,
    wallet_structure_mode: str = "observe",
    resume: bool = False,
) -> dict[str, Any]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = root / "checkpoint" / "wallet_structure_auto_task_checkpoint.json"
    manifest_path = root / "manifest" / "wallet_structure_auto_task_manifest.json"
    guard_trend_index_path = root / "guard_index" / "wallet_data_guard_trend_index.json"
    previous_manifest = _load_existing_manifest(manifest_path) if resume else {}
    cycle_records: list[dict[str, Any]] = list(previous_manifest.get("cycles", [])) if resume else []
    completed_cycles = len(cycle_records)
    started_at = (previous_manifest.get("generated_at") if resume and previous_manifest else (now_sequence[0] if now_sequence else _utc_now()))

    safety_boundary = {
        "paper_only": True,
        "read_only_collectors": True,
        "real_swap_enabled": False,
        "private_key_required": False,
        "secret_file_reading_enabled": False,
        "signing_enabled": False,
        "broadcast_enabled": False,
    }

    for idx in range(completed_cycles, cycles):
        cycle_no = idx + 1
        sequence_idx = idx - completed_cycles
        now = now_sequence[sequence_idx] if now_sequence and sequence_idx < len(now_sequence) else _utc_now()
        cycle_dir = root / "cycles" / f"cycle_{cycle_no:04d}_{_safe_stamp(now)}"
        pipeline_result = pipeline_runner(
            output_root=cycle_dir,
            limit=limit,
            include_s2=include_s2,
            run_wallet_structure=True,
            wallet_structure_mode=wallet_structure_mode,
            run_quote_security=run_quote_security,
        )
        pipeline_manifest = _read_json(pipeline_result.get("manifest_json", ""))
        acceptance = _run_acceptance(Path(__file__).resolve().parent)
        cycle_record = {
            "cycle": cycle_no,
            "started_at": now,
            "cycle_dir": str(cycle_dir),
            "pipeline_manifest": pipeline_result.get("manifest_json", ""),
            "pipeline_report": pipeline_result.get("report_md", ""),
            "wallet_structure_status": _wallet_structure_status(pipeline_manifest),
            "state_machine_stats": pipeline_manifest.get("阶段统计", {}).get("状态机", {}),
            "wallet_structure_stats": pipeline_manifest.get("阶段统计", {}).get("钱包结构门禁", {}),
            "acceptance_status": acceptance.get("status"),
            "acceptance": acceptance,
        }
        cycle_records.append(cycle_record)
        checkpoint = {
            "artifact_type": "wallet_structure_auto_task_checkpoint",
            "status": "RUNNING" if cycle_no < cycles else "COMPLETED",
            "started_at": started_at,
            "updated_at": now,
            "last_completed_cycle": cycle_no,
            "cycles_requested": cycles,
            "cycles_remaining": max(cycles - cycle_no, 0),
            "last_cycle": cycle_record,
            "safety_boundary": safety_boundary,
        }
        _write_json(checkpoint_path, checkpoint)
        if interval_seconds and cycle_no < cycles:
            time.sleep(interval_seconds)

    guard_trend_index = _build_guard_trend_index(cycle_records)
    _write_json(guard_trend_index_path, guard_trend_index)
    audit = audit_wallet_structure_system(project_root=Path(__file__).resolve().parent, output_dir=root / "system_audit")
    manifest = {
        "artifact_type": "wallet_structure_auto_task_manifest",
        "status": "COMPLETED",
        "generated_at": _utc_now(),
        "long_running_task": {
            "cycles_requested": cycles,
            "cycles_completed": len(cycle_records),
            "interval_seconds": interval_seconds,
            "checkpoint_path": str(checkpoint_path),
            "resume": resume,
        },
        "canonical_route": [
            "modules/source_wallet_bot",
            "modules/wallet_data_guard",
            "sikk_candidate_wallet_structure_pipeline.py",
            "sikk_wallet_structure_gate.py",
            "sikk_candidate_state_machine.py / sikk_live_run.py",
        ],
        "cycles": cycle_records,
        "guard_trend_index_path": str(guard_trend_index_path),
        "system_audit": {
            "overall_status": audit.get("overall_status"),
            "json_path": audit.get("json_path"),
            "md_path": audit.get("md_path"),
            "gap_count": len(audit.get("gaps", [])),
        },
        "safety_boundary": safety_boundary,
    }
    _write_json(manifest_path, manifest)
    return {
        "status": "COMPLETED",
        "cycles_completed": len(cycle_records),
        "checkpoint_path": str(checkpoint_path),
        "manifest_path": str(manifest_path),
        "audit_report_path": str(audit.get("md_path", "")),
        "guard_trend_index_path": str(guard_trend_index_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run long-running SIKK Wallet-Intel auto task")
    parser.add_argument("--output-root", default="data/source_wallet_bot/auto_tasks/wallet_structure_longrun")
    parser.add_argument("--cycles", type=int, default=3)
    parser.add_argument("--interval-seconds", type=float, default=60.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-s2", action="store_true")
    parser.add_argument("--run-quote-security", action="store_true")
    parser.add_argument("--wallet-structure-mode", choices=["off", "observe", "soft", "hard"], default="observe")
    parser.add_argument("--resume", action="store_true", help="从已有 checkpoint/manifest 继续未完成 cycle")
    args = parser.parse_args()
    result = run_wallet_structure_auto_task(
        output_root=args.output_root,
        cycles=args.cycles,
        interval_seconds=args.interval_seconds,
        limit=args.limit,
        include_s2=args.include_s2,
        run_quote_security=args.run_quote_security,
        wallet_structure_mode=args.wallet_structure_mode,
        resume=args.resume,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
