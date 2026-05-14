# ChatGPT Share 69f809c6 文档结构索引

来源链接: https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426
标题: Branch · Branch · Branch · Branch · Branch · Branch · Branch · 纸面交易优化方案
处理方式: 按“文档驱动型自动化落地流程”进行结构识别，先不把全文简单总结为一篇 inbox note，也不直接大改代码。

## 处理纠偏说明

上一轮处理误区：只做了单篇吸收笔记 + `sikk_knowledge_absorption.py`，这会把大文档压扁成普通知识吸收，丢失“标题 → Section Task → 文件/字段/命令/验收”的方法轮。

正确方式：

```text
Share / 文档 / 需求
  ↓
标题结构识别
  ↓
每个标题生成 Section Task
  ↓
每个 Section Task 绑定代码文件 / 数据文件 / 验收命令
  ↓
逐节实现
  ↓
逐节测试
  ↓
逐节归档
  ↓
再进入下一节
```

## 已识别的主 Section

### S01：Full Automation Runtime 总任务书

来源 extract: 2
主题: `full_automation_runtime`
长度: 32548
标题: 下面是一套可直接复制到 Hermes 的完整全流程任务书。

核心标题:

- 一、系统目标架构
- 二、需要新增 / 整合的核心文件
- 三、完整 Hermes 长任务指令
- 四、部署运行命令
- 五、日常使用命令
- 六、最终判断标准

当前项目映射:

- 原文提到 `sikk_full_auto_orchestrator.py`，但当前项目主入口必须保持 `sikk_live_run.py`。
- 本节不应创建并行主循环，应改写成 `sikk_live_run.py` 单入口下的 registry / auditor / adapter / builder 任务。

优先级: P0 结构对齐，不直接实现。

### S02：OKX Top300 Cluster 正式上游数据源

来源 extract: 6
主题: `okx_top300_cluster`
长度: 20817
标题: OKX 的前 300 集群关联非常关键。

核心标题:

- OKX Top300 Cluster 在系统里的定位
- 它能补全哪些“待补”字段
- 它和 GMGN 钱包系统的区别
- OKX Top300 应该怎样进入判断逻辑
- 必须新增的模块
- OKX Top300 输出标准化
- 集群门禁如何和钱包门禁合并
- 融合判断规则

当前项目映射:

- 现有/应检查模块：`sikk_okx_cluster_holding_analyzer.py`、`sikk_okx_cluster_delta.py`、`sikk_chip_control_state_machine.py`、`sikk_system_audit.py`、`sikk_explainability_engine.py`、`sikk_dashboard_builder.py`、`sikk_live_run.py`。
- 本节应生成差距矩阵，而不是重复创建 `sikk_okx_top300_cluster_adapter.py`。

优先级: P1 字段差距审计。

### S03：旧 GMGN / OKX 钱包结构系统作为正式上游

来源 extract: 12
主题: `legacy_wallet_data_source_backfill`
长度: 22010
标题: 可以，而且应该参考你之前建立的 GMGN / OKX 钱包结构分析系统。

核心标题:

- 答案先明确：可以用，但不能直接乱用
- 缺的不是数据源，而是数据源接入标准
- SIKK 数据源注册与字段映射层
- 旧钱包系统在新交易体系的位置
- GMGN / OKX 分工
- 网站“待补”字段分类
- 字段来源统一字典
- 交易系统每个阶段必须保存快照

当前项目映射:

- 应产出 `字段 → source_trace → 缺失原因 → 可回填源 → 展示入口` 矩阵。
- 应检查 `site/dashboard_data.json` 里所有“待补”字段。
- 应映射旧 reports / wallet_structure / okx_cluster / paper_live 到 dashboard/case file。

优先级: P0，直接关系用户指出的网站“待补”。

### S04：Superpowers / Harness 5 小时系统审计方法

来源 extracts: 19, 20, 25
主题: `harness_superpowers_audit`

核心标题:

- Superpowers 方法论
- 5 小时后台执行总控
- Planner / Generator / Evaluator 分离
- 每阶段验收合同
- Evaluator 真实点击、真实运行、真实验收
- 修复失败写 FAILED_ITEMS.md

当前项目映射:

- 不应只生成长任务提示词。
- 应沉淀为 `reports/<doc_id>/PHASE_CONTRACT.md`、`PHASE_HANDOFF.md`、验收报告模板。

优先级: P2 工程纪律。

### S05：Case File 数据证据链补齐

来源 extracts: 28, 80, 81
主题: `case_file_data_completeness`

核心标题:

- Case File 外壳成型但证据链未补齐
- Paper Lifecycle Recorder
- 单笔仓位 8/12 阶段记录
- 自然语言解释模块
- 每笔仓位必须记录发现、盘型、信号、钱包、quote/security、入场、持仓、退出、复盘

当前项目映射:

- 应检查 `paper_live/case_files/*.json/md`、`site/case_files/`、`paper_positions_open/closed.csv/json`。
- 应优先确认 `field_sources`、`evidence_missing_fields`、`case_completeness_score`、`case_quality` 是否真实存在且被 dashboard 展示。

优先级: P1。

### S06：Telegram 中文专业控制台 / 三端交互

来源 extracts: 33, 51, 72
主题: `telegram_interaction_console`

核心标题:

- 中文专业控制台
- 系统总览、开放仓位、已关闭仓位、单代币详情、单仓位详情、入场证据、钱包结构、持仓过程、自动复盘、系统健康、风险提醒
- 中文 callback 命名策略
- 统一索引层
- TG / Web / CLI 一致性

当前项目映射:

- 应检查 `sikk_telegram_views.py`、`sikk_telegram_callback_index.py`、`sikk_unified_view_builder.py`、`data/gmgn_candidates_live_run/index/*.json`。
- Telegram slash command 底层保留英文/短码；中文放在按钮与面板文案。

优先级: P2。

### S07：Visual Console Pro / Token 详情点击

来源 extracts: 103, 108
主题: `visual_console_dashboard`

核心标题:

- Visual Console Pro
- 统一 Dashboard 数据模型
- Dashboard 数据构建器
- Token 点击详情 Drawer
- 筛选、排序、搜索、自动刷新
- Paper Lab 专业化
- System Health 与数据质量诊断
- 接入主流程自动刷新

当前项目映射:

- 当前静态站点为 `data/gmgn_candidates_live_run/site/index.html/app.js/style.css/dashboard_data.json`。
- 应检查 Token 详情区是否真能点击、是否读取字段、是否只显示模板“待补”。

优先级: P1。

### S08：Live Runtime v0.1 / v0.2 / v0.3 运行层设计

来源 extracts: 158, 160, 162
主题: `live_runtime_design`

核心标题:

- Runtime v0.1：候选发现接入、token_status 合并、CLI、live_board
- Runtime v0.2：module_runner、trace_logger、skip_policy、dashboard、notifier
- Runtime v0.3：模块 CLI 参数统一、输出新鲜度、open position 优先处理、confirmation ticket

当前项目映射:

- 当前 canonical 主入口是 `sikk_live_run.py`。
- `sikk_live_orchestrator.py` 只作为观测/看板/token-status 组件复用。
- 本节只用于审计当前运行层缺口，不重启旧 runtime 设计。

优先级: P2。

### S09：钱包结构门禁 v1.0 / 同源组 / 分数 / delta / failure attribution

来源 extracts: 167, 169, 171, 179
主题: `wallet_structure_gate`

核心标题:

- same_source_group_id 生成
- sync_buy_score / sync_sell_score
- counterparty_pressure_score
- 多轮快照 delta
- failure attribution
- 8 类钱包角色
- wallet_structure_score / wallet_risk_score / data_quality_score
- 门禁最终决策规则

当前项目映射:

- 现有记忆显示这些能力已部分进入 SIKK 下一阶段设计。
- 应检查 `sikk_wallet_structure_gate.py`、`sikk_candidate_wallet_structure_pipeline.py`、`sikk_same_source_grouping.py`、`sikk_wallet_structure_snapshot.py`、`sikk_wallet_structure_daily_report.py` 等是否实现并进入主入口。

优先级: P1/P2，视当前字段缺口决定。

## 下一步应该生成的 Section Task

按照正确方法，下一步不应直接全量实现，而应先生成任务文件：

```text
tasks/chatgpt_share_69f809c6/S01_full_automation_runtime_task.md
tasks/chatgpt_share_69f809c6/S02_okx_top300_cluster_task.md
tasks/chatgpt_share_69f809c6/S03_legacy_wallet_data_source_backfill_task.md
tasks/chatgpt_share_69f809c6/S04_harness_superpowers_audit_task.md
tasks/chatgpt_share_69f809c6/S05_case_file_data_completeness_task.md
tasks/chatgpt_share_69f809c6/S06_telegram_interaction_console_task.md
tasks/chatgpt_share_69f809c6/S07_visual_console_dashboard_task.md
tasks/chatgpt_share_69f809c6/S08_live_runtime_design_task.md
tasks/chatgpt_share_69f809c6/S09_wallet_structure_gate_task.md
```

每个 task 必须包含：

- 本节目标
- 涉及模块
- 需要读取的文件
- 允许修改的文件
- 禁止修改的文件
- 新增字段
- 输出文件
- 验收命令
- 测试命令
- 完成标准
- 风险边界

## 当前最高优先级建议

先做 S03 + S07 的可运行闭环：

```text
网站“待补”字段盘点
→ 字段来源矩阵
→ 可回填/不可回填分类
→ dashboard_data.json 样例验证
→ Visual Console 抽样检查
→ 验收报告
```

这是最贴合用户当前问题的路线。
