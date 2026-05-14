# Trace Plane HER Context

Trace Plane 是 SIKK Stable Trader OS 的全链路追踪平面。HER 执行前必须读取本上下文，确认本阶段只定义/记录 trace，不做调度、验收裁决、交接执行、策略判断或真实交易。

## 必须回答
- 当前任务属于哪个阶段/任务树？
- 输入、输出、创建文件、状态变化、验收与 handoff 是否都有 trace？
- Acceptance Plane / Handoff Plane 是否被要求读取 trace_handoff_packet？

## 禁止
- 无 trace 创建核心文件。
- 无 acceptance_trace 交接。
- 无 tool_trace 绑定 Runner。
- 无 runtime_trace 执行 Paper Runtime。
- 任何真实交易、自动下单、私钥/助记词路径。
