---
artifact_type: workflow_call_guide
status: verified
version: v2.0-stage2
generated_at: 2026-05-07T05:53:01Z
workflow: wallet_intel_semantic_integration
---
# Wallet-Intel Workflow 调用说明 V2.0

## 1. 何时调用
当任务命中以下任一关键词或意图时，调用：

```text
wallet_intel_semantic_integration
```

关键词包括：钱包数据、钱包采集、钱包事实、钱包画像、钱包交易、结构分析、同源证据、筹码分析、主导侧行为、handoff、旧目录导入、数据整合、wallet intel、source wallet bot、intel bot、旧路径映射、字段字典、数据护照。

## 2. 调用前必须读取

```text
01_control_plane/wallet_intel_task_routing_rule_v2.md
01_control_plane/wallet_intel_route_failure_recovery_rule_v2.md
01_control_plane/wallet_intel_data_layering_rule_v2.md
01_control_plane/wallet_intel_layer_boundary_spec_v2.md
05_templates/wallet_intel_data_layer_judgement_table_v2.md
01_control_plane/wallet_intel_data_contracts_rule_v2.md
01_control_plane/wallet_intel_data_contract_risk_boundary_v2.md
05_templates/wallet_intel_module_read_contract_template_v2.md
01_control_plane/wallet_intel_data_passport_rule_v2.md
01_control_plane/wallet_intel_token_level_verification_requirement_v2.md
05_templates/wallet_intel_data_passport_template_v2.md
01_control_plane/wallet_intel_field_dictionary_rule_v2.md
01_control_plane/wallet_intel_field_risk_boundary_v2.md
05_templates/wallet_intel_field_dictionary_template_v2.md
01_control_plane/wallet_intel_legacy_directory_compatibility_rule_v2.md
01_control_plane/wallet_intel_compat_read_priority_rule_v2.md
01_control_plane/wallet_intel_legacy_directory_risk_classification_rule_v2.md
05_templates/wallet_intel_legacy_path_mapping_template_v2.md
01_control_plane/wallet_intel_completion_verification_rule_v2.md
01_control_plane/wallet_intel_verification_failure_recovery_rule_v2.md
05_templates/wallet_intel_sampling_verification_template_v2.md
01_control_plane/wallet_intel_recovery_policy_v2.md
05_templates/wallet_intel_recovery_decision_table_v2.md
05_templates/wallet_intel_conflict_handling_template_v2.md
10_audit/wallet_intel_memory_candidate_entries_v2.md
10_audit/wallet_intel_memory_promotion_criteria_v2.md
10_audit/wallet_intel_stale_memory_review_note_v2.md
06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md
06_verification/project_governance/wallet_intel_stage11_route_simulation_verification.md
05_templates/wallet_intel_workflow_phase_template.md
```

## 3. 最小调用合同

```text
task_type: wallet_intel_semantic_integration
scope: system_write | readonly_scout | copy_only_import | import_after_validation | full_semantic_integration
allowed_legacy_scan: true|false
allowed_copy: true|false
allowed_code_change: false by default
allowed_trade: false
target_token_scope: explicit list | sample | none
standard_entry_path:
legacy_mapping_path:
field_dictionary_path:
data_passport_path:
validation_report_path:
```

## 4. 阶段执行顺序
必须按阶段 0-12 顺序执行。若某阶段不适用，必须写明：

```text
status: SKIPPED
reason: <为什么不适用>
checkpoint: <仍需生成 checkpoint>
```

不得静默跳过阶段。

## 5. 恢复调用
如果发生路由失败、越权、混层、验证失败，立即调用：

```text
01_control_plane/wallet_intel_route_failure_recovery_rule_v2.md
```

恢复后从最近可信 checkpoint 继续，不得继续错误路由。

## 6. 完成声明
只有阶段 10 抽样验证和阶段 11 最终整合报告通过，才能声明本轮语义整合完成。系统写入类任务只能声明“workflow 写入完成”，不能声明“旧数据迁移完成”。
