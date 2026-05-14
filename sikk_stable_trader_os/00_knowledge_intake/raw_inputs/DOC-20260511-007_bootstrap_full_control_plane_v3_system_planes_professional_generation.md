# 判断

是的，你这条链路 **比之前更全面，也更接近专业机构化系统建造逻辑**。

但要做成真正专业版，需要做一个关键修正：

```text
Control Plane 不能只放在 Data Plane 后面。
必须拆成两层：

1. Bootstrap Control Plane：由 P00 先建立，用来阻断 P01、注册阶段、裁决下一步。
2. Full Control Plane：在 Governance / Domain / Data 生成后，再补全字段消费、任务队列、runner 状态、验收结果和 handoff 状态。
```

否则会出现一个问题：

```text
Governance Plane、Domain Plane、Data Plane 还没生成时，
系统没有 current_system_state.json 和 phase_registry.yaml，
就无法阻断 P01，也无法裁决下一合法阶段。
```

所以你的链路方向是对的，但专业版应该改成：

```text
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md：系统方法论蓝图
  ↓
P00：系统建造与方法论编译控制器
  ↓
Bootstrap Control Plane：启动控制面
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Full Control Plane：完整控制面
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

---

# 一、为什么要这样改

你原来的链路是：

```text
Governance Plane
  ↓
Domain Plane
  ↓
Data Plane
  ↓
Control Plane
```

这个逻辑在“设计文档”层面没问题。

但在 HER 执行层面有一个缺口：

```text
如果 Control Plane 太晚出现，
系统早期就没有状态裁决权。
```

专业系统必须先有一个最小但正式的启动控制面：

```text
00_control/current_system_state.json
00_control/phase_registry.yaml
00_control/system_asset_index.json
00_control/current_blockers.json
00_control/next_stage_decision.json
```

它先解决：

```text
当前阶段是谁？
P01 是否被阻断？
K00 是否被 P00 消费？
下一步是否合法？
哪些平面还缺？
```

然后等 Governance / Domain / Data 完成后，再把 Control Plane 补全成完整运行控制面。

---

# 二、专业机构化系统建造总链路 v3.0

## 0. K00：知识摄取与 Phase Controller 候选任务化

### 目标

```text
把输入资料从“普通文本 / 文档 / 旧系统资料”
转化成 P00 可消费的系统建造材料。
```

### 必须产物

```text
raw_input_copy
document_passport
methodology_requirement_extract
phase_controller_candidate_spec.yaml
k00_to_p00_handoff_packet.json
gap_report.json
```

### 关键要求

K00 不注册正式阶段，只生成候选规格。

```text
K00 = 资产化 + 候选任务化
P00 = 正式编译 + 系统注册
```

---

## 1. Methodology Plane：系统方法论蓝图

### 目标

```text
定义系统如何建造，而不是定义某个交易策略。
```

### 必须产物

```text
00_methodology/system_methodology_blueprint.md
00_methodology/methodology_requirement_index.yaml
00_methodology/methodology_compilation_rules.yaml
```

### 必须回答

```text
系统总目标是什么？
系统如何分层？
Phase Controller 是什么？
K00 和 P00 的边界是什么？
哪些顺序禁止？
哪些验收必须存在？
```

---

## 2. P00：系统建造与方法论编译控制器

### 目标

```text
把 K00 资产和方法论蓝图编译成正式系统结构。
```

### 必须产物

```text
06_phase_controllers/P00_system_bootstrap_controller/context.md
06_phase_controllers/P00_system_bootstrap_controller/controller.yaml
06_phase_controllers/P00_system_bootstrap_controller/input_contract.json
06_phase_controllers/P00_system_bootstrap_controller/output_contract.json
06_phase_controllers/P00_system_bootstrap_controller/task_tree.yaml
06_phase_controllers/P00_system_bootstrap_controller/acceptance_gate.yaml
06_phase_controllers/P00_system_bootstrap_controller/state_writeback_policy.yaml
06_phase_controllers/P00_system_bootstrap_controller/handoff_packet.schema.json
```

### P00 必须做

```text
消费 K00 handoff
消费 methodology blueprint
建立 Bootstrap Control Plane
注册 K00 / P00 / P01-P10
阻断 P01
生成下一合法阶段裁决
```

---

## 3. Bootstrap Control Plane：启动控制面

这是你原链路中需要补进去的专业化关键层。

### 目标

```text
在 Governance / Domain / Data 尚未生成前，先建立最小权威状态源，防止系统乱跑。
```

### 必须产物

```text
00_control/current_system_state.json
00_control/phase_registry.yaml
00_control/system_asset_index.json
00_control/current_blockers.json
00_control/next_stage_decision.json
00_control/task_consumption_log.json
```

### 状态要求

```json
{
  "current_authoritative_stage": "P00_system_bootstrap_controller",
  "p00_status": "BOOTSTRAP_EXECUTED",
  "p01_status": "BLOCKED_BY_DATA_PLANE",
  "p01_runtime_connection_allowed": false,
  "next_legal_stage": "GOVERNANCE_DOMAIN_DATA_PLANE_GENERATION",
  "paper_only": true,
  "real_trade_enabled": false
}
```

---

## 4. Governance Plane：治理平面

### 目标

```text
定义权限边界、禁止事项、硬否定规则和安全边界。
```

### 必须产物

```text
00_governance/governance_plane.md
00_governance/authority_boundary.yaml
00_governance/stage_permission_matrix.yaml
00_governance/hard_negative_rules.yaml
00_governance/risk_boundary.yaml
00_governance/real_trade_forbidden_policy.yaml
00_governance/review_to_upgrade_policy.yaml
```

### 必须回答

```text
谁能裁决？
谁只能记录？
什么情况硬阻断？
什么阶段可以进入 paper？
什么阶段禁止触碰真实交易？
复盘如何进入升级层？
```

---

## 5. Domain Plane：领域平面

### 目标

```text
定义系统到底判断什么。
```

### 必须产物

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

### 必须包含的领域对象

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

### 必须包含的领域关系

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

---

## 6. Data Plane：数据平面

### 目标

```text
把领域判断转化为字段、来源、质量等级、证据等级、缺失策略和统一事实模型。
```

### 必须产物

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

### 必须覆盖字段域

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

每个字段必须有：

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

## 7. Full Control Plane：完整控制面

### 目标

```text
在 Governance / Domain / Data 生成后，补全系统状态裁决、任务队列、字段消费、runner 绑定、验收结果和 handoff 消费状态。
```

### 必须补全

```text
00_control/task_queue.json
00_control/task_consumption_log.json
00_control/runner_status_index.json
00_control/phase_output_index.json
00_control/handoff_consumption_status.json
00_control/data_plane_acceptance_status.json
```

### 它必须回答

```text
Data Plane 是否通过？
P01 是否可以进入 preflight？
哪些字段还缺？
哪些缺口是 blocking？
哪些阶段仍 blocked？
runner 是否绑定？
handoff 是否被消费？
```

---

## 8. Trace Plane：追踪平面

### 目标

```text
证明系统不是只写了文件，而是方法论、资产、领域对象、字段、阶段、runner、验收之间有追踪关系。
```

### 必须产物

```text
00_trace/methodology_implementation_trace_matrix.yaml
00_trace/asset_consumption_matrix.yaml
00_trace/domain_to_data_trace_matrix.yaml
00_trace/data_to_phase_trace_matrix.yaml
00_trace/acceptance_coverage_matrix.yaml
00_trace/handoff_consumption_matrix.yaml
00_trace/runner_execution_trace.yaml
```

---

## 9. Acceptance Plane：验收平面

### 目标

```text
把“完成”从口头判断变成可检查的五级验收。
```

### 五级验收

```text
1. 文件级验收：文件存在、格式可解析。
2. 结构级验收：目录、合约、控制器、注册表齐全。
3. 语义级验收：方法论、领域对象、数据需求真正落实。
4. 消费级验收：上游资产被下游读取并写入 consumed_by。
5. 运行级验收：runner 执行、状态回写、阻断生效。
```

### 必须产物

```text
08_acceptance/global_acceptance_policy.yaml
08_acceptance/phase_acceptance_gate_index.yaml
08_acceptance/semantic_acceptance_rules.yaml
08_acceptance/consumption_acceptance_rules.yaml
08_acceptance/runtime_acceptance_rules.yaml
```

---

## 10. Handoff Plane：交接平面

### 目标

```text
让上游输出成为下游正式输入，避免“任务包存在但未被使用”。
```

### 必须产物

```text
09_handoff/handoff_packet_registry.yaml
09_handoff/handoff_packet.schema.json
09_handoff/k00_to_p00/
09_handoff/p00_to_governance/
09_handoff/p00_to_domain/
09_handoff/p00_to_data/
09_handoff/data_to_p01/
09_handoff/p01_to_p02_p03_p04/
```

每个 handoff 必须包含：

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

---

## 11. P01-P10 Phase Controller

### 目标

```text
把业务阶段全部变成可调度运行单元，而不是阶段说明。
```

每个阶段必须包含：

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

阶段顺序：

```text
P01 数据事实层
P02 钱包结构层
P03 筹码控制层
P04 市场结构层
P05 场景识别层
P06 策略门禁层
P07 执行风控层
P08 纸面交易验证层
P09 复盘学习层
P10 系统升级层
```

---

## 12. Runner / Tool Binding

### 目标

```text
把阶段控制器绑定到真实脚本、验证工具、CLI、replay 和 paper runner。
```

### 必须产物

```text
07_runners/runner_registry.yaml
07_runners/phase_runner_binding.yaml
07_runners/validation_runner_registry.yaml
07_runners/replay_runner_registry.yaml
07_runners/runner_failure_policy.yaml
```

runner 不得绕过 Phase Controller。

---

## 13. Paper-only Runtime

### 目标

```text
只在 paper-only 边界下验证策略门禁和执行模拟。
```

### 必须产物

```text
10_runtime/paper_only_runtime/
10_runtime/paper_only_runtime/runtime_state.json
10_runtime/paper_only_runtime/paper_positions_open.json
10_runtime/paper_only_runtime/paper_positions_closed.json
10_runtime/paper_only_runtime/paper_trades.csv
10_runtime/paper_only_runtime/paper_equity_curve.csv
10_runtime/paper_only_runtime/risk_events.jsonl
```

前提条件：

```text
P06 strategy_gate_decision = PAPER_ALLOWED
P07 execution_risk_report = ACCEPTABLE_FOR_PAPER
real_trade_enabled = false
```

---

## 14. Review / Upgrade

### 目标

```text
把失败样本、错判样本、延迟样本和执行偏差转化为系统升级候选。
```

### 必须产物

```text
11_review/failure_attribution_report.json
11_review/rule_adjustment_candidates.json
11_review/data_gap_feedback.json
12_upgrade/upgrade_proposal.json
12_upgrade/schema_migration_plan.json
12_upgrade/acceptance_update_plan.json
12_upgrade/backward_compatibility_check.json
```

复盘结果禁止直接修改实时规则，必须进入 P10。

---

# 三、专业版禁止顺序

你列的禁止顺序是正确的，建议固定为全局硬规则。

```text
K00 → P01
K00 → 自动交易
文档 → 直接判断
方法论 → 直接跑交易
旧脚本 → 直接并入正式系统
paper runner → 绕过策略门禁
复盘结果 → 直接修改实时规则
```

我建议再补几条：

```text
Data Plane 未验收 → P01
Domain Plane 未建立 → Data Plane 字段随意生成
Control Plane 缺失 → 任何业务阶段运行
Trace Plane 缺失 → 标记系统完成
Acceptance Plane 缺失 → 标记阶段完成
Handoff 未被消费 → 下游阶段运行
Runner 未绑定 → 阶段 runtime 执行
P06 未通过 → P08 paper trading
P09 复盘结果 → 直接修改 P06 规则
```

完整禁止顺序应该是：

```text
K00 → P01
K00 → 自动交易
文档 → 直接判断
方法论 → 直接跑交易
旧脚本 → 直接并入正式系统
Data Plane 未验收 → P01
Control Plane 缺失 → 业务阶段运行
Trace Plane 缺失 → 系统完成
Acceptance Plane 缺失 → 阶段完成
Handoff 未消费 → 下游运行
Runner 未绑定 → runtime 执行
paper runner → 绕过策略门禁
复盘结果 → 直接修改实时规则
真实交易 → 自动执行
```

---

# 四、专业化完成标准

系统不能因为“P00 执行完成”就叫专业版。

专业机构化 v1.0 至少要满足：

```text
1. K00 已能生成 Phase Controller 候选规格。
2. system_methodology_blueprint.md 已被 P00 消费。
3. P00 已生成 Bootstrap Control Plane。
4. Governance Plane 已生成并通过验收。
5. Domain Plane 已生成并通过验收。
6. Data Plane 已生成并通过验收。
7. Full Control Plane 已补全。
8. Trace Plane 已覆盖方法论、资产、领域、字段、阶段。
9. Acceptance Plane 已定义五级验收。
10. Handoff Plane 已能记录上游输出被下游消费。
11. P01-P10 均已注册为 Phase Controller。
12. P01 在 Data Plane 通过前始终 blocked。
13. Runner 不可绕过 Phase Controller。
14. Paper-only Runtime 不可绕过 P06 / P07。
15. Review 结果不可绕过 P10。
16. paper_only=true。
17. real_trade_enabled=false。
```

---

# 五、当前下一步应执行什么

如果现在已经完成：

```text
P00_BOOTSTRAP_EXECUTION
```

那么下一步不是 P01。

下一步就是你这条链路里的正式系统平面生成：

```text
GOVERNANCE_DOMAIN_DATA_PLANE_GENERATION
```

但我建议任务名更专业一些：

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

它一次性生成：

```text
Governance Plane
Domain Plane
Data Plane
Full Control Plane update
Trace Plane update
Acceptance Plane update
Handoff Plane update
```

---

# 六、给 HER 的下一阶段任务标题

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

任务目标：

```text
基于 P00_BOOTSTRAP_EXECUTION 已生成的启动控制面，按照 system_methodology_blueprint.md 的机构化系统建造逻辑，一次性生成 Governance Plane、Domain Plane、Data Plane，并同步补全 Full Control Plane、Trace Plane、Acceptance Plane 和 Handoff Plane。禁止进入 P01，禁止运行自动化交易，禁止真实交易。
```

---

# 七、最终判断

你的链路是正确的，而且已经接近专业机构化系统设计。

但最终专业版应采用这个增强链路：

```text
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md：系统方法论蓝图
  ↓
P00：系统建造与方法论编译控制器
  ↓
Bootstrap Control Plane：启动控制面
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Full Control Plane：完整控制面
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

这条链路才真正解决：

```text
文档如何进系统
系统如何知道当前阶段
领域对象如何变成字段
字段如何进入阶段
阶段如何被 runner 执行
输出如何被验收
结果如何被下游消费
失败如何复盘
规则如何升级
```

当前最合理的推进不是 P01，而是：

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

---

# 本次认知升级点

```text
1. 原链路总体正确，但 Control Plane 必须拆成 Bootstrap Control Plane 和 Full Control Plane。

2. Bootstrap Control Plane 由 P00 先建立，用于阶段注册、P01 阻断和下一步裁决。

3. Full Control Plane 在 Governance / Domain / Data 完成后补全，用于任务队列、字段消费、runner 状态、handoff 消费和验收状态。

4. 专业化不是继续增加交易功能，而是让每个平面都有输入、输出、验收、追踪和消费关系。

5. 下一步应做 SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE，而不是 P01。
```

# 尚未解决问题

```text
1. Bootstrap Control Plane 是否已真实生成？

2. Governance Plane 是否已经有 authority_boundary、hard_negative_rules 和 stage_permission_matrix？

3. Domain Plane 是否已经有对象注册表、关系图、问题树、场景分类和生命周期分类？

4. Data Plane 是否已经有 field_source_map、normalized_fact_model 和 data_input_contract？

5. Trace Plane 是否已能追踪 methodology → domain → data → phase？

6. Acceptance Plane 是否已经定义五级验收？

7. Handoff Plane 是否已经记录 K00 → P00、P00 → Data、Data → P01 的消费关系？

8. P01 是否仍然被正确阻断？
```