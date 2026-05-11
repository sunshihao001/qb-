# Verification Workflow

## 1. 适用条件

当任务需要声明完成、验证代码/文件/目录/状态/记忆/建议是否可靠，或用户要求检查结果时，使用本 workflow。

典型场景：

- 代码变更后。
- 新 artifact 创建后。
- recovery 后。
- 基于 memory 给出建议前。
- 任务完成前。
- compact rebuild 或 resume 后。

## 2. 输入

必须输入：

- 待验证对象
- 预期结果
- 验证标准
- 相关文件路径或命令
- 执行日志或变更摘要

可选输入：

- active task state
- verification definition
- memory revalidation log
- command log
- git diff

## 3. 允许工具

允许：

- `read_file`：读取待验证文件、报告、策略、日志
- `search_files`：确认文件存在、字段存在、重复项、引用关系
- `terminal`：运行测试、语法检查、验证脚本、git status/diff
- `execute_code`：批量结构化检查
- `todo`：更新验证阶段状态

## 4. 禁止工具

禁止：

- 由同一个执行结论直接自证完成
- 没有工具证据就声明 PASSED
- 只检查文件存在，不检查关键内容
- 只检查脚本退出码，不检查输出语义
- 将未验证 memory 当作事实
- 验证失败后仍输出 DONE

## 5. 执行阶段

### Phase 1：定义验证对象

明确验证对象类型：

- file
- directory
- code
- command_output
- runtime_state
- memory
- workflow
- report
- recommendation

### Phase 2：建立验证标准

至少包括：

- 存在性
- 完整性
- 语义正确性
- 路径正确性
- 与控制面一致性
- 可复现性

### Phase 3：执行独立检查

使用与执行步骤不同的检查方式验证，例如：

- 创建文件后用 `search_files` / `read_file` 读取确认
- 修改代码后运行测试和 `git diff`
- memory 使用前运行 revalidation
- 目录写入后检查 route policy

### Phase 4：记录证据

记录：

- 检查命令或工具
- 输出摘要
- pass/fail 判定
- 失败原因

### Phase 5：形成结论

结论只能是：

- PASSED
- FAILED
- PARTIAL
- BLOCKED

不得用模糊词替代。

### Phase 6：失败转 recovery

任何 FAILED 或 BLOCKED 必须给出 recovery entrypoint。

## 6. 输出物

必须输出：

- verification report
- checked_objects
- evidence
- result：PASSED / FAILED / PARTIAL / BLOCKED
- next_action

建议输出路径：

- `hermes_harness/06_verification/`
- 或当前 task_id 对应 verification report

## 7. 验证标准

本 workflow 自身通过条件：

- 验证对象已列明
- 验证标准已列明
- 至少一个独立工具检查已执行
- 结论为四态之一
- 失败时给出 recovery entrypoint
- 未把执行者主观判断当成证据

## 8. 失败处理

如果验证无法完成：

1. 标记为 BLOCKED。
2. 说明缺失证据。
3. 不声明 DONE。
4. 若缺失可补充，补充后重试验证。
5. 若发现执行错误，转 `recovery.workflow.md`。
