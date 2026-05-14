# Phase Runtime Application Index

- final_status: `PHASE_RUNTIME_APPLICATION_INDEX_READY_WITH_GAPS`
- P00_system_boundary: `data/gmgn_candidates_live_run/live_run_manifest.json` / evidence=`PRESENT` / policy=`BLOCK_IF_BOUNDARY_UNKNOWN`
- P01_data_fact: `data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json` / evidence=`PRESENT` / policy=`BLOCK`
- P02_wallet_structure: `data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json` / evidence=`MISSING` / policy=`DEGRADED_NOT_SAFE`
- P03_chip_control: `data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json` / evidence=`MISSING` / policy=`DEGRADED_NOT_SAFE`
- P04_scenario_recognition: `data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json` / evidence=`PRESENT` / policy=`PAUSE`
- P05_structure_position: `data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json` / evidence=`PRESENT` / policy=`PAUSE`
- P06_strategy_gate: `data/gmgn_candidates_live_run/state_machine/candidate_states.json` / evidence=`PRESENT` / policy=`BLOCK`
- P07_execution_risk: `data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json + paper_live/paper_positions_open.json` / evidence=`PRESENT` / policy=`QUOTE_MISSING_PAUSE; PAPER_ONLY`
- P08_review_learning: `data/gmgn_candidates_live_run/reports` / evidence=`PRESENT_DIR` / policy=`READY_WITH_GAPS`
- P09_system_upgrade: `data/her_document_function_system/system_review/trading_system_core_20260514/u00_review_upgrade_candidate_package.json` / evidence=`CREATED_BY_AUTO_REPAIR` / policy=`CANDIDATE_ONLY`
