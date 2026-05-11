---
artifact_type: workflow_phase_template
status: verified
version: v2.0-stage2
generated_at: 2026-05-07T05:53:01Z
workflow: wallet_intel_semantic_integration
---
# Wallet-Intel 每阶段模板 V2.0

用于为阶段 0-12 生成标准阶段记录。每个阶段必须完整填写，不允许只写“已完成”。

```markdown
# Wallet-Intel 阶段 <N>：<阶段名称>

## 1. 阶段目标

## 2. 输入
- input_artifacts:
- source_paths:
- authorization_scope:

## 3. 允许动作
- 

## 4. 禁止动作
- 

## 5. 执行记录
- actions_taken:
- tools_used:
- files_read:
- files_written:
- files_not_touched:

## 6. 输出物
- output_artifacts:
- report_paths:
- index_paths:

## 7. 验证标准
- required_checks:
- pass_conditions:
- fail_conditions:

## 8. 验证结果
- status: PASS / PARTIAL / FAIL
- evidence:
- missing_items:

## 9. 失败处理
- failure_type:
- recovery_action:
- rollback_required:
- next_phase_allowed: true / false

## 10. checkpoint
- checkpoint_id:
- checkpoint_path:
- resumable_from_here: true / false
```

## 阶段 checkpoint 命名

```text
checkpoint_00_task_passport
checkpoint_01_readonly_scout
checkpoint_02_semantic_classification
checkpoint_03_token_index
checkpoint_04_layer_assignment
checkpoint_05_copy_register
checkpoint_06_legacy_mapping
checkpoint_07_field_dictionary
checkpoint_08_data_passport
checkpoint_09_read_entry
checkpoint_10_sampling_validation
checkpoint_11_final_report
checkpoint_12_candidate_memory
```
