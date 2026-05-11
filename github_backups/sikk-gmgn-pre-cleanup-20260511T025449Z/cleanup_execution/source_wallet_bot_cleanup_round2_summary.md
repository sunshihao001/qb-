# SIKK-GMGN source_wallet_bot cleanup round2

## 结论

`data/source_wallet_bot/` 是**强保留目录**，不能整体清理。

本轮只做**目录内分级**，不做一刀切删除。

## 分级结果

### KEEP

- `data/source_wallet_bot/live/`
- `data/source_wallet_bot/registry/`
- `data/source_wallet_bot/schemas/`
- `data/source_wallet_bot/paper/`
- `data/source_wallet_bot/replay/`
- `data/source_wallet_bot/audit/`
- `data/source_wallet_bot/system_audit_20260508_014528/`
- `data/source_wallet_bot/_template_token/`
- `data/source_wallet_bot/backtest/`（保留占位，待确认空目录后再处理）

### REVIEW

- `data/source_wallet_bot/legacy/`
- `data/source_wallet_bot/auto_tasks/`
- `data/source_wallet_bot/ad_hoc/`

## REVIEW 的处理原则

这些目录不是删除候选，而是**内部瘦身候选**：

- 保留代表性 token / case / fixture
- 删除或隔离重复中间产物
- 删除一次性调试导出
- 保留能支撑回归、对比、验证的样本

## 特别说明

### `legacy/`

这是最大的历史桶，但仍然属于钱包结构分析资产。

处理方式：

- 保留目录
- 只缩减内部重复 run、旧临时导出、过旧副本
- 不直接整目录删除

### `auto_tasks/`

这是自动化输出区，通常会含有多轮任务产物。

处理方式：

- 保留任务结构和少量代表样本
- 清掉重复阶段产物和过旧任务批次

### `ad_hoc/`

这是临时实验区，最适合做抽样保留。

处理方式：

- 留 1-2 个代表案例
- 其余可归档或隔离

## 结论

这一步不是“删目录”，而是把 `data/source_wallet_bot/` 定义成：

- 主资产区
- 保留区
- 可抽样区
- 可缩减区

而不是普通垃圾输出区。
