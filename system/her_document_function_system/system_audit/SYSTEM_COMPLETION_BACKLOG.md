# HER-DFAFS System Completion Backlog

## P0：已补齐

1. K00 canonical bridge
   - 状态：`DONE`
   - 路径：`/root/sikk-gmgn/system/her_document_function_system/controllers/K00_knowledge_intake_controller/`
   - 结果：F00 输入合约现在有真实上游控制器资产，不再依赖聊天上下文。

2. 系统自审 runner
   - 状态：`DONE`
   - 路径：`/root/sikk-gmgn/tools/her_doc_system_audit.py`
   - 结果：可输出 `audit_result_auto.json`、阶段完整性、gap register、status policy。

3. F00 输入合约入口规则
   - 状态：`DONE`
   - 规则：无 K00 handoff / document passport / corpus index / gap detection 时，F00 必须阻断；无 repo_root 或 write_policy 时只能 DESIGN_ONLY；无 KV 可继续但标记 KV_GAP。

## P1：仍建议增强

1. 统一 controller semantic asset registry
   - 状态：`PARTIAL`
   - 当前 runner 已兼容 `01_f00_manifest.yaml` 与 `01_manifest.yaml` 两类命名。
   - 建议后续写入正式 registry 文档，避免未来误判。

2. command registry 升级
   - 状态：`OPEN`
   - 把 `HER_DOC_PIPELINE`、`HER_DOC_SYSTEM_AUDIT`、`HER_DOC_SYSTEM_REVIEW` 写入 CLI/command registry 或 slash-trigger registry。

3. README 任务运行示例
   - 状态：`PARTIAL`
   - 已更新系统级 README；后续可补 mobile-safe one-line commands。

## P2：增强

1. sample replay 覆盖 K00 缺失场景。
2. sample replay 覆盖 F00_BLOCKED 场景。
3. sample replay 覆盖 READY_WITH_GAPS 不得升级 READY 的治理测试。
4. Telegram/mobile-safe one-line command 文档。

## 当前推荐下一步

建立真实 K00 run writer / sample run：

- 输入：source_material + operator_goal + repo_root + execution_boundary + write_policy
- 输出：真实 `k00_handoff_packet.json`
- 然后调用 F00 preflight，验证缺失项能正确 `F00_BLOCKED` 或 `DESIGN_ONLY`。

原因：当前已经完成**系统结构补全**；下一步应验证**具体任务运行闭环**。
