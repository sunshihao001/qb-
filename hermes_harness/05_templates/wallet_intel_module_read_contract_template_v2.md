---
artifact_type: module_read_contract_template
status: verified
version: v2.0-stage4
generated_at: 2026-05-07T08:39:07Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 模块读取契约模板 V2.0 — 阶段 4

## 使用场景
当某个模块要读取 Wallet-Intel 数据时，必须先声明读取契约。

## 模板字段

```text
module_name
module_role
allowed_contracts
forbidden_contracts
required_read_order
must_validate_fields
must_not_assume
fallback_policy
risk_boundary
output_usage
```

## 结构模板

```text
模块名称：<module_name>
模块角色：<module_role>
允许读取契约：<allowed_contracts>
禁止读取契约：<forbidden_contracts>
必须按顺序读取：<required_read_order>
必须验证字段：<must_validate_fields>
不可自行假设：<must_not_assume>
fallback 策略：<fallback_policy>
风险边界：<risk_boundary>
输出用途：<output_usage>
```

## 读取要求

```text
1. 先判断模块是否有权读取该契约。
2. 再判断该契约属于事实、证据、推断还是交接。
3. 若契约含推断字段，必须连带 uncertainty / evidence_refs 一起读取。
4. 若契约为交接包，不得把它当成交易信号。
5. 若契约缺失关键字段，必须标记 review_required。
```
