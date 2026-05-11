---
artifact_type: verification_failure_recovery_rule
status: verified
version: v2.0-stage8
generated_at: 2026-05-07T08:52:47Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 验证失败恢复规则 V2.0 — 阶段 8

## 1. 触发条件

```text
抽样验证 token 失败；
无法说明事实/证据/推断/交接；
无法追溯旧数据来源；
旧目录状态不明；
发现旧文件被删除、移动或覆盖；
发现业务代码被修改；
发现交易触发痕迹；
```

## 2. 恢复规则

### F1：token 护照缺失

```text
恢复动作：停止完成声明，回到阶段 8 数据护照生成。
输出：missing_passport_report。
```

### F2：旧路径映射缺失

```text
恢复动作：停止 fallback，回到阶段 6 旧新路径映射。
输出：trace_missing_report。
```

### F3：事实/证据/推断/交接混层

```text
恢复动作：回到阶段 4 数据分层归属判断，重写分层。
输出：layer_contamination_report。
```

### F4：无法说明样本 token

```text
恢复动作：重新生成 token 护照与读取入口。
输出：token_understanding_failure_report。
```

### F5：旧目录被破坏

```text
恢复动作：立即停止任务，记录 incident，不得继续整合。
输出：legacy_directory_integrity_incident。
```

### F6：业务代码被修改或触发交易

```text
恢复动作：立即停止任务，进入安全事故处理。
输出：safety_boundary_violation_report。
```

## 3. 禁止

```text
禁止在验证失败后仍声明完成。
禁止用“部分完成”掩盖 token 理解失败。
禁止跳过恢复继续最终报告。
禁止把文件复制成功当成整合成功。
```
