import json
from pathlib import Path


def test_build_her_task_router_plan_classifies_chatgpt_share_and_preserves_safety():
    from sikk_her_task_router import build_task_router_plan

    plan = build_task_router_plan(
        "https://chatgpt.com/share/69f83af2-a380-83a7-a429-200c72d43279",
        root="/root/sikk-gmgn",
    )

    assert plan["task_type"] == "chatgpt_share"
    assert plan["source"] == "https://chatgpt.com/share/69f83af2-a380-83a7-a429-200c72d43279"
    assert plan["safety_boundary"]["paper_only"] is True
    assert plan["safety_boundary"]["real_swap_enabled"] is False
    assert plan["safety_boundary"]["private_key_required"] is False
    assert plan["safety_boundary"]["signing_enabled"] is False
    assert plan["safety_boundary"]["broadcast_enabled"] is False
    assert plan["recommended_skills"][0] == "conversation-transcript-ingestion"
    assert "sikk-sol-core-methodology" in plan["recommended_skills"]
    assert "任务棱镜" in plan["task_lens"][0]["中文名称"]
    assert any(route["工具"] == "sikk_knowledge_absorption.py" for route in plan["tool_routes"])
    assert any("knowledge/inbox" in item for item in plan["expected_outputs"])
    assert any("pytest" in check for check in plan["acceptance_checks"])


def test_write_her_task_router_can_execute_absorption_for_chatgpt_share(tmp_path):
    from sikk_her_task_router import write_task_router_plan

    result = write_task_router_plan(
        "https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426",
        root=tmp_path,
        output_dir=tmp_path / "tasks" / "chatgpt_share_69f809c6",
        execute_absorption=True,
    )

    assert Path(result["inbox"]).exists()
    assert Path(result["passport"]).exists()
    assert Path(result["rules"]).exists()
    assert Path(result["audit"]).exists()
    assert Path(result["system_update"]).exists()
    assert Path(result["skill"]).exists()
    assert Path(result["hindsight"]).exists()
    assert Path(result["acceptance_report"]).exists()
    acceptance = Path(result["acceptance_report"]).read_text(encoding="utf-8")
    assert "自动吸收" in acceptance
    assert "paper-only" in acceptance

    json_path = Path(result["task_router_json"])
    md_path = Path(result["task_router_md"])
    section_path = Path(result["section_task_md"])

    assert json_path.exists()
    assert md_path.exists()
    assert section_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["task_type"] == "chatgpt_share"
    assert payload["safety_boundary"]["real_swap_enabled"] is False
    assert "chatgpt_share_69f809c6" in payload["slug"]

    md = md_path.read_text(encoding="utf-8")
    assert "HER 任务启动器" in md
    assert "任务棱镜" in md
    assert "工具路由" in md
    assert "不执行真实 swap" in md

    section = section_path.read_text(encoding="utf-8")
    assert "Section Task" in section
    assert "读取相关文件" in section
    assert "测试命令" in section
    assert "验收标准" in section


def test_build_workflow_automation_package_creates_mobile_command_and_report(tmp_path):
    from sikk_her_task_router import build_workflow_automation_package

    result = build_workflow_automation_package(
        "https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426",
        root=tmp_path,
        execute_absorption=True,
    )

    package_json = Path(result["workflow_package_json"])
    command_md = Path(result["mobile_command_md"])
    report_md = Path(result["workflow_report_md"])
    shell_path = Path(result["shell_entry"])

    assert package_json.exists()
    assert command_md.exists()
    assert report_md.exists()
    assert shell_path.exists()

    package = json.loads(package_json.read_text(encoding="utf-8"))
    assert package["工作流名称"] == "SIKK GPT 工作流自动化"
    assert package["触发入口"]["Telegram自然语言"] == "工作流自动化 <GPT链接>"
    assert package["安全边界"]["paper_only"] is True
    assert package["安全边界"]["real_swap_enabled"] is False
    assert package["自动执行"]["knowledge_absorption"] is True
    assert "python3 sikk_her_task_router.py" in package["本地一键命令"]
    assert "--execute-absorption" in package["本地一键命令"]

    command_text = command_md.read_text(encoding="utf-8")
    assert "手机可用入口" in command_text
    assert "工作流自动化 https://chatgpt.com/share/69f809c6" in command_text
    assert "禁止真实交易" in command_text
    assert "无需 slash command" in command_text

    report = report_md.read_text(encoding="utf-8")
    assert "工作流自动化验收报告" in report
    assert "已生成" in report
    assert "paper-only" in report
