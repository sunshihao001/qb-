# Source Wallet Bot 量化结构字段补充合同

## 目的

本合同将 Wallet-Intel 量化结构字段补充到 Source Wallet Bot 的钱包结构分析体系，用于后续 `wallet_structure_normalized.json`、`same_source_groups.json`、`chip_distribution_summary.json` 和 handoff 包的扩展，不直接改旧 schema 的必填字段。

## 适用路径

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/
```

## 字段组 1：同源组成本

- `same_source_group_cost_low`
- `same_source_group_cost_mid`
- `same_source_group_cost_high`
- `same_source_group_cost_confidence`

### 计算约束

```text
same_source_group_cost_mid = sum(group_active_buy_usd) / sum(group_active_buy_token_amount)
same_source_group_cost_low = 组内结构侧主动买入钱包平均成本 25 分位
same_source_group_cost_high = 组内结构侧主动买入钱包平均成本 75 分位
same_source_group_cost_confidence = 组内可确认主动买入钱包成本置信度 + 样本数量
```

### 排除对象

- Token 转入钱包
- 分发接收钱包
- 晚期接盘鲸鱼
- 普通噪音钱包
- 交易所 / router / LP / infra 地址

## 字段组 2：主导侧成本区

- `dominant_cost_low`
- `dominant_cost_mid`
- `dominant_cost_high`
- `dominant_cost_confidence`
- `dominant_cost_deviation_rate`
- `dominant_cost_deviation_status_zh`

### 解释

`dominant_cost_*` 是结构侧候选钱包成本区，不是所有买入者均值，不是确定“庄家成本”。

## 字段组 3：库存与派发进度

- `structure_inventory_remaining_pct`
- `inventory_status_zh`
- `distribution_progress_score`
- `distribution_progress_status_zh`
- `early_wallet_sold_pct`
- `same_source_group_sold_pct`
- `distribution_receiver_sold_pct`
- `backflow_confirmed_pct`

### 降级规则

缺少 denominator 时不得强算；卖出比例高不等于派发完成，必须结合剩余库存、同源同步卖出、分发接收钱包后续行为、利润回流和对手盘压力。

## 字段组 4：继续推进动机

- `remaining_inventory_score`
- `unfinished_distribution_score`
- `cost_position_score`
- `pattern_control_score`
- `liquidity_need_score`
- `second_stage_condition_score`
- `counterparty_pressure_penalty`
- `same_source_exit_penalty`
- `markup_motivation_score`
- `markup_motivation_status_zh`
- `markup_motivation_notes_zh`

允许状态：

- `继续推进动机强`
- `继续推进动机中等`
- `继续推进动机弱`
- `更偏向派发退出`
- `动机证据不足`

## 字段组 5：对手盘压力

- `late_large_buyer_score`
- `whale_bagholder_score`
- `retailization_score`
- `early_to_late_transfer_score`
- `floating_loss_late_holder_score`
- `counterparty_pressure_score`
- `counterparty_pressure_status_zh`
- `counterparty_pressure_notes_zh`

允许状态：

- `对手盘压力低`
- `对手盘压力中`
- `对手盘压力高`
- `疑似散户接盘`
- `疑似鲸鱼接盘`
- `疑似结构侧派发给对手盘`
- `对手盘状态未知`

## 硬边界

这些字段只能用于结构情报和证据解释，不得直接变成：

- 交易建议
- PAPER_READY / BLOCKED
- 开仓 / 止盈 / 止损
- state_machine 状态
- real swap / signing / broadcast
