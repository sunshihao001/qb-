# 04 Stop Condition Protocol

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 全局停止条件
- required 总控文件缺失。
- 阶段数据/代码落地/验收 REJECTED。
- pytest 或 replay 失败。
- handoff/shared_handoff 未生成或二者不一致。
- required input 缺失但未 BLOCK。
- missing 被 0/空字符串/AI 推测值伪装。
- 硬否决被下游覆盖。
- 旧数据被移动或删除。
- 阶段越权输出下游结论。
- `PAPER_READY` 被当成 `PAPER_EXECUTED`。
- P09 回归测试失败仍生成可应用升级包。

## 停止动作
写 audit、blocking_issues、runtime_task_state，锁定后续 Wave，设置 `next_allowed_task=FIX_CURRENT_BLOCKING_ISSUES`。

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

## Gap-aware progression stop additions

- anchor: `READY_WITH_GAPS_DOES_NOT_EQUAL_READY`
- 若 READY_WITH_GAPS 被当作 READY、paper/mock evidence 被当作 live evidence、P08 从缺失证据输出确定性策略结论、P09 在回归/rollback/shadow 缺失时应用升级，立即 REJECTED。
- `BLOCKING_ZERO_REQUIRED_FOR_PROGRESSION`: blocking_issues 非空时不得以 READY_WITH_GAPS 绕过停止条件。
