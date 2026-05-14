# Atomic Skill Candidate Index

本目录保存 Atomic Skill 候选规格。它们是可复用能力候选，不等于已经启用的独立 Hermes Skill。成熟前只能通过 Phase Controller 调用或作为实现规格。

## Shared Output Contract

每个候选能力只能输出：`facts`、`evidence`、`counter_evidence`、`scores`、`labels`、`missing`、`risk_flags`、`handoff_suggestions`、`audit`。不得输出 `buy_now`、`auto_trade`、`real_trade_allowed`、`final_trade_state`。

## Candidate Inventory

### chip_control
- `chip_control/chip_transfer_detector_skill.md`
- `chip_control/counterparty_pressure_skill.md`
- `chip_control/dominant_side_status_skill.md`
- `chip_control/early_wallet_retention_skill.md`

### data_fact
- `data_fact/data_quality_scorer_skill.md`
- `data_fact/gmgn_field_mapping_skill.md`
- `data_fact/kline_normalizer_skill.md`
- `data_fact/missing_field_checker_skill.md`
- `data_fact/phase_handoff_writer_skill.md`
- `data_fact/raw_snapshot_writer_skill.md`
- `data_fact/time_validity_checker_skill.md`
- `data_fact/wallet_trade_normalizer_skill.md`

### execution_risk
- `execution_risk/paper_trade_writer_skill.md`
- `execution_risk/quote_risk_skill.md`
- `execution_risk/security_check_skill.md`
- `execution_risk/slippage_liquidity_skill.md`

### review_learning
- `review_learning/case_library_update_skill.md`
- `review_learning/failure_attribution_skill.md`
- `review_learning/rule_update_suggestion_skill.md`

### scenario_recognition
- `scenario_recognition/distribution_scene_detector_skill.md`
- `scenario_recognition/scenario_classifier_skill.md`
- `scenario_recognition/scenario_counter_evidence_skill.md`
- `scenario_recognition/trap_detector_skill.md`

### strategy_gate
- `strategy_gate/a_plus_p1_gate_skill.md`
- `strategy_gate/hard_negative_checklist_skill.md`
- `strategy_gate/strategy_reason_writer_skill.md`

### structure_position
- `structure_position/avwap_completion_gate_skill.md`
- `structure_position/failure_test_skill.md`
- `structure_position/fatigue_filter_skill.md`
- `structure_position/poc_context_skill.md`

### system_upgrade
- `system_upgrade/model_recalibration_skill.md`
- `system_upgrade/rule_versioning_skill.md`
- `system_upgrade/upgrade_audit_skill.md`

### wallet_structure
- `wallet_structure/address_role_classifier_skill.md`
- `wallet_structure/backflow_path_detector_skill.md`
- `wallet_structure/current_token_behavior_skill.md`
- `wallet_structure/gmgn_note_generator_skill.md`
- `wallet_structure/same_source_group_detector_skill.md`
- `wallet_structure/token_source_classifier_skill.md`
- `wallet_structure/wallet_entity_profiler_skill.md`

## Promotion Gate

候选能力升级为正式 Skill 或 runtime module 前必须满足：输入输出稳定、字段来源清楚、规则不频繁变化、独立测试存在、Phase Controller 能稳定读取、反证/缺口/审计完整。
