# Paper Case File: $TRUNC

> 纸面验证档案；不执行真实 swap，不读取私钥，不签名，不广播。

## 1. 基础信息

| 字段 | 数值 |
|---|---|
| Position ID | paper-6Wbs2dcRwMMivXV3TmBP1MmrqJ7SJkN768tC5rG5pump-2026-05-04T04:55:43Z |
| Token | TRUNC |
| Address | 6Wbs2dcRwMMivXV3TmBP1MmrqJ7SJkN768tC5rG5pump |
| 状态 | CLOSED |
| 策略 | SIKK-B 控盘箱体突破回踩 |
| 信号等级 | S4_强确认信号 |
| 入场时间 | 2026-05-04T04:55:43Z |
| 退出时间 | 2026-05-04T05:04:35Z |
| 纸面仓位 | 0.054981 SOL |
| 入场市值 | 待补 |
| 退出市值 | 待补 |
| 净收益 | -28.371 |

---

## 1.5 Case File 质量

| 字段 | 数值 |
|---|---|
| 质量等级 | E2_部分可复盘 |
| 完整度 | 83.3333% |
| 缺失核心字段 | 发现时市值、入场市值 |
| 质量说明 | E1 只能作为记录型样本；E2 部分复盘；E3 才可进入高质量策略复盘。 |

- 修复建议：补齐 paper entry snapshot 硬字段：发现/信号/钱包/入场市值、流动性、holder、quote/security 与延迟。；补齐钱包结构、主导侧生命周期、持仓 journal、退出证据和 failure attribution 后再作为策略样本。

---

## 2. 候选发现

系统在 待补 发现 TRUNC。发现时市值 待补，流动性 待补，持有人 待补。纳入观察原因：进入 GMGN/SIKK 候选观察池，等待盘型、信号和钱包结构进一步确认。

---

## 3. 盘型判断

- pattern_type：SIKK-B 控盘箱体突破回踩
- lifecycle_phase：待补
- control_box_low：待补
- control_box_high：待补
- AVWAP：待补
- POC：待补

当前盘型记录为 SIKK-B 控盘箱体突破回踩。控制箱体区间 low=待补、high=待补，AVWAP=待补，价格结构状态=待补。该解释用于确认是否属于结构性回踩，而不是简单追涨。

---

## 4. 入场信号

信号在 2026-05-04 04:37:00 UTC 触发，等级为 S4_强确认信号，类型为 SIKK-B 控盘箱体突破回踩。信号价 0.00014592022，信号时市值 待补。失效条件：跌破关键结构位或钱包结构转弱。

---

## 5. 钱包结构门禁

| 字段 | 数值 |
|---|---|
| wallet_structure_status | WALLET_PAUSE |
| wallet_structure_score | 32.0 |
| wallet_risk_score | 64.0 |
| counterparty_pressure_score | 48.0 |
| data_quality_score | 100.0 |

钱包结构在 2026-05-04T04:55:43Z 给出 WALLET_PAUSE。结构分 32.0，风险分 64.0，对手盘压力 48.0，数据质量 100.0。钱包解释：缺失字段：wallet_address, role, game_side, evidence_level；筹码控制状态机：CONTROL_UNCLEAR。钱包结构在这里是纸面验证门禁，不是实盘买入授权。

---

## 6. Quote / Security

Quote/Security 检查状态：quote_gate=READY_FOR_CONFIRMATION，quote_source=okx_market_price，价格偏差=待补，security_gate=PAUSE。该层只确认纸面可执行性，不触发真实交易。

---

## 7. 纸面入场

| 字段 | 数值 |
|---|---|
| 入场市值 | 待补 |
| 发现时市值 | 待补 |
| 信号时市值 | 待补 |
| 从发现到入场市值变化 | % |
| 从信号到入场市值变化 | % |
| 入场上下文 | UNKNOWN_ENTRY |
| 买入规模 | 0.054981 SOL |
| 估算 token 数量 | 328.41643799 |

纸面仓位在 2026-05-04T04:55:43Z 入场。入场模式 live，原始报价 0.0001674124484637937，模拟入场价 0.0001674124484637937，滑点 3.0%。入场时市值 待补，相对发现时市值变化 待补，上下文为 UNKNOWN_ENTRY。本次纸面规模 0.054981 SOL，约 0 USD，估算 token 数量 328.41643799。入场依据：盘型、信号、钱包结构和 quote/security 同时满足纸面验证条件。

---

## 8. 主导侧心理与生命周期

| 字段 | 数值 |
|---|---|
| 主导侧生命周期 | UNKNOWN |
| 主导侧心理 | 证据不足 / 待复查 |
| 行为动机 | UNKNOWN |
| 对手盘心理 | UNKNOWN |
| 流动性意图 | UNKNOWN |
| 陷阱风险 | UNKNOWN |
| 结构防守 | UNKNOWN |
| 筹码控制权 | CONTROL_UNCLEAR |
| 纸面入场匹配度 | DATA_INSUFFICIENT |
| 证据等级 | E1 |

主导侧心理解释：主导侧心理证据不足，不能把盘型直接解释为明确控筹或派发。

- 下一步观察：证据不足，先复查生命周期、钱包结构、市值上下文与多轮快照。
- 失效条件：生命周期证据缺失；钱包结构或 K线 delta 未形成

---

## 9. 持仓过程

持仓过程已记录 3 条 journal。最近一次 2026-05-04T05:03:48Z，价格 0.0001345528382177966，浮动收益 -19.63%，动作 EXIT_MONITOR，原因 钱包结构出现风险，但 多轮 delta 未确认；盘型冲突未确认；市场确认不足，默认 EXIT_MONITOR。

| 时间 | 价格 | 市值 | 浮盈 | 钱包状态 | 动作 | 原因 |
|---|---:|---:|---:|---|---|---|
| 2026-05-04T04:55:43Z | 0.0001674124484637937 | 待补 | 0.0 | WALLET_PAUSE | PAPER_ENTRY | 新纸面仓位入场后记录首条持仓日志 |
| 2026-05-04T04:59:46Z | 0.00012990325966590809 | 待补 | -22.4053 | WALLET_PAUSE | EXIT_MONITOR | 钱包结构出现风险，但 多轮 delta 未确认；盘型冲突未确认；市场确认不足，默认 EXIT_MONITOR |
| 2026-05-04T05:03:48Z | 0.0001345528382177966 | 待补 | -19.6279 | WALLET_PAUSE | EXIT_MONITOR | 钱包结构出现风险，但 多轮 delta 未确认；盘型冲突未确认；市场确认不足，默认 EXIT_MONITOR |

---

## 10. 退出

纸面仓位在 2026-05-04T05:04:35Z 退出，退出价 0.000119915881844809，退出市值 待补。退出触发 待补，原因码 待补，原因：命中纸面止损。

---

## 11. 策略复盘

本次交易结果：LOSS  
失败归因：命中纸面止损

本次结果为 LOSS，收益 -28.37%。需要重点复查入场是否追高、钱包结构是否误判、quote/security 是否延迟，以及退出是否过慢。

---

## 12. 策略调整建议

钱包结构已进入 EXIT_MONITOR，后续需要用多轮 delta 与价格结构确认，避免过早强退。

---

## 13. 需要继续观察的问题

退出是否过早、钱包结构是否过敏、入场市值分桶是否需要调整，均需继续用 paper 样本验证。

---

## 14. 字段来源追踪

| 字段 | 来源文件 |
|---|---|
| counterparty_pressure_score | paper_position_json |
| current_price | paper_position_json |
| data_quality_score | paper_position_json |
| discovery_source | paper_position_json |
| entry_price | paper_position_json |
| estimated_token_amount | paper_position_json |
| exit_price | paper_position_json |
| exit_reason | paper_position_json |
| exit_time | paper_position_json |
| max_drawdown_pct | paper_position_json |
| max_floating_profit_pct | paper_position_json |
| net_pnl_pct | paper_position_json |
| paper_entry_time | paper_position_json |
| paper_size_sol | paper_position_json |
| paper_size_usd | paper_position_json |
| position_id | paper_position_json |
| quote_gate | paper_position_json |
| quote_source | paper_position_json |
| security_gate | data/gmgn_candidates_live_run/index/token_detail_index.json |
| security_risk_level | data/gmgn_candidates_live_run/wallet_structure/6Wbs2dcRwMMivXV3TmBP1MmrqJ7SJkN768tC5rG5pump/wallet_structure_decision.json |
| signal_level | paper_position_json |
| signal_price | paper_position_json |
| signal_time | paper_position_json |
| signal_type | paper_position_json |
| status | paper_position_json |
| token_address | paper_position_json |
| token_symbol | paper_position_json |
| unrealized_pnl_pct | paper_position_json |
| wallet_decision_time | paper_position_json |
| wallet_risk_score | paper_position_json |
| wallet_structure_reason | paper_position_json |
| wallet_structure_score | paper_position_json |
| wallet_structure_status | paper_position_json |

---

## 15. 仍然缺失的字段清单

- Case 缺失字段：candidate_discovered_at、discovery_price、discovery_market_cap_usd、discovery_liquidity_usd、discovery_holder_count、signal_market_cap_usd、signal_reason、early_wallet_remaining_pct、early_wallet_sold_pct、same_source_sync_sell_score、wallet_support_signals、wallet_risk_signals、quote_check_time、quote_price、gmgn_price、okx_price、kline_close_price、price_deviation_pct、security_flags、entry_market_cap_usd、current_market_cap_usd、exit_market_cap_usd、failure_type
- 质量层缺失字段：发现时市值、入场市值
- 下一步动作：补齐缺失证据后再进入核心策略统计
- 是否进入核心策略统计：否
