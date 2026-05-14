# Patch And Regression Loop

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 目标
处理 Wave 或 E2E 的 REJECTED 状态，形成可回放修复闭环。

## 输入
current_blocking_issues.json、对应 Wave audit、阶段 audit、pytest/replay 输出。

## 执行
读取 blocking → 定位阶段/文件 → patch_plan → 修改 → pytest → replay → handoff 验证 → regression_result → 重新解锁当前 Wave。

## 输出
- reports/system_audit/patch_plan.md
- reports/system_audit/regression_result.md
- updated runtime_task_state.json

## 状态
`PATCH_REGRESSION_READY | PATCH_REGRESSION_READY_WITH_GAPS | PATCH_REGRESSION_REJECTED`。

## 状态码 / missing / 阻断 / 降级 / 验收 补强
- 状态码: `PATCH_REGRESSION_READY`、`PATCH_REGRESSION_READY_WITH_GAPS`、`PATCH_REGRESSION_REJECTED`。
- missing: 修复计划必须列出未能定位的文件/证据为 `missing`，不得伪造。
- 阻断: blocking_issues 无法定位、pytest/replay 仍失败、handoff 不一致、hard negative 被覆盖时 REJECTED。
- 降级: 非关键 optional fixture 或外部上下文缺失可 READY_WITH_GAPS，但不得解锁后续 Wave 前隐藏。
- 验收: patch_plan、regression_result、对应 Wave audit、runtime/checkpoint 更新齐全。
