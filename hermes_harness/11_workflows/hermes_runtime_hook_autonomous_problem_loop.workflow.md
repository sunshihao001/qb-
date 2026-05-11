---
artifact_type: workflow
version: v1.4
status: canonical
created_at: 2026-05-09T01:03:33Z
route: hermes_runtime_hook_autonomous_problem_loop
uses: problem_understanding_closed_loop_resolution
---
# Hermes Harness V1.4 Runtime Hook Workflow

## 输入
- user_request: 用户原始请求。
- task_context: 当前会话/项目/文件/历史摘要。
- risk_scope: 读写、执行、网络、凭证、安全边界。

## 阶段
1. `router_hook`：判定任务复杂度与 route。
2. `runtime_run_create`：生成 `runtime_run_id` 与目录。
3. `problem_passport_hook`：写入/引用 APUR problem passport。
4. `apur_execution_hook`：推进 V1.3 APUR 判断链。
5. `tool_ledger_hook`：记录关键工具调用。
6. `verification_hook`：执行独立验证。
7. `recovery_hook`：失败时生成 recovery report。
8. `learning_writeback_hook`：追加 memory queue 候选。
9. `completion_audit_hook`：生成 final report。

## 状态机
- `CREATED`
- `ROUTED`
- `APUR_RUNNING`
- `TOOLS_RECORDED`
- `VERIFICATION_RUNNING`
- `PASSED`
- `FAILED_RECOVERY_REQUIRED`
- `RECOVERY_REPORTED`
- `LEARNING_QUEUED`
- `COMPLETED`

## 输出
- `14_runtime_hooks/runtime_runs/<runtime_run_id>/runtime_state.json`
- `14_runtime_hooks/runtime_runs/<runtime_run_id>/tool_ledger.jsonl`
- `14_runtime_hooks/runtime_runs/<runtime_run_id>/runtime_completion_audit.md`
- `06_verification/verification_reports/HERMES_HARNESS_V1_4_RUNTIME_HOOK_VERIFICATION.md`
- `08_reports/final_reports/HERMES_HARNESS_V1_4_RUNTIME_HOOK_REPORT.md`
