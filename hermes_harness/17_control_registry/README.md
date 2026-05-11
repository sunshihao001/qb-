# 17_control_registry — V2.0 显式控制注册表

## 定位

这里是 HER V2.0+ 的 canonical control registry layer。它负责把控制规则显式登记为可审计条目，而不是散落在自然语言里。

## Canonical 文件

- `control_registry.jsonl`：当前唯一 canonical registry。
- `precedence_policy.md`：规则优先级。
- `rule_scope_map.md`：规则作用域。
- `rule_conflict_report.md`：冲突记录。

## 命名兼容说明

历史讨论中可能出现 `rule_registry.jsonl` 这个名字。当前系统不使用它作为 canonical 文件。

```text
canonical_registry = 17_control_registry/control_registry.jsonl
legacy_name = rule_registry.jsonl
compatibility_action = document_only_do_not_duplicate
```

不要复制一份 `rule_registry.jsonl`，避免两个 registry 漂移。
