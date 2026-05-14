# P05 Acceptance Check｜phase_05_structure_position｜结构位置确认层

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-09T15:39:01.028624+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: Task 0 只建立任务包、协议、状态、审计；不写 P01-P09 业务代码，不运行 P01-P09 runtime。

## 阶段数据检查
确认 `p05_stage_data.md` 包含目标、定位、上游/下游 handoff、输入合约、输出合约、字段、推理、反证、hard negative、状态码、missing、降级、阻断、验收、gaps。

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
运行 `python3 -m pytest tests/phase_05_structure_position -q`，失败则 REJECTED。

## replay 检查
运行 replay 命令，必须生成本地 handoff、shared_handoff、audit。

## handoff 检查
本地 handoff 与 shared_handoff 关键字段一致；不一致 REJECTED。

## 越权输出检查
禁止输出下游最终结论；本阶段禁止项：策略最终放行、执行交易。

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
`P05_ACCEPTANCE_READY | P05_ACCEPTANCE_READY_WITH_GAPS | P05_ACCEPTANCE_REJECTED`。

## Wave2 专项 counter-evidence 验收
- 检查 P05 replay/audit 是否读取 P04 handoff，并保留 P04 反证链。
- 检查 P05 output 是否包含自身 `counter_evidence`，尤其针对 AVWAP/POC/Failure/Fatigue/Overextension。
- 若 P05 输出策略放行、执行交易、或在缺少 P04 反证时升级结论，状态必须为 `P05_ACCEPTANCE_REJECTED`。
