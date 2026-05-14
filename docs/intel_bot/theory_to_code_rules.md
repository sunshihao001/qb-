# Intel Bot 理论到代码落地规则

## 背景

Intel Bot 负责 Telegram Bot 的结构情报层：结构分析、钱包画像、筹码结构、同源判断、分发判断、接盘钱包判断、结果钱包判断。

以后不能再只写理论文档而不说明代码如何理解、如何落地。每个理论模块必须同时给出代码接口、输入输出、测试入口和目录归属。

## 强制规则

### 1. 每个理论模块必须绑定代码模块

文档里新增任何模型、字段、状态或判断规则时，必须同步写明：

- 生产代码文件：`modules/wallet_structure/<module_name>.py`
- 测试文件：`tests/test_<module_name>.py`
- 输出对象：对应 dataclass / dict schema
- 输出路径：必须落在 `data/gmgn_candidates_live_run/intel-bot/logs/`

如果暂时无法实现，文档必须明确标注：

```text
代码状态：TODO，缺 <具体函数名> / <具体测试名>
```

不能只写“后续实现”。

### 2. 理论字段必须能被代码直接理解

每个理论字段必须有：

- 英文字段名
- 中文展示名
- 类型
- 单位 / 取值范围
- 缺失时默认值
- 是否允许 `null`
- 对应计算函数

示例：

```text
字段：counterparty_pressure_score
中文：对手盘压力总分
类型：float
范围：0-100
缺失默认：0.0
计算函数：calculate_counterparty_pressure
代码文件：modules/wallet_structure/counterparty_pressure_calculator.py
```

### 3. 理论公式必须转成可测试函数

文档中出现公式时，必须同时给出函数签名。

示例：

```text
理论公式：同源组成本中枢 = 组内主动买入金额总和 / 组内主动买入 token 数量总和
代码函数：calculate_dominant_cost_zone(...).same_source_group_cost_mid
测试：tests/test_dominant_cost_zone_calculator.py::test_same_source_group_cost_uses_weighted_average_active_buys
```

### 4. 理论状态必须有枚举落点

文档中出现中文状态时，必须说明代码枚举或输出状态。

示例：

```text
状态：对手盘压力高
字段：counterparty_pressure_status_zh
来源函数：calculate_counterparty_pressure
代码文件：modules/wallet_structure/counterparty_pressure_calculator.py
```

### 5. 每个模型文档必须增加“代码理解”小节

每个 `docs/intel_bot/*model*.md` 或 schema 合同文档，新增或修改理论时必须包含以下结构：

```markdown
## 代码理解

- 代码文件：`modules/wallet_structure/<module>.py`
- 测试文件：`tests/test_<module>.py`
- 入口函数：`calculate_xxx(...)`
- 输入对象：...
- 输出对象：...
- 输出路径：`data/gmgn_candidates_live_run/intel-bot/logs/...`
- 禁止事项：不改状态机、不写 PAPER_READY、不写 BLOCKED、不执行交易
```

### 6. TDD 是默认落地方式

只要理论进入代码实现阶段，必须：

1. 先写失败测试
2. 再写最小实现
3. 跑测试通过
4. 再更新文档里的代码理解小节

### 7. 理论和代码优先同轮推进

除非用户明确只要文档，否则默认做法是：

1. 简短说明理论意图
2. 新增/修改代码
3. 新增/修改测试
4. 更新文档
5. 跑测试验证

不再做“先写一堆理论，代码以后再说”的交付方式。

## 当前已绑定的模块

- 主导侧成本区：
  - 代码：`modules/wallet_structure/dominant_cost_zone_calculator.py`
  - 测试：`tests/test_dominant_cost_zone_calculator.py`

- 筹码库存估算：
  - 代码：`modules/wallet_structure/structure_inventory_calculator.py`
  - 测试：`tests/test_structure_inventory_calculator.py`

- 派发进度：
  - 代码：`modules/wallet_structure/distribution_progress_calculator.py`
  - 测试：`tests/test_distribution_progress_calculator.py`

- 继续推进 / 二段扩张动机：
  - 代码：`modules/wallet_structure/markup_motivation_calculator.py`
  - 测试：`tests/test_markup_motivation_calculator.py`

- 对手盘压力：
  - 代码：`modules/wallet_structure/counterparty_pressure_calculator.py`
  - 测试：`tests/test_counterparty_pressure_calculator.py`

- 钱包 × 盘型 × 成本区匹配：
  - 代码：`modules/wallet_structure/wallet_pattern_cost_alignment_calculator.py`
  - 测试：`tests/test_counterparty_pressure_calculator.py`

- Token 集群 / 主导侧生命周期 / 主导侧行为动机：
  - 代码：`modules/wallet_structure/token_cluster_analyzer.py`
  - 测试：`tests/test_token_cluster_analyzer.py`

- 量化统一导出：
  - 代码：`modules/wallet_structure/quantitative_aggregator.py`
  - 测试：`tests/test_quantitative_aggregator.py`

## 目录约束

Intel Bot 的运行数据只允许放在：

```text
data/gmgn_candidates_live_run/intel-bot/
  code/
  logs/
```

历史迁移数据也必须放入：

```text
data/gmgn_candidates_live_run/intel-bot/logs/
```

禁止新增运行数据到：

```text
data/gmgn_candidates_live_run/intel_bot/
data/gmgn_candidates_live_run/wallet_structure/
data/wallet_intelligence/
```
