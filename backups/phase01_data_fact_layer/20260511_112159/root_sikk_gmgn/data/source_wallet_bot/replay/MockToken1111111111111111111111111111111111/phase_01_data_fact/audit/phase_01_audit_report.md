# phase_01_data_fact audit

- task: phase_01_data_fact_code_skeleton_landing
- phase: phase_01_data_fact
- data_quality_status: DATA_PARTIAL
- handoff_status: HANDOFF_DEGRADED
- local_handoff: `/root/sikk-gmgn/data/source_wallet_bot/replay/MockToken1111111111111111111111111111111111/phase_01_data_fact/handoff/phase_01_handoff_packet.json`
- shared_handoff: `/root/sikk-gmgn/data/shared_handoff/data_fact/MockToken1111111111111111111111111111111111/phase_01_handoff_packet.json`
- blocking_issues: []
- degraded_issues: ['missing_optional_raw:raw_top_trader.json', 'missing_optional_raw:raw_transfer.json', 'missing_optional_raw:legacy_candidate_snapshot.json', 'optional_missing_field:raw_top_trader.json', 'optional_missing_field:raw_transfer.json', 'transfer_missing_no_distribution_inference', 'transfer_missing_no_backflow_inference']

P01 only. No wallet role, chip control, scenario, strategy, execution, buy signal.
