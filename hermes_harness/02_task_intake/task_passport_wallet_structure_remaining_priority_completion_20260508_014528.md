---
artifact_type: task_passport
status: active
generated_at: 2026-05-08T01:45:28Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 任务护照 — 钱包结构系统剩余补全优先级与补全

## user_goal
用户要求：先列出需要补全的优先级，然后补全。

## priority_decision

### P0 — 审计器状态校准
当前 `sikk_wallet_structure_system_audit.py` 仍静态报告：

```text
LONG_RUNNING_AUTO_RUNNER
ACCEPTANCE_NOT_IN_PIPELINE_MANIFEST
WALLET_GUARD_SYSTEM_WIDE_INDEX
```

但这三项已经在 auto runner 中补入。最高优先级是让审计器动态检测实际代码锚点，避免系统长期显示 false gap。

### P1 — acceptance / guard / resume 动态锚点
审计器必须检查：

```text
run_wallet_structure_auto_task
validate_source_wallet_design_package
acceptance_status
wallet_data_guard_trend_index
resume / --resume
```

命中则标记 resolved，不再当未补全项。

### P2 — 全自动流程再次验证
补完后跑 pytest、审计器、auto runner smoke，确认 `overall_status` 从 `NEEDS_COMPLETION` 转为 `PASS` 或只剩真实未补项。

## allowed_changes
- 修改 `sikk_wallet_structure_system_audit.py`。
- 修改 `tests/test_sikk_wallet_structure_auto_runner.py`。
- 写 HER 验证报告。

## forbidden
- 不创建新钱包主系统。
- 不执行真实 swap/sign/broadcast。
- 不读取/输出 secret。
