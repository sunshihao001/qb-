# HER Harness 最小版本 v0

- 创建时间：2026-05-06
- 主根目录：`/root/sikk-gmgn/`
- 适用对象：HER / Hermes / SIKK-GMGN 钱包数据分析与结构分析任务
- 当前目标：先建立一个可理解、可执行、可验证、可回流的最小工作环境；后续再逐步专业化。

## 0. 一句话定义

HER Harness 不是一个功能脚本，而是 HER 能稳定工作的环境：

```text
目标可见 → 数据可找 → 目录可控 → 合约可查 → 执行可复现 → 验收可证明 → 结论可回流
```

## 1. 最小版本必须解决的问题

当前最小版本只解决 5 件事：

1. HER 知道当前系统的目标是什么。
2. HER 知道钱包事实数据和结构推断数据写到哪里。
3. HER 知道不同模块之间用哪些文件交接。
4. HER 知道什么叫完成，不是表面完成。
5. HER 做完后必须把结论写回 repo，而不是只停留在聊天里。

## 2. 单一 canonical 根目录

后续钱包数据分析 / 结构分析统一使用：

```text
/root/sikk-gmgn/
```

`/root/sikk-wallet-intel/` 只作为旧工作区、迁移参考或兼容来源；不再作为新任务主写路径。

## 3. 最小目录标准

### 3.1 钱包事实层

主写路径：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

最小必备输出：

```text
structure_analysis/wallet_fact/wallet_structure_normalized.json
structure_analysis/wallet_fact/chip_distribution_summary.json
structure_analysis/wallet_fact/same_source_groups.json
structure_analysis/wallet_fact/fund_flow_edges.csv
structure_analysis/wallet_fact/address_history.json
structure_analysis/reports/wallet_fact_report.md
manifest/token_output_manifest.json
```

职责：

- 采集 GMGN / 链上 / legacy 钱包事实。
- 标准化钱包、交易、持仓、标签、同源、资金路径。
- 只回答事实：发生了什么、谁买卖、谁持有、是否同源、是否回流、历史是否复现。
- 不推断主导侧意图。
- 不输出交易建议。

### 3.2 结构推断层

主写路径：

```text
/root/sikk-gmgn/data/intel_bot/<mode>/<token_address>/
```

最小必备输出：

```text
behavior_inference/dominant_behavior_inference.json
behavior_inference/chip_control_status.json
reports/behavior_reasoning_report.md
manifest/token_output_manifest.json
```

职责：

- 只读取钱包事实层标准输出或 handoff。
- 推断疑似吸筹、疑似控盘、疑似洗盘、疑似推进、疑似派发、疑似撤退等行为状态。
- 缺少事实文件时必须降级为 `INSUFFICIENT_DATA`。
- 不直接读取 paper、dashboard、state_machine、swap/signing/broadcast。

### 3.3 导入与旧数据

旧包、备份、外部资料先进入：

```text
/root/sikk-gmgn/imports/
```

旧路径映射、兼容规则进入：

```text
/root/sikk-gmgn/legacy_compat/
```

规则：

- 旧文件 copy-only。
- 不删除旧文件。
- 不移动旧文件。
- 不覆盖旧 runtime 输出。
- 必须写 old_path → new_path 映射。

## 4. 最小执行流程

```text
用户提出目标
  ↓
HER 判断任务类型：事实 / 推断 / 导入 / 报告 / 方法论 / 代码
  ↓
HER 查目录宪法与 routes
  ↓
HER 确认主写路径
  ↓
HER 读取或生成标准输入
  ↓
HER 分阶段输出文件
  ↓
HER 验收路径、字段、manifest、报告
  ↓
HER 把结论回流到 repo
```

## 5. 最小任务分类规则

- 新原始数据：写 `data/source_wallet_bot/<mode>/<token>/wallet_data/raw/`
- 新标准化事实：写 `data/source_wallet_bot/<mode>/<token>/wallet_data/normalized/`
- 钱包结构事实：写 `data/source_wallet_bot/<mode>/<token>/structure_analysis/wallet_fact/`
- 钱包事实报告：写 `data/source_wallet_bot/<mode>/<token>/structure_analysis/reports/`
- 行为推断：写 `data/intel_bot/<mode>/<token>/behavior_inference/`
- 推断报告：写 `data/intel_bot/<mode>/<token>/reports/`
- 人类总报告：写 `reports/<bot>/<mode>/<token>/`
- 旧包导入：写 `imports/staging/<import_id>/`
- 旧路径兼容：写 `legacy_compat/`
- 方法论 / 新理解：写 `research_loop/methodology/` 或 `docs/harness/`

## 6. 最小验收标准

每次任务完成前，HER 必须检查：

1. 是否写入 `/root/sikk-gmgn/` canonical 根目录。
2. 是否符合 `docs/system_directory_routes.json`。
3. 是否没有写入旧工作区作为主路径。
4. 是否没有越权读取 paper / swap / signing / broadcast 文件。
5. 输出文件是否存在。
6. 必需字段是否存在。
7. 缺字段是否明确写出，而不是编造。
8. 是否有 manifest 或报告记录。
9. 是否把关键结论回流到 repo 文档 / state / acceptance。

## 7. 最小回流规则

完成任务后，不能只在聊天里总结，至少写入一种 repo 产物：

- 任务计划：`research_loop/plans/`
- 验收记录：`research_loop/acceptance/`
- 状态文件：`research_loop/state/`
- 目录映射：`legacy_compat/path_maps/`
- 方法沉淀：`research_loop/methodology/`
- Harness 更新：`docs/harness/`

## 8. 当前最小版本边界

v0 不做：

- 不接真实交易。
- 不接状态机。
- 不做 paper runner。
- 不读取私钥。
- 不签名。
- 不广播。
- 不 swap。
- 不做买卖建议。
- 不自动删除旧目录。

## 9. 后续专业化方向

v1 应补齐：

- 机器可读 Harness route。
- 每个任务的 task ticket schema。
- 文件级 manifest schema。
- legacy migration hash 校验规则。
- wallet_fact → intel_bot handoff schema。
- acceptance 自动检查脚本。
- 目录越权扫描脚本。
- Agent 可观测日志：读了什么、写了什么、为什么判断。

v2 应补齐：

- 多 Bot 任务锁。
- 自动 runner。
- 失败降级策略。
- 每日目录审计。
- 数据血缘 lineage。
- schema diff。
- 回归测试。
- dashboard 只读展示。
