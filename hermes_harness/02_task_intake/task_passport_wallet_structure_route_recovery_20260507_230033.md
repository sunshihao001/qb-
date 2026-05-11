---
artifact_type: task_passport
status: active_recovery
created_at: 2026-05-07T23:00:33Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 当前任务护照 — HER Runtime 路由恢复 / 钱包结构系统主路线纠偏

## original_goal
用户指出：HER 底层系统设计可能被污染，当前执行没有按照既有 HER/Hermes Harness 控制面走。

## real_intent
确认并纠正执行路线：钱包结构分析必须进入既有 Wallet-Intel / source_wallet_bot / wallet_structure_pipeline 主系统，不得另起并行系统；`sikk_sol_full_auto_workflow.py` 仅保留为兼容路线。

## task_type
```text
wallet_intel_semantic_integration
```

## matched_keywords
```text
HER底层系统
钱包结构分析系统
完善那套系统
兼容路线
污染
不按照那个来走
```

## involved_systems
```text
hermes_harness/01_control_plane/task_routing_policy.md
hermes_harness/01_control_plane/wallet_intel_task_routing_rule_v2.md
hermes_harness/01_control_plane/wallet_intel_route_failure_recovery_rule_v2.md
hermes_harness/11_workflows/wallet_intel_semantic_integration.workflow.md
modules/source_wallet_bot/
sikk_candidate_wallet_structure_pipeline.py
sikk_wallet_structure_gate.py
sikk_sol_full_auto_workflow.py
```

## canonical_route
```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

## compatibility_route
```text
sikk_sol_full_auto_workflow.py = legacy_compat_one_shot
```

## boundaries

允许：

- 只读检查 HER control plane。
- 写入本次 route failure recovery note。
- 写入当前恢复任务护照。
- 保留兼容路线标记。
- 后续把 GMGN/OKX collector 能力接入 canonical 钱包结构系统。

禁止：

- 删除旧目录。
- 移动旧数据。
- 覆盖旧任务包。
- 读取或输出 secret/API key/private key/token。
- 触发真实交易、签名、broadcast。
- 将 `sikk_sol_full_auto_workflow.py` 扩展成第二套主系统。
- 不经验证声称 HER 已完全恢复。

## verification_method

- 读取恢复报告文件是否存在。
- 检查恢复报告包含 failure_type / corrected_route / rollback_required / next_required_workflow。
- 检查任务护照包含 task_type / canonical_route / compatibility_route / boundaries。
- 后续代码改动必须跑对应测试。

## next_route

```text
读取 wallet_intel_semantic_integration.workflow.md
→ 按阶段 0 任务护照开始
→ 后续钱包结构改动只走 canonical_route
```
