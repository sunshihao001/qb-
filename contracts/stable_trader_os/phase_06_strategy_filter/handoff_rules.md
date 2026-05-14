# Phase06 Handoff Rules

Phase06 handoff 目标：`phase_07_execution_risk_controller`。

允许交接：
- `PAPER_READY`
- `READY_FOR_CONFIRMATION`
- `A_PLUS_P1_PASS`

暂停或复核：
- `STRATEGY_PAUSE`
- `REVIEW_ONLY`

阻断：
- `STRATEGY_BLOCK`

硬否决优先级：任何上游硬否决不得被策略层覆盖，包括：
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

`PAPER_READY` 必须同时满足：
1. A 结构质量通过。
2. P1 位置质量通过。
3. 无上游硬否决。
4. 证据链完整或足够强。
5. 有 `invalidation_conditions`。
6. 有 `required_execution_checks`。
