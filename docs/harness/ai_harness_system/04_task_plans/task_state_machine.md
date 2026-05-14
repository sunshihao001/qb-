# AI 调节系统任务状态机

每个任务必须有状态。

## 状态定义

```text
RECEIVED          已接收目标
SCOUTING          正在侦察
PLANNING          正在规划
READY_TO_EXECUTE  可以执行
EXECUTING         正在执行
VERIFYING         正在验证
RECOVERING        正在恢复
BLOCKED           被阻断
DONE              已完成
ARCHIVED          已归档
```

## 状态流转

```text
RECEIVED
↓
SCOUTING
↓
PLANNING
↓
READY_TO_EXECUTE
↓
EXECUTING
↓
VERIFYING
├── 验证通过 → DONE → ARCHIVED
├── 验证失败 → RECOVERING → PLANNING
└── 高风险 → BLOCKED
```

## 规则

- 任务进入系统后状态为 RECEIVED。
- 完成侦察后进入 SCOUTING。
- 方案确定后进入 PLANNING。
- 满足输入、输出、权限、验证条件后进入 READY_TO_EXECUTE。
- 执行中进入 EXECUTING。
- 执行后必须进入 VERIFYING。
- 验证失败进入 RECOVERING。
- 高风险或权限不足进入 BLOCKED。
- 验证通过后进入 DONE。
- 复盘和归档后进入 ARCHIVED。
