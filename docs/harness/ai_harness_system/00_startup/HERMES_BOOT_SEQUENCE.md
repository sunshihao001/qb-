# HERMES BOOT SEQUENCE

## 用途
定义 Hermes 每次执行前的严格启动协议。

## 启动顺序

```text
启动检查
↓
读取启动上下文
↓
读取控制面
↓
读取 natural_language_intake_protocol.md
↓
读取 verified memory
↓
检查当前任务是否有 active state
↓
判断是否是新任务 / 续跑任务 / 恢复任务
↓
对当前自然语言输入执行 task routing
↓
生成 startup_check_report.md
```

## 每次执行前必须知道
1. 当前是不是新任务。
2. 当前有没有未完成任务。
3. 是否存在 blocked / recovery 状态。
4. 是否允许继续执行。
5. 是否需要先验证旧任务。

## 禁止行为
- 不检查 active state 就直接执行。
- 不读控制面就修改文件。
- 不判断 blocked / recovery 状态就继续推进。
- 把旧任务状态当成新任务目标。

## 检查标准
- 是否生成 startup_check_report.md。
- 是否识别 task_mode：new / resume / recovery。
- 是否检查 active_task_state.json。
- 是否检查 blocked 和 recovery_required。
