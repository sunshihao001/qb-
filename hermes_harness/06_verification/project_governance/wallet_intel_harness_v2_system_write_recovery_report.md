# Hermes Wallet-Intel Harness V2.0 系统写入 Recovery 报告

- 验证时间：2026-05-07T10:29:32Z
- 验证范围：Hermes Wallet-Intel Harness V2.0 系统写入状态
- 总体结论：FAIL

## 1. 失败项
- 任务路由规则已写入：FAIL（`01_control_plane/wallet_intel_task_routing_rule_v2.md`；MISSING_ANCHOR: task_type = wallet_intel_semantic_integration, 任务路由规则）
- workflow 已写入：FAIL（`11_workflows/wallet_intel_semantic_integration.workflow.md`；MISSING_ANCHOR: Wallet-Intel Semantic Integration Workflow, 固定工作流）
- 数据分层规则已写入：FAIL（`01_control_plane/wallet_intel_data_layering_rule_v2.md`；MISSING_ANCHOR: 四个核心语义层, 钱包事实层, 结构证据层, 行为推断层, 策略交接层）
- 数据契约规则已写入：FAIL（`01_control_plane/wallet_intel_data_contracts_rule_v2.md`；MISSING_ANCHOR: 数据契约）
- 字段字典规则已写入：FAIL（`01_control_plane/wallet_intel_field_dictionary_rule_v2.md`；MISSING_ANCHOR: 字段字典）
- 数据护照规则已写入：FAIL（`01_control_plane/wallet_intel_data_passport_rule_v2.md`；MISSING_ANCHOR: 数据护照）
- 旧目录兼容规则已写入：FAIL（`01_control_plane/wallet_intel_legacy_directory_compatibility_rule_v2.md`；MISSING_ANCHOR: 旧目录）
- 完成验证规则已写入：FAIL（`01_control_plane/wallet_intel_completion_verification_rule_v2.md`；MISSING_ANCHOR: 不是“文件复制完成”，而是“Hermes 能按 token 理解数据”）
- 恢复规则已写入：FAIL（`01_control_plane/wallet_intel_recovery_policy_v2.md`；MISSING_ANCHOR: 不会乱判断）
- 记忆候选已写入：FAIL（`10_audit/wallet_intel_memory_candidate_entries_v2.md`；MISSING_ANCHOR: validation_status: candidate, 本文件仅写入 candidate）
- 路由模拟测试通过：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_verification.md`；MISSING_ANCHOR: 总体结论：PASS）
- 没有实际扫描旧目录：PASS（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；PASS）
- 没有复制旧数据：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；MISSING_ANCHOR: 本次仅为路由模拟, 不复制）
- 没有删除、移动、覆盖旧文件：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；MISSING_ANCHOR: 删除旧目录, 移动旧目录, 覆盖旧文件, 本次仅为路由模拟）
- 没有修改业务代码：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；MISSING_ANCHOR: 不修改业务代码）
- 没有触发交易：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；MISSING_ANCHOR: 不触发交易）
- 没有读取或输出密钥：FAIL（`06_verification/project_governance/wallet_intel_stage11_route_simulation_output.md`；MISSING_ANCHOR: 读取或输出私钥、API key、token）

## 2. Recovery 动作
1. 停止声明系统写入完成。
2. 回到失败项对应阶段重写或补写 artifact。
3. 重新读取验证报告。
4. 重新生成系统写入验证报告。
5. 在全部 PASS 前不得提升记忆状态，不得声明 Harness V2.0 写入完成。
