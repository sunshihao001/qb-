# Phase 05 Required Fields

- phase_04_handoff_packet.phase
- token_address
- snapshot_id
- scenario_status
- primary_scenario
- handoff_files.primary_scenario
- handoff_files.scenario_counter_evidence
- handoff_files.scenario_hard_negative_checklist
- handoff_files.kline_normalized
- handoff_files.token_market_context

## Kline required columns

- close
- high
- low
- volume_usd

Missing required fields must be written as `missing`; never coerce to 0.
