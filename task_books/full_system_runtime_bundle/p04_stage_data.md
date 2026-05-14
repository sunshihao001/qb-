# P04 Stage Data｜phase_04_scenario_recognition｜多模型场景识别层

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 阶段目标
多模型场景识别层接收上游 handoff，完成本阶段事实/判断边界内的结构化输出，并将 missing、gaps、hard negative 显式传递给下游。

## 阶段定位
- phase_id: `phase_04_scenario_recognition`
- phase_code: `P04`
- 系统推导: 本文件由 Task0 从总控文件与 v4.0 工作流推导生成。

## 上游 handoff
- P01: raw/source input。
- 非 P01: 上一阶段 `phase_xx_handoff_packet.json`。
- required input 缺失且不能降级时，必须 BLOCK。

## 下游 handoff
输出给下一阶段；本阶段不得替下游做最终结论。

## 输入合约
- required_fields: token_id、source_refs、fetched_at_or_observed_at、upstream_status、evidence_refs。
- optional_fields: external_context、legacy_refs、operator_note。
- missing 规则: 缺失写 `missing`，不得写 0、空字符串或推测值。

## 输出合约
- phase_id、status、positive_evidence、counter_evidence、hard_negatives、missing、gaps、handoff_packet_path、audit_path。
- 允许输出: 吸筹/拉升/二段扩张/高位派发/下跌再派发/诱多反抽/退出流动性陷阱/假横盘/再吸筹/末端拉盘派发/刷量假突破/接盘鲸鱼陷阱等场景候选与反证。

## 必需字段
 token_id; phase_id; upstream_handoff; required_inputs; output_artifacts; status_code; missing; gaps; audit_result.

## 可选字段
legacy_context; degraded_reason; replay_refs; sample_refs; operator_notes.

## 推理规则
- 先证据，后判断。
- 正向证据必须配套反证检查。
- 上游 hard negative 继承优先于本阶段打分。
- 不确定写 gaps，不补成确定结论。

## 反证规则
每个正向结论至少检查：数据时效、样本偏差、上游降级、相反链上行为、字段缺失。

## 硬否决规则
DATA_INVALID、UPSTREAM_BLOCK、MISSING_REQUIRED_INPUT、HANDOFF_MISMATCH、HARD_NEGATIVE_INHERITED、PHASE_SCOPE_VIOLATION。

## 状态码
- `P04_READY`
- `P04_READY_WITH_GAPS`
- `P04_REJECTED`
- `P04_BLOCKED_BY_UPSTREAM`

## handoff 规则
本地 handoff 与 shared_handoff 必须字段一致；不一致时 REJECTED。

## 降级规则
optional 缺失、legacy fallback 缺失、外部上下文不可用可降级，但必须写 degraded_issues。

## 阻断规则
required input 缺失、hard negative 触发、越权输出、旧数据移动/删除、handoff 缺失均阻断。

## 禁止事项
买点、PAPER_READY、执行交易。

## 验收标准
stage_data 通过、code_landing 通过、acceptance_check 通过、pytest/replay/handoff 在 Wave 执行时通过。

## gaps
- Task0 不执行业务代码，因此 runtime evidence 为 `missing`，进入 READY_WITH_GAPS。

## implementation plan
由 `p04_code_landing.md` 执行代码骨架/runner/test/replay 任务。

## test plan
由 `p04_acceptance_check.md` 执行目录、contract、schema、pytest、replay、handoff、安全边界检查。

## audit report
Wave 执行后写入 reports/system_audit/waves 或阶段 audit；Task0 只写任务包审计。

## 最终状态
Task0 文件状态：`TASKBOOK_READY_WITH_GAPS`。
