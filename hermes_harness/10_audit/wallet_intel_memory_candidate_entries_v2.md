---
artifact_type: memory_candidate_entries
status: candidate
version: v2.0-stage10
generated_at: 2026-05-07T09:04:38Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Memory Candidate Entries V2.0 — 阶段 10

## 原则
本文件仅写入 candidate，不直接写长期记忆。
所有候选记忆必须带来源、适用范围、验证状态和失效条件。
本任务结束前只能写入 candidate，不得直接标记 verified。

## 候选记忆条目

### 1
- content: Wallet-Intel 任务必须路由到 wallet_intel_semantic_integration。
- source: wallet_intel_task_routing_rule_v2.md / wallet_intel_workflow_call_guide.md
- scope: Hermes 任务路由
- validation_status: candidate
- invalidation_condition: routing policy changes or task_type renamed

### 2
- content: Wallet-Intel 数据必须按语义分层，不按旧目录名分类。
- source: wallet_intel_data_layering_rule_v2.md / wallet_intel_layer_boundary_spec_v2.md
- scope: Wallet-Intel data organization
- validation_status: candidate
- invalidation_condition: new layering model supersedes four-layer design

### 3
- content: 钱包事实层、结构证据层、行为推断层、策略交接层必须分开。
- source: wallet_intel_data_layering_rule_v2.md / wallet_intel_data_contracts_rule_v2.md
- scope: Wallet-Intel analysis outputs
- validation_status: candidate
- invalidation_condition: layer taxonomy changes

### 4
- content: 旧目录默认保留为只读参考。
- source: wallet_intel_legacy_directory_compatibility_rule_v2.md / wallet_intel_compat_read_priority_rule_v2.md
- scope: legacy wallet data handling
- validation_status: candidate
- invalidation_condition: legacy retention policy changes

### 5
- content: 高价值旧数据可以复制导入，但必须保留旧新路径映射。
- source: wallet_intel_legacy_directory_compatibility_rule_v2.md / wallet_intel_legacy_path_mapping_template_v2.md
- scope: copy-only import of legacy wallet data
- validation_status: candidate
- invalidation_condition: copy-only policy is revoked

### 6
- content: 每个 token 必须有数据护照。
- source: wallet_intel_data_passport_rule_v2.md / wallet_intel_token_level_verification_requirement_v2.md
- scope: token-level wallet integration
- validation_status: candidate
- invalidation_condition: passport requirement changes

### 7
- content: 字段字典必须区分事实字段和推断字段。
- source: wallet_intel_field_dictionary_rule_v2.md / wallet_intel_field_risk_boundary_v2.md
- scope: wallet field schema governance
- validation_status: candidate
- invalidation_condition: field taxonomy is revised

### 8
- content: 完成标准是 Hermes 能按 token 理解数据，而不是文件复制完成。
- source: wallet_intel_completion_verification_rule_v2.md / wallet_intel_stage8_completion_verification.md
- scope: Wallet-Intel completion definition
- validation_status: candidate
- invalidation_condition: completion definition changes

### 9
- content: 推断结论不能写成确定事实。
- source: wallet_intel_data_layering_rule_v2.md / wallet_intel_layer_boundary_spec_v2.md / wallet_intel_data_passport_rule_v2.md
- scope: inference writing discipline
- validation_status: candidate
- invalidation_condition: inference/ तथ्य boundary policy changes

### 10
- content: 策略交接字段不能单独作为买入依据。
- source: wallet_intel_data_contract_risk_boundary_v2.md / wallet_intel_field_risk_boundary_v2.md / wallet_intel_completion_verification_rule_v2.md
- scope: downstream wallet decision support
- validation_status: candidate
- invalidation_condition: handoff policy changes
