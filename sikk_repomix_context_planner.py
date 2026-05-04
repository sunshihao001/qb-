#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Repomix context planner.

Generate local-only Repomix context plan/scripts for GPT → Hermes → Repomix → SIKK workflows.
This module writes files only; it does not run repomix, read secrets, trade, sign, or broadcast.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SAFETY_BOUNDARY: Dict[str, bool] = {
    "paper_only": True,
    "不真实交易": True,
    "不读取私钥": True,
    "不签名": True,
    "不广播": True,
}

DEFAULT_CONTEXTS: List[Dict[str, Any]] = [
    {
        "phase": "full",
        "description": "全仓库压缩上下文，用于系统架构审计。",
        "output": "ai_context/full/sikk_full_architecture.xml",
        "files": [],
    },
    {
        "phase": "index",
        "description": "统一索引、查询、dashboard 与 paper review 上下文。",
        "output": "ai_context/index/sikk_index_context.xml",
        "files": [
            "sikk_unified_view_builder.py",
            "sikkctl.py",
            "sikk_dashboard_site_builder.py",
            "sikk_paper_live_runner.py",
            "sikk_paper_auto_reviewer.py",
            "sikk_paper_explanation_builder.py",
            "tests/test_sikk_unified_view_builder.py",
            "tests/test_sikkctl.py",
        ],
    },
    {
        "phase": "wallet",
        "description": "GMGN 钱包结构、同源候选、结构融合上下文。",
        "output": "ai_context/wallet/sikk_wallet_context.xml",
        "files": [
            "sikk_gmgn_token_report.py",
            "sikk_candidate_wallet_structure_pipeline.py",
            "sikk_wallet_structure_gate.py",
            "sikk_wallet_structure_snapshot.py",
            "sikk_same_source_grouping.py",
            "sikk_wallet_intelligence_adapter.py",
            "sikk_structure_intelligence_fusion.py",
            "tests/test_sikk_wallet_structure_gate.py",
        ],
    },
    {
        "phase": "cluster",
        "description": "OKX Top300 cluster 与筹码控制上下文。",
        "output": "ai_context/cluster/sikk_cluster_context.xml",
        "files": [
            "sikk_okx_cluster_holding_analyzer.py",
            "sikk_okx_cluster_delta.py",
            "sikk_chip_control_state_machine.py",
            "sikk_structure_intelligence_fusion.py",
            "tests/test_sikk_okx_cluster_holding_analyzer.py",
        ],
    },
    {
        "phase": "case",
        "description": "Case File、证据链、完整性审计上下文。",
        "output": "ai_context/case/sikk_case_context.xml",
        "files": [
            "sikk_case_field_source_map.py",
            "sikk_case_data_completeness_auditor.py",
            "sikk_case_data_backfill.py",
            "sikk_paper_explanation_builder.py",
        ],
    },
    {
        "phase": "telegram",
        "description": "Telegram 中文控制台、按钮与回调上下文。",
        "output": "ai_context/telegram/sikk_telegram_context.xml",
        "files": [
            "sikk_telegram_bot_handler.py",
            "sikk_telegram_views.py",
            "sikk_telegram_gateway_adapter.py",
            "tests/test_sikk_telegram_views.py",
        ],
    },
    {
        "phase": "web",
        "description": "静态 dashboard 与移动端详情页上下文。",
        "output": "ai_context/web/sikk_web_context.xml",
        "files": [
            "sikk_dashboard_site_builder.py",
            "site/app.js",
            "site/index.html",
            "site/style.css",
            "tests/test_sikk_dashboard_site_builder.py",
        ],
    },
    {
        "phase": "runtime",
        "description": "canonical runtime 与 paper runner 上下文。",
        "output": "ai_context/runtime/sikk_runtime_context.xml",
        "files": [
            "sikk_live_run.py",
            "sikk_full_auto_orchestrator.py",
            "sikk_paper_live_runner.py",
            "tests/test_sikk_live_run.py",
            "tests/test_sikk_full_auto_orchestrator.py",
        ],
    },
    {
        "phase": "audit",
        "description": "系统审计、解释、研究循环上下文。",
        "output": "ai_context/audit/sikk_audit_context.xml",
        "files": [
            "sikk_system_audit.py",
            "sikk_explainability_engine.py",
            "sikk_research_loop_controller.py",
            "sikk_gap_detector.py",
            "tests/test_sikk_system_audit.py",
            "tests/test_sikk_research_loop_controller.py",
        ],
    },
]

IGNORE_PATTERNS = "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"


def _slug(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value).strip("_") or "repomix_context"


def _render_shell(root: Path) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        'PHASE="${1:-full}"',
        f'ROOT="{root}"',
        'OUT="$ROOT/ai_context"',
        'mkdir -p "$OUT"/{full,index,wallet,cluster,case,telegram,web,runtime,audit,diff}',
        'cd "$ROOT"',
        'case "$PHASE" in',
    ]
    for ctx in DEFAULT_CONTEXTS:
        phase = ctx["phase"]
        output = ctx["output"]
        files = ctx["files"]
        lines.append(f"  {phase})")
        if files:
            lines.append(f'    cat > "$OUT/{phase}/files.txt" <<\'FILES\'')
            lines.extend(files)
            lines.append("FILES")
            lines.append(f'    cat "$OUT/{phase}/files.txt" | repomix --stdin --compress --output "$ROOT/{output}" --ignore "{IGNORE_PATTERNS}"')
        else:
            lines.append(f'    repomix --compress --output "$ROOT/{output}" --ignore "{IGNORE_PATTERNS}"')
        lines.append("    ;;")
    lines.extend([
        "  *)",
        '    echo "Unknown phase: $PHASE" >&2',
        "    exit 2",
        "    ;;",
        "esac",
        "",
    ])
    return "\n".join(lines)


def build_repomix_context_plan(*, root: str | Path = "/root/sikk-gmgn", task_slug: str = "repomix_deerflow_harness") -> Dict[str, str]:
    root_path = Path(root)
    slug = _slug(task_slug)
    plan_dir = root_path / "tasks" / slug / "repomix_context"
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan = {
        "task_slug": slug,
        "root": str(root_path),
        "contexts": DEFAULT_CONTEXTS,
        "ignore_patterns": IGNORE_PATTERNS,
        "安全边界": SAFETY_BOUNDARY,
    }
    plan_json = plan_dir / "REPOMIX_CONTEXT_PLAN.json"
    plan_md = plan_dir / "REPOMIX_CONTEXT_PLAN.md"
    shell = plan_dir / "make_sikk_context.sh"
    plan_json.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    plan_md.write_text(
        "\n".join([
            "# Repomix Context Plan｜SIKK",
            "",
            "- 目标: 为 Hermes/DeerFlow-style 多角色执行提供分阶段代码上下文。",
            "- 边界: paper-only；不读取私钥；不签名；不广播；不执行真实交易。",
            "",
            "## Contexts",
            *[f"- `{ctx['phase']}`: {ctx['description']} → `{ctx['output']}`" for ctx in DEFAULT_CONTEXTS],
            "",
            "## 使用",
            "```bash",
            f"bash {shell} full",
            f"bash {shell} runtime",
            "```",
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    shell.write_text(_render_shell(root_path), encoding="utf-8")
    shell.chmod(0o755)
    return {"plan_json": str(plan_json), "plan_md": str(plan_md), "shell_script": str(shell)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SIKK Repomix context plan")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    parser.add_argument("--task-slug", default="repomix_deerflow_harness")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_repomix_context_plan(root=args.root, task_slug=args.task_slug), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
