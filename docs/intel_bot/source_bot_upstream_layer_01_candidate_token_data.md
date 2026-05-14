# Source Bot 上游数据源分层：第 1 类候选与基础代币数据

## 定位

第 1 类数据只负责回答：

- token 是什么时候出现的
- 系统是什么时候发现它的
- 当前快照来自哪个候选批次和哪个上游来源
- 当前基础市场状态是什么
- 后续钱包证据包应该挂在哪个时间锚点下

它不负责判断：

- 主导侧动机
- 对手盘压力
- 派发是否完成
- 是否确定庄家
- 是否进入交易

## 必须采集字段

### 代币身份字段

- `token_address`
- `token_symbol`
- `chain`
- `pool_address`

### 时间锚点字段

- `token_open_time`
- `pool_created_at`
- `discovered_at`
- `first_seen_at`
- `last_seen_at`
- `candidate_snapshot_at`

### 候选批次字段

- `candidate_batch_id`
- `candidate_source`

### 市场基础字段

- `market_cap_usd`
- `liquidity_usd`
- `holder_count`
- `volume_1m`
- `volume_5m`
- `volume_15m`
- `price_usd`

## 字段来源

- GMGN 新币池
- GMGN token info
- GMGN pool info
- OKX / GMGN market data
- 本地 `first_seen_registry`

## 必须输出

- `candidates_normalized.json`
- `token_market_snapshot.json`
- `token_first_seen_registry.json`

## 标准化输出约束

### `candidates_normalized.json`

用途：候选列表标准化后的入口文件。每一行必须是一个标准 token candidate object。

每个对象至少包含：

```json
{
  "token_address": "",
  "token_symbol": "",
  "chain": "sol",
  "pool_address": "",
  "token_open_time": "",
  "pool_created_at": "",
  "discovered_at": "",
  "first_seen_at": "",
  "last_seen_at": "",
  "candidate_snapshot_at": "",
  "candidate_batch_id": "",
  "candidate_source": "",
  "market_cap_usd": 0,
  "liquidity_usd": 0,
  "holder_count": 0,
  "volume_1m": 0,
  "volume_5m": 0,
  "volume_15m": 0,
  "price_usd": 0,
  "source_trace": {
    "gmgn_new_pool": "",
    "gmgn_token_info": "",
    "gmgn_pool_info": "",
    "okx_or_gmgn_market_data": "",
    "first_seen_registry": ""
  },
  "field_quality": {
    "missing_required_fields": [],
    "time_anchor_status": "",
    "market_snapshot_status": ""
  }
}
```

### `token_market_snapshot.json`

用途：保存当前市场快照，不参与交易裁决。

必须包含：

```json
{
  "generated_at": "",
  "candidate_batch_id": "",
  "tokens": [
    {
      "token_address": "",
      "token_symbol": "",
      "chain": "sol",
      "pool_address": "",
      "snapshot_at": "",
      "market_cap_usd": 0,
      "liquidity_usd": 0,
      "holder_count": 0,
      "volume_1m": 0,
      "volume_5m": 0,
      "volume_15m": 0,
      "price_usd": 0,
      "source": ""
    }
  ]
}
```

### `token_first_seen_registry.json`

用途：维护本地 first seen 时间，不允许每轮覆盖首次发现时间。

必须包含：

```json
{
  "tokens": {
    "<token_address>": {
      "token_address": "",
      "token_symbol": "",
      "chain": "sol",
      "pool_address": "",
      "token_open_time": "",
      "pool_created_at": "",
      "first_seen_at": "",
      "last_seen_at": "",
      "first_candidate_batch_id": "",
      "last_candidate_batch_id": "",
      "first_candidate_source": "",
      "last_candidate_source": ""
    }
  }
}
```

## 质量规则

- `first_seen_at` 一旦写入，不允许被后续刷新覆盖。
- `last_seen_at` 每次候选刷新都可以更新。
- `candidate_snapshot_at` 必须等于本轮候选快照生成时间。
- `candidate_batch_id` 必须能唯一标识本轮候选采集批次。
- `token_open_time` 与 `pool_created_at` 如果缺失，必须在 `field_quality.missing_required_fields` 中标记。
- `market_cap_usd / liquidity_usd / holder_count / volume_* / price_usd` 不能臆造；源数据缺失时填 `0` 并记录缺失。
- `source_trace` 必须保留字段来自哪个上游或本地 registry。

## 给钱包证据包的交接字段

后续钱包证据包必须继承以下字段作为时间与来源上下文：

- `token_address`
- `token_symbol`
- `chain`
- `pool_address`
- `token_open_time`
- `pool_created_at`
- `discovered_at`
- `first_seen_at`
- `candidate_snapshot_at`
- `candidate_batch_id`
- `candidate_source`

## 当前代码映射

当前已有基础：

- `sikk_gmgn_new_token_filter.py`
  - 已有 `token_open_time`
  - 已有 `pool_created_at`
  - 已有 `discovered_at`
  - 已有 `first_seen_at`
  - 已有 `last_seen_at`
  - 已有 `candidate_snapshot_at`
  - 已有 `candidate_batch_id`
  - 已有 `candidate_source`
  - 已有本地 `time_context/token_first_seen_registry.json`

需要补强：

- 输出 `candidates_normalized.json`
- 输出 `token_market_snapshot.json`
- 将 registry 结构标准化为 `tokens` 包裹格式
- 明确补齐 `pool_address / holder_count / volume_1m / volume_5m / volume_15m / price_usd`
- 为每个字段补 `source_trace` 与 `field_quality`
