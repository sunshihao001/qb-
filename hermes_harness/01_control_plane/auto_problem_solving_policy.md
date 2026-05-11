# 自动问题理解与闭环解决策略

- artifact_type: control_policy
- version: v1.3-apur
- route: problem_understanding_closed_loop_resolution
- module: APUR Loop / Auto Problem Understanding & Resolution Loop
- status: canonical

## 模块定位

APUR Loop 是 Hermes 的认知运行时模块。它不负责替代具体业务执行器，而负责让 Hermes 在处理复杂问题前后形成可审计的外部判断产物链：问题护照、理解报告、证据计划、假设集合、根因报告、方案设计、执行计划、验证裁决、失败归因、复盘写回。

## 根原则

Hermes 不得直接跳到解决方案。任何复杂问题必须先经过问题护照、理解报告、证据计划、假设生成、根因定位、方案设计、执行计划、验证和复盘。

## 问题闭环流程

1. 问题接收：生成 problem_passport。
2. 自动理解：生成 understanding_report，定位系统层级。
3. 证据规划：生成 evidence_plan，区分必看证据、可选证据、禁止证据。
4. 假设生成：生成 hypothesis_set，候选假设不得冒充结论。
5. 根因定位：生成 root_cause_report，区分症状、直接原因、系统根因、过程根因、验证根因、恢复根因。
6. 方案设计：生成 solution_design，必须可执行、可验证、可恢复。
7. 执行计划：生成 execution plan / loop_state，拆阶段执行。
8. 验证裁决：生成 resolution_verification，判断问题是否真的解决。
9. 失败归因：验证失败时生成 failure_attribution，不得声称完成。
10. 复盘写回：验证通过后生成 learning_writeback，并写入 memory_write_queue.jsonl。

## 禁止行为

1. 禁止无证据直接下结论。
2. 禁止只解释问题不生成解决方案。
3. 禁止只生成方案不定义验证。
4. 禁止验证失败后继续声称完成。
5. 禁止把未验证经验写入长期记忆。
6. 禁止把表面症状当根因。
7. 禁止把执行动作当闭环完成。
8. 禁止把模型自称完成当作验证证据。
9. 禁止读取、输出或保存私钥/API key/token。
10. 禁止在 APUR dry-run 中修改 SIKK 业务代码或触发真实交易。

## 闭环完成定义

只有同时满足以下条件，才允许标记 CLOSED：

- 问题已结构化；
- 证据已收集或明确缺口；
- 假设已生成并标注证据状态；
- 根因已定位；
- 方案已生成；
- 执行或 dry-run 已完成；
- 结果已独立验证；
- 失败时已归因并给出恢复入口；
- 通过验证的经验进入 memory_write_queue；
- 下一轮入口已明确。

## 失败处理

验证失败时，状态不得进入 CLOSED，必须进入 FAILURE_ATTRIBUTION 或 RECOVERY_PLANNED，并写明失败阶段、失败类型、失败证据、可恢复动作与下一轮入口。

## 记忆写回规则

APUR 只允许把稳定规则、复用流程、失败教训写入 `04_memory/memory_write_queue.jsonl`。不得直接写 `verified_memory.jsonl`，不得写入未验证猜测，不得写入临时任务进度。
