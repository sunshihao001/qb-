# 19_exec_policy — Execution Policy / Tool Schema / Permission Decisions

## 定位

HER V2.0+ 的执行策略层，负责工具 schema、权限裁决、sandbox policy 与工具账本。

## 主要文件

- `tool_schema_registry.jsonl`：工具 schema 注册。
- `exec_policy_rules.jsonl`：执行策略规则。
- `permission_decisions.jsonl`：权限裁决记录。
- `tool_ledger.jsonl`：工具调用账本。
- `sandbox_policy.md`：沙箱/执行边界。

## 规则

执行叙事必须和工具账本一致；失败工具调用也必须记录 outcome，不允许只记录成功路径。
