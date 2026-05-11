# SIKK-SOL HER 核心自动化工作流计划

- 输出目录：`data/gmgn_candidates_live_run`
- 核心认知：目标自治 + 工具选择自治 + 阶段执行自治 + 验收自治，但必须受 paper-only 与测试验收护栏约束。
- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。

## 任务棱镜阶段
- 读取与证据保存：存在 inbox 原文；报告中不假装读取。
- 问题识别与隐藏断点：输出缺口清单与约束报告。
- 系统映射审计：每个结论绑定文件、字段、命令或测试。
- 分阶段实现：测试通过且产物可追溯。
- 审计验收与沉淀：验收报告说明完成项、未完成项、风险、下一步。

## 工具路由
- GPT/ChatGPT 分享链接：conversation-transcript-ingestion / sikk_knowledge_absorption.py / Section Task 合同
- 复杂代码/架构审计：Super Hermes prism-scan/prism-3way/prism-reflect / systematic-debugging / requesting-code-review
- 跨模型代码库上下文包：repomix / secretlint/安全排除 / 限定 include/exclude 范围
- 多小时研究/多代理任务：DeerFlow / delegate_task 子代理 / 阶段验收报告
- SIKK 运行落地：sikk_live_run.py 单入口 / sikk_query/sikkctl / Telegram 中文视图 / 静态 dashboard

## 调度节奏
- 候选发现 + K线信号 + 状态机 + quote/security + 纸面更新：每 10 分钟
  - 命令：`PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01`
- 纸面持仓刷新：每 3 分钟
  - 命令：`PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01`
- 日报 + 钱包结构日报 + 静态控制台刷新：cron `0 0 * * *`
  - 命令：`PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01`

## 门禁
- PAPER_READY 才能进入纸面候选
- quote/security 为 BLOCK_BUY 时必须阻断
- PAUSE_NEED_CONFIRM 只暂停，不纸面入场
- 同一 token 只允许一个开放纸面仓位
- 钱包结构强风险默认 EXIT_MONITOR；多轮 delta + 盘型/市场确认后才 FORCE_PAPER_EXIT

## 验收命令
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01`
- `检查 live_run_manifest.json 中 real_swap_enabled=false 且 confirmation_enabled=false`
- `检查 paper_daily_report 中包含 不执行真实 swap`
