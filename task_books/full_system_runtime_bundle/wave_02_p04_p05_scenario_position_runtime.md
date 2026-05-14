# Wave 02 P04-P05 Scenario Position Runtime

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## Wave 目标
P04 phase_04_scenario_recognition → P05 phase_05_structure_position

## 输入
上游阶段 handoff、required fields、missing/gaps、hard-negative inheritance、audit refs。

## 输出
phase_05_handoff_packet

## 执行步骤
1. 读取本 Wave 涉及的 pXX_stage_data/code_landing/acceptance_check。
2. 自举缺失 contracts/schemas/src/tests/fixtures。
3. 逐阶段运行 pytest、replay、handoff、shared_handoff。
4. 审计越权输出、旧数据保护、missing、hard negative。
5. 写 Wave audit 与 runtime/checkpoint 状态。

## Stop condition
任一阶段 REJECTED、pytest/replay 失败、handoff 缺失、shared_handoff 不一致、required input 未 BLOCK、hard negative 被覆盖、旧数据被移动/删除。

## 状态码
WAVE_02_RUNTIME_READY | WAVE_02_RUNTIME_READY_WITH_GAPS | WAVE_02_RUNTIME_REJECTED

## 下一步
通过后解锁 Wave 3；失败进入 Patch + Regression。

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

## Wave2 反证 / counter-evidence 总控补强
- P04 必须产出场景候选的正证与反证；P05 必须读取并继承 P04 的 counter-evidence。
- P05 的 POC/AVWAP/Failure/Fatigue/Overextension 判断必须新增自身反证，不能覆盖 P04 hard negative。
- 任一阶段缺少 counter_evidence 时，Wave2 状态不得为 READY；可在明确 degraded_issues 后进入 READY_WITH_GAPS，若正向结论依赖该缺失反证则 REJECTED。
