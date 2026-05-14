# 16 Gap-Aware Progression Protocol｜缺口感知推进协议

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-10T03:57:52.530995+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` maintained until live/business evidence closes inherited gaps
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: 本协议只定义 gap-aware progression 底层认知、P08/P09 READY_WITH_GAPS 推进规则与审计口径；不执行真实交易、签名、广播、swap，不把 paper-only 证据伪装成 live evidence。

## 1. 底层认知｜gap-aware progression

`READY_WITH_GAPS` 不是失败，也不是完全 READY；它是“可继续但必须携带缺口上下文”的受控中间态。

HER/SIKK 在长任务中必须区分三类状态：
- `READY`: required evidence、handoff、validation、audit 全部闭合，可无降级推进。
- `READY_WITH_GAPS`: blocking_issues 为空，但存在 inherited/degraded/missing/mock/paper-only/low-confidence evidence；允许推进下一 Wave，但必须显式携带 gap register、degraded issues、evidence confidence 与禁止推断项。
- `REJECTED`: blocking_issues 非空，或 required evidence 被伪造/覆盖/越权解释；必须停止并进入 Patch + Regression。

## 2. 推进门槛

允许从 `READY_WITH_GAPS` 推进的必要条件：
1. `blocking_issues == []`。
2. 所有 missing/gaps 使用 `missing` 或结构化 missing entry 记录，不得用 0、空字符串、AI 推测值替代。
3. 当前阶段输出必须包含 `degraded_issues`、`gap_register_ref`、`audit_refs`。
4. handoff 与 shared_handoff 关键字段一致；若业务 handoff 未执行，必须明确 `HANDOFF_DEGRADED`。
5. 下游阶段不得把上游 gap 推断为否定事实，例如不得从 `transfer_missing` 推断“无分发/无回流”。
6. hard negative、scope violation、安全边界、旧数据移动/删除、JSON parse failure 任一触发即 REJECTED。

## 3. P08 READY_WITH_GAPS 推进规则

P08 复盘学习层可以在上游为 `READY_WITH_GAPS` 时继续执行 review learning，但必须遵守：
- 输入侧继承 P01-P07 的 `degraded_issues`、`missing_fields`、`hard_negative_flags`、`paper_only` 标记。
- 输出侧允许生成 `review_learning_summary`、`rule_update_candidates`、`threshold_review_candidates`、`scenario_case_library`。
- 若 evidence chain 存在 missing，P08 只能写 `review_fact_missing` / `prior_evidence_chain_all_missing` / `low_confidence_review`，不得输出确定性胜率、确定性策略有效性、确定性因果结论。
- P08 的 `P08_READY_WITH_GAPS` 可解锁 P09，但 handoff 必须标记 `HANDOFF_DEGRADED`，并附带不能升级为实时规则的限制。

## 4. P09 READY_WITH_GAPS 推进规则

P09 系统升级层可以接收 P08 的 gap-aware handoff 并生成 review-only upgrade package，但必须遵守：
- `P09_READY_WITH_GAPS` 只能表示“升级建议包/影子验证计划/回滚计划已形成”，不表示已应用到实时系统。
- 任何 `rule_update_package` 必须包含 `review_only=true`、`shadow_mode_required=true`、`rollback_plan`、`regression_validation_plan`、`known_success_case_preservation`。
- 若回归未通过、known success cases 不保留、或 evidence confidence 低，则只能输出 `UPGRADE_PROPOSED_WITH_GAPS` 或 `UPGRADE_BLOCKED_WITH_GAPS`，不得输出 `UPGRADE_APPLIED`。
- P09 READY_WITH_GAPS 可解锁 Full System E2E 的 replay/paper-only 验证；禁止解锁 live trading、自动部署、真实签名、广播或 swap。

## 5. E2E 与 Patch + Regression 关系

- Full System E2E 可在 Wave1-4 均 `READY_WITH_GAPS` 且 blocking 为 0 时运行，但最终只能给出 `FULL_SYSTEM_E2E_READY_WITH_GAPS` 或更低置信状态。
- Patch + Regression 的任务不是隐藏 gap，而是把 gap 分类为：可关闭、需真实数据、需人工复核、需新 fixture、需代码修复。
- 未关闭的 gap 必须继续写入 runtime_task_state、missing_gap_register、validation artifact。

## 6. 验收锚点

验证时必须命中以下锚点：
- `GAP_AWARE_PROGRESSION_PROTOCOL`
- `P08_READY_WITH_GAPS_PROGRESSION_RULE`
- `P09_READY_WITH_GAPS_REVIEW_ONLY_UPGRADE_RULE`
- `READY_WITH_GAPS_DOES_NOT_EQUAL_READY`
- `BLOCKING_ZERO_REQUIRED_FOR_PROGRESSION`

## 7. 状态码映射

- `P08_READY_WITH_GAPS` → allowed_next: `P09_REVIEW_ONLY_UPGRADE_RUNTIME`，handoff: `HANDOFF_DEGRADED`。
- `P09_READY_WITH_GAPS` → allowed_next: `FULL_SYSTEM_E2E_RUNTIME`，upgrade_effect: `REVIEW_ONLY_NOT_APPLIED`。
- `WAVE4_READY_WITH_GAPS` → allowed_next: `FULL_SYSTEM_E2E_RUNTIME`，live_action: `FORBIDDEN`。
- `FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS` → system usable for replay/paper-only audit, not live execution.

## 8. Stop condition additions｜阻断条件补充

以下情况从 READY_WITH_GAPS 直接转为 REJECTED：
- gap 被下游删除、覆盖或改写为 ready evidence。
- paper/mock/replay evidence 被标记为 live evidence。
- P09 upgrade package 缺少 rollback/shadow/regression/known-success preservation。
- P08 从缺失 evidence 推导确定性交易/策略结论。
- 任何真实交易、签名、广播、swap 自动化被解锁。
