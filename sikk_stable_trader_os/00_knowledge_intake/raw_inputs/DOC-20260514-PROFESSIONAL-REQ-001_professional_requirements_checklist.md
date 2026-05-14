# 专业化水准需求清单

## 用于 SIKK / HER 交易结构系统从“文档体系”进入“真实 Token 可运行闭环”

你知道的核心点是：

```text
全体系必须统一标准化。
```

这没错，但专业化水准不只是统一命名、统一目录、统一格式。还必须做到：

```text
统一目标
统一方法
统一数据
统一合约
统一状态
统一验收
统一运行
统一复盘
统一升级
统一风险边界
```

下面是你可能还没有完全展开的准备清单。

---

# 1. 总目标映射标准

这是最高层准备。

必须明确：

```text
系统不是为了流程完整，
而是为了真实 token / candidate batch 阶段化判断。
```

必须准备：

```text
goal_to_system_mapping_matrix.yaml
goal_to_method_loop_mapping.yaml
goal_to_control_plane_mapping.yaml
goal_to_phase_mapping.yaml
goal_to_runtime_mapping.yaml
goal_to_review_upgrade_mapping.yaml
goal_mapping_acceptance_rules.yaml
goal_mapping_hard_negative_rules.yaml
```

专业要求：

|项目|必须回答|
|---|---|
|最终目标是什么|真实 token 阶段化分析判断|
|最终输出是什么|EXCLUDE / RECORD / RISK_MONITOR / WATCH / PAPER_READY / READY_FOR_CONFIRMATION|
|哪些阶段服务目标|P01-P10|
|哪些运行器验证目标|R00|
|哪些复盘目标|P09/P10|
|哪些输出不服务目标|必须标记为无效或 reference-only|

你之前容易忽略的是：

```text
不是所有文档、模块、字段都值得纳入系统。
只有能服务最终 token 判断闭环的对象，才应该进入核心链路。
```

---

# 2. 方法轮标准化

你现在已经有方法轮思路，但要变成系统检查标准。

方法轮应固定为：

```text
目标定义
→ 结构拆解
→ 机制抽取
→ 阶段映射
→ 数据对象化
→ 系统实现
→ 验收反馈
→ 复盘升级
```

每一步必须有输出：

|方法轮步骤|系统输出|
|---|---|
|目标定义|final_goal_reference|
|结构拆解|system_layer_mapping|
|机制抽取|functional_object_registry|
|阶段映射|phase_mapping_matrix|
|数据对象化|schema_candidate / contract_candidate|
|系统实现|runner_binding / tool_binding|
|验收反馈|acceptance_result|
|复盘升级|p09_review / p10_upgrade_candidate|

专业要求：

```text
任何 GPT 研究资料、HER_DOC 扫描结果、阶段补全任务，都必须经过方法轮。
```

否则就会继续停留在解释层。

---

# 3. 系统对象标准化

你现在不能只说“文档完善”。  
必须统一系统对象。

核心对象包括：

```text
controller
context
input_contract
output_contract
schema
runtime_output_model
runner_binding
tool_binding
trace_requirements
acceptance_criteria
handoff_contract
test_matrix
report_model
r00_binding
p09_review_requirements
p10_upgrade_requirements
```

每个阶段都必须有这套对象。

专业检查：

|对象|没有会导致什么|
|---|---|
|controller|阶段职责不清|
|input_contract|上游无法交接|
|output_contract|下游无法消费|
|schema|字段无法验证|
|runner_binding|R00 无法调用|
|trace_requirements|P09 无法复盘|
|acceptance_criteria|无法判断完成|
|handoff_contract|阶段断链|
|r00_binding|不能跑真实 token|
|p09/p10 requirements|不能学习升级|

---

# 4. 数据标准化

这是你最容易低估的部分。

专业化不是“有数据”，而是：

```text
字段有来源
字段有时间
字段有质量
字段有权限
字段有用途
字段有下游消费者
```

必须准备：

```text
data_source_registry.yaml
field_lineage_registry.yaml
field_quality_policy.yaml
field_permission_matrix.yaml
field_freshness_policy.yaml
field_conflict_resolution_policy.yaml
canonical_field_dictionary.yaml
```

字段必须至少包含：

```yaml
field_name: string
source: GMGN | OKX | KLINE | WALLET | INTERNAL | DERIVED
source_path: string
source_trace_id: string
freshness_status: FRESH | STALE | UNKNOWN
quality_status: HIGH | MEDIUM | LOW | MISSING | CONFLICTED
usage_permission: STRONG_USE | WEAK_USE_ONLY | REFERENCE_ONLY | DO_NOT_USE
used_by_phase: list
downstream_consumers: list
```

你可能没完全考虑的是：

```text
字段不能因为存在就能用于强判断。
```

例如：

```text
钱包持仓字段存在 ≠ 可判断主导侧没出货
交易量存在 ≠ 可判断真实成交
市值存在 ≠ 可判断位置安全
```

---

# 5. 目录与路径标准化

全体系必须统一路径。

建议标准：

```text
/system/                 系统定义
/data/                   运行数据
/tools/                  可执行工具
/modules/                可复用模块
/reports/                报告
/tasks/                  任务包
/tests/                  测试
/audits/                 审计
/legacy/                 旧系统只读映射
```

关键准备：

```text
directory_constitution.md
canonical_path_registry.yaml
legacy_path_absorption_matrix.yaml
write_permission_matrix.yaml
read_only_legacy_policy.yaml
```

专业要求：

```text
旧数据不能直接变成主路径。
旧脚本不能直接变成新 runner。
必须先登记、映射、吸收、绑定。
```

---

# 6. 状态码标准化

你现在已经有很多状态，但需要统一。

建议统一状态族：

```text
READY
READY_WITH_GAPS
BLOCKED
REJECTED
PAUSED
FAILED
DEFERRED
REFERENCE_ONLY
```

交易判断标签：

```text
EXCLUDE
RECORD
RISK_MONITOR
WATCH
PAPER_READY
READY_FOR_CONFIRMATION
```

运行状态：

```text
NOT_RUN
RUNNING
COMPLETED
COMPLETED_WITH_GAPS
PAUSED
BLOCKED
FAILED
```

必须准备：

```text
global_status_code_table.yaml
phase_status_policy.yaml
runtime_status_policy.yaml
decision_label_policy.yaml
status_transition_matrix.yaml
```

你可能忽略的是：

```text
READY_WITH_GAPS 不能随便下游使用。
必须携带 gap_tags 和 limitation_tags。
```

---

# 7. Handoff 标准化

这是系统能否串起来的关键。

每个 handoff 必须包含：

```yaml
handoff_id: string
from_stage: string
to_stage: string
run_id: string
token_address: string
output_contract_id: string
payload_paths: list
trace_ids: list
acceptance_status: string
gap_tags: list
limitation_tags: list
downstream_permission:
  may_continue: true | false
  may_continue_with_gaps: true | false
  must_stop: true | false
```

必须准备：

```text
handoff_packet_standard.yaml
handoff_contract_index.yaml
handoff_validation_policy.yaml
handoff_consumption_check.yaml
```

专业要求：

```text
上游生成 handoff 不算完成。
必须证明下游读取了 handoff。
```

---

# 8. Trace 标准化

Trace 不是日志。  
Trace 是“判断可复盘的证据链”。

必须准备：

```text
trace_id_standard.yaml
trace_event_schema.yaml
field_trace_policy.yaml
decision_trace_policy.yaml
runtime_trace_policy.yaml
review_trace_policy.yaml
```

Trace 必须覆盖：

```text
数据来源
字段转换
阶段判断
证据引用
反证引用
runner 调用
acceptance 结果
handoff 传递
paper runtime
P09 复盘
P10 升级候选
```

专业要求：

```text
无 trace，不允许进入 P09。
无 trace，不允许标记阶段 READY。
```

---

# 9. Acceptance 标准化

Acceptance 不是“任务完成确认”。

它必须判断：

```text
这个阶段是否真的可以进入下游？
```

每个 acceptance 需要包含：

```yaml
acceptance_id: string
stage_id: string
run_id: string
schema_validated: true | false
contract_validated: true | false
trace_complete: true | false
handoff_created: true | false
downstream_permission_declared: true | false
goal_mapping_passed: true | false
hard_negative_triggered: true | false
final_status: READY | READY_WITH_GAPS | BLOCKED | REJECTED | FAILED
```

必须准备：

```text
acceptance_plane_policy.yaml
professional_baseline_acceptance.md
acceptance_runner_binding.yaml
acceptance_result_schema.yaml
goal_alignment_acceptance_gate.yaml
```

你可能没完全考虑的是：

```text
文件生成完成 ≠ 阶段验收完成。
runner 执行完成 ≠ 阶段可下游消费。
```

---

# 10. Runner / Tool Binding 标准化

这是 R00 能否跑真实 token 的关键。

必须准备：

```text
runner_registry.yaml
phase_runner_binding.yaml
tool_binding_registry.yaml
validation_runner_registry.yaml
replay_runner_registry.yaml
runner_failure_policy.yaml
```

每个 runner 必须登记：

```yaml
runner_id: string
target_stage: P01
entrypoint: string
input_contract: string
output_contract: string
required_tools: list
writes_to: list
trace_required: true
acceptance_required: true
handoff_required: true
paper_only: true
```

专业要求：

```text
runner 不能因为代码存在就能运行。
必须绑定阶段、合约、输出路径、trace、acceptance。
```

---

# 11. R00 Runtime 标准化

R00 是真实 token 验证核心。

必须准备：

```text
runtime_plane_context_manifest_schema.yaml
runtime_readiness_gate_schema.yaml
runtime_run_manifest_schema.yaml
token_case_manifest_schema.yaml
token_case_state_schema.yaml
phase_execution_plan_schema.yaml
phase_execution_record_schema.yaml
p08_permission_gate_schema.yaml
paper_runtime_invocation_schema.yaml
p09_review_trigger_schema.yaml
p10_upgrade_review_trigger_schema.yaml
full_pipeline_report_schema.yaml
```

R00 必须支持：

```text
single-token
batch-candidate
current-GMGN-pool
replay
scheduled-paper-cycle
```

R00 必须输出：

```text
run_id
token_case_manifest
phase_execution_records
p08_permission_gate
paper_runtime_invocation
p09_review_trigger
p10_upgrade_trigger
full_pipeline_report
final_decision_label
```

专业要求：

```text
R00 不只是跑流程。
R00 必须输出 EXCLUDE / RECORD / RISK_MONITOR / WATCH / PAPER_READY / READY_FOR_CONFIRMATION。
```

---

# 12. P08 Paper-only 风控标准化

Paper Runtime 不能随便进。

必须有 P08 permission gate：

```yaml
p08_permission:
  PAPER_RUNTIME_ALLOWED
  PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS
  PAPER_RUNTIME_PAUSED
  PAPER_RUNTIME_BLOCKED
  EXECUTION_RISK_REJECTED
```

P08 必须检查：

```text
quote
security
liquidity
sellability
slippage
cost
position size
market cap context
data freshness
risk event
paper-only boundary
```

必须准备：

```text
p08_permission_gate_schema.yaml
paper_runtime_permission_contract.yaml
execution_risk_policy.yaml
paper_only_boundary_policy.yaml
```

专业要求：

```text
P07 不能直接进入 paper runtime。
P08 是唯一入口。
```

---

# 13. Paper Runtime 标准化

Paper Runtime 必须是账本，不是报告。

必须准备：

```text
paper_position_schema.yaml
paper_trade_schema.yaml
paper_equity_curve_schema.yaml
paper_risk_event_schema.yaml
paper_exit_event_schema.yaml
paper_review_input_schema.yaml
```

每个 paper position 至少包含：

```yaml
position_id: string
run_id: string
token_address: string
entry_reason: string
entry_price_model: string
entry_market_cap: number
slippage_model: string
cost_model: string
risk_limits: object
p08_permission_id: string
trace_id: string
```

专业要求：

```text
paper 结果必须能进入 P09。
否则 paper 只是日报，不是学习系统。
```

---

# 14. P09 / P10 标准化

P09 负责复盘，不负责改规则。

P10 负责生成受控升级候选，不负责自动部署。

必须准备：

```text
p09_review_case_schema.yaml
p09_failure_attribution_schema.yaml
p09_success_attribution_schema.yaml
p09_to_p10_handoff_contract.yaml
p10_upgrade_candidate_schema.yaml
p10_controlled_upgrade_package_schema.yaml
regression_test_plan_schema.yaml
rollback_plan_schema.yaml
approval_policy.yaml
```

专业要求：

```text
P09 只能提出问题。
P10 只能生成候选。
真正系统更新必须经过 shadow / regression / approval。
```

---

# 15. HER_DOC 扫描标准化

HER_DOC 不能只扫描文件。

必须扫描：

```text
目标差距
阶段目标差距
方法轮缺口
系统对象缺口
R00 阻断项
旧脚本吸收
旧数据复盘价值
GPT 研究队列
HER 落地队列
```

必须输出：

```text
total_goal_gap_matrix.yaml
phase_goal_gap_matrix.yaml
method_loop_gap_matrix.yaml
r00_runtime_blocker_matrix.yaml
legacy_module_absorption_matrix.yaml
gpt_research_queue.yaml
her_build_queue.yaml
goal_mapping_issue_registry.yaml
```

专业要求：

```text
HER_DOC 的产物不是总结，而是问题清单和任务队列。
```

---

# 16. 问题清单 / 任务包标准化

专业系统必须有 issue registry。

问题不能只写在报告里。

必须准备：

```text
issue_registry_schema.yaml
issue_severity_policy.yaml
fix_route_policy.yaml
auto_repair_task_packet_contract.yaml
gpt_research_task_packet_contract.yaml
her_build_task_packet_contract.yaml
```

问题分流：

```text
HER_AUTO_REPAIR
GPT_RESEARCH_REQUIRED
K00_ASSETIZATION_REQUIRED
STAGE_COMPLETION_REQUIRED
R00_VALIDATION_REQUIRED
MANUAL_REVIEW_REQUIRED
```

你可能没完全考虑的是：

```text
报告如果不能转成 issue 和 task packet，就无法自动化修复。
```

---

# 17. GPT 研究资料标准化

GPT 研究不能是文章。

必须输出：

```text
核心机制
字段模型
数据来源
计算方式
证据规则
反证规则
hard negative rules
schema candidate
contract candidate
acceptance candidate
runner binding 建议
R00 binding 建议
P09/P10 字段
HER 落地任务书
```

必须准备：

```text
gpt_research_output_contract.yaml
research_to_k00_assetization_contract.yaml
research_quality_checklist.yaml
```

专业要求：

```text
GPT 研究资料必须能被 K00 资产化。
否则还是解释性文档。
```

---

# 18. K00 资产化标准化

K00 必须把研究资料转成系统对象。

必须准备：

```text
document_passport_schema.yaml
functional_object_registry_schema.yaml
system_mapping_matrix_schema.yaml
schema_candidate_registry.yaml
contract_candidate_registry.yaml
acceptance_candidate_registry.yaml
handoff_candidate_registry.yaml
```

K00 不能只做摘要。

专业要求：

```text
K00 的输出必须能进入 stage_completion_program。
```

---

# 19. Legacy 吸收标准化

你有大量旧脚本和旧数据。  
专业化必须处理 legacy。

必须准备：

```text
legacy_module_absorption_matrix.yaml
legacy_data_absorption_matrix.yaml
legacy_readonly_policy.yaml
legacy_to_phase_mapping.yaml
legacy_to_r00_binding_candidate.yaml
```

吸收方式：

```text
KEEP_AS_LEGACY_READONLY
WRAP_AS_ATOMIC_SKILL
MIGRATE_TO_MODULE
BIND_TO_PHASE_RUNNER
BIND_TO_R00
RETIRE_AFTER_REPLAY
```

专业要求：

```text
旧资产不能直接丢。
也不能直接进入主链。
必须分类吸收。
```

---

# 20. 测试与回归标准化

没有测试矩阵，系统不能算专业。

必须准备：

```text
unit_test_matrix.yaml
integration_test_matrix.yaml
r00_runtime_test_matrix.yaml
paper_runtime_test_matrix.yaml
p09_p10_replay_test_matrix.yaml
regression_test_matrix.yaml
shadow_validation_plan.yaml
```

最低测试：

```text
单 token dry-run
单 token paper-only
batch candidate paper-only
P08 blocked 不进 paper
P09 能读取 paper
P10 能生成升级候选
缺 trace 必阻断
缺 handoff 必阻断
旧数据 replay
```

---

# 21. 安全边界标准化

必须系统级写死：

```text
no_live_execution
no_wallet_signing
no_auto_order
no_auto_deploy
no_direct_rule_mutation
no_single_case_global_upgrade
```

必须准备：

```text
forbidden_use_policy.yaml
safety_boundary_policy.yaml
runtime_safety_guard.yaml
paper_only_enforcement_policy.yaml
```

专业要求：

```text
任何真实交易路径出现，都必须 BLOCK。
```

---

# 22. 报告标准化

报告不能只是人读。

报告必须同时服务：

```text
人工理解
P09 复盘
P10 升级
CPO 样本库
R00 验收
```

必须准备：

```text
full_pipeline_report_model.yaml
phase_report_model.yaml
paper_runtime_report_model.yaml
p09_review_report_model.yaml
p10_upgrade_report_model.yaml
goal_alignment_report_model.yaml
```

报告必须包含：

```text
结论
证据
反证
缺口
状态
下游权限
trace
acceptance
handoff
下一步
```

---

# 23. 运行观察与健康监控标准化

专业系统必须知道自己是否健康。

必须准备：

```text
operation_health_schema.yaml
runner_stability_schema.yaml
data_quality_monitor_schema.yaml
model_drift_monitor_schema.yaml
risk_event_schema.yaml
operation_metrics_schema.yaml
```

监控项：

```text
数据源是否可用
runner 是否失败
trace 是否断
handoff 是否断
acceptance 是否缺
paper 模型是否失真
P09/P10 是否滞后
样本数量是否不足
```

---

# 24. 版本与变更控制标准化

P10 生成升级候选后，不能直接改系统。

必须准备：

```text
change_request_schema.yaml
controlled_upgrade_package_schema.yaml
version_registry.yaml
shadow_validation_policy.yaml
regression_policy.yaml
approval_policy.yaml
rollback_policy.yaml
```

专业要求：

```text
所有系统更新必须可回滚。
所有规则升级必须经过 shadow / regression / approval。
```

---

# 25. 权限与执行边界标准化

系统必须知道谁能做什么。

必须准备：

```text
permission_matrix.yaml
write_permission_matrix.yaml
runtime_permission_policy.yaml
manual_approval_policy.yaml
operator_confirmation_policy.yaml
```

区分：

```text
AI 可建议
HER 可创建文件
Runner 可执行 dry-run
R00 可执行 paper-only
P10 可生成候选
人工才可批准高风险变更
```

---

# 26. 样本库标准化

CPO 的核心资产是样本库。

必须准备：

```text
sample_library_schema.yaml
review_case_library_schema.yaml
failure_case_schema.yaml
success_case_schema.yaml
blocked_case_schema.yaml
regression_case_schema.yaml
```

样本分类：

```text
PAPER_WIN
PAPER_LOSS
BLOCKED_CORRECTLY
FALSE_POSITIVE
FALSE_NEGATIVE
RISK_EVENT_CASE
INVALIDATION_CASE
MODEL_DRIFT_CASE
```

专业要求：

```text
没有样本库，系统无法学习。
```

---

# 27. 专业化需求总表

可以压缩为 12 个必备系统准备：

|编号|需求|作用|
|---|---|---|
|1|Goal Mapping|防止偏离真实 token 判断目标|
|2|Method Loop Mapping|让所有研究进入固定推理流程|
|3|Data Standard|字段来源、质量、权限统一|
|4|Schema / Contract Standard|阶段输入输出统一|
|5|Trace / Acceptance / Handoff|可复盘、可验收、可交接|
|6|Runner / Tool Binding|阶段能被 R00 调度|
|7|R00 Runtime Standard|真实 token 可运行|
|8|P08 Paper Gate|策略门禁后才 paper|
|9|P09/P10 Review Upgrade|结果能学习升级|
|10|Issue / Task Packet|扫描结果能自动修复|
|11|Legacy Absorption|旧资产能被系统吸收|
|12|Regression / Approval / Rollback|系统升级可控|

---

# 28. 你现在最容易忽略的准备

我认为你最可能忽略这 8 项：

## 1. 下游消费证明

不是输出 handoff 就够了，必须证明下游读取了。

```text
handoff_created ≠ handoff_consumed
```

## 2. 字段使用权限

字段不能因为存在就强判断。

```text
field_exists ≠ field_allowed_for_strong_evidence
```

## 3. READY_WITH_GAPS 的传播

带缺口的输出必须把限制传给下游。

```text
gap 不能在下游丢失
```

## 4. 旧数据分类

旧数据不能直接成为 canonical。

```text
legacy data 必须 reference / replay / sample / obsolete 分类
```

## 5. P09 复盘输入

paper 报告必须提前设计成 P09 可读，不是事后解释。

## 6. P10 升级边界

P10 只能生成升级候选，不能自动改规则。

## 7. R00 最终标签输出

R00 不能只输出 report，必须输出最终判断标签。

## 8. 自动修复边界

HER 可以修结构文件，不能发明交易判断模型。

---

# 29. 当前最优先级

不要一次全部做完。按阻断度排序：

```text
第一优先级：goal_mapping + 统一标准
第二优先级：HER_DOC 全体系扫描 + issue registry
第三优先级：R00 runtime blocker matrix
第四优先级：P02/P03/P04/P05 数据与判断基础
第五优先级：P07/P08 paper 门禁
第六优先级：P09/P10 复盘升级
第七优先级：CPO 持续样本库
第八优先级：shadow / regression / approval / rollback
```

---

# 最终结论

你已知的“全体系统一标准化”是对的，但专业化还必须补齐：

```text
目标映射
方法轮映射
数据血缘
字段权限
schema / contract
runner binding
trace / acceptance / handoff
R00 验证
P08 permission gate
P09/P10 复盘升级
issue registry
task packet
legacy absorption
sample library
regression / rollback
安全边界
```

最关键的一句话：

```text
专业化不是系统文件多，
而是每个文件、字段、runner、报告、判断都能被追踪、验收、交接、复盘，并服务真实 token 阶段化判断。
```