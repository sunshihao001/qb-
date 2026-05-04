# ChatGPT Share 69f809c6：纸面交易优化方案 / Full Automation v1.0 吸收笔记

来源链接: https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426
标题: Branch · Branch · Branch · Branch · Branch · Branch · Branch · 纸面交易优化方案
读取状态: 已成功读取页面 HTML 与 React stream payload；不是 deleted share。

## 1. 原文核心目标

该 GPT 文档提出把 SIKK 从“多个脚本手动运行 + 数据分散 + 面板待补 + Telegram 只能广播”升级为一套全自动纸面验证系统。

原文中的系统最终形态包括：

- 自动候选发现
- 自动 K线 / 信号分析
- 自动 GMGN 钱包结构分析
- 自动 OKX Top300 集群关联分析
- 自动 quote / security 检查
- 自动状态机判断
- 自动 paper entry / monitor / exit
- 自动 Case File 数据补全
- 自动 Auto Review
- 自动 Unified Index 刷新
- 自动 Web Visual Console 刷新
- 自动 Telegram 中文交互面板刷新
- 自动风险提醒
- 自动日报 / 审计报告
- 自动失败归因
- 自动字段缺失审计
- 自动模板落地审计
- 自动 runtime health 检查

## 2. 必须保留的安全边界

原文反复强调，全自动不等于真实交易：

```text
当前全自动 = 全自动发现、分析、纸面交易、复盘、播报、审计、面板刷新
不是全自动真实交易

真实 swap / buy / sell / execute / approve / broadcast 全部禁止
```

落入当前 SIKK 时继续保持：

- 不执行真实 swap
- 不新增真实 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST
- 不读取私钥
- 不写入私钥
- 不打印 TELEGRAM_BOT_TOKEN
- 不输出 webhook_url
- 不破坏 `sikk_live_run.py`
- 不破坏 paper runner 当前纸面交易逻辑
- 不把“写了文档”当作完成
- 所有功能必须有真实输出文件
- 所有阶段必须有测试或命令验收

## 3. 与当前系统的关键冲突：不能新建并行主入口

原文提到 `sikk_full_auto_orchestrator.py` 作为 Full Automation 主控。但当前 SIKK 已经确立新的 canonical 主入口：

```text
sikk_live_run.py 单入口
→ paper JSON/CSV 同步
→ wallet daily report 使用新 CSV
→ live_state / live_board / live_dashboard
→ site/dashboard_data.json
→ site/index.html / app.js / style.css
→ safety 默认关闭真实交易
```

因此本次吸收规则是：

```text
不要新增并行主循环 sikk_full_auto_orchestrator.py。
把原文提出的 Full Automation 能力拆成 sikk_live_run.py 下游/旁路模块、审计器、adapter、builder 和 report。
```

`sikk_live_orchestrator.py` 如存在，仅作为观测、看板、token-status 或历史组件复用，不重新成为主入口。

## 4. 数据补全主线

原文指出网站大量“待补”的根因不是页面，而是数据链路未接齐：

```text
模板已经先做出来了
字段设计也有了
但数据采集层、快照层、字段映射层、回填层没有真正接上
```

建议落地为 SIKK 数据源注册与字段映射层：

- `sikk_data_source_registry.py`
- `sikk_field_source_map.py`
- `sikk_wallet_intelligence_adapter.py`
- `sikk_case_data_backfill.py`
- `sikk_case_data_completeness_auditor.py`

关键原则：

- 旧 GMGN / OKX 钱包结构系统可以作为正式上游数据源。
- 旧 AI 自然语言判断不能直接当事实字段。
- 所有字段必须带 `source_trace`。
- 历史不可还原字段必须标记 `missing_reason`。
- AI 推断字段必须标记 `AI_INFERRED` 与 `evidence_level`。
- 缺数据时显示“待补/证据缺失/数据质量不足”，不编造。

## 5. OKX Top300 Cluster 的定位

原文明确认为 OKX 前300集群关联应成为正式上游数据源：

```text
SIKK Cluster Intelligence Layer
集群关联智能层
```

它解决：

- 前300关键地址之间是否存在集群关系
- 集群是否与早期钱包、Top Holder、高结果钱包、分发接收者、接盘鲸鱼重叠
- 是否出现同集群集中买入 / 集中卖出 / 集中转移
- 当前筹码控制权在结构侧还是正在转移给对手盘

建议输出字段：

- `cluster_id`
- `cluster_size`
- `cluster_rank`
- `top300_cluster_count`
- `top300_cluster_density`
- `same_cluster_wallet_count`
- `same_cluster_buy_score`
- `same_cluster_sell_score`
- `cluster_net_flow_score`
- `cluster_distribution_score`
- `cluster_accumulation_score`
- `cluster_counterparty_pressure_score`
- `cluster_holder_overlap_score`
- `cluster_top_holder_overlap`
- `cluster_early_wallet_overlap`
- `cluster_late_whale_overlap`
- `cluster_relation_confidence`
- `cluster_risk_reason`
- `cluster_support_reason`

建议标准文件：

- `okx_top300_wallets.csv`
- `okx_cluster_groups.csv`
- `okx_cluster_edges.csv`
- `okx_cluster_decision.json`

当前项目已有 v0.4 OKX cluster layer 的部分落地记录，因此该文档应主要用于查漏补缺，而不是重做一套。

## 6. 钱包结构门禁与退出策略

原文多处强调钱包结构不能粗暴等于交易执行，应拆成三层：

```text
第一层：钱包结构信号
第二层：退出策略判断
第三层：paper runner 执行动作
```

重点修正方向：

- `WALLET_SUPPORT` 不等于买入，只能作为 paper-ready 的证据之一。
- `WALLET_BLOCK` / `WALLET_PAUSE` / `WALLET_SUPPORT` 必须进入状态机，但不能绕过 signal / quote / security。
- `FORCE_PAPER_EXIT` 只表示纸面退出或复盘，不是真实卖出。
- `STRUCTURE_WEAKENING` 不能被简单当作失败归因；需要拆成状态变化、退出触发和最终 failure attribution。
- 缺钱包数据不能直接触发 FORCE_EXIT，应先标记 `DATA_QUALITY_FAIL` 或 `EXIT_MONITOR`。

## 7. Case File 与纸面复盘补全

原文把 Case File 视为纸面交易系统的核心验收对象。每笔 paper position 应记录：

- 发现阶段
- 盘型判断
- 入场信号
- 钱包结构门禁
- quote / security
- 纸面入场
- 持仓过程
- 退出
- 策略复盘
- 策略调整建议
- 继续观察问题

Case File 必须带：

- 字段来源 `source_trace`
- 缺失字段 `evidence_missing_fields`
- 完整度评分 `case_completeness_score`
- 质量等级 `case_quality`
- 是否适合策略复盘 `strategy_review_eligible`

## 8. Visual Console / Web / TG / CLI 交互要求

原文强调网站不能只是打开，必须能回答策略问题。

Visual Console 应显示：

- Token 可点击进入详情
- Paper Lab
- Case File 入口
- Review Lab
- Alert Center
- System Health
- 字段缺失诊断
- 数据质量诊断

`dashboard_data.json` 必须包含 detail 所需字段，`index.html/app.js/style.css` 必须支持 token detail drawer 或等价详情区。

Telegram 方面，中文展示可以完整中文化，但 Telegram slash command 本身受平台限制，命令名通常需要英文/数字/下划线，中文应放在按钮、标题、面板文案中。

## 9. Harness / Superpowers 工程方法论

原文吸收了 Anthropic Harness 与 Superpowers 工作流，适合 SIKK 长任务：

- 不让执行 Agent 自己评价自己；Planner / Generator / Evaluator 分离。
- 每个阶段先写 `PHASE_CONTRACT.md`。
- 每个阶段必须有验收命令。
- 每个阶段必须有真实输出文件。
- 每个阶段必须写 `PHASE_HANDOFF.md`。
- Evaluator 必须真实点击、真实运行、真实验收。
- 没有命令输出，不允许声明完成。
- 修复失败必须写入 `FAILED_ITEMS.md`。

该方法论应作为后续 SIKK 自动化改造的工程纪律，而不是作为新增复杂模块的理由。

## 10. 当前吸收后的推荐落地顺序

基于当前 SIKK 已有状态，推荐不要重做全套，而是合并去重：

1. 建立 GPT 文档总索引与冲突矩阵。
2. 统一确认 `sikk_live_run.py` 为唯一主入口。
3. 盘点 `site/dashboard_data.json` 与页面上的“待补”字段。
4. 建立 `字段 → source_trace → 缺失原因 → 可回填源 → 展示入口` 矩阵。
5. 优先补 Case File / paper JSON/CSV / wallet daily report / dashboard_data 的数据链路。
6. 复查 OKX cluster v0.4 已落地能力与本 share 中字段要求的差距。
7. 运行主入口 smoke test，确认安全开关仍关闭真实交易。

## 11. 验收标准

吸收本 share 后，后续工程改动必须至少验证：

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_knowledge_absorption.py -q
PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none
```

安全验收重点：

- `real_swap_enabled=false`
- `broadcast_allowed=false`
- `confirmation_enabled=false` 或未开启真实确认流
- 不新增私钥读取
- 不新增真实 swap / broadcast
- 所有运行输出仍在 `data/gmgn_candidates_live_run` 下

## 12. 本文档结论

该 share 是一套较大的 Full Automation / 纸面交易优化总任务书。它的价值在于：

- 明确全自动纸面验证系统的完整闭环；
- 明确字段补全与 source_trace 纪律；
- 强化 OKX Top300 cluster 作为上游关系证据；
- 强化 Case File 与 Visual Console 的验收标准；
- 强化 Harness/Superpowers 阶段合同与独立验收方法。

但它不应覆盖当前 SIKK 的最新单入口原则。正确吸收方式是：

```text
保留认知与字段要求
收敛主入口到 sikk_live_run.py
把新增能力变成 adapter/auditor/builder/report
继续保持 paper-only/no-swap/no-private-key/no-broadcast
```
