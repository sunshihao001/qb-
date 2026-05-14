# 00 Full Bundle Manifest

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 目标
建立 P01-P09 全阶段自动化系统建设任务包，使 HER 能按总控协议自举、自检、自补、分 Wave 执行、失败停止、审计回填、回归修复。

## 已读取/必须存在的总控文件
- `/root/sikk-gmgn/skills/sikk_stable_trader_os/SKILL.md`
- `/root/sikk-gmgn/docs/01_stage_definitions/full_stage_map.md`
- `/root/sikk-gmgn/docs/02_phase_layer_step_maps/full_phase_layer_step_map.md`
- `/root/sikk-gmgn/docs/03_handoff_flow/phase_handoff_flow.md`
- `/root/sikk-gmgn/docs/04_status_codes/global_status_code_table.md`
- `/root/sikk-gmgn/docs/05_hard_negative_rules/global_hard_negative_rules.md`
- `/root/sikk-gmgn/docs/06_directory_constitution/directory_constitution.md`
- `/root/sikk-gmgn/docs/07_contract_index/contract_index.md`
- `/root/sikk-gmgn/docs/08_schema_index/schema_index.md`
- `/root/sikk-gmgn/docs/09_her_execution_protocol/her_total_control_execution_protocol.md`
- `/root/sikk-gmgn/docs/10_professional_acceptance/professional_baseline_acceptance.md`

## Bundle 文件族
- 全局协议：00-15 共 16 个控制文件。
- 阶段任务：P01-P09 每阶段 `stage_data`、`code_landing`、`acceptance_check`。
- Wave 任务：Wave 1-4、Full E2E、Patch Regression。
- Runtime 状态：runtime_task_state、checkpoint_state、wave_state、blocking/degraded issues、last_successful_checkpoint。

## 最终状态
- `FULL_SYSTEM_BUNDLE_READY`: 无阻断且无继承 gap。
- `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS`: Task0 完成，但未执行业务代码/pytest/replay，或继承显式 degraded issues。
- `FULL_SYSTEM_BUNDLE_REJECTED`: required 总控文件缺失或任务包审计失败。

## 不做事项
- 不创建真实交易、签名、广播、swap。
- 不把 `PAPER_READY` 当作 `PAPER_EXECUTED`。
- 不移动或删除旧数据。

## 质量加深补充｜输入/输出/handoff/状态码/missing/阻断/降级/验收/审计
- 输入: 读取 11 个 total-control 文件、当前 bundle 文件、runtime_task_state.json、checkpoint_state.json、missing_gap_register.md。
- 输出: 对应协议文件、状态 JSON、审计报告、validation.json、gap register 更新。
- handoff: Task0 的 handoff 是 `next_allowed_task` 与 runtime/checkpoint 状态；Wave 执行时才产生业务 handoff。
- 状态码: READY、READY_WITH_GAPS、REJECTED 必须映射到 `FULL_SYSTEM_BUNDLE_*` 或 Wave 专属状态。
- missing: 缺失必须记录为 `missing` 或 missing entry；不得写 0、空字符串或 AI 推测值。
- 阻断: required 控制文件缺失、bundle 文件缺失、JSON 不可 parse、越权交易声明、旧数据移动/删除均阻断。
- 降级: Task0 未执行业务代码/pytest/replay/handoff 是显式 degraded issue，不阻断 Wave1，但必须先读 gap register。
- 验收: 文件存在、非空、关键词完整、JSON parse、禁用目录未创建、禁用交易话术仅出现在禁止语境。
- 审计: 所有判断写入 `full_system_runtime_bundle_audit.md` 与 `full_system_runtime_bundle_validation.json`。

## 10. System integration & cognition update

Task0 is not complete if the bundle only exists as readable text. It is complete only when the bundle can be consumed by the control plane, routed by runtime state, audited independently, and promoted into durable system cognition when rules are verified.

- document-ready: files exist, are cross-linked, and can be consumed by the runtime.
- system-ready-with-gaps: runtime and audit are wired, but some Waves remain intentionally deferred.
- system-rejected: required control files, audit links, or gap-aware progression hooks are missing.

Verified stable rules may be promoted into durable governance or skill layers; unresolved gaps stay in the gap register and must not be rewritten as facts.
