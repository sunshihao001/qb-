# SIKK 钱包结构纸面交易日报

- 报告日期：20260504
- 边界：本报告只统计纸面交易、钱包结构变化和失败归因，不执行真实 swap。

## 总体统计
- 关闭仓位数：201
- 盈利仓位数：57
- 胜率_pct：28.3582
- 平均收益率_pct：1.5444
- 中位数收益率_pct：-0.1813
- 总收益SOL：0.0
- 平均最大浮盈_pct：10.2998
- 平均最大浮亏_pct：-4.0515
- 最佳单笔_pct：679.3995
- 最差单笔_pct：-99.1427

## 按钱包结构状态统计
- UNKNOWN
  - 关闭仓位数：5
  - 胜率：60.0%
  - 平均收益率：163.786%
  - 平均最大浮亏：-12.1884%
- WALLET_BLOCK
  - 关闭仓位数：195
  - 胜率：27.6923%
  - 平均收益率：-2.4623%
  - 平均最大浮亏：-3.7181%
- WALLET_PAUSE
  - 关闭仓位数：1
  - 胜率：0.0%
  - 平均收益率：-28.371%
  - 平均最大浮亏：-28.371%

## 按失败归因统计
- STRUCTURE_WEAKENING
  - 关闭仓位数：158
  - 胜率：36.0759%
  - 平均收益率：6.7813%
  - 平均最大浮亏：-0.3374%
- 命中纸面止损
  - 关闭仓位数：43
  - 胜率：0.0%
  - 平均收益率：-17.6985%
  - 平均最大浮亏：-17.6985%

## 按钱包结构状态与信号等级统计
- UNKNOWN|S4_强确认信号
  - 关闭仓位数：5
  - 胜率：60.0%
  - 平均收益率：163.786%
  - 平均最大浮亏：-12.1884%
- WALLET_BLOCK|S4_强确认信号
  - 关闭仓位数：195
  - 胜率：27.6923%
  - 平均收益率：-2.4623%
  - 平均最大浮亏：-3.7181%
- WALLET_PAUSE|S4_强确认信号
  - 关闭仓位数：1
  - 胜率：0.0%
  - 平均收益率：-28.371%
  - 平均最大浮亏：-28.371%

## failure_attribution 事件统计
- STRUCTURE_WEAKENING：304
- WALLET_EXIT：1

## 审计统计
- 样本独立性审计
  - position_count：201
  - unique_token_count：28
  - duplicate_token_count：15
  - duplicate_tokens：{'F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump': 8, 'ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1': 58, '9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump': 8, '7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump': 27, 'EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump': 9, 'CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump': 5, '5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump': 5, 'GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump': 13, '3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump': 3, 'q7oDiKKY8j5FecGwvUR5Eyv7se9sh2DSaUD7aXEpump': 6, '6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump': 17, '3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump': 14, '3XwDQHMKcner1GhXRqLKojrWWwNdMaruQs7g7riDpump': 9, '6Wbs2dcRwMMivXV3TmBP1MmrqJ7SJkN768tC5rG5pump': 3, 'FESx6q1owjzTqaysjSkcaJRBKvNAcE6TEwSuaY65pump': 3}
  - audit_note：同一 token 多笔重复会抬高统计权重，策略结论应优先看 unique token 与分桶表现。
- 加权收益审计
  - position_size_weighted_return_pct：2.3051
  - weight_source：paper_position_sol/paper_size_sol/position_sol；缺失时按 1 等权。
- 退出政策审计
  - force_paper_exit_count：158
  - force_paper_exit_rate_pct：78.607
  - exit_reason_counts：{'STRUCTURE_WEAKENING': 158, '命中纸面止损': 43}
  - audit_note：FORCE_PAPER_EXIT 过多时必须复查是否从 EXIT_MONITOR 过早升级。
- shadow_hold审计
  - shadow_hold_ready_count：0
  - shadow_hold_missing_count：201
  - audit_note：force exit 后应跟踪 shadow hold 15m/30m/60m，判断错杀右尾或规避回撤。
