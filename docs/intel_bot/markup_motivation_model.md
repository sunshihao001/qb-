# 继续推进动机模型

## 目标

建立一个用于判断结构侧是否仍有继续推进、二段扩张、控盘维护或偏向派发退出动机的量化模型。

## 模块名

`markup_motivation_model`

## 设计目标

这个模型回答的不是“要不要买”，而是：

- 结构侧是否还有继续推进的价值
- 是否存在二段扩张动机
- 是否仍在维护盘型
- 是否更偏向派发退出

## 输入维度

- 成本偏离
- 剩余库存
- 派发未完成程度
- 流动性承接情况
- 盘型可控程度
- 对手盘压力
- 同源组退出惩罚

## 关键字段

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

## 中文状态

- 继续推进动机强
- 继续推进动机中等
- 继续推进动机弱
- 更偏向派发退出
- 动机证据不足

## 解释逻辑

### 1. 剩余库存
库存越高，继续推进或维护盘型的理由越强。

### 2. 派发未完成
若派发尚未完成，继续推进可能用于完成后续分发或测试承接。

### 3. 成本位置
若价格远未脱离疑似主导侧成本区，说明维护成本区的动力仍可能存在。

### 4. 盘型可控
若盘型仍处于箱体、控盘、二段准备等状态，继续推进的动机更强。

### 5. 流动性承接
若市场承接良好，但风险仍可控，可能存在借流动性完成结构动作的动机。

### 6. 对手盘压力
若对手盘压力上升，但结构仍未完全出清，则可能更倾向于继续推进或制造流动性，而不是立刻退出。

## 评分建议

`markup_motivation_score` 由正负两类因子组成，正向因子相加，负向因子扣减：

```text
继续推进动机分 =
  结构侧未派发库存分
+ 派发未完成分
+ 成本偏离合理分
+ 盘型可控分
+ 流动性不足需制造承接分
+ 二段扩张条件分
- 对手盘压力扣分
- 同源组同步退出扣分
```

### 正向因子
- 剩余库存高
- 派发未完成
- 成本位置仍可控
- 盘型仍稳定
- 需要流动性承接
- 二段条件成立

### 负向因子
- 对手盘压力过高
- 同源组明显退出
- 成本区失守
- 盘型崩塌

## 输出建议

```json
{
  "remaining_inventory_score": 0,
  "unfinished_distribution_score": 0,
  "cost_position_score": 0,
  "pattern_control_score": 0,
  "liquidity_need_score": 0,
  "second_stage_condition_score": 0,
  "counterparty_pressure_penalty": 0,
  "same_source_exit_penalty": 0,
  "markup_motivation_score": 0,
  "markup_motivation_status_zh": "动机证据不足"
}
```

## 交接原则

该模型只能解释继续推进动机强弱，不能直接输出买点，也不能直接把动机解释成必然拉升。
