# Wallet Intelligence Contracts

## Scope
本文件定义 Source & Wallet Intelligence Bot 的 normalized 输出 contract。所有 contract 均为事实证据层，不负责交易决策。

## Contract files
- `wallet_trade_normalized.json`
- `wallet_profile_normalized.json`
- `token_transfer_normalized.json`
- `funding_flow_normalized.json`
- `token_source_normalized.json`
- `backflow_paths_normalized.json`
- `same_source_evidence_normalized.json`
- `wallet_intelligence_decision.json`
- `bot2_handoff_packet.json`

## wallet_trade_normalized.json
Purpose: single-wallet cost, buy/sell behavior, PnL and exit status.
Required fields:
- token_address
- wallet_address
- first_buy_time
- last_buy_time
- last_sell_time
- buy_count
- sell_count
- buy_amount_sol
- buy_amount_usd
- buy_token_amount
- sell_amount_sol
- sell_amount_usd
- sell_token_amount
- avg_buy_price
- avg_sell_price
- current_balance
- sold_pct
- remaining_pct
- realized_profit
- unrealized_profit
- total_profit
- pnl_multiple
- holding_duration_seconds
- is_full_exit
- is_partial_exit

## Allowed evidence roles
- 疑似结构执行钱包
- 疑似同源执行组
- 疑似分发接收钱包
- 疑似派发钱包
- 疑似利润回收钱包
- 疑似核心资金源候选
- 疑似接盘鲸鱼
- 疑似结果钱包
- 证据不足
- 字段缺失
- 需要链上补查

## Forbidden language
- 确定庄家
- 一定是庄家
- 百分百内幕
- 绝对老鼠仓

## Global safety rules
- L0 / L1 can be fact sources.
- L2 can be normalized fact artifacts.
- L3 can only be legacy historical samples / audit seeds.
- L4 can only be display / review / audit, never reverse fact source.
- Missing fields must be explicit; no fabricated time anchors.
