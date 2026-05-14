# SIKK 阶段 1.1：全系统时间坐标 Schema

## 目标

建立 SIKK 全系统每个阶段需要的时间字段、TTL、stale 判断、过期动作和输出 schema。
本阶段只做时间标准与文档/schema 产物，不修改状态机、钱包结构、paper runner、实盘逻辑，也不新增交易规则。

## 安全边界

- 不修改状态机。
- 不修改钱包结构逻辑。
- 不修改 paper runner。
- 不修改实盘逻辑。
- 不新增交易规则。
- 所有 stale_action 都是时间治理动作，不等于买入/卖出/实盘执行。

## 全局时间字段标准

- `source_time`：源数据自身时间；优先取链上事件时间、K线时间、API quote/security 时间。
- `created_at`：本阶段产物生成时间；`age_sec = now - created_at`。
- `input_window_start`：本阶段读取输入证据窗口开始时间。
- `input_window_end`：本阶段读取输入证据窗口结束时间。
- `age_sec`：当前时间距离 `created_at` 的秒数；缺失时写 `null/待补`，不得编造。
- `ttl_sec`：本阶段有效期秒数；可由模块显式配置覆盖 schema 默认值。
- `stale`：`age_sec > ttl_sec`；缺 age/ttl 时为 `null/UNKNOWN`。
- `elapsed_sec`：阶段处理耗时，通常为 `finished_at - started_at`。
- `time_skew_sec`：本阶段输入之间或跨阶段关键输入之间的最大 age 差。
- `refresh_required`：是否需要刷新；通常 `stale=true` 或 critical field missing 时为 `true`。
- `stale_action`：过期后的时间治理动作。

## 全局 stale 判断

```text
age_sec = now - created_at
stale = age_sec > ttl_sec
elapsed_sec = finished_at - started_at
time_skew_sec = max_available_age_sec - min_available_age_sec
```

同步状态：

- `TEMPORAL_SYNCED`：`time_skew_sec <= 180`
- `TEMPORAL_PARTIAL_SYNC`：`180 < time_skew_sec <= 600`
- `TEMPORAL_DESYNC`：`time_skew_sec > 600`
- `TEMPORAL_UNKNOWN`：关键时间字段缺失，无法判断

## 字段映射与枚举

### canonical_field_map

- **`token_open_time`**：`token_open_time`、`pool_open_time`、`opened_at`、`pair_created_at`、`launch_time`、`token_created_at`
- **`pool_created_at`**：`pool_created_at`、`liquidity_created_at`、`pair_created_at`、`lp_created_at`、`pool_open_time`
- **`discovered_at`**：`discovered_at`、`candidate_discovered_at`、`first_seen_at`、`candidate_snapshot_at`、`first_seen_by_system_at`
- **`candidate_discovered_at`**：`candidate_discovered_at`、`discovered_at`、`first_seen_at`、`first_seen_by_system_at`
- **`first_seen_at`**：`first_seen_at`、`first_seen_by_system_at`、`candidate_discovered_at`、`discovered_at`
- **`last_seen_at`**：`last_seen_at`、`last_update`、`updated_at`、`source_last_update`、`last_update_time`
- **`candidate_snapshot_at`**：`candidate_snapshot_at`、`snapshot_time`、`last_update`、`generated_at`、`last_update_time`
- **`signal_time`**：`signal_time`、`first_signal_at`、`signal.created_at`、`signal.detected_at`
- **`signal_level`**：`signal_level`、`signal_level_code`、`signal.level`、`signal.signal_level`
- **`wallet_decision_time`**：`wallet_decision_time`、`wallet_decision_created_at`、`wallet_decision_at`、`decision_time`
- **`wallet_decision_created_at`**：`wallet_decision_created_at`、`wallet_decision_time`、`wallet_decision_at`、`decision_time`
- **`pattern_created_at`**：`pattern_created_at`、`pattern_time`、`pattern_classified_at`、`pattern.detected_at`
- **`lifecycle_created_at`**：`lifecycle_created_at`、`lifecycle_classified_at`、`dominant_lifecycle_created_at`、`lifecycle.time`
- **`intent_created_at`**：`intent_created_at`、`intent_time`、`dominant_intent_created_at`、`intent.detected_at`
- **`quote_time`**：`quote_time`、`quote_checked_at`、`quote_received_at`、`quote_requested_at`
- **`quote_requested_at`**：`quote_requested_at`、`quote_requested_time`、`quote.requested_at`
- **`quote_received_at`**：`quote_received_at`、`quote_time`、`quote_checked_at`、`quote.received_at`
- **`security_scan_time`**：`security_scan_time`、`security_checked_at`、`security_time`、`security.scan_at`
- **`final_gate_created_at`**：`final_gate_created_at`、`final_gate_time`、`final_gate_checked_at`、`final_gate.generated_at`
- **`paper_entry_time`**：`paper_entry_time`、`paper_entry_at`、`entry_time`、`paper.entry_time`
- **`paper_signal_time`**：`paper_signal_time`、`signal_time`、`first_signal_at`、`paper.signal_time`
- **`entry_time`**：`entry_time`、`paper_entry_time`、`paper_entry_at`、`position_opened_at`
- **`exit_time`**：`exit_time`、`paper_exit_time`、`paper_exit_at`、`position_closed_at`
- **`last_update_time`**：`last_update_time`、`last_update`、`updated_at`、`source_last_update`、`generated_at`
- **`failure_detected_at`**：`failure_detected_at`、`failed_at`、`failure_time`、`exit_triggered_at`、`paper_failure_time`
- **`report_generated_at`**：`report_generated_at`、`generated_at`、`report_time`、`summary_generated_at`

### enum 定义

- **candidate_stage_enum**：`D0_SCOUT_ONLY`、`D1_EARLY_STRUCTURE_WINDOW`、`D2_MAIN_TRADING_WINDOW`、`D3_LATE_WINDOW`、`D4_OLD_TOKEN`、`STAGE_UNKNOWN`
- **discovery_quality_enum**：`EARLY_DISCOVERY`、`NORMAL_DISCOVERY`、`LATE_DISCOVERY`、`VERY_LATE_DISCOVERY`、`DISCOVERY_UNKNOWN`
- **temporal_sync_status_enum**：`TEMPORAL_SYNCED`、`TEMPORAL_PARTIAL_SYNC`、`TEMPORAL_DESYNC`、`TEMPORAL_UNKNOWN`
- **temporal_gate_enum**：`TEMPORAL_ALLOW`、`TEMPORAL_WATCH`、`TEMPORAL_PAUSE`、`TEMPORAL_EXPIRED`、`TEMPORAL_BLOCK`、`TEMPORAL_UNKNOWN`
- **stale_action_enum**：`TEMPORAL_AUDIT_ONLY`、`TEMPORAL_WATCH_OR_REFRESH_CANDIDATES`、`TEMPORAL_REFRESH_KLINE`、`TEMPORAL_EXPIRED_FOR_S3_S4_SIGNAL_STALE`、`TEMPORAL_REFRESH_WALLET_STRUCTURE`、`TEMPORAL_PAUSE_IF_DESYNC`、`TEMPORAL_REFRESH_LIFECYCLE`、`TEMPORAL_REFRESH_INTENT`、`TEMPORAL_EXPIRED_NO_ALLOW`、`TEMPORAL_PAUSE_OR_EXPIRED`、`TEMPORAL_REVIEW_PAPER_POSITION`、`TEMPORAL_APPEND_REVIEW_REQUIRED`、`TEMPORAL_GENERATE_DAILY_REVIEW`

### 统一时间字段分类

- `required_input_fields`：阶段必须从上游读取的字段。
- `optional_input_fields`：有则增强、无则允许 null 的字段。
- `derived_fields`：由时间门禁/汇总层计算出的字段。
- `output_fields`：每个 token 在 time_context 输出中必须写出的字段。
- `source_paths`：该阶段优先读取的文件/JSON path/上游来源。

## 特殊硬规则

- `D0_SCOUT_ONLY` 不能 `TEMPORAL_ALLOW`，只能 `TEMPORAL_WATCH` 或更保守状态。
- `D4_OLD_TOKEN` 不能自动 `BLOCK`。
- `D4_OLD_TOKEN` 必须 `requires_pattern_review=true`。
- `D4_OLD_TOKEN` 是否可继续分析由阶段 2 盘型识别判断。
- `quote_stale=true` 不能 `TEMPORAL_ALLOW`，必须刷新或 `TEMPORAL_EXPIRED`。
- `S3/S4 signal_stale=true` 必须 `TEMPORAL_EXPIRED`。

## 阶段覆盖与字段分类

> 注：用户阶段编号为 0-12，本文档覆盖“系统基线 + 12 个业务阶段”，即 13 个编号节点。

- **0｜S0_SYSTEM_BASELINE｜系统基线审查**
  - source：live_run_manifest / runtime safety / system index
  - source_paths：
    - `data/gmgn_candidates_live_run/live_run_manifest.json`
    - `data/gmgn_candidates_live_run/index/system_index.json`
    - `data/gmgn_candidates_live_run/site/dashboard_data.json`
  - ttl_sec：`3600`
  - stale_action：`TEMPORAL_AUDIT_ONLY`
  - required_input_fields：`report_generated_at, last_update_time`
  - optional_input_fields：`source_time, created_at, input_window_start, input_window_end, candidate_stage_enum, temporal_sync_status`
  - derived_fields：`age_sec, elapsed_sec, time_skew_sec, refresh_required, stale, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`time_context_gate, temporal_sync_status, temporal_gate, time_context_score, requires_pattern_review, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：只审查系统安全边界、入口、manifest 与运行目录；过期只要求重新审计，不改变交易状态。
- **1｜S1_CANDIDATE_DISCOVERY｜候选发现**
  - source：GMGN candidates / live_state / discovery list
  - source_paths：
    - `data/gmgn_candidates_live_run/live_state.json`
    - `data/gmgn_candidates_live_run/site/dashboard_data.json`
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
  - ttl_sec：`86400`
  - stale_action：`TEMPORAL_WATCH_OR_REFRESH_CANDIDATES`
  - required_input_fields：`discovered_at, candidate_discovered_at, first_seen_at`
  - optional_input_fields：`token_open_time, pool_created_at, last_seen_at, candidate_snapshot_at, signal_time, signal_level, candidate_stage_enum, discovery_quality_enum`
  - derived_fields：`age_sec, stale, refresh_required, discovery_quality, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`candidate_stage, discovery_quality, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：候选发现时间可较长；D0_SCOUT_ONLY 只能 WATCH，不能 TEMPORAL_ALLOW。
- **2｜S2_KLINE_COLLECTION｜K线采集**
  - source：GMGN/OKX kline latest candle
  - source_paths：
    - `gmgn market kline api response`
    - `data/gmgn_candidates_live_run/live_state.json`
    - `data/gmgn_candidates_live_run/site/dashboard_data.json`
  - ttl_sec：`300`
  - stale_action：`TEMPORAL_REFRESH_KLINE`
  - required_input_fields：`quote_time, quote_requested_at, quote_received_at, source_time`
  - optional_input_fields：`token_open_time, pool_created_at, last_update_time, input_window_start, input_window_end, signal_time`
  - derived_fields：`age_sec, stale, elapsed_sec, time_skew_sec, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`kline_window_start, kline_window_end, latest_kline_time, kline_stale, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：K线过期只能要求刷新K线或降级观察，不新增交易规则。
- **3｜S3_PATTERN_RECOGNITION｜盘型识别**
  - source：pattern classifier output
  - source_paths：
    - `data/gmgn_candidates_live_run/live_state.json`
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `pattern classifier output`
  - ttl_sec：`900`
  - stale_action：`TEMPORAL_EXPIRED_FOR_S3_S4_SIGNAL_STALE`
  - required_input_fields：`pattern_created_at, signal_level, latest_kline_time`
  - optional_input_fields：`candidate_stage_enum, discovered_at, wallet_decision_created_at, quote_time, source_time`
  - derived_fields：`pattern_stale, age_sec, stale, refresh_required, temporal_sync_status, temporal_gate, time_context_score, requires_pattern_review, stage_missing_fields`
  - output_fields：`pattern_created_at, pattern_stale, candidate_stage, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, requires_pattern_review, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：S3/S4 signal_stale=true 必须 TEMPORAL_EXPIRED。
- **4｜S4_WALLET_STRUCTURE｜钱包结构**
  - source：wallet_structure_decision / snapshot / delta
  - source_paths：
    - `data/gmgn_candidates_live_run/index/position_index.json`
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `wallet_structure_decision.json`
  - ttl_sec：`900`
  - stale_action：`TEMPORAL_REFRESH_WALLET_STRUCTURE`
  - required_input_fields：`wallet_decision_created_at, wallet_decision_time, last_update_time`
  - optional_input_fields：`pattern_created_at, discovered_at, candidate_stage_enum, signal_time`
  - derived_fields：`wallet_decision_age_sec, wallet_decision_stale, age_sec, stale, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`wallet_decision_created_at, wallet_decision_stale, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, requires_pattern_review, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：只定义时间上下文，不修改钱包结构评分或角色分类。
- **5｜S5_WALLET_PATTERN_ALIGNMENT｜钱包 × 盘型匹配**
  - source：alignment of wallet decision + pattern output
  - source_paths：
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `data/gmgn_candidates_live_run/site/dashboard_data.json`
    - `wallet_pattern_alignment output`
  - ttl_sec：`900`
  - stale_action：`TEMPORAL_PAUSE_IF_DESYNC`
  - required_input_fields：`wallet_decision_created_at, pattern_created_at`
  - optional_input_fields：`alignment_created_at, signal_time, discovered_at, candidate_stage_enum`
  - derived_fields：`alignment_created_at, alignment_age_sec, alignment_stale, alignment_time_skew_sec, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`alignment_created_at, alignment_stale, alignment_time_skew_sec, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：wallet与pattern时间偏移过大时暂停/复查，不直接放行。
- **6｜S6_DOMINANT_LIFECYCLE｜主导侧生命周期**
  - source：dominant lifecycle classifier
  - source_paths：
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `data/gmgn_candidates_live_run/index/case_file_index.json`
    - `dominant_lifecycle output`
  - ttl_sec：`1800`
  - stale_action：`TEMPORAL_REFRESH_LIFECYCLE`
  - required_input_fields：`lifecycle_created_at, signal_level, wallet_decision_created_at`
  - optional_input_fields：`phase_started_at, lifecycle_transition_at, candidate_stage_enum, pattern_created_at`
  - derived_fields：`lifecycle_age_sec, lifecycle_stale, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`lifecycle_created_at, dominant_lifecycle, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：生命周期过期时刷新或标记证据待复查。
- **7｜S7_DOMINANT_INTENT｜主导侧行为动机**
  - source：operator psychology / intent layer
  - source_paths：
    - `data/gmgn_candidates_live_run/index/case_file_index.json`
    - `data/gmgn_candidates_live_run/site/dashboard_data.json`
    - `operator_psychology output`
  - ttl_sec：`1800`
  - stale_action：`TEMPORAL_REFRESH_INTENT`
  - required_input_fields：`intent_created_at, lifecycle_created_at, signal_level`
  - optional_input_fields：`paper_signal_time, paper_entry_time, candidate_stage_enum, quote_time`
  - derived_fields：`intent_age_sec, intent_stale, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`intent_created_at, dominant_intent, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：行为动机只解释已有证据，不重新裁决。
- **8｜S8_QUOTE_SECURITY_LIQUIDITY｜quote/security/liquidity**
  - source：quote / security / liquidity checks
  - source_paths：
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `quote/security response`
    - `liquidity check output`
  - ttl_sec：`120`
  - stale_action：`TEMPORAL_EXPIRED_NO_ALLOW`
  - required_input_fields：`quote_time, quote_requested_at, quote_received_at, security_scan_time`
  - optional_input_fields：`token_open_time, pool_created_at, last_update_time, liquidity_check_time, source_time`
  - derived_fields：`quote_age_sec, quote_stale, security_scan_age_sec, security_scan_stale, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`quote_time, quote_stale, security_scan_time, security_scan_stale, liquidity_check_status, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：quote_stale=true 不能 TEMPORAL_ALLOW，必须 TEMPORAL_EXPIRED 或刷新。
- **9｜S9_FINAL_TRADE_GATE｜最终交易门禁**
  - source：final gate aggregation
  - source_paths：
    - `data/gmgn_candidates_live_run/live_run_manifest.json`
    - `data/gmgn_candidates_live_run/index/token_detail_index.json`
    - `final gate aggregation`
  - ttl_sec：`180`
  - stale_action：`TEMPORAL_PAUSE_OR_EXPIRED`
  - required_input_fields：`final_gate_created_at, quote_time, security_scan_time`
  - optional_input_fields：`candidate_stage_enum, wallet_decision_created_at, pattern_created_at, lifecycle_created_at`
  - derived_fields：`final_gate_age_sec, final_gate_stale, final_gate_input_time_skew_sec, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`final_gate_created_at, final_gate_stale, final_gate_input_time_skew_sec, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：最终门禁只读取上游；时间不同步不能放行。
- **10｜S10_PAPER_RUNNER｜paper runner**
  - source：paper live runner / paper positions
  - source_paths：
    - `data/gmgn_candidates_live_run/index/latest_open_positions.json`
    - `data/gmgn_candidates_live_run/index/latest_closed_positions.json`
    - `paper runner output`
  - ttl_sec：`86400`
  - stale_action：`TEMPORAL_REVIEW_PAPER_POSITION`
  - required_input_fields：`paper_signal_time, paper_entry_time, entry_time`
  - optional_input_fields：`exit_time, last_update_time, candidate_stage_enum, wallet_decision_created_at`
  - derived_fields：`paper_entry_age_from_signal_sec, paper_entry_age_from_wallet_decision_sec, position_age_sec, holding_duration_sec, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`paper_signal_time, paper_entry_time, entry_time, exit_time, position_age_sec, holding_duration_sec, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：只影响纸面复盘/纸面持仓更新，不触发真实买卖。
- **11｜S11_FAILURE_ATTRIBUTION｜失败归因**
  - source：failure attribution jsonl / case files
  - source_paths：
    - `data/gmgn_candidates_live_run/index/case_file_index.json`
    - `failure attribution jsonl`
    - `paper failure review output`
  - ttl_sec：`604800`
  - stale_action：`TEMPORAL_APPEND_REVIEW_REQUIRED`
  - required_input_fields：`failure_detected_at, entry_time, exit_time`
  - optional_input_fields：`time_to_failure_sec, time_to_max_profit_sec, time_to_max_drawdown_sec, last_update_time, candidate_stage_enum`
  - derived_fields：`failure_detected_at, holding_duration_sec, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`failure_detected_at, time_to_failure_sec, time_to_max_profit_sec, time_to_max_drawdown_sec, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：失败归因允许长TTL；过期表示日报/复盘需要补跑。
- **12｜S12_DAILY_REVIEW｜日报复盘**
  - source：daily report / dashboard / case index
  - source_paths：
    - `data/gmgn_candidates_live_run/events/latest_events.md`
    - `data/gmgn_candidates_live_run/index/system_index.json`
    - `daily report output`
  - ttl_sec：`129600`
  - stale_action：`TEMPORAL_GENERATE_DAILY_REVIEW`
  - required_input_fields：`report_generated_at, last_update_time`
  - optional_input_fields：`report_window_start, report_window_end, sample_first_time, sample_last_time, candidate_stage_enum`
  - derived_fields：`report_generated_at, refresh_required, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - output_fields：`report_generated_at, report_window_start, report_window_end, time_context_gate, temporal_sync_status, temporal_gate, time_context_score, stage_missing_fields`
  - 必备时间字段：`source_time`、`created_at`、`input_window_start`、`input_window_end`、`age_sec`、`ttl_sec`、`stale`、`elapsed_sec`、`time_skew_sec`、`refresh_required`、`stale_action`
  - 说明：日报过期只触发复盘生成/提醒，不改交易逻辑。

## 输出 schema 文件

- `data/gmgn_candidates_live_run/time_context/time_context_schema.json`

schema 顶层包含：

- `schema_version`
- `common_required_time_fields`
- `common_field_definitions`
- `canonical_field_map`
- `enums`
- `temporal_gate_rules`
- `stages`
- `output_contract`
- `existing_time_like_fields_sample`

## 当前目录审查摘要

- 项目目录：`/root/sikk-gmgn`
- Runtime 输出目录：`data/gmgn_candidates_live_run`
- 当前已存在 time_context 目录与旧产物：`time_context_summary.json`、`time_context_summary.csv`、`time_context_report.md`、`time_context_schema.json`
- 本阶段更新：只写入文档与 schema，不改 Python 交易/钱包/paper 代码。

## 当前样本中发现的既有时间字段/路径样本

- `closed_positions[].entry_time`
- `closed_positions[].exit_time`
- `closed_positions[].last_update_time`
- `generated_at`
- `last_update`
- `meta.generated_at`
- `meta.source_last_update`
- `metadata.generated_at`
- `metadata.source_last_update`
- `methodology.exit_plan.time_stop`
- `open_positions[].candidate_discovered_at`
- `open_positions[].entry_time`
- `open_positions[].last_update_time`
- `open_positions[].paper_entry_snapshot.candidate.candidate_discovered_at`
- `open_positions[].paper_entry_snapshot.entry.paper_entry_time`
- `open_positions[].paper_entry_snapshot.signal.signal_time`
- `open_positions[].paper_entry_snapshot.wallet.wallet_decision_time`
- `open_positions[].paper_entry_time`
- `open_positions[].signal_time`
- `open_positions[].wallet_decision_time`
- `opportunities[].last_update`
- `paper_positions.closed[].entry_time`
- `paper_positions.closed[].exit_time`
- `paper_positions.closed[].last_update_time`
- `paper_positions.closed[].paper_entry_time`
- `paper_positions.closed[].paper_last_update_time`
- `paper_positions.closed[].paper_signal_time`
- `paper_positions.open[].candidate_discovered_at`
- `paper_positions.open[].entry_time`
- `paper_positions.open[].last_update_time`
- `paper_positions.open[].paper_entry_snapshot.candidate.candidate_discovered_at`
- `paper_positions.open[].paper_entry_snapshot.entry.paper_entry_time`
- `paper_positions.open[].paper_entry_snapshot.signal.signal_time`
- `paper_positions.open[].paper_entry_snapshot.wallet.wallet_decision_time`
- `paper_positions.open[].paper_entry_time`
- `paper_positions.open[].paper_last_update_time`
- `paper_positions.open[].paper_signal_time`
- `paper_positions.open[].signal_time`
- `paper_positions.open[].wallet_decision_time`
- `paper_positions.strategy_metrics.snapshot_time`
- `paper_positions.strategy_panel.summary.snapshot_time`
- `runtime_outputs`
- `strategy_panel.summary.snapshot_time`
- `system_health.runtime_status`
- `system_health.source_last_update`
- `tokens[].last_update`

## 缺失字段处理原则

现有 runtime 数据尚未保证每个阶段都提供统一的 `source_time/created_at/input_window_start/input_window_end/age_sec/ttl_sec/stale/elapsed_sec/time_skew_sec/refresh_required/stale_action`。
阶段 1.1 不强行回填、不改逻辑，只将缺失字段列入后续阶段 1.2 的接入任务。

## 阶段 1.2 实现 sikk_time_context_gate.py 的边界

- 只读读取现有文件。
- 不改变状态机交易动作。
- 不修改钱包结构。
- 不修改 paper runner。
- 只输出 `time_context_summary.json` / `time_context_summary.csv` / `time_context_report.md`。
- 缺字段写 `null` 并进入 `missing_fields`。
- 每个候选 token 都必须输出一行。

## 阶段 1.2 前置条件

可以进入阶段 1.2 的条件：

- 本文档存在。
- JSON schema 存在。
- 0-12 阶段均有时间字段、TTL、stale_action。
- 特殊硬规则已写入 schema。
- 未修改交易逻辑、钱包结构逻辑、paper runner。
