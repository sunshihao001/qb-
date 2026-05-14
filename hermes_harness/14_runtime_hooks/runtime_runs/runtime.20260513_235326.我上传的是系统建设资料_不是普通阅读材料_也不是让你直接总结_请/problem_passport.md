# Runtime Problem Passport

- runtime_run_id: `runtime.20260513_235326.我上传的是系统建设资料_不是普通阅读材料_也不是让你直接总结_请`
- route: `hermes_runtime_hook_autonomous_problem_loop`
- created_at: `2026-05-13T23:53:26Z`
- user_request: 我上传的是系统建设资料，不是普通阅读材料，也不是让你直接总结。

请先按 HER 底层逻辑处理该文档。

你必须理解：

1. HER 不是聊天总结助手，而是一个受控运行系统。
2. HER 的工作方式是：
   目标识别 → 任务护照 → 路由 → Phase Controller → 输入合约 → 执行协议 → 输出合约 → 验收门 → 状态更新 → handoff → 下一阶段。
3. Phase Controller 不是阶段说明文档，而是 HER 的最小可调节运行单元。
4. 每个 Phase Controller 必须具备：
   - phase_id
   - controller_identity
   - responsibilities
   - permissions
   - forbidden_actions
   - input_contract
   - output_contract
   - execution_protocol
   - state_machine
   - acceptance_gate
   - trace_requirements
   - recovery_policy
   - handoff_packet
5. 上传文档不能直接进入 PXX / IXX / Runner / Tool Binding。
6. 上传文档必须先进入 K00 Knowledge Intake & Taskization。
7. K00 不是只做文档摄取，而是：
   raw 保存 → source registry → document passport → corpus index → system mapping → gap detection → phase task package → phase state → K00 acceptance → K00 handoff。
8. 只有 K00_ACCEPTED 或 K00_READY_WITH_GAPS，并且生成 handoff packet 后，才允许进入目标 Phase Controller。
9. 目标 Phase Controller 执行后，也必须生成自己的 system files、runtime outputs、trace、acceptance、report、handoff。

禁止事项：

1. 不要直接总结文档。
2. 不要直接给结论。
3. 不要跳过 K00。
4. 不要只做 raw 保存就宣称 K00 完成。
5. 不要把聊天上下文当作系统状态。
6. 不要在没有 K00 acceptance / handoff 的情况下进入 PXX / IXX / Controller 执行。
7. 不要把 Phase Controller 当成普通说明文档。
8. 不要无输入合约执行阶段。
9. 不要无输出合约交接下游。
10. 不要无验收门宣称 READY。
11. 不要无 trace / audit 宣称完成。
12. 不要直接修改生产规则。
13. 不要启动 runner / paper runtime / live execution。
14. 不要 wallet signing。
15. 不要 auto deploy。

请按以下完整流程执行：

第一层：HER 任务入口识别

- 判断该文档是否是系统建设资料。
- 生成 task intent / goal passport。
- 判断它影响哪些系统层：
  - methodology
  - control plane
  - phase controller
  - schema / contract
  - data plane
  - trace plane
  - acceptance / handoff plane
  - governance
  - runner / tool binding
  - paper-only runtime
  - report / audit
- 判断它应该进入哪个目标阶段：
  - K00
  - P00-P10
  - I01-I05
  - Governance
  - Runner / Tool Binding
  - Paper Runtime
  - Review / Upgrade

第二层：K00 Knowledge Intake & Taskization

必须生成或更新以下资产：

1. raw input
   - 保存原始上传资料
   - 不覆盖原文
   - 记录 raw_path、source_name、source_type、received_at、doc_id

2. source registry
   - 登记 material_id / doc_id
   - 记录来源、类型、标题、用途、目标阶段候选、处理状态

3. document passport
   - doc_id
   - source_type
   - source_name
   - received_at
   - raw_path
   - document_role.primary_role
   - document_role.secondary_roles
   - summary.core_intent
   - summary.key_points
   - system_mapping.planes
   - system_mapping.affected_phases
   - required_actions
   - evidence_level
   - status

4. corpus index
   - 章节索引
   - 关键对象
   - 核心规则
   - 关键断言
   - 输入输出要求
   - 禁止事项
   - 验收要求
   - handoff 要求

5. system mapping
   - 映射到 HER 系统层
   - 映射到 PXX / IXX / Controller
   - 明确可以影响什么
   - 明确不能直接改变什么

6. gap detection
   - 识别缺失的上游资料、合约、schema、trace、acceptance、handoff、runner、test、index
   - gap 必须分级：
     - BLOCKING_GAP
     - CRITICAL_GAP
     - HIGH_GAP
     - MEDIUM_GAP
     - LOW_GAP

7. phase task package
   生成标准 9 文件：
   - 01_phase_manifest.yaml
   - 02_phase_context_pack.md
   - 03_phase_objective_tree.yaml
   - 04_phase_input_contract.json
   - 05_phase_output_contract.json
   - 06_phase_execution_protocol.md
   - 07_phase_acceptance_gate.yaml
   - 08_phase_state.json
   - 09_phase_handoff_packet.schema.json

8. phase state
   写入 K00 / 目标阶段状态，不允许只存在聊天里。

9. K00 acceptance
   验收 raw / registry / passport / index / mapping / gap / task package / state / handoff 是否齐全。

10. K00 handoff
   生成 K00 → 目标 Phase Controller 的 handoff packet。

第三层：目标 Phase Controller 执行

只有 K00 acceptance 和 K00 handoff 通过后，才允许进入目标阶段。

目标 Phase Controller 执行时必须遵守：

1. 先读取 K00 handoff。
2. 读取 phase task package。
3. 校验 input contract。
4. 按 execution protocol 执行。
5. 生成 output contract 要求的文件。
6. 写 phase_state。
7. 写 trace。
8. 执行 acceptance_gate。
9. 生成 final report。
10. 生成 downstream handoff。
11. 如失败，写 recovery report，不允许假装 READY。

第四层：验收判断

最终状态只能从以下状态中选择：

K00 层：
- K00_ACCEPTED
- K00_READY_WITH_GAPS
- K00_BLOCKED
- K00_REJECTED

目标阶段层：
- PXX_READY
- PXX_READY_WITH_GAPS
- PXX_BLOCKED
- PXX_REJECTED
- IXX_READY
- IXX_READY_WITH_GAPS
- IXX_BLOCKED
- IXX_REJECTED

如果存在 gap，必须保留 gap，不允许把 READY_WITH_GAPS 改写成 READY。

第五层：最终回复格式

完成后必须报告：

1. doc_id
2. raw_path
- classification: `complex`
- requires_apur: `True`
- risk: `medium`

## Intent
把用户的执行命令转成可追踪、可验证、可恢复的 runtime hook 任务。
