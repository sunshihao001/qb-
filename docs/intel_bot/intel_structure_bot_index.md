# Intel Structure Bot 总索引

## 1. 索引目标

本文档把新增的“疑似主导侧成本区与量化结构推断层”串成一条清晰的只读结构链路，供后续实现、复核与门禁交接使用。

## 2. 总体定位

Intel Structure Bot / Intel Bot 是结构情报与筹码分析 Bot，只负责结构判断，不负责交易决策。

代币 holder 集群分析、钱包结构、筹码结构、同源执行组、资金路径、对手盘压力、主导侧生命周期、主导侧行为动机推断、钱包 × 盘型匹配都归入 Intel Bot；专业表达中不使用“庄家心理”，统一称为“主导侧行为动机推断”。

它要回答的是：
- 疑似主导侧筹码是否仍在
- 疑似主导侧成本区在哪里
- 当前价格相对成本处于什么位置
- 结构侧筹码库存还剩多少
- 派发是否已经推进到什么阶段
- 是否仍有继续推进、二段扩张或控盘维护动机
- 当前是否更像把筹码转给了对手盘
- 钱包行为和盘型是否匹配

最终交给 Strategy Gate Bot 做风险收益比筛选。

## 3. 模块链路

### 3.1 上游事实层
- `wallet_source_reader`
- `wallet_normalized_adapter`
- `wallet_entity_profiler`
- `current_token_behavior_analyzer`
- `same_source_group_analyzer`
- `chip_transfer_analyzer`
- `historical_wallet_profiler`

### 3.2 量化结构层
- `dominant_cost_zone_calculator`
- `structure_inventory_estimator`
- `distribution_progress_estimator`
- `markup_motivation_model`
- `counterparty_pressure_quant_model`
- `wallet_pattern_cost_alignment`

### 3.3 汇总层
- `quantitative_structure_report`
- `wallet_structure_decision`
- `gmgn_note_exporter`

## 4. 量化输出文件

本阶段新增的标准输出文件如下：

Intel Bot 专属数据目录：
- `data/gmgn_candidates_live_run/intel-bot/`
  - `code/`
  - `logs/`

运行期交付路径统一落在 `intel-bot/logs/` 下：
- `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/wallet_structure_decision.json`
- `data/gmgn_candidates_live_run/intel-bot/logs/chip/<token>/chip_transfer_decision.json`
- `data/gmgn_candidates_live_run/intel-bot/logs/lifecycle/<token>/dominant_lifecycle_decision.json`
- `data/gmgn_candidates_live_run/intel-bot/logs/intent/<token>/dominant_intent_decision.json`
- `data/gmgn_candidates_live_run/intel-bot/logs/reports/<token>/wallet_report.md`

shared 目录只作为跨 Bot 交接镜像，不作为 Intel Bot 主数据目录：
- `shared/decisions/wallet_structure/<token>/wallet_structure_decision.json`
- `shared/decisions/chip/<token>/chip_transfer_decision.json`
- `shared/decisions/lifecycle/<token>/dominant_lifecycle_decision.json`
- `shared/decisions/intent/<token>/dominant_intent_decision.json`
- `shared/reports/wallet/<token>/wallet_report.md`

当前本地研究合同与量化输出文件：

- `dominant_cost_zone.json`
- `structure_inventory_estimate.json`
- `distribution_progress.json`
- `markup_motivation.json`
- `counterparty_pressure_quant.json`
- `wallet_pattern_cost_alignment.json`
- `quantitative_structure_report.md`

## 5. 字段与状态约束

### 5.1 字段约束
- JSON key 可以英文。
- 所有对外判断 value 必须中文化。
- 所有状态字段必须带中文解释。
- 缺失值必须保留 `null` 或 `未知`，不能编造。

### 5.2 语言约束
- 不直接使用“庄家成本”。
- 不直接输出“庄家一定要拉”。
- 不给买点。
- 不输出实盘建议。

## 6. 结构判断顺序

推荐顺序：
1. 先算疑似主导侧成本区
2. 再算结构侧筹码库存
3. 再算派发进度
4. 再算继续推进动机
5. 再算对手盘压力
6. 最后算钱包行为与盘型匹配度

这个顺序的目的，是先确认“结构还在不在”，再判断“结构想做什么”，最后再把解释交给 Strategy Gate Bot。

## 7. Strategy Gate Bot 交接边界

Intel Structure Bot 只输出结构判断，不负责：
- 参与点选择
- 风险收益比筛选
- 状态机写入
- 直接 `PAPER_READY`
- 直接 `BLOCKED`
- 开仓
- 止损
- 止盈
- 实盘执行
- paper runner 触发

Strategy Gate Bot 负责消费这些结构判断，并决定是否进入下一层门禁。

## 8. 最小字段集合

建议最小交付对象如下：
- `dominant_cost_zone`
- `structure_inventory_estimate`
- `distribution_progress`
- `markup_motivation`
- `counterparty_pressure`
- `wallet_pattern_cost_alignment`
- `summary_zh`

## 9. 交付原则

- 所有判断必须有证据来源。
- 所有状态必须中文化。
- 所有解释必须可复核。
- 所有输出必须保持只读。

## 10. 结论

这套索引把“成本区、库存、派发、动机、压力、盘型匹配”统一为一个可交接、可审计、可扩展的量化结构层，供 Strategy Gate Bot 使用。
