---
artifact_type: legacy_directory_compatibility_rule
status: verified
version: v2.0-stage7
generated_at: 2026-05-07T08:15:59Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 旧目录兼容规则 V2.0 — 阶段 7

## 1. 目标
防止 Wallet-Intel 旧目录被破坏，同时支持新标准体系优先读取。旧目录是历史证据来源和兼容 fallback，不是新任务默认写入位置。

## 2. 硬规则

```text
1. 旧目录默认保留。
2. 旧目录默认只读。
3. 不直接删除旧目录。
4. 不直接移动旧目录。
5. 不覆盖旧文件。
6. 高价值数据只允许复制导入。
7. 复制后必须记录旧路径和新路径映射。
8. 新任务优先读取新标准体系。
9. 新标准体系缺数据时，再通过旧路径映射补查。
10. 如果旧路径仍被代码调用，标记为 compatibility_required。
11. 旧目录不能继续作为新任务默认写入位置。
12. 所有旧路径处理必须可回溯。
```

## 3. 旧目录定位

```text
legacy_directory = historical_reference_only
write_policy = read_only_by_default
migration_policy = copy_only_if_authorized
fallback_policy = mapping_based_lookup_only
```

## 4. 允许动作

```text
只读列出已授权旧目录
读取必要元数据
登记候选旧路径
登记 compatibility_required
copy-only 导入高价值数据
生成 old_path -> new_path 映射
通过映射进行补查
```

## 5. 禁止动作

```text
删除旧目录
移动旧目录
覆盖旧文件
把旧目录作为新任务默认写入位置
未授权批量扫描旧数据
未授权复制旧数据
绕过旧新路径映射直接读旧路径
把 fallback 当成默认入口
```

## 6. compatibility_required 标记
当发现旧路径仍被代码、脚本、dashboard、reader、报告生成器或历史索引调用时，必须标记：

```text
compatibility_status: compatibility_required
reason: <仍被哪个模块调用>
legacy_path: <旧路径>
required_until: <替换完成或 reader fallback 完成>
replacement_target: <新标准路径>
```

## 7. 完成标准
旧目录兼容处理必须能回答：

```text
哪些旧目录仍存在？
哪些旧路径被映射到新路径？
哪些旧路径只做 fallback？
哪些旧路径仍被代码调用？
哪些旧目录禁止写入？
任一新数据能否追溯 old_path？
```
