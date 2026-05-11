---
artifact_type: route_failure_recovery_note
status: recovery_active
generated_at: 2026-05-07T23:00:33Z
failure_type: F1|F3|F5
original_route: ad_hoc_engineering_execution + legacy one-shot workflow expansion
corrected_route: wallet_intel_semantic_integration
related_workflow: hermes_harness/11_workflows/wallet_intel_semantic_integration.workflow.md
---
# HER Runtime Route Failure Recovery Note — 2026-05-07

## 1. 结论

本轮确实发生了 HER 底层运行偏离。不是 repo 里的 HER 设计文件被删除或物理污染，而是执行过程没有严格按 HER/Hermes Harness 控制面运行。

主要表现：

- 未先生成本轮任务护照就进入实现。
- 钱包结构任务未第一时间路由到 `wallet_intel_semantic_integration`。
- 将 GMGN/OKX 接入先做成了偏独立的 `sikk_sol_full_auto_workflow.py` one-shot 路线，形成并行系统倾向。
- 后续虽然纠正为 canonical 钱包结构系统，但恢复记录没有及时写入 HER runtime。
- 语义层一度混淆：collector / StageOutput / wallet_structure_gate / state_machine 的主从关系没有先由控制面裁定。

## 2. 失败类型判定

```text
failure_type: F1|F3|F5
```

- F1：漏判 Wallet-Intel / 钱包结构分析专用路由。
- F3：未生成任务护照，直接扫描/实现/测试。
- F5：语义层混淆，把兼容 one-shot workflow 与 canonical 钱包结构系统主路线混在一起。

未确认发生：

- F4 越权旧数据迁移：未移动、删除旧目录；未读取私钥/API key；未触发交易。

## 3. 副作用清单

已发生文件修改：

```text
modules/source_wallet_bot/gmgn_okx_readonly_adapter.py
sikk_candidate_wallet_structure_pipeline.py
sikk_sol_full_auto_workflow.py
tests/test_sikk_candidate_wallet_structure_pipeline.py
tests/test_sikk_gmgn_okx_readonly_adapter.py
tests/test_sikk_sol_full_auto_workflow.py
```

副作用性质：

- `gmgn_okx_readonly_adapter.py`：有效，作为 canonical source_wallet_bot 数据源保留。
- `sikk_candidate_wallet_structure_pipeline.py`：有效，接入原钱包结构 pipeline。
- `sikk_sol_full_auto_workflow.py`：保留为 legacy/compat one-shot 路线，不作为主入口继续扩展。
- tests：有效，用于防止兼容路线冒充主入口。

## 4. 恢复决策

```text
corrected_route: wallet_intel_semantic_integration
next_required_workflow: hermes_harness/11_workflows/wallet_intel_semantic_integration.workflow.md
unsafe_actions_started: false
unsafe_actions_stopped: true
rollback_required: false
```

不执行 rollback，原因：

1. 已改代码中有一部分已经恢复到正确主线：`source_wallet_bot + wallet_structure_pipeline + wallet_structure_gate`。
2. `sikk_sol_full_auto_workflow.py` 已标记为 compatibility route，不删除旧兼容入口。
3. 未发生破坏性旧数据迁移、删除、覆盖或交易动作。

## 5. 立即恢复规则

从本报告之后，涉及钱包结构 / Wallet-Intel / source_wallet_bot / 结构分析 / 数据护照 / 字段字典 / handoff 的任务必须：

```text
1. 先读 hermes_harness/01_control_plane/task_routing_policy.md
2. 命中 wallet_intel_semantic_integration
3. 生成任务护照
4. 读取 hermes_harness/11_workflows/wallet_intel_semantic_integration.workflow.md
5. 区分事实 / 证据 / 推断 / 结论 / handoff
6. 主路线固定为 modules/source_wallet_bot → sikk_candidate_wallet_structure_pipeline.py → sikk_wallet_structure_gate.py
7. 任何 one-shot/full_auto 只能作为兼容路线，不得作为主系统扩展
8. 完成前必须生成验证报告或至少写入 verification note
```

## 6. 禁止继续掩盖

后续报告中必须明确说明：

```text
曾发生一次 HER runtime 路由偏离；
已经纠正为 wallet_intel_semantic_integration；
sikk_sol_full_auto_workflow.py 只保留为 legacy compatibility route；
canonical 主系统仍是既有钱包结构分析系统。
```
