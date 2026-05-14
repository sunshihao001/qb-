# Phase09 System Upgrade Controller

## 定位

Phase09 是 SIKK Stable Trader OS 的系统自我升级层。

它不是自由改规则层，不是自动调参层，不是直接上线层。它只把 Phase08 复盘学习结果转成可审查、可回归、可版本化、可回滚、需人工确认的升级包。

## 上游输入

- `phase_08_handoff_packet.json`
- `review_learning_summary.json`
- `failure_attribution.jsonl`
- `success_attribution.jsonl`
- `rule_update_candidates.json`
- `threshold_review_candidates.json`
- `model_recalibration_candidates.json`
- `scenario_case_library.json`
- `address_history_update.csv`
- `strategy_performance_summary.json`

## 必需字段

每个升级候选必须包含：

- `candidate_id`
- `target_phase`
- `candidate_type`
- `evidence_cases`
- `evidence_refs`
- `reason`

缺少 `target_phase` 或 `evidence_cases` 必须阻断升级包。

## Atomic Skill 调用边界

- upgrade_input_validator
- upgrade_candidate_classifier
- evidence_strength_reviewer
- rule_update_reviewer
- hard_negative_reviewer
- threshold_calibration_reviewer
- model_weight_reviewer
- schema_contract_update_reviewer
- status_code_update_reviewer
- telegram_panel_update_reviewer
- regression_validation_planner
- regression_validation_runner
- upgrade_package_writer
- rollback_plan_writer
- phase_handoff_writer
- audit_writer

## 硬否决

- Phase08 handoff 缺失
- Phase08 必读文件缺失
- 候选无法识别 `target_phase`
- 候选缺少 `evidence_cases`
- 阈值调整只基于单个偶然样本并试图直接生效
- 回归测试失败
- 升级包无 rollback plan
- 试图直接覆盖 runtime / production 文件

## 输出

- `upgrade_fact/*`
- `upgrade_review/*`
- `validation/*`
- `upgrade_package/*`
- `reports/*`
- `handoff/phase_09_handoff_packet.json`
- `audit/*`

## 完成定义

只有当输入校验、候选分类、证据强度审查、规则/阈值/模型/schema/status/telegram 审查、回归验证、升级包、rollback、handoff、audit 全部存在时，Phase09 才能输出 `SYSTEM_UPGRADE_READY`。

即使 READY，也必须保持：

- `requires_manual_confirmation=true`
- `allow_apply_to_runtime=false`
- `recommended_apply_mode=SHADOW_MODE_FIRST`
