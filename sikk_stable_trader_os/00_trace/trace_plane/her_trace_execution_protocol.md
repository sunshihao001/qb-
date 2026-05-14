# HER Trace Execution Protocol

HER 执行任何系统建造任务时必须：
1. 读取当前任务目标。
2. 生成或读取 task_tree_id。
3. 为当前任务创建 TASK_TRACE。
4. 每创建一个文件，创建 ARTIFACT_TRACE。
5. 每生成一个合约，创建 CONTRACT_TRACE。
6. 每改变一个阶段状态，创建 STATE_TRACE。
7. 每执行验收，创建 ACCEPTANCE_TRACE。
8. 每生成交接包，创建 HANDOFF_TRACE。
9. 每绑定工具，创建 TOOL_TRACE。
10. 每运行纸面任务，创建 RUNTIME_TRACE。
11. 每次复盘，创建 REVIEW_TRACE。
12. 每次升级建议，创建 UPGRADE_TRACE。
13. 如果出现缺失、冲突、断链、越权，创建 ERROR_TRACE。

## Forbidden
- 不允许无 trace 创建核心文件。
- 不允许无 trace 进入验收。
- 不允许无 acceptance_trace 交接。
- 不允许无 handoff_trace 进入下游。
- 不允许无 tool_trace 绑定 Runner。
- 不允许无 runtime_trace 执行纸面运行。
- 不允许无 review_trace 做升级。
- 不允许任何 live execution。
