     1|# Workflow 模块目录
     2|
     3|## 定位
     4|`11_workflows/` 用于保存 Hermes Harness 的可执行工作流模块。
     5|
     6|这里的 workflow 不是普通 prompt，也不是自由文本提示词，而是可被 runtime 调用、约束、验证和恢复的工作流模块。
     7|
     8|每个 `.workflow.md` 必须至少包含：
     9|
    10|- 适用条件
    11|- 输入
    12|- 允许工具
    13|- 禁止工具
    14|- 执行阶段
    15|- 输出物
    16|- 验证标准
    17|- 失败处理
    18|
    19|## 模块清单
    20|
    21|- `method_wheel.workflow.md`：方法轮选择与调度工作流
    22|- `directory_governance.workflow.md`：目录治理与写入路径工作流
    23|- `code_change.workflow.md`：代码变更工作流
    24|- `recovery.workflow.md`：失败恢复工作流
    25|- `verification.workflow.md`：独立验证工作流
    26|- `wallet_intel_semantic_integration.workflow.md`：Wallet-Intel 钱包数据语义整合、旧目录导入、数据护照、事实/证据/推断/交接分层与导入后理解验证工作流
    27|- `problem_understanding_closed_loop_resolution.workflow.md`：Hermes Harness V1.3 全自动问题理解与闭环解决工作流；用于问题接收、自动理解、证据收集、假设生成、根因定位、方案生成、执行、验证、失败恢复与复盘写回
    28|- `hermes_runtime_hook_autonomous_problem_loop.workflow.md`：Hermes Harness V1.4 runtime hook 工作流；用于把复杂任务入口绑定到 router/state/tool-ledger/verification/recovery/writeback/completion-audit 闭环
- `judgment_governance.workflow.md`：Hermes Harness V1.6 判断治理工作流；用于治理问题分诊、证据阈值、拒绝行动、复杂度刹车、元验证、反自欺、记忆生命周期与人类裁决边界
    29|
    30|## 核心原则
    31|
    32|```text
    33|Skill 不直接等于 prompt。
    34|Skill / workflow 应作为边界明确、工具受控、结果可验证的执行模块。
    35|```
    36|
    37|## 调用规则
    38|
    39|1. 先判断任务是否匹配 workflow 的适用条件。
    40|2. 再检查输入是否满足 workflow 的输入契约。
    41|3. 只使用 workflow 明确允许的工具。
    42|4. 不使用 workflow 明确禁止的工具。
    43|5. 按阶段执行，不跳过验证。
    44|6. 输出必须能被验证标准检查。
    45|7. 失败时进入 workflow 定义的失败处理路径。
    46|