# Task ID Policy

## 用途
标准化 Hermes 任务 ID，避免靠文件名或聊天记忆随意判断任务。

## 标准格式

```text
hermes.task.YYYYMMDD.HHMMSS.slug
```

示例：

```text
hermes.task.20260506.183000.hermes_harness_v1
```

## 所有关键文件必须挂 task_id
- task_passport
- phase_plan
- active_task_state
- execution_loop_log
- verification_report
- recovery_report
- final_report
- memory_write_queue

## 规则
1. 一个任务只能有一个 canonical task_id。
2. 子阶段使用 phase_id，不重新生成 task_id。
3. 续跑任务必须复用原 task_id。
4. 恢复任务必须引用原 task_id 和 recovery_id。
5. 无 task_id 的产物只能算草稿。

## 禁止行为
- 用文件名替代 task_id。
- 用聊天标题替代 task_id。
- 续跑时新建无关联 task_id。
