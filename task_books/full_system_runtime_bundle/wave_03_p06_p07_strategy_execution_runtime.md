# Wave 03 P06-P07 Strategy Execution Runtime

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## Wave 目标
P06 phase_06_strategy_gate → P07 phase_07_execution_risk

## 输入
上游阶段 handoff、required fields、missing/gaps、hard-negative inheritance、audit refs。

## 输出
paper-only risk decision and Phase08 handoff

## 执行步骤
1. 读取本 Wave 涉及的 pXX_stage_data/code_landing/acceptance_check。
2. 自举缺失 contracts/schemas/src/tests/fixtures。
3. 逐阶段运行 pytest、replay、handoff、shared_handoff。
4. 审计越权输出、旧数据保护、missing、hard negative。
5. 写 Wave audit 与 runtime/checkpoint 状态。

## Stop condition
任一阶段 REJECTED、pytest/replay 失败、handoff 缺失、shared_handoff 不一致、required input 未 BLOCK、hard negative 被覆盖、旧数据被移动/删除。

## 状态码
WAVE_03_RUNTIME_READY | WAVE_03_RUNTIME_READY_WITH_GAPS | WAVE_03_RUNTIME_REJECTED

## 下一步
通过后解锁 Wave 4；失败进入 Patch + Regression。

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

## Wave3 hard negative / counter-evidence / no-trade 总控补强
- P06 策略候选必须继承 P05 反证链，并写自身 counter-evidence；P07 必须继承 P06 反证链并新增执行风险反证。
- P06/P07 输出只能是 paper-only candidate / gate / risk plan；禁止真实交易、签名、广播、secret 读取。
- 缺少 counter_evidence 时，Wave3 不得为 READY；若同时给出正向策略/执行允许则 REJECTED。
- hard negative 不允许被下游覆盖，只能继承、升级阻断或显式登记为 unresolved gap。
- Terminology guard: Wave3 controller blocks signing and `broadcast` at protocol level.
