# Acceptance Context

HER 执行验收前必须读取本文件。Acceptance Plane 是系统验收裁决平面，不是检查清单。它读取 Trace Plane 的 trace_handoff_packet、Full Control Plane task tree、合约、状态、gap 与治理规则，输出 acceptance_result_packet 与 downstream_permission。

禁止：调度任务、写 trace、执行 handoff、创建业务内容、运行工具、运行 paper runtime、批准 live execution。

硬规则：无 trace 不通过；无合约不交接；Handoff/Tool Binding/Paper Runtime 不得绕过 Acceptance；real_trade_enabled=false。
