---
artifact_type: data_passport_rule
status: verified
version: v2.0-stage6
generated_at: 2026-05-07T08:44:02Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 数据护照规则 V2.0 — 阶段 6

## 1. 目标
规定每个 token 必须生成数据护照，否则不算完成整合。

## 2. 强制规则

```text
1. 没有数据护照的 token，不允许标记为已完成整合。
2. 数据护照必须明确区分已有数据和缺失数据。
3. 数据护照必须说明哪些结论只是推断。
4. 数据护照必须能让 Hermes 直接理解这个 token 的数据状态。
5. 数据护照不是总结文案，而是状态契约。
```

## 3. 必含字段

```text
token 地址
data_source_old_paths
current_standard_paths
existing_wallet_facts
existing_structure_evidence
existing_behavior_inference
existing_handoff_data
missing_data
data_confidence
fact_vs_inference_boundary
followup_reading_suggestion
usable_for_followup_analysis
needs_additional_collection
```

## 4. 规则说明

- `data_source_old_paths` 必须记录所有旧路径来源。
- `current_standard_paths` 必须记录当前标准体系路径。
- `existing_*` 与 `missing_data` 必须分开列出，不能混写。
- `fact_vs_inference_boundary` 必须明确哪些内容是事实、哪些只是推断。
- `usable_for_followup_analysis` 必须写明 yes/no 与原因。
- `needs_additional_collection` 必须写明是否需要继续采集。

## 5. 禁止

```text
禁止把未完成 token 标记为已完成。
禁止把推断结论写成事实结论。
禁止把缺失项隐藏在备注里。
禁止不写 old_path 只写 new_path。
禁止跳过数据护照直接进入最终整合完成。
```

## 6. 完成标准

```text
仅当 token 护照存在、字段完整、事实/推断边界明确、缺失项明确、验证通过时，token 才能被视为已完成整合候选。
```
