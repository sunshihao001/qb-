---
artifact_type: completion_verification_rule
status: verified
version: v2.0-stage8
generated_at: 2026-05-07T08:52:26Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 完成验证规则 V2.0 — 阶段 8

## 1. 完成定义
不是“文件复制完成”，而是“Hermes 能按 token 理解数据”。

## 2. 完成标准

```text
1. 已生成任务护照；
2. 已完成旧目录侦察；
3. 已完成文件语义分类；
4. 已建立 token 索引；
5. 已建立旧新路径映射；
6. 已复制或登记高价值旧数据；
7. 已建立字段字典；
8. 已建立数据护照；
9. 已建立 Hermes 读取入口；
10. 已抽样验证 3-5 个 token；
11. Hermes 能说明样本 token 的事实数据、结构证据、行为推断、handoff 数据和缺失项；
12. Hermes 能说明旧数据来源；
13. Hermes 能区分事实、证据、推断、交接；
14. 旧目录仍然保留；
15. 没有删除、移动、覆盖旧文件；
16. 没有修改业务代码；
17. 没有触发交易。
```

## 3. 通过条件

```text
- 任务护照存在
- token 级数据护照存在
- 旧路径映射存在
- 字段字典存在
- 抽样验证通过
- facts / evidence / inference / handoff 分层清晰
- old_path 与 new_path 可追溯
- 旧目录只读保留
```

## 4. 不通过条件

```text
- 只能说明复制完成，不能说明 token 数据状态
- 无法说清样本 token 的事实/证据/推断/交接
- 无法说明旧数据来源
- 旧目录被删除/移动/覆盖
- 业务代码被修改
- 触发交易
- 护照缺失或未验证
```

## 5. 验收原则

```text
完成标准必须由独立验证报告确认，系统自身不能自证完成。
```
