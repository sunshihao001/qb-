# Wallet-Intel / Intel Bot 底层系统设计流程

> 目的：把 Wallet-Intel 的底层结构分析流程固定成“事实先行、量化分层、行为假设、总控汇总”的系统设计图谱。本文只描述 Intel Bot / Wallet-Intel 的只读结构分析链路，不生成交易指令、不修改状态机、不写 paper runner、不触碰实盘逻辑。

## 0. 系统边界

- 系统类型：钱包结构情报系统。
- 主入口：用户只向 Orchestrator 提交目标。
- 事实层：Wallet-Fact 先采集、标准化、输出事实文件。
- 推断层：Behavior-Inference 只读事实文件，输出主导侧行为动机假设。
- 总控层：Orchestrator 负责任务票、调度、字段验收、缺口清单和最终汇总。
- 禁止事项：不直接输出开仓/止盈/止损，不直接 PAPER_READY/BLOCKED，不执行 swap，不签名，不广播，不读写私钥。

## 1. 端到端底层流程

1. 用户提交目标：token、钱包、群组、历史样本或结构问题。
2. Orchestrator 生成任务票：`task_id`、目标对象、数据窗口、阶段锁、验收字段。
3. Wallet-Fact 采集源数据：GMGN / legacy archive / holder / trader / transfer / funding traces。
4. Wallet-Fact 标准化：输出 `wallet_structure_normalized`，缺失值保持 `null` / `UNKNOWN`。
5. Orchestrator 验收事实文件：字段完整性、来源引用、缺口列表。
6. Behavior-Inference 读取标准事实：不得自行编造事实，不得为了结论补字段。
7. 量化层按 11 层模型计算：成本、库存、派发、对手盘、盘型匹配、生命周期、意图。
8. Orchestrator 汇总：合并事实证据、推断证据、冲突说明、下一步建议。
9. 输出报告：只输出结构情报和证据等级，不输出交易动作。

## 2. 11 层结构分析模型

### Layer 1：钱包事实层

- 输入：原始钱包、holder、trader、transfer、funding 数据。
- 输出：标准事实字段、来源引用、缺失字段。
- 代码/合同：`wallet_structure_normalized`、`wallet_source_reader`。
- 禁止：从 dashboard / paper / narrative 反推事实。

### Layer 2：钱包基础分类层

- 输入：标准事实记录。
- 输出：钱包年龄、新钱包标记、活跃度、GMGN 标签、基础角色候选。
- 代码/合同：`wallet_entity_profiler`。
- 禁止：直接说“庄家”或单字段强判。

### Layer 3：当前 token 行为层

- 输入：当前 token 内买入、卖出、持仓、收益、交易次数。
- 输出：`first_buy_time`、`last_sell_time`、`holding_pct`、`sold_pct`、`roi`、`pnl`。
- 代码/合同：`current_token_behavior_analyzer`。
- 禁止：跨 token 历史直接覆盖当前 token 事实。

### Layer 4：同源组与资金路径层

- 输入：资金来源、同步买卖、Token 分发、利润回流、基础设施边。
- 输出：`same_source_group_id`、relation edges、edge strength、conflict notes。
- 代码/合同：`same_source_group_analyzer`。
- 禁止：冲突证据下强行合并同源。

### Layer 5：主导侧成本区计算层（核心）

- 输入：结构侧候选钱包主动买入金额、主动买入 token 数量、同源组成员。
- 输出：
  - `wallet_avg_cost`
  - `same_source_group_cost_low`
  - `same_source_group_cost_mid`
  - `same_source_group_cost_high`
  - `same_source_group_cost_confidence`
  - `dominant_cost_low/mid/high`
  - `dominant_cost_confidence`
- 公式：
  - 单钱包成本：`buy_amount_usd / buy_token_amount`
  - 同源组成本中枢：`sum(group_active_buy_usd) / sum(group_active_buy_token_amount)`
  - 同源组成本下沿：组内钱包平均成本 25 分位
  - 同源组成本上沿：组内钱包平均成本 75 分位
- 代码：`modules/wallet_structure/dominant_cost_zone_calculator.py`
- 测试：`tests/test_dominant_cost_zone_calculator.py`
- 禁止：Token 转入钱包、分发接收钱包、接盘鲸鱼、普通噪音钱包直接参与主导侧成本确认。

### Layer 6：筹码库存与派发进度层（核心）

- 输入：结构侧最大库存、当前可识别库存、同源组剩余比例、早期钱包剩余比例、接收钱包卖出比例、回流比例。
- 输出：
  - `structure_inventory_remaining_pct`
  - `inventory_status_zh`
  - `distribution_progress_score`
  - `distribution_progress_status_zh`
- 代码：
  - `modules/wallet_structure/structure_inventory_calculator.py`
  - `modules/wallet_structure/distribution_progress_calculator.py`
- 测试：`tests/test_structure_state_calculators.py`
- 禁止：把库存充足或派发未完成直接翻译成买入信号。

### Layer 7：继续推进 / 二段扩张动机层（核心）

- 输入：成本偏离、库存剩余、派发未完成、流动性需求、控盘匹配、对手盘压力。
- 输出：
  - `markup_motivation_score`
  - `markup_motivation_status_zh`
  - `markup_motivation_notes_zh`
- 代码：`modules/wallet_structure/markup_motivation_calculator.py`
- 测试：`tests/test_markup_motivation_calculator.py`
- 禁止：输出“必拉 / 必砸 / 买点”。

### Layer 8：对手盘压力层

- 输入：晚期大额买入、接盘鲸鱼、散户化、早晚期转移、浮亏晚持钱包。
- 输出：`counterparty_pressure_score`、`counterparty_pressure_status_zh`、`counterparty_pressure_profile_zh`。
- 代码：`modules/wallet_structure/counterparty_pressure_calculator.py`
- 测试：`tests/test_counterparty_pressure_calculator.py`

### Layer 9：钱包 × 盘型匹配层

- 输入：成本区、价格结构、库存状态、派发进度、钱包行为。
- 输出：`pattern_type_zh`、`cost_pattern_match_score`、`wallet_behavior_match_score`、`alignment_status_zh`。
- 代码：`modules/wallet_structure/wallet_pattern_cost_alignment_calculator.py`
- 测试：`tests/test_counterparty_pressure_calculator.py`

### Layer 10：主导侧生命周期层

- 输入：集群、成本、库存、派发、对手盘、盘型匹配。
- 输出：生命周期阶段假设。
- 代码：`modules/wallet_structure/token_cluster_analyzer.py::infer_dominant_lifecycle`
- 测试：`tests/test_token_cluster_analyzer.py`

### Layer 11：wallet_structure_decision 输出层

- 输入：事实层、量化层、行为推断层、冲突说明。
- 输出：结构情报交接对象、原因码、证据等级、风险等级、下一步建议。
- 注意：这里的 decision 是结构情报交接，不是交易执行指令。

## 3. 当前代码落地映射

- 成本区：`modules/wallet_structure/dominant_cost_zone_calculator.py`
- 数据模型：`modules/wallet_structure/quantitative_structure_models.py`
- 库存：`modules/wallet_structure/structure_inventory_calculator.py`
- 派发：`modules/wallet_structure/distribution_progress_calculator.py`
- 动机：`modules/wallet_structure/markup_motivation_calculator.py`
- 对手盘：`modules/wallet_structure/counterparty_pressure_calculator.py`
- 盘型匹配：`modules/wallet_structure/wallet_pattern_cost_alignment_calculator.py`
- 生命周期 / 意图：`modules/wallet_structure/token_cluster_analyzer.py`
- 聚合报告：`modules/wallet_structure/quantitative_aggregator.py`

## 4. 验收命令

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_dominant_cost_zone_calculator.py -q
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_quantitative_aggregator.py tests/test_dominant_cost_zone_calculator.py tests/test_markup_motivation_calculator.py tests/test_token_cluster_analyzer.py tests/test_counterparty_pressure_calculator.py -q
```

## 5. 输出目录规则

- Intel Bot 运行期输出默认放在：`data/gmgn_candidates_live_run/intel-bot/logs/`
- 定量结构报告默认放在：`data/gmgn_candidates_live_run/intel-bot/logs/quantitative_structure/<token_address>/`
- 文档和方法论放在：`docs/intel_bot/`
- 代码放在：`modules/wallet_structure/`
- 测试放在：`tests/`

## 6. 最终原则

底层系统设计必须按顺序执行：先事实、再标准化、再成本/库存/派发/动机/对手盘量化、再行为假设、最后总控汇总。任何行为判断都必须能回指到事实字段、量化字段和冲突说明。
