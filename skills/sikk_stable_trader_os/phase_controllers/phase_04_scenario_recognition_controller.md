# Phase 04 Scenario Recognition Controller

## 阶段目标
读取 Phase01/02/03 输出，将钱包结构、筹码控制、K线、成交量、市值上下文转化为多场景竞争裁决。

## 边界
- 不是买点层。
- 不是策略层。
- 不输出真实交易建议。
- 二段扩张只能输出候选，完成判断交给 Phase05。

## Atomic Skills
market_lifecycle_classifier, price_structure_classifier, volume_quality_classifier, wallet_scenario_context_builder, chip_scenario_context_builder, market_cap_scenario_context_builder, risk_scenario_detector, positive_scenario_detector, scenario_score_engine, scenario_counter_evidence_checker, scenario_hard_negative_checker, primary_scenario_decision_writer, phase_04_handoff_writer, phase_04_auditor.

## 硬否决
风险场景优先级高于正向场景；硬否决高于模型打分。
