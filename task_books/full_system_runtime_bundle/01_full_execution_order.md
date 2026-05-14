# 01 Full Execution Order

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 执行顺序
1. Task 0：全系统任务包自举。
2. Task 1 / Wave 1：P01-P03 基础事实与结构运行。
3. Task 2 / Wave 2：P04-P05 场景与位置运行。
4. Task 3 / Wave 3：P06-P07 策略与执行风控运行。
5. Task 4 / Wave 4：P08-P09 复盘与升级运行。
6. Task 5：Full System E2E 全链路验证。
7. Task 6：Patch + Regression 修复回归循环。

## 解锁规则
- Task0 READY/READY_WITH_GAPS → Wave1 PENDING。
- 任一 Wave REJECTED → 后续 LOCKED，Patch Regression PENDING。
- Wave4 READY/READY_WITH_GAPS → Full E2E PENDING。

## 禁止跳步
不得绕过上游 handoff，不得在 shared_handoff 缺失时推进下游。

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
