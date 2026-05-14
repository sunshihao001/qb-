# Trace Plane Acceptance Criteria

## TRACE_READY
必须具备 27 个核心文件、trace_id 体系、对象注册、全部模型、trace_handoff_contract、HER trace execution protocol，并且不存在无 trace 的核心阶段产物。

## TRACE_READY_WITH_GAPS
允许进入 Acceptance Plane，但限制为：历史文件部分无 trace、legacy runtime 未完整映射、Runner/Paper Runtime/Review 样本尚未真实接入、trace validator 未代码化。禁止自动 Paper Runtime 与任何实盘路径。

## TRACE_REJECTED
没有 trace_id、任务树 trace、artifact/contract/state/acceptance/handoff trace，或允许 Acceptance/Handoff/Runner/Paper Runtime 绕过 trace 时必须驳回。
