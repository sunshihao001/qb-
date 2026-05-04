# ChatGPT share 69f6fc90｜SIKK 纸面交易优化与单入口运行层知识吸收原文节选

来源链接：https://chatgpt.com/share/69f6fc90-989c-83ab-adc5-f0659d6dd6eb
提取文件：/tmp/sikk_share_69f6fc90_relevant.md
说明：本文件为从 ChatGPT share 动态页面提取出的 SIKK 相关正文节选；用于知识吸收链路。原始 HTML 与完整相关正文保存在 /tmp，未写入凭证或私钥。

## 核心主题

- SIKK Paper Lifecycle Recorder：纸面仓位全生命周期记录与自动复盘系统。
- Paper Position Case File：单币实战档案、策略执行日志、入场/出场证据链、失败归因、调整建议。
- 纸面报告复盘：右尾收益明显，但样本独立性、入场记录、退出逻辑、钱包结构 FORCE_PAPER_EXIT 过度主导需要审查。
- 钱包结构退出策略：钱包结构不是直接卖出按钮；默认先 EXIT_MONITOR，强证据、多快照、盘型/市场确认才允许 FORCE_PAPER_EXIT；真实交易仍默认关闭。
- Live Runtime：保持 sikk_live_run.py 单入口，paper JSON/CSV 同步，wallet daily report 使用新 CSV，live_state/live_board/live_dashboard/site 静态控制台连续输出。
- Dashboard / Visual Console：静态专业控制台、单币详情抽屉、移动端可读、展示未入场原因、纸面仓位、失败归因、系统健康。

---
<!-- source_marker=642 -->

# SIKK Paper Lifecycle Recorder  
# 纸面仓位全生命周期记录与自动复盘系统
```text
→ 策略调整建议
```text
# 一、可以实现到什么程度
## 第 1 层：结构化记录
```json
  "wallet_structure_status": "WALLET_SUPPORT",
## 第 2 层：自然语言记录
```text
入场时市值约 126,000 USD，模拟入场价格为 0.00005356。
## 第 3 层：自动复盘
给策略优化用。
```text
本次交易的主要问题是入场市值相对发现市值已经上涨 230%，属于 LATE_ENTRY。
# 二、从开始到结束应该记录哪些阶段
```text
```text
# 三、每个阶段具体记录什么
## S0：候选发现
```text
发现时市值多少？
```text
```text
发现时市值约 {{discovery_market_cap_usd}} USD，流动性约 {{discovery_liquidity_usd}} USD，持有人数量为 {{discovery_holder_count}}。
## S1：初筛判断
```text
```text
```text
```text
## S2：盘型识别
```text
```text
```text
系统暂时判断该结构具备 {{pattern_confidence}} 的策略适配度。
## S3：信号触发
```text
信号触发时价格和市值是多少？
```text
```text
触发时价格为 {{signal_price}}，市值约 {{signal_market_cap_usd}} USD。
## S4：钱包结构门禁
```text
```text
wallet_decision_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_wallet_remaining_pct
wallet_support_signals
wallet_risk_signals
wallet_reason
```text
钱包结构在 {{wallet_decision_time}} 给出 {{wallet_structure_status}}。
结构分为 {{wallet_structure_score}}，风险分为 {{wallet_risk_score}}，对手盘压力为 {{counterparty_pressure_score}}，数据质量为 {{data_quality_score}}。
支持证据包括：{{wallet_support_signals}}。
风险证据包括：{{wallet_risk_signals}}。
综合判断：{{wallet_reason}}。
## S5：Quote / Security 检查
```text
```text
```text
## S6：入场决策
```text
```text
```text
## S7：纸面入场
```text
什么市值买？
```text
```text
入场时市值约 {{entry_market_cap_usd}} USD，流动性约 {{entry_liquidity_usd}} USD。
入场市值相对发现时变化 {{entry_market_cap_change_from_discovery_pct}}%，入场上下文被标记为 {{market_cap_context_status}}。
## S8：持仓监控
```text
价格、市值、钱包、风险如何变化？
每次更新写一行 JSONL：
```text
```text
wallet_structure_status
wallet_risk_score
```text
{{time}}，仓位当前浮动收益为 {{unrealized_pnl_pct}}%，当前市值约 {{current_market_cap_usd}} USD。
钱包结构状态为 {{wallet_structure_status}}，钱包风险分为 {{wallet_risk_score}}，对手盘压力为 {{counterparty_pressure_score}}。
## S9：风险变化
```text
```text
wallet_risk_score_before
wallet_risk_score_after
```text
钱包风险分从 {{wallet_risk_score_before}} 变化到 {{wallet_risk_score_after}}，对手盘压力从 {{counterparty_pressure_before}} 变化到 {{counterparty_pressure_after}}。
当前策略动作调整为：{{risk_action}}。
## S10：退出决策
```text
```text
wallet_exit_action
wallet_exit_confidence
wallet_exit_reason_code
wallet_exit_evidence
```text
钱包退出策略给出的动作为 {{wallet_exit_action}}，置信度为 {{wallet_exit_confidence}}。
## S11：纸面退出
```text
退出时市值多少？
```text
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
```text
退出价格为 {{exit_price}}，退出时市值约 {{exit_market_cap_usd}} USD，流动性约 {{exit_liquidity_usd}} USD。
退出时钱包结构状态为 {{exit_wallet_structure_status}}，风险分为 {{exit_wallet_risk_score}}，对手盘压力为 {{exit_counterparty_pressure_score}}。
## S12：自动复盘
```text
```text
wallet_gate_review
```text
{{wallet_gate_review}}
策略调整建议：
# 四、自动复盘如何实现
## 自动复盘规则示例
### 1. 判断是否追高
```text
→ 复盘提示：入场可能过晚，需要限制发现后市值涨幅。
```text
本次入场被标记为 CHASE_ENTRY。入场市值相对发现时已经上涨超过 300%，说明系统可能在趋势末端才触发入场。后续需要检查 SIKK-B 信号是否过于滞后，或者是否需要增加 entry_market_cap_change_from_discovery_pct 上限。
### 2. 判断钱包退出是否过早
```text
```text
本次退出可能过早。FORCE_PAPER_EXIT 后 60 分钟内价格继续上涨超过 30%，且未出现明显更大回撤，说明钱包结构退出信号可能过于敏感。建议将类似场景从 FORCE_EXIT 降级为 EXIT_MONITOR。
### 3. 判断入场信号是否有效
```text
```text
本次 S4 信号未能提供有效保护。入场后最大回撤快速扩大，且未产生明显浮盈，说明单独依赖 S4 强确认不足。需要结合钱包结构、入场市值和 quote 偏差进一步过滤。
### 4. 判断止损是否太晚
```text
```text
### 5. 判断右尾依赖
```text
```text
当前策略收益高度依赖少数右尾样本。虽然累计收益为正，但中位数收益接近 0，说明大多数交易并没有稳定优势。后续应继续扩大样本，并分别观察剔除 Top 1 / Top 2 赢家后的策略表现。
# 五、需要新增的文件结构
```text
```text
| `sikk_paper_explanation_builder.py` | 把阶段数据转成自然语言 case file |
# 六、Visual Console 里怎么展示
```text
```text
```text
入场市值：126K
```text
# 七、给 OpenClaw / Hermes 的专业任务书
```text
- 什么时间发现
- 发现时市值多少
- 为什么进入观察
- 什么时候识别盘型
- 为什么触发信号
- 钱包结构当时是否支持
- quote/security 是否通过
- 什么时候纸面入场
- 入场时市值多少
- 买了多少 SOL
- 估算获得多少 token
- 入场位置相对箱体 / AVWAP / POC 在哪里
- 持仓过程中风险如何变化
- 什么时候退出
- 退出时市值多少
- 为什么退出
- 这笔交易暴露了策略什么问题
- 下一次应该怎么调整
1. 结构化数据
2. 自然语言解释
3. 风险点
4. 下一步动作
5. 后续复盘依据
- sikk_paper_lifecycle_recorder.py
- sikk_paper_explanation_builder.py
- sikk_paper_auto_reviewer.py
- tests/test_sikk_paper_lifecycle_recorder.py
- tests/test_sikk_paper_explanation_builder.py
- tests/test_sikk_paper_auto_reviewer.py
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- paper_live/case_files/<position_id>.json
- paper_live/case_files/<position_id>.md
- paper_live/position_journal/<position_id>.jsonl
- paper_live/auto_reviews/<position_id>_review.json
- paper_live/auto_reviews/<position_id>_review.md
1. 不执行真实 swap。
2. 不接自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
7. 不改变真实交易逻辑。
8. 只增强 paper 记录、自然语言解释、自动复盘和 dashboard 展示。
- stage_name
- stage_time
- stage_status
- data
- natural_language_summary
- risk_points
- decision
- next_action
- evidence
- missing_fields
- candidate_discovered_at
- discovery_source
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
- discovery_age_minutes
- discovery_volume_5m
- discovery_volume_1h
- discovery_reason
- natural_language_summary
- initial_filter_time
- initial_filter_result
- min_liquidity_pass
- min_holder_pass
- age_filter_pass
- risk_filter_pass
- initial_filter_reason
- natural_language_summary
- pattern_time
- pattern_type
- lifecycle_phase
- control_box_high
- control_box_low
- control_box_mid
- poc_price
- avwap_price
- ema20
- ema50
- volume_state
- volatility_state
- price_structure_status
- pattern_confidence
- pattern_reason
- natural_language_summary
- signal_time
- signal_level
- signal_type
- signal_gate
- signal_price
- signal_market_cap_usd
- signal_liquidity_usd
- signal_kline_interval
- signal_reason
- confirmation_conditions
- invalid_level
- invalid_conditions
- natural_language_summary
- wallet_decision_time
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- early_wallet_remaining_pct
- early_wallet_sold_pct
- same_source_group_count
- same_source_sync_sell_score
- high_result_wallet_remaining_pct
- late_large_buyer_count
- wallet_support_signals
- wallet_risk_signals
- wallet_reason
- natural_language_summary
- quote_check_time
- quote_source
- quote_price
- gmgn_price
- okx_price
- kline_close_price
- price_deviation_pct
- quote_gate
- quote_reason
- security_check_time
- security_gate
- security_risk_level
- security_flags
- security_reason
- natural_language_summary
- entry_decision_time
- entry_decision
- entry_decision_reason
- entry_evidence_chain
- entry_block_reasons
- entry_invalid_conditions
- next_action
- natural_language_summary
- paper_entry_time
- entry_price_mode
- entry_quote_source
- entry_raw_quote_price
- entry_simulated_price
- entry_slippage_pct
- entry_fee_sol
- entry_market_cap_usd
- entry_liquidity_usd
- entry_holder_count
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_delay_from_discovery_sec
- entry_delay_from_signal_sec
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- market_cap_context_status
- entry_reason_summary
- natural_language_summary
- position_journal_path
- first_update_time
- max_profit_time
- max_drawdown_time
- max_floating_profit_pct
- max_drawdown_pct
- current_price
- current_market_cap_usd
- current_wallet_structure_status
- current_wallet_risk_score
- current_counterparty_pressure_score
- natural_language_summary
- time
- current_price
- current_market_cap_usd
- unrealized_pnl_pct
- unrealized_pnl_sol
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- wallet_risk_score
- counterparty_pressure_score
- price_structure_status
- paper_action
- monitor_reason
- natural_language_summary
- risk_events
  - risk_event_time
  - risk_event_type
  - risk_event_level
  - risk_source
  - risk_reason
  - wallet_risk_score_before
  - wallet_risk_score_after
  - counterparty_pressure_before
  - counterparty_pressure_after
  - price_structure_before
  - price_structure_after
  - risk_action
  - natural_language_summary
- exit_decision_time
- exit_action
- exit_trigger
- exit_reason_code
- exit_reason
- exit_evidence_chain
- wallet_exit_action
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_evidence
- market_confirmation
- pattern_conflict
- natural_language_summary
- exit_time
- exit_price
- exit_market_cap_usd
- exit_liquidity_usd
- exit_slippage_pct
- exit_fee_sol
- net_pnl_pct
- net_pnl_sol
- trade_result_type
- failure_type
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- natural_language_summary
- review_time
- strategy_fit_result
- entry_quality_review
- wallet_gate_review
- exit_quality_review
- risk_management_review
- main_success_factors
- main_failure_factors
- missed_opportunity
- false_exit_flag
- strategy_adjustment_suggestion
- open_questions
- natural_language_summary
1. 如果 market_cap_context_status = CHASE_ENTRY：
   - 标记 entry_quality_review = 入场偏晚
   - strategy_adjustment_suggestion 增加：限制发现后市值涨幅或提高早期入场条件
2. 如果 market_cap_context_status = LATE_ENTRY 且 net_pnl_pct < 0：
   - 标记 entry_quality_review = 入场滞后导致亏损风险增加
3. 如果 net_pnl_pct < -80：
   - risk_management_review = 风控严重滞后
   - suggestion = 增加最大亏损硬止损或快速下跌保护
4. 如果 FORCE_PAPER_EXIT 后 shadow_hold 60m 继续上涨 > 30：
   - false_exit_flag = true
   - exit_quality_review = 钱包退出可能过早
   - suggestion = 将类似场景从 FORCE_EXIT 降级为 EXIT_MONITOR
5. 如果 S4 信号入场后最大浮盈 < 10 且最大回撤 < -40：
   - strategy_fit_result = S4 信号质量不足
   - suggestion = 增加 quote/security 和钱包确认过滤
6. 如果 entry_wallet_structure_status = WALLET_BLOCK：
   - wallet_gate_review = 入场门禁异常
   - suggestion = 修复状态机，禁止 WALLET_BLOCK 进入 paper entry
7. 如果 entry_wallet_structure_status = MISSING：
   - wallet_gate_review = 钱包数据缺失
   - suggestion = 不允许 MISSING 直接 PAPER_READY，或降低仓位 / 仅观察
   - trade_result_type = BIG_WIN
   - review 中标记：右尾赢家，需检查是否可复现
   - 清空 failure_type
   - 记录 warning：failure_type should not be set for profitable trade
# Paper Case File: $TOKEN
1. 基础信息
2. 候选发现
3. 初筛判断
4. 盘型识别
5. 入场信号
15. 策略调整建议
- 关键结构化数据表
- 自然语言解释
- 风险点
- 下一步动作或复盘结论
- Lifecycle Timeline
- Stage Detail
- Open Case File
- Open Auto Review
- Recent Case Files
- Strategy Weakness Summary
- Adjustment Suggestions
dashboard_data.json 增加：
- case_files
- auto_reviews
- lifecycle_summary
  sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py \
for section in ["候选发现","盘型识别","入场信号","钱包结构门禁","纸面入场","持仓过程","纸面退出","自动复盘","策略调整建议"]:
1. 每笔 paper position 都有 case json。
2. 每笔 paper position 都有 case markdown。
3. 每个 case 包含 S0-S12 全阶段。
4. 每个阶段有自然语言解释。
5. 每笔记录能回答什么时候发现、什么时候入场、入场市值、买了多少、为什么入场、为什么退出。
6. 自动复盘能指出策略不足和调整建议。
8. 不允许真实交易。
# 八、最终判断
```text
```text
策略实战复盘系统
```text
如果错了，策略应该怎么改？

---

<!-- source_marker=864 -->

```text
> **单币实战档案 + 策略执行日志 + 入场证据链 + 出场证据链 + 失败归因 + 调整建议。**
```text
入场时市值多少？
退出时市值多少？
下一次策略应该怎么调整？
# 一、你现在需要新增一个核心概念
```text
```text
JSON 给系统统计用。  
# 二、每一笔仓位必须分 8 个阶段记录
## 阶段 1：候选发现
```text
```text
发现时市值约 82,000 USD，流动性约 26,000 USD，持有人 412。
该 token 被纳入观察的原因是：市值仍处于早期区间，流动性满足最低观察条件，并且后续 K线进入控盘箱体候选结构。
## 阶段 2：盘型识别
```text
```text
## 阶段 3：信号触发
```text
```text
当时价格为 0.000052，市值约 118,000 USD。
## 阶段 4：钱包结构门禁
```text
wallet_decision_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_wallet_remaining_pct
wallet_reason
wallet_support_signals
wallet_risk_signals
```text
## 阶段 5：Quote / Security 检查
```text
```text
## 阶段 6：纸面入场
```text
```text
入场时市值约 126,000 USD，流动性约 33,000 USD。
1. 盘型符合 SIKK-B 控盘箱体突破回踩。
2. S4 强确认信号触发。
3. 价格回踩未破关键结构位。
4. 钱包结构为 WALLET_SUPPORT，早期钱包没有集中清仓。
5. Quote 与 security 均通过。
6. 入场市值相对发现时上涨 53.6%，属于 NORMAL_ENTRY，不属于严重追高。
1. 跌破 control_box_low。
2. 跌破 AVWAP 后无法收回。
3. 钱包结构从 SUPPORT 转为明确同源组同步退出。
4. 对手盘压力快速升至 75 以上。
## 阶段 7：持仓过程
```text
```text
wallet_structure_status
wallet_risk_score
```text
```text
## 阶段 8：退出与复盘
```text
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
```text
退出价格为 0.000069，退出时市值约 162,000 USD。
本次入场逻辑基本符合 SIKK-B 策略预期。
# 三、必须新增自然语言解释模块
```text
```text
```text
wallet_structure_decision.json
```text
# 四、单笔 Case File 的完整 Markdown 模板
# Paper Case File: $ABC
## 1. 基础信息
| 策略 | SIKK-B 控盘箱体突破回踩 |
| 入场市值 | 126,000 USD |
| 退出市值 | 162,000 USD |
## 2. 候选发现
发现时市值为 {{discovery_market_cap_usd}}，流动性为 {{discovery_liquidity_usd}}，持有人数量为 {{discovery_holder_count}}。
## 3. 盘型判断
- pattern_type：{{pattern_type}}
- lifecycle_phase：{{lifecycle_phase}}
- control_box_low：{{control_box_low}}
- control_box_high：{{control_box_high}}
- AVWAP：{{avwap_price}}
- POC：{{poc_price}}
## 4. 入场信号
信号触发时市值：{{signal_market_cap_usd}}
## 5. 钱包结构门禁
钱包判断时间：{{wallet_decision_time}}
| wallet_structure_status | {{wallet_structure_status}} |
| wallet_structure_score | {{wallet_structure_score}} |
| wallet_risk_score | {{wallet_risk_score}} |
{{wallet_explanation}}
{{wallet_support_signals}}
{{wallet_risk_signals}}
## 6. Quote / Security
## 7. 纸面入场
| 入场市值 | {{entry_market_cap_usd}} |
| 发现时市值 | {{discovery_market_cap_usd}} |
| 信号时市值 | {{signal_market_cap_usd}} |
| 从发现到入场市值变化 | {{entry_market_cap_change_from_discovery_pct}}% |
| 从信号到入场市值变化 | {{entry_market_cap_change_from_signal_pct}}% |
## 8. 持仓过程
| 时间 | 价格 | 市值 | 浮盈 | 钱包状态 | 动作 | 原因 |
## 9. 退出
退出市值：{{exit_market_cap_usd}}  
## 10. 策略复盘
## 11. 策略调整建议
## 12. 需要继续观察的问题
# 五、策略每一步必须自然语言化
## 1. `discovery_explanation`
```text
市值是否合适？
## 2. `pattern_explanation`
```text
## 3. `signal_explanation`
```text
## 4. `wallet_explanation`
```text
## 5. `entry_explanation`
```text
进场市值相对发现时涨了多少？
## 6. `holding_explanation`
```text
## 7. `exit_explanation`
```text
退出时市值是多少？
## 8. `post_trade_review`
```text
是策略有效，还是右尾偶然？
## 9. `strategy_adjustment_suggestion`
```text
市值区间不适合？
# 六、需要新增的字段分组
## A. 市值路径字段
```text
wallet_decision_market_cap_usd
```text
发现市值 → 信号市值 → 入场市值 → 退出市值
## B. 时间路径字段
```text
wallet_decision_time
```text
## C. 价格路径字段
```text
## D. 仓位规模字段
```text
## E. 策略证据字段
```text
## F. 钱包证据字段
```text
entry_wallet_structure_status
entry_wallet_structure_score
entry_wallet_risk_score
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
wallet_support_signals
wallet_risk_signals
# 七、Visual Console 必须增加一个 “Case File” 入口
```text
```text
```text
```text
1. Timeline
2. Entry Evidence
3. Wallet Evidence
4. Position Progress
5. Exit Evidence
# 八、给 OpenClaw / Hermes 的完整任务书
```text
任务：升级 SIKK 纸面交易系统，新增 Paper Position Case File 和自然语言策略复盘解释。
- 一个代币当前市值多少
- 什么时间进去
- 入场时市值多少
- 买了多少 SOL
- 估算买了多少 token
- 什么价格进
- 什么时候退出
- 退出时市值多少
- 为什么进场
- 为什么退出
- 进场时指标和钱包结构是否支持
- 持仓过程中发生了什么
- 策略到底哪里不足
- 哪个位置需要调整
每笔仓位必须记录发现、盘型、信号、钱包结构、quote/security、入场、持仓过程、退出、复盘和策略调整建议。
同时生成 JSON 结构化文件和 Markdown 自然语言报告。
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- sikk_paper_explanation_builder.py
- sikk_wallet_structure_daily_report.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_paper_explanation_builder.py
- sikk_paper_explanation_builder.py
- tests/test_sikk_paper_explanation_builder.py
- case_files/<position_id>.json
- case_files/<position_id>.md
1. 不执行真实 swap。
2. 不接自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
7. 不改变真实交易逻辑。
10. 可以增强 dashboard 展示。
- candidate_discovered_at
- signal_time
- wallet_decision_time
- quote_check_time
- paper_entry_time
- first_update_time
- max_profit_time
- max_drawdown_time
- exit_time
二、每笔 paper position 必须新增完整市值路径：
- discovery_market_cap_usd
- signal_market_cap_usd
- wallet_decision_market_cap_usd
- entry_market_cap_usd
- current_market_cap_usd
- exit_market_cap_usd
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- exit_market_cap_change_from_entry_pct
- market_cap_context_status
- EARLY_ENTRY：entry_market_cap_change_from_discovery_pct < 50
- NORMAL_ENTRY：50 <= change < 150
- LATE_ENTRY：150 <= change < 300
- CHASE_ENTRY：change >= 300
- UNKNOWN_ENTRY：缺少 discovery_market_cap_usd 或 entry_market_cap_usd
- discovery_price
- signal_price
- entry_raw_quote_price
- entry_simulated_price
- current_price
- exit_price
- price_change_from_entry_pct
- max_price_after_entry
- min_price_after_entry
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_slippage_pct
- entry_fee_sol
- exit_slippage_pct
- exit_fee_sol
- net_pnl_pct
- net_pnl_sol
五、每笔 paper position 必须新增策略字段：
- strategy_name
- strategy_version
- signal_level
- signal_type
- signal_gate
- pattern_type
- lifecycle_phase
- control_box_high
- control_box_low
- control_box_mid
- poc_price
- avwap_price
- ema20
- ema50
- volume_state
- volatility_state
- price_structure_status
- invalid_level
- entry_reason_summary
- entry_evidence_chain
- invalid_conditions
- entry_wallet_structure_status
- entry_wallet_structure_score
- entry_wallet_risk_score
- entry_counterparty_pressure_score
- entry_data_quality_score
- entry_early_wallet_remaining_pct
- entry_early_wallet_sold_pct
- entry_same_source_sync_sell_score
- entry_high_result_wallet_remaining_pct
- entry_wallet_support_signals
- entry_wallet_risk_signals
- entry_wallet_reason
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- exit_data_quality_score
- exit_early_wallet_remaining_pct
- exit_early_wallet_sold_pct
- exit_same_source_sync_sell_score
- exit_high_result_wallet_remaining_pct
- exit_wallet_reason
- quote_gate
- quote_source
- quote_price
- gmgn_price
- okx_price
- kline_close_price
- price_deviation_pct
- quote_reason
- security_gate
- security_risk_level
- security_flags
- security_reason
- exit_trigger
- exit_reason
- exit_reason_code
- trade_result_type
- failure_type
- wallet_exit_action
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_evidence
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct
1. exit_trigger 表示谁触发退出，例如 WALLET_STRUCTURE / STOP_LOSS / TAKE_PROFIT / TIME_STOP。
2. exit_reason_code 表示具体信号码，例如 STRUCTURE_WEAKENING / SAME_SOURCE_SYNC_EXIT。
3. failure_type 只用于亏损或无效交易，盈利交易不要写 failure_type。
4. 盈利交易如果由钱包结构退出，应记录：
- time
- current_price
- current_market_cap_usd
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- wallet_risk_score
- counterparty_pressure_score
- price_structure_status
- paper_action
- monitor_reason
十、生成 Paper Case File JSON：
- basic
- discovery
- pattern
- signal
- wallet_entry
- quote_security
- entry
- holding_journal
- exit
- review
- adjustment
1. 基础信息
2. 候选发现
3. 盘型判断
4. 入场信号
5. 钱包结构门禁
10. 策略复盘
11. 策略调整建议
- discovery_explanation
- pattern_explanation
- signal_explanation
- wallet_explanation
- quote_security_explanation
- entry_explanation
- holding_explanation
- exit_explanation
- post_trade_review
- strategy_adjustment_suggestion
- open_questions
1. 必须使用自然语言。
2. 不能只堆字段。
3. 必须说明为什么入场。
4. 必须说明入场时位置在哪里。
5. 必须说明入场时市值多少。
10. 必须说明策略哪里可能不足。
- paper_entry_time
- paper_size_sol
- estimated_token_amount
- discovery_market_cap_usd
- signal_market_cap_usd
- entry_market_cap_usd
- current_market_cap_usd
- exit_market_cap_usd
- market_cap_context_status
- entry_reason_summary
- entry_evidence_chain
- exit_reason
- strategy_adjustment_suggestion
- case_file_path
十四、日报增强：
1. Case File Summary
2. Entry Market Cap Context
3. Entry Delay Analysis
4. Strategy Weakness Summary
5. Wallet Exit Effectiveness
  sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py \
for k in ["basic","discovery","pattern","signal","wallet_entry","quote_security","entry","holding_journal","exit","review","adjustment"]:
for section in ["基础信息","候选发现","盘型判断","入场信号","钱包结构门禁","纸面入场","持仓过程","退出","策略复盘","策略调整建议"]:
print("paper case file OK")
1. 每笔 paper position 都能看到什么时候买。
2. 每笔 paper position 都能看到买了多少 SOL。
3. 每笔 paper position 都能看到估算 token 数量。
4. 每笔 paper position 都能看到发现时市值、信号时市值、入场时市值、当前市值、退出市值。
5. 每笔 paper position 都能看到为什么进场。
9. 每笔 paper position 都能看到策略复盘。
10. 每笔 paper position 都能看到策略调整建议。
12. 不允许真实交易。
# 九、你最终要的效果
以后你打开某个 token 的 case file，应该能直接看出：
```text
发现时市值多少
信号触发时市值多少
入场时市值多少
策略哪里需要调
# 十、当前优先级
```text
P0：每笔仓位的 case file
P0：策略调整建议
```text
P1：Visual Console 展示 case file
```text
# 最短结论
> **纸面仓位的目标不是展示赚钱，而是暴露策略哪里不足。**
```text
+ 策略证据链
+ 市值路径

---

<!-- source_marker=1081 -->

这份纸面报告非常有价值。它已经明确暴露出一个核心问题：

> **当前系统不是在验证“SIKK-B 控盘箱体突破回踩是否有效”，而是在验证“钱包结构强制退出机制是否过度主导”。**

现在不能只看累计收益是正的。  
这份报告说明：**系统确实能抓到右尾大收益，但退出逻辑、样本独立性、入场记录、钱包结构接入方式都有明显偏差。**

---

# 一、这份报告的真实结论

## 1. 累计收益为正，但稳定性不强

数据：

```text
已关闭累计收益：+1104.26%
平均单笔收益：+9.5195%
中位数收益：-0.0493%
胜率：29.31%
```

这说明：

```text
系统收益来自少数极端赢家
大部分交易接近小亏 / 小波动 / 持平
```

这不是坏事。meme 策略本来就可能是右尾收益模型。

但问题是：

> **你现在还不能判断系统真的稳定有效，因为 AALIEN 和 lolcat 对结果贡献过大。**

AALIEN 一项贡献：

```text
+1184.2034%
```

总收益：

```text
+1104.26%
```

这意味着：**如果去掉 AALIEN，整体收益可能完全变样。**

所以现在必须新增：

```text
剔除最大赢家后的收益
剔除 Top 1 token 后收益
剔除 Top 2 token 后收益
按 token 聚合后的收益
```

否则容易被极端右尾误导。

---

## 2. 当前样本不是 116 个独立样本

报告显示：

```text
总纸面记录：119
涉及代币总数：17
AALIEN 次数：34
WOLVERINE 次数：16
```

这说明你的纸面仓位不是 119 个独立 token 样本，而是：

```text
17 个 token 上重复产生了 119 条仓位记录
```

这会造成一个问题：

> **单个 token 的多次记录会严重放大统计权重。**

例如 AALIEN 34 次，如果它表现好，就会把系统整体收益拉高；WOLVERINE 16 次，如果表现差，也会放大拖累。

所以必须把日报拆成两套统计：

```text
按仓位统计
按 token 统计
```

当前报告主要是按仓位统计，不足够。

---

## 3. 钱包结构强制退出占比过高

核心数据：

```text
钱包结构触发纸面强制退出：96 / 116
FORCE_PAPER_EXIT：96
STRUCTURE_WEAKENING：96
WALLET_BLOCK：112
```

这说明当前系统几乎变成：

```text
钱包结构退出系统
```

而不是：

```text
K线结构 + 钱包结构 + quote/security + paper runner 的综合验证系统
```

这个问题非常严重。

钱包结构当然重要，但现在它已经过度主导退出。尤其你前面担心“很多刚因为钱包结构触发就强制退出”，这份数据已经验证了这个担心。

---

## 4. `STRUCTURE_WEAKENING` 被误用为失败归因

最好单笔：

```text
AALIEN
最终收益：+679.3995%
退出原因：钱包结构触发纸面强制退出
失败归因：STRUCTURE_WEAKENING
```

这里逻辑不对。

如果一笔交易盈利 +679%，它不应该被简单归为：

```text
失败归因：STRUCTURE_WEAKENING
```

更准确应该分开：

```text
exit_trigger = WALLET_STRUCTURE_EXIT
exit_reason_code = STRUCTURE_WEAKENING
trade_result = BIG_WIN
failure_type = null
```

现在你的系统把“退出触发原因”和“失败归因”混在一起了。

必须拆开：

```text
exit_reason        退出原因
exit_trigger       谁触发退出
exit_reason_code   退出信号码
trade_result_type  交易结果类型
failure_type       只有亏损或无效交易才写失败归因
```

否则日报会误导你。

---

## 5. S4 信号样本过于单一

报告显示：

```text
所有记录都是 S4_强确认信号
所有策略都是 SIKK-B 控盘箱体突破回踩
```

这说明当前纸面验证只覆盖了一个子策略：

```text
SIKK-B + S4
```

不能推导到整个 SIKK 系统。

当前只能说：

> **你正在验证 SIKK-B 强确认突破回踩模型。**

不能说：

```text
SIKK 整体策略有效
钱包结构系统整体有效
```

后续必须拆：

```text
S3 vs S4
WALLET_SUPPORT vs WALLET_BLOCK
EARLY_ENTRY vs LATE_ENTRY
EXIT_MONITOR vs FORCE_EXIT
不同市值区间
不同 token 生命周期
不同盘型
```

---

# 二、当前最关键的 6 个问题

## 问题 1：重复入场 / 多记录是否合理

AALIEN 34 次，WOLVERINE 16 次。

你需要确认：

```text
这是同一 token 多次独立入场？
还是 paper runner 重复开仓？
是否违反“单 token 只允许一笔实盘”的原则？
```

如果未来实盘原则是：

```text
一个 token 只允许一笔实盘
```

那纸面也应该至少增加一个统计：

```text
single_token_first_entry_only_result
```

否则纸面表现和未来实盘不一致。

---

## 问题 2：钱包结构状态可能被当前状态覆盖

报告里：

```text
钱包结构状态统计：WALLET_BLOCK 112
```

这可能是“退出时状态”，不一定是“入场时状态”。

你必须拆开：

```text
entry_wallet_structure_status
exit_wallet_structure_status
current_wallet_structure_status
```

否则你无法判断：

```text
入场时钱包结构支持，后来恶化？
还是入场时就已经 WALLET_BLOCK，但系统仍然开仓？
```

这是非常关键的数据审计点。

---

## 问题 3：强制退出没有验证对错

96 次 FORCE_PAPER_EXIT，现在你不知道：

```text
它们是真的规避了后续下跌？
还是误杀了后续上涨？
```

所以必须加：

```text
shadow_hold_tracking
```

每次 FORCE_EXIT 后继续追踪：

```text
退出后 15m / 30m / 60m 的价格
退出后最大涨幅
退出后最大回撤
是否误杀
是否规避下跌
```

否则无法评估钱包退出机制是否正确。

---

## 问题 4：入场市值上下文缺失

你已经指出了：

```text
什么时候买
买了多少
什么市值进去
```

这份报告也说明这个字段必须补。

没有这些字段，就无法判断：

```text
AALIEN 是早期吃到右尾？
还是已经高位追进但继续冲？
GRUMP 是高位追进？
还是早期失败？
```

必须新增：

```text
discovery_market_cap_usd
signal_market_cap_usd
entry_market_cap_usd
exit_market_cap_usd
entry_market_cap_change_from_discovery_pct
market_cap_context_status
```

---

## 问题 5：收益统计方式需要升级

当前：

```text
总收益率累计：+1104.26%
```

这是把每笔百分比直接相加。

这可以看方向，但不能代表真实账户曲线。

必须新增：

```text
position_size_weighted_pnl
equity_curve_return
max_equity_drawdown
token_weighted_return
capital_weighted_return
```

否则 0.042 SOL 的仓位和 0.2 SOL 的仓位被同等看待，会失真。

---

## 问题 6：退出时机可能滞后

报告里说：

```text
GRUMP、GOBLIEN、NYAN 接近归零亏损
但退出原因仍然是钱包结构强制退出
```

这说明：

```text
钱包结构退出不是太早，而是某些情况下太晚
```

所以问题不是简单把 FORCE_EXIT 全部降级。

更准确是：

```text
钱包结构退出需要分层：
- 提前预警：EXIT_MONITOR
- 市场确认：REDUCE_RISK / TIGHT_STOP
- 强证据：FORCE_EXIT
```

当前只有 FORCE_EXIT，缺中间层。

---

# 三、当前系统应该如何重新定性

现在的系统阶段不是简单“纸面验证表现很好”。

更准确：

```text
Phase B-1A：右尾收益型纸面样本已出现，但退出机制和样本统计口径需要审计
```

当前不能进入实盘。

原因：

```text
1. 样本被少数 token 主导
2. 钱包结构强制退出过度主导
3. 入场快照缺失
4. 退出对错没有 shadow hold 验证
5. 失败归因字段混乱
6. 按 token 独立统计不足
```

---

# 四、现在必须新增的核心指标

## 1. 剔除极端赢家后的表现

日报新增：

```text
total_pnl_excluding_top_1_token
total_pnl_excluding_top_2_tokens
median_token_pnl
token_level_win_rate
position_level_win_rate
```

用途：

```text
判断系统是否只靠 AALIEN / lolcat 撑起来
```

---

## 2. 单 token 聚合统计

新增：

```text
token_count
position_count_per_token
token_total_pnl_pct
token_avg_pnl_pct
token_median_pnl_pct
token_win_rate
token_best_trade
token_worst_trade
```

同时展示：

```text
Top token contribution concentration
```

例如：

```text
AALIEN 贡献 / 总收益
Top 3 token 贡献 / 总收益
```

---

## 3. 入场上下文统计

新增：

```text
entry_market_cap_usd
entry_market_cap_bucket
entry_delay_from_discovery_sec
entry_delay_from_signal_sec
market_cap_context_status
```

市值分桶：

```text
<50K
50K-100K
100K-200K
200K-500K
500K-1M
>1M
```

---

## 4. 钱包退出有效性

新增：

```text
force_exit_count
exit_monitor_count
true_positive_exit_count
false_positive_exit_count
false_exit_rate
avg_avoided_drawdown_pct
avg_missed_profit_pct
price_change_after_exit_15m
price_change_after_exit_30m
price_change_after_exit_60m
```

---

## 5. 入场钱包状态 vs 出场钱包状态

新增：

```text
entry_wallet_structure_status
entry_wallet_structure_score
entry_wallet_risk_score
entry_counterparty_pressure_score

exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
exit_counterparty_pressure_score
```

这个是钱包结构审计的核心。

---

# 五、钱包结构接入方式需要改成“三层制”

现在：

```text
wallet_structure → FORCE_PAPER_EXIT
```

应该改成：

```text
wallet_structure_signal
  ↓
wallet_exit_policy
  ↓
paper_action
```

## 第一层：钱包结构信号

只判断事实：

```text
早期钱包是否卖出
同源组是否同步卖出
高结果钱包是否退出
对手盘压力是否上升
数据质量是否足够
```

输出：

```text
wallet_risk_signal
wallet_risk_score
wallet_evidence
```

---

## 第二层：退出策略判断

结合：

```text
盘型
生命周期
K线结构
quote/security
多轮 delta
paper 当前盈亏
```

输出：

```text
HOLD
EXIT_MONITOR
FORCE_PAPER_EXIT
```

---

## 第三层：paper runner 执行动作

```text
HOLD → 继续持仓
EXIT_MONITOR → 不退出，提高监控，记录风险
FORCE_PAPER_EXIT → 关闭纸面仓位，并创建 shadow hold
```

---

# 六、FORCE_EXIT 规则需要收紧

当前 96 次 FORCE_EXIT 太多。

建议立刻修改：

```text
默认钱包风险 → EXIT_MONITOR
强证据钱包风险 → FORCE_PAPER_EXIT
```

允许 FORCE_EXIT 的条件：

```text
1. data_quality_score >= 65
2. wallet_exit_confidence >= 80
3. hard_exit_code 命中
4. 至少 2 轮 delta 确认，或同源组同步退出非常明确
5. 市场结构确认恶化
```

hard_exit_code 只允许：

```text
SAME_SOURCE_SYNC_EXIT
ACTIVE_DISTRIBUTION
HIGH_RESULT_GROUP_EXIT
COUNTERPARTY_ABSORBING
WALLET_RISK_WITH_PRICE_BREAKDOWN
```

不允许 FORCE_EXIT：

```text
wallet_structure_status = MISSING
单个钱包卖出
单轮 early_wallet_sold_pct 上升
高 ROI 钱包部分止盈
data_quality_score < 65
长横盘控盘箱体正常换手
二段启动前筹码轮换
```

---

# 七、这份日报下一版应该变成这样

## 新增一：样本独立性

```text
样本独立性
- 总仓位记录：119
- 涉及 token：17
- 平均每 token 仓位数：7.0
- 最高重复 token：AALIEN 34 次
- Top 1 token 贡献占比：xxx%
- 剔除 Top 1 token 后总收益：xxx%
- 剔除 Top 2 token 后总收益：xxx%
```

---

## 新增二：钱包退出有效性

```text
钱包退出有效性
- FORCE_EXIT 次数：96
- EXIT_MONITOR 次数：x
- 退出后 30m 平均价格变化：x%
- 退出后 60m 平均价格变化：x%
- 误杀次数：x
- 误杀率：x%
- 平均规避回撤：x%
- 平均错过收益：x%
```

---

## 新增三：入场市值上下文

```text
入场市值上下文
- EARLY_ENTRY：x 笔，平均收益 x%
- NORMAL_ENTRY：x 笔，平均收益 x%
- LATE_ENTRY：x 笔，平均收益 x%
- CHASE_ENTRY：x 笔，平均收益 x%
```

---

## 新增四：入场钱包状态 vs 出场钱包状态

```text
钱包结构迁移
- ENTRY WALLET_SUPPORT → EXIT WALLET_BLOCK：x 笔
- ENTRY WALLET_NEUTRAL → EXIT WALLET_BLOCK：x 笔
- ENTRY MISSING → EXIT WALLET_BLOCK：x 笔
```

这个能告诉你：

```text
是入场后结构恶化
还是入场时就不该进
```

---

# 八、给 OpenClaw / Hermes 的修复任务书

直接复制：

```text
任务：审计并升级 SIKK 纸面交易统计和钱包结构退出机制。

当前纸面报告显示：
- 总纸面记录：119
- 已关闭仓位：116
- 涉及 token：17
- 胜率：29.31%
- 平均单笔收益：+9.5195%
- 中位数收益：-0.0493%
- 最大单笔收益：+679.3995%
- 钱包结构强制退出：96 / 116
- WALLET_BLOCK：112
- STRUCTURE_WEAKENING：96
- 所有样本都是 S4_强确认信号 + SIKK-B 控盘箱体突破回踩

当前问题：
1. 样本被少数 token 主导，AALIEN 和 lolcat 贡献过大。
2. 119 条仓位记录只涉及 17 个 token，样本不是独立样本。
3. 钱包结构强制退出占比过高，FORCE_PAPER_EXIT 可能过度主导。
4. STRUCTURE_WEAKENING 被同时当作退出原因和失败归因，字段语义混乱。
5. 缺少 paper entry snapshot，无法知道什么时候买、买了多少、什么市值进去。
6. 缺少 entry_wallet_status 和 exit_wallet_status，无法判断入场时是否已风险。
7. 缺少 shadow hold tracking，无法判断 FORCE_EXIT 是否误杀。
8. 当前统计只覆盖 S4 + SIKK-B，不能推导整个系统有效。

目标：
升级纸面交易统计、钱包结构退出策略和 Visual Console Paper Lab，使系统能够判断：
- 收益是否过度依赖少数右尾 token
- 钱包结构强制退出是否有效
- 入场是不是太晚
- 钱包结构在入场时和退出时分别是什么状态
- FORCE_EXIT 是否规避风险还是卖飞
- SIKK-B S4 是否真的具备稳定性

允许修改：
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- sikk_wallet_structure_gate.py
- sikk_wallet_structure_snapshot.py
- sikk_wallet_structure_daily_report.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_wallet_structure_gate.py

禁止：
- 不执行真实 swap
- 不修改真实交易逻辑
- 不新增交易按钮
- 不删除已有模块
- 不使用数据库
- 不新增复杂后端

一、修正字段语义

新增并拆分：
- exit_trigger
- exit_reason
- exit_reason_code
- trade_result_type
- failure_type

规则：
1. exit_trigger 表示谁触发退出，例如 WALLET_STRUCTURE / STOP_LOSS / TAKE_PROFIT / TIME_STOP。
2. exit_reason_code 表示具体信号码，例如 STRUCTURE_WEAKENING / SAME_SOURCE_SYNC_EXIT。
3. failure_type 只用于亏损或无效交易，不要把盈利交易标记为 failure。
4. 盈利交易如果由钱包结构退出，应记录：
   exit_trigger = WALLET_STRUCTURE
   exit_reason_code = STRUCTURE_WEAKENING
   trade_result_type = BIG_WIN / WIN
   failure_type = null

二、新增 paper entry snapshot

每笔 paper position 必须记录：
- candidate_discovered_at
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
- signal_time
- signal_level
- signal_type
- signal_price
- signal_market_cap_usd
- wallet_decision_time
- entry_wallet_structure_status
- entry_wallet_structure_score
- entry_wallet_risk_score
- entry_counterparty_pressure_score
- paper_entry_time
- entry_price_mode
- entry_quote_source
- entry_raw_quote_price
- entry_simulated_price
- entry_market_cap_usd
- entry_liquidity_usd
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_delay_from_discovery_sec
- entry_delay_from_signal_sec
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- market_cap_context_status

market_cap_context_status：
- EARLY_ENTRY：涨幅 < 50%
- NORMAL_ENTRY：50%-150%
- LATE_ENTRY：150%-300%
- CHASE_ENTRY：>=300%
- UNKNOWN_ENTRY：缺少数据

三、新增 exit wallet snapshot

关闭仓位时记录：
- exit_time
- exit_price
- exit_market_cap_usd
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- exit_reason
- exit_reason_code
- exit_trigger
- net_pnl_pct
- trade_result_type
- failure_type

四、钱包结构退出改为三层

当前不要让 wallet_structure 直接触发 FORCE_PAPER_EXIT。

新增 wallet_exit_policy：
输入：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- same_source_sync_sell_score
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- pattern_type
- lifecycle_phase
- price_structure_status
- latest_delta
- current paper position

输出：
- wallet_exit_action：HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_reason
- wallet_exit_evidence

规则：
1. wallet_structure_status = MISSING 不允许 FORCE_PAPER_EXIT。
2. data_quality_score < 65 不允许 FORCE_PAPER_EXIT。
3. 单轮钱包风险默认 EXIT_MONITOR。
4. 长横盘控盘箱体 / 二段启动 / 再吸筹盘型下，早期钱包部分卖出默认 EXIT_MONITOR。
5. 只有 hard_exit_code 才允许 FORCE_PAPER_EXIT：
   - SAME_SOURCE_SYNC_EXIT
   - ACTIVE_DISTRIBUTION
   - HIGH_RESULT_GROUP_EXIT
   - COUNTERPARTY_ABSORBING
   - WALLET_RISK_WITH_PRICE_BREAKDOWN
6. FORCE_PAPER_EXIT 需要：
   - wallet_exit_confidence >= 80
   - data_quality_score >= 65
   - hard_exit_code 命中
   - market_confirmation = true
   - pattern_conflict = true

五、新增 shadow hold tracking

每次 FORCE_PAPER_EXIT 后，创建 shadow hold：
- wallet_exit_trigger_time
- wallet_exit_trigger_type
- force_exit_price
- shadow_tracking_until
- shadow_hold_price_15m
- shadow_hold_price_30m
- shadow_hold_price_60m
- shadow_hold_max_profit_after_exit
- shadow_hold_max_drawdown_after_exit
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct

判断：
1. 如果 FORCE_EXIT 后 60m 内继续上涨超过 30%，且没有更大回撤，标记 false_exit_flag = true。
2. 如果 FORCE_EXIT 后出现更大下跌，记录 avoided_drawdown_pct。
3. 每日统计 false_exit_rate。

六、新增样本独立性统计

日报增加：
- position_count
- token_count
- avg_positions_per_token
- max_positions_per_token
- top_1_token_contribution_pct
- top_3_token_contribution_pct
- total_pnl_excluding_top_1_token
- total_pnl_excluding_top_2_tokens
- token_level_win_rate
- token_level_avg_pnl
- token_level_median_pnl

七、新增按市值和入场上下文统计

日报和 dashboard 增加：
按 entry_market_cap_usd 分桶：
- <50K
- 50K-100K
- 100K-200K
- 200K-500K
- 500K-1M
- >1M

每个桶统计：
- trades
- win_rate
- avg_pnl
- median_pnl
- max_drawdown

按 market_cap_context_status 统计：
- EARLY_ENTRY
- NORMAL_ENTRY
- LATE_ENTRY
- CHASE_ENTRY
- UNKNOWN_ENTRY

统计：
- trades
- win_rate
- avg_pnl
- median_pnl

八、Visual Console Paper Lab 升级

Paper Lab 必须展示：
1. 当前开放仓位：
- Token
- Entry Time
- Entry MC
- Current MC
- MC Change %
- Entry Price
- Current Price
- Size SOL
- Token Amount
- PnL %
- Max Profit %
- Max Drawdown %
- Entry Wallet
- Exit Policy
- Market Cap Context

2. 已关闭仓位：
- Token
- Entry Time
- Exit Time
- Entry MC
- Exit MC
- Size SOL
- Net PnL %
- Exit Trigger
- Exit Reason Code
- Trade Result Type
- Failure Type
- Entry Wallet
- Exit Wallet
- Market Cap Context

3. Wallet Exit Effectiveness：
- wallet_force_exit_count
- exit_monitor_count
- true_positive_exit_count
- false_positive_exit_count
- false_exit_rate
- avg_avoided_drawdown_pct
- avg_missed_profit_pct

4. Right Tail Dependency：
- total_pnl
- total_pnl_excluding_top_1_token
- total_pnl_excluding_top_2_tokens
- top_1_token_contribution_pct
- top_3_token_contribution_pct

九、验收命令

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_live_runner.py \
  sikk_dashboard_site_builder.py \
  sikk_wallet_structure_gate.py \
  sikk_wallet_structure_snapshot.py \
  sikk_wallet_structure_daily_report.py

python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

open_p = Path("data/gmgn_candidates_live_run/paper_live/paper_positions_open.json")
closed_p = Path("data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json")
site_p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")

for p in [open_p, closed_p, site_p]:
    print(p, p.exists())

def rows(path):
    if not path.exists():
        return []
    d = json.loads(path.read_text())
    return d if isinstance(d, list) else d.get("positions", [])

all_rows = rows(open_p) + rows(closed_p)
print("positions:", len(all_rows))

if all_rows:
    r = all_rows[0]
    required = [
        "paper_entry_time",
        "paper_size_sol",
        "entry_market_cap_usd",
        "discovery_market_cap_usd",
        "signal_market_cap_usd",
        "entry_wallet_structure_status",
        "market_cap_context_status",
        "exit_trigger",
        "exit_reason_code",
        "trade_result_type"
    ]
    for k in required:
        print(k, "=", r.get(k))
        assert k in r, k

d = json.loads(site_p.read_text())
assert "paper_metrics" in d
assert "paper_positions" in d
assert "tokens" in d
print("dashboard paper fields OK")
PY

十、验收标准：
1. paper 报告能显示每笔什么时候买。
2. paper 报告能显示每笔买了多少 SOL。
3. paper 报告能显示入场时市值。
4. paper 报告能显示发现时市值、信号时市值、入场时市值。
5. paper 报告能显示入场是不是 EARLY / NORMAL / LATE / CHASE。
6. paper 报告能按 token 聚合统计。
7. paper 报告能剔除 Top 1 / Top 2 贡献后统计。
8. FORCE_EXIT 不再由 wallet_structure 直接触发。
9. MISSING wallet 不再 FORCE_EXIT。
10. 每个 FORCE_EXIT 都有 shadow hold tracking。
11. Visual Console Paper Lab 展示这些字段。
12. 不允许真实交易。
```

---

# 九、现在的执行优先级

## P0：先修统计口径

```text
1. 拆分 exit_trigger / exit_reason_code / failure_type
2. 增加 entry_wallet_status / exit_wallet_status
3. 增加 paper entry snapshot
4. 增加按 token 聚合统计
```

## P1：再修钱包退出策略

```text
5. wallet_exit_policy
6. EXIT_MONITOR
7. FORCE_EXIT 收紧
8. shadow hold tracking
```

## P2：最后改面板展示

```text
9. Paper Lab Pro
10. Right Tail Dependency
11. Entry MC Bucket
12. Wallet Exit Effectiveness
```

不要反过来。  
先数据，后策略，再面板。

---

# 十、最终判断

这份报告说明：

```text
SIKK-B S4 当前确实能抓到大右尾
但系统稳定性还没证明
钱包结构退出机制过度主导
样本被少数 token 高度影响
纸面记录缺少入场证据链
```

所以现在最重要的不是继续增加 token，也不是马上调 dashboard，而是：

> **把 paper 统计从“收益表”升级成“交易证据链 + 退出有效性审计表”。**

这一步完成后，你才能真正判断：

```text
钱包结构接入方式是否正确
FORCE_EXIT 是否误杀
SIKK-B 是否靠少数右尾维持
入场是不是太晚
哪些市值区间更有效
哪些钱包状态真的有价值
```

---

<!-- source_marker=1161 -->

纸面仓位总览

数据更新时间：2026-05-03T05:27:54Z

- 总纸面记录：119
- 当前开放仓位：3
- 已关闭仓位：116
- 涉及代币总数：17
- 已关闭代币数：16

已关闭仓位表现

- 已关闭记录数：116
- 总收益率累计：+1104.26%
- 平均单笔收益率：+9.5195%
- 中位数收益率：-0.0493%
- 最大单笔收益：+679.3995%
- 最大单笔亏损：-98.3146%

胜负结构

- 盈利笔数：34
- 亏损笔数：58
- 持平笔数：24
- 胜率：29.31%

解读：胜率不高，但靠少数大幅盈利仓位拉高了总收益。中位数接近 0，说明大部分仓位结果偏小幅波动或小亏，小部分极端大盈对总结果贡献很大。

当前开放仓位表现

- 开放仓位：3
- 当前浮动总收益率：-21.5976%
- 平均浮动收益率：-7.1992%
- 中位数浮动收益率：0.0%
- 当前盈利仓位：0
- 当前亏损仓位：1
- 当前持平仓位：2

解读：当前开放仓位整体轻微偏弱，主要由一个浮亏仓位拖累。

仓位规模统计

- 平均仓位：0.1728 SOL
- 中位仓位：0.1857 SOL
- 最小仓位：0.042 SOL
- 最大仓位：0.2 SOL
- 总记录仓位规模累计：20.5664 SOL

注意：这里是纸面记录的仓位规模累计，不代表真实资金投入，也不代表当前净敞口。

止盈触发情况

- 有止盈统计的记录：99
- 总触发止盈次数：18
- 平均每笔触发止盈：0.1818 次
- 最大单笔触发止盈：3 次
- 触发过止盈的记录：8
- 未触发止盈的记录：91

解读：大多数纸面仓位没有走到止盈区，少数强势币贡献了主要收益。

退出原因统计

- 钱包结构触发纸面强制退出：96
- 命中纸面止损：20

钱包动作统计

- FORCE_PAPER_EXIT：96
- 未标记：20

失败归因统计

- STRUCTURE_WEAKENING：96
- 未标记：20

钱包结构状态统计

- WALLET_BLOCK：112
- 未标记：4

解读：当前纸面系统主要是被钱包结构恶化触发退出，而不是传统价格止损触发退出。也就是说，系统现在的风险控制核心已经偏向“钱包结构门禁”，而不是单纯价格线。

信号和策略分布

所有记录都是：

- 信号等级：S4_强确认信号
- 策略类型：SIKK-B 控盘箱体突破回踩

这说明当前纸面样本还比较单一，主要验证的是强确认突破回踩模型，没有覆盖 S3、S2、SX 等更多状态。

贡献最大的代币

正贡献 Top

1. AALIEN
   - 次数：34
   - 总收益率：+1184.2034%
   - 平均收益：+34.8295%
   - 胜率：44.12%
   - 最大单次：+679.3995%

2. lolcat
   - 次数：8
   - 总收益率：+462.6269%
   - 平均收益：+57.8284%
   - 胜率：50.0%
   - 最大单次：+343.0812%

3. UNIPUMP
   - 次数：8
   - 总收益率：+42.9981%
   - 平均收益：+5.3748%
   - 胜率：37.5%

4. CHARITYDROP
   - 次数：5
   - 总收益率：+2.6248%
   - 平均收益：+0.525%
   - 胜率：60.0%

拖累最大的代币

1. HDD
   - 次数：6
   - 总收益率：-108.7725%
   - 平均收益：-18.1288%
   - 胜率：0%

2. GRUMP
   - 次数：1
   - 总收益率：-98.3146%

3. GOBLIEN
   - 次数：1
   - 总收益率：-97.2723%

4. NYAN
   - 次数：1
   - 总收益率：-92.6342%

5. FINE
   - 次数：3
   - 总收益率：-70.1676%

6. WOLVERINE
   - 次数：16
   - 总收益率：-68.4914%
   - 平均收益：-4.2807%
   - 胜率：18.75%

最好和最差单笔

最好单笔

- 代币：AALIEN
- 最终收益率：+679.3995%
- 入场价：0.000048220098
- 退出价：0.00037582719343021165
- 退出原因：钱包结构触发纸面强制退出
- 失败归因：STRUCTURE_WEAKENING

最差单笔

- 代币：GRUMP
- 最终收益率：-98.3146%
- 入场价：0.00024935266
- 退出价：0.0000042025141525633655
- 退出原因：钱包结构触发纸面强制退出
- 失败归因：STRUCTURE_WEAKENING

核心结论

1. 纸面系统整体累计是正的
   - 已关闭累计：+1104.26%
   - 但主要靠 AALIEN、lolcat 这类大波动赢家贡献。

2. 胜率偏低
   - 胜率只有 29.31%
   - 中位数 -0.0493%
   - 说明多数仓位不是稳定盈利，而是靠少数右尾大赚拉起来。

3. 钱包结构退出是主导机制
   - 96 / 116 个关闭仓位来自钱包结构强制退出。
   - 这说明当前系统已经在执行“钱包结构恶化优先退出”的逻辑。

4. 样本信号过于集中
   - 全部是 S4_强确认信号
   - 全部是 SIKK-B 控盘箱体突破回踩
   - 后面需要按 S3/S4、钱包结构状态、失败归因继续拆分，否则不知道到底是哪一层真正有效。

5. 风险点
   - GRUMP、GOBLIEN、NYAN 这类接近归零亏损说明：即使是 S4，也不能单独作为入场充分条件。
   - 钱包结构虽然能触发退出，但有些 token 已经大幅下跌后才退出，说明钱包结构检测和退出时机还需要提前。

---

<!-- source_marker=1283 -->

对，你现在这个担心是对的。

如果现在出现很多：

```text
因为钱包结构触发 → FORCE_PAPER_EXIT
```

那说明系统可能已经从：

```text
钱包结构作为风险证据
```

过度变成了：

```text
钱包结构直接控制退出
```

这不一定正确。

---

# 一句话判断

> **钱包筹码结构不应该默认直接强制退出。它应该先作为“风险监控层”和“失败归因层”，只有在强证据、多快照、与盘型冲突时，才允许 FORCE_PAPER_EXIT。**

现在你要重点检查：

```text
这些强制退出是真的规避了风险？
还是把正常洗盘 / 换手 / 横盘二段前的筹码轮换误判成出货？
```

---

# 一、钱包结构在系统里的正确位置

钱包结构不应该是单独的买卖按钮。

它应该有 4 个作用：

```text
1. 入场前门禁
2. 持仓中风险监控
3. 异常时退出观察
4. 失败后归因
```

不是：

```text
看到早期钱包卖出 → 立刻退出
看到钱包结构变差 → 立刻退出
看到 WALLET_BLOCK → 立刻平仓
```

正确逻辑应该是：

```text
钱包结构变化
  ↓
判断是不是与当前盘型冲突
  ↓
判断是不是多轮快照确认
  ↓
判断是不是价格/成交/quote 同步恶化
  ↓
再决定 HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
```

---

# 二、现在最可能的问题

你现在很多强制退出，可能来自这几种误判。

## 1. 把正常换手当成出货

尤其是这种盘：

```text
长时间横盘
控盘箱体
二段放量前
早期钱包部分减仓
新钱包承接
```

这不一定是坏事。

可能是：

```text
结构侧部分换手
利润钱包释放浮盈
新承接方接力
二段前清理不稳定筹码
```

不能直接 FORCE_EXIT。

---

## 2. 单次快照触发太敏感

如果只看一轮：

```text
early_wallet_sold_pct 增加
same_source_sync_sell_score 上升
counterparty_pressure_score 上升
```

就强制退出，会有很多误杀。

正确做法：

```text
至少需要 2 轮快照 delta 确认
```

比如：

```text
snapshot_1：早期钱包卖出增加
snapshot_2：继续卖出 + 价格承压 + 对手盘压力上升
```

这才更接近真实结构恶化。

---

## 3. 没有结合盘型

不同盘型下，同一个钱包行为意义不同。

| 盘型 | 钱包卖出含义 |
|---|---|
| 爆拉后高位放量 | 大概率派发风险 |
| 长横盘控盘箱体 | 可能是换手 |
| 二段启动前 | 可能是清筹 |
| 下跌破位 | 大概率结构失败 |
| 横盘缩量 | 需要等 delta，不应马上退出 |

所以你的钱包结构门禁必须是：

```text
pattern-aware wallet gate
```

不能是：

```text
wallet-only exit gate
```

---

# 三、正确退出动作应该分 3 档

不要只有 `FORCE_PAPER_EXIT`。

应该改成：

```text
HOLD
EXIT_MONITOR
FORCE_PAPER_EXIT
```

## 1. HOLD

结构没有明显恶化。

```text
继续持有
继续观察钱包 delta
```

---

## 2. EXIT_MONITOR

风险出现，但证据不够强。

动作：

```text
不立刻退出
提高监控频率
禁止加仓
缩短时间止损
观察下一轮钱包 delta
记录风险事件
```

适合：

```text
早期钱包部分卖出
高结果钱包减仓
counterparty_pressure 中等上升
wallet_structure_score 小幅下降
data_quality 不够高
```

---

## 3. FORCE_PAPER_EXIT

只用于强证据。

必须同时满足：

```text
数据质量足够
钱包结构明确恶化
多轮 delta 确认
与当前盘型冲突
价格/成交/quote 同步支持风险判断
```

---

# 四、什么时候才允许 FORCE_PAPER_EXIT

建议只有这些情况允许强制退出。

## A. 同源组同步出货

```text
same_source_sync_sell_score >= 80
并且 group_sold_pct_delta >= 20
并且 group_remaining_pct 明显下降
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## B. 价格上涨中早期钱包集中派发

```text
price_change_pct > 0
early_wallet_sold_pct_delta >= 25
late_large_buyer_count 增加
counterparty_pressure_score >= 75
```

这说明可能是：

```text
拉升过程中把筹码转给对手盘
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## C. 高结果钱包集体退出

```text
high_result_remaining_pct_delta <= -30
wallet_risk_score_delta >= 20
same_source_sell 同时上升
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## D. 钱包恶化 + K线破位

```text
wallet_risk_score >= 75
并且 price 跌破 control_box_low / POC / AVWAP
并且 volume 放大
```

结论：

```text
FORCE_PAPER_EXIT
```

---

# 五、哪些情况不应该直接 FORCE_EXIT

这些应该先进入 `EXIT_MONITOR`。

```text
1. 单个早期钱包卖出
2. 早期钱包部分减仓但同源组没同步出货
3. 高 ROI 钱包部分止盈
4. 钱包结构 MISSING
5. data_quality_score < 60
6. 长横盘控盘箱体中的正常换手
7. 二段启动前的筹码轮换
8. price 仍在结构位上方
9. quote/security 没恶化
10. 只有一轮快照出现风险
```

特别注意：

```text
wallet_structure_status = MISSING
```

不能强制退出。  
只能：

```text
EXIT_MONITOR / FIX_DATA_SOURCE
```

---

# 六、你现在应该新增一个退出策略层

叫：

```text
wallet_exit_policy
```

不要让 `wallet_structure_gate` 直接决定退出。

结构应该是：

```text
wallet_structure_decision
  ↓
wallet_exit_policy
  ↓
paper_runner action
```

也就是：

```text
钱包结构判断：风险是什么
退出策略层：该不该退出
paper runner：执行 HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
```

---

# 七、建议配置

你可以让系统默认变成保守一点：

```json
{
  "wallet_exit_policy": {
    "enabled": true,
    "default_action": "EXIT_MONITOR",
    "force_exit_min_confidence": 80,
    "min_data_quality_score": 65,
    "require_delta_snapshots": 2,
    "require_pattern_conflict": true,
    "require_market_confirmation": true,
    "shadow_hold_tracking": true,
    "hard_exit_codes": [
      "SAME_SOURCE_SYNC_EXIT",
      "ACTIVE_DISTRIBUTION",
      "HIGH_RESULT_GROUP_EXIT",
      "COUNTERPARTY_ABSORBING",
      "WALLET_RISK_WITH_PRICE_BREAKDOWN"
    ]
  }
}
```

核心是：

```text
默认 EXIT_MONITOR
强证据才 FORCE_EXIT
```

---

# 八、必须加 Shadow Hold Tracking

这是关键。

现在如果系统 FORCE_EXIT 了，你不知道它是对是错。

所以每次触发强制退出后，还要继续模拟一个“如果不退出”的影子仓位。

新增字段：

```text
wallet_exit_trigger_time
wallet_exit_trigger_type
wallet_exit_trigger_score
wallet_exit_action
force_exit_price
shadow_hold_price_15m
shadow_hold_price_30m
shadow_hold_price_60m
shadow_hold_max_profit_after_exit
shadow_hold_max_drawdown_after_exit
false_exit_flag
avoided_drawdown_pct
missed_profit_pct
```

这样你才能知道：

```text
这次强制退出到底是规避了亏损
还是卖飞了后面的上涨
```

---

# 九、日报必须统计 FORCE_EXIT 是否有效

Paper 日报加一段：

```text
Wallet Exit Effectiveness
```

字段：

```text
wallet_force_exit_count
true_positive_exit_count
false_positive_exit_count
false_exit_rate
avg_avoided_drawdown_pct
avg_missed_profit_pct
avg_price_change_after_exit_30m
avg_price_change_after_exit_60m
```

判断：

```text
如果 false_exit_rate 很高
说明钱包退出规则过严
```

例如：

```text
force exit 后 60 分钟价格上涨 > 30%
并且没有触发更深回撤
```

标记：

```text
FALSE_EXIT
```

---

# 十、你现在应该怎么修

当前优先修 4 件事。

## 1. 不要让 wallet_structure 直接触发 FORCE_EXIT

改成：

```text
wallet_structure_signal
  ↓
wallet_exit_policy
  ↓
action
```

---

## 2. 默认从 FORCE_EXIT 降级为 EXIT_MONITOR

除非满足强证据。

```text
单轮钱包风险 → EXIT_MONITOR
多轮确认 + 盘型冲突 + 市场确认 → FORCE_EXIT
```

---

## 3. 加 pattern-aware 判断

必须把当前盘型传进去：

```text
pattern_type
lifecycle_phase
control_box_status
second_stage_candidate
price_structure_status
```

如果是：

```text
LONG_CONTROL_BOX
SECOND_STAGE_EXPANSION
REACCUMULATION
```

则部分钱包卖出不直接退出。

---

## 4. 加 force exit 复盘统计

否则你永远不知道规则对不对。

---

# 十一、给 OpenClaw / Hermes 的修复指令

直接复制：

```text
任务：审计并修正 SIKK-SOL 钱包结构触发 FORCE_PAPER_EXIT 的逻辑。

当前问题：
很多 paper positions 因钱包结构风险直接触发 FORCE_PAPER_EXIT。需要检查这种接入方式是否过于激进。钱包结构不应该默认直接控制退出，而应该通过 wallet_exit_policy 分层判断。

目标：
1. 钱包结构作为风险证据，不直接等于强制退出。
2. 新增 wallet_exit_policy 层。
3. 默认钱包风险触发 EXIT_MONITOR。
4. 只有强证据、多轮 delta、盘型冲突、市场确认时才 FORCE_PAPER_EXIT。
5. 所有 FORCE_EXIT 必须进入后续影子持仓复盘，判断是否误杀。

允许修改：
- sikk_paper_live_runner.py
- sikk_wallet_structure_gate.py
- sikk_wallet_structure_snapshot.py
- sikk_dashboard_site_builder.py
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_wallet_structure_gate.py

禁止：
- 不执行真实 swap
- 不修改真实交易逻辑
- 不删除已有模块
- 不新增复杂后端

新增 wallet_exit_policy：

输入：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- same_source_sync_sell_score
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- same_source_group_sold_pct_delta
- pattern_type
- lifecycle_phase
- price_structure_status
- latest_delta
- current paper position

输出：
- wallet_exit_action: HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_reason
- wallet_exit_evidence

规则：
1. data_quality_score < 65 时，不允许 FORCE_PAPER_EXIT，只能 EXIT_MONITOR。
2. 单轮钱包风险不允许 FORCE_PAPER_EXIT，至少需要 2 轮 delta 或明确 hard_exit_code。
3. pattern_type 为 LONG_CONTROL_BOX / SECOND_STAGE_EXPANSION / REACCUMULATION 时，早期钱包部分卖出默认 EXIT_MONITOR，不直接 FORCE_EXIT。
4. 只有以下 hard_exit_code 允许 FORCE_PAPER_EXIT：
   - SAME_SOURCE_SYNC_EXIT
   - ACTIVE_DISTRIBUTION
   - HIGH_RESULT_GROUP_EXIT
   - COUNTERPARTY_ABSORBING
   - WALLET_RISK_WITH_PRICE_BREAKDOWN

FORCE_PAPER_EXIT 条件：
- wallet_exit_confidence >= 80
- data_quality_score >= 65
- hard_exit_code 命中
- pattern_conflict = true
- market_confirmation = true

EXIT_MONITOR 条件：
- early_wallet_sold_pct_delta >= 10
- counterparty_pressure_score >= 55
- high_result_remaining_pct_delta <= -15
- wallet_risk_score_delta >= 15
- data_quality_score 不足
- 只有单轮快照风险

Paper runner 修改：
1. wallet_exit_action = HOLD → 继续持仓
2. wallet_exit_action = EXIT_MONITOR → 不关闭仓位，标记 exit_monitor=true，提高监控频率
3. wallet_exit_action = FORCE_PAPER_EXIT → 关闭纸面仓位，但创建 shadow_hold_tracking

新增 shadow_hold_tracking 字段：
- wallet_exit_trigger_time
- wallet_exit_trigger_type
- force_exit_price
- shadow_tracking_until
- shadow_hold_price_15m
- shadow_hold_price_30m
- shadow_hold_price_60m
- shadow_hold_max_profit_after_exit
- shadow_hold_max_drawdown_after_exit
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct

Daily report 增加：
Wallet Exit Effectiveness
- wallet_force_exit_count
- exit_monitor_count
- true_positive_exit_count
- false_positive_exit_count
- false_exit_rate
- avg_avoided_drawdown_pct
- avg_missed_profit_pct
- avg_price_change_after_exit_30m
- avg_price_change_after_exit_60m

Visual Console 增加：
1. Paper Lab 显示 FORCE_EXIT / EXIT_MONITOR 数量
2. 显示 false_exit_rate
3. 单币详情显示 wallet_exit_policy 结果
4. 显示 shadow hold tracking

验收：
1. 钱包结构 MISSING 不再触发 FORCE_PAPER_EXIT。
2. 单轮 early wallet sell 不再触发 FORCE_PAPER_EXIT。
3. LONG_CONTROL_BOX / SECOND_STAGE_EXPANSION 盘型下，部分早期钱包卖出进入 EXIT_MONITOR。
4. SAME_SOURCE_SYNC_EXIT + market confirmation 才 FORCE_PAPER_EXIT。
5. 每次 FORCE_PAPER_EXIT 都有 wallet_exit_reason_code 和 evidence。
6. 每次 FORCE_PAPER_EXIT 都创建 shadow hold tracking。
7. Daily report 能统计 false_exit_rate。
8. 不允许真实交易。
```

---

# 十二、当前结论

你现在的怀疑是正确的。

如果很多仓位刚因为钱包结构就被强制退出，说明现在系统可能过于激进。

正确方向不是取消钱包结构，而是：

```text
钱包结构继续保留
但从“直接退出器”
改成“风险证据 + 退出策略层 + 复盘验证层”
```

最终目标：

```text
不是让钱包结构少触发
而是让每一次触发都能回答：
为什么触发？
证据够不够？
是否与盘型冲突？
退出后是否证明正确？
有没有卖飞？
```

这样你的 SIKK 才会从“规则驱动退出”升级成“证据驱动退出”。

---

<!-- source_marker=1609 -->

# SIKK-SOL Visual Console Pro
```text
```text
不修改真实交易逻辑。
不接真实 swap。
# 复制给 Hermes / OpenClaw 的总任务书
```text
1. 不执行真实 swap。
2. 不新增自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
7. 不破坏 sikk_live_run.py 主入口。
11. 可以重构 dashboard 前端，但不能重构交易核心逻辑。
- sikk_dashboard_site_builder.py
- sikk_dashboard_schema.py
- sikk_dashboard_quality_check.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/dashboard_data.json
- data/gmgn_candidates_live_run/site/AGENTS.md
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_dashboard_schema.py
- 真实交易执行逻辑
- swap / broadcast 相关代码
- 私钥 / API key / webhook 配置逻辑
- paper runner 的交易判定逻辑，除非只是增加读取展示字段
# 阶段 0：项目侦察与数据源盘点
```text
1. data/gmgn_candidates_live_run/live_state.json
2. data/gmgn_candidates_live_run/live_board.md
3. data/gmgn_candidates_live_run/tokens/*/token_status.json
4. data/gmgn_candidates_live_run/state_machine/candidate_states.json
5. data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json
7. data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
8. data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
9. data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
10. data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv
11. data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
16. data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.md
- SIKK_DASHBOARD_READINESS_REPORT.md
1. 已存在文件
2. 缺失文件
3. 每个 JSON 的字段样本
4. dashboard_data.json 需要合并哪些字段
5. 当前无法展示的原因
# 阶段 1：统一 Dashboard 数据模型
```text
先定义统一 dashboard_data.json 数据模型，解决当前面板散乱的问题。
- sikk_dashboard_schema.py
定义 dashboard_data.json 的标准结构：
  "paper_positions": [],
  "wallet_structure_summary": {},
  "wallet_missing_reasons": [],
- generated_at
- base_dir
- runtime_status
- data_version
- dashboard_version
- source_files
- stale_warnings
- token_count
- watching_count
- pause_count
- blocked_count
- paper_ready_count
- paper_open_count
- wallet_support_count
- wallet_pause_count
- wallet_block_count
- wallet_missing_count
- wallet_coverage_count
- wallet_coverage_rate
- open_positions
- closed_positions
- closed_win_rate
- avg_closed_pnl_pct
- max_drawdown_pct
- new_paper_entries_today
- paper_exits_today
- candidates
- signal_ready
- wallet_support
- wallet_not_missing
- quote_security_pass
- paper_ready
- paper_open
- paper_closed
- token_symbol
- token_address
- current_state
- priority_level
- signal_level
- signal_gate
- signal_type
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- quote_gate
- security_gate
- paper_status
- paper_pnl_pct
- main_reason
- next_action
- last_update
- market
- signal
- wallet_structure
- quote
- security
- paper
- recent_events
- P0_ACTIVE_POSITION：paper_status 为 OPEN / PAPER_OPEN
- P1_PAPER_READY：current_state 为 PAPER_READY
- P2_STRUCTURE_SUPPORT：wallet_structure_status 为 WALLET_SUPPORT
- P3_WATCHING：current_state 为 WATCHING
- P4_PAUSE：current_state 为 PAUSE
- P5_BLOCKED：current_state 为 BLOCKED 或 wallet_structure_status 为 WALLET_BLOCK
- P6_DATA_MISSING：wallet_structure_status 为 MISSING
- P7_ERROR：current_state 为 ERROR
1. BLOCKED reason
2. WALLET_BLOCK reason
3. wallet MISSING reason
4. WATCHING watching_reason
5. quote reason
- HOLD
- WAIT_SIGNAL
- WAIT_WALLET
- WAIT_QUOTE
- WAIT_SECURITY
- READY_FOR_PAPER
- OPEN_PAPER_POSITION
- EXIT_MONITOR
- FORCE_PAPER_EXIT
- COOLING
- FIX_DATA_SOURCE
- IGNORE
- PAPER_OPEN → HOLD
- PAPER_READY → OPEN_PAPER_POSITION
- WALLET_SUPPORT 但 signal 未通过 → WAIT_SIGNAL
- wallet MISSING → FIX_DATA_SOURCE
- WALLET_BLOCK / BLOCKED → COOLING
- quote 失败 → WAIT_QUOTE
- security 失败 → WAIT_SECURITY
- PAUSE → WAIT_WALLET
- ERROR → FIX_DATA_SOURCE
新增 tests/test_sikk_dashboard_schema.py，测试：
1. priority_level 不为空
2. main_reason 不为空
3. next_action 不为空
4. MISSING token 的 next_action = FIX_DATA_SOURCE
5. BLOCKED token 的 next_action = COOLING
# 阶段 2：Dashboard 数据构建器
```text
实现 sikk_dashboard_site_builder.py，读取现有 SIKK 输出，生成 dashboard_data.json。
- sikk_dashboard_site_builder.py
- tests/test_sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py \
1. 读取 token_status
2. 读取状态机
3. 读取信号
4. 读取 quote/security
5. 读取钱包结构
data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
data/gmgn_candidates_live_run/site/dashboard_data.json
dashboard_data.json 必须包含：
- meta
- kpi
- funnel
- tokens
- opportunities
- paper_positions
- paper_metrics
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- failure_attribution
- system_health
- events
1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
1. wallet_structure_score 高的靠前
2. counterparty_pressure_score 低的靠前
3. data_quality_score 高的靠前
4. paper_pnl_pct 高的靠前
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3 / S4 signal
- quote/security pass
- live_state_exists
- token_status_count
- wallet_decision_count
- paper_open_exists
- paper_closed_exists
- strategy_metrics_exists
- events_exists
- dashboard_data_generated_at
- stale_data_warnings
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready
- data_quality_low
python3 -m py_compile sikk_dashboard_schema.py sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py \
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160
p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")
for k in ["meta","kpi","funnel","tokens","opportunities","paper_positions","entry_block_reasons","system_health","events"]:
print("dashboard_data schema OK")
# 阶段 3：Visual Console 页面骨架
```text
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- Command Center
- Opportunities
- Token Explorer
- Paper Lab
- Wallet Structure
- System Health
- Events
- SIKK-SOL Visual Console Pro
- generated_at
- runtime_status
- auto refresh 状态
- dashboard_version
- KPI cards
- Pipeline funnel
- Entry Block Reasons
- System warning banner
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3/S4 signal
- quote/security pass
- Token 总表
- 搜索框
- current_state 筛选
- wallet_structure_status 筛选
- paper_status 筛选
- reason 搜索
- priority 排序
- 当前开放仓位
- 已关闭统计
- 胜率
- 平均收益
- 最大回撤
- 失败原因 Top
- paper_positions 表
- 钱包结构状态分布
- WALLET_SUPPORT / PAUSE / BLOCK / MISSING 统计
- wallet_missing_reasons
- counterparty_pressure 高风险 token
- 各数据源是否存在
- token_status 数量
- wallet_decision 数量
- paper files 状态
- events 状态
- stale warning
- 深色专业风格。
- 表格紧凑。
- 卡片化。
- 状态 badge。
- 保持金融终端风格，不要花哨。
- 不加入任何交易按钮。
- PAPER_OPEN / PAPER_READY：绿色
- WALLET_SUPPORT：青绿色
- WATCHING / PAUSE：黄色
- BLOCKED / WALLET_BLOCK：红色
- MISSING / DATA_QUALITY_LOW：灰色
- ERROR：紫红色
- POSITIVE PNL：绿色
- NEGATIVE PNL：红色
1. 顶部 KPI
2. 漏斗
3. 重点机会
4. Token 总表
5. Paper Lab
# 阶段 4：Token 点击详情 Drawer
```text
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- sikk_dashboard_site_builder.py
- detailOverlay
- tokenDetailDrawer
- drawerTokenTitle
- drawerTokenAddress
- drawerCloseBtn
- drawerContent
- loadDashboardData()
- renderDashboard()
- renderTokenTable()
- bindTokenClicks()
- openTokenDrawer(tokenAddress)
- closeTokenDrawer()
- renderTokenDetail(token)
- renderSection(title, fields)
- renderField(label, value)
- renderEvents(events)
- 点击 token 行打开右侧 drawer
- 点击遮罩关闭 drawer
- 点击 X 关闭 drawer
- 按 Escape 关闭 drawer
- 找不到 token 时显示 Token not found
- 浏览器控制台不能有 JS 报错
1. Decision
- current_state
- priority_level
- main_reason
- next_action
- last_update
2. Market
- price
- market_cap
- liquidity
- holder_count
- pool_address
3. Signal
- signal_level
- signal_gate
- signal_type
- invalid_level
- reason
4. Wallet Structure
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- dominant_side_status
- chip_transfer_status
- reason
- support_signals
- risk_signals
5. Quote / Security
- quote_gate
- price_deviation_pct
- quote reason
- security_gate
- risk_level
- security reason
- paper_status
- entry_price
- current_price
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- exit_reason
- failure_type
- time
- event_type
- message
1. Token 总表每一行可点击。
2. 点击后右侧 drawer 打开。
3. Drawer 内容完整。
4. 关闭按钮有效。
5. 遮罩关闭有效。
7. dashboard_data.json 每个 token 有 market/signal/wallet_structure/quote/security/paper/recent_events。
# 阶段 5：筛选、排序、搜索、自动刷新
```text
- token_symbol
- token_address
- current_state
- wallet_structure_status
- paper_status
- priority_level
- main_reason
- next_action
- wallet_structure.reason
- quote.reason
- security.reason
- Only PAPER_OPEN
- Only PAPER_READY
- Only WALLET_SUPPORT
- Only BLOCKED
- Only MISSING
- Only HIGH COUNTERPARTY
- priority_level
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- paper_pnl_pct
- last_update
- 默认每 60 秒重新拉取 dashboard_data.json
- Header 显示 last refresh
- 手动 Refresh 按钮
- 加 ?ts=Date.now() 防止缓存
1. 搜索 token 有效。
2. State 筛选有效。
3. Wallet 筛选有效。
4. Paper 筛选有效。
5. Reason 搜索有效。
# 阶段 6：Paper Lab 专业化
```text
让纸面验证区真正能评估策略有效性。
- paper_positions_open.json
- paper_positions_closed.json
- paper_trades.csv
- paper_equity_curve.csv
- strategy_metrics.json
- risk_events.jsonl
- failure_attribution.jsonl
- open_positions
- closed_positions
- win_rate
- avg_pnl_pct
- median_pnl_pct
- best_trade_pct
- worst_trade_pct
- max_drawdown_pct
- avg_hold_time
- sample_confidence
- 0-9 closed：LOW
- 10-19 closed：EARLY
- 20-49 closed：OBSERVABLE
- 50+ closed：MORE_RELIABLE
- token_symbol
- entry_time
- entry_price
- current_price
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- next_action
- token_symbol
- entry_price
- exit_price
- net_pnl_pct
- exit_reason
- failure_type
- wallet_structure_status
- STRUCTURE_FAIL
- LIQUIDITY_FAIL
- QUOTE_FAIL
- SECURITY_FAIL
- MOMENTUM_FAIL
- WALLET_EXIT
- STOP_LOSS
- TIME_STOP
- COUNTERPARTY_ABSORBING
六、按 wallet_structure_status 分组统计：
- WALLET_SUPPORT 胜率
- WALLET_PAUSE 胜率
- WALLET_BLOCK 后续表现
- MISSING 样本表现
1. 当前开放仓位是什么
2. 当前盈亏多少
3. 最大回撤多少
4. 关闭样本是否足够
5. 失败主要集中在哪些原因
# 阶段 7：System Health 与数据质量诊断
```text
- live_state.json exists
- token_status count
- wallet_structure_decision count
- candidate count
- signal summary exists
- quote/security summary exists
- paper open exists
- paper closed exists
- strategy metrics exists
- events exists
- wallet_structure coverage = wallet_decision_count / token_count
- token_status coverage
- quote/security coverage
- signal coverage
- paper output health
如果 dashboard_data generated_at 超过 10 分钟，显示 STALE。
如果 wallet_structure coverage < 80%，显示 WALLET COVERAGE LOW。
- FIX_WALLET_STRUCTURE_PIPELINE
- FIX_TOKEN_STATUS_BUILDER
- FIX_QUOTE_SECURITY_OUTPUT
- FIX_PAPER_OUTPUT
- CHECK_RUNTIME_LOOP
- CHECK_EVENT_LOG
1. 当前系统是否正常
2. 哪些数据源缺失
3. 哪个模块覆盖率低
4. 下一步修什么
# 阶段 8：安全与部署
```text
- private key
- api key
- bot token
- webhook url
- 真实交易签名
- 私密配置
五、增加安全检查命令：
  data/gmgn_candidates_live_run/site sikk_dashboard_site_builder.py | cat
- swap button
- execute button
- broadcast button
- approve real trade button
1. 页面无交易按钮。
2. dashboard_data.json 不含私钥。
3. site/ 目录不含 webhook url。
4. 安全 grep 无真实密钥。
# 阶段 9：接入主流程自动刷新
```text
每轮 sikk_live_run.py 完成后，自动刷新 Visual Console。
1. sikk_live_run.py 每轮结束后调用：
python3 sikk_dashboard_site_builder.py \
2. dashboard builder 失败不能中断主流程。
3. 失败只写入 events/live_events.jsonl。
4. 不影响 paper runner。

---

<!-- source_marker=1767 -->

可以。现在这个问题要从“面板简陋”进一步细化到：

# Token 不能点击进入详情的问题

这不是小问题。  
专业面板里，**Token 总表不能点进去查看详情**，就会导致你只能看一堆表格，无法判断：

```text
这个 token 为什么 WATCHING？
钱包结构为什么 MISSING？
为什么 BLOCKED？
为什么没有 paper entry？
纸面仓位当前风险是什么？
```

所以 v2 里必须补：

> **Token Detail Drawer / 单币详情抽屉**

不是跳转新页面，第一版建议做右侧抽屉，点击表格里的 token 后，右侧弹出详情。

---

# 一、你现在“不能点击进去”的常见原因

一般是这几种：

```text
1. 表格 token 没有绑定 onclick
2. app.js 没有正确加载
3. dashboard_data.json 没有 token_address
4. token 行没有 data-token-address
5. CSS 盖层挡住点击
6. href 指向 token_status.md，但浏览器找不到相对路径
7. JS 报错导致后续点击事件失效
8. dashboard_data.json 里 tokens 是空数组
```

所以不要只改 UI，要同时检查：

```text
HTML 结构
app.js 点击逻辑
dashboard_data.json 字段
CSS 抽屉层
浏览器控制台错误
```

---

# 二、正确交互设计

Token 表格应该这样：

```text
点击 Token 行
  ↓
根据 token_address 从 dashboard_data.tokens 找到完整对象
  ↓
打开右侧 Detail Drawer
  ↓
展示 market / signal / wallet / quote / security / paper / events
```

不要第一版做复杂路由。

不建议现在做：

```text
/token/xxxx 单独页面
复杂前端路由
React Router
后端 API
```

先做：

```text
右侧详情抽屉
```

---

# 三、Token 总表必须有这些字段

每一行必须至少有：

```html
<tr class="token-row" data-token-address="TOKEN_ADDRESS">
```

Token 名称这一列：

```html
<td>
  <button class="token-link" data-token-address="TOKEN_ADDRESS">
    $TOKEN
  </button>
</td>
```

不要只写纯文本：

```html
<td>ABC</td>
```

否则当然不能点。

---

# 四、`dashboard_data.json` 必须包含 detail 所需字段

每个 token 对象至少要有：

```json
{
  "token_symbol": "ABC",
  "token_address": "...",
  "current_state": "WATCHING",
  "priority_level": "P3_WATCHING",
  "main_reason": "wallet_structure_missing",
  "next_action": "FIX_DATA_SOURCE",

  "market": {
    "price": null,
    "market_cap": null,
    "liquidity": null,
    "holder_count": null
  },

  "signal": {
    "signal_level": "S2",
    "signal_gate": "WAIT",
    "signal_type": "CONTROL_BOX"
  },

  "wallet_structure": {
    "wallet_structure_status": "MISSING",
    "wallet_structure_score": 0,
    "wallet_risk_score": 0,
    "counterparty_pressure_score": 0,
    "data_quality_score": 0,
    "dominant_side_status": null,
    "chip_transfer_status": null,
    "reason": "early_wallet_raw.csv missing",
    "support_signals": [],
    "risk_signals": []
  },

  "quote": {
    "quote_gate": "NOT_RUN",
    "price_deviation_pct": null,
    "reason": null
  },

  "security": {
    "security_gate": "NOT_RUN",
    "risk_level": null,
    "reason": null
  },

  "paper": {
    "paper_status": "NONE",
    "entry_price": null,
    "current_price": null,
    "unrealized_pnl_pct": null,
    "max_floating_profit_pct": null,
    "max_drawdown_pct": null,
    "exit_reason": null,
    "failure_type": null
  },

  "recent_events": []
}
```

如果 builder 只给 token 表字段，没有嵌套 detail 字段，点击后也显示不出专业详情。

---

# 五、`index.html` 要加 Detail Drawer 容器

让 OpenClaw / Hermes 改 `index.html`，加入这个结构：

```html
<div id="detailOverlay" class="detail-overlay hidden"></div>

<aside id="tokenDetailDrawer" class="token-detail-drawer hidden">
  <div class="drawer-header">
    <div>
      <div class="drawer-kicker">Token Detail</div>
      <h2 id="drawerTokenTitle">-</h2>
      <div id="drawerTokenAddress" class="muted mono">-</div>
    </div>
    <button id="drawerCloseBtn" class="drawer-close">×</button>
  </div>

  <div id="drawerContent" class="drawer-content">
    <!-- app.js 注入详情 -->
  </div>
</aside>
```

---

# 六、`style.css` 要有抽屉样式

加入：

```css
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 80;
}

.detail-overlay.hidden {
  display: none;
}

.token-detail-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: min(720px, 92vw);
  height: 100vh;
  background: #111827;
  border-left: 1px solid #273244;
  box-shadow: -20px 0 60px rgba(0, 0, 0, 0.45);
  z-index: 90;
  overflow-y: auto;
  transform: translateX(0);
  transition: transform 160ms ease;
}

.token-detail-drawer.hidden {
  transform: translateX(105%);
}

.drawer-header {
  position: sticky;
  top: 0;
  background: #111827;
  border-bottom: 1px solid #273244;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 2;
}

.drawer-kicker {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.drawer-header h2 {
  margin: 4px 0;
  font-size: 22px;
}

.drawer-close {
  background: #1f2937;
  color: #e5e7eb;
  border: 1px solid #374151;
  border-radius: 10px;
  width: 36px;
  height: 36px;
  cursor: pointer;
  font-size: 22px;
}

.drawer-content {
  padding: 18px 20px 40px;
}

.detail-section {
  background: #0b1220;
  border: 1px solid #1f2937;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 14px;
}

.detail-section h3 {
  margin: 0 0 10px;
  font-size: 15px;
  color: #e5e7eb;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 14px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.detail-label {
  font-size: 11px;
  color: #94a3b8;
}

.detail-value {
  font-size: 13px;
  color: #e5e7eb;
  word-break: break-word;
}

.token-link {
  background: transparent;
  border: none;
  color: #93c5fd;
  cursor: pointer;
  font-weight: 700;
  padding: 0;
}

.token-link:hover {
  text-decoration: underline;
}

.token-row {
  cursor: pointer;
}

.token-row:hover {
  background: rgba(59, 130, 246, 0.08);
}
```

---

# 七、`app.js` 要加点击逻辑

核心逻辑如下：

```javascript
let dashboardData = null;
let tokenIndex = new Map();

async function loadDashboardData() {
  const response = await fetch("./dashboard_data.json?ts=" + Date.now());
  dashboardData = await response.json();

  tokenIndex = new Map(
    (dashboardData.tokens || []).map(t => [String(t.token_address), t])
  );

  renderDashboard(dashboardData);
  bindDrawerEvents();
}

function bindDrawerEvents() {
  const closeBtn = document.getElementById("drawerCloseBtn");
  const overlay = document.getElementById("detailOverlay");

  if (closeBtn) closeBtn.addEventListener("click", closeTokenDrawer);
  if (overlay) overlay.addEventListener("click", closeTokenDrawer);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeTokenDrawer();
  });
}

function bindTokenClicks() {
  document.querySelectorAll("[data-token-address]").forEach(el => {
    el.addEventListener("click", (e) => {
      const tokenAddress = e.currentTarget.getAttribute("data-token-address");
      if (!tokenAddress) return;
      openTokenDrawer(tokenAddress);
    });
  });
}

function openTokenDrawer(tokenAddress) {
  const token = tokenIndex.get(String(tokenAddress));

  if (!token) {
    console.warn("Token not found:", tokenAddress);
    return;
  }

  document.getElementById("drawerTokenTitle").textContent =
    `$${token.token_symbol || "UNKNOWN"} | ${token.current_state || "-"}`;

  document.getElementById("drawerTokenAddress").textContent =
    token.token_address || "-";

  document.getElementById("drawerContent").innerHTML = renderTokenDetail(token);

  document.getElementById("detailOverlay").classList.remove("hidden");
  document.getElementById("tokenDetailDrawer").classList.remove("hidden");
}

function closeTokenDrawer() {
  document.getElementById("detailOverlay").classList.add("hidden");
  document.getElementById("tokenDetailDrawer").classList.add("hidden");
}

function val(x) {
  if (x === null || x === undefined || x === "") return "-";
  return String(x);
}

function esc(x) {
  return val(x)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderField(label, value) {
  return `
    <div class="detail-item">
      <div class="detail-label">${esc(label)}</div>
      <div class="detail-value">${esc(value)}</div>
    </div>
  `;
}

function renderSection(title, fields) {
  return `
    <section class="detail-section">
      <h3>${esc(title)}</h3>
      <div class="detail-grid">
        ${fields.map(([label, value]) => renderField(label, value)).join("")}
      </div>
    </section>
  `;
}

function renderTokenDetail(t) {
  const market = t.market || {};
  const signal = t.signal || {};
  const wallet = t.wallet_structure || {};
  const quote = t.quote || {};
  const security = t.security || {};
  const paper = t.paper || {};

  return `
    ${renderSection("Decision", [
      ["Current State", t.current_state],
      ["Priority", t.priority_level],
      ["Main Reason", t.main_reason],
      ["Next Action", t.next_action],
      ["Last Update", t.last_update],
    ])}

    ${renderSection("Market", [
      ["Price", market.price],
      ["Market Cap", market.market_cap],
      ["Liquidity", market.liquidity],
      ["Holders", market.holder_count],
      ["Pool", market.pool_address],
    ])}

    ${renderSection("Signal", [
      ["Signal Level", signal.signal_level || t.signal_level],
      ["Signal Gate", signal.signal_gate || t.signal_gate],
      ["Signal Type", signal.signal_type],
      ["Invalid Level", signal.invalid_level],
      ["Reason", signal.reason],
    ])}

    ${renderSection("Wallet Structure", [
      ["Status", wallet.wallet_structure_status || t.wallet_structure_status],
      ["Structure Score", wallet.wallet_structure_score || t.wallet_structure_score],
      ["Risk Score", wallet.wallet_risk_score || t.wallet_risk_score],
      ["Counterparty Pressure", wallet.counterparty_pressure_score || t.counterparty_pressure_score],
      ["Data Quality", wallet.data_quality_score || t.data_quality_score],
      ["Dominant Side", wallet.dominant_side_status],
      ["Chip Transfer", wallet.chip_transfer_status],
      ["Reason", wallet.reason],
    ])}

    ${renderSection("Quote / Security", [
      ["Quote Gate", quote.quote_gate || t.quote_gate],
      ["Price Deviation", quote.price_deviation_pct],
      ["Quote Reason", quote.reason],
      ["Security Gate", security.security_gate || t.security_gate],
      ["Risk Level", security.risk_level],
      ["Security Reason", security.reason],
    ])}

    ${renderSection("Paper", [
      ["Paper Status", paper.paper_status || t.paper_status],
      ["Entry Price", paper.entry_price],
      ["Current Price", paper.current_price],
      ["Unrealized PnL %", paper.unrealized_pnl_pct || t.paper_pnl_pct],
      ["Max Floating Profit %", paper.max_floating_profit_pct],
      ["Max Drawdown %", paper.max_drawdown_pct],
      ["Exit Reason", paper.exit_reason],
      ["Failure Type", paper.failure_type],
    ])}

    ${renderEvents(t.recent_events || [])}
  `;
}

function renderEvents(events) {
  if (!events.length) {
    return `
      <section class="detail-section">
        <h3>Recent Events</h3>
        <div class="muted">No recent events.</div>
      </section>
    `;
  }

  return `
    <section class="detail-section">
      <h3>Recent Events</h3>
      <div class="event-list">
        ${events.map(e => `
          <div class="event-item">
            <div class="muted">${esc(e.time)}</div>
            <div><strong>${esc(e.event_type)}</strong> ${esc(e.message)}</div>
          </div>
        `).join("")}
      </div>
    </section>
  `;
}
```

重点：渲染完 Token 表后必须调用：

```javascript
bindTokenClicks();
```

比如：

```javascript
function renderTokenTable(tokens) {
  const tbody = document.getElementById("tokenTableBody");

  tbody.innerHTML = tokens.map(t => `
    <tr class="token-row" data-token-address="${esc(t.token_address)}">
      <td>
        <button class="token-link" data-token-address="${esc(t.token_address)}">
          $${esc(t.token_symbol)}
        </button>
      </td>
      <td>${esc(t.current_state)}</td>
      <td>${esc(t.wallet_structure_status)}</td>
      <td>${esc(t.wallet_structure_score)}</td>
      <td>${esc(t.wallet_risk_score)}</td>
      <td>${esc(t.counterparty_pressure_score)}</td>
      <td>${esc(t.paper_status)}</td>
      <td>${esc(t.paper_pnl_pct)}</td>
      <td>${esc(t.main_reason)}</td>
      <td>${esc(t.next_action)}</td>
    </tr>
  `).join("");

  bindTokenClicks();
}
```

---

# 八、注意一个常见 bug：按钮和行同时绑定会触发两次

如果 `<tr>` 和 `<button>` 都有 `data-token-address`，点击按钮可能触发两次。  
可以这样避免：

```javascript
function bindTokenClicks() {
  document.querySelectorAll(".token-row").forEach(row => {
    row.addEventListener("click", (e) => {
      const tokenAddress = row.getAttribute("data-token-address");
      openTokenDrawer(tokenAddress);
    });
  });
}
```

然后 token button 不单独绑定，保留样式即可：

```html
<button class="token-link" type="button">$ABC</button>
```

---

# 九、必须增加空数据提示

如果点击后没有详情，不要空白，要显示：

```text
Token detail missing
```

代码：

```javascript
function openTokenDrawer(tokenAddress) {
  const token = tokenIndex.get(String(tokenAddress));

  if (!token) {
    document.getElementById("drawerTokenTitle").textContent = "Token not found";
    document.getElementById("drawerTokenAddress").textContent = tokenAddress || "-";
    document.getElementById("drawerContent").innerHTML = `
      <section class="detail-section">
        <h3>Missing Detail</h3>
        <div class="detail-value">dashboard_data.json 中没有找到该 token 的详情。</div>
      </section>
    `;
    document.getElementById("detailOverlay").classList.remove("hidden");
    document.getElementById("tokenDetailDrawer").classList.remove("hidden");
    return;
  }

  ...
}
```

---

# 十、给 OpenClaw / Hermes 的精确修复指令

直接复制这段：

```text
任务：修复 SIKK Visual Console v2 中 Token 不能点击进入详情的问题。

当前问题：
网站能打开，但 Token 总表不能点击查看单币详情，导致无法查看每个 token 的 market、signal、wallet_structure、quote/security、paper、reason、next_action 和 recent_events。

要求：
1. 不新增后端。
2. 不使用数据库。
3. 不使用 React。
4. 不接真实 swap。
5. 不改变 paper runner 交易逻辑。
6. 不删除已有模块。
7. 只修改静态网站相关文件和 dashboard_data 构建逻辑。

允许修改：
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

必须实现：

一、dashboard_data.json
每个 token 必须包含完整 detail 字段：
- token_symbol
- token_address
- current_state
- priority_level
- main_reason
- next_action
- market
- signal
- wallet_structure
- quote
- security
- paper
- recent_events

二、index.html
增加右侧 Token Detail Drawer：
- detailOverlay
- tokenDetailDrawer
- drawerTokenTitle
- drawerTokenAddress
- drawerContent
- drawerCloseBtn

三、Token 表格
每个 tr 必须有：
data-token-address="..."

每一行 class="token-row"。
点击任意 token 行，打开对应详情抽屉。

四、app.js
实现：
- tokenIndex = new Map(tokens.map(t => [token_address, t]))
- bindTokenClicks()
- openTokenDrawer(tokenAddress)
- closeTokenDrawer()
- renderTokenDetail(token)
- renderSection()
- renderField()
- renderEvents()

要求：
- 点击 token 行打开 drawer。
- 点击遮罩关闭 drawer。
- 点击 X 关闭 drawer。
- 按 Escape 关闭 drawer。
- 找不到 token 时显示 Token not found。
- main_reason 和 next_action 不能为空。
- 每次重新渲染表格后重新 bindTokenClicks()。

五、style.css
增加：
- detail-overlay
- token-detail-drawer
- drawer-header
- drawer-content
- detail-section
- detail-grid
- token-row:hover
- token-link

六、验收命令：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

验收标准：
1. 打开网站后，Token 总表里的每一行都可以点击。
2. 点击后右侧打开详情抽屉。
3. 详情抽屉显示：
   - Decision
   - Market
   - Signal
   - Wallet Structure
   - Quote / Security
   - Paper
   - Recent Events
4. 关闭按钮有效。
5. 点击遮罩有效。
6. Escape 关闭有效。
7. 浏览器控制台无 JS 报错。
```

---

# 十一、你自己在 VPS 上怎么检查

## 1. 重新生成网站

```bash
cd /root/sikk-gmgn

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

## 2. 检查 dashboard_data 是否有 token detail

```bash
python3 - <<'PY'
import json
from pathlib import Path

p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")
d = json.loads(p.read_text())

tokens = d.get("tokens", [])
print("tokens:", len(tokens))

if tokens:
    t = tokens[0]
    print("sample keys:", sorted(t.keys()))
    print("token:", t.get("token_symbol"), t.get("token_address"))
    print("has market:", "market" in t)
    print("has signal:", "signal" in t)
    print("has wallet_structure:", "wallet_structure" in t)
    print("has quote:", "quote" in t)
    print("has security:", "security" in t)
    print("has paper:", "paper" in t)
    print("main_reason:", t.get("main_reason"))
    print("next_action:", t.get("next_action"))
PY
```

应该看到：

```text
has market: True
has signal: True
has wallet_structure: True
has quote: True
has security: True
has paper: True
```

---

## 3. 检查 HTML 有没有 drawer

```bash
grep -n "tokenDetailDrawer\|detailOverlay\|drawerContent" data/gmgn_candidates_live_run/site/index.html
```

应该能看到对应节点。

---

## 4. 检查 JS 有没有点击函数

```bash
grep -n "openTokenDrawer\|bindTokenClicks\|renderTokenDetail" data/gmgn_candidates_live_run/site/app.js
```

应该能看到函数。

---

## 5. 检查 CSS 有没有 drawer 样式

```bash
grep -n "token-detail-drawer\|detail-overlay\|detail-section" data/gmgn_candidates_live_run/site/style.css
```

---

# 十二、如果还是不能点击，按这个排查

## 1. 浏览器控制台是否有 JS 错误

最常见：

```text
Cannot read properties of null
Unexpected token
dashboard_data.json 404
```

修法：

```text
先修 JS 报错，任何一个 JS 报错都可能导致点击事件不绑定。
```

---

## 2. dashboard_data.json 是否加载成功

浏览器直接打开：

```text
http://96.126.130.99:8080/dashboard_data.json
```

必须能看到 JSON。

---

## 3. app.js 是否加载成功

打开：

```text
http://96.126.130.99:8080/app.js
```

如果 404，说明路径错了。

---

## 4. token 行是否真的有 data-token-address

在浏览器检查元素，看 `<tr>` 有没有：

```html
data-token-address="..."
```

没有就说明表格渲染逻辑没写对。

---

## 5. 是否有透明层挡住表格

CSS 里检查有没有：

```css
pointer-events: none;
z-index 很高的 overlay;
```

如果 overlay 没隐藏，会挡住点击。

---

# 最短结论

你现在要修的不是“点击链接跳转”，而是做：

```text
Token Detail Drawer
```

最小闭环是：

```text
dashboard_data.json 每个 token 有完整详情
→ Token 表格行带 data-token-address
→ app.js 绑定 click
→ 右侧 drawer 展示详情
→ 可关闭
```

这个补完后，面板才从“列表展示”变成“可分析控制台”。

---

<!-- source_marker=1998 -->

对，现在这个网站只是“能打开”，还不是专业面板。  
你现在需要做的不是继续小修样式，而是升级成：

# SIKK-SOL Visual Console v2

定位：

```text
本地 / VPS 静态专业控制台
读取现有 SIKK 输出
展示系统状态、机会、阻断原因、纸面仓位、钱包结构、未入场原因
不执行交易
不接真实 swap
不新增复杂后端
```

我这边没有稳定拉取到你这个 IP 页面内容，所以不能逐项点评页面代码；但根据你描述“太简陋、功能不完善”，现在应该直接按 v2 标准重做信息架构。

---

# 一、为什么现在看起来简陋

大概率是因为当前页面只是：

```text
KPI + 简单表格 + 一些事件
```

但专业控制台需要的是：

```text
分层导航
状态优先级
漏斗诊断
机会池
风险池
单币详情
纸面仓位
未入场原因
系统健康
自动刷新
```

所以问题不是“颜色不好看”，而是：

> **数据没有被组织成决策视图。**

---

# 二、v2 网站必须改成 6 个页面 / 分区

## 1. Command Center｜总控台

一打开先看到：

```text
系统是否正常
本轮发现多少 token
PAPER_OPEN 有几个
PAPER_READY 有几个
WALLET_BLOCK 有几个
钱包结构接入率
新增纸面入场数
未入场主因
```

顶部 KPI 卡片：

```text
Token Count
Wallet Coverage
PAPER_READY
PAPER_OPEN
WALLET_BLOCK
Open Positions
Closed Win Rate
Avg Closed PnL
```

---

## 2. Funnel｜流程漏斗

必须可视化这条链：

```text
Candidates
 → Signal Ready
 → Wallet Support
 → Quote/Security Pass
 → PAPER_READY
 → PAPER_OPEN
```

你现在最需要看到：

```text
到底卡在钱包结构？
卡在 K线？
卡在 quote/security？
还是 paper runner 没入场？
```

这比单纯表格重要。

---

## 3. Opportunities｜重点机会

只显示最值得看的 token：

```text
PAPER_OPEN
PAPER_READY
WALLET_SUPPORT
S3 / S4
quote/security 通过
```

字段：

```text
Token
Priority
State
Signal
Wallet
Structure Score
Risk Score
Counterparty
Paper PnL
Next Action
Reason
```

这个区域不能被 48 个普通 WATCHING 淹没。

---

## 4. Token Explorer｜Token 总表

必须支持：

```text
搜索 token
按 current_state 筛选
按 wallet_structure_status 筛选
按 paper_status 筛选
按 reason 搜索
按 priority 排序
```

字段必须有：

```text
token_symbol
current_state
priority_level
signal_gate
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
quote_gate
security_gate
paper_status
paper_pnl_pct
main_reason
next_action
last_update
```

点击某个 token 后，右侧弹出详情面板。

---

## 5. Token Detail｜单币详情抽屉

点击 token 后展示：

```text
市场数据
K线信号
钱包结构
quote/security
paper 状态
阻断原因
下一步动作
最近事件
```

这是你现在最缺的。  
否则你只能在表格里猜。

---

## 6. Paper Lab｜纸面验证区

展示：

```text
当前开放仓位
已关闭仓位
胜率
平均收益
最大回撤
失败原因 Top
不同 wallet status 的表现
```

当前最需要看：

```text
WALLET_SUPPORT 的 paper 表现
WALLET_BLOCK 后是否真的规避失败
EXIT_MONITOR 是否有效
```

---

# 三、v2 页面交互必须补齐

第一版至少要有这些功能：

```text
1. 自动刷新 dashboard_data.json
2. 刷新时间显示
3. Token 搜索
4. State 筛选
5. Wallet 筛选
6. Paper 筛选
7. Reason 搜索
8. Token 点击详情
9. Priority 排序
10. Missing / Error 高亮
```

不要先做复杂图表。  
先把“看得懂”做好。

---

# 四、视觉布局建议

页面结构：

```text
左侧 Sidebar
  - Command Center
  - Opportunities
  - Token Explorer
  - Paper Lab
  - System Health
  - Events

顶部 Header
  - SIKK-SOL Visual Console
  - Last Update
  - Runtime Status
  - Auto Refresh 状态

主体区域
  - KPI Cards
  - Funnel
  - Tables
  - Detail Drawer
```

颜色规则：

| 状态 | 颜色 |
|---|---|
| PAPER_OPEN / PAPER_READY | 绿色 |
| WALLET_SUPPORT | 青绿色 |
| WATCHING / PAUSE | 黄色 |
| BLOCKED / WALLET_BLOCK | 红色 |
| MISSING | 灰色 |
| ERROR | 紫红色 |

---

# 五、必须补的数据字段

你现在页面简陋，通常不是 UI 问题，而是 `dashboard_data.json` 不够完整。

v2 的 `dashboard_data.json` 应该长这样：

```json
{
  "meta": {
    "generated_at": "...",
    "base_dir": "data/gmgn_candidates_live_run",
    "runtime_status": "OK"
  },
  "kpi": {},
  "funnel": {},
  "tokens": [],
  "opportunities": [],
  "paper_positions": [],
  "wallet_structure_summary": {},
  "wallet_missing_reasons": [],
  "entry_block_reasons": [],
  "events": [],
  "system_health": {}
}
```

每个 token 至少要有：

```json
{
  "token_symbol": "ABC",
  "token_address": "...",
  "current_state": "WATCHING",
  "priority_level": "P3_WATCHING",
  "signal_level": "S2",
  "signal_gate": "WAIT",
  "wallet_structure_status": "MISSING",
  "wallet_structure_score": 0,
  "wallet_risk_score": 0,
  "counterparty_pressure_score": 0,
  "data_quality_score": 0,
  "quote_gate": "NOT_RUN",
  "security_gate": "NOT_RUN",
  "paper_status": "NONE",
  "paper_pnl_pct": null,
  "main_reason": "wallet_structure_missing: early_wallet_raw.csv missing",
  "next_action": "FIX_DATA_SOURCE",
  "last_update": "..."
}
```

关键是：

```text
main_reason 不能为空
next_action 不能为空
priority_level 不能为空
```

---

# 六、现在公网 8080 也要注意

你现在是：

```text
http://96.126.130.99:8080/
```

这意味着很可能是公网直接暴露。

建议你至少做一个安全处理：

```text
第一阶段：只用 SSH 隧道访问
第二阶段：Nginx + Basic Auth
第三阶段：再考虑域名 / HTTPS
```

当前如果面板里有 token、仓位、日志、webhook 配置、路径信息，不建议长期裸奔公网 8080。

更安全的方式：

```bash
ssh -L 8080:127.0.0.1:8080 root@96.126.130.99
```

然后本地访问：

```text
http://127.0.0.1:8080
```

---

# 七、给 OpenClaw / Hermes 的 v2 重做指令

直接复制：

```text
任务：升级 SIKK-SOL 静态可视化网站为 Visual Console v2。

当前问题：
现有 http://96.126.130.99:8080 页面太简陋，信息散乱，无法专业表达系统状态、机会、风险、纸面仓位和未入场原因。

目标：
重做 data/gmgn_candidates_live_run/site/ 下的静态网站控制台。
只做前端静态控制台，不新增后端，不使用数据库，不接真实交易，不加入 swap 按钮。

允许修改 / 新增：
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/dashboard_data.json

禁止：
- 不删除已有模块
- 不改 sikk_live_run.py 主交易逻辑
- 不改 paper runner 交易逻辑
- 不执行真实 swap
- 不新增 FastAPI / React / 数据库
- 不新增登录系统
- 不新增 Telegram 功能

页面结构必须包含：

1. Sidebar 导航
- Command Center
- Opportunities
- Token Explorer
- Paper Lab
- System Health
- Events

2. 顶部 Header
- SIKK-SOL Visual Console
- generated_at
- runtime_status
- auto refresh 状态

3. Command Center
- KPI cards:
  token_count
  wallet_coverage
  paper_ready_count
  paper_open_count
  wallet_block_count
  wallet_missing_count
  open_positions
  closed_win_rate
  avg_closed_pnl

4. Pipeline Funnel
展示：
- candidates
- signal_ready
- wallet_support
- quote_security_pass
- paper_ready
- paper_open

5. Opportunities
只展示：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3/S4 signal
- quote/security pass

6. Token Explorer
字段：
- token_symbol
- current_state
- priority_level
- signal_gate
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- quote_gate
- security_gate
- paper_status
- paper_pnl_pct
- main_reason
- next_action
- last_update

功能：
- token 搜索
- state 筛选
- wallet 筛选
- paper 筛选
- reason 搜索
- priority 排序
- 点击 token 打开详情面板

7. Token Detail Drawer
点击 token 后显示：
- market
- signal
- wallet_structure
- quote
- security
- paper
- main_reason
- next_action
- recent_events

8. Paper Lab
显示：
- 当前开放仓位
- 已关闭仓位统计
- 胜率
- 平均收益
- 最大回撤
- 失败原因 Top
- paper_positions 表

9. Entry Block Reasons
显示：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready
- data_quality_low

10. System Health
显示：
- live_state 是否存在
- token_status 数量
- wallet_structure_decision 数量
- paper files 是否存在
- events 是否存在
- dashboard_data generated_at
- stale data warning

视觉要求：
- 深色专业风格
- 卡片化布局
- 表格紧凑
- 状态 badge
- PAPER_OPEN/PAPER_READY 绿色
- WALLET_SUPPORT 青绿色
- WATCHING/PAUSE 黄色
- BLOCKED/WALLET_BLOCK 红色
- MISSING 灰色
- ERROR 紫红色
- Reason 和 Next Action 不允许为空

数据要求：
dashboard_data.json 必须包含：
- meta
- kpi
- funnel
- tokens
- opportunities
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- paper_positions
- paper_metrics
- events
- system_health

验收命令：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120

ls -lh data/gmgn_candidates_live_run/site

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

验收标准：
打开网站后必须一眼看到：
1. 系统是否正常
2. 当前有没有 PAPER_READY / PAPER_OPEN
3. 钱包结构接入率
4. 为什么没有新增 paper entry
5. 哪些 token 被 BLOCK
6. 当前纸面仓位盈亏
7. 每个 token 的 reason 和 next_action
8. 哪些数据源缺失
```

---

# 八、开发顺序，不要一步到位

让 Hermes 分 3 次做。

## Round 1：只重做 `dashboard_data.json`

目标：

```text
数据完整，不管 UI
```

验收：

```bash
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120
```

必须看到：

```text
kpi
funnel
tokens
entry_block_reasons
paper_positions
system_health
```

---

## Round 2：重做 UI

目标：

```text
index.html + app.js + style.css
```

先实现：

```text
KPI
漏斗
Token 表
筛选
详情抽屉
纸面仓位
事件
```

---

## Round 3：接入主流程刷新

每轮 `sikk_live_run.py` 结束后自动刷新 site：

```bash
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

失败不能中断主系统，只写事件。

---

# 九、最短判断

你现在这个网站不是“修修样式”就行。  
应该升级为：

```text
SIKK-SOL Visual Console v2
```

核心不是更炫，而是：

```text
信息分层
机会优先
原因解释
筛选排序
单币详情
纸面表现
系统健康
```

这样你才会从“看一堆散乱数据”变成“看专业决策控制台”。

---

<!-- source_marker=5177 -->

你说得对。  
前面有些内容已经开始偏“系统扩展”，现在要收回来。

当前不要再继续做：

```text
复杂 dashboard
Discord / Telegram 播报
confirmation ticket
网页筛选
复杂 Runtime 分层
过多状态枚举
过多文件拆分
```

这些不是现在的重点。

---

# 现在最实用的重点

你现在真正需要的是：

```text
系统能自己跑
能发现 token
能告诉你发现了什么 token
能告诉你这个 token 当前为什么通过 / 暂停 / 阻断
能进入纸面交易
能记录纸面结果
能让你每天看到哪些规则有效
```

所以当前只做 **5 个实用核心功能**。

---

# 一、最小实用系统结构

当前只保留这条主线：

```text
候选发现
  ↓
K线信号
  ↓
钱包结构门禁
  ↓
quote / security 检查
  ↓
状态机
  ↓
纸面交易
  ↓
日报复盘
```

其他全部后置。

---

# 二、现在最应该先做的 5 件事

## 1. 自动跑一轮

先不要 loop、dashboard、通知器。

只要做到：

```bash
python sikk_live_run.py
```

运行后自动执行：

```text
发现候选
分析 K线
分析钱包结构
检查 quote
检查 security
更新状态
更新纸面交易
输出结果
```

这是第一优先级。

---

## 2. 输出一个总览文件

只需要一个：

```text
data/gmgn_candidates_live_run/live_board.md
```

里面显示：

```text
发现了哪些 token
每个 token 当前状态
为什么通过 / 暂停 / 阻断
是否进入纸面交易
当前纸面盈亏
```

先不要网页。

---

## 3. 每个 token 输出一个状态文件

只需要：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

里面显示：

```text
K线结论
钱包结构结论
quote 结论
security 结论
状态机结论
paper 状态
```

这比 dashboard 更实用。

---

## 4. 钱包结构只做门禁，不要继续扩展角色

当前钱包结构只输出 4 种状态：

```text
WALLET_SUPPORT
WALLET_PAUSE
WALLET_BLOCK
WALLET_NEUTRAL
```

不要继续扩展太多身份。

核心只看：

```text
早期钱包是否清仓
同源组是否同步卖出
高结果钱包是否退出
是否出现分发
是否出现对手盘承接
```

够用了。

---

## 5. 每天输出纸面日报

只需要：

```text
data/gmgn_candidates_live_run/daily_report.md
```

统计：

```text
候选数
通过数
阻断数
纸面入场数
关闭仓位数
胜率
平均收益
最大回撤
失败原因 Top 5
```

这是最能帮助你判断系统有没有用的东西。

---

# 三、现在不要做的东西

暂时不做：

```text
Telegram / Discord / 微信播报
网页 dashboard
confirmation ticket
自动实盘
复杂 replay
复杂历史地址库
多链扩展
复杂 UI
过多测试文件
复杂模块注册器
```

这些以后再说。

---

# 四、当前最小可运行版本

现在应该把系统压缩成 4 个核心文件：

```text
sikk_live_run.py
sikk_wallet_structure_gate.py
sikk_paper_runner.py
sikk_daily_report.py
```

最多再加：

```text
sikk_config.json
```

就够了。

---

# 五、真正实用的运行结果应该长这样

运行：

```bash
python sikk_live_run.py
```

输出：

```text
本轮发现 12 个 token

$AAA
状态：BLOCKED
原因：早期钱包清仓 88%，同源组同步卖出 74

$BBB
状态：PAUSE
原因：对手盘压力 58，数据质量不足

$CCC
状态：PAPER_READY
原因：K线 S3，钱包结构 SUPPORT，quote/security 通过

$DDD
状态：PAPER_OPEN
当前浮盈：+8.4%
钱包结构：STRUCTURE_HOLDING
```

同时生成：

```text
live_board.md
tokens/<token>/token_status.md
paper_positions.csv
daily_report.md
```

这才是现在最有价值的东西。

---

# 六、当前优先级重新排序

## P0：必须先做

```text
1. sikk_live_run.py 一键跑完整流程
2. live_board.md 总览输出
3. token_status.md 单币状态输出
4. paper_positions.csv 纸面仓位记录
5. daily_report.md 日报
```

## P1：跑稳定后再做

```text
6. loop 定时运行
7. 钱包结构 delta
8. 失败归因
9. SQLite
10. replay
```

## P2：以后再做

```text
11. dashboard
12. 通知机器人
13. confirmation ticket
14. 实盘 gate
15. 历史地址库
```

---

# 七、下一步最实际的任务

现在最应该让 AI / Codex 做的是：

```text
把当前已有的候选发现、K线信号、钱包结构、quote/security、paper runner 串成一个 sikk_live_run.py。
```

要求非常简单：

```text
输入：candidates.json
输出：
- live_board.md
- token_status.md
- paper_positions.csv
- daily_report.md
```

不是继续加功能。

---

# 结论

你现在的判断是对的。

当前系统应该收缩为：

> **最小可运行纸面验证系统**

不是继续升级 Runtime、Dashboard、Webhook、确认票据。

现在唯一重点：

```text
能不能自动发现 token
能不能判断状态
能不能进入纸面交易
能不能记录结果
能不能每天复盘
```

先把这个跑稳，其他全部后置。

---

<!-- source_marker=5376 -->

# SIKK Live Runtime v0.3：5 个关键接缝定稿
```text
paper runner 与 skip 策略协调
> Runtime 不再只是“能跑”，而是能按统一协议调度各模块，并且知道哪些结果过期、哪些 token 要继续处理、哪些进入人工确认。
# 一、K线 / 钱包 / quote / security / paper 模块 CLI 参数统一
## 1. 标准 CLI 协议
```bash
### 通用参数解释
## 2. 各模块统一输出文件
### K线模块
```text
### 钱包结构模块
```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
### quote 模块
```text
### security 模块
```text
### paper runner
```text
data/gmgn_candidates_live_run/paper_positions.csv
## 3. 每个模块输出必须有统一元字段
所有 JSON 输出必须包含：
```json
  "module": "wallet_structure",
```text
## 4. 各模块推荐 stale_after_sec
| security | 1800 秒 | 安全扫描不必每分钟跑 |
## 5. module_runner 调用 CLI 统一代码
## 6. 每个模块的标准 argparse 模板
# 二、module_runner 如何识别模块输出是否过期
```text
## 1. 新增输出新鲜度判断
```text
        "wallet_structure": base_dir / "wallet_structure" / token_address / "wallet_structure_decision.json",
## 2. module_runner 中使用 freshness
# 三、live_dashboard.html 增加状态筛选和搜索
```text
## 1. dashboard 增加控件
在 `sikk_dashboard_builder.py` 的 HTML 中加入：
  <select id="walletFilter" onchange="filterTable()">
## 2. table row 增加 data 属性
  data-wallet="WALLET_SUPPORT"
  data-wallet="{esc(wallet.get("wallet_structure_status"))}"
>
  <td class="{wallet_class(wallet.get("wallet_structure_status"))}">{esc(wallet.get("wallet_structure_status"))}</td>
  <td>{esc(wallet.get("wallet_structure_score"))}</td>
  <td>{esc(wallet.get("wallet_risk_score"))}</td>
  <td>{esc(wallet.get("counterparty_pressure_score"))}</td>
## 3. 增加 JS 筛选逻辑
  const wallet = document.getElementById("walletFilter").value;
    const rowWallet = row.getAttribute("data-wallet") || "";
    const matchWallet = !wallet || rowWallet === wallet;
## 4. table 加 ID
## 5. 增加 CSS
# 四、paper runner 的持仓更新和 token skip 策略如何协调
```text
```text
## 1. 两种处理优先级
### 分析处理
```text
```text
### 持仓处理
```text
## 2. 新增判断：是否有 open paper position
    path = BASE_DIR / "paper_positions.csv"
## 3. 修改 should_process_token
## 4. paper runner 应该独立有 update-open 模式
```bash
```bash
## 5. orchestrator 每轮先更新 open positions
def update_open_paper_positions(config: Dict[str, Any]) -> None:
    update_open_paper_positions(config)
# 五、confirmation ticket 如何接入 PAPER_READY → READY_FOR_CONFIRMATION
```text
```text
## 1. 状态流重建
```text
## 2. ticket 文件目录
```text
## 3. ticket JSON 标准
```json
  "wallet_structure": {
    "wallet_structure_status": "WALLET_SUPPORT",
    "wallet_structure_score": 72,
    "wallet_risk_score": 28,
## 4. 新增 `sikk_confirmation_ticket.py`
        "wallet_structure": token_status.get("wallet_structure", {}),
    w = ticket.get("wallet_structure", {})
## 基础信息
- Ticket：{ticket.get("ticket_id")}
- Token：${ticket.get("token_symbol")}
- Address：{ticket.get("token_address")}
- 状态：{ticket.get("status")}
- 创建时间：{ticket.get("created_at")}
- 过期时间：{ticket.get("expires_at")}
- 建议仓位：{ticket.get("suggested_size_sol")} SOL
## 市场
- 价格：{m.get("price")}
- 市值：{m.get("market_cap")}
- 池子：{m.get("liquidity")}
## 信号
- 信号等级：{sig.get("signal_level")}
- 信号类型：{sig.get("signal_type")}
- Signal Gate：{sig.get("signal_gate")}
## 钱包结构
- 钱包状态：{w.get("wallet_structure_status")}
- 结构分：{w.get("wallet_structure_score")}
- 风险分：{w.get("wallet_risk_score")}
- 对手盘压力：{w.get("counterparty_pressure_score")}
- 原因：{w.get("reason")}
## Quote / Security
- Quote Gate：{q.get("quote_gate")}
- 价格偏差：{q.get("price_deviation_pct")}
- Security Gate：{s.get("security_gate")}
- 风险等级：{s.get("risk_level")}
## 执行限制
- 允许自动实盘：False
- 需要人工确认：True
- 允许 broadcast：False
## 5. token_status_builder 中接入 READY_FOR_CONFIRMATION
def infer_current_state(token_address, signal, wallet, quote, security, paper):
## 6. orchestrator 里从 PAPER_READY 创建 ticket
```json
```json
# 六、CLI 增加 ticket 命令
```bash
# 七、Runtime v0.3 最终运行流
```text
update_open_paper_positions()
      ├─ wallet_structure
build_live_dashboard.html
# 八、当前最优开发顺序
```text
1. 统一所有模块 CLI 参数
2. 所有模块 JSON 输出增加 generated_at / stale_after_sec / expires_at
3. module_runner 改成 freshness 判断，而不是只看文件存在
4. paper runner 增加 update-open 模式
5. skip_policy 增加 has_open_paper_position()
6. dashboard 增加搜索和筛选
# 九、最小验收标准
```bash
```text
1. 各模块使用统一 CLI 参数
2. 已存在但未过期的模块输出会跳过
3. 过期 quote 会重跑
4. BLOCKED token 不会重复跑
5. 有 open paper position 的 token 即使 BLOCKED 也会更新
6. live_dashboard.html 可以搜索 / 筛选
# 十、给 Codex / OpenClaw 的任务提示词
```text
- module_runner
- token_status
- process_trace
- live_dashboard.html
- token_skip_policy
- notifier
所有模块 JSON 输出必须包含：
- token_address
- token_symbol
- module
- status
- gate
- reason
- generated_at
- stale_after_sec
- expires_at
- run_id
- 文件不存在 → stale
- 文件不可读 → stale
- status=ERROR → stale
- expires_at 已过 → stale
- generated_at + stale_after_sec 已过 → stale
- force=True → 强制重跑
wallet_structure stale_after_sec = 600
三、live_dashboard.html 增加搜索和筛选
- searchInput
- stateFilter
- walletFilter
- data-state
- data-wallet
- data-search
四、paper runner 和 skip 策略协调
run_once() 开头先执行 update_open_paper_positions()。
- 创建 confirmation ticket
- 状态进入 READY_FOR_CONFIRMATION
- ticket 10 秒过期
- ticket 只允许人工批准 / 拒绝
- 当前阶段禁止自动 broadcast
- tickets
- approve TICKET_ID
- reject TICKET_ID
- dashboard 可搜索筛选
- 过期模块会重跑
- 未过期模块会跳过
- PAPER_READY 在 human_confirmation 模式下生成 ticket
- open paper position 不会被 skip policy 跳过
# 本次认知升级点
```text
> 系统开始具备“运行治理能力”，而不是简单循环执行脚本。
# 尚未解决问题
```text
1. confirmation ticket 过期自动清理逻辑
2. approved ticket 如何进入真实 execution gate，但仍不自动 broadcast
3. paper runner 的 update-open 真实实现
4. dashboard 增加 PnL 曲线和失败原因统计
5. 模块输出 schema 校验，防止某个模块输出字段缺失导致 Runtime 误判

---

<!-- source_marker=5571 -->

# SIKK Live Runtime v0.2：运行层完整接入
```text
1. run_external_modules_for_token() 如何实际调用 K线 / 钱包 / quote / security / paper 模块
2. live_board.md 如何转成 live_dashboard.html
3. Discord / Telegram webhook 如何配置
4. token_status.json 的状态变化如何写入 process_trace.jsonl
5. loop 模式下如何避免重复处理 BLOCKED / EXPIRED / 无变化 token
> 系统不只是“跑一轮”，而是能持续运行、记录状态变化、生成看板、必要时播报，同时避免重复无效处理。
# 一、Runtime v0.2 总结构
```text
  sikk_dashboard_builder.py      # live_dashboard.html
  sikk_token_skip_policy.py      # loop 跳过策略
```text
  live_dashboard.html
  wallet_structure/<token>/wallet_structure_decision.json
  paper_positions.csv
# 二、`run_external_modules_for_token()` 如何实际调用模块
```text
```text
## 2.1 模块调用原则
```text
1. Python 函数调用
2. subprocess 调用独立脚本
3. 如果输出文件已存在，则只读取，不重复跑
```text
## 2.2 配置文件扩展
```text
```json
    "wallet_structure": {
      "module_name": "sikk.wallet_structure.sikk_candidate_wallet_structure_pipeline",
## 2.3 新增 `sikk_module_runner.py`
        "wallet_structure": BASE_DIR / "wallet_structure" / token_address / "wallet_structure_decision.json",
    1. K线信号
    2. 钱包结构
    3. quote
    4. security
    5. paper runner
        "wallet_structure",
## 2.4 修改 orchestrator 里的调用
# 三、`token_status.json` 状态变化写入 `process_trace.jsonl`
```text
```text
## 3.1 新增 `sikk_trace_logger.py`
    prev_wallet = previous.get("wallet_structure", {}).get("wallet_structure_status")
    cur_wallet = current.get("wallet_structure", {}).get("wallet_structure_status")
        "wallet_changed": prev_wallet != cur_wallet,
        "previous_wallet_status": prev_wallet,
        "current_wallet_status": cur_wallet,
        "wallet_changed": change["wallet_changed"],
        "previous_wallet_status": change["previous_wallet_status"],
        "current_wallet_status": change["current_wallet_status"],
        "wallet_structure": current_status.get("wallet_structure", {}),
## 3.2 orchestrator 接入 trace
```text
# 四、loop 模式下如何避免重复处理 BLOCKED / EXPIRED token
如果不做跳过策略，loop 会每 10 分钟重复处理已经无效的 token。  
```text
## 4.1 跳过策略原则
| 状态 | 处理策略 |
## 4.2 新增 `sikk_token_skip_policy.py`
## 4.3 orchestrator 中接入 skip policy
# 五、live_board.md 转 `live_dashboard.html`
```text
sikk/runtime/sikk_dashboard_builder.py
## 5.1 功能
```text
```text
live_dashboard.html
## 5.2 代码
DASHBOARD_PATH = BASE_DIR / "live_dashboard.html"
def wallet_class(wallet_status: str) -> str:
    wallet_status = str(wallet_status or "").upper()
    if wallet_status == "WALLET_SUPPORT":
    if wallet_status in {"WALLET_PAUSE", "WALLET_NEUTRAL"}:
    if wallet_status == "WALLET_BLOCK":
def build_dashboard_html() -> str:
        wallet = t.get("wallet_structure", {})
          <td class="{wallet_class(wallet.get("wallet_structure_status"))}">{esc(wallet.get("wallet_structure_status"))}</td>
          <td>{esc(wallet.get("wallet_structure_score"))}</td>
          <td>{esc(wallet.get("wallet_risk_score"))}</td>
          <td>{esc(wallet.get("counterparty_pressure_score"))}</td>
def write_dashboard(path: Path = DASHBOARD_PATH) -> None:
    path.write_text(build_dashboard_html(), encoding="utf-8")
    write_dashboard()
## 5.3 orchestrator 中自动生成 HTML
from sikk.runtime.sikk_dashboard_builder import write_dashboard
write_dashboard()
# 六、Discord / Telegram webhook 实际配置
## 6.1 新增 `sikk_notifier.py`
## 6.2 配置 Discord
```json
```text
## 6.3 配置 Telegram
```json
```text
1. 找 BotFather 创建 bot
2. 拿到 bot_token
3. 给 bot 发一条消息
4. 用 getUpdates 查 chat_id
```text
```text
## 6.4 orchestrator 的 emit_event 接通知
# 七、完整运行顺序
```text
            ├─ wallet_structure
write_live_dashboard.html
# 八、当前最优开发顺序
```text
1. 新增 sikk_module_runner.py
2. 在 orchestrator 接入 run_external_modules_for_token()
3. 新增 sikk_trace_logger.py
4. 写 process_trace.jsonl
5. 新增 sikk_token_skip_policy.py
6. loop 接入跳过策略
7. 新增 sikk_dashboard_builder.py
8. 生成 live_dashboard.html
# 九、最小验收标准
```bash
```text
live_dashboard.html
```bash
```text
# 十、直接给 Codex / OpenClaw 的任务提示词
```text
1. kline_signal
2. wallet_structure
3. quote
4. security
5. paper_runner
- python_function
- script
- disabled
- previous_state
- current_state
- previous_wallet_status
- current_wallet_status
- previous_paper_status
- current_paper_status
- latest_action
- latest_reason
- wallet_structure
- signal
- quote
- security
- paper
- module_result
三、loop 跳过策略
- PAPER_OPEN / PAPER_READY 每轮处理
- WATCHING 正常处理
- PAUSE 30 分钟冷却
- BLOCKED 6 小时冷却
- ERROR 30 分钟后重试
- EXPIRED / CLOSED 24 小时冷却或跳过
新增 sikk/runtime/sikk_dashboard_builder.py。
data/gmgn_candidates_live_run/live_dashboard.html
- 状态数量卡片
- token 表格
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- signal / quote / security / paper
- PnL
- latest_reason
- 最新事件
- WALLET_SUPPORT
- WALLET_BLOCK
- PAPER_READY
- PAPER_OPENED
- PAPER_FORCE_EXIT
- ERROR
- DAILY_REPORT_READY
- live_state.json
- live_board.md
- live_dashboard.html
- events/live_events.jsonl
- tokens/<token>/token_status.json
- tokens/<token>/token_status.md
- tokens/<token>/process_trace.jsonl
- BLOCKED 不会每轮重复跑
- PAUSE 会降低频率
- PAPER_OPEN 会持续更新
- ERROR 会延迟重试
# 本次认知升级点
```text
> 系统开始具备真正的 Runtime 能力，而不只是分析能力。
# 尚未解决问题
```text
1. K线 / 钱包 / quote / security / paper 各模块的真实 CLI 参数统一
2. module_runner 如何识别模块输出是否过期
3. live_dashboard.html 增加状态筛选和搜索
4. paper runner 的持仓更新和 token skip 策略如何协调
5. confirmation ticket 如何接入 PAPER_READY → READY_FOR_CONFIRMATION

---

<!-- source_marker=5763 -->

# SIKK Live Runtime v0.1：运行层接入方案
```text
1. sikk_live_orchestrator.py 如何实际接入现有候选发现模块
2. token_status.json 如何合并 K线、钱包、quote、security、paper 数据
3. sikk_cli.py 的完整命令行代码
4. live_board.md 是否需要转成网页 dashboard
5. 是否要增加 Telegram / Discord / 微信机器人播报
> 现在不要先做复杂网页，也不要先做机器人。  
> 先做 **本地运行层 + 文件看板 + CLI 查看工具**。  
> 等它能稳定跑 24 小时，再加网页 dashboard 和机器人播报。
# 一、推荐新增目录
```text
```text
  wallet_structure/
      wallet_structure_decision.json
# 二、候选发现模块怎么接入 orchestrator
```text
1. 已经输出 candidates.json
2. 是一个 Python 函数
3. 是一个独立脚本
4. 还只是手动导出的 CSV / JSON
## 1. 新增 `sikk_candidate_adapter.py`
```text
DEFAULT_CANDIDATES_JSON = BASE_DIR / "candidates.json"
DEFAULT_CANDIDATES_CSV = BASE_DIR / "candidates.csv"
def load_candidates_from_json(path: Path = DEFAULT_CANDIDATES_JSON) -> List[Dict[str, Any]]:
def load_candidates_from_csv(path: Path = DEFAULT_CANDIDATES_CSV) -> List[Dict[str, Any]]:
    output_path: Path = DEFAULT_CANDIDATES_JSON,
    1. Python 函数
    2. 独立脚本
    3. candidates.json
    4. candidates.csv
            output_path=Path(config.get("output_path", DEFAULT_CANDIDATES_JSON)),
            Path(config.get("path", DEFAULT_CANDIDATES_CSV))
    # 默认 JSON
        Path(config.get("path", DEFAULT_CANDIDATES_JSON))
## 2. 配置文件建议
```text
```json
```json
```json
# 三、`token_status.json` 如何合并 K线、钱包、quote、security、paper 数据
> 所有模块不直接互相强耦合，而是各自输出文件；`sikk_status_builder.py` 负责读取这些文件并合并成单币状态。
## 1. 推荐每个模块输出
```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
data/gmgn_candidates_live_run/paper_positions.csv
## 2. 新增 `sikk_status_builder.py`
```text
    rows = read_csv_rows(BASE_DIR / "paper_positions.csv")
    wallet: Mapping[str, Any],
    wallet_status = wallet.get("wallet_structure_status")
    if wallet_status == "WALLET_BLOCK":
    if wallet_status == "WALLET_PAUSE":
        wallet_status == "WALLET_SUPPORT"
    wallet = read_json_optional(base_dir / "wallet_structure" / token_address / "wallet_structure_decision.json")
    current_state = infer_current_state(signal, wallet, quote, security, paper)
        "wallet_structure": {
            "wallet_structure_status": wallet.get("wallet_structure_status", "MISSING"),
            "wallet_structure_score": wallet.get("wallet_structure_score"),
            "wallet_risk_score": wallet.get("wallet_risk_score"),
            "counterparty_pressure_score": wallet.get("counterparty_pressure_score"),
            "data_quality_score": wallet.get("data_quality_score"),
            "wallet_structure_factor": wallet.get("wallet_structure_factor"),
            "dominant_side_status": wallet.get("dominant_side_status"),
            "chip_transfer_status": wallet.get("chip_transfer_status"),
            "reason": wallet.get("reason"),
            "support_signals": wallet.get("support_signals", []),
            "risk_signals": wallet.get("risk_signals", []),
        "latest_action": infer_latest_action(current_state, wallet, quote, security, paper),
        "latest_reason": infer_latest_reason(current_state, wallet, quote, security, paper),
    wallet: Mapping[str, Any],
    wallet: Mapping[str, Any],
        return wallet.get("reason") or security.get("reason") or quote.get("reason") or "等待更多证据"
        return "signal / wallet / quote / security 已通过，允许纸面入场"
    w = status.get("wallet_structure", {})
## 当前状态
- Token：{status.get("token_address")}
- 状态：{status.get("current_state")}
- 最新动作：{status.get("latest_action")}
- 原因：{status.get("latest_reason")}
- 更新时间：{status.get("last_update")}
## 市场
- 价格：{m.get("price")}
- 市值：{m.get("market_cap")}
- 池子：{m.get("liquidity")}
- 持有人：{m.get("holder_count")}
- 来源：{m.get("source")}
## K线 / 信号
- 信号等级：{sig.get("signal_level")}
- 信号类型：{sig.get("signal_type")}
- 信号门禁：{sig.get("signal_gate")}
- 失效位：{sig.get("invalid_level")}
- 原因：{sig.get("reason")}
## 钱包结构
- 钱包状态：{w.get("wallet_structure_status")}
- 结构分：{w.get("wallet_structure_score")}
- 风险分：{w.get("wallet_risk_score")}
- 对手盘压力：{w.get("counterparty_pressure_score")}
- 数据质量：{w.get("data_quality_score")}
- 主导侧状态：{w.get("dominant_side_status")}
- 筹码迁移：{w.get("chip_transfer_status")}
- 原因：{w.get("reason")}
### 支持信号
### 风险信号
## Quote
- Quote 门禁：{q.get("quote_gate")}
- OKX：{q.get("okx_price")}
- GMGN：{q.get("gmgn_price")}
- 价格偏差：{q.get("price_deviation_pct")}
- 原因：{q.get("reason")}
## Security
- Security 门禁：{sec.get("security_gate")}
- 风险等级：{sec.get("risk_level")}
- 原因：{sec.get("reason")}
## Paper
- Paper 状态：{p.get("paper_status")}
- 仓位 ID：{p.get("position_id")}
- 入场价：{p.get("entry_price")}
- 当前价：{p.get("current_price")}
- 浮盈：{p.get("unrealized_pnl_pct")}
- 净收益：{p.get("net_pnl_pct")}
- 最大浮盈：{p.get("max_floating_profit_pct")}
- 最大回撤：{p.get("max_drawdown_pct")}
- 退出原因：{p.get("exit_reason")}
- 失败归因：{p.get("failure_type")}
# 四、`sikk_live_orchestrator.py` 实际接入版本
```text
    - K线信号模块
    - 钱包结构 pipeline
    - quote 模块
    - security 模块
    - paper runner
    # run_candidate_wallet_structure_pipeline_for_one_token(token)
        wallet_status = status.get("wallet_structure", {}).get("wallet_structure_status")
        if wallet_status in {"WALLET_SUPPORT", "WALLET_PAUSE", "WALLET_BLOCK"}:
                wallet_status,
                f"{token.get('token_symbol')} 钱包结构：{wallet_status}，原因：{status.get('wallet_structure', {}).get('reason')}",
                data=status.get("wallet_structure", {}),
        wallet = r.get("wallet_structure", {}).get("wallet_structure_status")
            f"| {token} | {state} | {wallet} | {signal} | {quote} | {security} | {paper} | {pnl} | {reason} |"
# 五、`sikk_cli.py` 完整命令行代码
```text
```bash
## 代码
    print(f"Wallet Structure: {BASE_DIR / 'wallet_structure'}")
# 六、`live_board.md` 是否需要转成网页 dashboard？
## 当前阶段：不需要先做复杂网页
```text
1. live_board.md
2. token_status.md
3. sikk_cli.py
4. daily_report.md
5. 稳定跑 24 小时
不要一开始做复杂 dashboard。  
```text
## 什么时候做网页 dashboard？
```text
1. loop 模式能连续运行 24 小时
2. 至少处理过 30 个 token
3. token_status.json 字段稳定
4. paper_positions.csv 字段稳定
5. live_board.md 已经能满足日常观察
## 网页 dashboard 的最低版本
```text
data/gmgn_candidates_live_run/live_dashboard.html
```text
```text
```text
# 七、是否增加 Telegram / Discord / 微信机器人播报？
## 结论
```text
1. 本地 event log
2. latest_events.md
3. CLI events
4. Discord / Telegram webhook
5. 微信机器人
## 为什么不先做微信？
```text
```text
## 播报分级
```text
```text
## 播报配置
```json
## 后续通知器骨架
```text
# notify_event(event, config)
# 八、现在最优开发顺序
```text
1. 建 config/sikk_runtime_config.json
2. 建 sikk_candidate_adapter.py
3. 建 sikk_status_builder.py
4. 改 sikk_live_orchestrator.py
5. 建 sikk_cli.py
7. 再接真实候选发现模块
# 九、最小验收标准
```bash
```text
```bash
```text
```bash
```bash
# 十、下一步给 AI / Codex 的任务提示词
```text
1. 系统可以自己跑一轮
2. 系统可以读取候选 token
3. 系统可以生成每个 token 的 token_status.json / token_status.md
4. 系统可以生成 live_board.md
5. 系统可以记录 live_events.jsonl
7. 当前阶段先不做复杂网页 dashboard
8. 当前阶段先不接真实自动实盘
- sikk/runtime/sikk_candidate_adapter.py
- sikk/runtime/sikk_status_builder.py
- sikk/runtime/sikk_live_orchestrator.py
- sikk/runtime/sikk_cli.py
1. file_json：读取 data/gmgn_candidates_live_run/candidates.json
2. file_csv：读取 data/gmgn_candidates_live_run/candidates.csv
3. python_function：从指定 module/function 调用候选发现
4. script：运行独立候选发现脚本后读取 candidates.json
- signals/<token>/signal.json
- wallet_structure/<token>/wallet_structure_decision.json
- quotes/<token>/quote.json
- security/<token>/security.json
- paper_positions.csv
- data/gmgn_candidates_live_run/tokens/<token>/token_status.json
- data/gmgn_candidates_live_run/tokens/<token>/token_status.md
- data/gmgn_candidates_live_run/live_board.md
- data/gmgn_candidates_live_run/live_state.json
- data/gmgn_candidates_live_run/events/live_events.jsonl
- status
- events
- inspect TOKEN_ADDRESS
- board
- run-once
- loop
- paths
# 本次认知升级点
> SIKK-SOL 不只是分析系统，还必须是运行系统。
```text
```text
```text
# 尚未解决问题
```text
1. run_external_modules_for_token() 里如何实际调用 K线 / 钱包 / quote / security / paper 模块
2. live_board.md 转 live_dashboard.html 的静态网页版本
3. Discord / Telegram webhook 的实际配置方式
4. token_status.json 中状态变化如何写入 process_trace.jsonl
5. loop 模式下如何避免重复处理已经 BLOCKED 或已过期 token

---

<!-- source_marker=5971 -->

你说得对。  
现在你的系统主要是在搭建“分析模块”，但还缺一个真正让系统活起来的部分：

> **运行控制层 + 可观测层 + 播报层**

没有这三层，就会出现你说的情况：

```text
不会自己运行
不知道发现了哪个代币
不知道流程跑到哪一步
不知道某个 token 当前是什么状态
不知道为什么进 / 不进 PAPER_READY
没有地方看实时结果
```

所以现在系统必须从“分析脚本集合”升级成：

> **SIKK-SOL 实时运行控制台系统**

---

# 一、当前真正缺的不是分析逻辑，而是运行系统

你现在已经设计了很多模块：

```text
候选发现
K线分析
钱包结构门禁
quote 检查
security 扫描
paper runner
失败归因
日报
```

但缺少一个主控：

```text
谁来定时调用这些模块？
谁来记录每一步发生了什么？
谁来告诉你发现了哪个 token？
谁来生成当前 token 状态？
谁来把结果显示出来？
```

所以现在最应该新增的是：

```text
sikk_live_orchestrator.py       主控运行器
sikk_event_logger.py            事件播报器
sikk_token_status_board.py      单币状态面板
sikk_cli.py                     命令行查看工具
```

---

# 二、新系统大局应该这样重建

```text
SIKK Live Orchestrator
  ↓
定时发现候选 token
  ↓
发现后写入事件日志
  ↓
对每个 token 跑：
  1. 候选过滤
  2. K线信号
  3. 钱包结构门禁
  4. quote 检查
  5. security 检查
  6. 状态机更新
  7. paper runner 更新
  ↓
每一步都写事件日志
  ↓
生成 token_status.json
  ↓
生成 live_board.md
  ↓
你可以随时查看：
  当前发现了什么 token
  每个 token 在哪个状态
  为什么被 BLOCK / PAUSE / PAPER_READY
  当前纸面仓位盈亏
```

---

# 三、需要新增的运行目录

建议统一到：

```text
data/gmgn_candidates_live_run/
```

里面增加：

```text
data/gmgn_candidates_live_run/
  live_state.json
  live_board.md

  events/
    live_events.jsonl
    latest_events.md

  tokens/
    <token_address>/
      token_status.json
      token_status.md
      process_trace.jsonl

  runs/
    run_20260502_120000.json
    latest_run.json

  reports/
    daily_report.md
    daily_wallet_structure_report.md
```

---

# 四、第一层：主控运行器

新增：

```text
sikk_live_orchestrator.py
```

它负责让系统自己跑起来。

---

## 4.1 运行模式

需要支持三种模式：

```bash
python sikk_live_orchestrator.py --mode once
python sikk_live_orchestrator.py --mode loop
python sikk_live_orchestrator.py --mode paper-update
```

含义：

| 模式 | 作用 |
|---|---|
| once | 手动跑一轮完整流程 |
| loop | 持续循环运行 |
| paper-update | 只更新纸面持仓 |

---

## 4.2 建议运行频率

```text
候选发现：每 10 分钟
K线 / 信号：每 10 分钟
钱包结构：每 10 分钟
quote / security：每 5 分钟
paper 持仓更新：每 3 分钟
日报：每天一次
```

---

## 4.3 主控流程

```text
run_cycle()
  ↓
discover_candidates()
  ↓
emit TOKEN_DISCOVERED
  ↓
for each token:
    run_kline_signal()
    emit SIGNAL_CHECKED

    run_wallet_structure_gate()
    emit WALLET_GATE_RESULT

    run_quote_gate()
    emit QUOTE_CHECKED

    run_security_gate()
    emit SECURITY_CHECKED

    update_state_machine()
    emit STATE_CHANGED

    update_paper_runner()
    emit PAPER_UPDATED

    build_token_status()
    emit TOKEN_STATUS_UPDATED
  ↓
build_live_board()
```

---

# 五、第二层：事件播报器

新增：

```text
sikk_event_logger.py
```

它的作用是让系统“会说话”。

每发生一件事，都写入：

```text
data/gmgn_candidates_live_run/events/live_events.jsonl
```

---

## 5.1 事件类型

```text
RUN_STARTED
RUN_FINISHED

TOKEN_DISCOVERED
TOKEN_FILTERED_OUT
TOKEN_ACCEPTED

SIGNAL_DETECTED
SIGNAL_BLOCKED

WALLET_SUPPORT
WALLET_PAUSE
WALLET_BLOCK
WALLET_NEUTRAL

QUOTE_OK
QUOTE_FAIL
SECURITY_OK
SECURITY_BLOCK

STATE_CHANGED

PAPER_OPENED
PAPER_UPDATED
PAPER_EXIT_MONITOR
PAPER_FORCE_EXIT
PAPER_CLOSED

DAILY_REPORT_READY
ERROR
```

---

## 5.2 事件格式

```json
{
  "time": "2026-05-02T12:00:00Z",
  "event_type": "TOKEN_DISCOVERED",
  "token_address": "xxx",
  "token_symbol": "TEST",
  "level": "INFO",
  "message": "发现新候选 token TEST，市值 120000，池子 45000",
  "data": {
    "market_cap": 120000,
    "liquidity": 45000,
    "holder_count": 830
  }
}
```

---

## 5.3 播报文本示例

发现 token：

```text
[12:00:03] 发现候选：$TEST
市值：120K
池子：45K
持有人：830
状态：进入初筛
```

钱包门禁通过：

```text
[12:01:12] $TEST 钱包结构：WALLET_SUPPORT
结构分：72
风险分：28
对手盘压力：32
原因：早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出
```

钱包阻断：

```text
[12:02:44] $TEST 钱包结构：WALLET_BLOCK
原因：同源组同步卖出达到 76，早期钱包剩余筹码不足
动作：BLOCKED
```

paper 入场：

```text
[12:04:21] $TEST 进入 PAPER_READY
live_entry_price：0.000123
wallet_structure_factor：1.15
quote/security：通过
```

paper 强制退出：

```text
[12:19:02] $TEST 触发 FORCE_PAPER_EXIT
原因：对手盘压力从 38 上升到 74，疑似筹码向晚期承接方转移
归因：COUNTERPARTY_ABSORBING
```

---

# 六、第三层：单币状态面板

新增：

```text
sikk_token_status_board.py
```

每个 token 都要生成：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.json
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

---

## 6.1 token_status.json 标准

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TEST",
  "last_update": "2026-05-02T12:05:00Z",

  "current_state": "PAPER_READY",
  "previous_state": "WATCHING",

  "market": {
    "price": 0.000123,
    "market_cap": 120000,
    "liquidity": 45000,
    "holder_count": 830
  },

  "signal": {
    "signal_level": "S3",
    "signal_type": "CONTROL_BOX_BREAKOUT_PULLBACK",
    "signal_gate": "ALLOW",
    "reason": "控盘箱体突破后回踩未破"
  },

  "wallet_structure": {
    "wallet_structure_status": "WALLET_SUPPORT",
    "wallet_structure_score": 72,
    "wallet_risk_score": 28,
    "counterparty_pressure_score": 32,
    "data_quality_score": 76,
    "dominant_side_status": "STRUCTURE_HOLDING",
    "chip_transfer_status": "NO_MAJOR_TRANSFER",
    "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出"
  },

  "quote": {
    "quote_gate": "ALLOW",
    "okx_price": 0.000123,
    "gmgn_price": 0.000122,
    "price_deviation_pct": 0.8
  },

  "security": {
    "security_gate": "ALLOW",
    "risk_level": "LOW"
  },

  "paper": {
    "paper_status": "OPEN",
    "entry_price": 0.000123,
    "current_price": 0.000131,
    "unrealized_pnl_pct": 6.5,
    "max_floating_profit_pct": 12.2,
    "max_drawdown_pct": -3.1
  },

  "latest_action": "HOLD",
  "latest_reason": "钱包结构未触发退出条件"
}
```

---

## 6.2 token_status.md 展示格式

```markdown
# $TEST Token 状态

## 当前状态

- 状态：PAPER_READY
- 上次更新：2026-05-02 12:05 UTC
- 最新动作：HOLD

## 市场数据

- 市值：120K
- 池子：45K
- 持有人：830
- 当前价格：0.000123

## SIKK 信号

- 信号等级：S3
- 信号类型：控盘箱体突破回踩
- 信号结论：ALLOW

## 钱包结构

- 钱包状态：WALLET_SUPPORT
- 结构分：72
- 风险分：28
- 对手盘压力：32
- 数据质量：76
- 主导侧状态：STRUCTURE_HOLDING
- 筹码迁移：NO_MAJOR_TRANSFER

原因：

早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出。

## Quote / Security

- Quote：ALLOW
- Security：ALLOW
- 价格偏差：0.8%

## Paper 仓位

- 入场价：0.000123
- 当前价：0.000131
- 浮盈：6.5%
- 最大浮盈：12.2%
- 最大回撤：-3.1%
```

---

# 七、第四层：总览看板

新增：

```text
data/gmgn_candidates_live_run/live_board.md
```

---

## 7.1 live_board.md 示例

```markdown
# SIKK-SOL Live Board

更新时间：2026-05-02 12:10 UTC

## 总览

- 本轮发现 token：12
- 通过初筛：5
- WALLET_SUPPORT：2
- WALLET_PAUSE：1
- WALLET_BLOCK：2
- PAPER_READY：1
- PAPER_OPEN：1
- BLOCKED：4

## 当前关注 token

| Token | State | Wallet | Signal | Quote | Security | Paper PnL | Reason |
|---|---|---|---|---|---|---:|---|
| TEST | PAPER_OPEN | SUPPORT | S3 | ALLOW | ALLOW | +6.5% | 结构维持 |
| AAA | PAUSE | PAUSE | S2 | ALLOW | ALLOW | - | 对手盘压力偏高 |
| BBB | BLOCKED | BLOCK | S3 | - | - | - | 同源组同步卖出 |
```

这个文件就是你每天最该看的“控制台”。

---

# 八、第五层：命令行查看工具

新增：

```text
sikk_cli.py
```

目标是让你可以直接问系统：

```bash
python sikk_cli.py status
python sikk_cli.py events
python sikk_cli.py inspect TOKEN_ADDRESS
python sikk_cli.py board
python sikk_cli.py run-once
python sikk_cli.py loop
```

---

## 8.1 命令含义

| 命令 | 作用 |
|---|---|
| status | 查看系统当前状态 |
| events | 查看最新事件 |
| inspect TOKEN | 查看某个 token 详情 |
| board | 打开 / 输出 live_board |
| run-once | 手动跑一轮 |
| loop | 持续运行 |
| paper | 更新纸面仓位 |

---

## 8.2 CLI 示例输出

```bash
python sikk_cli.py status
```

输出：

```text
SIKK-SOL 当前状态

运行模式：loop
最近一轮：2026-05-02 12:10 UTC
发现 token：12
WATCHING：5
PAPER_READY：1
PAPER_OPEN：1
PAUSE：2
BLOCKED：4

最新事件：
[12:09] $TEST PAPER_OPEN +6.5%
[12:08] $BBB WALLET_BLOCK，同源组同步卖出
[12:07] $AAA WALLET_PAUSE，对手盘压力 58
```

---

# 九、最小主控代码骨架

新增：

```text
sikk_live_orchestrator.py
```

```python
from __future__ import annotations

import time
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path("data/gmgn_candidates_live_run")
EVENTS_PATH = BASE_DIR / "events" / "live_events.jsonl"
LIVE_STATE_PATH = BASE_DIR / "live_state.json"
LIVE_BOARD_PATH = BASE_DIR / "live_board.md"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_type: str, message: str, token: dict | None = None, level: str = "INFO", data: dict | None = None):
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "time": iso_now(),
        "event_type": event_type,
        "level": level,
        "token_address": token.get("token_address") if token else None,
        "token_symbol": token.get("token_symbol") if token else None,
        "message": message,
        "data": data or {},
    }

    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[{event['time']}] {event_type}: {message}")


def discover_candidates() -> List[Dict[str, Any]]:
    """
    这里接你的 GMGN 候选发现逻辑。
    v1.0 可以先读取 candidates.json。
    """
    path = BASE_DIR / "candidates.json"

    if not path.exists():
        emit_event("ERROR", "没有找到 candidates.json，候选发现为空", level="ERROR")
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data.get("candidates", [])

    if isinstance(data, list):
        return data

    return []


def run_token_pipeline(token: Dict[str, Any]) -> Dict[str, Any]:
    """
    这里应该接入：
    1. K线信号
    2. 钱包结构 pipeline
    3. quote gate
    4. security gate
    5. state machine
    6. paper runner
    """

    emit_event(
        "TOKEN_DISCOVERED",
        f"发现候选 {token.get('token_symbol')}，进入分析流程",
        token=token,
        data=token,
    )

    # v1.0 占位状态
    status = {
        "token_address": token.get("token_address"),
        "token_symbol": token.get("token_symbol"),
        "current_state": "WATCHING",
        "wallet_structure_status": "UNKNOWN",
        "signal_gate": "UNKNOWN",
        "quote_gate": "UNKNOWN",
        "security_gate": "UNKNOWN",
        "paper_status": "NONE",
        "reason": "等待模块接入",
        "last_update": iso_now(),
    }

    # 后续这里实际调用：
    # run_candidate_wallet_structure_pipeline_for_one_token(token)
    # apply_wallet_structure_gate_to_state(...)
    # update_paper_position(...)

    write_token_status(token, status)

    return status


def write_token_status(token: Dict[str, Any], status: Dict[str, Any]):
    token_address = token.get("token_address")
    token_dir = BASE_DIR / "tokens" / token_address
    token_dir.mkdir(parents=True, exist_ok=True)

    json_path = token_dir / "token_status.json"
    md_path = token_dir / "token_status.md"

    json_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

    md = f"""# ${status.get('token_symbol')} 状态

- Token：{status.get('token_address')}
- 当前状态：{status.get('current_state')}
- 钱包结构：{status.get('wallet_structure_status')}
- Signal：{status.get('signal_gate')}
- Quote：{status.get('quote_gate')}
- Security：{status.get('security_gate')}
- Paper：{status.get('paper_status')}
- 原因：{status.get('reason')}
- 更新时间：{status.get('last_update')}
"""
    md_path.write_text(md, encoding="utf-8")


def build_live_board(status_rows: List[Dict[str, Any]]):
    lines = []
    lines.append("# SIKK-SOL Live Board")
    lines.append("")
    lines.append(f"更新时间：{iso_now()}")
    lines.append("")

    lines.append("## 当前 Token 状态")
    lines.append("")
    lines.append("| Token | State | Wallet | Signal | Quote | Security | Paper | Reason |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for r in status_rows:
        lines.append(
            f"| {r.get('token_symbol')} "
            f"| {r.get('current_state')} "
            f"| {r.get('wallet_structure_status')} "
            f"| {r.get('signal_gate')} "
            f"| {r.get('quote_gate')} "
            f"| {r.get('security_gate')} "
            f"| {r.get('paper_status')} "
            f"| {r.get('reason')} |"
        )

    LIVE_BOARD_PATH.write_text("\n".join(lines), encoding="utf-8")


def save_live_state(status_rows: List[Dict[str, Any]]):
    state = {
        "last_update": iso_now(),
        "token_count": len(status_rows),
        "tokens": status_rows,
    }
    LIVE_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_once():
    emit_event("RUN_STARTED", "SIKK-SOL 开始运行一轮")

    candidates = discover_candidates()
    status_rows = []

    for token in candidates:
        try:
            status = run_token_pipeline(token)
            status_rows.append(status)
        except Exception as e:
            emit_event(
                "ERROR",
                f"{token.get('token_symbol')} 处理失败：{e}",
                token=token,
                level="ERROR",
            )

    build_live_board(status_rows)
    save_live_state(status_rows)

    emit_event("RUN_FINISHED", f"本轮结束，处理 token 数：{len(status_rows)}")


def run_loop(interval_sec: int = 600):
    emit_event("RUN_STARTED", f"进入 loop 模式，每 {interval_sec} 秒运行一次")

    while True:
        run_once()
        time.sleep(interval_sec)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--interval-sec", type=int, default=600)

    args = parser.parse_args()

    if args.mode == "once":
        run_once()
    else:
        run_loop(args.interval_sec)
```

---

# 十、你现在应该怎么改系统

现在不是继续加分析规则，而是先补这 5 个运行能力。

## 第 1 步：先让它能跑一轮

```bash
python sikk_live_orchestrator.py --mode once
```

必须输出：

```text
live_events.jsonl
live_state.json
live_board.md
tokens/<token>/token_status.json
tokens/<token>/token_status.md
```

---

## 第 2 步：让它能持续跑

```bash
python sikk_live_orchestrator.py --mode loop --interval-sec 600
```

这样每 10 分钟跑一次。

---

## 第 3 步：让它会播报

每个阶段都必须 `emit_event()`：

```text
发现 token
K线信号
钱包结构结果
quote 结果
security 结果
状态变化
paper 入场
paper 退出
失败归因
```

---

## 第 4 步：让你能看某个 token

每个 token 必须生成：

```text
token_status.json
token_status.md
```

你以后就看这个文件：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

---

## 第 5 步：让你看总览

每天主要看：

```text
data/gmgn_candidates_live_run/live_board.md
```

这个就是你的系统看板。

---

# 十一、现在的系统阶段重新定义

你现在不是缺“更复杂的庄家判断”。  
你缺的是：

```text
自动调度
事件播报
状态可视化
单币状态追踪
结果看板
```

所以当前阶段应该从：

```text
钱包结构门禁开发
```

升级为：

```text
SIKK Live Runtime v0.1
```

目标是：

```text
系统可以自己跑
系统可以播报发现了什么 token
系统可以告诉你每个 token 当前状态
系统可以保存每一步判断过程
系统可以让你复盘为什么进 / 不进
```

---

# 十二、最小验收标准

只要实现下面这些，就算运行层 v0.1 成立：

```text
1. python sikk_live_orchestrator.py --mode once 可以跑一轮
2. 发现 token 后写入 TOKEN_DISCOVERED 事件
3. 每个 token 生成 token_status.json
4. 每个 token 生成 token_status.md
5. 总览生成 live_board.md
6. 钱包结构状态写入 token_status
7. 状态机状态写入 token_status
8. paper 状态写入 token_status
9. 出错时写 ERROR 事件
10. loop 模式可以每 10 分钟运行一次
```

---

# 十三、最终结论

你现在的问题判断正确：

> 当前系统只有分析骨架，还没有“自动运行与可观测控制台”。

下一步最优先不是继续细化钱包分类，而是新增：

```text
sikk_live_orchestrator.py
sikk_event_logger.py
sikk_token_status_board.py
sikk_cli.py
live_board.md
token_status.md
live_events.jsonl
```

这样系统才会真正从：

```text
一堆分析脚本
```

变成：

```text
可以自己跑、会播报、能查看状态、能复盘原因的 SIKK Live Runtime
```

---

# 本次认知升级点

核心升级：

> SIKK-SOL 不能只做“分析正确”，还必须做到“运行可见”。

真正可用的交易系统必须同时具备：

```text
分析能力
运行能力
播报能力
状态可视化能力
复盘能力
```

现在缺的是后四个。

---

# 尚未解决问题

下一步需要继续补：

```text
1. sikk_live_orchestrator.py 如何实际接入现有候选发现模块
2. token_status.json 如何合并 K线、钱包、quote、security、paper 数据
3. sikk_cli.py 的完整命令行代码
4. live_board.md 是否需要转成网页 dashboard
5. 是否要增加 Telegram / Discord / 微信机器人播报
```

---

<!-- source_marker=6162 -->

# SIKK-SOL v1.0 钱包结构层：5 个工程接缝补全
```text
1. same_source_group_id 实际生成代码
2. pipeline 如何读取 sikk_gmgn_token_report.py 输出
3. snapshots / delta 文件生成逻辑
4. paper runner 的 FORCE_PAPER_EXIT 策略
5. daily_report 如何统计钱包结构状态下的胜率和收益
# 0. 建议新增文件
```text
sikk/wallet_structure/sikk_same_source_group.py
sikk/wallet_structure/sikk_wallet_snapshot.py
sikk/reporting/sikk_wallet_structure_daily_report.py
```text
  wallet_structure/
    sikk_wallet_structure_gate.py
    sikk_candidate_wallet_structure_pipeline.py
    sikk_wallet_snapshot.py
    sikk_wallet_structure_daily_report.py
# 1. `same_source_group_id` 的实际生成代码
```text
sikk/wallet_structure/sikk_same_source_group.py
## 1.1 功能
```text
输入：wallet_rows
1. 给每个钱包补 same_source_group_id
2. 生成 candidate_groups.csv 需要的 group rows
3. 计算 sync_buy_score
4. 计算 sync_sell_score
## 1.2 代码
def build_similarity_graph(wallet_rows: List[Dict[str, Any]], threshold: float = 70.0) -> Dict[int, List[int]]:
    for i in range(len(wallet_rows)):
        for j in range(i + 1, len(wallet_rows)):
            sim = same_source_similarity(wallet_rows[i], wallet_rows[j])
            wallet_rows[i].setdefault("pair_similarity", {})
            wallet_rows[j].setdefault("pair_similarity", {})
            wallet_rows[i]["pair_similarity"][s(wallet_rows[j].get("wallet_address") or wallet_rows[j].get("address"))] = sim
            wallet_rows[j]["pair_similarity"][s(wallet_rows[i].get("wallet_address") or wallet_rows[i].get("address"))] = sim
    wallet_rows: List[Dict[str, Any]],
    给 wallet_rows 写入 same_source_group_id / sync_buy_score / sync_sell_score。
    - updated wallet_rows
    - candidate_groups rows
    if not wallet_rows:
        return wallet_rows, []
    graph = build_similarity_graph(wallet_rows, threshold=similarity_threshold)
    components = connected_components(graph, len(wallet_rows))
        group_rows = [wallet_rows[i] for i in comp]
        wallets = []
            wallet_address = s(wallet_rows[idx].get("wallet_address") or wallet_rows[idx].get("address"))
            wallets.append(wallet_address)
            wallet_rows[idx]["same_source_group_id"] = group_id
            wallet_rows[idx]["same_source_group_size"] = len(group_rows)
            wallet_rows[idx]["sync_buy_score"] = sync_buy_score
            wallet_rows[idx]["sync_sell_score"] = sync_sell_score
            wallet_rows[idx]["same_source_group_type"] = group_type
            wallet_rows[idx]["source_reliability"] = source_reliability(wallet_rows[idx])
            "wallets": ",".join(wallets),
    return wallet_rows, candidate_groups
# 2. pipeline 如何读取 `sikk_gmgn_token_report.py` 输出
## 2.1 推荐约定
```text
data/gmgn_candidates_live_run/wallet_structure/<token_address>/
```text
early_wallet_raw.csv
wallet_classification.csv    # 可选，pipeline 也能重新 classify
```text
<token>/early_wallet_raw.csv
```text
<token>/wallet_classification.csv
<token>/wallets.csv
## 2.2 修改 `sikk_candidate_wallet_structure_pipeline.py`
在之前的 pipeline 里替换 `fetch_or_load_token_wallet_raw()`。
DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/wallet_structure")
    "address": "wallet_address",
    "wallet": "wallet_address",
    "wallet_address": "wallet_address",
def normalize_wallet_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    normalized.setdefault("wallet_address", normalized.get("address", ""))
def load_wallet_rows_from_existing_report(
        "early_wallet_raw.csv",
        "wallet_classification.csv",
        "wallets.csv",
            return [normalize_wallet_row(r) for r in rows]
def fetch_or_load_token_wallet_raw(
    existing = load_wallet_rows_from_existing_report(token_address, output_dir=output_dir)
        existing = load_wallet_rows_from_existing_report(token_address, output_dir=output_dir)
## 2.3 在 pipeline 中接入同源组
from sikk.wallet_structure.sikk_same_source_group import apply_same_source_groups
# 1. 获取钱包原始数据
wallet_rows = fetch_or_load_token_wallet_raw(
# 2. 生成 same_source_group_id + candidate_groups
wallet_rows, candidate_groups = apply_same_source_groups(
    wallet_rows=wallet_rows,
# 3. 保存 early_wallet_raw.csv
write_csv(token_dir / "early_wallet_raw.csv", wallet_rows)
# 4. classify(w)
classifications = [classify_wallet(w) for w in wallet_rows]
# 5. 保存 wallet_classification.csv
for raw, cls in zip(wallet_rows, classifications):
write_csv(token_dir / "wallet_classification.csv", classification_rows)
# 6. 保存 candidate_groups.csv
## 2.4 聚合 metrics 时使用 candidate_groups
# 3. snapshots / delta 的真实文件生成逻辑
```text
sikk/wallet_structure/sikk_wallet_snapshot.py
## 3.1 功能
```text
```text
## 3.2 代码
        "early_wallet_count": n(metrics.get("early_wallet_count")),
        "early_wallet_remaining_pct": n(metrics.get("early_wallet_remaining_pct")),
        "early_wallet_sold_pct": n(metrics.get("early_wallet_sold_pct")),
        "high_result_wallet_count": n(metrics.get("high_result_wallet_count")),
        "distribution_wallet_count": n(metrics.get("distribution_wallet_count")),
        "wallet_structure_status": decision.wallet_structure_status,
        "wallet_structure_score": decision.wallet_structure_score,
        "wallet_risk_score": decision.wallet_risk_score,
        "early_wallet_remaining_pct_delta": (
            n(current.get("early_wallet_remaining_pct"))
            - n(previous.get("early_wallet_remaining_pct"))
        "early_wallet_sold_pct_delta": (
            n(current.get("early_wallet_sold_pct"))
            - n(previous.get("early_wallet_sold_pct"))
            - n(previous.get("high_result_remaining_pct"))
            - n(previous.get("same_source_group_remaining_pct"))
            - n(previous.get("same_source_group_sold_pct"))
        "distribution_wallet_count_delta": (
            n(current.get("distribution_wallet_count"))
            - n(previous.get("distribution_wallet_count"))
            - n(previous.get("bagholder_whale_count"))
            - n(previous.get("late_buyer_count"))
            - n(previous.get("late_large_buyer_count"))
            - n(previous.get("late_buyer_buy_amount_usd"))
        "wallet_structure_score_delta": (
            n(current.get("wallet_structure_score"))
            - n(previous.get("wallet_structure_score"))
        "wallet_risk_score_delta": (
            n(current.get("wallet_risk_score"))
            - n(previous.get("wallet_risk_score"))
            - n(previous.get("counterparty_pressure_score"))
    early_sold_delta = n(delta.get("early_wallet_sold_pct_delta"))
    risk_delta = n(delta.get("wallet_risk_score_delta"))
## 3.3 在 pipeline 中接入 snapshot/delta
from sikk.wallet_structure.sikk_wallet_snapshot import write_snapshot_and_delta
# 4. paper runner 的 FORCE_PAPER_EXIT：立即退出还是先 EXIT_MONITOR？
## 4.1 v1.0 策略结论
```text
硬性结构恶化 → FORCE_PAPER_EXIT
真实交易阶段 → 不自动卖出，只生成确认票据
| WALLET_BLOCK | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| sync_sell_score >= 70 | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| counterparty_pressure_score >= 70 且 delta >= 25 | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| early_wallet_sold_pct_delta >= 20 但仓位盈利 | EXIT_MONITOR | 提醒人工 |
## 4.2 为什么 paper 可以直接 FORCE_EXIT？
```text
但实盘不能自动退出，因为真实交易存在：
```text
```text
## 4.3 推荐动作等级
```text
FORCE_PAPER_EXIT
## 4.4 paper runner 持仓动作函数
def decide_wallet_position_action(
    - paper: 可以 FORCE_PAPER_EXIT
    - live: 不自动卖，生成 confirmation ticket
    current_status = current_decision.wallet_structure_status
    early_sold_delta = float(latest_delta.get("early_wallet_sold_pct_delta") or 0)
    risk_delta = float(latest_delta.get("wallet_risk_score_delta") or 0)
                "action": "FORCE_PAPER_EXIT",
# 5. daily_report 如何统计不同 wallet_structure_status 的胜率和收益
```text
sikk/reporting/sikk_wallet_structure_daily_report.py
## 5.1 输入
```text
data/gmgn_candidates_live_run/paper_positions.csv
```text
paper_positions.csv
```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
## 5.2 统计指标
按 `wallet_structure_status` 分组：
```text
## 5.3 代码
    return status in {"CLOSED", "PAPER_CLOSED", "EXITED", "FORCE_PAPER_EXIT"}
def group_positions_by_wallet_status(rows: List[Mapping[str, Any]]) -> Dict[str, List[Mapping[str, Any]]]:
        status = r.get("wallet_structure_status") or "UNKNOWN"
def build_wallet_structure_daily_report(
    paper_positions_path: Path,
    report_name: str = "daily_wallet_structure_report",
    rows = read_csv_rows(paper_positions_path)
    groups = group_positions_by_wallet_status(rows)
        "by_wallet_structure_status": status_summary,
        "| wallet_structure_status | total | closed | win_rate | avg_pnl | median_pnl | total_sol | avg_max_profit | avg_drawdown | best | worst |"
    for status, item in report["by_wallet_structure_status"].items():
    for status, item in report["by_wallet_structure_status"].items():
    build_wallet_structure_daily_report(
        paper_positions_path=Path("data/gmgn_candidates_live_run/paper_positions.csv"),
# 6. daily report 的判断标准
## 6.1 如果 WALLET_SUPPORT 表现好
```text
```text
## 6.2 如果 WALLET_SUPPORT 表现差
```text
```text
wallet_structure_score SUPPORT 阈值 65 → 70
early_wallet_remaining_pct 30 → 40
## 6.3 如果 WALLET_BLOCK 后续经常大涨
```text
early_wallet_sold_pct 是否过严
distribution_wallet_count 是否识别过宽
```text
early_wallet_sold_pct 85 → 90
distribution_wallet_count >=3 → >=4
## 6.4 如果 WALLET_PAUSE 太多
### 数据不足导致
```text
### 规则过保守导致
```text
```text
# 7. 最终接入流程
```text
early_wallet_raw.csv
sikk_candidate_wallet_structure_pipeline.py
wallet_classification.csv
decide_wallet_structure()
wallet_structure_decision.json
状态机读取 wallet_structure_decision.json
paper runner 写入 wallet_structure_factor
HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
daily_wallet_structure_report.md
# 8. 当前最优开发顺序
```text
1. 加 sikk_same_source_group.py
2. 修改 pipeline，读取 sikk_gmgn_token_report.py 输出
3. pipeline 中接入 apply_same_source_groups()
4. 生成 candidate_groups.csv
5. 生成 wallet_structure_decision.json
6. 加 sikk_wallet_snapshot.py
8. paper runner 读取 wallet_structure_decision.json + latest_delta.json
9. paper runner 支持 EXIT_MONITOR / FORCE_PAPER_EXIT
10. daily_report 按 wallet_structure_status 统计收益
```text
# 本次认知升级点
```text
→ 日报统计
> 钱包结构不再只是“入场前判断”，而是贯穿持仓全过程：入场门禁、持仓监控、失败归因、阈值校准。
# 尚未解决问题
```text
1. sikk_gmgn_token_report.py 的真实输出字段与 COLUMN_MAP 对齐
2. same_source_group 的 CEX / 路由器过滤名单扩展
3. latest_delta.json 如何进入 paper runner 的现有更新循环
4. EXIT_MONITOR 后是否触发减仓、移动止损或缩短时间止损
5. daily_report 增加“钱包结构状态 × SIKK信号等级”的交叉统计

---

<!-- source_marker=6367 -->

定位是：**能接入状态机、能跑测试、能被 paper runner 使用**。真实 GMGN 抓取部分先做 adapter 占位，后面再替换成你的接口。
# 0. 建议目录结构
```text
  wallet_structure/
    sikk_wallet_structure_gate.py
    sikk_candidate_wallet_structure_pipeline.py
  test_sikk_wallet_structure_gate.py
# 1. `sikk_wallet_structure_gate.py` 完整代码骨架
```text
sikk/wallet_structure/sikk_wallet_structure_gate.py
# =========================
# 1. 枚举定义
# =========================
# =========================
# 2. 数据结构
# =========================
    wallet_address: str
    wallet_role: str
    wallet_structure_score: Dict[str, float] = field(default_factory=dict)
    wallet_risk_score: Dict[str, float] = field(default_factory=dict)
    wallet_structure_status: str
    wallet_structure_score: float
    wallet_risk_score: float
    wallet_structure_factor: float
    wallet_evidence_level: str
# =========================
# 3. 工具函数
# =========================
    """安全转数字。"""
# =========================
# 4. 钱包角色分类 classify(w)
# =========================
def classify_wallet(w: Mapping[str, Any]) -> WalletClassification:
    wallet_address = s(w.get("wallet_address") or w.get("address"))
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
            wallet_address=wallet_address,
            wallet_role=role,
        wallet_address=wallet_address,
        wallet_role=role,
# =========================
# 5. 分数计算
# =========================
def compute_wallet_structure_score(metrics: Mapping[str, Any]) -> Tuple[float, Dict[str, float]]:
    early_wallet_remaining_pct = n(metrics.get("early_wallet_remaining_pct"))
    high_result_wallet_count = n(metrics.get("high_result_wallet_count"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    wallet_behavior_matches_price_action = s(metrics.get("wallet_behavior_matches_price_action"), "UNCLEAR").upper()
    if early_wallet_remaining_pct >= 50:
    elif early_wallet_remaining_pct >= 30:
    elif early_wallet_remaining_pct >= 15:
    if high_result_wallet_count >= 2 and high_result_remaining_pct >= 40:
    elif high_result_wallet_count >= 1 and high_result_remaining_pct >= 25:
    elif high_result_wallet_count >= 1 and high_result_remaining_pct >= 10:
    if distribution_wallet_count == 0:
    elif distribution_wallet_count == 1:
    elif distribution_wallet_count == 2:
    if wallet_behavior_matches_price_action in {"TRUE", "MATCH", "YES"}:
    elif wallet_behavior_matches_price_action in {"UNCLEAR", "UNKNOWN"}:
def compute_wallet_risk_score(
    early_wallet_sold_pct = n(metrics.get("early_wallet_sold_pct"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    high_result_wallet_count = n(metrics.get("high_result_wallet_count"))
    if early_wallet_sold_pct >= 85:
    elif early_wallet_sold_pct >= 70:
    elif early_wallet_sold_pct >= 50:
    if distribution_wallet_count >= 5:
    elif distribution_wallet_count >= 3:
    elif distribution_wallet_count >= 1:
    if high_result_wallet_count >= 2 and high_result_remaining_pct <= 10:
    elif high_result_wallet_count >= 1 and high_result_remaining_pct <= 20:
    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    if early_wallet_sold_pct_delta >= 20 and late_buyer_buy_amount_usd_delta > 0:
    elif early_wallet_sold_pct_delta >= 10 and late_buyer_buy_amount_usd_delta > 0:
    elif early_wallet_sold_pct_delta >= 5 and late_buyer_buy_amount_usd_delta > 0:
    if price_change_pct > 20 and early_wallet_sold_pct_delta >= 15:
    early_wallet_count = n(metrics.get("early_wallet_count"))
    # A. early_wallet_data_score，0-25
    if early_wallet_count >= 50:
        early_wallet_data_score = 25
    elif early_wallet_count >= 30:
        early_wallet_data_score = 18
    elif early_wallet_count >= 10:
        early_wallet_data_score = 10
        early_wallet_data_score = 3
        "early_wallet_data_score": early_wallet_data_score,
# =========================
# 6. 状态推断
# =========================
    early_wallet_remaining_pct_delta = n(metrics.get("early_wallet_remaining_pct_delta"))
    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    distribution_wallet_count_delta = n(metrics.get("distribution_wallet_count_delta"))
        distribution_wallet_count_delta >= 2
        (late_large_buyer_count_delta >= 2 and early_wallet_sold_pct_delta >= 10)
        early_wallet_remaining_pct_delta <= -10
        early_wallet_remaining_pct_delta >= 0
        early_wallet_remaining_pct_delta > -10
    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    distribution_wallet_count_delta = n(metrics.get("distribution_wallet_count_delta"))
    if early_wallet_sold_pct_delta >= 10 and late_large_buyer_count_delta >= 1:
    if distribution_wallet_count_delta >= 2 and late_large_buyer_count_delta >= 1:
    early_wallet_count = n(metrics.get("early_wallet_count"))
    if data_quality_score >= 80 and early_wallet_count >= 30 and same_source_group_count >= 1:
    if data_quality_score >= 60 and early_wallet_count >= 10:
def wallet_structure_factor(status: str) -> float:
        "structure_side_wallet_count": 0,
        "execution_side_wallet_count": 0,
        "distribution_side_wallet_count": 0,
        "counterparty_side_wallet_count": 0,
        "noise_side_wallet_count": 0,
        "unknown_side_wallet_count": 0,
            summary["structure_side_wallet_count"] += 1
            summary["execution_side_wallet_count"] += 1
            summary["distribution_side_wallet_count"] += 1
            summary["counterparty_side_wallet_count"] += 1
            summary["noise_side_wallet_count"] += 1
            summary["unknown_side_wallet_count"] += 1
# =========================
# 7. 最终门禁决策
# =========================
def decide_wallet_structure(
    wallet_structure_score, ws_breakdown = compute_wallet_structure_score(metrics)
    wallet_risk_score, wr_breakdown = compute_wallet_risk_score(metrics, data_quality_score)
    early_wallet_sold_pct = n(metrics.get("early_wallet_sold_pct"))
    early_wallet_remaining_pct = n(metrics.get("early_wallet_remaining_pct"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    if early_wallet_remaining_pct >= 30:
    if distribution_wallet_count <= 1:
    if early_wallet_sold_pct >= 70:
    if wallet_risk_score >= 75:
    elif counterparty_pressure_score >= 70 and wallet_risk_score >= 50:
    elif early_wallet_sold_pct >= 85 and high_result_remaining_pct <= 10:
    elif distribution_wallet_count >= 3 and early_wallet_remaining_pct <= 20:
    elif wallet_risk_score >= 50:
        wallet_structure_score >= 65
        and wallet_risk_score <= 40
        and early_wallet_remaining_pct >= 30
        and distribution_wallet_count <= 1
        wallet_structure_score=ws_breakdown,
        wallet_risk_score=wr_breakdown,
        wallet_structure_status=status,
        wallet_structure_score=wallet_structure_score,
        wallet_risk_score=wallet_risk_score,
        wallet_structure_factor=wallet_structure_factor(status),
        wallet_evidence_level=evidence_level,
# 2. `tests/test_sikk_wallet_structure_gate.py` 测试样例
```text
tests/test_sikk_wallet_structure_gate.py
from sikk.wallet_structure.sikk_wallet_structure_gate import (
    classify_wallet,
    decide_wallet_structure,
        "early_wallet_count": 50,
        "early_wallet_remaining_pct": 40,
        "early_wallet_sold_pct": 60,
        "high_result_wallet_count": 2,
        "distribution_wallet_count": 0,
        "wallet_behavior_matches_price_action": "MATCH",
        "early_wallet_sold_pct_delta": 0,
# =========================
# classify_wallet 测试
# =========================
        "wallet_address": "W1",
    result = classify_wallet(w)
    assert result.wallet_role == WalletRole.DISTRIBUTION_SELLER.value
        "wallet_address": "W2",
    result = classify_wallet(w)
    assert result.wallet_role == WalletRole.EARLY_EXIT.value
        "wallet_address": "W3",
    result = classify_wallet(w)
    assert result.wallet_role == WalletRole.SAME_SOURCE_GROUP.value
def test_classify_high_result_wallet():
        "wallet_address": "W4",
    result = classify_wallet(w)
    assert result.wallet_role == WalletRole.HIGH_RESULT_WALLET.value
        "wallet_address": "W5",
    result = classify_wallet(w)
    assert result.wallet_role == WalletRole.BAGHOLDER_WHALE.value
# =========================
# decide_wallet_structure 测试
# =========================
def test_wallet_support_case():
    decision = decide_wallet_structure(
    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_SUPPORT.value
    assert decision.wallet_structure_factor == 1.15
def test_wallet_block_when_same_source_sync_sell_high():
    decision = decide_wallet_structure(
            early_wallet_remaining_pct=35,
            early_wallet_sold_pct=65,
    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_BLOCK.value
    assert decision.wallet_structure_factor == 0.0
def test_wallet_block_when_early_exit_and_high_result_exit():
    decision = decide_wallet_structure(
            early_wallet_sold_pct=90,
            early_wallet_remaining_pct=10,
    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_BLOCK.value
def test_wallet_pause_when_data_quality_low():
    decision = decide_wallet_structure(
            early_wallet_count=5,
    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_PAUSE.value
def test_wallet_pause_when_counterparty_pressure_high():
    decision = decide_wallet_structure(
            early_wallet_sold_pct_delta=20,
    assert decision.wallet_structure_status in {
def test_wallet_neutral_case():
    decision = decide_wallet_structure(
            early_wallet_remaining_pct=22,
            early_wallet_sold_pct=55,
            high_result_wallet_count=0,
            distribution_wallet_count=1,
    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_NEUTRAL.value
```bash
pytest tests/test_sikk_wallet_structure_gate.py -q
# 3. `sikk_candidate_wallet_structure_pipeline.py` 输入输出流程
```text
sikk/wallet_structure/sikk_candidate_wallet_structure_pipeline.py
```text
→ 调用 decide_wallet_structure()
→ 输出 wallet_structure_decision.json
→ 汇总 candidate_wallet_structure_summary.csv/json/md
from sikk.wallet_structure.sikk_wallet_structure_gate import (
    classify_wallet,
    decide_wallet_structure,
DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/wallet_structure")
# =========================
# 1. 基础 IO
# =========================
            f"| {r.get('token_symbol')} | {r.get('wallet_structure_status')} "
            f"| {r.get('wallet_structure_score')} "
            f"| {r.get('wallet_risk_score')} "
# =========================
# 2. 输入候选
# =========================
# =========================
# 3. GMGN 数据 adapter 占位
# =========================
def fetch_or_load_token_wallet_raw(token: Mapping[str, Any]) -> List[Dict[str, Any]]:
    - GMGN holder 接口
    - early buyer 数据
    - top trader 数据
    - sikk_gmgn_token_report.py 的输出读取
    如果存在 data/gmgn_candidates_live_run/wallet_structure/<token>/early_wallet_raw.csv，
    则可以在这里读取 CSV。
    当前骨架返回空列表，真实项目里必须替换。
# =========================
# 4. 字段完整率
# =========================
# =========================
# 5. 聚合 token 级 metrics
# =========================
def aggregate_wallet_metrics(
    wallet_rows: List[Mapping[str, Any]],
    - early_wallet metrics
    - same_source_group metrics
    - top_holder metrics
    - delta metrics
    early_wallets = [
        w for w in wallet_rows
    high_result_wallets = [
        w for w in wallet_rows
    distribution_wallets = [
        if c.wallet_role == "DISTRIBUTION_SELLER"
    bagholder_wallets = [
        if c.wallet_role == "BAGHOLDER_WHALE"
        float(w.get("remaining_pct") or 0) for w in early_wallets
        float(w.get("sold_pct") or 0) for w in early_wallets
        float(w.get("remaining_pct") or 0) for w in high_result_wallets
    # 这几个字段后续应由 same_source_group 模块真实生成
        "early_wallet_count": len(early_wallets),
        "early_wallet_remaining_pct": early_remaining,
        "early_wallet_sold_pct": early_sold,
        "high_result_wallet_count": len(high_result_wallets),
        "distribution_wallet_count": len(distribution_wallets),
        "bagholder_whale_count": len(bagholder_wallets),
        "wallet_behavior_matches_price_action": token.get("wallet_behavior_matches_price_action", "UNCLEAR"),
            wallet_rows,
            wallet_rows,
            wallet_rows,
            wallet_rows,
            wallet_rows,
        "early_wallet_sold_pct_delta": 0,
        "early_wallet_remaining_pct_delta": 0,
        metrics["early_wallet_sold_pct_delta"] = (
            metrics["early_wallet_sold_pct"] - float(previous_snapshot.get("early_wallet_sold_pct") or 0)
        metrics["early_wallet_remaining_pct_delta"] = (
            metrics["early_wallet_remaining_pct"] - float(previous_snapshot.get("early_wallet_remaining_pct") or 0)
# =========================
# 6. 单 token 处理
# =========================
    wallet_rows = fetch_or_load_token_wallet_raw(token)
    # 2. 保存 early_wallet_raw.csv
    write_csv(token_dir / "early_wallet_raw.csv", wallet_rows)
    classifications = [classify_wallet(w) for w in wallet_rows]
    for raw, cls in zip(wallet_rows, classifications):
    write_csv(token_dir / "wallet_classification.csv", classification_rows)
    metrics = aggregate_wallet_metrics(token, wallet_rows, classifications)
    decision = decide_wallet_structure(
    # 8. 保存 wallet_structure_decision.json
    save_decision(decision, token_dir / "wallet_structure_decision.json")
        "wallet_structure_status": decision.wallet_structure_status,
        "wallet_structure_score": decision.wallet_structure_score,
        "wallet_risk_score": decision.wallet_risk_score,
        "wallet_structure_factor": decision.wallet_structure_factor,
        wallet_address = r.get("wallet_address") or r.get("address")
        role = r.get("wallet_role")
            "wallet_address": wallet_address,
            "gmgn_name": f"[{role}] {str(wallet_address)[:6]}...{str(wallet_address)[-4:]}",
            "wallet_role": role,
# =========================
# 7. 批量入口
# =========================
def run_candidate_wallet_structure_pipeline(
                "wallet_structure_status": "DATA_SOURCE_MISSING",
    write_json(output_dir / "candidate_wallet_structure_summary.json", summary_rows)
    write_csv(output_dir / "candidate_wallet_structure_summary.csv", summary_rows)
    write_md_summary(output_dir / "candidate_wallet_structure_summary.md", summary_rows)
    run_candidate_wallet_structure_pipeline()
# 4. `wallet_structure_decision.json` 与状态机的实际接入点
```text
```text
wallet_structure_gate
- 钱包结构如果已经 `WALLET_BLOCK`，没必要继续 quote。
- 钱包结构 `WALLET_PAUSE`，也不应直接进入 `PAPER_READY`。
- `WALLET_SUPPORT` 只是允许继续过 quote/security，不是直接开仓。
## 状态机接入函数骨架
from sikk.wallet_structure.sikk_wallet_structure_gate import load_decision
def apply_wallet_structure_gate_to_state(
    base_dir: str = "data/gmgn_candidates_live_run/wallet_structure",
    decision_path = Path(base_dir) / token_address / "wallet_structure_decision.json"
            "wallet_gate_status": "MISSING_DECISION",
            "reason": "缺少 wallet_structure_decision.json，不能进入 PAPER_READY",
    status = decision.wallet_structure_status
            "wallet_gate_status": status,
            "wallet_decision": decision,
            "wallet_gate_status": status,
            "wallet_decision": decision,
                "wallet_gate_status": status,
                "wallet_decision": decision,
            "wallet_gate_status": status,
            "wallet_decision": decision,
            "wallet_gate_status": status,
            "wallet_decision": decision,
        "wallet_gate_status": status,
        "wallet_decision": decision,
## 状态机动作表
| wallet 状态 | 状态机动作 |
```text
# 5. paper runner 如何根据钱包结构变化触发持仓管理或提前退出
```text
## 5.1 入场前：写入 wallet_structure_factor
```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
wallet_structure_factor
wallet_structure_reason
def enrich_paper_position_with_wallet_structure(position: dict, wallet_decision) -> dict:
    position["wallet_structure_status"] = wallet_decision.wallet_structure_status
    position["wallet_structure_score"] = wallet_decision.wallet_structure_score
    position["wallet_risk_score"] = wallet_decision.wallet_risk_score
    position["counterparty_pressure_score"] = wallet_decision.counterparty_pressure_score
    position["data_quality_score"] = wallet_decision.data_quality_score
    position["wallet_structure_factor"] = wallet_decision.wallet_structure_factor
    position["wallet_structure_reason"] = wallet_decision.reason
    position["dominant_side_status"] = wallet_decision.dominant_side_status
    position["chip_transfer_status"] = wallet_decision.chip_transfer_status
## 5.2 持仓中：钱包结构恶化监控
```text
wallet_structure_decision.json
```text
entry_wallet_structure_score
current_wallet_structure_score
entry_wallet_risk_score
current_wallet_risk_score
## 5.3 持仓中动作等级
| FORCE_PAPER_EXIT | 纸面强制退出 |
## 5.4 持仓管理规则
### A. 直接纸面退出
```text
→ FORCE_PAPER_EXIT
```text
### B. 对手盘压力快速上升
```text
→ FORCE_PAPER_EXIT
```text
### C. 同源组同步卖出
```text
→ FORCE_PAPER_EXIT
```text
### D. 早期钱包快速退出
```text
early_wallet_sold_pct_delta >= 20
```text
```text
FORCE_PAPER_EXIT
```text
### E. 高结果钱包退出
```text
```text
wallet_risk_score_delta >= 20
```text
FORCE_PAPER_EXIT
```text
### F. 数据质量恶化
```text
```text
```text
## 5.5 paper runner 持仓更新伪代码
from sikk.wallet_structure.sikk_wallet_structure_gate import load_decision
def evaluate_wallet_structure_for_open_position(
    wallet_structure_dir: str = "data/gmgn_candidates_live_run/wallet_structure",
    decision_path = Path(wallet_structure_dir) / token_address / "wallet_structure_decision.json"
    entry_structure_score = float(position.get("wallet_structure_score") or 0)
    entry_risk_score = float(position.get("wallet_risk_score") or 0)
    current_structure_score = current.wallet_structure_score
    current_risk_score = current.wallet_risk_score
    wallet_structure_score_delta = current_structure_score - entry_structure_score
    wallet_risk_score_delta = current_risk_score - entry_risk_score
    early_wallet_sold_pct_delta = float(metrics.get("early_wallet_sold_pct_delta") or 0)
    if current.wallet_structure_status == "WALLET_BLOCK":
            "action": "FORCE_PAPER_EXIT",
            "current_wallet_decision": current,
            "action": "FORCE_PAPER_EXIT",
            "current_wallet_decision": current,
            "action": "FORCE_PAPER_EXIT",
            "current_wallet_decision": current,
    if early_wallet_sold_pct_delta >= 20 and position_pnl_pct <= 0:
            "action": "FORCE_PAPER_EXIT",
            "current_wallet_decision": current,
    if early_wallet_sold_pct_delta >= 20:
            "current_wallet_decision": current,
    if high_result_remaining_pct_delta <= -20 and wallet_risk_score_delta >= 20:
            "action": "FORCE_PAPER_EXIT",
            "current_wallet_decision": current,
            "current_wallet_decision": current,
            "current_wallet_decision": current,
        "current_wallet_decision": current,
# 6. failure_attribution 接入 paper runner
当 paper runner 触发 `FORCE_PAPER_EXIT` 时，写入：
```text
```text
wallet_structure_status_at_entry
wallet_structure_score_at_entry
wallet_risk_score_at_entry
wallet_structure_status_before_exit
wallet_structure_score_before_exit
wallet_risk_score_before_exit
wallet_structure_score_delta
wallet_risk_score_delta
def build_wallet_failure_attribution(
    current = evaluation.get("current_wallet_decision")
        "wallet_structure_status_at_entry": position.get("wallet_structure_status"),
        "wallet_structure_score_at_entry": position.get("wallet_structure_score"),
        "wallet_risk_score_at_entry": position.get("wallet_risk_score"),
        "wallet_structure_status_before_exit": getattr(current, "wallet_structure_status", None),
        "wallet_structure_score_before_exit": getattr(current, "wallet_structure_score", None),
        "wallet_risk_score_before_exit": getattr(current, "wallet_risk_score", None),
        "wallet_structure_score_delta": (
            getattr(current, "wallet_structure_score", 0)
            - float(position.get("wallet_structure_score") or 0)
        "wallet_risk_score_delta": (
            getattr(current, "wallet_risk_score", 0)
            - float(position.get("wallet_risk_score") or 0)
            - float(position.get("counterparty_pressure_score") or 0)
        "suggested_rule_adjustment": suggest_wallet_rule_adjustment(failure_type),
def suggest_wallet_rule_adjustment(failure_type: str) -> str:
        return "检查 early_wallet_sold_pct_delta 是否应加入持仓中退出规则"
# 7. 最小开发顺序
```text
1. 先实现 sikk_wallet_structure_gate.py
2. 先跑 tests/test_sikk_wallet_structure_gate.py
3. 再接 sikk_candidate_wallet_structure_pipeline.py
4. 再生成 wallet_structure_decision.json
5. 再让状态机读取 wallet_structure_decision.json
6. 再让 paper runner 写入 wallet_structure_factor
```text
paper runner 能因钱包结构恶化触发 FORCE_PAPER_EXIT
# 本次认知升级点
```text
```text
# 尚未解决问题
```text
1. same_source_group_id 的实际生成代码
2. sikk_candidate_wallet_structure_pipeline.py 如何读取你现有 sikk_gmgn_token_report.py 输出
3. snapshots/delta 的真实文件生成逻辑
4. paper runner 的 FORCE_PAPER_EXIT 是否立即退出，还是先触发 EXIT_MONITOR
5. daily_report 如何统计不同 wallet_structure_status 的胜率和收益

---

<!-- source_marker=6820 -->

# SIKK-SOL v1.0：5 个工程问题定稿
```text
```text
# 1. same_source_group_id 如何生成
## 1.1 定义
```text
```text
```text
## 1.2 v1.0 使用三类证据生成同源组
### A. 强证据：资金来源相同
```text
```text
### B. 中证据：资金来源相似 + 入场接近
```text
```text
### C. 弱证据：行为高度同步
```text
```text
```text
## 1.3 不要把这些地址直接当同源
```text
```text
```text
```text
## 1.4 same_source_group_id 生成流程
### 第一步：生成钱包指纹
### 第二步：计算两两相似度
```text
### 第三步：建立边
```text
### 第四步：形成连通分组
```text
### 第五步：生成 group_id
```text
```text
```text
## 1.5 same_source_group_id 输出字段
```text
wallets
## 1.6 group_type 枚举
```text
# 2. sync_buy_score / sync_sell_score 如何计算
```text
```text
# 2.1 sync_buy_score 计算公式
## 公式
```text
## A. buy_time_cohesion_score：买入时间集中度，0-30
```text
```text
> 10 分钟    → 0
## B. entry_rank_cohesion_score：入场排名集中度，0-20
```text
```text
> 50    → 0
## C. buy_amount_similarity_score：买入金额相似度，0-15
```text
```text
## D. buy_participation_score：参与比例，0-20
```text
```text
>= 90% → 20
>= 70% → 14
>= 50% → 8
## E. funding_support_score：资金来源支持，0-15
```text
## sync_buy_score 解释
# 2.2 sync_sell_score 计算公式
## 公式
```text
## A. sell_time_cohesion_score：卖出时间集中度，0-30
```text
```text
```text
> 30 分钟    → 0
## B. sell_participation_score：卖出参与比例，0-25
```text
```text
>= 90% → 25
>= 70% → 18
>= 50% → 10
## C. sold_pct_similarity_score：卖出比例相似度，0-15
```text
```text
## D. group_exit_pressure_score：组内整体退出压力，0-20
```text
```text
>= 60 → 15
>= 40 → 8
## E. top_holder_exit_bonus：Top Holder 出货加权，0-10
```text
## sync_sell_score 解释
# 2.3 关键应用逻辑
```text
```text
    增加 wallet_structure_score
    增加 wallet_risk_score
# 3. counterparty_pressure_score 的精确字段来源
## 3.1 定义
```text
```text
## 3.2 所需字段来源
### A. 早期钱包卖出字段
```text
early_wallet_raw.csv
wallet_classification.csv
```text
early_wallet_sold_pct
early_wallet_remaining_pct
early_wallet_sold_pct_delta
early_exit_wallet_count
```text
### B. 晚期买盘字段
```text
```text
```text
```text
### C. 套牢鲸鱼字段
```text
wallet_classification.csv
```text
```text
### D. 价格上涨但结构钱包卖出
```text
wallet snapshot delta
```text
early_wallet_sold_pct_delta
```text
且 early_wallet_sold_pct_delta > 0
```text
### E. 持有人数增加但 Top Holder 下降
```text
```text
```text
```text
### F. 高结果钱包退出
```text
wallet_classification.csv
```text
high_result_wallet_count
## 3.3 counterparty_pressure_score 公式
```text
## A. early_to_late_transfer_score，0-25
```text
early_wallet_sold_pct_delta >= 20 且 late_buyer_buy_amount_delta > 0 → 25
early_wallet_sold_pct_delta >= 10 且 late_buyer_buy_amount_delta > 0 → 18
early_wallet_sold_pct_delta >= 5  且 late_buyer_buy_amount_delta > 0 → 10
```text
early_wallet_sold_pct >= 70 且 late_buyer_ratio >= 40 → 18
early_wallet_sold_pct >= 50 且 late_buyer_ratio >= 30 → 10
## B. late_large_buyer_score，0-20
```text
```text
## C. bagholder_pressure_score，0-15
```text
## D. price_up_structure_sell_score，0-20
```text
且 early_wallet_sold_pct_delta >= 15
```text
```text
```text
## E. holder_growth_top_exit_score，0-10
```text
```text
```text
## F. high_result_exit_score，0-10
```text
```text
high_result_wallet_count >= 2 且 high_result_remaining_pct <= 10 → 10
high_result_wallet_count >= 1 且 high_result_remaining_pct <= 20 → 6
## 3.4 counterparty_pressure_score 动作
```text
且 wallet_risk_score >= 50
```text
# 4. 多轮快照 delta 如何设计
## 4.1 为什么必须做 delta
```text
```text
```text
## 4.2 快照频率建议
## 4.3 snapshot 文件结构
```text
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/
```text
```text
## 4.4 单次 snapshot 标准
```json
  "early_wallet_count": 50,
  "early_wallet_remaining_pct": 42.5,
  "early_wallet_sold_pct": 57.5,
  "high_result_wallet_count": 3,
  "distribution_wallet_count": 1,
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
## 4.5 delta 标准字段
```json
  "early_wallet_remaining_pct_delta": -8.5,
  "early_wallet_sold_pct_delta": 8.5,
  "distribution_wallet_count_delta": 2,
  "wallet_structure_score_delta": -14,
  "wallet_risk_score_delta": 18,
## 4.6 chip_transfer_status 枚举
```text
## 4.7 dominant_side_status 迁移规则
### STRUCTURE_STRENGTHENING
```text
early_wallet_remaining_pct_delta >= 0
```text
### STRUCTURE_HOLDING
```text
early_wallet_remaining_pct_delta > -10
wallet_risk_score_delta < 10
```text
### STRUCTURE_WEAKENING
```text
early_wallet_remaining_pct_delta <= -10
```text
### DISTRIBUTION_ACTIVE
```text
distribution_wallet_count_delta >= 2
```text
### COUNTERPARTY_ABSORBING
```text
且 early_wallet_sold_pct_delta >= 10
```text
```text
# 5. 钱包结构失败如何进入 failure_attribution
## 5.1 原则
```text
```text
```text
```text
## 5.2 新增失败类型
```text
## 5.3 failure_attribution 字段
```text
wallet_structure_status_at_entry
wallet_structure_score_at_entry
wallet_risk_score_at_entry
wallet_structure_status_before_exit
wallet_structure_score_delta
wallet_risk_score_delta
early_wallet_sold_pct_delta
distribution_wallet_count_delta
## 5.4 归因规则
### A. WALLET_EXIT
```text
early_wallet_sold_pct_delta >= 20
```text
early_wallet_remaining_pct 在持仓期间下降超过 20%
```text
### B. SAME_SOURCE_EXIT
```text
```text
```text
### C. DISTRIBUTION_ACTIVE
```text
distribution_wallet_count_delta >= 2
```text
```text
### D. COUNTERPARTY_ABSORBING
```text
```text
### E. STRUCTURE_WEAKENING
```text
wallet_structure_score_delta <= -20
或 wallet_risk_score_delta >= 20
```text
### F. HIGH_RESULT_EXIT
```text
```text
### G. BAGHOLDER_PRESSURE
```text
```text
### H. DATA_QUALITY_FAIL
```text
```text
### I. WALLET_FALSE_SUPPORT
```text
wallet_structure_status_at_entry == WALLET_SUPPORT
且 wallet_risk_score_delta >= 20
```text
### J. WALLET_GATE_MISSED
```text
wallet_risk_score >= 50
```text
## 5.5 failure_attribution 示例
```json
  "wallet_structure_status_at_entry": "WALLET_SUPPORT",
  "wallet_structure_score_at_entry": 68,
  "wallet_risk_score_at_entry": 34,
  "wallet_structure_status_before_exit": "WALLET_PAUSE",
  "wallet_structure_score_delta": -22,
  "wallet_risk_score_delta": 26,
  "early_wallet_sold_pct_delta": 18.5,
  "suggested_rule_adjustment": "当 counterparty_pressure_score_delta >= 25 且 early_wallet_sold_pct_delta >= 10 时，强制从 PAPER_OPEN 降级为 EXIT_MONITOR 或触发风控退出"
# 6. v1.0 直接落地的数据流
```text
GMGN wallet raw data
wallet_classification.csv
wallet_structure_score
wallet_risk_score
wallet_structure_decision.json
# 7. 直接给 AI / Codex 的开发指令
```text
- wallet_address
- funding_source_address
- funding_source_label
- first_funding_time
- first_funding_amount_sol
- entry_time
- entry_rank
- buy_amount_usd
- sell_amount_usd
- sold_pct
- remaining_pct
- trade_count
- buy_count
- sell_count
1. 对每个钱包生成 funding_signature、entry_signature、behavior_signature。
2. 计算钱包两两 similarity_score，满分 100。
3. 权重：
   - funding_source_address 相同：40
   - funding_time 接近：15
   - funding_amount 相近：10
   - entry_time 接近：15
   - buy_amount 相近：10
   - sell/hold 行为相似：10
4. similarity_score >= 70 建立强边。
5. group_size >= 3 生成 same_source_group_id。
- token_address
- group_id
- group_type
- group_size
- wallets
- primary_evidence
- source_reliability
- avg_entry_rank
- entry_time_span_sec
- avg_buy_amount_usd
- buy_amount_cv
- sync_buy_score
- sync_sell_score
- group_remaining_pct
- group_sold_pct
- group_risk_level
- group_evidence_level
- reason
- buy_time_cohesion_score：0-30
- entry_rank_cohesion_score：0-20
- buy_amount_similarity_score：0-15
- buy_participation_score：0-20
- funding_support_score：0-15
- entry_time_span <=30秒 → 30；<=2分钟 →24；<=5分钟 →16；<=10分钟 →8；否则0
- entry_rank_span <=10 →20；<=25 →15；<=50 →8；否则0
- buy_amount_cv <=0.25 →15；<=0.50 →10；<=1.00 →5；否则0
- buy_participation_ratio >=90% →20；>=70% →14；>=50% →8；否则0
- FUNDING_STRONG_GROUP →15；FUNDING_WEAK_GROUP →8；BEHAVIOR_SYNC_GROUP →3；其他0
- sell_time_cohesion_score：0-30
- sell_participation_score：0-25
- sold_pct_similarity_score：0-15
- group_exit_pressure_score：0-20
- top_holder_exit_bonus：0-10
- sell_time_span <=1分钟 →30；<=5分钟 →22；<=15分钟 →12；<=30分钟 →6；否则0
- sell_participation_ratio >=90% →25；>=70% →18；>=50% →10；否则0
- sold_pct_cv <=0.25 →15；<=0.50 →10；<=1.00 →5；否则0
- group_sold_pct >=80 →20；>=60 →15；>=40 →8；否则0
- 组内存在 Top Holder 且 sold_pct >=60 →10；>=30 →5；否则0
- sync_sell_score >=70 → WALLET_BLOCK
- sync_sell_score >=60 → WALLET_PAUSE
- sync_buy_score >=70 且 sync_sell_score <40 → 增加 wallet_structure_score
- sync_buy_score >=70 且 sync_sell_score >=50 → 增加 wallet_risk_score
- early_to_late_transfer_score：0-25
- late_large_buyer_score：0-20
- bagholder_pressure_score：0-15
- price_up_structure_sell_score：0-20
- holder_growth_top_exit_score：0-10
- high_result_exit_score：0-10
- early_wallet_sold_pct_delta
- early_wallet_remaining_pct_delta
- late_buyer_count_delta
- late_large_buyer_count_delta
- late_buyer_buy_amount_usd_delta
- bagholder_whale_count_delta
- price_change_pct
- holder_count_delta_pct
- top10_holder_pct_delta
- high_result_remaining_pct_delta
- early_wallet_sold_pct_delta >=20 且 late_buyer_buy_amount_delta >0 →25
- >=10 且 late_buyer_buy_amount_delta >0 →18
- >=5 且 late_buyer_buy_amount_delta >0 →10
- late_large_buyer_count >=5 →20；>=3 →14；>=1 →6
- bagholder_whale_count >=5 →15；>=3 →10；>=1 →5
- price_change_pct >20 且 early_wallet_sold_pct_delta >=15 →20
- price_change_pct >10 且 same_source_group_sold_pct_delta >=10 →16
- price_change_pct >0 且 high_result_remaining_pct_delta <=-10 →10
- holder_count_delta_pct >10 且 top10_holder_pct_delta <=-5 →10
- holder_count_delta_pct >5 且 top10_holder_pct_delta <=-3 →6
- high_result_remaining_pct_delta <=-30 →10；<=-15 →6；<=-5 →3
- counterparty_pressure_score >=70 且 wallet_risk_score >=50 → WALLET_BLOCK
- counterparty_pressure_score >=50 → WALLET_PAUSE
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/snapshot_<timestamp>.json
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/delta_<from>__<to>.json
- token_address
- snapshot_time
- price
- market_cap
- liquidity
- holder_count
- top10_holder_pct
- top20_holder_pct
- early_wallet_count
- early_wallet_remaining_pct
- early_wallet_sold_pct
- high_result_wallet_count
- high_result_remaining_pct
- same_source_group_count
- same_source_group_remaining_pct
- same_source_group_sold_pct
- distribution_wallet_count
- bagholder_whale_count
- late_buyer_count
- late_large_buyer_count
- late_buyer_buy_amount_usd
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- dominant_side_status
- chip_transfer_status
- price_change_pct
- holder_count_delta_pct
- top10_holder_pct_delta
- early_wallet_remaining_pct_delta
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- same_source_group_remaining_pct_delta
- same_source_group_sold_pct_delta
- distribution_wallet_count_delta
- bagholder_whale_count_delta
- late_buyer_count_delta
- late_large_buyer_count_delta
- late_buyer_buy_amount_usd_delta
- wallet_structure_score_delta
- wallet_risk_score_delta
- counterparty_pressure_score_delta
- dominant_side_status_from
- dominant_side_status_to
- chip_transfer_status
- delta_interpretation
- NO_MAJOR_TRANSFER
- STRUCTURE_ACCUMULATION
- STRUCTURE_HOLDING
- EARLY_TO_LATE_TRANSFER
- GROUP_TO_RETAIL_TRANSFER
- PROFIT_WALLET_EXIT
- DISTRIBUTION_TO_COUNTERPARTY
- COUNTERPARTY_TRAPPED
- UNKNOWN
- WALLET_EXIT
- SAME_SOURCE_EXIT
- DISTRIBUTION_ACTIVE
- COUNTERPARTY_ABSORBING
- STRUCTURE_WEAKENING
- HIGH_RESULT_EXIT
- BAGHOLDER_PRESSURE
- DATA_QUALITY_FAIL
- WALLET_GATE_MISSED
- WALLET_FALSE_SUPPORT
- early_wallet_sold_pct_delta >=20 且 position_pnl_pct <0 → WALLET_EXIT
- same_source_group_sold_pct_delta >=20 或 sync_sell_score >=70 → SAME_SOURCE_EXIT
- distribution_wallet_count_delta >=2 且 price_change_pct >=0 → DISTRIBUTION_ACTIVE
- counterparty_pressure_score_delta >=25 且 late_large_buyer_count_delta >=2 → COUNTERPARTY_ABSORBING
- wallet_structure_score_delta <=-20 或 wallet_risk_score_delta >=20 → STRUCTURE_WEAKENING
- high_result_remaining_pct_delta <=-20 → HIGH_RESULT_EXIT
- bagholder_whale_count_delta >=2 且 price_change_pct <=0 → BAGHOLDER_PRESSURE
- data_quality_score_at_entry <50 且交易失败 → DATA_QUALITY_FAIL
- entry 时 counterparty_pressure_score >=50 或 wallet_risk_score >=50 或 sync_sell_score >=60 或 data_quality_score <50，但仍进入 PAPER_READY → WALLET_GATE_MISSED
- entry 时 WALLET_SUPPORT，但交易亏损且 wallet_risk_score_delta >=20 → WALLET_FALSE_SUPPORT
# 本次认知升级点
```text
```text
# 尚未解决问题
```text
1. sikk_wallet_structure_gate.py 的完整代码骨架
2. tests/test_sikk_wallet_structure_gate.py 测试样例
3. sikk_candidate_wallet_structure_pipeline.py 的输入输出流程
4. wallet_structure_decision.json 与状态机的实际接入点
5. paper runner 如何根据钱包结构变化触发持仓管理或提前退出

---

<!-- source_marker=7133 -->

# SIKK-SOL 系统认知已重建

当前系统不再按“找庄家钱包脚本”理解，而应重建为：

> **SIKK-SOL 筹码控制权状态机**  
> 用钱包结构、筹码迁移、K线状态、报价安全、流动性成本、失败归因，持续判断一个 token 是否允许进入纸面交易验证。

核心变化：

```text
旧理解：识别哪个钱包是庄家
新理解：判断筹码控制权是否仍在结构侧，是否正在向对手盘转移
```

---

# 一、系统总定义

## SIKK-SOL v1.0 定位

```text
SIKK-SOL = 结构钱包行为识别 + 筹码迁移判断 + K线结构确认 + quote 安全验证 + 纸面交易复盘系统
```

它不是单纯的：

```text
量价策略
钱包跟单器
庄家识别器
自动实盘机器人
```

而是：

```text
结构智能交易验证系统
```

当前阶段：

```text
Phase A → Phase B 准备阶段
```

即：

```text
paper only → paper + human confirmation ticket
```

仍然禁止自动实盘。

---

# 二、核心认知重建

## 1. 不直接判断“庄家”

链上不能直接证明某个地址就是庄家。  
所以系统中不使用绝对裁决词：

```text
庄家
老鼠仓
内幕盘
绝对控盘
```

改用证据化语言：

```text
疑似结构侧钱包
疑似执行侧钱包
疑似同源执行组
疑似分发侧钱包
疑似对手盘承接钱包
疑似筹码转移
疑似结构侧减弱
```

---

## 2. 系统真正判断的是“筹码控制权”

核心问题不是：

```text
谁是庄？
```

而是：

```text
筹码现在在哪一侧？
早期优势钱包是否仍持有？
同源组是否同步撤退？
高结果钱包是否退出？
晚期钱包是否正在接货？
价格上涨是推进，还是出货？
当前入场是否会成为退出流动性？
```

---

## 3. 钱包结构是门禁，不是买入信号

正确逻辑：

```text
钱包结构支持
+ K线结构支持
+ quote 可靠
+ 安全扫描通过
+ 流动性可执行
+ 状态未过期
= 允许 PAPER_READY
```

错误逻辑：

```text
钱包结构好 → 直接买入
```

---

# 三、系统总架构：7 层

## 第 1 层：数据层

解决问题：

```text
数据从哪里来，字段是否完整，格式是否统一。
```

输入数据：

```text
GMGN 候选池
GMGN holder 数据
GMGN top trader
GMGN early buyer
GMGN wallet pnl
K线 1m / 5m
OKX quote
GMGN quote
GMGN pool price
安全扫描
流动性数据
```

输出：

```text
标准化 token 数据
标准化 wallet 数据
标准化 quote 数据
标准化 K线数据
```

---

## 第 2 层：钱包实体层

解决问题：

```text
单个地址是什么类型的钱包。
```

核心输出：

```text
wallet_classification.csv
```

核心字段：

```text
wallet_address
wallet_role
game_side
role_confidence
entry_rank
entry_time
sold_pct
remaining_pct
roi_pct
pnl_usd
same_source_group_id
risk_level
evidence_level
reason
```

---

## 第 3 层：当前 token 事件层

解决问题：

```text
这个钱包在当前 token 里做了什么。
```

判断内容：

```text
谁早入
谁清仓
谁部分持有
谁高收益
谁同步卖出
谁接盘
谁被套
谁可能是噪音
```

---

## 第 4 层：筹码迁移层

解决问题：

```text
筹码正在从哪一侧转移到哪一侧。
```

核心判断：

```text
结构侧是否增强
结构侧是否维持
结构侧是否减弱
派发是否活跃
对手盘是否正在承接
```

新增状态：

```text
STRUCTURE_STRENGTHENING   结构侧增强
STRUCTURE_HOLDING         结构侧维持
STRUCTURE_WEAKENING       结构侧减弱
DISTRIBUTION_ACTIVE       派发进行中
COUNTERPARTY_ABSORBING    对手盘承接中
UNKNOWN                   不明确
```

---

## 第 5 层：钱包结构门禁层

解决问题：

```text
钱包结构是否允许进入 PAPER_READY。
```

核心输出：

```text
wallet_structure_decision.json
```

核心分数：

```text
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
wallet_structure_factor
```

核心状态：

```text
WALLET_BLOCK
WALLET_PAUSE
WALLET_SUPPORT
WALLET_NEUTRAL
```

---

## 第 6 层：交易状态机层

解决问题：

```text
当前 token 应该处于什么交易状态。
```

状态流：

```text
WATCHING
  ↓
PAPER_READY
  ↓
READY_FOR_CONFIRMATION
  ↓
PAPER_OPEN
  ↓
PAPER_MANAGING
  ↓
PAPER_CLOSED
```

异常流：

```text
WALLET_BLOCK → BLOCKED
WALLET_PAUSE → PAUSE / WATCHING
QUOTE_FAIL → PAUSE_NEED_CONFIRM
SECURITY_FAIL → BLOCKED
STATE_EXPIRED → EXPIRED
```

---

## 第 7 层：复盘进化层

解决问题：

```text
系统判断是否真的有效。
```

复盘对象：

```text
10 个 token：字段完整性
30 个 token：阈值合理性
100 个 token：胜率、回撤、失败归因
```

输出：

```text
review_batch_001.csv
daily_report.md
failure_attribution.csv
threshold_adjustment_suggestions.md
```

---

# 四、v1.0 核心模块重建

## 模块 1：候选发现模块

职责：

```text
从 GMGN 新币池 / 热门池中发现候选 token。
```

输出：

```text
candidates.json
candidates.csv
```

字段：

```text
token_address
token_symbol
market_cap
liquidity
holder_count
pool_address
open_time
discovered_at
source
risk_tags
```

---

## 模块 2：K线结构模块

职责：

```text
判断价格是否出现可交易结构。
```

核心识别：

```text
吸筹窗口
控盘箱体
突破
回踩
二次推进
高低点结构
假突破
失效位
```

输出：

```text
sikk_signal_level
control_box_high
control_box_low
breakout_status
pullback_status
invalid_level
```

---

## 模块 3：钱包结构模块

职责：

```text
识别钱包角色、博弈侧、筹码迁移状态。
```

核心文件：

```text
sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
```

输出目录：

```text
data/gmgn_candidates_live_run/wallet_structure/
```

每个 token 输出：

```text
early_wallet_raw.csv
wallet_classification.csv
candidate_groups.csv
gmgn_note_table.csv
wallet_structure_decision.json
```

---

## 模块 4：对手盘压力模块

职责：

```text
判断主导侧是否正在把筹码转移给对手盘。
```

新增分数：

```text
counterparty_pressure_score
```

核心观察：

```text
早期钱包卖出增加
晚期大额钱包买入增加
套牢鲸鱼增加
持有人数上涨但价格推进弱
价格上涨但 Top Holder 下降
高结果钱包退出
```

---

## 模块 5：quote 一致性模块

职责：

```text
判断纸面入场价是否真实可靠。
```

比较：

```text
OKX quote
GMGN quote
GMGN pool price
Kline close price
paper runner price
```

规则：

```text
偏差 <= 2%      → ALLOW
偏差 2% - 5%    → PAUSE_NEED_CONFIRM
偏差 > 5%       → BLOCK_QUOTE_UNRELIABLE
```

---

## 模块 6：安全扫描模块

职责：

```text
排除不可交易风险。
```

检查：

```text
honeypot
高税
黑名单
mint 风险
暂停交易风险
LP 风险
池子过浅
异常权限
```

原则：

```text
钱包结构支持不能绕过安全门禁。
```

---

## 模块 7：纸面交易 runner

职责：

```text
用实时 quote 和交易成本模拟真实入场。
```

新增字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
wallet_structure_factor
wallet_structure_reason
wallet_evidence_level
```

入场价模式：

```text
--entry-price-mode signal
--entry-price-mode live
```

默认：

```text
live
```

---

## 模块 8：失败归因模块

职责：

```text
每笔失败都要知道失败原因。
```

失败类型：

```text
STRUCTURE_FAIL
LIQUIDITY_FAIL
QUOTE_FAIL
SECURITY_FAIL
MOMENTUM_FAIL
WALLET_EXIT
COUNTERPARTY_ABSORBING
DISTRIBUTION_ACTIVE
STOP_LOSS
TIME_STOP
STATE_EXPIRED
EXECUTION_FAIL
```

---

## 模块 9：Replay 回放模块

职责：

```text
验证规则是否在实时条件下有效，而不是事后看起来合理。
```

回放内容：

```text
过去 24h 候选
当时 K线
当时 quote
当时钱包状态
当时门禁判断
模拟入场
模拟止损
模拟止盈
失败归因
```

---

## 模块 10：历史地址库

职责：

```text
从单币判断升级到跨币复现。
```

长期字段：

```text
address
repeat_appearance_count
historical_role
historical_roi_profile
historical_exit_behavior
cross_token_group_similarity
old_money_confidence
last_seen_token
last_seen_time
```

v1.0 暂不作为主门禁，v2.0 接入。

---

# 五、钱包角色体系重建

## v1.0 先保留 8 类

```text
EARLY_BUYER              早期买入钱包
EARLY_EXIT               早期清仓钱包
PARTIAL_HOLDER           部分持有钱包
HIGH_RESULT_WALLET       高结果钱包
SAME_SOURCE_GROUP        疑似同源组钱包
DISTRIBUTION_SELLER      疑似分发/派发钱包
BAGHOLDER_WHALE          套牢鲸鱼
RETAIL_NOISE             普通噪音钱包
```

---

## 新增博弈侧字段：game_side

```text
STRUCTURE_SIDE        疑似结构侧
EXECUTION_SIDE        疑似执行侧
DISTRIBUTION_SIDE     疑似派发侧
COUNTERPARTY_SIDE     疑似对手盘侧
NOISE_SIDE            噪音侧
UNKNOWN_SIDE          未知
```

映射：

| 钱包角色 | 博弈侧 |
|---|---|
| EARLY_BUYER | STRUCTURE_SIDE / UNKNOWN_SIDE |
| EARLY_EXIT | DISTRIBUTION_SIDE |
| PARTIAL_HOLDER | STRUCTURE_SIDE / DISTRIBUTION_SIDE |
| HIGH_RESULT_WALLET | EXECUTION_SIDE |
| SAME_SOURCE_GROUP | EXECUTION_SIDE |
| DISTRIBUTION_SELLER | DISTRIBUTION_SIDE |
| BAGHOLDER_WHALE | COUNTERPARTY_SIDE |
| RETAIL_NOISE | NOISE_SIDE |

---

# 六、核心分数体系重建

## 1. wallet_structure_score：结构支持分

回答：

```text
钱包结构是否支持继续观察 / PAPER_READY？
```

满分 100：

```text
早期钱包仍持有              25
高结果钱包仍持有            20
同源组没有同步卖出          15
分发风险低                  15
持仓结构稳定                10
Top Trader 未反向           10
钱包行为与价格不冲突         5
```

解释：

```text
0-39   结构不支持
40-64  中性 / 观察
65-79  结构支持
80-100 强结构支持，但不直接买入
```

---

## 2. wallet_risk_score：钱包风险分

回答：

```text
是否存在清仓、同步卖出、派发、撤退风险？
```

满分 100：

```text
早期钱包集中清仓            30
同源组同步卖出              25
分发钱包增加                15
高结果钱包退出              10
Top Holder 出货             10
套牢鲸鱼压力                 5
数据不足                     5
```

解释：

```text
0-39   风险可接受
40-59  中风险
60-74  高风险
75-100 极高风险，WALLET_BLOCK
```

---

## 3. counterparty_pressure_score：对手盘压力分

回答：

```text
主导侧是否正在把筹码转移给对手盘？
```

满分 100：

```text
早期钱包卖出给晚期买盘        25
晚期大额钱包增加              20
套牢鲸鱼增加                  15
价格上涨但结构钱包卖出        20
持有人数增加但 Top Holder 下降 10
高结果钱包退出                10
```

解释：

```text
0-29   暂无明显对手盘压力
30-49  观察
50-69  中等对手盘压力
70-100 高对手盘压力
```

---

## 4. data_quality_score：数据质量分

回答：

```text
这次钱包结构判断的数据够不够用？
```

满分 100：

```text
早期钱包数据完整度            25
持仓 / 买卖字段完整度          20
时间字段完整度                15
ROI / PnL 字段完整度           15
资金来源 / 同源字段完整度      15
Top Holder / Top Trader 完整度 10
```

解释：

```text
80-100 数据较完整
60-79  可用但需保守
50-59  勉强可用
<50    数据不足，WALLET_PAUSE
```

---

# 七、门禁状态重建

## WALLET_SUPPORT

含义：

```text
结构侧仍未完全退出，对手盘压力不高，钱包行为与价格没有明显冲突。
```

触发条件：

```text
wallet_structure_score >= 65
wallet_risk_score <= 40
counterparty_pressure_score <= 40
data_quality_score >= 60
early_wallet_remaining_pct >= 30
same_source_sync_sell_score < 50
distribution_wallet_count <= 1
```

动作：

```text
允许进入 PAPER_READY，但不能绕过 quote/security/K线门禁。
```

---

## WALLET_NEUTRAL

含义：

```text
没有明显结构支持，也没有明显阻断。
```

动作：

```text
继续走其他门禁，不加分、不阻断。
```

---

## WALLET_PAUSE

含义：

```text
可能发生筹码转移、数据不足、或风险偏高，需要继续观察。
```

触发条件：

```text
data_quality_score < 50
wallet_risk_score >= 50
counterparty_pressure_score >= 50
top_holder_exit_pressure == HIGH
```

动作：

```text
进入 PAUSE / WATCHING。
```

---

## WALLET_BLOCK

含义：

```text
结构侧大概率撤退，继续入场可能成为退出流动性。
```

触发条件：

```text
wallet_risk_score >= 75
counterparty_pressure_score >= 70 且 wallet_risk_score >= 50
same_source_sync_sell_score >= 70
early_wallet_sold_pct >= 85 且 high_result_remaining_pct <= 10
distribution_wallet_count >= 3 且 early_wallet_remaining_pct <= 20
```

动作：

```text
BLOCKED
```

---

# 八、状态机接入重建

状态机读取：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
```

逻辑：

```python
if wallet_structure_status == "WALLET_BLOCK":
    state = "BLOCKED"

elif wallet_structure_status == "WALLET_PAUSE":
    state = "PAUSE"

elif wallet_structure_status == "WALLET_SUPPORT":
    if signal_gate == "ALLOW" and quote_gate == "ALLOW" and security_gate == "ALLOW":
        state = "PAPER_READY"
    else:
        state = "WATCHING"

elif wallet_structure_status == "WALLET_NEUTRAL":
    continue_with_existing_gates()
```

---

# 九、输出文件体系重建

## 总目录

```text
data/gmgn_candidates_live_run/
```

## 钱包结构目录

```text
data/gmgn_candidates_live_run/wallet_structure/
```

## 汇总文件

```text
candidate_wallet_structure_summary.json
candidate_wallet_structure_summary.csv
candidate_wallet_structure_summary.md
```

## 单 token 文件

```text
<token_address>/
  early_wallet_raw.csv
  wallet_classification.csv
  candidate_groups.csv
  gmgn_note_table.csv
  wallet_structure_decision.json
```

## 复盘文件

```text
review_batch_001.csv
review_batch_001.md
daily_report.md
failure_attribution.csv
```

---

# 十、wallet_structure_decision.json 标准

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TOKEN",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 32,
  "data_quality_score": 76,
  "wallet_structure_factor": 1.15,
  "wallet_evidence_level": "E2",
  "decision_action": "ALLOW_PAPER_READY",
  "dominant_side_status": "STRUCTURE_HOLDING",
  "chip_transfer_status": "NO_MAJOR_TRANSFER",
  "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出，对手盘压力不高",
  "support_signals": [
    "EARLY_WALLETS_PARTIAL_HOLDING",
    "HIGH_RESULT_WALLETS_STILL_HOLDING",
    "LOW_DISTRIBUTION_RISK"
  ],
  "risk_signals": [
    "TOP_TRADER_NEUTRAL"
  ],
  "game_side_summary": {
    "structure_side_wallet_count": 8,
    "execution_side_wallet_count": 5,
    "distribution_side_wallet_count": 1,
    "counterparty_side_wallet_count": 2,
    "noise_side_wallet_count": 34
  },
  "metrics": {
    "early_wallet_count": 42,
    "early_wallet_remaining_pct": 38.5,
    "early_wallet_sold_pct": 61.5,
    "high_result_wallet_count": 3,
    "high_result_remaining_pct": 31.2,
    "same_source_group_count": 1,
    "same_source_sync_sell_score": 22,
    "distribution_wallet_count": 1,
    "bagholder_whale_count": 0,
    "top_holder_exit_pressure": "LOW",
    "top_trader_buy_sell_bias": "NEUTRAL"
  },
  "created_at": "2026-05-02T00:00:00Z"
}
```

---

# 十一、开发优先级重建

当前不要先做完整历史库，也不要先做自动实盘。

## 第一优先级

```text
1. sikk_wallet_structure_gate.py
2. classify(w) v1.0
3. wallet_structure_score
4. wallet_risk_score
5. data_quality_score
6. counterparty_pressure_score
```

---

## 第二优先级

```text
7. sikk_candidate_wallet_structure_pipeline.py
8. wallet_structure_decision.json
9. 状态机读取 wallet_structure_decision.json
10. paper runner 写入 wallet_structure_factor
```

---

## 第三优先级

```text
11. 10 个 token 复盘模板
12. 多轮快照 delta
13. failure_attribution 接入钱包结构原因
14. replay 模式
```

---

## 第四优先级

```text
15. 历史地址库
16. 跨币复现
17. 老庄画像
18. confirmation ticket
19. 小仓实盘门禁
```

---

# 十二、下一步最小可执行版本

你现在最应该让 AI / Codex / OpenClaw 做的是：

```text
实现 SIKK-SOL v1.0 钱包结构门禁层。
```

最小可执行文件：

```text
sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
tests/test_sikk_wallet_structure_gate.py
tests/test_sikk_candidate_wallet_structure_pipeline.py
```

最小输出：

```text
wallet_structure_decision.json
candidate_wallet_structure_summary.csv
```

最小接入：

```text
状态机读取 WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT / WALLET_NEUTRAL
paper runner 写入 wallet_structure_factor
```

---

# 十三、可以直接复制给 AI 的总指令

```text
你现在负责重建 SIKK-SOL v1.0 钱包结构门禁层。

系统目标不是直接识别“庄家钱包”，而是构建一个筹码控制权状态机，用钱包结构、筹码迁移、K线结构、quote 安全、流动性成本、失败归因来判断一个 token 是否允许进入 PAPER_READY。

核心原则：
1. 不直接使用“庄家”作为结论，只使用证据化表达。
2. 钱包结构是门禁，不是独立买入信号。
3. 系统要判断筹码控制权是否仍在结构侧，是否正在向对手盘转移。
4. WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。
5. 当前阶段禁止自动实盘，只允许 paper trading 和 future confirmation ticket。

请实现以下文件：
1. sikk_wallet_structure_gate.py
2. sikk_candidate_wallet_structure_pipeline.py
3. tests/test_sikk_wallet_structure_gate.py
4. tests/test_sikk_candidate_wallet_structure_pipeline.py

钱包角色 v1.0：
- EARLY_BUYER
- EARLY_EXIT
- PARTIAL_HOLDER
- HIGH_RESULT_WALLET
- SAME_SOURCE_GROUP
- DISTRIBUTION_SELLER
- BAGHOLDER_WHALE
- RETAIL_NOISE

新增 game_side：
- STRUCTURE_SIDE
- EXECUTION_SIDE
- DISTRIBUTION_SIDE
- COUNTERPARTY_SIDE
- NOISE_SIDE
- UNKNOWN_SIDE

核心分数：
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score

核心状态：
- WALLET_BLOCK
- WALLET_PAUSE
- WALLET_SUPPORT
- WALLET_NEUTRAL

状态机接入：
- WALLET_BLOCK → BLOCKED
- WALLET_PAUSE → PAUSE / WATCHING
- WALLET_SUPPORT → 只有 signal_gate、quote_gate、security_gate 都通过，才允许 PAPER_READY
- WALLET_NEUTRAL → 不加分、不阻断，继续走其他门禁

输出文件：
data/gmgn_candidates_live_run/wallet_structure/
  candidate_wallet_structure_summary.json
  candidate_wallet_structure_summary.csv
  candidate_wallet_structure_summary.md

每个 token 子目录：
  early_wallet_raw.csv
  wallet_classification.csv
  candidate_groups.csv
  gmgn_note_table.csv
  wallet_structure_decision.json

paper runner 新增字段：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- wallet_structure_factor
- wallet_structure_reason
- wallet_evidence_level

测试要求：
1. 早期钱包集中清仓 → WALLET_BLOCK
2. 同源组同步卖出 → WALLET_BLOCK
3. 对手盘压力高 → WALLET_BLOCK 或 WALLET_PAUSE
4. 数据不足 → WALLET_PAUSE
5. 早期钱包仍持有、高结果钱包未退出、风险低 → WALLET_SUPPORT
6. 无明显结构证据 → WALLET_NEUTRAL
```

---

# 十四、最终重建结论

SIKK-SOL 现在应该被定义为：

```text
筹码控制权状态机
```

而不是：

```text
庄家钱包识别脚本
```

它的核心能力是：

```text
1. 识别早期优势钱包是否仍在
2. 判断同源执行组是否撤退
3. 判断高结果钱包是否退出
4. 判断筹码是否向晚期对手盘转移
5. 判断价格上涨是推进还是派发
6. 判断当前入场是否会成为别人退出流动性
7. 把这些判断转成 WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT
8. 接入状态机和纸面交易验证
```

---

# 本次认知升级点

本次系统重建的核心升级是：

> **从“找庄家”升级为“判断筹码控制权状态”。**

新的 SIKK-SOL 不再围绕单个钱包身份做绝对判断，而是围绕：

```text
结构侧
执行侧
派发侧
对手盘侧
噪音侧
```

持续判断：

```text
谁在控制筹码
谁在退出
谁在接货
谁在提供流动性
当前结构是否仍值得进入 PAPER_READY
```

---

# 尚未解决问题

下一步需要继续定稿 5 个具体工程问题：

```text
1. same_source_group_id 如何生成
2. sync_buy_score / sync_sell_score 如何计算
3. counterparty_pressure_score 的精确字段来源
4. 多轮快照 delta 如何设计
5. 钱包结构失败如何进入 failure_attribution
```

---

<!-- source_marker=7229 -->

从整体大局看，你的脚本不要理解成“找庄家脚本”，而应该理解成：

> **把链上钱包行为、筹码迁移、价格结构、报价安全、历史复现，统一转成一个可执行的结构状态判断系统。**

也就是说，脚本的核心不是直接判断：

```text
这个钱包是不是庄家？
```

而是连续回答：

```text
筹码现在在谁手里？
早期优势钱包有没有退出？
疑似执行组是否还在维护结构？
筹码是不是正在转移给对手盘？
现在入场是不是在接别人出货？
这个 token 是否允许进入 PAPER_READY？
```

---

# 一、脚本对“庄家筹码实时分析”应该怎么理解？

## 1. 不是实时识别庄家，而是实时识别筹码状态

链上不能直接证明某个地址就是庄家。  
所以系统应该避免使用绝对判断：

```text
庄家钱包
庄家正在出货
庄家正在控盘
```

应该改成证据化表达：

```text
疑似结构侧钱包
疑似执行组钱包
疑似早期优势钱包
疑似分发钱包
疑似对手盘承接钱包
疑似筹码向晚期钱包转移
```

你的脚本真正要做的是：

```text
连续追踪筹码控制权是否增强、维持、减弱、转移、崩塌。
```

---

## 2. “实时”本质是多轮快照对比

GMGN / K线 / quote / holder 数据不是一次看完就结束。  
真正有价值的是：

```text
第 1 次快照：早期钱包还持有多少
第 2 次快照：早期钱包是否开始卖
第 3 次快照：同源组是否同步卖
第 4 次快照：晚期大额钱包是否接货
第 5 次快照：价格是否还能继续推进
```

所以脚本要从“单次报告”升级为：

```text
多轮快照 → 差值变化 → 结构状态迁移
```

也就是：

```text
Snapshot A
  ↓
Snapshot B
  ↓
Delta 变化
  ↓
结构状态判断
  ↓
状态机动作
```

---

## 3. 单次数据看身份，多次数据看意图

单次钱包数据只能判断：

```text
这个钱包早入
这个钱包卖出多
这个钱包 ROI 高
这个钱包持仓大
```

但连续数据才能判断：

```text
它是不是在撤退
它是不是在维护结构
它是不是边拉边卖
它是不是接盘后被套
它是不是同源组同步操作
```

所以你的系统应该明确分成两类判断：

| 判断类型 | 数据基础 | 作用 |
|---|---|---|
| 静态身份判断 | 单次快照 | 钱包角色分类 |
| 动态行为判断 | 多轮快照 | 筹码迁移、分发、撤退、承接 |

---

# 二、钱包数据分析在系统里的位置

钱包分析不是单独存在的模块。  
它应该是整个 SIKK 系统的核心中层。

完整结构应该是：

```text
候选发现
  ↓
K线结构信号
  ↓
钱包结构分析
  ↓
筹码迁移判断
  ↓
quote / 安全扫描
  ↓
状态机
  ↓
纸面交易 / confirmation ticket
  ↓
复盘校准
```

其中钱包结构层负责回答：

```text
这个 token 的“人”是否还支持继续走？
```

K线层负责回答：

```text
这个 token 的“价格结构”是否出现可交易形态？
```

quote 层负责回答：

```text
这个 token 现在是否能按合理价格成交？
```

安全层负责回答：

```text
这个 token 是否存在交易风险、合约风险、池子风险？
```

状态机负责回答：

```text
现在应该 WATCHING、PAUSE、BLOCKED，还是 PAPER_READY？
```

---

# 三、脚本应该围绕 5 个核心问题运行

## 问题 1：谁先拿到了筹码？

对应字段：

```text
entry_rank
entry_time
buy_amount_usd
is_new_wallet
funding_source
same_source_group_id
```

目的：

```text
识别早期优势钱包、疑似执行钱包、疑似同源组。
```

如果多个钱包在极短时间内进入，并且资金来源相似、买入行为相似，就不是普通散户行为。

---

## 问题 2：早期筹码还在不在？

对应字段：

```text
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_remaining_pct
same_source_group_remaining_pct
```

目的：

```text
判断结构侧是否仍有继续维护价格的动机。
```

如果早期优势钱包大部分已经清仓，那么价格再涨也可能只是晚期对手盘在追。

---

## 问题 3：筹码有没有转移给对手盘？

对应字段：

```text
late_buyer_ratio
bagholder_whale_count
new_holder_growth
top_holder_exit_pressure
counterparty_pressure_score
```

目的：

```text
判断自己入场后是否会成为别人的退出流动性。
```

典型危险结构：

```text
早期钱包卖出增加
晚期钱包买入增加
持有人数上涨
价格推进变弱
成交量放大但结构钱包退出
```

这就是对手盘承接压力。

---

## 问题 4：拉升是推进还是派发？

对应字段：

```text
price_change_pct
volume_change
early_wallet_sold_pct_delta
same_source_sync_sell_score
distribution_wallet_count
top_holder_pct_delta
```

判断逻辑：

```text
价格涨 + 结构钱包继续持有 = 推进可能性增加
价格涨 + 结构钱包同步卖出 = 边拉边卖风险增加
价格涨 + Top Holder 下降 = 派发风险增加
价格涨 + 晚期接盘增加 = 对手盘压力增加
```

---

## 问题 5：结构状态正在增强还是衰减？

最终输出应该不是一句话，而是状态：

```text
STRUCTURE_STRENGTHENING   结构增强
STRUCTURE_HOLDING         结构维持
STRUCTURE_WEAKENING       结构衰减
DISTRIBUTION_ACTIVE       派发进行中
COUNTERPARTY_ABSORBING    对手盘承接中
UNKNOWN                   不明确
```

这比简单说“好 / 坏”更适合自动交易系统。

---

# 四、脚本应该输出的不是报告，而是决策材料

你的钱包分析脚本最终应该生成 4 类东西。

## 1. 钱包分类表

```text
wallet_classification.csv
```

回答：

```text
每个钱包是谁？
它属于哪一类？
它站在哪个博弈侧？
证据等级是多少？
```

核心字段：

```text
wallet_address
wallet_role
game_side
role_confidence
remaining_pct
sold_pct
roi_pct
pnl_usd
same_source_group_id
evidence_level
risk_level
reason
```

---

## 2. 筹码迁移摘要

```text
wallet_structure_decision.json
```

回答：

```text
整个 token 的结构状态是什么？
是否支持 PAPER_READY？
是否应该 PAUSE / BLOCK？
```

核心字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
dominant_side_status
chip_transfer_status
decision_action
reason
```

---

## 3. GMGN 备注表

```text
gmgn_note_table.csv
```

回答：

```text
哪些钱包值得放进 GMGN 监控？
应该怎么备注？
```

格式继续用证据化表达：

```text
$TOKEN@D1｜早入｜重仓+低频｜高ROI+部分退｜CL_xxx｜E2
```

---

## 4. 纸面交易因子

写入 paper runner：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
wallet_structure_factor
wallet_structure_reason
```

这一步的意义是：

```text
让钱包结构真正影响 PAPER_READY，而不是只生成分析报告。
```

---

# 五、整体系统里还需要哪些辅助部分？

钱包结构很重要，但它不能独立决定交易。  
它必须和下面这些模块配合。

---

## 1. K线结构模块

作用：

```text
判断价格是否出现可交易结构。
```

主要看：

```text
吸筹窗口
控盘箱体
突破
回踩
二次推进
高低点结构
成交量扩张
假突破
失效位
```

钱包结构告诉你：

```text
谁在持有、谁在卖、谁在接。
```

K线结构告诉你：

```text
这些行为有没有反映到价格推进上。
```

两者必须结合。

典型判断：

```text
钱包结构支持 + K线突破回踩成功 = PAPER_READY 概率提高
钱包结构支持 + K线跌破箱体 = 不入场
钱包结构风险高 + K线拉升 = 警惕边拉边卖
```

---

## 2. 成交量 / 成交效率模块

作用：

```text
判断拉升质量。
```

不能只看价格涨，要看：

```text
上涨是否需要越来越大的成交量
放量后价格是否能保持
OBV 是否跟随
买盘是否有效推动
成交量是否只是在给出货提供流动性
```

辅助判断：

```text
价格上涨 + 成交效率下降 + 结构钱包卖出 = 派发嫌疑增加
价格上涨 + 成交效率上升 + 结构钱包持有 = 推进质量较好
```

---

## 3. quote / 多报价源一致性模块

作用：

```text
判断纸面入场价是否可靠。
```

必须比较：

```text
OKX quote
GMGN quote
GMGN pool price
K线 close price
paper runner price
```

如果价格偏差大：

```text
PAUSE_NEED_CONFIRM
```

否则纸面收益会失真。

钱包结构再好，如果 quote 不可靠，也不能进入真实交易路径。

---

## 4. 安全扫描模块

作用：

```text
排除交易不可执行或高风险 token。
```

检查：

```text
是否 honeypot
是否高税
是否可暂停交易
是否池子过浅
是否 LP 风险
是否 mint 权限异常
是否黑名单风险
```

状态机原则：

```text
wallet_structure_support 不能绕过 security_gate
```

也就是说：

```text
钱包结构支持 ≠ 可以交易
```

---

## 5. 流动性 / 滑点模块

作用：

```text
判断你能不能以合理成本进出。
```

meme token 最大的问题之一是：

```text
看起来涨了，但你真实成交吃不到。
```

所以必须有：

```text
buy_slippage_pct
sell_slippage_pct
dex_fee_pct
priority_fee_sol
failed_tx_cost_sol
quote_deviation_buffer_pct
```

否则纸面交易会高估收益。

---

## 6. 历史地址库

这是你系统的长期核心。

单币分析只能告诉你：

```text
这个地址在当前 token 做了什么。
```

历史地址库能告诉你：

```text
这个地址以前有没有出现过？
它以前是早期执行者还是接盘者？
它是否多次参与高结果 token？
它是否多次清仓后 token 崩？
它是否属于某个反复出现的结构组？
```

后续可以增加：

```text
address_history_score
repeat_appearance_count
historical_roi_profile
historical_exit_behavior
cross_token_group_similarity
old_money_confidence
```

这是从 v1.0 进入 v2.0 的关键。

---

## 7. Replay / 回放模块

作用：

```text
验证规则是不是事后看起来合理，还是实时也能成立。
```

你需要回放：

```text
过去 24h 的候选
当时的钱包状态
当时的 K线状态
当时的 quote
当时的风险扫描
当时是否应该 PAPER_READY
```

如果只看结果，容易产生幸存者偏差。  
Replay 是防止系统自欺的关键模块。

---

## 8. 失败归因模块

每笔失败都要归因：

```text
STRUCTURE_FAIL
LIQUIDITY_FAIL
QUOTE_FAIL
SECURITY_FAIL
MOMENTUM_FAIL
WALLET_EXIT
COUNTERPARTY_ABSORBING
DISTRIBUTION_ACTIVE
STOP_LOSS
TIME_STOP
```

否则你只能看到亏了，但不知道为什么亏。

长期优化不是靠感觉，而是靠：

```text
失败原因 Top 5
不同失败类型的亏损贡献
不同钱包状态下的胜率
不同结构状态下的最大回撤
```

---

# 六、系统最终应该形成 7 层理解

## 第 1 层：数据层

收集：

```text
GMGN 候选
holder 数据
top trader
early buyer
wallet pnl
K线
quote
security scan
liquidity
```

目标：

```text
保证字段完整、时间统一、格式统一。
```

---

## 第 2 层：钱包实体层

处理：

```text
钱包地址
资金来源
同源组
交易行为
持仓变化
角色分类
```

目标：

```text
把地址从“孤立地址”变成“有角色的钱包实体”。
```

---

## 第 3 层：当前 token 事件层

判断：

```text
谁早入
谁清仓
谁部分持有
谁高 ROI
谁同步卖
谁接盘
```

目标：

```text
看清当前 token 内部的筹码行为。
```

---

## 第 4 层：筹码迁移层

判断：

```text
筹码是否从早期钱包转给晚期钱包
结构侧是否减弱
对手盘是否增加
派发是否正在发生
```

目标：

```text
理解当前博弈方向。
```

---

## 第 5 层：门禁评分层

生成：

```text
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
wallet_structure_status
```

目标：

```text
把复杂钱包行为转成状态机可读取的决策信号。
```

---

## 第 6 层：交易状态机层

决策：

```text
BLOCKED
WATCHING
PAUSE
PAPER_READY
READY_FOR_CONFIRMATION
PAPER_OPEN
PAPER_CLOSED
```

目标：

```text
把分析结果接入交易流程。
```

---

## 第 7 层：复盘进化层

统计：

```text
10 个 token 字段完整性
30 个 token 阈值合理性
100 个 token 胜率 / 回撤 / 失败归因
```

目标：

```text
不断校准标准，而不是凭感觉改规则。
```

---

# 七、最重要的系统原则

## 原则 1：钱包结构是门禁，不是单独买入信号

不能因为钱包结构好就买。

正确逻辑：

```text
钱包结构支持
+ K线结构支持
+ quote 可靠
+ 安全扫描通过
+ 状态未过期
= 允许 PAPER_READY
```

---

## 原则 2：早期钱包退出比散户买入更重要

如果你看到：

```text
holder_count 增加
散户买入增加
价格上涨
```

但同时：

```text
early_wallet_sold_pct 上升
high_result_remaining_pct 下降
same_source_sync_sell_score 上升
```

这不是强势，可能是派发。

---

## 原则 3：同源组同步卖出是高优先级风险

同源组同步买入可能是结构支持。  
同源组同步卖出通常是结构撤退信号。

所以：

```text
same_source_sync_sell_score
```

应该是 v1.0 里面最重要的风险字段之一。

---

## 原则 4：接盘鲸鱼不一定是好事

很多时候“大钱包买入”不是利好，而是：

```text
被动承接
追涨接货
高位被套
给早期钱包退出
```

所以要看：

```text
它买入后价格是否继续推进
它买入时早期钱包是否卖出
它买入后是否迅速浮亏
```

---

## 原则 5：数据不足不能强行支持

如果：

```text
data_quality_score < 50
```

即使 K线好，也应该：

```text
WALLET_PAUSE
```

因为你不是没有风险，而是没有看清风险。

---

# 八、你当前最应该补齐的系统部分

按优先级：

```text
1. wallet_structure_decision.json 标准化
2. classify(w) v1.0 角色分类
3. wallet_structure_score / wallet_risk_score
4. counterparty_pressure_score
5. 状态机读取钱包结构门禁
6. paper runner 写入 wallet_structure_factor
7. 10 个 token 复盘模板
8. 多轮快照 delta 对比
9. 历史地址库
10. replay 模式
```

最先不要做太复杂的“庄家画像”。  
先把钱包结构变成可运行的门禁。

---

# 九、最终大局图

```text
GMGN 新币候选
  ↓
数据标准化
  ↓
K线结构分析
  ↓
钱包结构分析
  ├─ 早期钱包
  ├─ 高结果钱包
  ├─ 同源执行组
  ├─ 分发钱包
  ├─ 接盘鲸鱼
  └─ 普通噪音
  ↓
筹码迁移判断
  ├─ 结构侧增强
  ├─ 结构侧维持
  ├─ 结构侧减弱
  ├─ 派发进行中
  └─ 对手盘承接中
  ↓
门禁评分
  ├─ wallet_structure_score
  ├─ wallet_risk_score
  ├─ counterparty_pressure_score
  └─ data_quality_score
  ↓
状态机
  ├─ WALLET_BLOCK → BLOCKED
  ├─ WALLET_PAUSE → PAUSE / WATCHING
  ├─ WALLET_SUPPORT → 可进入 PAPER_READY
  └─ WALLET_NEUTRAL → 继续其他门禁
  ↓
quote / security / liquidity
  ↓
paper runner
  ↓
日报 + 失败归因 + replay
  ↓
阈值校准 + 历史地址库
```

---

# 十、简短结论

你的脚本体系应该这样理解：

> **钱包数据分析不是为了单次找出“庄家钱包”，而是为了持续判断筹码控制权是否还在结构侧、是否正在向对手盘转移、是否已经进入派发阶段。**

其他辅助模块的作用是：

```text
K线模块：验证价格结构是否配合
成交量模块：验证推进质量
quote 模块：验证入场价格是否真实
安全扫描：排除不可交易风险
流动性模块：修正真实成本
历史地址库：识别反复出现的结构钱包
replay 模块：验证规则是否实时有效
失败归因：告诉你系统错在哪里
```

最终你的 SIKK 系统不是普通交易机器人，而是：

```text
结构钱包行为识别
+ 筹码迁移判断
+ K线状态确认
+ quote 安全验证
+ 纸面交易复盘
= 结构智能交易系统
```

---

# 本次认知升级点

核心升级是：

> 你不是在做“庄家识别脚本”，而是在做“筹码控制权状态机”。

这个状态机要持续判断：

```text
结构侧是否还在
执行组是否撤退
筹码是否转移给对手盘
价格推进是否真实
当前入场是否会成为退出流动性
```

---

# 尚未解决问题

下一步最值得继续定稿：

```text
1. counterparty_pressure_score 完整公式
2. 多轮快照 delta 字段标准
3. dominant_side_status 状态迁移规则
4. 钱包结构与 K线结构如何共振
5. 钱包结构失败如何进入 failure_attribution
```