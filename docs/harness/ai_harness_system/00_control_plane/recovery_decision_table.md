# Recovery Decision Table

## 用途
建立“失败类型 → 恢复动作”的标准映射，避免 recovery 只有模板、没有决策规则。

## 失败类型与恢复动作

| 失败类型 | 恢复动作 |
|---|---|
| 文件未生成 | 回到该阶段重新生成 |
| 文件为空 | 重新生成并检查输入 |
| JSON 非法 | 修复 JSON，重新验证 |
| 命令失败 | 记录 stderr，生成 retry plan |
| 权限越界 | BLOCKED，等待用户授权 |
| 任务跑偏 | 回到任务护照重判目标 |
| 上下文缺失 | 重建 active_task_context |
| 验证失败 | 不进入下一阶段，写 recovery |
| 旧任务未完成 | 恢复旧任务，不开新执行流 |

## 规则
1. recovery 必须先分类失败类型。
2. recovery 动作必须写入 recovery_report。
3. 权限越界必须进入 BLOCKED。
4. 验证失败不得进入下一阶段。
5. 旧任务未完成时优先续跑旧任务。
