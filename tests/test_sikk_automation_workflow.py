import json
from pathlib import Path


def test_build_workflow_plan_keeps_paper_only_boundaries_and_schedules():
    from sikk_automation_workflow import build_workflow_plan

    plan = build_workflow_plan(output_root="data/gmgn_candidates_live_run")

    assert plan["workflow_name"] == "SIKK-SOL HER 核心自动化工作流"
    assert plan["version"] == "her_core_automation_v1"
    assert "目标自治" in plan["cognitive_principle"]
    assert "GPT/ChatGPT 分享链接" in plan["tool_routing"]
    assert "Super Hermes prism-scan/prism-3way/prism-reflect" in plan["tool_routing"]["复杂代码/架构审计"]
    assert "repomix" in plan["tool_routing"]["跨模型代码库上下文包"]
    assert "DeerFlow" in plan["tool_routing"]["多小时研究/多代理任务"]
    assert plan["safety_boundary"]["paper_only"] is True
    assert plan["safety_boundary"]["real_swap_enabled"] is False
    assert plan["safety_boundary"]["private_key_required"] is False
    assert plan["safety_boundary"]["signing_enabled"] is False
    assert plan["safety_boundary"]["broadcast_enabled"] is False
    assert len(plan["schedules"]) == 3
    assert {job["job_id"] for job in plan["schedules"]} == {"candidate_signal_cycle", "paper_position_refresh", "daily_review"}
    assert any(job.get("interval_minutes") == 10 for job in plan["schedules"])
    assert any(job.get("interval_minutes") == 3 for job in plan["schedules"])
    assert any(job.get("cron") == "0 0 * * *" for job in plan["schedules"])
    assert [stage["stage_id"] for stage in plan["task_lens_stages"]] == [
        "lens_1_read",
        "lens_2_problem",
        "lens_3_map",
        "lens_4_execute",
        "lens_5_verify",
    ]
    assert plan["task_lens_stages"][0]["中文名称"] == "读取与证据保存"
    assert all("acceptance" in stage for stage in plan["task_lens_stages"])
    assert all("swap" not in job["command"].lower() for job in plan["schedules"])
    assert any("同一 token" in gate for gate in plan["gates"])


def test_write_workflow_plan_outputs_json_and_mobile_readable_md(tmp_path):
    from sikk_automation_workflow import write_workflow_plan

    paths = write_workflow_plan(output_root=tmp_path / "run")

    json_path = Path(paths["workflow_plan_json"])
    md_path = Path(paths["workflow_plan_md"])
    assert json_path.exists()
    assert md_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["safety_boundary"]["real_swap_enabled"] is False
    md = md_path.read_text(encoding="utf-8")
    assert "SIKK-SOL HER 核心自动化工作流计划" in md
    assert "任务棱镜阶段" in md
    assert "工具路由" in md
    assert "DeerFlow" in md
    assert "repomix" in md
    assert "prism" in md
    assert "不执行真实 swap" in md
    assert "每 10 分钟" in md
    assert "每 3 分钟" in md
    assert "cron `0 0 * * *`" in md
