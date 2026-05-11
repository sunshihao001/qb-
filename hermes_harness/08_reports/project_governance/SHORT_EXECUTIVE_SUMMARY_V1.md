# Hermes 项目体系侦察与目录治理长任务 V1 — 简短总报告

## 任务状态

已完成。

本次任务不是目录迁移，也不是代码重构，而是建立 `/root/sikk-gmgn` 的项目知识地图与目录治理基础。

## 本次实际完成了什么

已完成 0-8 阶段：

1. 启动与边界锁定
2. 只读全局侦察
3. 目录与文件分类
4. 模块注册表建立
5. 路径注册表建立
6. 旧路径映射建立
7. 冲突与混乱点审计
8. 迁移建议生成
9. 完整性验证与长期规则候选

## 关键产物

### 机器可读索引

- `hermes_harness/03_task_runtime/project_inventory/file_inventory.jsonl`
- `hermes_harness/03_task_runtime/project_inventory/directory_inventory.jsonl`
- `hermes_harness/03_task_runtime/project_inventory/module_registry.json`
- `hermes_harness/03_task_runtime/project_inventory/path_registry.json`
- `hermes_harness/03_task_runtime/project_inventory/legacy_path_map.json`
- `hermes_harness/03_task_runtime/project_inventory/code_entrypoint_index.json`
- `hermes_harness/03_task_runtime/project_inventory/dataflow_map.json`

### 人类可读报告

- `hermes_harness/08_reports/final_reports/PROJECT_SYSTEM_MAP_V1.md`
- `hermes_harness/08_reports/final_reports/DIRECTORY_GOVERNANCE_REPORT_V1.md`
- `hermes_harness/08_reports/final_reports/MIGRATION_RECOMMENDATION_V1.md`
- `hermes_harness/08_reports/project_governance/FINAL_TASK_SUMMARY_V1.md`
- `hermes_harness/08_reports/project_governance/PROJECT_GOVERNANCE_LONG_TASK_REPORT_V1.md`

### 验证产物

- `hermes_harness/06_verification/project_governance/PROJECT_GOVERNANCE_VERIFICATION_V1.md`

## 侦察结果摘要

- 文件数：`12253`
- 目录数：`1469`
- 模块数：`126`
- 代码入口数：`257`
- 旧路径候选：`164`
- 冲突 / 歧义信号：`370`

## 主要发现

1. 项目已经可以被完整索引，不需要先移动文件。
2. 项目中存在多个并行系统：`hermes_harness`、`docs`、`modules`、`research_loop`、`reports`、`data` 等。
3. 旧路径、运行输出、缓存、报告、方法轮和数据区确实存在混杂现象。
4. 当前最缺的不是迁移动作，而是稳定的 canonical path standard。
5. Hermes 后续续跑依赖：inventory、registry、checkpoint、verification，而不是靠模型记忆猜路径。

## 最终建议

当前不建议马上迁移。

推荐顺序是：

```text
先保留旧路径
→ 建立 canonical path standard
→ 明确 current path 到 recommended path 的映射
→ 人工确认高风险路径
→ 最后才执行 copy-only 或迁移
```

## 禁止事项保持有效

本次任务没有执行：

- 删除文件
- 移动旧目录
- 重命名核心文件
- 修改业务代码
- 触发交易
- 读取密钥
- git push
- git reset / git clean

## 结论

本次任务已经达成第一阶段治理目标：

```text
项目从“散乱目录状态”进入“可读取、可索引、可追踪、可继续治理”的状态。
```

下一步不应该直接搬目录，而应该制定：

- canonical path standard
- path migration matrix
- legacy keep-in-place policy
- high-risk path human review list
