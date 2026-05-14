# Phase 01 Data Fact Run Checklist

用于每次调用 `sikk-phase01-data-fact-skill` 时执行。

## 0. Boundary Check

- [ ] 当前任务属于数据事实层。
- [ ] 项目主目录为 `/root/sikk-gmgn/`。
- [ ] 不写入 `/root/sikk-wallet-intel/` 作为新事实主目录。
- [ ] 不触碰 private keys / signing / broadcasting / swap / real execution。

## 1. Required Contract Read

- [ ] `contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json`
- [ ] `contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json`
- [ ] `contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json`
- [ ] `contracts/stable_trader_os/phase_01_data_fact/phase_01_forbidden_judgement_contract.md`
- [ ] `contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json`

## 2. Required Schema Read

- [ ] `token_fact_schema.json`
- [ ] `wallet_fact_table_schema.json`
- [ ] `trade_fact_table_schema.json`
- [ ] `holder_fact_table_schema.json`
- [ ] `kline_fact_table_schema.json`
- [ ] `quote_fact_schema.json`
- [ ] `security_fact_schema.json`
- [ ] `transfer_fact_table_schema.json`
- [ ] `phase_01_quality_gate_schema.json`
- [ ] `phase_01_field_schema.json`

## 3. Source Inventory

- [ ] raw GMGN holders
- [ ] raw GMGN traders
- [ ] raw kline
- [ ] wallet trade detail
- [ ] wallet profile / GMGN tag
- [ ] token transfer
- [ ] funding source
- [ ] backflow path
- [ ] quote/security
- [ ] source manifest

## 4. Normalize

- [ ] `token_fact.json`
- [ ] `wallet_fact_table.csv`
- [ ] `trade_fact_table.csv`
- [ ] `holder_fact_table.csv`
- [ ] `kline_fact_table.csv`
- [ ] `quote_fact.json`
- [ ] optional `security_fact.json`
- [ ] optional `transfer_fact_table.csv`
- [ ] optional funding/backflow/same-source facts

## 5. Cross-check

- [ ] Trade × Transfer: active buy/sell vs token movement separated.
- [ ] Wallet × Holder: current balance reconciled or anomaly recorded.
- [ ] Quote × Security: restricted models updated if missing.
- [ ] Funding × Same-source: CEX-only not promoted to deterministic same-source.
- [ ] Backflow × Same-source: path evidence preserved.
- [ ] Snapshot delta × Chip: no accumulation/distribution conclusion in Phase 01.

## 6. Audit Outputs

- [ ] `phase_01_quality_gate.json`
- [ ] `field_quality_report.json`
- [ ] `anomaly_fields_report.csv`
- [ ] `phase_01_runtime_trace.jsonl`
- [ ] `raw_source_manifest.json`

## 7. Handoff

- [ ] Required files exist for Phase 02.
- [ ] `quality_score` carried forward.
- [ ] `phase_01_gate_status` carried forward.
- [ ] `missing_fields` carried forward.
- [ ] `restricted_models` carried forward.
- [ ] `data_snapshot_time` carried forward.

## 8. Forbidden Output Scan

Search output for forbidden terms:

```text
确定庄家
可以买
强烈建议买入
吸筹完成
派发完成
主力控盘
二段扩张概率高
buy_signal
sell_signal
trade_allowed
execute_now
PAPER_READY
real_execution
swap
signing
broadcast
```

Any match must be removed or moved to downstream non-Phase-01 context with explicit boundary.
