# Distribution / Recovery / Whale Evidence Rules

## Scope
本文件定义分发、派发、利润回流、疑似接盘鲸鱼、疑似结果钱包的证据规则。只输出候选与证据，不输出确定性结论。

## 疑似分发接收钱包
证据字段：
- token_transfer_edges
- transfer_in.from_address
- amount_percentage
- first_transfer_in_time
- wallet_snapshot_time

## 疑似派发钱包
证据字段：
- sell_amount_percentage
- sold_pct
- remaining_pct
- avg_sell_price
- realized_profit
- last_sell_time

## 疑似利润回收钱包
证据字段：
- backflow_address
- backflow_amount
- backflow_time
- backflow_delay_seconds
- shared backflow receiver

## 疑似接盘鲸鱼
证据字段：
- buy_amount_sol
- buy_amount_usd
- buy_token_amount
- current_balance
- remaining_pct
- wallet_age_days
- gmgn_tags

## 疑似结果钱包
证据字段：
- realized_profit
- unrealized_profit
- total_profit
- pnl_multiple
- is_full_exit
- holding_duration_seconds

## Missing policy
- 字段缺失：写 `missing`
- 需要链上补查：写 `requires_followup_fields`
- 禁止用 dashboard / paper / report 反推事实字段
