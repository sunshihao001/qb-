# SIKK-GMGN Runtime Contract v1｜结构情报 → 交易系统数据契约

## 1. Contract Scope

本契约定义 GMGN/SIKK 结构分析如何成为交易系统可消费的数据，而不是独立报告。

安全边界：paper-only；不读取私钥；不签名；不广播；不真实 swap。

## 2. Allowed Final Statuses

只允许输出：

- `EXCLUDE`
- `RECORD_ONLY`
- `RISK_MONITOR`
- `OBSERVE`
- `PAPER_CANDIDATE`
- `LIVE_CANDIDATE_REQUIRES_HUMAN_CONFIRMATION`

禁止输出：

- `BUY_NOW`
- `SELL_NOW`
- `AUTO_TRADE`
- `GUARANTEED_PROFIT`
- `CONFIRMED_DEALER`

## 3. Objects

### 3.1 TokenIntakePayload

必填：

- `token_address`: string
- `chain`: string, e.g. `sol`
- `mode`: `live|paper|backtest|manual_review`
- `source`: `telegram|gmgn|manual|cron|fixture`
- `received_at`: ISO UTC timestamp
- `requested_by`: string
- `safety_boundary`: object

### 3.2 GMGNRawSnapshot

必填：

- `token_address`
- `chain`
- `snapshot_at`
- `token_info`
- `security`
- `pool`
- `holders`
- `traders`
- `wallet_tags`
- `source_commands`
- `missing_sections`

### 3.3 WalletEntityProfile

单钱包字段：

- `address`
- `role_candidate`
- `level`: `E0|E1|E2|E3|E4|R1|R2|R3|I0|I1|I2|I3|I4|I5`
- `action_code`: `A0|A1|A2|A3|A4|A5|R|I`
- `is_infra`
- `is_excluded_from_wallet_scoring`
- `tags`
- `buy_usd`
- `sell_usd`
- `realized_pnl_usd`
- `unrealized_pnl_usd`
- `holding_pct`
- `funding_status`
- `evidence_refs`

### 3.4 StructuralIntelResult

必填：

- `token_address`
- `chain`
- `analysis_window`: `W1|W2|W3|W4|UNKNOWN`
- `structure_activity_score`: `LOW|MEDIUM|HIGH|UNKNOWN`
- `early_execution_strength`: `NONE|WEAK|MEDIUM|STRONG|UNKNOWN`
- `bundler_pressure`: `LOW|MEDIUM|HIGH|UNKNOWN`
- `sniper_density`: `LOW|MEDIUM|HIGH|UNKNOWN`
- `fresh_wallet_rate`: number or enum
- `holder_concentration`: `LOW|MEDIUM|HIGH|UNKNOWN`
- `transfer_in_risk`: `NONE|LOW|MEDIUM|HIGH|NEEDS_SOURCE_CHECK|UNKNOWN`
- `smart_kol_distribution_state`: string
- `chase_risk`: `LOW|MEDIUM|MEDIUM_HIGH|HIGH|UNKNOWN`
- `funding_status`: string
- `wallet_profiles`: list of WalletEntityProfile
- `missing_evidence`: list
- `counter_evidence`: list

### 3.5 EvidenceBundle

必填：

- `evidence_level`: `LOW|MEDIUM|HIGH`
- `source_files`
- `source_commands`
- `observed_at`
- `time_context_policy`
- `assumptions`
- `gaps`
- `degraded_continuation_allowed`: boolean

### 3.6 TradeGateDecision

必填：

- `token_address`
- `final_status`: Allowed Final Status
- `signal_level`: `S0|S1|S2|S3|S4|SX`
- `permission`: `BLOCK_BUY_禁止买入|PAUSE_NEED_CONFIRM_需要人工确认|ALLOW_PAPER_TRADE_允许纸面交易|ALLOW_SMALL_REAL_WITH_CONFIRM_极小仓实盘需确认`
- `risk_level`: `低|中|高|UNKNOWN`
- `block_reasons`
- `pause_reasons`
- `allow_reasons`
- `missing_evidence`
- `human_confirmation_required`: boolean
- `real_trade_enabled`: false

### 3.7 RiskControlProfile

必填：

- `liquidity_usd`
- `min_liquidity_usd`
- `slippage_pct`
- `price_impact_pct`
- `security_risk_level`
- `is_honeypot`
- `can_sell`
- `quote_available`
- `early_wallet_clearout_ratio`
- `data_delayed`
- `wallet_evidence_missing`

### 3.8 ExecutionIntent

仅纸面/观察：

- `intent_type`: `OBSERVE|PAPER_ENTER|PAPER_EXIT|PAPER_HOLD|REVIEW_ONLY`
- `position_plan`
- `exit_plan`
- `requires_human_confirmation`
- `real_swap_enabled`: false
- `signing_enabled`: false
- `broadcast_enabled`: false

### 3.9 ExecutionResult

纸面结果：

- `paper_trade_id`
- `entry_time`
- `entry_price`
- `exit_time`
- `exit_price`
- `max_unrealized_pnl_pct`
- `max_drawdown_pct`
- `final_return_pct`
- `final_r_multiple`
- `exit_reason`

### 3.10 ReviewWriteback

复盘回写：

- `review_id`
- `token_address`
- `input_decision_ref`
- `execution_result_ref`
- `what_worked`
- `what_failed`
- `false_positive_signals`
- `false_negative_signals`
- `rule_update_candidates`
- `memory_candidate`: false by default
- `skill_update_candidate`: optional

## 4. Routing

- Source wallet primary root: `data/source_wallet_bot/{mode}/{token_address}/`
- Intel bot root: `data/intel_bot/{mode}/{token_address}/`
- Strategy gate root: `data/strategy_gate_bot/{mode}/{token_address}/`
- Execution risk root: `data/execution_risk_bot/{mode}/{token_address}/`
- Review ops root: `data/review_ops_bot/{mode}/{token_address}/`
- Legacy live run root: `data/gmgn_candidates_live_run/` remains keep-in-place runtime output, not new wallet primary write root.

## 5. Gate Rules

- Infra/CEX/LP/router/program/suspicious hub/recovery/token distributor must bypass normal wallet scoring.
- Missing funding path is `资金待查` and must not block paper observation by itself.
- Funding/same-source/backflow are optional unless task explicitly asks.
- `BLOCK_BUY` dominates all positive signals.
- `PAUSE_NEED_CONFIRM` downgrades S3/S4 to human-confirm observation unless paper-only test explicitly allows.
- S4 cannot authorize real trade.

## 6. Acceptance

- Contract file exists under `contracts/shared/trading_structure_control/`.
- Planbook references this contract.
- Planbook repository validation indexes the planbook.
- Focused tests pass: `python3 -m pytest tests/test_sikk_auto_framework.py tests/test_sikk_automation_workflow.py tests/test_planbook_repository.py -q`.
