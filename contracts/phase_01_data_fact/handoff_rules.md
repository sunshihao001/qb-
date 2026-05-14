# phase_01_data_fact handoff_rules v2.1

## Target
- Handoff target: `phase_02_wallet_structure`。
- Shared handoff path: `data/shared_handoff/data_fact/<token>/phase_01_handoff_packet.json`。

## Status transition
- `DATA_OK` -> `HANDOFF_READY` -> P02 正常执行。
- `DATA_PARTIAL` -> `HANDOFF_DEGRADED` -> P02 降级执行，必须继承 missing/degraded context。
- `DATA_WEAK` -> `HANDOFF_DEGRADED` -> P02 降级执行或只读观察。
- `DATA_STALE` -> `HANDOFF_REFRESH_REQUIRED` -> P02 停止，返回 P01 刷新。
- `DATA_INVALID` -> `HANDOFF_BLOCKED` -> P02 不得执行。

## Minimum files for P02
1. `handoff/phase_01_handoff_packet.json`
2. `quality/data_quality_summary.json`
3. `normalized/token_basic_normalized.json`
4. `normalized/token_market_context.json`
5. `normalized/wallet_trade_normalized.csv`
6. `normalized/holder_normalized.csv`

## Optional files for P02
- `normalized/top_trader_normalized.csv`
- `normalized/transfer_normalized.csv`

## Validation rules
- `phase_status` 必须来自全局 P01 状态码。
- `handoff_status` 必须与 `phase_status` 一致。
- `hard_negative_triggered=true` 时必须有 `block_reason`。
- `missing_fields` 必须与 `reports/missing_fields_report.md` 和 `quality/data_quality_summary.json` 同步。
- `required_files_for_next_stage` 必须真实存在；不存在时不得标记 `HANDOFF_READY`。
