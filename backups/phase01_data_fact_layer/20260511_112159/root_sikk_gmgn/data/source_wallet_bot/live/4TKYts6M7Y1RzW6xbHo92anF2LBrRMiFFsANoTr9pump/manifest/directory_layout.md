# Source Wallet Bot Directory Layout

token_address: `4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump`
root_dir: `/root/sikk-gmgn/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump`

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

- copied: 17
- created_placeholder: 9
- skipped_missing_source: 0

## Missing sources
- none
