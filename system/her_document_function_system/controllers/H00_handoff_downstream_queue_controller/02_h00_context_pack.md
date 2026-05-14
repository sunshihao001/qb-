# H00 Context Pack

H00 是 HER 的 Handoff / Downstream Queue 控制器。它读取 A00 handoff/readiness/evidence/gap/risk/forbidden actions，输出 downstream targets、routing decisions、queue items、dependency graph、priority plan、gap/risk binding、handoff packets、queue state、trace/audit、recovery 和 final report。

禁止：启动 live/paper runtime、执行下游任务、wallet signing、auto deploy、production trading、把 queue_created 当作 task_executed。
