# 量化结构模型设计

## 目标

定义 Intel Structure Bot 的量化结构推断层字段、状态、评分方式与输出结构，确保所有判断中文化、可审计、可交接。

## 模块总览

### 1. `dominant_cost_zone_calculator`
作用：计算疑似主导侧成本区。

覆盖内容：
- 单钱包成本
- 同源组成本
- 早期结构钱包成本
- 市场成交成本
- 箱体成本

### 2. `structure_inventory_estimator`
作用：计算结构侧剩余筹码库存。

覆盖内容：
- 早期钱包剩余
- 同源组剩余
- 高结果钱包剩余
- Top Holder 结构侧稳定性

### 3. `distribution_progress_estimator`
作用：计算派发进度。

覆盖内容：
- 早期钱包卖出率
- 同源组同步卖出率
- 分发接收卖出率
- 利润回流比例

### 4. `markup_motivation_model`
作用：计算继续推进 / 二段扩张 / 控盘维护动机。

### 5. `counterparty_pressure_quant_model`
作用：计算对手盘压力。

代码理解：
- 代码文件：`modules/wallet_structure/counterparty_pressure_calculator.py`
- 入口函数：`calculate_counterparty_pressure(...)`
- 测试文件：`tests/test_counterparty_pressure_calculator.py`
- 输出对象：`CounterpartyPressureResult`

### 6. `cost_risk_reward_ratio`（Strategy Gate Bot 下游）
作用：由 Strategy Gate Bot 计算参与风险收益比，不属于 Intel Bot 核心职责。

代码理解：
- 代码位置：不放在 `modules/wallet_structure/`，应放入 Strategy Gate Bot 对应模块
- Intel Bot 仅输出上游输入：`dominant_cost_zone`、`structure_inventory_estimate`、`distribution_progress`、`markup_motivation`、`counterparty_pressure`、`wallet_pattern_cost_alignment`
- 计算公式：`上方目标空间 / 下方失效空间`
- 结论用途：参与点筛选、风险收益比门禁

中文状态：
- `风险收益比合适`
- `风险收益比一般`
- `风险收益比不足`
- `追高接盘风险高`

边界：
- 该模型属于 Strategy Gate Bot，不在 Intel Bot 内实现
- Intel Bot 只提供成本区、库存、派发、动机、对手盘压力
- 输出对象：`WalletPatternCostAlignmentResult`

### 7. `token_cluster_analyzer` / `dominant_lifecycle` / `dominant_intent`
作用：统一 Token 集群、主导侧生命周期与主导侧行为动机推断入口。

代码理解：
- 代码文件：`modules/wallet_structure/token_cluster_analyzer.py`
- 入口函数：`analyze_token_cluster(...)`、`infer_dominant_lifecycle(...)`、`classify_dominant_intent(...)`
- 测试文件：`tests/test_token_cluster_analyzer.py`
- 输出对象：dict bundle，后续可升级 dataclass

### 8. `quantitative_structure_aggregator`
作用：统一导出量化结构对象与入口函数。

代码理解：
- 代码文件：`modules/wallet_structure/quantitative_aggregator.py`
- 测试文件：`tests/test_quantitative_aggregator.py`
- 输出对象：`QuantitativeStructureReport`，并可写出 JSON / Markdown 报告

### 9. `strategy_gate_cost_risk_reward_ratio`
作用：Strategy Gate Bot 根据 Intel Bot 上游量化对象，计算参与风险收益比。

代码理解：
- 代码文件：`modules/strategy_gate/cost_risk_reward_calculator.py`
- 测试文件：`tests/test_strategy_gate_cost_risk_reward_calculator.py`
- 输出对象：`StrategyGateRiskRewardResult`
- 说明：该模型不在 Intel Bot 核心层实现，只消费上游结构信号

## 模型原则

1. 所有评分只用于结构解释，不直接等价于交易信号。
2. 缺失字段必须保留 `null` 或 `UNKNOWN`。
3. 所有中文状态必须可由字段组合解释出来。
4. 评分需能拆解为多个子项，不能只有一个黑箱总分。

## 标准输出对象

建议输出六个 JSON 对象：
- `dominant_cost_zone.json`
- `structure_inventory_estimate.json`
- `distribution_progress.json`
- `markup_motivation.json`
- `counterparty_pressure_quant.json`
- `wallet_pattern_cost_alignment.json`

## 通用约束

- JSON key 可以英文。
- 所有判断 value 必须中文化。
- 所有状态必须有中文解释字段。
- 不允许输出“庄家一定要拉”之类结论。
- 不给买点。

## 量化顺序

1. 先算成本区。
2. 再算库存。
3. 再算派发进度。
4. 再算继续推进动机。
5. 再算对手盘压力。
6. 最后算钱包行为与盘型是否匹配。

## 结构解释层输出建议

输出应包含：
- 指标值
- 中文状态
- 证据摘要
- 证据等级
- 关键风险提示
- 交接给 Strategy Gate Bot 的说明

## 建议 JSON 结构

```json
{
  "token_address": "...",
  "analysis_time": "...",
  "dominant_cost_zone": {
    "dominant_cost_low": 0,
    "dominant_cost_mid": 0,
    "dominant_cost_high": 0,
    "dominant_cost_confidence": 0,
    "dominant_cost_status_zh": "疑似主导侧成本区证据不足"
  },
  "structure_inventory_estimate": {
    "structure_current_inventory": 0,
    "structure_inventory_remaining_pct": 0,
    "inventory_status_zh": "库存状态未知"
  },
  "distribution_progress": {
    "distribution_progress_score": 0,
    "distribution_progress_status_zh": "派发进度未知"
  },
  "markup_motivation": {
    "markup_motivation_score": 0,
    "markup_motivation_status_zh": "动机证据不足"
  },
  "counterparty_pressure": {
    "counterparty_pressure_score": 0,
    "counterparty_pressure_status_zh": "对手盘状态未知"
  },
  "wallet_pattern_cost_alignment": {
    "alignment_status_zh": "盘型匹配度未知"
  }
}
```

## 交接原则

该模型只负责结构判断，不负责最终参与点筛选。最终门禁交给 Strategy Gate Bot。
