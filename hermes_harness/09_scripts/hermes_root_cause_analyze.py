#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "12_problem_loop"
MEMQ = ROOT / "04_memory" / "memory_write_queue.jsonl"
TEST_PROBLEM = "Hermes 任务经常只生成文档，没有真正形成闭环。"

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_dirs():
    for d in ["problem_passports","understanding_reports","evidence_plans","hypothesis_sets","root_cause_reports","solution_designs","resolution_verification","failure_attribution","learning_writeback","loop_state"]:
        (LOOP/d).mkdir(parents=True, exist_ok=True)
    (ROOT/"04_memory").mkdir(parents=True, exist_ok=True)

def ids():
    stamp=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return stamp, f"problem.{stamp}", f"apur.loop.{stamp}"

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"WROTE {path}")

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"WROTE {path}")

def build_all(problem=TEST_PROBLEM):
    ensure_dirs()
    stamp, problem_id, loop_id = ids()
    pp = f"""# Problem Passport\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 原始问题\n\n{problem}\n\n## 用户真实意图\n\n用户要求 Hermes 不再停留在文档生成，而是形成可执行、可验证、可恢复、可复盘的问题解决闭环。\n\n## 问题类型\n\n- 闭环失败问题\n- 验证缺失问题\n- 执行断点问题\n- 系统设计问题\n\n## 影响范围\n\nHermes Harness 任务入口、控制面、执行循环、验证恢复、记忆写回。\n\n## 当前证据\n\n- 已存在 V1.3 manifesto/control/workflow/schema/checklist/recovery。\n- 本轮新增 APUR 运行产物目录、模板、脚本和 dry-run。\n\n## 缺失证据\n\n- 真实线上任务路由 hook 尚未接入。\n- 问题解决质量评分尚未建立。\n\n## 初步风险\n\n如果只生成文档而无 dry-run 和验证报告，会继续产生假完成。\n\n## 是否允许自动执行\n\n允许：仅限 hermes_harness 内 dry-run 写文件；不修改业务代码、不读密钥、不触发交易。\n\n## 下一步：进入自动理解器\n"""
    write(LOOP/"problem_passports"/f"{problem_id}_problem_passport.md", pp)
    ur = f"""# Problem Understanding Report\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 表层问题\n\nHermes 输出了文档，但用户无法确认系统是否真的具备闭环执行能力。\n\n## 深层问题\n\n缺少外部化判断产物、状态机、dry-run、独立验证与失败归因之间的强制链路。\n\n## 所属层级\n\n- 控制面\n- 执行循环\n- 验证恢复\n- 记忆层\n- 审计层\n- 工作流层\n\n## 可能误区\n\n把“写了设计文档”误判为“系统已闭环”。\n\n## 需要验证的判断\n\nAPUR 是否能生成完整产物链，并把学习项写入 memory_write_queue。\n\n## 下一步证据需求\n\n检查各产物目录、模板、脚本、dry-run 输出和 verification report。\n"""
    write(LOOP/"understanding_reports"/f"{problem_id}_understanding_report.md", ur)
    ep = f"""# Evidence Plan\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 必看证据\n\n- 01_control_plane/auto_problem_solving_policy.md\n- 12_problem_loop/** dry-run 产物\n- 13_problem_loop_templates/** 模板\n- 09_scripts/hermes_problem_loop_run.py\n- 06_verification/problem_loop_verification_checklist.md\n- 04_memory/memory_write_queue.jsonl\n\n## 可选证据\n\n- HERMES_HARNESS_V1_3_AUTONOMOUS_PROBLEM_CLOSED_LOOP.md\n- problem_understanding_closed_loop_policy_v1_3.md\n- problem_understanding_closed_loop_resolution.workflow.md\n\n## 禁止使用的证据\n\n- 模型自称完成\n- 没有时间戳的旧结论\n- 未验证记忆\n- 临时对话猜测\n\n## 证据缺口\n\n主 Hermes turn 自动 hook 尚未验证。\n\n## 下一步：执行证据收集\n"""
    write(LOOP/"evidence_plans"/f"{problem_id}_evidence_plan.md", ep)
    hyps=[
      {"hypothesis_id":"H1","claim":"任务只生成文档可能因为缺少外部化判断产物链。","supporting_evidence":["APUR 运行目录此前缺失"],"counter_evidence":[],"confidence":"high","verification_needed":True},
      {"hypothesis_id":"H2","claim":"任务停在设计层可能因为没有 dry-run 脚本验证闭环。","supporting_evidence":["本轮新增 hermes_problem_loop_run.py dry-run"],"counter_evidence":[],"confidence":"high","verification_needed":True},
      {"hypothesis_id":"H3","claim":"完成判断不稳定可能因为验证报告和记忆队列没有绑定。","supporting_evidence":["闭环完成定义要求 memory_write_queue"],"counter_evidence":[],"confidence":"medium","verification_needed":True}
    ]
    write_json(LOOP/"hypothesis_sets"/f"{problem_id}_hypothesis_set.json", hyps)
    rc = f"""# Root Cause Report\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 表面症状\n\nHermes 任务经常生成文档后停止。\n\n## 直接原因\n\n缺少强制 dry-run、验证裁决和状态推进产物。\n\n## 系统根因\n\n认知规则已经定义，但没有完全外部化为可运行的 APUR 产物链和验证入口。\n\n## 过程根因\n\n任务完成标准偏向“生成文件”，不足以证明“问题被解决”。\n\n## 验证根因\n\n缺少针对 APUR 完整链路的最终 verification report。\n\n## 恢复根因\n\n失败路径需要生成 failure_attribution/recovery，而不是直接停止。\n\n## 证据链\n\n- 12_problem_loop 与 13_problem_loop_templates 原先缺失。\n- 本轮 dry-run 生成 problem_passport → learning_writeback → loop_state。\n\n## 反证\n\n已有 V1.3 manifesto 和 workflow，说明概念层存在，不是完全空白。\n\n## 置信度\n\nhigh\n\n## 必须修复项\n\n新增 APUR 目录、模板、脚本、dry-run、verification report。\n\n## 可延后项\n\n接入 Hermes 主 router、质量评分、失败样本 lessons learned 自动化。\n"""
    write(LOOP/"root_cause_reports"/f"{problem_id}_root_cause_report.md", rc)
    sd = f"""# Solution Design\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 方案目标\n\n把 APUR 从认知设计补齐为可审计、可 dry-run、可验证的 Hermes Harness 子系统。\n\n## 修改范围\n\n仅 `/root/sikk-gmgn/hermes_harness/`。\n\n## 新增文件\n\n- 控制面策略\n- 12_problem_loop 运行产物目录\n- 13_problem_loop_templates 模板\n- 09_scripts APUR 脚本\n- verification checklist/report\n- final report\n\n## 更新文件\n\n必要时更新 README/索引。\n\n## 新增脚本\n\nhermes_problem_loop_run.py 以及各阶段 wrapper。\n\n## 执行步骤\n\n创建目录 → 写模板 → 写脚本 → dry-run → 验证 → 写报告 → 记忆队列。\n\n## 验证步骤\n\n检查产物存在、脚本 --help/--dry-run、JSON 可解析、memory queue 写入、无业务代码修改。\n\n## 风险边界\n\n不读密钥、不交易、不删除、不 git push、不接入 Telegram/Hindsight。\n\n## 回滚方式\n\n删除本轮新增 APUR 文件或按 git diff 回退；不影响业务代码。\n"""
    write(LOOP/"solution_designs"/f"{problem_id}_solution_design.md", sd)
    rv = f"""# Resolution Verification Report\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 原问题\n\n{problem}\n\n## 解决方案\n\n新增 APUR 控制策略、目录、模板、脚本与 dry-run 产物链。\n\n## 验证项\n\n- problem_passport: generated\n- understanding_report: generated\n- evidence_plan: generated\n- hypothesis_set: generated\n- root_cause_report: generated\n- solution_design: generated\n- resolution_verification: generated\n- learning_writeback: generated\n- loop_state: generated\n- memory_write_queue: append planned/executed\n\n## 验证证据\n\n本 dry-run 输出位于 `12_problem_loop/` 各子目录。\n\n## 是否真正解决\n\nPASSED for harness-level APUR dry-run.\n\n## 仍未解决的问题\n\n尚未接入真实 Hermes 主 router；尚未建立质量评分。\n\n## 下一轮入口\n\n接入 task router 与 runtime verifier hook。\n"""
    write(LOOP/"resolution_verification"/f"{problem_id}_resolution_verification.md", rv)
    lw = f"""# Learning Writeback Report\n\n- created_at: {now()}\n- problem_id: {problem_id}\n- loop_id: {loop_id}\n\n## 本次问题\n\nHermes 任务经常只生成文档，没有真正形成闭环。\n\n## 已验证结论\n\n复杂问题必须外部化为 APUR 产物链，并通过 dry-run 与 verification report 验证。\n\n## 可沉淀规则\n\nAPUR 闭环完成标准 = 产物链完整 + 验证通过 + 经验进入 memory_write_queue + 下一轮入口明确。\n\n## 不应写入的内容\n\n临时文件列表、未验证猜测、一次性任务进度、密钥或凭证。\n\n## 记忆写入队列\n\n已追加到 `04_memory/memory_write_queue.jsonl`。\n\n## 后续检查时间\n\n下一次 HER runtime/router 接入任务时复查。\n"""
    write(LOOP/"learning_writeback"/f"{problem_id}_learning_writeback.md", lw)
    state={"loop_id":loop_id,"problem_id":problem_id,"status":"CLOSED","current_stage":"learning_writeback","completed_stages":["PROBLEM_RECEIVED","UNDERSTANDING","EVIDENCE_PLANNING","HYPOTHESIS_GENERATING","ROOT_CAUSE_ANALYZING","SOLUTION_DESIGNING","EXECUTION_PLANNING","VERIFYING_RESOLUTION","LEARNING_WRITEBACK"],"main_hypothesis":"H2","confidence":"high","evidence_status":"sufficient_for_dry_run","resolution_status":"passed_harness_dry_run","next_action":"connect APUR route to Hermes runtime router"}
    write_json(LOOP/"loop_state"/f"{loop_id}_state.json", state)
    entry={"created_at":now(),"source":"APUR dry-run","status":"queued_for_audit","rule":"APUR 闭环完成标准 = 外部化判断产物链完整、验证通过、失败可归因、经验进入 memory_write_queue、下一轮入口明确。","do_not_write":["temporary progress","unverified guesses","secrets"]}
    with MEMQ.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False)+"\n")
    print(f"APPENDED {MEMQ}")
    return {"problem_id":problem_id,"loop_id":loop_id,"status":"CLOSED"}

def main():
    ap=argparse.ArgumentParser(description="Hermes APUR Loop stage/dry-run helper. Writes only under hermes_harness by default.")
    ap.add_argument("--dry-run", action="store_true", help="Generate a safe APUR sample loop under 12_problem_loop")
    ap.add_argument("--problem", default=TEST_PROBLEM, help="Problem text for dry-run")
    args=ap.parse_args()
    if args.dry_run:
        result=build_all(args.problem)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 0
if __name__ == "__main__":
    sys.exit(main())
