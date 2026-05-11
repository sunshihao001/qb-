---
artifact_type: audit_policy
status: verified
version: v1.1
valid_until: null
---
# Surface Completion Audit Policy

## Purpose
Prevent Hermes from doing surface engineering: writing files, making directories, or claiming completion without runtime integration and verification.

## Must audit
- 是否只写了文档没执行
- 是否只建了目录没接入
- 是否状态文件没有更新
- 是否验证报告为空或 pending
- 是否绕过任务护照
- 是否绕过权限规则
- 是否把失败伪装成完成
- 是否把候选记忆直接写成 verified

## Minimum pass conditions
A task cannot be DONE unless:
- `active_task_state.json` exists and is valid JSON
- final or verification report exists
- surface audit returns `surface_completion_risk=false`
- key artifacts are linked from state/report
- recovery path exists when any phase fails

## DENY condition
If surface audit reports findings, final status must not be `DONE` until resolved or explicitly accepted by user.
