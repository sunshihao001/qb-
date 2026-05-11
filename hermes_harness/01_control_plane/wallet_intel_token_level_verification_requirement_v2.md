---
artifact_type: token_level_verification_requirement
status: verified
version: v2.0-stage6
generated_at: 2026-05-07T08:44:02Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel token 级验证要求 V2.0 — 阶段 6

## 1. 验证目标
每个 token 必须通过 token 级验证，证明数据护照足以让 Hermes 理解其数据状态。

## 2. 验证检查项

```text
- token_address 存在且可唯一识别
- old_paths 与 current_standard_paths 同时存在或明确说明缺失
- wallet_facts / structure_evidence / behavior_inference / handoff_data 分栏清晰
- missing_data 与已有数据严格分开
- fact_boundary / inference_boundary 明确
- followup_reading_suggestion 可执行
- usable_for_followup_analysis 结论明确
- needs_additional_collection 明确
```

## 3. 验证方式

```text
1. 抽样读取 token 护照。
2. 追溯至少一个事实字段到来源。
3. 追溯至少一个证据字段到 fact_refs。
4. 检查至少一个推断字段是否写明 uncertainty。
5. 检查至少一个 handoff 是否不是交易信号。
6. 检查缺失项是否明确列出。
```

## 4. 不通过条件

```text
- 护照缺失
- 护照字段缺失
- 事实与推断混写
- old_path 未记录
- 缺失项未列出
- 将推断写成事实
- 将 handoff 当买入依据
```
