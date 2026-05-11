---
artifact_type: sampling_verification_template
status: verified
version: v2.0-stage8
generated_at: 2026-05-07T08:52:47Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 抽样验证模板 V2.0 — 阶段 8

## 1. 抽样范围

```text
sample_size: 3-5 tokens
sample_method: representative | random | risk_based | mixed
```

## 2. 单 token 验证模板

```text
token_address:
token_symbol:
data_passport_path:
standard_entry_path:
legacy_mapping_path:
field_dictionary_path:

事实数据说明：
- wallet_facts:
- transaction_facts:
- top_holder_status:
- funding_source:

结构证据说明：
- same_source_evidence:
- candidate_group:
- funding_path:
- chip_distribution:
- evidence_level:
- fact_refs:

行为推断说明：
- dominant_side_status:
- lifecycle_state:
- distribution_state:
- uncertainty:
- inference_refs:

handoff 数据说明：
- handoff_package:
- wallet_structure_decision:
- allowed_downstream_modules:
- action_boundary:

缺失项说明：
- missing_facts:
- missing_evidence:
- missing_inference:
- missing_handoff:
- needs_additional_collection:

旧数据来源说明：
- old_paths:
- mapping_ids:
- copy_or_reference_status:

分层判断：
- facts/evidence/inference/handoff separated: PASS/FAIL
- inference_not_written_as_fact: PASS/FAIL
- handoff_not_trade_signal: PASS/FAIL

验证结论：PASS/FAIL
失败原因：
恢复动作：
```

## 3. 总体验证模板

```text
sample_count:
pass_count:
fail_count:
failed_tokens:
completion_status: complete_candidate | incomplete | recovery_required
summary:
```
