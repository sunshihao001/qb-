# P06 Code Landing｜phase_06_strategy_gate｜策略过滤层

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 代码落地目标
在 Wave 执行时为 `phase_06_strategy_gate` 建立可运行、可测试、可 replay、可 handoff 的代码骨架和最小 runtime。Task0 不落业务代码。

## 允许事项
- 创建 contracts/phase_06_strategy_gate/ 或 contracts/p06/ 等总控认可路径。
- 创建 schemas/phase_06_strategy_gate/、src/phase_06_strategy_gate/、tests/phase_06_strategy_gate/、tests/fixtures/phase_06_strategy_gate/。
- 写 runner、validator、handoff writer、audit writer。
- 仅输出本阶段允许范围：A+P1、证据链、风险收益比、策略适配、PAPER_READY / STRATEGY_BLOCK。

## 禁止事项
直接执行、直接写 paper_positions_open、绕过 P07；禁止真实签名、广播、swap、自动实盘；禁止移动/删除旧数据。

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
- test_phase_06_strategy_gate_validator.py
- test_phase_06_strategy_gate_runner.py
- test_phase_06_strategy_gate_handoff.py
- test_phase_06_strategy_gate_hard_negative.py
- test_phase_06_strategy_gate_scope_guard.py

## fixtures 清单
- ready_case.json
- ready_with_gaps_case.json
- rejected_missing_required_case.json
- rejected_hard_negative_case.json
- scope_violation_case.json

## runner 命令
`python3 -m src.phase_06_strategy_gate.cli --mode replay --input tests/fixtures/phase_06_strategy_gate/ready_case.json`

## pytest 命令
`python3 -m pytest tests/phase_06_strategy_gate -q`

## replay 命令
`python3 -m src.phase_06_strategy_gate.cli --mode replay --write-handoff --write-audit`

## 阶段输出
本地 output、handoff_packet、audit_report。

## shared_handoff 输出
`/root/sikk-gmgn/data/shared_handoff/phase_06_strategy_gate/<token>/phase_handoff_packet.json` 或合同索引指定路径。

## audit 输出
`/root/sikk-gmgn/reports/system_audit/phase_06_strategy_gate_audit.md` 或 Wave 审计文件。

## stop condition
代码目录缺失、contract/schema 缺失、pytest 失败、replay 失败、handoff 缺失、shared_handoff 不一致、越权输出均 REJECTED。

## READY / READY_WITH_GAPS / REJECTED
- READY: 代码、测试、replay、handoff 全通过。
- READY_WITH_GAPS: 可运行但 optional/legacy/context degraded。
- REJECTED: required 或安全边界失败。

## 下一步规则
通过后交给 `p06_acceptance_check.md`；失败进入 Patch + Regression。

## 输入 / 状态码 / 阻断 / 降级 / 验收 补强
- 输入: 上游 handoff packet、合同索引、schema 索引、required fields、missing/gaps、hard-negative inheritance、legacy read-only refs。
- 状态码: `P06_CODE_READY`、`P06_CODE_READY_WITH_GAPS`、`P06_CODE_REJECTED`、`P06_CODE_BLOCKED_BY_UPSTREAM`。
- 阻断: contracts/schemas/src/tests/fixtures 缺失且无法自举、pytest 失败、replay 失败、handoff/shared_handoff 缺失或不一致、required input 未 BLOCK、越权输出、旧数据被移动/删除。
- 降级: optional context 缺失、legacy fallback 缺失、外部数据临时不可用可进入 READY_WITH_GAPS，但必须写 degraded_issues 与 audit。
- 验收: 目录检查、contract 检查、schema parse、fixture 安全、pytest、replay、handoff 一致性、missing 规则、hard negative 继承、paper-only/安全边界全部通过后才允许进入下一阶段。

## Wave3 策略门控反证 / counter-evidence 自检
- P06 只能输出 `paper_decision_candidate`、strategy gate、risk flags，不得输出真实买入/卖出执行。
- 任一策略候选必须同时包含 `positive_evidence`、`counter_evidence`、`hard_negatives_inherited`、`missing/gaps`。
- counter-evidence 至少覆盖：P05 位置降级、AVWAP/POC 失效、流动性不足、追高/过度延伸、反向钱包行为、字段缺失。
- 若 P05 hard negative 存在，P06 必须 BLOCK 或输出 rejected_candidate，不得覆盖成可执行信号。
- Terminology guard: Wave3 is explicit `no-trade`; P06 must mention and enforce no `secret` access and no `broadcast` capability.
