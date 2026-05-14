# 派发进度模型

## 目标

建立一个只读的派发进度推断模型，用来判断结构侧是否已经明显出清，或者仍处于边拉边派发、主动派发、维持维护等阶段。

## 模块名

`distribution_progress_estimator`

## 输入信号

- 早期钱包卖出行为
- 同源组同步卖出行为
- 分发接收钱包的后续转手行为
- 利润回流路径
- 早期持仓减少速度
- 同源组持仓减少速度
- 晚期接收钱包是否开始承接并浮亏

## 关键字段

- `structure_sold_pct`
- `early_wallet_sold_pct`
- `same_source_group_sold_pct`
- `distribution_receiver_sold_pct`
- `backflow_confirmed_pct`
- `distribution_progress_score`

## 中文状态

- 尚未明显派发
- 部分派发
- 边拉边派发
- 主动派发
- 派发基本完成
- 派发进度未知

## 解释逻辑

### 1. 早期钱包卖出率
若早期钱包持续减仓，且卖出比例高于一般参与者，则派发进度上升。

### 2. 同源组同步卖出率
若同源组内多个钱包同步减仓，说明结构侧筹码可能在系统性转移。

### 3. 分发接收卖出率
若接收分发筹码的钱包很快继续卖出，说明筹码转移并未形成稳定新结构，更多是派发链条的一环。

### 4. 利润回流比例
若利润回流路径增加，且回流与卖出结合出现，说明结构侧可能在进行资金回收或派发收尾。

## 评分建议

`distribution_progress_score` 建议由以下子项构成：

- 早期钱包卖出贡献
- 同源组同步卖出贡献
- 分发接收卖出贡献
- 利润回流贡献
- 结构侧剩余筹码减少贡献

## 输出建议

```json
{
  "structure_sold_pct": 0,
  "early_wallet_sold_pct": 0,
  "same_source_group_sold_pct": 0,
  "distribution_receiver_sold_pct": 0,
  "backflow_confirmed_pct": 0,
  "distribution_progress_score": 0,
  "distribution_progress_status_zh": "尚未明显派发"
}
```

## 判断注意事项

- 卖出率高不等于一定已经出清。
- 需要结合剩余库存和对手盘压力一起看。
- 若派发进度高但库存仍大，可能意味着仍有继续推进或制造流动性完成后续派发的动机。

## 交接原则

该模型只描述派发进度，不输出交易建议，也不直接给买点。
