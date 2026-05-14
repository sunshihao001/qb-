# Sample Document: 测试计划不能等于测试证据

这是一份系统建设资料，不是普通阅读材料。

当前系统存在一个风险：AI 经常把“测试计划已生成”误认为“测试已完成”。

需要建立一条系统规则：

1. test_plan 只能表示计划。
2. TESTED 必须要求真实 test_command、exit_code、stdout_path、stderr_path、passed_count、failed_count。
3. 如果只有 test_plan，没有 test_evidence，状态必须是 TEST_PLANNED_ONLY 或 READY_WITH_GAPS。
4. 该规则应该影响 V00_validation_evidence_controller、A00_acceptance_evidence_controller 和 G00_governance_boundary_controller。
5. 该规则需要进入 evidence_policy。
6. 后续所有 controller 不允许把 PLAN 当作 EVIDENCE。
