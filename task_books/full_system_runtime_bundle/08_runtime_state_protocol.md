# 08 Runtime State Protocol

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## runtime_task_state.json
维护 current_allowed_task、waves、next_allowed_task、final_status_candidate、blocking_issues、degraded_issues。

## wave_state.json
维护每个 Wave 的 LOCKED/PENDING/RUNNING/READY/READY_WITH_GAPS/REJECTED。

## issue files
- current_blocking_issues.json：阻断项，非空则禁止推进。
- current_degraded_issues.json：降级项，非空则允许 READY_WITH_GAPS。

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

## Gap-aware progression runtime rule

- anchor: `GAP_AWARE_PROGRESSION_PROTOCOL`
- progression_gate: `BLOCKING_ZERO_REQUIRED_FOR_PROGRESSION`
- `READY_WITH_GAPS_DOES_NOT_EQUAL_READY`: runtime 可推进，但必须保留 degraded issues、gap register refs、audit refs。
- P08/P09 特例: `P08_READY_WITH_GAPS` 可进入 P09 review-only upgrade；`P09_READY_WITH_GAPS` 可进入 Full E2E replay/paper-only，不可进入 live execution。

## System integration and cognition update rule

- bundle 只有被控制平面、runtime state、audit、gap register 同时消费时，才算系统接入完成。
- verified stable rules 可以进入 durable cognition layer；conditional rules、missing facts、gap 只能留在 bundle 文档和 gap register。
- 文档完成不等于系统完成；若缺少 route 接入或 durable update 目标，状态仍应保留为 `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS`。
