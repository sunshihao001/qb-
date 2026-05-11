# Code Change Workflow

## 1. 适用条件

当任务涉及修改代码、脚本、测试、配置、运行逻辑、CLI 行为或自动化检查时，使用本 workflow。

典型场景：

- 新增或修改 Python / JavaScript / shell 脚本。
- 修改 Hermes Harness runtime 脚本。
- 添加验证器、检查器、报告生成器。
- 修复 bug 或测试失败。
- 调整配置但不涉及私钥或真实交易。

## 2. 输入

必须输入：

- 变更目标
- 涉及文件路径或模块范围
- 当前失败现象或需求描述
- 风险等级
- 验证命令或验证标准

可选输入：

- 现有测试输出
- 相关控制面策略
- active task state
- 目录治理 path decision

## 3. 允许工具

允许：

- `read_file`：读取代码、策略、测试、配置
- `search_files`：定位文件、函数、测试、引用
- `patch`：小范围修改既有文件
- `write_file`：仅在目录治理通过后创建新文件
- `terminal`：运行测试、lint、脚本 dry-run、git diff/status
- `execute_code`：处理批量检查或结构化验证
- `todo`：维护阶段状态

## 4. 禁止工具

禁止：

- 未读取相关代码就直接改
- 未经目录治理创建新文件
- 未经明确授权执行真实 swap、签名、broadcast、私钥读取或写入
- 删除已有模块作为默认修复方式
- 以通过表面测试为由跳过独立验证
- 将 paper / simulation 改成真实交易逻辑

## 5. 执行阶段

### Phase 1：范围确认

确认：

- 目标文件
- 影响面
- 是否需要新文件
- 是否触及权限边界
- 是否需要先进入 directory governance

### Phase 2：现状读取

读取相关代码、测试、控制面策略，不凭记忆改代码。

### Phase 3：最小变更设计

设计最小可验证变更：

- 变更点
- 不变边界
- 验证命令
- 回滚方式

### Phase 4：执行修改

使用 `patch` 优先；仅当创建完整新文件时使用 `write_file`。

### Phase 5：运行验证

至少运行：

- 语法检查
- 相关脚本 dry-run
- 针对性测试或现有测试
- 必要时运行 project-specific validator

### Phase 6：审查 diff

检查：

- 变更是否超出范围
- 是否引入危险行为
- 是否破坏目录治理
- 是否需要更新文档或 workflow

## 6. 输出物

必须输出：

- 修改文件清单
- 变更摘要
- 验证命令与结果
- 未解决风险或后续入口

建议输出：

- runtime execution log
- verification report
- git diff 摘要

## 7. 验证标准

通过条件：

- 修改前已读取相关文件
- 修改范围与目标一致
- 语法检查通过
- 相关测试或 dry-run 通过
- 没有触发禁止工具或禁止行为
- diff 可解释且无意外大改

## 8. 失败处理

如果修改失败：

1. 不扩大修改范围。
2. 保留错误输出。
3. 分类失败类型：syntax / test / integration / permission / directory / unknown。
4. 如果连续失败或策略冲突，转 `recovery.workflow.md`。
5. 如果缺少输入，回到 `method_wheel.workflow.md` 或 task intake。
