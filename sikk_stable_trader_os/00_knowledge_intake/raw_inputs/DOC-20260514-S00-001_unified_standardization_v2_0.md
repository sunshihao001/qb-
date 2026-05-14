# 全体系统一标准化模块 v2.0：专业级别统一化数据模型

## 0. 结论判断

你现在列出的方向是**正确的**，但还不能直接算“专业级别 / 轻量机构水准”。原因不是缺少文件，而是还缺少一个**统一标准控制层**，负责把所有标准变成可执行、可追踪、可验收、可交接、可复盘的系统约束。

更准确的定位应是：

> **全体系统一标准化模块不是文档目录。它是 HER / SIKK 全体系的“标准控制层”，用于规定所有目标、方法、数据、字段、runner、判断、报告、复盘升级如何被统一命名、绑定、验证、追踪和回滚。**

专业化达标的关键不是“文件多”，而是做到：

> 任意一个 token 判断结果，都能反向追溯到：  
> 目标来源 → 方法轮 → 输入数据 → 字段权限 → schema / contract → runner → trace → acceptance → handoff → P08 permission gate → paper-only 结果 → P09/P10 复盘升级 → regression / rollback。

---

# 1. 模块正式命名

建议建立：

```text
/system/unified_standardization/
```

模块名称：

```text
S00_unified_system_standardization
```

模块职责：

```text
统一目标、方法、数据、字段、合约、runner、验证、追踪、验收、交接、复盘、回滚、安全边界。
```

它不是 P01-P10 的某个业务阶段，而是：

```text
K00 / P00 / R00 / P01-P10 / paper runtime / P09-P10 review upgrade 的共同标准层。
```

---

# 2. 专业化判断：现有清单是否完善？

## 2.1 你已识别的必要项

你列出的这些是正确的核心项：

|标准项|是否必要|作用|
|---|--:|---|
|目标映射|必须|防止系统只做文件，不服务真实 token 判断|
|方法轮映射|必须|把 GPT 研究方法转成 HER 可执行流程|
|数据血缘|必须|每个判断必须知道字段来源|
|字段权限|必须|区分事实字段、推理字段、裁决字段、禁止修改字段|
|schema / contract|必须|保证阶段间可消费|
|runner binding|必须|防止文件存在但没有 runner 执行|
|trace / acceptance / handoff|必须|追踪、验收、下游交接闭环|
|R00 验证|必须|runner 绑定与运行验证中心|
|P08 permission gate|必须|paper-only / real-risk 权限边界|
|P09/P10 复盘升级|必须|失败样本进入升级，不直接污染实时规则|
|issue registry|必须|系统缺口、失败、异常统一登记|
|task packet|必须|把问题转成可执行任务|
|legacy absorption|必须|吸收旧 runtime，不重建孤岛|
|sample library|必须|用样本验证判断逻辑|
|regression / rollback|必须|防止升级后破坏旧能力|
|安全边界|必须|paper-only、权限、真实交易隔离|

## 2.2 仍需补齐的专业项

要达到轻量机构级，还必须补齐以下统一化数据：

|需要补齐|为什么必须有|
|---|---|
|全局对象身份标准|没有统一 ID，trace / handoff / regression 无法串联|
|全局状态码标准|阶段状态、runner 状态、判断状态不能各写各的|
|领域实体模型|token、wallet、cluster、trade、signal、decision、position 必须有统一对象定义|
|事件类型标准|所有状态变化、runner 执行、判断、阻断、退出都要事件化|
|证据等级模型|区分事实、计算、推理、假设、裁决|
|反证模型|专业判断必须记录“为什么可能错”|
|数据质量评分|判断不能只输出结论，要输出数据是否足够可信|
|消费矩阵|每个文件被谁读取、谁产生、谁验证、谁消费|
|版本治理|schema、contract、runner、规则必须有版本号|
|变更审批 / shadow 验证|P10 升级不能直接改 live 规则|
|失败处理策略|runner 失败、数据缺失、schema 不兼容时怎么处理|
|报告统一格式|dashboard、daily report、case file 必须共享判断字段|

---

# 3. 模块总结构

建议统一成 16 个子层，不再无限拆分。

```text
/system/unified_standardization/
  00_module_charter/
  01_global_identity/
  02_goal_mapping/
  03_method_wheel_mapping/
  04_domain_entity_model/
  05_data_lineage/
  06_field_governance/
  07_schema_contract/
  08_runner_binding/
  09_trace_acceptance_handoff/
  10_validation_r00/
  11_permission_gate_p08/
  12_review_upgrade_p09_p10/
  13_issue_task_registry/
  14_legacy_absorption/
  15_sample_regression_rollback/
  16_security_boundary/
  index/
```

核心原则：

```text
少建重复模块，多建统一标准。
每个标准文件必须回答：
1. 谁产生？
2. 谁消费？
3. 字段从哪里来？
4. 是否允许被改？
5. 如何验收？
6. 如何失败处理？
7. 如何进入下游？
8. 如何复盘回滚？
```

---

# 4. 必须产物清单

## 4.1 总控文件

```text
00_module_charter/
  s00_unified_standardization_charter.md
  s00_scope_boundary.yaml
  s00_standard_object_registry.yaml
```

### `s00_standard_object_registry.yaml`

用于登记所有标准对象。

核心字段：

```yaml
standard_id:
standard_name:
standard_type: goal | method | schema | contract | runner | trace | acceptance | handoff | gate | review | security
owner_plane:
applies_to_phases:
producer:
consumer:
source_files:
output_files:
version:
status: draft | active | deprecated | rejected
acceptance_required: true
last_reviewed_at:
risk_level:
```

---

# 5. 目标映射层

## 5.1 目标

解决一个问题：

> 系统建设不能停留在“完善文件”，必须全部映射到真实 token 阶段化判断。

## 5.2 文件

```text
02_goal_mapping/
  system_goal_mapping.yaml
  token_judgment_goal_map.yaml
  phase_goal_alignment_matrix.yaml
  goal_to_runner_consumption_map.yaml
```

## 5.3 核心字段

```yaml
goal_id:
goal_name:
goal_type: system | phase | token_analysis | paper_runtime | review_upgrade
goal_statement:
success_definition:
related_phases:
required_inputs:
required_outputs:
required_decisions:
required_evidence:
required_runners:
acceptance_gate:
downstream_consumer:
```

## 5.4 专业标准

每个目标必须能映射到至少一个：

```text
Phase Controller
runner
schema / contract
acceptance gate
handoff packet
trace event
```

否则该目标只是口号，不能进入系统主链路。

---

# 6. 方法轮映射层

## 6.1 目标

把 GPT 里的研究方法、判断模型、方法轮，转成 HER 可执行结构。

## 6.2 文件

```text
03_method_wheel_mapping/
  method_wheel_registry.yaml
  method_to_phase_map.yaml
  method_to_field_map.yaml
  method_to_decision_map.yaml
  method_to_counter_evidence_map.yaml
```

## 6.3 方法轮对象

```yaml
method_id:
method_name:
method_source:
method_purpose:
applies_to:
phase_bindings:
input_fields:
derived_fields:
decision_outputs:
counter_evidence_required:
confidence_model:
failure_conditions:
sample_cases:
regression_tests:
```

## 6.4 示例

```yaml
method_id: MW_WALLET_CHIP_DOMINANT_SIDE_001
method_name: 钱包筹码主导侧生命周期判断
applies_to:
  - P03_wallet_entity
  - P04_chip_structure
  - P05_evidence
  - P06_scenario_recognition
input_fields:
  - wallet_holding_delta
  - same_source_group_id
  - sync_sell_score
  - counterparty_pressure_score
  - market_cap_change_from_discovery_pct
decision_outputs:
  - dominant_side_status
  - chip_control_retention
  - distribution_progress
  - reaccumulation_possibility
counter_evidence_required:
  - early_wallet_concentrated_exit
  - quote_liquidity_inconsistency
  - falling_obv
  - negative_cmf
```

---

# 7. 领域实体统一模型

这是你目前清单里隐含但没有单独提出的关键部分。

没有领域实体模型，schema / contract 会散。

## 7.1 文件

```text
04_domain_entity_model/
  canonical_entity_model.yaml
  token_entity_schema.yaml
  wallet_entity_schema.yaml
  cluster_entity_schema.yaml
  trade_event_schema.yaml
  signal_entity_schema.yaml
  decision_entity_schema.yaml
  paper_position_entity_schema.yaml
```

## 7.2 核心实体

|实体|作用|
|---|---|
|token|单币分析主对象|
|wallet|钱包行为对象|
|cluster|地址组 / 同源组 / 结构组|
|trade_event|买卖行为事件|
|market_snapshot|K线、成交量、市值、流动性快照|
|signal|信号，不等于决策|
|evidence|证据对象|
|counter_evidence|反证对象|
|decision|阶段裁决|
|handoff_packet|交接对象|
|paper_position|纸面仓位对象|
|review_case|复盘样本对象|
|upgrade_candidate|升级候选对象|

## 7.3 统一 ID 标准

```yaml
token_id: chain:address
wallet_id: chain:wallet_address
cluster_id: chain:token:cluster_hash
event_id: timestamp:source:hash
phase_run_id: phase_id:token_id:run_timestamp
decision_id: phase_id:token_id:decision_timestamp
trace_id: run_id:event_sequence
handoff_id: source_phase:target_phase:token_id:timestamp
```

---

# 8. 数据血缘层

## 8.1 目标

任何字段都必须知道：

```text
来自哪里
何时生成
由哪个 runner 生成
有没有被修改
被哪个阶段消费
是否参与裁决
```

## 8.2 文件

```text
05_data_lineage/
  data_source_registry.yaml
  field_lineage_registry.yaml
  file_lineage_map.yaml
  decision_lineage_map.yaml
  report_lineage_map.yaml
```

## 8.3 字段血缘对象

```yaml
field_name:
entity:
source_type: raw | normalized | derived | inferred | decision | manual
source_file:
source_api:
source_runner:
source_phase:
transform_function:
depends_on_fields:
generated_at:
schema_version:
confidence_level:
data_quality_score:
consumed_by:
  - phase_id:
    runner_id:
    decision_field:
```

## 8.4 专业验收

一个字段不能说明来源时：

```text
不能进入 P07 策略门禁
不能进入 P08 权限门
不能进入 paper runner
只能作为观察字段
```

---

# 9. 字段权限层

## 9.1 目标

防止 AI 或 runner 随意改裁决字段、事实字段、风险字段。

## 9.2 文件

```text
06_field_governance/
  field_permission_matrix.yaml
  field_mutation_policy.yaml
  field_confidence_policy.yaml
  field_manual_override_policy.yaml
```

## 9.3 字段权限类型

|类型|说明|是否允许修改|
|---|---|--:|
|raw_fact|原始事实|禁止修改|
|normalized_fact|标准化事实|允许重建，不允许手改|
|derived_metric|计算指标|允许 runner 重算|
|inferred_state|推理状态|允许带证据更新|
|decision_field|阶段裁决|只能由 Phase Controller 写|
|permission_field|权限字段|只能由 P08 / Control Plane 写|
|review_field|复盘字段|只能由 P09 写|
|upgrade_field|升级字段|只能由 P10 写|
|manual_note|人工备注|允许，但不得参与自动裁决|

## 9.4 权限矩阵字段

```yaml
field_name:
entity:
field_class:
write_permission:
read_permission:
allowed_writers:
allowed_consumers:
manual_override_allowed:
requires_trace_event:
requires_acceptance:
prohibited_usage:
```

---

# 10. Schema / Contract 层

## 10.1 目标

防止“文件存在但下游不能消费”。

## 10.2 文件

```text
07_schema_contract/
  schema_index.yaml
  contract_index.yaml
  phase_input_contracts.yaml
  phase_output_contracts.yaml
  handoff_contracts.yaml
  report_contracts.yaml
  backward_compatibility_policy.yaml
```

## 10.3 Contract 标准对象

```yaml
contract_id:
contract_name:
producer_phase:
consumer_phase:
required_files:
required_fields:
optional_fields:
forbidden_fields:
schema_version:
validation_runner:
acceptance_gate:
failure_policy:
handoff_packet:
```

## 10.4 专业验收

每个 P01-P10 阶段必须具备：

```text
input_contract
output_contract
handoff_contract
trace_contract
acceptance_contract
failure_contract
```

否则该阶段不能算完整 Phase Controller。

---

# 11. Runner Binding 层

## 11.1 目标

把旧脚本、验证工具、replay、paper runner 全部收编进阶段控制器，不允许绕过 Phase Controller。

## 11.2 文件

```text
08_runner_binding/
  runner_registry.yaml
  phase_runner_binding.yaml
  validation_runner_registry.yaml
  replay_runner_registry.yaml
  paper_runner_binding.yaml
  runner_failure_policy.yaml
  runner_output_contract_map.yaml
```

## 11.3 Runner 对象

```yaml
runner_id:
runner_name:
runner_type: ingestion | normalization | analysis | validation | replay | paper | report
script_path:
entry_command:
bound_phase:
input_contract:
output_contract:
writes_trace: true
writes_acceptance: true
writes_handoff: true
allowed_modes:
  - dry_run
  - replay
  - paper_only
forbidden_modes:
  - live_swap
failure_policy:
timeout_policy:
rollback_policy:
```

## 11.4 旧 runtime 吸收原则

你当前已有链路：

```text
sikk_live_run.py
→ run_sikk_gmgn_pipeline.py
→ GMGN 候选发现
→ K线/吸筹/信号
→ 状态机
→ 钱包结构门禁
→ quote/security
→ paper live runner
→ failure attribution
→ daily report
→ dashboard/static site
```

不能推倒重建。应该做：

```text
旧脚本保留
↓
登记到 runner_registry.yaml
↓
绑定到 phase_runner_binding.yaml
↓
输出接入 trace / acceptance / handoff
↓
由 R00 统一验证
↓
由 Control Plane 统一判断下一阶段
```

---

# 12. Trace / Acceptance / Handoff 层

## 12.1 目标

让每一次系统动作都能复盘。

## 12.2 文件

```text
09_trace_acceptance_handoff/
  trace_event_schema.yaml
  process_trace_policy.yaml
  acceptance_gate_matrix.yaml
  acceptance_evidence_schema.yaml
  handoff_packet_standard.yaml
  downstream_consumption_matrix.yaml
```

## 12.3 Trace 事件标准

```yaml
trace_id:
run_id:
token_id:
phase_id:
runner_id:
event_type:
event_time:
input_refs:
output_refs:
decision_refs:
status_before:
status_after:
evidence_refs:
counter_evidence_refs:
error_refs:
schema_version:
```

## 12.4 Acceptance 对象

```yaml
acceptance_id:
phase_id:
token_id:
run_id:
required_checks:
passed_checks:
failed_checks:
missing_fields:
schema_validation_result:
runner_validation_result:
data_quality_result:
decision_quality_result:
status: PASS | WITH_GAPS | FAIL
blocking_reason:
next_allowed_phase:
```

## 12.5 Handoff 对象

```yaml
handoff_id:
source_phase:
target_phase:
token_id:
handoff_status:
required_payload:
payload_files:
decision_summary:
evidence_summary:
counter_evidence_summary:
data_quality_summary:
known_gaps:
next_phase_permissions:
```

---

# 13. R00 验证层

## 13.1 目标

R00 不是普通 runner。R00 是：

```text
Runner / Tool Binding 验证控制器
```

它负责判断：

```text
脚本是否存在
命令是否可运行
输入是否符合 contract
输出是否符合 schema
trace 是否写入
acceptance 是否生成
handoff 是否可消费
是否绕过 Phase Controller
```

## 13.2 文件

```text
10_validation_r00/
  r00_validation_controller.md
  r00_validation_checklist.yaml
  r00_runner_dry_run_matrix.yaml
  r00_replay_validation_matrix.yaml
  r00_failure_report_schema.yaml
```

## 13.3 R00 验收标准

```text
R00 不负责交易判断。
R00 只负责验证系统组件是否被正确绑定、正确运行、正确输出、正确交接。
```

---

# 14. P08 Permission Gate 层

## 14.1 目标

P08 是权限闸门，不是普通风控说明。

它回答：

```text
当前 token 是否允许进入 paper-only？
是否允许继续持仓？
是否允许退出？
是否允许进入人工确认？
是否绝对禁止 real swap？
```

## 14.2 文件

```text
11_permission_gate_p08/
  p08_permission_gate_policy.yaml
  p08_action_permission_matrix.yaml
  p08_paper_only_boundary.yaml
  p08_real_trade_forbidden_policy.yaml
  p08_risk_event_schema.yaml
```

## 14.3 权限状态

```yaml
permission_status:
  - BLOCKED
  - WATCH_ONLY
  - PAPER_ELIGIBLE
  - PAPER_READY
  - PAPER_ACTIVE
  - EXIT_MONITOR
  - FORCE_PAPER_EXIT
  - READY_FOR_CONFIRMATION
  - REAL_TRADE_FORBIDDEN
```

## 14.4 P08 必须读取

```text
P01 data_fact_handoff_packet
P02/P03 wallet/chip handoff
P04 chip structure result
P05 evidence / counter-evidence
P06 scenario recognition
P07 strategy gate decision
quote/security result
wallet_structure_decision
market_cap_context
trace / acceptance status
```

## 14.5 硬边界

```text
没有 P08 permission gate 通过，paper runner 不得开仓。
没有人工确认，任何真实交易不得执行。
P09/P10 复盘结论不得直接改 P08 live permission rule。
```

---

# 15. P09 / P10 复盘升级层

## 15.1 目标

失败样本、成功样本、误判样本不能只进入日报，必须进入复盘升级闭环。

## 15.2 文件

```text
12_review_upgrade_p09_p10/
  p09_review_case_schema.yaml
  p09_failure_attribution_schema.yaml
  p09_replay_packet_schema.yaml
  p10_upgrade_candidate_schema.yaml
  p10_shadow_validation_policy.yaml
  p10_rule_promotion_policy.yaml
```

## 15.3 P09 复盘对象

```yaml
review_case_id:
token_id:
paper_position_id:
entry_decision_id:
exit_decision_id:
expected_scenario:
actual_outcome:
failure_type:
success_type:
missed_counter_evidence:
wrong_assumption:
data_gap:
runner_gap:
rule_gap:
recommended_action:
```

## 15.4 P10 升级对象

```yaml
upgrade_candidate_id:
source_review_case:
affected_rule:
affected_phase:
change_proposal:
expected_improvement:
risk_of_change:
shadow_test_required:
regression_test_required:
rollback_plan:
approval_status:
promotion_status:
```

## 15.5 专业标准

P10 升级必须经过：

```text
review case
→ upgrade candidate
→ shadow validation
→ regression test
→ rollback plan
→ approval
→ versioned promotion
```

不能直接把复盘结论改成实时规则。

---

# 16. Issue Registry / Task Packet 层

## 16.1 目标

把“发现问题”变成“可执行修复任务”。

## 16.2 文件

```text
13_issue_task_registry/
  issue_registry.yaml
  issue_taxonomy.yaml
  task_packet_schema.yaml
  task_priority_policy.yaml
  task_acceptance_policy.yaml
```

## 16.3 Issue 对象

```yaml
issue_id:
issue_type:
affected_phase:
affected_module:
severity:
symptom:
root_cause_hypothesis:
evidence:
blocking_status:
related_files:
related_runners:
required_fix:
owner:
status:
```

## 16.4 Task Packet 对象

```yaml
task_packet_id:
source_issue_id:
task_goal:
scope:
non_goals:
files_to_create:
files_to_modify:
commands_to_run:
validation_steps:
acceptance_criteria:
rollback_plan:
handoff_target:
completion_status:
```

专业标准：

```text
issue 没有 task packet，不能算进入修复流程。
task packet 没有 acceptance，不能算完成。
```

---

# 17. Legacy Absorption 层

## 17.1 目标

旧系统不能变成混乱目录，也不能全部推倒。

## 17.2 文件

```text
14_legacy_absorption/
  legacy_asset_inventory.yaml
  legacy_to_new_mapping.yaml
  legacy_runtime_absorption_plan.yaml
  legacy_keep_deprecate_migrate_policy.yaml
  legacy_readonly_boundary.yaml
```

## 17.3 Legacy 对象

```yaml
legacy_asset_id:
legacy_path:
asset_type:
current_usage:
new_system_mapping:
absorption_mode: keep_in_place | wrap_runner | migrate_output | deprecate | archive
risk_level:
consumer:
replacement_plan:
validation_required:
```

## 17.4 你的系统应采用的策略

```text
/root/sikk-gmgn/data/gmgn_candidates_live_run
```

应作为：

```text
legacy_runtime_keep_in_place
```

含义：

```text
保留原路径
不强行搬迁
通过 mapping 和 runner wrapper 收编
新标准输出写入 trace / acceptance / handoff
```

---

# 18. Sample Library / Regression / Rollback 层

## 18.1 目标

没有样本库，判断模型无法证明稳定。

## 18.2 文件

```text
15_sample_regression_rollback/
  sample_library_index.yaml
  labeled_token_case_schema.yaml
  regression_suite_registry.yaml
  regression_result_schema.yaml
  rollback_policy.yaml
  rule_version_registry.yaml
```

## 18.3 样本类型

|样本类型|用途|
|---|---|
|confirmed_distribution|验证派发识别|
|failed_breakout|验证假突破|
|second_stage_expansion|验证二段扩张|
|long_control_box|验证长横盘控制箱|
|wallet_exit_failure|验证钱包结构阻断|
|paper_success_case|验证有效入场|
|paper_failure_case|验证失败归因|
|false_positive|验证误报控制|
|false_negative|验证漏报控制|

## 18.4 Regression 标准

每次规则升级必须回答：

```text
是否提升新样本判断？
是否破坏旧样本判断？
是否增加误报？
是否增加漏报？
是否影响 P08 permission gate？
是否影响 paper runner？
是否有 rollback plan？
```

---

# 19. 安全边界层

## 19.1 目标

明确系统当前是：

```text
paper-only validation system
```

不是自动真实交易系统。

## 19.2 文件

```text
16_security_boundary/
  security_boundary_policy.yaml
  paper_only_execution_policy.yaml
  real_trade_forbidden_policy.yaml
  api_key_permission_policy.yaml
  manual_confirmation_policy.yaml
  emergency_stop_policy.yaml
```

## 19.3 硬规则

```text
默认禁止真实 swap
默认只允许 paper-only
任何 runner 不得直接绕过 P08
任何 P10 升级不得直接进入 live rule
API key 不得赋予无审计真实交易权限
真实交易必须独立人工确认
```

---

# 20. 全体系统一索引层

必须建立：

```text
index/
  unified_standardization_index.yaml
  phase_consumption_matrix.yaml
  file_to_runner_index.yaml
  runner_to_phase_index.yaml
  schema_to_contract_index.yaml
  goal_to_phase_to_runner_index.yaml
  report_to_lineage_index.yaml
```

这个索引层的作用是让 HER 能直接回答：

```text
这个文件属于哪个标准？
由谁生成？
被谁消费？
是否有 runner？
是否有 schema？
是否有 acceptance？
是否进入 handoff？
是否影响 token 判断？
```

---

# 21. 判断是否达到专业级别的验收标准

## 21.1 模块级验收

全体系统一标准化模块只有满足以下条件，才算达到轻量机构水准：

|验收项|标准|
|---|---|
|目标闭环|每个系统目标都映射到 phase / runner / output|
|方法闭环|每个方法轮都能转成字段、判断、反证、样本|
|数据闭环|每个裁决字段都有血缘|
|权限闭环|每个字段有读写权限|
|合约闭环|每个阶段有 input/output/handoff contract|
|运行闭环|每个关键输出绑定 runner|
|验证闭环|每个 runner 有 R00 验证|
|权限闭环|P08 控制 paper-only 权限|
|复盘闭环|P09/P10 吸收 paper 结果|
|修复闭环|issue 能生成 task packet|
|旧系统闭环|legacy runtime 被收编而不是混用|
|样本闭环|规则有样本验证|
|回归闭环|升级前后可对比|
|回滚闭环|错误升级可撤销|
|安全闭环|默认禁止真实交易绕过|

## 21.2 Token 判断级验收

任意一个 token 输出结论时，必须能生成：

```yaml
token_id:
analysis_run_id:
phase_path:
goal_refs:
method_refs:
input_data_refs:
field_lineage_refs:
schema_refs:
contract_refs:
runner_refs:
trace_refs:
acceptance_refs:
handoff_refs:
permission_gate_result:
paper_decision:
review_status:
upgrade_candidate_refs:
known_gaps:
```

如果做不到，说明系统还没有达到专业化判断闭环。

---

# 22. 推荐最终状态码

统一标准模块本身也需要状态。

```text
S00_NOT_STARTED
S00_STRUCTURE_CREATED
S00_STANDARD_OBJECTS_DEFINED
S00_PHASES_MAPPED
S00_RUNNERS_BOUND
S00_TRACE_ACCEPTANCE_READY
S00_R00_VALIDATED
S00_P08_BOUND
S00_P09_P10_BOUND
S00_LEGACY_ABSORBED
S00_REGRESSION_READY
S00_PROFESSIONAL_READY_WITH_GAPS
S00_PROFESSIONAL_READY
S00_REJECTED
```

当前你应该定位为：

```text
S00_STANDARD_OBJECTS_DEFINED_WITH_GAPS
```

下一步目标应是：

```text
S00_TRACE_ACCEPTANCE_RUNNER_BOUND_READY_WITH_GAPS
```

也就是先让统一标准真正绑定到 runner、trace、acceptance、handoff，而不是继续扩展更多概念文件。

---

# 23. Hermes / OpenClaw 可复制任务书

```text
任务名称：
S00_unified_system_standardization 全体系统一标准化模块专业化落地

任务目标：
建立 /system/unified_standardization/，作为 HER / SIKK 全体系的统一标准控制层。目标不是增加文档数量，而是让每个目标、方法、字段、schema、contract、runner、trace、acceptance、handoff、P08 权限、P09/P10 复盘升级、legacy runtime、sample library、regression、rollback、安全边界都能被统一登记、追踪、验证、交接和复盘，并最终服务真实 token 阶段化判断。

核心原则：
1. 任意判断必须能追溯到目标、方法、输入数据、字段血缘、runner、trace、acceptance、handoff。
2. 任意 runner 必须绑定 Phase Controller，不得绕过阶段控制器。
3. 任意 paper-only 决策必须经过 P08 permission gate。
4. 任意复盘升级必须进入 P09/P10，不得直接修改实时规则。
5. 任意 legacy runtime 只允许通过 absorption map 收编，不允许继续形成孤岛。
6. 任意 schema / contract 必须有版本、消费者、验证方式和失败策略。
7. 任意安全敏感动作默认禁止真实交易，保持 paper-only。

需要创建目录：
/system/unified_standardization/
  00_module_charter/
  01_global_identity/
  02_goal_mapping/
  03_method_wheel_mapping/
  04_domain_entity_model/
  05_data_lineage/
  06_field_governance/
  07_schema_contract/
  08_runner_binding/
  09_trace_acceptance_handoff/
  10_validation_r00/
  11_permission_gate_p08/
  12_review_upgrade_p09_p10/
  13_issue_task_registry/
  14_legacy_absorption/
  15_sample_regression_rollback/
  16_security_boundary/
  index/

必须创建文件：
00_module_charter/s00_unified_standardization_charter.md
00_module_charter/s00_scope_boundary.yaml
00_module_charter/s00_standard_object_registry.yaml

01_global_identity/global_id_standard.yaml
01_global_identity/global_status_code_table.yaml
01_global_identity/global_event_type_registry.yaml

02_goal_mapping/system_goal_mapping.yaml
02_goal_mapping/token_judgment_goal_map.yaml
02_goal_mapping/phase_goal_alignment_matrix.yaml
02_goal_mapping/goal_to_runner_consumption_map.yaml

03_method_wheel_mapping/method_wheel_registry.yaml
03_method_wheel_mapping/method_to_phase_map.yaml
03_method_wheel_mapping/method_to_field_map.yaml
03_method_wheel_mapping/method_to_decision_map.yaml
03_method_wheel_mapping/method_to_counter_evidence_map.yaml

04_domain_entity_model/canonical_entity_model.yaml
04_domain_entity_model/token_entity_schema.yaml
04_domain_entity_model/wallet_entity_schema.yaml
04_domain_entity_model/cluster_entity_schema.yaml
04_domain_entity_model/trade_event_schema.yaml
04_domain_entity_model/signal_entity_schema.yaml
04_domain_entity_model/decision_entity_schema.yaml
04_domain_entity_model/paper_position_entity_schema.yaml

05_data_lineage/data_source_registry.yaml
05_data_lineage/field_lineage_registry.yaml
05_data_lineage/file_lineage_map.yaml
05_data_lineage/decision_lineage_map.yaml
05_data_lineage/report_lineage_map.yaml

06_field_governance/field_permission_matrix.yaml
06_field_governance/field_mutation_policy.yaml
06_field_governance/field_confidence_policy.yaml
06_field_governance/field_manual_override_policy.yaml

07_schema_contract/schema_index.yaml
07_schema_contract/contract_index.yaml
07_schema_contract/phase_input_contracts.yaml
07_schema_contract/phase_output_contracts.yaml
07_schema_contract/handoff_contracts.yaml
07_schema_contract/report_contracts.yaml
07_schema_contract/backward_compatibility_policy.yaml

08_runner_binding/runner_registry.yaml
08_runner_binding/phase_runner_binding.yaml
08_runner_binding/validation_runner_registry.yaml
08_runner_binding/replay_runner_registry.yaml
08_runner_binding/paper_runner_binding.yaml
08_runner_binding/runner_failure_policy.yaml
08_runner_binding/runner_output_contract_map.yaml

09_trace_acceptance_handoff/trace_event_schema.yaml
09_trace_acceptance_handoff/process_trace_policy.yaml
09_trace_acceptance_handoff/acceptance_gate_matrix.yaml
09_trace_acceptance_handoff/acceptance_evidence_schema.yaml
09_trace_acceptance_handoff/handoff_packet_standard.yaml
09_trace_acceptance_handoff/downstream_consumption_matrix.yaml

10_validation_r00/r00_validation_controller.md
10_validation_r00/r00_validation_checklist.yaml
10_validation_r00/r00_runner_dry_run_matrix.yaml
10_validation_r00/r00_replay_validation_matrix.yaml
10_validation_r00/r00_failure_report_schema.yaml

11_permission_gate_p08/p08_permission_gate_policy.yaml
11_permission_gate_p08/p08_action_permission_matrix.yaml
11_permission_gate_p08/p08_paper_only_boundary.yaml
11_permission_gate_p08/p08_real_trade_forbidden_policy.yaml
11_permission_gate_p08/p08_risk_event_schema.yaml

12_review_upgrade_p09_p10/p09_review_case_schema.yaml
12_review_upgrade_p09_p10/p09_failure_attribution_schema.yaml
12_review_upgrade_p09_p10/p09_replay_packet_schema.yaml
12_review_upgrade_p09_p10/p10_upgrade_candidate_schema.yaml
12_review_upgrade_p09_p10/p10_shadow_validation_policy.yaml
12_review_upgrade_p09_p10/p10_rule_promotion_policy.yaml

13_issue_task_registry/issue_registry.yaml
13_issue_task_registry/issue_taxonomy.yaml
13_issue_task_registry/task_packet_schema.yaml
13_issue_task_registry/task_priority_policy.yaml
13_issue_task_registry/task_acceptance_policy.yaml

14_legacy_absorption/legacy_asset_inventory.yaml
14_legacy_absorption/legacy_to_new_mapping.yaml
14_legacy_absorption/legacy_runtime_absorption_plan.yaml
14_legacy_absorption/legacy_keep_deprecate_migrate_policy.yaml
14_legacy_absorption/legacy_readonly_boundary.yaml

15_sample_regression_rollback/sample_library_index.yaml
15_sample_regression_rollback/labeled_token_case_schema.yaml
15_sample_regression_rollback/regression_suite_registry.yaml
15_sample_regression_rollback/regression_result_schema.yaml
15_sample_regression_rollback/rollback_policy.yaml
15_sample_regression_rollback/rule_version_registry.yaml

16_security_boundary/security_boundary_policy.yaml
16_security_boundary/paper_only_execution_policy.yaml
16_security_boundary/real_trade_forbidden_policy.yaml
16_security_boundary/api_key_permission_policy.yaml
16_security_boundary/manual_confirmation_policy.yaml
16_security_boundary/emergency_stop_policy.yaml

index/unified_standardization_index.yaml
index/phase_consumption_matrix.yaml
index/file_to_runner_index.yaml
index/runner_to_phase_index.yaml
index/schema_to_contract_index.yaml
index/goal_to_phase_to_runner_index.yaml
index/report_to_lineage_index.yaml

验收要求：
1. 每个文件必须写明 producer、consumer、version、status、acceptance。
2. 每个 phase 必须能映射 input_contract、output_contract、runner、trace、acceptance、handoff。
3. 每个 runner 必须有 runner_id、script_path、entry_command、bound_phase、input_contract、output_contract、failure_policy。
4. 每个裁决字段必须能在 field_lineage_registry.yaml 和 field_permission_matrix.yaml 中找到。
5. P08 必须定义 paper-only 权限状态，不允许真实交易绕过。
6. P09/P10 必须定义 review_case、upgrade_candidate、shadow_validation、regression、rollback。
7. legacy runtime 必须登记，不允许继续孤岛运行。
8. 最终输出 S00_ACCEPTANCE_REPORT.md，说明哪些完成、哪些 WITH_GAPS、哪些阻断。
```

---

# 24. 这个模块建完后，下一步应该做什么？

不要继续新增复杂子阶段。

正确顺序是：

```text
S00 全体系统一标准化
↓
绑定 K00 / P00 / HER_DOC / R00
↓
把现有 runtime 纳入 runner_registry
↓
把 P01-P10 阶段全部接入 schema / contract / trace / acceptance / handoff
↓
用一个真实 token replay 跑完整链路
↓
检查是否能生成完整 token_judgment_case_file
↓
再进入 P08 paper-only permission gate
↓
paper 结果进入 P09/P10
```

也就是说，下一步不是继续“设计更多标准”，而是做：

```text
统一标准 → 真实 runtime 吸收 → 单 token 全链路 replay → acceptance report
```

---

# 本次认知升级点

1. **全体系统一标准化不是文件标准，而是判断闭环标准。**  
    它必须服务真实 token 阶段化判断，而不是只服务目录整齐。
    
2. **专业化的核心是可追踪、可验收、可交接、可复盘。**  
    文件数量不是专业化指标，字段血缘、runner 绑定、trace、acceptance、handoff 才是。
    
3. **P08 是权限闸门，P09/P10 是升级闸门。**  
    paper-only 决策不能绕过 P08，复盘升级不能绕过 P09/P10。
    
4. **legacy absorption 是当前重点。**  
    你已经有能跑的 runtime，下一步应收编它，而不是另建一套空体系。
    
5. **统一标准模块必须先服务 replay。**  
    只有能用一个真实 token 跑出完整 trace / acceptance / handoff，才说明标准不是空文档。
    

---

# 尚未解决问题

1. 现有 `/root/sikk-gmgn` 中哪些 runner 已经能直接登记，哪些需要 wrapper，还需要实际扫描确认。
2. P01-P10 当前已有文件与新版标准之间的字段差异，需要做一次 contract diff。
3. `wallet_structure_decision.json`、`paper_positions_open.json`、`strategy_metrics.json` 等旧输出是否满足新版 schema，需要 R00 验证。
4. sample library 需要真实 token 样本标注，否则 regression 只能是空框架。
5. P08 permission gate 需要和当前 paper runner 实际接入，否则仍然只是权限说明。