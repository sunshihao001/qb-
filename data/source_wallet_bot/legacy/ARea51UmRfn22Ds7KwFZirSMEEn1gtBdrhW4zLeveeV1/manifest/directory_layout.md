# Token legacy wallet data layout

- token_address: `ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1`
- root: `data/source_wallet_bot/legacy/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/`
- copied_files: `142`
- layers: `{'facts': 8, 'handoff': 128, 'inference': 4, 'ingest': 2}`

## 读取顺序

1. `manifest/token_output_manifest.json`
2. `wallet_data/normalized/` facts
3. `structure_analysis/intelligence/` evidence/inference; 推断不是确定事实
4. `structure_analysis/handoff/`
5. `structure_analysis/reports/`
6. `wallet_data/raw/` only for source trace
