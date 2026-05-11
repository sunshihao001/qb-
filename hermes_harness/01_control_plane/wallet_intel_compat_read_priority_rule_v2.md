---
artifact_type: compatibility_read_priority_rule
status: verified
version: v2.0-stage7
generated_at: 2026-05-07T08:15:59Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 兼容读取优先级规则 V2.0 — 阶段 7

## 1. 读取优先级

```text
P0：新标准入口
P1：token 索引
P2：数据护照
P3：字段字典
P4：旧新路径映射
P5：旧目录只读 fallback
```

## 2. 标准读取流程

```text
先读取 new_standard_entry。
再读取 token_index。
再读取 token_data_passport。
再用 field_dictionary 解释字段。
如果新体系缺数据，读取 legacy_path_map。
只有 legacy_path_map 指向的旧路径允许只读补查。
补查结果必须写回缺失项或待复查记录，不能写回旧目录。
```

## 3. 禁止读取方式

```text
禁止对所有旧目录盲搜。
禁止跳过数据护照直接读旧目录。
禁止把旧目录作为默认入口。
禁止将 fallback 结果直接提升为事实，除非有 raw_ref / old_path / mapping_id。
```

## 4. fallback 条件
仅当满足以下条件时允许旧路径 fallback：

```text
新标准体系缺失目标字段或文件；
legacy_path_map 存在对应 mapping_id；
fallback_allowed = true；
旧路径风险等级不是 R3/R4；
读取目的为补查或验证，不是新任务写入。
```

## 5. fallback 输出要求

```text
fallback_source: old_path
mapping_id: map_xxx
reason: <为什么 fallback>
read_mode: readonly
result_status: found/missing/blocked
next_action: import_candidate / mark_missing / review_required
```
