# wallet_fact_report

token_address: `4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump`

## 总体统计
- wallet_count: 95
- same_source_group_count: 4
- same_source_group_wallet_count: 10
- total_current_balance: 287742930.20126
- top10_wallet_balance_pct_of_tracked: 51.019219
- data_quality_score: 1.0

## 角色候选统计
- 疑似结构执行钱包: 47
- 疑似同源执行组: 10
- 疑似接盘鲸鱼: 31
- 证据不足: 26
- 疑似结果钱包: 6

## 筹码结构摘要
- chip_concentration_level: high
- chip_transfer_status: 存在疑似同源/分发线索
- full_exit_wallet_count: 54
- partial_exit_wallet_count: 2

## 字段缺口 / 下一步
- Class 5 Token transfer source: 需要链上补查以区分主动买入 / Token 转入 / 分发接收 / 空投接收。
- Class 6 Funding source: GMGN native_transfer 可作候选，金额和时间仍需链上确认。
- Class 7 Backflow: 需要从 sell tx/time 向后追踪 24h/72h 回流路径。
- Class 10 Snapshot delta: 需要多快照才能计算 holder_delta。
- Class 11 Quote/security: 需要 OKX quote/security scan 补充当前条件背景。

## 安全边界
- no_state_machine
- no_paper_runner
- no_real_execution
- no_signing
- no_broadcast
- no_swap
