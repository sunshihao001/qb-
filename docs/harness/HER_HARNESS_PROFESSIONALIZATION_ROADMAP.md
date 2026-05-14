# HER Harness 专业化路线图

- 创建时间：2026-05-06
- 依赖：`docs/harness/HER_HARNESS_MINIMAL_V0.md`
- 目标：先用最小版本约束 HER，再逐步靠近专业化 Agent Harness。

## 阶段 v0：最小可用 Harness

目标：不再散写文件，不再靠聊天记录承载系统事实。

必须具备：

- 单一 canonical 根目录：`/root/sikk-gmgn/`
- 钱包事实主路径：`data/source_wallet_bot/`
- 结构推断主路径：`data/intel_bot/`
- 旧包入口：`imports/`
- 旧路径兼容：`legacy_compat/`
- 最小验收：路径正确、文件存在、缺字段明确、结论回流。

验收：

- `docs/harness/HER_HARNESS_MINIMAL_V0.md` 存在。
- 新任务能先判断资产类型再写文件。
- 新输出不再主写 `/root/sikk-wallet-intel/`。

## 阶段 v1：机器可读 Harness

目标：HER 不靠口头记忆判断目录，而是读取机器规则。

新增：

```text
docs/harness/her_harness_routes.json
schemas/harness/task_ticket.schema.json
schemas/harness/file_manifest.schema.json
schemas/harness/acceptance.schema.json
```

能力：

- 输入一个任务，先生成 task ticket。
- task ticket 绑定 bot、asset_type、asset_id、mode、allowed_paths、forbidden_paths。
- 文件写入前检查 route。
- 完成后生成 acceptance record。

## 阶段 v2：执行与验收自动化

目标：减少人工口头检查，改为脚本验收。

新增：

```text
tools/harness/check_routes.py
tools/harness/check_required_outputs.py
tools/harness/check_forbidden_paths.py
tools/harness/write_acceptance_record.py
```

能力：

- 检查输出是否落在 canonical 目录。
- 检查是否越权读写旧路径。
- 检查 wallet_fact 必需文件。
- 检查 intel_bot 必需文件。
- 生成验收报告。

## 阶段 v3：可观测性与数据血缘

目标：HER 每次任务都能说明自己读了什么、写了什么、为什么这么判断。

新增：

```text
research_loop/state/<task_id>/read_set.json
research_loop/state/<task_id>/write_set.json
research_loop/state/<task_id>/decision_trace.md
research_loop/state/<task_id>/lineage.json
```

能力：

- 每次任务记录 read_set。
- 每次任务记录 write_set。
- 每个输出能追溯来源。
- 旧包迁移保留 sha256。
- 重要判断有证据链。

## 阶段 v4：多 Bot 协同 Harness

目标：让 Orchestrator / Wallet-Fact / Behavior-Inference 有固定任务锁和交接协议。

新增：

```text
orchestrator/active_task_lock.json
contracts/bot_handoff/wallet_fact_to_intel_bot.md
schemas/bot_handoff/wallet_fact_to_intel_bot.schema.json
research_loop/task_packages/pending/
research_loop/task_packages/done/
research_loop/task_packages/blocked/
```

能力：

- 一个阶段只允许一个 Bot 发言或写入。
- Wallet-Fact 只能产事实。
- Behavior-Inference 只能读事实后推断。
- Orchestrator 只汇总，不替代子模块判断。

## 阶段 v5：专业化持续运行

目标：系统能长期运行、审计、复盘，但仍保持只读/纸面边界。

新增：

```text
reports/harness/daily_directory_audit.md
reports/harness/weekly_schema_drift.md
reports/harness/legacy_compat_status.md
reports/harness/agent_failure_review.md
```

能力：

- 每日目录审计。
- schema drift 检查。
- legacy 路径逐步降级。
- 失败任务复盘。
- 技术债进入 repo。
- 新方法沉淀为 skill 或 methodology 文件。

## 专业化判断标准

一个任务只有满足以下条件，才算专业完成：

1. 任务目标写入 task ticket。
2. 输入来源可追踪。
3. 输出路径符合 routes。
4. 必需文件存在。
5. 缺字段明确标记。
6. 没有越权读写。
7. 有验收记录。
8. 关键结论回流到 repo。
9. 新经验进入 methodology / skill / docs。

## 当前推荐下一步

从 v0 进入 v1 前，先完成：

1. 确认 `/root/sikk-gmgn/` 为唯一 canonical root。
2. 把 `/root/sikk-wallet-intel/` 定义为 legacy workspace，不再主写。
3. 建立 `her_harness_routes.json`。
4. 建立最小 task ticket schema。
5. 写一个 route checker。
