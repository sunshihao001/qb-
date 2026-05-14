# Intel Structure Bot 量化结构 Schema 合同

> 本文档把“疑似主导侧成本区 / 结构侧筹码库存 / 派发进度 / 继续推进动机 / 对手盘压力 / 钱包行为匹配度”整理成可直接接代码的字段合同。
>
> 约束：
> - 只做 schema 与字段合同，不写交易代码。
> - 不改状态机，不动 paper runner，不开启实盘。
> - 所有对外判断 value 必须中文化。
> - 不直接使用“庄家成本”。

## 1. 统一输出包结构

建议最终由 Intel Structure Bot 输出一个总对象，再拆成 6 个子对象文件。

```json
{
  "schema_version": "intel_structure_quantitative_v1.0",
  "token_address": "",
  "token_symbol": "",
  "chain": "sol",
  "analysis_time": "",
  "data_window": {
    "snapshot_time": "",
    "lookback_days": 0
  },
  "dominant_cost_zone": {},
  "structure_inventory_estimate": {},
  "distribution_progress": {},
  "markup_motivation": {},
  "counterparty_pressure": {},
  "wallet_pattern_cost_alignment": {},
  "summary_zh": ""
}
```

## 2. 通用字段规范

### 2.1 通用字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `schema_version` | string | 是 | 合同版本号 |
| `token_address` | string | 是 | 代币地址 |
| `token_symbol` | string | 否 | 代币符号 |
| `chain` | string | 是 | 链名称，如 `sol` |
| `analysis_time` | string | 否 | 分析时间 |
| `summary_zh` | string | 否 | 中文总结句 |

### 2.2 值规范

- 数值字段优先使用 `number`。
- 缺失值使用 `null`。
- 无法判断的状态统一使用中文 `未知` 类表述。
- 所有状态字段必须提供 `*_zh`。
- 如果同时保留英文内部码，必须配对中文解释字段。

### 2.3 证据原则

- 单字段不能独立裁决结构结论。
- 需要至少两个来源维度才能形成稳定判断。
- 若证据不足，必须显式输出 `证据不足` / `未知` / `不确定`。

## 3. `dominant_cost_zone` 合同

### 3.1 目的

输出疑似主导侧成本区、成本中枢、市场成交成本、箱体成本，以及当前价格相对成本的关系。

### 3.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `wallet_avg_cost` | number/null | 否 | 单钱包平均成本，主动买入钱包按 `buy_amount_usd / buy_token_amount` 计算 |
| `wallet_first_buy_cost` | number/null | 否 | 单钱包首次买入成本 |
| `wallet_last_buy_cost` | number/null | 否 | 单钱包最后买入成本 |
| `wallet_cost_confidence` | number/null | 否 | 单钱包成本置信度，Token 转入或分发接收成本不可直接确认时为低置信或 0 |
| `same_source_group_cost_low` | number/null | 否 | 同源组成本下沿，取组内结构侧主动买入钱包平均成本 25 分位 |
| `same_source_group_cost_mid` | number/null | 否 | 同源组成本中枢，按 `sum(group_active_buy_usd) / sum(group_active_buy_token_amount)` 计算 |
| `same_source_group_cost_high` | number/null | 否 | 同源组成本上沿，取组内结构侧主动买入钱包平均成本 75 分位 |
| `same_source_group_cost_confidence` | number/null | 否 | 同源组成本证据置信度，来自组内可确认主动买入钱包成本置信度与样本数量 |
| `dominant_cost_low` | number/null | 否 | 疑似主导侧成本区下沿 |
| `dominant_cost_mid` | number/null | 否 | 疑似主导侧成本区中枢 |
| `dominant_cost_high` | number/null | 否 | 疑似主导侧成本区上沿 |
| `dominant_cost_confidence` | number/null | 否 | 证据置信度，建议 0-1 |
| `market_cost_mid` | number/null | 否 | 市场成交成本中枢 |
| `box_cost_mid` | number/null | 否 | 箱体成本中枢 |
| `current_price` | number/null | 否 | 当前价格 |
| `price_to_dominant_cost_pct` | number/null | 否 | 当前价格相对主导侧成本区的偏离百分比 |
| `cost_position_status_zh` | string | 是 | 中文状态 |
| `cost_evidence_grade_zh` | string | 否 | 中文证据等级说明 |
| `cost_notes_zh` | string | 否 | 中文补充说明 |

### 3.3 中文状态枚举

- 当前价格接近主导侧成本区
- 当前价格略高于主导侧成本区
- 当前价格大幅高于主导侧成本区
- 当前价格跌破主导侧成本区
- 成本区证据不足

### 3.4 校验规则

- `dominant_cost_low <= dominant_cost_mid <= dominant_cost_high`。
- 若任一核心成本字段缺失，则 `cost_position_status_zh` 不能输出强判断。
- `dominant_cost_confidence` 建议区间为 `0.0 ~ 1.0`。

### 3.5 推荐 JSON 骨架

```json
{
  "wallet_avg_cost": null,
  "same_source_group_cost_low": null,
  "same_source_group_cost_mid": null,
  "same_source_group_cost_high": null,
  "same_source_group_cost_confidence": null,
  "dominant_cost_low": null,
  "dominant_cost_mid": null,
  "dominant_cost_high": null,
  "dominant_cost_confidence": null,
  "market_cost_mid": null,
  "box_cost_mid": null,
  "current_price": null,
  "price_to_dominant_cost_pct": null,
  "cost_position_status_zh": "成本区证据不足",
  "cost_evidence_grade_zh": "证据不足",
  "cost_notes_zh": "缺少足够的同源组、早期钱包或成交密集区证据，暂无法稳定定位疑似主导侧成本区。"
}
```

### 3.6 单钱包成本输入规则

主动买入钱包可计算成本，公式为：

```text
wallet_avg_cost = buy_amount_usd / buy_token_amount
```

输入字段：
- `wallet_address`
- `token_address`
- `buy_amount_usd`
- `buy_token_amount`
- `first_buy_time`
- `buy_count`
- `sell_amount_usd`
- `sell_token_amount`
- `current_balance`

输出字段：
- `wallet_avg_cost`
- `wallet_first_buy_cost`
- `wallet_last_buy_cost`
- `wallet_cost_confidence`

约束：
- 主动买入钱包可以估算成本。
- Token 转入钱包不能直接用转入价格当成本。
- 分发接收钱包成本未知，必须标记“成本不可直接确认”。

## 4. `structure_inventory_estimate` 合同

### 4.1 目的

估计结构侧剩余筹码库存。

### 4.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `structure_max_inventory` | number/null | 否 | 结构侧理论最大库存 |
| `structure_current_inventory` | number/null | 否 | 当前可识别库存 |
| `structure_inventory_remaining_pct` | number/null | 否 | 当前库存剩余比例 |
| `early_wallet_remaining_pct` | number/null | 否 | 早期钱包剩余比例 |
| `same_source_group_remaining_pct` | number/null | 否 | 同源组剩余比例 |
| `top_holder_structure_stability_score` | number/null | 否 | Top Holder 结构侧稳定性分数 |
| `inventory_status_zh` | string | 是 | 中文状态 |
| `inventory_notes_zh` | string | 否 | 中文补充说明 |

### 4.3 中文状态枚举

- 库存充足
- 库存中等
- 库存偏低
- 库存接近出清
- 库存状态未知

### 4.4 校验规则

- 若 `structure_max_inventory` 有值，则 `structure_current_inventory <= structure_max_inventory`。
- 剩余比例建议范围 `0 ~ 100`。
- 当早期钱包与同源组剩余都偏低时，库存状态不能仍输出“库存充足”。

### 4.5 推荐 JSON 骨架

```json
{
  "structure_max_inventory": null,
  "structure_current_inventory": null,
  "structure_inventory_remaining_pct": null,
  "early_wallet_remaining_pct": null,
  "same_source_group_remaining_pct": null,
  "top_holder_structure_stability_score": null,
  "inventory_status_zh": "库存状态未知",
  "inventory_notes_zh": "缺少结构侧初始可识别库存基线，暂无法精确估计剩余筹码规模。"
}
```

## 5. `distribution_progress` 合同

### 5.1 目的

量化派发进度。

### 5.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `structure_sold_pct` | number/null | 否 | 结构侧整体卖出比例 |
| `early_wallet_sold_pct` | number/null | 否 | 早期钱包卖出比例 |
| `same_source_group_sold_pct` | number/null | 否 | 同源组同步卖出比例 |
| `distribution_receiver_sold_pct` | number/null | 否 | 分发接收方卖出比例 |
| `backflow_confirmed_pct` | number/null | 否 | 利润回流确认比例 |
| `distribution_progress_score` | number/null | 否 | 派发进度分数 |
| `distribution_progress_status_zh` | string | 是 | 中文状态 |
| `distribution_notes_zh` | string | 否 | 中文补充说明 |

### 5.3 中文状态枚举

- 尚未明显派发
- 部分派发
- 边拉边派发
- 主动派发
- 派发基本完成
- 派发进度未知

### 5.4 校验规则

- 所有比例建议范围 `0 ~ 100`。
- `distribution_progress_score` 必须可由各子项解释。
- 若早期钱包与同源组卖出率同步上升，应提高派发进度解释权重。

### 5.5 推荐 JSON 骨架

```json
{
  "structure_sold_pct": null,
  "early_wallet_sold_pct": null,
  "same_source_group_sold_pct": null,
  "distribution_receiver_sold_pct": null,
  "backflow_confirmed_pct": null,
  "distribution_progress_score": null,
  "distribution_progress_status_zh": "派发进度未知",
  "distribution_notes_zh": "缺少连续卖出与回流链路证据，暂无法判断派发进度。"
}
```

## 6. `markup_motivation` 合同

### 6.1 目的

判断主导侧是否还有继续拉升、二段扩张、控盘维护的动力。

### 6.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `remaining_inventory_score` | number/null | 否 | 剩余库存驱动分数 |
| `unfinished_distribution_score` | number/null | 否 | 未完成派发驱动分数 |
| `cost_position_score` | number/null | 否 | 成本位置驱动分数 |
| `pattern_control_score` | number/null | 否 | 盘型可控分数 |
| `liquidity_need_score` | number/null | 否 | 流动性承接需求分数 |
| `second_stage_condition_score` | number/null | 否 | 二段条件分数 |
| `counterparty_pressure_penalty` | number/null | 否 | 对手盘压力惩罚项 |
| `same_source_exit_penalty` | number/null | 否 | 同源组同步退出惩罚项 |
|| `markup_motivation_score` | number/null | 否 | 继续推进动机总分 |
| `markup_motivation_status_zh` | string | 是 | 中文状态 |
| `markup_motivation_notes_zh` | string | 否 | 中文补充说明 |

### 6.3 中文状态枚举

- 继续推进动机强
- 继续推进动机中等
- 继续推进动机弱
- 更偏向派发退出
- 动机证据不足

### 6.4 校验规则

- `markup_motivation_score = remaining_inventory_score + unfinished_distribution_score + cost_position_score + pattern_control_score + liquidity_need_score + second_stage_condition_score - counterparty_pressure_penalty - same_source_exit_penalty`。
- 正向因子与负向因子应分开计算。
- 若对手盘压力惩罚显著上升，应降低继续推进动机解释。
- 若库存高、派发未完成、盘型可控，则动机不应被写成“弱”。

### 6.5 推荐 JSON 骨架

```json
{
  "remaining_inventory_score": null,
  "unfinished_distribution_score": null,
  "cost_position_score": null,
  "pattern_control_score": null,
  "liquidity_need_score": null,
  "second_stage_condition_score": null,
  "counterparty_pressure_penalty": null,
  "same_source_exit_penalty": null,
  "markup_motivation_score": null,
  "markup_motivation_status_zh": "动机证据不足",
  "markup_motivation_notes_zh": "缺少库存、派发和盘型三类证据，暂无法判断继续推进动机。"
}
```

## 7. `counterparty_pressure` 合同

### 7.1 目的

量化对手盘压力。

### 7.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `late_large_buyer_score` | number/null | 否 | 晚期大额买入分数 |
| `whale_bagholder_score` | number/null | 否 | 接盘鲸鱼分数 |
| `retailization_score` | number/null | 否 | 散户化分数 |
| `early_to_late_transfer_score` | number/null | 否 | 早期筹码流向晚期买家分数 |
| `floating_loss_late_holder_score` | number/null | 否 | 晚期浮亏钱包增加分数 |
| `counterparty_pressure_score` | number/null | 否 | 对手盘压力总分 |
| `counterparty_pressure_status_zh` | string | 是 | 中文状态 |
| `counterparty_pressure_notes_zh` | string | 否 | 中文补充说明 |

### 7.3 中文状态枚举

- 对手盘压力低
- 对手盘压力中
- 对手盘压力高
- 疑似散户接盘
- 疑似鲸鱼接盘
- 疑似结构侧派发给对手盘
- 对手盘状态未知

### 7.4 校验规则

- 晚期大额买入若与高位成本偏离同时出现，应提高压力警觉。
- 接盘鲸鱼与浮亏钱包增加可同时成立。
- `counterparty_pressure_score` 需要能追溯到子项，不得黑箱输出。

### 7.5 推荐 JSON 骨架

```json
{
  "late_large_buyer_score": null,
  "whale_bagholder_score": null,
  "retailization_score": null,
  "early_to_late_transfer_score": null,
  "floating_loss_late_holder_score": null,
  "counterparty_pressure_score": null,
  "counterparty_pressure_status_zh": "对手盘状态未知",
  "counterparty_pressure_notes_zh": "缺少晚期买入、浮亏和筹码转移证据，暂无法判断对手盘压力。"
}
```

## 8. `wallet_pattern_cost_alignment` 合同

### 8.1 目的

判断成本区、钱包行为和盘型是否匹配。

### 8.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `pattern_type_zh` | string | 是 | 盘型中文判断 |
| `cost_pattern_match_score` | number/null | 否 | 成本与盘型匹配分数 |
| `wallet_behavior_match_score` | number/null | 否 | 钱包行为与盘型匹配分数 |
| `alignment_status_zh` | string | 是 | 总体匹配度中文状态 |
| `alignment_notes_zh` | string | 否 | 中文补充说明 |

### 8.3 可用盘型状态

- 横盘控筹
- 二段放量
- 主动派发
- 结构崩塌
- 匹配度未知

### 8.4 校验规则

- 若结构侧成本区与横盘区高度重合，可偏向“横盘控筹”。
- 若成本区上移且卖出与承接同时增强，可偏向“二段放量”或“主动派发”。
- 若价格跌破成本区且库存失守，可偏向“结构崩塌”。

### 8.5 推荐 JSON 骨架

```json
{
  "pattern_type_zh": "匹配度未知",
  "cost_pattern_match_score": null,
  "wallet_behavior_match_score": null,
  "alignment_status_zh": "匹配度未知",
  "alignment_notes_zh": "证据不足，无法判断成本区、钱包行为和盘型是否匹配。"
}
```

## 9. 汇总输出建议

如果要直接落地成文件，建议每个对象单独保存：

- `dominant_cost_zone.json`
- `structure_inventory_estimate.json`
- `distribution_progress.json`
- `markup_motivation.json`
- `counterparty_pressure_quant.json`
- `wallet_pattern_cost_alignment.json`

并额外保存：

- `quantitative_structure_report.md`

## 10. 对接建议

### 10.1 对上游

上游只提供事实，不提供结论：
- 钱包持仓
- 同源关系
- 买卖时序
- 回流路径
- 成交密集区
- 价格区间

### 10.2 对下游

下游 Strategy Gate Bot 只消费结构结论，不消费交易建议。

### 10.3 禁止事项

- 不输出“庄家一定要拉”。
- 不输出买点。
- 不输出实盘指令。
- 不修改状态机。

## 11. 最终建议

这套合同已经足够接代码。实现时建议把每个 JSON 对象映射为独立 dataclass / pydantic model，再由统一汇总器拼装总报告。
