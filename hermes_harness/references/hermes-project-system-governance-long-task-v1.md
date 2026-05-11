---
artifact_type: task_book
status: draft
version: v1.0
scope: hermes_harness_project_governance
---
# Hermes 项目体系侦察与目录治理长任务 V1

## 任务目的

把 `/root/sikk-gmgn` 中过去零散建立的项目、目录、代码、报告、数据、方法轮、运行输出，统一梳理成一套可读取、可索引、可追踪、可继续开发的项目知识地图。

本任务的目标不是立即搬目录，而是先完成：

1. 完整侦察
2. 分类
3. 目录宪法
4. 路径注册表
5. 模块注册表
6. 旧目录映射
7. 迁移建议
8. 完整性验证

只有在地图建立完成后，才讨论是否迁移。

## 核心判断

当前核心问题不是文件多，而是：

- 系统没有统一控制面
- 项目根目录不统一
- 代码、数据、报告、方法轮、运行输出混在一起
- Hermes 读取上下文时不知道哪里是主路径
- 后续开发任务无法稳定续跑

## 严格边界

### 允许
- 只读扫描目录和文件
- 读取文本文件必要片段
- 统计文件、目录、大小、修改时间
- 建立索引、注册表、映射、建议、报告
- 在 Hermes harness 目录内创建本任务产物
- 分阶段推进并写 checkpoint
- 生成迁移建议，但不执行迁移

### 禁止
- 不删除任何文件
- 不执行 `rm` 或 `rm -rf`
- 不移动旧目录
- 不重命名旧文件
- 不覆盖旧运行数据
- 不修改交易系统
- 不触发真实交易
- 不读取或输出私钥、API key、token
- 不执行 `git push`
- 不执行 `git reset --hard`
- 不执行 `git clean -fd`
- 不把未知目录标记为可删除
- 不把未验证结论写入长期记忆
- 不声称完成但没有验证报告

## 最终输出

至少生成以下产物：

### 人类可读报告
- `/root/sikk-gmgn/hermes_harness/08_reports/final_reports/PROJECT_SYSTEM_MAP_V1.md`
- `/root/sikk-gmgn/hermes_harness/08_reports/final_reports/DIRECTORY_GOVERNANCE_REPORT_V1.md`
- `/root/sikk-gmgn/hermes_harness/08_reports/final_reports/MIGRATION_RECOMMENDATION_V1.md`

### 机器可读索引
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/file_inventory.jsonl`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/directory_inventory.jsonl`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/module_registry.json`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/path_registry.json`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/legacy_path_map.json`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/code_entrypoint_index.json`
- `/root/sikk-gmgn/hermes_harness/03_task_runtime/project_inventory/dataflow_map.json`

### 验证与恢复
- 验证报告
- 恢复报告（仅在失败时）
- checkpoint 文件

## 推荐长期执行方式

这个任务应运行成一个**多阶段长任务**，每个阶段结束必须写 checkpoint，然后继续下一阶段。

### 阶段 0：启动与边界锁定
目标：初始化本任务状态，固定边界和输出目录。

产物：
- task passport / task state
- checkpoint 0
- 启动摘要

### 阶段 1：只读全局侦察
目标：扫描 `/root/sikk-gmgn`，建立全局目录感知，不修改任何文件。

产物：
- 初版 file inventory
- 初版 directory inventory
- 初版 runtime map

### 阶段 2：目录与文件分类
目标：把文件和目录按类型分层。

分类至少包括：
- 代码
- 数据
- 报告
- 方法轮
- 运行输出
- 配置
- 旧系统
- 入口脚本
- 测试
- 模板
- 研究产物

### 阶段 3：代码入口与数据流识别
目标：识别主要脚本入口、CLI 参数、输入输出、数据去向。

产物：
- code_entrypoint_index.json
- dataflow_map.json

### 阶段 4：混乱点与冲突点审计
目标：识别重复、冲突、旧路径、命名漂移、主路径不统一问题。

产物：
- conflict list
- ambiguity list
- stale path list

### 阶段 5：目录宪法与路径注册表
目标：建立推荐结构，但不执行迁移。

产物：
- directory governance recommendation
- path registry
- module registry
- legacy path map

### 阶段 6：迁移建议，不执行迁移
目标：列出哪些路径建议保留、映射、标准化、归档或人工确认。

### 阶段 7：验证完整性与续跑入口
目标：验证所有索引、注册表、报告是否存在且可读。

### 阶段 8：写入长期规则候选
目标：把已经验证过的稳定规则整理为未来可纳入 Hermes 控制面的候选规则。

## 自动化执行原则

如果要做成全自动长任务，必须遵守以下运行模式：

1. **先侦察，再决定**
2. **先建图，再迁移**
3. **每阶段都写 checkpoint**
4. **每阶段都可独立验证**
5. **失败必须进入 recovery，不允许假完成**
6. **所有产物必须可回读、可索引、可追踪**
7. **禁止在没有地图时直接做大规模写入**

## 目录属性判断规则

每个目录都要判断以下 6 个属性：

- 目录类型：代码 / 数据 / 报告 / 方法轮 / 运行输出 / 配置 / 旧系统
- 当前状态：活跃 / 旧版保留 / 未知 / 可归档候选
- 是否可写：新任务是否允许继续写入
- 是否可读：是否可作为上下文来源
- 所属模块：属于哪个系统或阶段
- 后续动作：保留 / 标准化 / 建映射 / 待人工确认

## 推荐标准结构

最终推荐采用以下逻辑，而不是立刻强制迁移：

```text
/root/sikk-gmgn/
├── AGENTS.md
├── hermes_harness/
├── docs/
├── contracts/
├── schemas/
├── scripts/
├── tests/
├── tools/
├── research_loop/
├── data/
│   ├── legacy_runtime_keep_in_place/
│   ├── source_wallet_bot/
│   ├── intel_bot/
│   └── runtime_runs/
└── reports/
```

## 任务完成条件

任务只有在以下条件同时满足时才能结束：

- 已完成全局侦察
- 已完成分类
- 已建立目录宪法建议
- 已建立路径注册表
- 已建立模块注册表
- 已建立旧目录映射
- 已建立迁移建议
- 已完成验证
- 没有删除、移动或重命名旧文件
- 没有伪造历史记录

## 失败处理

如果任何阶段失败：

- 保留失败证据
- 写 recovery report
- 标记 blocked 或 partial
- 不进入迁移阶段
- 不声称完成

## 给 Hermes 的执行口令

```text
先侦察，后分类；先建图，后迁移；先验证，后收束。
```
