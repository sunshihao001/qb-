---
artifact_type: control_plane_update_verification
status: PASS
generated_at: 2026-05-07T23:00:33Z
scope: HER bottom runtime correction for Wallet-Intel / SIKK wallet structure
---
# HER 底层规则修改验证记录 — Wallet-Intel / 钱包结构主路线纠偏

## 1. 修改目标

把用户纠正规则写入 HER 底层控制面，而不是只停留在聊天上下文：

```text
SIKK 钱包/Wallet-Intel 任务不得直接跳代码、跑数据或另建并行 workflow；
必须先 route → task_passport → wallet_intel_semantic_integration → 读取 workflow；
然后只修改既有 canonical 钱包结构系统；
sikk_sol_full_auto_workflow.py 仅为 legacy compatibility route。
```

## 2. 已修改文件

```text
hermes_harness/01_control_plane/hermes_constitution.md
hermes_harness/01_control_plane/task_routing_policy.md
hermes_harness/01_control_plane/wallet_intel_task_routing_rule_v2.md
```

## 3. 已写入长期记忆

长期记忆已更新为：

```text
HER/Hermes：目标护照、控制面、分阶段、独立验证、失败 recovery、验证后写记忆。SIKK 钱包/Wallet-Intel 强制 route→passport→wallet_intel_semantic_integration→读 workflow→改既有 canonical 钱包结构；不得跳代码或另建并行 workflow；sikk_sol_full_auto_workflow.py 仅 legacy compat。
```

同时删除了一个重复的 Hermes V1.2 cognition 记忆条目以释放记忆空间。

## 4. 必须存在的锚点

### hermes_constitution.md

```text
跳过控制面路由直接改代码、建 workflow 或跑数据
Wallet-Intel / 钱包结构强制底层规则
sikk_sol_full_auto_workflow.py 只能作为 legacy_compat_one_shot
```

### task_routing_policy.md

```text
Mandatory execution order for Wallet-Intel / wallet-structure work
Set route_decision = wallet_intel_semantic_integration
Execute only inside the existing canonical wallet structure system
sikk_sol_full_auto_workflow.py = legacy_compat_one_shot
```

### wallet_intel_task_routing_rule_v2.md

```text
不得直接跳代码或创建并行主系统
new_parallel_workflow
standalone_full_auto_wallet_system
modules/source_wallet_bot → sikk_candidate_wallet_structure_pipeline.py → sikk_wallet_structure_gate.py
```

## 5. 结论

```text
verification_status: PASS
bottom_rule_persisted: true
memory_updated: true
canonical_wallet_route_enforced: true
legacy_full_auto_demoted_to_compat: true
```
