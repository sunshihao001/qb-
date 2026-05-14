# Phase Controller 数据模型自动化方案书 v1.0

> planbook_id: `phase_controller_data_model_workflow_v1`
> status: `ACTIVE_CONTROL_SURFACE`
> runtime_boundary: `OBSERVE_PAPER_ONLY`
> owner_layer: `HER_CONTROL_PLANE`
> source: 用户定义 Phase Controller 专业化要求 + system_methodology_blueprint.md

## 1. 核心定义

Phase Controller 不是阶段说明文档。

Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。

它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

## 2. 目标

建立 HER 可读取、可调度、可验证的 Phase Controller 任务书执行包，使每个 P00-P09 阶段具备统一数据模型，而不是自由发挥式 Markdown 说明。

## 3. 标准 9 件套数据模型

每个 Phase Controller 必须包含：

1. `phase_manifest.yaml`：阶段身份证，定义是谁、负责什么、权限边界、上下游。
2. `phase_context_pack.md`：HER 阶段上下文压缩包，运行时必须先读，防止把事实阶段误做策略判断。
3. `phase_objective_tree.yaml`：目标层级与任务树，使 HER 按任务树推进。
4. `phase_input_contract.json`：阶段输入契约，定义 required/optional 字段、缺失处理、上游来源。
5. `phase_output_contract.json`：阶段输出契约，定义必须写出的机器文件与字段。
6. `phase_execution_protocol.md`：运行协议，告诉 HER 怎么运行、怎么失败恢复、怎么回写。
7. `phase_acceptance_gate.yaml`：验收门，决定什么时候可以说完成。
8. `phase_state.json`：运行状态，每跑一步都要回写。
9. `phase_handoff_packet.schema.json`：交接包结构，定义下游只能读什么。

## 4. 执行顺序

HER 每次执行本任务包必须：

1. 读取 `00_methodology/system_methodology_blueprint.md`。
2. 读取 `00_system_registry/phase_registry.yaml`。
3. 检查 P00-P09 每个 phase package 是否有 9 件套。
4. 对每个文件检查：是否是占位说明、是否有字段来源/证据/反证/失败处理/验收/交接路径。
5. 先补控制模型，不做交易策略判断。
6. 写总控 Skill 核心定义，使后续 HER 启动有固定入口。
7. 更新运行状态与审计报告。
8. 运行验证脚本。
9. 只有验收门通过，才允许进入下一阶段落地。

## 5. 专业数据模型原则

- `manifest` 管身份和权限，不管判断结论。
- `context_pack` 管上下文压缩，不作为机器判断来源。
- `objective_tree` 管任务树和依赖关系，不允许 HER 跳步。
- `input_contract` 管字段来源与缺失动作。
- `output_contract` 管必须输出与下游读取范围。
- `execution_protocol` 管调度、恢复、回写、禁止事项。
- `acceptance_gate` 管完成判定。
- `phase_state` 管当前运行事实。
- `handoff_schema` 管下游交接边界。

## 6. 自动化交易工作流边界

本阶段只建立自动化交易研究系统的控制闭环，不授权真实交易：

- allowed: observe, replay, paper-only, manual review ticket, rule proposal.
- forbidden: private key read/write, signing, broadcast, swap execution, real_trade_enabled.

## 7. 验收标准

- P00-P09 均存在 9 件套。
- 9 件套均可解析（yaml/json/md）。
- 总控 Skill 存在并包含 Phase Controller 核心定义。
- 至少 P00/P01 的 placeholder 被替换为可执行控制语义。
- 验收结果写入 `09_reports/acceptance_reports/phase_controller_data_model_acceptance_result.json`。
- 安全扫描没有实盘授权关键字。

## 8. 下一步

验收通过后进入 `system_planes_definition_landing` 或更深层的 Phase Controller runnable runner/code validator，不把文档完成误判为实盘 ready。
