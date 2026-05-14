# V00 Runtime Evidence Bundle

- bundle_id: `V00_RUNTIME_EVIDENCE_BUNDLE_TRADING_SYSTEM_20260514`
- final_status: `V00_RUNTIME_EVIDENCE_READY_WITH_GAPS`
- safety_boundary: `SAFE_MODE_PAPER_ONLY_NO_REAL_SWAP_NO_PRIVATE_KEY_NO_SIGNATURE_NO_BROADCAST`

## Artifacts
- P01_candidate_discovery: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json` / sample_count=`11` / policy=`PASS_REQUIRED`
- P04_P05_signal: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json` / sample_count=`8` / policy=`PASS_REQUIRED`
- P06_state_machine: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/state_machine/candidate_states.json` / sample_count=`6` / policy=`PASS_REQUIRED`
- P02_P03_wallet_structure: `MISSING` / path=`data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json` / sample_count=`None` / policy=`DEGRADED_NOT_SAFE`
- P07_quote_security: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json` / sample_count=`8` / policy=`PAUSE_IF_MISSING`
- P07_paper_live_open: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/paper_live/paper_positions_open.json` / sample_count=`5` / policy=`PAPER_ONLY`
- P08_reports: `PRESENT_DIR` / path=`data/gmgn_candidates_live_run/reports` / sample_count=`10` / policy=`PASS_WITH_GAPS`
- runtime_manifest: `PRESENT_JSON_OK` / path=`data/gmgn_candidates_live_run/live_run_manifest.json` / sample_count=`9` / policy=`BOUNDARY_EVIDENCE`

## Acceptance Policy
- safe_mode_not_equal_production_accepted: `True`
- wallet_structure_missing_not_safe: `True`
- quote_scan_missing_pause_or_block: `True`
- paper_ready_not_real_trade_authorization: `True`
- review_output_candidate_only: `True`
