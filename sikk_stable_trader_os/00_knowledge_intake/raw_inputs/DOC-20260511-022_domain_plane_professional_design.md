# Domain Plane：领域平面专业化设计

## 0. 核心定位

**Domain Plane 不是策略说明，也不是数据采集层。**

它是整个 SIKK Stable Trader OS 的**领域语义总控层**，负责把“交易世界里的概念、对象、状态、场景、风险、证据、反证、推理边界”定义成系统可以稳定理解和调用的结构。

简单说：

> **Governance Plane 决定系统能不能做。**  
> **Domain Plane 决定系统到底在判断什么。**  
> **Data Plane 决定系统用什么数据判断。**  
> **Strategy / Gate Plane 决定是否允许进入交易候选。**

---

# 1. Domain Plane 的阶段目标

## 1.1 总目标

建立一套专业化、轻量机构级别的**交易领域模型**，让 HER / SIKK 系统在后续执行时不会把不同概念混在一起。

它要解决的问题是：

|问题|Domain Plane 的职责|
|---|---|
|什么是“结构机会”？|定义机会不是上涨，而是“风险被连续否定后仍保留的高质量结构样本”|
|什么是“主导侧”？|定义为证据推断对象，而不是直接声称知道庄家|
|什么是“吸筹 / 控盘 / 派发 / 再吸筹”？|建立统一生命周期与场景分类|
|钱包结构和 K 线结构如何对齐？|定义领域对象之间的关系|
|什么证据可以支持判断？|定义证据等级、字段来源、反证机制|
|什么情况下必须否决？|定义领域级硬否定规则|
|系统什么时候不能推理？|定义未知、缺失、不足、冲突状态|
|后续阶段怎么调用？|输出标准合约和领域词典|

---

# 2. Domain Plane 在总体系中的位置

```text
P00 Bootstrap Control Plane
    ↓
P01 Governance Plane
    ↓
P02 Domain Plane
    ↓
P03 Data Plane
    ↓
P04 Evidence Plane
    ↓
P05 Scenario Recognition Plane
    ↓
P06 Strategy Gate Plane
    ↓
P07 Execution Risk Plane
    ↓
P08 Review / Replay Plane
    ↓
P09 Self-Upgrade Plane
```

Domain Plane 是 P02，不应该跳过。

如果没有 Domain Plane，后面会出现严重问题：

```text
数据很多，但不知道哪些字段真正支持判断
规则很多，但不知道每条规则属于哪个领域对象
场景很多，但定义互相重叠
钱包分析和 K 线分析各说各话
AI 可以解释，但解释没有稳定边界
系统会把“像机会”误判成“可参与”
```

---

# 3. Domain Plane 的专业化定义

## 3.1 标准定义

```text
Domain Plane 是 SIKK Stable Trader OS 的领域语义建模层。

它负责定义系统研究对象、领域实体、行为事件、生命周期状态、交易场景、风险类型、证据类型、反证类型、领域规则、推理边界、状态迁移语义和下游交接合约。

它不直接采集数据，不直接生成交易信号，不直接执行交易。

它的核心价值是把混乱的交易经验、盘口语言、钱包行为、K 线结构、风险判断和复盘经验，转化为 HER 可调用、可检查、可审计、可复盘的领域模型。
```

---

# 4. Domain Plane 必须包含的数据

## 4.1 阶段身份证数据

文件建议：

```text
/root/sikk-gmgn/system/domain_plane/domain_plane.yaml
```

核心字段：

```yaml
plane_id: P02_DOMAIN_PLANE
plane_name: 领域平面
plane_level: light_institutional
version: v1.0
status: DRAFT_READY_FOR_AUDIT

mission:
  primary: 建立 SIKK Stable Trader OS 的领域语义、对象、场景、状态、风险和证据模型
  secondary:
    - 统一钱包结构、K线结构、市值上下文、主导侧生命周期、策略门禁之间的概念边界
    - 为 Data Plane 提供字段需求
    - 为 Evidence Plane 提供证据分类
    - 为 Scenario Plane 提供场景分类基础
    - 为 Strategy Gate Plane 提供可否决、可暂停、可观察、可进入的领域语义

authority:
  can_define:
    - 领域对象
    - 领域状态
    - 领域事件
    - 场景类型
    - 生命周期类型
    - 钱包角色类型
    - 风险类型
    - 证据等级
    - 反证类型
    - 推理边界
  cannot_do:
    - 直接采集链上数据
    - 直接下交易结论
    - 直接生成买入信号
    - 直接修改执行层
    - 用缺失数据强行推断

upstream_planes:
  - P00_BOOTSTRAP_CONTROL_PLANE
  - P01_GOVERNANCE_PLANE

downstream_planes:
  - P03_DATA_PLANE
  - P04_EVIDENCE_PLANE
  - P05_SCENARIO_RECOGNITION_PLANE
  - P06_STRATEGY_GATE_PLANE

acceptance_status_codes:
  - DOMAIN_READY
  - DOMAIN_READY_WITH_GAPS
  - DOMAIN_REJECTED
  - DOMAIN_NEEDS_DATA_BACKFILL
  - DOMAIN_CONFLICT_DETECTED
```

---

# 5. Domain Plane 的核心领域对象

## 5.1 一级领域对象

|领域对象|中文定义|系统用途|
|---|---|---|
|代币对象|当前被分析的交易标的|所有判断的根对象|
|钱包对象|单个链上地址或归并实体|判断结构资金行为|
|钱包群组对象|疑似同源、协同、资金关联、执行关联的钱包集合|判断主导侧、对手盘、派发路径|
|主导侧对象|疑似掌握筹码控制权的一方，不等同于真实庄家|生命周期与意图推断|
|对手盘对象|接收筹码、追涨、承接、被动流动性一方|判断派发风险|
|筹码对象|代币持仓、迁移、集中、分散、清仓、再吸筹状态|判断控制权|
|市值对象|从发现到当前的市值变化上下文|判断早期、追高、退出流动性|
|价格结构对象|K 线、趋势、箱体、突破、回踩、失败结构|场景识别|
|成交结构对象|成交量、换手、刷量、放量、缩量、异常成交|判断真实推进与假动作|
|流动性对象|池子、深度、滑点、可成交性|风控和执行前置|
|安全对象|合约、权限、黑名单、税、冻结、钓鱼风险|硬门禁|
|场景对象|当前代币所处的结构场景|策略适配|
|证据对象|支撑判断的数据来源与可信度|可审计推理|
|反证对象|否定当前假设的证据|防止解释污染|
|状态对象|系统内部对代币的处理状态|状态机调用|
|复盘对象|历史运行与结果反馈|自我升级|

---

## 5.2 领域对象关系图

```text
代币对象
 ├── 钱包对象
 │    ├── 钱包角色
 │    ├── 资金来源
 │    ├── 持仓行为
 │    ├── 盈亏表现
 │    └── 历史复现
 │
 ├── 钱包群组对象
 │    ├── 同源执行组
 │    ├── 分发接收组
 │    ├── 利润回收组
 │    ├── 对手盘鲸鱼组
 │    └── 疑似主导侧组
 │
 ├── 筹码对象
 │    ├── 集中度
 │    ├── 迁移路径
 │    ├── 留存率
 │    ├── 清仓率
 │    └── 派发进度
 │
 ├── 市值对象
 │    ├── 发现市值
 │    ├── 钱包判断时市值
 │    ├── 信号市值
 │    ├── 入场市值
 │    └── 当前市值
 │
 ├── 价格结构对象
 │    ├── 箱体
 │    ├── 突破
 │    ├── 回踩
 │    ├── 失败测试
 │    ├── 二段扩张
 │    └── 下跌派发
 │
 ├── 成交结构对象
 │    ├── 放量推进
 │    ├── 缩量回踩
 │    ├── 刷量异常
 │    ├── 换手异常
 │    └── 成交疲劳
 │
 ├── 场景对象
 │    ├── 吸筹
 │    ├── 控盘箱体
 │    ├── 一段拉升
 │    ├── 二段扩张
 │    ├── 高位派发
 │    ├── 下跌派发
 │    ├── 流动性陷阱
 │    └── 再激活
 │
 └── 证据 / 反证 / 状态 / 复盘对象
```

---

# 6. 钱包角色领域模型

Domain Plane 必须提前定义钱包角色，否则 Data Plane 不知道要采集什么字段。

## 6.1 核心钱包角色分类

|钱包角色|定义|典型证据|风险含义|
|---|---|---|---|
|新钱包狙击者|开盘早期买入、历史记录少、资金来源集中|开盘早期成交、低历史交互、同源资金|可能是结构资金，也可能是机器人|
|早期结构钱包|低位或开盘早期持续吸筹，未完全清仓|早买、持仓留存、分批行为、未同步退出|支持主导侧未完全派发|
|同源执行钱包|多个钱包资金来源、时间、行为高度同步|同资金源、同步买卖、相似持仓路径|若同步卖出，是强风险|
|主控筹码候选|持仓集中、早期参与、对价格推进有影响|大额持仓、关键位置不清仓、配合 K 线|支持筹码控制权判断|
|分发接收钱包|在拉升或高位承接筹码|高位接收、持仓转移、亏损承接|可能是对手盘|
|利润回收钱包|结构资金把利润转移到该地址|卖出后资金归集|说明派发路径形成|
|接盘鲸鱼|高位大额买入，来源非结构侧|高市值进入、大额承接、无早期成本|可能提供退出流动性|
|历史复现钱包|曾在多个类似代币中出现|地址历史库匹配|提高结构可信度|
|噪音交易钱包|小额、随机、无结构关联|无同步、无资金路径、无复现|降低权重|
|可疑刷量钱包|高频小额、对敲、成交制造|高频、低净变化、时间密集|否定成交真实性|

---

## 6.2 钱包角色输出字段

```yaml
wallet_role_model:
  wallet_address: string
  entity_id: string | null
  wallet_role_primary: enum
  wallet_role_secondary: list
  role_confidence: 0.0-1.0
  evidence_level: A|B|C|D|UNKNOWN
  funding_source_type: enum
  token_source_type: enum
  first_seen_time: datetime
  first_buy_time: datetime
  first_buy_market_cap_usd: number
  current_holding_pct: number
  realized_profit_usd: number
  unrealized_profit_usd: number
  holding_duration_seconds: number
  sync_group_id: string | null
  same_source_group_id: string | null
  distribution_path_id: string | null
  risk_tags: list
  supporting_evidence_ids: list
  counter_evidence_ids: list
  current_action_label: enum
```

---

# 7. 主导侧生命周期领域模型

## 7.1 为什么必须有生命周期模型

SIKK 系统不能只判断：

```text
有没有早期钱包
有没有突破
有没有放量
```

专业判断必须回答：

```text
主导侧现在处于哪个生命周期？
筹码控制权是否还在结构侧？
派发是否已经完成？
当前上涨是推进、诱多、反抽，还是退出流动性？
```

---

## 7.2 生命周期状态表

|生命周期状态|定义|关键证据|系统倾向|
|---|---|---|---|
|早期吸筹|开盘或低位阶段结构钱包持续积累|早买、未清仓、低市值、筹码集中|观察，不直接交易|
|控盘箱体|价格横盘压缩，筹码未明显派发|箱体、低波动、结构钱包留存|等待突破与回踩|
|一段扩张|主导侧第一次推动价格|放量突破、早期钱包未同步退出|可进入候选|
|部分派发|一部分早期资金卖出，但结构未完全崩|部分清仓、承接存在、价格未崩|降权观察|
|再吸筹|派发后重新积累|回落不破、重新买入、对手盘减少|观察或二次候选|
|二段扩张|长箱体或再吸筹后再次推进|AVWAP/POC 收复、放量、钱包留存|高价值候选|
|主动派发|结构侧持续卖出，价格仍被维持|高位转移、接盘鲸鱼、同步卖|风险升高|
|下跌派发|下跌中反抽出货|反抽放量、卖压持续、承接变弱|阻断|
|流动性陷阱|制造反弹吸引接盘|反抽无结构支持、对手盘承接|阻断|
|崩塌退出|结构侧失去控制或完成退出|跌破关键结构、同步清仓|硬阻断|
|死亡横盘|低活跃、无推进、无再吸筹|成交枯竭、无钱包动作|移除观察|
|再激活|老币重新出现资金结构|历史钱包回归、放量、结构收复|重新建档|

---

# 8. 场景识别领域模型

## 8.1 场景不是策略

Domain Plane 只定义场景。

是否交易，要交给 Strategy Gate Plane。

---

## 8.2 核心场景分类

|场景编号|场景名称|领域定义|主要判断问题|
|---|---|---|---|
|S01|开盘吸筹|开盘后结构钱包逐步拿货|是否存在真实结构资金？|
|S02|控盘箱体|价格压缩、筹码集中、波动降低|是否仍在控盘？|
|S03|箱体突破|从控制区放量突破|是真实推进还是假突破？|
|S04|突破回踩完成|回踩关键结构后重新走强|是否形成可执行候选？|
|S05|二段扩张|第一轮后未完全派发，再次推动|是否有剩余派发动机？|
|S06|高位派发|涨幅较大后结构资金逐步转移|是否正在给别人接盘？|
|S07|下跌派发|下跌中通过反抽继续卖出|反抽是机会还是陷阱？|
|S08|诱多反抽|弱反弹制造流动性|是否缺乏结构钱包支持？|
|S09|接盘鲸鱼陷阱|高位大钱包承接但非结构侧|是否变成退出流动性？|
|S10|刷量假突破|成交放大但无真实筹码变化|成交是否可信？|
|S11|假横盘|看似箱体，实际筹码流失|是否控盘已经消失？|
|S12|再吸筹|派发后重新低位吸筹|是否出现新结构周期？|
|S13|老币再激活|历史代币重新放量|是再激活还是骗流动性？|
|S14|崩塌后反抽|大跌后快速反弹|是修复还是二次派发？|

---

# 9. 证据等级模型

## 9.1 证据等级

|等级|定义|是否可用于强判断|
|---|---|---|
|A 级证据|多源一致、字段完整、时间对齐、可复盘|可以|
|B 级证据|单源强证据或多源弱一致|可以辅助|
|C 级证据|有迹象但缺字段或缺时间对齐|仅观察|
|D 级证据|噪音、解释空间大、不可复验|不可用于决策|
|UNKNOWN|数据缺失或无法判断|必须标记未知|

---

## 9.2 证据对象字段

```yaml
evidence_object:
  evidence_id: string
  evidence_type: enum
  source_module: string
  source_file: string
  source_field: string
  observed_value: any
  observed_time: datetime
  related_entity_id: string
  related_domain_object: enum
  supports_hypothesis: list
  contradicts_hypothesis: list
  evidence_level: A|B|C|D|UNKNOWN
  confidence_score: 0.0-1.0
  freshness_status: FRESH|STALE|EXPIRED|UNKNOWN
  replay_available: boolean
```

---

# 10. 反证模型

Domain Plane 必须定义反证，否则 AI 会不断为错误机会找理由。

## 10.1 反证类型

|反证类型|含义|处理|
|---|---|---|
|钱包同步退出|同源或结构钱包集中卖出|硬否决|
|早期钱包清仓|关键早期筹码完全离场|强降权或阻断|
|接盘鲸鱼高位承接|高位大额买入但非结构侧|派发风险|
|市值过度扩张|从发现到当前涨幅过大|追高风险|
|成交量失真|高频小额刷量或对敲|否定成交推进|
|价格跌破结构|跌破 POC / AVWAP / 箱体低点|阻断或回退|
|回踩超时|回踩结构长期无推进|疲劳降级|
|二次下探失败缺失|没有完成有效失败测试|不允许执行|
|数据缺失|关键字段无来源|禁止强判断|
|证据冲突|钱包支持但成交反证，或反之|进入待审状态|

---

# 11. 领域级硬否定规则

这些不是策略规则，而是领域语义上的“禁止解释污染”。

```yaml
domain_hard_negative_rules:
  - rule_id: DHN_001
    name: 同源执行组同步退出
    condition: same_source_group_sync_sell_score >= high_threshold
    result: DOMAIN_BLOCK
    reason: 结构侧存在同步退出，不能解释为健康换手

  - rule_id: DHN_002
    name: 关键早期钱包集中清仓
    condition: early_structural_wallet_remaining_pct <= critical_threshold
    result: DOMAIN_BLOCK
    reason: 早期结构筹码控制权显著消失

  - rule_id: DHN_003
    name: 高位接盘鲸鱼成为主要承接方
    condition: counterparty_whale_absorption_score >= high_threshold
    result: DOMAIN_PAUSE_OR_BLOCK
    reason: 当前价格可能主要依赖对手盘承接

  - rule_id: DHN_004
    name: 刷量假突破
    condition: volume_expansion == true and real_chip_transfer_support == false
    result: DOMAIN_REJECT_BREAKOUT
    reason: 成交结构缺少真实筹码支持

  - rule_id: DHN_005
    name: 回踩完成证据不足
    condition: avwap_acceptance == true and failure_test_confirmed == false and adx_noise_rejection == false
    result: DOMAIN_TRANSITION_ONLY
    reason: 不能把未完成回踩解释为完成结构

  - rule_id: DHN_006
    name: 关键字段缺失仍试图强判断
    condition: required_evidence_missing == true and decision_strength in [STRONG_ALLOW, BUY_READY]
    result: DOMAIN_REJECTED
    reason: 数据不足不能强推理
```

---

# 12. 市值上下文领域模型

## 12.1 为什么 Domain Plane 必须定义市值上下文

同一个钱包行为，在不同市值阶段含义完全不同。

例如：

```text
早期钱包在 80K 市值买入，300K 市值仍持有：
可能支持结构侧未完全派发。

早期钱包在 80K 买入，3M 市值大量转移给接盘鲸鱼：
更可能是派发进度较高。

用户在 3M 市值才看到信号：
可能已经不是机会，而是退出流动性。
```

---

## 12.2 市值上下文字段

```yaml
market_cap_context:
  discovery_market_cap_usd: number
  current_market_cap_usd: number
  market_cap_change_from_discovery_pct: number
  market_cap_at_wallet_decision_usd: number
  market_cap_at_signal_usd: number
  market_cap_at_paper_entry_usd: number
  market_cap_stage_label:
    - EARLY
    - MID_EXPANSION
    - LATE_EXPANSION
    - HIGH_RISK_CHASING
    - EXIT_LIQUIDITY_ZONE
    - UNKNOWN
  market_cap_context_status:
    - SUPPORTS_EARLY_STRUCTURE
    - NEUTRAL
    - WARNING_LATE_ENTRY
    - BLOCK_EXIT_LIQUIDITY_RISK
    - UNKNOWN
```

---

# 13. 领域状态模型

Domain Plane 应该定义状态含义，状态机阶段再调用。

## 13.1 领域状态

|状态|含义|
|---|---|
|DOMAIN_UNINITIALIZED|尚未建立领域对象|
|DOMAIN_CONTEXT_READY|领域上下文已建立|
|DOMAIN_DATA_REQUIREMENT_READY|已生成数据需求|
|DOMAIN_EVIDENCE_PENDING|等待证据填充|
|DOMAIN_SCENARIO_CANDIDATE|具备场景候选|
|DOMAIN_CONFLICT_DETECTED|证据冲突|
|DOMAIN_SUPPORT|领域层支持继续分析|
|DOMAIN_PAUSE|领域层要求暂停|
|DOMAIN_BLOCK|领域层阻断|
|DOMAIN_UNKNOWN|无法判断|
|DOMAIN_READY_FOR_HANDOFF|可交给下游平面|

---

# 14. 领域推理边界

这一部分非常关键。

## 14.1 允许推理

系统允许说：

```text
根据早期钱包留存、同源组未同步退出、价格结构仍在箱体上方、成交未出现明显刷量反证，当前更接近“控盘箱体后等待二段扩张”的候选状态。
```

## 14.2 禁止推理

系统禁止说：

```text
庄家一定还在。
庄家一定要拉。
这个币一定二段。
早期钱包没卖，所以可以买。
成交放量，所以突破成功。
```

## 14.3 标准表达

应该统一使用：

```text
疑似主导侧
结构侧
筹码控制权可能仍部分保留
派发进度尚未完成
二段扩张假设成立但需要回踩完成证据
当前存在对手盘承接风险
证据不足，禁止强判断
```

---

# 15. Domain Plane 对 Data Plane 的字段需求

Domain Plane 必须向 Data Plane 输出字段需求，否则数据采集会失焦。

## 15.1 钱包字段需求

```yaml
required_wallet_fields:
  - wallet_address
  - first_buy_time
  - first_buy_price
  - first_buy_market_cap_usd
  - first_buy_amount
  - total_buy_amount
  - total_sell_amount
  - current_holding_amount
  - current_holding_pct
  - realized_profit
  - unrealized_profit
  - funding_source_address
  - funding_source_type
  - token_source
  - wallet_age
  - transaction_count
  - historical_token_count
  - historical_win_rate
  - sync_buy_group_id
  - sync_sell_group_id
  - same_source_group_id
  - distribution_path_id
```

---

## 15.2 K 线与成交字段需求

```yaml
required_market_structure_fields:
  - open_time
  - current_time
  - candle_interval
  - open
  - high
  - low
  - close
  - volume
  - turnover
  - buy_volume
  - sell_volume
  - volume_delta
  - price_change_pct
  - box_high
  - box_low
  - box_mid
  - breakout_status
  - pullback_status
  - failure_test_status
  - avwap_status
  - poc_status
  - obv_status
  - cmf_status
  - ao_status
  - adx_noise_rejection_status
```

---

## 15.3 市值与流动性字段需求

```yaml
required_market_cap_liquidity_fields:
  - discovery_market_cap_usd
  - current_market_cap_usd
  - market_cap_change_from_discovery_pct
  - liquidity_usd
  - liquidity_change_pct
  - pool_age_seconds
  - holder_count
  - top_holder_pct
  - top_10_holder_pct
  - buy_sell_ratio
  - slippage_estimate
  - quote_source
  - quote_deviation_pct
```

---

# 16. Domain Plane 输出合约

建议文件：

```text
/root/sikk-gmgn/system/domain_plane/contracts/domain_handoff_contract.yaml
```

核心结构：

```yaml
domain_handoff_packet:
  packet_id: string
  token_address: string
  generated_at: datetime
  domain_plane_version: string

  domain_context:
    token_lifecycle_hypothesis: enum
    primary_scenario_candidate: enum
    secondary_scenario_candidates: list
    dominant_side_status: enum
    chip_control_status: enum
    counterparty_pressure_status: enum
    market_cap_context_status: enum

  domain_objects:
    wallet_roles_defined: boolean
    wallet_groups_defined: boolean
    chip_structure_defined: boolean
    market_structure_defined: boolean
    evidence_model_defined: boolean

  evidence_requirements:
    required_fields: list
    missing_fields: list
    critical_missing_fields: list

  hard_negative_screen:
    triggered_rules: list
    blocked: boolean
    pause_required: boolean

  reasoning_boundary:
    allowed_claims: list
    forbidden_claims: list
    uncertainty_tags: list

  downstream_instruction:
    next_plane: P03_DATA_PLANE
    allowed_next_actions:
      - DATA_REQUIREMENT_GENERATION
      - EVIDENCE_COLLECTION
      - SCENARIO_PRECHECK
    forbidden_next_actions:
      - DIRECT_BUY_SIGNAL
      - EXECUTION_DECISION
      - UNVERIFIED_STRONG_CLAIM
```

---

# 17. Domain Plane 文件体系

建议目录：

```text
/root/sikk-gmgn/system/domain_plane/
```

建议文件：

```text
domain_plane.yaml
domain_context.md
domain_object_model.yaml
domain_wallet_role_taxonomy.yaml
domain_lifecycle_model.yaml
domain_scenario_taxonomy.yaml
domain_evidence_model.yaml
domain_counter_evidence_model.yaml
domain_hard_negative_rules.yaml
domain_market_cap_context_model.yaml
domain_reasoning_boundary.md
domain_data_requirement_map.yaml
domain_handoff_contract.yaml
domain_acceptance_criteria.md
domain_gap_register.md
domain_review_checklist.md
```

---

# 18. 每个文件的作用

|文件|作用|
|---|---|
|domain_plane.yaml|阶段身份证，定义权限、边界、上下游|
|domain_context.md|给 HER 读取的领域上下文压缩包|
|domain_object_model.yaml|领域实体对象表|
|domain_wallet_role_taxonomy.yaml|钱包角色分类|
|domain_lifecycle_model.yaml|主导侧生命周期模型|
|domain_scenario_taxonomy.yaml|场景分类模型|
|domain_evidence_model.yaml|证据等级与证据对象|
|domain_counter_evidence_model.yaml|反证模型|
|domain_hard_negative_rules.yaml|领域级硬否定规则|
|domain_market_cap_context_model.yaml|市值上下文模型|
|domain_reasoning_boundary.md|允许与禁止推理边界|
|domain_data_requirement_map.yaml|领域对象 → 数据字段需求|
|domain_handoff_contract.yaml|下游交接包格式|
|domain_acceptance_criteria.md|验收标准|
|domain_gap_register.md|缺口登记|
|domain_review_checklist.md|审计清单|

---

# 19. 专业化验收标准

## 19.1 DOMAIN_READY

必须同时满足：

```text
1. 领域对象已完整定义
2. 钱包角色分类已定义
3. 主导侧生命周期已定义
4. 场景分类已定义
5. 证据等级已定义
6. 反证模型已定义
7. 硬否定规则已定义
8. 市值上下文已定义
9. 推理边界已定义
10. Data Plane 字段需求已输出
11. 下游 handoff 合约已生成
12. 缺口已登记
13. HER 可读取 domain_context.md
14. 不存在“直接生成买入信号”的越权逻辑
```

---

## 19.2 DOMAIN_READY_WITH_GAPS

允许进入下一阶段，但必须标记缺口：

```text
1. 场景模型已完成，但部分阈值待 Data Plane 回填
2. 钱包角色已定义，但历史地址库未完善
3. 生命周期模型已定义，但 replay 样本不足
4. 反证模型已定义，但部分字段来源未落实
5. 市值上下文字段已定义，但发现市值数据不稳定
```

---

## 19.3 DOMAIN_REJECTED

以下情况必须驳回：

```text
1. 把 Domain Plane 写成普通说明文档
2. 直接输出交易信号
3. 没有定义证据和反证
4. 没有定义推理边界
5. 钱包角色、场景、生命周期混在一起
6. 没有下游字段需求
7. 没有验收门
8. 没有缺口登记
9. 没有状态码
10. 无法被 HER 调度读取
```

---

# 20. 当前是否达到专业化轻量机构水准？

## 20.1 判断

按你现在的认知要求，Domain Plane 要达到的是：

```text
不是“写得详细”
而是“后续所有阶段都能围绕它稳定运行”
```

如果按上面的结构落地，标准可以达到：

```text
轻量机构级 v1.0 合格
```

但还不是完整机构级 v2.0。

原因是：

|层级|当前设计状态|
|---|---|
|领域对象|已能完整覆盖|
|生命周期|已具备专业判断框架|
|场景分类|已覆盖主要交易结构|
|钱包角色|已具备结构分析基础|
|证据链|已达到可审计要求|
|反证机制|已达到风险优先要求|
|量化阈值|仍需 Data Plane 和 Replay Plane 校准|
|历史样本库|仍需后续补充|
|自动状态迁移|需要后续 State Machine 接入|
|真实执行安全|不属于 Domain Plane，后续处理|

结论：

```text
Domain Plane 现在可以作为专业化系统建设的 P02 阶段基准版本。
它的目标不是完成交易系统，而是让后续 Data、Evidence、Scenario、Strategy 不再概念混乱。
```

---

# 21. 给 HER 的可执行任务书

下面这段可以直接复制给 HER。

```text
任务名称：建立 P02 Domain Plane｜领域平面专业化阶段数据包

任务目标：
在 /root/sikk-gmgn/system/domain_plane/ 下建立 SIKK Stable Trader OS 的 P02 Domain Plane 领域平面。该阶段不是普通说明文档，而是一个可调度的阶段运行单元，负责定义系统的领域对象、钱包角色、主导侧生命周期、场景分类、证据模型、反证模型、硬否定规则、市值上下文、推理边界、数据需求和下游交接合约。

执行原则：
1. 不允许直接生成交易信号。
2. 不允许直接写执行层逻辑。
3. 不允许把“疑似主导侧”写成确定庄家。
4. 不允许在关键字段缺失时输出强判断。
5. 所有判断都必须有字段来源、证据等级、反证记录和不确定性标签。
6. 该阶段输出必须服务于后续 Data Plane、Evidence Plane、Scenario Plane、Strategy Gate Plane。
7. 所有核心术语使用中文。
8. 文件必须结构化，可被 HER 后续读取和调用。

需要创建目录：
/root/sikk-gmgn/system/domain_plane/

需要创建文件：
1. domain_plane.yaml
2. domain_context.md
3. domain_object_model.yaml
4. domain_wallet_role_taxonomy.yaml
5. domain_lifecycle_model.yaml
6. domain_scenario_taxonomy.yaml
7. domain_evidence_model.yaml
8. domain_counter_evidence_model.yaml
9. domain_hard_negative_rules.yaml
10. domain_market_cap_context_model.yaml
11. domain_reasoning_boundary.md
12. domain_data_requirement_map.yaml
13. domain_handoff_contract.yaml
14. domain_acceptance_criteria.md
15. domain_gap_register.md
16. domain_review_checklist.md

每个文件要求：

domain_plane.yaml：
定义阶段 ID、阶段名称、版本、权限边界、上下游平面、可定义内容、禁止内容、状态码和验收状态。

domain_context.md：
写成 HER 运行前必须读取的领域上下文压缩包，说明 Domain Plane 的作用、边界、目标、核心语义和禁止事项。

domain_object_model.yaml：
定义代币对象、钱包对象、钱包群组对象、主导侧对象、对手盘对象、筹码对象、市值对象、价格结构对象、成交结构对象、流动性对象、安全对象、场景对象、证据对象、反证对象、状态对象、复盘对象。

domain_wallet_role_taxonomy.yaml：
定义新钱包狙击者、早期结构钱包、同源执行钱包、主控筹码候选、分发接收钱包、利润回收钱包、接盘鲸鱼、历史复现钱包、噪音交易钱包、可疑刷量钱包。每类必须包含定义、支持证据、反证、风险含义、所需字段、输出字段。

domain_lifecycle_model.yaml：
定义早期吸筹、控盘箱体、一段扩张、部分派发、再吸筹、二段扩张、主动派发、下跌派发、流动性陷阱、崩塌退出、死亡横盘、再激活。每个状态必须包含进入条件、退出条件、支持证据、反证、下游倾向。

domain_scenario_taxonomy.yaml：
定义开盘吸筹、控盘箱体、箱体突破、突破回踩完成、二段扩张、高位派发、下跌派发、诱多反抽、接盘鲸鱼陷阱、刷量假突破、假横盘、再吸筹、老币再激活、崩塌后反抽。每个场景必须包含定义、数据需求、支持证据、反证、禁止误判、下游状态建议。

domain_evidence_model.yaml：
定义证据等级 A/B/C/D/UNKNOWN，证据对象字段，证据来源，证据新鲜度，证据可复盘性，证据冲突处理。

domain_counter_evidence_model.yaml：
定义钱包同步退出、早期钱包清仓、接盘鲸鱼高位承接、市值过度扩张、成交量失真、价格跌破结构、回踩超时、二次下探失败缺失、数据缺失、证据冲突等反证类型。

domain_hard_negative_rules.yaml：
定义领域级硬否定规则，包括同源执行组同步退出、关键早期钱包集中清仓、高位接盘鲸鱼成为主要承接方、刷量假突破、回踩完成证据不足、关键字段缺失仍试图强判断。

domain_market_cap_context_model.yaml：
定义 discovery_market_cap_usd、current_market_cap_usd、market_cap_change_from_discovery_pct、market_cap_at_wallet_decision_usd、market_cap_at_signal_usd、market_cap_at_paper_entry_usd、market_cap_stage_label、market_cap_context_status。

domain_reasoning_boundary.md：
写清楚允许表达、禁止表达、标准表达。禁止说“庄家一定还在”“一定会拉”“可以买”。必须使用“疑似主导侧”“结构侧”“筹码控制权可能仍部分保留”“派发进度尚未完成”“证据不足，禁止强判断”等表达。

domain_data_requirement_map.yaml：
把每个领域对象映射到 Data Plane 必须采集的字段。必须包括钱包字段、K线字段、成交字段、市值字段、流动性字段、安全字段、历史地址字段。

domain_handoff_contract.yaml：
定义 domain_handoff_packet，包括 packet_id、token_address、generated_at、domain_context、domain_objects、evidence_requirements、hard_negative_screen、reasoning_boundary、downstream_instruction。

domain_acceptance_criteria.md：
定义 DOMAIN_READY、DOMAIN_READY_WITH_GAPS、DOMAIN_REJECTED 三类验收结果。每一类必须有明确条件。

domain_gap_register.md：
登记当前无法完全解决的问题，包括阈值缺失、历史样本不足、字段来源未确认、钱包归因误差、刷量识别误差、主导侧推断不确定性。

domain_review_checklist.md：
建立审计清单，用于检查该阶段是否只是说明文档，是否缺少证据模型，是否缺少反证模型，是否越权生成交易信号，是否没有下游字段需求，是否没有 HER 可调用合约。

验收命令：
完成后输出：
1. 文件创建清单
2. 每个文件的核心内容摘要
3. DOMAIN_READY / DOMAIN_READY_WITH_GAPS / DOMAIN_REJECTED 判断
4. 缺口清单
5. 下一阶段 P03 Data Plane 的字段需求摘要
6. 是否存在越权逻辑
7. 是否可以交接到 Data Plane

最终验收标准：
只有当领域对象、钱包角色、生命周期、场景、证据、反证、硬否定规则、市值上下文、推理边界、字段需求、handoff 合约、验收标准、缺口登记全部存在时，才允许标记为 DOMAIN_READY。
```

---

# 22. 下一步应该做什么

Domain Plane 完成后，下一步不是直接写策略，而是进入：

```text
P03 Data Plane：数据平面
```

P03 的目标是把 Domain Plane 提出的字段需求落地成：

```text
数据源清单
字段字典
采集路径
标准化格式
缺失字段处理
字段质量评分
数据新鲜度判断
字段到证据的映射
```

顺序应该是：

```text
P02 Domain Plane 完成
    ↓
P02 阶段审计
    ↓
DOMAIN_READY / DOMAIN_READY_WITH_GAPS
    ↓
P03 Data Plane 字段建模
    ↓
P03 数据采集与标准化合约
    ↓
P04 Evidence Plane 证据链生成
```

---

# 本次认知升级点

1. **Domain Plane 不是文档，是领域语义运行单元。**  
    它要让 HER 知道系统到底在判断什么，而不是让 AI 自由解释。
    
2. **交易系统专业化的关键不是规则多，而是概念边界稳定。**  
    钱包角色、主导侧生命周期、场景、证据、反证、状态必须分开。
    
3. **Domain Plane 不负责买卖，只负责定义“什么叫有效判断”。**  
    是否买入是 Strategy Gate Plane 的职责。
    
4. **反证模型必须和证据模型同级。**  
    没有反证，AI 会把任何结构解释成机会。
    
5. **市值上下文必须进入领域模型。**  
    同样的钱包行为，在早期和高位含义完全不同。
    
6. **HER 要先读取领域上下文，再执行后续任务。**  
    不能依靠对话上下文临时理解。
    

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|钱包角色阈值还未量化|已定义分类，未定义精确阈值|P03 / P04 / Replay 补充|
|主导侧生命周期需要样本校准|模型已建立，样本不足|P08 复盘层校准|
|刷量识别规则还需要真实数据验证|逻辑已定义，字段待落实|Data Plane 补字段|
|市值阶段边界未完全确定|字段已定义，阈值待回测|Replay Plane 统计|
|同源钱包归因存在误差|已定义不确定性|Evidence Plane 设置置信度|
|二段扩张与诱多反抽容易混淆|场景已拆分|Scenario Plane 深化|
|Domain Plane 与 Strategy Gate 的边界需后续强制校验|已定义禁止越权|Governance Plane 增加审计门|