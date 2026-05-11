---
artifact_type: memory_promotion_criteria
status: candidate
version: v2.0-stage10
generated_at: 2026-05-07T09:04:38Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Memory Promotion Criteria V2.0 — 阶段 10

## 1. 提升到长期记忆的条件

```text
1. 规则已经在控制面/模板/验证报告中稳定落地。
2. 规则已至少经过一次独立验证。
3. 规则不是一次性任务进度，而是可复用的稳定约束。
4. 规则不会和更高优先级用户指令冲突。
5. 规则不依赖临时路径、临时 token、临时样本。
6. 规则具有明确来源、适用范围、验证状态和失效条件。
```

## 2. 不应提升的条件

```text
- 仅是任务阶段进度
- 仅是未验证假设
- 仅适用于单次导入或单次目录
- 仍在恢复/冲突处理中
- 与后续阶段可能冲突
```

## 3. 提升前检查

```text
- source exists
- scope is stable
- validation_status is PASS or independently verified
- invalidation_condition is defined
- no contradiction with existing memory
```
