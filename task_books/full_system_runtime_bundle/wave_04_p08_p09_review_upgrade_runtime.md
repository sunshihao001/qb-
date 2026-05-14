# Wave 04 P08-P09 Review Upgrade Runtime

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## Wave 目标
P08 phase_08_review_learning → P09 phase_09_system_upgrade

## 输入
上游阶段 handoff、required fields、missing/gaps、hard-negative inheritance、audit refs。

## 输出
review learning outputs and review-only upgrade package with rollback/shadow-mode

## 执行步骤
1. 读取本 Wave 涉及的 pXX_stage_data/code_landing/acceptance_check。
2. 自举缺失 contracts/schemas/src/tests/fixtures。
3. 逐阶段运行 pytest、replay、handoff、shared_handoff。
4. 审计越权输出、旧数据保护、missing、hard negative。
5. 写 Wave audit 与 runtime/checkpoint 状态。

## Stop condition
任一阶段 REJECTED、pytest/replay 失败、handoff 缺失、shared_handoff 不一致、required input 未 BLOCK、hard negative 被覆盖、旧数据被移动/删除。

## 状态码
WAVE_04_RUNTIME_READY | WAVE_04_RUNTIME_READY_WITH_GAPS | WAVE_04_RUNTIME_REJECTED

## 下一步
通过后解锁 Full System E2E；失败进入 Patch + Regression。

## Gap-aware progression｜P08/P09 READY_WITH_GAPS 推进

- anchor: `P08_READY_WITH_GAPS_PROGRESSION_RULE`
- P08 可在上游 READY_WITH_GAPS 且 blocking 为 0 时执行复盘学习；必须保留 evidence_chain missing、low_confidence、paper_only、degraded_context，不得输出确定性交易/策略因果结论。
- anchor: `P09_READY_WITH_GAPS_REVIEW_ONLY_UPGRADE_RULE`
- P09 可在 P08 READY_WITH_GAPS 下生成 review-only upgrade package；必须包含 rollback_plan、shadow_mode_required、regression_validation_plan、known_success_case_preservation；不得自动应用到实时系统。
- `READY_WITH_GAPS_DOES_NOT_EQUAL_READY`: Wave4 READY_WITH_GAPS 只解锁 Full System E2E replay/paper-only 验证，不解锁 live trading。

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

## Wave4 hard negative / counter-evidence / review-only 总控补强
- P08 必须把 P01-P07 的反证链合并为复盘证据，不允许从单次样本直接生成稳定规则。
- P09 必须继承 P08 反证与 unresolved gaps，只生成 review-only upgrade package。
- 任何自动修改策略、交易参数、权限、provider、密钥、执行器的行为均触发 REJECTED。
- 缺少 counter_evidence 或 regression/rollback plan 的升级候选不得进入 READY，只能 READY_WITH_GAPS 或 REJECTED。
- Terminology guard: P09 approval_required is mandatory before any future implementation; no auto-approval.
