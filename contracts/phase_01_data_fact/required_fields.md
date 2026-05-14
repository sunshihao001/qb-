# phase_01_data_fact required_fields v2.1

## Critical / BLOCK
- token_address
- chain
- snapshot_time
- raw_token_basic
- raw_wallet_trade.wallet_address
- raw_wallet_trade.token_address
- raw_wallet_trade.transaction_time
- raw_wallet_trade.transaction_type
- raw_wallet_trade.current_token_balance
- raw_holder
- raw_kline.timestamp
- raw_kline.open
- raw_kline.high
- raw_kline.low
- raw_kline.close
- raw_kline.volume
- raw_quote_security.quote_price_usd

## Optional / DEGRADE
- raw_top_trader
- raw_transfer
- legacy_candidate_snapshot

## Missing policy
- Critical missing -> `DATA_INVALID` + `HANDOFF_BLOCKED`。
- Optional missing -> `DATA_PARTIAL` 或 `DATA_WEAK` + `HANDOFF_DEGRADED`。
- Time stale -> `DATA_STALE` + `HANDOFF_REFRESH_REQUIRED`。
- 禁止用 `0`、空字符串、`null` 或 AI 推测值伪装 missing；缺失必须写 `missing` 并进入报告/handoff/audit。
- 缺失 transfer 时，不得判断“无分发/无转账”；缺失 holder 时，不得判断“筹码仍在”；缺失 quote 时，不得生成入场价。
