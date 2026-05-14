# Runtime Data Integrity Audit

- final_status: `RUNTIME_DATA_INTEGRITY_PASS_WITH_GAPS`
- mode: safe-mode / read-only / paper-only

## Stage checks
- P0_candidate_discovery: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=5; path=data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json
- P1_signal: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=8; path=data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json
- P2_state_machine: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=6; path=data/gmgn_candidates_live_run/state_machine/candidate_states.json
- P3_wallet_structure: status=MISSING; exists=False; json_ok=False; sample_count=0; path=data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json
- P4_quote_security: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=8; path=data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- P5_paper_live_open: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=5; path=data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
- P6_live_state: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=5; path=data/gmgn_candidates_live_run/live_state.json
- P7_manifest: status=PASS_WITH_GAPS; exists=True; json_ok=True; sample_count=9; path=data/gmgn_candidates_live_run/live_run_manifest.json

## Gaps
- runtime_P3_wallet_structure_missing_or_invalid: HIGH / missing/degraded must not be treated as safe
