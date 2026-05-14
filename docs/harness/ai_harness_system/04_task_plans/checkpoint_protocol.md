# Checkpoint Protocol

## 用途
为 Hermes 长任务建立断点续跑协议。

## checkpoint 文件
每阶段完成后生成：

```text
checkpoint.json
```

## 格式

```json
{
  "task_id": "hermes.task.20260506.183000.long_task",
  "checkpoint_id": "checkpoint.phase_03",
  "completed_phase": "phase_03",
  "verified": true,
  "next_phase": "phase_04",
  "resume_command": "continue from phase_04 using active_task_state.json",
  "required_context_files": [
    "active_task_context.md",
    "phase_plan.md",
    "execution_loop_log.jsonl"
  ]
}
```

## 规则
1. 每阶段完成后写 checkpoint。
2. 未 verified 的 checkpoint 不能作为续跑入口。
3. resume 必须读取 active_task_state.json。
4. 缺 required_context_files 时必须进入 recovery。
