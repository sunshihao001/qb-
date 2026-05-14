# Command Log Schema

命令日志必须能复盘 Hermes 到底做过什么，而不是只看 Hermes 说了什么。

建议文件：

```text
command_log.jsonl
```

## JSONL 单行格式

```json
{
  "task_id": "hermes.task.20260506.183000.hermes_harness_v1",
  "phase_id": "phase_02_control_plane",
  "command_id": "cmd.0001",
  "cwd": "/root/sikk-gmgn",
  "command": "mkdir -p hermes_harness/01_control_plane",
  "risk_tier": "R1",
  "permission": "ALLOW",
  "expected_effect": "create directory only",
  "actual_result": "success",
  "stdout_path": null,
  "stderr_path": null,
  "exit_code": 0,
  "timestamp": "2026-05-06T18:30:00Z"
}
```

## 必填字段
- task_id
- phase_id
- command_id
- cwd
- command
- risk_tier
- permission
- expected_effect
- actual_result
- exit_code
- timestamp

## 禁止行为
- 只记录命令，不记录预期效果。
- 只记录成功，不记录失败。
- 不记录 cwd。
- 不记录权限判断。
