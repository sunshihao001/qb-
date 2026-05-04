#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK HER 任务启动器。

输入 GPT 链接或普通目标，生成任务棱镜、工具路由、Section Task 与验收清单。
本模块只写本地任务计划文件，不启动真实交易、不读取私钥、不签名、不广播。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from sikk_knowledge_absorption import absorb_article

SAFETY_BOUNDARY: Dict[str, Any] = {
    "paper_only": True,
    "real_swap_enabled": False,
    "private_key_required": False,
    "signing_enabled": False,
    "broadcast_enabled": False,
    "scope_note": "HER 任务启动器只生成任务计划、知识吸收入口、工具路由和验收清单；不执行真实 swap。",
}

DEFAULT_ACCEPTANCE = [
    "PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q",
    "PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q",
    "PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none",
    "检查 live_run_manifest.json 中 real_swap_enabled=false 且 confirmation_enabled=false",
]


def classify_task(source: str) -> str:
    lowered = source.lower().strip()
    if "chatgpt.com/share/" in lowered or "chat.openai.com/share/" in lowered:
        return "chatgpt_share"
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return "external_link"
    return "manual_goal"


def _safe_slug(source: str, task_type: str) -> str:
    if task_type == "chatgpt_share":
        match = re.search(r"share/([A-Za-z0-9_-]+)", source)
        if match:
            return "chatgpt_share_" + match.group(1).split("-")[0]
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:10]
    return f"{task_type}_{digest}"


def _recommended_skills(task_type: str, source: str) -> List[str]:
    skills = ["sikk-sol-core-methodology", "test-driven-development"]
    if task_type in {"chatgpt_share", "external_link"}:
        skills.insert(0, "conversation-transcript-ingestion")
    if any(term in source.lower() for term in ["debug", "bug", "失败", "报错"]):
        skills.append("systematic-debugging")
    if any(term in source.lower() for term in ["telegram", "tg", "面板", "命令"]):
        skills.append("sikk-sol-core-methodology")
    return list(dict.fromkeys(skills))


def _task_lens(task_type: str) -> List[Dict[str, Any]]:
    return [
        {
            "stage_id": "lens_1_read",
            "中文名称": "任务棱镜 1：读取与证据保存",
            "actions": ["读取链接或确认不可读", "保存原文/目标到 knowledge/inbox 或 tasks", "记录来源、时间、可读性"],
            "acceptance": "存在可追溯输入文件；不可读时明确声明。",
        },
        {
            "stage_id": "lens_2_problem",
            "中文名称": "任务棱镜 2：问题识别与断点发现",
            "actions": ["提取核心机制", "识别隐藏问题", "指出表面完成但未接入真实流程的部分"],
            "acceptance": "输出问题诊断、缺口清单和约束报告。",
        },
        {
            "stage_id": "lens_3_mapping",
            "中文名称": "任务棱镜 3：系统映射与工具选择",
            "actions": ["搜索 SIKK/Hermes 相关文件", "选择 skill/命令/工具", "绑定字段、模块、测试和报告"],
            "acceptance": "每个结论都落到文件、字段、命令、测试或验收标准。",
        },
        {
            "stage_id": "lens_4_execution",
            "中文名称": "任务棱镜 4：分阶段执行",
            "actions": ["先写测试", "修改知识资产/代码/文档", "运行专项测试"],
            "acceptance": "阶段产物可追溯，测试通过。",
        },
        {
            "stage_id": "lens_5_acceptance",
            "中文名称": "任务棱镜 5：审计验收与沉淀",
            "actions": ["运行全量测试", "运行 sikk_live_run 最小验证", "更新 skill/knowledge/index/报告"],
            "acceptance": "安全断言通过，生成中文验收报告。",
        },
    ]


def _tool_routes(task_type: str) -> List[Dict[str, str]]:
    routes = [
        {"场景": "SIKK 运行落地", "工具": "sikk_live_run.py", "用途": "保持 canonical 单入口与 paper-only runtime 验证。"},
        {"场景": "测试验收", "工具": "pytest", "用途": "专项测试、全量测试、防回归。"},
    ]
    if task_type in {"chatgpt_share", "external_link"}:
        routes.insert(0, {"场景": "链接读取", "工具": "browser/readability", "用途": "读取链接或明确声明不可读。"})
        routes.insert(1, {"场景": "知识吸收", "工具": "sikk_knowledge_absorption.py", "用途": "生成 passport/rules/audit/update/skill/Hindsight。"})
    routes.extend([
        {"场景": "结构深度审计", "工具": "Super Hermes prism 思维", "用途": "生成任务棱镜、盲点与约束报告。"},
        {"场景": "跨模型上下文", "工具": "repomix", "用途": "需要跨 LLM 提供代码库上下文时打包，必须先排除 secrets。"},
        {"场景": "多代理长任务", "工具": "DeerFlow/delegate_task", "用途": "研究、审计、实现、验收可拆分为独立子代理。"},
    ])
    return routes


def build_task_router_plan(source: str, *, root: str | Path = "/root/sikk-gmgn") -> Dict[str, Any]:
    task_type = classify_task(source)
    slug = _safe_slug(source, task_type)
    root = Path(root)
    expected_outputs = [
        f"tasks/{slug}/TASK_ROUTER.json",
        f"tasks/{slug}/TASK_ROUTER.md",
        f"tasks/{slug}/SECTION_TASK.md",
        "reports/<slug>/acceptance.md",
    ]
    if task_type in {"chatgpt_share", "external_link"}:
        expected_outputs.extend([
            f"knowledge/inbox/{slug}.md",
            f"knowledge/passports/{slug}.passport.md",
            f"knowledge/extracted_rules/{slug}.rules.md",
            f"knowledge/audits/{slug}.system_audit.md",
            f"knowledge/system_updates/{slug}.sikk_update.md",
        ])
    return {
        "task_router_name": "SIKK HER 任务启动器",
        "version": "her_task_router_v1",
        "source": source,
        "task_type": task_type,
        "slug": slug,
        "root": str(root),
        "safety_boundary": SAFETY_BOUNDARY,
        "recommended_skills": _recommended_skills(task_type, source),
        "task_lens": _task_lens(task_type),
        "tool_routes": _tool_routes(task_type),
        "expected_outputs": expected_outputs,
        "acceptance_checks": DEFAULT_ACCEPTANCE,
        "next_action": "先执行任务棱镜 1：读取与证据保存；不要直接改核心代码。",
    }


def _render_md(plan: Dict[str, Any]) -> str:
    lines = [
        "# HER 任务启动器",
        "",
        f"- 来源：`{plan['source']}`",
        f"- 任务类型：`{plan['task_type']}`",
        f"- Slug：`{plan['slug']}`",
        "- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
        "",
        "## 推荐 Skills",
    ]
    lines.extend(f"- `{skill}`" for skill in plan["recommended_skills"])
    lines.extend(["", "## 任务棱镜"])
    for lens in plan["task_lens"]:
        lines.append(f"- {lens['中文名称']}：{lens['acceptance']}")
    lines.extend(["", "## 工具路由"])
    for route in plan["tool_routes"]:
        lines.append(f"- {route['场景']}：`{route['工具']}` — {route['用途']}")
    lines.extend(["", "## 预期产物"])
    lines.extend(f"- `{item}`" for item in plan["expected_outputs"])
    lines.extend(["", "## 验收命令"])
    lines.extend(f"- `{check}`" for check in plan["acceptance_checks"])
    lines.extend(["", "## 下一步", plan["next_action"]])
    return "\n".join(lines) + "\n"


def _render_section_task(plan: Dict[str, Any]) -> str:
    return f"""# Section Task｜{plan['slug']}

## 目标
把输入任务转成 HER/Hermes 可执行的分阶段工作包，而不是只做总结。

## 范围
- 来源：`{plan['source']}`
- 类型：`{plan['task_type']}`
- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。

## 执行步骤
1. 读取相关文件或链接；不可读必须说明。
2. 建立任务棱镜与约束报告。
3. 做系统映射审计。
4. 按 TDD 修改知识资产/代码/文档。
5. 运行测试命令。
6. 输出验收标准与报告。

## 测试命令
{chr(10).join('- `' + check + '`' for check in plan['acceptance_checks'])}

## 验收标准
- 输入已保存或不可读已说明。
- 每个结论绑定文件、字段、命令、测试或验收标准。
- 所有新增能力可被真实命令或测试调用。
- 安全边界保持 false：real_swap/signing/broadcast/confirmation。
"""


def write_task_router_plan(source: str, *, root: str | Path = "/root/sikk-gmgn", output_dir: str | Path | None = None, execute_absorption: bool = False) -> Dict[str, str]:
    plan = build_task_router_plan(source, root=root)
    base = Path(output_dir) if output_dir else Path(root) / "tasks" / plan["slug"]
    base.mkdir(parents=True, exist_ok=True)
    json_path = base / "TASK_ROUTER.json"
    md_path = base / "TASK_ROUTER.md"
    section_path = base / "SECTION_TASK.md"
    json_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_render_md(plan), encoding="utf-8")
    section_path.write_text(_render_section_task(plan), encoding="utf-8")
    result: Dict[str, str] = {
        "task_router_json": str(json_path),
        "task_router_md": str(md_path),
        "section_task_md": str(section_path),
    }

    if execute_absorption and plan["task_type"] in {"chatgpt_share", "external_link"}:
        inbox_path = Path(root) / "knowledge" / "inbox" / f"{plan['slug']}.md"
        if not inbox_path.exists():
            inbox_path.parent.mkdir(parents=True, exist_ok=True)
            inbox_path.write_text(
                f"# {plan['slug']}\n\n来源：`{plan['source']}`\n\n自动吸收前置占位文件。\n",
                encoding="utf-8",
            )
        absorbed = absorb_article(root, inbox_path)
        result.update(absorbed)
        report_path = Path(root) / "reports" / plan["slug"] / "automation_absorption_acceptance.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            "# 自动吸收验收\n\n"
            f"- 任务：`{plan['source']}`\n"
            "- 结论：已执行知识吸收链路。\n"
            "- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。\n",
            encoding="utf-8",
        )
        result["acceptance_report"] = str(report_path)
    return result


def _render_workflow_command_md(source: str, plan: Dict[str, Any], package: Dict[str, Any]) -> str:
    command = package["本地一键命令"]
    return f"""# 手机可用入口｜SIKK GPT 工作流自动化

## Telegram 自然语言入口

直接发送：

```text
工作流自动化 {source}
```

说明：这是自然语言触发词，*无需 slash command*，可避开 Hermes Gateway 对未知 `/命令` 的拦截。

## VPS 本地一键命令

```bash
{command}
```

## 安全边界

- paper-only
- 禁止真实交易
- 禁止真实 swap
- 禁止读取私钥
- 禁止签名
- 禁止 broadcast

## 自动执行链路

1. 识别 GPT share / 外链 / 普通目标。
2. 生成 TASK_ROUTER 与 SECTION_TASK。
3. 自动执行知识吸收：inbox → passport → rules → audit → update → skill → Hindsight。
4. 生成工作流包与验收报告。
5. 后续仍通过 `sikk_live_run.py` 单入口做 paper-only runtime 验证。

## 当前 Slug

`{plan['slug']}`
"""


def _render_workflow_report_md(source: str, plan: Dict[str, Any], result: Dict[str, str]) -> str:
    lines = [
        "# 工作流自动化验收报告",
        "",
        f"- 来源：`{source}`",
        f"- Slug：`{plan['slug']}`",
        "- 状态：已生成",
        "- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
        "",
        "## 已生成产物",
    ]
    for key, value in sorted(result.items()):
        lines.append(f"- {key}：`{value}`")
    lines.extend([
        "",
        "## 验收命令",
        "- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q`",
        "- `PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py '<GPT链接>' --execute-absorption --workflow-package`",
    ])
    return "\n".join(lines) + "\n"


def build_workflow_automation_package(source: str, *, root: str | Path = "/root/sikk-gmgn", execute_absorption: bool = True) -> Dict[str, str]:
    """生成手机/TG 可用的一键工作流自动化包。

    该函数仍只写本地任务文件与知识资产，不启动真实交易、不签名、不广播。
    """
    root = Path(root)
    plan = build_task_router_plan(source, root=root)
    task_result = write_task_router_plan(source, root=root, execute_absorption=execute_absorption)
    workflow_dir = root / "tasks" / plan["slug"] / "workflow_automation"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    command = (
        "PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py "
        f"'{source}' --root /root/sikk-gmgn --execute-absorption --workflow-package"
    )
    package = {
        "工作流名称": "SIKK GPT 工作流自动化",
        "source": source,
        "slug": plan["slug"],
        "触发入口": {
            "Telegram自然语言": "工作流自动化 <GPT链接>",
            "本地CLI": "python3 sikk_her_task_router.py <GPT链接> --execute-absorption --workflow-package",
        },
        "自动执行": {
            "task_router": True,
            "section_task": True,
            "knowledge_absorption": bool(execute_absorption),
            "acceptance_report": True,
        },
        "安全边界": SAFETY_BOUNDARY,
        "本地一键命令": command,
        "产物": task_result,
    }

    package_json = workflow_dir / "WORKFLOW_AUTOMATION_PACKAGE.json"
    command_md = workflow_dir / "MOBILE_COMMAND.md"
    shell_entry = workflow_dir / "run_workflow_automation.sh"
    report_md = root / "reports" / plan["slug"] / "workflow_automation_acceptance.md"
    report_md.parent.mkdir(parents=True, exist_ok=True)

    task_result_with_package = dict(task_result)
    package_json.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    command_md.write_text(_render_workflow_command_md(source, plan, package), encoding="utf-8")
    shell_entry.write_text("#!/usr/bin/env bash\nset -euo pipefail\ncd /root/sikk-gmgn\n" + command + "\n", encoding="utf-8")
    shell_entry.chmod(0o755)

    final_result = {
        **task_result_with_package,
        "workflow_package_json": str(package_json),
        "mobile_command_md": str(command_md),
        "shell_entry": str(shell_entry),
        "workflow_report_md": str(report_md),
    }
    report_md.write_text(_render_workflow_report_md(source, plan, final_result), encoding="utf-8")
    return final_result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 SIKK HER 任务启动计划")
    parser.add_argument("source", help="GPT 链接、外部链接或普通任务目标")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--execute-absorption", action="store_true")
    parser.add_argument("--workflow-package", action="store_true", help="生成手机/TG 可用的一键工作流自动化包")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.workflow_package:
        result = build_workflow_automation_package(args.source, root=args.root, execute_absorption=args.execute_absorption)
    else:
        result = write_task_router_plan(args.source, root=args.root, output_dir=args.output_dir, execute_absorption=args.execute_absorption)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
