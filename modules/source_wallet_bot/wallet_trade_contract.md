# Wallet Trade Normalized Contract

## 用途
用于计算：
- 单钱包成本
- 同源组成本
- 派发进度
- 疑似结果钱包判断
- 疑似接盘鲸鱼判断

## 来源
允许来源：
- GMGN wallet trade
- GMGN trader detail
- 链上 DEX swap 记录

禁止反推来源：
- dashboard
- paper
- report
- case file
- state_machine

## 输出
- `data/source_wallet_bot/wallet_trade_normalized.json`
- `data/source_wallet_bot/schemas/wallet_trade_normalized.schema.json`

## 必须采集字段
- `token_address`
- `wallet_address`
- `first_buy_time`
- `last_buy_time`
- `last_sell_time`
- `buy_count`
- `sell_count`
- `buy_amount_sol`
- `buy_amount_usd`
- `buy_token_amount`
- `sell_amount_sol`
- `sell_amount_usd`
- `sell_token_amount`
- `avg_buy_price`
- `avg_sell_price`
- `current_balance`
- `sold_pct`
- `remaining_pct`
- `realized_profit`
- `unrealized_profit`
- `total_profit`
- `pnl_multiple`
- `holding_duration_seconds`
- `is_full_exit`
- `is_partial_exit`

## 缺失策略
- 缺失字段写 `missing`
- 未知字段写 `unknown`
- 需要链上补查的字段写入 `missing_fields` 与 `requires_followup_fields`
- 不使用旧 dashboard / paper / report / case file 反推交易时间、成本或派发比例

## 输出语义
该 contract 只定义事实字段，不输出主导侧动机、最终控筹判断、`PAPER_READY`、`BLOCKED` 或交易 gate。
