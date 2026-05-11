# phase_01_data_fact audit_report

- phase_status: `DATA_PARTIAL`
- handoff_status: `HANDOFF_DEGRADED`
- hard_negative_triggered: `False`
- missing_fields: `['legacy_candidate_snapshot', 'raw_top_trader', 'raw_transfer', 'transfer_missing']`
- allowed_next_stage: `phase_02_wallet_structure`
- local_handoff: `/root/sikk-gmgn/data/source_wallet_bot/replay/MockToken1111111111111111111111111111111111/phase_01_v2_replay/handoff/phase_01_handoff_packet.json`
- shared_handoff: `/root/sikk-gmgn/data/shared_handoff/data_fact/MockToken1111111111111111111111111111111111/phase_01_handoff_packet.json`

## atomic_skills_called
- raw_snapshot_writer_skill
- gmgn_field_mapping_skill
- token_basic_normalizer_skill
- wallet_trade_normalizer_skill
- holder_trader_normalizer_skill
- transfer_normalizer_skill
- kline_normalizer_skill
- quote_security_normalizer_skill
- missing_field_checker_skill
- time_validity_checker_skill
- data_quality_scorer_skill
- phase_handoff_writer_skill
