# SIKK OKX/GMGN Paper Live Runner Implementation Plan

> **For Hermes:** Use TDD; do not add any real swap execution path.

**Goal:** Add a paper-live runner that can run for several days using OKX/GMGN read-only price evidence to validate SIKK strategy viability before controlled real-execution permissions are considered.

**Architecture:** The runner consumes existing candidate state, signal summary, and quote/security summary outputs. It maintains paper open/closed positions, writes trade events, metrics, risk events, and a Chinese daily report. It accepts an injected read-only `price_provider` for tests/future orchestrators; the CLI default uses only OKX read-only `onchainos market price --address <token> --chain solana` and blocks swap/execute snippets.

**Tech Stack:** Python stdlib JSON/CSV, existing SIKK output schemas, pytest.

---

### Task 1: Add failing paper-live tests

**Files:**
- Create: `tests/test_sikk_paper_live_runner.py`

**Objective:** Cover paper entry, existing-position update, stop-loss exit, risk block skip, daily outputs, and no duplicate re-entry.

**Verification:**

```bash
cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_paper_live_runner.py -q
```

Expected first run: fail with `ModuleNotFoundError: No module named 'sikk_paper_live_runner'`.

### Task 2: Implement runner

**Files:**
- Create: `sikk_paper_live_runner.py`

**Objective:** Implement `run_paper_live_cycle(...)` with an injected `price_provider`, writing:

```text
paper_positions_open.json
paper_positions_closed.json
paper_trades.csv
paper_equity_curve.csv
strategy_metrics.json
risk_events.jsonl
daily_reports/paper_daily_report_YYYYMMDD.md
```

**Safety boundaries:**

```text
- No gmgn-cli swap.
- No onchainos swap execute.
- No signing/broadcast/private-key handling.
- Default CLI price source only runs OKX read-only `onchainos market price`.
- Entry is paper-only and gated by PAPER_READY plus quote/security not BLOCK.
```

### Task 3: Verify

```bash
cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_paper_live_runner.py -q
python3 -m py_compile sikk_paper_live_runner.py
```

### Task 4: Full regression and forbidden command check

```bash
cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_paper_live_runner.py tests/test_sikk_transaction_broadcast_guard.py tests/test_sikk_execution_state_machine.py tests/test_sikk_candidate_quote_security_pipeline.py tests/test_run_sikk_gmgn_pipeline.py tests/test_sikk_candidate_state_machine.py tests/test_sikk_candidate_signal_pipeline.py tests/test_sikk_candidate_kline_pipeline.py tests/test_sikk_gmgn_new_token_filter.py tests/test_sikk_live_collectors.py tests/test_sikk_quote_security_outputs.py tests/test_sikk_trade_confirmation_ticket.py tests/test_sikk_execution_adapters.py tests/test_sikk_auto_framework.py -q
python3 -m py_compile sikk_paper_live_runner.py sikk_transaction_broadcast_guard.py sikk_execution_state_machine.py run_sikk_gmgn_pipeline.py sikk_candidate_quote_security_pipeline.py sikk_candidate_state_machine.py sikk_candidate_signal_pipeline.py sikk_candidate_kline_pipeline.py sikk_gmgn_new_token_filter.py sikk_live_quote_security_collector.py sikk_quote_security_review.py sikk_trade_confirmation_ticket.py sikk_execution_adapter_base.py sikk_gmgn_quote_adapter.py sikk_okx_quote_adapter.py sikk_pre_trade_security_checker.py sikk_real_trade_guard.py sikk_auto_trade_types.py sikk_auto_risk_gate.py sikk_auto_signal_engine.py sikk_auto_position_sizer.py sikk_auto_exit_planner.py sikk_paper_trading_engine.py sikk_trade_journal.py sikk_auto_readiness_runner.py
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|gmgn-cli order strategy create\|order strategy create\|onchainos swap execute\|swap execute" sikk_paper_live_runner.py tests/test_sikk_paper_live_runner.py
```
