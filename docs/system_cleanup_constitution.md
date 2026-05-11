# SIKK-GMGN 系统清理宪法

## 0. 目的

本文件定义 `/root/sikk-gmgn` 在清理、归档、隔离、抽样保留时的长期规则。

它的目标不是删除数据，而是把项目从“堆积型历史目录”整理成“可验证、可回放、可维护”的结构系统。

## 1. 核心原则

1. 先备份，再归档/隔离，最后才考虑删除。
2. 强保留资产不得被移动、删除或改写主职责。
3. 能由 API 重新拉取的数据，不应无限堆积成历史仓库。
4. 大量重复 run、临时输出、缓存、旧快照应优先收缩。
5. 任何长期规则必须 copy-only 固化，不要直接把任务记录当作系统宪法。

## 2. 强保留资产

以下资产属于长期核心，默认保留：

- `hermes_harness/`
- `sikk_stable_trader_os/`
- `modules/`
- `contracts/`
- `schemas/`
- `tests/`
- `skills/`
- `docs/`
- `tools/`
- `scripts/`
- `research_loop/methodology/`
- `research_loop/mappings/`
- `research_loop/total_control/`
- `research_loop/acceptance/`
- `shared_handoff/`
- `task_books/`
- `audits/`
- `legacy_compat/`（仅保留兼容索引，不删除旧映射）

## 3. 钱包结构分析项目保留规则

所有“钱包结构分析 / 钱包数据采集 / Source Wallet Bot”相关项目，默认视为主资产，不应因为它们属于历史项目就被一刀切清理。

### 3.1 必须保留的主目录

- `data/source_wallet_bot/`
- `data/gmgn_candidates_live_run/`（当前兼容运行区）
- 与钱包结构分析相关的主方法论、contracts、schemas、tests、fixtures、reports 索引

### 3.2 为什么要保留

这些目录通常包含：

- 钱包事实数据
- 钱包结构标准化结果
- 角色分类与群组判断
- 结构快照
- same-source / chip / fund-flow 证据
- token 级分析项目
- 回放与回归 fixture

这些不是普通垃圾输出，而是钱包结构分析的基础资产。

### 3.3 允许缩减的内容

即使在 `data/source_wallet_bot/` 里，也只缩减以下内容：

- 重复中间产物
- 明显一次性试验目录
- 过旧且已有替代快照的副本
- 可重拉、可再生的临时导出
- 无法再服务于回归/演示/对比的冗余输出

### 3.4 不要做的事

- 不要把 `data/source_wallet_bot/` 整体当作可删历史仓库。
- 不要因为目录体积大就一刀切归档。
- 不要把钱包结构分析项目和普通缓存同等对待。
- 不要移动主目录职责到别的工作区。

## 4. 类似项目保留规则

和钱包结构分析类似的项目，只要满足以下特征，也应默认保留：

- 是结构化采集项目
- 是 token/wallet 级分析项目
- 是事实/证据/结构/回放资产
- 是后续方法论或 fixture 的来源
- 是可重复验证的分析主目录

这类目录不能因为“老”“多”“散”就直接清空。

## 5. 可归档对象

以下类型可以归档到 `/root/sikk-archive/`：

- 历史 run 输出
- 旧状态快照
- 重复 report
- 临时 dashboard 产物
- 不再参与回归的旧实验目录
- 可由 API 或脚本重建的重复中间文件

## 6. 可隔离对象

以下类型优先放 quarantine：

- `__pycache__/`
- `.pytest_cache/`
- 构建缓存
- 临时编译产物
- 一次性工具缓存

## 7. 目录治理顺序

标准顺序必须是：

1. 备份
2. 记录路径与用途
3. 归档到 `/root/sikk-archive/`
4. 隔离缓存
5. 验证
6. 最后才考虑删除

## 8. 钱包结构分析目录治理优先级

对钱包结构分析项目，优先级顺序是：

1. 保留主目录和主方法论
2. 保留少量代表性 fixture
3. 保留回归测试所需样本
4. 归档旧 run 和重复输出
5. 隔离缓存
6. 不删除核心结构资产

## 9. 与旧清洗任务的关系

`research_loop/plans/data_cleanup_20260511/` 下的文件属于本次任务记录，不是长期宪法。

长期规则应以本文件为准。

如果后续需要补充规则，应继续 copy-only 修订本文件，而不是把临时计划直接当作最终规范。
