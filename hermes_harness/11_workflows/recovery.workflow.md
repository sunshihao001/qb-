# Recovery Workflow

## 1. 适用条件

当任务执行失败、验证失败、状态不一致、路径冲突、工具调用异常、上下文压缩后无法恢复，或连续尝试触发 circuit breaker 时，使用本 workflow。

典型场景：

- 命令失败或测试失败。
- 文件写错路径。
- active task state 与实际文件不一致。
- memory 与当前状态冲突。
- compact 后任务入口丢失。
- 执行路线错误，需要回滚到安全入口。

## 2. 输入

必须输入：

- 失败步骤
- 错误输出或异常描述
- 影响文件 / 命令 / artifact
- 当前 active task state
- 最近一次 verification result

可选输入：

- command log
- execution log
- checkpoint
- recovery circuit breaker policy
- recovery decision table

## 3. 允许工具

允许：

- `read_file`：读取状态、日志、策略、报告、受影响文件
- `search_files`：定位缺失或冲突 artifact
- `terminal`：只读诊断、验证命令、git status/diff
- `patch`：仅用于明确、安全、最小的修复
- `write_file`：仅用于恢复报告或补充缺失治理文件
- `todo`：记录 recovery 阶段

## 4. 禁止工具

禁止：

- 未分类失败就直接继续原路线
- 删除文件作为默认恢复方式
- 用更大范围重写掩盖小错误
- 在 recovery 中引入新功能
- 忽略 circuit breaker 连续失败限制
- 将失败状态写成长久有效 memory

## 5. 执行阶段

### Phase 1：冻结现场

停止继续执行原动作，保留：

- 失败命令
- 错误输出
- 受影响文件
- 当前状态

### Phase 2：失败分类

分类为：

- input_missing
- permission_blocked
- directory_conflict
- syntax_error
- test_failure
- runtime_error
- integration_mismatch
- memory_stale
- compact_rebuild_gap
- unknown

### Phase 3：影响评估

判断影响范围：

- 是否只影响当前文件
- 是否影响 runtime state
- 是否影响控制面规则
- 是否需要用户授权
- 是否触发 circuit breaker

### Phase 4：选择恢复路径

可选路径：

- retry_same_step：同一步最小重试
- patch_and_retry：小修后重试
- rollback_to_checkpoint：回到检查点
- reroute_workflow：重新进入 method wheel
- ask_human：需要用户裁决
- abort_safely：安全终止

### Phase 5：执行恢复

只执行被选中的最小恢复动作，并记录依据。

### Phase 6：恢复验证

恢复后必须运行对应 verification workflow 或最小验证命令。

## 6. 输出物

必须输出：

- recovery report
- failure_type
- impact_scope
- selected_recovery_path
- recovery_action
- verification_after_recovery
- next_entrypoint

建议输出路径：

- `hermes_harness/07_recovery/`
- 或当前 task_id 对应 recovery report

## 7. 验证标准

通过条件：

- 失败已分类
- 影响范围已说明
- 恢复动作与失败类型匹配
- 没有扩大变更范围
- 恢复后验证通过或明确 blocked
- 下一入口明确

## 8. 失败处理

如果 recovery 也失败：

1. 增加 circuit breaker 计数。
2. 不进行第三次盲目重试。
3. 输出 blocked report。
4. 若需要权限或业务裁决，询问用户。
5. 若可重新路由，回到 `method_wheel.workflow.md`。
