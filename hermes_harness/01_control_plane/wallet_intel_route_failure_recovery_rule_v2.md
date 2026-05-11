---
artifact_type: routing_failure_recovery_rule
status: verified
version: v2.0-stage1
generated_at: 2026-05-07T05:48:09Z
related_task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 路由失败恢复规则 V2.0 — 阶段 1

## 1. 目标
当 Hermes 未能正确识别 Wallet-Intel 钱包数据语义整合任务，或错误地按普通目录整理处理时，必须进入恢复流程。

## 2. 路由失败类型

### F1：漏判 Wallet-Intel
表现：输入包含触发关键词，但没有路由到：

```text
wallet_intel_semantic_integration
```

### F2：误按普通目录整理
表现：任务涉及钱包数据、结构分析、旧目录导入、字段字典、数据护照、handoff 等，但 Hermes 直接进入普通目录治理或文件整理。

### F3：未生成任务护照
表现：命中 Wallet-Intel 任务后，直接扫描/读取/写入，没有先生成任务护照。

### F4：越权执行
表现：在未授权情况下扫描旧数据目录、复制旧数据、移动旧目录、删除旧目录、覆盖旧文件、修改业务代码或触发交易。

### F5：语义层混淆
表现：把钱包事实、结构证据、行为推断、结论、handoff 混在同一层处理。

## 3. 恢复动作
一旦发现 F1-F5 任一情况，必须执行：

```text
1. 立即停止当前执行。
2. 不继续扫描旧目录。
3. 不复制、不移动、不删除、不覆盖任何旧文件。
4. 写入 route_failure_recovery_note。
5. 重新判定关键词。
6. 将 task_type 改为 wallet_intel_semantic_integration。
7. 读取 wallet_intel_semantic_integration.workflow.md。
8. 生成或修正任务护照。
9. 从 Wallet-Intel 语义分层重新开始。
```

## 4. 恢复输出合同
恢复报告必须包含：

```text
failure_type: F1|F2|F3|F4|F5
original_route: <错误路由>
corrected_route: wallet_intel_semantic_integration
matched_keywords: [...]
unsafe_actions_started: true|false
unsafe_actions_stopped: true|false
files_changed_before_recovery: [...]
rollback_required: true|false
next_required_workflow: 11_workflows/wallet_intel_semantic_integration.workflow.md
```

## 5. 禁止自我掩盖
不得把路由失败隐藏在最终总结里。必须在报告中明确写出：

```text
曾经发生路由失败；
失败类型是什么；
是否产生副作用；
如何恢复；
恢复后从哪个阶段重新开始。
```

## 6. 通过标准
恢复完成后必须满足：

```text
task_type = wallet_intel_semantic_integration
已读取专用 workflow
已生成任务护照
未继续普通目录整理路径
未发生未授权旧数据扫描/复制/移动/删除/覆盖
```
