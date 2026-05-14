# P08 复盘学习层 Execution Protocol

## Runtime Rule

Phase Controller 不是阶段说明文档。Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

## Execution Steps

1. Read `phase_context_pack.md` and `phase_manifest.yaml`.
2. Read upstream handoff required by `phase_input_contract.json`.
3. Validate required fields and apply each `missing_action`.
4. Execute objective tree tasks in order; do not skip failed prerequisites.
5. Invoke only registered Atomic Skills: `failure_attribution_skill, explanation_report_skill, hard_negative_filter_skill`.
6. Build evidence bundle: 字段来源 field source, evidence level, 反证 counter evidence, hard negatives, invalidation conditions.
7. Write all required outputs from `phase_output_contract.json`.
8. Run 验收 gate `phase_acceptance_gate.yaml`.
9. Update `phase_state.json`.
10. Emit handoff packet matching `phase_handoff_packet.schema.json`.

## Failure Recovery

- Missing recoverable input → `PHASE_PAUSED` with gap record.
- Critical required field missing → `PHASE_REJECTED`.
- Contract/schema parse failure → `PHASE_ERROR` or `PHASE_REJECTED` by gate.
- Hard negative hit → block downstream unless acceptance gate explicitly maps to observe-only continuation.

## 禁止 / Forbidden

No private key, no signing, no broadcast, no swap, no real trade authorization, no AI fact invention, no report-as-state.
