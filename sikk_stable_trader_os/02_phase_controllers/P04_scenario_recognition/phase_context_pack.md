# P04 场景盘型层 Context Pack

## HER 必读定位

Phase Controller 不是阶段说明文档。Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

## 本阶段目标

识别吸筹、拉升、派发、反抽、二段扩张、陷阱风险等场景并记录反证

## 权限边界

- 运行边界：`OBSERVE_PAPER_ONLY`。
- 禁止授权真实交易、签名、broadcast、swap 或私钥读取。
- Markdown 只作为上下文压缩包，不作为机器判断来源。
- 缺失 required 字段必须按 contract 标记 `missing` / `blocked` / `degraded`，不得由 AI 推测补齐。

## HER 运行前必须读取

1. `phase_manifest.yaml`
2. `phase_objective_tree.yaml`
3. `phase_input_contract.json`
4. `phase_output_contract.json`
5. `phase_acceptance_gate.yaml`
6. upstream handoff packet（如存在）

## 证据要求

每个判断必须绑定：字段来源、证据等级、反证记录、失败处理、审计引用、验收结果、下游 handoff 交接路径。
