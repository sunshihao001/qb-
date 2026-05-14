# 15 Full System Acceptance Protocol

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## Full System E2E 准入
Wave1-4 全部 READY/READY_WITH_GAPS 且 blocking_issues 为空。

## 验收项
P01-P09 全链路 handoff、status inheritance、hard-negative inheritance、missing propagation、shared_handoff 一致性、paper-only 安全、P09 review-only upgrade package。

## 最终状态
Full E2E 输出 FULL_SYSTEM_E2E_READY / READY_WITH_GAPS / REJECTED；不等同真实交易可用。

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

## Gap-aware progression E2E 准入补充

- anchor: `GAP_AWARE_PROGRESSION_PROTOCOL`
- Wave1-4 若为 READY_WITH_GAPS，可进入 Full System E2E 的 replay/paper-only 验证；最终状态必须保留 READY_WITH_GAPS，不得升级为 live-ready。
- `BLOCKING_ZERO_REQUIRED_FOR_PROGRESSION`: 只要 blocking_issues 非空，E2E 禁止推进并进入 Patch + Regression。

## System integration acceptance

- 只有当 bundle 文件可被 runtime 消费、audit 可被独立验证、gap register 可被同步、并且 verified rule 能进入 durable cognition surface 时，才可判定为系统接入完成。
- 若只是文档完整但没有路由/状态/审计接入，则仍属于 `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS`。
