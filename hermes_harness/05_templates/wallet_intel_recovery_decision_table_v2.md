---
artifact_type: recovery_decision_table
status: verified
version: v2.0-stage9
generated_at: 2026-05-07T09:01:42Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Recovery Decision Table V2.0 — 阶段 9

## 1. 决策表

```text
failure_type | 状态标记 | 处理动作 | 是否允许完成声明
legacy_directory_not_found | not_found | 记录缺失，继续任务 | 否
file_unknown | unknown | 进入未知文件候选池 | 否
token_unresolved | unresolved_token_candidates | 保留候选，等待验证 | 否
token_source_conflict | source_conflict | 合并索引，等待验证 | 否
new_path_name_conflict | conflict_candidates | 保留并列版本 | 否
field_undocumented | undocumented_field | 进入字段字典待补 | 否
legacy_compatibility_required | compatibility_required | 保留旧路径兼容层 | 否
sample_validation_failed | recovery_report_required | 回到验证阶段重检 | 否
```

## 2. 决策规则

```text
- not_found 只表示缺失，不表示删除。
- unknown 只表示未知，不进入核心层。
- unresolved_token_candidates 必须保留原始候选。
- source_conflict 必须保留全部来源。
- conflict_candidates 不能覆盖任何已存在文件。
- undocumented_field 只能进入待补字典。
- compatibility_required 不能被强行清除。
- recovery_report_required 不能跳过。
```

## 3. 使用边界

```text
此表用于恢复分流，不用于交易、评分或完成判定。
```
