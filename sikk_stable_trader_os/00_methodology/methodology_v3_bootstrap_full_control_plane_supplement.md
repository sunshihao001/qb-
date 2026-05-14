# Methodology v3 Supplement: Bootstrap Control Plane / Full Control Plane Split

文件编号：METHODOLOGY-SUPPLEMENT-003
来源文档：DOC-20260511-007
状态：AUTHORITATIVE_METHODOLOGY_SUPPLEMENT
适用系统：SIKK Stable Trader OS
适用执行器：HER / P00_system_bootstrap_controller / Plane Validators
安全边界：paper-only；禁止真实交易；禁止启动 P01；禁止自动下单
写入时间：2026-05-11T15:46:58.346373+00:00

## 1. 本补丁定位

本文件是 `system_methodology_blueprint.md` 的 v3.0 方法论补充，不替代 v2.0 总宪法，而是修正并细化 Control Plane 的阶段位置与职责拆分。

核心裁决：Control Plane 不应被理解为只在 Data Plane 之后生成的单一平面，而必须拆分为：

1. **Bootstrap Control Plane**：由 P00 先建立，用于阻断 P01、注册阶段、登记资产、裁决下一步、维持安全边界。
2. **Full Control Plane**：在 Governance Plane、Domain Plane、Data Plane 生成后补全，用于追踪字段消费、任务队列、runner 状态、验收结果、handoff 消费状态和运行级状态回写。

## 2. 修正后的专业机构化链路

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
```

## 3. 当前阶段裁决

由于 P00 bootstrap 已通过，Bootstrap Control Plane 已存在；但 Full Control Plane、Trace/Acceptance/Handoff 的专业化索引与消费状态仍需补齐。因此当前下一合法阶段应从单点 `DATA_PLANE_ACCEPTANCE_REVIEW` 上移为：

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

该阶段包含：Governance、Domain、Data 的专业化验收，以及 Full Control、Trace、Acceptance、Handoff 的补全与验收。

## 4. P01 阻断规则

在 `SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE` 未通过前，P01 必须保持阻断。

```json
{
  "p01_runtime_connection_allowed": false,
  "p01_status": "BLOCKED_BY_SYSTEM_PLANES_ACCEPTANCE",
  "paper_only": true,
  "real_trade_enabled": false,
  "auto_order_allowed": false
}
```

## 5. Full Control Plane 必补资产

```text
00_control/runner_status_index.json
00_control/phase_output_index.json
00_control/handoff_consumption_status.json
00_control/data_plane_acceptance_status.json
00_trace/runner_execution_trace.yaml
08_acceptance/phase_acceptance_gate_index.yaml
08_acceptance/semantic_acceptance_rules.yaml
08_acceptance/consumption_acceptance_rules.yaml
08_acceptance/runtime_acceptance_rules.yaml
09_handoff/handoff_packet.schema.json
09_handoff/k00_to_p00/
09_handoff/p00_to_governance/
09_handoff/p00_to_domain/
09_handoff/p00_to_data/
09_handoff/data_to_p01/
```

## 6. 禁止事项

- 禁止启动 P01。
- 禁止将 Data Plane 文件存在等同于 Data Plane acceptance passed。
- 禁止将 P00 bootstrap passed 等同于 Full Control Plane 完成。
- 禁止绕过 handoff consumption matrix。
- 禁止真实交易、签名、广播、swap、自动下单。

## 7. 验收条件

1. 本补丁文件存在并登记为 methodology supplement。
2. `system_methodology_blueprint.md` 包含本补丁引用锚点。
3. `current_system_state.json` 的 `next_legal_stage` 指向 `SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE`。
4. `next_stage_decision.json` 记录从 `DATA_PLANE_ACCEPTANCE_REVIEW` 调整到该阶段的原因。
5. P01 仍保持不允许运行。
6. paper-only / no-real-trade / no-auto-order 安全边界保持为 true/false/false。
