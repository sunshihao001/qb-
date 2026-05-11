---
artifact_type: field_dictionary_template
status: verified
version: v2.0-stage5
generated_at: 2026-05-07T06:03:18Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 字段字典模板 V2.0 — 阶段 5

用于生成每个 token / 数据集的字段字典。

## 1. 字段字典表模板

| 字段名 | 中文名称 | 字段类型 | 字段来源 | 字段用途 | 是否事实字段 | 是否推断字段 | 风险边界 | 后续模块如何使用 |
|---|---|---|---|---|---|---|---|---|
| field_name | 中文名称 | 事实字段/统计字段/结构证据字段/行为推断字段/策略交接字段 | source_path / raw_ref / upstream_module | 该字段用于什么 | 是/否 | 是/否 | 允许解释的边界与禁止误读 | 下游模块如何读取、是否可直接引用、是否需结合证据 |

## 2. 必填校验项

每个字段行必须至少写清：

```text
- 字段名
- 中文名称
- 字段类型
- 字段来源
- 字段用途
- 是否事实字段
- 是否推断字段
- 风险边界
- 后续模块如何使用
```

## 3. 字段分层示例

```text
wallet_address → 钱包地址 → 事实字段
buy_count → 买入次数 → 统计字段
same_source_group_id → 疑似同源组编号 → 结构证据字段
dominant_side_status → 主导侧状态 → 行为推断字段
wallet_structure_decision → 钱包结构门禁决策输入 → 策略交接字段
```

## 4. 输出建议

字段字典建议同时输出：

```text
field_dictionary.csv
field_dictionary.md
field_dictionary.json
unknown_fields_review.md
```
