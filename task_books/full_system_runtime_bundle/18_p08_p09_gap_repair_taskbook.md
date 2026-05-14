# 18 P08/P09 Gap Repair Taskbook｜Evidence Chain / Known Success / Collector Replay Closure

- task_id: `task_7_p08_p09_gap_repair_closure`
- version: `v1.0`
- status: `RUNTIME_CONSUMABLE`
- scope: `SIKK Stable Trader OS / Wave4 P08-P09 / full_system_runtime_bundle gaps`
- owner_layer: `HER total control plane`
- source_type: `runtime_gap_repair_taskbook`
- updated_at: `2026-05-10T14:32:00Z`
- runtime_consumption: `Full-system controllers route READY_WITH_GAPS through Patch + Regression before any READY claim; this taskbook defines the repair closure contract for Wave4 degraded gaps.`
- control_plane_refs: `task_books/full_system_runtime_bundle/16_gap_aware_progression_protocol.md; task_books/full_system_runtime_bundle/wave_04_p08_p09_review_upgrade_runtime.md; runtime_logs/full_system_runtime/current_degraded_issues.json; reports/system_audit/missing_gap_register.md`
- gap_policy: `unresolved gaps remain degraded and cannot be converted into READY claims; missing evidence must be literal missing or structured missing entry`
- audit_policy: `repair outputs must write acceptance evidence, gap closure report, no-checkpoint replay result, runtime_state reconcile, and audit refs before status promotion`
- durable_cognition_policy: `only verified stable control-plane rules may be promoted; temporary task progress and unresolved gaps stay in gap registers`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade / no secrets`

## 1. HER 定位

本任务书不是业务实现单，而是 `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` 后的系统内修复路由单。
它把 Wave4 P08/P09 剩余 degraded gaps 转换为可执行、可验收、可审计、可回归的 repair package。

控制目标：
- 自举：允许生成缺失 fixture/schema/report 骨架，但不得伪造 evidence。
- 自检：每个 repair item 必须有 validator/test/replay/audit。
- 自补：只关闭被证据证明关闭的 gap；未证明的继续保留。
- 分 Wave：本任务只处理 Wave4 P08/P09 与 full-system replay gate。
- 失败停止：触发 hard negative、scope violation、unsafe runtime apply 时立即 REJECTED。
- 审计回填：所有 closure / remaining gap 写回 gap ledger 与 audit refs。
- 回归修复：任何规则升级必须通过 known-success preservation 与 rollback/shadow validation。

## 2. 输入契约

必须读取：
- `runtime_logs/full_system_runtime/current_degraded_issues.json`
- `runtime_logs/full_system_runtime/runtime_task_state.json`
- `reports/system_audit/missing_gap_register.md`
- `reports/system_audit/full_system_automation_result.json`
- `task_books/full_system_runtime_bundle/p08_acceptance_check.md`
- `task_books/full_system_runtime_bundle/p09_acceptance_check.md`
- `task_books/full_system_runtime_bundle/16_gap_aware_progression_protocol.md`

缺失输入处理：
- required control file missing → `TASK_7_REJECTED`
- degraded issue file missing → `TASK_7_REJECTED`
- evidence file missing → 保留对应 gap，不得补空值或假值
- JSON parse failure → `TASK_7_REJECTED`

## 3. 输出契约

本任务完成时必须生成或更新：
- `reports/system_audit/p08_p09_gap_repair_closure_report.json`
- `reports/system_audit/p08_p09_gap_repair_closure_audit.md`
- `runtime_logs/full_system_runtime/p08_p09_gap_repair_state.json`
- `reports/system_audit/full_system_workflow_v4_gap_register.json` 或等价 gap ledger 回填
- full-system no-checkpoint replay result 引用
- targeted pytest result 引用

禁止输出：
- `UPGRADE_APPLIED`
- `LIVE_READY`
- `real_trade_enabled=true`
- 签名、广播、swap、真实交易动作
- 从 mock/paper/replay evidence 推断 live evidence

## 4. Repair Items

### R1｜PHASE08_EVIDENCE_CHAIN_REPAIR

覆盖 gaps：
- `PHASE08_NEXT_STAGE_BLOCKED_GAP_AWARE_PROGRESSION`
- `PHASE08_DEGRADE_REASON`
- `PHASE08_MISSING_FIELDS`

执行步骤：
1. 收集 P01-P07 handoff、shared_handoff、audit refs、missing_fields、hard_negative_flags。
2. 生成 `phase08_evidence_chain_manifest.json`，字段至少包含 `phase_id`、`handoff_path`、`audit_refs`、`missing_fields`、`evidence_confidence`、`counter_evidence`。
3. P08 review learning 只能基于已存在 evidence；缺失处写 structured missing entry。
4. 重新运行 P08 controller targeted tests 与 Wave4 runner tests。
5. 若 P01-P07 evidence chain 仍缺失，保持 READY_WITH_GAPS，不得提升 READY。

验收：
- `phase08_evidence_chain_manifest.json` 可 parse。
- 所有 P01-P07 阶段均有 evidence entry 或 structured missing entry。
- P08 输出包含 `gap_register_ref`、`counter_evidence`、`paper_only`、`low_confidence`。
- 不出现确定性胜率、确定性策略有效性、确定性因果结论。

### R2｜PHASE09_KNOWN_SUCCESS_REGRESSION_FIXTURE

覆盖 gap：
- `PHASE09_SYSTEM_UPGRADE_BLOCKED_GAP_AWARE_PROGRESSION`

执行步骤：
1. 建立 known-success fixture registry，来源必须是已验证历史成功案例或显式 paper fixture。
2. 每个 fixture 记录 `case_id`、`source_ref`、`expected_outcome`、`preservation_assertions`、`evidence_confidence`。
3. P09 upgrade candidate 必须运行 known-success preservation check。
4. 若 known-success fixture 为空或低置信，只允许 `UPGRADE_BLOCKED_WITH_GAPS`。

验收：
- known-success registry 非空且每项有 source_ref 与 expected_outcome；否则保留 gap。
- preservation check 失败时不得进入 READY。
- P09 handoff 暴露 `regression_fixture_required`、`preservation_gate`、`block_reason`。

### R3｜PHASE09_SHADOW_ROLLBACK_VALIDATION_CLOSURE

覆盖 gap：
- `PHASE09_SYSTEM_UPGRADE_BLOCKED_GAP_AWARE_PROGRESSION`

执行步骤：
1. 为每个 upgrade_candidate 建立 shadow-mode validation plan。
2. 为每个 upgrade_candidate 建立 rollback plan。
3. 建立 regression validation plan，覆盖 happy path、known-success preservation、gap-aware negative、scope violation。
4. 未通过前保持 review-only。

验收：
- 每个 upgrade_candidate 均有 `review_only=true`、`shadow_mode_required=true`、`approval_required=true`。
- 每个 upgrade_candidate 均有 `rollback_plan`、`regression_validation_plan`、`known_success_case_preservation`、`counter_evidence`。
- 缺任一字段 → `TASK_7_READY_WITH_GAPS` 或 `TASK_7_REJECTED`，不得 READY。

### R4｜COLLECTOR_AND_REPLAY_FIXTURE_CLOSURE

覆盖 gap：
- `PHASE_09_LOW_CONFIDENCE_REPLAY`

执行步骤：
1. 建立 collector/replay fixture manifest；只记录数据需求、采集命令计划、脱敏样例、paper replay path。
2. 不读取 secrets，不执行真实交易，不广播交易。
3. 使用 canonical replay fixture 验证 full-system no-checkpoint replay。
4. 若无真实 collector/live data，保留 low-confidence gap。

验收：
- replay fixture manifest 可 parse。
- no-checkpoint replay 记录 `checkpoint_reused=false`、`executed_phase_count=9`、`skipped_phase_count=0`。
- mock/canonical/paper evidence 不得标记为 live evidence。

## 5. 状态机

- `TASK_7_READY`: R1-R4 全部验收通过，gap register 无剩余 degraded/blocking，full-system no-checkpoint replay 通过。
- `TASK_7_READY_WITH_GAPS`: 无 blocking，但仍缺真实 evidence、known-success、collector/live replay 或低置信 evidence。
- `TASK_7_REJECTED`: required input 缺失、JSON 不可 parse、越权交易/签名/广播、伪造 evidence、known-success preservation 失败却申请 READY。

## 6. Handoff

READY：允许重新评估 `FULL_SYSTEM_BUNDLE_READY`。
READY_WITH_GAPS：继续保持 `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS`，下一任务仍为 Patch + Regression / evidence collection。
REJECTED：停止 Wave4/Full-system promotion，必须先修复 blocker。

## 7. 回归命令

最低 targeted regression：
- `python3 -m pytest tests/stable_trader_os/phase_08_review_learning/test_phase_08_controller_runtime_closure.py tests/stable_trader_os/phase_09_system_upgrade/test_phase_09_controller_runtime_closure.py tests/test_wave4_p08_p09_runner.py -q`
- `python3 -m pytest tests/test_full_system_workflow_v4.py tests/test_full_system_runtime_controls.py tests/test_planbook_repository.py -q`

Full-system acceptance replay：
- `python3 -m modules.runtime.full_system_runner --root <tmp_root> --mode replay --token [REDACTED]`

## 8. Stop Conditions

立即 REJECTED：
- evidence missing 被改写为 0、空字符串、成功事实或 ready evidence。
- paper/mock/replay evidence 被标记为 live evidence。
- P09 upgrade package 缺 rollback/shadow/regression/known-success preservation。
- P08 输出确定性交易结论。
- 出现真实交易、签名、广播、swap、secret access。

## 9. 最终判定

本任务书接入系统后，允许系统识别下一阶段修复工作为：
`task_7_p08_p09_gap_repair_closure`。

当前若 R1-R4 尚未执行完，系统状态只能是：
`TASK_7_READY_WITH_GAPS` / `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS`。
