# Compact Rebuild Policy V2.1

## 定位

compact rebuild 是 semantic reconstruction（语义重建），不是聊天历史摘要。目标是在上下文压缩后恢复 HER 运行所需的最小可执行状态。

## 重建优先级

```text
1. control_plane rules
2. active goal / task passport
3. current phase / route / status
4. acceptance criteria
5. input/output contracts
6. verified evidence
7. current errors / blockers
8. recent tool results with outcomes
9. recovery state
10. memory revalidation status
11. next executable step
12. historical summary only if still causally relevant
```

## 必须保留

- 当前目标和禁止事项。
- 当前阶段、状态码、handoff 状态。
- 已验证事实和证据来源。
- 未解决错误、阻断原因、恢复计划。
- 文件路径、命令、测试结果、运行目录。
- 下一步可执行动作。

## 必须降噪

- 重复自然语言。
- 未验证记忆。
- 过期计划。
- 已完成且无后续依赖的工具日志。
- 与当前目标无因果关系的历史讨论。

## 禁止

- 把 compact 当作“总结得越全越好”。
- 丢失验收标准和阻断条件。
- 把未验证记忆写成事实。
- 把 dry-run 结果写成真实完成。
- 把计划文件生成写成实现完成。

## 输出格式

每次 compact rebuild 至少包含：

```text
Active Task
Goal
Constraints
Completed Actions
Active State
Blocked
Key Decisions
Relevant Files
Remaining Work
Verification Evidence
Next Executable Step
```

## 完成判断

compact rebuild 完成标准：新上下文可以不依赖原聊天全文继续执行，并且不会误判完成状态、不会丢失阻断条件、不会丢失验证证据。
