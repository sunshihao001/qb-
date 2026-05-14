# P09 Review Replay Controller Context v3.0

P09 是复盘回放控制器，不是日报、失败总结脚本或自动调参器。执行前必须读取 K00 handoff、P08/Paper Runtime 输出、当时快照和 trace/handoff/acceptance 包。P09 的核心原则是 **historical snapshot first**：只能使用当时可见数据重建判断，不允许用当前数据覆盖历史决策。

边界：P09 可以生成 calibration / rule review / threshold review / P10 upgrade candidates，但不能直接修改规则、阈值、runtime、paper runtime 或 live execution。

Source doc: `DOC-20260512-P09_REVIEW_REPLAY_CONTROLLER_V3`
