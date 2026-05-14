# SIKK Stable Trader OS 系统方法论蓝图

文件编号：METHODOLOGY-BLUEPRINT-001  
版本：v1.0-light-institutional  
状态：AUTHORITATIVE_BLUEPRINT  
适用系统：SIKK Stable Trader OS  
适用执行器：HER / Hermes / Phase Controller / Runner  
安全边界：paper-only，禁止真实交易自动执行  
最后更新：2026-05-11  

---

## 0. 文件定位

system_methodology_blueprint.md 不是普通说明文档。

它是 SIKK Stable Trader OS 的系统建造方法论蓝图，用于指导 HER 将用户输入、研究资料、历史文档、交易逻辑、钱包结构逻辑、风险规则和阶段任务，编译成一个可调度、可验收、可回写、可复盘的轻量机构化系统。

本文件的职责不是直接执行交易，也不是直接判断某个 token 是否可以买。

本文件的职责是定义：

1. 系统应该如何思考。
2. 系统应该如何分层。
3. 系统应该如何把文档转成系统资产。
4. 系统应该如何把系统资产转成领域模型。
5. 系统应该如何把领域模型转成数据模型。
6. 系统应该如何把数据模型转成阶段控制器。
7. 系统应该如何验证阶段是否真正被消费。
8. 系统应该如何防止“文件存在但系统没有使用”。
9. 系统应该如何保持 paper-only 安全边界。
10. 系统应该如何从轻量可运行逐步接近机构级别。

---

## 1. 系统总目标

SIKK Stable Trader OS 不是一个单纯寻找交易机会的系统。

它的核心目标是：

> 从所有看起来像机会的 token、钱包结构、K 线结构和筹码行为中，连续剔除低质量、错误场景、假成交、派发风险、疲劳拖延、执行风险和错误位置，只保留极少数证据链未被否决、风险收益比可被纸面验证的结构样本。

系统的本质不是“预测上涨”，而是：

```text
事实采集
  ↓
结构还原
  ↓
筹码控制权判断
  ↓
场景识别
  ↓
硬否定过滤
  ↓
策略门禁
  ↓
纸面验证
  ↓
失败归因
  ↓
规则修正
```

系统必须始终保持以下认知：
文件存在不等于系统接入。
任务包存在不等于 runner 执行。
锚点验收不等于语义验收。
局部阶段通过不等于全局状态一致。
文档资产化不等于被下游消费。
AI 理解不等于字段、合约、状态、验收已经落地。
交易判断必须由数据事实、领域关系、反证规则和阶段门禁共同产生。
不允许依靠聊天上下文直接进入判断。
不允许以“感觉像机会”代替系统证据链。

## 2. 系统建造总原则

### 2.1 先建立体系，再推进功能

系统建设顺序必须是：

```text
方法论蓝图
  ↓
治理平面
  ↓
领域平面
  ↓
数据平面
  ↓
控制平面
  ↓
阶段控制器
  ↓
Runner
  ↓
验收与回写
  ↓
下游业务工作流
```

禁止在缺少数据平面、控制平面、阶段控制器和验收矩阵时，直接推进自动化交易功能。

### 2.2 轻量机构化原则

本系统不追求一开始就建立大型机构全量架构。

本系统采用轻量机构化原则：

```text
保留机构级核心控制逻辑
减少无效复杂度
优先建立可运行闭环
所有文件必须有消费关系
所有阶段必须有输入、输出、验收、回写
所有判断必须有字段来源、证据等级和反证记录
```

轻量机构化保留以下能力：

- 唯一系统状态源。
- 阶段注册表。
- 资产索引。
- 领域对象注册表。
- 数据字段来源图。
- 阶段输入输出合约。
- 验收门。
- trace matrix。
- handoff packet。
- paper-only 风控边界。

轻量机构化暂不强制以下能力：

- 大规模多团队权限系统。
- 实盘自动执行。
- 高频撮合系统。
- 复杂 dashboard 优先建设。
- 多租户架构。
- 分布式数据库。
- 过度微服务化。

### 2.3 系统分层原则

系统必须分成以下平面：

```text
Knowledge Plane      知识资产平面
Methodology Plane    方法论平面
Governance Plane     治理平面
Domain Plane         领域平面
Data Plane           数据平面
Control Plane        控制平面
Execution Plane      执行平面
Acceptance Plane     验收平面
Trace Plane          追踪平面
Handoff Plane        交接平面
Review Plane         复盘平面
Upgrade Plane        升级平面
```

每一个平面都必须回答一个明确问题。

- Knowledge Plane：哪些资料已经被摄取、保存、建档？
- Methodology Plane：系统应该按照什么方法建造？
- Governance Plane：什么允许做，什么禁止做，谁有权限裁决？
- Domain Plane：系统到底在判断哪些对象、关系、场景和问题？
- Data Plane：判断这些对象需要哪些字段、来源、质量等级？
- Control Plane：当前系统状态是什么，下一步谁合法？
- Execution Plane：哪个 runner 执行哪个任务？
- Acceptance Plane：什么条件才算阶段真正完成？
- Trace Plane：方法论、资产、字段、阶段是否被覆盖？
- Handoff Plane：上游如何把产物交给下游？
- Review Plane：纸面交易和错判如何复盘？
- Upgrade Plane：哪些规则允许被更新？

## 3. 系统编译链路

所有文档、方法、旧系统资料、交易逻辑，必须经过系统编译链路。

```text
用户输入 / 文档 / 链接 / 旧系统资料
  ↓
K00 知识摄取与任务化
  ↓
方法论蓝图读取
  ↓
P00 系统建造控制器
  ↓
治理平面生成
  ↓
领域平面生成
  ↓
数据平面生成
  ↓
控制平面生成
  ↓
阶段控制器生成
  ↓
runner 绑定
  ↓
验收门生成
  ↓
trace matrix 生成
  ↓
handoff packet 生成
```

其中最关键的断点是：

```text
K00 资产化
  ≠
系统消费
```

K00 完成后，必须由 P00 系统建造控制器继续处理。

## 4. HER 底层执行逻辑

HER 在读取本文件时，必须按照以下逻辑执行：

```text
1. 先识别当前任务属于哪个系统阶段。
2. 再读取 current_system_state.json。
   - 规范锚点：先读取 current_system_state.json。
3. 再读取 phase_registry.yaml。
4. 再确认当前阶段是否合法。
5. 再检查输入资产是否存在。
6. 再检查输入资产是否已经被登记。
7. 再检查输入资产是否被下游消费。
8. 再执行当前阶段目标。
9. 再写入输出文件。
10. 再写入验收结果。
11. 再写入状态回写。
12. 再生成 handoff packet。
13. 再裁决下一合法阶段。
```

HER 禁止直接根据聊天上下文跳过系统状态源。
HER 禁止因为用户说“继续”就绕过当前 blocking gaps。
HER 禁止把“生成了文件”直接判定为“阶段完成”。

HER 必须区分：

```text
diagnostic_artifact_passed
system_integration_repaired
phase_acceptance_passed
downstream_consumption_verified
runtime_execution_completed
```

## 5. 核心系统状态原则

系统必须始终存在唯一权威状态源：

```text
00_control/current_system_state.json
```

它必须回答：

- 当前唯一权威阶段是什么？
- 哪些阶段被阻断？
- 阻断原因是什么？
- 哪些资产已经登记？
- 哪些资产已经被消费？
- 当前允许执行什么？
- 当前禁止执行什么？
- 下一个合法阶段是什么？
- 是否 paper-only？
- 是否允许真实交易？

任何阶段启动前，必须先读取该文件。

如果该文件不存在，则系统状态为：

```text
SYSTEM_CONTROL_PLANE_MISSING
```

此时禁止进入 P01-P10 业务阶段。

## 6. 系统阶段总表

### 6.1 阶段编号

| 阶段 | 名称 | 定位 |
|---|---|---|
| K00 | 知识摄取与任务化 | 把文档、资料、旧系统资产化 |
| P00 | 系统建造与方法论编译 | 把方法论编译成系统平面 |
| P01 | 数据事实层 | 统一事实模型与字段标准化 |
| P02 | 钱包结构层 | 钱包角色、同源组、资金路径 |
| P03 | 筹码控制层 | 控制权、筹码迁移、对手盘压力 |
| P04 | 市场结构层 | K线、成交量、箱体、AVWAP、POC |
| P05 | 场景识别层 | 识别吸筹、派发、二段、陷阱等盘型 |
| P06 | 策略门禁层 | 剔除低质量样本，裁决 paper 资格 |
| P07 | 执行风控层 | 模拟成交、滑点、手续费、熔断 |
| P08 | 纸面交易验证层 | 纸面持仓、交易、收益曲线、统计 |
| P09 | 复盘学习层 | 错判归因、规则修正候选 |
| P10 | 系统升级层 | 经过复盘证据后升级字段、规则、阶段 |

## 7. 阶段目标数据标准

每一个阶段都必须使用统一的阶段目标数据格式。

### 7.1 阶段目标数据字段

每个阶段必须定义：

```yaml
phase_id: ""
phase_name_cn: ""
phase_type: ""
phase_status: ""
authority_scope: ""
primary_goal: ""
non_goal: []
upstream_dependencies: []
required_inputs: []
optional_inputs: []
forbidden_inputs: []
core_objects: []
core_questions: []
required_outputs: []
handoff_outputs: []
acceptance_gate: []
blocking_conditions: []
downstream_consumers: []
runner_binding_status: ""
state_writeback_required: true
paper_only_required: true
real_trade_allowed: false
```

### 7.2 阶段状态枚举

合法阶段状态包括：

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
RUNNING
OUTPUT_CREATED
ACCEPTANCE_PENDING
ACCEPTANCE_PASSED
ACCEPTANCE_FAILED
HANDOFF_READY
CONSUMED_BY_DOWNSTREAM
DEPRECATED
```

禁止使用模糊状态：

```text
done
finished
ok
looks good
almost complete
maybe ready
```

## 8. K00 阶段目标数据

```yaml
phase_id: K00_knowledge_intake_taskization
phase_name_cn: 知识摄取与任务化
phase_type: knowledge_assetization
phase_status: ASSETIZATION_LAYER
authority_scope: 只负责知识资产化，不负责系统运行裁决
primary_goal: >
  将用户输入、研究资料、旧系统文件、链接内容、方法轮文本转化为可登记、可索引、可交接的知识资产。
non_goal:
  - 不直接生成交易判断
  - 不直接启动 P01-P10
  - 不直接裁决策略是否可运行
  - 不直接修改真实交易系统
upstream_dependencies:
  - user_input
  - uploaded_documents
  - existing_project_files
required_inputs:
  - raw_text_or_file
  - source_metadata
optional_inputs:
  - user_goal
  - related_stage_hint
  - old_system_reference
forbidden_inputs:
  - real_trade_instruction
core_objects:
  - knowledge_asset
  - document_passport
  - task_package
  - intake_mapping
  - gap_report
core_questions:
  - 资料是否已经保存？
  - 资料属于哪个系统主题？
  - 资料中包含哪些方法、规则、阶段、字段、缺口？
  - 资料应该交给哪个下游阶段？
required_outputs:
  - raw_input_copy
  - document_passport
  - knowledge_index
  - task_execution_package
  - gap_report
  - handoff_packet
handoff_outputs:
  - task_package_to_P00
acceptance_gate:
  - 输入资料已保存
  - passport 已生成
  - task package 已生成
  - handoff packet 已生成
blocking_conditions:
  - 输入为空
  - 无法确定资料来源
  - 输出文件不可解析
downstream_consumers:
  - P00_system_bootstrap_controller
runner_binding_status: optional
state_writeback_required: true
paper_only_required: true
real_trade_allowed: false
```

## 9. P00 阶段目标数据

P00 是当前系统最关键的系统建造阶段。

```yaml
phase_id: P00_system_bootstrap_controller
phase_name_cn: 系统建造与方法论编译
phase_type: system_bootstrap_and_methodology_compilation
phase_status: REQUIRED_BEFORE_BUSINESS_PHASES
authority_scope: >
  负责把方法论蓝图、治理要求、领域对象、K00 资产和任务包编译成系统平面、注册表、控制状态和阶段骨架。
primary_goal: >
  建立 SIKK Stable Trader OS 的轻量机构化运行骨架，使 K00 产物从资产化进入系统消费闭环。
non_goal:
  - 不执行交易
  - 不判断 token 是否可以买
  - 不做钱包分类具体推断
  - 不做纸面交易
upstream_dependencies:
  - K00_knowledge_intake_taskization
  - system_methodology_blueprint
required_inputs:
  - 00_methodology/system_methodology_blueprint.md
  - 00_knowledge_intake/task_packages/
  - 00_knowledge_intake/intake_reports/
optional_inputs:
  - governance_plane.md
  - domain_plane.md
  - legacy_runtime_files
forbidden_inputs:
  - unverified_real_trade_signal
core_objects:
  - methodology_requirement
  - system_plane
  - phase_registry
  - asset_index
  - current_system_state
  - trace_matrix
core_questions:
  - 当前系统要按照什么方法建？
  - 哪些资产已经进入系统？
  - 哪些资产只是保存但未消费？
  - 哪些平面必须先生成？
  - 哪些阶段被阻断？
  - 当前唯一合法下一步是什么？
required_outputs:
  - 00_control/current_system_state.json
  - 00_control/phase_registry.yaml
  - 00_control/system_asset_index.json
  - 00_trace/methodology_implementation_trace_matrix.yaml
  - 00_trace/asset_consumption_matrix.yaml
  - 06_phase_controllers/P01-P10 controller stubs
handoff_outputs:
  - system_bootstrap_handoff_packet
  - data_plane_generation_task
acceptance_gate:
  - current_system_state.json 存在且可解析
  - phase_registry.yaml 包含 K00、P00、P01-P10
  - system_asset_index.json 登记核心资产
  - trace matrix 能追踪方法论要求
  - P01 在 Data Plane 完成前必须保持 blocked
blocking_conditions:
  - 缺少 system_methodology_blueprint.md
  - 缺少 current_system_state.json
  - 缺少 phase_registry.yaml
  - P01 被错误标记为 READY
downstream_consumers:
  - Governance Plane
  - Domain Plane
  - Data Plane
  - Control Plane
  - P01_data_fact_controller
runner_binding_status: required
state_writeback_required: true
paper_only_required: true
real_trade_allowed: false
```

## 10. Governance Plane 阶段目标数据

```yaml
phase_id: GOVERNANCE_PLANE
phase_name_cn: 治理平面
phase_type: authority_and_risk_boundary
phase_status: REQUIRED_BEFORE_DOMAIN_AND_DATA
authority_scope: 定义系统权限、禁止事项、硬否定规则、安全边界
primary_goal: >
  建立系统运行边界，确保分析层、策略层、执行层、复盘层之间权限清晰，防止未验证逻辑进入真实交易。
non_goal:
  - 不做领域对象推断
  - 不定义数据字段细节
  - 不执行 runner
required_inputs:
  - system_methodology_blueprint.md
  - current_system_state.json
required_outputs:
  - 00_governance/governance_plane.md
  - 00_governance/authority_boundary.yaml
  - 00_governance/hard_negative_rules.yaml
  - 00_governance/risk_boundary.yaml
  - 00_governance/stage_permission_matrix.yaml
  - 00_governance/real_trade_forbidden_policy.yaml
core_questions:
  - 什么阶段有裁决权？
  - 什么阶段只能记录事实？
  - 什么情况必须阻断？
  - 什么情况禁止进入真实交易？
  - 复盘数据如何进入升级层？
acceptance_gate:
  - paper_only=true
  - real_trade_enabled=false
  - stage_permission_matrix 存在
  - hard_negative_rules 存在
  - P01-P10 权限边界明确
```

## 11. Domain Plane 阶段目标数据

Domain Plane 不是领域说明文档。  
Domain Plane 是系统判断对象、关系、问题树、场景分类、钱包角色、主导侧生命周期和证据需求的注册层。

```yaml
phase_id: DOMAIN_PLANE
phase_name_cn: 领域平面
phase_type: domain_object_and_decision_model
phase_status: REQUIRED_BEFORE_DATA_PLANE
authority_scope: 定义系统要判断的对象、关系、问题、场景、证据和反证
primary_goal: >
  将 SIKK Stable Trader OS 的交易认知转化为可机读、可追踪、可被数据平面消费的领域模型。
non_goal:
  - 不直接采集数据
  - 不直接执行交易
  - 不直接生成买入信号
required_inputs:
  - system_methodology_blueprint.md
  - governance_plane.md
  - K00 task packages
required_outputs:
  - 00_domain/domain_plane.md
  - 00_domain/domain_object_registry.yaml
  - 00_domain/domain_relation_graph.yaml
  - 00_domain/domain_decision_question_tree.yaml
  - 00_domain/scenario_taxonomy.yaml
  - 00_domain/wallet_role_taxonomy.yaml
  - 00_domain/dominant_side_lifecycle_taxonomy.yaml
  - 00_domain/domain_to_data_demand_map.yaml
  - 00_domain/domain_to_phase_map.yaml
  - 00_domain/domain_acceptance_gate.yaml
core_objects:
  - token
  - wallet
  - wallet_entity
  - same_source_group
  - funding_source
  - chip_cluster
  - early_wallet_group
  - dominant_side
  - counterparty_group
  - market_structure
  - scenario
  - strategy_candidate
  - paper_trade
  - review_case
core_questions:
  - 系统到底判断什么？
  - 钱包事实如何进入实体归并？
  - 同源组如何影响筹码控制权？
  - 筹码控制权如何影响主导侧生命周期？
  - 主导侧生命周期如何影响场景识别？
  - 场景识别如何约束策略门禁？
  - 反证如何阻断下游？
acceptance_gate:
  - domain_object_registry.yaml 存在
  - domain_relation_graph.yaml 存在
  - domain_decision_question_tree.yaml 存在
  - scenario_taxonomy.yaml 存在
  - wallet_role_taxonomy.yaml 存在
  - dominant_side_lifecycle_taxonomy.yaml 存在
  - domain_to_data_demand_map.yaml 存在
blocking_conditions:
  - 没有领域对象注册表
  - 没有领域到数据需求映射
  - 场景分类没有反证规则
  - 钱包角色没有证据要求
downstream_consumers:
  - Data Plane
  - P01_data_fact_controller
  - P02_wallet_structure_controller
  - P05_scenario_classification_controller
```

## 12. Data Plane 阶段目标数据

```yaml
phase_id: DATA_PLANE
phase_name_cn: 数据平面
phase_type: normalized_fact_and_field_source_model
phase_status: REQUIRED_BEFORE_P01_RUNTIME
authority_scope: 定义系统字段、来源、质量等级、证据等级、缺失处理和统一事实模型
primary_goal: >
  将 Domain Plane 中的判断需求转化为字段来源、标准化事实模型、输入合约和下游交接包。
non_goal:
  - 不做交易判断
  - 不做钱包意图推断
  - 不做策略信号裁决
required_inputs:
  - domain_object_registry.yaml
  - domain_to_data_demand_map.yaml
  - governance_plane.md
required_outputs:
  - 00_data/data_plane.md
  - 00_data/field_source_map.yaml
  - 00_data/normalized_fact_model.schema.json
  - 00_data/data_input_contract.json
  - 00_data/data_quality_rules.yaml
  - 00_data/evidence_level_rules.yaml
  - 00_data/contradiction_record_rules.yaml
  - 00_data/data_handoff_packet.json
core_questions:
  - 每个判断需要哪些字段？
  - 每个字段来自哪里？
  - 字段缺失时如何处理？
  - 哪些字段是阻断性字段？
  - 哪些字段只是降级置信度？
  - 哪些阶段消费这些字段？
acceptance_gate:
  - field_source_map.yaml 存在
  - normalized_fact_model.schema.json 可解析
  - data_input_contract.json 可解析
  - data_handoff_packet.json 可解析
  - P01 所需字段全部有来源或 missing_policy
blocking_conditions:
  - 核心字段无来源
  - 缺失字段无处理策略
  - schema 不可解析
  - data_handoff_packet 缺失
downstream_consumers:
  - P01_data_fact_controller
  - P02_wallet_structure_controller
  - P03_chip_control_controller
  - P04_market_structure_controller
```

## K00/P00 Professional System Chain — DOC-20260511-019

K00 专业化后，系统链路固定为：

```text
输入资料 / 用户目标 / 方法论 / 旧系统文件
  ↓
K00：知识摄取与 Phase Controller 候选任务化
  ↓
phase_controller_candidate_spec.yaml
  ↓
k00_to_p00_handoff_packet.json
  ↓
P00：方法论编译与系统建造控制器
  ↓
正式 controller.yaml
  ↓
phase_registry.yaml
  ↓
current_system_state.json
  ↓
input_contract / output_contract / acceptance_gate / handoff_packet
  ↓
P01-P10 可调度运行
```

该链路是 K00 与 P00 的控制边界：K00 不直接生成正式控制器、不注册 `phase_registry.yaml`、不裁决 `current_system_state.json`、不启动 P01-P10。K00 输出只到候选规格与 K00→P00 交接包。

P00 是方法论编译与系统建造控制器，负责将 K00 候选规格编译为正式 `controller.yaml`，注册 `phase_registry.yaml`，接入 `current_system_state.json`，并将 `input_contract / output_contract / acceptance_gate / handoff_packet` 绑定为可调度运行资产。只有 P00 消费并验收后，P01-P10 才能进入可调度运行。

安全边界：`paper_only=true`，`real_trade_enabled=false`，当前不允许进入 P01。

