# H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS

## HER 文档到功能自动化落实系统：真实下游队列与交接证据层 v1.0

这一阶段目标是把前面完成的：

```text
A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS
```

继续推进到：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS
```

它代表系统已经可以把 A00 的真实总验收结果转化为：

```text
downstream target inventory
routing decision
target capability matrix
downstream queue
queue items
dependency graph
priority plan
gap / risk propagation binding
downstream handoff packets
queue state
trace / audit
final report
```

但它仍然是：

```text
READY_WITH_GAPS
```

不是：

```text
DOWNSTREAM_EXECUTED
SYSTEM_FULLY_IMPLEMENTED
PRODUCTION_READY
```

因为 H00 的责任是 **真实生成下游队列与交接包**，不是替下游阶段执行任务。

---

# 1. 阶段总定义

```yaml
status_code: H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS
status_family: DOWNSTREAM_QUEUE_RUNTIME_STATUS
owner_controller: H00_handoff_downstream_queue_controller

upstream_required_status:
  - A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS

required_upstream_assets:
  - A00 readiness_certificate
  - A00 real_evidence_bundle
  - A00 phase_status_matrix
  - A00 artifact_manifest
  - A00 gap_propagation_report
  - A00 acceptance_decision
  - A00 handoff_packet

downstream_targets:
  - U00_review_upgrade_controller
  - G00_governance_boundary_controller
  - PXX_phase_controllers
  - IXX_integration_controllers
  - R00_runner_tool_binding_controller
  - Report_Audit_System
  - Backlog_Upgrade_Queue
```

中文定义：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS 表示：
系统已经可以读取 A00 的真实验收证据和 readiness certificate，
并把其中的功能资产、验证证据、绑定证据、gap、风险、禁止动作、下游要求，
转化为真实 downstream queue、queue item、routing decision、handoff packet 和 queue state。

但由于下游任务尚未被 PXX/IXX/U00/G00 实际消费完成，所以状态只能是 READY_WITH_GAPS。
```

---

# 2. H00 真实队列阶段解决的问题

A00 已经回答：

```text
证据是否足够？
状态是否真实？
是否允许下游交接？
哪些 gap 仍然开放？
```

H00 必须继续回答：

```text
交给谁？
按什么优先级交？
每个下游需要什么输入？
下游必须输出什么？
哪些任务能执行？
哪些任务只能进入 review / backlog / governance？
哪些 gap 必须继续传播？
哪些 forbidden actions 必须继承？
哪些任务因为能力不足要阻断？
```

没有 H00_REAL 阶段，系统会停在：

```text
A00 已验收，但不知道如何落到下游执行。
```

有 H00_REAL 阶段后，系统进入：

```text
真实下游队列可生成，可被 U00/G00/PXX/IXX/R00 消费。
```

---

# 3. 本阶段不是做什么

|错误理解|正确理解|
|---|---|
|不是执行 PXX 任务|H00 只生成队列和交接包|
|不是启动 runner|R00 负责 runner binding|
|不是启动 paper runtime|paper runtime 需要单独授权|
|不是启用 live runtime|live 全局禁止|
|不是把 queue_created 当 completed|queue 只是待执行对象|
|不是删除 gap|所有 open gap 必须传播|
|不是把 READY_WITH_GAPS 改成 READY|必须保留真实缺口|
|不是自动修改生产规则|需要 G00 治理路径|

---

# 4. 阶段核心目标

建立：

```text
H00_real_downstream_queue_executor
```

核心链路：

```text
A00 readiness certificate
↓
A00 real evidence bundle
↓
A00 gap propagation report
↓
Downstream target classification
↓
Target capability matrix
↓
Routing decision
↓
Queue item builder
↓
Dependency graph
↓
Priority plan
↓
Gap / risk / forbidden action binding
↓
Downstream handoff packets
↓
Queue state
↓
H00 acceptance result
↓
H00 handoff to U00 / G00 / PXX / IXX / R00
```

---

# 5. 必须建立的系统目录

```text
/root/sikk-gmgn/system/her_document_function_system/handoff/
  h00_real_downstream_queue/
    01_h00_real_queue_manifest.yaml
    02_h00_real_queue_context_pack.md
    03_h00_real_queue_input_contract.json
    04_h00_real_queue_output_contract.json
    05_h00_real_queue_execution_protocol.md
    06_h00_real_queue_acceptance_gate.yaml
    07_h00_real_queue_state.json
    08_h00_real_queue_handoff.schema.json
    09_downstream_target.schema.json
    10_target_capability_matrix.schema.json
    11_routing_decision.schema.json
    12_queue_item.schema.json
    13_downstream_queue.schema.json
    14_dependency_graph.schema.json
    15_priority_plan.schema.json
    16_gap_risk_binding.schema.json
    17_downstream_handoff_packet.schema.json
    18_queue_state.schema.json
    19_failure_evidence.schema.json
    20_trace_audit_spec.yaml
    21_recovery_policy.md
    22_h00_real_queue_report_template.md
```

运行输出目录：

```text
/root/sikk-gmgn/data/her_document_function_system/h00_real_queue_runs/<queue_run_id>/
  input/
  preflight/
  downstream_targets/
  capability_matrix/
  routing/
  queue/
  dependency/
  priority/
  gap_risk/
  handoff_packets/
  queue_state/
  failure_evidence/
  trace/
  audit/
  acceptance/
  recovery/
  reports/
```

---

# 6. 必须建立的工具文件

```text
/root/sikk-gmgn/tools/
  h00_real_queue_executor.py
  h00_a00_handoff_loader.py
  h00_target_classifier.py
  h00_target_capability_checker.py
  h00_routing_decision_engine.py
  h00_queue_item_builder.py
  h00_dependency_graph_builder.py
  h00_priority_plan_builder.py
  h00_gap_risk_binder.py
  h00_downstream_handoff_writer.py
  h00_queue_state_writer.py
  h00_queue_status.py
```

|工具文件|责任|
|---|---|
|`h00_real_queue_executor.py`|H00 真实下游队列总入口|
|`h00_a00_handoff_loader.py`|读取 A00 handoff / certificate / evidence|
|`h00_target_classifier.py`|判断交给 U00/G00/PXX/IXX/R00/Backlog|
|`h00_target_capability_checker.py`|检查下游是否有接收能力|
|`h00_routing_decision_engine.py`|生成 routing decision|
|`h00_queue_item_builder.py`|生成 queue item|
|`h00_dependency_graph_builder.py`|生成任务依赖图|
|`h00_priority_plan_builder.py`|生成优先级计划|
|`h00_gap_risk_binder.py`|绑定 gap、risk、forbidden actions|
|`h00_downstream_handoff_writer.py`|写不同下游 handoff packet|
|`h00_queue_state_writer.py`|写 queue state|
|`h00_queue_status.py`|查询 H00 queue 状态|

---

# 7. 输入合约

## `03_h00_real_queue_input_contract.json`

```json
{
  "phase_id": "H00_REAL_DOWNSTREAM_QUEUE",
  "required_inputs": {
    "a00_handoff_packet": {
      "required": true,
      "description": "A00 real acceptance 到 H00 的交接包"
    },
    "readiness_certificate": {
      "required": true,
      "description": "A00 生成的 readiness certificate"
    },
    "real_evidence_bundle": {
      "required": true,
      "description": "A00 真实总证据包"
    },
    "phase_status_matrix": {
      "required": true,
      "description": "A00 阶段状态矩阵"
    },
    "artifact_manifest": {
      "required": true,
      "description": "A00 资产清单"
    },
    "gap_propagation_report": {
      "required": true,
      "description": "A00 gap 传播报告"
    },
    "acceptance_decision": {
      "required": true,
      "description": "A00 验收裁决"
    },
    "allowed_next_actions": {
      "required": true,
      "description": "A00 允许的下游动作"
    },
    "forbidden_next_actions": {
      "required": true,
      "description": "A00 禁止的下游动作"
    },
    "execution_boundary": {
      "required": true,
      "description": "执行边界"
    },
    "controller_registry": {
      "required": true,
      "description": "下游 controller 注册表"
    },
    "repo_root": {
      "required": true,
      "description": "仓库根目录"
    },
    "safe_mode": {
      "required": true,
      "description": "必须为 true"
    }
  }
}
```

---

# 8. 输出合约

## `04_h00_real_queue_output_contract.json`

```json
{
  "phase_id": "H00_REAL_DOWNSTREAM_QUEUE",
  "required_outputs": {
    "preflight_result": "preflight/h00_real_queue_preflight.json",
    "downstream_target_inventory": "downstream_targets/downstream_target_inventory.json",
    "target_capability_matrix": "capability_matrix/target_capability_matrix.json",
    "routing_decision": "routing/routing_decision.json",
    "downstream_queue": "queue/downstream_queue.json",
    "queue_items": "queue/queue_items.json",
    "dependency_graph": "dependency/dependency_graph.json",
    "priority_plan": "priority/priority_plan.json",
    "gap_risk_binding": "gap_risk/gap_risk_binding.json",
    "downstream_handoff_packets": "handoff_packets/",
    "queue_state": "queue_state/queue_state.json",
    "failure_evidence": "failure_evidence/h00_queue_failure_evidence.json",
    "trace_log": "trace/h00_real_queue_trace.jsonl",
    "audit_log": "audit/h00_real_queue_audit.jsonl",
    "acceptance_result": "acceptance/h00_real_queue_acceptance.json",
    "recovery_report": "recovery/recovery_report.json",
    "final_report": "reports/h00_real_queue_report.md"
  }
}
```

---

# 9. H00 真实队列内部流程

```text
H00_REAL.0 Preflight Gate
H00_REAL.1 A00 Evidence Loader
H00_REAL.2 Readiness Certificate Interpreter
H00_REAL.3 Downstream Target Classifier
H00_REAL.4 Target Capability Matrix Builder
H00_REAL.5 Routing Decision Engine
H00_REAL.6 Queue Item Builder
H00_REAL.7 Dependency Graph Builder
H00_REAL.8 Priority Plan Builder
H00_REAL.9 Gap / Risk / Forbidden Action Binder
H00_REAL.10 Downstream Handoff Packet Writer
H00_REAL.11 Queue State Writer
H00_REAL.12 Failure Evidence Builder
H00_REAL.13 Acceptance Gate
H00_REAL.14 Final Report Writer
```

---

# 10. H00_REAL.0 Preflight Gate

## 10.1 检查项

|检查项|要求|
|---|---|
|A00 handoff 是否存在|必须|
|readiness certificate 是否存在|必须|
|A00 final status 是否允许交接|必须|
|real_evidence_bundle 是否存在|必须|
|gap_propagation_report 是否存在|必须|
|allowed_next_actions 是否存在|必须|
|forbidden_next_actions 是否存在|必须|
|controller_registry 是否存在|必须|
|safe_mode 是否为 true|必须|
|live / signing / deploy / trading 是否禁止|必须|

## 10.2 输出

```json
{
  "preflight_status": "PASSED",
  "safe_mode": true,
  "a00_status": "A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS",
  "readiness_level": "HANDOFF_READY_WITH_NON_BLOCKING_GAPS",
  "loaded_inputs": [
    "a00_handoff_packet",
    "readiness_certificate",
    "real_evidence_bundle",
    "gap_propagation_report",
    "controller_registry"
  ],
  "forbidden_actions_checked": [
    "live_runtime",
    "wallet_signing",
    "auto_deploy",
    "production_trading"
  ],
  "blocking_gaps": []
}
```

---

# 11. H00_REAL.1 A00 Evidence Loader

必须加载：

```text
a00_handoff_packet
readiness_certificate
real_evidence_bundle
phase_status_matrix
artifact_manifest
gap_propagation_report
acceptance_decision
allowed_next_actions
forbidden_next_actions
```

输出：

```json
{
  "loader_status": "LOADED",
  "loaded_evidence_groups": [
    "readiness_certificate",
    "real_evidence_bundle",
    "phase_status_matrix",
    "gap_propagation_report",
    "acceptance_decision"
  ],
  "missing_evidence": [],
  "invalid_refs": [],
  "handoff_allowed": true
}
```

---

# 12. H00_REAL.2 Readiness Certificate Interpreter

## 12.1 必须解释字段

```text
final_status
readiness_level
accepted_phases
open_gaps
accepted_risks
allowed_next_actions
forbidden_next_actions
ready_for_h00
ready_for_u00
ready_for_g00
ready_for_production
```

## 12.2 解释输出

```json
{
  "certificate_interpretation_id": "cert_interp_h00_<timestamp>",
  "final_status": "A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS",
  "readiness_level": "HANDOFF_READY_WITH_NON_BLOCKING_GAPS",
  "handoff_allowed": true,
  "execution_allowed": false,
  "queue_generation_allowed": true,
  "must_route_to_u00": true,
  "must_route_to_g00": true,
  "production_allowed": false,
  "reason": "A00 evidence is sufficient for downstream queue, but open gaps and governance pending items remain."
}
```

---

# 13. H00_REAL.3 Downstream Target Classifier

## 13.1 目标分类

H00 必须把 A00 输出中的对象分流到不同下游：

|输入对象|下游目标|
|---|---|
|open gaps|U00|
|policy candidates / governance risk|G00|
|controller upgrade needs|PXX / U00|
|integration upgrade needs|IXX / U00|
|safe dry-run binding evidence|A00 / Report / R00|
|run-document 准备项|O00 / K00 / F00|
|production risk|G00|
|report / audit 输出|Report_Audit_System|
|未能执行项|Backlog / U00|

## 13.2 `downstream_target_inventory.json`

```json
{
  "inventory_id": "downstream_target_inventory_h00_<timestamp>",
  "targets": [
    {
      "target_id": "target_u00_review_upgrade",
      "target_type": "U00_REVIEW_UPGRADE",
      "target_controller": "U00",
      "reason": "A00 contains open gaps and READY_WITH_GAPS status",
      "handoff_required": true,
      "execution_allowed": true
    },
    {
      "target_id": "target_g00_governance",
      "target_type": "G00_GOVERNANCE_BOUNDARY",
      "target_controller": "G00",
      "reason": "policy_not_active and evidence policy candidates require governance review",
      "handoff_required": true,
      "execution_allowed": true
    },
    {
      "target_id": "target_o00_run_document_preparation",
      "target_type": "O00_PIPELINE_PREPARATION",
      "target_controller": "O00",
      "reason": "next stage requires run-document safe-mode preparation",
      "handoff_required": true,
      "execution_allowed": false
    }
  ]
}
```

---

# 14. H00_REAL.4 Target Capability Matrix Builder

## 14.1 能力检查

每个目标必须检查：

```text
controller_registered
input_contract_exists
can_accept_handoff
can_accept_gap_refs
can_accept_evidence_refs
can_accept_forbidden_actions
requires_additional_contract
target_status
```

## 14.2 `target_capability_matrix.json`

```json
{
  "matrix_id": "target_capability_matrix_h00_<timestamp>",
  "targets": [
    {
      "target_controller": "U00",
      "controller_registered": true,
      "input_contract_exists": true,
      "can_accept_review_cases": true,
      "can_accept_gap_refs": true,
      "can_accept_failure_refs": true,
      "can_accept_evidence_refs": true,
      "target_status": "TARGET_READY"
    },
    {
      "target_controller": "G00",
      "controller_registered": true,
      "input_contract_exists": true,
      "can_accept_governance_candidates": true,
      "can_accept_policy_risk_refs": true,
      "can_accept_evidence_refs": true,
      "target_status": "TARGET_READY_WITH_GAPS",
      "gaps": [
        "policy_activation_workflow_not_yet_executed"
      ]
    }
  ],
  "matrix_status": "BUILT"
}
```

---

# 15. H00_REAL.5 Routing Decision Engine

## 15.1 路由状态

```text
ROUTE_TO_U00
ROUTE_TO_G00
ROUTE_TO_PXX
ROUTE_TO_IXX
ROUTE_TO_R00
ROUTE_TO_O00
ROUTE_TO_REPORT
ROUTE_TO_BACKLOG
ROUTE_TO_RECOVERY
BLOCK_ROUTE
```

## 15.2 `routing_decision.json`

```json
{
  "routing_decision_id": "routing_h00_<timestamp>",
  "routes": [
    {
      "route_id": "route_to_u00_gap_review",
      "target_controller": "U00",
      "decision": "ROUTE_TO_U00",
      "reason": "A00 real acceptance has open gaps and READY_WITH_GAPS status",
      "priority": "P0_CRITICAL",
      "required_handoff_packet": "handoff_packets/h00_to_u00_handoff_packet.json",
      "execution_allowed": true
    },
    {
      "route_id": "route_to_g00_policy_review",
      "target_controller": "G00",
      "decision": "ROUTE_TO_G00",
      "reason": "policy_not_active and evidence policy candidate require governance boundary update",
      "priority": "P0_CRITICAL",
      "required_handoff_packet": "handoff_packets/h00_to_g00_handoff_packet.json",
      "execution_allowed": true
    },
    {
      "route_id": "route_to_o00_run_document_safe_mode",
      "target_controller": "O00",
      "decision": "ROUTE_TO_O00",
      "reason": "prepare next stage: run-document safe-mode, but do not execute production",
      "priority": "P2_MEDIUM",
      "required_handoff_packet": "handoff_packets/h00_to_o00_handoff_packet.json",
      "execution_allowed": false
    }
  ]
}
```

---

# 16. H00_REAL.6 Queue Item Builder

## 16.1 queue item 必须字段

```text
queue_item_id
source_phase
target_controller
task_type
priority
status
required_inputs
expected_outputs
allowed_actions
forbidden_actions
gap_refs
risk_refs
evidence_refs
handoff_packet_ref
acceptance_requirements
created_at
```

## 16.2 `queue_items.json`

```json
{
  "queue_items": [
    {
      "queue_item_id": "queue_h00_u00_review_gaps",
      "source_phase": "H00_REAL_DOWNSTREAM_QUEUE",
      "target_controller": "U00",
      "task_type": "REVIEW_OPEN_GAPS_AND_BUILD_UPGRADE_QUEUE",
      "priority": "P0_CRITICAL",
      "status": "QUEUED",
      "required_inputs": [
        "readiness_certificate",
        "gap_propagation_report",
        "acceptance_decision",
        "real_evidence_bundle"
      ],
      "expected_outputs": [
        "review_cases",
        "root_cause_analysis",
        "upgrade_candidates",
        "upgrade_queue",
        "u00_handoff"
      ],
      "allowed_actions": [
        "load_handoff",
        "classify_review_cases",
        "build_upgrade_queue",
        "write_learning_index"
      ],
      "forbidden_actions": [
        "live_runtime",
        "wallet_signing",
        "auto_deploy",
        "production_trading",
        "mark_upgrade_applied_without_execution"
      ],
      "gap_refs": [
        "policy_not_active",
        "paper_runtime_not_enabled",
        "run_document_not_validated"
      ],
      "risk_refs": [
        "safe_dry_run_only"
      ],
      "handoff_packet_ref": "handoff_packets/h00_to_u00_handoff_packet.json"
    },
    {
      "queue_item_id": "queue_h00_g00_policy_review",
      "source_phase": "H00_REAL_DOWNSTREAM_QUEUE",
      "target_controller": "G00",
      "task_type": "REVIEW_AND_REGISTER_GOVERNANCE_POLICY_CANDIDATES",
      "priority": "P0_CRITICAL",
      "status": "QUEUED",
      "required_inputs": [
        "governance_candidate_refs",
        "evidence_policy_gap_refs",
        "forbidden_actions",
        "trace_audit_refs"
      ],
      "expected_outputs": [
        "policy_conflict_report",
        "pending_policy_bundle",
        "active_policy_bundle_if_accepted",
        "g00_handoff"
      ],
      "allowed_actions": [
        "classify_governance_candidate",
        "check_policy_conflict",
        "write_policy_registry"
      ],
      "forbidden_actions": [
        "activate_policy_without_acceptance",
        "weaken_forbidden_actions",
        "silent_policy_overwrite"
      ],
      "handoff_packet_ref": "handoff_packets/h00_to_g00_handoff_packet.json"
    }
  ]
}
```

---

# 17. H00_REAL.7 Dependency Graph Builder

## `dependency_graph.json`

```json
{
  "graph_id": "dependency_graph_h00_<timestamp>",
  "nodes": [
    {
      "queue_item_id": "queue_h00_u00_review_gaps",
      "target_controller": "U00"
    },
    {
      "queue_item_id": "queue_h00_g00_policy_review",
      "target_controller": "G00"
    },
    {
      "queue_item_id": "queue_h00_o00_run_document_safe_mode",
      "target_controller": "O00"
    }
  ],
  "edges": [
    {
      "from": "queue_h00_u00_review_gaps",
      "to": "queue_h00_g00_policy_review",
      "dependency_type": "GOVERNANCE_CANDIDATES_FROM_U00"
    },
    {
      "from": "queue_h00_g00_policy_review",
      "to": "queue_h00_o00_run_document_safe_mode",
      "dependency_type": "REQUIRES_POLICY_REVIEW_FIRST"
    }
  ],
  "blocked_nodes": [],
  "execution_order": [
    "queue_h00_u00_review_gaps",
    "queue_h00_g00_policy_review",
    "queue_h00_o00_run_document_safe_mode"
  ]
}
```

---

# 18. H00_REAL.8 Priority Plan Builder

## 18.1 优先级规则

|优先级|用途|
|---|---|
|P0_CRITICAL|阻断后续闭环或治理安全|
|P1_HIGH|影响核心验证/绑定/验收质量|
|P2_MEDIUM|影响可用性和扩展|
|P3_LOW|报告、展示、整理|
|P4_BACKLOG|后续优化|

## 18.2 `priority_plan.json`

```json
{
  "priority_plan_id": "priority_plan_h00_<timestamp>",
  "items": [
    {
      "queue_item_id": "queue_h00_u00_review_gaps",
      "priority": "P0_CRITICAL",
      "reason": [
        "open_gaps_exist",
        "ready_with_gaps_must_be_reviewed",
        "upgrade_queue_required"
      ]
    },
    {
      "queue_item_id": "queue_h00_g00_policy_review",
      "priority": "P0_CRITICAL",
      "reason": [
        "policy_not_active",
        "forbidden_action_policy_must_be_preserved",
        "evidence_policy_candidate_exists"
      ]
    },
    {
      "queue_item_id": "queue_h00_o00_run_document_safe_mode",
      "priority": "P2_MEDIUM",
      "reason": [
        "next capability milestone",
        "requires U00/G00 first"
      ]
    }
  ]
}
```

---

# 19. H00_REAL.9 Gap / Risk / Forbidden Action Binder

## 19.1 必须绑定的对象

```text
open_gaps
accepted_risks
blocking_conditions
forbidden_actions
safe_mode_required
trace_requirements
acceptance_requirements
handoff_requirements
```

## 19.2 `gap_risk_binding.json`

```json
{
  "binding_id": "gap_risk_binding_h00_<timestamp>",
  "bindings": [
    {
      "queue_item_id": "queue_h00_u00_review_gaps",
      "gap_refs": [
        "policy_not_active",
        "paper_runtime_not_enabled",
        "run_document_not_validated"
      ],
      "risk_refs": [
        "safe_dry_run_only"
      ],
      "forbidden_actions": [
        "live_runtime",
        "wallet_signing",
        "auto_deploy",
        "production_trading"
      ],
      "must_preserve_in_downstream": true
    },
    {
      "queue_item_id": "queue_h00_g00_policy_review",
      "gap_refs": [
        "policy_not_active"
      ],
      "risk_refs": [
        "governance_candidate_not_active"
      ],
      "forbidden_actions": [
        "weaken_forbidden_actions",
        "silent_policy_overwrite",
        "activate_policy_without_acceptance"
      ],
      "must_preserve_in_downstream": true
    }
  ]
}
```

---

# 20. H00_REAL.10 Downstream Handoff Packet Writer

必须生成不同下游的不同 handoff，不能只生成一个总包。

```text
handoff_packets/h00_to_u00_handoff_packet.json
handoff_packets/h00_to_g00_handoff_packet.json
handoff_packets/h00_to_o00_handoff_packet.json
handoff_packets/h00_to_report_audit_handoff_packet.json
handoff_packets/h00_to_backlog_handoff_packet.json
```

## 20.1 U00 handoff 示例

```json
{
  "handoff_id": "handoff_h00_to_u00_<timestamp>",
  "from_phase": "H00_REAL_DOWNSTREAM_QUEUE",
  "to_phase": "U00_REVIEW_UPGRADE",
  "handoff_type": "QUEUE_TO_REVIEW_UPGRADE",
  "source_acceptance_run_id": "a00_real_<timestamp>",
  "readiness_certificate_refs": [
    "certificate/readiness_certificate.json"
  ],
  "real_evidence_bundle_refs": [
    "evidence_bundle/real_evidence_bundle.json"
  ],
  "gap_refs": [
    "policy_not_active",
    "paper_runtime_not_enabled",
    "run_document_not_validated"
  ],
  "queue_item_refs": [
    "queue_h00_u00_review_gaps"
  ],
  "required_next_action": "build_review_cases_and_upgrade_queue",
  "allowed_next_actions": [
    "classify_review_cases",
    "build_root_cause_analysis",
    "build_upgrade_candidates",
    "write_learning_index"
  ],
  "forbidden_next_actions": [
    "mark_upgrade_completed_without_execution",
    "delete_gap_evidence",
    "live_runtime",
    "wallet_signing"
  ],
  "handoff_status": "HANDOFF_READY_WITH_GAPS"
}
```

## 20.2 G00 handoff 示例

```json
{
  "handoff_id": "handoff_h00_to_g00_<timestamp>",
  "from_phase": "H00_REAL_DOWNSTREAM_QUEUE",
  "to_phase": "G00_GOVERNANCE_BOUNDARY",
  "handoff_type": "QUEUE_TO_GOVERNANCE_REVIEW",
  "governance_candidate_refs": [
    "evidence_policy_candidate",
    "status_code_policy_candidate"
  ],
  "evidence_refs": [
    "real_evidence_bundle.json",
    "status_consistency_report.json",
    "gap_propagation_report.json"
  ],
  "required_next_action": "classify_and_validate_policy_candidates",
  "allowed_next_actions": [
    "build_policy_conflict_report",
    "write_pending_policy_bundle",
    "write_governance_registry"
  ],
  "forbidden_next_actions": [
    "activate_policy_without_acceptance",
    "weaken_forbidden_actions",
    "silent_policy_overwrite"
  ],
  "handoff_status": "HANDOFF_READY_WITH_GAPS"
}
```

---

# 21. H00_REAL.11 Queue State Writer

## `queue_state.json`

```json
{
  "queue_id": "downstream_queue_h00_<timestamp>",
  "queue_status": "QUEUE_READY_WITH_GAPS",
  "source_acceptance_status": "A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS",
  "total_items": 3,
  "ready_items": 2,
  "blocked_items": 0,
  "deferred_items": 1,
  "review_items": 1,
  "governance_items": 1,
  "created_at": "",
  "last_updated_at": "",
  "next_dispatch_candidates": [
    "queue_h00_u00_review_gaps",
    "queue_h00_g00_policy_review"
  ],
  "forbidden_global_actions": [
    "live_runtime",
    "wallet_signing",
    "auto_deploy",
    "production_trading"
  ]
}
```

## 队列状态定义

```text
QUEUE_READY
QUEUE_READY_WITH_GAPS
QUEUE_BLOCKED
ITEM_QUEUED
ITEM_READY
ITEM_BLOCKED
ITEM_DEFERRED
ITEM_DISPATCHED
ITEM_ACCEPTED_BY_TARGET
ITEM_REJECTED_BY_TARGET
ITEM_COMPLETED
ITEM_FAILED
```

当前目标状态应是：

```text
QUEUE_READY_WITH_GAPS
```

---

# 22. H00_REAL.12 Failure Evidence Builder

即使没有失败，也必须生成空结构。

```json
{
  "failure_evidence_id": "h00_queue_failure_<timestamp>",
  "queue_run_id": "h00_real_<timestamp>",
  "failures": []
}
```

失败示例：

```json
{
  "failure_id": "failure_h00_001",
  "failure_type": "TARGET_CAPABILITY_MISSING",
  "gap_level": "BLOCKING_GAP",
  "affected_target": "G00",
  "failure_reason": "G00 input contract missing or cannot accept governance candidates",
  "required_fix": "Create or repair G00 input contract before dispatch",
  "can_continue": false,
  "route_to": "U00"
}
```

---

# 23. H00_REAL.13 Acceptance Gate

## 23.1 最终状态

允许状态：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS
H00_REAL_DOWNSTREAM_QUEUE_BLOCKED
H00_REAL_DOWNSTREAM_QUEUE_REJECTED
```

目标状态：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS
```

## 23.2 acceptance result

```json
{
  "acceptance_id": "h00_real_queue_acceptance_<timestamp>",
  "final_status": "H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS",
  "queue_status": "QUEUE_READY_WITH_GAPS",
  "reason": "A00 real acceptance evidence is loaded and downstream queue/handoff packets are generated, but downstream targets have not yet consumed or completed the queue items.",
  "ready_for_u00": true,
  "ready_for_g00": true,
  "ready_for_pxx": false,
  "ready_for_production": false,
  "blocking_gaps": [],
  "non_blocking_gaps": [
    "downstream_items_not_executed",
    "policy_not_active",
    "run_document_not_validated"
  ],
  "forbidden_claims_blocked": [
    "DOWNSTREAM_EXECUTED",
    "QUEUE_COMPLETED",
    "POLICY_ACTIVE",
    "PRODUCTION_READY"
  ]
}
```

---

# 24. 为什么仍然是 READY_WITH_GAPS

即使 H00 成功生成真实下游队列，也不能标记为完成闭环。

原因：

```text
1. H00 只生成 queue，不执行 queue。
2. U00 还未实际消费 review queue。
3. G00 还未实际消费 governance queue。
4. PXX / IXX 尚未读取并应用 handoff。
5. policy 仍可能是 pending，不是 active。
6. run-document safe-mode 尚未真实运行。
7. paper/live runtime 没有授权。
8. production trading 全局禁止。
```

所以正确状态是：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS
```

不是：

```text
DOWNSTREAM_EXECUTED
QUEUE_COMPLETED
SYSTEM_FULLY_IMPLEMENTED
PIPELINE_ACCEPTED
PRODUCTION_READY
```

---

# 25. 阶段验收门

## 25.1 必须通过项

|验收项|要求|
|---|---|
|A00 handoff 已加载|必须|
|readiness_certificate 已加载|必须|
|real_evidence_bundle 已加载|必须|
|gap_propagation_report 已加载|必须|
|downstream_target_inventory 已生成|必须|
|target_capability_matrix 已生成|必须|
|routing_decision 已生成|必须|
|downstream_queue 已生成|必须|
|queue_items 已生成|必须|
|dependency_graph 已生成|必须|
|priority_plan 已生成|必须|
|gap_risk_binding 已生成|必须|
|downstream handoff packets 已生成|必须|
|queue_state 已生成|必须|
|failure_evidence 已生成|必须|
|trace / audit 已生成|必须|
|final_report 已生成|必须|
|final_status = READY_WITH_GAPS|必须|

---

## 25.2 不允许通过的情况

```text
没有 A00 handoff
没有 readiness_certificate
没有 queue_items
没有 routing_decision
没有 handoff_packets
没有 gap_risk_binding
没有 queue_state
A00_BLOCKED 仍进入 execution queue
open gap 被删除
forbidden actions 被删除
queue_created 被标记为 task_completed
policy_candidate 被标记为 policy_active
live runtime 被启动
wallet signing 被请求
```

---

# 26. 推荐测试目录

```text
/root/sikk-gmgn/tests/her_document_function_system/
  test_h00_requires_a00_handoff.py
  test_h00_queue_item_required_fields.py
  test_h00_routing_decision_targets.py
  test_h00_gap_risk_binding_preserves_gaps.py
  test_h00_forbidden_actions_inherited.py
  test_h00_no_queue_completed_without_execution.py
  test_h00_no_policy_active_claim.py
  test_h00_queue_state_required_fields.py
```

---

# 27. 关键测试用例

## 27.1 没有 A00 handoff 不能生成队列

```python
def test_h00_requires_a00_handoff():
    inputs = {
        "a00_handoff_packet": None,
        "readiness_certificate": "certificate.json"
    }

    assert inputs["a00_handoff_packet"] is None
```

真实 executor 应返回：

```text
H00_BLOCKED_MISSING_A00_HANDOFF
```

---

## 27.2 queue_created 不能等于 completed

```python
def test_queue_created_is_not_completed():
    queue_state = {
        "queue_status": "QUEUE_CREATED",
        "task_status": "ITEM_COMPLETED"
    }

    assert queue_state["queue_status"] == "QUEUE_CREATED"
    assert queue_state["task_status"] != "VALID_COMPLETED_STATUS"
```

真实 validator 应返回：

```text
QUEUE_STATUS_INCONSISTENT
```

---

## 27.3 forbidden actions 必须继承

```python
def test_forbidden_actions_inherited():
    queue_item = {
        "queue_item_id": "queue_h00_g00_policy_review",
        "forbidden_actions": []
    }

    required_forbidden = [
        "live_runtime",
        "wallet_signing",
        "auto_deploy",
        "production_trading"
    ]

    missing = [a for a in required_forbidden if a not in queue_item["forbidden_actions"]]

    assert missing
```

真实 validator 应返回：

```text
FORBIDDEN_ACTIONS_NOT_INHERITED
```

---

# 28. Final Report 模板

```markdown
# H00 Real Downstream Queue Report

## 1. Run Info

- queue_run_id:
- source_acceptance_run_id:
- source_pipeline_run_id:
- repo_root:
- safe_mode:
- started_at:
- completed_at:
- final_status:

## 2. Loaded A00 Evidence

- A00 handoff:
- readiness_certificate:
- real_evidence_bundle:
- phase_status_matrix:
- gap_propagation_report:
- acceptance_decision:

## 3. Readiness Interpretation

- readiness_level:
- handoff_allowed:
- queue_generation_allowed:
- execution_allowed:
- production_allowed:

## 4. Downstream Targets

| Target | Type | Status | Reason |
|---|---|---|---|

## 5. Target Capability Matrix

## 6. Routing Decisions

## 7. Queue Items

| Queue Item | Target | Priority | Status |
|---|---|---|---|

## 8. Dependency Graph

## 9. Priority Plan

## 10. Gap / Risk / Forbidden Action Binding

## 11. Handoff Packets

## 12. Queue State

## 13. Failure Evidence

## 14. Trace / Audit

## 15. Final Decision
```

---

# 29. 可直接给 HER 的执行任务书

```text
任务：建立并执行 H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS 阶段

你不是继续写 H00 设计说明，而是建立真实下游队列与交接执行层，让 H00 从 handoff design 进入 real downstream queue evidence 阶段。

目标：
在 /root/sikk-gmgn 中建立 H00 real queue 工具链，读取 A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS 输出的 A00 handoff、readiness_certificate、real_evidence_bundle、phase_status_matrix、artifact_manifest、gap_propagation_report、acceptance_decision，并生成真实 downstream_target_inventory、target_capability_matrix、routing_decision、downstream_queue、queue_items、dependency_graph、priority_plan、gap_risk_binding、downstream handoff packets、queue_state、trace、audit 和 final report。

必须建立目录：

/root/sikk-gmgn/system/her_document_function_system/handoff/h00_real_downstream_queue/
/root/sikk-gmgn/data/her_document_function_system/h00_real_queue_runs/

必须创建系统文件：

01_h00_real_queue_manifest.yaml
02_h00_real_queue_context_pack.md
03_h00_real_queue_input_contract.json
04_h00_real_queue_output_contract.json
05_h00_real_queue_execution_protocol.md
06_h00_real_queue_acceptance_gate.yaml
07_h00_real_queue_state.json
08_h00_real_queue_handoff.schema.json
09_downstream_target.schema.json
10_target_capability_matrix.schema.json
11_routing_decision.schema.json
12_queue_item.schema.json
13_downstream_queue.schema.json
14_dependency_graph.schema.json
15_priority_plan.schema.json
16_gap_risk_binding.schema.json
17_downstream_handoff_packet.schema.json
18_queue_state.schema.json
19_failure_evidence.schema.json
20_trace_audit_spec.yaml
21_recovery_policy.md
22_h00_real_queue_report_template.md

必须创建工具文件：

tools/h00_real_queue_executor.py
tools/h00_a00_handoff_loader.py
tools/h00_target_classifier.py
tools/h00_target_capability_checker.py
tools/h00_routing_decision_engine.py
tools/h00_queue_item_builder.py
tools/h00_dependency_graph_builder.py
tools/h00_priority_plan_builder.py
tools/h00_gap_risk_binder.py
tools/h00_downstream_handoff_writer.py
tools/h00_queue_state_writer.py
tools/h00_queue_status.py

必须创建测试文件：

tests/her_document_function_system/test_h00_requires_a00_handoff.py
tests/her_document_function_system/test_h00_queue_item_required_fields.py
tests/her_document_function_system/test_h00_routing_decision_targets.py
tests/her_document_function_system/test_h00_gap_risk_binding_preserves_gaps.py
tests/her_document_function_system/test_h00_forbidden_actions_inherited.py
tests/her_document_function_system/test_h00_no_queue_completed_without_execution.py
tests/her_document_function_system/test_h00_no_policy_active_claim.py
tests/her_document_function_system/test_h00_queue_state_required_fields.py

必须执行命令：

cd /root/sikk-gmgn

python3 tools/h00_real_queue_executor.py \
  --a00-handoff data/her_document_function_system/a00_real_acceptance_runs/<acceptance_run_id>/handoff/a00_real_acceptance_to_h00_handoff.json \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/h00_real_queue_runs/<queue_run_id> \
  --safe-mode

必须输出：

- preflight/h00_real_queue_preflight.json
- downstream_targets/downstream_target_inventory.json
- capability_matrix/target_capability_matrix.json
- routing/routing_decision.json
- queue/downstream_queue.json
- queue/queue_items.json
- dependency/dependency_graph.json
- priority/priority_plan.json
- gap_risk/gap_risk_binding.json
- handoff_packets/h00_to_u00_handoff_packet.json
- handoff_packets/h00_to_g00_handoff_packet.json
- handoff_packets/h00_to_o00_handoff_packet.json
- queue_state/queue_state.json
- failure_evidence/h00_queue_failure_evidence.json
- trace/h00_real_queue_trace.jsonl
- audit/h00_real_queue_audit.jsonl
- acceptance/h00_real_queue_acceptance.json
- recovery/recovery_report.json
- reports/h00_real_queue_report.md

必须保证：

1. safe_mode 必须为 true。
2. 禁止 live_runtime。
3. 禁止 wallet_signing。
4. 禁止 auto_deploy。
5. 禁止 production_trading。
6. 禁止 execute_real_order。
7. 必须加载 A00 handoff。
8. 必须加载 readiness_certificate。
9. 必须加载 real_evidence_bundle。
10. 必须生成 downstream_target_inventory。
11. 必须生成 target_capability_matrix。
12. 必须生成 routing_decision。
13. 必须生成 queue_items。
14. 每个 queue_item 必须包含 target_controller、task_type、priority、required_inputs、expected_outputs、allowed_actions、forbidden_actions、gap_refs、handoff_packet_ref。
15. 必须生成 dependency_graph。
16. 必须生成 priority_plan。
17. 必须生成 gap_risk_binding，且不得删除 open gaps。
18. forbidden_actions 必须继承到每个 queue item 和 handoff packet。
19. 必须生成 U00/G00/O00 至少三类 handoff packet。
20. queue_state 必须是 QUEUE_READY_WITH_GAPS，除非出现 blocking failure。
21. 不能把 queue_created 标记为 task_completed。
22. 不能把 governance candidate 标记为 POLICY_ACTIVE。
23. 不能把下游队列生成标记为下游任务已执行。
24. 最终状态必须是 H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS，除非存在 blocking failure。

验收标准：

- 所有系统文件存在。
- 所有 tools/h00_*.py 文件存在。
- 所有 tests/her_document_function_system/test_h00_*.py 文件存在。
- h00_real_queue_executor.py 可执行。
- downstream_target_inventory.json 存在。
- routing_decision.json 存在。
- queue_items.json 存在且字段完整。
- dependency_graph.json 存在。
- priority_plan.json 存在。
- gap_risk_binding.json 存在并保留 open gaps。
- handoff_packets 至少包含 U00/G00/O00 handoff。
- queue_state.json final queue_status = QUEUE_READY_WITH_GAPS。
- acceptance/h00_real_queue_acceptance.json final_status = H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS。
- final report 存在。
```

---

# 30. 当前设计状态判断

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS 阶段体系：已建立
专业化程度：轻量机构级真实下游队列与交接证据层设计完成
数据完整性：覆盖 target inventory、capability matrix、routing、queue item、dependency、priority、gap/risk binding、handoff packet、queue state、failure、trace、audit、report
工程状态：需要 HER 实际创建文件并运行 h00_real_queue_executor.py
当前真实状态：REAL_DOWNSTREAM_QUEUE_BLUEPRINT_READY

不能宣称：
- H00_REAL_QUEUE_EXECUTED
- DOWNSTREAM_TASKS_COMPLETED
- U00_UPGRADE_APPLIED
- G00_POLICY_ACTIVE
- PIPELINE_ACCEPTED
- PRODUCTION_READY
```

---

# 31. 下一步

完成这个阶段后，系统会从：

```text
A00 真实总验收证据可生成
```

升级到：

```text
H00 真实下游队列可生成
```

下一阶段应该是：

```text
U00_REAL_REVIEW_UPGRADE_QUEUE_READY_WITH_GAPS
```

也就是让 U00 真正消费 H00 生成的 review queue，把 open gaps、failure、READY_WITH_GAPS、policy_not_active、run_document_not_validated 等转化为：

```text
review cases
root cause analysis
upgrade candidates
upgrade queue
learning index
governance candidates
U00 handoff
```

最终判断：

```text
H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS 是系统从“真实验收”进入“真实下游调度”的关键门槛。

它证明系统不只是知道哪里有 gap，而是可以把 gap、风险、证据、禁止动作和下一步任务转化为可追踪的下游队列。

但只要 U00/G00/PXX/IXX 尚未消费队列，就必须保留 READY_WITH_GAPS。
```