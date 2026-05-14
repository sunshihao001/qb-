# Source Wallet Bot Directory Layout

token_address: `4JrarqBBkE13v6kAAgmRWKwTCBxDku6t7ZquPdY7pump`
root_dir: `/root/sikk-gmgn/data/source_wallet_bot/live_test/4JrarqBBkE13v6kAAgmRWKwTCBxDku6t7ZquPdY7pump/source_wallet_packet`

## Target layout

```text
<token>/
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

## Policy

- 只做目录治理。
- 不重写钱包判断逻辑。
- 不重写结构分析逻辑。
- 不删除旧文件。
- 不移动旧文件。
- 只复制 / 重新输出到新目录。
- 保留旧路径兼容。
- 后续新输出必须写入新目录。
- 不接交易 / 状态机 / paper runner。
- 不读取私钥 / 不签名 / 不广播 / 不 swap。

## Mapping summary

- copied: 0
- created_placeholder: 9
- skipped_missing_source: 9

## Missing sources
- summary_overview.json
- summary_overview.md
- wallet_fact/wallet_structure_normalized.json
- wallet_fact/chip_distribution_summary.json
- wallet_fact/same_source_groups.json
- wallet_fact/fund_flow_edges.csv
- wallet_fact/address_history.json
- wallet_fact/wallet_fact_report.md
- wallet_fact/wallet_fact_package_manifest.json
