---
artifact_type: control_policy
version: v1.4
status: canonical
created_at: 2026-05-09T01:03:33Z
route: hermes_runtime_hook_autonomous_problem_loop
supersedes: problem_understanding_closed_loop_policy_v1_3.md
---
# Hermes Harness V1.4 Runtime Hook Policy

## 核心定位
V1.4 不是替代 V1.3 APUR Loop，而是把 V1.3 从“可运行模块”接入 Hermes/HER 任务运行时入口。

目标：复杂任务进入系统后，不再依赖模型自觉记得闭环，而由 runtime hook 强制生成、推进、验证和写回以下链路：

`intake → route_decision → problem_passport → APUR loop → tool_ledger → verification_hook → recovery_hook → learning_writeback → completion_audit`

## 触发条件
当用户请求满足任一条件时，必须进入 V1.4 runtime hook：
- “执行任务 / 全自动完成 / 你来做 / 不要只说方案”类执行命令。
- Hermes/HER/SIKK 底层逻辑、runtime、控制面、闭环、验证、恢复、memory、router、hook 相关改造。
- 需要 3+ 工具步骤、多个文件写入、脚本执行、验证报告或恢复报告的任务。
- 失败后需要追踪根因、不可直接重试的任务。

## Runtime Hook 强制规则
1. **Router Hook**：先判断是否复杂任务；复杂任务必须创建 `runtime_run_id`。
2. **Problem Passport Hook**：不得直接跳方案，必须产生问题护照或引用已有 APUR 问题护照。
3. **State Hook**：每一阶段写入 runtime state；状态不得只存在于对话中。
4. **Tool Ledger Hook**：关键工具调用必须记录目的、输入范围、结果、失败/副作用。
5. **Verification Hook**：完成声明必须由独立验证脚本/报告支持。
6. **Recovery Hook**：验证失败时必须生成 recovery report，不能标记完成。
7. **Learning Writeback Hook**：经验先进入 memory write queue，不直接写 verified memory。
8. **Completion Audit Hook**：最终报告必须包含完成标准、证据、未完成项、下一步。

## 完成定义
V1.4 完成不是“回答已生成”，而是：
- runtime hook 产物存在且非空；
- APUR/run state 可追踪；
- tool ledger 可审计；
- verification report 为 PASSED；
- 若失败则 recovery report 存在且任务状态为 FAILED/PARTIAL；
- learning candidate 已进入 `04_memory/memory_write_queue.jsonl`；
- README / control-plane / scripts / workflow 索引已经更新。

## 禁止项
- 禁止只口头承诺“会自动执行”。
- 禁止无 evidence 直接下结论。
- 禁止跳过 verification hook 声称完成。
- 禁止将未验证经验直接写入长期 memory。
