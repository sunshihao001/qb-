# SIKK Stable Trader OS — System Methodology Blueprint v2.0

> Status: `METHODOLOGY_BLUEPRINT_READY`
> Runtime boundary: `OBSERVE_PAPER_ONLY`
> Source material: `stable_trader_os_v2_0_design_doc_20260511`
> Generated from: uploaded Markdown design document, preserved and registered under `00_methodology/materials/`.

## 0. 总定位

SIKK Stable Trader OS 不是“寻找交易机会”的预测器，而是由 HER 调度的结构化交易研究控制系统。

系统目标不是让 AI 直接判断“买不买”，而是把候选 token 样本通过事实校验、场景识别、钱包结构、筹码控制、策略门禁、风险否定、纸面验证、复盘归因和规则升级，逐层过滤、审计、验证和沉淀。

核心原则：

- 系统输出状态，不输出自由文本买卖判断。
- 系统执行受控判断链，不执行无约束实盘。
- 每个判断必须有字段来源、证据、反证、置信度、失效条件。
- 每个阶段必须有验收门与 `handoff_packet`。
- 复盘只能生成规则升级建议，不直接污染实时规则。

## 1. 系统底层方法论

### 1.1 控制论模型

系统是控制系统，不是预测器。

```text
输入信号 → 状态识别 → 控制判断 → 风险约束 → 输出动作 → 反馈校准
```

映射到 SIKK：

```text
候选 token
  → P01 事实层校验
  → P02 市场场景识别
  → P03 钱包结构判断
  → P04 筹码控制判断
  → P05 策略门禁
  → P06 风险否定
  → P07 纸面执行 / 人工确认
  → P08 复盘归因
  → P09 规则升级提案
```

控制论验收：任何阶段不能绕过上游状态、验收门、hard negative 与 handoff。

### 1.2 OODA 模型

- Observe：P01 数据事实层
- Orient：P02 市场场景层 / P03 钱包结构层 / P04 筹码控制层
- Decide：P05 策略门禁层 / P06 风险控制层
- Act：P07 执行隔离层
- Feedback：P08 复盘学习层 / P09 系统自升级层

约束：P01-P04 不负责买入结论；P05-P06 只裁决是否允许进入纸面验证或人工确认；P07 不允许绕过 P05/P06。

### 1.3 V-Model 验证模型

每一个设计必须有对应验证：

- 系统目标 → 系统验收报告
- 阶段目标 → 阶段验收门
- 输入字段 → 字段校验
- 输出合约 → Contract 校验
- 判断规则 → Replay 样例
- Atomic Skill → Skill 测试
- 策略门禁 → 纸面交易验证
- 规则升级 → 审计日志

没有验证机制的设计不能进入正式系统；没有 replay 的判断只能作为研究假设；没有 handoff 的阶段不能进入下游。

### 1.4 STAMP / STPA 控制失效模型

系统不只看结果是否亏损，更要识别控制为什么失效。

典型控制失效：

- P01 字段缺失但仍进入 P02。
- P03 钱包证据弱但仍进入 P04。
- P04 已出现主动派发但 P05 放行。
- P06 风险拒绝但 P07 执行。
- P08 复盘结论直接改实时规则。

每个阶段必须定义：错误放行损害、必须阻断的错误、硬否定条件、证据不足降级条件。

### 1.5 数据血缘模型

所有判断必须追溯字段来源。

必备产物：

- `field_source_map`
- `evidence_chain`
- `counter_evidence`
- `decision_trace`
- `invalidation_conditions`

禁止 AI 推测补全事实字段。缺失字段只能标记 `missing`、`gap`、`degraded` 或 `blocked`。

### 1.6 领域驱动设计模型

先定义领域对象，再定义阶段。

核心对象：

- `Token`：候选代币。
- `Wallet`：钱包地址行为分析对象。
- `AddressGroup`：同源组、结构组、资金路径组。
- `TransactionEvent`：买入、卖出、转账、归集等事件。
- `MarketScene`：吸筹、拉升、派发、反抽、二段扩张等场景。
- `ChipState`：筹码集中、迁移、派发、失控。
- `DominantSide`：疑似结构侧 / 控盘侧行为假设。
- `Counterparty`：接盘鲸鱼、散户、分发接收方等对手盘。
- `GateDecision`：`BLOCK` / `PAUSE` / `WATCH` / `PAPER_READY` / `READY_FOR_CONFIRMATION`。
- `RiskEvent`：安全、流动性、报价、执行、熔断风险。
- `PaperPosition`：纸面交易验证记录。
- `ReviewCase`：成功 / 失败 / 误判样本。
- `RuleChange`：规则升级候选。
- `EvidenceBundle`：证据、反证、字段来源、置信度与失效条件集合。
- `HandoffPacket`：阶段交接最小机器包。

每个对象必须具备唯一 ID、字段来源、当前状态、证据链、反证项、下游用途和更新时间。

### 1.7 状态机模型

系统核心输出是状态。

主状态流：

```text
TOKEN_DISCOVERED
  → FACT_READY
  → SCENE_CLASSIFIED
  → WALLET_ANALYZED
  → CHIP_STATE_ANALYZED
  → STRATEGY_BLOCK / STRATEGY_PAUSE / STRATEGY_WATCH / PAPER_READY
  → RISK_REJECTED / RISK_APPROVED
  → PAPER_OPEN / READY_FOR_CONFIRMATION
  → PAPER_CLOSED
  → REVIEWED
  → RULE_UPDATE_PROPOSED
```

HER 的职责是读取状态、调用阶段、生成证据、更新状态、输出 handoff，而不是自由写判断。

### 1.8 决策情报模型

每个结论必须包含：

- decision
- evidence
- counter_evidence
- confidence
- invalidation_conditions
- next_action
- source_fields
- audit_ref

标准决策不能单独存在，必须绑定 `decision_trace` 与 `field_source_map`。

### 1.9 闭环学习模型

P08 负责归因：错误类型、错误来源阶段、错误字段、错误判断规则、是否需要新增硬否定、是否需要新增字段、是否需要升级 Skill。

P09 负责把归因转成：规则升级提案、Skill 升级计划、字段补充建议、审计日志、人工确认或版本切换候选。

禁止未审计规则自动生效，禁止一次失败直接修改核心参数。

## 2. 九大系统平面

### 2.1 治理平面

回答系统为什么存在、允许做什么、禁止做什么、当前是研究/纸面/实盘哪种模式。

核心产物：`system_manifest.yaml`、`global_building_principles.md`、`forbidden_action_policy.yaml`、`risk_boundary_policy.yaml`。

### 2.2 领域平面

回答系统处理哪些对象以及对象关系。

核心产物：`domain_object_registry.yaml`、`field_dictionary.yaml`、`state_dictionary.yaml`、`entity_relationship_map.md`。

### 2.3 数据平面

回答数据来源、字段标准化、事实/推理字段边界、缺失字段处理。

核心产物：`source_registry.yaml`、`input_contracts/`、`field_source_maps/`、`normalized_fact_models/`、`data_quality_report.md`。

### 2.4 控制平面

回答阶段如何走、谁能调用谁、什么状态允许进入下一阶段。

核心产物：`phase_registry.yaml`、`phase_transition_map.yaml`、`handoff_policy.yaml`、`acceptance_policy.yaml`、`current_system_state.json`。

### 2.5 决策平面

回答阶段如何判断、证据/反证/置信度/失效条件如何记录。

核心产物：`decision_rule_registry.yaml`、`evidence_registry.yaml`、`counter_evidence_registry.yaml`、`invalidation_policy.yaml`、`decision_trace_schema.json`。

### 2.6 风险平面

回答哪些情况必须否定，哪些风险不能被解释绕过。

核心产物：`hard_negative_registry.yaml`、`risk_gate_policy.yaml`、`execution_risk_policy.yaml`、`safety_filter_policy.yaml`。

### 2.7 执行平面

回答系统调用什么工具、如何运行、如何失败恢复。

核心产物：`tool_registry.yaml`、`runner_protocol.md`、`runtime_log_schema.json`、`error_recovery_policy.md`。

### 2.8 验证平面

回答如何证明输出合格、如何 replay、如何测试。

核心产物：`schemas/`、`contracts/`、`replay_fixtures/`、`acceptance_reports/`、`test_results/`。

### 2.9 学习平面

回答复盘如何进入规则升级，哪些结论能改规则，哪些只能观察。

核心产物：`failure_attribution/`、`review_reports/`、`rule_upgrade_proposals/`、`skill_upgrade_logs/`。

## 3. P00-P09 阶段职责

- P00_system_boundary：定义系统目标、运行模式、允许事项、禁止事项，输出边界与 handoff。
- P01_data_fact：把上游原始数据转成标准事实层，输出字段来源、事实表、缺口与 handoff。
- P02_market_scene：识别 token 市场场景，输出场景证据、反证、失效条件与 handoff。
- P03_wallet_structure：识别钱包角色、同源组、结构地址、资金路径和历史复现地址。
- P04_chip_control：判断筹码是否仍在结构侧、是否出现派发/迁移/失控/对手盘增强。
- P05_strategy_gate：裁决是否允许进入纸面验证或人工确认；不是直接买入。
- P06_risk_control：处理安全、流动性、滑点、报价偏差、亏损限制、熔断条件。
- P07_execution：执行隔离、纸面交易、人类确认；禁止无约束自动实盘。
- P08_review：对纸面交易、失败样本、错误判断、遗漏机会进行归因。
- P09_self_upgrade：把复盘结果转成可审计的规则升级建议，默认 shadow/manual review。

## 4. P00-P09 × 九大平面矩阵

强度定义：`强` = 本阶段主责任；`中` = 必须读取或写入；`弱` = 边界约束或下游引用。

- P00 系统边界: 治理强 / 领域中 / 数据弱 / 控制强 / 决策弱 / 风险强 / 执行弱 / 验证中 / 学习弱
- P01 数据事实: 治理中 / 领域强 / 数据强 / 控制中 / 决策弱 / 风险中 / 执行中 / 验证强 / 学习弱
- P02 市场场景: 治理弱 / 领域强 / 数据强 / 控制中 / 决策强 / 风险中 / 执行中 / 验证强 / 学习中
- P03 钱包结构: 治理弱 / 领域强 / 数据强 / 控制中 / 决策强 / 风险强 / 执行中 / 验证强 / 学习中
- P04 筹码控制: 治理弱 / 领域强 / 数据强 / 控制强 / 决策强 / 风险强 / 执行中 / 验证强 / 学习中
- P05 策略门禁: 治理强 / 领域中 / 数据中 / 控制强 / 决策强 / 风险强 / 执行中 / 验证强 / 学习中
- P06 风控: 治理强 / 领域中 / 数据中 / 控制强 / 决策强 / 风险强 / 执行强 / 验证强 / 学习中
- P07 执行隔离: 治理强 / 领域中 / 数据中 / 控制强 / 决策中 / 风险强 / 执行强 / 验证强 / 学习中
- P08 复盘: 治理中 / 领域强 / 数据强 / 控制中 / 决策强 / 风险中 / 执行中 / 验证强 / 学习强
- P09 自升级: 治理强 / 领域强 / 数据中 / 控制强 / 决策强 / 风险强 / 执行中 / 验证强 / 学习强

## 5. 系统状态机

### 5.1 系统状态

`SYSTEM_BUILDING` → `SYSTEM_READY` / `SYSTEM_WITH_GAPS` / `SYSTEM_BLOCKED` → `SYSTEM_RUNNING` → `SYSTEM_PAUSED` / `SYSTEM_REVIEWING` / `SYSTEM_UPGRADING`。

### 5.2 阶段状态

`PHASE_NOT_STARTED` → `PHASE_RUNNING` → `PHASE_READY` / `PHASE_WITH_GAPS` / `PHASE_PAUSED` / `PHASE_REJECTED` / `PHASE_ERROR`。

### 5.3 钱包结构状态

`WALLET_SUPPORT` / `WALLET_NEUTRAL` / `WALLET_PAUSE` / `WALLET_BLOCK`。

### 5.4 筹码控制状态

`CHIP_CONTROL_RETAINED` / `CHIP_CONTROL_WEAKENING` / `CHIP_TRANSFER_ACTIVE` / `DISTRIBUTION_ACTIVE` / `COUNTERPARTY_DOMINANT` / `CONTROL_COLLAPSED`。

### 5.5 策略门禁状态

`STRATEGY_BLOCK` / `STRATEGY_PAUSE` / `STRATEGY_WATCH` / `PAPER_READY` / `READY_FOR_CONFIRMATION`。

### 5.6 执行状态

`PAPER_ONLY` / `PAPER_OPEN` / `PAPER_CLOSED` / `HUMAN_CONFIRMATION_REQUIRED` / `LIVE_DISABLED` / `LIVE_GATE_LOCKED`。

## 6. 数据流、判断流、风险硬否定流、Handoff 流

### 6.1 数据流

```text
候选 token 输入
  → P01 输入快照
  → 字段来源映射
  → 标准事实表
  → 场景识别输入
  → 钱包结构输入
  → 筹码控制输入
  → 策略门禁输入
  → 风险控制输入
  → 纸面执行输入
  → 复盘输入
```

### 6.2 判断流

```text
事实是否足够？
  → 市场场景是什么？
  → 钱包结构是否支持？
  → 筹码控制是否保留？
  → 主导侧是否仍有行为动机？
  → 是否存在强反证？
  → 策略门禁是否允许？
  → 风险是否否定？
  → 是否进入纸面验证？
```

### 6.3 风险硬否定流

硬否定高于所有解释。一旦命中，不允许用“但是、可能、也许、这次特殊”继续放行。

全局硬否定：字段来源不明、关键时间戳缺失、token/wallet 主键缺失、schema/contract 校验失败、report 与 JSON 冲突、AI 推测补全事实字段、无 handoff_packet 进入下游、未检查反证直接通过、硬否定命中但仍输出 READY。

交易判断硬否定：安全扫描失败、报价源严重偏差、流动性不足、滑点不可控、早期结构钱包同步退出、主动派发明确、接盘鲸鱼压力过高、筹码控制权崩塌、P01 事实字段不足、P05 策略证据不足、P06 风控拒绝。

执行层硬否定：未通过 P05/P06、未生成 execution_ticket、未记录模拟成交价、未定义止损/失效条件、触发连续失败熔断、触发当日最大亏损限制。

### 6.4 Handoff 流

每个阶段必须输出：`summary.json`、`evidence.json`、`counter_evidence.json`、`gap_list.json`、`decision_trace.json`、`report.md`、`handoff_packet.json`、`runtime_log.jsonl`。

`handoff_packet` 必须包含：`phase_id`、`phase_status`、`input_files`、`output_files`、`decision`、`evidence_level`、`gap_list`、`hard_negative_hits`、`counter_evidence`、`next_phase_allowed`、`next_phase_id`、`generated_at`。

## 7. Replay / Review / Upgrade 流

```text
paper/replay fixture
  → 阶段输出重放
  → 验收门复验
  → 失败归因
  → rule_adjustment_candidate
  → upgrade_proposal
  → regression/shadow/rollback plan
  → manual approval / version switch
```

规则：P08 只归因，P09 只生成升级包；默认 `allow_apply_to_runtime=false`、`requires_manual_confirmation=true`。

## 8. Atomic Skill 抽取原则与第一批清单

Atomic Skill 不是阶段本身，而是跨阶段复用的能力单元。

Skill 化条件：

- 跨 2 个以上阶段复用。
- 输入输出稳定。
- 判断逻辑明确。
- 反证规则清楚。
- 可单独测试。
- 可被 HER 多次调用。
- 后续可能接代码工具。

第一批候选：

- `field_source_audit_skill`
- `hard_negative_filter_skill`
- `time_context_skill`
- `token_lifecycle_skill`
- `market_scene_recognition_skill`
- `wallet_role_classification_skill`
- `same_source_group_skill`
- `fund_flow_skill`
- `chip_distribution_skill`
- `dominant_side_lifecycle_skill`
- `dominant_side_intent_skill`
- `counterparty_pressure_skill`
- `strategy_gate_skill`
- `risk_gate_skill`
- `explanation_report_skill`
- `failure_attribution_skill`
- `rule_upgrade_skill`

限制：Atomic Skill 不能输出 `buy_now`、`sell_now`、`auto_trade`、`real_trade_allowed`、`final_trade_state`。

## 9. HER 执行协议

HER 每次执行必须按以下顺序：

1. 读取治理平面：允许事项、禁止事项、运行模式。
2. 读取运行状态：active_phase、blocking_gap、completed_phases、next_action。
3. 读取控制平面：阶段顺序、输入输出、进入下一阶段条件。
4. 读取领域平面：对象、字段、状态定义。
5. 读取数据平面：输入文件、字段来源、数据质量。
6. 读取风险平面：hard negative、暂停/拒绝条件。
7. 读取决策平面：规则、证据、反证、置信度、失效条件。
8. 执行阶段任务：调用 Atomic Skill / 工具，写 runtime log。
9. 读取验证平面：schema、contract、acceptance gate。
10. 写入交接：handoff packet、phase state、current system state。
11. 进入学习平面：复盘、归因、规则升级提案。

禁止：不读状态直接执行、不读阶段边界直接推理、不查硬否定直接放行、无 handoff 进入下游、用 report 代替机器状态、用 AI 推测补全事实字段。

## 10. 下一步落地顺序


现在 SIKK Stable Trader OS / HER 的系统建设顺序固定为：

1. 第一步：建立 `system_methodology_blueprint.md`。
2. 第二步：建立 `K00_knowledge_intake_taskization_controller`。
3. 第三步：更新总控 Skill，加入“文档输入必须任务化”规则。
4. 第四步：建立 `P00_system_boundary`。
5. 第五步：建立 `P01_data_fact`。
6. 第六步：建立 `P02-P09` 阶段控制器。
7. 第七步：建立 Atomic Skill。
8. 第八步：接入工具 / schema / contract / replay。
9. 第九步：跑纸面交易与复盘。
10. 第十步：进入规则升级闭环。

顺序约束：K00 必须位于 P00 之前；总控 Skill 的文档输入任务化规则必须位于 P00/P01/P02-P09 执行之前；纸面交易与复盘必须位于工具/schema/contract/replay 接入之后；规则升级闭环必须基于复盘结果，而不是基于聊天上下文。


## 11. 本蓝图验收门

- 已覆盖 9 个方法论模型。
- 已覆盖 9 个系统平面。
- 已覆盖核心领域对象。
- 已覆盖 P00-P09 职责。
- 已覆盖 P00-P09 × 九平面矩阵。
- 已覆盖系统状态机。
- 已覆盖数据流、判断流、风险硬否定流、handoff 流。
- 已覆盖 replay/review/upgrade 流。
- 已覆盖 Atomic Skill 抽取原则与第一批清单。
- 已覆盖 HER 执行协议与下一步落地顺序。
- 已保留纸面/观察边界，不授权实盘、签名、broadcast、swap。

## 13. 更新后的系统建设顺序

现在 SIKK Stable Trader OS / HER 的系统建设顺序固定为：

1. 第一步：建立 `system_methodology_blueprint.md`。
2. 第二步：建立 `K00_knowledge_intake_taskization_controller`。
3. 第三步：更新总控 Skill，加入“文档输入必须任务化”规则。
4. 第四步：建立 `P00_system_boundary`。
5. 第五步：建立 `P01_data_fact`。
6. 第六步：建立 `P02-P09` 阶段控制器。
7. 第七步：建立 Atomic Skill。
8. 第八步：接入工具 / schema / contract / replay。
9. 第九步：跑纸面交易与复盘。
10. 第十步：进入规则升级闭环。

顺序约束：K00 必须位于 P00 之前；总控 Skill 的文档输入任务化规则必须位于 P00/P01/P02-P09 执行之前；纸面交易与复盘必须位于工具/schema/contract/replay 接入之后；规则升级闭环必须基于复盘结果，而不是基于聊天上下文。

## 14. 本次版本更新的核心结论

HER 输入文档 / 知识资料时，不能再当作普通文档阅读。

必须新增 K00 知识资料摄取与任务化控制器。

K00 的作用是把所有输入资料变成：

- 原始资料保存
- 文档护照
- 系统平面映射
- 阶段映射
- 缺口识别
- 阶段任务执行包
- `phase_state`
- `acceptance_gate`
- `handoff_packet`

这样 HER 才能不依赖聊天上下文，而是依赖系统数据执行长任务。

### 本次认知升级点

1. 上传资料不是普通文档，而是系统建设输入。
2. HER 不能只读文档、总结文档，必须先保存和任务化。
3. 必须新增 K00 知识摄取与任务化控制器。
4. Phase Controller 必须是阶段运行单元，不是阶段说明文档。
5. 每个阶段必须有 9 个核心文件：manifest、context、objective_tree、input_contract、output_contract、execution_protocol、acceptance_gate、state、handoff_schema。
6. HER 长任务不能完成一个阶段就停，必须通过 acceptance_gate 决定是否进入下一阶段。
7. 系统不能依靠上下文，必须依靠文件化系统数据、状态回写和 handoff。

### 版本边界

本次更新是 HER / SIKK Stable Trader OS 的系统建设顺序与知识输入治理升级，不授权真实交易执行、签名、broadcast、swap 或私钥材料处理。K00 只负责知识资料资产化、任务化、验收与交接。
