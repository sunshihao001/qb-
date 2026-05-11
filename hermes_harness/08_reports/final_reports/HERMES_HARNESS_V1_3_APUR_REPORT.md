# HERMES HARNESS V1.3 APUR REPORT

- created_at: 2026-05-09T00:57:38Z
- artifact_type: final_report
- version: v1.3-apur
- route: problem_understanding_closed_loop_resolution
- status: completed_for_harness_dry_run

## 新增模块

新增 `APUR Loop / Auto Problem Understanding & Resolution Loop`，中文名：自动问题理解与闭环解决模块。

定位：它不是业务执行器，而是 Hermes 的认知运行时模块，用于把复杂问题转成可审计的外部化判断产物链。

## 新增目录

- `12_problem_loop/problem_passports/`
- `12_problem_loop/understanding_reports/`
- `12_problem_loop/evidence_plans/`
- `12_problem_loop/hypothesis_sets/`
- `12_problem_loop/root_cause_reports/`
- `12_problem_loop/solution_designs/`
- `12_problem_loop/resolution_verification/`
- `12_problem_loop/failure_attribution/`
- `12_problem_loop/learning_writeback/`
- `12_problem_loop/loop_state/`
- `13_problem_loop_templates/`

## 新增模板

- `problem_passport_template.md`
- `understanding_report_template.md`
- `evidence_plan_template.md`
- `hypothesis_set_template.json`
- `root_cause_report_template.md`
- `solution_design_template.md`
- `resolution_verification_template.md`
- `failure_attribution_template.md`
- `learning_writeback_template.md`
- `problem_loop_state_template.json`

## 新增脚本

- `09_scripts/hermes_problem_intake.py`
- `09_scripts/hermes_problem_understand.py`
- `09_scripts/hermes_evidence_plan.py`
- `09_scripts/hermes_hypothesis_generate.py`
- `09_scripts/hermes_root_cause_analyze.py`
- `09_scripts/hermes_solution_design.py`
- `09_scripts/hermes_resolution_verify.py`
- `09_scripts/hermes_failure_attribution.py`
- `09_scripts/hermes_learning_writeback.py`
- `09_scripts/hermes_problem_loop_run.py`

所有脚本支持：

- `--help`
- `--dry-run`
- 默认只写 `hermes_harness/`
- 不删除文件
- 不修改业务代码
- 不读取密钥
- 不触发交易
- 错误时退出非 0
- 输出明确日志

## 自动问题理解流程

`problem_passport → understanding_report → evidence_plan → hypothesis_set → root_cause_report → solution_design → resolution_verification → failure_attribution / learning_writeback → loop_state`

## 闭环完成定义

APUR 闭环只有在以下条件满足时才允许标记 CLOSED：

1. 问题已结构化；
2. 证据已收集或缺口已记录；
3. 假设已生成并标注证据状态；
4. 根因已定位；
5. 方案已生成；
6. dry-run 或执行产物已生成；
7. 结果已验证；
8. 失败时有归因入口；
9. 经验进入 `04_memory/memory_write_queue.jsonl`；
10. 下一轮入口明确。

## dry-run 结果

测试问题：`Hermes 任务经常只生成文档，没有真正形成闭环。`

已生成：

- `12_problem_loop/problem_passports/problem.20260509_005854_problem_passport.md`
- `12_problem_loop/understanding_reports/problem.20260509_005854_understanding_report.md`
- `12_problem_loop/evidence_plans/problem.20260509_005854_evidence_plan.md`
- `12_problem_loop/hypothesis_sets/problem.20260509_005854_hypothesis_set.json`
- `12_problem_loop/root_cause_reports/problem.20260509_005854_root_cause_report.md`
- `12_problem_loop/solution_designs/problem.20260509_005854_solution_design.md`
- `12_problem_loop/resolution_verification/problem.20260509_005854_resolution_verification.md`
- `12_problem_loop/learning_writeback/problem.20260509_005854_learning_writeback.md`
- `12_problem_loop/loop_state/apur.loop.20260509_005854_state.json`

并已追加：

- `04_memory/memory_write_queue.jsonl`

## 未完成事项

- APUR 尚未接入 Hermes Agent 主 router / turn loop。
- 尚未建立问题解决质量评分。
- 尚未把失败样本自动转成 lessons learned。
- 失败路径脚本目前具备模板与 wrapper 能力，但本次 PASSED dry-run 未触发真实 failure_attribution 样本。

## 下一版本建议

V1.4 应进入 runtime hook 层：

- 接入 task router；
- 接入 runtime verifier hook；
- 接入 recovery hook；
- 接入 retrospective writeback hook；
- 给每个复杂任务自动分配 `problem_id` / `loop_id`；
- 建立 APUR quality score。
