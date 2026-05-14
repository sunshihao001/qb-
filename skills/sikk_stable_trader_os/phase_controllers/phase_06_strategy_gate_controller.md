# Phase 06 Strategy Gate Controller

## 阶段目标

Phase06 将 Phase01 数据事实、Phase02 结构地址、Phase03 筹码控制、Phase04 场景识别、Phase05 结构位置确认统一汇总为策略资格判断。

它不是买点生成器，不是执行层，不输出实盘交易指令。

## 上游输入

通过 `phase_05_handoff_packet.json` 的 `handoff_files` 读取：

- Phase01：`phase_01_handoff_packet`、`data_quality_summary`、`quote_security_normalized`、`token_market_context`
- Phase02：`phase_02_handoff_packet`、`wallet_structure_decision`、`wallet_classification`
- Phase03：`phase_03_handoff_packet`、`chip_control_summary`、`dominant_side_status`、`chip_transfer_status`、`counterparty_pressure`
- Phase04：`phase_04_handoff_packet`、`primary_scenario`、`scenario_counter_evidence`、`scenario_hard_negative_checklist`
- Phase05：`phase_05_handoff_packet`、`structure_position_decision`、`avwap_completion_gate`、`failure_test_result`、`fatigue_filter_result`、`position_overextension_check`

## Atomic Skill

- upstream_status_integrator_skill
- a_plus_structure_quality_skill
- p1_position_quality_skill
- hard_negative_checklist_skill
- strategy_fit_scorer_skill
- strategy_reason_writer_skill

## 输出

- `strategy_fact/upstream_state_summary.json`
- `strategy_fact/upstream_state_matrix.csv`
- `strategy_decision/hard_negative_checklist.json`
- `strategy_decision/structure_quality_assessment.json`
- `strategy_decision/position_quality_assessment.json`
- `strategy_decision/strategy_template_match.json`
- `strategy_decision/risk_reward_check.json`
- `strategy_decision/evidence_chain_check.json`
- `strategy_decision/multi_dimensional_strategy_scores.json`
- `strategy_decision/a_plus_p1_result.json`
- `strategy_decision/strategy_gate_decision.json`
- `handoff/phase_06_handoff_packet.json`
- `audit/missing_fields_report.md`
- `reports/system_audit/phase_06_strategy_gate_audit.md`

## 状态码

- `A_PLUS_P1_PASS`
- `PAPER_READY`
- `READY_FOR_CONFIRMATION`
- `STRATEGY_PAUSE`
- `STRATEGY_BLOCK`
- `REVIEW_ONLY`

## 硬否决

上游硬否决不得被策略层覆盖：

- `DATA_INVALID`
- `WALLET_BLOCK`
- `ACTIVE_DISTRIBUTION`
- `TRANSFER_TO_COUNTERPARTY`
- `STRUCTURE_COLLAPSE`
- `SCENARIO_BLOCK`
- `SCENARIO_TRAP_RISK`
- `SCENARIO_DISTRIBUTION_RISK`
- `COMPLETION_FAIL`
- `FATIGUE_BLOCK`
- `POSITION_OVEREXTENDED`

## 完成标准

- 必需输入存在。
- A 结构质量与 P1 位置质量分别裁决。
- 正证、反证、硬否决均输出。
- `PAPER_READY` 必须带 `invalidation_conditions` 与 `required_execution_checks`。
- 输出 handoff 给 Phase07。
- 写 audit report。
