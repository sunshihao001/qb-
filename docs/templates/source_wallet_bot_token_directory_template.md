# Source Wallet Bot 目录模板

本模板受 `docs/system_directory_constitution.md` 约束。

## token 输出根目录

```text
data/source_wallet_bot/<mode>/<token_address>/
```

`mode` 允许：

- `live`
- `ad_hoc`
- `staging`
- `legacy`
- `audit`

## 标准目录

```text
<token_address>/
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

## wallet_data/raw

只放只读采集原始数据或采集输入：

- `gmgn_wallet_rows_raw.json`
- `gmgn_wallet_trade_input.json`
- `gmgn_wallet_profile_input.json`

## wallet_data/normalized

只放钱包事实标准化数据：

- `wallet_trade_normalized.json`
- `wallet_entity_profile_normalized.json`
- `token_transfer_normalized.json`
- `token_source_classification_base.json`
- `funding_flow_normalized.json`
- `funding_source_normalized.json`
- `backflow_paths_normalized.json`
- `gmgn_wallet_tags_normalized.json`
- `wallet_snapshot_delta_source.json`
- `holder_delta_normalized.json`
- `quote_security_normalized.json`

## wallet_data/summary

只放钱包数据统计总览：

- `summary_overview.json`
- `summary_overview.md`

## structure_analysis/wallet_fact

只放结构聚合事实包：

- `wallet_structure_normalized.json`
- `chip_distribution_summary.json`
- `same_source_groups.json`
- `fund_flow_edges.csv`
- `address_history.json`
- `wallet_fact_package_manifest.json`

## structure_analysis/intelligence

只放结构证据与钱包候选判断：

- `same_source_evidence_normalized.json`
- `wallet_intelligence_decision.json`

## structure_analysis/handoff

只放 Bot2 handoff：

- `bot2_handoff_packet.json`

## structure_analysis/reports

只放结构可读报告：

- `wallet_fact_report.md`
- `structure_summary.md`

## manifest

必须记录路径和兼容映射：

- `token_output_manifest.json`
- `directory_layout.md`

## 禁止

- 禁止把新 token 输出散放到 token 根目录。
- 禁止把钱包事实数据放入 structure_analysis。
- 禁止把结构判断数据放入 wallet_data。
- 禁止输出交易许可、买卖信号、实盘动作。
