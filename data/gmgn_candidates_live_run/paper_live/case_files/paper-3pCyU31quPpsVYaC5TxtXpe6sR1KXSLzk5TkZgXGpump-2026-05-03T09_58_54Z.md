# Paper Case File: $GOP

> 纸面验证档案；不执行真实 swap，不读取私钥，不签名，不广播。

## 1. 基础信息

| 字段 | 数值 |
|---|---|
| Position ID | paper-3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump-2026-05-03T09:58:54Z |
| Token | GOP |
| Address | 3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump |
| 状态 | CLOSED |
| 策略 | SIKK-B 控盘箱体突破回踩 |
| 信号等级 | S4_强确认信号 |
| 入场时间 | 2026-04-28 03:41:00 UTC |
| 退出时间 | 2026-05-03T10:09:28Z |
| 纸面仓位 | 0.040857 SOL |
| 入场市值 | 待补 |
| 退出市值 | 待补 |
| 净收益 | 2.634 |

---

## 1.5 Case File 质量

| 字段 | 数值 |
|---|---|
| 质量等级 | E2_部分可复盘 |
| 完整度 | 66.6667% |
| 缺失核心字段 | 发现时市值、入场市值、paper entry snapshot、持仓 journal |
| 质量说明 | E1 只能作为记录型样本；E2 部分复盘；E3 才可进入高质量策略复盘。 |

- 修复建议：补齐 paper entry snapshot 硬字段：发现/信号/钱包/入场市值、流动性、holder、quote/security 与延迟。；补齐钱包结构、主导侧生命周期、持仓 journal、退出证据和 failure attribution 后再作为策略样本。

---

## 2. 候选发现

系统在 待补 发现 GOP。发现时市值 待补，流动性 待补，持有人 待补。纳入观察原因：进入 GMGN/SIKK 候选观察池，等待盘型、信号和钱包结构进一步确认。

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

信号在 待补 触发，等级为 S4_强确认信号，类型为 SIKK-B 控盘箱体突破回踩。信号价 0.00011084533，信号时市值 待补。失效条件：跌破关键结构位或钱包结构转弱。

---

## 5. 钱包结构门禁

| 字段 | 数值 |
|---|---|
| wallet_structure_status | WALLET_BLOCK |
| wallet_structure_score | 0.0 |
| wallet_risk_score | 100.0 |
| counterparty_pressure_score | 0.0 |
| data_quality_score | 100 |

钱包结构在 待补 给出 WALLET_BLOCK。结构分 0.0，风险分 100.0，对手盘压力 0.0，数据质量 100。钱包解释：发现分发侧钱包 53 个；缺失字段：wallet_address, role, game_side, evidence_level；筹码控制状态机：CONTROL_BREAK_OR_DISTRIBUTION；筹码控制状态机：WALLET_BLOCK；筹码控制状态机：DISTRIBUTION_ACTIVE。钱包结构在这里是纸面验证门禁，不是实盘买入授权。

---

## 6. Quote / Security

Quote/Security 检查状态：quote_gate=READY_FOR_CONFIRMATION，quote_source=待补，价格偏差=待补，security_gate=READY_FOR_CONFIRMATION。该层只确认纸面可执行性，不触发真实交易。

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
| 买入规模 | 0.040857 SOL |
| 估算 token 数量 | 待补 |

纸面仓位在 2026-04-28 03:41:00 UTC 入场。入场模式 live，原始报价 0.0005057348407797846，模拟入场价 0.0005057348407797846，滑点 待补%。入场时市值 待补，相对发现时市值变化 待补，上下文为 UNKNOWN_ENTRY。本次纸面规模 0.040857 SOL，约 待补，估算 token 数量 待补。入场依据：盘型、信号、钱包结构和 quote/security 同时满足纸面验证条件。

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

暂无持仓过程 journal；后续每轮 paper update 会写入价格、市值、浮盈回撤、钱包状态和动作。

| 时间 | 价格 | 市值 | 浮盈 | 钱包状态 | 动作 | 原因 |
|---|---:|---:|---:|---|---|---|
| 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 暂无 journal |

---

## 10. 退出

纸面仓位在 2026-05-03T10:09:28Z 退出，退出价 0.0005190559686536042，退出市值 待补。退出触发 待补，原因码 STRUCTURE_WEAKENING，原因：钱包结构触发纸面强制退出。

---

## 11. 策略复盘

本次交易结果：WIN  
失败归因：无 / 不适用

本次结果为 WIN，收益 2.634%。盈利交易不自动写 failure_type；需要继续判断收益是否来自策略证据链，还是右尾偶然。

---

## 12. 策略调整建议

继续积累同类样本，按入场市值分桶、钱包结构状态和退出原因统计策略稳定性。

---

## 13. 需要继续观察的问题

退出是否过早、钱包结构是否过敏、入场市值分桶是否需要调整，均需继续用 paper 样本验证。

---

## 14. 字段来源追踪

| 字段 | 来源文件 |
|---|---|
| counterparty_pressure_score | paper_position_json |
| current_price | paper_position_json |
| data_quality_score | data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json |
| entry_price | paper_position_json |
| exit_price | paper_position_json |
| exit_reason | paper_position_json |
| exit_time | paper_position_json |
| failure_type | paper_position_json |
| max_drawdown_pct | paper_position_json |
| max_floating_profit_pct | paper_position_json |
| net_pnl_pct | paper_position_json |
| paper_entry_time | paper_position_json |
| paper_size_sol | paper_position_json |
| position_id | paper_position_json |
| quote_gate | paper_position_json |
| security_gate | data/gmgn_candidates_live_run/index/token_detail_index.json |
| security_risk_level | data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json |
| signal_level | paper_position_json |
| signal_price | paper_position_json |
| signal_type | paper_position_json |
| status | paper_position_json |
| token_address | paper_position_json |
| token_symbol | paper_position_json |
| unrealized_pnl_pct | paper_position_json |
| wallet_risk_score | paper_position_json |
| wallet_structure_reason | paper_position_json |
| wallet_structure_score | paper_position_json |
| wallet_structure_status | paper_position_json |

---

## 15. 仍然缺失的字段清单

- Case 缺失字段：candidate_discovered_at、discovery_source、discovery_price、discovery_market_cap_usd、discovery_liquidity_usd、discovery_holder_count、signal_time、signal_market_cap_usd、signal_reason、wallet_decision_time、early_wallet_remaining_pct、early_wallet_sold_pct、same_source_sync_sell_score、wallet_support_signals、wallet_risk_signals、quote_check_time、quote_source、quote_price、gmgn_price、okx_price、kline_close_price、price_deviation_pct、security_flags、entry_market_cap_usd、paper_size_usd、estimated_token_amount、current_market_cap_usd、exit_market_cap_usd
- 质量层缺失字段：发现时市值、入场市值、paper entry snapshot、持仓 journal
- 下一步动作：补齐缺失证据后再进入核心策略统计
- 是否进入核心策略统计：否
