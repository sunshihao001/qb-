# SIKK wallet_structure_normalized 合约文档

## 0. 文档目的

本文档定义 SIKK-SOL v2.0 中 `wallet_structure_normalized.json` 的标准合约。

`wallet_structure_normalized.json` 是 GMGN 钱包 / holder / trade / cluster 等原始接口进入 SIKK 钱包结构分析层前的唯一标准化事实产物。

当前阶段只定义方法与字段合约，不写代码。

---

## 1. 定位

`wallet_structure_normalized.json` 位于以下链路中：

```text
GMGN 钱包 / holder / trade / cluster 接口
  ↓
wallet_source_adapter
  ↓
wallet_structure_normalized.json
  ↓
钱包实体画像
  ↓
当前 token 钱包行为分析
  ↓
同源关系 / 资金路径 / 筹码迁移分析
  ↓
历史地址画像
  ↓
wallet_structure_decision.json
  ↓
final_trade_gate
  ↓
state_machine
```

它是事实标准化层，不是门禁层，不是评分层，不是状态机输入层。

---

## 2. 设计原则

### 2.1 事实优先

normalized 只表达从 GMGN 或其他明确钱包事实源得到的钱包事实。

允许来源：

- GMGN wallet
- GMGN holder
- GMGN trade / trader
- GMGN cluster
- 后续明确接入的钱包事实源

禁止来源：

- dashboard
- paper runner
- report
- case file
- state_machine
- final_trade_gate

### 2.2 不反推

不能从展示层、复盘层、paper 层反推出钱包事实。

例如：

- 不能因为 dashboard 显示某 token 已进入观察，就反推钱包支持。
- 不能因为 paper runner 记录了入场，就反推钱包首次买入时间。
- 不能因为 report 写了风险，就反推 GMGN cluster 风险字段。

### 2.3 原始字段不可直连状态机

GMGN 原始钱包字段必须先进入 `wallet_source_adapter`，再进入 normalized 合约。状态机不得读取 GMGN 原始钱包字段。

### 2.4 缺失不编造

字段缺失时：

- 时间字段填 `null`。
- 数值字段填 `null`，除非字段语义明确允许 `0`。
- 枚举字段填 `UNKNOWN` 或 `MISSING`。
- `fallback_used=true` 时必须说明 fallback 来源。

### 2.5 normalized 不裁决交易

`wallet_structure_normalized.json` 不输出：

- `PAPER_READY`
- `BLOCKED`
- 买入
- 卖出
- 真实交易执行
- hard gate

---

## 3. 推荐文件位置

单 token normalized：

```text
data/gmgn_candidates_live_run/wallet_normalized/<token_address>/wallet_structure_normalized.json
```

可选质量报告：

```text
data/gmgn_candidates_live_run/wallet_normalized/<token_address>/wallet_normalized_quality_report.json
```

可选 adapter 日志：

```text
data/gmgn_candidates_live_run/wallet_sources/<token_address>/wallet_source_adapter_log.json
```

---

## 4. 顶层结构

推荐 JSON 顶层结构：

```json
{
  "schema_version": "sikk_wallet_structure_normalized_v2.0",
  "token_address": "",
  "snapshot_time": "",
  "source_name": "gmgn",
  "retrieved_at": "",
  "normalized_at": "",
  "fallback_used": false,
  "fallback_reason": "",
  "data_quality": {
    "status": "OK",
    "score": 100,
    "missing_fields": [],
    "source_files": [],
    "raw_field_refs": []
  },
  "wallets": []
}
```

说明：

- `wallets[]` 中每一项代表一个钱包在当前 token 快照下的标准化事实。
- 顶层 `snapshot_time` 是本批钱包事实快照时间。
- 行级钱包可有自己的 `snapshot_time`，用于多源字段不完全同步的情况。

---

## 5. wallet_structure_normalized 必须字段

每个 `wallets[]` item 必须包含以下字段。

### 5.1 身份字段

#### token_address

- 中文名：代币地址
- 类型：string
- 必填：是
- 来源优先级：运行参数 / GMGN token context / holder/trade response
- 缺失处理：整行无效，写入质量报告
- 说明：当前钱包事实所属 token。

#### wallet_address

- 中文名：钱包地址
- 类型：string
- 必填：是
- 来源优先级：GMGN holder address / trader address / wallet address
- 缺失处理：整行无效，写入质量报告
- 说明：当前被分析钱包。

### 5.2 时间字段

#### snapshot_time

- 中文名：快照时间
- 类型：ISO8601 string 或 null
- 必填：是
- 来源优先级：GMGN 返回快照时间 / provider response timestamp / retrieved_at fallback
- 缺失处理：无 provider 时间时可用 `retrieved_at` fallback，并标记 `fallback_used=true`
- 说明：该钱包事实对应的数据快照时间。

#### first_buy_time

- 中文名：首次买入时间
- 类型：ISO8601 string 或 null
- 必填：是，可为 null
- 来源优先级：GMGN trader first buy time / trade list first buy event
- 缺失处理：null，不得从 paper entry 或 dashboard 时间反推
- 说明：该钱包在当前 token 的首次主动买入时间。

#### last_sell_time

- 中文名：最后卖出时间
- 类型：ISO8601 string 或 null
- 必填：是，可为 null
- 来源优先级：GMGN trader last sell time / trade list latest sell event
- 缺失处理：null
- 说明：该钱包在当前 token 的最后一次主动卖出时间。

### 5.3 持仓与结果字段

#### holding_amount

- 中文名：当前持仓数量
- 类型：number 或 null
- 必填：是，可为 null
- 来源优先级：GMGN holder amount / wallet token balance
- 缺失处理：null
- 说明：当前 token 持仓数量。

#### holding_pct

- 中文名：当前持仓占比
- 类型：number 或 null
- 单位：百分比，0-100
- 必填：是，可为 null
- 来源优先级：GMGN holder percentage / calculated amount over supply
- 缺失处理：null
- 说明：当前钱包持仓占 token 总量比例。

#### sold_pct

- 中文名：已卖出比例
- 类型：number 或 null
- 单位：百分比，0-100
- 必填：是，可为 null
- 来源优先级：GMGN trader sold percentage / sell amount over acquired amount
- 缺失处理：null
- 说明：该钱包在当前 token 中已卖出比例。

#### roi

- 中文名：收益倍数 / ROI
- 类型：number 或 null
- 必填：是，可为 null
- 来源优先级：GMGN trader ROI / realized + unrealized return ratio
- 缺失处理：null
- 说明：当前 token 维度的钱包 ROI。

#### pnl

- 中文名：盈亏金额
- 类型：number 或 null
- 单位：优先 USD；如来源为 SOL，应在 `pnl_currency` 扩展字段说明
- 必填：是，可为 null
- 来源优先级：GMGN PnL / realized + unrealized pnl
- 缺失处理：null
- 说明：当前 token 维度的钱包盈亏。

### 5.4 交易行为字段

#### trade_count

- 中文名：交易次数
- 类型：integer 或 null
- 必填：是，可为 null
- 来源优先级：GMGN trader trade count / buy_count + sell_count
- 缺失处理：null
- 说明：该钱包当前 token 相关交易次数。

#### holder_rank

- 中文名：Holder 排名
- 类型：integer 或 null
- 必填：是，可为 null
- 来源优先级：GMGN holder rank / top holder list index
- 缺失处理：null
- 说明：该钱包在 holder 列表中的排名。

### 5.5 关系字段

#### funding_source_address

- 中文名：资金来源地址
- 类型：string 或 null
- 必填：是，可为 null
- 来源优先级：GMGN funding source / on-chain funding adapter
- 缺失处理：null，不能强判同源
- 说明：该钱包买入前或活动前的资金来源地址。

#### cluster_id

- 中文名：GMGN 集群编号
- 类型：string 或 null
- 必填：是，可为 null
- 来源优先级：GMGN cluster id / holder cluster id
- 缺失处理：null
- 说明：GMGN 或 holder cluster 维度的集群标识。

#### same_source_group_id

- 中文名：SIKK 同源候选组编号
- 类型：string 或 null
- 必填：是，可为 null
- 来源优先级：wallet_source_adapter 初步归并 / 后续 same source analyzer
- 缺失处理：null
- 说明：SIKK 内部同源候选组编号，不等同于确认同一个人。

### 5.6 来源与标准化字段

#### source_name

- 中文名：来源名称
- 类型：string
- 必填：是
- 推荐值：`gmgn_wallet`、`gmgn_holder`、`gmgn_trade`、`gmgn_cluster`、`gmgn_mixed`
- 缺失处理：`UNKNOWN_SOURCE`
- 说明：该行事实主要来源。

#### retrieved_at

- 中文名：拉取时间
- 类型：ISO8601 string
- 必填：是
- 来源优先级：wallet_source_adapter 拉取时间
- 缺失处理：当前 adapter 时间，但必须标记 adapter 生成
- 说明：系统从来源接口取得数据的时间。

#### normalized_at

- 中文名：标准化时间
- 类型：ISO8601 string
- 必填：是
- 来源优先级：wallet_source_adapter 标准化产物生成时间
- 缺失处理：不可缺失
- 说明：该 normalized 行生成时间。

#### fallback_used

- 中文名：是否使用 fallback
- 类型：boolean
- 必填：是
- 来源优先级：adapter 生成
- 缺失处理：默认 false
- 说明：是否有字段使用 fallback；若 true，应在扩展字段写 `fallback_fields` 与 `fallback_reason`。

---

## 6. 推荐扩展字段

为了后续钱包画像与门禁稳定，建议保留以下扩展字段：

```text
wallet_tags
maker_token_tags
is_new_wallet
is_suspicious
is_transfer_in
buy_amount_usd
sell_amount_usd
realized_pnl
unrealized_pnl
pnl_currency
buy_count
sell_count
avg_buy_market_cap_usd
avg_sell_market_cap_usd
token_source_type
raw_unit_refs
raw_field_refs
missing_fields
fallback_fields
data_quality_score
```

这些字段不属于用户当前指定的最小必填字段，但建议 normalized 阶段保留，方便后续钱包实体画像、同源关系、资金路径和门禁证据追溯。

---

## 7. wallet_structure_decision 合约

`wallet_structure_decision.json` 是 normalized 之后的钱包门禁标准输出。

推荐位置：

```text
data/gmgn_candidates_live_run/wallet_structure/<token_address>/wallet_structure_decision.json
```

### 7.1 必须字段

#### wallet_structure_status

- 中文名：钱包结构状态
- 类型：string enum
- 推荐值：
  - `WALLET_SUPPORT`
  - `WALLET_OBSERVE`
  - `WALLET_PAUSE`
  - `WALLET_RISK`
  - `WALLET_BLOCK_CANDIDATE`
  - `WALLET_UNKNOWN`
  - `WALLET_DATA_QUALITY_FAIL`
- 说明：钱包结构层状态，不等于状态机状态。

#### wallet_structure_score

- 中文名：钱包结构评分
- 类型：number
- 范围：0-100
- 说明：结构支持强度。

#### wallet_risk_score

- 中文名：钱包风险评分
- 类型：number
- 范围：0-100
- 说明：钱包层风险强度。

#### counterparty_pressure_score

- 中文名：对手盘压力评分
- 类型：number
- 范围：0-100
- 说明：晚买、套牢、承接、卖压等对手盘压力。

#### data_quality_score

- 中文名：数据质量评分
- 类型：number
- 范围：0-100
- 说明：钱包数据完整性与新鲜度。

#### same_source_sync_buy_score

- 中文名：同源同步买入评分
- 类型：number
- 范围：0-100
- 说明：同源候选组同步买入强度。

#### same_source_sync_sell_score

- 中文名：同源同步卖出评分
- 类型：number
- 范围：0-100
- 说明：同源候选组同步卖出或派发强度。

#### dominant_side_status

- 中文名：主导侧状态
- 类型：string enum
- 推荐值：
  - `STRUCTURE_SIDE_HOLDING`
  - `STRUCTURE_SIDE_ACCUMULATING`
  - `STRUCTURE_SIDE_DISTRIBUTING`
  - `COUNTERPARTY_ABSORBING`
  - `DOMINANT_SIDE_UNKNOWN`
- 说明：钱包结构视角下主导侧筹码状态。

#### chip_transfer_status

- 中文名：筹码迁移状态
- 类型：string enum
- 推荐值：
  - `NO_MAJOR_TRANSFER`
  - `ACCUMULATION_TO_STRUCTURE_SIDE`
  - `PARTIAL_DISTRIBUTION`
  - `DISTRIBUTION_TO_COUNTERPARTY`
  - `CHIP_TRANSFER_UNKNOWN`
- 说明：筹码从结构侧向对手盘迁移或反向吸筹的状态。

#### wallet_pattern_alignment

- 中文名：钱包与盘型一致性
- 类型：string enum
- 推荐值：
  - `ALIGNED`
  - `PARTIAL_ALIGNED`
  - `CONFLICT`
  - `UNKNOWN`
- 说明：钱包行为与盘型 / lifecycle 是否一致。

#### decision_action

- 中文名：钱包门禁动作
- 类型：string enum
- 推荐值：
  - `SUPPORT_FINAL_GATE`
  - `OBSERVE_ONLY`
  - `PAUSE_FOR_REFRESH`
  - `RISK_REVIEW`
  - `DATA_QUALITY_REVIEW`
  - `NO_DECISION`
- 说明：只给 final gate 使用，不直接进入状态机。

#### reason

- 中文名：原因
- 类型：string
- 说明：中文证据摘要，必须说明主要证据与缺失项。

#### evidence_level

- 中文名：证据等级
- 类型：string enum
- 推荐值：`E0`、`E1`、`E2`、`E3`、`E4`、`E5`
- 说明：钱包结构证据等级。

#### created_at

- 中文名：决策生成时间
- 类型：ISO8601 string
- 说明：wallet_structure_decision 生成时间。

#### wallet_snapshot_time

- 中文名：钱包快照时间
- 类型：ISO8601 string 或 null
- 说明：该决策对应的 normalized / wallet snapshot 时间。

#### expires_at

- 中文名：过期时间
- 类型：ISO8601 string 或 null
- 说明：钱包结构决策失效时间；过期后 final gate 应刷新或降级，而不是直接交易。

---

## 8. decision 与状态机的边界

`wallet_structure_decision.json` 不能直接：

- 改状态机。
- 进入 `PAPER_READY`。
- 触发 `BLOCKED`。
- 发起 paper 开仓。
- 发起 paper 平仓。
- 发起真实买入。
- 发起真实卖出。

它只能被 `final_trade_gate` 综合消费。

---

## 9. fallback 规则

### 9.1 允许 fallback 的场景

允许：

- provider 没有 `snapshot_time`，使用 `retrieved_at` 作为 snapshot fallback。
- holder 接口没有 `trade_count`，用 trade 接口的 buy/sell count 合并。
- holder 接口没有 `holding_pct`，在有供应量时由 amount / supply 计算。

### 9.2 禁止 fallback 的场景

禁止：

- 用 dashboard 时间反推 `first_buy_time`。
- 用 paper entry 时间反推 `first_buy_time`。
- 用 report 生成时间反推 `snapshot_time`。
- 用 case file 文本反推 `funding_source_address`。
- 用状态机状态反推 `wallet_structure_status`。

### 9.3 fallback 标记

当任意字段 fallback 时：

```json
{
  "fallback_used": true,
  "fallback_fields": ["snapshot_time"],
  "fallback_reason": "provider_snapshot_time_missing_use_retrieved_at"
}
```

---

## 10. 数据质量规则

### 10.1 行级质量

每个钱包行建议输出：

```json
{
  "data_quality_score": 85,
  "missing_fields": ["funding_source_address"],
  "raw_unit_refs": ["gmgn_holder_raw.json:holders[0]"],
  "raw_field_refs": ["holders[0].address", "holders[0].amount"]
}
```

### 10.2 token 级质量

token 级质量报告建议包含：

- 钱包总数
- 可用钱包数
- 缺 `first_buy_time` 数
- 缺 `holding_pct` 数
- 缺 `funding_source_address` 数
- 缺 `cluster_id` 数
- fallback 使用数
- 来源接口成功 / 失败 / 超时情况

### 10.3 缺失字段处理原则

缺失字段不能导致系统静默通过。

应当进入：

- normalized quality report
- wallet decision reason
- final gate data quality check
- failure_attribution，如后续失败与钱包数据缺失相关

---

## 11. normalized 示例

```json
{
  "schema_version": "sikk_wallet_structure_normalized_v2.0",
  "token_address": "Token111111111111111111111111111111111111111",
  "snapshot_time": "2026-05-04T12:00:00Z",
  "source_name": "gmgn_mixed",
  "retrieved_at": "2026-05-04T12:00:03Z",
  "normalized_at": "2026-05-04T12:00:04Z",
  "fallback_used": false,
  "fallback_reason": "",
  "data_quality": {
    "status": "OK",
    "score": 92,
    "missing_fields": [],
    "source_files": [
      "gmgn_holder_raw.json",
      "gmgn_trade_raw.json",
      "gmgn_cluster_raw.json"
    ],
    "raw_field_refs": [
      "holders[0].address",
      "traders[0].first_buy_time",
      "clusters[0].cluster_id"
    ]
  },
  "wallets": [
    {
      "token_address": "Token111111111111111111111111111111111111111",
      "wallet_address": "Wallet11111111111111111111111111111111111111",
      "snapshot_time": "2026-05-04T12:00:00Z",
      "first_buy_time": "2026-05-04T11:42:10Z",
      "last_sell_time": null,
      "holding_amount": 1200000.0,
      "holding_pct": 2.4,
      "sold_pct": 0.0,
      "roi": 1.8,
      "pnl": 4200.0,
      "trade_count": 3,
      "holder_rank": 8,
      "funding_source_address": null,
      "cluster_id": "GMGN_CLUSTER_001",
      "same_source_group_id": "SIKK_SAME_SOURCE_20260504_001",
      "source_name": "gmgn_mixed",
      "retrieved_at": "2026-05-04T12:00:03Z",
      "normalized_at": "2026-05-04T12:00:04Z",
      "fallback_used": false,
      "wallet_tags": ["fresh_wallet", "sniper"],
      "maker_token_tags": ["top_holder"],
      "raw_unit_refs": ["gmgn_holder_raw.json:holders[0]"],
      "missing_fields": ["funding_source_address"]
    }
  ]
}
```

---

## 12. wallet_structure_decision 示例

```json
{
  "schema_version": "sikk_wallet_structure_decision_v2.0",
  "token_address": "Token111111111111111111111111111111111111111",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 76,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 22,
  "data_quality_score": 92,
  "same_source_sync_buy_score": 68,
  "same_source_sync_sell_score": 12,
  "dominant_side_status": "STRUCTURE_SIDE_HOLDING",
  "chip_transfer_status": "NO_MAJOR_TRANSFER",
  "wallet_pattern_alignment": "ALIGNED",
  "decision_action": "SUPPORT_FINAL_GATE",
  "reason": "早期钱包持仓稳定，同源同步买入分较高，同步卖出压力低；资金来源缺失，证据等级不提升到 E5。",
  "evidence_level": "E3",
  "created_at": "2026-05-04T12:02:00Z",
  "wallet_snapshot_time": "2026-05-04T12:00:00Z",
  "expires_at": "2026-05-04T12:17:00Z"
}
```

---

## 13. 与 final_trade_gate 的消费关系

`final_trade_gate` 读取 `wallet_structure_decision.json` 时，只应读取标准字段，不读取 GMGN 原始字段。

建议消费方式：

```text
wallet_structure_status + decision_action + scores + evidence_level + created_at/expires_at
```

final gate 应自行判断：

- 是否过期
- 数据质量是否不足
- 是否与 pattern / lifecycle / quote/security 冲突
- 是否只能 observe
- 是否需要 refresh

---

## 14. 后续推进顺序

按用户指定顺序推进：

1. 建立 wallet normalized 合约。
2. 建立 wallet_source_adapter。
3. 迁移旧钱包结构分析逻辑读取 normalized。
4. 输出 wallet_structure_decision。
5. final_trade_gate 读取 wallet_structure_decision。
6. 状态机只读 final gate。
7. paper runner 记录钱包字段。
8. failure_attribution 统计钱包结构失败原因。

---

## 15. 当前禁止事项清单

- 不直接改状态机。
- 不直接进入 `PAPER_READY`。
- 不直接触发 `BLOCKED`。
- 不从 dashboard / paper / report / case file 反推钱包事实。
- 不修改实盘逻辑。
- 不开启 hard gate。
- 不读取私钥。
- 不签名。
- 不广播。
- 不让状态机直接读取 GMGN 原始钱包字段。
- 不让钱包结构系统直接决定交易。

---

## 16. 验收标准

本文档阶段的验收标准：

- 明确 `wallet_structure_normalized.json` 是钱包事实标准化层。
- 明确 normalized 必须字段。
- 明确 `wallet_structure_decision.json` 必须字段。
- 明确 fallback 与缺失字段处理规则。
- 明确禁止从 dashboard / paper / report / case file 反推钱包事实。
- 明确状态机只能通过 final gate 间接消费钱包结构结论。
- 明确当前只做方法文档，不写代码。
