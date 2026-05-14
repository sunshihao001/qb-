# Phase 01 Data Fact Asset Matrix

本文件是 `sikk-phase01-data-fact-skill` 的隔离参考资料，用于记录数据事实层可复用数据资产、互相调节关系、污染风险和下游交接方式。

## Layer Purpose

Phase 01 数据事实层只回答：

- 有哪些原始数据？
- 每个字段来自哪里？
- 字段是否存在、可信度如何、缺什么？
- 哪些标准事实可以交给 Phase 02？
- 哪些模型因为缺字段必须降级或禁止？

Phase 01 不回答：

- 是否庄家控盘。
- 是否可以买。
- 是否二段扩张。
- 是否 PAPER_READY / BLOCKED。
- 是否执行交易。

## Asset Groups

### Runtime / Snapshot

- `run_id`
- `token_address`
- `chain`
- `run_mode`
- `data_snapshot_time`
- `raw_source_manifest.json`

调节作用：统一所有事实的时间截面，防止不同时间的数据混算。

### Token Fact

标准输出：

```text
01_data_fact/normalized/token_fact.json
```

用途：固定分析对象身份，是所有下游表的 join anchor。

调节对象：quote/security/kline/holder/trade 都必须回到同一 token identity。

### Wallet Fact

标准输出：

```text
01_data_fact/normalized/wallet_fact_table.csv
```

Source Wallet Bot 相关产物：

```text
wallet_trade_normalized.json
wallet_entity_profile_normalized.json
gmgn_wallet_tags_normalized.json
```

用途：单钱包事实、标签、成本、持仓、候选结构钱包证据。

调节对象：holder、trade、transfer、funding、same_source。

### Trade Fact

标准输出：

```text
01_data_fact/normalized/trade_fact_table.csv
```

用途：主动买卖事实。

调节规则：

- 与 transfer 区分主动买入和 token 转入。
- 与 holder 校验当前余额。
- 与 kline 提供买卖发生时的市场时间背景。

### Transfer Fact

标准输出：

```text
01_data_fact/normalized/transfer_fact_table.csv
```

用途：token 转入、分发接收、空投接收、来源未知。

调节规则：

- transfer-in 无 buy trade 时，不得生成主动买入成本。
- transfer-out 可影响 current_balance，但不得自动解释为派发完成。

### Holder Fact

标准输出：

```text
01_data_fact/normalized/holder_fact_table.csv
```

用途：持仓分布、top holders、holder count、balance distribution。

调节规则：

- 与 wallet current_balance 双向校验。
- 与 snapshot delta 组合形成筹码变化事实。

### Kline Fact

标准输出：

```text
01_data_fact/normalized/kline_fact_table.csv
```

用途：市场时序背景。

调节规则：

- 只作为事实背景，不输出二段扩张判断。
- 与 trade time 对齐，提供价格/成交环境。

### Quote Fact

标准输出：

```text
01_data_fact/normalized/quote_fact.json
```

用途：价格、流动性、slippage 背景。

调节规则：

- 与 security 一起决定哪些下游模型可用。
- 缺失时写入 `missing_fields` 和 `restricted_models`。

### Security Fact

标准输出：

```text
01_data_fact/normalized/security_fact.json
```

用途：mint/freeze authority、tax、burn、liquidity lock/security flags。

调节规则：

- 缺失不必自动 BLOCK。
- 但禁止下游强通过风险判断。

### Funding Source Fact

标准输出参考：

```text
funding_flow_normalized.json
funding_source_normalized.json
```

用途：买入前 SOL/USDC 来源、疑似同源资金组。

调节规则：

- 可生成同源候选。
- CEX-only / common exchange 不得确定同源。
- 必须携带 evidence_basis/confidence/risk_level。

### Backflow Fact

标准输出参考：

```text
backflow_paths_normalized.json
```

用途：卖后利润回流路径事实。

调节规则：

- 回流同地址可升级同源证据。
- 缺失时写 `need_onchain_followup`，不得补造路径。

### Same-source Evidence

标准输出参考：

```text
same_source_evidence_normalized.json
same_source_groups.json
```

用途：同源候选证据底座。

证据来源：

- by_funding_source
- by_backflow_address
- by_path_signature
- by_gmgn_tag_set

调节规则：

- 输出候选同源、证据等级、风险等级。
- 不输出确定同伙。

### Snapshot Delta

标准输出参考：

```text
wallet_snapshot_delta_source.json
holder_delta_normalized.json
```

用途：多快照余额变化、holder 变化、筹码变化事实。

调节规则：

- 可以进入 chip_distribution_summary。
- 不得输出吸筹完成/派发完成。

### Aggregate Wallet Fact Package

标准输出：

```text
wallet_structure_normalized.json
chip_distribution_summary.json
same_source_groups.json
fund_flow_edges.csv
address_history.json
wallet_fact_package_manifest.json
wallet_fact_report.md
```

用途：把分散 facts 固化为 Phase 02/behavior_inference 可读的稳定 HER cache artifact。

## Mutual Adjustment Summary

```text
Runtime snapshot anchors all data.
Token fact anchors all tables.
Trade × Transfer separates active buy/sell from token movement.
Wallet × Holder validates current balance and holder distribution.
Quote × Security gates downstream risk models.
Funding × Same-source creates weak/medium same-source candidate evidence.
Backflow × Same-source upgrades evidence when paths converge.
Snapshot delta × Chip summary records change without behavior conclusion.
GMGN tags × Wallet role candidates gives strong hint but remains candidate-level.
Quality gate carries missing/restricted constraints forward.
```

## Pollution Control

Never ingest as upstream facts:

- downstream reports
- paper runner output
- state machine output
- trading decisions
- Telegram interpretation text
- old generated reports unless explicitly imported under legacy read-only mode

If such data is useful, store as reference/report only, not normalized fact.
