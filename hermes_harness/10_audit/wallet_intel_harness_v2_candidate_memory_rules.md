---
artifact_type: candidate_memory_rules
audit_status: candidate_only
version: v2.0
generated_at: 2026-05-07T05:40:28Z
---
# Wallet-Intel Harness V2.0 候选记忆规则

## 1. 目的
本文件记录 Wallet-Intel Harness V2.0 系统写入后，可候选进入长期记忆的规则。除非通过独立验证并在后续任务中证明稳定复用，否则不得直接写入长期记忆。

## 2. 候选规则

1. Wallet-Intel 数据整合任务必须路由到 `wallet_intel_semantic_integration`，不得按普通目录整理处理。
2. 钱包数据必须按语义分层：ingest、facts、evidence、inference、conclusion、handoff、reports、index。
3. 事实层可以直接引用；推断层必须带证据等级；结论层必须带反证条件和失效条件。
4. 旧目录默认保留，只读参考；高价值旧数据只能 copy-only 导入，不能移动。
5. 读取优先级为：新标准入口 → token 索引 → 数据护照 → 字段字典 → 旧路径映射 → 旧目录只读补查。
6. 导入完成标准是 Hermes 能按 token 理解数据，而不是文件复制完成。
7. 导入后必须抽样 3-5 个 token 做理解验证。
8. handoff 包必须说明下游读取、字段层级、缺失项和动作边界。
9. 未验证规则只能写入候选记忆，不能直接写长期记忆。

## 3. 暂不写入长期记忆的原因
- 本轮任务是系统写入，不做实际数据迁移。
- 尚未执行真实 token 抽样导入后验证。
- 规则已写入 Harness 控制面和 workflow，但仍需后续任务复用验证。

## 4. 可转正条件
满足以下条件后，才可将精简规则写入长期记忆：

```text
至少一次真实 Wallet-Intel 任务按该 workflow 成功执行；
生成导入后理解验证报告；
未出现推断污染事实、旧路径追溯失败、handoff 不可读等重大问题；
用户确认该流程作为长期规则稳定采用。
```
