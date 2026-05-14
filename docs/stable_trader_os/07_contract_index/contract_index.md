# Stable Trader OS Contract Index

本索引是总控 Skill 与 Phase Controller 读取 repo-level contracts 的入口。业务合约以 `/root/sikk-gmgn/contracts/stable_trader_os/` 为 source of truth；Skill 目录只做引用，不复制。

## Rules

- 每个 required input 必须有来源或显式 missing/degraded。
- 每个 required output 必须有 downstream reader 或 audit 用途。
- 自然语言报告不能替代 JSON contract/handoff。
- 缺失 required fields 不能强行升级为 READY。

## Files

- `phase_01_data_fact` / `input`: `contracts/stable_trader_os/phase_01_data_fact/input_contract.json`
- `phase_01_data_fact` / `output`: `contracts/stable_trader_os/phase_01_data_fact/output_contract.json`
- `phase_01_data_fact` / `acceptance`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json`
- `phase_01_data_fact` / `support`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_forbidden_judgement_contract.md`
- `phase_01_data_fact` / `support`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_goal_passport.json`
- `phase_01_data_fact` / `input`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json`
- `phase_01_data_fact` / `output`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json`
- `phase_01_data_fact` / `support`: `contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json`
- `phase_02_wallet_structure` / `acceptance`: `contracts/stable_trader_os/phase_02_wallet_structure/phase_02_acceptance_matrix.json`
- `phase_02_wallet_structure` / `input`: `contracts/stable_trader_os/phase_02_wallet_structure/phase_02_input_contract.json`
- `phase_02_wallet_structure` / `output`: `contracts/stable_trader_os/phase_02_wallet_structure/phase_02_output_contract.json`
- `phase_02_wallet_structure` / `support`: `contracts/stable_trader_os/phase_02_wallet_structure/phase_02_to_phase_03_contract.json`
- `phase_03_chip_control` / `handoff`: `contracts/stable_trader_os/phase_03_chip_control/handoff_rules.md`
- `phase_03_chip_control` / `acceptance`: `contracts/stable_trader_os/phase_03_chip_control/phase_03_acceptance_matrix.json`
- `phase_03_chip_control` / `input`: `contracts/stable_trader_os/phase_03_chip_control/phase_03_input_contract.json`
- `phase_03_chip_control` / `output`: `contracts/stable_trader_os/phase_03_chip_control/phase_03_output_contract.json`
- `phase_03_chip_control` / `required_fields`: `contracts/stable_trader_os/phase_03_chip_control/required_fields.md`
- `phase_04_scenario_recognition` / `handoff`: `contracts/stable_trader_os/phase_04_scenario_recognition/handoff_rules.md`
- `phase_04_scenario_recognition` / `acceptance`: `contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_acceptance_matrix.json`
- `phase_04_scenario_recognition` / `input`: `contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_input_contract.json`
- `phase_04_scenario_recognition` / `output`: `contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_output_contract.json`
- `phase_04_scenario_recognition` / `required_fields`: `contracts/stable_trader_os/phase_04_scenario_recognition/required_fields.md`
- `phase_05_structure_position` / `handoff`: `contracts/stable_trader_os/phase_05_structure_position/handoff_rules.md`
- `phase_05_structure_position` / `acceptance`: `contracts/stable_trader_os/phase_05_structure_position/phase_05_acceptance_matrix.json`
- `phase_05_structure_position` / `input`: `contracts/stable_trader_os/phase_05_structure_position/phase_05_input_contract.json`
- `phase_05_structure_position` / `output`: `contracts/stable_trader_os/phase_05_structure_position/phase_05_output_contract.json`
- `phase_05_structure_position` / `required_fields`: `contracts/stable_trader_os/phase_05_structure_position/required_fields.md`
- `phase_06_strategy_filter` / `handoff`: `contracts/stable_trader_os/phase_06_strategy_filter/handoff_rules.md`
- `phase_06_strategy_filter` / `input`: `contracts/stable_trader_os/phase_06_strategy_filter/phase_06_input_contract.json`
- `phase_06_strategy_filter` / `output`: `contracts/stable_trader_os/phase_06_strategy_filter/phase_06_output_contract.json`
- `phase_06_strategy_filter` / `required_fields`: `contracts/stable_trader_os/phase_06_strategy_filter/required_fields.md`
- `phase_07_execution_risk` / `handoff`: `contracts/stable_trader_os/phase_07_execution_risk/handoff_rules.md`
- `phase_07_execution_risk` / `input`: `contracts/stable_trader_os/phase_07_execution_risk/phase_07_input_contract.json`
- `phase_07_execution_risk` / `output`: `contracts/stable_trader_os/phase_07_execution_risk/phase_07_output_contract.json`
- `phase_07_execution_risk` / `required_fields`: `contracts/stable_trader_os/phase_07_execution_risk/required_fields.md`
- `phase_08_review_learning` / `handoff`: `contracts/stable_trader_os/phase_08_review_learning/handoff_rules.md`
- `phase_08_review_learning` / `input`: `contracts/stable_trader_os/phase_08_review_learning/phase_08_input_contract.json`
- `phase_08_review_learning` / `output`: `contracts/stable_trader_os/phase_08_review_learning/phase_08_output_contract.json`
- `phase_08_review_learning` / `required_fields`: `contracts/stable_trader_os/phase_08_review_learning/required_fields.md`
- `phase_09_system_upgrade` / `handoff`: `contracts/stable_trader_os/phase_09_system_upgrade/handoff_rules.md`
- `phase_09_system_upgrade` / `input`: `contracts/stable_trader_os/phase_09_system_upgrade/phase_09_input_contract.json`
- `phase_09_system_upgrade` / `output`: `contracts/stable_trader_os/phase_09_system_upgrade/phase_09_output_contract.json`
- `phase_09_system_upgrade` / `required_fields`: `contracts/stable_trader_os/phase_09_system_upgrade/required_fields.md`
