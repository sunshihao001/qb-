# 对手盘压力量化模型

## 目标

建立一个用于判断当前结构是否正在把筹码转移给对手盘的只读压力模型。

## 模块名

`counterparty_pressure_quant_model`

## 设计目标

该模型用于识别：
- 晚期大额买入是否增多
- 是否出现接盘鲸鱼
- 是否出现散户化接力
- 是否有早期筹码流向晚期参与者
- 是否有浮亏钱包持续增加
- 是否存在结构侧向对手盘派发的迹象

## 关键字段

- `late_large_buyer_score`
- `whale_bagholder_score`
- `retailization_score`
- `early_to_late_transfer_score`
- `floating_loss_late_holder_score`
- `counterparty_pressure_score`
- `counterparty_pressure_status_zh`
- `counterparty_pressure_notes_zh`

## 中文状态

- 对手盘压力低
- 对手盘压力中
- 对手盘压力高
- 疑似散户接盘
- 疑似鲸鱼接盘
- 疑似结构侧派发给对手盘
- 对手盘状态未知

## 解释逻辑

### 1. 晚期大额买入
如果晚期出现明显大额买入，但价格位置已经偏离疑似主导侧成本区，则需要警惕是否在形成接盘压力。

### 2. 接盘鲸鱼
若大额钱包在高位持续承接并快速浮亏，则可标记为疑似接盘鲸鱼。

### 3. 散户化
若买盘广泛分散、金额小、频次高、缺乏持续性，则可能是散户化接力。

### 4. 早期筹码流向
若早期结构筹码持续转移给后续买入方，说明压力可能从结构侧外溢到对手盘。

### 5. 浮亏钱包增加
若晚期持仓钱包的浮亏数量与浮亏幅度同步上升，则对手盘压力通常更高。

## 评分建议

`counterparty_pressure_score` 可由以下项构成：

- 晚期大额买入强度
- 接盘鲸鱼强度
- 散户化程度
- 早期筹码流向对手盘程度
- 浮亏钱包增加程度
- Top Holder 结构侧流失程度

## 输出建议

```json
{
  "late_large_buyer_score": 0,
  "whale_bagholder_score": 0,
  "retailization_score": 0,
  "early_to_late_transfer_score": 0,
  "floating_loss_late_holder_score": 0,
  "counterparty_pressure_score": 0,
  "counterparty_pressure_status_zh": "对手盘状态未知",
  "counterparty_pressure_notes_zh": "缺少晚期买入、浮亏、筹码转移和 Top Holder 流失证据，暂无法判断对手盘压力。"
}
```

## 代码理解

- 代码文件：`modules/wallet_structure/counterparty_pressure_calculator.py`
- 测试文件：`tests/test_counterparty_pressure_calculator.py`
- 入口函数：`calculate_counterparty_pressure(...)`
- 输出对象：`CounterpartyPressureResult`
- 聚合导出：`modules/wallet_structure/quantitative_aggregator.py`
- 输出路径：`data/gmgn_candidates_live_run/intel-bot/logs/counterparty_pressure_quant.json`
- 禁止事项：不改状态机、不写 `PAPER_READY`、不写 `BLOCKED`、不执行交易

### 字段到代码映射

- `late_large_buyer_score`：晚期大额买入强度，float，0-1，缺失允许 `None`
- `whale_bagholder_score`：接盘鲸鱼强度，float，0-1，缺失允许 `None`
- `retailization_score`：散户化程度，float，0-1，缺失允许 `None`
- `early_to_late_transfer_score`：早期筹码流向晚期买家程度，float，0-1，缺失允许 `None`
- `floating_loss_late_holder_score`：晚期浮亏钱包增加程度，float，0-1，缺失允许 `None`
- `counterparty_pressure_score`：对手盘压力总分，float，0-100，由入口函数加权计算
- `counterparty_pressure_status_zh`：中文压力状态，由总分分段得到
- `counterparty_pressure_notes_zh`：中文解释

## 交接原则

该模型只负责压力识别，不负责交易建议，也不输出“可以追”之类结论。
