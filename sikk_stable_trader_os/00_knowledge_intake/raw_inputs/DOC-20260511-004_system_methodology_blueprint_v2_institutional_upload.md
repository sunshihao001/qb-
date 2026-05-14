下面这版是 **`system_methodology_blueprint.md` 专业机构化 v2.0**。它不是说明文档，而是 HER / P00 必须读取的 **系统建造方法论总宪法**。

建议保存路径：

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_methodology/system_methodology_blueprint.md
```

---

````markdown
# SIKK Stable Trader OS 系统方法论蓝图

文件编号：METHODOLOGY-BLUEPRINT-002  
文件名称：system_methodology_blueprint.md  
版本：v2.0-institutional-system-build  
状态：AUTHORITATIVE_SYSTEM_BUILD_BLUEPRINT  
适用系统：SIKK Stable Trader OS  
适用执行器：HER / Hermes / Phase Controller / Runner / Validator  
安全边界：paper-only，禁止真实交易自动执行  
上游来源：K00_knowledge_intake_taskization  
首要消费者：P00_system_bootstrap_controller  
下游消费者：Governance Plane / Domain Plane / Data Plane / Control Plane / P01-P10  
最后更新：2026-05-11  

---

# 0. 文件定位

`system_methodology_blueprint.md` 不是普通说明文档。

它是 SIKK Stable Trader OS 的系统建造方法论蓝图，是 HER 在建立系统体系时必须优先读取的权威文件。

它的作用不是直接判断某个 token 是否可以买，不是直接生成交易策略，也不是直接运行自动化交易。

它的作用是定义：

1. 系统如何理解目标。
2. 系统如何把知识资料转成系统资产。
3. 系统如何把系统资产转成阶段控制器候选。
4. 系统如何把阶段控制器候选编译成正式 Phase Controller。
5. 系统如何建立治理平面、领域平面、数据平面、控制平面。
6. 系统如何建立输入合约、输出合约、验收门、状态回写和下游交接。
7. 系统如何防止“文档存在但系统未消费”。
8. 系统如何防止“任务包存在但 runner 未执行”。
9. 系统如何防止“文件级验收通过但语义未落实”。
10. 系统如何保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

本文件必须被 P00 系统建造控制器消费。

如果本文件存在但未被 P00 消费，则系统状态必须标记为：

```text
METHODOLOGY_BLUEPRINT_CREATED_NOT_CONSUMED
````

如果本文件被 P00 消费但未生成控制平面，则系统状态必须标记为：

```text
METHODOLOGY_CONSUMED_CONTROL_PLANE_MISSING
```

如果本文件被 P00 消费，并生成控制平面、阶段注册表、资产索引、追踪矩阵和验收体系，则系统状态可标记为：

```text
METHODOLOGY_COMPILED_TO_SYSTEM_STRUCTURE
```

---

# 1. 系统总目标

SIKK Stable Trader OS 不是单纯寻找交易机会的系统。

它的本质是：

```text
从所有看起来像机会的 token、钱包结构、K 线结构、筹码结构和市场行为中，
连续剔除低质量样本、错误场景样本、假成交样本、派发风险样本、疲劳拖延样本、错误位置样本和执行风险样本，
只保留极少数证据链未被否定、风险收益比可被纸面验证的结构样本。
```

系统核心目标不是预测上涨，而是建立：

```text
事实采集
  ↓
字段标准化
  ↓
结构还原
  ↓
主导侧筹码控制权判断
  ↓
场景识别
  ↓
反证与硬否定过滤
  ↓
策略门禁
  ↓
纸面交易验证
  ↓
失败归因
  ↓
规则升级
```

系统的专业目标是：

```text
将主观交易判断转化为可追踪、可验收、可复盘、可升级的结构化判断系统。
```

---

# 2. 系统基本认知

系统必须始终遵守以下认知：

```text
文件存在 ≠ 系统接入
任务包存在 ≠ runner 执行
阶段说明存在 ≠ Phase Controller 存在
锚点验收通过 ≠ 语义落实
局部阶段完成 ≠ 全局状态一致
文档资产化 ≠ 下游消费
AI 理解 ≠ 系统结构落地
字段存在 ≠ 字段质量合格
证据存在 ≠ 证据等级足够
没有反证记录 ≠ 没有风险
paper 盈利 ≠ 规则有效
一次成功 ≠ 策略成立
```

系统的默认姿态不是寻找买点，而是：

```text
先证明不应该做。
如果无法否定，再进入 paper-only 验证。
```

---

# 3. HER 底层执行逻辑

HER 不能把用户聊天上下文当作系统状态源。

HER 在执行任何任务前，必须按以下顺序判断：

```text
1. 读取 system_methodology_blueprint.md
2. 读取 current_system_state.json
3. 读取 phase_registry.yaml
4. 判断当前请求属于哪个阶段
5. 判断当前阶段是否合法
6. 校验输入合约
7. 校验上游 handoff
8. 校验资产是否已登记
9. 校验资产是否已被消费
10. 执行阶段任务树
11. 生成阶段输出
12. 执行验收门
13. 写入状态回写
14. 写入 trace matrix
15. 写入 handoff packet
16. 裁决下一合法阶段
```

如果 `current_system_state.json` 不存在，则系统状态为：

```text
CONTROL_PLANE_MISSING
```

此时禁止进入 P01-P10 业务阶段。

如果 `phase_registry.yaml` 不存在，则系统状态为：

```text
PHASE_REGISTRY_MISSING
```

此时禁止任何业务阶段运行。

如果 Data Plane 未通过验收，则 P01 必须保持：

```text
BLOCKED_BY_DATA_PLANE
```

---

# 4. 系统建造总链路

系统建造必须按以下顺序：

```text
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md：系统方法论蓝图
  ↓
P00：系统建造与方法论编译控制器
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Control Plane：控制平面
  ↓
Trace Plane：追踪平面
  ↓
Acceptance Plane：验收平面
  ↓
Handoff Plane：交接平面
  ↓
P01-P10 Phase Controller：业务阶段控制器
  ↓
Runner / Tool Binding：执行工具绑定
  ↓
Paper-only Runtime：纸面验证运行
  ↓
Review / Upgrade：复盘与升级
```

禁止顺序：

```text
K00 → P01
K00 → 自动交易
文档 → 直接判断
方法论 → 直接跑交易
旧脚本 → 直接并入正式系统
paper runner → 绕过策略门禁
复盘结果 → 直接修改实时规则
```

---

# 5. 系统平面总表

系统必须建立以下平面。

|平面|中文名称|核心职责|是否阻断 P01|
|---|---|---|---|
|Knowledge Plane|知识资产平面|保存、建档、索引、任务化输入资料|是|
|Methodology Plane|方法论平面|定义系统如何建造|是|
|Governance Plane|治理平面|定义权限、安全边界、硬否定规则|是|
|Domain Plane|领域平面|定义系统判断对象、关系、场景、问题树|是|
|Data Plane|数据平面|定义字段、来源、事实模型、缺失策略|是|
|Control Plane|控制平面|定义当前状态、阶段注册、任务裁决|是|
|Trace Plane|追踪平面|追踪方法论、资产、字段、阶段覆盖|是|
|Acceptance Plane|验收平面|定义文件级、结构级、语义级、消费级、运行级验收|是|
|Handoff Plane|交接平面|定义上游产物如何交给下游|是|
|Execution Plane|执行平面|runner、工具、CLI、验证脚本绑定|条件阻断|
|Review Plane|复盘平面|失败归因、错判分析、统计反馈|否|
|Upgrade Plane|升级平面|基于复盘证据升级字段、规则、阶段|否|

---

# 6. Phase Controller 核心定义

Phase Controller 不是阶段说明文档。

Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。

它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

任何阶段如果只有说明文档，但没有以下结构，不能被视为正式 Phase Controller：

```text
controller.yaml
context.md
input_contract.json
output_contract.json
task_tree.yaml
acceptance_gate.yaml
runner_binding.yaml
state_writeback_policy.yaml
handoff_packet.schema.json
```

正式 Phase Controller 必须回答：

```text
这个阶段负责什么？
不负责什么？
读取什么？
输出什么？
依赖谁？
下游是谁？
用什么工具？
如何验收？
失败如何处理？
如何回写状态？
如何交给下游？
```

---

# 7. K00 阶段方法论

## 7.1 K00 定位

K00 是知识摄取与 Phase Controller 候选任务化阶段。

K00 不只是保存文档。

K00 必须把输入资料转换为 P00 可消费的系统建造材料。

K00 的核心任务：

```text
输入资料
  ↓
知识资产
  ↓
document passport
  ↓
方法论要求抽取
  ↓
系统目标抽取
  ↓
阶段目标候选
  ↓
任务树候选
  ↓
输入合约候选
  ↓
输出合约候选
  ↓
Atomic Skill 候选
  ↓
代码工具 / runner 候选
  ↓
验收门候选
  ↓
状态回写候选
  ↓
handoff 候选
  ↓
phase_controller_candidate_spec
  ↓
k00_to_p00_handoff_packet
```

## 7.2 K00 禁止事项

K00 禁止：

```text
直接注册正式 Phase Controller
直接写入 phase_registry.yaml
直接裁决 P01 可以运行
直接启动 P01-P10
直接执行交易
把候选规格当作正式控制器
把文档存在当作系统消费完成
```

## 7.3 K00 必须输出

```text
00_knowledge_intake/raw_inputs/
00_knowledge_intake/passports/
00_knowledge_intake/methodology_extracts/
00_knowledge_intake/phase_controller_candidates/
00_knowledge_intake/handoff_packets/
00_knowledge_intake/gap_reports/
00_knowledge_intake/runtime/k00_runtime_state.json
```

核心文件：

```text
phase_controller_candidate_spec.yaml
k00_to_p00_handoff_packet.json
gap_report.json
document_passport.json
methodology_requirement_extract.yaml
```

---

# 8. P00 阶段方法论

## 8.1 P00 定位

P00 是系统建造与方法论编译控制器。

P00 是系统编译器。

它负责把 K00 候选资产和本方法论蓝图编译成正式系统结构。

P00 不做交易判断，不做钱包判断，不运行 P01，不做 paper trade。

P00 负责生成：

```text
Control Plane
Phase Registry
System Asset Index
Governance Plane
Domain Plane
Data Plane
Trace Matrix
Acceptance Policy
Handoff Registry
P01-P10 Controller Stub
```

## 8.2 P00 必须解决的问题

```text
方法论是否被消费？
K00 资产是否被消费？
阶段是否注册？
P01 是否被正确阻断？
治理平面是否存在？
领域平面是否存在？
数据平面是否存在？
控制平面是否存在？
trace matrix 是否存在？
handoff 是否注册？
下一合法阶段是什么？
```

## 8.3 P00 必须输出

```text
00_control/current_system_state.json
00_control/phase_registry.yaml
00_control/system_asset_index.json
00_control/task_consumption_log.json
00_control/current_blockers.json
00_control/next_stage_decision.json

00_trace/methodology_implementation_trace_matrix.yaml
00_trace/asset_consumption_matrix.yaml
00_trace/domain_to_data_trace_matrix.yaml
00_trace/data_to_phase_trace_matrix.yaml
00_trace/acceptance_coverage_matrix.yaml

08_acceptance/global_acceptance_policy.yaml
09_handoff/handoff_packet_registry.yaml
```

P00 完成后，P01 仍然不得直接进入 READY。

P01 的合法状态只能是：

```text
BLOCKED_BY_DATA_PLANE
```

或者在 Data Plane 通过后：

```text
READY_FOR_PREFLIGHT
```

---

# 9. Governance Plane 方法论

治理平面不是制度说明。

治理平面是系统权限、安全边界、硬否定规则和阶段裁决边界。

## 9.1 Governance Plane 必须回答

```text
什么阶段有裁决权？
什么阶段只能记录事实？
什么阶段可以生成判断？
什么阶段可以进入 paper？
什么阶段禁止执行交易？
什么条件触发硬否定？
什么条件必须回退？
什么条件必须降级为 UNKNOWN？
```

## 9.2 必须建立文件

```text
00_governance/governance_plane.md
00_governance/authority_boundary.yaml
00_governance/stage_permission_matrix.yaml
00_governance/hard_negative_rules.yaml
00_governance/risk_boundary.yaml
00_governance/real_trade_forbidden_policy.yaml
00_governance/review_to_upgrade_policy.yaml
```

## 9.3 核心治理规则

```text
paper_only = true
real_trade_enabled = false
P01 不得绕过 Data Plane
策略层不得读取未标准化原始数据直接裁决
执行层不得反向污染分析层
复盘层不得直接修改实时规则
真实交易必须保持禁用
任何阶段不得跳过 acceptance gate
任何阶段不得绕过 current_system_state.json
```

---

# 10. Domain Plane 方法论

领域平面不是概念说明。

领域平面是系统判断对象、关系、问题树、场景分类、钱包角色、主导侧生命周期、证据需求和反证模型的注册层。

## 10.1 Domain Plane 必须回答

```text
系统到底判断什么？
有哪些对象？
对象之间是什么关系？
每个对象有哪些状态？
每个判断需要哪些证据？
哪些证据支持？
哪些证据反驳？
哪些反证触发硬阻断？
哪些判断可以进入下游？
```

## 10.2 必须建立文件

```text
00_domain/domain_plane.md
00_domain/domain_object_registry.yaml
00_domain/domain_relation_graph.yaml
00_domain/domain_decision_question_tree.yaml
00_domain/scenario_taxonomy.yaml
00_domain/wallet_role_taxonomy.yaml
00_domain/dominant_side_lifecycle_taxonomy.yaml
00_domain/domain_to_data_demand_map.yaml
00_domain/domain_to_phase_map.yaml
00_domain/domain_acceptance_gate.yaml
```

## 10.3 领域对象注册表必须包含

```text
token
wallet
wallet_entity
same_source_group
funding_source
chip_cluster
early_wallet_group
dominant_side
counterparty_group
market_structure
scenario
strategy_candidate
execution_risk
paper_trade
review_case
upgrade_candidate
```

## 10.4 领域关系图必须表达

```text
wallet → belongs_to → wallet_entity
wallet_entity → may_form → same_source_group
same_source_group → may_control → chip_cluster
chip_cluster → affects → dominant_side_status
dominant_side_status → affects → scenario
scenario → constrains → strategy_gate
strategy_gate → controls → paper_permission
paper_trade_result → feeds → review_learning
review_learning → proposes → system_upgrade
```

## 10.5 场景分类必须包含

```text
吸筹
控盘箱体
第一次拉升
二段扩张
高位派发
下跌派发
诱多反抽
退出流动性陷阱
假横盘
再吸筹
末端拉盘派发
刷量假突破
接盘鲸鱼陷阱
死亡横盘
旧币再激活
```

每个场景必须定义：

```text
场景编号
场景名称
定义
必要正向证据
必要反向证据
硬阻断条件
兼容的钱包行为
冲突的钱包行为
市场结构要求
成交量要求
允许进入 paper 的条件
禁止进入 paper 的条件
失效条件
```

---

# 11. Data Plane 方法论

数据平面不是字段列表。

数据平面是把领域判断转成字段、来源、质量等级、证据等级、缺失策略和统一事实模型。

## 11.1 Data Plane 必须回答

```text
每个领域判断需要什么字段？
字段来自哪里？
字段质量如何判断？
字段缺失怎么办？
哪些字段缺失会阻断？
哪些字段缺失只降低置信度？
哪个阶段消费这个字段？
字段如何进入统一事实模型？
```

## 11.2 必须建立文件

```text
00_data/data_plane.md
00_data/field_source_map.yaml
00_data/normalized_fact_model.schema.json
00_data/data_input_contract.json
00_data/data_quality_rules.yaml
00_data/evidence_level_rules.yaml
00_data/contradiction_record_rules.yaml
00_data/missing_data_policy.yaml
00_data/data_handoff_packet.json
```

## 11.3 数据对象必须包含

```text
system_context
token_fact
wallet_fact
wallet_entity_fact
same_source_group_fact
chip_distribution_fact
fund_flow_fact
market_structure_fact
scenario_fact
strategy_gate_fact
execution_risk_fact
paper_trade_fact
review_fact
evidence_trace
contradiction_trace
handoff_context
```

## 11.4 字段来源图必须覆盖

```text
token_identity
market_cap_context
kline_volume_structure
wallet_identity
wallet_behavior
chip_distribution
same_source_group
fund_flow
quote_security
scenario_context
paper_trade_result
review_feedback
system_state
```

每个字段必须包含：

```text
field_name
field_name_cn
source_asset
source_module
required_by_phase
consumer_controller
evidence_level
quality_level
missing_policy
blocking_if_missing
status
```

---

# 12. Control Plane 方法论

控制平面是系统运行的唯一状态裁决层。

没有控制平面，系统不得进入任何业务阶段。

## 12.1 Control Plane 必须回答

```text
当前唯一权威阶段是什么？
哪些阶段被阻断？
阻断原因是什么？
哪些资产已登记？
哪些资产已消费？
哪些任务包已执行？
下一合法阶段是什么？
P01 是否允许运行？
系统是否仍 paper-only？
```

## 12.2 必须建立文件

```text
00_control/current_system_state.json
00_control/phase_registry.yaml
00_control/system_asset_index.json
00_control/task_queue.json
00_control/task_consumption_log.json
00_control/current_blockers.json
00_control/next_stage_decision.json
```

## 12.3 当前系统状态必须包含

```json
{
  "system_id": "SIKK_STABLE_TRADER_OS",
  "current_authoritative_stage": "",
  "blocked_stages": [],
  "block_reasons": {},
  "next_legal_stage": "",
  "paper_only": true,
  "real_trade_enabled": false,
  "p01_runtime_connection_allowed": false
}
```

---

# 13. Trace Plane 方法论

追踪平面用于证明系统不是只写了文件，而是真正被消费、覆盖、执行和验收。

## 13.1 必须建立文件

```text
00_trace/methodology_implementation_trace_matrix.yaml
00_trace/asset_consumption_matrix.yaml
00_trace/domain_to_data_trace_matrix.yaml
00_trace/data_to_phase_trace_matrix.yaml
00_trace/acceptance_coverage_matrix.yaml
00_trace/handoff_consumption_matrix.yaml
```

## 13.2 追踪关系必须覆盖

```text
methodology_requirement → implemented_by
knowledge_asset → consumed_by
domain_object → required_fields
field → consumer_phase
phase_output → downstream_handoff
acceptance_gate → acceptance_result
runner_output → state_writeback
paper_result → review_case
review_case → upgrade_candidate
```

---

# 14. Acceptance Plane 方法论

验收不能只看文件是否存在。

系统验收分为五级。

## 14.1 文件级验收

验证：

```text
文件是否存在
JSON/YAML 是否可解析
路径是否正确
```

## 14.2 结构级验收

验证：

```text
目录是否符合系统结构
阶段是否注册
字段是否有来源
输出是否有合约
handoff 是否存在
```

## 14.3 语义级验收

验证：

```text
方法论要求是否落实
领域对象是否注册
场景是否有证据与反证
数据字段是否服务于判断问题
Phase Controller 是否符合可调度定义
```

## 14.4 消费级验收

验证：

```text
上游资产是否被下游读取
task package 是否被 consumed_by 标记
handoff packet 是否被目标阶段消费
runner 是否执行了任务
trace matrix 是否更新
```

## 14.5 运行级验收

验证：

```text
状态是否回写
阶段是否推进
阻断是否生效
paper 结果是否产生
复盘是否进入 P09
升级是否进入 P10
```

任何阶段只通过文件级验收，不得标记为完成。

---

# 15. Handoff Plane 方法论

每个阶段必须生成 handoff packet。

handoff packet 不是附属说明，而是下游阶段的正式输入。

## 15.1 Handoff Packet 必须包含

```json
{
  "handoff_id": "",
  "source_stage": "",
  "target_stage": "",
  "included_assets": [],
  "included_schemas": [],
  "included_field_maps": [],
  "known_gaps": [],
  "blocking_gaps": [],
  "non_blocking_gaps": [],
  "acceptance_status": "",
  "next_legal_stage": "",
  "consumption_required": true
}
```

下游消费后必须写入：

```text
00_control/task_consumption_log.json
00_trace/handoff_consumption_matrix.yaml
```

---

# 16. Execution Plane 方法论

执行平面负责 runner、工具、CLI、验证脚本的绑定。

执行平面不拥有策略裁决权。

## 16.1 Runner 绑定必须回答

```text
哪个阶段调用哪个 runner？
runner 输入是什么？
runner 输出是什么？
runner 失败如何处理？
runner 输出如何验收？
runner 输出如何回写状态？
```

## 16.2 必须建立文件

```text
07_runners/runner_registry.yaml
07_runners/phase_runner_binding.yaml
07_runners/validation_runner_registry.yaml
07_runners/replay_runner_registry.yaml
```

## 16.3 Runner 禁止事项

```text
runner 不得绕过 Phase Controller
runner 不得直接产生交易指令
runner 不得修改真实交易状态
runner 不得把失败结果静默吞掉
runner 输出必须进入验收门
```

---

# 17. P01-P10 阶段目标数据

## 17.1 P01 数据事实层

```yaml
phase_id: P01_data_fact_controller
phase_name_cn: 数据事实层
phase_type: normalized_fact_runtime
primary_goal: 将 GMGN、OKX、K线、钱包、市值、quote、安全扫描、paper 数据转成统一事实模型
non_goal:
  - 不判断主导侧意图
  - 不裁决买卖
  - 不进入策略门禁
required_inputs:
  - data_input_contract.json
  - normalized_fact_model.schema.json
  - field_source_map.yaml
required_outputs:
  - normalized_token_fact.json
  - normalized_wallet_fact.json
  - normalized_market_fact.json
  - data_quality_report.json
  - p01_handoff_packet.json
default_status: BLOCKED_BY_DATA_PLANE
```

## 17.2 P02 钱包结构层

```yaml
phase_id: P02_wallet_structure_controller
phase_name_cn: 钱包结构层
phase_type: wallet_entity_and_role_analysis
primary_goal: 识别钱包角色、实体归并、同源组、资金路径、利润回收和分发接收关系
required_inputs:
  - normalized_wallet_fact.json
  - wallet_role_taxonomy.yaml
required_outputs:
  - wallet_classification.json
  - same_source_groups.json
  - fund_flow_edges.json
  - wallet_structure_decision.json
default_status: NOT_READY
```

## 17.3 P03 筹码控制层

```yaml
phase_id: P03_chip_control_controller
phase_name_cn: 筹码控制层
phase_type: chip_control_and_counterparty_pressure
primary_goal: 判断早期结构筹码是否仍然保留、是否撤退、是否转移给接盘方
required_inputs:
  - wallet_classification.json
  - same_source_groups.json
  - normalized_token_fact.json
required_outputs:
  - chip_control_status.json
  - counterparty_pressure_report.json
  - dominant_side_status.json
default_status: NOT_READY
```

## 17.4 P04 市场结构层

```yaml
phase_id: P04_market_structure_controller
phase_name_cn: 市场结构层
phase_type: kline_volume_avwap_structure
primary_goal: 识别箱体、AVWAP、POC、成交量、趋势结构、疲劳和失败测试
required_inputs:
  - normalized_market_fact.json
required_outputs:
  - market_structure_report.json
  - avwap_acceptance_report.json
  - volume_structure_report.json
  - fatigue_filter_report.json
default_status: NOT_READY
```

## 17.5 P05 场景识别层

```yaml
phase_id: P05_scenario_classification_controller
phase_name_cn: 场景识别层
phase_type: multi_model_scenario_classification
primary_goal: 综合钱包、筹码、市场结构判断当前属于什么盘型
required_inputs:
  - chip_control_status.json
  - dominant_side_status.json
  - market_structure_report.json
  - scenario_taxonomy.yaml
required_outputs:
  - scenario_classification.json
  - scenario_confidence_report.json
  - contradiction_report.json
default_status: NOT_READY
```

## 17.6 P06 策略门禁层

```yaml
phase_id: P06_strategy_gate_controller
phase_name_cn: 策略门禁层
phase_type: opportunity_rejection_and_paper_permission
primary_goal: 剔除低质量样本，只允许证据链未被否定样本进入 paper
required_inputs:
  - scenario_classification.json
  - contradiction_report.json
  - risk_boundary.yaml
required_outputs:
  - strategy_gate_decision.json
  - paper_permission_packet.json
  - block_reason_report.json
default_status: NOT_READY
```

## 17.7 P07 执行风控层

```yaml
phase_id: P07_execution_risk_controller
phase_name_cn: 执行风控层
phase_type: paper_execution_risk_simulation
primary_goal: 模拟执行风险、滑点、手续费、流动性和熔断条件
required_inputs:
  - paper_permission_packet.json
  - quote_security_report.json
required_outputs:
  - execution_risk_report.json
  - simulated_fill_policy.json
  - risk_event_log.jsonl
default_status: NOT_READY
```

## 17.8 P08 纸面交易验证层

```yaml
phase_id: P08_paper_trading_controller
phase_name_cn: 纸面交易验证层
phase_type: paper_trade_validation
primary_goal: 运行纸面交易，验证策略门禁是否有统计价值
required_inputs:
  - paper_permission_packet.json
  - execution_risk_report.json
required_outputs:
  - paper_positions_open.json
  - paper_positions_closed.json
  - paper_trades.csv
  - paper_equity_curve.csv
  - strategy_metrics.json
  - paper_daily_report.md
default_status: NOT_READY
```

## 17.9 P09 复盘学习层

```yaml
phase_id: P09_review_learning_controller
phase_name_cn: 复盘学习层
phase_type: failure_attribution_and_rule_feedback
primary_goal: 将失败样本、错判样本、延迟样本转化为规则修正候选
required_inputs:
  - paper_positions_closed.json
  - strategy_metrics.json
  - risk_event_log.jsonl
required_outputs:
  - failure_attribution_report.json
  - rule_adjustment_candidates.json
  - data_gap_feedback.json
default_status: NOT_READY
```

## 17.10 P10 系统升级层

```yaml
phase_id: P10_system_upgrade_controller
phase_name_cn: 系统升级层
phase_type: controlled_system_upgrade
primary_goal: 基于复盘证据升级字段、规则、schema、阶段逻辑和验收门
required_inputs:
  - failure_attribution_report.json
  - rule_adjustment_candidates.json
  - data_gap_feedback.json
required_outputs:
  - upgrade_proposal.json
  - schema_migration_plan.json
  - acceptance_update_plan.json
  - backward_compatibility_check.json
default_status: NOT_READY
```

---

# 18. 系统状态枚举

## 18.1 合法状态

```text
NOT_CREATED
STUB_REQUIRED
WAITING_INPUT
READY_TO_BUILD
READY_TO_EXECUTE
BLOCKED
BLOCKED_BY_DATA_PLANE
BLOCKED_BY_CONTROL_PLANE
BLOCKED_BY_ACCEPTANCE
BLOCKED_BY_UPSTREAM
RUNNING
OUTPUT_CREATED
ACCEPTANCE_PENDING
ACCEPTANCE_PASSED
ACCEPTANCE_FAILED
HANDOFF_READY
CONSUMED_BY_DOWNSTREAM
DEPRECATED
```

## 18.2 非法状态

```text
done
ok
finished
looks_good
maybe_ready
almost_complete
should_work
probably_ready
trade_ready
real_trade_ready
```

---

# 19. 系统禁止规则

系统全局禁止：

```text
禁止 Data Plane 未完成时启动 P01
禁止 Control Plane 缺失时执行业务阶段
禁止把 K00 资产化结果当作系统消费完成
禁止把 verification overall_passed 当作系统整体完成
禁止用文件存在代替语义覆盖
禁止用聊天上下文代替输入合约
禁止策略层直接读取未标准化数据
禁止执行层反向污染分析层
禁止复盘结果未经 P10 直接改变实时规则
禁止任何自动真实交易
禁止把未知钱包强行分类
禁止把主导侧意图假设写成确定事实
禁止单一指标直接给买点
禁止在缺少反证记录时通过策略门禁
禁止新增阶段逃避已有 blocking gaps
```

---

# 20. 系统标准输出格式

每个阶段必须输出统一状态摘要：

```json
{
  "stage_id": "",
  "stage_status": "",
  "input_assets": [],
  "consumed_assets": [],
  "created_assets": [],
  "output_assets": [],
  "blocking_gaps": [],
  "non_blocking_gaps": [],
  "evidence_level": "",
  "contradiction_records": [],
  "acceptance_result": "",
  "handoff_status": "",
  "next_legal_stage": "",
  "paper_only": true,
  "real_trade_enabled": false
}
```

---

# 21. 专业机构化完成标准

系统达到专业机构化 v1.0，必须满足：

```text
1. system_methodology_blueprint.md 已存在并被 P00 消费。
2. K00 已升级为 Phase Controller 候选任务化阶段。
3. P00_system_bootstrap_controller 已建立。
4. Governance Plane 已建立。
5. Domain Plane 已建立。
6. Data Plane 已建立。
7. Control Plane 已建立。
8. Trace Plane 已建立。
9. Acceptance Plane 已建立。
10. Handoff Plane 已建立。
11. K00、P00、P01-P10 已注册。
12. P01 在 Data Plane 验收前保持 BLOCKED_BY_DATA_PLANE。
13. 所有阶段都有 controller.yaml。
14. 所有阶段都有 input_contract / output_contract。
15. 所有阶段都有 acceptance_gate。
16. 所有阶段都有 handoff_packet。
17. trace matrix 可以追踪方法论要求。
18. asset consumption matrix 可以追踪资产消费。
19. data_to_phase matrix 可以追踪字段消费。
20. paper_only=true。
21. real_trade_enabled=false。
```

---

# 22. 当前默认系统裁决

在本方法论蓝图建立后，系统默认裁决为：

```json
{
  "current_authoritative_stage": "P00_system_bootstrap_controller",
  "k00_status": "ASSETIZED_OR_READY_FOR_P00_CONSUMPTION",
  "methodology_blueprint_status": "CREATED",
  "p00_status": "REQUIRED",
  "governance_plane_status": "REQUIRED",
  "domain_plane_status": "REQUIRED",
  "data_plane_status": "REQUIRED",
  "control_plane_status": "REQUIRED",
  "p01_runtime_connection_allowed": false,
  "next_legal_stage": "P00_system_bootstrap_controller",
  "paper_only": true,
  "real_trade_enabled": false
}
```

---

# 23. 当前优先执行顺序

当前系统不得直接进入自动化交易业务。

当前合法顺序：

```text
Step 1：确认 system_methodology_blueprint.md 落盘
Step 2：确认 K00 已升级为 Phase Controller 候选任务化阶段
Step 3：建立 P00_system_bootstrap_controller
Step 4：P00 消费 K00 与方法论蓝图
Step 5：P00 生成 Control Plane
Step 6：P00 生成 Governance Plane
Step 7：P00 生成 Domain Plane
Step 8：P00 生成 Data Plane
Step 9：P00 注册 P01-P10
Step 10：建立 Trace / Acceptance / Handoff
Step 11：Data Plane Acceptance Review
Step 12：P01 Preflight
Step 13：P01 才允许进入 READY_TO_EXECUTE
```

---

# 24. HER 执行提醒

HER 在执行任何系统建设任务时，必须避免以下错误：

```text
只写文档，不建立控制文件
只生成目录，不建立输入输出合约
只生成 task package，不建立 consumed_by
只生成阶段说明，不生成 controller.yaml
只生成 schema，不说明字段来源
只生成报告，不更新 current_system_state
只说完成，不输出验收结果
只通过文件级验收，不做语义级和消费级验收
```

HER 每次执行结束必须明确回答：

```text
当前权威阶段是什么？
哪些阶段被阻断？
阻断原因是什么？
哪些资产被消费？
哪些文件只是候选？
下一合法阶段是什么？
P01 是否允许运行？
是否仍 paper-only？
```

---

# 25. 最终方法论定义

SIKK Stable Trader OS 的系统建造方法论是：

```text
先建方法论。
再建系统建造控制器。
再建治理边界。
再建领域对象。
再建数据字段。
再建控制状态。
再建阶段控制器。
再建 runner。
再建验收。
再建交接。
最后才进入业务运行。
```

系统真正的专业化不是文件多，而是每个文件都能回答：

```text
它来自哪里？
它解决什么问题？
它被谁读取？
它输出什么？
它由谁验收？
它如何回写状态？
它如何影响下一阶段？
它是否被下游消费？
```

只有满足这些条件，系统才从“文档堆叠”进入“机构化运行体系”。

---

# 26. 本文件验收标准

`system_methodology_blueprint.md` 本身必须满足以下验收：

```text
1. 明确系统总目标。
2. 明确 HER 执行逻辑。
3. 明确 K00 定位。
4. 明确 P00 定位。
5. 明确 Phase Controller 定义。
6. 明确系统平面。
7. 明确 Governance Plane。
8. 明确 Domain Plane。
9. 明确 Data Plane。
10. 明确 Control Plane。
11. 明确 Trace / Acceptance / Handoff。
12. 明确 P01-P10 阶段目标数据。
13. 明确禁止规则。
14. 明确系统状态枚举。
15. 明确专业机构化完成标准。
16. 明确 P01 当前不得启动。
17. 明确 next legal stage 是 P00。
18. 明确 paper_only=true。
19. 明确 real_trade_enabled=false。
```

---

# 27. 本文件输出状态

本文件落盘后，系统状态应更新为：

```json
{
  "methodology_blueprint_status": "CREATED",
  "methodology_blueprint_consumed_by_p00": false,
  "next_legal_stage": "P00_system_bootstrap_controller",
  "p01_runtime_connection_allowed": false,
  "paper_only": true,
  "real_trade_enabled": false
}
```

P00 消费本文件后，状态应更新为：

```json
{
  "methodology_blueprint_status": "CONSUMED_BY_P00",
  "p00_status": "BOOTSTRAP_IN_PROGRESS_OR_PASSED",
  "p01_runtime_connection_allowed": false,
  "paper_only": true,
  "real_trade_enabled": false
}
```

````

---

# HER 落盘任务书

下面这段可以直接发给 HER：

```text
任务名称：
CREATE_SYSTEM_METHODOLOGY_BLUEPRINT_V2_INSTITUTIONAL

任务类型：
系统方法论蓝图建立任务。
不是交易功能开发。
不是 P01 数据事实运行。
不是真实交易任务。

目标：
创建或更新 /root/sikk-gmgn/sikk_stable_trader_os/00_methodology/system_methodology_blueprint.md。
该文件必须作为 SIKK Stable Trader OS 的权威系统建造方法论蓝图，供 P00_system_bootstrap_controller 优先读取和消费。

必须创建目录：
/root/sikk-gmgn/sikk_stable_trader_os/00_methodology/

必须创建文件：
/root/sikk-gmgn/sikk_stable_trader_os/00_methodology/system_methodology_blueprint.md

文件内容必须包含：
1. 文件定位。
2. 系统总目标。
3. HER 底层执行逻辑。
4. 系统建造总链路。
5. Phase Controller 核心定义。
6. K00 阶段方法论。
7. P00 阶段方法论。
8. Governance Plane 方法论。
9. Domain Plane 方法论。
10. Data Plane 方法论。
11. Control Plane 方法论。
12. Trace Plane 方法论。
13. Acceptance Plane 方法论。
14. Handoff Plane 方法论。
15. Execution Plane 方法论。
16. P01-P10 阶段目标数据。
17. 系统状态枚举。
18. 系统禁止规则。
19. 专业机构化完成标准。
20. 当前默认系统裁决。

验收标准：
1. 文件存在。
2. 文件非空。
3. 包含 Phase Controller 核心定义。
4. 包含 K00 / P00 职责边界。
5. 包含 Governance / Domain / Data / Control Plane。
6. 包含 P01-P10 阶段目标数据。
7. 明确 P01 当前不得启动。
8. 明确 next legal stage 是 P00_system_bootstrap_controller。
9. 明确 paper_only=true。
10. 明确 real_trade_enabled=false。

禁止事项：
1. 禁止启动 P01。
2. 禁止运行自动化交易 workflow。
3. 禁止真实交易。
4. 禁止把该文件创建完成解释为系统集成完成。
5. 禁止把 methodology_blueprint_status 直接标记为 CONSUMED_BY_P00，除非 P00 已实际读取并写入 consumption log。

最终输出：
1. 创建文件路径。
2. 文件是否创建成功。
3. 验收结果。
4. 当前下一合法阶段。
5. P01 是否允许运行：必须回答否。
````

---

# 本次认知升级点

```text
1. system_methodology_blueprint.md 不是说明文档，而是系统建造宪法。

2. K00 不再只是知识摄取，而是 Phase Controller 候选任务化入口。

3. P00 不再只是阶段之一，而是系统编译器，负责把方法论与 K00 资产编译成正式系统结构。

4. 专业机构化的关键不是增加功能，而是建立平面、控制、合约、验收、追踪、交接和状态回写。

5. P01 不是下一步，P00 才是下一步。

6. 任何交易业务运行前，必须先完成 Governance Plane、Domain Plane、Data Plane、Control Plane、Trace Plane、Acceptance Plane、Handoff Plane。

7. 当前系统应从“文档堆叠”升级为“可调度运行体系”。
```

# 尚未解决问题

```text
1. 该 system_methodology_blueprint.md 是否已经真实落盘？

2. K00 是否已经生成 phase_controller_candidate_spec？

3. K00 是否已经生成 k00_to_p00_handoff_packet？

4. P00_system_bootstrap_controller 是否已经建立？

5. P00 是否已经消费本方法论蓝图？

6. current_system_state.json 是否已经存在？

7. phase_registry.yaml 是否已经注册 K00、P00、P01-P10？

8. Domain Plane 是否已经从概念说明升级为对象注册表、关系图、问题树和场景分类？

9. Data Plane 是否已经形成字段来源图、统一事实模型和输入合约？

10. P01 是否仍然被正确阻断？
```