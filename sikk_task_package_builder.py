#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes task package builder for the research loop.

Consumes a gap report or system map and emits a paper-only task package with
clear safety boundaries, phase plan, acceptance checklist, and execution hints.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT_ROOT = Path("research_loop/task_packages/generated")


def _slug(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(value).strip())
    return cleaned.strip("_") or "task"


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _task_id(doc_id: str) -> str:
    return f"{_slug(doc_id)}_task"


def build_task_package(*, doc_id: str, gap_matrix_csv: str | Path, output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    task_id = _task_id(doc_id)
    task_dir = root / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    gaps = _read_csv(Path(gap_matrix_csv))
    gap_types = sorted({row.get("gap_type", "") for row in gaps if row.get("gap_type")})
    modules = sorted({row.get("module", "") for row in gaps if row.get("module")})

    master = task_dir / "MASTER_TASK.md"
    phase_plan = task_dir / "PHASE_PLAN.md"
    safety = task_dir / "SAFETY_BOUNDARY.md"
    checklist = task_dir / "ACCEPTANCE_CHECKLIST.md"
    context = task_dir / "CURRENT_CONTEXT.md"
    repomix = task_dir / "REPOMIX_CONTEXT_PLAN.md"
    deerflow = task_dir / "DEERFLOW_METHOD.md"
    hermes = task_dir / "HERMES_START_COMMAND.md"

    gap_lines = [f"- {gap}" for gap in gap_types] or ["- 无缺口"]
    module_lines = [f"- {module}" for module in modules] or ["- 无模块"]
    master.write_text(
        "\n".join([
            f"# {task_id}｜Hermes 任务包",
            "",
            "## 目标",
            "把 gap report 中的缺口转成可执行、可验收、paper-only 的研究/实现任务包。",
            "",
            "## 当前缺口概览",
            *gap_lines,
            "",
            "## 关联模块",
            *module_lines,
            "",
            "## 安全边界",
            "paper-only；不执行真实 swap；不读取私钥；不签名；不广播；不新增 BUY/SELL/SWAP/EXECUTE/APPROVE/BROADCAST。",
        ]) + "\n",
        encoding="utf-8",
    )
    phase_plan.write_text(
        "\n".join([
            "# Phase Plan",
            "",
            "1. 识别 gap 类型与优先级",
            "2. 找到最小文件改动路径",
            "3. 写测试先行",
            "4. 实现最小功能",
            "5. 运行专项测试",
            "6. 输出验收报告",
        ]) + "\n",
        encoding="utf-8",
    )
    safety.write_text(
        "\n".join([
            "# Safety Boundary",
            "",
            "- paper_only: true",
            "- real_swap_enabled: false",
            "- private_key_required: false",
            "- signing_enabled: false",
            "- broadcast_enabled: false",
            "- no buy/sell/swap/execute/approve/broadcast terms in generated instructions",
        ]) + "\n",
        encoding="utf-8",
    )
    checklist.write_text(
        "\n".join([
            "# Acceptance Checklist",
            "",
            "- gap matrix 已生成",
            "- 任务包目录已生成",
            "- 安全边界明确为 paper-only",
            "- 没有真实交易动作",
            "- 没有私钥读取",
            "- 没有广播",
            "- 每个任务都能映射到测试",
        ]) + "\n",
        encoding="utf-8",
    )
    context.write_text(
        "\n".join([
            "# Current Context",
            "",
            f"- doc_id: `{doc_id}`",
            f"- gap_matrix_csv: `{gap_matrix_csv}`",
            f"- gap_types: {', '.join(gap_types) if gap_types else 'none'}",
            f"- modules: {', '.join(modules) if modules else 'none'}",
            "- runtime: paper-only",
        ]) + "\n",
        encoding="utf-8",
    )
    repomix.write_text(
        "\n".join([
            "# Repomix Context Plan",
            "",
            "- Include: target module files, tests, AGENTS.md, current research loop docs",
            "- Exclude: secrets, tokens, private keys, generated artifacts not needed for implementation",
            "- Goal: provide compact cross-model context for the next Hermes execution step",
        ]) + "\n",
        encoding="utf-8",
    )
    deerflow.write_text(
        "\n".join([
            "# DeerFlow Method",
            "",
            "- Split the package into small tasks",
            "- Each task must have a test-first step",
            "- Run verify after each task",
            "- Keep paper-only safety boundary",
        ]) + "\n",
        encoding="utf-8",
    )
    hermes.write_text(
        "\n".join([
            "# Hermes Start Command",
            "",
            "```bash",
            f"python3 sikk_research_loop_controller.py review-hermes --input {task_dir}",
            "```",
        ]) + "\n",
        encoding="utf-8",
    )

    return {
        "task_dir": str(task_dir),
        "MASTER_TASK.md": str(master),
        "PHASE_PLAN.md": str(phase_plan),
        "SAFETY_BOUNDARY.md": str(safety),
        "ACCEPTANCE_CHECKLIST.md": str(checklist),
        "CURRENT_CONTEXT.md": str(context),
        "REPOMIX_CONTEXT_PLAN.md": str(repomix),
        "DEERFLOW_METHOD.md": str(deerflow),
        "HERMES_START_COMMAND.md": str(hermes),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Hermes task package from gap matrix")
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--gap-matrix-csv", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_task_package(doc_id=args.doc_id, gap_matrix_csv=args.gap_matrix_csv, output_root=args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
