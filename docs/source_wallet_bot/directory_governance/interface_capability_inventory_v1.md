# Source Wallet Bot 接口能力清单 v1.0

## 0. 定位

本文件是 Source Wallet Bot 在接入 GMGN / OKX / 链上 RPC / 第三方交易平台接口之前的**接口能力审计清单**。

它不是采集脚本，也不是字段标准化脚本。它的作用是先回答：

```text
平台到底能提供什么？
每个接口返回什么字段？
这些字段能支撑 12 类分析问题中的哪些问题？
哪些判断能自动化？哪些只能部分自动化？哪些必须补数据源？哪些暂时不能做？
```

## 1. 总原则

1. 不要马上写采集脚本。
2. 先做接口能力审计，再做字段映射，再做采集器。
3. 每个接口必须回指到 `data_dependency_map_v1.md` 的 12 类分析问题。
4. 每个接口必须声明能提供的字段、不能提供的字段、限制条件和缺失风险。
5. 任何接口只要无法支撑分析问题，就不能因为“看起来有用”而进入首版结构分析合同。
6. 接口能力不足时，结论必须降级，不能用推断补事实。
7. 凭证、API key、私钥、token、cookie 不得写入本文；如发现统一写 `[REDACTED]`。

## 2. 接口审计维度

每个接口至少审计以下字段：

| 审计项 | 说明 |
|---|---|
| 平台 / 数据源 | GMGN / OKX / Solana RPC / Helius / Birdeye / DexScreener / 内部历史库等 |
| 接口名称 | 人类可读名称 |
| endpoint / tool | URL、CLI、SDK 函数或工具名；敏感参数必须省略 |
| 接口类别 | 8 类之一 |
| 支持按 token 查询 | yes / no / partial / unknown |
| 支持按 wallet 查询 | yes / no / partial / unknown |
| 支持历史交易 | yes / no / partial / unknown |
| 支持 holder 快照 | yes / no / partial / unknown |
| 支持资金流 | yes / no / partial / unknown |
| 支持 K线/市值/流动性 | yes / no / partial / unknown |
| 支持分页 | yes / no / partial / unknown |
| 速率限制 | 明确数值；未知写 unknown |
| 时间范围限制 | 可查多久；是否只能近 N 天 |
| 字段缺失风险 | 哪些关键字段可能没有 |
| 原始返回形态 | JSON / CSV / Web table / CLI output / trace event |
| 关键原始字段 | 原始字段名，不提前改名 |
| SIKK 标准字段候选 | 后续可能映射的标准字段 |
| 支撑分析问题 | 12 类问题中的一类或多类 |
| 自动化等级 | full / partial / manual_required / blocked |
| 缺失降级 | 字段不足时最多能输出什么 |
| 验证方式 | 用样例 token / wallet / 时间窗口验证 |

## 3. 8 类接口能力清单

### 3.1 Token 基础信息接口

用途：获取 token 地址、名称、创建时间、市值、流动性、池子、发行/部署相关基础信息。

必须审计：

- 是否支持按 token address 查询。
- 是否返回 token 创建时间或首个池创建时间。
- 是否返回当前市值、流动性、池子地址、交易对。
- 是否返回 mint / deployer / owner / 权限字段。
- 是否区分实时值和历史值。
- 是否能查发现时/买入时/分析时市值。

关键字段候选：

```text
token_address
token_symbol
token_name
chain
mint_time
pool_create_time
pool_address
pair_address
market_cap
liquidity_usd
fdv
price_usd
decimals
owner_authority
mint_authority
freeze_authority
renounced_status
```

支撑分析问题：

- 市值上下文判断
- 主导侧生命周期
- 策略门禁输出
- 安全 / 风险判断

自动化初判：partial。若没有历史市值，只能支撑当前上下文，不能还原发现时/买入时阶段。

### 3.2 交易明细接口

用途：获取买卖记录、成交金额、时间、价格、交易方向、钱包地址、tx hash。

必须审计：

- 是否支持按 token 查询全部交易者。
- 是否支持按 wallet 查询某钱包交易历史。
- 是否返回买入/卖出方向。
- 是否返回交易时间、成交数量、成交金额、成交价格、成交市值。
- 是否支持开盘早期窗口，例如 0-60s、1-5m、5-30m。
- 是否支持分页和时间范围过滤。
- 是否会漏掉 transfer / 非 swap 事件。

关键字段候选：

```text
tx_hash
block_time
wallet_address
token_address
side
amount_token
amount_sol
amount_usd
price_usd
market_cap_at_trade
pool_address
maker_tags
source_platform
```

支撑分析问题：

- 早期钱包识别
- 同步行为识别
- 筹码控制判断
- 对手盘压力判断
- 主导侧生命周期
- 策略门禁输出

自动化初判：full/partial 取决于是否能覆盖完整早期窗口和分页。缺交易时间时不能排序早期钱包。

### 3.3 钱包持仓接口

用途：获取当前持仓、Top Holder、余额、持仓占比、余额变化、holder 快照。

必须审计：

- 是否支持按 token 查询 holders / top holders。
- 是否支持按 wallet 查询当前持仓。
- 是否有 holder rank、holding percentage、value USD。
- 是否支持历史 holder 快照或 holder delta。
- 是否返回 Token 来源 / transfer_in 标记。
- 是否可分页获取前 N 名，例如前 100 / 前 300。

关键字段候选：

```text
wallet_address
token_address
holder_rank
holding_amount
holding_pct
holding_value_usd
balance_change
snapshot_time
is_top_holder
wallet_tag_v2
transfer_in_flag
token_source_type
```

支撑分析问题：

- Top Holder 判断
- 筹码控制判断
- 对手盘压力判断
- 分发路径判断
- 策略门禁输出

自动化初判：partial。只有当前快照不能判断历史变化；缺 holder delta 时生命周期判断必须降级。

### 3.4 钱包画像接口

用途：获取钱包历史行为、胜率、PnL、交易偏好、钱包年龄、标签、部署代币记录。

必须审计：

- 是否支持按 wallet address 查询。
- 是否返回钱包创建时间 / 年龄。
- 是否返回 realized / unrealized PnL、winrate、ROI、交易次数。
- 是否返回历史交易偏好，例如平均买入市值、持仓时长、收益分布。
- 是否返回 GMGN 标签、KOL/Smart/fresh/sniper/bundler 等标签。
- 是否返回部署代币记录。
- 是否有时间范围，例如 7D / 30D / all。

关键字段候选：

```text
wallet_address
wallet_created_time
wallet_age_days
wallet_balance_sol
wallet_balance_usd
realized_profit
unrealized_profit
total_profit
total_roi
winrate
trade_count
avg_buy_market_cap
avg_hold_duration
gmgn_tags
maker_token_tags
is_new_wallet
is_suspicious
has_deployed_tokens
deployed_token_count
```

支撑分析问题：

- 钱包角色分类
- 早期钱包识别
- 对手盘压力判断
- 主导侧生命周期
- 策略门禁输出

自动化初判：partial。钱包画像可增强角色判断，但不能单独确认同源、回流或结构身份。

### 3.5 转账 / 资金流接口

用途：获取资金来源、转移路径、利润回收、Token 分发、SOL/Token 流入流出。

必须审计：

- 是否支持按 wallet 查询转账活动。
- 是否支持按 tx hash 查询 trace。
- 是否支持 token transfer 与 native SOL transfer。
- 是否能识别资金来源地址、入金时间、入金金额。
- 是否能识别卖出后利润是否转走或回流。
- 是否支持多 hop trace。
- 是否能区分 CEX / router / LP / program / 普通钱包。

关键字段候选：

```text
tx_hash
block_time
from_address
to_address
wallet_address
counterparty_address
transfer_type
asset_address
asset_symbol
amount_token
amount_sol
amount_usd
funding_source_address
funding_time
funding_amount
return_flow_address
return_flow_time
return_flow_amount
tx_path
hop_count
entity_type
```

支撑分析问题：

- 同源关系识别
- 资金路径追踪
- 分发路径判断
- 钱包角色分类
- 利润回收 / 核心资金源
- 策略门禁输出

自动化初判：partial/manual_required。多 hop、CEX、router、合约交互会导致路径解释必须降级。

### 3.6 K线 / 价格接口

用途：获取价格结构、市值变化、成交量、流动性变化、阶段位置。

必须审计：

- 是否支持按 token / pool 查询 K线。
- 是否支持 1m / 5m / 15m / 1h 分辨率。
- 是否支持开盘后 0-2h 的完整 1m K线。
- 是否返回 open/high/low/close/volume/amount。
- volume 单位是 USD 还是 token，必须确认。
- 是否有单次返回条数限制，例如 100 根。
- 是否支持 before/after/time range 分页。

关键字段候选：

```text
kline_time
resolution
open
high
low
close
volume_usd
amount_token
market_cap
liquidity_usd
price_change_pct
source
```

支撑分析问题：

- 市值上下文判断
- 主导侧生命周期
- 早期钱包识别
- 对手盘压力判断
- 策略门禁输出

自动化初判：full/partial。若能完整分页覆盖早期窗口，可自动化阶段判断；若只能当前价格，不能做生命周期。

### 3.7 安全 / 风险接口

用途：检查黑名单、貔貅、权限、税费、合约风险、可疑地址、钓鱼风险。

必须审计：

- 是否支持按 token 查询安全项。
- 是否支持按 wallet 查询风险标签。
- 是否返回 mint/freeze 权限、黑名单、税费、honeypot、可暂停交易、可增发等字段。
- 是否返回风险等级和原始规则名。
- 是否能区分 token 风险、钱包风险、交易路径风险。
- 是否有误报说明。

关键字段候选：

```text
token_address
wallet_address
risk_type
risk_level
blacklist_flag
honeypot_flag
mint_authority
freeze_authority
owner_authority
tax_buy
tax_sell
is_suspicious
phishing_risk_check
wash_trader_flag
risk_reason
raw_rule_id
```

支撑分析问题：

- 策略门禁输出
- 钱包角色分类
- 基础设施地址识别
- 对手盘压力判断

自动化初判：partial。风险命中可作为 BLOCK/PAUSE 强证据，但风险未命中不代表安全。

### 3.8 集群 / 关联接口

用途：获取前 300 集群、持仓关联、地址行为关系、同源候选、共同资金源或共同交易模板。

必须审计：

- 是否支持前 100 / 300 holders 或 traders。
- 是否返回 cluster id / group id / related addresses。
- 是否返回共同资金源、共同交易时间、共同 Token 来源。
- 是否返回边关系强度、关系类型、证据来源。
- 是否支持按 token 生成集群。
- 是否支持按 wallet 扩展邻居。
- 是否能导出原始边，而不是只给平台结论。

关键字段候选：

```text
cluster_id
group_id
wallet_address
related_address
relation_type
relation_strength
shared_funding_source
shared_intermediate_node
shared_token_source
same_time_window
same_holder_group
edge_count
first_seen_time
last_seen_time
raw_edge_refs
```

支撑分析问题：

- 同源关系识别
- 同步行为识别
- 筹码控制判断
- 分发路径判断
- Top Holder 判断
- 策略门禁输出

自动化初判：partial。若平台只给 cluster 结论而不给原始边，不能直接强判同源，只能作为候选证据。

## 4. 自动化可行性分级

| 等级 | 含义 | 允许输出 |
|---|---|---|
| full | 接口字段完整、可分页、可覆盖所需时间范围、可复验 | 可自动生成对应事实表和弱结论 |
| partial | 字段部分可得，但缺历史/路径/分页/关键字段 | 只能生成候选或待查结论 |
| manual_required | 需要人工导出、截图、页面确认或二次核验 | 输出人工复查项，不自动判断 |
| blocked | 平台无法提供关键字段，且无替代源 | 该判断暂时不能做 |

## 5. 接口能力 → 12 类问题覆盖矩阵

| 分析问题 | 必需接口能力 | 缺口时降级 |
|---|---|---|
| 早期钱包识别 | 交易明细 + K线/价格 + 钱包持仓 | 缺交易时间不能排序；缺 K线只做时间窗口，不做阶段 |
| 钱包角色分类 | 钱包画像 + 交易明细 + 转账/资金流 + 持仓 | 缺资金流只做交易行为角色候选 |
| 同源关系识别 | 转账/资金流 + 集群/关联 + 交易明细 | 缺资金边不得强判同源 |
| 同步行为识别 | 交易明细 + 转账/资金流 + 集群/关联 | 只有时间接近则写同步候选 |
| 筹码控制判断 | 钱包持仓 + 交易明细 + holder delta + K线 | 缺 holder delta 不判断控筹变化 |
| 资金路径追踪 | 转账/资金流 + 钱包画像 + 内部历史库 | 缺多 hop 只能一跳待查 |
| Top Holder 判断 | 钱包持仓 + Top Holder 快照 + 交易明细 | 缺快照时间写大户状态待查 |
| 分发路径判断 | 转账/资金流 + 钱包持仓 + 交易明细 | 只看到接收无卖出，写分发接收候选 |
| 对手盘压力判断 | 交易明细 + 钱包持仓 + K线/价格 + 钱包画像 | 缺收益/持仓时写压力待查 |
| 主导侧生命周期 | K线/价格 + 交易明细 + 持仓变化 | 缺 K线或 holder delta 不输出生命周期 |
| 市值上下文判断 | Token 基础信息 + K线/价格 + 交易明细 | 缺历史市值只写当前上下文 |
| 策略门禁输出 | 以上事实层 + 安全/风险 + 字段缺失报告 | 证据不足默认 PAUSE / DATA_BACKFILL |

## 6. 接口审计输出模板

每个待接入平台必须生成一个审计记录：

```yaml
platform:
interface_name:
endpoint_or_tool:
interface_category:
supports_token_query:
supports_wallet_query:
supports_historical_trades:
supports_holder_snapshot:
supports_fund_flow:
supports_kline_marketcap_liquidity:
supports_pagination:
rate_limit:
time_range_limit:
known_missing_fields:
raw_response_shape:
raw_fields:
sikk_field_candidates:
supports_analysis_questions:
automation_level:
degradation_when_missing:
verification_sample:
verification_status:
notes:
```

## 7. 完成后才能进入下一步

接口能力清单完成后，才能进入：

1. 字段映射更新。
2. 原始数据落盘 schema。
3. 采集脚本设计。
4. API wrapper 编写。
5. 自动化判断或门禁接入。

完成前禁止：

- 直接写采集脚本。
- 直接按接口返回字段设计结论。
- 直接把平台标签当 SIKK 角色。
- 直接把缺字段补成推断。

## 8. 本阶段最终产物

接口能力审计完成后，Hermes 必须能回答：

- 哪些判断可以自动化。
- 哪些判断只能部分自动化。
- 哪些判断需要其他数据源补充。
- 哪些判断暂时不能做。
- 哪些接口只适合原始证据保存，不适合直接出结论。
