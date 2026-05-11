---
artifact_type: data_passport_template
status: verified
version: v2.0-stage6
generated_at: 2026-05-07T08:44:02Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 数据护照模板 V2.0 — 阶段 6

## 模板字段

```text
token_address
old_paths
current_standard_paths
wallet_facts
structure_evidence
behavior_inference
handoff_data
missing_data
data_confidence
fact_boundary
inference_boundary
followup_reading_suggestion
usable_for_followup_analysis
needs_additional_collection
validation_status
validation_notes
```

## 结构模板

```text
Token 地址：<token_address>
旧路径来源：<old_paths>
当前标准路径：<current_standard_paths>
已有钱包事实数据：<wallet_facts>
已有结构证据数据：<structure_evidence>
已有行为推断数据：<behavior_inference>
已有 handoff 数据：<handoff_data>
缺失数据：<missing_data>
数据可信度：<data_confidence>
事实边界：<fact_boundary>
推断边界：<inference_boundary>
后续模块读取建议：<followup_reading_suggestion>
是否可用于后续分析：<usable_for_followup_analysis>
是否需要补充采集：<needs_additional_collection>
验证状态：<validation_status>
验证说明：<validation_notes>
```

## 约束

```text
wallet_facts 与 structure_evidence 必须分开。
behavior_inference 必须标注不确定性。
missing_data 必须明确列出。
old_paths 与 current_standard_paths 必须同时可见。
```
