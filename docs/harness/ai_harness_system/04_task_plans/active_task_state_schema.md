# Active Task State JSON Schema

Markdown 适合人看，但 Hermes 必须使用机器可读状态文件判断进度。

## 建议文件

```text
active_task_state.json
```

## 示例结构

```json
{
  "task_id": "hermes.task.20260506.183000.hermes_harness_v1",
  "status": "EXECUTING",
  "task_type": "system_design",
  "current_phase": "phase_03_templates",
  "phases": [
    {
      "phase_id": "phase_00_scan",
      "status": "PASSED",
      "outputs": ["hermes_initial_scan.md"],
      "verification": "PASSED"
    },
    {
      "phase_id": "phase_01_directory_init",
      "status": "PASSED",
      "outputs": ["directory_map.md"],
      "verification": "PASSED"
    }
  ],
  "blocked": false,
  "recovery_required": false,
  "next_action": "run phase_03_templates"
}
```

## 专业意义
Hermes 不再靠聊天记忆判断进度，而靠状态文件判断进度。

## 状态要求
- status 必须来自任务状态机。
- current_phase 必须存在于 phases。
- blocked=true 时不得继续执行。
- recovery_required=true 时必须进入 recovery。
- 每个 phase 必须列出 outputs 和 verification。
