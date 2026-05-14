# P08 Code Landing｜phase_08_review_learning｜复盘学习层

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 代码落地目标
在 Wave 执行时为 `phase_08_review_learning` 建立可运行、可测试、可 replay、可 handoff 的代码骨架和最小 runtime。Task0 不落业务代码。

## 允许事项
- 创建 contracts/phase_08_review_learning/ 或 contracts/p08/ 等总控认可路径。
- 创建 schemas/phase_08_review_learning/、src/phase_08_review_learning/、tests/phase_08_review_learning/、tests/fixtures/phase_08_review_learning/。
- 写 runner、validator、handoff writer、audit writer。
- 仅输出本阶段允许范围：失败归因、成功归因、阻断样本复盘、规则候选、阈值候选、地址历史更新、场景样本库。

## 禁止事项
直接修改实时规则、单样本直接升级系统；禁止真实签名、广播、swap、自动实盘；禁止移动/删除旧数据。

## 上游 handoff
读取上游 handoff，校验 status、required fields、hard_negative inheritance、missing propagation。

## contracts 清单
- input_contract.json/md
- output_contract.json/md
- handoff_contract.json/md
- audit_contract.json/md

## schemas 清单
- input_schema.json
- output_schema.json
- handoff_packet_schema.json
- audit_schema.json

## src 模块清单
- validator.py
- runner.py
- handoff_writer.py
- audit_writer.py
- cli.py

## tests 清单
- test_phase_08_review_learning_validator.py
- test_phase_08_review_learning_runner.py
- test_phase_08_review_learning_handoff.py
- test_phase_08_review_learning_hard_negative.py
- test_phase_08_review_learning_scope_guard.py

## fixtures 清单
- ready_case.json
- ready_with_gaps_case.json
- rejected_missing_required_case.json
- rejected_hard_negative_case.json
- scope_violation_case.json

## runner 命令
`python3 -m src.phase_08_review_learning.cli --mode replay --input tests/fixtures/phase_08_review_learning/ready_case.json`

## pytest 命令
`python3 -m pytest tests/phase_08_review_learning -q`

## replay 命令
`python3 -m src.phase_08_review_learning.cli --mode replay --write-handoff --write-audit`

## 阶段输出
本地 output、handoff_packet、audit_report。

## shared_handoff 输出
`/root/sikk-gmgn/data/shared_handoff/phase_08_review_learning/<token>/phase_handoff_packet.json` 或合同索引指定路径。

## audit 输出
`/root/sikk-gmgn/reports/system_audit/phase_08_review_learning_audit.md` 或 Wave 审计文件。

## stop condition
代码目录缺失、contract/schema 缺失、pytest 失败、replay 失败、handoff 缺失、shared_handoff 不一致、越权输出均 REJECTED。

## READY / READY_WITH_GAPS / REJECTED
- READY: 代码、测试、replay、handoff 全通过。
- READY_WITH_GAPS: 可运行但 optional/legacy/context degraded。
- REJECTED: required 或安全边界失败。

## 下一步规则
通过后交给 `p08_acceptance_check.md`；失败进入 Patch + Regression。

## 输入 / 状态码 / 阻断 / 降级 / 验收 补强
- 输入: 上游 handoff packet、合同索引、schema 索引、required fields、missing/gaps、hard-negative inheritance、legacy read-only refs。
- 状态码: `P08_CODE_READY`、`P08_CODE_READY_WITH_GAPS`、`P08_CODE_REJECTED`、`P08_CODE_BLOCKED_BY_UPSTREAM`。
- 阻断: contracts/schemas/src/tests/fixtures 缺失且无法自举、pytest 失败、replay 失败、handoff/shared_handoff 缺失或不一致、required input 未 BLOCK、越权输出、旧数据被移动/删除。
- 降级: optional context 缺失、legacy fallback 缺失、外部数据临时不可用可进入 READY_WITH_GAPS，但必须写 degraded_issues 与 audit。
- 验收: 目录检查、contract 检查、schema parse、fixture 安全、pytest、replay、handoff 一致性、missing 规则、hard negative 继承、paper-only/安全边界全部通过后才允许进入下一阶段。

## Wave4 复盘反证 / counter-evidence 自检
- P08 只做 post-run review 与 evidence reconciliation，不允许输出新的交易执行建议。
- 必须读取 P07 handoff，并继承 P01-P07 的 missing、gaps、hard_negatives、counter_evidence、audit refs。
- counter-evidence 至少覆盖：回放样本偏差、幸存者偏差、上游降级、未验证的 paper decision、审计缺失、执行风控否决。
- P08 结论必须区分 observation、lesson_candidate、rejected_lesson、unresolved_gap；不得把单次 lucky case 写成稳定规则。
- Terminology guard: P08 is `review-only`; downstream rollback/approval implications must be passed to P09 as missing/gaps, not decided by P08.
