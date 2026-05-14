# Phase Routing Protocol

## Rule

Phase 是 workflow boundary，不是 Skill。总控 Skill 只决定路由和校验，不替代 Phase Controller 的领域判断。

## Route

```text
phase_00_system_constitution
→ phase_01_data_fact_controller
→ phase_02_wallet_structure_controller
→ phase_03_chip_control_controller
→ phase_04_scenario_recognition_controller
→ phase_05_structure_position_controller
→ phase_06_strategy_gate_controller
→ phase_07_execution_risk_controller
→ phase_08_review_learning_controller
→ phase_09_system_upgrade_controller
```

## Token Run UX

日常 CA 分析优先 skill-driven token analysis；P01-P09 全展开仅用于 audit/regression/debug。
