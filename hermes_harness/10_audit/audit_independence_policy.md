# Audit Independence Policy

## 用途
将审计层独立出来，防止审计被执行报告替代。

## 审计分类目录

```text
08_audit/
├── task_audit_reports/
├── memory_audit_reports/
├── permission_audit_reports/
├── surface_completion_audit/
└── stale_rule_audit/
```

## 重点审计
- 是否只写了文档没执行。
- 是否只建了目录没接入。
- 是否状态文件没有更新。
- 是否验证报告是空的。
- 是否绕过任务护照。
- 是否绕过权限规则。
- 是否把失败伪装成完成。
- 是否把候选记忆直接写成 verified。

## 规则
1. 审计报告必须独立于执行报告。
2. 审计失败不得宣布 DONE。
3. surface completion 必须进入补全或 recovery。
4. stale rule 必须进入记忆审计。
