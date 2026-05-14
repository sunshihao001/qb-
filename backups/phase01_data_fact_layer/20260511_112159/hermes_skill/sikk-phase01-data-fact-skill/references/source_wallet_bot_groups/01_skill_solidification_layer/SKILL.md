---
name: sikk-phase01-data-fact-skill
description: "Use when designing, rebuilding, auditing, or running the SIKK/Wallet-Intel Phase 01 data-fact layer as an isolated reusable HER skill: enumerate usable source data, normalize facts, produce quality gates and handoff packets, and prevent inference/trading contamination."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sikk, wallet-intel, phase-01, data-fact, source-wallet-bot, handoff-contracts, data-pollution-control]
    related_skills: [ai-collaboration-harness, her-logic-kv-cache-pattern, hermes-agent-skill-authoring]
---

# SIKK Phase 01 Data Fact Skill

## Overview

这是 SIKK / Wallet-Intel 系统的数据事实层可复用 skill。它把“数据事实层”从杂乱项目目录中抽离成一个可调用、可审计、可复现的 HER 子能力。

核心原则：

```text
Phase 01 只做事实采集、字段标准化、质量门禁、缺失显式化、handoff。
Phase 01 不做结构动机推断、不做交易判断、不输出执行建议。
```

在 HER KV-cache 逻辑中，Phase 01 的产物就是下游结构分析的稳定事实缓存：下游 Phase 02/Intel Bot 不应该重复读取 raw、聊天记录、dashboard、paper runner 或报告反推事实，而应读取 Phase 01 的标准输出和质量门禁。

## When to Use

Use when the user asks to:

- 整理钱包结构分析项目的数据事实层。
- 把 Phase 01 设计成可复用 skill / 可调用能力。
- 扫描哪些数据能进入数据事实层。
- 设计 Source Wallet Bot / wallet_fact 的输入、输出、质量门禁、handoff。
- 防止 dashboard、paper、report、case file 反推污染事实层。
- 为 Phase 02 钱包结构分析准备标准上游数据。
- 将可复现系统设计沉淀成 HER 底层逻辑子 skill。

Do not use for:

- 主导侧动机判断。
- PAPER_READY / BLOCKED / final_trade_gate。
- 买卖信号、真实执行、签名、广播、swap。
- 从下游报告反推上游事实。

## Project Boundary

Canonical project root:

```text
/root/sikk-gmgn/
```

Primary Source Wallet Bot data root:

```text
data/source_wallet_bot/<mode>/<token_address>/
```

Canonical token layout:

```text
data/source_wallet_bot/<mode>/<token_address>/
├── wallet_data/
│   ├── raw/
│   ├── normalized/
│   └── summary/
├── structure_analysis/
│   ├── wallet_fact/
│   ├── intelligence/
│   ├── handoff/
│   └── reports/
└── manifest/
```

Forbidden new primary roots:

- `/root/sikk-wallet-intel/` as new wallet-structure primary data root.
- `data/gmgn_candidates_live_run/` as new Source Wallet Bot write root.
- project root scattered `.json` / `.csv` / `.md` runtime outputs.

## Phase 01 Responsibility

Phase 01 accepts input data, normalizes it, scores quality, and creates a handoff packet.

Allowed outputs:

- 字段存在 / 缺失。
- 来源优先级。
- 数据质量分。
- `PASS` / `PASS_WITH_WARNING` / `PAUSE` / `BLOCK`.
- `restricted_models`.
- Phase 01 → Phase 02 handoff packet.

Forbidden outputs:

- 确定庄家。
- 可以买 / 强烈建议买入。
- 吸筹完成 / 派发完成。
- 主力控盘。
- 二段扩张概率高。
- 真实交易执行建议。
- `buy_signal`, `sell_signal`, `trade_allowed`, `execute_now`, `PAPER_READY`, `BLOCKED`.

## Usable Data Assets in Phase 01

### 1. Runtime config

Required config fields:

- `run_id`
- `token_address`
- `chain`
- `run_mode`
- `data_snapshot_time`

Purpose:

- 固定本次事实快照。
- 防止回测污染和时间穿越。
- 给后续所有文件提供同一运行上下文。

### 2. Raw source manifest

Canonical output:

```text
01_data_fact/raw/raw_source_manifest.json
```

Purpose:

- 记录每个 raw source 的来源、抓取时间、可信等级、文件路径、记录数。
- 让后续审计可以追溯字段来源。

### 3. Token fact

Canonical output:

```text
01_data_fact/normalized/token_fact.json
```

Source candidates:

- manual config
- chain
- GMGN
- quote/security sources

Purpose:

- 固定 token identity、chain、mint、snapshot time、基础状态。
- 下游 phase 用它确认分析对象，不再从 chat 或 URL 重猜 token。

### 4. Wallet fact table

Canonical output:

```text
01_data_fact/normalized/wallet_fact_table.csv
```

Related Source Wallet Bot outputs:

```text
wallet_data/normalized/wallet_trade_normalized.json
wallet_data/normalized/wallet_entity_profile_normalized.json
wallet_data/normalized/gmgn_wallet_tags_normalized.json
```

Purpose:

- 标准化单钱包事实。
- 支撑成本、持仓、退出、GMGN 标签、fresh/sniper/bundle/insider/whale hint。
- 只给出证据字段和候选标签，不给确定性庄家结论。

### 5. Trade fact table

Canonical output:

```text
01_data_fact/normalized/trade_fact_table.csv
```

Source candidates:

- GMGN traders
- GMGN wallet trade
- GMGN trader detail
- on-chain DEX swap records

Purpose:

- 买卖行为事实。
- 支撑单钱包成本、买入/卖出统计、时间窗口、交易方向。
- 与 transfer facts 互相校验，避免把 token transfer-in 误当成主动买入。

### 6. Holder fact table

Canonical output:

```text
01_data_fact/normalized/holder_fact_table.csv
```

Source candidates:

- GMGN holders
- chain holder snapshot

Purpose:

- 持仓结构事实。
- 支撑 top holders、holder count、balance distribution、tracked balance。
- 与 wallet/trade facts 联动校验当前 balance 是否合理。

### 7. Kline fact table

Canonical output:

```text
01_data_fact/normalized/kline_fact_table.csv
```

Purpose:

- 市场时序事实。
- 为后续结构阶段提供价格/时间背景。
- Phase 01 不解释“二段扩张概率”，只交付 kline facts。

### 8. Quote fact

Canonical output:

```text
01_data_fact/normalized/quote_fact.json
```

Related Source Wallet Bot output:

```text
wallet_data/normalized/quote_security_normalized.json
```

Source candidates:

- OKX quote
- GMGN quote
- read-only scan providers

Purpose:

- liquidity、price、quote amount、slippage/security context。
- 只作为事实背景，不输出交易许可。

### 9. Security fact

Optional canonical output:

```text
01_data_fact/normalized/security_fact.json
```

Purpose:

- mint/freeze authority、tax、burn/liquidity/security flags。
- 若缺失，不允许下游强通过，应写入 missing/restricted_models。

### 10. Transfer fact table

Optional canonical output:

```text
01_data_fact/normalized/transfer_fact_table.csv
```

Related Source Wallet Bot outputs:

```text
wallet_data/normalized/token_transfer_normalized.json
wallet_data/normalized/token_source_classification_base.json
```

Purpose:

- 区分主动买入、token 转入、分发接收、空投接收、来源未知。
- 防止把 transfer-in 当成真实买入成本。

### 11. Funding source facts

Related Source Wallet Bot outputs:

```text
wallet_data/normalized/funding_flow_normalized.json
wallet_data/normalized/funding_source_normalized.json
```

Purpose:

- 买入前 SOL / USDC 来源。
- 支撑弱同源证据。
- CEX-only 是弱证据，不得直接确定同源。

### 12. Backflow facts

Related Source Wallet Bot output:

```text
wallet_data/normalized/backflow_paths_normalized.json
```

Purpose:

- 卖后利润回流路径事实。
- 可升级同源/回流候选证据。
- 若缺失，写 `need_onchain_followup`，不得补造。

### 13. Same-source evidence base

Related Source Wallet Bot output:

```text
structure_analysis/intelligence/same_source_evidence_normalized.json
```

Purpose:

- by_funding_source
- by_backflow_address
- by_path_signature
- by_gmgn_tag_set

Phase 01/Source Bot 只能输出候选同源证据、证据等级、风险等级；不得输出确定同伙。

### 14. Snapshot delta facts

Related Source Wallet Bot outputs:

```text
wallet_data/normalized/wallet_snapshot_delta_source.json
wallet_data/normalized/holder_delta_normalized.json
```

Purpose:

- 多快照持仓变化。
- 派发进度变化的事实底座。
- Phase 01 不判断“派发完成”，只输出变化事实与缺失情况。

### 15. Wallet fact aggregate package

Canonical Source Wallet Bot package:

```text
structure_analysis/wallet_fact/wallet_structure_normalized.json
structure_analysis/wallet_fact/chip_distribution_summary.json
structure_analysis/wallet_fact/same_source_groups.json
structure_analysis/wallet_fact/fund_flow_edges.csv
structure_analysis/wallet_fact/address_history.json
structure_analysis/wallet_fact/wallet_fact_package_manifest.json
structure_analysis/reports/wallet_fact_report.md
```

Purpose:

- 把分散 normalized facts 聚合为下游可读事实包。
- 是 Phase 02 / behavior_inference 的稳定 HER cache artifact。

## Adjustment Logic Between Data Assets

### Trade × Transfer

Rule:

```text
trade_fact 负责主动买卖；transfer_fact 负责 token 转入/转出。
若某钱包当前持仓来自 transfer-in，而无 buy trade，则不得计算为主动买入成本。
```

Effect:

- 降低伪成本污染。
- 防止把分发接收钱包误判成主动建仓钱包。

### Wallet × Holder

Rule:

```text
wallet_fact_table 的 current_balance 应与 holder_fact_table / holder snapshot 互相校验。
若两者冲突，保留 source provenance，并在 anomaly_fields_report.csv 中记录。
```

Effect:

- 找出抓取时点差、source 不一致、精度问题。

### Quote × Security

Rule:

```text
quote_fact 给流动性/价格背景；security_fact 给合约与权限安全背景。
任一缺失都不自动 BLOCK，但必须进入 quality_gate.missing_fields 与 restricted_models。
```

Effect:

- 后续阶段知道哪些模型不能强判断。

### Funding × Same-source

Rule:

```text
funding_source 可生成 same_source 候选，但 CEX-only / common exchange 出金不能作为确定同源。
同源必须携带 evidence_basis、confidence、risk_level。
```

Effect:

- 保护同源判断不被弱资金来源污染。

### Backflow × Same-source

Rule:

```text
卖后回流到同一地址可提高同源证据等级，但必须保留路径、时间、金额、资产与 source_type。
```

Effect:

- 把“利润回收”从直觉判断转成可审计边表。

### Snapshot delta × Chip distribution

Rule:

```text
delta facts 只描述余额/holder 变化；chip_distribution_summary 聚合筹码集中和变化。
不得在 Phase 01 输出派发完成、吸筹完成等行为结论。
```

Effect:

- 把后续结构判断所需素材提前固化，但不越界。

### GMGN tags × Role candidates

Rule:

```text
GMGN 标签可作为强 hint；早期买入 + bundler/sniper/insider 等标签可升为“疑似结构钱包候选”。
仍必须使用“疑似/候选”措辞，并输出 evidence fields。
```

Effect:

- 既不过度保守，也不做确定性内幕/庄家判断。

## Quality Gate

Canonical output:

```text
01_data_fact/audit/phase_01_quality_gate.json
```

Allowed statuses:

- `PASS`
- `PASS_WITH_WARNING`
- `PAUSE`
- `BLOCK`

Required quality fields:

- `run_id`
- `token_address`
- `data_snapshot_time`
- `quality_score`
- `phase_01_gate_status`
- `missing_fields`
- `restricted_models`

Missing rule:

```text
任何缺失字段必须显式写为 missing，不允许用 0 或空字符串替代。
```

## Handoff Contract

Canonical Phase 01 → Phase 02 files:

```text
01_data_fact/normalized/token_fact.json
01_data_fact/normalized/kline_fact_table.csv
01_data_fact/normalized/trade_fact_table.csv
01_data_fact/normalized/holder_fact_table.csv
01_data_fact/normalized/quote_fact.json
01_data_fact/audit/phase_01_quality_gate.json
```

Optional files:

```text
01_data_fact/normalized/security_fact.json
01_data_fact/normalized/transfer_fact_table.csv
01_data_fact/audit/field_quality_report.json
```

Downstream must carry forward:

- `quality_score`
- `phase_01_gate_status`
- `missing_fields`
- `restricted_models`
- `data_snapshot_time`

Forbidden downstream behavior:

- Phase 02 不得忽略 Phase 01 的 missing 字段。
- Phase 02 不得把缺失 security 的样本判定为强通过。
- Phase 02 不得使用 Phase 01 未输出的字段进行判断。
- Phase 02 不得覆盖 Phase 01 的 BLOCK 状态。

## Standard Run Procedure

1. Classify the task as `phase_01_data_fact`.
2. Resolve primary root under `/root/sikk-gmgn/`.
3. Resolve token layout under `data/source_wallet_bot/<mode>/<token_address>/` or stable runtime `01_data_fact/` layout.
4. Read contracts and schemas before writing:
   - `contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json`
   - `contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json`
   - `contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json`
   - `schemas/stable_trader_os/phase_01_data_fact/*.json`
5. Inventory available raw sources.
6. Normalize each fact table with source provenance.
7. Cross-check fact tables and record anomalies.
8. Write quality gate, missing fields, anomaly report, runtime trace.
9. Write handoff packet.
10. Verify no forbidden judgment/output fields appear.

## Canonical Project Files to Check

Contracts:

```text
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_forbidden_judgement_contract.md
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json
```

Schemas:

```text
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/token_fact_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/wallet_fact_table_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/trade_fact_table_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/holder_fact_table_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/kline_fact_table_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/quote_fact_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/security_fact_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/transfer_fact_table_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/phase_01_quality_gate_schema.json
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/phase_01_field_schema.json
```

Source Wallet Bot files:

```text
/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_builder.py
/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_output_contract.md
/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_schema_index.json
/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_architecture.md
/root/sikk-gmgn/modules/source_wallet_bot/wallet_trade_normalizer.py
/root/sikk-gmgn/modules/source_wallet_bot/wallet_profile_normalizer.py
/root/sikk-gmgn/modules/source_wallet_bot/source_group_engine.py
/root/sikk-gmgn/modules/source_wallet_bot/handoff_exporter.py
/root/sikk-gmgn/modules/source_wallet_bot/schema_validator.py
/root/sikk-gmgn/modules/source_wallet_bot/path_resolver.py
/root/sikk-gmgn/modules/source_wallet_bot/directory_governance.py
/root/sikk-gmgn/modules/source_wallet_bot/gmgn_live_adapter.py
/root/sikk-gmgn/modules/source_wallet_bot/gmgn_okx_readonly_adapter.py
```

Examples:

```text
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/mock_phase_01_input.json
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/mock_raw_gmgn_holders.json
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/mock_raw_gmgn_traders.json
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/mock_raw_kline.json
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/expected_token_fact.json
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/expected_wallet_fact_table.csv
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/expected_trade_fact_table.csv
/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/expected_phase_01_quality_gate.json
```

## Common Pitfalls

1. **把报告当事实源。** Reports are human-readable outputs, not upstream fact sources.
2. **把 dashboard/paper runner 反推成事实。** This creates circular evidence and time pollution.
3. **缺失字段用 0 填充。** Missing must be explicit `missing`, not zero.
4. **Phase 01 过早下判断。** It may output candidate/evidence fields but not motive or trading conclusions.
5. **忽略 snapshot time。** Every fact package must carry `data_snapshot_time` to prevent time leakage.
6. **同源证据过强。** CEX-only, common funding source, or tag overlap cannot become deterministic same-source.
7. **目录污染。** New runtime outputs must not be scattered in root or legacy runtime folders.

## Verification Checklist

- [ ] Task is classified as Phase 01 data fact.
- [ ] Primary root is `/root/sikk-gmgn/`.
- [ ] Output path follows `data/source_wallet_bot/<mode>/<token_address>/` or approved stable runtime layout.
- [ ] Contracts and schemas were read before output design.
- [ ] All missing fields are explicit `missing`.
- [ ] Source provenance exists for each normalized field/table.
- [ ] Quality gate exists with legal status.
- [ ] Handoff packet exists and points to required normalized files.
- [ ] Downstream restrictions are carried forward.
- [ ] No forbidden trading or deterministic dealer/insider language appears.
