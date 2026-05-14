#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-auto task-package runner for K00 KV → next_actions → verification.

This runner is the machine control loop:
1. consume a task package / task manifest
2. extract K00 standard KV facts
3. execute runner-readable next_actions when present
4. write apply manifest, verification, writeback, and next task manifest

It stays paper-only and additive. It never signs, broadcasts, swaps, or reads
private keys.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sikk_k00_kv_extractor import extract_kv_from_task_package, safe_slug
from sikk_wallet_structure_apply_task_package import apply_task_package

DEFAULT_OUTPUT_ROOT = Path("research_loop/state/full_auto_task_runner")
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def read_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)


def normalize_manifest_for_runner(source_package: str | Path, output_dir: Path) -> dict[str, Any]:
    payload = read_json(source_package)
    if isinstance(payload.get("next_actions"), list):
        return {"manifest_path": str(source_package), "manifest": payload, "created": False}

    # K00 task_execution_package often uses `tasks`; convert them into safe runner actions.
    actions = []
    for idx, task in enumerate(payload.get("tasks", []) if isinstance(payload.get("tasks"), list) else [], 1):
        if not isinstance(task, dict):
            continue
        output = str(task.get("output") or "sikk_stable_trader_os/00_knowledge_intake/task_packages")
        actions.append({
            "order": idx,
            "priority": "P0" if str(task.get("phase", "")).startswith("K00") else "P1",
            "source_file": str(source_package),
            "gap_type": "k00_task_execution_package_task",
            "capability": safe_slug(task.get("task_id") or task.get("action") or f"task_{idx}"),
            "action": "materialize_task_output_contract",
            "target_module": output,
            "task_id": task.get("task_id"),
            "task_action": task.get("action"),
            "acceptance": task.get("acceptance"),
            "automation_step": {
                "create_test_first": True,
                "suggested_runtime_target": output,
                "safe_mode": "paper_only_readonly_additive",
            },
        })
    manifest = {
        "artifact_type": "normalized_full_auto_task_manifest",
        "task_id": payload.get("package_id") or payload.get("task_id") or safe_slug(Path(str(source_package)).stem),
        "source_task_package": str(source_package),
        "status": "NEEDS_ACTION" if actions else "COMPLETED",
        "generated_at": utc_now(),
        "objective": payload.get("objective"),
        "next_actions": actions,
        "automation_policy": {
            "delete_old_files": False,
            "move_old_files": False,
            "copy_legacy_to_new_layout": True,
            "paper_only": True,
            "no_private_key": True,
            "no_signing": True,
            "no_broadcast": True,
            "no_swap": True,
        },
        "safety_boundary": payload.get("safety_boundary", "OBSERVE_PAPER_ONLY"),
    }
    manifest_path = output_dir / "normalized_task_manifest.json"
    write_json(manifest_path, manifest)
    return {"manifest_path": str(manifest_path), "manifest": manifest, "created": True}


def build_verification(*, k00_result: dict[str, Any], apply_result: dict[str, Any] | None, normalized_manifest: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "kv_cache_manifest_exists": Path(k00_result["kv_cache_manifest"]).exists(),
        "kv_items_exists": Path(k00_result["kv_items"]).exists(),
        "k00_facts_exists": Path(k00_result["k00_facts"]).exists(),
        "has_kv_items": k00_result.get("item_count", 0) > 0,
        "normalized_manifest_exists": Path(normalized_manifest["manifest_path"]).exists(),
        "apply_manifest_exists": bool(apply_result and Path(apply_result.get("apply_manifest", "")).exists()),
    }
    status = "PASS" if all(checks.values()) else "NEEDS_ACTION"
    return {
        "artifact_type": "full_auto_task_runner_verification",
        "generated_at": utc_now(),
        "status": status,
        "checks": checks,
        "k00_result": k00_result,
        "apply_result": apply_result or {"status": "SKIPPED", "reason": "no runner actions"},
    }


def build_next_task_manifest(*, source_manifest: dict[str, Any], verification: dict[str, Any], apply_result: dict[str, Any] | None) -> dict[str, Any]:
    pending_actions = []
    if verification["status"] != "PASS":
        pending_actions.append({
            "order": 1,
            "priority": "P0",
            "source_file": verification.get("k00_result", {}).get("k00_facts"),
            "gap_type": "full_auto_runner_verification_gap",
            "capability": "runner_verification_repair",
            "action": "repair_missing_runner_artifacts",
            "target_module": "research_loop/state/full_auto_task_runner",
        })
    if apply_result and apply_result.get("skipped_count", 0) > 0:
        pending_actions.append({
            "order": len(pending_actions) + 1,
            "priority": "P1",
            "source_file": apply_result.get("apply_manifest"),
            "gap_type": "deferred_lower_priority_actions",
            "capability": "apply_remaining_next_actions",
            "action": "rerun_with_higher_max_priority",
            "target_module": "sikk_full_auto_task_package_runner.py",
        })
    return {
        "artifact_type": "next_task_manifest",
        "source_task_id": source_manifest.get("task_id"),
        "generated_at": utc_now(),
        "status": "NEEDS_ACTION" if pending_actions else "COMPLETED",
        "next_actions": pending_actions,
        "acceptance": {
            "full_auto_runner_status": verification["status"],
            "pending_action_count": len(pending_actions),
        },
    }


def run_full_auto_task_package(
    *,
    project_root: str | Path = ".",
    task_package: str | Path,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    task_id: str | None = None,
    max_priority: str = "P2",
    only_priority: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    tid = task_id or f"full_auto_{safe_slug(Path(str(task_package)).stem)}_{utc_stamp()}"
    run_dir = root / Path(output_root) / tid
    run_dir.mkdir(parents=True, exist_ok=True)

    k00 = extract_kv_from_task_package(
        task_package_path=task_package,
        output_root=run_dir / "k00_kv",
        schema_path=root / "sikk_stable_trader_os/00_knowledge_intake/kv_cache/kv_cache.schema.json",
    )
    normalized = normalize_manifest_for_runner(task_package, run_dir / "runner_input")
    manifest = normalized["manifest"]
    apply_result = None
    if manifest.get("next_actions"):
        apply_result = apply_task_package(
            project_root=root,
            task_manifest=normalized["manifest_path"],
            max_priority=max_priority,
            only_priority=only_priority,
            task_id=f"{tid}_apply",
        )

    verification = build_verification(k00_result=k00, apply_result=apply_result, normalized_manifest=normalized)
    verification_path = write_json(run_dir / "verification.json", verification)
    verification_md_path = write_text(
        run_dir / "verification.md",
        "\n".join([
            "# Full Auto Task Runner Verification",
            "",
            f"- status: `{verification['status']}`",
            f"- task_package: `{task_package}`",
            f"- kv_cache_manifest: `{k00['kv_cache_manifest']}`",
            f"- k00_facts: `{k00['k00_facts']}`",
            f"- apply_manifest: `{(apply_result or {}).get('apply_manifest', 'SKIPPED')}`",
            "",
            "## Checks",
            *[f"- {key}: `{value}`" for key, value in verification["checks"].items()],
            "",
        ]) + "\n",
    )
    next_task = build_next_task_manifest(source_manifest=manifest, verification=verification, apply_result=apply_result)
    next_task_path = write_json(run_dir / "next_task_manifest.json", next_task)
    writeback = {
        "artifact_type": "full_auto_task_runner_writeback",
        "task_id": tid,
        "generated_at": utc_now(),
        "status": "COMPLETED" if verification["status"] == "PASS" else "NEEDS_ACTION",
        "source_task_package": str(task_package),
        "normalized_task_manifest": normalized["manifest_path"],
        "k00_facts": k00["k00_facts"],
        "kv_cache_manifest": k00["kv_cache_manifest"],
        "apply_manifest": (apply_result or {}).get("apply_manifest"),
        "verification_json": verification_path,
        "verification_md": verification_md_path,
        "next_task_manifest": next_task_path,
        "safety_boundary": {
            "paper_only": True,
            "readonly_source_files": True,
            "additive_outputs_only": True,
            "no_private_key": True,
            "no_signing": True,
            "no_broadcast": True,
            "no_swap": True,
        },
    }
    writeback_path = write_json(run_dir / "writeback_manifest.json", writeback)
    return {
        "status": writeback["status"],
        "task_id": tid,
        "run_dir": str(run_dir),
        "k00_facts": k00["k00_facts"],
        "kv_cache_manifest": k00["kv_cache_manifest"],
        "normalized_task_manifest": normalized["manifest_path"],
        "apply_manifest": (apply_result or {}).get("apply_manifest"),
        "verification_json": verification_path,
        "verification_md": verification_md_path,
        "writeback_manifest": writeback_path,
        "next_task_manifest": next_task_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full-auto K00 task-package flow")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--task-package", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--task-id", default="")
    parser.add_argument("--max-priority", choices=["P0", "P1", "P2"], default="P2")
    parser.add_argument("--only-priority", choices=["P0", "P1", "P2"], default=None)
    args = parser.parse_args()
    result = run_full_auto_task_package(
        project_root=args.project_root,
        task_package=args.task_package,
        output_root=args.output_root,
        task_id=args.task_id or None,
        max_priority=args.max_priority,
        only_priority=args.only_priority,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
