# Source Bot 上游数据源分层：第 3 类 Holder 快照数据

## 定位

第 3 类数据负责把 GMGN holder、链上 holder snapshot、KryptoGO / cluster source 等来源整理成 Holder 快照与钱包结构事实层。

用途：

- 判断筹码集中度
- 观察 Top Holder
- 估算结构侧剩余筹码
- 观察筹码是否转移

它不负责：

- 直接判断主导侧动机
- 直接判断对手盘压力
- 直接判断派发是否完成
- 输出确定庄家
- 触发交易

## 必须采集字段

- `token_address`
- `snapshot_time`
- `holder_rank`
- `wallet_address`
- `holding_amount`
- `holding_pct`
- `holding_value_usd`
- `top10_holder_pct`
- `top20_holder_pct`
- `holder_count`
- `holder_delta`

## 数据来源

- GMGN holder
- 链上 holder snapshot
- KryptoGO / cluster source 如可用

## 必须输出

- `holder_snapshot_normalized.json`
- `wallet_structure_normalized.json`

## `holder_snapshot_normalized.json` 标准结构

每一行代表一个 holder 快照记录。

```json
{
  "token_address": "",
  "snapshot_time": "",
  "holder_rank": 1,
  "wallet_address": "",
  "holding_amount": 0,
  "holding_pct": 0,
  "holding_value_usd": 0,
  "top10_holder_pct": 0,
  "top20_holder_pct": 0,
  "holder_count": 0,
  "holder_delta": 0,
  "source_trace": {
    "gmgn_holder": "",
    "onchain_holder_snapshot": "",
    "kryptogo_or_cluster_source": ""
  },
  "field_quality": {
    "missing_required_fields": [],
    "holder_snapshot_status": ""
  }
}
```

## `wallet_structure_normalized.json` 标准结构

用途：把 holder 快照汇总成 Intel Bot 可以消费的钱包结构事实层。

```json
{
  "schema_version": "sikk_holder_wallet_structure_normalized_v1",
  "token_address": "",
  "snapshot_time": "",
  "holder_metrics": {
    "holder_count": 0,
    "holder_delta": 0,
    "top10_holder_pct": 0,
    "top20_holder_pct": 0,
    "top_holder_count": 0,
    "top_holder_total_pct": 0
  },
  "intel_bot_usage_zh": [
    "结构侧剩余库存",
    "Top Holder 稳定性",
    "对手盘承接",
    "筹码迁移"
  ],
  "scope_limits_zh": [
    "本文件只提供 Holder 快照和钱包结构事实层",
    "不直接判断主导侧动机、对手盘压力或派发是否完成",
    "不输出确定庄家，不触发交易"
  ],
  "holders": []
}
```

## 质量规则

- `snapshot_time` 必须记录本轮 holder 快照时间；优先使用源数据时间，否则使用分析时间。
- `holder_rank` 必须按持仓比例从高到低稳定排序。
- `top10_holder_pct` / `top20_holder_pct` 优先使用上游字段；缺失时可基于快照样本估算，并在质量字段说明。
- `holder_count` 必须来自 GMGN / 链上 holder 总数；缺失时填 0 并记录缺失。
- `holder_delta` 是相邻快照差值；没有历史快照时填 0 并标记为待补。
- `holding_pct` 不能臆造；上游缺失时填 0。
- `wallet_structure_normalized.json` 只做事实汇总，不输出裁决结论。

## 给 Intel Bot 的用途

- 结构侧剩余库存
- Top Holder 稳定性
- 对手盘承接
- 筹码迁移

## 当前代码映射

当前已有基础：

- `modules/wallet_structure/source_reader.py`
  - 已通过 `gmgn-cli token holders` 拉取 holder 列表
  - 已合并 tagged holders / traders 证据
- `modules/wallet_structure/decision_builder.py`
  - 已输出钱包结构证据包
  - 已输出兼容 CSV 与决策 JSON

本次补强目标：

- 输出 `holder_snapshot_normalized.json`
- 输出 `wallet_structure_normalized.json`
- 将 holder rank、持仓金额、持仓比例、Top10/Top20、holder_count、holder_delta 纳入标准事实层
