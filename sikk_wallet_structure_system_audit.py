#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wallet structure system audit.

Finds places where Wallet-Intel rules exist only as documents/contracts but are
not wired into the runnable wallet-structure system.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANONICAL_ROUTE = [
    "modules/source_wallet_bot",
    "modules/wallet_data_guard",
    "sikk_candidate_wallet_structure_pipeline.py",
    "sikk_wallet_structure_gate.py",
    "sikk_same_source_grouping.py",
    "sikk_chip_control_state_machine.py",
    "sikk_candidate_state_machine.py / sikk_live_run.py",
]

EXPECTED_RUNTIME_ARTIFACTS = {
    "source_wallet_runner": "modules/source_wallet_bot/runner.py",
    "source_wallet_gmgn_adapter": "modules/source_wallet_bot/gmgn_live_adapter.py",
    "wallet_data_guard": "modules/wallet_data_guard/contamination_scan.py",
    "candidate_wallet_pipeline": "sikk_candidate_wallet_structure_pipeline.py",
    "wallet_structure_gate": "sikk_wallet_structure_gate.py",
    "same_source_grouping": "sikk_same_source_grouping.py",
    "chip_control_state_machine": "sikk_chip_control_state_machine.py",
    "candidate_state_machine": "sikk_candidate_state_machine.py",
    "pipeline_orchestrator": "run_sikk_gmgn_pipeline.py",
}

GAP_DEFINITIONS = [
    {
        "id": "LONG_RUNNING_AUTO_RUNNER",
        "status": "needs_runtime_code",
        "severity": "HIGH",
        "description": "缺少面向钱包结构系统的长时间循环 runner、checkpoint/resume、周期 manifest。",
        "runtime_fix": "sikk_wallet_structure_auto_runner.py",
        "resolution_anchors": [
            ("sikk_wallet_structure_auto_runner.py", "run_wallet_structure_auto_task"),
            ("sikk_wallet_structure_auto_runner.py", "checkpoint_path"),
            ("sikk_wallet_structure_auto_runner.py", "wallet_structure_auto_task_manifest"),
        ],
    },
    {
        "id": "ACCEPTANCE_NOT_IN_PIPELINE_MANIFEST",
        "status": "partial_runtime_integration",
        "severity": "MEDIUM",
        "description": "Source Wallet acceptance validator 存在，但未作为全流程 orchestrator/长任务每轮固定验收输出。",
        "runtime_fix": "auto runner 每轮写 acceptance/system audit 引用。",
        "resolution_anchors": [
            ("sikk_wallet_structure_auto_runner.py", "validate_source_wallet_design_package"),
            ("sikk_wallet_structure_auto_runner.py", "acceptance_status"),
            ("sikk_wallet_structure_auto_runner.py", "_run_acceptance"),
        ],
    },
    {
        "id": "WALLET_GUARD_SYSTEM_WIDE_INDEX",
        "status": "partial_runtime_integration",
        "severity": "MEDIUM",
        "description": "wallet_data_guard 已接入 upstream 与 candidate pipeline，但缺系统级汇总索引方便长时间任务追踪污染趋势。",
        "runtime_fix": "auto runner 聚合每轮 guard 状态。",
        "resolution_anchors": [
            ("sikk_wallet_structure_auto_runner.py", "wallet_data_guard_trend_index"),
            ("sikk_wallet_structure_auto_runner.py", "guard_trend_index_path"),
            ("sikk_wallet_structure_auto_runner.py", "_build_guard_trend_index"),
        ],
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _build_md(report: dict[str, Any]) -> str:
    lines = [
        "# 钱包结构分析系统全流程审计",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- overall_status: `{report['overall_status']}`",
        "",
        "## Canonical Route",
        "",
    ]
    for item in report["canonical_route"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Runtime Artifacts", ""])
    for item in report["runtime_artifacts"]:
        lines.append(f"- {item['name']}：{item['status']} — `{item['path']}`")
    lines.extend(["", "## 文档已有但运行接入不足", ""])
    if report["gaps"]:
        for gap in report["gaps"]:
            lines.append(f"- {gap['id']}｜{gap['severity']}｜{gap['status']}：{gap['description']}")
            lines.append(f"  - runtime_fix: {gap['runtime_fix']}")
    else:
        lines.append("- none")
    lines.extend(["", "## 已补全运行能力", ""])
    if report.get("resolved_gaps"):
        for gap in report["resolved_gaps"]:
            lines.append(f"- {gap['id']}｜{gap['severity']}｜resolved：{gap['runtime_fix']}")
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Safety Boundary",
        "",
        "- paper_only: true",
        "- read_only_collectors: true",
        "- real_swap_enabled: false",
        "- signing_enabled: false",
        "- broadcast_enabled: false",
    ])
    return "\n".join(lines) + "\n"


def _is_gap_resolved(root: Path, gap: dict[str, Any]) -> bool:
    anchors = gap.get("resolution_anchors") or []
    for rel, needle in anchors:
        path = root / rel
        if not path.exists():
            return False
        if needle not in path.read_text(encoding="utf-8", errors="ignore"):
            return False
    return True


def _public_gap(gap: dict[str, Any], *, resolved: bool) -> dict[str, Any]:
    cleaned = {k: v for k, v in gap.items() if k != "resolution_anchors"}
    cleaned["resolution_status"] = "resolved" if resolved else "open"
    return cleaned


def audit_wallet_structure_system(*, project_root: str | Path = ".", output_dir: str | Path | None = None) -> dict[str, Any]:
    root = Path(project_root)
    out = Path(output_dir) if output_dir is not None else root / "data" / "source_wallet_bot" / "system_audit"
    artifacts = []
    for name, rel in EXPECTED_RUNTIME_ARTIFACTS.items():
        path = root / rel
        artifacts.append({
            "name": name,
            "path": rel,
            "status": "present" if path.exists() else "missing",
        })
    missing = [a for a in artifacts if a["status"] == "missing"]
    open_gaps = []
    resolved_gaps = []
    for gap in GAP_DEFINITIONS:
        resolved = _is_gap_resolved(root, gap)
        (resolved_gaps if resolved else open_gaps).append(_public_gap(gap, resolved=resolved))
    report: dict[str, Any] = {
        "artifact_type": "wallet_structure_system_audit",
        "generated_at": _utc_now(),
        "overall_status": "NEEDS_COMPLETION" if open_gaps or missing else "PASS",
        "canonical_route": CANONICAL_ROUTE,
        "runtime_artifacts": artifacts,
        "missing_runtime_artifacts": missing,
        "gaps": open_gaps,
        "resolved_gaps": resolved_gaps,
        "safety_boundary": {
            "paper_only": True,
            "read_only_collectors": True,
            "real_swap_enabled": False,
            "private_key_required": False,
            "signing_enabled": False,
            "broadcast_enabled": False,
        },
    }
    json_path = out / "wallet_structure_system_audit.json"
    md_path = out / "wallet_structure_system_audit.md"
    report["json_path"] = _write_json(json_path, report)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(_build_md(report), encoding="utf-8")
    report["md_path"] = str(md_path)
    _write_json(json_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit SIKK Wallet-Intel runnable system coverage")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    result = audit_wallet_structure_system(project_root=args.project_root, output_dir=args.output_dir or None)
    print(json.dumps({"json_path": result["json_path"], "md_path": result["md_path"], "overall_status": result["overall_status"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
