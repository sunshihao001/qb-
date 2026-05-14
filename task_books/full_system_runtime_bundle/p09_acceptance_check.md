# P09 Acceptance Check｜phase_09_system_upgrade｜系统自我升级层

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 阶段数据检查
确认 `p09_stage_data.md` 包含目标、定位、上游/下游 handoff、输入合约、输出合约、字段、推理、反证、hard negative、状态码、missing、降级、阻断、验收、gaps。

## 代码目录检查
Wave 执行时检查 contracts、schemas、src、tests、fixtures 五类目录。缺失则按 code_landing 自举，无法自举则 REJECTED。

## contract 检查
input/output/handoff/audit contract 必须存在，且 required fields 不得降级成 optional。

## schema 检查
JSON schema 必须可 parse，必须表达 missing 与 hard_negative 字段。

## tests 检查
ready、ready_with_gaps、missing required、hard negative、scope violation 至少五类 fixture/test。

## fixtures 检查
fixture 不得包含真实私钥、签名、广播、swap secret。

## pytest 检查
运行 `python3 -m pytest tests/phase_09_system_upgrade -q`，失败则 REJECTED。

## replay 检查
运行 replay 命令，必须生成本地 handoff、shared_handoff、audit。

## handoff 检查
本地 handoff 与 shared_handoff 关键字段一致；不一致 REJECTED。

## 越权输出检查
禁止输出下游最终结论；本阶段禁止项：回归失败仍升级、无 rollback_plan 升级、自动修改实时系统。

## 旧数据保护检查
确认未移动、删除、覆盖 legacy data；只允许 copy-only 或只读 fallback。

## missing 检查
missing 必须为字符串 `missing` 或结构化 missing entry；禁止 0/空字符串/AI 推测值。

## hard negative 继承检查
上游 hard negative 不得被本阶段覆盖；触发时优先 BLOCK/REJECTED。

## 是否允许进入下一阶段
- READY/READY_WITH_GAPS 且 blocking_issues 为空：允许。
- REJECTED：禁止，进入 Patch + Regression。

## 最终状态
`P09_ACCEPTANCE_READY | P09_ACCEPTANCE_READY_WITH_GAPS | P09_ACCEPTANCE_REJECTED`。

## Gap-aware progression acceptance

- anchor: `P09_READY_WITH_GAPS_REVIEW_ONLY_UPGRADE_RULE`
- `P09_ACCEPTANCE_READY_WITH_GAPS` 成立条件：blocking_issues 为空、upgrade package 为 review-only、包含 rollback_plan、shadow_mode_required、regression_validation_plan、known_success_case_preservation。
- 禁止：回归失败仍应用升级、缺少 rollback_plan 仍升级、把 review-only proposal 当作 applied runtime rule。

## Wave4 counter-evidence / upgrade-governance 验收
- 检查 P09 upgrade package 是否继承 P08 counter-evidence 与 unresolved gaps。
- 检查每个 upgrade_candidate 是否包含 regression plan、rollback plan、approval_required 与反证。
- 若 P09 自动改策略/配置/权限、绕过人工批准、或缺少回归仍标记可上线，状态必须为 `P09_ACCEPTANCE_REJECTED`。
- Terminology guard: literal `counter_evidence` must exist for every P09 upgrade_candidate.
