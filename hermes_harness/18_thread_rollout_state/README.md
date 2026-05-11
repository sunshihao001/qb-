# 18_thread_rollout_state — Thread / Rollout / State Bridge

## 定位

记录 HER V2.0+ 的 thread_id、rollout events、state bridge 与全局事件日志。

## 主要结构

- `threads/`：线程级状态文件。
- `rollouts/`：每次 rollout 的运行事件、thread_state、state_bridge。
- `state_snapshots/`：state_bridge 快照。
- `event_log.jsonl`：全局事件日志。
- `state_bridge_index.md`：状态桥索引。

## 使用边界

这里记录运行时状态流转，不负责替代 `14_runtime_hooks/runtime_runs/` 的 runtime audit。
