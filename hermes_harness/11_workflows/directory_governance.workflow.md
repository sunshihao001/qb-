# Directory Governance Workflow

## 1. 适用条件

当任务涉及创建、修改、移动、映射、归档、生成任何文件或目录时，必须先使用本 workflow。

典型场景：

- 新建 markdown / json / csv / script / report。
- 整理目录结构。
- 判断 artifact 应该写入哪里。
- 防止文件散落在项目根目录或 legacy runtime 区。
- 建立 canonical path 与 legacy path 的映射。

## 2. 输入

必须输入：

- 待创建或修改的 artifact 类型
- 所属 bot / domain
- asset_id 或 task_id
- 预期文件名
- 当前项目目录宪法或 route policy

建议读取：

- `/root/sikk-gmgn/AGENTS.md`
- `/root/sikk-gmgn/docs/system_directory_constitution.md`
- `/root/sikk-gmgn/docs/system_directory_routes.json`
- `hermes_harness/01_control_plane/directory_invocation_policy.md`

## 3. 允许工具

允许：

- `read_file`：读取目录宪法、路由表、控制面策略
- `search_files`：检查目标路径是否存在、查找同类文件
- `write_file`：仅在路径判定完成后创建新文件
- `patch`：仅在路径判定完成后修改既有文件
- `terminal`：仅用于 `mkdir`、验证脚本、`git status --short` 等必要命令
- `todo`：记录治理步骤

## 4. 禁止工具

禁止：

- 未回答四个目录问题前直接写文件
- 在项目根目录散放运行输出
- 为了迁移直接删除或移动旧文件
- 将 legacy runtime 目录作为新主写路径
- 用临时备份目录替代 canonical 目录
- 未记录 old_path -> new_path 就做迁移映射

## 5. 执行阶段

### Phase 1：回答四个目录问题

写入前必须回答：

1. 这是哪个 Bot / domain？
2. 这是哪类资产：方法论、代码、数据、schema、contract、报告、token 输出、长任务状态、import、legacy compat？
3. 资产 ID 是什么：token、run、import、case、task？
4. 主写路径是否符合 route policy？

### Phase 2：读取目录规则

读取项目目录宪法与 Hermes 目录策略，确认该类型 artifact 的 canonical 位置。

### Phase 3：检查现状

检查：

- 目标目录是否存在
- 是否已有同名文件
- 是否存在旧版本或相似文件
- 是否需要 copy-only manifest

### Phase 4：路径决策

生成 path decision：

- canonical_path
- reason
- asset_type
- asset_id
- legacy_path_if_any
- migration_mode：none / copy_only / index_only

### Phase 5：执行写入

只在 path decision 通过后进行写入或 patch。

### Phase 6：记录映射

如果涉及旧路径，必须记录 old_path -> new_path，不删除旧文件。

## 6. 输出物

必须输出：

- path decision
- 已写入文件路径
- 是否涉及 legacy mapping
- 是否通过目录治理验证

建议输出：

- 文件自身 header 中记录 canonical path
- 运行日志或 report 中记录 path decision

## 7. 验证标准

通过条件：

- 四个目录问题已回答
- 文件写入 canonical path
- 未在根目录散放运行输出
- 未删除或移动旧文件
- legacy 映射可追踪
- 目标文件可被 `search_files` 或 `read_file` 找到

## 8. 失败处理

如果无法确定路径：

1. 不写运行文件。
2. 将计划写入允许的 plan / task intake 区。
3. 标记缺失：domain / asset_type / asset_id / route。
4. 需要用户决策时只询问最小必要问题。
5. 若规则冲突，转 `recovery.workflow.md`。
