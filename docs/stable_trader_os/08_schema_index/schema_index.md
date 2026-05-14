# Stable Trader OS Schema Index

本索引用于总控 Skill、Phase Controller 与验证器定位 repo-level JSON schemas。Schema source of truth 是 `/root/sikk-gmgn/schemas/stable_trader_os/`。

## Rules

- schema parse failure = BLOCKED。
- schema missing but optional = DEGRADED_WITH_GAPS。
- handoff packet schema 是跨阶段读取的最低要求。

## Files

- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/holder_fact_table_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/kline_fact_table_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/phase_01_field_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/phase_01_quality_gate_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/quote_fact_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/security_fact_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/token_fact_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/trade_fact_table_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/transfer_fact_table_schema.json`
- `phase_01_data_fact`: `schemas/stable_trader_os/phase_01_data_fact/wallet_fact_table_schema.json`
- `phase_02_wallet_structure`: `schemas/stable_trader_os/phase_02_wallet_structure/phase_02_handoff_packet.schema.json`
- `phase_02_wallet_structure`: `schemas/stable_trader_os/phase_02_wallet_structure/wallet_structure_decision.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/backflow_risk_state.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/chip_control_summary.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/chip_transfer_status.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/counterparty_pressure.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/distribution_sell_state.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/dominant_side_status.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/early_chip_state.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/phase_03_handoff_packet.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/same_source_group_chip_state.schema.json`
- `phase_03_chip_control`: `schemas/stable_trader_os/phase_03_chip_control/structure_wallet_sets.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/chip_scenario_context.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/market_cap_scenario_context.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/market_lifecycle_context.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/phase_04_handoff_packet.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/price_structure_state.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/primary_scenario.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/scenario_counter_evidence.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/scenario_scores.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/volume_quality_state.schema.json`
- `phase_04_scenario_recognition`: `schemas/stable_trader_os/phase_04_scenario_recognition/wallet_scenario_context.schema.json`
- `phase_05_structure_position`: `schemas/stable_trader_os/phase_05_structure_position/phase_05_handoff_packet.schema.json`
- `phase_05_structure_position`: `schemas/stable_trader_os/phase_05_structure_position/structure_position_decision.schema.json`
- `phase_06_strategy_filter`: `schemas/stable_trader_os/phase_06_strategy_filter/phase_06_handoff_packet.schema.json`
- `phase_06_strategy_filter`: `schemas/stable_trader_os/phase_06_strategy_filter/strategy_gate_decision.schema.json`
- `phase_07_execution_risk`: `schemas/stable_trader_os/phase_07_execution_risk/execution_risk_decision.schema.json`
- `phase_07_execution_risk`: `schemas/stable_trader_os/phase_07_execution_risk/phase_07_handoff_packet.schema.json`
- `phase_08_review_learning`: `schemas/stable_trader_os/phase_08_review_learning/phase_08_handoff_packet.schema.json`
- `phase_08_review_learning`: `schemas/stable_trader_os/phase_08_review_learning/review_learning_summary.schema.json`
- `phase_09_system_upgrade`: `schemas/stable_trader_os/phase_09_system_upgrade/phase_09_handoff_packet.schema.json`
- `phase_09_system_upgrade`: `schemas/stable_trader_os/phase_09_system_upgrade/rule_update_package.schema.json`
- `phase_09_system_upgrade`: `schemas/stable_trader_os/phase_09_system_upgrade/upgrade_candidate_classification.schema.json`
