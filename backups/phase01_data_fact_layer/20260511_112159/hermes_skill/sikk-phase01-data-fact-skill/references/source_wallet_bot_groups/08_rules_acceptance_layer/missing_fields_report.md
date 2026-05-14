# Missing Fields Report — Round 3 Field Mapping

## 处理原则
- 未知字段写 `unknown`
- 缺失字段写 `missing`
- 不编造字段
- dashboard / paper / report 不反向生成事实字段
- 不伪造 `discovered_at`
- 不伪造 `wallet_snapshot_time`

## 当前覆盖字段
已覆盖用户指定的 29 个字段，包括 token、wallet、trade、PnL、GMGN tags、native transfer、token transfer、wallet profile、funding source、backflow、cross-token recurrence、snapshot time。

## 仍需真实采集验证的字段
- `realized_profit`：依赖 GMGN trader detail 或链上成本计算。
- `unrealized_profit`：依赖当前余额与当前价格。
- `pnl_multiple`：依赖 buy/sell 成本口径一致。
- `wallet_age_days`：依赖钱包首次链上活动或 GMGN profile。
- `cross_token_reappearance`：依赖历史地址库。
- `backflow_address`：依赖资金路径 / 回流路径追踪。
- `token_transfer_edges`：依赖链上 token transfer graph。

## 缺失处理
- 若 GMGN/API 没返回：写 `missing`。
- 若字段语义未知：写 `unknown`。
- 若需要链上补查：写 `需要链上补查` 到数据质量备注或 blocker notes。

## 禁止处理
- 不用 dashboard 反推 `discovered_at`。
- 不用 case file 反推 `wallet_snapshot_time`。
- 不用 paper entry_time 反推 token open time。
- 不用 report 反推 quote time。
