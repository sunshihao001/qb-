# 模块清单

## sikk_accumulation_window_detector.py
- 行数: 593
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 类: Candle
- 函数: to_float, parse_timestamp, fmt_time, sma, rolling_sum, median, load_csv, compute_indicators, detect_swings, compute_volume_profile, score_accumulation, find_t_start, latest_lh_before, has_sequence_ll_lh_hl_hh, detect_window, write_outputs, main

## sikk_auto_exit_planner.py
- 行数: 58
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: build_exit_plan

## sikk_auto_position_sizer.py
- 行数: 50
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: calculate_position_plan

## sikk_auto_readiness_runner.py
- 行数: 227
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: ts_to_utc_text, load_json, load_kline_csv, derive_control_box, find_first_sikk_b_bar, build_runner_context, run, parse_args

## sikk_auto_risk_gate.py
- 行数: 111
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: _num, _bool, evaluate_risk_gate

## sikk_auto_signal_engine.py
- 行数: 132
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: _num, _bool, evaluate_signal

## sikk_auto_trade_types.py
- 行数: 100
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 类: SignalLevel, TradePermission, RiskGateResult, SignalResult, PositionPlan, ExitPlan
- 函数: _serialize, readiness_to_dict

## sikk_candidate_kline_pipeline.py
- 行数: 386
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _num, _int, _first, _utc_now, _assert_readonly_kline_command, build_gmgn_kline_command, default_runner, _extract_kline_rows, write_kline_csv, select_candidates_for_kline, _candidate_address, _candidate_symbol, _candidate_open_ts, _candidate_supply, _resolution_duration_minutes, run_accumulation_detector_for_csv, run_candidate_kline_pipeline, main

## sikk_candidate_quote_security_pipeline.py
- 行数: 410
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now_text, _read_json, _write_json, _write_csv, _state_rows, _signal_index, _to_float, _sol_to_lamports, _readiness_path_for_token, _map_final_permission, _build_requests, run_candidate_quote_security_pipeline, parse_args, main

## sikk_candidate_signal_pipeline.py
- 行数: 269
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now_text, _read_json, _write_json, _write_csv, _safe_token_dir_name, _extract_kline_path, _load_readiness_result, _flatten_signal_row, _make_runner_args, run_candidate_signal_pipeline, parse_args, main

## sikk_candidate_state_machine.py
- 行数: 428
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now_text, _read_json, _write_json, _write_jsonl, _write_csv, _as_float, _candidate_rows, _index_by_token, _load_accumulation, _wallet_structure_rows, _apply_wallet_structure_gate, _derive_state, run_candidate_state_machine, parse_args, main

## sikk_candidate_wallet_structure_pipeline.py
- 行数: 351
- CLI入口: True
- argparse: True
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now_text, _read_json, _write_json, _write_csv, _state_rows, _assert_readonly_command, _run_json_command, _text, _num, _classify_gmgn_wallet, default_gmgn_wallet_collector, run_candidate_wallet_structure_pipeline, parse_args, main

## sikk_control_chip_window_detector.py
- 行数: 245
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: fl, ts, short, tags, load_wallets, load_kline, wallet_role, phase_name, detect_pull_start, find_kline_at, main

## sikk_dashboard_builder.py
- 行数: 135
- CLI入口: True
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _read_json, _read_events, _esc, _cls, build_dashboard_html, write_dashboard

## sikk_dominant_lifecycle_classifier.py
- 行数: 545
- CLI入口: True
- argparse: True
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 函数: _now_iso, _num, _bool, _first, _load_json, _rows_from_payload, _index_by_token, _load_wallet_decision, _score_accumulation, _score_distribution, _score_control_retention, classify_lifecycle, _cn_row, _write_csv, _write_md, run_dominant_lifecycle_classifier, main

## sikk_execution_adapter_base.py
- 行数: 85
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: TokenSide, QuoteRequest, QuoteResult, SecurityScanResult, PreTradeSecurityDecision, ReadOnlyQuoteAdapter

## sikk_execution_state_machine.py
- 行数: 267
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: ExecutionGateDecision
- 函数: _get, _parse_utc, _quote_age_seconds, _token_from_inputs, evaluate_execution_gate, _decision_to_dict, _markdown, _order_monitor_stub, write_execution_gate_review

## sikk_gmgn_new_token_filter.py
- 行数: 463
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _num, _int, _first, _pct_text, load_filter_config, normalize_token, _below_min, _above_max, classify_token, build_gmgn_trenches_command, _assert_readonly_command, default_runner, _iter_trenches_tokens, _csv_value, write_candidate_outputs, collect_and_write_candidate_pool, main

## sikk_gmgn_quote_adapter.py
- 行数: 40
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: GMGNQuoteAdapter

## sikk_gmgn_token_report.py
- 行数: 330
- CLI入口: True
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: sh, fl, fmt, pct, ts, hm, tags, get_any, write_csv, classify, main

## sikk_live_orchestrator.py
- 行数: 418
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: iso_now, _write_json, _read_json, _append_jsonl, _token_address, _token_symbol, load_existing_token_status, emit_event, build_token_status, write_token_status_files, write_live_state, write_latest_events_md, _status_rank, _priority_level, _next_action, _reason, write_live_board, run_once, load_candidates_from_file, parse_args, main

## sikk_live_quote_security_collector.py
- 行数: 312
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: GMGNLiveQuoteCollector, OKXLiveQuoteCollector, OKXSecurityScanCollector
- 函数: _assert_readonly_command, run_readonly_cli, _loads_json, _first_payload_object, _pick, _parse_pct, collect_live_pre_trade_inputs, collect_and_write_live_pre_trade_review

## sikk_live_run.py
- 行数: 533
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: iso_now, _send_message_tool, report_date_from_now, _read_json, _write_json, _append_jsonl, build_runtime_candidates_from_state_file, _token_address, _token_symbol, _status_from_state_row, _extract_rows, _index_rows_by_token, _quote_rows, _open_paper_rows, _quote_gate_from_row, _security_gate_from_row, _paper_pnl, _apply_latest_runtime_decision, build_enriched_runtime_statuses, _write_token_status_files, _write_live_state, _write_live_board, _write_latest_events, _format_broadcast_message, _send_telegram_broadcast

## sikk_module_runner.py
- 行数: 145
- CLI入口: False
- argparse: False
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 函数: _base_dir, _token_address, _token_symbol, output_path_for_module, output_exists_for_module, _assert_safe_command, default_script_runner, run_python_function, run_one_module, run_external_modules_for_token

## sikk_notifier.py
- 行数: 63
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: should_notify, format_event_message, default_post_json, notify_event

## sikk_okx_quote_adapter.py
- 行数: 34
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: OKXQuoteAdapter

## sikk_paper_live_runner.py
- 行数: 744
- CLI入口: True
- argparse: True
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now_text, _read_json, _write_json, _write_csv, _append_jsonl, _to_float, _state_rows, _signal_rows, _quote_rows, _index_by_token, _readiness_path, _load_open_positions, _load_closed_positions, _load_wallet_structure_runtime_inputs, _close_position_for_wallet_action, _failure_attribution_row, _extract_exit_plan, _entry_allowed, _default_cost_model, _cost_buffer_pct, _new_position, _decision_get, _decision_metrics, decide_wallet_position_action, _update_position

## sikk_paper_trading_engine.py
- 行数: 116
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _bar_price, simulate_paper_trade

## sikk_pre_trade_security_checker.py
- 行数: 78
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: _norm, evaluate_pre_trade_security

## sikk_quote_security_review.py
- 行数: 295
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _serialize, _now_utc_text, _to_float, _quote_deviation_pct, _max_price_impact, build_quote_snapshot, build_security_scan_report, _security_decision_from_report, build_quote_security_decision, _decision_to_security_gate, _write_json, build_and_write_pre_trade_review

## sikk_real_trade_guard.py
- 行数: 69
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: TradePlan, TradeAuthorization, RealTradeGuard

## sikk_same_source_grouping.py
- 行数: 380
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: _text, _num, _parse_time, _cv, _source_reliability, _funding_time_close, _entry_time_close, _relative_close, same_source_similarity_score, _connected_components, _time_span_sec, _entry_rank_span, _score_by_threshold, _funding_group_type, compute_sync_buy_score, compute_sync_sell_score, _group_id, _risk_level, _evidence_level, _group_row, build_same_source_groups, write_candidate_groups_csv

## sikk_token_skip_policy.py
- 行数: 90
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: _parse_time, _now, _token_address, read_token_status, should_process_token

## sikk_trace_logger.py
- 行数: 96
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: False
- 函数: iso_now, _token_address, _token_symbol, read_json_optional, append_jsonl, _nested_status, detect_state_change, write_process_trace

## sikk_trade_confirmation_ticket.py
- 行数: 363
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: TradeConfirmationTicket
- 函数: _serialize, _enum_value, _trade_permission_from_value, _signal_level_from_value, _readiness_sections_from_payload, _get_attr, _is_real_execution_candidate, _quote_lines, _markdown_for_ticket, build_trade_confirmation_ticket, build_trade_confirmation_ticket_from_readiness_payload, write_trade_confirmation_ticket

## sikk_trade_journal.py
- 行数: 119
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _ensure_dir, write_json, write_csv, write_readiness_outputs

## sikk_transaction_broadcast_guard.py
- 行数: 189
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 类: BroadcastGateDecision
- 函数: _has_payload, evaluate_broadcast_gate, _decision_to_dict, _markdown, _broadcast_monitor, write_broadcast_gate_review

## sikk_wallet_structure_daily_report.py
- 行数: 239
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _num, _read_csv, _read_jsonl, _write_json, _write_csv, _closed_return, _wallet_status, _signal_level, _failure_type, _summarize, _group_summary, _flatten_summary, _write_md, build_wallet_structure_daily_report, parse_args, main

## sikk_wallet_structure_gate.py
- 行数: 541
- CLI入口: False
- argparse: False
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 类: WalletStructureDecision
- 函数: _utc_now_text, _text, _num, _ratio, _role, _game_side, _evidence_level, _clearout, _highest_evidence, evaluate_wallet_structure_gate, _write_json, _write_csv, _gmgn_action, evaluate_and_write_wallet_structure

## sikk_wallet_structure_snapshot.py
- 行数: 259
- CLI入口: False
- argparse: False
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _iso_now, _safe_name, _num, _pct_change, _write_json, _read_json, _decision_value, _dominant_side_from_decision, build_snapshot, interpret_delta, classify_delta_status, build_delta, write_snapshot_and_delta

## sikk_wallet_trade_adapter.py
- 行数: 241
- CLI入口: False
- argparse: False
- 读取钱包决策: True
- 涉及swap/real/broadcast字样: True
- 函数: _read_json, _as_float, _as_bool, _pick, missing_wallet_decision, normalize_wallet_decision, load_wallet_decision, apply_wallet_gate, attach_wallet_factor_to_position, evaluate_wallet_change_for_open_position

## run_sikk_gmgn_pipeline.py
- 行数: 401
- CLI入口: True
- argparse: True
- 读取钱包决策: False
- 涉及swap/real/broadcast字样: True
- 函数: _utc_now, _read_json, _write_json, _read_gmgn_env_value, _default_wallet_address, _count_state_machine_candidates, _candidate_filter_stats, _kline_stats, _signal_stats, _state_stats, _quote_security_stats, _wallet_structure_stats, _build_markdown_report, run_full_pipeline, parse_args, main

