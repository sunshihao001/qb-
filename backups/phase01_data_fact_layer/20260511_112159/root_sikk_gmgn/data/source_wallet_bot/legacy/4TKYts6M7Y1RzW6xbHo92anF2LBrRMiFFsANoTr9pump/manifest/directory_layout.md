# Token legacy wallet data layout

- token_address: `4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump`
- root: `data/source_wallet_bot/legacy/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/`
- copied_files: `36`
- layers: `{'inference': 2, 'facts': 31, 'handoff': 3}`

## 读取顺序

1. `manifest/token_output_manifest.json`
2. `wallet_data/normalized/` facts
3. `structure_analysis/intelligence/` evidence/inference; 推断不是确定事实
4. `structure_analysis/handoff/`
5. `structure_analysis/reports/`
6. `wallet_data/raw/` only for source trace
