# Phase Handoff Flow

- `phase_00_system_constitution` -> `phase_01_data_fact` via schema-validated handoff packet.
- `phase_01_data_fact` -> `phase_02_wallet_structure` via schema-validated handoff packet.
- `phase_02_wallet_structure` -> `phase_03_chip_control` via schema-validated handoff packet.
- `phase_03_chip_control` -> `phase_04_scenario_recognition` via schema-validated handoff packet.
- `phase_04_scenario_recognition` -> `phase_05_structure_position` via schema-validated handoff packet.
- `phase_05_structure_position` -> `phase_06_strategy_gate` via schema-validated handoff packet.
- `phase_06_strategy_gate` -> `phase_07_execution_risk` via schema-validated handoff packet.
- `phase_07_execution_risk` -> `phase_08_review_learning` via schema-validated handoff packet.
- `phase_08_review_learning` -> `phase_09_system_upgrade` via schema-validated handoff packet.

Rules: downstream reads only allowed handoff fields; no Markdown-as-state; hard negatives and degraded gaps must be inherited.
