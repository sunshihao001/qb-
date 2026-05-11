# Method Wheel Workflow

## 1. 适用条件

当任务需要选择执行方法、分流任务类型、决定下一步路线，或在多个执行策略之间切换时，使用本 workflow。

典型场景：

- 新任务进入 Hermes Harness runtime。
- 用户输入包含多个可能任务类型。
- 当前任务需要从 research / code / recovery / verification / directory governance 中选择路线。
- 执行中发现原路线不适用，需要重新路由。

## 2. 输入

必须输入：

- 用户原始请求
- 当前任务上下文或 active task state
- 可用 artifact 列表
- 当前权限等级
- 当前风险等级

可选输入：

- 历史任务报告
- memory revalidation 结果
- compact rebuild 摘要
- 上一次 method wheel 决策

## 3. 允许工具

允许：

- `read_file`：读取控制面、状态、报告、模板
- `search_files`：查找相关策略、workflow、artifact
- `terminal`：仅用于只读检查命令，例如 `pwd`、`git status --short`、验证脚本 dry-run
- `todo`：维护当前执行阶段

## 4. 禁止工具

禁止：

- 未经路由直接 `write_file` 创建业务 artifact
- 未经权限检查直接修改代码
- 未经风险评估执行 destructive shell 命令
- 用长期 memory 直接替代当前状态检查
- 跳过 workflow 选择，直接进入实现

## 5. 执行阶段

### Phase 1：任务识别

识别任务属于以下一种或多种类型：

- research
- design
- code_change
- debugging
- verification
- recovery
- directory_governance
- memory_revalidation
- audit

### Phase 2：输入完整性检查

检查是否具备：

- 原始目标
- 当前状态
- 输出要求
- 风险边界
- 验证方式

缺失关键输入时，进入 blocked 或 intake 状态。

### Phase 3：方法轮选择

根据任务类型选择主 workflow：

- 需要选择方法：继续本 workflow
- 需要写文件：转 `directory_governance.workflow.md`
- 需要改代码：转 `code_change.workflow.md`
- 需要验证：转 `verification.workflow.md`
- 需要恢复：转 `recovery.workflow.md`

### Phase 4：生成路由结果

输出 route decision：

- selected_workflow
- reason
- required_inputs
- allowed_tools
- forbidden_tools
- next_entrypoint
- verification_method

### Phase 5：交接执行

将 route decision 写入任务上下文或执行日志，然后进入被选中的 workflow。

## 6. 输出物

必须输出：

- 方法轮路由结果
- 选择理由
- 下一执行入口
- 验证方法

建议输出路径：

- `hermes_harness/03_task_runtime/route_decision.json`
- 或当前 task_id 对应的 runtime/report 文件

## 7. 验证标准

通过条件：

- 任务类型已明确
- selected_workflow 不为空
- 选择理由能追溯到输入
- 下一入口存在或可创建
- 工具权限与风险等级一致
- 没有在路由前执行高风险写入或修改

## 8. 失败处理

如果无法选择 workflow：

1. 标记状态为 `blocked_needs_input`。
2. 写明缺失输入。
3. 不进行写入或代码修改。
4. 若是状态缺失，先执行 startup / runtime state 检查。
5. 若是策略冲突，转 `recovery.workflow.md`。
