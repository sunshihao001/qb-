下面是可直接保存为：

```text
/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_data_fact_controller.md
```

的完整版本。

---

# phase_01_data_fact_controller.md

# SIKK Stable Trader OS

## Phase 01：数据事实层控制器

版本：v1.0  
阶段编号：Phase 01  
阶段名称：数据事实层控制器  
英文标识：`phase_01_data_fact_controller`  
系统定位：事实接收、字段标准化、数据质量审计、下游交接  
适用系统：SIKK Stable Trader OS / SIKK-GMGN / Wallet-Intel / Hermes 自动化执行体系  
输出原则：只保留事实，不提前解释，不越级判断

---

# 0. 本阶段核心结论

第 1 阶段不是“分析阶段”，而是整个系统的 **事实地基层**。

它的任务不是判断：

```text
这个币是不是好机会
是不是吸筹
是不是派发
是不是二段扩张
是不是庄家控盘
是不是可以买
```

它只负责回答：

```text
当前系统到底拿到了什么数据？
这些数据来自哪里？
字段含义是否统一？
字段是否缺失？
时间、金额、地址、代币、钱包行为是否可以被下游安全使用？
是否足够进入第 2 阶段场景识别？
```

所以本阶段的核心不是“聪明判断”，而是：

```text
数据保真
字段统一
来源可追溯
缺失可识别
质量可审计
下游可读取
```

这个阶段必须服务于后面的结构地址识别、钱包行为分类、同源组判断、历史地址库和 GMGN 备注输出逻辑。现有结构地址方法论中已经明确要求“证据优先、不做绝对定性、每个判断必须有字段证据、规则依据、证据等级和风险等级”，第 1 阶段就是为这些后续判断提供可靠证据底座。

---

# 1. 阶段定位

## 1.1 本阶段负责什么

Phase 01 负责建立当前 token 的 **统一事实快照**。

主要职责：

```text
1. 接收 GMGN / 链上 / K线 / quote / security / 历史库等上游数据
2. 保留原始数据快照
3. 建立字段映射表
4. 统一 token、wallet、trade、holder、transfer、kline、quote 等基础字段
5. 统一时间口径
6. 统一金额单位
7. 校验 Solana 地址格式
8. 标记缺失字段
9. 标记字段可信度
10. 输出标准化事实包
11. 判断是否允许进入 Phase 02 多模型场景识别
```

---

## 1.2 本阶段不负责什么

Phase 01 严格禁止做以下事情：

```text
禁止判断吸筹
禁止判断派发
禁止判断二段扩张
禁止判断主导侧动机
禁止判断庄家心理
禁止判断买点
禁止判断卖点
禁止判断是否值得参与
禁止生成交易信号
禁止输出最终评分
禁止写“确定庄家”
禁止把 GMGN 标签当成最终结论
```

允许输出的只能是：

```text
字段存在
字段缺失
字段异常
数据来源
基础事实
可用程度
是否满足下游分析最低数据条件
```

---

# 2. 本阶段在总系统中的位置

```text
Phase 00：目标边界定义
        ↓
Phase 01：数据事实层控制器
        ↓
Phase 02：多模型交易场景识别体系
        ↓
Phase 03：钱包筹码结构分析
        ↓
Phase 04：主导侧生命周期与意图假设
        ↓
Phase 05：策略门禁与参与条件
        ↓
Phase 06：执行风控
        ↓
Phase 07：纸面交易验证
        ↓
Phase 08：复盘归因
        ↓
Phase 09：解释审计
        ↓
Phase 10：系统校准
```

Phase 01 是所有后续阶段的入口。

如果 Phase 01 的事实层不稳定，后面所有判断都会被污染。

---

# 3. 阶段目标

## 3.1 总目标

把来自不同来源的原始数据统一成一个可审计、可复盘、可交接的标准事实包。

标准事实包必须满足：

```text
1. 每个字段有中文解释
2. 每个字段有来源
3. 每个字段有数据类型
4. 每个字段有单位
5. 每个字段有缺失状态
6. 每个字段有可信度
7. 每个文件有生成时间
8. 每个 token 有唯一 run_id
9. 每个钱包地址可追溯到原始数据
10. 每个下游阶段可以直接读取
```

---

## 3.2 本阶段最终回答的问题

```text
Q1：当前分析对象是谁？
Q2：当前 token 的基础信息是否完整？
Q3：GMGN 数据是否拿到？
Q4：交易地址、持仓地址、转账地址是否拿到？
Q5：钱包级数据是否可以用于后续分类？
Q6：K线与成交量数据是否可以用于场景识别？
Q7：quote / security 数据是否可以用于安全过滤？
Q8：历史地址库是否可以对接？
Q9：哪些字段缺失？
Q10：哪些字段异常？
Q11：是否允许进入 Phase 02？
```

---

# 4. 输入前置条件

Phase 01 启动前，Phase 00 必须至少提供以下配置。

## 4.1 必填配置

```json
{
  "token_address": "Solana token mint address",
  "chain": "solana",
  "run_mode": "manual | live | replay | paper",
  "analysis_depth": "basic | standard | deep",
  "created_at": "ISO8601 time"
}
```

---

## 4.2 建议配置

```json
{
  "token_symbol": "可选，缺失时由上游补查",
  "start_time": "分析窗口开始时间",
  "end_time": "分析窗口结束时间",
  "discovery_time": "系统首次发现该 token 的时间",
  "discovery_market_cap_usd": "发现时市值",
  "fetch_gmgn_traders": true,
  "fetch_gmgn_holders": true,
  "fetch_gmgn_labels": true,
  "fetch_wallet_profiles": true,
  "fetch_fund_flow": true,
  "fetch_token_transfers": true,
  "fetch_kline": true,
  "fetch_quote": true,
  "fetch_security": true,
  "update_history_database": false
}
```

---

# 5. 输入数据来源

Phase 01 支持多源输入，但所有来源必须被标记。

## 5.1 GMGN 数据源

| 数据类型                | 用途                                  | 本阶段处理方式 |
| ------------------- | ----------------------------------- | ------- |
| token 基础信息          | 获取符号、市值、流动性、创建时间                    | 标准化     |
| trader 列表           | 获取买卖地址与盈亏                           | 标准化     |
| holder 列表           | 获取当前持仓结构                            | 标准化     |
| wallet profile      | 获取钱包画像                              | 标准化     |
| gmgn 标签             | sniper / fresh / bundle / insider 等 | 只作为标签事实 |
| pnl 数据              | 盈亏、倍数、已实现/未实现                       | 标准化     |
| buy / sell 记录       | 买卖时间、金额、次数                          | 标准化     |
| top holder          | 判断筹码集中度的原始依据                        | 只保留事实   |
| smart money / whale | 标签信息                                | 不直接下结论  |

---

## 5.2 链上数据源

|数据类型|用途|本阶段处理方式|
|---|---|---|
|Solana transfer|Token 转入转出事实|标准化|
|SOL / USDC funding|资金来源事实|标准化|
|swap transaction|买卖路径事实|标准化|
|wallet first_seen|钱包首次出现时间|标准化|
|wallet activity|钱包活跃度|标准化|
|token mint info|代币基础信息|标准化|
|pool info|池子信息|标准化|

---

## 5.3 市场结构数据源

|数据类型|用途|本阶段处理方式|
|---|---|---|
|K线|后续场景识别|标准化|
|成交量|后续真假突破判断|标准化|
|VWAP / AVWAP 输入数据|后续结构判断|只保留基础 OHLCV|
|market cap|判断入场早晚|标准化|
|liquidity|流动性风险|标准化|
|quote|价格一致性|标准化|
|security scan|安全过滤|标准化|

---

## 5.4 历史库数据源

|数据类型|用途|本阶段处理方式|
|---|---|---|
|address_history_database|判断地址是否复现|只读取，不更新|
|known_noise_wallets|噪音地址过滤|标记|
|known_cex_wallets|CEX 地址过滤|标记|
|known_router_wallets|路由地址过滤|标记|
|previous_token_runs|历史 token 对比|只建立引用|

---

# 6. 输出目录结构

建议统一写入新系统目录，不污染旧运行目录。

```text
/root/sikk-gmgn/
└── data/
    └── stable_trader_os/
        └── runs/
            └── <run_id>/
                ├── 00_config/
                │   ├── analysis_config.json
                │   └── phase_00_boundary_summary.md
                │
                ├── 01_data_fact/
                │   ├── raw/
                │   │   ├── raw_gmgn_token.json
                │   │   ├── raw_gmgn_traders.json
                │   │   ├── raw_gmgn_holders.json
                │   │   ├── raw_gmgn_wallet_profiles.json
                │   │   ├── raw_chain_transfers.json
                │   │   ├── raw_kline.json
                │   │   ├── raw_quote.json
                │   │   └── raw_security.json
                │   │
                │   ├── normalized/
                │   │   ├── token_fact.json
                │   │   ├── wallet_fact_table.csv
                │   │   ├── trade_fact_table.csv
                │   │   ├── holder_fact_table.csv
                │   │   ├── transfer_fact_table.csv
                │   │   ├── kline_fact_table.csv
                │   │   ├── quote_fact.json
                │   │   └── security_fact.json
                │   │
                │   ├── audit/
                │   │   ├── field_mapping.md
                │   │   ├── field_quality_report.json
                │   │   ├── missing_fields_report.csv
                │   │   ├── anomaly_fields_report.csv
                │   │   ├── source_coverage_report.md
                │   │   └── phase_01_quality_gate.json
                │   │
                │   ├── handoff/
                │   │   ├── phase_01_handoff_to_phase_02.json
                │   │   └── phase_01_handoff_summary.md
                │   │
                │   └── phase_01_data_fact_report.md
                │
                └── manifest/
                    ├── run_manifest.json
                    └── file_index.json
```

---

# 7. 文件命名规范

## 7.1 run_id 规则

```text
<chain>_<token_symbol_or_unknown>_<token_address_short>_<YYYYMMDD_HHMMSS>
```

示例：

```text
solana_ABC_8xk2P9_20260509_112300
```

如果 token_symbol 缺失：

```text
solana_UNKNOWN_8xk2P9_20260509_112300
```

---

## 7.2 文件命名原则

```text
raw_*          原始数据，不修改
*_fact         标准化事实数据
*_report       人类可读报告
*_audit        审计文件
*_handoff      下游交接文件
*_quality_gate 是否允许进入下一阶段
```

---

# 8. 标准字段体系

Phase 01 的字段分成 8 组。

```text
A. 运行字段
B. token 基础字段
C. 钱包基础字段
D. 交易行为字段
E. 持仓字段
F. 转账字段
G. 市场结构字段
H. 数据质量字段
```

---

# 9. A组：运行字段

|字段名|中文含义|类型|是否必填|示例|
|---|---|---|---|---|
|run_id|本次运行唯一编号|string|是|solana_ABC_xxxx|
|phase_id|阶段编号|string|是|phase_01|
|run_mode|运行模式|string|是|live|
|chain|链名称|string|是|solana|
|token_address|代币地址|string|是|xxx|
|created_at|本阶段开始时间|datetime|是|2026-05-09T11:23:00+09:00|
|completed_at|本阶段完成时间|datetime|否|2026-05-09T11:24:00+09:00|
|data_snapshot_time|数据快照时间|datetime|是|2026-05-09T11:23:40+09:00|
|source_version|数据源版本|string|否|gmgn_api_v1|
|operator|执行主体|string|否|hermes|

---

# 10. B组：Token 基础字段

输出文件：

```text
normalized/token_fact.json
```

建议结构：

```json
{
  "run_id": "solana_ABC_xxxx",
  "chain": "solana",
  "token_address": "token mint address",
  "token_symbol": "ABC",
  "token_name": "ABC Token",
  "token_create_time": "2026-05-09T10:00:00+09:00",
  "token_age_seconds": 4980,
  "discovery_time": "2026-05-09T10:10:00+09:00",
  "discovery_delay_seconds": 600,
  "current_price_usd": 0.00012,
  "current_market_cap_usd": 420000,
  "discovery_market_cap_usd": 120000,
  "market_cap_change_from_discovery_pct": 250.0,
  "current_liquidity_usd": 56000,
  "current_volume_24h_usd": 980000,
  "holder_count": 1420,
  "top10_holder_ratio": 0.34,
  "pool_address": "pool address",
  "dex": "raydium",
  "data_source": ["gmgn", "chain"],
  "field_quality_status": "usable"
}
```

---

# 11. C组：钱包基础字段

输出文件：

```text
normalized/wallet_fact_table.csv
```

字段表：

|字段名|中文含义|类型|来源|缺失处理|
|---|---|---|---|---|
|wallet_address|钱包地址|string|GMGN/链上|必填|
|wallet_address_valid|地址格式是否有效|bool|系统校验|false|
|wallet_first_seen_time|钱包首次出现时间|datetime|链上/历史库|missing|
|wallet_age_days|钱包年龄|number|计算|missing|
|wallet_last_active_time|最近活跃时间|datetime|链上/GMGN|missing|
|active_days|活跃天数|number|计算|missing|
|total_token_count|历史交易 token 数|number|GMGN/历史库|missing|
|traded_token_count|交易过的 token 数|number|GMGN|missing|
|current_token_count|当前持有 token 数|number|GMGN/链上|missing|
|tx_count|总交易数|number|链上|missing|
|dex_tx_count|DEX 交易数|number|链上|missing|
|transfer_tx_count|转账次数|number|链上|missing|
|historical_profit_usd|历史盈利|number|GMGN/历史库|missing|
|historical_winrate|历史胜率|number|GMGN/历史库|missing|
|historical_roi|历史 ROI|number|GMGN/历史库|missing|
|gmgn_tags|GMGN 标签|array/string|GMGN|[]|
|is_fresh_wallet|是否新钱包|bool/unknown|GMGN/计算|unknown|
|is_old_wallet|是否老钱包|bool/unknown|GMGN/计算|unknown|
|is_smart_money|是否 smart money 标签|bool|GMGN|false|
|is_whale|是否 whale 标签|bool|GMGN|false|
|is_sniper|是否 sniper 标签|bool|GMGN|false|
|is_bundle|是否 bundle 标签|bool|GMGN|false|
|is_insider|是否 insider 标签|bool|GMGN|false|
|known_cex_wallet|是否已知 CEX 地址|bool|本地库|false|
|known_router_wallet|是否路由地址|bool|本地库|false|
|known_noise_wallet|是否噪音地址|bool|本地库|false|
|wallet_data_quality|钱包数据质量|string|系统计算|poor/partial/usable/good|

注意：

```text
is_fresh_wallet 只能表示数据事实或标签事实。
不能在本阶段推导“疑似结构新钱包”。
```

---

# 12. D组：交易行为字段

输出文件：

```text
normalized/trade_fact_table.csv
```

字段表：

| 字段名                      | 中文含义               | 类型       | 来源         |
| ------------------------ | ------------------ | -------- | ---------- |
| wallet_address           | 钱包地址               | string   | GMGN/链上    |
| token_address            | 代币地址               | string   | 配置         |
| first_buy_time           | 首次买入时间             | datetime | GMGN/链上    |
| first_buy_delay_seconds  | 距 token 创建后的首次买入延迟 | number   | 计算         |
| first_buy_amount_sol     | 首次买入 SOL 数量        | number   | GMGN/链上    |
| first_buy_amount_usd     | 首次买入美元金额           | number   | GMGN/quote |
| total_buy_amount_sol     | 总买入 SOL            | number   | GMGN/链上    |
| total_buy_amount_usd     | 总买入美元              | number   | GMGN/quote |
| total_sell_amount_sol    | 总卖出 SOL            | number   | GMGN/链上    |
| total_sell_amount_usd    | 总卖出美元              | number   | GMGN/quote |
| buy_count                | 买入次数               | number   | GMGN/链上    |
| sell_count               | 卖出次数               | number   | GMGN/链上    |
| avg_buy_price_usd        | 平均买入价格             | number   | 计算         |
| avg_sell_price_usd       | 平均卖出价格             | number   | 计算         |
| realized_profit_usd      | 已实现盈利              | number   | GMGN/计算    |
| unrealized_profit_usd    | 未实现盈利              | number   | GMGN/计算    |
| total_profit_usd         | 总盈利                | number   | GMGN/计算    |
| pnl_multiple             | 盈亏倍数               | number   | GMGN/计算    |
| holding_duration_seconds | 持仓时长               | number   | 计算         |
| is_full_exit             | 是否完全清仓             | bool     | 计算         |
| is_partial_exit          | 是否部分卖出             | bool     | 计算         |
| is_still_holding         | 是否仍在持仓             | bool     | 计算         |
| trade_data_source        | 交易数据来源             | string   | GMGN/chain |
| trade_data_quality       | 交易数据质量             | string   | 系统计算       |

---

# 13. E组：持仓字段

输出文件：

```text
normalized/holder_fact_table.csv
```

字段表：

|字段名|中文含义|类型|来源|
|---|---|---|---|
|wallet_address|钱包地址|string|GMGN/链上|
|token_address|代币地址|string|配置|
|current_token_balance|当前 token 持仓数量|number|GMGN/链上|
|current_token_value_usd|当前持仓价值|number|GMGN/quote|
|holding_ratio_of_supply|占总供应比例|number|计算|
|holding_rank|持仓排名|number|GMGN|
|is_top_holder|是否 Top Holder|bool|GMGN/计算|
|top_holder_rank|Top Holder 排名|number|GMGN|
|holder_snapshot_time|持仓快照时间|datetime|系统|
|holder_data_quality|持仓数据质量|string|系统计算|

---

# 14. F组：转账与资金来源字段

输出文件：

```text
normalized/transfer_fact_table.csv
```

字段表：

|字段名|中文含义|类型|来源|
|---|---|---|---|
|tx_hash|交易哈希|string|链上|
|wallet_address|当前钱包地址|string|链上|
|counterparty_address|对手方地址|string|链上|
|token_address|代币地址|string|链上|
|transfer_asset|转账资产|string|链上|
|transfer_amount|转账数量|number|链上|
|transfer_amount_usd|转账美元价值|number|quote|
|transfer_time|转账时间|datetime|链上|
|transfer_direction|转账方向|string|in/out|
|transfer_type|转账类型|string|token_transfer/sol_funding/usdc_funding/swap_related|
|before_first_buy|是否发生在首次买入前|bool|计算|
|after_sell|是否发生在卖出后|bool|计算|
|source_address|资金来源地址|string|链上|
|possible_cex_source|是否可能来自 CEX|bool|本地库/标签|
|transfer_data_quality|转账数据质量|string|系统计算|

注意：

```text
本阶段只记录“资金来源事实”。
不判断“同源执行组”。
同源执行组判断交给 Phase 03 或专门钱包结构阶段。
```

---

# 15. G组：市场结构字段

输出文件：

```text
normalized/kline_fact_table.csv
```

字段表：

|字段名|中文含义|类型|来源|
|---|---|---|---|
|token_address|代币地址|string|配置|
|timeframe|K线周期|string|GMGN/行情源|
|open_time|开盘时间|datetime|行情源|
|open|开盘价|number|行情源|
|high|最高价|number|行情源|
|low|最低价|number|行情源|
|close|收盘价|number|行情源|
|volume_token|token 成交量|number|行情源|
|volume_usd|美元成交量|number|行情源|
|market_cap_usd|当前市值|number|行情源|
|liquidity_usd|当前流动性|number|行情源|
|trade_count|成交笔数|number|行情源|
|buy_volume_usd|买入成交额|number|行情源|
|sell_volume_usd|卖出成交额|number|行情源|
|kline_data_quality|K线数据质量|string|系统计算|

注意：

```text
本阶段不计算吸筹区间。
不画 Fibonacci。
不判断 AVWAP 支撑。
不判断真假突破。
只保留后续计算需要的 OHLCV 事实。
```

---

# 16. H组：数据质量字段

每个标准化文件都必须包含或关联以下质量字段。

|字段名|中文含义|取值|
|---|---|---|
|data_source|数据来源|gmgn/chain/quote/security/history/manual|
|raw_file_path|原始文件路径|string|
|normalized_file_path|标准化文件路径|string|
|field_missing_count|缺失字段数量|number|
|critical_missing_count|关键字段缺失数量|number|
|duplicate_count|重复记录数量|number|
|invalid_address_count|无效地址数量|number|
|time_conflict_count|时间冲突数量|number|
|amount_conflict_count|金额冲突数量|number|
|quality_score|数据质量分|0-100|
|quality_status|数据质量状态|blocked/poor/partial/usable/good|
|phase_01_gate_status|阶段门禁状态|BLOCK/PAUSE/PASS|
|quality_reason|质量原因|string|

---

# 17. 关键字段缺失规则

## 17.1 致命缺失

以下字段缺失时，Phase 01 必须 `BLOCK`：

```text
token_address
chain
至少一个有效数据源
token 基础信息完全缺失
全部钱包地址无效
交易数据和持仓数据同时缺失
```

---

## 17.2 暂停缺失

以下字段缺失时，Phase 01 输出 `PAUSE`：

```text
token_create_time 缺失
current_market_cap_usd 缺失
first_buy_time 大量缺失
wallet_address 部分无效
GMGN 标签缺失
K线数据缺失
quote 数据缺失
security 数据缺失
```

PAUSE 代表：

```text
可以保留数据
可以生成事实报告
但不能直接进入完整 Phase 02
只能进入低置信度分析或等待补数
```

---

## 17.3 可容忍缺失

以下字段缺失时可 `PASS_WITH_WARNING`：

```text
token_name 缺失
部分 wallet profile 缺失
部分历史胜率缺失
部分 GMGN 标签缺失
部分 transfer 细节缺失
部分 holder rank 缺失
```

---

# 18. 数据质量评分

Phase 01 输出一个 0-100 的数据质量分。

## 18.1 评分结构

```text
数据质量分 = 
基础配置完整度 15分
+ token 信息完整度 15分
+ 钱包数据完整度 15分
+ 交易数据完整度 20分
+ 持仓数据完整度 10分
+ 转账/资金数据完整度 10分
+ K线/市场数据完整度 10分
+ 地址/时间/金额一致性 5分
```

---

## 18.2 质量等级

|分数|状态|含义|
|---|---|---|
|90-100|good|可完整进入下游|
|75-89|usable|可进入下游，但需带 warning|
|60-74|partial|只能做部分分析|
|40-59|poor|不建议进入下游|
|0-39|blocked|阻断|

---

## 18.3 阶段门禁

| 条件                         | phase_01_gate_status |
| -------------------------- | -------------------- |
| quality_score >= 75 且无致命缺失 | PASS                 |
| quality_score 60-74 且无致命缺失 | PASS_WITH_WARNING    |
| quality_score 40-59        | PAUSE                |
| quality_score < 40         | BLOCK                |
| 存在致命缺失                     | BLOCK                |

---

# 19. 输出文件清单

Phase 01 必须输出以下文件。

## 19.1 原始数据文件

```text
raw/raw_gmgn_token.json
raw/raw_gmgn_traders.json
raw/raw_gmgn_holders.json
raw/raw_gmgn_wallet_profiles.json
raw/raw_chain_transfers.json
raw/raw_kline.json
raw/raw_quote.json
raw/raw_security.json
```

如果没有对应数据，也必须生成占位文件：

```json
{
  "status": "missing",
  "reason": "source_not_available",
  "created_at": "2026-05-09T11:23:00+09:00"
}
```

---

## 19.2 标准化事实文件

```text
normalized/token_fact.json
normalized/wallet_fact_table.csv
normalized/trade_fact_table.csv
normalized/holder_fact_table.csv
normalized/transfer_fact_table.csv
normalized/kline_fact_table.csv
normalized/quote_fact.json
normalized/security_fact.json
```

---

## 19.3 审计文件

```text
audit/field_mapping.md
audit/field_quality_report.json
audit/missing_fields_report.csv
audit/anomaly_fields_report.csv
audit/source_coverage_report.md
audit/phase_01_quality_gate.json
```

---

## 19.4 下游交接文件

```text
handoff/phase_01_handoff_to_phase_02.json
handoff/phase_01_handoff_summary.md
```

---

## 19.5 阶段报告

```text
phase_01_data_fact_report.md
```

---

# 20. phase_01_quality_gate.json 标准格式

```json
{
  "run_id": "solana_ABC_xxxx",
  "phase_id": "phase_01",
  "token_address": "token mint address",
  "chain": "solana",
  "quality_score": 82,
  "quality_status": "usable",
  "phase_01_gate_status": "PASS_WITH_WARNING",
  "can_enter_phase_02": true,
  "can_enter_full_scene_recognition": true,
  "can_enter_wallet_structure_analysis": true,
  "can_enter_strategy_gate": false,
  "critical_missing_fields": [],
  "warning_missing_fields": [
    "部分 wallet_first_seen_time 缺失",
    "部分 transfer 来源缺失"
  ],
  "blocked_reasons": [],
  "data_sources_available": [
    "gmgn_token",
    "gmgn_traders",
    "gmgn_holders",
    "kline",
    "quote"
  ],
  "data_sources_missing": [
    "security_scan"
  ],
  "created_at": "2026-05-09T11:23:00+09:00"
}
```

---

# 21. phase_01_handoff_to_phase_02.json 标准格式

```json
{
  "run_id": "solana_ABC_xxxx",
  "from_phase": "phase_01_data_fact_controller",
  "to_phase": "phase_02_multi_model_scene_recognition",
  "token_address": "token mint address",
  "chain": "solana",
  "phase_01_gate_status": "PASS_WITH_WARNING",
  "quality_score": 82,
  "input_files_for_phase_02": {
    "token_fact": "01_data_fact/normalized/token_fact.json",
    "kline_fact_table": "01_data_fact/normalized/kline_fact_table.csv",
    "trade_fact_table": "01_data_fact/normalized/trade_fact_table.csv",
    "holder_fact_table": "01_data_fact/normalized/holder_fact_table.csv",
    "quote_fact": "01_data_fact/normalized/quote_fact.json",
    "security_fact": "01_data_fact/normalized/security_fact.json"
  },
  "allowed_phase_02_models": [
    "吸筹识别",
    "拉升识别",
    "二段扩张识别",
    "高位派发识别",
    "下跌再派发识别",
    "诱多反抽识别",
    "退出流动性陷阱识别",
    "假横盘识别",
    "再吸筹识别",
    "末端拉盘派发识别",
    "刷量假突破识别",
    "接盘鲸鱼陷阱识别"
  ],
  "restricted_models": [
    {
      "model": "安全门禁强判断",
      "reason": "security_scan 缺失"
    }
  ],
  "missing_fields_to_carry_forward": [
    "security_scan",
    "部分 wallet_first_seen_time"
  ],
  "handoff_notes": "数据可进入 Phase 02，但所有涉及安全扫描的判断必须降级为低置信度。"
}
```

---

# 22. field_mapping.md 标准结构

```markdown
# Phase 01 字段映射表

## 1. Token 字段

| SIKK 标准字段 | 中文含义 | 来源字段 | 来源系统 | 单位 | 是否必填 | 缺失处理 |
|---|---|---|---|---|---|---|
| token_address | 代币地址 | mint / address | GMGN/链上 | 无 | 是 | BLOCK |
| token_symbol | 代币符号 | symbol | GMGN | 无 | 否 | UNKNOWN |
| current_market_cap_usd | 当前市值 | market_cap | GMGN/quote | USD | 建议 | missing |

## 2. 钱包字段

| SIKK 标准字段 | 中文含义 | 来源字段 | 来源系统 | 单位 | 是否必填 | 缺失处理 |
|---|---|---|---|---|---|---|

## 3. 交易字段

...

## 4. 持仓字段

...

## 5. 转账字段

...

## 6. K线字段

...

## 7. Quote / Security 字段

...
```

---

# 23. missing_fields_report.csv 字段

```csv
run_id,phase_id,file_name,record_id,field_name,field_chinese_name,missing_level,impact,next_action
```

示例：

```csv
solana_ABC_xxxx,phase_01,wallet_fact_table.csv,8xk2...,wallet_first_seen_time,钱包首次出现时间,warning,钱包年龄无法判断,carry_forward_as_unknown
```

---

# 24. anomaly_fields_report.csv 字段

```csv
run_id,phase_id,file_name,record_id,field_name,field_value,anomaly_type,impact,next_action
```

异常类型包括：

```text
invalid_address
negative_amount
future_time
time_order_conflict
duplicate_record
amount_outlier
source_conflict
empty_required_field
unsupported_chain
```

---

# 25. source_coverage_report.md 标准结构

```markdown
# Phase 01 数据源覆盖报告

## 1. 数据源总览

| 数据源 | 状态 | 记录数 | 覆盖率 | 备注 |
|---|---|---:|---:|---|
| GMGN Token | available | 1 | 100% | 可用 |
| GMGN Traders | available | 328 | 100% | 可用 |
| GMGN Holders | available | 100 | partial | 只返回 Top 100 |
| Chain Transfers | missing | 0 | 0% | 未接入 |
| Kline | available | 500 | 100% | 可用 |
| Quote | available | 1 | 100% | 可用 |
| Security | missing | 0 | 0% | 缺失 |

## 2. 主要缺口

- security_scan 缺失
- chain transfer 缺失
- wallet profile 部分缺失

## 3. 对下游影响

- Phase 02 可以运行，但安全相关判断降级
- Phase 03 钱包同源判断不足
- Phase 05 策略门禁不得给出强通过
```

---

# 26. phase_01_data_fact_report.md 标准结构

```markdown
# Phase 01 数据事实层报告

## 1. 本次运行信息

- run_id:
- token_address:
- token_symbol:
- chain:
- run_mode:
- data_snapshot_time:
- quality_score:
- phase_01_gate_status:

## 2. 数据源覆盖情况

| 数据源 | 状态 | 记录数 | 质量 |
|---|---|---:|---|

## 3. Token 基础事实

| 字段 | 值 |
|---|---|

## 4. 钱包事实概览

| 指标 | 数值 |
|---|---:|
| 钱包总数 | |
| 有效地址数 | |
| 无效地址数 | |
| GMGN 标签地址数 | |
| 新钱包标签数 | |
| whale 标签数 | |
| sniper 标签数 | |
| bundle 标签数 | |

## 5. 交易事实概览

| 指标 | 数值 |
|---|---:|
| 买入地址数 | |
| 卖出地址数 | |
| 完全清仓地址数 | |
| 仍持仓地址数 | |
| 总买入金额 USD | |
| 总卖出金额 USD | |

## 6. 持仓事实概览

| 指标 | 数值 |
|---|---:|
| Holder 数 | |
| Top10 持仓比例 | |
| Top20 持仓比例 | |
| 当前持仓总价值 | |

## 7. K线与市场事实概览

| 指标 | 数值 |
|---|---:|
| 当前价格 | |
| 当前市值 | |
| 当前流动性 | |
| 24h 成交量 | |
| K线数量 | |

## 8. 缺失字段

| 字段 | 缺失等级 | 影响 | 处理方式 |
|---|---|---|---|

## 9. 异常字段

| 字段 | 异常类型 | 影响 | 处理方式 |
|---|---|---|---|

## 10. 下游交接结论

- 是否允许进入 Phase 02:
- 限制条件:
- 必须携带的 warning:
- 不允许越级判断的部分:

## 11. 本阶段结论

本阶段只输出数据事实结论，不输出交易判断。
```

---

# 27. Phase 01 控制流程

```text
Step 1：读取 Phase 00 analysis_config.json
Step 2：创建 run_id 与阶段目录
Step 3：接收 GMGN / 链上 / K线 / quote / security 原始数据
Step 4：写入 raw/ 原始快照
Step 5：建立字段映射
Step 6：统一 token 基础字段
Step 7：统一 wallet 基础字段
Step 8：统一 trade 行为字段
Step 9：统一 holder 持仓字段
Step 10：统一 transfer 资金字段
Step 11：统一 kline 市场字段
Step 12：统一 quote / security 字段
Step 13：执行地址校验、时间校验、金额校验、重复校验
Step 14：生成缺失字段报告
Step 15：生成异常字段报告
Step 16：计算数据质量分
Step 17：生成 phase_01_quality_gate.json
Step 18：生成 handoff_to_phase_02.json
Step 19：生成 phase_01_data_fact_report.md
Step 20：返回 PASS / PASS_WITH_WARNING / PAUSE / BLOCK
```

---

# 28. HER 执行任务模板

可以直接复制给 HER。

```text
任务名称：构建 SIKK Stable Trader OS Phase 01 数据事实层控制器

目标：
在 /root/sikk-gmgn 中创建并完善 Phase 01 数据事实层控制器，用于接收、保留、标准化、审计 GMGN / 链上 / K线 / quote / security / 历史库等输入数据，并输出可供 Phase 02 多模型场景识别读取的标准事实包。

工作范围：
1. 新建或更新文档：
   /root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_data_fact_controller.md

2. 建立推荐目录：
   /root/sikk-gmgn/data/stable_trader_os/runs/<run_id>/01_data_fact/

3. 不要移动或删除旧目录：
   /root/sikk-gmgn/data/gmgn_candidates_live_run/
   该目录作为 legacy_runtime_keep_in_place，只能读取参考，不作为新写入主目录。

4. Phase 01 只负责事实层，不允许输出吸筹、派发、二段扩张、主导侧动机、买点、卖点、策略通过等结论。

必须实现的输出结构：
- raw/
- normalized/
- audit/
- handoff/
- phase_01_data_fact_report.md

必须设计或实现的文件：
- normalized/token_fact.json
- normalized/wallet_fact_table.csv
- normalized/trade_fact_table.csv
- normalized/holder_fact_table.csv
- normalized/transfer_fact_table.csv
- normalized/kline_fact_table.csv
- normalized/quote_fact.json
- normalized/security_fact.json
- audit/field_mapping.md
- audit/field_quality_report.json
- audit/missing_fields_report.csv
- audit/anomaly_fields_report.csv
- audit/source_coverage_report.md
- audit/phase_01_quality_gate.json
- handoff/phase_01_handoff_to_phase_02.json
- handoff/phase_01_handoff_summary.md

验收标准：
1. 所有字段必须有中文解释。
2. 所有金额字段必须标明单位。
3. 所有时间字段必须统一时区。
4. 缺失字段必须标记 missing，不允许编造。
5. 原始数据必须保留在 raw/。
6. 标准化数据必须写入 normalized/。
7. 审计结果必须写入 audit/。
8. 下游交接文件必须写入 handoff/。
9. phase_01_quality_gate.json 必须输出 PASS / PASS_WITH_WARNING / PAUSE / BLOCK。
10. Phase 01 不得输出任何交易建议或主导侧心理判断。
11. 生成一份 phase_01_data_fact_report.md。
12. 添加最少一个样例 token 的 mock 数据测试。
13. 如果已有测试目录，则添加 tests/test_phase_01_data_fact_controller.py。
14. 测试必须覆盖：
    - 缺失字段
    - 无效地址
    - 重复钱包
    - 时间冲突
    - 金额异常
    - quality_score 计算
    - handoff 文件生成

完成后输出：
1. 修改过的文件列表
2. 新增目录列表
3. 样例运行命令
4. 样例输出文件路径
5. 测试结果
6. 尚未实现的缺口
7. 是否允许进入 Phase 02
```

---

# 29. Phase 01 验收清单

|验收项|必须满足|
|---|---|
|目录是否创建|是|
|raw 原始数据是否保留|是|
|normalized 标准化数据是否生成|是|
|audit 审计文件是否生成|是|
|handoff 文件是否生成|是|
|字段是否中文解释|是|
|缺失字段是否标记 missing|是|
|地址是否校验|是|
|时间是否统一|是|
|金额单位是否统一|是|
|是否禁止越级判断|是|
|是否生成 quality gate|是|
|是否可供 Phase 02 读取|是|

---

# 30. 本阶段最重要的硬规则

```text
Phase 01 不解释市场。
Phase 01 不判断机会。
Phase 01 不输出信号。
Phase 01 不判断主导侧。
Phase 01 不判断庄家。
Phase 01 只建立事实。
```

如果 HER 或 AI 在本阶段输出以下内容，视为错误：

```text
当前属于吸筹
当前可以关注买点
疑似庄家开始控盘
主力还没出完
二段扩张概率高
建议等待回踩
可以买
进入 PAPER_READY
```

正确表达应该是：

```text
当前已获得 K线数据 500 条
当前已获得 GMGN trader 数据 328 条
当前 holder 数据仅覆盖 Top 100
security_scan 缺失
wallet_first_seen_time 部分缺失
数据质量分 82
允许进入 Phase 02，但安全相关判断降级
```

---

# 31. 与 Phase 02 的交接边界

Phase 01 给 Phase 02 提供：

```text
token_fact.json
kline_fact_table.csv
trade_fact_table.csv
holder_fact_table.csv
quote_fact.json
security_fact.json
field_quality_report.json
phase_01_quality_gate.json
```

Phase 02 才负责判断：

```text
吸筹
拉升
二段扩张
高位派发
下跌再派发
诱多反抽
退出流动性陷阱
假横盘
再吸筹
末端拉盘派发
刷量假突破
接盘鲸鱼陷阱
```

Phase 01 不能提前做这些判断。

---

# 32. 当前版本尚未解决的问题

Phase 01 v1.0 还需要后续继续补充：

```text
1. GMGN 实际 API / 页面字段与 SIKK 标准字段的逐项映射
2. Solana 链上数据查询源的优先级
3. quote 数据源一致性校验
4. security_scan 的字段标准
5. 历史地址库读取接口
6. mock 数据样例
7. Phase 01 Python 控制器
8. Phase 01 测试文件
9. 与现有 source_wallet_bot 目录的读取兼容
10. 与 legacy gmgn_candidates_live_run 的桥接规则
```

---

# 33. 本次认知升级点

第 1 阶段的核心不是“采集更多数据”，而是建立：

```text
可追溯事实层
可审计字段层
可交接标准层
可阻断质量门禁
```

这一步做好之后，Phase 02 的多模型场景识别才不会变成主观解释。

---

# 34. 尚未解决问题

下一步应该继续设计：

```text
Phase 02：多模型交易场景识别体系
```

但在进入 Phase 02 之前，建议先把 Phase 01 再拆成两个工程文件：

```text
1. phase_01_data_fact_controller.md
2. phase_01_field_schema.md
```

其中：

```text
phase_01_data_fact_controller.md 负责阶段逻辑
phase_01_field_schema.md 负责字段字典
```

这样后面 HER 写代码时不会把阶段逻辑和字段表混在一起。