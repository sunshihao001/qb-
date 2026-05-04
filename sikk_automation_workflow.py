#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 自动工作流计划器。

把 ChatGPT share 中的“连续定时运行”建议落成项目内可审计计划文件。
本模块只生成计划/cron 提示/验收清单，不启动真实交易，不读取私钥，不签名，不广播。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping

DEFAULT_ROOT = Path("data/gmgn_candidates_live_run")
DEFAULT_COMMAND = (
    "PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py "
    "--mode once --output-root data/gmgn_candidates_live_run "
    "--limit 50 --quote-sources okx --default-quote-amount-sol 0.01"
)


def build_workflow_plan(*, output_root: str | Path = DEFAULT_ROOT, command: str = DEFAULT_COMMAND) -> Dict[str, Any]:
    """构建 SIKK paper-only 自动工作流计划。

    返回结构化 JSON，供 Telegram/Hermes/cron/job runner 读取。这里不直接创建
    系统 cron，避免在项目脚本里隐藏副作用；真正调度由 Hermes cronjob 或用户明确启动。
    """

    root = str(Path(output_root))
    return {
        "workflow_name": "SIKK-SOL HER 核心自动化工作流",
        "version": "her_core_automation_v1",
        "output_root": root,
        "cognitive_principle": "目标自治 + 工具选择自治 + 阶段执行自治 + 验收自治，但必须受 paper-only 与测试验收护栏约束。",
        "tool_routing": {
            "GPT/ChatGPT 分享链接": ["conversation-transcript-ingestion", "sikk_knowledge_absorption.py", "Section Task 合同"],
            "复杂代码/架构审计": ["Super Hermes prism-scan/prism-3way/prism-reflect", "systematic-debugging", "requesting-code-review"],
            "跨模型代码库上下文包": ["repomix", "secretlint/安全排除", "限定 include/exclude 范围"],
            "多小时研究/多代理任务": ["DeerFlow", "delegate_task 子代理", "阶段验收报告"],
            "SIKK 运行落地": ["sikk_live_run.py 单入口", "sikk_query/sikkctl", "Telegram 中文视图", "静态 dashboard"],
        },
        "safety_boundary": {
            "paper_only": True,
            "real_swap_enabled": False,
            "private_key_required": False,
            "signing_enabled": False,
            "broadcast_enabled": False,
            "scope_note": "本计划只调度候选发现、报价安全、纸面持仓、复盘与静态看板；不执行真实 swap。",
        },
        "default_command": command,
        "task_lens_stages": [
            {
                "stage_id": "lens_1_read",
                "中文名称": "读取与证据保存",
                "required_actions": ["读取链接或声明不可读", "保存原文到 knowledge/inbox", "记录来源与可读性"],
                "acceptance": "存在 inbox 原文；报告中不假装读取。",
            },
            {
                "stage_id": "lens_2_problem",
                "中文名称": "问题识别与隐藏断点",
                "required_actions": ["提取核心机制", "识别表面完成但未接入流程的断点", "列出盲点"],
                "acceptance": "输出缺口清单与约束报告。",
            },
            {
                "stage_id": "lens_3_map",
                "中文名称": "系统映射审计",
                "required_actions": ["搜索现有文件", "映射到 runtime/TG/dashboard/paper/skill", "确定最小修改路径"],
                "acceptance": "每个结论绑定文件、字段、命令或测试。",
            },
            {
                "stage_id": "lens_4_execute",
                "中文名称": "分阶段实现",
                "required_actions": ["先写/更新测试", "修改代码或知识资产", "运行专项验证"],
                "acceptance": "测试通过且产物可追溯。",
            },
            {
                "stage_id": "lens_5_verify",
                "中文名称": "审计验收与沉淀",
                "required_actions": ["运行主入口最小验证", "检查 manifest 安全开关", "更新 skill/knowledge/index"],
                "acceptance": "验收报告说明完成项、未完成项、风险、下一步。",
            },
        ],
        "schedules": [
            {
                "job_id": "candidate_signal_cycle",
                "中文名称": "候选发现 + K线信号 + 状态机 + quote/security + 纸面更新",
                "interval_minutes": 10,
                "command": command,
                "expected_outputs": [
                    f"{root}/gmgn_new_token_filter/token_candidates.json",
                    f"{root}/candidate_signal_outputs/candidate_signal_summary.json",
                    f"{root}/state_machine/candidate_states.json",
                    f"{root}/quote_security/candidate_quote_security_summary.json",
                    f"{root}/paper_live/paper_positions_open.json",
                    f"{root}/paper_live/paper_positions_closed.json",
                ],
            },
            {
                "job_id": "paper_position_refresh",
                "中文名称": "纸面持仓刷新",
                "interval_minutes": 3,
                "command": command,
                "expected_outputs": [
                    f"{root}/paper_live/paper_positions_open.json",
                    f"{root}/paper_live/paper_trades.csv",
                    f"{root}/paper_live/position_journal/",
                ],
            },
            {
                "job_id": "daily_review",
                "中文名称": "日报 + 钱包结构日报 + 静态控制台刷新",
                "cron": "0 0 * * *",
                "command": command,
                "expected_outputs": [
                    f"{root}/paper_live/daily_reports/",
                    f"{root}/wallet_structure_daily_report/",
                    f"{root}/site/dashboard_data.json",
                    f"{root}/site/index.html",
                ],
            },
        ],
        "gates": [
            "PAPER_READY 才能进入纸面候选",
            "quote/security 为 BLOCK_BUY 时必须阻断",
            "PAUSE_NEED_CONFIRM 只暂停，不纸面入场",
            "同一 token 只允许一个开放纸面仓位",
            "钱包结构强风险默认 EXIT_MONITOR；多轮 delta + 盘型/市场确认后才 FORCE_PAPER_EXIT",
        ],
        "acceptance_checks": [
            "PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q",
            command,
            "检查 live_run_manifest.json 中 real_swap_enabled=false 且 confirmation_enabled=false",
            "检查 paper_daily_report 中包含 不执行真实 swap",
        ],
    }


def write_workflow_plan(*, output_root: str | Path = DEFAULT_ROOT, path: str | Path | None = None, command: str = DEFAULT_COMMAND) -> Dict[str, str]:
    out = Path(output_root)
    plan_path = Path(path) if path else out / "automation" / "sikk_paper_workflow_plan.json"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan = build_workflow_plan(output_root=output_root, command=command)
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = plan_path.with_suffix(".md")
    lines: List[str] = [
        "# SIKK-SOL HER 核心自动化工作流计划",
        "",
        f"- 输出目录：`{plan['output_root']}`",
        f"- 核心认知：{plan['cognitive_principle']}",
        "- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
        "",
        "## 任务棱镜阶段",
    ]
    for stage in plan["task_lens_stages"]:
        lines.append(f"- {stage['中文名称']}：{stage['acceptance']}")
    lines.extend(["", "## 工具路由"])
    for scenario, tools in plan["tool_routing"].items():
        lines.append(f"- {scenario}：" + " / ".join(tools))
    lines.extend(["", "## 调度节奏"])
    for job in plan["schedules"]:
        cadence = f"每 {job['interval_minutes']} 分钟" if job.get("interval_minutes") else f"cron `{job.get('cron')}`"
        lines.append(f"- {job['中文名称']}：{cadence}")
        lines.append(f"  - 命令：`{job['command']}`")
    lines.extend(["", "## 门禁", *[f"- {gate}" for gate in plan["gates"]], "", "## 验收命令", *[f"- `{check}`" for check in plan["acceptance_checks"]]])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"workflow_plan_json": str(plan_path), "workflow_plan_md": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 SIKK paper-only 自动工作流计划")
    parser.add_argument("--output-root", default=str(DEFAULT_ROOT))
    parser.add_argument("--path", default=None)
    parser.add_argument("--command", default=DEFAULT_COMMAND)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(write_workflow_plan(output_root=args.output_root, path=args.path, command=args.command), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
