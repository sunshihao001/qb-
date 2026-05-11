---
artifact_type: semantic_layer_boundary_spec
status: verified
version: v2.0-stage3
generated_at: 2026-05-07T05:59:20Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 事实 / 证据 / 推断 / 交接边界说明 V2.0 — 阶段 3

## 1. 核心边界

```text
事实 = 发生了什么。
证据 = 哪些事实组合后支持某种结构可能性。
推断 = 这些证据可能意味着什么。
交接 = 后续模块基于当前判断应该读取什么，但不是交易指令。
```

## 2. 钱包事实层边界

允许写：

```text
钱包 A 在 T 时刻买入 X。
钱包 A 在 T 时刻卖出 Y。
钱包 A 当前持仓 Z。
钱包 A 的资金来源状态为资金待查。
钱包 A 进入 Top Holder 第 N 位。
钱包 A 收到 Token 转入。
```

禁止写：

```text
钱包 A 是执行组。
钱包 A 是控筹钱包。
钱包 A 正在派发。
钱包 A 有二次扩张动机。
```

## 3. 结构证据层边界

允许写：

```text
钱包 A/B/C 在 W1 同步买入，金额接近，形成同步执行候选证据 E2。
钱包 A/B/C 的资金来源存在相同上游，形成资金同源候选证据 E4。
多个 Top Holder 持仓稳定，形成结构持仓证据 E3。
```

禁止写：

```text
钱包 A/B/C 确定同源。
这些钱包确定一个团队。
Top Holder 稳定 = 确认控盘。
```

## 4. 行为推断层边界

允许写：

```text
当前证据支持“疑似早期执行组候选”，证据等级 E3，不确定性：资金来源未完全确认。
当前证据支持“疑似派发风险观察”，反向证据：关键 Top Holder 尚未明显下降。
当前证据不足以判断二次扩张动机，仅保留观察。
```

禁止写：

```text
确定控盘。
确定派发。
马上二拉。
必涨。
可以跟。
```

## 5. 策略交接层边界

允许写：

```text
handoff_to: paper_gate
suggested_action: WATCH
reason_refs: fact_001, evidence_003, inference_002
action_boundary: 仅 paper/observe，不代表真实买入
invalidation_conditions: 关键早期钱包集中卖出、Top Holder 快速下降
```

禁止写：

```text
因为 SUPPORT 所以买入。
因为 BLOCK 所以卖出。
handoff 单独触发真实交易。
跳过 quote/security/人工确认。
```

## 6. 污染防止规则

```text
事实层不得引用 inference_id 作为事实依据。
证据层必须引用 fact_id 或 raw_unit_ref。
推断层必须引用 fact_id/evidence_id，并写 uncertainty。
交接层必须引用 inference_id/fact_id/evidence_id，并写 action_boundary。
历史推断只能作为 historical_inference，不能变成 current_fact。
```

## 7. 验证问题
每次导入后验证必须抽样回答：

```text
这个 token 哪些是事实？
哪些是结构证据？
哪些是行为推断？
哪些是策略交接？
每个推断引用了哪些事实/证据？
handoff 是否声明不能作为买入依据？
当前缺什么事实或证据？
```
