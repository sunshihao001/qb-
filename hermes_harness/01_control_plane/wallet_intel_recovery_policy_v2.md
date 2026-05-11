---
artifact_type: recovery_policy
status: verified
version: v2.0-stage9
generated_at: 2026-05-07T09:01:22Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Recovery Policy V2.0 — 阶段 9

## 1. 目标
让 Hermes 遇到旧目录缺失、文件未知、token 冲突、字段不明时不会乱判断。

## 2. 恢复总原则

```text
1. 先记录状态，再决定动作。
2. 不删除、不覆盖、不强行迁移未知对象。
3. 任何冲突都进入候选区，不进入核心结论。
4. 恢复的目标是保留可追溯性，而不是立即“修好”所有问题。
5. 失败不等于终止；误判才是必须阻断的风险。
```

## 3. 失败类型与处理

### 3.1 旧目录不存在

```text
处理：记录 not_found，不中断任务。
状态：legacy_directory_not_found
动作：继续当前任务流，但标注缺失来源。
```

### 3.2 文件无法识别

```text
处理：标记 unknown，不删除、不复制到核心层。
状态：file_unknown
动作：进入未知文件候选池。
```

### 3.3 token 无法识别

```text
处理：进入 unresolved_token_candidates。
状态：token_unresolved
动作：等待后续索引或人工验证。
```

### 3.4 同一 token 多路径冲突

```text
处理：合并索引，标记 source_conflict，等待验证。
状态：token_source_conflict
动作：保留全部来源，不做单边裁决。
```

### 3.5 新路径已有同名文件

```text
处理：不覆盖，进入 conflict_candidates。
状态：new_path_name_conflict
动作：保留并列版本，等待裁决。
```

### 3.6 字段无法解释

```text
处理：标记 undocumented_field，进入字段字典待补。
状态：field_undocumented
动作：不擅自定义语义。
```

### 3.7 旧代码仍读取旧路径

```text
处理：标记 compatibility_required，不强行迁移。
状态：legacy_compatibility_required
动作：保留旧路径兼容层。
```

### 3.8 抽样验证失败

```text
处理：生成 recovery report，不允许标记完成。
状态：sample_validation_failed
动作：回到完成验证或数据护照阶段重检。
```

## 4. 禁止

```text
禁止把 unknown 当作已知。
禁止把 conflict 当作已解决。
禁止把 not_found 当作删除指令。
禁止因恢复而覆盖原始来源。
禁止未经验证就进入完成声明。
```
