# Phase06 Required Fields

Phase06 必需字段来自 Phase05 handoff 的 `handoff_files`：

- phase_01_handoff_packet
- data_quality_summary
- phase_02_handoff_packet
- wallet_structure_decision
- wallet_classification
- phase_03_handoff_packet
- chip_control_summary
- dominant_side_status
- chip_transfer_status
- counterparty_pressure
- phase_04_handoff_packet
- primary_scenario
- scenario_counter_evidence
- scenario_hard_negative_checklist
- phase_05_handoff_packet
- structure_position_decision
- avwap_completion_gate
- failure_test_result
- fatigue_filter_result
- position_overextension_check
- quote_security_normalized
- token_market_context

缺失规则：
- required input 缺失或路径不存在：`PHASE_06_INPUT_BLOCKED` + `STRATEGY_BLOCK`。
- optional evidence 缺失：降级为 `PHASE_06_INPUT_DEGRADED`，不得输出无反证的 `PAPER_READY`。
- 禁止用 `0`、空字符串或 AI 推测替代 missing。
